---
trigger: always_on
glob: "**/*.{py,js,ts,go,java}"
description: "Security Logging (OWASP A09): Auth logging, correlation IDs, and sensitive data protection."
---
# Security Logging & Monitoring Standards (OWASP A09)

## 1. What to Log

- **Authentication**: Successful and FAILED login attempts (User ID, IP).
- **Authorization**: Access denials (401/403).
- **Critical Ops**: Password changes, role updates, financial transactions.
- **Startup/Shutdown**: Server lifecycle events.

## 2. Log Content & Security

- **Correlation IDs**: Attach a `X-Request-ID` to all logs to trace requests across microservices.
- **NO Sensitive Data**: NEVER log passwords, API keys, or raw tokens. Mask PII (credit cards, emails).
- **Time**: Use ISO 8601 timestamps (`2023-01-01T12:00:00Z`).

## 3. Monitoring

- **Centralized**: Aggregate logs (ELK, Splunk, Datadog). Don't just log to local files.
- **Alerting**: Set alerts for high failure rates (e.g., >10 failed logins/min).

### Example: Secure Logging (Python)

#### Good

```python
import logging
logger = logging.getLogger(__name__)

def login(username, password):
    # ... check creds ...
    if failed:
        # LOG USERNAME, BUT NEVER PASSWORD
        logger.warning("Auth failed", extra={
            "user": username, 
            "ip": request.ip, 
            "request_id": request.id
        })
        return False
```

#### Bad

```python
# LOGGING PASSWORD - SECURITY RISK
logger.info(f"Login failed for {username} with password {password}")
```
