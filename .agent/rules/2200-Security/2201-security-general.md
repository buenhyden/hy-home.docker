---
trigger: model_decision
glob: ["**/*"]
description: "Security Strategy: High-level principles, Zero Trust architecture, defense in depth, and security index."
---

# 0750-Security-General

- **Role**: Security Architect
- **Purpose**: Enforce high-level security principles, Zero Trust patterns, and define the security rule index.
- **Activates When**: Assessing architecture, writing code examples, or performing general security reviews.

## 1. Standards

### 1.1 Principles

- **[REQ-SEC-GEN-01] Security First**: Default to the most secure option. Complexity is the enemy of security.
- **[REQ-SEC-GEN-02] Deny by Default**: Access MUST be denied unless explicitly allowed.
- **[REQ-SEC-GEN-03] Defense in Depth**: Defenses MUST be layered (e.g., WAF + Input Validation + DB constraints).
- **[REQ-SEC-GEN-04] Zero Trust**: Internal services MUST NOT implicitly trust other internal services.

### 1.2 Scope

- **In-Scope**: General security principles, Zero Trust patterns, Reliability patterns.
- **Out-of-Scope**: Specific Language rules (see 0751/0755), Infrastructure rules (see 0200).

### 1.3 Inputs & Outputs

- **Inputs**: Code examples, Architecture designs.
- **Outputs**: Secure patterns, Validation results.

### 1.4 Must / Must Not

- **[REQ-SEC-ZT-01] Verify Identity**: Services MUST verify identity tokens for every request.
- **[REQ-SEC-ZT-02] Validate Inputs**: Services MUST validate all input data regardless of source.
- **[REQ-SEC-ZT-03] Least Privilege**: Permissions MUST be scoped to the minimum required.
- **[BAN-SEC-GEN-01] Implicit Trust**: Code MUST NOT assume a request is safe just because it originates from the internal network.

## 2. Procedures

### 2.1 Zero Trust Implementation

1. **Verify Identity**: Check `auth_token` validity.
2. **Validate Data**: Ensure payload matches schema.
3. **Check Permissions**: Assert required scopes.
4. **Process**: Execute logic.

### 2.2 Reliability Pattern

1. **Timeout**: Set explicit timeouts for external calls.
2. **Retry**: Implement exponential backoff for transient errors.
3. **Circuit Breaker**: Fail fast if dependency is down.

## 3. Examples

### 3.1 Zero Trust (Python)

```python
# VULNERABILITY: Implicit trust
def internal_api(data):
    return process(data)  # No validation

# ZERO TRUST: Verify everything
def internal_api(data, auth_token):
    # 1. Verify service identity
    if not verify_service_token(auth_token):
        raise UnauthorizedError("Service authentication failed")

    # 2. Validate request data
    if not validate_request(data):
        raise ValidationError("Request validation failed")

    # 3. Check permissions
    if not check_permissions(auth_token, required_permissions=['write']):
        raise ForbiddenError("Insufficient permissions")

    # 4. Process with least privilege
    return process(data)
```

### 3.2 Reliability (Python)

```python
# VULNERABILITY: No error handling
response = requests.get(api_url)

# SECURE: Retry with exponential backoff
import time
import requests
from requests.exceptions import RequestException

for attempt in range(3):  # Max 3 attempts
    try:
        response = requests.get(
            api_url,
            timeout=30,      # Prevent hanging
            verify=True       # Verify SSL certificates
        )
        if response.status_code == 200:
            break
    except RequestException as e:
        if attempt < 2:
            time.sleep(2 ** attempt)  # Exponential backoff
        else:
            raise
```

## 4. Validation Criteria

- [ ] **[VAL-SEC-GEN-01]** Zero Trust: Identity and Input validation exist for internal APIs.
- [ ] **[VAL-SEC-GEN-02]** Least Privilege: Permissions check exists before processing.
- [ ] **[VAL-SEC-GEN-03]** Reliability: Timeouts and Retries are configured for network calls.

## 5. Security Index (References)

- **Auth & Guardrails**: [0200-security-guardrails.md](./0200-security-guardrails.md)
- **OWASP Standards**: [760-security-owasp-standards.md](./760-security-owasp-standards.md)
- **JavaScript/TS**: [751-security-javascript-typescript.md](./751-security-javascript-typescript.md)
- **Python**: [755-security-python-specific.md](./755-security-python-specific.md)
- **AI Safety**: [790-security-ai-safety-specific.md](./790-security-ai-safety-specific.md)
