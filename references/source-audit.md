# Аудит исходного репозитория

**Источник:** `https://github.com/CrazyElephantX/OpenCode.git`
**Автор оригинала:** CrazyElephantX
**Назначение оригинала:** набор агентов и skills для OpenCode (системный/бизнес-/продуктовый аналитик + security review).
**Назначение переработки:** переносимый Agent Skill Suite для Hermes Agent и OpenClaw.

В этом документе каждый исходный файл отображён на его новую роль в `BeandsAnalystik`. Подробное лицензионное примечание — в `../SOURCE_NOTICE.md`.

---

## Конфигурация и метаданные

| Исходный файл | Назначение | Используемые данные | Новая роль в Hermes/OpenClaw | Изменения |
|---|---|---|---|---|
| `opencode.jsonc` | Конфиг OpenCode: default_agent, model, разрешения edit/bash и белый список skills | Модель маршрутизации, философия разрешений (read allow, edit/bash ask, skills allow) | Перенесена в `SKILL.md` (раздел «Маршрутизация») и `workflows/router.md` | Убраны `$schema` OpenCode и `default_agent`; модель заменена на платформонезависимую |
| `readme.md` | README с таблицей агентов/skills и ссылками на видео | Таблицы соответствий, список команд OpenCode | Переработан в корневой `README.md` | Убраны ссылки на установку OpenCode; добавлены Hermes/OpenClaw |

---

## Агенты (4 файла)

| Исходный файл | Назначение | Используемые данные | Новая роль | Изменения |
|---|---|---|---|---|
| `agents/product-owner.md` | Роль PO: видение, US, AC, приоритизация, бизнес-кейс, роадмап, stakeholders | Фреймворки JTBD/Kano/OST, RICE/WSJF/MoSCoW, INVEST, метрики AARRR/OKR/North Star | `references/agents/product-owner.md` | Убран frontmatter OpenCode (mode/temperature/permission); убраны ссылки на `.roo/rules-*`; оставлены принципы и формат ответов |
| `agents/business-analyst.md` | Роль BA: AS-IS/TO-BE, BPMN, BRD, Use Case, Gap, traceability | BABOK, BPMN 2.0, шаблон BRS (с AC-кодом Story-N, Gherkin Given/When/Then), таблицы NFR/прав доступа | `references/agents/business-analyst.md` | Перенесён шаблон BRS; убраны ссылки на `system-analyst`/`product-owner` как агентов OpenCode |
| `agents/system-analyst.md` | Роль SA: backend logic, ERD, Sequence, OpenAPI, AsyncAPI, NFR | Принципы качества, KPI артефактов, форматы имён файлов, отчёты качества | `references/agents/system-analyst.md` | Убраны пути `.roo/rules-{mode-slug}/01_Backend Logic.md` и т.п. — заменены на ссылки на `references/skills/*` |
| `agents/security-reviewer.md` | Роль security: проверка по 6 столпам ИБ, STRIDE/PASTA/DREAD/MITRE, ISO/NIST/OWASP/152-ФЗ | Методология review, формат отчёта | `references/agents/security-reviewer.md` | Зафиксирован **строгий read-only**; убран frontmatter OpenCode |

---

## Skills (13 файлов)

| Исходный skill | Назначение | Используемые данные | Новый файл | Изменения |
|---|---|---|---|---|
| `skills/user-story/SKILL.md` | User Story по INVEST + AC в Gherkin | Формат «Как/Я хочу/Чтобы», INVEST, Gherkin, чек-лист | `references/skills/user-story.md` | Минимальные: убран frontmatter OpenCode, добавлены идентификаторы US-XXX |
| `skills/backlog-prioritization/SKILL.md` | RICE/WSJF/MoSCoW/Value-Effort | Формулы, шкала Fibonacci, правила выбора метода | `references/skills/backlog-prioritization.md` | Переработан без потерь; добавлены идентификаторы приоритетов |
| `skills/business-case/SKILL.md` | Бизнес-кейс: ROI/TCO/Payback | Формулы ROI/TCO/Payback, шаблон, чек-лист | `references/skills/business-case.md` | Сохранён полностью; добавлены идентификаторы GOAL-* |
| `skills/business-process-bpmn/SKILL.md` | BPMN AS-IS/TO-BE | Элементы BPMN, Mermaid flowchart, Gap-анализ | `references/skills/business-process-bpmn.md` | Сохранён; убраны специфичные финтех-примеры как единственные |
| `skills/stakeholder-map/SKILL.md` | Power-Interest + RACI | Матрицы, правила RACI, чек-лист | `references/skills/stakeholder-map.md` | Сохранён |
| `skills/product-roadmap/SKILL.md` | Now/Next/Later + Theme-based | Шаблоны роадмапа, правила | `references/skills/product-roadmap.md` | Сохранён |
| `skills/backend-logic/SKILL.md` | Спецификация backend-логики (8 блоков) | Структура 8 блоков, метрики, валидации, 2 примера | `references/skills/backend-logic.md` | Сохранён полностью (~500 строк); убраны пути `.roo` |
| `skills/erd-model/SKILL.md` | ERD в PlantUML + SQL | Синтаксис PlantUML, типы связей, соответствие ERD↔SQL, примеры | `references/skills/erd-model.md` | Сохранён полностью; добавлены идентификаторы DATA-* |
| `skills/sequence-diagram/SKILL.md` | Sequence в PlantUML | autonumber, участники, этапы, протоколы, alt/opt/loop | `references/skills/sequence-diagram.md` | Сохранён |
| `skills/openapi-spec/SKILL.md` | OpenAPI 3.0 | Структура YAML, components, коды статусов, полный пример | `references/skills/openapi-spec.md` | Сохранён; добавлены идентификаторы API-* |
| `skills/asyncapi-spec/SKILL.md` | AsyncAPI 2.6 для Kafka | Шаблон YAML, 9 блоков, метрики, 2 примера | `references/skills/asyncapi-spec.md` | Сохранён полностью (~900 строк) — самый объёмный skill |
| `skills/nfr-requirements/SKILL.md` | NFR (8 категорий) | Шаблоны по категориям, метрики, инструменты, примеры | `references/skills/nfr-requirements.md` | Сохранён; добавлены идентификаторы NFR-XXX |
| `skills/security-review-checklist/SKILL.md` | Security review | 6 столпов ИБ, STRIDE/OWASP/ISO/NIST, шаблон отчёта | `references/skills/security-review-checklist.md` | Сохранён полностью (~600 строк); связан с security-reviewer |

---

## Новые материалы (отсутствуют в источнике)

Эти файлы созданы с нуля для закрытия пробелов исходного репозитория и требований ТЗ:

| Новый файл | Назначение | Происхождение |
|---|---|---|
| `SKILL.md` (главный) | Оркестратор, маршрутизация, progressive disclosure | Новый: объединяет логику `opencode.jsonc` + best practices |
| `references/workflows/router.md` | Правила выбора роли/артефакта | Новый |
| `references/workflows/interview.md` | 8-этапный adaptive-опрос пользователя | Новый (раздел #5 ТЗ) |
| `references/workflows/full-analysis.md` | Сквозной пайплайн USER→…→REPORT | Новый (раздел #4 ТЗ) |
| `references/workflows/quality-gates.md` | Чек-листы согласованности артефактов | Новый (раздел #12 ТЗ); расширяет локальные чек-листы skills |
| `templates/project-context.md` | Шаблон собираемого контекста | Новый (раздел #6 ТЗ) |
| `templates/final-report.md` | 24-секционный отчёт | Новый (раздел #8 ТЗ) |
| `templates/report-config.json` | Настройки экспорта | Новый (раздел #9 ТЗ) |
| `scripts/install.py` | Универсальный installer для Hermes/OpenClaw | Новый (раздел #10 ТЗ) |
| `scripts/export_report.py` | Экспорт md→PDF/DOCX | Новый (раздел #9 ТЗ) |
| `SOURCE_NOTICE.md` | Атрибуция и лицензионная оговорка | Новый (раздел #2 ТЗ) |
| `requirements.txt` | Зависимости Python для exporter | Новый |

---

## Принципы переработки

1. **Методология сохранена полностью** — все формулы (RICE, WSJF, ROI, TCO), шаблоны (BRS, NFR, AsyncAPI), чек-листы и методологии (INVEST, Gherkin, STRIDE, OWASP Top 10) перенесены без сокращений.
2. **Убрана привязка к OpenCode** — `.roo/rules-{mode-slug}/`, `opencode.jsonc`, frontmatter `mode: primary`/`subagent`, ссылки на агентов по имени как на процессы OpenCode.
3. **Добавлена трассируемость** — идентификаторы `GOAL-*`, `BR-*`, `FR-*`, `US-*`, `AC-*`, `NFR-*`, `API-*`, `DATA-*`, `SEC-*` (раздел #7 ТЗ), отсутствовавшие в оригинале как единая система.
4. **Оркестрация и adaptive-опрос** — новая функциональность, которой не было в оригинале (оригинал — набор независимых агентов/skills без сквозного пайплайна).
5. **Тексты переработаны своими словами** — см. `SOURCE_NOTICE.md` для деталей атрибуции.
