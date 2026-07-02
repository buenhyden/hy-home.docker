---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-17-scripts-ci-qa-cleanup.md -->

# Scripts CI/CD & QA Cleanup Plan

## Overview

This plan implements the approved root `scripts/` cleanup for CI/CD, QA, hook,
knowledge, and manual-operation entrypoints.

## Context

This plan supersedes the deletion non-goals in
`2026-05-09-scripts-lifecycle-contract-cleanup.md` for the root `scripts/`
surface only. Historical `docs/01`, `docs/02`, completed `docs/04`, and
governance memory references remain audit evidence unless they are active
instructions.

## Goals & In-Scope

- Delete redundant root script entrypoints and keep one canonical command per behavior.
- Preserve CI-safe Compose structural validation.
- Preserve real local preflight checks as `validate-docker-compose.sh --preflight`.
- Replace active docs references to removed scripts.
- Keep service-local `infra/**/scripts/` out of scope.

## Non-Goals & Out-of-Scope

- Do not change service-local `infra/**/scripts/`.
- Do not rewrite historical `docs/01`, `docs/02`, completed `docs/04`, or governance memory evidence only because it references deleted scripts.
- Do not change Docker Compose service behavior beyond the approved script cleanup.

## Work Breakdown

| Task | Description | Files / Docs Affected | Validation Criteria |
| --- | --- | --- | --- |
| PLN-SCRIPT-001 | Consolidate Compose preflight into explicit validator mode | `scripts/validation/validate-docker-compose.sh` | Normal mode still creates only temporary CI dummy files; `--preflight` creates none |
| PLN-SCRIPT-002 | Remove redundant root script entrypoints | `scripts/hardening/`, `scripts/validation/`, `scripts/operations/` | Deleted scripts are absent and no active references remain |
| PLN-SCRIPT-003 | Update repository script contracts | `scripts/validation/check-repo-contracts.sh` | Current inventory matches tracked scripts; deleted-script references fail in active surfaces |
| PLN-SCRIPT-004 | Update active docs and runtime hook surface | `README.md`, `scripts/README.md`, `docs/03.specs/**`, `docs/05.operations/**`, `.claude/settings.json` | Active commands use canonical replacements and hook routing is dispatcher-based |
| PLN-SCRIPT-005 | Refresh generated navigation | `docs/90.references/llm-wiki/llm-wiki-index.md`, `graphify-out/` | Generated index is fresh; Graphify refresh attempted when available |

## Verification Plan

| ID | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- |
| VAL-SCRIPT-001 | Bash syntax | `bash -n .claude/hooks/*.sh scripts/**/*.sh` | No syntax errors |
| VAL-SCRIPT-002 | JSON syntax | `python3 -m json.tool .claude/settings.json`; `python3 -m json.tool .codex/hooks.json` | JSON parses |
| VAL-SCRIPT-003 | Hook dispatcher behavior | Simulate `SessionStart`, `PreToolUse`, and `PostToolUse` payloads | Hook commands exit successfully |
| VAL-SCRIPT-004 | Repository contracts | `bash scripts/validation/check-repo-contracts.sh` | failures=0 |
| VAL-SCRIPT-005 | Docs traceability | `bash scripts/validation/check-doc-traceability.sh` | failures=0 |
| VAL-SCRIPT-006 | Compose validation | `bash scripts/validation/validate-docker-compose.sh` | Pass |
| VAL-SCRIPT-007 | Real preflight mode | `bash scripts/validation/validate-docker-compose.sh --preflight` | Pass or explicitly skipped when local prerequisites are absent |
| VAL-SCRIPT-008 | Baseline gates | template, quickwin, and hardening checks | Pass |
| VAL-SCRIPT-009 | Generated navigation | `bash scripts/knowledge/generate-llm-wiki-index.sh --check`; `bash scripts/knowledge/report-graphify-health.sh` | Fresh index; Graphify health reported |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Historical docs appear to reference deleted scripts | Medium | Allow historical/reference records in `check-repo-contracts.sh`; update active surfaces only |
| Preflight behavior regresses | High | Keep `--preflight` non-mutating and validate it separately from normal mode |
| Secret values leak through replacement procedures | High | Keep TLS and Vault procedures procedural; never instruct users to paste generated secrets into docs, PRs, summaries, or logs |
| Hook routing becomes unclear | Medium | Remove inline Graphify shell and rely on `.claude/hooks/docker-compose-pre.sh` -> `scripts/hooks/agent-event-hook.sh` |

## Completion Criteria

- [x] Redundant root script entrypoints removed or consolidated into canonical commands.
- [x] Active docs and runtime hook surfaces reference canonical commands.
- [x] Validation commands in this plan pass or explicitly record local prerequisite limits.
- [x] Generated navigation is refreshed or verified fresh.

## Related Documents

- [Scripts README](../../../scripts/README.md)
- [Execution Task](../tasks/2026-05-17-scripts-ci-qa-cleanup.md)
- [Repository contract checker](../../../scripts/validation/check-repo-contracts.sh)
- [Prior scripts lifecycle cleanup plan](./2026-05-09-scripts-lifecycle-contract-cleanup.md)
- [Harness Agent-first validation runbook](../../05.operations/runbooks/00-workspace/harness-agent-first-engineering-validation.md)
