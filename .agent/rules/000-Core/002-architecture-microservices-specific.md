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

## 4. Communication Patterns (Advanced)

### Circuit Breaker

- **Purpose**: Prevent cascading failures when a dependent service is down.
- **Implementation**: Wrap external calls.
  - **Open**: Fail fast immediately.
  - **Half-Open**: Test with limited requests.
  - **Closed**: Normal operation.

### Saga Pattern (Distributed Transactions)

- **Goal**: Maintain data consistency across services without 2PC (Two-Phase Commit).
- **Choreography**: Services emit events, others react. Simple, loose coupling.
- **Orchestration**: Central coordinator commands services. Better visibility for complex flows.

### Event Sourcing

- **Concept**: Store state as a sequence of events, not just current snapshot.
- **Benefit**: Audit trail, temporal queries, ability to replay history.
- **Snapshot**: Periodically save current state to optimize read performance.

## 5. Service Discovery & Gateway

- **Registry**: Services register heartbeat. Clients query registry for active instances.
- **Gateway**: Single entry point. Handles auth, rate limiting, and routing to internal services.

## See Also

- [020-core-project-structure-specific.md](./020-core-project-structure-specific.md) - Project Structure
- [200-Backend/205-backend-api-standards.md](../200-Backend/205-backend-api-standards.md) - API Standards
