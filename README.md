# BeandsAnalystik

Переносимый skill-пакет для продуктового, бизнес-, системного и security-анализа. Он помогает вести пользователя от неструктурированной идеи к набору связанных артефактов: требованиям, моделям данных, API-спецификациям, security review и итоговому отчёту.

Поддерживаются **Hermes Agent** и **OpenClaw** через единый `SKILL.md` и установщик.

> Статус лицензии: перед публичным распространением изучите [SOURCE_NOTICE.md](SOURCE_NOTICE.md). Пакет включает переработанные материалы из OpenCode, у которого на дату аудита не была обнаружена явная лицензия. Получите разрешение правообладателя, прежде чем публиковать производные материалы.

## Зачем нужен skill

BeandsAnalystik не генерирует большой документ без контекста. Он сначала изучает имеющиеся данные, задаёт адаптивные вопросы небольшими блоками, выбирает только необходимые роли и методологии, а затем проводит quality gate.

## Возможности

- Маршрутизация запросов между Product Owner, Business Analyst, System Analyst и Security Reviewer.
- Адаптивный опрос: 2-4 вопроса за шаг, варианты ответа, учёт уже известного контекста.
- User Story и acceptance criteria, backlog-prioritization, business case, roadmap, stakeholder map.
- BPMN/AS-IS/TO-BE, BRD, use cases и трассировка требований.
- Backend logic, ERD/SQL, sequence diagrams, OpenAPI, AsyncAPI, NFR и интеграции.
- Read-only security review по STRIDE/OWASP/IAM/PII.
- Итоговый Markdown-отчёт и экспорт в PDF/DOCX.
- Проверка структуры и установка для Hermes Agent и OpenClaw.

## Структура

```text
.
├── SKILL.md
├── README.md
├── SOURCE_NOTICE.md
├── requirements.txt
├── references/
│   ├── agents/
│   ├── skills/
│   └── workflows/
├── templates/
├── scripts/
├── tests/
└── reports/
```

`reports/` в репозитории содержит только проверочные отчёты готовности. Рабочие отчёты и PDF/DOCX исключены через `.gitignore`.

## Требования

- Python 3.8+.
- Hermes Agent или OpenClaw для использования как skill.
- Зависимости из `requirements.txt` для локального PDF/DOCX-экспорта.

Установка зависимостей:

```bash
py -m pip install -r requirements.txt
```

На Windows используйте `py`; на macOS/Linux обычно подойдёт `python3`.

## Установка

Проверить пакет без копирования:

```bash
py scripts/install.py --verify
py scripts/install.py --target both --dry-run
```

Установить глобально:

```bash
py scripts/install.py --target both --global
```

Установить в конкретный workspace:

```bash
py scripts/install.py --target both --workspace C:/path/to/workspace
```

## Быстрый старт

После установки обратитесь к агенту с задачей, например:

```text
Помоги спроектировать B2B-сервис: AI-агент квалифицирует лиды из Telegram,
пишет результат в CRM и передаёт сложные обращения менеджеру.
```

Skill прочитает доступный контекст, уточнит самое важное, создаст нужные артефакты в `reports/` целевого проекта и сообщит о пробелах. Для полного анализа используются все роли последовательно; для узкого запроса загружается только соответствующий модуль.

## Пример маршрутизации

| Запрос | Роль | Артефакты |
|---|---|---|
| «Нужна user story» | Product Owner | User Story, AC |
| «Нужны BPMN или BRD» | Business Analyst | AS-IS/TO-BE, BPMN, BRD |
| «Сделай OpenAPI или ERD» | System Analyst | OpenAPI, ERD/SQL, Sequence |
| «Проведи security review» | Security Reviewer | Read-only security report |
| «Спроектируй сервис» | Оркестратор | Полный набор по мере необходимости |

## Экспорт PDF и DOCX

Сначала сформируйте Markdown-отчёт, затем выполните:

```bash
py scripts/export_report.py reports/final_report.md --format both
```

По умолчанию файлы появятся в `exports/`. Можно указать каталог явно:

```bash
py scripts/export_report.py reports/final_report.md --format pdf --output-dir exports
```

Экспортёр сканирует входной Markdown на распространённые маркеры секретов. PDF использует WeasyPrint, если он доступен, и кроссплатформенный ReportLab fallback с кириллицей. На Windows ReportLab не требует GTK/Pango; при его использовании шрифт Arial должен быть доступен в системе. DOCX создаётся через `python-docx`.

## Обновление и удаление

Обновление сохраняет прежнюю установку в `BeandsAnalystik.bak`:

```bash
py scripts/install.py --target both --global --update
```

Удаление также создаёт backup:

```bash
py scripts/install.py --target hermes --global --uninstall
py scripts/install.py --target openclaw --global --uninstall
```

## Проверка

```bash
py -m unittest discover -s tests -v
```

Тесты проверяют frontmatter и references, режимы проверки/сухого запуска установщика, экспорт PDF/DOCX с кириллицей и чистую ошибку при отсутствующем входном файле.

## Ограничения

- Skill создаёт аналитические артефакты, но не заменяет юридическую, финансовую или compliance-экспертизу.
- Security Reviewer работает только на чтение и пишет отчёты; он не меняет анализируемый проект.
- Неподтверждённые метрики должны быть помечены как требующие подтверждения, а не выдаваться за факты.
- PDF fallback поддерживает типовой Markdown: заголовки, абзацы, списки и таблицы. Сложную вёрстку следует визуально проверять после экспорта.
- Установка ориентирована на стандартные каталоги Hermes/OpenClaw; при нестандартном расположении используйте `--workspace`.

## Troubleshooting

| Проблема | Решение |
|---|---|
| Skill не появляется | Перезапустите клиент, затем выполните `py scripts/install.py --verify`. |
| Не найден модуль | Выполните `py -m pip install -r requirements.txt`. |
| WeasyPrint не запускается в Windows | Это допустимо: экспортёр использует ReportLab fallback. Для WeasyPrint установите GTK/Pango по его официальной документации. |
| В PDF квадраты вместо кириллицы | Используйте актуальный `scripts/export_report.py`; на Windows проверьте наличие `C:\Windows\Fonts\arial.ttf`. |
| Таблица в PDF плохо читается | Сократите число колонок либо перенесите длинные поля в текст под таблицей; после экспорта проверьте PDF визуально. |
| Установщик не находит путь | Передайте явный `--workspace PATH`. |

## Происхождение и acknowledgements

Методологии и структура пакета были переработаны с учётом материалов [CrazyElephantX/OpenCode](https://github.com/CrazyElephantX/OpenCode). Полная атрибуция, аудит происхождения и ограничение по лицензированию находятся в [SOURCE_NOTICE.md](SOURCE_NOTICE.md) и [references/source-audit.md](references/source-audit.md).

## Лицензия

В этом репозитории намеренно нет файла `LICENSE`, пока не будет подтверждён правовой статус производных материалов. См. [SOURCE_NOTICE.md](SOURCE_NOTICE.md).
