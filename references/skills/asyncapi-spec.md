# Skill: Спецификация AsyncAPI (Kafka Message Broker)

**Роль:** System Analyst
**Назначение:** спецификация асинхронных событий через Apache Kafka в формате AsyncAPI.
**Имя файла:** `*_asyncapi.yaml`
**Стандарт:** AsyncAPI 2.6.0+

> Создавай AsyncAPI-спецификацию **только если** в проекте есть брокер сообщений / события
> (Kafka, RabbitMQ, NATS). Для чисто REST-систем этот артефакт не нужен.

## Содержание
1. Формат выходного файла
2. Шаблон описания Kafka-архитектуры
3. Метрики качества
4. Валидационные правила
5. Методология проектирования
6. Критерии качества
7. Чек-лист

---

## 1. Формат выходного файла

### Обязательная структура AsyncAPI YAML

```yaml
# {feature-name}_asyncapi.yaml
asyncapi: '2.6.0'
info:
  title: '{Feature Name} Kafka Events API'
  version: '1.0.0'
  description: |
    Описание асинхронных событий для {feature-name} через Apache Kafka
  contact:
    name: 'Development Team'
    email: 'dev-team@company.com'
  license:
    name: 'MIT'

servers:
  kafka-cluster:
    url: '{kafka-broker-urls}'
    protocol: kafka
    description: 'Production Kafka cluster'
    bindings:
      kafka:
        schemaRegistryUrl: 'http://schema-registry:8081'
        schemaRegistryVendor: 'confluent'
    security:
      - saslScram: []

defaultContentType: application/json

channels:
  'domain.entity.events':
    description: 'События жизненного цикла {entity}'
    bindings:
      kafka:
        topic: 'domain.entity.events'
        partitions: 12
        replicas: 3
        configs:
          retention.ms: 2592000000  # 30 дней
          cleanup.policy: 'delete'
          compression.type: 'snappy'
    publish:
      summary: 'Отправка событий {entity}'
      operationId: 'publishEntityEvent'
      bindings:
        kafka:
          groupId: 'entity-producers'
          clientId: 'entity-service'
          acks: 'all'
          key:
            type: string
            description: 'ID сущности для партиционирования'
      message:
        $ref: '#/components/messages/EntityEvent'
    subscribe:
      summary: 'Получение событий {entity}'
      operationId: 'subscribeEntityEvent'
      bindings:
        kafka:
          groupId: 'entity-consumers'
          clientId: 'consumer-service'
      message:
        $ref: '#/components/messages/EntityEvent'

components:
  messages:
    EntityEvent:
      name: 'EntityEvent'
      title: 'Событие сущности'
      summary: 'Событие изменения состояния сущности'
      contentType: application/json
      headers:
        type: object
        properties:
          eventType:
            type: string
            enum: ['CREATED', 'UPDATED', 'DELETED']
          source:
            type: string
            description: 'Источник события'
          timestamp:
            type: string
            format: date-time
      payload:
        $ref: '#/components/schemas/EntityEventPayload'
      examples:
        - name: 'entityCreated'
          summary: 'Создание сущности'
          headers:
            eventType: 'CREATED'
            source: 'entity-service'
            timestamp: '2024-01-15T10:30:00Z'
          payload:
            entityId: 'uuid-here'
            status: 'ACTIVE'
            createdAt: '2024-01-15T10:30:00Z'

  schemas:
    EntityEventPayload:
      type: object
      required: [entityId, status, createdAt]
      properties:
        entityId:
          type: string
          format: uuid
          description: 'Уникальный идентификатор сущности'
        status:
          type: string
          enum: ['ACTIVE', 'INACTIVE', 'PENDING']
        createdAt:
          type: string
          format: date-time
        metadata:
          type: object
          additionalProperties: true

  securitySchemes:
    saslScram:
      type: scramSha512
      description: 'SASL/SCRAM authentication'

  parameters:
    EntityId:
      description: 'Идентификатор сущности'
      schema:
        type: string
        format: uuid

# Дополнительная конфигурация Kafka
x-kafka-config:
  cluster:
    brokers: 3
    replication:
      default: 2
      critical_topics: 3
  producers:
    default_config:
      acks: 'all'
      retries: 10
      batch.size: 100000
      linger.ms: 5
      enable.idempotence: true
      compression.type: 'snappy'
  consumers:
    default_config:
      auto.commit.enable: false
      max.poll.records: 500
      session.timeout.ms: 30000
      fetch.min.bytes: 1
  monitoring:
    metrics:
      - 'kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec'
      - 'kafka.consumer:type=consumer-fetch-manager-metrics'
      - 'kafka.producer:type=producer-metrics'
    alerts:
      - name: 'high_consumer_lag'
        condition: 'consumer_lag > 10000'
        severity: 'critical'
      - name: 'broker_down'
        condition: 'broker_availability < 100%'
        severity: 'critical'
  security:
    authentication:
      protocol: 'SASL_SSL'
      mechanism: 'SCRAM-SHA-512'
    acls:
      - principal: 'User:entity-service'
        operations: ['Write', 'Describe']
        resources: ['Topic:domain.entity.events']
      - principal: 'User:consumer-service'
        operations: ['Read', 'Describe']
        resources: ['Topic:domain.entity.events', 'Group:entity-consumers']
```

### Правила именования файлов
- `{feature-name}_asyncapi.yaml` — для основных фич.
- `{domain}_events_asyncapi.yaml` — для доменных решений.
- `{system-name}_kafka_asyncapi.yaml` — для системных интеграций.

### Обязательные секции AsyncAPI
1. **asyncapi** — версия спецификации (2.6.0+).
2. **info** — метаданные API.
3. **servers** — конфигурация Kafka-кластера.
4. **channels** — топики и их конфигурация.
5. **components** — схемы сообщений, security schemes.
6. **x-kafka-config** — расширенная конфигурация Kafka (опционально).

---

## 2. Шаблон описания Kafka-архитектуры (9 блоков)

| № | Блок | Описание | Обязательность |
|---|------|----------|----------------|
| 1 | **Общий обзор** | Назначение Kafka в системе, роль в архитектуре | ✅ Обязательно |
| 2 | **Топики и схемы** | Структура топиков, схемы сообщений, партиционирование | ✅ Обязательно |
| 3 | **Продьюсеры** | Сервисы-отправители, стратегии отправки | ✅ Обязательно |
| 4 | **Консьюмеры** | Сервисы-получатели, группы консьюмеров | ✅ Обязательно |
| 5 | **Конфигурация кластера** | Настройки брокеров, репликация, отказоустойчивость | ✅ Обязательно |
| 6 | **Схемы данных** | Avro/JSON-схемы, Schema Registry, версионирование | ✅ Обязательно |
| 7 | **Безопасность** | Аутентификация, авторизация, шифрование | 🔶 Рекомендуется |
| 8 | **Мониторинг и алерты** | Метрики, логирование, SLA | 🔶 Рекомендуется |
| 9 | **Производительность** | Throughput, latency, оптимизации | 🔶 Рекомендуется |

---

## 3. Метрики качества

### Целевые показатели
- **Полнота структуры:** 6/6 обязательных блоков = 100%.
- **Покрытие топиков:** описание всех основных топиков системы.
- **Схемы данных:** 100% топиков имеют описание схем.
- **Группы консьюмеров:** чёткое разделение ответственности.
- **Отказоустойчивость:** минимум 2× репликация критичных топиков.

### Система оценки
- **Production-ready:** 95–100% + безопасность + мониторинг.
- **Отличное:** 85–94%.
- **Хорошее:** 70–84%.
- **Требует доработки:** < 70%.

---

## 4. Валидационные правила

### Структурная валидация
- Все 6 обязательных блоков присутствуют.
- Каждый топик имеет описание схемы.
- Продьюсеры и консьюмеры чётко идентифицированы.
- Указана стратегия партиционирования.

### Архитектурная валидация
- Топики логически связаны с доменами системы.
- Схемы данных соответствуют API-спецификациям.
- Группы консьюмеров не пересекаются по ответственности.
- Репликация настроена для критичных топиков.

### Производственная валидация
- Указаны retention policies для всех топиков.
- Описана стратегия обработки ошибок.
- Настроен мониторинг и алертинг.
- Документированы процедуры disaster recovery.

---

## 5. Методология проектирования

### Шаг 1: Анализ доменных событий
Источники: User Stories, Use Cases, Sequence-диаграммы, архитектурная диаграмма, API-спецификации.

### Шаг 2: Выделение событий
- **Domain Events** — изменения состояния бизнес-сущностей.
- **Integration Events** — межсервисное взаимодействие.
- **System Events** — технические события (логи, метрики).
- **Command Events** — асинхронные команды.

### Шаг 3: Проектирование топиков
Принцип именования: `{domain}.{entity}.{event-type}`
```
banking.transfer.created
banking.transfer.completed
ecommerce.order.placed
notification.email.sent
```

### Шаг 4: Определение схем
- **Avro** — строгая типизация, эволюция схем.
- **JSON Schema** — гибкость, простота.
- **Protobuf** — производительность, совместимость.

### Шаг 5: Планирование партиций
- По ID пользователя (user-based).
- По ID сущности (entity-based).
- По временным меткам (time-based).
- Round-robin (равномерное распределение).

### Шаг 6: Настройка консьюмеров
- **Single Consumer** — обработка в порядке.
- **Consumer Group** — параллельная обработка.
- **Multiple Groups** — различная бизнес-логика.

---

## 6. Пример описания топика

### Топик: `banking.transfer.events`
```yaml
Назначение: События жизненного цикла переводов
Партиции: 12 (по account_id % 12)
Replication Factor: 3
Retention: 30 дней
Cleanup Policy: delete
```

### Схема сообщения (Avro)
```json
{
  "type": "record",
  "name": "TransferEvent",
  "namespace": "com.bank.events",
  "fields": [
    {"name": "transferId",   "type": "string"},
    {"name": "fromAccountId","type": "string"},
    {"name": "toAccountId",  "type": "string"},
    {"name": "amount",       "type": {"type": "fixed", "name": "Decimal", "size": 16}},
    {"name": "currency",     "type": "string"},
    {"name": "status",       "type": {"type": "enum", "symbols": ["PENDING","PROCESSING","COMPLETED","FAILED"]}},
    {"name": "timestamp",    "type": {"type": "long", "logicalType": "timestamp-millis"}},
    {"name": "userId",       "type": "string"},
    {"name": "comment",      "type": ["null","string"], "default": null}
  ]
}
```

### Продьюсер
```yaml
Сервис: transfer-service
Топики: banking.transfer.events
Стратегия:
  - Идемпотентность: включена
  - Acks: all (гарантия записи на все реплики)
  - Retries: 10
  - Batch Size: 100KB
  - Linger: 5ms
Обработка ошибок:
  - Retry с exponential backoff
  - Dead Letter Queue: banking.transfer.dlq
```

### Консьюмер
```yaml
Группа: fraud-detection-group
Топики: banking.transfer.events
Стратегия:
  - Auto Commit: false (ручное подтверждение)
  - Max Poll Records: 50
  - Session Timeout: 30s
  - Partition Assignment: cooperative-sticky
Логика:
  - Анализ на мошенничество
  - Публикация результата в fraud.detection.results
```

---

## 7. Критерии качества для ИИ

### Архитектурная зрелость
- **Обязательно:** все 6 основных блоков заполнены.
- **Продакшн:** добавлены блоки безопасности, мониторинга, производительности.
- **Enterprise:** добавлены disaster recovery, compliance, governance.

### Техническая детализация
- **Топики:** ясная схема партиционирования и retention-политики.
- **Схемы:** валидные Avro/JSON Schema с примерами.
- **Конфигурация:** realistic настройки для целевой нагрузки.
- **Безопасность:** ACL, аутентификация, шифрование.

### Операционная готовность
- **Мониторинг:** ключевые метрики и алерты определены.
- **Обработка ошибок:** DLQ, retry policies, circuit breakers.
- **Производительность:** SLA, throughput, latency.
- **Disaster Recovery:** backup, restore, failover процедуры.

### Интеграция с системой
- **Domain Events:** соответствуют бизнес-логике из Use Cases.
- **API Integration:** дополняют REST API архитектуру.
- **Data Flow:** согласованы с Sequence-диаграммами.
- **Services:** соответствуют компонентной архитектуре.

---

## 8. Чек-лист качества

**Обязательная проверка:**
- [ ] AsyncAPI YAML-файл создан с правильным именем.
- [ ] Версия AsyncAPI указана (2.6.0+).
- [ ] Секция `info` заполнена полностью.
- [ ] `servers` содержит конфигурацию Kafka.
- [ ] `channels` описывают все топики.
- [ ] Каждый channel имеет publish/subscribe операции.
- [ ] `components` содержат схемы сообщений.
- [ ] Определена стратегия партиционирования в bindings.
- [ ] Настроена репликация в kafka bindings.
- [ ] Описаны retention policies в configs.
- [ ] Схемы данных валидны (JSON Schema).
- [ ] Указаны группы консьюмеров в bindings.
- [ ] AsyncAPI YAML-синтаксис корректен.

**Качественная проверка:**
- [ ] Топики логически связаны с доменами.
- [ ] Схемы поддерживают эволюцию (backward compatibility).
- [ ] Обработка ошибок через DLQ описана.
- [ ] Идемпотентность обработки обеспечена.
- [ ] Producer acknowledgements настроены корректно.
- [ ] Consumer offset management определён.

**Production-ready проверка:**
- [ ] Безопасность: SASL/SSL, ACL настроены.
- [ ] Мониторинг: метрики и алерты определены.
- [ ] Производительность: SLA и оптимизации описаны.
- [ ] Backup и disaster recovery процедуры.
- [ ] Schema Registry настроен.
- [ ] Consumer lag мониторинг.
- [ ] Dead Letter Queue обработка.
- [ ] Capacity planning (партиции, brokers).

**Интеграционная проверка:**
- [ ] События соответствуют Use Cases.
- [ ] Схемы совместимы с API-спецификациями.
- [ ] Сервисы-продьюсеры есть в архитектурной диаграмме.
- [ ] Consumer groups не конфликтуют по ответственности.
- [ ] Временные характеристики реалистичны.
- [ ] Объёмы данных соответствуют масштабу системы.

**Финальная проверка YAML:**
- [ ] Файл сохранён с расширением `.yaml`.
- [ ] Имя файла соответствует конвенции именования.
- [ ] AsyncAPI-структура соответствует спецификации.
- [ ] Все строковые значения заключены в кавычки.
- [ ] Отступы выполнены пробелами (не табами).
- [ ] JSON Schema корректно определены в `components`.
- [ ] Kafka bindings настроены для channels.
- [ ] Security schemes определены при необходимости.
- [ ] Examples включены для каждого типа сообщения.

**Цель:** создавать YAML-файлы с описанием Kafka-архитектуры, готовые для production-развёртывания
с полным покрытием функциональных и нефункциональных требований.

---

## 9. Дополнительные рекомендации

### Стиль документирования
- **Структурированность:** YAML для конфигураций.
- **Конкретность:** точные числа партиций, retention, throughput.
- **Примеры:** реальные схемы Avro/JSON Schema.
- **Визуализация:** ASCII-диаграммы для topology.

### Производственные аспекты
- **Именование:** конвенция `{domain}.{entity}.{event}`.
- **Партиционирование:** обоснуй выбор ключа.
- **Retention:** учитывай compliance и storage costs.
- **Версионирование:** планируй эволюцию схем заранее.

### Интеграция с DevOps
- **Infrastructure as Code:** Terraform/Helm конфигурации.
- **CI/CD:** Schema validation в pipeline.
- **Monitoring:** Prometheus/Grafana метрики.
- **Alerting:** PagerDuty/Slack интеграции.

### Disaster Recovery
- **Backup:** MirrorMaker 2.0 для репликации.
- **Recovery:** RTO/RPO требования.
- **Testing:** Chaos engineering практики.
- **Documentation:** Runbooks для операционной команды.
