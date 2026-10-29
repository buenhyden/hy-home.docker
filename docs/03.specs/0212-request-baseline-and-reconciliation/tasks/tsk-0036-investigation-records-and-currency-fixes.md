---
title: "Investigation Records and Currency Fixes Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0036"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Investigation Records and Currency Fixes Task

## Overview

### Objective

Execute W52: record the read-only investigations behind the partly met
request lines, the owner decisions taken on them, and the fixes they led to.
This Task owns criterion 47 only.

## Inputs and Authorization

On 2026-10-29 the owner chose the investigation and owner-decision groups of
the remaining partly met lines. The owner decided the GitHub Projects,
`_workspace` and SPEC-0211 questions and approved every listed Stage 01, 02
and 05 fix. The input is `main` at merged PR #632. The authorization covers
these documents, the archive moves below, this branch, its pull request, and
merge.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0036 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0036 | ready | in-progress | #objective |
| SPEC-0212-TSK-0036 | in-progress | completed | #evidence |

### Investigations

Three read-only investigations ran on 2026-10-29 at a clean tree. They ran
no gate, test or container.

| Area | Lines | Finding | Disposition |
| --- | --- | --- | --- |
| QA inventory | L089–L094, L221 | No legacy, deprecated or conflicting test; two manifest shell tests that no profile runs; three tests that repeat a real-tree gate run; no fixture without a consumer | Fixed below |
| QA timing | L122 | No tracked per-gate time for one complete FULL run | Recorded in SPEC-0211 TSK-0003 from the 2026-10-29 FULL receipt |
| Stage 01 and 02 | L066, L282, L295 | AD section names and lifecycle lists differ from the Registry; Locust named as the default although k6 owns the result contract; the Vault ADRs describe a removed product while OpenBao has no ADR; tier 13 has no AD; REQ titles say "Product Requirements"; AD-0011 carries obligations | Fixed below |
| Stage 05 | L071, L076, L301 | The Terraform triplet covers no service; the 0074 triplet is named after the removed `11-laboratory` tier; seven hardening triplets may be split too finely | First two fixed below; the split stays as is because each triplet mirrors its own AD and ADR |
| Agent surfaces | L166, L264, L273, L288, L293, L127, L079 | Every role and skill is projected and used; memory has no session-start load, no search and no expiry for its short-term tier; Task files grow large; local document validation is the slowest local cost | No change; these are recorded limits, not defects |

### Owner decisions

| Question | Decision |
| --- | --- |
| GitHub Projects | Not used; `github-governance.md` records this (SPEC-0211 PR #633) |
| `_workspace` | The one folder no Task cites, `four_repository_consolidated_implementation_20261027` (6.2 MB, untracked), was deleted; the five folders that Tasks cite stay |
| SPEC-0211 | Rerun the open checks; TSK-0003 completed and criteria 1, 4 and 5 accepted in PR #633; criteria 2 and 3 wait for TSK-0037 |
| ADR-0009 | Amended in place, not superseded: ADR-0047 does not cover its OpenTofu, Terrakube, SonarQube and registry choices |

### Fixes

| Fix | Location |
| --- | --- |
| AD section names and Stage lifecycle lists match the Registry | `documentation-protocol.md`, `sdlc.md` |
| Two unreached shell tests run in `leaf.repo-contracts-control-plane-regressions`; three real-tree repeats removed or moved to a fixture | `tests/validation/test_shell_regressions.py`, workflow contract |
| ADR-0050 proposes OpenBao as the secrets manager; a new ADR must start as `proposed`, and only an accepted ADR can supersede, so ADR-0003 and ADR-0018 move in a later change | Stage 02 |
| ADR-0009, REQ-0010, AD-0009 and AD-0024 name k6 as the default load tool | Stage 01 and 02 |
| ADR-0011 is deprecated; ADR-0024 and ADR-0025 use current tier names | Stage 02 |
| AD-0032 covers tier 13, with REQ-0027-FR-0009 | Stage 01 and 02 |
| Thirteen REQ titles drop "Product"; the AD-0011 obligations become REQ-0012-FR-0005 | Stage 01 and 02 |
| The Terraform triplet is retired after its live steps moved to the 0082 OpenTofu documents | Stage 05 and 98 |
| The 0074 triplet is renamed "Admin and Experiment Tools Hardening" | Stage 05 |

The Terraform move keeps the two-commit rule: `e9c87bad2` sets the statuses
in place and `a7275a527` moves the bodies unchanged, with catalog rows whose
source is `e9c87bad2`. A first branch (PR #634) also archived ADR-0003 and
ADR-0018 under an accepted ADR-0050. Hosted CI rejected ADR-0050 because a
new ADR must start at `proposed`, and only an accepted ADR can supersede. An
archive capture that reaches `main` history cannot be withdrawn, so that PR was
closed and this branch was rebuilt from `main` without the Vault move.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Metadata contracts | 47 | W52 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |
| Link check | 47 | W52 | `check-document-links.py --mode all` | This branch | PASS | 0 failures | required | - |
| Hosted changed metadata | 47 | W52 | Hosted `candidate-quality` changed metadata | PR 634 head `ebcdfc601` | FAIL | `invalid-initial-status` for ADR-0050 | required | - |
| Hosted changed metadata rerun | 47 | W52 | Hosted `candidate-quality` changed metadata | This branch with ADR-0050 proposed; local `check-changed` against `origin/main` | PASS | 0 violations | required | Hosted changed metadata |
| Corpus and archive | 47 | W52 | `check-document-corpus-lifecycle.py` | This branch | PASS | 0 violations; archive recovery 0 violations with 114 preserved units | required | - |
| Workflow contract | 47 | W52 | `check-github-workflow-contract.py` and the contract tests | This branch | PASS | 0 findings | required | - |
| Shell and fixture tests | 47 | W52 | `test_shell_regressions`, `test_links`, `test_postgres_logical_upgrade_rehearsal` | This branch | PASS | OK | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 47 | accepted | Metadata contracts, Link check, Hosted changed metadata rerun, Corpus and archive, Workflow contract, Shell and fixture tests | Each investigated line has a recorded finding, and each approved fix is in its canonical owner. | SPEC-0212 TSK-0036 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Partial gap rules](tsk-0035-partial-gap-rules.md)
