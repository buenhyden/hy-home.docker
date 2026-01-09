---
trigger: always_on
glob: "**/*"
description: "Debugging: Strategies, Tools, Logging, and Systematic Approaches."
---
# Debugging Standards

## 1. Systematic Approach

- **Reproduce**: First, reliably reproduce the bug.
- **Isolate**: Narrow down to the smallest failing unit.
- **Hypothesize**: Form a hypothesis before changing code.
- **Verify**: Confirm the fix AND ensure no regression.

### Example: Process

**Good**

1. Write a failing test that reproduces the bug.
2. Use debugger/logs to identify root cause.
3. Fix the code.
4. Verify test passes.
5. Run full test suite.

**Bad**
> Making random changes until it "seems to work".

## 2. Logging Best Practices

- **Structured Logs**: Use JSON format with correlation IDs.
- **Levels**: Use DEBUG for verbose, INFO for normal, ERROR for failures.
- **Context**: Include request ID, user ID, timestamps.

### Example: Logging

**Good**

```python
logger.info("User created", extra={"user_id": user.id, "request_id": request_id})
```

**Bad**

```python
print("user created")  # No context, hard to trace
```

## 3. Debugger Tools

- **Python**: `pdb`, `ipdb`, VS Code debugger.
- **JavaScript**: Chrome DevTools, `debugger` statement.
- **Java**: IntelliJ/Eclipse debugger, remote debugging.

## 4. Production Debugging

- **Distributed Tracing**: Use OpenTelemetry, Jaeger, or Zipkin.
- **Error Tracking**: Use Sentry, Rollbar, or Bugsnag.
- **APM**: Use Datadog, New Relic, or Dynatrace.

## 5. Common Pitfalls

- **Heisenbug**: Bug disappears when debugging (timing issues).
- **Fix Symptoms**: Fix the root cause, not just the symptom.
