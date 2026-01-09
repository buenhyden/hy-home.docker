---
trigger: always_on
glob: "**/*.py"
description: "Python UV: Modern Package Management, Lockfiles, and Virtual Environments."
---
# Python UV Standards

## 1. Installation & Setup

- **Install**: Use `curl -LsSf https://astral.sh/uv/install.sh | sh`.
- **Replacement**: UV replaces pip, pip-tools, pyenv, and virtualenv.

## 2. Virtual Environments

- **Create**: `uv venv` (creates `.venv` in project root).
- **Activate**: `source .venv/bin/activate` (or `.venv\Scripts\activate` on Windows).

### Example: Setup

**Good**

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

**Bad**

```bash
pip install -r requirements.txt  # Global install, no isolation
```

## 3. Dependency Management

- **Lock**: Use `uv pip compile` to generate `requirements.lock`.
- **Sync**: Use `uv pip sync requirements.lock` for reproducible installs.
- **Add**: Use `uv pip install <package>` then re-compile.

### Example: Lock

**Good**

```bash
uv pip compile requirements.in -o requirements.lock
uv pip sync requirements.lock
```

## 4. Speed Advantages

- **Parallel**: UV is 10-100x faster than pip.
- **Caching**: Efficient caching of downloaded packages.
- **Resolution**: Fast dependency resolution.

## 5. pyproject.toml Integration

- **Modern**: Define dependencies in `pyproject.toml`.
- **Build**: Use `uv pip install -e .` for editable installs.

### Example: pyproject.toml

**Good**

```toml
[project]
name = "myapp"
dependencies = [
    "fastapi>=0.100.0",
    "uvicorn[standard]",
]
```
