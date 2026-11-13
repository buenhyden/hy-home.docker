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
repositories. Twenty rows had local narrowings or dropped clauses. Each is
now an English rendering of the contract row, and its local meaning moved to
a Local Extensions row:

| Term ID | Deviation | Local Extensions row |
| --- | --- | --- |
| TERM-CANONICAL | Added "an authored file under `.agents/`" | Canonical location |
| TERM-APPROVAL | Dropped "distinct from accepting the result" | - |
| TERM-ADOPTION | Added the Task record and tracked configuration | Adoption record |
| TERM-EXECUTION | Moved the contract's distinction to Not to Confuse | - |
| TERM-ACCEPTANCE | Added runtime and risk acceptance; "authorized owner" for "authorized party" | Acceptance record |
| TERM-RETIREMENT | Merged retirement into file deletion | Retirement, here |
| TERM-ARCHIVE | Replaced the common goal with the local binding | Archive, here |
| TERM-REMOVAL | Dropped "or an approved separate copy" | - |
| TERM-REGISTRY | Added the file path; template instead of generator bindings | Registry file |
| TERM-TEMPLATE | Dropped "common rules, policies" | - |
| TERM-PROFILE | Replaced the definition with the Registry entry form | Document Profile entry |
| TERM-EVIDENCE | Replaced the scopes with local evidence classes | Evidence class (existing) |
| TERM-RESOLVES | Narrowed to a PASS row with the same Check and Work Unit | Resolves row |
| TERM-SUPERSESSION | Added "reciprocal" | Supersession lineage |
| TERM-HOLD | Added "recorded"; "until resolved" for "until a basis to resolve" | - |
| TERM-EXCEPTION | "review condition" for "period or end condition" | - |
| TERM-TASK | Dropped "derive from" | - |
| TERM-PROJECTION | Dropped "synchronized" | - |
| TERM-HARNESS | Not to Confuse dropped "as actual application" | - |
| TERM-VERIFICATION | "owner acceptance" for "user acceptance" | - |

An automated comparison of the common rows with the contract file stays
H-W01-4 (W05).

The glossary moves from `draft` to `active`, an allowed `living` transition:
the contract it implements is approved and adopted on `main` (TSK-0060).

#### Never-retire rule 2026-11-13

The documentation protocol's Retention by status section now says Incident
and Postmortem records never retire, and that a Registry disposition entry
listing a status its lifecycle cannot reach is a defect. Removing those
Registry entries and the reachability check stay with W05.

#### TemplateDefinition binding 2026-11-13

`template_definition.py` now derives the three contract-conditional H3s
(Requirement Quality Requirements, ADR Supersession, Runbook Rollback) as
`conditional` with the contract condition through `conditional_units`,
keeps the template's declared subsection order, and carries each role's
contract prohibited content from the new Registry
`common.section_prohibited_content` (English renderings, 21 roles). A test
rejects a key that names no template role.

Recorded, not changed: the H3 rule list keeps both empty-section rules in
addition to the contract's two, and the empty-section rules omit the
contract's "only a template guidance comment" case; both predate this change
and go to W05 with the validators.

#### Link types and document relations 2026-11-13

The documentation protocol gains `Link types and document relations`, and the
Registry `common` binds `link_types`, `link_profiles` and
`document_relations`, validated by `registry.py` against the profile schema:

- R08: normative, evidence, historical and navigation links, each forward
  only, with requiredness, authority, a pinned version and the consumer
  action when the target is removed or moved. Vault wiki links are a separate
  `vault-wiki` profile.
- R07: `rel.traceability` (child to parent through `parent_ids`, and
  `supersedes`), `rel.ownership` (frontmatter `owner`), `rel.authority`
  (normative links), `rel.reference` (other links) and
  `rel.change-propagation` (derived), each with direction, writers and the
  check that validates the writer. The reviewer derives reverse lookups and
  change propagation at removal or move time; no tool derives them yet.

Authors assign link types and reviewers confirm them. The checkers enforce
only that links resolve, that metadata keys and `parent_ids` are valid and
that the Registry binding is valid; the schema pins every relation ID and direction and every
link-type and link-profile value, and the validator checks the writers,
owners and retained reverse fields. Existing documents are not retyped, and tool enforcement of
types, reverse lookups and change propagation goes to W05.
`superseded_by` stays as a recorded hand-written reverse until the
coordinated lineage change the protocol already requires. The Registry
`template_roles[*].consumer_paths` list is a manual reverse lookup; it is
recorded for W05.

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
| Glossary contract comparison | 115 | W120 | contract-row-comparison | Each common row against `REPOSITORY-VOCABULARY.json` v14.5, commit `a69ee1f54` | FAIL | Fresh-context rules-engineer: 13 restored rows faithful, but TERM-SUPERSESSION, HOLD and EXCEPTION still added meaning and five rows dropped or shifted a clause; the Resolves row omitted "required" and "shared criterion" | required | - |
| Glossary contract re-comparison | 115 | W120 | contract-row-comparison | All 33 common rows and the Local Extensions rows at commit `40618cb38` | PASS | Same reviewer: every common row matches `REPOSITORY-VOCABULARY.md` in meaning; the 20 corrected rows listed above; Supersession lineage and Resolves rows match their policy lines | required | Glossary contract comparison |
| TemplateDefinition RED | 115 | W120 | red-green-proof | Three new tests against `template_definition.py` before the fix | FAIL | 23 failures: Rollback, Supersession and Quality Requirements derived `optional`; Runbook Recovery order Escalation before Rollback; 21 roles without their prohibited content | required | - |
| TemplateDefinition GREEN | 115 | W120 | red-green-proof | `test_template_definition`, `metadata.test_heading`, `test_registry` at `88613bc30` | PASS | 242 tests OK | required | TemplateDefinition RED |
| TemplateDefinition review | 115 | W120 | independent-review | Fresh-context code-reviewer of `88613bc30` | PASS | No Critical or Important finding; conditional set, order and 15 role texts checked against the contract; three Minor findings, the unchecked map keys fixed by a test | required | - |
| Relation types RED | 115 | W120 | red-green-proof | Ten new `test_relations` tests before the Registry binding | FAIL | All ten errored with `KeyError: 'link_types'` | required | - |
| Relation types GREEN | 115 | W120 | red-green-proof | `test_relations` and `test_registry` at `5adac8664` | PASS | 138 tests OK; two historical-Registry cases first failed and were fixed by checking the contract only where the schema declares it | required | Relation types RED |
| Relation types review | 115 | W120 | independent-review | Fresh-context rules-engineer of `e8b456e00` | FAIL | CHANGES_REQUIRED: the policy claimed checker enforcement and derived lookups that no code provides; the schema accepted any relation, link type or profile value; four minor (`superseded_by` wording, Vault converter, evidence pinning, test gaps) | required | - |
| Relation fix RED | 115 | W120 | red-green-proof | Three new mutation tests against `e8b456e00` | FAIL | 11 of 14 mutation cases accepted, including a derived writer naming its own relation | required | - |
| Relation fix GREEN | 115 | W120 | red-green-proof | `test_relations`, `test_registry`, `test_template_definition`, `test_surface_ownership` at `535557ef8` | PASS | All pass; check-contracts 0, agent governance contract 0, links alignment 0 | required | Relation fix RED |
| Relation types re-review | 115 | W120 | independent-review | Same reviewer, commits `535557ef8` and `dfdb04c1d` | FAIL | All six earlier findings resolved; new Important: policy and this Task claimed the schema pins every table value, but writers, owners and retained reverse fields are only validator-checked; Minor: the policy named the W05 wave | required | - |

### Resolution Links

The Glossary contract comparison FAIL is resolved by the Glossary contract re-comparison PASS, TemplateDefinition RED by TemplateDefinition GREEN, Relation types RED by Relation types GREEN, and Relation fix RED by Relation fix GREEN. The Relation types review and re-review FAILs are resolved by the final re-review once it passes.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 115 | pending | - | - | SPEC-0212 TSK-0062 |

### Remaining Conditions

All four corrections are on this branch. The relation review, the final
checks and owner acceptance of criterion 115 are open.

## Handoff

### Promotion Receipt

None: the change has not landed on `main` yet.

### Next Owner

The current owner is @buenhyden, who decides criterion 115.
