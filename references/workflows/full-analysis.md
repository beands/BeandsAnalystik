# Workflow: Полный анализ проекта

Сквозной пайплайн от идеи до единого отчёта. Запускается, когда пользователь просит
«спроектируй/проанализируй …» без указания конкретного артефакта.

```
1. INTAKE        — разведка файлов + адаптивный опрос
2. PO            — User Story, AC, приоритизация, бизнес-кейс, roadmap, stakeholders
3. BA            — BPMN AS-IS/TO-BE, BRD, Use Cases, Gap, traceability
4. SA            — Backend Logic, ERD+SQL, Sequence, OpenAPI, AsyncAPI, NFR
5. SECURITY      — read-only review всех артефактов
6. QUALITY GATE  — проверка связности и полноты
7. FINAL REPORT  — компиляция из артефактов + экспорт
```

**Общие правила для каждого шага:**
- Создавай артефакты в папке `reports/` проекта пользователя.
- Каждый артефакт — отдельный файл с правильным расширением (см. `router.md`).
- После создания каждого артефакта прогоняй его чек-лист из соответствующего skill.
- Передавай результаты между ролями: вход следующего артефакта = выход предыдущего.
- Не придумывай данные; недостающее помечай `[ТРЕБУЕТСЯ: ...]` и фиксируй в `project-context.md`.

---

## Шаг 1. INTAKE (разведка + опрос)

1. **Разведка проекта.** Прочитай файлы проекта: README, манифесты зависимостей
   (`package.json`, `pom.xml`, `requirements.txt`, `go.mod`), конфиги, существующие
   документы, схемы БД, API-спецификации. Извлеки факты (стек, сущности, эндпоинты).
2. **Адаптивный опрос.** Запусти `workflows/interview.md`. Пройди этапы 1–8, пока не
   достигнешь ~70–80% контекста или пользователь не скажет «достаточно».
3. **Создай/обнови** `reports/project-context.md` (шаблон `templates/project-context.md`).
4. **Определи scope артефактов** на основе контекста (не все 13 skills могут быть нужны —
   например, без Kafka не нужен AsyncAPI; без PII — упрощённый security).

**Выход:** `reports/project-context.md` с заполненными разделами и списком открытых вопросов.

---

## Шаг 2. PRODUCT OWNER

Загрузи `references/agents/product-owner.md` и нужные skills.

Минимальный набор артефактов PO:
1. **User Stories + AC** (`skills/user-story.md`) — формат INVEST, AC в Gherkin.
   Идентификаторы `US-*`, `AC-<код Story>-<номер>`.
2. **Приоритизация backlog** (`skills/backlog-prioritization.md`) — RICE и/или WSJF + MoSCoW.
3. **Stakeholder map + RACI** (`skills/stakeholder-map.md`) — если есть несколько сторон.
4. **Business case** (`skills/business-case.md`) — ROI/TCO/Payback, **только если**
   пользователь дал финансовые вводные; иначе пометить `NEED USER INPUT`.
5. **Roadmap** (`skills/product-roadmap.md`) — Now/Next/Later.

**Передача дальше:** US + AC — основа для BA (сценарии) и SA (функции).

---

## Шаг 3. BUSINESS ANALYST

Загрузи `references/agents/business-analyst.md` и `skills/business-process-bpmn.md`.

Минимальный набор BA:
1. **BPMN AS-IS** — текущий процесс (если система уже работает или есть ручной процесс).
2. **BPMN TO-BE** — целевой процесс.
3. **Gap-анализ** — что меняется и зачем (с количественной оценкой, где возможно).
4. **BRD / BRS** — бизнес-требования по шаблону из агента BA (с глоссарием, AC в Gherkin,
   NFR-разделом-заголовком для SA).
5. **Use Cases** — основной + альтернативные сценарии.
6. **Бизнес-правила** (`BR-*`).

**Передача дальше:** Use Cases + BRD — основа для SA (функции, валидации, сценарии).

---

## Шаг 4. SYSTEM ANALYST

Загрузи `references/agents/system-analyst.md` и нужные skills.

Порядок создания (по зависимостям):
1. **Backend Logic** (`skills/backend-logic.md`, `*_backend.md`) — 8 блоков: обзор, входные,
   валидации, основная логика, интеграции, исключения, выходные, производительность.
2. **ERD + SQL** (`skills/erd-model.md`, `*_erd.plantuml` + `*_sql.sql`) — сущности из
   Backend/BRD, идентификаторы `DATA-*`, нормализация 3NF, SQL для SQLite.
3. **Sequence** (`skills/sequence-diagram.md`, `*_sequence.plantuml`) — сценарии из Use Case,
   участники из архитектуры, этапы, alt/opt/loop, обработка ошибок.
4. **OpenAPI** (`skills/openapi-spec.md`, `*_openapi.yaml`) — эндпоинты из Backend, схемы из
   ERD, идентификаторы `API-*`.
5. **AsyncAPI** (`skills/asyncapi-spec.md`, `*_asyncapi.yaml`) — **только если** есть
   события/Kafka/брокер. Иначе пропустить.
6. **NFR** (`skills/nfr-requirements.md`, `*_nfr.md`) — по 8 категориям; числа — только из
   контекста пользователя, иначе `NEED USER INPUT`. Идентификаторы `NFR-*`.

**Передача дальше:** все артефакты SA — на вход Security Reviewer и quality gate.

---

## Шаг 5. SECURITY REVIEW

Загрузи `references/agents/security-reviewer.md` и `skills/security-review-checklist.md`.
**Режим: строго read-only.**

1. Просмотри все созданные артефакты (US, BRD, Backend, ERD, OpenAPI, AsyncAPI, NFR).
2. Примени методологии: 6 столпов ИБ, STRIDE, OWASP Top 10, IAM-проверки, PII/secrets,
   compliance (GDPR / 152-ФЗ / PCI DSS / отраслевые).
3. Сформири `reports/<project>_security_review.md` по шаблону из skill
   (исполнительное резюме, threat modeling, compliance, риск-матрица, рекомендации).
4. Идентификаторы находок `SEC-*` с уровнем критичности (Critical/High/Medium/Low).
5. **Не изменяй** анализируемые артефакты и проект. Только отчёт.

---

## Шаг 6. QUALITY GATE

Загрузи `references/workflows/quality-gates.md`. Проверь:
- Полноту (все запланированные артефакты созданы).
- Непротиворечивость между артефактами (API↔backend, API↔ERD, Sequence↔API, NFR↔архитектура,
  Security↔NFR, US↔AC).
- Трассируемость (каждая US → AC → FR → Backend → API → Data → NFR; разрывы зафиксировать).
- Архитектурную согласованность.

Сформири `reports/quality_report.md` со статусами `PASS / WARNING / FAIL / NEED USER INPUT`.

---

## Шаг 7. FINAL REPORT + ЭКСПОРТ

1. **Скомпилируй** `reports/final_report.md` из существующих артефактов по шаблону
   `templates/final-report.md` (24 раздела). **Не пиши содержимое заново** — вставляй
   секции из уже созданных файлов. Если раздела нет — пиши
   `Не сформировано (требуется: <артефакт>)`.
2. **Экспорт** по запросу пользователя:
   ```bash
   python scripts/export_report.py reports/final_report.md --format both
   ```
   → `exports/final_report.pdf`, `exports/final_report.docx`.

---

## Контрольные точки пайплайна

| После шага | Что должно быть готово |
|---|---|
| 1. INTAKE | `reports/project-context.md` (≥70%), определён scope |
| 2. PO | `*_user-story.md`, `*_backlog-priority.md`, (опц.) `*_stakeholder-map.md`, `*_business-case.md`, `*_roadmap.md` |
| 3. BA | `*_bpmn.md` (AS-IS+TO-BE), `*_gap-analysis.md`, `*_brd.md`, `*_use-case.md` |
| 4. SA | `*_backend.md`, `*_erd.plantuml`, `*_sql.sql`, `*_sequence.plantuml`, `*_openapi.yaml`, (опц.) `*_asyncapi.yaml`, `*_nfr.md` |
| 5. SECURITY | `*_security_review.md` |
| 6. QUALITY | `reports/quality_report.md` |
| 7. FINAL | `reports/final_report.md`, (опц.) `exports/*.{pdf,docx}` |

## Что делать, если данных не хватает

- На шаге анализа: помечай `[ТРЕБУЕТСЯ: ...]` и продолжай с тем, что есть.
- В quality_report: ставь `NEED USER INPUT` для этих пунктов.
- Не блокируй весь пайплайн из-за одной недостающей детали — создавай остальные артефакты.
- Финальный отчёт честно показывает пробелы; пользователь решает, уточнять ли их.
