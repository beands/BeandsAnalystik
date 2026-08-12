# GitHub Readiness Report

## Status

**READY WITH WARNINGS**

Техническая часть skill проверена и подготовлена. Единственное блокирующее для полностью открытой публикации предупреждение - неурегулированный правовой статус производных материалов из OpenCode.

## Skill verification

Проверены `SKILL.md`, references, roles, workflows, adaptive interview, структура, installer и exporter. Полный перечень тестов приведён в [verification-report.md](verification-report.md).

## Tests

- `py -m unittest discover -s tests -v`: PASS, 5 тестов.
- `py scripts/install.py --verify`: PASS.
- `py scripts/install.py --target both --workspace <temp> --dry-run`: PASS.
- Реальная установка для Hermes и OpenClaw в изолированный workspace: PASS.
- Экспорт `examples/sample-report.md` в PDF и DOCX: PASS.
- Проверка PDF: кириллица, заголовки и таблицы присутствуют.
- Ошибка отсутствующего входного файла экспортёра: корректный code 1 и сообщение `ERROR:`.

## Fixed issues

- Исправлен PDF с потерянной кириллицей.
- Исправлен рендер и перенос строк таблиц в PDF.
- Исправлена обработка нерабочего WeasyPrint в Windows.
- Исправлена коллизия Hermes/OpenClaw при `--target both --workspace`.
- Добавлены smoke-тесты и пример отчёта.

## Repository structure

```text
.
├── SKILL.md
├── README.md
├── SOURCE_NOTICE.md
├── requirements.txt
├── references/
├── templates/
├── scripts/
├── examples/
├── tests/
└── reports/
```

## Security / secrets check

Проведён поиск по текстовым файлам на распространённые маркеры API-ключей, токенов, private keys и credentials. Секреты не обнаружены. В `.gitignore` добавлены правила для `.env`, ключей, credentials и локальных конфигураций.

## .gitignore

Исключаются: virtual environments, Python cache, `.env`, ключи и credentials, IDE/OS-файлы, runtime exports, временные файлы, логи, DB dumps и `node_modules`.

## Files planned for Git

- Исходники skill: `SKILL.md`, `references/`, `templates/`.
- Документация: `README.md`, `SOURCE_NOTICE.md`.
- Скрипты: `scripts/install.py`, `scripts/export_report.py`.
- Тесты и пример: `tests/test_smoke.py`, `examples/sample-report.md`.
- Проверочные отчёты: `reports/verification-report.md`, `reports/github-readiness-report.md`.
- Конфигурация: `.gitignore`, `requirements.txt`.

Перед финальной проверкой локальный Git-репозиторий был инициализирован, и в индекс помещены 37 необходимых текстовых файлов. Подозрительных файлов, бинарных artefact-ов и файлов более 1 MB в списке нет.

## Excluded files

- Сгенерированные PDF/DOCX и тестовые exports.
- Персональный бизнес-отчёт, project context и временные рабочие отчёты.
- `tmp/`, `__pycache__/`, `.env`, редакторские и системные файлы.

## README

README создан и включает: назначение, возможности, Hermes/OpenClaw, структуру, установку, быстрый старт, пример запроса, PDF/DOCX, обновление, удаление, требования, ограничения, troubleshooting, acknowledgements и статус лицензии.

## Recommended GitHub description

Portable AI-agent skill for product, business, system and security analysis with adaptive interviews and PDF/DOCX reports.

## Recommended topics

- `agent-skills`
- `ai-agent`
- `business-analysis`
- `system-analysis`
- `requirements-engineering`
- `product-management`
- `openapi`
- `openclaw`
- `hermes-agent`

## Remaining warnings

1. В OpenCode, указанном как источник части переработанных материалов, на дату проверки не была обнаружена явная лицензия. До получения разрешения автора не публикуйте производные `references/agents/` и `references/skills/` как открытый репозиторий под собственной лицензией.
2. WeasyPrint в Windows требует внешние нативные библиотеки; встроенный ReportLab fallback протестирован и является рабочим вариантом.
