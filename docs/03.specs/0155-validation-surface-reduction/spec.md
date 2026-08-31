---
profile_id: spec
status: completed
artifact_id: SPEC-0155
artifact_type: spec
parent_ids: [REQ-0024, REQ-0025]
created: 2026-08-30
updated: 2026-09-01
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

| Cluster                                                                                                                    |  Lines |
| :------------------------------------------------------------------------------------------------------------------------- | -----: |
| SPEC-0137 gates: `agentic-research-gate9-evidence`, `gate2_claim_review_contract`, `carry_owner_contract`, and their tests | 13,032 |
| Document corpus lifecycle: `check-document-corpus-lifecycle.py` and its tests                                              | 13,378 |
| Gate framework: `ci_gate_contract`, `ci_gate_runner`, `ci_gate_adapters`, `run-ci-gate`, and their tests                   | 10,116 |
| Document metadata validation and its tests                                                                                 |  9,271 |
| Target surface contracts and their tests                                                                                   |  2,617 |
| Git provenance, identity history, provenance policy, and their tests                                                       |  2,126 |
| Old-path gate and its tests                                                                                                |  1,958 |
| Agentic audit semantic freshness                                                                                           |    938 |
| `scripts/**/*.py` total                                                                                                    | 50,640 |
| `tests/**/*.py` total                                                                                                      | 58,553 |

**SPEC-0137 gate observations.**

| Fact                                                          | Value                                                                               |
| :------------------------------------------------------------ | :---------------------------------------------------------------------------------- |
| Validators registered in `run-ci-gate.py --profile full`      | 22                                                                                  |
| `agentic-research-gate9-evidence.py` present in that set      | no                                                                                  |
| `gate2_claim_review_contract.py` present in that set          | no                                                                                  |
| Present in `--profile changed`                                | no                                                                                  |
| Non-test, non-manifest references outside SPEC-0137 documents | none                                                                                |
| SPEC-0137 Task states                                         | 3 `cancelled`, 1 `active`                                                           |
| Ledger that gate 2 quantifies over                            | lives in `tsk-0001-rebuild.md`, `cancelled`                                         |
| Old research pack the gates protect                           | `docs/90.references/research/0002-agentic-engineering-research-pack/` still present |

**SHA tracking observations.**

| Fact                                                     | Value                                                                                   |
| :------------------------------------------------------- | :-------------------------------------------------------------------------------------- |
| Provenance library size                                  | 1,499 lines across three modules                                                        |
| Documents carrying `archived_commit` and `archived_blob` | 2                                                                                       |
| Status of those two documents                            | invalid `archived`, corrected by SPEC-0154                                              |
| Design already superseded                                | `target_surface_delta_contract.py` validates the surface "without branch/SHA snapshots" |
| Normative document pinning a commit literal              | `docs/98.archive/README.md`                                                             |
| Full-gate test failing on a bounded Git identity scan    | `test_reverse_transition_without_override_is_blocked`                                   |
| Blobs the identity scan reads per run                    | 498 markdown files, 11.07 MiB                                                           |
| Metadata advisory state guarded by a `ProfileError`      | `metadata_validator.py`                                                                 |
| `docs/04.execution` literals pinned inside a validator   | `metadata_validator.py` `planned_partitions`                                            |

**Routed in from SPEC-0154, measured.**

| Fact                                                   | Value                                                                                        |
| :----------------------------------------------------- | :------------------------------------------------------------------------------------------- |
| Blocking violations SPEC-0154 closes with              | 4                                                                                            |
| `governance-policy` `required_sections`                | `["Related Documents"]`                                                                      |
| `governance-policy` `optional_sections`                | `[]`                                                                                         |
| Documents carrying the profile                         | 16                                                                                           |
| Distinct H2 headings across them                       | 51                                                                                           |
| Consequence                                            | every H2 except `Related Documents` is unregistered in all 16                                |
| Why the corpus passes                                  | only headings a change introduces are counted, so the profile blocks edits and not the state |
| Emission site                                          | `metadata_validator.py:2442`, reading `registry.profiles`                                    |
| Registering the 13 changed headings drops the count to | 0, measured and reverted                                                                     |
| Transition override requires `evidence_task` prefix    | `docs/03.specs/spec-`                                                                        |
| Transition override requires `evidence_task` basename  | `task.md`                                                                                    |
| Directories matching `docs/03.specs/spec-*`            | 0                                                                                            |
| Files named `task.md` under `docs/03.specs/`           | 0, against 15 named `tsk-*.md`                                                               |
| Consequence                                            | no path in this repository can satisfy the override, so the mechanism is unreachable         |
| Dead links behind `DEFERRED_PREFIXES` in the link gate | 158                                                                                          |

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

### 3. Bounded Git identity scan

`run-ci-gate.py --profile full` fails on
`tests.validation.test_document_metadata.ChangedModeRolloutTests.test_reverse_transition_without_override_is_blocked`
with `configuration-error: bounded Git identity scan failed`. SPEC-0154
measured and rejected the two obvious causes: the 45-second deadline is not
reached, and the 16 MiB shared output cap is not exhausted. The failure also
reproduces standalone before SPEC-0154's first commit.

Find the actual bound the scan exhausts, then decide whether the bound or the
scan is wrong. `identity_history.py` spawns one `git cat-file` per document and
shares a single byte budget across the run; whether that design is needed at all
is part of the narrowing below.

### 4. Provenance narrowing

Collapse `git_provenance.py`, `identity_history.py`, and `provenance_policy.py`
into a single module that resolves `archived_commit:path` tuples to a Git blob
and validates nothing else. Remove the commit literal from
`docs/98.archive/README.md` and state the recovery procedure in terms of the
frontmatter tuple the tombstone itself carries.

### 5. Taxonomy-wave enforcement and Stage 04 literals

`metadata_validator.py` raises
`ProfileError("sdlc-taxonomy-convergence remains advisory until corpus
migration")` and pins `planned_partitions` to `docs/04.execution/plans` and
`docs/04.execution/tasks`. Both are corpus-migration artefacts, which is why
SPEC-0154 routes them here rather than editing a guarded invariant from a
documentation change.

Once SPEC-0154 leaves the corpus with zero `invalid-status` records, decide the
migration complete, remove the advisory guard so the full inventory blocks, and
replace the Stage 04 partition literals with the co-located Spec Package paths
that replaced them. Record the completion judgement and its evidence in the
Task.

### 6. Generated evidence deduplication

Merge the three summary and detail pairs that publish the same measurement, and
add `generated_by` to every snapshot a generator writes.

| Pair                                                                            | Action                  |
| :------------------------------------------------------------------------------ | :---------------------- |
| `0066-foundation-summary` and `0067-foundation`                                 | merge into one snapshot |
| `0068-target-surface-convergence-summary` and `0069-target-surface-convergence` | merge into one snapshot |
| `0073-target-surface-delta-manifest` and `0074-target-surface-delta-summary`    | merge into one snapshot |

### 7. The `governance-policy` heading contract

The profile declares one required section and no optional sections, so all 16 of
its documents are already in violation of their own contract. The gate does not
say so because it counts only headings a change introduces. The effect is a
contract that permits any existing document and rejects any edit to one.

Two dispositions are available and one must be chosen from evidence, not from
convenience.

1. **Declare the profile free-form.** Stage 00 policies differ from each other
   by design; `documentation-protocol.md` is a routing table and
   `quality-standards.md` is a numbered rubric. If no shared vocabulary is
   defensible, the profile registers no heading contract beyond `Related
Documents` and the validator stops treating an unregistered heading as a
   finding for it. This requires the validator change SPEC-0154 attempted and
   withdrew, placed on the path that `metadata_validator.py:2442` actually
   consults.
2. **Give the profile a real contract.** Extract the shared vocabulary across
   the 16 documents, register it, and conform the outliers.

Registering only the headings of the two documents SPEC-0154 changed is
prohibited: it whitelists one change and leaves 38 headings unregistered.
Whichever disposition is chosen, the acceptance measurement is the same, that
the blocking mode reports zero `body-heading-forbidden` findings for every
document of the profile and not only for the recently changed ones.

### 8. The unreachable transition override

`load_transition_overrides` at `metadata_validator.py:6135` accepts an
`evidence_task` only when it starts with `docs/03.specs/spec-` and is named
`task.md`. The taxonomy migration replaced both forms. The repository holds no
path that can satisfy the contract, so the only sanctioned way to record an
approved lifecycle exception cannot be used by any document.

Correct the path contract to the co-located Task form,
`docs/03.specs/####-<slug>/tasks/tsk-####-<slug>.md`, with a test that fails
against the old form. Then record the two `archived -> completed` migration
transitions through the repaired mechanism, with approval and reason, rather
than by relaxing the lifecycle.

The two Stage 98 migration documents record a correction from an invalid status
rather than an ordinary lifecycle step, which is exactly the case the override
exists to carry. Their evidence is
`docs/03.specs/0154-governance-consistency-convergence/tasks/tsk-0003-lifecycle-completion.md`.

### 9. Research-pack link exemption

`check-document-links.py` carries `DEFERRED_PREFIXES` naming the two agentic
research packs, behind which 158 dead links sit. The exemption states SPEC-0155
as its owner and its removal condition. Once step 1 records the SPEC-0137
disposition, delete the exemption and repair or delink what it was hiding.

### 10. Gate framework

The framework is not retired. Its 10,116 lines are reviewed only for nodes left
without an implementation after steps 1 and 2, and for test files that assert
the removed nodes. No orchestration redesign is in scope.

## Interfaces and Data

| Interface                                               | Change                                                                                                                                                                                                 |
| :------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scripts/manifest.yaml`                                 | entries removed for retired modules                                                                                                                                                                    |
| `scripts/lib/document_governance/suite_registry.py`     | suite bindings removed                                                                                                                                                                                 |
| `scripts/validation/ci_gate_contract.py`                | `carry_owner_contract` node removed                                                                                                                                                                    |
| `scripts/lib/document_governance/`                      | three provenance modules collapse to one                                                                                                                                                               |
| `docs/90.references/data/`                              | three snapshot pairs merge; `generated_by` added                                                                                                                                                       |
| `docs/98.archive/README.md`                             | commit literal replaced by a tuple-based procedure                                                                                                                                                     |
| `scripts/lib/document_governance/metadata_validator.py` | advisory guard removed; `planned_partitions` Stage 04 literals replaced; `load_transition_overrides` path contract corrected to the co-located Task form; `governance-policy` heading handling settled |
| `docs/99.templates/registry.json`                       | `governance-policy` sections settled under the step 7 disposition                                                                                                                                      |
| `scripts/validation/check-document-links.py`            | `DEFERRED_PREFIXES` removed                                                                                                                                                                            |

## Failure Modes and Guardrails

| Failure mode                                                 | Guardrail                                                                                                  |
| :----------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------- |
| A removal drops a guarantee that a live document still needs | Every removal names its guarantee and the document set it covered; removal without that record is rejected |
| A gate node loses its implementation                         | `check-script-manifest.py` and the gate contract tests run after each removal                              |
| SPEC-0137 is retired while `tsk-0004` still has work         | Disposition is decided from Task evidence first and recorded before any module is deleted                  |
| Snapshot merge loses a measurement                           | The merged snapshot is regenerated and diffed against both sources before the sources are removed          |
| Reduction is measured by line count rather than by guarantee | The Task records retired guarantees, not only deleted lines                                                |
| A registry or validator change is described before it is measured | Every such change records the failing count before and after in the same Task row; a commit message may not claim an effect no measurement showed |
| The heading contract is closed by whitelisting only the changed headings | Acceptance item 12 measures all 16 documents of the profile, not the changed set |
| The override is closed by relaxing the lifecycle instead of repairing the mechanism | Acceptance item 13 requires a test that fails against the old path form |
| Verification uses the advisory inventory instead of the blocking mode | Acceptance item 11 names `--mode check-changed` explicitly |

## Acceptance Contract

This Spec Package is complete. All eight Tasks are `completed`; the obligations
transferred from SPEC-0154 are closed; and SPEC-0157 Task 9 revalidated the
combined Full profile before applying this legal `active -> completed`
endpoint. No transition override is used.

1. `python3 scripts/validation/run-ci-gate.py --profile full` exits 0, including `test_reverse_transition_without_override_is_blocked`.
2. `python3 scripts/validation/run-ci-gate.py --profile changed` exits 0.
3. `python3 scripts/validation/check-script-manifest.py` exits 0 with no entry naming a removed module.
4. `python3 -m unittest discover -s tests` passes with no test referencing a removed module. This repository has no `pytest` installed; `unittest` is its runner.
5. `grep -rn "f259c139" docs` returns no match.
6. `grep -rn "04.execution" scripts` returns no match.
7. `python3 scripts/validation/check-document-metadata.py` runs its full inventory in blocking mode and exits 0.
8. Every file under `docs/90.references/data/` that a generator writes carries `generated_by`.
9. The Task records, for each retired module, the guarantee retired and the evidence that no live document depends on it.
10. Measured `scripts` plus `tests` line count is recorded before and after.
11. `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref <merge-base>`
    reports zero violations. This is the blocking condition CI enforces and the
    condition SPEC-0154 closed without meeting.
12. The blocking mode reports zero `body-heading-forbidden` findings for all 16
    `governance-policy` documents, not only for recently changed ones, under
    whichever disposition step 7 selects.
13. A transition override whose `evidence_task` is a co-located
    `tasks/tsk-####-<slug>.md` path is accepted, proven by a test that fails
    against the `docs/03.specs/spec-*/task.md` form, and the two Stage 98
    migration transitions are recorded through it.
14. `DEFERRED_PREFIXES` is absent from `check-document-links.py` and
    `--mode all` still exits 0.

## Traceability

| Upstream  | Relation                                                                       |
| :-------- | :----------------------------------------------------------------------------- |
| REQ-0024  | Agent governance standardization bounds which controls must survive            |
| REQ-0025  | Operational readiness closure is the need that a proportionate gate set serves |
| SPEC-0154 | Supplies the corrected lifecycle vocabulary used for the SPEC-0137 disposition |
| SPEC-0137 | Subject of the disposition decision in step 1                                  |

## Related Documents

- [Script manifest](../../../scripts/manifest.yaml)
- [Task checklists](../../00.agent-governance/policies/task-checklists.md)
- [Quality standards](../../00.agent-governance/policies/quality-standards.md)
- [Agentic research pack rebuild](../0137-agentic-research-pack-rebuild/spec.md)
