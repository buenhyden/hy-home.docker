---
title: "Stale Agent Paths Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0024"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Stale Agent Paths Task

## Overview

### Objective

Execute W40: find repository paths named in `.agents/`, `.claude/`, and
`.codex/` that no longer exist, and correct them. This Task owns criterion 35
only.

## Inputs and Authorization

The original request asks for outdated statements in `.agents/`, `.claude/`,
and `.codex/` to be found and corrected. On 2026-10-29 the owner asked for the
request review to continue through to merge. The input is `main` at merged
PR #621. The authorization covers path corrections in those surfaces, this
branch, its pull request, and merge.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0024 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0024 | ready | in-progress | #objective |
| SPEC-0212-TSK-0024 | in-progress | completed | #evidence |

### Scan

Every backticked path under a repository root (`scripts/`, `docs/`, `infra/`,
`labs/`, `.agents/`, `.claude/`, `.codex/`, `.github/`, `tests/`, `secrets/`,
`_workspace/`) in the Markdown, YAML, TOML, and JSON files of the three
surfaces was compared with the tracked tree.

| Path named | Where | Decision |
| --- | --- | --- |
| `docs/05.operations/runbooks/0009-release-management.md` | `.agents/governance/github-governance.md` | Stale; corrected to `runbooks/10-platform-and-backup/0009-release-management.md` |
| `scripts/classify-changed-files.sh` | `style-validation` skill | Kept; a link relative to the skill's own `scripts/` |
| `scripts/static-checks.sh` | `infra-validate` skill | Kept; a link relative to the skill's own `scripts/` |
| `.codex/skills/` | `.codex/provider.md` | Kept; the text states that it is absent |
| `docs/01`, `docs/05`, `docs/90`, `docs/99`, `docs/...` | Rule and hook text | Kept; stage ranges, not paths |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Path existence scan | 35 | W40 | Backticked repository paths in `.agents/`, `.claude/`, `.codex/` against `git ls-files` | `main`@`b2c6d3eee` | PASS | One stale path, corrected | required | - |
| Governance contract | 35 | W40 | `check-agent-governance-contract.py` | This branch | PASS | 0 failures | required | - |
| Provider render | 35 | W40 | `provider_surface_renderer.py --check` | This branch | PASS | 0 drift | required | - |
| Metadata contracts | 35 | W40 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 35 | accepted | Path existence scan, Governance contract, Provider render, Metadata contracts | Every repository path the agent and provider surfaces name now exists or is intentionally absent. | SPEC-0212 TSK-0024 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
