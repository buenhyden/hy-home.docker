---
profile_id: task
status: completed
artifact_id: task-0153-0011
artifact_type: task
parent_ids:
  - SPEC-0153
  - plan-0153
created: 2026-08-21
updated: 2026-08-28
---

# Task 0011: Script Tests

## Objective

Refactor document-governance scripts and tests by responsibility while preserving registered executable authority.

## Inputs

- [Specification](../spec.md)
- [Implementation Plan](../plan.md)
- [Migration 0003](../../../98.archive/migrations/0003-workspace-governance-simplification.md)
- Task 10 archive convergence, scripts manifest, approved Migration owner_task 11 rows.

## Work Log

| Event | Actual result |
| :--- | :--- |
| 2026-08-27 | Registered immutable six-suite ownership, created mirrored test roots, and moved focused document-governance unit tests with native Git moves. Manifest ownership and stale Task10 test paths were updated; Task12 routing/deletion remains deferred. |
| 2026-08-28 | Closed four independent-review findings, preserved focused behavioral ownership alongside bounded smoke checks, and committed Task 11 as `f042bc1e`. |

## Verification Evidence

| Check | Command | Result |
| :--- | :--- | :--- |
| RED | `PYTHONPATH=. python3 -m unittest tests.validation.test_script_manifest tests.validation.test_ci_gate_contract -v` | Completed in 18.7 seconds with 41 pre-existing manifest/assertion failures; classified in the Task 11 report. |
| GREEN (pre-review) | `timeout 60s env PYTHONPATH=. python3 -m unittest tests.validation.test_script_manifest tests.validation.test_ci_gate_contract tests.validation.test_ci_gate_runner tests.lib.document_governance.test_suite_registry -q` | Pass: 68 tests in 15.810 seconds before semantic-evidence review correction. |
| Review RED | `timeout 60s env PYTHONPATH=. python3 -m unittest tests.validation.test_script_manifest -q` | 32 failures after restoring semantic consumer/test evidence; closed with bounded direct entrypoint behavior and truthful manifest references. |
| Final GREEN | `timeout 60s env PYTHONPATH=. python3 -m unittest tests.validation.test_script_manifest tests.validation.test_ci_gate_contract tests.validation.test_ci_gate_runner tests.lib.document_governance.test_suite_registry tests.validation.test_validator_entrypoints -q` | Pass: 74 tests in 20.972 seconds after review remediation. |
| Static checks | `timeout 60s python3 -m py_compile ...`; `timeout 60s ruff check ...`; `git diff --check` | Pass. |
| Manifest checker | `timeout 120s python3 scripts/validation/check-script-manifest.py` | Pass: `PASS: script manifest is valid`. |
| Diff hygiene | `git diff --check` | Pass. |

## Review Evidence

| Review | Status | Findings and disposition |
| :--- | :--- | :--- |
| Independent review | approved | Initial review found C0/H4/M0; fix round 1 closed all findings and scoped re-review approved C0/H0/M0. |

## Commit Ledger

| Commit | Description |
| :--- | :--- |
| `f042bc1e` | Mirror document-governance test ownership and register six immutable public suites. |

## Rulings

- Current 41 RED failures are authoritative over the historical plan count of 19.
- Task11 owns the suite registry, manifest/test ownership, and stale Task10 path expectations. Task12 owns entrypoint routing and legacy-validator deletion.

## Deferred Items

- Actual hook/local/pre-commit/GitHub Actions routing and deletion of legacy validators after successor coverage (Task12).
