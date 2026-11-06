---
title: "Scripts Agent Guide"
version: "0.2.1"
type: "common/agent-guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
---

# Scripts Agent Guide

## Overview

`scripts/` holds the executable gates: validators, hardening checks, hooks,
operation commands and their shared libraries. This guide routes an agent that
changes or runs them. The human guide is [README.md](README.md).

## Scope

`scripts/validation/`, `scripts/hardening/`, `scripts/hooks/`,
`scripts/knowledge/`, `scripts/operations/`, `scripts/security/`,
`scripts/lib/<domain>/` and `scripts/manifest.yaml`.
Policy text is out of scope; a script implements a canonical rule and never
becomes its owner.

## Working Rules

- Register every new, moved or retired script in `scripts/manifest.yaml`; the
  Script Manifest check rejects an unregistered or orphaned script.
- Give a change to `scripts/lib/<domain>/` a behavior test in
  `tests/lib/<domain>/`, and a CLI or entrypoint change a test in
  `tests/validation/`.
- Inspect the selected gates with
  `python3 scripts/validation/run-ci-gate.py --profile changed --explain`
  before running them.
- Never run `pre-commit run` directly. Use
  `scripts/validation/run-ci-precommit.sh --mode local-staged` before a commit.
  An all-files run follows the
  [execution boundary](../.agents/governance/quality-standards.md#4-execution-boundary)
  and its `scripts/validation/run-agent-precommit-all-files.sh` route.
- Generated provider surfaces under `.claude/` and `.codex/` come from
  `scripts/operations/provider_surface_renderer.py`; re-render them, never
  hand-edit them.
- A script never prints, logs or writes a secret value.

## Canonical References

- [Bootstrap](../.agents/governance/bootstrap.md),
  [quality standards](../.agents/governance/quality-standards.md),
  [approval boundaries](../.agents/governance/approval-boundaries.md),
  [GitHub governance](../.agents/governance/github-governance.md).
- Roles: [`qa-engineer`](../.agents/roles/qa-engineer.md),
  [`ci-cd-engineer`](../.agents/roles/ci-cd-engineer.md),
  [`hook-developer`](../.agents/roles/hook-developer.md).
- Skills: [`ci-cd-patterns`](../.agents/skills/ci-cd-patterns/SKILL.md),
  [`style-validation`](../.agents/skills/style-validation/SKILL.md),
  [`test-authoring`](../.agents/skills/test-authoring/SKILL.md).
- Hook rule: [`warn-pre-commit-manual`](../.agents/governance/hooks/hookify.warn-pre-commit-manual.md).
- Native hooks: `.claude/hooks/` and `.codex/hooks.json` call
  `scripts/hooks/agent-event-hook.sh`, which calls
  `scripts/hooks/post-tool-validate.sh` for post-edit validation.
- Provider loading: [Claude adapter](../.claude/provider.md),
  [Codex adapter](../.codex/provider.md).

## Verification

- `python3 scripts/validation/check-script-manifest.py`
- `python3 scripts/operations/provider_surface_renderer.py --check`
- `python3 scripts/validation/check-agent-governance-contract.py`
- `bash scripts/validation/run-ci-precommit.sh --mode local-staged`

## Related Documents

- [Scripts README](README.md)
- [Tests agent guide](../tests/AGENTS.md)
