---
trigger: always_on
glob: "**/*"
description: "Backend Core: 12-Factor, API Design, Observability, and Reliability."
---
# Backend General Standards

## 1. Architectural Foundations

- **12-Factor App**: Config in Envs, Stateless Processes, Disposability.
- **Modular Monolith First**: Extract microservices only when scaling demands it.
- **Graceful Shutdown**: Finish in-flight requests before exit (SIGTERM handling).

## 2. API Excellence

- **Consistency**: Use a unified error envelope (`{ "error": { "code": ..., "message": ... } }`).
- **Pagination**: NEVER return unbounded lists. Use `limit/offset` or cursors.
- **Rate Limiting**: Implement at gateway or app level.

### Example: API Envelope

**Good**

```json
{ "data": { "id": 1 }, "links": { "self": "/api/v1/users/1" } }
```

**Bad**

```json
{ "id": 1 } // Naked objects break extensibility
```

## 3. Request Validation

- **Early Fail**: Validate inputs at the API edge (Controller/Route) using schemas.
- **Schema Libraries**: Use Pydantic, Zod, Valibot, or equivalent.

## 4. Observability & Health

- **Health Checks**: Expose `/health` (liveness) and `/ready` (dependency checks).
- **Correlation IDs**: Propagate `X-Request-ID` through all logs.
- **Metrics**: Track P50, P95, P99 latency, not just averages.

### Example: Readiness

**Good**

```python
@app.get("/ready")
def ready():
    if db.is_connected():
        return {"status": "ok"}
    raise HTTPException(503, "DB not ready")
```

## 5. Async & Background Tasks

- **Offload**: Use message queues for tasks > 100ms.
- **Timeouts**: Every external call (DB, HTTP) MUST have a timeout configured.
