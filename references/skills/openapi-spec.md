# Skill: Спецификация OpenAPI

**Роль:** System Analyst
**Назначение:** написание спецификации REST API в формате OpenAPI 3.0.
**Имя файла:** `*_openapi.yaml`
**Идентификаторы:** `API-*` для эндпоинтов/операций

## Содержание
1. Основы структуры
2. Метрики качества
3. Валидационные правила
4. Обязательные разделы
5. Описание эндпоинтов
6. Компоненты и схемы
7. Лучшие практики
8. Полный пример
9. Чек-лист качества

---

## 1. Основы структуры

Минимальная структура файла:
```yaml
openapi: 3.0.3
info:
  title: Название API
  description: Описание назначения и особенностей API
  version: '1.0.0'
servers:
  - url: https://api.example.com/v1
    description: Production server
tags:
  - name: users
    description: Операции с пользователями
paths: {}
components:
  schemas: {}
```

---

## 2. Метрики качества

### Целевые показатели
- **Полнота CRUD:** 100% покрытие операций Create, Read, Update, Delete.
- **Документация:** все эндпоинты имеют `description` и `examples`.
- **Валидность:** синтаксическая корректность YAML/JSON.
- **Схемы данных:** 95% переиспользование через `components`.

### Система оценки
- **Отличное:** CRUD + документация + валидность ≥ 90%.
- **Хорошее:** частичное CRUD + документация 70–89%.
- **Требует доработки:** базовая функциональность < 70%.

---

## 3. Валидационные правила

- `openapi` версия 3.0.0 или выше.
- `info` содержит `title`, `version`, `description`.
- `servers` указаны с URL и `description`.
- Все `paths` имеют операции (`get`, `post`, `put`, `delete`).
- `responses` содержат минимум 200 и 400/500 коды.
- `schemas` используют `$ref` для переиспользования.
- `parameters` имеют `description` и `schema`.
- `requestBody` содержит `content` с `schema`.

---

## 4. Обязательные разделы

### info
```yaml
info:
  title: User Management API
  description: |
    REST API для управления пользователями системы.
    Поддерживает полный CRUD для пользователей и ролей.
  version: '1.0.0'
  contact:
    name: API Support
    email: support@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT
```

### servers
```yaml
servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server
```

### tags
```yaml
tags:
  - name: users
    description: Управление пользователями
  - name: auth
    description: Аутентификация и авторизация
```

---

## 5. Описание эндпоинтов

### Структура операции
```yaml
/users/{id}:
  get:
    tags: [users]
    summary: Получить пользователя по ID
    description: Возвращает детальную информацию о пользователе
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
        description: Уникальный идентификатор пользователя
    responses:
      '200':
        description: Пользователь найден
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
            example:
              id: 1
              email: "user@example.com"
              name: "John Doe"
      '404':
        description: Пользователь не найден
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
```

### Обязательные элементы операции
- **tags** — группировка по функциональности.
- **summary** — краткое описание (до 50 символов).
- **description** — подробное описание.
- **parameters** — описание всех параметров.
- **responses** — минимум 200 и error codes.
- **examples** — примеры запросов и ответов.

---

## 6. Компоненты и схемы

### Переиспользуемые схемы
```yaml
components:
  schemas:
    User:
      type: object
      required: [id, email]
      properties:
        id:
          type: integer
          description: Уникальный идентификатор
          example: 1
        email:
          type: string
          format: email
          description: Email пользователя
          example: "user@example.com"
        name:
          type: string
          description: Полное имя пользователя
          example: "John Doe"
        created_at:
          type: string
          format: date-time
          description: Дата создания
          example: "2024-01-15T10:30:00Z"

    UserCreateRequest:
      type: object
      required: [email, password]
      properties:
        email:
          type: string
          format: email
        password:
          type: string
          minLength: 8
        name:
          type: string

    Error:
      type: object
      required: [code, message]
      properties:
        code:
          type: integer
          description: Код ошибки
        message:
          type: string
          description: Описание ошибки

  parameters:
    PageParam:
      name: page
      in: query
      schema:
        type: integer
        minimum: 1
      description: Номер страницы для пагинации

  responses:
    NotFound:
      description: Ресурс не найден
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

---

## 7. Лучшие практики

### Именование и структура
- **Пути:** kebab-case (`/user-profiles`).
- **Схемы:** PascalCase (`UserProfile`).
- **Параметры:** snake_case (`user_id`).
- **Операции:** группируй по тегам логически.

### Коды статусов

| Операция | Успех | Ошибка клиента | Ошибка сервера |
|----------|-------|----------------|----------------|
| **GET** | 200 | 404, 400 | 500 |
| **POST** | 201 | 400, 409 | 500 |
| **PUT** | 200 | 400, 404 | 500 |
| **DELETE** | 204 | 404 | 500 |

### Валидация данных
```yaml
properties:
  email:
    type: string
    format: email
    maxLength: 255
  age:
    type: integer
    minimum: 0
    maximum: 150
  status:
    type: string
    enum: [active, inactive, pending]
```

### Примеры и документация
- Добавляй `example` для каждого поля.
- Используй `description` для всех элементов.
- Включай реалистичные примеры запросов/ответов.
- Документируй бизнес-логику в `description`.

---

## 8. Полный пример API

```yaml
openapi: 3.0.3
info:
  title: User Management API
  description: REST API для управления пользователями
  version: '1.0.0'

servers:
  - url: https://api.example.com/v1
    description: Production server

tags:
  - name: users
    description: Операции с пользователями

paths:
  /users:
    get:
      tags: [users]
      summary: Получить список пользователей
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - name: limit
          in: query
          schema:
            type: integer
            maximum: 100
          description: Количество пользователей на странице
      responses:
        '200':
          description: Список пользователей
          content:
            application/json:
              schema:
                type: object
                properties:
                  users:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  total:
                    type: integer

    post:
      tags: [users]
      summary: Создать пользователя
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreateRequest'
      responses:
        '201':
          description: Пользователь создан
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'

  /users/{id}:
    get:
      tags: [users]
      summary: Получить пользователя
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Пользователь найден
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    User:
      type: object
      required: [id, email]
      properties:
        id:
          type: integer
          example: 1
        email:
          type: string
          format: email
          example: "user@example.com"
        name:
          type: string
          example: "John Doe"

    UserCreateRequest:
      type: object
      required: [email, password]
      properties:
        email:
          type: string
          format: email
        password:
          type: string
          minLength: 8
        name:
          type: string

  parameters:
    PageParam:
      name: page
      in: query
      schema:
        type: integer
        minimum: 1
      description: Номер страницы

  responses:
    BadRequest:
      description: Некорректный запрос
      content:
        application/json:
          schema:
            type: object
            properties:
              message:
                type: string
    NotFound:
      description: Ресурс не найден
      content:
        application/json:
          schema:
            type: object
            properties:
              message:
                type: string
```

---

## 9. Чек-лист качества

**Структурная проверка:**
- [ ] `openapi` версия 3.0.0+.
- [ ] `info` содержит `title`, `version`, `description`.
- [ ] `servers` указаны с `description`.
- [ ] `tags` определены для группировки.

**Проверка эндпоинтов:**
- [ ] Все CRUD-операции описаны.
- [ ] Каждая операция имеет `summary` и `description`.
- [ ] `parameters` содержат `schema` и `description`.
- [ ] `responses` покрывают success и error cases.

**Проверка схем:**
- [ ] Схемы вынесены в `components` для переиспользования.
- [ ] Обязательные поля указаны в `required`.
- [ ] Типы данных и форматы корректны.
- [ ] Добавлены `examples` для полей.

**Качественная проверка:**
- [ ] Покрыты все бизнес-операции.
- [ ] Валидация соответствует бизнес-правилам.
- [ ] Коды ошибок логически обоснованы.
- [ ] Документация понятна разработчикам.

**Интеграционная проверка:**
- [ ] API соответствует архитектуре системы.
- [ ] Схемы данных соответствуют ERD.
- [ ] Операции покрывают Use Case сценарии.
- [ ] Идентификаторы `API-*` проставлены для ключевых эндпоинтов.

**Цель:** создавать OpenAPI-спецификации, готовые для генерации клиентского кода и документации.

---

## 10. Инструменты проверки
- [Swagger Editor](https://editor.swagger.io/) — онлайн валидатор.
- OpenAPI Generator — генерация кода.
- Spectral — линтер для OpenAPI.

### Примеры качественной документации
✅ «Возвращает список пользователей с пагинацией»
✅ «Создает нового пользователя с валидацией email»
✅ «Ошибка 409 при дублировании email»

❌ «Получает данные»
❌ «Создает объект»
❌ «Возвращает ошибку»
