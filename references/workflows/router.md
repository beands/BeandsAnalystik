# Workflow: Маршрутизация

Правила выбора роли и артефакта по запросу пользователя. Оркестратор загружает этот файл,
когда запрос неоднозначен или нужно решить, какие роли/skills задействовать.

## 1. Сначала проверь контекст

Перед маршрутизацией:
1. Прочитай `reports/project-context.md` (если существует) — возможно, роль/этап уже определены.
2. Прочитай существующие артефакты в `reports/` — не дублируй уже созданное.
3. Просканируй файлы проекта (`glob`/`grep`), чтобы извлечь очевидные факты (стек, сущности, API).

## 2. Три режима работы

### Режим A — Полный анализ («спроектируй …», «помоги с …», «анализируй проект»)

Пользователь хочет сквозной результат. Запусти `full-analysis.md`:
```
INTAKE → PO → BA → SA → SECURITY → QUALITY GATE → FINAL REPORT
```
Сначала обязательно пройди адаптивный опрос (`interview.md`), затем последовательно
создавай артефакты, передавая результаты между ролями.

### Режим B — Отдельный артефакт

Пользователь назвал конкретный артефакт. Маршрутизируй по таблице (раздел 3):
- выбери роль,
- загрузи соответствующий `references/skills/<name>.md`,
- при необходимости проведи мини-опрос (только то, чего не хватает для этого артефакта),
- создай файл, прогони чек-лист skill'а.

### Режим C — Ревью/проверка («проверь …», «оцени качество …», «security review»)

- Security review → роль Security Reviewer, skill `security-review-checklist.md`, read-only.
- Quality review артефакта → прогони чек-лист из соответствующего skill, отчёт в `reports/<name>_review_report.md`.

## 3. Таблица маршрутизации (запрос → роль → skill → имя файла)

| Триггеры в запросе | Роль | Skill | Имя файла |
|---|---|---|---|
| user story, история, AC, критерии приёмки | PO | `user-story.md` | `*_user-story.md` |
| приоритизация, backlog, что первым, RICE, WSJF, MoSCoW | PO | `backlog-prioritization.md` | `*_backlog-priority.md` |
| бизнес-кейс, ROI, TCO, окупаемость, обоснование инициативы | PO | `business-case.md` | `*_business-case.md` |
| роадмап, roadmap, план релизов, now/next/later | PO | `product-roadmap.md` | `*_roadmap.md` |
| стейкхолдеры, stakeholder map, RACI, кто за что отвечает | PO | `stakeholder-map.md` | `*_stakeholder-map.md` |
| бизнес-процесс, BPMN, as-is, to-be, swimlane, gap | BA | `business-process-bpmn.md` | `*_bpmn.md`, `*_gap-analysis.md` |
| требования, BRD, BRS, use case, бизнес-правила | BA | (роль BA) | `*_brd.md`, `*_use-case.md`, `*_brs.md` |
| backend логика, алгоритм, серверная логика | SA | `backend-logic.md` | `*_backend.md` |
| ERD, модель данных, схема БД, сущности | SA | `erd-model.md` | `*_erd.plantuml`, `*_sql.sql` |
| sequence, диаграмма взаимодействия, поток вызовов | SA | `sequence-diagram.md` | `*_sequence.plantuml` |
| API, OpenAPI, REST, swagger, эндпоинты | SA | `openapi-spec.md` | `*_openapi.yaml` |
| Kafka, AsyncAPI, брокер сообщений, события, топики | SA | `asyncapi-spec.md` | `*_asyncapi.yaml` |
| NFR, нефункциональные требования, производительность, надёжность, SLA | SA | `nfr-requirements.md` | `*_nfr.md` |
| безопасность, security review, уязвимости, ИБ, compliance | Security | `security-review-checklist.md` | `*_security_review.md` |

## 4. Зависимости между артефактами (порядок создания)

```
project-context.md (контекст из интервью)
        │
        ▼
User Story (US-*) + Acceptance Criteria (AC-*)
        │
        ├──▶ BPMN AS-IS/TO-BE + Gap-анализ  (BA)
        │         │
        │         ▼
        │    BRD / Use Cases + бизнес-правила (BR-*)
        │
        ▼
Backend Logic  ◀──── зависит от US + Use Case + архитектуры
   │
   ├──▶ ERD + SQL (DATA-*)      ◀── сущности из Backend/BRD
   ├──▶ Sequence                ◀── сценарии из Use Case + участники архитектуры
   ├──▶ OpenAPI (API-*)         ◀── эндпоинты из Backend, схемы из ERD
   ├──▶ AsyncAPI                ◀── события из Backend/Sequence
   └──▶ NFR (NFR-*)             ◀── ограничения из контекста + архитектуры
        │
        ▼
Security Review (SEC-*)   ◀── ревьюит ВСЕ вышестоящие артефакты (read-only)
        │
        ▼
Quality Report            ◀── проверки связности (quality-gates.md)
        │
        ▼
Final Report              ◀── компиляция из всех артефактов
```

**Правило:** если артефакт требует входных данных, которых ещё нет, сначала создай
предшествующий артефакт (или запроси недостающие данные у пользователя). Не придумывай
входы — помечай `[ТРЕБУЕТСЯ: ...]`.

## 5. Когда менять роль по ходу работы

- PO обнаружил бизнес-процесс, требующий формализации → передать BA (BPMN/BRD).
- BA сформировал Use Case, из которого видна техническая сложность → передать SA.
- SA создал OpenAPI/ERD → предложить Security Review.
- Security Reviewer нашёл критичные SEC-* → предупредить пользователя; **не исправлять
  самостоятельно**, а зафиксировать в `reports/<name>_security_review.md` и отметить в
  quality report как FAIL/WARNING.

## 6. Антипаттерны (не делать)

- Не запускай все роли для запроса одного артефакта.
- Не создавай ERD/OpenAPI, пока нет хотя бы User Story или описания функций.
- Не генерируй NFR с придуманными числами (RPS, latency) — это всегда `NEED USER INPUT`,
  пока пользователь не подтвердит.
- Не пиши final_report, пока не созданы составляющие артефакты (он компилируется, а не пишется с нуля).
