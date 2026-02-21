# Utilities & Automation Scripts

This directory is reserved for repository maintenance, utility scripts, and automation triggers.

## Purpose

- Hold scripts that humans or CI/CD pipelines run to manage the project environment.
- Separate development toolings from application logic (`src/`) and operational deployments (`runbooks/`).
- Serve as the execution layer for tasks like dataset syncing, pre-commit hook setups, or database seeding.

## Guidelines

Ensure cross-platform compatibility where possible, or document explicit dependencies.

### Agent Workflow Standardization

Any automation scripts or workflows added to this directory MUST comply with the **Idempotent and Deterministic** principles defined in `.agent/rules/0200-workflows-pillar-standard.md`.

- **Idempotency**: Running a script twice should have the same effect as running it once (no corrupted state or duplicate data).
- **Clear Boundaries**: Scripts should have single responsibilities and handle failures gracefully.
