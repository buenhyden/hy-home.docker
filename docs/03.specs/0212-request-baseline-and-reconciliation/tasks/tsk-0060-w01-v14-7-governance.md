---
title: "W01 v14.7 Governance Task"
version: "0.8.0"
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
revisions, and a Task record cannot authorize itself, so the owner was asked.
The four revision approvals given on 2026-11-12 are recorded under Common
contract adoption. Each row records only this repository's adoption state.

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
| GOV-01 | KEEP | `sdlc.md` owns Task execution state and approval separate from acceptance. The Repository Vocabulary now defines each term once with its policy owner (TSK-0059, `07f1943c6`). Consumer check: `test_generation7` rejects acceptance without PASS evidence and the deletion of failed rows (W01 final tests) |
| GOV-02 | KEEP | `bootstrap.md` limits the Provider Registry to translation; adapters own syntax only. Consumer check: agent governance contract PASS and renderer drift 0 (W01 final checks) |
| GOV-03 | CHANGE | Registry frontmatter rules are enforced. The adoption table adds a revision, approval and state per contract. The Release role removal has no contract id in the package, and TemplateDefinition is identified by its schema version; neither id is invented. Both are approved |
| GOV-04 | CHANGE (local) | TSK-0056 recorded "KEEP local, DEFER cross-repo" and deferred the contract fields. Local adoption is now recorded per contract, and partial adoption is labelled partial. Cross-repository adoption stays out of scope (D-04) |
| GOV-05 | PARTIAL | Policy KEEP: `github-governance.md` says one person's review is never two approvals, and an App or signature never stands in for owner acceptance. No local test exercises it, and the remote branch protection that enforces it was not read: UNVERIFIED (H-W01-3) |
| GOV-06 | KEEP | TSK-0056 gave the five duplicated rules one owner each. Renderer drift was 0 in this run (W01 final checks). `test_validator_entrypoints` shows that a hand-edited generated shim is reported as drift and regenerated, and that a hand-written `CLAUDE.md` is reported and never overwritten; these cases cover folder shims only (W01 final tests). The Markdown-versus-JSON ledger check is N/A: open items live only in the Task, with no second machine ledger to diverge. The glossary is read directly, never projected (TSK-0059 H-11). The review found the new reuse rule duplicating the execution identity, fixed by keeping one key list |
| GOV-07 | PARTIAL | Policy KEEP: the code-rule contradiction rule in `quality-standards.md` stands. It is a review rule, and no test rejects an implementation made to pass by changing only its tests (H-W01-6) |
| GOV-08 | PARTIAL | Policy KEEP: `approval-boundaries.md:63-67` reuses approval inside an approved scope. No test exercises that reuse. `test_agent_governance_ci_routing` covers only the refusal side, the deny rules for secret reads and `main` pushes (H-W01-5). Native runtime denial is UNVERIFIED |
| SUP-12 | KEEP (process) | This repository records only its own adoption. The consumer is this Task: no adoption row names another repository, checked in the independent reviews |
| R45-03, R147-19 | KEEP (process) | Q-08 path, the no-old-form decision and the OPEN-01/02 supersession are reused, and none was asked again. The only question in this run was the contract revision approval, which no earlier decision covered |
| R45-08, R147-09 | KEEP (done in TSK-0059) | Glossary in the Repository Vocabulary form at v14.5; profile, template and Registry test exist; Release document role removal kept (C-01) |
| R147-03 | CHANGE | Approved policy was corrected where it differs from the target; see Policy corrections |
| W01-A | CHANGE | Local adoption record below |
| W01-B | KEEP; test handed off | `approval-boundaries.md:25-31`: only the trusted user, operator or native channel authorizes, and a record in a Task, schema, CLI argument or hook cannot authorize itself. A negative test that injects a CI success as deployment approval is W05's (H-W01-1) |
| QA-C01 | PARTIAL | Revision and adoption recorded here; an automated check of consumer revisions is W05's (H-W01-2) |
| WP-06, WP-07 | KEEP, CHANGE | Same owners and verdicts as GOV-06 (KEEP) and GOV-04 (CHANGE) |
| Archive contract | KEEP | ADR-0051 summarize-and-delete retirement is consumed by `test_spec_packages` (an archive copy cannot record an unreserved removal) and `test_registry` (archive authorization needs scoped explicit approval) (W01 final tests). `docs/98.archive/` holds only `README.md` by listing; no check enforces README-only |

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

A second re-check found three rules that lived only in this Task or in a
README, which the prompt forbids (one owner per rule):

- `approval-boundaries.md` (1.4.1 to 1.5.0) now defines draft, approved and
  adopted, partial adoption, and the fields an adoption record names.
- `documentation-protocol.md` (3.14.0 to 3.15.0), Role-Specific Authoring, now
  owns the common role form: `COMMON-DOC-FORM-1` 1.0.0, one change per role
  covering all its current documents, the old form and placeholder bodies
  rejected for a moved role, unmoved roles kept on `SDLC-COMMON-r10-local-v1`,
  and a product difference handled as an Exception. It states that the
  validator orders required sections only. The templates README (2.4.0 to
  2.5.0) now only points to it.
- `quality-standards.md` (1.10.0 to 1.11.0) says the canonical delivery phase
  matrix implements `QA-STAGES-1` 1.0.0 and that not all of its Git-stage cells
  are implemented yet.

The delivery phase matrix itself is KEEP. Implementing the Git-stage cells is
W06's (TSK-0059 H-09).

### Common contract adoption

States follow `approval-boundaries.md:79-84`: draft, then approved, then
adopted once implemented on `main` and verified; partial is called partial.
The obligation is approved. Q-08 and the Release role removal are named in the
owner's prompt. On 2026-11-12 @buenhyden approved `repository-vocabulary`
v14.5, `COMMON-DOC-FORM-1` 1.0.0, `QA-STAGES-1` 1.0.0 and the TemplateDefinition
v14.5 schema for this repository, answering a question that named each
revision as taken from the package contract files. Binding each revision to a
file hash is this Task's own record.

Fields common to every row: single authoring owner @buenhyden, who owns the
shared contracts (`approval-boundaries.md:73-77`); the authoring file is the
package contract file, and Project-Template `dev` as the shared authoring copy
is UNVERIFIED (D-04). Exceptions: none. Effective date: set when the change
merges to `main`; nothing here is effective yet.

| Contract | Revision (package file, SHA-256 prefix) | Local scope | State here | Consumer version | Migration and rollback |
| --- | --- | --- | --- | --- | --- |
| Repository Vocabulary | `repository-vocabulary` v14.5 (`REPOSITORY-VOCABULARY.json`, `b03ae3c00a42`) | `.agents/knowledge/glossary.md`, `governance-vocabulary` profile | Approved; implemented on this branch, not on `main` | Glossary `Contract Version` column reads v14.5 | Done in `07f1943c6`, `8903eeaf2`, `4ec4d7182`; rollback is a revert of those commits |
| Common section form | `COMMON-DOC-FORM-1` 1.0.0 (`COMMON-SECTION-CONTRACT.json`, `4f79183d59c3`) | 16 common roles | Approved; partial: 3 of 16 roles on this branch (Incident, Postmortem, AGENTS) | Named in `documentation-protocol.md`; not in the Registry (H-W01-2) | Per role in one commit, no old form; remaining roles TSK-0059 H-04. Rollback: revert that role's commit |
| Stage QA | `QA-STAGES-1` 1.0.0 (`STAGE-QA-MATRIX.json`, `12d8962c96c7`) | `quality-standards.md`, workflows and hooks | Approved; partial: policy meanings on this branch, not all Git-stage cells | Named in `quality-standards.md` | Cells are TSK-0059 H-09 (W06). Rollback: revert `532902934` and the `quality-standards.md` hunks of `6b5c4bf27` and `6885be9cf` |
| TemplateDefinition | v14.5 schema (`TEMPLATE-DEFINITION.schema.json`, `e490cf402419`) | Registry and templates | Approved; not implemented | None | TSK-0059 H-06 (W03). Rollback: none needed |
| Template path | `Q-08` (`TEMPLATE-PATH-DECISION.json`, `7089347e62b1`) | `docs/99.templates/` | Adopted: approved in the prompt, path unchanged | N/A, a path decision | None |
| Release document role removal | v14.7 direct requirement; no contract id | documentation protocol, Registry guards | Approved; partial: policy and fixed-name guards on this branch, renamed profiles not yet rejected | N/A, no contract id | Wider guard TSK-0059 H-12 (W05). Rollback: revert `7f1c82ab9` |

Every implemented state above rests on changes on this branch that are not
yet on `main`. No row is reported as adopted by another repository.

### Handoffs

| ID | Writer | Difference |
| --- | --- | --- |
| H-W01-1 | W05 | A negative test that a CI success, check result or role string is rejected as approval for a deployment or other protected operation |
| H-W01-2 | W05 | An automated check that each consumer reads the adopted contract revision recorded here (QA-C01); the Registry does not yet name the `COMMON-DOC-FORM-1` revision it implements |
| H-W01-3 | W06 | Observe, read only, whether the remote branch protection enforces GOV-05 (one person's review is not two approvals), and record it |
| H-W01-4 | W05 | Vocabulary violation fixtures: a merged PR read as Acceptance, an OPEN ID read as current state, and an approved Registry read as a KEEP exemption are each rejected |
| H-W01-5 | W05 | GOV-08: a test that an approved reversible edit inside the request's scope proceeds without a second approval, next to the existing refusals |
| H-W01-6 | W05 | GOV-07: a test that rejects an implementation made to pass by changing only its tests or by adopting an unapproved test constant as policy |

### W01 re-check 2026-11-12

A second pass compared the whole W01 prompt with this Task and found four
conflicts with the current requirement, each corrected above:

- KEEP needs a consumer check, not policy text alone. Each executable KEEP now
  names the test or check that consumes it; process KEEPs name the record that
  shows them. GOV-05, GOV-07 and GOV-08 have no consumer test of their rule and
  are PARTIAL.
- The adoption table called implemented work "adopted" while revision approval
  was pending. States now follow draft, approved and adopted, and the owner
  then approved the four revisions.
- The contract fields lacked owner, consumer version, exceptions, effective
  date and rollback; they are now recorded, and the missing consumer versions
  go to H-W01-2.
- The archive contract KEEP and the vocabulary violation cases were not
  recorded; they are now (Archive row, H-W01-4).

The role and relation table in prompt section 7.2 is reused from the
documentation protocol; relation fields are W03's and state meanings W04's
(TSK-0059 H-06 and H-07).

### Read denominator

| Surface | Read |
| --- | --- |
| W01 prompt | All 501 lines, re-read in the re-check |
| Consumer tests | `test_validator_entrypoints` renderer cases, `test_generation7`, `test_agent_governance_ci_routing` deny cases, the archive cases in `test_spec_packages` and `test_registry` |
| Governance policies | `approval-boundaries.md` 1.5.0 (Authorization Source and Records, shared-contract bullet), `quality-standards.md` 1.11.0 (QA reuse rule, Execution Boundary, Canonical delivery phase matrix), `documentation-protocol.md` 3.15.0 (README and AGENTS.md, Role-Specific Authoring), read in full at each commit that changed them, plus the earlier W01 and W00 citations |
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
| W01 consumer tests | 113 | W118 | consumer-unittest | `tests.validation.test_validator_entrypoints`, `tests.lib.document_governance.test_generation7` at `7bec8a82f` | PASS | 22 tests OK | required | - |
| W01 policy tests | 113 | W118 | policy-unittest | Five modules reading `quality-standards.md` (`test_ci_gate_evidence`, `test_github_workflow_contract`, `test_agent_governance_ci_routing`, `test_spec_packages`, `test_registry`), run while the review fixes were uncommitted | FAIL | 369 tests, 1 failure; the output was cut to its last lines, so the failing test was not identified | required | - |
| W01 policy tests result | 113 | W118 | policy-unittest | Same five modules at `7bec8a82f`, clean tree | PASS | 369 tests OK in 861 s | required | W01 policy tests |
| W01 re-check review | 113 | W118 | independent-review | Commits `c61f518d4` to `b947ec52d` | FAIL | rules-engineer CHANGES_REQUIRED: nine Important and five Minor findings (overclaims in the protocol bullet, README still owning rules, GOV-06, GOV-07 and GOV-08 evidence, adoption fields and labels, stale pending text, no evidence at the new revision) | required | - |
| W01 re-check review result | 113 | W118 | independent-review | Commits `6885be9cf`, `46fb58b84`, `5bc39297e` and `8628193b9` | PASS | rules-engineer re-review: 13 of 14 findings resolved, then the protocol's Task dependency and four minor items fixed; final verdict PASS | required | W01 re-check review |
| W01 final checks | 113 | W118 | metadata-links-governance | HEAD `8628193b9` | PASS | metadata check-changed selected 29 violations 0; links alignment PASS; occupancy 0; agent governance contract PASS; renderer drift 0; operations catalog PASS | required | - |
| W01 final tests | 113 | W118 | policy-unittest | Nine modules (`test_ci_gate_evidence`, `test_github_workflow_contract`, `test_agent_governance_ci_routing`, `test_spec_packages`, `test_registry`, `test_heading`, `test_profile`, `test_validator_entrypoints`, `test_generation7`) started at `8628193b9`. W02 edits to Stage 02 and 05 documents and to the protocol's retention section were made in the working tree during the run | PASS | 497 tests OK in 925 s | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 113 | accepted | W01 v14.7 assessment, W01 policy checks result, W01 independent review, W01 re-check review result, W01 final checks, W01 final tests | Owner accepted on 2026-11-12 in this chat. Handoffs H-W01-1 to H-W01-6 and the partial or unadopted contracts stay with their named owners | SPEC-0212 TSK-0060 |

## Review and Completion

In progress. The assessment, the adoption record and the policy corrections
are recorded. The owner accepted criterion 113 on 2026-11-12. The Task stays
in progress only as the record of the contract adoption it started.
Open: H-W01-1, H-W01-2, H-W01-4, H-W01-5 and H-W01-6 (W05), H-W01-3 (W06), and the partial or unadopted contracts
through TSK-0059 H-04, H-06, H-09 and H-12.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [v14.2 W01 governance standardization](tsk-0056-w01-governance-standardization.md)
- [v14.7 W00 intake](tsk-0059-w00-v14-7-intake.md)
- [Approval boundaries](../../../../.agents/governance/approval-boundaries.md)
- [Quality standards](../../../../.agents/governance/quality-standards.md)
