---
title: "Completed Spec Package Deletion Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-03"
layer: "specs"
artifact_id: "SPEC-0250-TSK-0001"
parent_ids:
- "SPEC-0250-PLAN-0001"
created: "2026-11-03"
---

# Completed Spec Package Deletion Task

## Overview

### Objective

Implement W1–W5: delete the fully terminal Spec packages, reserve their
numbers, unlink current documents, and keep the checks passing without editing
a terminal Task body.

## Inputs and Authorization

The user directed that completed Spec, Plan, and Task documents in
`docs/03.specs/` be deleted, and chose to keep every package with a
non-terminal Task together with its completed Tasks. The coordinator moved the
branch-integration receipt handoff, Stage 98 preservation readers, and the
REQ-0026, AD-0030, and ADR-0037 revisions to the PR #723 review fix and limited
this Task's governance edits to the package-deletion rule. No push, pull
request, or merge from this Task.

The user's instruction to delete completed Spec, Plan, and Task documents is
the removal approval for this batch. On 2026-11-03 the owner also decided,
through the coordinator, that SPEC-0207 and SPEC-0210 are removal-ready on
their older-format acceptance records.

## Work Log

### Current contract decision

The user's direction authorizes this Spec and Plan as written.

### Current readiness and execution

Inputs, work units, and checks are recorded here. The Task is ready and in
progress under the approved parents. Hosted CI has not run.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0250 | draft | approved | #current-contract-decision |
| SPEC-0250-PLAN-0001 | draft | approved | #current-contract-decision |
| SPEC-0250-TSK-0001 | draft | ready | #current-readiness-and-execution |
| SPEC-0250-TSK-0001 | ready | in-progress | #current-readiness-and-execution |

### Deleted packages

SPEC-0182, 0207, 0208, 0210, 0211, 0213–0217, 0219–0225, 0227–0230, 0232,
0233, 0235–0237, 0239, 0241–0243, 0246 and 0247: 32 packages whose Spec, Plan,
and every Task were terminal and ready for removal review. Their numbers
joined the Spec `reserved_history`.

### Removal readiness

Read at `2227ea300`, before the first deletion; SPEC-0208 at `2571c5760`.

| Package | Criterion state | Unresolved required non-PASS |
| --- | --- | --- |
| SPEC-0182, 0211, 0213–0217, 0219–0225, 0227, 0228, 0230, 0232, 0233, 0235–0237, 0239, 0241–0243, 0246, 0247 | every typed Criterion Acceptance row `accepted` | none |
| SPEC-0229 | criteria 1, 2, 4 `accepted`; 3 `not-required` by the owner on 2026-10-29 | the NOT_RUN "Owner token run" row covers criterion 3 only |
| SPEC-0207 | no typed table; the older tables of TSK-0001 and TSK-0002 record criteria 1–7 PASS, and TSK-0003 records 1–6/W5 PASS/accepted. TSK-0003's body says "SPEC-0207 Spec/Plan remain in-progress" while the frontmatter read `approved` | none; ready by the owner's decision on 2026-11-03 |
| SPEC-0210 | no typed table; the independent reviewer explicitly accepted AC1–AC3 and Spec, Plan, and Task completed through `#final-acceptance` | none; ready by the owner's decision on 2026-11-03 |
| SPEC-0208 | no typed table; the older Review Evidence table records criteria 1–5 `accepted` | none; ready under the same older-format rule |

### Kept packages

| Package | Reason |
| --- | --- |
| SPEC-0204, 0212, 0218, 0226, 0244, 0245, 0248, 0249 | at least one non-terminal Task |
| SPEC-0209 | carries the generation 5 Contract Migration proof that admits current terminal Tasks closed under generations 3 and 4 |
| SPEC-0231 | carries the generation 6 Contract Migration proof |

Deleting all three proof carriers at once made `load_spec_packages` fail with
"lifecycle generation migration requires one proof". `_migration_proof` uses
only targets 5 and 6, and SPEC-0208's proof starts at generation 3, so
SPEC-0208 was then deleted alone: the load succeeded and corpus lifecycle
against `d6b535503` reported zero violations.

### Summary map

| Deleted package | Current owner of its still-current meaning |
| --- | --- |
| SPEC-0182 | ADR-0041, ADR-0042, POL-0021, GDE-0079 and the Stage 05 documents that name it for lineage |
| SPEC-0211 | the workflow contract and `.agents/knowledge` maps; the CI evidence owner label keeps its ID |
| SPEC-0213 | ADR-0047, REQ-0005, GDE-0021, POL-0021 |
| SPEC-0214 | AD-0006, AD-0026, GDE-0061, POL-0061 |
| SPEC-0215 | AD-0026, ADR-0004, REQ-0004, REQ-0006, POL-0078, RUN-0027 |
| SPEC-0219 | AD-0032 and POL-0101 |
| SPEC-0220 | GDE-0091 and the crawl4ai READMEs |
| SPEC-0221 | `scripts/README.md` and the agent governance contract |
| SPEC-0223, 0225 | `docker-compose.yml` comments and the observability guides |
| SPEC-0224 | GDE-0045, POL-0045 |
| SPEC-0228 | ADR-0041, POL-0021, POL-0048, RUN-0021 |
| SPEC-0229 | `grype_db_seed.py` comment |
| SPEC-0233 | ADR-0048 |
| SPEC-0236 | ADR-0049 |
| SPEC-0239, 0242, 0243 | ADR-0042, POL-0085, GDE-0085, RUN-0085, RUN-0105 |
| SPEC-0241 | `.github/rulesets/main-protection.md` |
| SPEC-0246 | POL-0102 Traceability (C1–C6) and POL-0021 (the 11 upstream images) |
| SPEC-0247 | `scripts/README.md` and the Hermes tests |
| SPEC-0207, 0208, 0210, 0216, 0217, 0222, 0227, 0230, 0232, 0235, 0237 | no current dependency |

### Check changes

- `spec_packages.py`: the SPEC-0211-TSK-0002 Resolves correction and its
  helper are removed, so a terminal Task body admits no change at all.
- `spec_packages.py`: generation 7 historical admission now reads only the
  packages still in the tree. Before, it re-read every package of the
  generation 7 source revision, and a deleted pre-generation-5 Task without an
  `## Evidence` section broke the load. Admission only ever applied to present
  Tasks, so this admits nothing new.
- `links.py`: alignment excuses a missing target only for a link from a
  terminal Task, at a registered Task path, by frontmatter or row-derived
  status, into `docs/03.specs/NNNN-*` where the checked root's Registry reserves
  NNNN. Terminal statuses and the reserved set both come from the checked
  root's Registry, so a missing or invalid one excuses nothing. This covers 13
  links in the completed SPEC-0212 Tasks 0003, 0007, and 0009.

### Reference cleanup

- 21 Markdown links in 11 current Stage 02 and Stage 05 documents and 7 links
  in editable Stage 03 documents became plain text.
- RUN-0098 no longer names SPEC-0182 in `parent_ids`; runbook parents are
  optional and no current policy owns the procedure.
- Two README path mentions of SPEC-0220 became the bare ID.
- POL-0021 lists the 11 upstream images that only the deleted SPEC-0246 Task
  named. POL-0102 Traceability summarizes SPEC-0246 C1–C6, and SPEC-0212
  TSK-0048 reads them there, with criterion 92 owned by @buenhyden.
- Present-tense pointers in GDE-0091, AD-0032 (now POL-0101), RUN-0027,
  GDE-0021, POL-0061, GDE-0061, and the infra exceptions verification text now
  say the record is in version history.
- Prose and code comments naming a deleted ID for lineage stay, as the
  documentation protocol allows. DATA-0096 `data.yaml` is a dated snapshot and
  stays. The CI gate evidence `owner` label `SPEC-0211-TSK-0003` stays; changing
  it is a gate-contract change.

### Test changes

| Test | Change | Reason |
| --- | --- | --- |
| `TerminalTaskResolvesCorrectionTests.test_registered_resolves_correction_matches` | replaced by `TerminalTaskBodyTests.test_the_former_resolves_correction_is_rejected` | the correction was removed; the test now asserts rejection |
| `TerminalTaskResolvesCorrectionTests` path and ID | repointed to a synthetic `0001-example` Task | SPEC-0211 is deleted |
| `RetiredPackageLinkTests` | added | a terminal Task link into a reserved package is excused; editable Task, unreserved number, missing Registry, and self-declared Task cases still fail. A run with the exemption disabled failed (RED) |
| `test_reference` evidence fixture anchor | SPEC-0209 row replaced by the SPEC-0204 row | the anchor must stay in the index |
| `test_ci_gate_plan` | four 0211 path strings repointed to `0001-example` | selector-only paths |
| `RetiredPackageLinkTests` | added row-derived multi-item cases (terminal and not), a target outside `docs/03.specs`, and a malformed Registry that exempts nothing | review M2 |

### Open issues

- The link exemption covers any Task that is terminal in the checked tree and
  any slug under a reserved number. That is the design ceiling the Spec
  contract states; narrowing it to Tasks terminal at the base needs a Git read.
- SPEC-0209 and SPEC-0231 stay until their migration proofs move out of
  Stage 03, for example into the Registry.
- The CI gate evidence `owner` label still reads `SPEC-0211-TSK-0003`; changing
  it is a gate-contract change.
- Version and `updated` bumps: metadata `check-changed` passes body edits
  without them, so only POL-0021 and POL-0102 were bumped, as the review asked.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W2 | corpus-lifecycle | tree with the 31 packages deleted | PASS | document corpus lifecycle zero violations; active stage occupancy zero | required | - |
| E2 | 3 | W3 | document-links | alignment mode after the reference cleanup | PASS | 850 documents, 7904 links, zero failures and warnings | required | - |
| E3 | 2 | W3 | metadata-changed | `check-changed --base-ref origin/chore/delete-stage98-archive` before this package | PASS | selected 124, zero violations | required | - |
| E4 | 3 | W1 | link-exemption-tests | `RetiredPackageLinkTests` | PASS | 2 tests OK; failed with the exemption disabled | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | - | @buenhyden |
| 2 | pending | - | - | @buenhyden |
| 3 | pending | - | - | @buenhyden |
| 4 | pending | - | - | @buenhyden |

## Review and Completion

Local checks are recorded above. Independent review and hosted CI have not run,
and no criterion is accepted yet.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
