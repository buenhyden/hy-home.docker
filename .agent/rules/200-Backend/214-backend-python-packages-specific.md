---
trigger: always_on
glob: "**/*.{py,toml}"
description: "Python Packages: Dependency Management (UV/Poetry) and Libraries."
---
# Python Package Standards

## 1. Dependency Management

- **Tool**: Use `uv` (preferred) or `poetry`. `pip` + `requirements.txt` is legacy.
- **Lockfile**: Always commit `uv.lock` / `poetry.lock`.

### Example: UV

**Good**

```bash
uv pip install pydantic
uv pip compile pyproject.toml -o uv.lock
```

**Bad**

```bash
pip install pydantic # No record in lockfile
```

## 2. Libraries

- **Standard Lib**: Prefer `pathlib` over `os.path`. Prefer `datetime` (UTC) over `time`.
- **Requests**: Use `httpx` for modern Async/Sync support.

### Example: Path

**Good**

```python
from pathlib import Path
p = Path("data") / "file.txt"
```

**Bad**

```python
import os
p = os.path.join("data", "file.txt")
```
