---
profile_id: spec
status: draft
artifact_id: SPEC-0155
artifact_type: spec
parent_ids: [REQ-0024, REQ-0025]
created: 2026-08-30
updated: 2026-08-30
---

# Validation Surface Reduction Specification

## Overview

The repository carries 109,193 lines of Python across `scripts/` and `tests/`
to validate a corpus of 680 Markdown documents and 46 Compose files. Eight
identifiable clusters account for 53,436 of those lines. One cluster of 13,032
lines exists to gate a deletion that never occurred, driven by Tasks that were
cancelled, and no runnable gate profile executes it.

This specification reduces validation surface without reducing the guarantees
the workspace actually relies on. Every removal must name the guarantee it
retires and show that no registered profile depends on it.

## Boundaries and Inputs

**Measured inputs.**

| Cluster | Lines |
| :--- | ---: |
| SPEC-0137 gates: `agentic-research-gate9-evidence`, `gate2_claim_review_contract`, `carry_owner_contract`, and their tests | 13,032 |
| Document corpus lifecycle: `check-document-corpus-lifecycle.py` and its tests | 13,378 |
| Gate framework: `ci_gate_contract`, `ci_gate_runner`, `ci_gate_adapters`, `run-ci-gate`, and their tests | 10,116 |
| Document metadata validation and its tests | 9,271 |
| Target surface contracts and their tests | 2,617 |
| Git provenance, identity history, provenance policy, and their tests | 2,126 |
| Old-path gate and its tests | 1,958 |
| Agentic audit semantic freshness | 938 |
| `scripts/**/*.py` total | 50,640 |
| `tests/**/*.py` total | 58,553 |

**SPEC-0137 gate observations.**

| Fact | Value |
| :--- | :--- |
| Validators registered in `run-ci-gate.py --profile full` | 22 |
| `agentic-research-gate9-evidence.py` present in that set | no |
| `gate2_claim_review_contract.py` present in that set | no |
| Present in `--profile changed` | no |
| Non-test, non-manifest references outside SPEC-0137 documents | none |
| SPEC-0137 Task states | 3 `cancelled`, 1 `active` |
| Ledger that gate 2 quantifies over | lives in `tsk-0001-rebuild.md`, `cancelled` |
| Old research pack the gates protect | `docs/90.references/research/0002-agentic-engineering-research-pack/` still present |

**SHA tracking observations.**

| Fact | Value |
| :--- | :--- |
| Provenance library size | 1,499 lines across three modules |
| Documents carrying `archived_commit` and `archived_blob` | 2 |
| Status of those two documents | invalid `archived`, corrected by SPEC-0154 |
| Design already superseded | `target_surface_delta_contract.py` validates the surface "without branch/SHA snapshots" |
| Normative document pinning a commit literal | `docs/98.archive/README.md` |

**In scope.** `scripts/validation/`, `scripts/lib/document_governance/`,
`tests/`, `scripts/manifest.yaml`, the generated evidence snapshots under
`docs/90.references/data/`, and the disposition of SPEC-0137.

**Out of scope.** Everything SPEC-0154 owns, the Compose enablement model owned
by SPEC-0156, and any reduction that would leave a registered gate node without
an implementation.

## Behavior Contract

1. No validator remains whose only consumers are its own tests and a manifest
   entry, unless a registered profile executes it.
2. No document-corpus guarantee is silently dropped: each removal names the
   guarantee, the Spec that introduced it, and the evidence that its migration
   completed.
3. SHA and blob provenance is retained only where a document actually carries
   the fields, and no normative document pins a commit literal as a permanent
   procedure.
4. Generated evidence snapshots declare `generated_by`, and no two snapshots
   publish the same measurement.
5. `run-ci-gate.py --profile full` and `--profile changed` continue to exit 0,
   and the set of guarantees they enforce is documented in the owning Task
   before and after the reduction.

## Technical Approach

### 1. SPEC-0137 disposition, then gate retirement

The gates cannot be retired before their owning Spec has a disposition, because
retiring an executable gate whose Spec is `active` would leave the Spec citing
an absent control. Resolve in this order.

1. Record SPEC-0137's actual state in its Task: three cancelled Tasks, one
   active Task, and an undeleted old pack.
2. Choose the disposition under the SPEC-0154 rule. If `tsk-0004` is genuinely
   in flight the Spec stays `active` and only the gates bound to the cancelled
   Tasks retire; otherwise the Spec transitions and all four gate modules retire.
3. Remove `agentic-research-gate9-evidence.py`, `gate2_claim_review_contract.py`,
   `carry_owner_contract.py`, their tests, and their `scripts/manifest.yaml`
   entries and `suite_registry.py` bindings.
4. Rewrite the SPEC-0137 passages that cite the retired gates so the Spec
   describes what was actually built.

`carry_owner_contract.py` appears in `--profile full` and must therefore be
removed from the profile in the same logical change that removes the module.

### 2. Corpus lifecycle and old-path reduction

`check-document-corpus-lifecycle.py` and the old-path gate encode a migration
that has completed: `docs/98.archive/migrations/0001` through `0003` are the
executed record and SPEC-0136 is `superseded`. Retain only the invariants that
still bind a live document, specifically archive recovery-tuple resolution, and
retire the manifest-reconciliation predicates whose inputs no longer exist.

Each retained invariant is listed in the Task with the document it protects.
Each retired predicate is listed with the migration that made it vacuous.

### 3. Provenance narrowing

Collapse `git_provenance.py`, `identity_history.py`, and `provenance_policy.py`
into a single module that resolves `archived_commit:path` tuples to a Git blob
and validates nothing else. Remove the commit literal from
`docs/98.archive/README.md` and state the recovery procedure in terms of the
frontmatter tuple the tombstone itself carries.

### 4. Generated evidence deduplication

Merge the three summary and detail pairs that publish the same measurement, and
add `generated_by` to every snapshot a generator writes.

| Pair | Action |
| :--- | :--- |
| `0066-foundation-summary` and `0067-foundation` | merge into one snapshot |
| `0068-target-surface-convergence-summary` and `0069-target-surface-convergence` | merge into one snapshot |
| `0073-target-surface-delta-manifest` and `0074-target-surface-delta-summary` | merge into one snapshot |

### 5. Gate framework

The framework is not retired. Its 10,116 lines are reviewed only for nodes left
without an implementation after steps 1 and 2, and for test files that assert
the removed nodes. No orchestration redesign is in scope.

## Interfaces and Data

| Interface | Change |
| :--- | :--- |
| `scripts/manifest.yaml` | entries removed for retired modules |
| `scripts/lib/document_governance/suite_registry.py` | suite bindings removed |
| `scripts/validation/ci_gate_contract.py` | `carry_owner_contract` node removed |
| `scripts/lib/document_governance/` | three provenance modules collapse to one |
| `docs/90.references/data/` | three snapshot pairs merge; `generated_by` added |
| `docs/98.archive/README.md` | commit literal replaced by a tuple-based procedure |

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| :--- | :--- |
| A removal drops a guarantee that a live document still needs | Every removal names its guarantee and the document set it covered; removal without that record is rejected |
| A gate node loses its implementation | `check-script-manifest.py` and the gate contract tests run after each removal |
| SPEC-0137 is retired while `tsk-0004` still has work | Disposition is decided from Task evidence first and recorded before any module is deleted |
| Snapshot merge loses a measurement | The merged snapshot is regenerated and diffed against both sources before the sources are removed |
| Reduction is measured by line count rather than by guarantee | The Task records retired guarantees, not only deleted lines |

## Acceptance Contract

1. `python3 scripts/validation/run-ci-gate.py --profile full` exits 0.
2. `python3 scripts/validation/run-ci-gate.py --profile changed` exits 0.
3. `python3 scripts/validation/check-script-manifest.py` exits 0 with no entry naming a removed module.
4. `python3 -m pytest tests` passes with no test referencing a removed module.
5. `grep -rn "f259c139" docs` returns no match.
6. Every file under `docs/90.references/data/` that a generator writes carries `generated_by`.
7. The Task records, for each retired module, the guarantee retired and the evidence that no live document depends on it.
8. Measured `scripts` plus `tests` line count is recorded before and after.

## Traceability

| Upstream | Relation |
| :--- | :--- |
| REQ-0024 | Agent governance standardization bounds which controls must survive |
| REQ-0025 | Operational readiness closure is the need that a proportionate gate set serves |
| SPEC-0154 | Supplies the corrected lifecycle vocabulary used for the SPEC-0137 disposition |
| SPEC-0137 | Subject of the disposition decision in step 1 |

## Related Documents

- [Script manifest](../../../scripts/manifest.yaml)
- [Task checklists](../../00.agent-governance/policies/task-checklists.md)
- [Quality standards](../../00.agent-governance/policies/quality-standards.md)
- [Agentic research pack rebuild](../0137-agentic-research-pack-rebuild/spec.md)
