---
title: "Path-Aware PR Regression Execution"
version: "0.1.3"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-02"
layer: "specs"
artifact_id: "SPEC-0200-TSK-0001"
parent_ids:
- "SPEC-0200"
- "SPEC-0200-PLAN-0001"
created: "2026-10-02"
---

# Path-Aware PR Regression Execution

## Objective

Execute [SPEC-0200](../spec.md) and its [Plan](../plan.md) through W0-W4. Preserve the single required PR status and every document content contract while routing two expensive regression groups only to changes that can affect them.

## Inputs

The user approved the written Spec, the Plan, and same-session implementation with independent final review on 2026-10-02. The user selected a main-only delivery flow and change-path-specific required PR regressions with manual full coverage. The worktree branch is `codex/spec-0200-pr-gate-latency`. The trusted parent package was activated through protected PRs [#338](https://github.com/buenhyden/hy-home.docker/pull/338), [#339](https://github.com/buenhyden/hy-home.docker/pull/339), [#340](https://github.com/buenhyden/hy-home.docker/pull/340), and [#341](https://github.com/buenhyden/hy-home.docker/pull/341), each after the required `validation-changed` result passed. The implementation baseline is protected main `7b6ffb1bded0371696dcb0fd1e01ff1a1ec74e7d`, after Task draft, ready, and in-progress transitions passed PRs #342-#344.

## Work Log

- W0: The Spec advanced draft → review → approved → active and the Plan draft → approved → active on successive trusted main bases through PRs #338-#341. Task draft, ready, and in-progress transitions passed the same protected check through PRs #342-#344. No lifecycle edge was compressed.
- W1 baseline: Remote heads were only `main` and this feature branch. Main protection required strict `validation-changed` from GitHub Actions app 15368, zero approving reviews, no CODEOWNERS review, conversation resolution, and no force push or deletion. PR #340's gate took 17m25s and #341's 17m41s; measured run 36939016845 took 17m05s. The two slow leaves ran on both ordinary Stage 03 and Stage 05 document candidates. The changed PR plans had 31 Stage 03, 36 Stage 05, and 49 document-implementation invocations; manual full had 49.
- W1 dependency closure: The two slow test groups import `scripts/lib/document_governance/` and read Stage 99 Registry/templates plus governance and GitHub policy files. Ordinary authored document changes remain under metadata, lifecycle, links, and Stage 05 operations-catalog validators. The metadata `check-changed` route did not call `validate_repository_contracts`, so it did not preserve all current-corpus assertions, including index membership; the existing `check-contracts` route passed locally. Also, an unknown path alone selected only the fallback suite, so it could not retain optional document roots. W2 closes both gaps before pruning.

| Changed-path class | W1 owner and W2 selection |
| --- | --- |
| Ordinary Stage 03 and Stage 05 authored docs | Keep direct document validators; Stage 05 keeps operations-catalog. Omit only the two slow implementation-regression leaves. |
| `.github/`, `.pre-commit-config.yaml`, `.agents/`, `.claude/`, `.codex/`, root governance/config files, `docs/99.templates/` | Keep both slow document leaves because these are their contract and fixture inputs. |
| `scripts/lib/document_governance/`, `scripts/lib/gate/`, `scripts/validation/`, `tests/lib/document_governance/`, `tests/lib/gate/`, `tests/validation/` | Keep both slow leaves; these are implementation, selector, entrypoint, or test owners. |
| Unrelated script or test path | Retain existing required suites; do not select the two document leaves solely because the broad `scripts/` or `tests/` suite rule matched. |
| Any valid unregistered path, alone or mixed | Select all suites and all roots; fail closed. |
| Manual `full` | Keep every registered leaf exactly once. |

- W1 script/test disposition: The current manifest has 77 registered files, all `active`/`retain` with no successor. SPEC-0199 already recorded live consumers of apparent one-off, legacy, and duplicate scripts/tests. This audit found no new unreachable file with a tested replacement, so W2 deletes none.
- W2-W4: Pending implementation, hosted acceptance, lifecycle closure, and branch cleanup.

## Verification Evidence

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1, W3 | Pending phase-matrix and hosted timing comparison | [Quality standards](../../../../.agents/governance/quality-standards.md) |
| 2 | W2, W3 | Pending document-only validator parity proof | [Workflow contract](../../../../.github/workflow-contract.yml) |
| 3 | W2 | Pending owner-path, unknown-path, and bounded-root tests | [Gate contract](../../../../scripts/lib/gate/ci_gate_contract.py) |
| 4 | W2, W3 | Pending full-plan exact-count and hosted route receipts | [Quality workflow](../../../../.github/workflows/ci-quality.yml) |
| 5 | W1 | Pending consumer/replacement disposition for any removal | [Script manifest](../../../../scripts/manifest.yaml) |
| 6 | W3 | Pending governance alignment, independent review, and protected PR result | [Quality standards](../../../../.agents/governance/quality-standards.md) |

## Review Evidence

Independent final diff review is pending after the implementation candidate passes focused and changed-profile validation.

## Commit Ledger

W0 parent activation merged as `d46d892380d1d2faad234df6d9b872b928a61c6a` through PR #341; Task in-progress merged as `7b6ffb1bded0371696dcb0fd1e01ff1a1ec74e7d` through PR #344. Implementation commits and merge receipts are pending.

## Rulings

- The required PR check remains `validation-changed`; no second status or dev branch is introduced.
- A script or test is removed only when its callers and replacement are evidenced. Name or age alone is insufficient.
- The slow groups contain current-corpus assertions. W2 first adds repository-wide contract findings to the existing changed-document validator and strengthens unknown-path suite fallback; only then can routing omit those groups for ordinary authored docs.

## Deferred Items

None at Task creation. Any failed, skipped, or unobserved acceptance evidence will be recorded before terminal status.
