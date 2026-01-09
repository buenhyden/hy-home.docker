---
trigger: always_on
glob: "**/{pyproject.toml,setup.py,MANIFEST.in}"
description: "Python Packaging: Standards for setuptools and pyproject.toml configuration."
---
# Python Packaging Standards (Setuptools)

## 1. Project Structure

- **SRC Layout**: Use `src/` directory to isolate package code.
  - `src/package_name/`
  - `tests/`
  - `pyproject.toml`
  - `README.md`
- **Avoid Flat Layout**: Prevents import errors and test pollution.

## 2. Configuration (`pyproject.toml`)

- **Standard**: Use `pyproject.toml` (PEP 517/518) for *all* metadata and build configuration.
- **Build Backend**:

  ```toml
  [build-system]
  requires = ["setuptools>=61", "setuptools-scm>=8"]
  build-backend = "setuptools.build_meta"
  ```

- **Dependencies**: Declare `dependencies` and `optional-dependencies` (e.g., `[project.optional-dependencies] dev = [...]`).
- **Dynamic Versioning**: Use `setuptools-scm` to derive versions from Git tags.

## 3. Setup.py

- **Deprecated**: Avoid `setup.py` unless strictly necessary for compilation of C extensions.
- **Metadata**: Do NOT keep metadata in `setup.py` if using `pyproject.toml`.

## 4. Distribution

- **Build**: Use `python -m build`.
- **Test**: Upload to TestPyPI first using `twine`.
- **Ignore**: Ensure `dist/`, `build/`, `*.egg-info` are in `.gitignore`.
