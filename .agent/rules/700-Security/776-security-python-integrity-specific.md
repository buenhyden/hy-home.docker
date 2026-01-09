---
trigger: always_on
glob: "**/*.py"
description: "Python Security: Prevention of software and data integrity failures (OWASP A08)."
---
# Python Integrity Standards (OWASP A08)

## 1. Secure Deserialization

- **Pickle**: NEVER use `pickle`, `marshal`, or `shelve` on untrusted input.
- **YAML**: Always use `yaml.safe_load()`.
- **JSON**: Use JSON for untrusted data transfer.

## 2. Secure Downloads & Installs

- **Hashing**: Verify checksums of downloaded files.
- **Pip**: Pin dependencies with hashes in `requirements.txt`.
- **HTTPS**: Enforce TLS for all update mechanisms.

## 3. Dangerous Functions

- **Eval/Exec**: Avoid `eval()`, `exec()`, `compile()` with user input.
- **Subprocess**: Avoid `shell=True`. Use `shlex.split()` for command parsing.

### Example: Deserialization

#### Good

```python
import yaml
import json

# Safe YAML
data = yaml.safe_load(user_input)

# Safe JSON
data = json.loads(user_input)
```

#### Bad

```python
import pickle
import yaml

# Unsafe
data = pickle.loads(user_input)
data = yaml.load(user_input, Loader=yaml.Loader)
```
