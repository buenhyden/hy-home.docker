---
trigger: always_on
glob: "**/*.{js,ts,php,py,go}"
description: "Third Party Integration: Handling external APIs and services."
---
# Third-Party Integration Standards

## 1. Security

- **Credentials**: NEVER hardcode API keys. Use Environment Variables. (See [010-core-git-specific.md](./010-core-git-specific.md) for git security).
- **Output**: Do not log raw API responses if they contain PII or secrets.

## 2. Reliability

- **Error Handling**: Wrap external calls in `try/catch`. Handle timeouts and 5xx errors specifically.
- **Retries**: Implement exponential backoff for transient failures (networking, rate limits).
- **Circuit Breaker**: Use circuit breakers for high-volume dependencies to fail fast.

## 3. Abstraction

- **Service Layer**: Wrap third-party SDKs/clients in your own Service/Interface. Do not leak external implementation details into domain logic.
- **Testing**: Mock external services in Unit Tests. Use integration tests for actual connectivity.

## See Also

- [050-core-debugging-specific.md](./050-core-debugging-specific.md) - Error handling and logging
- [000-core-general.md](./000-core-general.md) - Dependency injection principles
