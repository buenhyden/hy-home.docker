---
status: active
artifact_id: task-0153-01
artifact_type: task
parent_ids:
  - spec-0153
  - plan-0153
created: 2026-08-20
updated: 2026-08-20
---

# Task: Workspace Governance Simplification Bootstrap Evidence

## Overview

This transient Task records actual bootstrap evidence before the canonical
prefixless Spec 0153 package and its numbered Task records exist. Task 3 migrates
the evidence into `tsk-0001-control-plane.md` and `tsk-0002-stage99.md`, verifies
field completeness, and removes this file.

## Inputs

- [Specification](spec.md)
- [Implementation Plan](plan.md)
- [ADR-0029](../../02.architecture/decisions/adr-0029-workspace-governance-authority.md)
- [Migration 0003](../../98.archive/migrations/mig-0003-workspace-governance-simplification.md)
- Frozen baseline commit `889d3868ecd0913cddac79a718584a54a8453525`

## Goals and Non-goals

- Register the cross-stage authority decision and a deterministic approved
  migration selection.
- Prove every tracked transition source is a regular baseline blob and every
  planned-output source has an earlier typed owner.
- Record actual RED/GREEN evidence without prospectively approving or executing
  any transition.
- Do not move or delete a corpus path, change provider surfaces, modify a
  validator implementation, stage, commit, push, merge, or change runtime state.

## Scope and Change Boundaries

The allowed Task 1 paths are the ADR, Migration, this Task, the focused test,
and bounded Spec/Plan evidence. All other document corpus, provider, script,
workflow, runtime, remote, and secret surfaces are excluded.

## Approval Evidence

| Approval source | Protected surface | Boundary | Rollback or recovery | Redaction boundary |
| :--- | :--- | :--- | :--- | :--- |
| User approval of the implementation plan and Subagent-Driven execution | Documentation and AI-agent governance control plane | Task 1 may create review evidence only; Migration execution requires a second explicit approval of the exact row packet | Discard the unstaged Task 1 diff; no corpus transition has executed | Paths, stable IDs, counts, commit objects, command outcomes, and review verdicts only |
| Controller ruling after the initial RED | Migration schema version 2 | Add typed `planned_creations`, sequential `planned-output` provenance, unique row IDs, and active-consumer lists without changing the Spec's semantic contract | Revert the bounded Plan/Test/Migration schema correction | No runtime or credential data |

The user approved the exact Migration selection digest on `2026-08-20`.
`approval.status`, `approved_by`, and `approved_at` now record
`approved/user/2026-08-20`. The Migration document's `status: archived`
frontmatter satisfies the
currently authoritative Stage 99 migration-document profile and describes its
evidence-preservation role; it does not approve the internal transition ledger.

## Work Breakdown

1. Read the advisory Graphify report and corroborate it against live Stage 00,
   Stage 99, Spec, Plan, and tracked inventory.
2. Add the missing-control-plane test and record its actual RED result.
3. Record ADR-0029.
4. Detect and correct the tracked-source-only schema defect without weakening
   source, target, collision, or recovery checks.
5. Freeze planned creations, transitions, active consumers, and the approval
   packet at the baseline commit.
6. Run focused tests, changed metadata, and diff hygiene.
7. Preserve the completed independent re-review and explicit user approval
   evidence, run the approved-state suite, and hand commit ownership to the
   controller.

## Work Log

| Event | Actual result |
| :--- | :--- |
| Graph corroboration | Graphify was built from `f8a72211` and is advisory. Live HEAD, Stage 00/99, Spec, Plan, and tracked inventory were used as authority. |
| Initial RED | The control-plane test failed because ADR-0029 was absent. |
| Ruling | A row contract that required every source to be tracked at the baseline could not represent ADR-0029, Migration 0003, and later Spec Task outputs consumed by subsequent Tasks. Schema version 2 separates typed creations from transitions and resolves planned outputs only through earlier owners. |
| Selection freeze | `17` planned creations and `903` transition rows; `3,571` owner-ordered literal/Markdown consumer edges; edge SHA-256 `2f1840983d98ed93ffdc183305c49b389b17e5c8362538e5df97d451be2b9139`; baseline-and-policy-bound selection SHA-256 `9328d04dc01ad60faa9be3f805eaa9414af1bacfe4751c61ef133749390e30e1`. |
| Consumer-scope correction | The first GREEN over-selected `6,550` edges and the initial review remediation then under-selected `1,840` by excluding every delete-disposition consumer. The current derivation excludes a delete consumer only when its owner Task is no later than the source transition owner, resolves repository-local Markdown links, and retains Stage 98, Graphify, and immutable/generated Stage 90 exclusions. |
| Initial review remediation | An initial review attempt edited shared files and therefore cannot serve as an independent review. Local re-audit retained independently justified technical corrections: the active-consumer exclusions above, a requirement that `git cat-file -t <baseline_commit>` return `commit`, and rejection of placeholder artifact IDs. No review approval is claimed. |
| Placeholder artifact correction | Owner review found `16` deleted template rows with `artifact_id: <artifact-id>`. Those template placeholders are not stable artifact identities, so the rows now use `artifact_id: null`, the test rejects placeholder IDs, and the selection SHA-256 changed to `b79f7da97811ab51fadb33ada15efaaaf51a40cef9bf55a31d4448ff30a2f9cf`. |
| Final quality review | `CHANGES_REQUIRED`, `C0/I5/M0`: consumer ordering/relative links, strict YAML, canonical namespaces, baseline/digest binding, and final Migration compaction were incomplete. |
| Quality remediation RED | The expanded focused suite ran `8` tests with `7` failures in `6.089s`, covering both required consumer edges, four noncanonical path variants, missing policy/compaction data, and ambiguous YAML acceptance. |
| Quality remediation | Added owner-order-aware consumer derivation, shared safe Markdown link resolution, one-fence duplicate/alias/anchor/tag rejection, canonical POSIX namespaces and collision mutations, pinned `ls-tree -rz` blob provenance, policy/edge digest selection binding, and Task 10/13 final-compaction requirements. |
| Quality re-review | `CHANGES_REQUIRED`, `C0/I1/M0`: execution approval states and the final compacted lifecycle state were not explicitly separated. |
| Lifecycle remediation RED | The focused suite ran `11` tests with one failure and one error in `6.545s`: the execution-state validator was absent and schema version `2` was accepted as a final compacted ledger. |
| Lifecycle remediation | Schema version `2` accepts only state-specific `pending` or `approved` approval fields; schema version `3` is the field-minimal durable mapping/recovery ledger. Approval and final-state mutations run in the same suite. |
| Final independent re-reviews | Specification `C0/I0/M0`; quality `C0/I0/M0`. The earlier quality `I5` and lifecycle `I1` are addressed. |
| Exact row-set approval | The user approved selection SHA-256 `9328d04dc01ad60faa9be3f805eaa9414af1bacfe4751c61ef133749390e30e1` on `2026-08-20`. The execution ledger records `approved/user/2026-08-20`; row/edge counts and both digests are unchanged. |
| Approved-state GREEN | The approved execution ledger passed `11/11` in `7.590s`. The Migration is `503,198` bytes over `1,039` lines, with one YAML flow row per mapping. |
| Changed metadata | `selected=5 violations=0 legacy_exceptions=0 transition_overrides=0`. |
| Diff hygiene | `git diff --check` exited `0` with no output. |

## Verification Evidence

### Initial RED

Command:

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_workspace_governance_migration -v
```

Actual result:

```text
test_governance_migration_control_plane_exists ... FAIL
AssertionError: False is not true
Ran 1 test in 0.000s
FAILED (failures=1)
```

The failure was specifically the missing
`docs/02.architecture/decisions/adr-0029-workspace-governance-authority.md`.

### Focused GREEN

Command:

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_workspace_governance_migration -v
```

Actual result:

```text
test_consumer_policy_covers_ordered_and_relative_edges ... ok
test_execution_ledger_lifecycle_mutations ... ok
test_final_compaction_contract_is_minimal ... ok
test_governance_migration_control_plane_exists ... ok
test_namespace_mutations_fail_closed ... ok
test_paths_are_canonical_posix ... ok
test_approved_selection_is_exact_and_reviewable ... ok
test_planned_creations_are_unique_and_typed ... ok
test_structural_source_families_are_complete ... ok
test_transition_rows_fail_closed ... ok
test_yaml_contract_rejects_ambiguity ... ok
Ran 11 tests in 7.590s
OK
```

### Quality Remediation RED

The expanded suite initially ran `8` tests with `7` failures in `6.089s`.
Failures proved that the pending contract omitted the ordered
`check-repo-contracts.sh` consumer, the Architecture Decisions README relative
ADR link, canonical-path rejection, consumer policy and final-compaction data,
and strict one-fence YAML parsing. No corpus transition executed during RED or
GREEN.

### Lifecycle Remediation RED

The quality re-review suite ran `11` tests with one failure and one error in
`6.545s`. It proved there was no explicit pending/approved execution-state
validator and that execution schema version `2` could incorrectly pass as the
final compacted ledger. The corrected suite validates pending null fields,
approved nonempty identity and real `YYYY-MM-DD` date, invalid state/date
combinations, schema-version-3 final minimality, null recovery, and forbidden
execution fields.

### Initial Review Remediation Probe

During the invalid initial review attempt, a mutation replaced `baseline_commit`
with the same commit's tree object SHA. The test suite failed before any row
validation:

```text
AssertionError: baseline_commit must identify a Git commit
Ran 0 tests in 0.013s
FAILED (errors=1)
```

Changed metadata then reported
`selected=5 violations=0 legacy_exceptions=0 transition_overrides=0`, and
`git diff --check` exited `0` with no output. A later owner review correction
changed deleted template placeholder artifact IDs to null and added a
placeholder rejection assertion before the current GREEN run.

## Controlled Agent Pre-commit Evidence

The controller staged exactly the six Task 1 paths, verified the cached path
set and `git diff --cached --check`, and created the approved logical commit.
No corpus transition, push, merge, runtime mutation, or secret operation was
performed.

## Review Evidence

| Review | Status | Findings and disposition |
| :--- | :--- | :--- |
| Implementation self-review | complete | Focused tests, exact selection digest, family counts, changed metadata, and diff hygiene are current. |
| Independent specification review | complete | Final re-review returned `C0/I0/M0` for the corrected exact packet. |
| Independent quality review | complete | Initial final review returned `C0/I5/M0`, lifecycle re-review returned `C0/I1/M0`, and final re-review returned `C0/I0/M0`; all findings are addressed. |
| User row-set approval | approved | Exact selection SHA-256 `9328d04dc01ad60faa9be3f805eaa9414af1bacfe4751c61ef133749390e30e1`, approved as `user` on `2026-08-20`. |

## Commit Ledger

- `e58d91796409fd562a8b395293942c0f73949c24` —
  `docs: register workspace governance migration`

## Deferred and Blocked Items

- Task 1 is complete. Task 2 may install the Stage 99 authority before any
  approved corpus transition executes.
- Recovery commits remain null while rows are planned. They become mandatory
  before a moved or deleted row is completed.
- Ordinary in-place semantic edits remain in the owning Task file lists and are
  intentionally not duplicated as Migration rows.

## Related Documents

- [Specification](spec.md)
- [Implementation Plan](plan.md)
- [ADR-0029](../../02.architecture/decisions/adr-0029-workspace-governance-authority.md)
- [Migration 0003](../../98.archive/migrations/mig-0003-workspace-governance-simplification.md)
