# {Название проекта} — Финальный отчёт

> Этот шаблон компилируется из уже созданных артефактов в `reports/`.
> **Не генерируй содержимое разделов заново** — вставляй из существующих файлов.
> Если раздела нет — пиши: `_Не сформировано (требуется: <артефакт>)_`.

**Версия отчёта:** 1.0
**Дата сборки:** YYYY-MM-DD
**Контекст собран:** NN%
**Автор(ы) анализа:** BeandsAnalystik Suite

---

## Оглавление

1. Executive Summary
2. Описание продукта
3. Цели и проблемы
4. Пользователи
5. Stakeholders
6. AS-IS
7. TO-BE
8. User Stories
9. Functional Requirements
10. Business Rules
11. Architecture
12. Backend Logic
13. ERD / Data Model
14. API
15. Integrations
16. NFR
17. Security Review
18. Risks
19. MVP Scope
20. Backlog
21. Roadmap
22. Open Questions
23. Recommendations
24. Requirements Traceability Matrix

---

## 1. Executive Summary

{1–3 абзаца: что за продукт, какую проблему решает, ключевые цифры/риски/рекомендация.
Источники: project-context.md, business-case.md, security_review.md (исполнительное резюме).}

## 2. Описание продукта

{Из project-context.md раздел 1 + business-case.md «Решение».}

## 3. Цели и проблемы

**Бизнес-цели:**
- GOAL-001: ...
- GOAL-002: ...

**Проблема:** {из business-case.md «Проблема» с цифрами}

## 4. Пользователи

{Из project-context.md: целевая аудитория, роли. Из user-story.md: роли акторов.}

## 5. Stakeholders

{Из *_stakeholder-map.md: таблица Power-Interest + RACI.}

## 6. AS-IS

{Из *_as-is.bpmn.md + gap-analysis.md: текущий процесс и выявленные проблемы.}

## 7. TO-BE

{Из *_to-be.bpmn.md: целевой процесс и устранённые проблемы.}

## 8. User Stories

{Из *_user-story.md: список US-XXX с формулировками и приоритетами.}

| US | Формулировка | Приоритет |
|----|--------------|-----------|
| US-001 | Как … я хочу … чтобы … | Must |

## 9. Functional Requirements

{Из *_brd.md / *_use-case.md: список FR-XXX.}

| FR | Описание | Связано с US |
|----|----------|--------------|
| FR-001 | ... | US-001 |

## 10. Business Rules

{Из *_brd.md: список BR-XXX.}

## 11. Architecture

{Описание архитектуры: компоненты, тип (monolith/microservices), diagram (если есть).}

## 12. Backend Logic

{Из *_backend.md: ключевые алгоритмы по фичам. Ссылки на файл.}

## 13. ERD / Data Model

{Из *_erd.plantuml + *_sql.sql: основные сущности DATA-*, связи. Вставить диаграмму.}

## 14. API

{Из *_openapi.yaml: список эндпоинтов API-*. Таблица методов.}

| API | Метод | Endpoint | Описание |
|-----|-------|----------|----------|
| API-001 | POST | /orders | Создание заказа |

## 15. Integrations

{Внешние сервисы, брокеры (из *_asyncapi.yaml если есть), партнёрские интеграции.}

## 16. NFR

{Из *_nfr.md: сводка по категориям. Ключевые NFR-* с приоритетами.}

| NFR | Категория | Значение | Приоритет |
|-----|-----------|----------|-----------|
| NFR-PERF-001 | Performance | p95 < 1с | Критический |

## 17. Security Review

{Из *_security_review.md: исполнительное резюме, критичные SEC-*, compliance статус.
**Secrets не включать** — только SEC-XXX ссылки.}

## 18. Risks

{Из business-case.md «Риски» + security_review.md «Risk Matrix» + quality_report.md FAIL-пункты.}

| Risk | Вероятность | Влияние | Митигация |
|------|-------------|---------|-----------|

## 19. MVP Scope

{Из backlog-priority.md (Must have) + roadmap.md (Now). Что обязательно в первой версии.}

## 20. Backlog

{Из *_backlog-priority.md: приоритизированная таблица.}

## 21. Roadmap

{Из *_roadmap.md: Now / Next / Later.}

## 22. Open Questions

{Из project-context.md «Открытые вопросы» + quality_report.md «NEED USER INPUT».}

- [ ] ...
- [ ] ...

## 23. Recommendations

{Из quality_report.md + security_review.md «Recommendations Roadmap» + business-case.md «Рекомендация».}

1. ...
2. ...

## 24. Requirements Traceability Matrix

{Из quality_report.md раздел Traceability Matrix. Сквозная цепочка GOAL→…→SEC.}

| US | AC | FR/BR | Backend | API | DATA | NFR | SEC | Статус |
|----|----|-------|---------|-----|------|-----|-----|--------|

---

## Приложения

- A. Глоссарий (из *_brd.md)
- B. Quality Report (полный — `reports/quality_report.md`)
- C. Список файлов артефактов в `reports/`
