---
title: "Documentation, Governance, QA and CI Contract Task"
version: "0.2.0"
type: "sdlc/task"
owner: "@buenhyden"
updated: "2026-11-10"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0049"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-03"
---

# Documentation, Governance, QA and CI Contract Task

## Overview

### Objective

Implement the approved local P10 document-contract, CI-route and governance wording corrections. Completed Task bodies and their acceptance scope remain historical records; local checks are not operational or remote acceptance.

## Inputs and Authorization

The observed starting revision is `43f112eb5452767f5ab56f95335ef59fb4ab743c`. Local source, document and synthetic QA are authorized. Service operation, actual credentials, external transmission and remote CI are not. The dependencies package was unavailable, so a complete historical crosscheck is not claimed.

## Work Log

### Execution Items

| Item | Work Unit | Scope | Owner | Status | Blocker |
| --- | --- | --- | --- | --- | --- |
| P10.01 | W99 | Current generation-7 records and validators | doc-writer | in-progress | Final sequential validator evidence pending source freeze |
| P10.02 | W100 | Existing P03/P04/P05 CI route registrations | ci-cd-engineer | in-progress | Final public-plan evidence pending |
| P10.03 | W101 | Hook and canonical governance wording | hook-developer, rules-engineer | in-progress | Native provider delivery is unrun |
| P10.04 | W102 | Local result lifecycle and residual handoff | doc-writer | in-progress | Remote CI and operation are unauthorized |

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0049 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0049 | ready | in-progress | #work-log |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Generation-7 current-task normalization | 94 | W99 | P08/P09 document-contract test | Current draft TSK-0047 and TSK-0048 | PASS | `tests.validation.test_p10_document_contract`: 1 local test passed after exact Evidence/Acceptance normalization; completed Task bodies were not changed. | required | - |
| Metadata baseline | 94 | W99 | Metadata validator | Current workspace at P10 start | FAIL | Explicit-baseline metadata completed exit 1 with 146 violations: this Task's initial Plan rows lacked criteria 94–97, plus preserved archive type-mismatch debt. The 30-second tool wait was not a validator timeout; final rerun follows the Spec repair. | required | - |
| Corpus lifecycle baseline | 94 | W99 | Corpus lifecycle validator | Current workspace at P10 start | PASS | Existing lifecycle suite completed 40/40 PASS after the metadata diagnosis; it is distinct from metadata profile validity. | required | - |
| Link alignment baseline | 94 | W99 | Link alignment validator | Current workspace at P10 start | PASS | Explicit-baseline alignment completed exit 0 in about 38.5 seconds; historical-link warning remains separately classified. | required | - |
| DATA-0096 retention-preserving refresh | 94 | W99 | Inventory scan/validate and retained-receipt comparison | Public DATA inventory | PASS | The first scan was rejected because it omitted retained receipts. A second scan used 98 extracted public review records plus the seven existing curated sections: files 42,038/42,038, full review 6/2,326, partial 78/2,326, render 0/17, runtime/restore 0/112; `validate` passed. Changed inputs remain in the compare invalidation set. | required | - |
| P03 public validator registration | 95 | W100 | Public plan/parity check | Registered local contexts | PASS | CI writer reports all public-plan/execution-context checks (79) and workflow-contract/P03 checks (75) passed; the registered runner's direct environment rejection remains distinct from an execution result. Remote CI is not run. | required | - |
| P04/P05 selector expectation correction | 95 | W100 | Required/optional selector contract | Registered local contexts | PASS | CI writer reports the same 79 local plan/execution-context checks passed after correcting the six required selectors and retaining their optional boundary. | required | - |
| Hook and governance local regressions | 96 | W101 | Focused hook, rule and projection checks | Hook/rules writer packets | PASS | Hook packet: 36 focused tests plus bash/shellcheck/Ruff PASS. Rules packet: contract PASS, renderer check (two providers, zero drift), four focused PASS. Native provider delivery remains unrun. | required | - |
| Evidence lifecycle and remote boundary | 97 | W102 | CI EvidenceStore and execution-context regressions | `tests.lib.gate.test_ci_gate_evidence` and `tests.validation.test_ci_gate_execution_context` | PASS | Independent local reproduction completed 40/40 PASS, exit 0 in 7.233 seconds. A separate manifest unit group has 7 existing failures (six mutation classifications and one `_workspace_model_connections.py` production-to-test reference); its owner must classify and repair them. Remote CI and operational acceptance are not run or inferred. | required | - |
| Metadata active rerun | 94 | W99 | Metadata validator | `check-document-metadata.py --mode check-active` on the active corpus at `a9d994367` | PASS | `metadata check-active: selected=538 violations=0 transition_overrides=0`, exit 0. Archive type-mismatch debt is outside the active selection and stays owned historical debt. | required | Metadata baseline |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 94 | accepted | Generation-7 current-task normalization, Metadata baseline, Corpus lifecycle baseline, Link alignment baseline, DATA-0096 retention-preserving refresh, Metadata active rerun | Draft records are normalized, lifecycle and receipt-preserving DATA refresh pass, but the 2026-11-10 active-corpus metadata rerun passed with 0 violations; preserved archive debt stays out of scope. Owner @buenhyden accepted on 2026-11-10. | SPEC-0212 TSK-0049 |
| 95 | pending | P03 public validator registration, P04/P05 selector expectation correction | CI implementation and complete local plan/parity evidence are pending. | SPEC-0212 TSK-0049 |
| 96 | accepted | Hook and governance local regressions | Local regressions are reported; native provider delivery is separate and unrun. Owner @buenhyden accepted on 2026-11-06. | SPEC-0212 TSK-0049 |
| 97 | accepted | Evidence lifecycle and remote boundary | Existing lifecycle machinery is reused; remote CI and operational acceptance remain unrun. Owner @buenhyden accepted on 2026-11-06. | SPEC-0212 TSK-0049 |

### Cross-package header handoff

The following active or blocked Tasks retain the prior eight-column Evidence
header (without `Required`). They caused the remaining corpus
`spec-package-invalid` result after SPEC-0212 was normalized. They are not
completed archives and are not rewritten by this Task. The frontmatter owner
is an attribution, not operational authority; their package writer must first
review each Task's criterion/status contract, normalize its table together with
the required evidence-result domain, and run that package's metadata and
lifecycle checks.

Affected Task entries (target, package writer, current state and resume condition). The `@buenhyden` package-writer labels for SPEC-0204 and SPEC-0218 are frontmatter attribution only, never operating authority.

- `SPEC-0204-TSK-0001` — `blocked`; the SPEC-0204 package writer must confirm blocked criterion ownership, migrate Evidence to generation 7, then run package validators.
- `SPEC-0204-TSK-0005` — `in-progress`; preserve cross-tier evidence and normalize its active Evidence contract before validation.
- `SPEC-0204-TSK-0006` — `blocked`; preserve OpenBao block/recovery evidence and migrate only after its blocked contract is reviewed.
- `SPEC-0204-TSK-0007` — `draft`; confirm retirement ownership and authorization boundary, then normalize the draft table.
- `SPEC-0204-TSK-0010` — `in-progress`; preserve the Secret catalog evidence and value-exclusion boundary while migrating the table.
- `SPEC-0204-TSK-0011` — `in-progress`; preserve P03 integration evidence and normalize with its criterion-to-work-unit mapping.
- `SPEC-0204-TSK-0012` — `in-progress`; preserve Airflow pipeline evidence and normalize its active table before package validation.
- `SPEC-0204-TSK-0014` — `in-progress`; preserve OpenBao consumer migration and residuals, then migrate the table.
- `SPEC-0204-TSK-0015` — `in-progress`; preserve operations-layout history and normalize the in-progress Evidence table.
- `SPEC-0204-TSK-0016` — `in-progress`; preserve Opsflow acceptance boundaries and normalize the current table.
- `SPEC-0218-TSK-0002` — `in-progress`; review root-resource criterion ownership, migrate the active table, then validate SPEC-0218.

## Review and Completion

Run metadata, corpus lifecycle and link alignment sequentially after final source changes, observing each up to five minutes and recording the actual exit result. Archive type mismatches remain owned historical debt: do not weaken the validator or rewrite preserved archives. Run `graphify update .` after all writers freeze source changes.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Workspace inventory](../../../90.references/data/0096-workspace-inventory/README.md)
