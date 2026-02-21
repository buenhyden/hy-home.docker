---
trigger: model_decision
glob: ["**/server/**", "**/backend/**", "**/api/**", "**/services/**"]
description: "Node.js Backend Standards: Enforces modern ES6+ syntax, asynchronous I/O (async/await), and secure Express/Fastify patterns."
---

# Node.js Backend Standards

- **Role**: Senior Node.js Backend Architect
- **Purpose**: Define standards for writing performant, secure, and scalable server-side logic using Node.js and its ecosystem of frameworks.
- **Activates When**: Developing server-side modules, configuring API routing, or managing backend process lifecycles.

**Trigger**: model_decision — Apply during the design and implementation of Node.js based backend features.

## 1. Standards

### Principles

- **[REQ-NODE-01] Non-Blocking Path Primacy**
  - All I/O operations MUST use asynchronous `async/await` patterns. Synchronous blocking calls (e.g., `fs.readFileSync`) are STRICTLY PROHIBITED in the main execution path.
- **[REQ-NODE-02] Scalable Resource Pooling**
  - Database and external service connections MUST utilize connection pooling and be managed via singleton-like lifecycle patterns.
- **[REQ-NODE-03] Fail-Safe Middleware Orchestration**
  - Error handling MUST be centralized via middleware or global error catchers. Unhandled promise rejections MUST lead to a graceful process restart.

### Framework Baseline (Express/Fastify)

| Category | Requirement ID | Critical Action |
| --- | --- | --- |
| Security | [REQ-NODE-04] | Use `helmet` and `cors` configuration |
| Validation | [REQ-NODE-05] | Use schema-based validation (e.g., Zod/Joi) |
| Performance | [REQ-NODE-06] | Use `compression` for response payloads |
| Monitoring | [REQ-NODE-07] | Structured logs with `Winston` or `Pino` |

### Must

- **[REQ-NODE-08] Environment-Driven Configuration**
  - All application configuration (DB URLs, Secrets, Log Levels) MUST be sourced from process environment variables.
- **[REQ-NODE-09] Explicit Versioned Routing**
  - APIs MUST implement versioning (e.g., `/v1/`) to ensure backward compatibility for clients.
- **[REQ-NODE-10] Native Stream Handling**
  - Large data operations (File uploads, log exports) MUST utilize Node.js `Streams` to prevent heap exhaustion.

### Must Not

- **[BAN-NODE-01] Magic Variable Scoping**
  - Avoid using `global` or attaching variables to the native `process` object; use formal dependency injection or module exports.
- **[BAN-NODE-02] Silent Catches**
  - Code MUST NOT catch asynchronous errors without logging the full stack trace and associated request context.

### Failure Handling

- **Stop Condition**: Stop feature execution if a database query is identified to be vulnerable to injection (e.g., using string concatenation instead of prepared statements).

## 2. Procedures

- **[PROC-NODE-01] Dependency Audit**
  - IF adding a new NPM package THEN MUST run `npm audit` or `snyk` to verify its security posture.
- **[PROC-NODE-02] Memory Profiling**
  - Regularly monitor the `process.memoryUsage()` metrics in the APM to identify and resolve potential memory leaks.

## 3. Examples

### Secure Async Route (Good)

```javascript
router.get('/user/:id', async (req, res, next) => {
  try {
    const user = await userService.get(req.params.id);
    res.json(user);
  } catch (err) {
    next(err); // Pass to global handler
  }
});
```

## 4. Validation Criteria

- **[VAL-NODE-01] Thread Safety**
  - [ ] audit confirms no CPU-bound operations are performed in the main event loop thread without worker partitioning.
- **[VAL-NODE-02] Middleware Presence**
  - [ ] Security scan confirms that `helmet` and CSRF protection are active for all public-facing routes.
- **[VAL-NODE-03] Log Quality**
  - [ ] Central aggregator confirms that 100% of backend logs are structured JSON with valid `trace_id`.
