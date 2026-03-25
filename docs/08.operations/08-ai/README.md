# 08-ai Operations

Operational policies and governance for AI services.

## Policies

### 1. Resource Governance
- **GPU Quotas**: Services must use Docker Compose reservations for GPU access.
- **Model Lifecycle**: Models should be pulled to the persistent `${DEFAULT_AI_MODEL_DIR}` to avoid redundant downloads.

### 2. Security
- **SSO Enforcement**: All AI interfaces must be behind the `sso-auth` middleware.
- **Data Privacy**: Local LLMs are preferred for sensitive data processing to ensure zero data leakage to external APIs.

## References
- [Global Operations Index](../README.md)
