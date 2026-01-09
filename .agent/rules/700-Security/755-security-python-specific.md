---
trigger: always_on
glob: "**/*.py"
description: "Python Security: OWASP Vulnerabilities, Input Validation, and Safe Coding."
---
# Python Security Standards

## 1. Injection Prevention

- **SQL**: Use parameterized queries or ORM. NEVER string concatenation.
- **Command**: Avoid `os.system()`, use `subprocess.run()` with `shell=False`.
- **Template**: Use auto-escaping templates. Avoid `| safe` with user input.

### Example: SQL Injection

**Good**

```python
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

**Bad**

```python
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

## 2. Path Traversal

- **Validate Paths**: Use `pathlib` to resolve and validate paths.
- **Whitelist**: Restrict file access to allowed directories.

### Example: Path

**Good**

```python
from pathlib import Path

base_dir = Path("/app/uploads")
user_path = (base_dir / user_input).resolve()
if not str(user_path).startswith(str(base_dir)):
    raise ValueError("Path traversal attempt")
```

## 3. Deserialization

- **Avoid Pickle**: Never unpickle untrusted data. Use JSON.
- **YAML**: Use `yaml.safe_load()`, never `yaml.load()`.

### Example: Deserialization

**Good**

```python
import json
data = json.loads(user_input)
```

**Bad**

```python
import pickle
data = pickle.loads(user_input)  # Remote code execution!
```

## 4. Secrets Management

- **Environment Variables**: Use `os.environ` or `python-dotenv`.
- **No Hardcoding**: Never commit secrets to Git.

### Example: Secrets

**Good**

```python
import os
api_key = os.environ.get("API_KEY")
```

**Bad**

```python
API_KEY = "sk-hardcoded-secret-key"  # Exposed in Git history
```

## 5. Dependencies

- **Audit**: Run `pip-audit` or `safety check` regularly.
- **Pin Versions**: Use lockfiles (`poetry.lock`, `requirements.txt` with hashes).

## 6. Access Control & Design (OWASP)

- **Principle**: Fail Closed (Deny by default).
- **Insecure Design**: Validate all input boundaries (Length/Type). Do not trust client IDs for ownership (IDOR).
- **Error Handling**: Fail securely. Do NOT return stack traces to clients. Log detailed errors internally.
- **Misconfiguration**:
  - Ensure `DEBUG=False` in production.
  - Set `SESSION_COOKIE_SECURE=True`.

## 7. Framework Specifics

- **Flask**: Use `@login_required`.
- **Django**: Use `LoginRequiredMixin`.
- **FastAPI**: Use `Depends(get_current_user)`.
