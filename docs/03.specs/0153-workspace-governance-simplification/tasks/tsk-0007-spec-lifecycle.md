---
profile_id: task
status: completed
artifact_id: task-0153-0007
artifact_type: task
parent_ids:
  - SPEC-0153
  - plan-0153
created: 2026-08-21
updated: 2026-08-23
completed_at: 2026-08-23
---

# Task 0007: Spec Lifecycle

## Objective

Converge Stage 03 packages on spec.md, plan.md, and numbered Task records without design.md or tests.md.

## Inputs

- [Specification](../spec.md)
- [Implementation Plan](../plan.md)
- [Migration 0003](../../../98.archive/migrations/0003-workspace-governance-simplification.md)
- Task 6 architecture convergence, Stage 99 Spec profiles, approved Migration owner_task 7 rows.

## Work Log

| Event | Actual result |
| :--- | :--- |
| TDD RED | Added nine parser mutation/current-surface tests; all nine failed because the production parser did not exist. |
| Frozen execution | Executed 46 literal row-exact native moves and only three approved Stage 04 index deletions. |
| Registry normalization | Materialized then natively normalized the five stale singular-Task targets to numbered Task paths without changing Migration bytes. |
| Canonical lifecycle | Added the bounded frozen Spec package parser and integrated it with current-authority metadata/lifecycle validation. |
| Consumer convergence | Rewrote declared/current live consumers; retained only bounded historical evidence and negative compatibility fixtures. |
| Review round 1 RED | Reproduced 24 active-route violations; four parent-directory swaps plus a final file symlink escape; absent cumulative budgets and public snapshot lifecycle validation; and the partial one-time-package removal bypass. |
| Review round 1 fixes | Canonicalized active routing, moved parsing to stable directory descriptors, enforced cumulative budgets, wired Git-base/Migration lifecycle checks into both production validators, constrained one-time retirement, and restored Task 10-owned tombstone literals. |
| Re-review round 1 RED | Reproduced two remaining active-route models plus unbounded Git stdout/stderr capture and missing per-file base-blob enforcement. |
| Review round 2 fixes | Canonicalized the residual Stage 00, Stage 99, validator, and wrapper routes; streamed both Git pipes under one deadline/byte budget with forced reap; and rejected base blobs at limit plus one. |
| Final approval and closeout | Both independent reviewers approved the final packet at `C0/I0/M0`; the controller reran the 16 parser tests, 14 taxonomy tests, lifecycle, changed metadata, provider projections, three generator freshness checks, syntax, Ruff, compilation, and diff gates before creating implementation commit `4e2e71cc60dbe54514d73d63dcef79acb74b4a61`. |

## Verification Evidence

| Check | Command | Result |
| :--- | :--- | :--- |
| Parser GREEN | `python3 -m unittest tests.validation.test_spec_packages -v` | PASS, 16/16 after review round 2. |
| Current integration | Focused co-located topology plus metadata integration tests | PASS, 5/5. |
| Taxonomy | `python3 -m unittest tests.validation.test_document_taxonomy -v` | PASS, 14/14. |
| Lifecycle contract | `python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract` | PASS, `violations=0`. |
| Changed metadata | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base HEAD` | PASS, `selected=169 violations=0 legacy_exceptions=1 transition_overrides=0`; exception is unchanged Task 8 scope. |
| Quality | Ruff, `py_compile`, modified-shell `bash -n`, `git diff --check` | PASS. |
| Inventory | Exact Task 7 row/package/path scan | 49/49 sources absent; 41 row targets plus five normalized finals present; 34 canonical packages; Stage 04 and forbidden roles absent. |
| Preservation | `sha256sum docs/98.archive/migrations/0003-workspace-governance-simplification.md` | `271f21c50cf4ab765422ee552de244a4340c160e53149231eb6be45f03476ab9`. |
| Active selected-old paths | Exact scan excluding five historical evidence files and five negative-fixture files | PASS, zero active authority occurrences; 16 historical and 139 fixture occurrences classified explicitly in the ignored report. |
| Bounded baseline attribution | Traceability / alignment / repository contracts | Not green: 2 Task 8, 22 earlier-Task/legacy, and 17 earlier-Task failures respectively; no Task 7 pass claim. |
| Broad suites | Combined metadata/lifecycle run | Interrupted at five-minute bound; not claimed as passing. |
| Review round 1 generators | Three bounded generator `--check` commands | PASS after restoring prefixed Stage 98 tombstone authority and refreshing the generated script-count witness. |
| Review round 2 wrapper | `bash tests/validation/test_run_agent_precommit_all_files.sh` | PASS, 34/34 including canonical acceptance and retired Stage 04 rejection. |
| Review round 2 contract | Focused migration-contract/static-manifest tests | PASS, 2/2; canonical partition Plans accepted and retired Stage 04 Plans rejected. |
| Review round 2 preservation | Active scans, package/index inventory, and Migration hash | PASS, zero active matches; 34 packages; zero forbidden roles; Stage 04 absent; 46 cached `R100` Task 7 rows only; Migration hash unchanged. |

## Review Evidence

| Review | Status | Findings and disposition |
| :--- | :--- | :--- |
| Focused implementation self-review | Complete | Registry is the sole machine authority; no singular exception, unregistered deletion, Migration mutation, or root `DESIGN.md` change. |
| Independent specification review round 1 | Needs fixes, `C0/I1/M1` | Active routing/projection drift and missing independent-review evidence were accepted for correction in this round. |
| Independent Python quality review round 1 | Needs fixes, `C0/I5/M0` | Descriptor containment/races, production lifecycle wiring, one-time semantics, and aggregate budgets were accepted for correction in this round. |
| Combined round 1 disposition | Needs fixes, `C0/I6/M1` | All seven findings have focused fixes and regressions; independent re-review is pending and no approval is claimed. |
| Independent specification re-review round 1 | Needs fixes, `C0/I2/M0` | Residual Stage 00 and active Stage 99/validator/wrapper execution routes were accepted for correction. |
| Independent Python re-review round 1 | Needs fixes, `C0/I1/M0` | Bounded Git snapshot streaming, deadline/reap, and base-blob enforcement were accepted for correction. |
| Combined round 2 disposition | Needs fixes, `C0/I3/M0` | All three residuals now have focused fixes and regressions; independent round 2 re-review is pending and no approval is claimed. |
| Independent specification re-review round 2 | Approved, `C0/I0/M0` | Canonical Stage 00, Stage 99, validator, and wrapper routes were independently verified. |
| Independent Python re-review round 2 | Approved, `C0/I0/M0` | Bounded Git pipe streaming, deadline, byte limits, process reap, and base-blob rejection were independently verified. |
| Final combined review | Approved, `C0/I0/M0` | Both required independent reviewers approved the round 2 result without residual findings. |

## Commit Ledger

| Commit | Description |
| :--- | :--- |
| `4e2e71cc60dbe54514d73d63dcef79acb74b4a61` | `refactor(specs): unify specification execution lifecycle`; parent-owned logical Task 7 implementation commit. Migration recovery commits remain intentionally unbound until Task 13. |

## Rulings

- The approved Stage 99 Registry is the sole machine authority for package
  roles. The five frozen Migration rows that target singular `task.md` were
  executed literally first, then normalized with a second native move to the
  package's canonical numbered Task path. Migration selection and bytes remain
  frozen; Task 13 owns later ledger status/evidence reconciliation.
- The final normalized Task paths are
  `0123-agentic-engineering-audit-remediation/tasks/tsk-0001-research-pack-extension.md`,
  `0134-agent-governance-canonical-convergence/tasks/tsk-0001-canonical-convergence.md`,
  `0135-target-surface-delta-convergence/tasks/tsk-0001-delta-convergence.md`,
  `0136-sdlc-taxonomy-convergence/tasks/tsk-0001-taxonomy-convergence.md`, and
  `0152-deleted-reference-leaf-disposition/tasks/tsk-0001-reference-disposition.md`.

## Deferred Items

- Task 11 owns script-manifest reconciliation, including registration of the new
  parser and pre-existing manifest drift.
- Task 13 owns Migration status/evidence/recovery compaction; Migration 0003
  selection, digests, and bytes remain frozen in this Task.
- Baseline traceability/alignment/repository-contract failures and the moved
  Spec 0137 old-path compatibility expectations remain recorded for their
  owning work; no false green result is claimed.
