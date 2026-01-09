---
trigger: always_on
glob: "*"
description: "Project Structure: Universal defaults (Polyrepo & Monorepo)."
---
# Core Project Structure Standards

## 1. Standard Directories

- **Source**: usage of `src/` is mandatory for Polyrepos.
- **Monorepo**: Use `apps/` and `packages/`. Each sub-package must follow the `src/` rule internally.
- **Tests**: `tests/` (Integration/E2E) at root; Unit tests colocated or in `__tests__`.
- **Docs**: `docs/` for architecture/api documentation.
- **Scripts**: `scripts/` for CI/Build/Maintenance tasks.

### Example: Polyrepo

**Good**

```text
my-app/
  ├── src/         # All code here
  ├── tests/       # Standard tests
  └── package.json
```

### Example: Monorepo

**Good**

```text
my-monorepo/
  ├── apps/
  │   └── web/src/
  ├── packages/
  │   └── ui/src/
  └── turbo.json
```

## 2. Root Hygiene

- **No Loose Files**: Root should ONLY contain config files (`.json`, `.toml`, `.js`, `.md`).
- **Logic Ban**: NEVER put application logic (`app.py`, `utils.js`) in the root.

### Example: Hygiene

**Bad**

```text
project/
  ├── auth_logic.py    # MOVED to src/
  ├── helper_utils.js  # MOVED to src/
  └── README.md
```

## 3. Configuration & Meta

- **Tooling**: `package.json`, `pnpm-workspace.yaml`, `Makefile` reside at root.
- **Secrets**: `.env` MUST be git-ignored. `.env.example` MUST be committed.
