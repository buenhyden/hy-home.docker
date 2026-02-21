---
trigger: always_on
glob: ["**/*.py"]
description: "Python Security Standards: Enforces injection prevention, safe deserialization, and async security tool patterns."
---

# Python Security Standards

- **Role**: Python Security Specialist
- **Purpose**: Define standards for writing secure, resilient Python code and developing security-focused automation tools.
- **Activates When**: Developing application backend logic, handling file systems, or writing async cybersecurity utilities in Python.

**Trigger**: always_on — Apply during the development of Python-based application and security assets.

## 1. Standards

### Principles

- **[REQ-PY_SEC-01] Parameterized Command Execution**
  - All external commands and database queries MUST use parameterized inputs. Use `subprocess.run()` with `shell=False` or a list of arguments.
- **[REQ-PY_SEC-02] Path Normalization & Guarding**
  - File system paths MUST be resolved and validated using `pathlib` to prevent path traversal attacks.
- **[REQ-PY_SEC-03] Safe Deserialization**
  - Untrusted data MUST NOT be deserialized using `pickle`. Use `json.loads()` or `yaml.safe_load()` for structured data interchange.

### Security Framework

| Domain | Requirement ID | Critical Action |
| --- | --- | --- |
| Injection | [REQ-PY_SEC-04] | Use ORM / Parameterization |
| YAML | [REQ-PY_SEC-05] | Always use `safe_load()` |
| File I/O | [REQ-PY_SEC-06] | Validate `Path.resolve()` prefix |
| Crypto | [REQ-PY_SEC-07] | Use `cryptography` library |

### Must

- **[REQ-PY_SEC-08] Async Context Management**
  - Network-bound security tools MUST utilize `asyncio` and `httpx`/`aiohttp` to ensure efficient, non-blocking execution.
- **[REQ-PY_SEC-09] Strict Path Check**
  - Every resolved user-provided path MUST be verified to start with the expected base directory prefix.
- **[REQ-PY_SEC-10] Secure Defaults (Frameworks)**
  - Flask/Django/FastAPI applications MUST run with `DEBUG=False` in production and enforce secure cookie attributes.

### Must Not

- **[BAN-PY_SEC-01] Shell Interpellation**
  - Python code MUST NOT use `os.system()` or `subprocess.run(shell=True)` with untrusted string interpolation.
- **[BAN-PY_SEC-02] Brute-Force Math**
  - Avoid using `Math.random` or the `random` module for cryptographic secrets; use the `secrets` module (CSPRNG).

### Failure Handling

- **Stop Condition**: Stop execution if a path traversal attempt is detected or a deserialization signature fails validation.

## 2. Procedures

- **[PROC-PY_SEC-01] Dependency Audit**
  - IF adding a new Python package THEN MUST run `pip-audit` to check for known security vulnerabilities.
- **[PROC-PY_SEC-02] Secret Scanning**
  - Verify that no PII or API tokens are hardcoded in the `.py` source files before commit.

## 3. Examples

### Path Traversal Guard

```python
from pathlib import Path

base_dir = Path("/app/uploads")
user_path = (base_dir / user_input).resolve()
if not str(user_path).startswith(str(base_dir)):
    raise ValueError("Path traversal attempt detected.")
```

## 4. Validation Criteria

- **[VAL-PY_SEC-01] Bandit Scan Pass**
  - [ ] Automated SAST tools (e.g., Bandit) return a zero-vulnerability report for the current Python code.
- **[VAL-PY_SEC-02] Path Integrity**
  - [ ] Unit tests confirm that `../` sequences in user input do not escape the designated upload directory.
- **[VAL-PY_SEC-03] Async Throughput**
  - [ ] Concurrent network scans demonstrate correct back-off and rate-limiting without thread exhaustion.
