# Utilities & Automation Scripts (`scripts/`)

This directory is reserved for repository maintenance, utility scripts, and automation triggers.

## 1. Necessity and Purpose

This folder is necessary to encapsulate build, test, and environment scaffolding tools.

- Separation of Concerns: It deliberately separates development tooling from application logic (`src/`/`web/`) and operational deployments (`runbooks/`).
- Consistent Execution: It serves as the common execution layer for tasks like dataset syncing, pre-commit hook setups, or database seeding across developer machines.

## 2. Required Content

- **Content**: Small, target-specific bash, Python, or Node scripts (`.sh`, `.py`, `.js`).
- Ensure cross-platform compatibility where possible, or document explicit OS dependencies at the top of the file.

## 3. Agent Workflow Standardization

Any automation scripts or workflows added to this directory MUST comply with the **Idempotent and Deterministic** principles defined in `.agent/rules/0200-workflows-pillar-standard.md`.

- **Idempotency**: Running a script twice should have the exact same effect as running it once (e.g., no corrupted state or duplicate data).
- **Clear Boundaries**: Scripts should have single responsibilities and handle failures gracefully.
- **No Hardcoded Secrets**: Scripts here MUST NEVER contain hardcoded API keys or passwords. They must fetch credentials securely from environment variables.
