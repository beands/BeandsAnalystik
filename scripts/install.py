#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BeandsAnalystik — install.py
Универсальный installer skill-набора для Hermes Agent и OpenClaw.

Usage:
    python install.py --target hermes
    python install.py --target openclaw
    python install.py --target both
    python install.py --target hermes --global
    python install.py --target hermes --workspace /path/to/workspace
    python install.py --target hermes --update
    python install.py --target hermes --uninstall
    python install.py --target hermes --dry-run
    python install.py --target hermes --verify

Возможности:
  1. определяет ОС
  2. находит Hermes / OpenClaw (через env/known paths/filesystem fallback)
  3. проверяет Python и зависимости exporter
  4. устанавливает skill (копирует файлы)
  5. создаёт backup предыдущей версии
  6. устанавливает зависимости exporter (опционально)
  7. проверяет структуру skill
  8. выводит понятный результат

НИКОГДА не удаляет существующие skills пользователя — только BeandsAnalystik (при --uninstall).
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import sys
from pathlib import Path


# -----------------------------------------------------------------------------
# Константы
# -----------------------------------------------------------------------------

SKILL_NAME = "BeandsAnalystik"

# Файлы/каталоги, входящие в skill (копируются как есть)
SKILL_ENTRIES = [
    "SKILL.md",
    "README.md",
    "SOURCE_NOTICE.md",
    "requirements.txt",
    "references",
    "templates",
    "scripts",
]

REQUIRED_SKILL_FILES = [
    "SKILL.md",
    "references/agents/product-owner.md",
    "references/agents/business-analyst.md",
    "references/agents/system-analyst.md",
    "references/agents/security-reviewer.md",
    "references/workflows/router.md",
    "references/workflows/interview.md",
    "references/workflows/full-analysis.md",
    "references/workflows/quality-gates.md",
    "templates/project-context.md",
    "templates/final-report.md",
    "scripts/install.py",
    "scripts/export_report.py",
]


# -----------------------------------------------------------------------------
# Утилиты
# -----------------------------------------------------------------------------

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    CYAN = "\033[36m"


def info(msg: str):
    print(f"{Colors.CYAN}[i]{Colors.RESET} {msg}")


def ok(msg: str):
    print(f"{Colors.GREEN}[+]{Colors.RESET} {msg}")


def warn(msg: str):
    print(f"{Colors.YELLOW}[!]{Colors.RESET} {msg}")


def err(msg: str):
    print(f"{Colors.RED}[x]{Colors.RESET} {msg}", file=sys.stderr)


def detect_os() -> str:
    system = platform.system().lower()
    if system.startswith("win"):
        return "windows"
    if system == "darwin":
        return "macos"
    return "linux"


# -----------------------------------------------------------------------------
# Поиск корня skill (откуда запускать установку)
# -----------------------------------------------------------------------------

def find_skill_root() -> Path:
    """SKILL.md находится на 2 уровня выше этого скрипта (skill_root/scripts/install.py)."""
    here = Path(__file__).resolve().parent
    candidate = here.parent
    if (candidate / "SKILL.md").exists():
        return candidate
    # fallback: текущий рабочий каталог
    if (Path.cwd() / "SKILL.md").exists():
        return Path.cwd()
    err("Не удалось определить корень skill (нет SKILL.md рядом со скриптом).")
    err("Запускайте из каталога skill: python scripts/install.py ...")
    sys.exit(1)


# -----------------------------------------------------------------------------
# Определение целевых путей Hermes / OpenClaw
# -----------------------------------------------------------------------------

def home() -> Path:
    return Path(os.path.expanduser("~"))


def hermes_skills_paths(global_scope: bool, workspace: str | None) -> list[Path]:
    """
    Кандидаты путей установки skills для Hermes.
    Глобально: профиль пользователя (skills/).
    Workspace: <workspace>/.hermes/skills/ или <workspace>/skills/.
    """
    candidates = []
    h = home()
    os_name = detect_os()

    # Глобальные типичные расположения
    if global_scope or workspace is None:
        if os_name == "windows":
            candidates.append(h / "AppData" / "Roaming" / "Hermes" / "skills")
            candidates.append(h / ".hermes" / "skills")
        elif os_name == "macos":
            candidates.append(h / "Library" / "Application Support" / "Hermes" / "skills")
            candidates.append(h / ".hermes" / "skills")
        else:
            candidates.append(h / ".config" / "hermes" / "skills")
            candidates.append(h / ".hermes" / "skills")

    if workspace:
        ws = Path(workspace).expanduser().resolve()
        candidates.append(ws / ".hermes" / "skills")
        candidates.append(ws / "skills")

    return candidates


def openclaw_skills_paths(global_scope: bool, workspace: str | None) -> list[Path]:
    """Кандидаты путей установки skills для OpenClaw."""
    candidates = []
    h = home()
    os_name = detect_os()

    if global_scope or workspace is None:
        if os_name == "windows":
            candidates.append(h / "AppData" / "Roaming" / "OpenClaw" / "skills")
            candidates.append(h / ".openclaw" / "skills")
        elif os_name == "macos":
            candidates.append(h / "Library" / "Application Support" / "OpenClaw" / "skills")
            candidates.append(h / ".openclaw" / "skills")
        else:
            candidates.append(h / ".config" / "openclaw" / "skills")
            candidates.append(h / ".openclaw" / "skills")

    if workspace:
        ws = Path(workspace).expanduser().resolve()
        candidates.append(ws / ".openclaw" / "skills")
        candidates.append(ws / "skills")

    return candidates


def resolve_target_dir(target_name: str, global_scope: bool, workspace: str | None) -> Path:
    """Выбрать первый существующий/создаваемый каталог из кандидатов."""
    # При одновременной workspace-установке Hermes и OpenClaw нельзя
    # использовать общий fallback <workspace>/skills: второй target увидит
    # установку первого как конфликт. Разводим платформы по их явным путям.
    if workspace:
        ws = Path(workspace).expanduser().resolve()
        platform_dir = ".hermes" if target_name == "hermes" else ".openclaw"
        return ws / platform_dir / "skills" / SKILL_NAME
    if target_name == "hermes":
        candidates = hermes_skills_paths(global_scope, workspace)
    elif target_name == "openclaw":
        candidates = openclaw_skills_paths(global_scope, workspace)
    else:
        err(f"Неизвестный target: {target_name}")
        sys.exit(1)

    # предпочитаем уже существующий родительский каталог skills/
    for c in candidates:
        if c.parent.exists():
            return c / SKILL_NAME
    # иначе — первый кандидат (создадим)
    if candidates:
        return candidates[0] / SKILL_NAME
    err(f"Не удалось определить целевой путь для {target_name}.")
    sys.exit(1)


# -----------------------------------------------------------------------------
# Проверка окружения
# -----------------------------------------------------------------------------

def check_python():
    v = sys.version_info
    if v < (3, 8):
        warn(f"Python {v.major}.{v.minor} — рекомендуется >= 3.8. Продолжаем, но без гарантий.")
    else:
        ok(f"Python {v.major}.{v.minor}.{v.micro} — подходит.")


def check_exporter_deps(dry_run: bool):
    """Мягко проверить наличие зависимостей export_report.py."""
    missing = []
    for modname, pip in [("markdown", "markdown"), ("docx", "python-docx")]:
        try:
            __import__(modname)
        except ImportError:
            missing.append(pip)
    # PDF-движки. ReportLab используется встроенным fallback экспортёра и
    # работает на Windows без нативных библиотек GTK/Pango.
    pdf_present = False
    for modname in ("weasyprint", "reportlab", "xhtml2pdf"):
        try:
            __import__(modname)
            pdf_present = True
            break
        except (ImportError, OSError):
            pass
    if missing:
        msg = "Отсутствуют зависимости exporter: " + ", ".join(missing)
        if dry_run:
            warn(msg + " (dry-run: установка пропущена)")
        else:
            warn(msg)
            warn("Установите позже: pip install -r requirements.txt")
    else:
        ok("Зависимости exporter (markdown, python-docx) — на месте.")
    if pdf_present:
        ok("PDF-движок доступен.")
    else:
        warn("PDF-движок не найден (reportlab/weasyprint/xhtml2pdf). Экспорт в PDF будет недоступен "
             "до установки: pip install reportlab")


# -----------------------------------------------------------------------------
# Установка
# -----------------------------------------------------------------------------

def do_backup(target_dir: Path):
    if not target_dir.exists():
        return None
    backup = target_dir.with_name(target_dir.name + ".bak")
    if backup.exists():
        shutil.rmtree(backup)
    shutil.move(str(target_dir), str(backup))
    return backup


def copy_skill(skill_root: Path, target_dir: Path):
    target_dir.mkdir(parents=True, exist_ok=True)
    for entry in SKILL_ENTRIES:
        src = skill_root / entry
        if not src.exists():
            warn(f"Элемент skill отсутствует и будет пропущен: {entry}")
            continue
        dst = target_dir / entry
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)


def install_target(target_name: str, skill_root: Path, global_scope: bool,
                   workspace: str | None, dry_run: bool, update: bool) -> bool:
    target_dir = resolve_target_dir(target_name, global_scope, workspace)
    info(f"Целевой каталог {target_name}: {target_dir}")

    if dry_run:
        ok(f"[dry-run] skill '{SKILL_NAME}' был бы установлен в: {target_dir}")
        verify_structure(target_dir if target_dir.exists() else skill_root)
        return True

    # backup если уже установлено
    if target_dir.exists():
        if update:
            backup = do_backup(target_dir)
            if backup:
                ok(f"Создан backup предыдущей версии: {backup}")
        else:
            err(f"Skill уже установлен в {target_dir}. Используйте --update для обновления.")
            return False

    copy_skill(skill_root, target_dir)
    ok(f"Skill '{SKILL_NAME}' установлен в: {target_dir}")

    verify_structure(target_dir)
    return True


# -----------------------------------------------------------------------------
# Удаление
# -----------------------------------------------------------------------------

def uninstall_target(target_name: str, global_scope: bool, workspace: str | None,
                     dry_run: bool) -> bool:
    target_dir = resolve_target_dir(target_name, global_scope, workspace)
    if not target_dir.exists():
        warn(f"Skill не найден в {target_dir} — нечего удалять.")
        return False
    if dry_run:
        ok(f"[dry-run] каталог {target_dir} был бы удалён.")
        return True
    backup = do_backup(target_dir)
    ok(f"Skill удалён. Backup сохранён: {backup}")
    return True


# -----------------------------------------------------------------------------
# Проверка структуры
# -----------------------------------------------------------------------------

def verify_structure(skill_root: Path) -> bool:
    info(f"Проверка структуры skill: {skill_root}")
    all_ok = True
    for rel in REQUIRED_SKILL_FILES:
        p = skill_root / rel
        if p.exists():
            ok(f"  найден: {rel}")
        else:
            err(f"  ОТСУТСТВУЕТ: {rel}")
            all_ok = False
    # проверка SKILL.md frontmatter
    skill_md = skill_root / "SKILL.md"
    if skill_md.exists():
        text = skill_md.read_text(encoding="utf-8")
        if text.lstrip().startswith("---") and "name:" in text[:500]:
            ok("  SKILL.md имеет frontmatter с 'name:'.")
        else:
            warn("  SKILL.md: frontmatter с 'name:' не найден в первых 500 байтах.")
    return all_ok


# -----------------------------------------------------------------------------
# Главный entry point
# -----------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="install.py",
        description=f"Универсальный installer skill-набора '{SKILL_NAME}' для Hermes/OpenClaw.",
    )
    parser.add_argument("--target", choices=["hermes", "openclaw", "both"], default="both",
                        help="Целевая платформа (по умолчанию: both)")
    parser.add_argument("--global", dest="global_scope", action="store_true",
                        help="Установить в глобальный профиль пользователя")
    parser.add_argument("--workspace", default=None,
                        help="Путь к workspace для workspace-установки")
    parser.add_argument("--update", action="store_true",
                        help="Обновить существующую установку (с backup)")
    parser.add_argument("--uninstall", action="store_true",
                        help="Удалить skill (с backup)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Показать, что было бы сделано, без реальных изменений")
    parser.add_argument("--verify", action="store_true",
                        help="Только проверить структуру skill и окружение")
    args = parser.parse_args(argv)

    info(f"ОС: {detect_os()} | Python: {sys.version.split()[0]}")
    check_python()

    skill_root = find_skill_root()
    info(f"Корень skill: {skill_root}")

    if args.verify:
        ok("Режим проверки (--verify).")
        check_exporter_deps(dry_run=True)
        sys.exit(0 if verify_structure(skill_root) else 1)

    if args.dry_run:
        warn("Режим dry-run: реальные изменения файловой системы НЕ выполняются.")

    check_exporter_deps(args.dry_run)

    targets = ["hermes", "openclaw"] if args.target == "both" else [args.target]
    results = []

    for t in targets:
        info(f"=== Цель: {t} ===")
        if args.uninstall:
            r = uninstall_target(t, args.global_scope, args.workspace, args.dry_run)
        else:
            r = install_target(t, skill_root, args.global_scope, args.workspace,
                               args.dry_run, args.update)
        results.append((t, r))

    print()
    print("=" * 50)
    ok("Сводка:")
    for t, r in results:
        mark = f"{Colors.GREEN}OK{Colors.RESET}" if r else f"{Colors.RED}FAIL{Colors.RESET}"
        print(f"  {t}: {mark}")

    if not args.dry_run and not args.uninstall:
        print()
        info("Дальнейшие шаги:")
        print("  1. Перезапустите Hermes/OpenClaw, чтобы skill подхватился.")
        print("  2. Установите зависимости exporter (если ещё не):")
        print("     pip install -r requirements.txt")
        print("  3. Для экспорта отчёта:")
        print("     python scripts/export_report.py reports/final_report.md --format both")

    return 0 if all(r for _, r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
