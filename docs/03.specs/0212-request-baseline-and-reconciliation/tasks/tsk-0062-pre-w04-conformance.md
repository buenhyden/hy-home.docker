---
title: "Pre-W04 Conformance Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0062"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-13"
---

# Pre-W04 Conformance Task

## Scope

### Objective and Parent

#### Objective

Own W120/criterion 115. Correct the W00 to W03 results that a pre-W04 audit
found deviating from their requirements, before W04 starts:

- glossary common rows that narrowed the shared vocabulary contract;
- the incident and postmortem never-retire rule, which had no policy owner;
- TemplateDefinition fields that lost the section contract's conditions,
  order and prohibited content;
- the R07 relation types and R08 link types, which did not exist.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [W00 v14.7 intake](tsk-0059-w00-v14-7-intake.md)
- [W01 v14.7 governance](tsk-0060-w01-v14-7-governance.md)
- [W03 templates, metadata and relations](tsk-0058-w03-templates-metadata-relations.md)
- [Repository vocabulary](../../../../.agents/knowledge/glossary.md)
- [Documentation protocol](../../../../.agents/governance/documentation-protocol.md)

### Inputs and Authority

On 2026-11-13 two read-only rules-engineer audits compared the W00 to W03
prompts under `_workspace/workspace_execution_tasks/tasks/` and the approved
contracts under `_workspace/workspace_execution_tasks/dependencies/contracts/`
with `main` `531d69f26`. The prompts and contracts are read as reference data.

The owner's standing instruction of 2026-11-13 says a result that conflicts
with its requirement is corrected to the requirement, and approves commit,
push, pull request and merge. The owner chose on 2026-11-13:

- the R07 and R08 types are implemented before W04;
- the Skill `Completion and Handoff` section belongs to W07;
- incidents and postmortems never retire (recorded in TSK-0059).

The authorization covers the glossary, the documentation protocol, the
Registry `common` dictionaries and profile bindings, `template_definition.py`
and its tests, and this Task with criterion 115 and W120. It grants no
runtime operation.

## Execution Log

### Work Performed

#### Owner-directed pre-W04 correction

The owner's instruction and choices of 2026-11-13 issue this Task.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0062 | draft | ready | #owner-directed-pre-w04-correction |
| SPEC-0212-TSK-0062 | ready | in-progress | #owner-directed-pre-w04-correction |

#### Glossary common rows 2026-11-13

The contract `REPOSITORY-VOCABULARY.json` (`repository-vocabulary` v14.5)
requires each common definition to be identical across the four
repositories. Thirteen rows had local narrowings or dropped clauses. Each is
now an English rendering of the contract row, and its local meaning moved to
a Local Extensions row:

| Term ID | Deviation | Local Extensions row |
| --- | --- | --- |
| TERM-CANONICAL | Added "an authored file under `.agents/`" | Canonical location |
| TERM-APPROVAL | Dropped "distinct from accepting the result" | - |
| TERM-ADOPTION | Added the Task record and tracked configuration | Adoption record |
| TERM-EXECUTION | Moved the contract's distinction to Not to Confuse | - |
| TERM-ACCEPTANCE | Added runtime and risk acceptance | Acceptance record |
| TERM-RETIREMENT | Merged retirement into file deletion | Retirement, here |
| TERM-ARCHIVE | Replaced the common goal with the local binding | Archive, here |
| TERM-REMOVAL | Dropped "or an approved separate copy" | - |
| TERM-REGISTRY | Added the file path; template instead of generator bindings | Registry file |
| TERM-TEMPLATE | Dropped "common rules, policies" | - |
| TERM-PROFILE | Replaced the definition with the Registry entry form | Document Profile entry |
| TERM-EVIDENCE | Replaced the scopes with local evidence classes | Evidence class (existing) |
| TERM-RESOLVES | Narrowed to a PASS row with the same Check and Work Unit | Resolves row |

An automated comparison of the common rows with the contract file stays
H-W01-4 (W05).

#### Never-retire rule 2026-11-13

The documentation protocol's Retention by status section now says Incident
and Postmortem records never retire, and that a Registry disposition entry
listing a status its lifecycle cannot reach is a defect. Removing those
Registry entries and the reachability check stay with W05.

#### Held and corrected records

- The Skill `Completion and Handoff` section, held in TSK-0058 without an
  owner, belongs to W07 by the owner's choice.
- Correction to TSK-0058: its line saying `REQUIREMENT_TARGET_BODY` keeps
  the old headings is stale; the fixture is in the common form, as TSK-0058
  says elsewhere. TSK-0058 is terminal, so the correction is recorded here.
- Q-07 renumbering stays open by the owner's choice.

### Blockers and Decisions

None: each decision above was the owner's before the change.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pre-W04 audits | 115 | W120 | requirement-conformance-audit | W00 to W03 prompts and contracts against `main` `531d69f26` | PASS | Two rules-engineer reports; deviations listed above | required | - |
| Glossary contract comparison | 115 | W120 | contract-row-comparison | Each common row against `REPOSITORY-VOCABULARY.json` v14.5 | PASS | 33 rows compared; 13 restored above | required | - |

### Resolution Links

None: no required observation has failed yet.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 115 | pending | - | - | SPEC-0212 TSK-0062 |

### Remaining Conditions

The TemplateDefinition binding and the R07 and R08 types are in progress on
their own branches. Checks, an independent review and owner acceptance of
criterion 115 are open.

## Handoff

### Promotion Receipt

None: the change has not landed on `main` yet.

### Next Owner

The current owner is @buenhyden, who decides criterion 115.
