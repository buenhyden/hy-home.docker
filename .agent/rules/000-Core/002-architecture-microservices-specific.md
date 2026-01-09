---
trigger: always_on
glob: "**/*"
description: "Microservices Architecture: Design Patterns, Communication, and Data Management."
---
# Microservices Architecture Standards

## 1. Design Principles

- **Single Responsibility**: Each service should focus on one business capability.
- **Database per Service**: Avoid shared databases to ensure loose coupling.
- **API First**: Define contracts (OpenAPI/gRPC) before implementation.

## 2. Communication Patterns

- **Synchronous**: REST/gRPC for external-facing or simple internal calls. Use Circuit Breakers.
- **Asynchronous**: Message brokers (RabbitMQ, Kafka) for inter-service events to decouple systems.

### Example: Circuit Breaker

**Good**

```python
# Using a library like pybreaker or resilience4j
@circuit_breaker
def call_inventory_service(sku):
    ...
```

**Bad**

```python
def call_inventory_service(sku):
    # No handling for timeouts or failures cascading
    return requests.get(f"http://inventory/{sku}")
```

## 3. Data Consistency

- **Saga Pattern**: Use choreography or orchestration for distributed transactions.
- **Event Sourcing**: Store state changes as a sequence of events for auditability and replay.

## 4. API Gateway

- Use an API Gateway (Kong, Nginx, or Cloud native) for:
  - Authentication/Authorization
  - Rate Limiting
  - Request Routing

### Example: Gateway Routing

**Good**
> Client requests `api.example.com/orders` -> Gateway -> Order Service

**Bad**
> Client requests many individual service IPs directly.
