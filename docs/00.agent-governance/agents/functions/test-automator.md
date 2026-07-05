---
layer: agentic
---

# test-automator

## Overview

Test automation function for the `hy-home.docker` workspace. Plans and executes unit and
integration checks for Docker Compose services and repository tooling, reusing existing
validation scripts rather than introducing parallel runners.

## Purpose

Give the `qa-engineer` a consistent, auditable way to validate service and tooling behavior
before changes are marked complete.

## Scope

**Covers:**

- Integration validation via `scripts/validation/validate-docker-compose.sh`
- Repository contract checks via `scripts/validation/check-repo-contracts.sh`
- Test evidence capture for `docs/04.execution/tasks/`

**Excludes:**

- End-to-end runtime smoke tests (see `e2e-testing`)
- CI pipeline design (see `deployment-pipeline-design`)

## Structure

- Identify changed services/tooling → select existing validation scripts → run → capture evidence

## Agents

- **qa-engineer** — primary caller

## Skills

- Runtime mirror: `.claude/skills/test-automator/skill.md`

## Usage

- Trigger when validating service or tooling changes before completion.
- **Inputs:** changed paths, target services
- **Outputs:** test evidence in `_workspace/repo-support/` and task docs

## Artifacts

- `_workspace/repo-support/test_<date>.md`

## Related Documents

- `../../scopes/common.md`
- `../../scopes/qa.md`
- `../functions/e2e-testing.md`
- `../README.md`
