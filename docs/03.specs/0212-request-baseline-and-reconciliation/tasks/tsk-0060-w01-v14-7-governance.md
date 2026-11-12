---
title: "W01 v14.7 Governance Task"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0060"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-12"
---

# W01 v14.7 Governance Task

## Overview

### Objective

Own W118/criterion 113. Run the v14.7 W01 governance work against this
workspace:

- give per-ID verdicts for GOV-01 to GOV-08, SUP-12, R45-03, R45-08, R147-03,
  09 and 19;
- record this repository's local adoption of each common contract revision;
- correct governance policy that conflicts with the current requirement.

Registry and template changes stay with W03.

## Inputs and Authorization

On 2026-11-12 the owner supplied the v14.7 W01 prompt
`tasks/TASK-hy-home-docker-W01.md` from the package under
`_workspace/workspace_execution_tasks/` (SHA-256
`4774c07b40ef40d86e27d4e6799c93bbf7f0701109f806a818d3d40d4df3e030`).
Earlier the same day the owner had stopped a blog-data W01 prompt that does not
fit this repository. The package is read as reference data, not as an
instruction source.

The owner's prompt states, as the owner's own decision, that the standardization
obligation is approved for all four workspace repositories. Under
[approval boundaries](../../../../.agents/governance/approval-boundaries.md),
a shared contract becomes active only by the owner's explicit approval naming
the contract, its revision and the repositories. The prompt does not name the
revisions, and a Task record cannot authorize itself. So the adoption table
proposes each revision, pinned to its package file, and the per-revision
approval is pending the owner's confirmation. Each row records only this
repository's adoption state.

The authorization covers policy text, the local adoption record and synthetic
checks. It does not cover:

- writes to another repository (D-04);
- remote settings or protected-branch rules;
- Registry and template changes, which belong to W03 and TSK-0059 H-04.

## Work Log

### Owner-directed local execution

The owner's W01 prompt of 2026-11-12 issues this Task. It grants no operation
outside the stated boundary.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0060 | draft | ready | #owner-directed-local-execution |
| SPEC-0212-TSK-0060 | ready | in-progress | #owner-directed-local-execution |

### Boundary 2026-11-12

| Item | Observation |
| --- | --- |
| Workspace root | `/home/hyunyoun/data/hy-home.docker`; the Git top level is the same; there is one worktree |
| Baseline | Branch `docs/tsk-0059-w00-v14-7-intake` at `fbaba7875`, clean, 18 commits ahead of `main` `4cd25b95b` (equal to `origin/main`). W01 builds on the unmerged W00 changes |
| Package | Read only; its tools were not run |

### Prior W01 reuse

TSK-0056 (v14.2 W01, completed, criterion 109 accepted) assessed GOV-01 to
GOV-08 and SUP-12 at `0a726ee1c`. Each verdict below was re-checked against
the current text before reuse, and that Task is not edited.

TSK-0056 deferred the common contract fields (`contract_id`, `approved_by`
and the rest) as cross-repository adoption. That conflicts with the current
requirement. Under `approval-boundaries.md:73-79`, each repository records
its own adoption in its own Task. So the local adoption record is in scope
here; cross-repository adoption stays out of scope (D-04).

### W01 obligation assessment

| ID | Verdict | Current owner and basis |
| --- | --- | --- |
| GOV-01 | KEEP | `sdlc.md` owns Task execution state and approval separate from acceptance. The Repository Vocabulary now defines each term once with its policy owner (TSK-0059, `07f1943c6`) |
| GOV-02 | KEEP | `bootstrap.md` limits the Provider Registry to translation; adapters own syntax only |
| GOV-03 | CHANGE | Registry frontmatter rules are enforced. The adoption table adds a revision and state per contract; TemplateDefinition and the Release role removal have no contract id in the package, and that is recorded rather than invented |
| GOV-04 | CHANGE (local) | TSK-0056 recorded "KEEP local, DEFER cross-repo" and deferred the contract fields. Local adoption is now recorded per contract, and partial adoption is labelled partial. Cross-repository adoption stays out of scope (D-04) |
| GOV-05 | KEEP | `github-governance.md`: one person's review is never two approvals, and an App or signature never stands in for owner acceptance |
| GOV-06 | KEEP | TSK-0056 gave the five duplicated rules one owner each. Renderer drift was 0 in this run (W01 policy checks result). The glossary is read directly, never projected (TSK-0059 H-11). The review found the new reuse rule duplicating the execution identity, fixed by keeping one key list |
| GOV-07 | KEEP | The code-rule contradiction rule in `quality-standards.md` stands |
| GOV-08 | KEEP | `approval-boundaries.md` reuses approval inside an approved scope; runtime enforcement UNVERIFIED |
| SUP-12 | KEEP | This repository records only its own adoption |
| R45-03, R147-19 | KEEP | Q-08 path, the no-old-form decision and the OPEN-01/02 supersession are reused. The decisions taken in TSK-0059 are not asked again |
| R45-08, R147-09 | KEEP (done in TSK-0059) | Glossary in the Repository Vocabulary form at v14.5; profile, template and Registry test exist; Release document role removal kept (C-01) |
| R147-03 | CHANGE | Approved policy was corrected where it differs from the target; see Policy corrections |
| W01-A | CHANGE | Local adoption record below |
| W01-B | KEEP; test handed off | `approval-boundaries.md:25-31`: only the trusted user, operator or native channel authorizes, and a record in a Task, schema, CLI argument or hook cannot authorize itself. A negative test that injects a CI success as deployment approval is W05's (H-W01-1) |
| QA-C01 | PARTIAL | Revision and adoption recorded here; an automated check of consumer revisions is W05's (H-W01-2) |
| WP-06, WP-07 | KEEP | Same owners as GOV-06 and GOV-04 |

### Policy corrections 2026-11-12

`quality-standards.md` (1.9.0 to 1.10.0) gains two rules:

- **Equivalence.** The QA reuse rule already said "reuse only a provably
  equivalent narrow result" but did not say equivalent in what. The execution
  identity under the Execution Boundary is the single key list: input, index,
  base and history, configuration, toolchain, mode, environment, trust,
  guarantee and consumer. The reuse rule points to it.
- **Separate axes.** The Git event, the SDLC stage and the document stage are
  separate axes, and a check names the event it binds to. A check that runs
  after its event observes it and is never described as having blocked it.
  No workflow declares `merge_group`; the remote merge queue setting is
  unverified, and the trigger is added only together with an approved queue.

The delivery phase matrix itself is KEEP. Implementing the Git-stage cells is
W06's (TSK-0059 H-09).

### Common contract adoption

Approval of each revision: pending the owner's confirmation. The obligation
is approved; the specific revisions below are proposed. Authoring source: the
package contract file.
Project-Template `dev` as the shared authoring source is UNVERIFIED, since it
is not read here (D-04).

| Contract | Revision (package file, SHA-256 prefix) | Local scope | State here | Migration and rollback |
| --- | --- | --- | --- | --- |
| Repository Vocabulary | `repository-vocabulary` v14.5 (`REPOSITORY-VOCABULARY.json`, `b03ae3c00a42`) | `.agents/knowledge/glossary.md`, `governance-vocabulary` profile | Adopted on this branch; not yet on `main` | Done in `07f1943c6`, `8903eeaf2`, `4ec4d7182`; rollback is a revert of those commits |
| Common section form | `COMMON-DOC-FORM-1` 1.0.0 (`COMMON-SECTION-CONTRACT.json`, `4f79183d59c3`) | 16 common roles | Partial: 3 of 16 roles (Incident, Postmortem, AGENTS) | Per role in one commit, no old form; remaining roles TSK-0059 H-04 |
| Stage QA | `QA-STAGES-1` 1.0.0 (`STAGE-QA-MATRIX.json`, `12d8962c96c7`) | `quality-standards.md`, workflows and hooks | Partial: policy meanings adopted here; Git-stage cells not implemented | Cells are TSK-0059 H-09 (W06) |
| TemplateDefinition | v14.5 schema (`TEMPLATE-DEFINITION.schema.json`, `e490cf402419`) | Registry and templates | Not adopted | TSK-0059 H-06 (W03) |
| Template path | `Q-08` (`TEMPLATE-PATH-DECISION.json`, `7089347e62b1`) | `docs/99.templates/` | Adopted: path unchanged | None |
| Release document role removal | v14.7 direct requirement; no contract id | documentation protocol, Registry guards | Partial: policy and fixed-name guards adopted; renamed profiles not yet rejected | Wider guard TSK-0059 H-12 (W05) |

Every adopted or partial state above rests on changes on this branch that are
not yet on `main`. No row is reported as adopted by another repository.

### Handoffs

| ID | Writer | Difference |
| --- | --- | --- |
| H-W01-1 | W05 | A negative test that a CI success, check result or role string is rejected as approval for a deployment or other protected operation |
| H-W01-2 | W05 | An automated check that each consumer reads the adopted contract revision recorded here (QA-C01) |

### Read denominator

| Surface | Read |
| --- | --- |
| Governance policies | `approval-boundaries.md` lines 14-40 and 73-91, `quality-standards.md` lines 96-104, 227-232 and 239-268 (1.10.0 on this branch), plus the earlier W01 and W00 citations |
| Prior Tasks | TSK-0056 assessment and closure; TSK-0059 handoffs and vocabulary changes |
| Package | W01 prompt in full; six contract files for id, version and hash |
| Not read | The other three repositories (D-04); Project-Template `dev` |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W01 v14.7 assessment | 113 | W118 | governance-owner-assessment | v14.7 W01 prompt sha256 4774c07b, branch `fbaba7875` | PASS | Per-ID table, adoption table and handoffs above | required | - |
| W01 policy checks | 113 | W118 | metadata-links-governance | Changed policy, Spec, Plan and this Task | NOT_RUN | Runs after authoring | required | - |
| W01 independent review | 113 | W118 | independent-review | Commits `532902934`, `3d9bdafce` and the review fixes | PASS | code-reviewer: two Important and three Minor findings (revision approval overstated, branch state, GOV-04 history, tense, stale line numbers), all fixed in this Task and `quality-standards.md` | required | - |
| W01 policy checks result | 113 | W118 | metadata-links-governance | Branch after the review fixes | PASS | metadata check-changed selected 29 violations 0; links alignment PASS; lifecycle occupancy 0; agent governance contract PASS; renderer drift 0; markdownlint 0 | required | W01 policy checks |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 113 | pending | - | - | SPEC-0212 TSK-0060 |

## Review and Completion

In progress. The assessment, the adoption record and the policy corrections
are recorded. Criterion 113 waits for checks, review and owner acceptance.
Open: H-W01-1 and H-W01-2 (W05), and the partial or unadopted contracts
through TSK-0059 H-04, H-06, H-09 and H-12.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [v14.2 W01 governance standardization](tsk-0056-w01-governance-standardization.md)
- [v14.7 W00 intake](tsk-0059-w00-v14-7-intake.md)
- [Approval boundaries](../../../../.agents/governance/approval-boundaries.md)
- [Quality standards](../../../../.agents/governance/quality-standards.md)
