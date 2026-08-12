# Workflow: Quality Gates

Чек-листы согласованности и полноты. Запускаются:
- после создания **каждого** артефакта (локальный чек-лист из соответствующего skill);
- после **полного** анализа (этот файл — сквозные проверки).

Результат итогового прогона — `reports/quality_report.md` со статусами
`PASS / WARNING / FAIL / NEED USER INPUT`.

---

## 1. Локальные чек-листы (на каждый артефакт)

Каждый skill в `references/skills/` заканчивается разделом «Чек-лист качества». После
создания артефакта обязательно прогони его. Если хоть один пункт провален — артефакт
получает `WARNING` или `FAIL` и пометку в quality_report.

| Артефакт | Чек-лист в skill |
|---|---|
| User Story | `skills/user-story.md` (INVEST, Gherkin, ≥2 сценария) |
| Backlog | `skills/backlog-prioritization.md` (метод обоснован, числа не «на глаз») |
| Business Case | `skills/business-case.md` (ROI по формуле, ≥3 риска, ≥1 альтернатива) |
| BPMN | `skills/business-process-bpmn.md` (триггер, swimlanes, gateway, метрики до/после) |
| Stakeholder Map | `skills/stakeholder-map.md` (стратегии, ровно 1 A на задачу в RACI) |
| Roadmap | `skills/product-roadmap.md` (привязка к целям, без точных дат в Later) |
| Backend Logic | `skills/backend-logic.md` (8 блоков, ≥5 типов ошибок, соответствие API/ERD) |
| ERD + SQL | `skills/erd-model.md` (3NF, FK→PK, SQL соответствует ERD, тестовые данные) |
| Sequence | `skills/sequence-diagram.md` (3–7 этапов, alt/opt/loop, ≥2 ошибки, протоколы) |
| OpenAPI | `skills/openapi-spec.md` (CRUD, components, коды статусов, examples) |
| AsyncAPI | `skills/asyncapi-spec.md` (6 блоков, схемы, партиционирование, retention) |
| NFR | `skills/nfr-requirements.md` (измеримость, единицы, приоритет, обоснование) |
| Security Review | `skills/security-review-checklist.md` (STRIDE, OWASP, compliance, риск-матрица) |

---

## 2. Сквозные проверки согласованности

Запускаются после шагов SA/Security полного анализа (или при явном запросе «проверь связи»).

### 2.1. API ↔ Backend Logic
- [ ] Каждый эндпоинт OpenAPI имеет соответствующее описание в Backend Logic.
- [ ] Параметры запросов API совпадают с «входными данными» Backend.
- [ ] Коды ответов API (400/401/403/404/409/500) покрыты в «исключительных ситуациях» Backend.
- [ ] Формат ответов API соответствует «выходным данным» Backend.

### 2.2. API ↔ ERD
- [ ] Каждая сущность в схемах OpenAPI имеет соответствующую таблицу в ERD.
- [ ] Поля схем API соответствуют колонкам таблиц (типы, обязательность).
- [ ] Связи (FK) в ERD отражены во вложенных/связанных схемах API.
- [ ] Нет «лишних» сущностей API без таблицы и наоборот (оправдано ли отсутствие).

### 2.3. Sequence ↔ API
- [ ] Эндпоинты, упомянутые в Sequence, существуют в OpenAPI.
- [ ] HTTP-методы в Sequence соответствуют методам в OpenAPI.
- [ ] Участники Sequence соответствуют компонентам архитектуры.
- [ ] Альтернативные потоки Sequence покрыты кодами ошибок API.

### 2.4. Backend ↔ ERD
- [ ] SQL-операции в Backend используют таблицы/колонки из ERD.
- [ ] Транзакции в Backend согласованы с ограничениями ERD (FK, уникальность).
- [ ] Индексы ERD покрывают часто запрашиваемые в Backend поля.

### 2.5. NFR ↔ Архитектура
- [ ] NFR-PERF (latency/throughput) достижимы при заявленной архитектуре (оценка).
- [ ] NFR-REL (availability) подкреплена резервированием в архитектуре.
- [ ] NFR-SCAL согласуется с выбором stateless/stateful компонентов.
- [ ] Нет противоречащих NFR (например, p99 < 50ms и синхронный вызов 3 внешних API).

### 2.6. Security ↔ NFR/Архитектура
- [ ] Каждый SEC-* (находка) имеет либо митигацию в архитектуре, либо зафиксирован как риск.
- [ ] NFR-SEC непротиворечивы сfindings security review.
- [ ] PII-поля из ERD имеют требования шифрования (NFR-SEC / SEC-*).
- [ ] Аутентификация/авторизация в API отражены в security review.

### 2.7. User Story ↔ Acceptance Criteria
- [ ] Каждая `US-*` имеет хотя бы один `AC-<код Story>-*`.
- [ ] Каждый AC в Gherkin (Given/When/Then) и проверяем.
- [ ] Нет AC, не привязанных к US; нет US без AC.
- [ ] Альтернативные/ошибочные сценарии AC покрыты в Sequence/Backend.

---

## 3. Трассируемость (Traceability Matrix)

Проверь сквозную цепочку. Для каждой `US-*` должна существовать цепочка:
```
GOAL-* (цель) → BR-*/FR-* (требование) → US-* (история) → AC-* (критерий)
   → Backend-блок → API-* (эндпоинт) → DATA-* (сущность) → NFR-* (ограничение) → SEC-* (если применимо)
```

Сформируй таблицу в `reports/quality_report.md`:

```markdown
| US | AC | FR/BR | Backend | API | DATA | NFR | SEC | Статус |
|----|----|-------|---------|-----|------|-----|-----|--------|
| US-001 | AC-001-1,2 | FR-003 | §3.2 | API-POST /orders | DATA-order | NFR-PERF-001 | SEC-012 | PASS |
| US-002 | AC-002-1 | FR-004 | [НЕТ] | API-GET /orders/{id} | DATA-order | — | — | FAIL: нет Backend |
```

Разрывы цепочки → `FAIL` или `WARNING` с пояснением.

---

## 4. Проверка полноты

- [ ] Все артефакты из scope (шаг 1 пайплайна) созданы.
- [ ] Каждый артефакт прошёл свой локальный чек-лист.
- [ ] `project-context.md` обновлён; открытые вопросы зафиксированы.
- [ ] Все `[ТРЕБУЕТСЯ: ...]` перенесены в раздел «Открытые вопросы» quality_report.
- [ ] В артефактах нет придуманных числовых показателей без пометки `требует подтверждения`.
- [ ] В отчётах нет secrets (ключей, паролей, токенов) — только SEC-* ссылки на файлы.

---

## 5. Шаблон `reports/quality_report.md`

```markdown
# Quality Report: <Проект>

**Дата:** YYYY-MM-DD
**Общий статус:** PASS / WARNING / FAIL
**Контекст собран:** NN%

## Сводка по артефактам
| Артефакт | Файл | Локальный чек-лист | Статус | Комментарий |
|---|---|---|---|---|
| User Stories | reports/crm_user-story.md | 6/6 | PASS | — |
| ERD | reports/crm_erd.plantuml | 5/6 | WARNING | Нет индекса на orders.user_id |

## Сквозные проверки согласованности
| Проверка | Статус | Детали |
|---|---|---|
| API ↔ Backend | PASS | все эндпоинты описаны |
| API ↔ ERD | WARNING | DATA-promo нет в API |
| Sequence ↔ API | PASS | — |
| Backend ↔ ERD | PASS | — |
| NFR ↔ Архитектура | FAIL | NFR-PERF-002 (p99<50ms) нереалистично при sync вызовах |
| Security ↔ NFR | PASS | — |
| US ↔ AC | PASS | — |

## Traceability Matrix
(таблица из раздела 3)

## Открытые вопросы (NEED USER INPUT)
- [ ] Уточнить RPS для peak load (для NFR-PERF-001)
- [ ] Подтвердить применимость 152-ФЗ (для SEC-compliance)
- [ ] Подтвердить latency budget p95 (для NFR-PERF-002)

## Рекомендации
1. (по FAIL-пунктам)
2. ...
```

## 6. Статусы и их смысл

| Статус | Значение | Действие |
|---|---|---|
| `PASS` | Проверка пройдена | Можно двигаться дальше |
| `WARNING` | Есть замечания, не блокирующие | Зафиксировать, продолжить, вернуться позже |
| `FAIL` | Критичный разрыв/противоречие | Обязательно исправить или явно согласовать с пользователем |
| `NEED USER INPUT` | Недостаточно данных для оценки | Запросить у пользователя, пометить в project-context |
