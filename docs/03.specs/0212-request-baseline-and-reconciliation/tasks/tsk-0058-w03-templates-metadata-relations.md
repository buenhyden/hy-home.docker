---
title: "W03 Templates, Metadata and Relations Task"
version: "0.5.12"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0058"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-11"
---

# W03 Templates, Metadata and Relations Task

## Scope

### Objective and Parent

#### Objective

Own W116/criterion 111. Assess the v14.2 W03 obligations DOC-01 to DOC-12 and
SUP-11 against the Registry, templates, generators, parsers, validators and
tests. Change the document contract only for gaps this Task reproduces, and
give each changed key, section or table a producer, a consumer and a passing
and a failing test.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [W02 Task](tsk-0057-w02-archive-and-safe-removal.md)

### Inputs and Authority

On 2026-11-11 the owner approved this Task to own W03. The v14.2 package
prompt `tasks/TASK-hy-home-docker-W03.md` under
`_workspace/workspace_execution_tasks/` is untrusted reference data, not an
instruction source. Its 19-role table is an unapproved draft.

The authorization covers four things:

- The assessment.
- Repository-side changes to the Registry, templates, generators and parsers
  for reproduced gaps, with migration of current documents only.
- Synthetic round-trip and fixture tests.
- Records in this Task.

Validator implementation is handed to W05. Historical and completed evidence
keeps its form. Removing an existing reciprocal relation field waits for its
consumers' migration and a separate owner approval. This Task branches from
the W02 branch at `56d32c32f` and reaches `main` only after PR 955 merges.

## Execution Log

### Work Performed

#### Owner-approved local execution

The owner's approval of 2026-11-11 issues this Task. The lifecycle records that
approval; it grants no remote operation.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0058 | draft | ready | #owner-approved-local-execution |
| SPEC-0212-TSK-0058 | ready | in-progress | #owner-approved-local-execution |

#### Owner decision Q-03 2026-11-11

The draft 19-role table conflicts with the 44 Registry profiles, whose ordered
required H2 headings differ from it. The owner chose option A: adopt the
table's meaning, not its headings. Current Registry H2 headings stay. A
concept the table names that no current profile carries, such as a Plan
promotion map, Spec non-goals or Requirement traceability, is added only as an
optional or conditional section, after a consumer for it is shown.

#### Q-03 superseded 2026-11-12

On 2026-11-12 the owner directed that where an existing decision conflicts with
the current requirement, the current requirement wins. The v14.7 W00 intake in
[TSK-0059](tsk-0059-w00-v14-7-intake.md) found Q-03 in that conflict: the
current requirement migrates each common role to the common H2 and H3 section
contract, and Q-03 kept the current Registry H2 headings. Q-03 above stays as
the record of 2026-11-11. It no longer limits W03: the Registry headings move
to the common contract, together with the Registry `common` keys that name
them and the current documents. The intake's handoff table lists the exact
differences. Historical and completed evidence still keeps its form.

#### Prior observations to re-check

The W02 readiness analysis recorded these before this Task existed. Each is
re-checked against the current tree before reuse:

- DOC-07: only the Markdown-link half applies; this workspace has no Vault.
- DOC-08: DEFER until a reproduced execution-document gap exists.

#### W03 obligation assessment 2026-11-11

Two fresh-context `qa-engineer` agents read the Registry, schema, templates,
parsers, validators and tests at `95a65be6d` without editing, and probed
negative cases in memory. The controller re-ran each deciding probe.

| ID | Verdict | Current owner and basis |
| --- | --- | --- |
| DOC-01 | GAP, CHANGE in part; DEFER rest | Seven README profiles split by role. The shared required core was not ordered: 13 package READMEs had `Related Documents` before later sections. A fixed service-README section set over the 83 `infra` READMEs (27 heading shapes) is a new contract, not a reproduced defect of the current one |
| DOC-02 | KEEP | `documentation-protocol.md` splits README, folder `AGENTS.md` and the generated `CLAUDE.md` import shim; renderer drift 0 |
| DOC-03 | KEEP | All generated Claude skills set `disable-model-invocation: true`; the output style owns presentation only. Native runtime acceptance UNVERIFIED |
| DOC-04 | GAP, CHANGE | Duplicate keys, invalid dates, forbidden, undeclared and missing keys are rejected. An unquoted `updated: 2026-02-28` passed, because `_json_schema_value` turned the YAML date into a string before the schema saw it |
| DOC-05 | GAP, CHANGE | `ordered_sections` and `nonempty_sections` were set on 13 profiles; 23 profiles with required sections accepted swapped or empty sections. Generic table contracts beyond the README Documents and Evidence tables have no consumer and are not added |
| DOC-06 | KEEP | Language rule in the documentation protocol, enforced by `language.py` through `--mode language` |
| DOC-07 | KEEP Markdown half; Vault N/A | Missing targets, missing anchors and case mismatches are rejected. No Vault or wiki-link surface exists here |
| DOC-08 | DEFER | 78 runbooks carry the ordered, non-empty Runbook sections; no execution document delegates its procedure to a historical link |
| DOC-09 | KEEP; test added | Only child-to-parent `parent_ids` is stored; `parent-cycle` and `parent-cardinality` work but had no committed test |
| DOC-10 | KEEP | Generated surfaces carry a marker and pass the renderer drift check |
| DOC-11 | KEEP | Every template is registered and its placeholders checked; the 29 templates pass a fill-and-check probe in Registry order |
| DOC-12 | KEEP; renumbering held | `reserved_history` and `high_water` block reuse. Path number equals the `artifact_id` number, so any renumbering is a Q-07 decision and is not made here |
| SUP-11 | KEEP | Terminal Task bodies are exempt from rewriting; corrections are added as new sections |

#### W03 changes 2026-11-11

- DOC-04: `registry.py` no longer converts YAML dates before the schema
  check, so an unquoted date fails the string type. No tracked document
  used one.
- DOC-05 and DOC-01: the Registry sets `ordered_sections` and
  `nonempty_sections` on the 22 remaining sectioned profiles, and
  `ordered_sections` only on `research-member`, whose Stage 90 members keep
  their empty parent headings. The `generated` profile stays with its
  producer. Current documents migrated: 13 package READMEs move
  `Related Documents` to the end, and `docs/README.md` and
  `scripts/README.md` lose one empty heading each. No heading is renamed.
- Review answer `aa1bde154`: nine moved READMEs lost a stray trailing
  `---`; the Ollama README also moves `Related Documents` last; the
  declaration test now covers free-form profiles, so `research-member`
  ordering is tested; the swap test handles a last second section.
- Tests: an unquoted-date rejection, a Registry rule that every sectioned
  profile declares order and content, a swapped and an emptied section per
  representative profile, and a parent cycle and a two-parent Plan.

#### v14.7 W03 run 2026-11-12

Input: the v14.7 W03 prompt the owner pasted on 2026-11-12, read as data.
Start point: `main` `0b1b2c6a1`, clean tree; work on branch
`docs/w03-requirement-common-form`. The W00 handoffs H-04, H-06 and H-13 and
the W02 handoff H-W02-2 are this run's inputs; H-07 (W04) moves with H-04.

Inventory at `0b1b2c6a1`, by Registry profile: three roles already use
`COMMON-DOC-FORM-1` 1.0.0 (incident, postmortem, folder AGENTS guide). The
other 13 common roles cover about 700 documents: Requirement 18, Spec 22,
Plan 22, Task 104 (54 terminal), ADR 30, Architecture 27, Guide 78, Runbook
78, Policy 77 plus 32 governance policies and rules, Skill 24 and 233
READMEs. Heading names are read by code in `requirements.py`,
`registry.py`, `identity_history.py`, `spec_packages.py` and
`operations_catalog.py`, and by the Registry `common` keys.

Owner decisions on 2026-11-12, in this chat:

| Question | Decision |
| --- | --- |
| The 54 terminal Tasks | Move them to the common form too; the terminal-body protection is lifted once, for the heading change only, and every recorded fact keeps its text |
| Requirement interface and non-functional sections | Follow the requirement: non-functional items go under `Quality Requirements`; interface needs are written as functional requirements; no `IF` section or identity |
| `Related Documents` | Follow the requirement: links move into each role's own sections; no extra heading |
| Delivery | One role per change and pull request, small SDLC roles first, then operations, then READMEs |

Role order: Requirement, Spec, Plan, ADR, Architecture, Task, Guide,
Runbook, Policy, Skill, READMEs. Each role changes its Registry profile,
template, parsers, tests and current documents together.

##### Requirement role 2026-11-12

- Registry `requirements-package`: H2 Overview, Scope, Requirements,
  Acceptance Criteria, Traceability with their required H3s, and the
  optional `Quality Requirements` H3; the old optional sections are gone, so
  the old form is rejected. `internal_id_spaces` drops `IF`: no current
  package declares an `IF` item. The Registry `REQ-####.IF` identity spaces
  stay, because identity history is append-only (their numbers are reserved,
  none is current), and the parser still checks that each has nothing
  current issued.
- Template rewritten to the same headings.
- `requirements.py` reads FR from `Functional Requirements` and NFR from
  `Quality Requirements`, and rejects an old `Non-functional Requirements` or
  `Interface Requirements` section instead of skipping it. `registry.py`
  accepts `Quality Requirements` only as an H3 under `Requirements` and keeps
  the historical names for baseline revisions.
- The hook rule `enforce-docs-templates` and the hook message in
  `agent-event-hook.sh` no longer demand `## Related Documents`; they point to
  the link section each template declares.
- The 18 packages are restructured by three `doc-writer` agents. Every REQ
  identity, item line and link target from `0b1b2c6a1` is kept; the only
  dropped text is the old headings, the "none issued" sentences of the empty
  NFR and interface sections, and the `**In scope**:` labels that repeated
  the new `In Scope` heading. `Verification Method` is new text in each package;
  `In Scope` is new for 0024, 0026 and 0027, whose old Scope held only
  constraints.
- The documentation protocol, the Stage 01 guide and README now say an
  interface need is a functional requirement and no `IF` identity is issued.
- Tests: the fixtures use the new form; a new test rejects the old
  `Related Documents` H2 and the old NFR and interface H3s; an old NFR or
  interface section and an issued `IF` identity fail the parser.
- First review answers (in `3e359935b`): old sections fail closed, ADR and
  retired Spec links moved to `Downstream Links`, each `Verification Method`
  names the method, the evidence, its Task and who judges, and `Stakeholders`
  names who writes, reviews and accepts.
- Re-review answers (`46890d318`): a test for an issued `IF` identity and
  one pinning an ignored H2 `Quality Requirements`; retired Requirement
  lineage moved to `Downstream Links`; the 0011 promotion evidence belongs to
  the Spec that promotes; the 0008, 0010 and 0011 methods name the runtime
  observations their conditions need.
- Re-review 2 answers (`baece5f5d`): the unused `interface` fixture parameter
  removed; the 0008 task-runner rendering and the 0010 change-path conditions
  given a method.
- Final review answers (the next commit): one test parses a package with a
  `Quality Requirements` section end to end; the remaining 0001, 0009 and
  0010 conditions are given a method.

##### Spec role 2026-11-12

- Registry `spec`: H2 Overview, Scope, Behavior Contract, Acceptance
  Criteria, References with their required H3s; the unused optional
  `Interfaces`, `Failure Modes` and `Quality Requirements` sections are gone,
  so the old form is rejected. `spec_section` stays `Acceptance Criteria`, so
  no Registry `common` key and no Spec Package reader changes.
- Template rewritten. `Evidence Requirements` is a bullet list: every
  numbered line under `Acceptance Criteria` is read as a criterion.
- The 22 Spec documents are restructured by three `doc-writer` agents:
  Background and observed state move to `Intent`, Contracts and Constraints
  to `Normal Behavior`, Error and Boundary Behavior and the old Failure
  Conditions to `Failure and Edge Cases`, Related Documents to `References`.
  Criterion numbers and every sentence, table row and link are kept; a few
  lines gained or lost a bold label. `Owning Requirements` and
  `Evidence Requirements` are new text from each package's frontmatter,
  Plan and Task rows.
- Review answers (`8f9265822` and `9a0677a43`): retired SPEC-0201 to 0203,
  SPEC-0236 and SPEC-0243 moved to historical references and SPEC-0249 kept
  normative; interface and failure content placed under the right behavior
  heading; evidence requirements name each package's recorded checks;
  criterion decisions are said to be recorded in the Task's Criterion
  Acceptance table; labels and en dashes restored.
- `8f9265822`, cited by the Spec re-review and GREEN rows, is the commit
  before the branch was rebased onto the Requirement branch; the pushed
  equivalent is `25f280a66`. `git diff 8f9265822 25f280a66` is empty for
  every `spec.md`, `docs/99.templates`, `scripts` and `tests`; it differs
  only in Requirement-branch and W02 records.
- Tests: the template-outline and nested-section fixtures use the Spec form,
  and the old-form test rejects `Contracts`, `Failure Conditions`, `Related
  Documents` and `Out of Scope`.

##### ADR role 2026-11-13

Branch `docs/w03-adr-common-form`, on top of the Spec branch.

- Registry `adr`: H2 Context, Decision, Alternatives, Consequences,
  Traceability with their required H3s; `Supersession` is the one optional
  H3, under Traceability, kept only where a decision supersedes, amends or is
  superseded by another. The old `Decision Drivers`, `Options` and `Related
  Documents` H2s and the `Compliance` H3 are rejected. No code reads ADR
  headings, so no parser changes.
- Template rewritten; its prompts say to write "not recorded" for an
  approval fact the record does not hold.
- The 30 ADRs are moved by three `doc-writer` agents. Every sentence, list
  item, table row and link is kept. New text is limited to `Decision Scope`,
  `Authority and Effect` and, where options carried no separable reasons,
  `Trade-offs`, written only from facts in each ADR. Compliance becomes an H4
  under Follow-up; ADR-0062's 2026-11-10 amendments are H4s under Follow-up,
  as `docs/02.architecture/AGENTS.md` requires for in-place amendments;
  ADR-0002 keeps its `AI Agent Guidance` H4.
- One agent dropped the frontmatter of six ADRs (0054, 0055, 0056, 0057,
  0059, 0061); the controller restored each block from the previous commit
  with only `version` and `updated` changed.
- Review answers: a lost word in ADR-0051, Supersession sections without a
  real predecessor in 0034 and 0042, an unrecorded effective date and a
  composed reason in 0046, and supersession or approval text under the wrong
  heading in 0032, 0037, 0059 and 0062.
- `docs/02.architecture/AGENTS.md` 0.3.1 and the decisions README 1.7.4 point
  the replacement summary to Traceability `Supersession`.

##### Plan role 2026-11-13

Branch `docs/w03-plan-common-form`, on top of the ADR branch.

- Registry `plan`: H2 Overview, Dependencies, Implementation Strategy,
  Verification Plan, Risks, Promotion Map with their required H3s. The old
  `Scope`, `Work Breakdown`, `Risks and Recovery` and `Related Documents` H2s
  are rejected.
- H-07 design: the Registry `common` heading values, the schema constants
  and `lifecycle_generation` 7 stay. Historical Registries are validated by
  the same pin code, so changing the values would invalidate every older
  generation 7 Registry. `spec_packages.py` instead maps each legacy H2 to its
  common-form path (`Work Breakdown` to `Implementation Strategy` / `Work
  Breakdown`) and accepts exactly one of the two; the Stage 99 README 2.5.2
  says so.
- The 22 Plans are moved by three `doc-writer` agents. Each `Work Breakdown`
  subsection was compared mechanically with its old H2: same lines, with
  inner headings one level deeper. New text is limited to Assumptions,
  Prerequisites, Dependency Order, Stage Placement, Escalation, Durable
  Meaning and Owner and Receipt, taken from each package. One agent dropped
  the closing frontmatter line of the SPEC-0204 Plan; the controller restored
  it.
- Review answers: Escalation no longer credits a Spec with a stop rule it
  lacks (it quotes the Spec's own stop sentence or cites the folder guide);
  SPEC-0244 no longer calls an ambiguous provider view a stop condition;
  rollback sentences name what they restore; Task links moved from
  Prerequisites to Owner and Receipt; SPEC-0263 links its reservations Task.

##### Architecture role 2026-11-13

Branch `docs/w03-architecture-common-form`, on top of the Plan branch.

- Registry `architecture-description`: H2 Overview, Context and Constraints,
  Current Structure, Interfaces, Decisions, Traceability with their required
  H3s. The old `Scope`, `Structure`, `Quality and Risks` and `Related
  Documents` H2s and the `Runtime View` H3 are rejected. No code reads these
  headings.
- The 27 descriptions are moved by three `doc-writer` agents. Runtime View,
  Deployment View, Quality Attributes, Risks and Evolution keep their text as
  H4s. Context, Constraints, Contracts and Failure Boundaries had no old
  counterpart; their text is written only from facts in the same document.
- Review answers: duplicated sentences removed; rewritten link items
  restored verbatim; retired ADR and Spec lines moved to Currentness and
  Lineage; ADR links kept as plain links; one sentence corrected so the MCP,
  not the static origin, lacks cookie `sso-auth`; operations links gathered
  under Currentness and Lineage. A second round restored three more
  rewritten link items and removed two added sentences.

##### Task role 2026-11-13

Branch `docs/w03-task-common-form`, on top of `main` after #971.

- Registry `task`: H2 Scope, Execution Log, Verification Evidence,
  Acceptance Decision, Handoff with their required H3s. The legacy H2s are
  rejected. As for the Plan, the Registry `common` heading values stay;
  `spec_packages.py` maps `Evidence`, `Criterion Acceptance` and `Work Log` to
  `Results`, `Criterion Decisions` and `Work Performed`, and the readers of
  Execution Items, Lifecycle Events, Lifecycle Event Reconciliation and
  Contract Migration read them as H4 under `Work Performed`.
- Terminal Tasks (owner decision of 2026-11-12, one-time heading move):
  `_same_task_body` accepts a legacy-to-common move only when every content
  line keeps its text, order and mapped target, inner headings move exactly
  one level (or two, consistently, under an H4 anchor heading), blank
  lines between content stay, every anchor the old body referenced still
  resolves, and the only added text is the fixed "None: nothing was recorded
  here before this Task moved to the common form." in an empty target. Every
  other change stays byte-strict. The historical admissions and the terminal
  migration check use it.
- All 104 Tasks are moved, including the 56 completed ones and tsk-0007 and
  tsk-0049, whose status comes from Execution Items. They are moved by a
  deterministic script, not by agents.
  Each moved body passes `_same_task_body` against its old body; frontmatter
  of completed and status-less Tasks is unchanged, the others bump the patch
  version. A heading another document or the Task itself links to stays as an
  H4 anchor. Two in-progress Tasks (0204 tsk-0015, 0212 tsk-0049) gained a
  one-line lead under an anchor that would otherwise be empty.
- A first run lost 86 Lifecycle Events anchors written as bare `#slug`
  cells and changed tsk-0007's frontmatter; the lifecycle validator and the
  review caught both, and the script was fixed and re-run from the old files.

##### Guide role 2026-11-13

Branch `docs/w03-guide-common-form`, on top of `main` after #975.

- Registry `guide`: H2 Purpose, Prerequisites, Procedure, Verification with
  their required H3s; the old `Overview`, `Usage`, `Related Documents` H2s and
  the `Common Checks` H3 are rejected. The operations catalog matches required
  section names to headings and needs no code change; `Runbook Handoff` is no
  longer an optional section and lives as an H4 under Troubleshooting.
- The 78 Guides (Korean bodies) are moved by four `doc-writer` agents. Every
  old line and code block is kept apart from 20 intended sentence edits;
  headings other documents link to stay as H4.
- Review answers: limits moved from Actions to Exceptions, procedures and
  checks to Actions and Expected Result; the generic Permissions and
  Exceptions sentences replaced in every Guide by the access, approval,
  secret-name and limit facts each file states; stale "Common Checks" and
  "Runbook Handoff" references renamed.

##### Runbook role 2026-11-13

Branch `docs/w03-runbook-common-form`, on top of the Guide branch that
merged as #977.

- Registry `runbook`: H2 Purpose, Preconditions, Steps, Validation, Recovery
  with their required H3s (Trigger and Outcome, Scope; Authority and Access,
  Safety Checks; Actions, Stop Conditions; Service Checks, Evidence;
  Escalation) and the optional H3 Rollback. The operations catalog matches
  required section names to headings and needs no code change.
- The 78 Runbooks (Korean bodies) are moved by `doc-writer` agents. Every old
  line and code block is kept apart from intended sentence edits; the 40
  links to the old `#procedure` and `#verification` anchors now point to
  `#actions` and `#service-checks`, and Guide and Policy link texts that
  named the old headings are renamed.
- Review answers: 0105 cleanup and abort rules moved under Rollback with their
  "위/아래" references renamed; pointer-only sentences replaced by the stop
  conditions, preflight checks and evidence lists each file states;
  record-keeping text moved from Service Checks to Evidence; forward actions
  moved out of Rollback and Escalation; false "별도의 점검 목록을 두지 않고"
  sentences removed; the 0098 reboot expectation corrected to the sealed
  `bao status` exit.

##### Policy role 2026-11-13

Branch `docs/w03-policy-common-form`, on top of the Runbook branch.

- Registry `policy`, `governance-policy` and `governance-hook-policy`: H2
  Purpose, Scope, Rules, Exceptions, Ownership with their required H3s
  (Objective, Authority; Applies To, Exclusions; Requirements, Enforcement;
  Exception Conditions, Approval and Review; Responsibilities, Change and
  Adoption). `governance-policy` no longer allows free-form sections, so an
  unregistered H2 is rejected. The operations catalog matches required
  section names to headings and needs no code change.
- The 77 operations Policies (Korean bodies) and the 32 governance policies
  and hook rules (English) are moved by `doc-writer` agents. Every rule
  sentence is kept and only moved; H4 titles other documents link to stay.
- Review answers: templated Exclusions sentences replaced by the exclusions
  each file states, or by "없음: 이 정책 본문에는 명시된 제외 대상이 없다.";
  forbidden items and rule clauses moved out of Exclusions; owner and
  approval paragraphs moved into Responsibilities; governance Authority
  lists replaced by the canonical-owner sentence under bootstrap precedence,
  with the displaced links returned to Change and Adoption; false Approval
  and Review and Exclusions sentences corrected; duplicate Guide and Runbook
  peer links removed.

##### Skill role 2026-11-13

Branch `docs/w03-skill-common-form`, on top of the Policy branch.

- Registry `governance-skill`: H2 Purpose and Trigger, Procedure, Inputs and
  Outputs, Verification with their required H3s (When to Use, When Not to
  Use; Steps, Failure Handling; Inputs, Outputs; Checks, Completion and
  Handoff). The old `Purpose`, `Inputs`, `Outputs`, `Failure Handling`,
  `References` H2s and the `Preconditions` H3 are rejected. The heading test
  now samples `.agents/` documents too, so the skill and governance profiles
  are exercised.
- The 24 skills are moved by two `skill-creator` agents. Every old line is
  kept; Preconditions text sits directly under When to Use, Gates become an
  H4 under Steps, and the old References links sit under Completion and
  Handoff after "Owning role, policies and related documents:". When Not to
  Use quotes the description's "Do NOT use" clause, states the exclusion the
  body gives, or says "None: this skill states no exclusion." where none is
  stated. Renderer drift 0.
- Review answers: one stale "below" reference, a false lead-in, an
  exclusion left under When to Use, four false "None" lines and two
  misplaced paragraphs fixed; adr-writing gains its owning role link.

Held for a later change: Completion and Handoff in all 24 skills holds only
links, and two Gates bullets (ops-runbook-agent, incident-response) state an
output location rather than a gate.

##### Handoffs H-W02-2 and H-13 2026-11-13

Branch `docs/w03-archive-vocabulary`.

- H-W02-2: a consumer survey found that nothing writes or reads
  `common.archive_source_prefixes` (the live root set is the separate
  `LEGACY_ARCHIVE_SOURCE_ROOTS` constant in `registry.py`) or the frontmatter
  keys `archived_from`, `archived_at`, `archive_reason`,
  `archive_disposition`, `archived_commit` and `archived_blob`; they were only
  declared and validated, and no tracked document carries them. They are
  retired from the Registry, both schemas, `metadata/profile.py`,
  `metadata/lifecycle.py` and the template timestamp keys.
  `archive_authorizations` stays, because the terminal TSK-0012 carries it,
  and `archive_retention.disposition_entry_statuses` stays, because
  `registry.py`, `spec_packages.py` and `lifecycle/occupancy.py` read it.
- H-13: the architecture description template asks the author to review a
  diagram against the C4 diagram review checklist; no rule requires it.

##### Root README role 2026-11-13

Branch `docs/w03-root-readme-common-form`.

- Registry `repository-readme` and `runtime-governance-readme`: H2 Purpose,
  Repository Map, Getting Started, References with their required H3s
  (Project Role, Boundaries; Directories, Canonical Entry Points;
  Prerequisites, First Verified Path; Current Documentation, Support and
  Ownership). The renderer writes the new form for `.claude/README.md` and
  `.codex/README.md`.
- The README Documents table check now reads `README_DOCUMENTS_HEADINGS`
  (Directories, Current Items, Documents); under Directories it checks every
  table that has a `Path` column.
- The 13 authored READMEs (Korean) are moved; `secrets/README.md` was read and
  edited with the owner's leave for that one file only. Added sentences state
  real prerequisites (Python, the hashed lock, Docker for the opt-in test),
  canonical entry points and the support routes (`bug_report.yml`,
  `feature_request.yml`, `SECURITY.md`, the owner).

##### Retirement and incident numbering 2026-11-13

Branch `docs/w03-retirement-consistency`. Two conflicts the Stage README
review surfaced, fixed toward the stated requirement:

- A replaced ADR or Architecture Description is summarized into its
  successor and deleted in the same change (the Stage 99 README and the ADR
  on summarize-and-delete retirement). Retirement precondition 1 in the
  documentation protocol required a Registry disposition status that neither
  lifecycle can reach, so no ADR or Description could ever retire. The
  precondition now also admits a document whose replacing ADR or Description,
  carrying its summary, lands in the same change, and the retention sentence
  says the same. The Registry map is unchanged: listing `accepted` or `active`
  would make the occupancy check demand removal of every live document.
- The Stage 99 README said incident numbers restart each year. The Registry
  has one `incident` identity space and `identity_history.py` collects one
  set, so the README now says the number comes from one global counter and
  the year appears only in the path and artifact ID. The code comment says
  the same.

Held, not changed: the `incident` and `postmortem` disposition entries list
statuses their lifecycles cannot reach, so those records never retire. No
rule says whether they should; a Registry check that each listed status
belongs to the profile's lifecycle is handed to W05 with the validator work.

##### Stage README role 2026-11-13

Branch `docs/w03-stage-readme-common-form`.

- Registry `readme`, `documentation-readme`, `reference-category-readme`,
  `incident-year-readme` and the three `.agents` index profiles: H2 Stage
  Responsibility, Contents, Workflow, Related Documents with their required
  H3s (Purpose and Readers, Inputs and Outputs; Current Items,
  Classification; Create and Review, Transition and Exit; Upstream and
  Downstream, Policy and Templates).
- The README table check, merged with the root form's: every table under
  Directories, Current Items or Documents is checked; under Directories and
  Current Items only a table with a `Path` column must use the registered
  columns, and under Documents every table must.
- The 68 READMEs (Korean) are moved. Transition and Exit states each stage's
  own lifecycle from the Registry and the retirement preconditions;
  Classification states the identifier form and, for operations folders,
  that other roles share the number and slug where they exist. Three folder
  READMEs that linked into a child's files now name them as text.

Held for an owner decision, not changed here, because each would change
what a requirement says:

- Acceptance conditions in REQ-0024 to REQ-0027 are not split per
  requirement identity.
- The REQ-0003 quality requirements have no acceptance condition of their
  own.
- `REQUIREMENT_TARGET_BODY` in the heading test support keeps the old
  headings; it serves tests whose subject is not the body form.

### Blockers and Decisions

None: nothing was recorded here before this Task moved to the common form.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W03 obligation assessment | 111 | W116 | template-contract-assessment | DOC-01 to DOC-12 and SUP-11 | NOT_RUN | Assessment not yet run | required | - |
| W03 obligation assessment result | 111 | W116 | template-contract-assessment | DOC-01 to DOC-12 and SUP-11 at `95a65be6d` | PASS | Per-ID table above: DOC-04 and DOC-05 GAP changed, DOC-01 changed in part, DOC-08 DEFER, DOC-07 Vault N/A, rest KEEP | required | W03 obligation assessment |
| W03 section and date RED | 111 | W116 | red-green-proof | New tests against the pre-change Registry and `_json_schema_value` | FAIL | Unquoted-date test failed; order and content tests failed for 28 profile cases with the Registry at `95a65be6d` | required | - |
| W03 section and date GREEN | 111 | W116 | red-green-proof | Commits `ce18338c8` and `85ed595b3` | PASS | test_registry 123 OK; test_heading, test_profile, test_language 110 OK; test_lifecycle 7 OK; metadata check-active selected534 violations0, check-changed selected16 violations0; links alignment and language PASS; renderer drift 0; script manifest PASS | required | W03 section and date RED |
| W03 code review | 111 | W116 | independent-source-review | Fresh-context code-reviewer of `ce18338c8` and `85ed595b3` | PASS | APPROVED: no false finding or exception from date objects; README content preserved; tests not vacuous. Four minor findings answered in `aa1bde154`; removing `research-member` ordering now fails the declaration test | required | - |
| W03 governance suite | 111 | W116 | document-governance-unit-suite | `tests/lib/document_governance` discover at `cab985393`; `aa1bde154` later changed only test_heading and READMEs, rerun alone 85 OK | PASS | Ran 769 tests, OK, exit 0 | optional | - |
| W03 v14.7 Requirement form RED | 111 | W116 | red-green-proof | The new old-form test against the `requirements-package` profile at `main` `0b1b2c6a1` | FAIL | Three cases failed: an old `Related Documents` H2 was reported only as duplicate and out of order, and the old NFR and interface H3s were not reported | required | - |
| W03 v14.7 Requirement review | 111 | W116 | independent-review | Fresh-context code-reviewer of the uncommitted Requirement change | FAIL | CHANGES_REQUIRED: old NFR and interface sections skipped, the `IF` reason in this Task wrong, unsupported verification text, consumers listed as sources, hook text demanding `Related Documents`; seven minor | required | - |
| W03 v14.7 Requirement re-review | 111 | W116 | independent-review | Fresh-context code-reviewer of `3e359935b` | FAIL | CHANGES_REQUIRED: no test for an issued `IF` identity; four minor (H2 `Quality Requirements` untested, promotion evidence owner, runtime observations, retired lineage under sources) | required | - |
| W03 v14.7 Requirement re-review 2 | 111 | W116 | independent-review | Fresh-context code-reviewer of `46890d318` | FAIL | CHANGES_REQUIRED: the five re-review fixes verified; no suite run recorded yet; three minor (the Task credited the wrong commit, a dead test parameter, three conditions with no named method) | required | - |
| W03 v14.7 Requirement final review | 111 | W116 | independent-review | Fresh-context code-reviewer of `baece5f5d` | FAIL | CHANGES_REQUIRED, minor only: an unused fixture parameter, three conditions in 0001, 0009 and 0010 without a method, review rounds merged in this Task | required | - |
| W03 v14.7 Requirement review result | 111 | W116 | independent-review | Fresh-context code-reviewer of `cf4f6c3fe` | PASS | PASS: the four final-review minors are fixed; one missing comma in 0010 fixed in `ad4bd359d` | required | W03 v14.7 Requirement review, W03 v14.7 Requirement re-review, W03 v14.7 Requirement re-review 2, W03 v14.7 Requirement final review |
| W03 v14.7 Requirement GREEN | 111 | W116 | red-green-proof | `tests/lib/document_governance` discover at `46890d318` in a detached worktree; `test_requirements` alone at `cf4f6c3fe` | PASS | Ran 780 tests, OK; `test_requirements` 27 OK, including the old-form, retired-section, issued-`IF` and Quality Requirements tests | required | W03 v14.7 Requirement form RED |
| W03 v14.7 Spec form RED | 111 | W116 | red-green-proof | The old-form test with Spec cases against the `spec` profile at `main` `0b1b2c6a1` | FAIL | All four Spec cases failed: the old `Contracts`, `Failure Conditions` and `Related Documents` H2s and the `Out of Scope` H3 were accepted | required | - |
| W03 v14.7 Spec review | 111 | W116 | independent-review | Fresh-context code-reviewer of the Spec move | FAIL | CHANGES_REQUIRED: deleted Specs listed as current authority, a current Spec labelled historical, interface content under Intent; nine minor | required | - |
| W03 v14.7 Spec re-review | 111 | W116 | independent-review | Fresh-context code-reviewer of `8f9265822` | FAIL | CHANGES_REQUIRED, minor only: an SPEC-0265 check not in its Task, SPEC-0263 constraint and boundary paragraphs inside numbered subsections, SPEC-0264 observed state under Owning Requirements; answered in `9a0677a43` | required | - |
| W03 v14.7 Spec review result | 111 | W116 | independent-review | Fresh-context code-reviewer of `9a0677a43` | PASS | PASS: the three re-review minors fixed; outline and criterion numbers of the three changed Specs unchanged | required | W03 v14.7 Spec review, W03 v14.7 Spec re-review |
| W03 v14.7 Spec GREEN | 111 | W116 | red-green-proof | `tests/lib/document_governance` discover at `8f9265822` in a detached worktree; `9a0677a43` later changed only three Spec documents | PASS | Ran 781 tests, OK, including the Spec old-form, template-outline and nested-section tests | required | W03 v14.7 Spec form RED |
| W03 v14.7 Requirement checks | 111 | W116 | metadata-links-governance | `46890d318`, clean tree | PASS | metadata check-changed selected 25 violations 0, check-active selected 534 violations 0; corpus lifecycle and occupancy 0; links alignment, commands and language PASS; renderer drift 0; governance contract PASS; Script Manifest PASS; staged pre-commit PASS | required | - |
| W03 v14.7 ADR form RED | 111 | W116 | red-green-proof | The old-form and template-outline tests with ADR cases against the `adr` profile at `29440dc61` | FAIL | Five failures: the old `Decision Drivers`, `Options` and `Related Documents` H2s and the `Compliance` H3 were accepted, and the template outline differed | required | - |
| W03 v14.7 ADR review | 111 | W116 | independent-review | Fresh-context code-reviewer of the uncommitted ADR move | FAIL | CHANGES_REQUIRED: a lost word in ADR-0051, Supersession without a predecessor in 0034 and 0042, an unrecorded effective date in 0046, amendment, approval and lineage text misplaced in 0032, 0037, 0059 and 0062 | required | - |
| W03 v14.7 ADR review result | 111 | W116 | independent-review | Fresh-context code-reviewer of `36e0dcf4f` | PASS | PASS: all nine fixes present, H2/H3 form intact, no text lost against the old diff | required | W03 v14.7 ADR review |
| W03 v14.7 ADR GREEN | 111 | W116 | red-green-proof | `tests/lib/document_governance` discover at `36e0dcf4f` | PASS | Ran 781 tests, OK, including the ADR old-form and template-outline tests | required | W03 v14.7 ADR form RED |
| W03 v14.7 ADR checks | 111 | W116 | metadata-links-governance | The tree committed as `36e0dcf4f`, checked before the commit | PASS | metadata check-changed selected 32 violations 0; links alignment PASS, 905 documents; corpus lifecycle and occupancy 0; staged pre-commit PASS | required | - |
| W03 v14.7 Plan form RED | 111 | W116 | red-green-proof | The resolver test and the Plan old-form and template-outline tests against the Plan code and `plan` profile at `009ced2c7` | FAIL | The resolver test errored (no `_contract_span`); six heading tests failed: the old Plan H2s and `Risks and Rollback` H3 were accepted and the template outline differed | required | - |
| W03 v14.7 Plan review | 111 | W116 | independent-review | Fresh-context code-reviewer of the uncommitted Plan move | FAIL | CHANGES_REQUIRED: Escalation credited Specs with stop rules they lack, SPEC-0244 called an ambiguous view a stop condition, two rollback sentences lost their referent; seven minor | required | - |
| W03 v14.7 Plan review result | 111 | W116 | independent-review | Fresh-context code-reviewer of `3ec0b008f` | PASS | PASS: all fixes hold, quoted Spec sentences match; two minor quote and link gaps answered in `7eb600321` | required | W03 v14.7 Plan review |
| W03 v14.7 Plan GREEN | 111 | W116 | red-green-proof | `tests/lib/document_governance` discover at `7eb600321` | PASS | Ran 782 tests, OK, including the resolver, Plan old-form and template-outline tests | required | W03 v14.7 Plan form RED |
| W03 v14.7 Plan checks | 111 | W116 | metadata-links-governance | The 22 Plans before the `3ec0b008f` commit and after the review answers | PASS | Every `Work Breakdown` equals its old H2 with inner headings one level deeper (22 of 22); metadata check-changed selected 22 violations 0; links alignment PASS; corpus lifecycle and occupancy 0 | required | - |
| W03 v14.7 Architecture form RED | 111 | W116 | red-green-proof | The old-form and template-outline tests with Architecture cases against the `architecture-description` profile at `36e0dcf4f` | FAIL | Six failures: the old `Scope`, `Structure`, `Quality and Risks` and `Related Documents` H2s and the `Runtime View` H3 were accepted, and the template outline differed | required | - |
| W03 v14.7 Architecture review | 111 | W116 | independent-review | Fresh-context code-reviewer of the uncommitted Architecture move | FAIL | CHANGES_REQUIRED: duplicated sentences, rewritten link items, retired ADR and Spec lines under current headings, a changed ADR item and an altered `sso-auth` fact; four minor | required | - |
| W03 v14.7 Architecture re-review | 111 | W116 | independent-review | Fresh-context code-reviewer of `f74c40413` | FAIL | CHANGES_REQUIRED: three more rewritten link items (0013, 0018, 0019); two minor added sentences | required | - |
| W03 v14.7 Architecture review result | 111 | W116 | independent-review | Fresh-context code-reviewer of `c9fa9d8aa` | PASS | PASS: every finding fixed, 18 required headings in each of the 27 descriptions | required | W03 v14.7 Architecture review, W03 v14.7 Architecture re-review |
| W03 v14.7 Architecture GREEN | 111 | W116 | red-green-proof | `tests/lib/document_governance` discover at `c9fa9d8aa` | PASS | Ran 782 tests, OK, including the Architecture old-form and template-outline tests | required | W03 v14.7 Architecture form RED |
| W03 v14.7 Architecture checks | 111 | W116 | metadata-links-governance | The 27 descriptions after each review round | PASS | metadata check-changed selected 27 violations 0, then 5 violations 0 after the last answer; links alignment PASS | required | - |
| W03 v14.7 Task form RED | 111 | W116 | red-green-proof | The Task reader, subsection, probe, terminal-body and heading tests against the code and `task` profile at `6350398ac` | FAIL | The resolver failed for Evidence, Criterion Acceptance and Work Log; the H4 subsection readers and the `#### Execution Items` probe failed; nine terminal-body accept cases failed; seven heading tests failed | required | - |
| W03 v14.7 Task code review | 111 | W116 | independent-review | Fresh-context code-reviewer of `897d96334`, `654fcdbf1`, `6e16c0c4d` | FAIL | CHANGES_REQUIRED: the relaxed body rule dropped real headings, ignored heading levels and blank lines; a receipt probe skipped moved Tasks; four minor | required | - |
| W03 v14.7 Task re-review | 111 | W116 | independent-review | Fresh-context code-reviewer of `3d0bbd341`, `319568e1d`, `363ce96cd` and the first moved Tasks | FAIL | CHANGES_REQUIRED: a referenced anchor could vanish while the rule passed; 86 Lifecycle Events anchors lost in 53 moved Tasks | required | - |
| W03 v14.7 Task final review | 111 | W116 | independent-review | Fresh-context code-reviewer of `3532abdcc` and `ae4df1873` | FAIL | Code and anchors PASS; CHANGES_REQUIRED for this Task's text (W05 named as W04, an ambiguous count, an overstated level rule) | required | - |
| W03 v14.7 Task review result | 111 | W116 | independent-review | Fresh-context code-reviewer of `13b444534` | PASS | PASS: the three text findings fixed; earlier code and anchor findings stay fixed | required | W03 v14.7 Task code review, W03 v14.7 Task re-review, W03 v14.7 Task final review |
| W03 v14.7 Task GREEN | 111 | W116 | red-green-proof | `tests/lib/document_governance` discover at `ae4df1873` | PASS | Ran 810 tests, OK, including the terminal-body, admission, resolver and heading tests | required | W03 v14.7 Task form RED |
| W03 v14.7 Task checks | 111 | W116 | metadata-links-governance | The 104 moved Tasks at `ae4df1873` with this Task's later text edits | PASS | Every completed Task body passes `_same_task_body` and the terminal migration check; Spec Package lifecycle against `origin/main` 0 findings; heading contract 0 findings; 0 lost same-file anchors; metadata check-changed selected 106 violations 0; links alignment PASS | required | - |
| W03 v14.7 Guide form RED | 111 | W116 | red-green-proof | The old-form and template-outline tests with Guide cases against the `guide` profile at `13b444534` | FAIL | Five failures: the old `Overview`, `Usage`, `Related Documents` H2s and the `Common Checks` H3 were accepted, and the template outline differed | required | - |
| W03 v14.7 Guide review | 111 | W116 | independent-review | Fresh-context code-reviewer of the uncommitted Guide move | FAIL | CHANGES_REQUIRED: limits and procedures in the wrong sections; generic Permissions and Exceptions sentences false in many Guides; stale heading references | required | - |
| W03 v14.7 Guide re-review | 111 | W116 | independent-review | Fresh-context code-reviewer of `c7ca7356e` | FAIL | CHANGES_REQUIRED, minor: four false Exceptions or Permissions sentences (0010, 0065, 0082, 0059) | required | - |
| W03 v14.7 Guide review result | 111 | W116 | independent-review | Fresh-context code-reviewer of `a8a55aead` | PASS | PASS: every finding fixed; anchors resolve | required | W03 v14.7 Guide review, W03 v14.7 Guide re-review |
| W03 v14.7 Guide GREEN | 111 | W116 | red-green-proof | `tests/lib/document_governance` discover at `a8a55aead` | PASS | Ran 810 tests, OK, including the Guide old-form, template-outline and operations catalog tests | required | W03 v14.7 Guide form RED |
| W03 v14.7 Guide checks | 111 | W116 | metadata-links-governance | The 78 moved Guides at `c7ca7356e` and `a8a55aead` | PASS | Heading contract 0 findings; metadata check-changed selected 78 violations 0; links alignment PASS; operations catalog, taxonomy and moves tests 162 OK; every old line and code block kept apart from 20 intended edits | required | - |
| W03 v14.7 Runbook form RED | 111 | W116 | red-green-proof | The old-form and template-outline tests with Runbook cases against the `runbook` profile at `089d4246d` (rebased as `662623dc9`) | FAIL | Six failures in the old-form and template-outline Runbook cases | required | - |
| W03 v14.7 Runbook review | 111 | W116 | independent-review | Fresh-context code-reviewer of the Runbook move at `61354e00e` | FAIL | CHANGES_REQUIRED: 0105 cleanup rules after their references; pointer-only sentences; preflight checks outside Safety Checks; Service Checks and Evidence swapped; forward actions under Rollback | required | - |
| W03 v14.7 Runbook re-review | 111 | W116 | independent-review | Fresh-context code-reviewer of `bac33e6a4` | FAIL | CHANGES_REQUIRED, minor: leftover false sentences, among them the 0098 reboot expectation and the 0065 "별도의 점검 목록을 두지 않고" sentence | required | - |
| W03 v14.7 Runbook review result | 111 | W116 | independent-review | Fresh-context code-reviewer of `98c4edd78` (rebased as `436bcc974`) | PASS | PASS: every finding fixed; anchors resolve | required | W03 v14.7 Runbook review, W03 v14.7 Runbook re-review |
| W03 v14.7 Runbook GREEN | 111 | W116 | red-green-proof | `tests/lib/document_governance` discover at `436bcc974` | PASS | Ran 810 tests, OK, including the Runbook old-form, template-outline and operations catalog tests | required | W03 v14.7 Runbook form RED |
| W03 v14.7 Runbook checks | 111 | W116 | metadata-links-governance | The 78 moved Runbooks and the Guide and Policy link texts at `436bcc974` | PASS | Heading contract 0 findings; metadata check-changed selected 113 violations 0; links alignment 905 documents 8319 links failures 0; operations catalog tests OK | required | - |
| W03 v14.7 Policy form RED | 111 | W116 | red-green-proof | The `test_heading` and `test_profile` changes of `b939b2994` against the profiles at `f1c6074dc` | FAIL | Ran 234 tests, eight failures: the three Policy template outlines differed, the old `Overview`, `Verification`, `Related Documents` and `Traceability` headings were accepted, and the governance-policy profile test failed | required | - |
| W03 v14.7 Policy review | 111 | W116 | independent-review | Fresh-context code-reviewer of the operations Policy move at `1a69231e3` (rebased as `9cd965911`) | FAIL | CHANGES_REQUIRED: templated Exclusions sentences; forbidden items and rule clauses under Exclusions; owner paragraphs outside Responsibilities; misplaced recovery, review and reconciliation text | required | - |
| W03 v14.7 Policy re-review | 111 | W116 | independent-review | Fresh-context code-reviewer of `bc40f2d72` and `f9e5b0e44` (rebased as `5d6796b25`, `df771d097`) | FAIL | CHANGES_REQUIRED twice, minor; the last round named three duplicate Guide and Runbook peer links (0081, 0086, 0087) | required | - |
| W03 v14.7 Policy review result | 111 | W116 | independent-review | Fresh-context code-reviewer of `d1d776465` (rebased as `c724bab02`) | PASS | PASS: every finding of the review and both re-reviews fixed | required | W03 v14.7 Policy review, W03 v14.7 Policy re-review |
| W03 v14.7 governance policy review | 111 | W116 | independent-review | Fresh-context code-reviewer of the governance move at `4ed686af5` (rebased as `7b48b923a`) | FAIL | CHANGES_REQUIRED: false Authority lists; false Approval and Review in approval-boundaries; false Exclusions in documentation-protocol; hook rule Applies To text | required | - |
| W03 v14.7 governance policy review result | 111 | W116 | independent-review | Fresh-context code-reviewer of `b7d418b31` (rebased as `1e0af3951`) | PASS | PASS: every finding fixed | required | W03 v14.7 governance policy review |
| W03 v14.7 Policy GREEN | 111 | W116 | red-green-proof | `tests/lib/document_governance` discover at `1e0af3951` | PASS | Ran 810 tests, OK, including the Policy old-form, template-outline, governance-policy profile and operations catalog tests | required | W03 v14.7 Policy form RED |
| W03 v14.7 Policy checks | 111 | W116 | metadata-links-governance | The 77 operations Policies and 32 governance policies and hook rules at `1e0af3951` | PASS | Heading contract on 109 documents 0 findings; metadata check-changed selected 114 violations 0; links alignment PASS | required | - |
| W03 v14.7 Skill form RED | 111 | W116 | red-green-proof | The `test_heading` changes of `e132c6607` and `fd4d37dea` against the `governance-skill` profile at `b7d418b31` | FAIL | The template outline failed (234 tests, one failure), and the old-form cases failed five times: `## Purpose`, `## Inputs`, `## Failure Handling`, `## References` and `### Preconditions` were accepted | required | - |
| W03 v14.7 Skill review | 111 | W116 | independent-review | Fresh-context code-reviewer of `4c335014f` (rebased as `f7f37d495`) | FAIL | CHANGES_REQUIRED, minor: a stale "below", a false lead-in, an exclusion under When to Use, a false "None", misplaced paragraphs | required | - |
| W03 v14.7 Skill re-review | 111 | W116 | independent-review | Fresh-context code-reviewer of `ae06dfc1f` (rebased as `8a8829190`) | FAIL | CHANGES_REQUIRED: the adr-writing lead-in had no role link; two more "None" lines were false | required | - |
| W03 v14.7 Skill review result | 111 | W116 | independent-review | Fresh-context code-reviewer of `8412eafea` (rebased as `5f18c6913`) | PASS | PASS: every finding fixed | required | W03 v14.7 Skill review, W03 v14.7 Skill re-review |
| W03 v14.7 Skill GREEN | 111 | W116 | red-green-proof | `tests/lib/document_governance` discover at `fd4d37dea` | PASS | Ran 810 tests, OK, including the skill old-form and template-outline tests | required | W03 v14.7 Skill form RED |
| W03 v14.7 Skill checks | 111 | W116 | metadata-links-governance | The 24 moved skills at `fd4d37dea` | PASS | Heading contract 0 findings (384 on the old copies); renderer drift 0; agent governance contract failures 0; links alignment PASS | required | - |
| W03 v14.7 archive vocabulary RED | 111 | W116 | red-green-proof | `test_retired_archive_vocabulary_is_rejected` against the Registry and schemas at `643629139` | FAIL | FAILED (failures=6): the retired keys were accepted and `archive_source_prefixes` was present | required | - |
| W03 v14.7 archive vocabulary review | 111 | W116 | independent-review | Fresh-context code-reviewer of `84002bc55` and `c44de6697` | PASS | PASS: no consumer remains for any retired key; the supply-chain `archived_at` is a separate JSON ledger; the C4 prompt is optional and harmless; one minor test weakness (`archived_at` with an invalid value) fixed in the next commit | required | - |
| W03 v14.7 archive vocabulary GREEN | 111 | W116 | red-green-proof | `tests/lib/document_governance` discover at `c44de6697` | PASS | Ran 811 tests, OK | required | W03 v14.7 archive vocabulary RED |
| W03 v14.7 archive vocabulary checks | 111 | W116 | metadata-links-governance | Registry, schemas and the active corpus at `84002bc55` | PASS | metadata check-active selected 534 violations 0; active stage occupancy violations 0 | required | - |
| W03 v14.7 Root README form RED | 111 | W116 | red-green-proof | The new test_heading and test_registry cases against the root README profiles at `588f2c3bd` | FAIL | Two failures and 11 errors: the template outlines differed, the old-form cases errored for both profiles, and the Directories table test errored | required | - |
| W03 v14.7 Root README review | 111 | W116 | independent-review | Fresh-context code-reviewer of `d712aee54` | FAIL | CHANGES_REQUIRED: a Path-column table could pass with swapped or lowercase headers; stale prose references; false "없음" prerequisites; content outside its section; incomplete support routes | required | - |
| W03 v14.7 Root README review result | 111 | W116 | independent-review | Fresh-context code-reviewer of `9a3836f72`, minors fixed in `a1683374f` | PASS | PASS: every finding fixed | required | W03 v14.7 Root README review |
| W03 v14.7 Root README GREEN | 111 | W116 | red-green-proof | `tests/lib/document_governance` discover at `a1683374f`; after merging main, test_heading and test_registry at `1ac114404` | PASS | Ran 813 tests, OK; after the merge 220 tests, OK | required | W03 v14.7 Root README form RED |
| W03 v14.7 Root README checks | 111 | W116 | metadata-links-governance | The 13 READMEs and two generated READMEs at `a1683374f` and `1ac114404` | PASS | Renderer drift 0; agent governance contract PASS; metadata check-changed violations 0; links alignment and navigation PASS | required | - |
| W03 v14.7 retirement consistency review | 111 | W116 | independent-review | Fresh-context rules-engineer assessment of the two conflicts at `3607497a6` | PASS | The protocol is the owner; precondition 1 and the retention sentence change together; no `.agents` link to a numbered-stage document; the incident wording is confirmed and no other document repeats the restart claim | required | - |
| W03 v14.7 retirement consistency checks | 111 | W116 | metadata-links-governance | The protocol, Stage 99 README and `identity_history.py` comment | PASS | test_identity_history OK; agent governance contract PASS; links alignment PASS; metadata check-changed at `92064f2f3` selected 3 violations 0 | required | - |
| W03 v14.7 retirement consistency approval | 111 | W116 | independent-review | Fresh-context rules-engineer review of the applied commit `92064f2f3` | PASS | APPROVED: the protocol wording, the README line and the code comment match the assessed wording; no `.agents` link to a numbered-stage document; the held incident and postmortem entries are recorded without claiming a retention rule | required | - |
| W03 v14.7 Stage README form RED | 111 | W116 | red-green-proof | The new test_heading cases against the stage README profiles at `588f2c3bd` | FAIL | Ran 90 tests, 13 failures: seven template outlines, five `readme` old-form cases and the Current Items table test | required | - |
| W03 v14.7 Stage README review | 111 | W116 | independent-review | Fresh-context code-reviewer of `b86a7a942` | FAIL | CHANGES_REQUIRED: three folder READMEs linked into a child's files; stale "Structure" prose; content outside its section; generic Transition and Exit text; an overclaiming link label | required | - |
| W03 v14.7 Stage README re-review | 111 | W116 | independent-review | Fresh-context code-reviewer of `8c062ce6d` | FAIL | CHANGES_REQUIRED: the operations README let Incident and Postmortem records retire, which no Registry status allows | required | - |
| W03 v14.7 Stage README review result | 111 | W116 | independent-review | Fresh-context code-reviewer of `8b000ae84` | PASS | PASS: removal limited to superseded or retired operations documents under the retirement preconditions; Incident transitions match the Registry | required | W03 v14.7 Stage README review, W03 v14.7 Stage README re-review |
| W03 v14.7 Stage README GREEN | 111 | W116 | red-green-proof | `tests/lib/document_governance` discover at `8b000ae84`; after merging main, test_heading and test_registry at `72e63401e` | PASS | Ran 812 tests, OK; after the merge 222 tests, OK | required | W03 v14.7 Stage README form RED |
| W03 v14.7 Stage README checks | 111 | W116 | metadata-links-governance | The 68 READMEs at `8b000ae84` and `72e63401e` | PASS | Links alignment and navigation PASS; metadata check-changed violations 0; renderer drift 0; agent governance contract PASS | required | - |

### Resolution Links

Each FAIL row in Results is resolved by the later PASS row of the same Check and Work Unit that names it in its Resolves column.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 111 | pending | - | - | SPEC-0212 TSK-0058 |

### Remaining Conditions

In progress. The assessment and the reproduced-gap changes are recorded.
Criterion 111 waits for the owner. Open: a fixed service-README section set
(DOC-01) needs an owner decision on a new contract; validator work beyond
these profile flags is handed to W05; renumbering stays a Q-07 decision.

## Handoff

### Promotion Receipt

Each role's Registry profile, template and documents land in `main` through its pull request: #967 (Requirement), #968 (Spec), #969 (ADR), #970 (Plan), #971 (Architecture), #975 (Task), #977 (Guide), #979 (Runbook), #980 (Policy), #981 (Skill), #982 (H-W02-2 and H-13), #983 (Root README), #984 (retirement and incident numbering).

### Next Owner

The current owner is @buenhyden. After each role pull request merges, the next W03 role starts here in the planned order; W05 owns the validator work handed over under Remaining Conditions.
