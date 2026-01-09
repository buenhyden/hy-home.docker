---
trigger: always_on
glob: "**/*.py"
description: "Requests: HTTP Client Best Practices."
---
# Requests Standards

## 1. Session Usage

- **Reuse Sessions**: ALWAYS use a `requests.Session()` object for multiple calls to the same host. This enables connection pooling and keeps-alive.

### Example: Session

**Good**

```python
with requests.Session() as session:
    session.get('https://api.example.com/1')
    session.get('https://api.example.com/2')
```

## 2. Reliability

- **Timeouts**: NEVER make a request without a `timeout`. Prefer a tuple `(connect, read)` e.g., `timeout=(3.05, 27)`.
- **Retries**: Mount an `HTTPAdapter` with `urllib3.util.retry.Retry` to handle transient failures (5xx, network errors) automatically.

### Example: Retry Adapter

**Good**

```python
adapter = HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1))
session.mount("https://", adapter)
```

## 3. Error Handling

- **Raise for Status**: Call `response.raise_for_status()` to ensure 4xx/5xx responses are treated as exceptions, unless you explicitly handle them.
