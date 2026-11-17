---
title: "T99 Role Design Adoption Task"
version: "0.12.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0081"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-17"
---

# T99 Role Design Adoption Task

## Scope

### Objective and Parent

Own criterion 137 and work units W142 to W147 under the [Spec](../spec.md)
and [Plan](../plan.md). Adopt the shared document role design core
`workspace-document-role-design` 4.0.0 in this workspace, one role group at
a time, and keep every unmoved form honest about the contract it follows.
The [W03-FORMS Task](tsk-0073-w03-forms-3-0-1.md) holds the form work this
reuses.

### Inputs and Authority

The direct 2026-11-17 request runs T99-CONFORMANCE from the git-ignored
package `_workspace/workspace_governance_4_2_0_20261116/`. It reads D01, D02,
D03, D24, D25, D26, D27 and D28 and the package's
`template-design-targets.json` 4.0.0. The package marks that core
`DESIGN_PROPOSAL_NOT_WORKSPACE_ADOPTION`. On 2026-11-17 the owner answered
the adoption question with full adoption in this chat, and authorized push,
pull request and merge. Terminal Task bodies stay as recorded, so the Task
role reaches new packages through a new lifecycle generation. No other
repository is opened or required.

## Execution Log

### Work Performed

#### Inventory and comparison

The Registry has 39 template roles over 47 tracked Stage 99 files. A one-time
export at `fdb92cd82` read the Registry and every template source with its
SHA-256, mapped 19 local roles to the 19 core roles and listed 20 unmapped
forms. The package's `compare_template_contracts.py` returned `MISMATCH`
for all 19 roles. Only the Task role shares its H2 titles; its H3 titles
and tables differ, with 9 evidence columns against the core's 12. 209
differences are in the typed contract fields the local Registry does not
carry. Four negative inputs were rejected as `INVALID_INPUT` or `MISMATCH`:
a changed source hash, a missing source digest, an inexact revision, and a
declared core with the local tables. The export and its output stayed in
the session scratchpad and are not committed.

About 700 current documents follow the moved forms. The largest groups are
130 package READMEs, 110 Tasks, and 78, 78 and 77 guides, runbooks and
policies.

#### Adoption design

The adopted core stays one file: the package source and its schema are
copied byte for byte to `docs/99.templates/contracts/`. The Registry pins
both in `common.role_design_contract` by path and SHA-256, as it pins the
glossary for the vocabulary contract. A template role declares either
`core_role` or `core_exception`. An exception is `pending-migration` with
its target core role, `domain` or `native`, each with a reason. The profile
schema holds that shape: exactly one of the two fields, a core role on a
pending exception and none on a domain or native one. 26 roles are
pending, 8 are domain forms and 5 are native syntax. TemplateDefinition reports
the role design contract only for a bound role, so an unmoved role keeps
reporting `COMMON-DOC-FORM-1` or the legacy contract it actually follows.

`check-document-metadata.py --mode check-contracts` checks the pin, the
schema, the identity and every bound role. A bound role conforms when its
H2 and H3 titles, their order and requiredness, and each table's section,
column labels and column requiredness equal the core. Matching titles with
different tables fail, and so does an extra or missing table. The core
assigns all 22 of its tables to an H2, so a table may sit in any H3 of that
H2. Not compared: a table's own condition, which the projection does not
carry, and the core's numeric order fields, which the array order already
expresses. The core is 196,063 bytes, 74.8% of the 262,144-byte read
limit it shares with the Stage 99 schemas. Each pinned file is read once to
hash it and once to parse it. Every core H2 and H3 in 4.0.0 is required, and so is every
column. The core assigns different value types to the same
column label in different roles, so the global column dictionary cannot
carry them. W143, which binds the first role, makes a bound role read its
column types from the core. W142 binds no role. Rejected: copying the
core into Registry profiles, which would leave two owners, and binding all
roles at once, which would report an unmoved form under the new contract.

Two classifications are decisions. The governance policy form moves to the
core policy role with the operations policy form in W143. The provider
runtime READMEs are Markdown READMEs that the provider renderer writes, so
they move to the core root README role in W145 through that renderer, not by
hand. The data model contract stays a domain form: it describes entities in
a Spec Package, not a Stage 90 data reference.

Each later work unit moves one role group in one change: the Registry
profile, the template, the readers and the current documents. The role then
switches from `core_exception` to `core_role`. Reverting a work unit
restores its form and exception together.

#### W143 incident and postmortem

W142 merged as `ea786fb86`. W143 starts with the two incident forms because
each has one current document. A bound role now reads its table columns,
value types and requiredness from its core table, and the template must
use a core table's exact columns. The core says a table's rows are written
only when something happens, so a bound document must show every table
header its core role always requires and may have no rows; a missing header
is `table-missing`.

The incident and postmortem templates and profiles now carry the core H2
and H3 titles, and both template roles switch to `core_role`. The
corrective-action binding for incident closure follows the postmortem's new
`Actions` section; the review fixes below narrow it to `Owners and Checks`. The `Tracking ID` column lost its last template and is
removed from the column dictionary.

The `inc-0002` incident and postmortem keep every recorded fact. The
incident's decisions and mitigations become rows of its Actions table.
Nobody who acted is recorded, so Owner says so. Condition names the
Timeline step that performed the action: the three decisions keep their
recorded steps, two mitigations cite the steps that record the same action
(steps 5, 7 and 9), and four that the source never tied to a step say so.
The postmortem's completion phrase
becomes Condition and its Tracking ID with the check becomes Evidence. Five
test literals that named the old sections now name the core ones. Two
behaviour tests move to the forms that still use the old contract:
the dictionary lookup to the Task evidence table, and the common form
revision to roles without `core_role`.

#### W143 review fixes

The independent review of `1a8fadde6` and `df8b7e8d2` asked for three
changes. The documentation protocol still required a published postmortem to
keep its columns and to separate a root cause; it now names the core
postmortem sections and lets only the binding change move a published table.
The incident first said none of the six mitigations had a recorded step,
although steps 5, 7 and 9 record two of them; their Condition now cites those steps. The
closure check read the whole `## Actions` H2, so an owner named only in
Prevention prose passed. Registry `incident_closure.corrective_section` now
names `Owners and Checks`, which `section_forms` places under Actions, so only
the table and its note count. The `## Overview` fallback matched a shape no
form uses and is removed. The postmortem template prompt now asks Evidence
for the tracking record and its check, as the protocol does. A core table is now matched by its owning H2 as
well as its labels.

Two notes are kept for later work units. A document that puts a core table
under another H3 of the same H2 reports `table-missing` rather than a
placement finding, because the document check follows the template's H3;
W143's later parts meet this first. The pinned core is cached per process,
which the contracts check bypasses by re-reading.

#### W143 runbooks

W143 part one merged as `8a09edb3c`. The runbook template and profile now
carry the core sections, the Rollback condition is dropped because the core
requires every H3, and `operation/runbook` is bound. A one-time script moved
all 78 runbooks section by section and refused any unmapped content; a check
compared every non-heading line before and after and found none lost or
added. An old H3 title stays as an H4 only where several old sections merge
into one core H3. 36 links in 30 guides and policies pointed at the old
`#actions` anchor and now point at `#steps`.

Each runbook gained a steps table under Procedure/Steps and an Unverified
Conditions text, written from that runbook only. Six writing agents drafted
them; 856 rows in all, and 448 Expected Result cells say the document records
nothing to observe. A second script regenerated each moved runbook from the
base and confirmed that nothing beyond the table and that text changed. One
table named `@buenhyden` where the release runbook names the repository owner
or the operator on duty; it now uses the runbook's words. The request-brief
hook drops its binding whenever a new event reaches the session, so parallel
agents lost it mid-run; the rest were drafted to the scratchpad and applied
here after one bind, and one agent wrote with a script instead of the editor.

An agent wrote a draft through an unquoted shell heredoc, and a backticked
`docker compose --profile mail-dev restart mailpit` in the draft text ran.
The `mailpit` container restarted at 2026-11-17T03:22:54Z without approval;
it came back healthy with no restart loop. Whether captured messages survived
was not checked at first, and nothing else ran. A later read-only inspection
found `MP_DATABASE` at `/data/mailpit.db` on a bind-mounted volume, which a
restart keeps; message counts before and after were not compared.

14 runbooks keep 21 reference tables of their own under Procedure/Steps, such
as alert maps and exit codes. The core keeps an existing real form rather
than deleting or disguising it, and a table that reuses core labels with other
columns must not pass, so a table sharing no label with its section's core
table is now the document's own table. One sharing a label must be the core
table exactly, and the core table stays required.

#### W143 runbook review fixes

The independent review asked for changes. Prose in about 28 runbooks still
named the removed sections, such as Actions, Safety Checks and Authority and
Access; 48 lines now name the core sections, and names that survive as an H4
are kept. The n8n table was drafted from a skimmed read: one cell called the
attestation queue readable where the runbook says 401, and most Expected
Result cells said nothing was recorded where the runbook records receipts and
status codes. It and its Unverified Conditions were derived again from the
whole runbook, which also records isolated results the first text denied. The
OpenBao window table had no Finish step, which restores the writers stopped
in W3 and runs the ESO gate; it now does. Cells in the lab promotion and k6
tables that held constraints or a failure outcome as a result were corrected,
and an n8n sentence that credited two stop rules to the wrong sections now
names scenario 2 and Hermes step 5.

An empty core table beside a document's own table would carry the steps under
other labels, which the binding rule calls disguise, so it now fails as
`table-core-empty`. The Registry migration text of the three bound roles now
records their core move.

The re-review found four n8n cells that sent the no-send steps to a DB owner
the runbook names only for scenario 2; they now follow the runbook's general
route to @buenhyden. Two step references to the removed Actions section and
six pointers to an Escalation section below them now name Steps and the Next
Owner above, and an open design note left the n8n Unverified Conditions.

#### W143 guides

The guide template and profile now carry the core sections, and
`operation/guide` is bound. The core asks for its steps table only when a
guide has an ordered procedure, so the template carries it with that
condition. A script moved all 78 guides section by section, and three prose
lines that named a removed section now name the core one. Where an old H3
began with its own H4 headings, the inserted old title had nothing under it;
75 such titles in 36 guides are removed, and no inbound anchor changed.

Six writing agents drafted, from each guide only, its Audience and Next
Action, and a steps table for the 28 guides whose Steps hold a numbered
list: 129 rows. They wrote to the scratchpad and the drafts were applied
here after one bind. Compared with the base, the guides lost no line and
gained only that authored text and the three prose corrections. Every Next
Action names a runbook or owner its guide states.

#### W143 guide review fixes

The independent review found 25 more prose lines that named a removed
section; the first sweep missed them because it took a Korean particle as
part of the word. They now name Steps, Outcome, Authority or Expected
Results, and names that remain as a heading are kept. A k6 cell held the
no-guard failure as the expected result, a Storybook cell pointed at the
wrong row, and five cells held a constraint or a result the guide does not
state; each now follows its guide. The Renovate Audience now names the
reader its guide states. The old-form test now rejects the replaced guide
headings.

#### W143 operations policies

The operations policy template and profile now carry the core sections, the
template holds the always-required rules table under Requirements, and
`operation/policy` is bound. A script moved all 77 operations policies section
by section; no prose named a removed section, no anchor changed, and old
titles the move left empty were removed in the same pass. The test fixture
for a policy body now uses the core headings and the rules table header.

Six writing agents drafted, from each policy only, a Limits text and a rules
table with one row per top-level requirement: 851 rows. A Rule ID is the
policy's `artifact_id` with `-R` and its order, which the policy did not have
before; Enforcement and Evidence name a check or record the policy states,
`수동` for a manual review, or `none`; the review fixes below replace these
first tables. One draft lacked the required
`필수:` prefix on a mandatory rule and gained it. Compared with the base,
the policies lost no line and gained only that authored text; 15 Limits lists
gained the blank line Markdown requires before a list.

#### W143 operations policy review fixes

The independent review found the first rules tables unreliable: twelve
`금지:` rows stated the opposite of their rule, Enforcement cells named
checks the policy never ties to the rule or that do not test it, and rules
under `####` subsections were left out. Seven writing agents derived every
table and Limits text again from the policy prose under stricter rules: a row
for every rule statement in Requirements and its subsections, `금지:` naming
the forbidden act, a check named only where the policy ties it to that rule,
and Limits that agree with the table. Each draft cited the source lines of its rows. A
script rejected uncited rows and negated `금지:` rows and flagged a named
check missing from its cited line; four such ties and eleven loose ones were
lowered to `none` or `수동` and listed in Limits, and two truncated rows were
completed. The tables now hold 2415 rows, and no `금지:` row is negated. The re-review found twenty Limits line citations computed before the
tables shifted the lines below them; they are removed. Three POL-0078 rows
the catalog check names regain it, and POL-0045's Limits now says its `rg`
patterns find values without enforcing the rules.
Exceptions sections stay outside the tables because they are not
Requirements.

#### W143 governance policies

The governance control template and profile now carry the core policy
sections, and `governance/policy` is bound. A script moved all 15 governance
policies section by section, and the governance body fixtures use the core
headings. The rules tables were written under the strict rules the operations
policy review set, before any review: a row for every rule statement in
Requirements and its subsections, `Forbidden:` naming the forbidden act, a
check named only where the policy ties it to that rule, otherwise `none`, and
Limits that agree with the table. A Rule ID is the upper-cased file stem with
`-R` and its order, for example `BOOTSTRAP-R1`. Compared with `main`, the
policies lost no body line; they changed only their `version` and `updated`
values and gained the tables and Limits text. The profile test still named
the old sections and now expects the core ones.

#### W143 governance policy review fixes

The independent review found that the tables named a manual review, a check
or a record the policy does not tie to the rule, left out rule statements in
Requirements, carried rows from Enforcement Mechanisms in three policies, and
had Limits that contradicted the table or the policy. Five writing agents
derived every table and Limits text again from Requirements and its
subsections only, with a check, `manual` or a record named only where the
prose ties it to that rule, permissions written as `Allowed:`, and Limits
stating only what the table and the policy say, including that rules under
Enforcement Mechanisms are outside the table. The verifying apply script
rejected one draft row that lacked its permission text, which was completed
from the policy. The tables now hold 1131 rows, no `Forbidden:` row is
negated, and nothing outside the tables and Limits changed. The old-form test
now covers the governance policy profile, and both policy template prompts
state the same table rules without changing their registered versions.
The re-review approved the fix range with seven minor notes. Four are
applied: "record in the Task" rows now all name the Task record as Evidence,
a state description became a `Forbidden:` row, the Guide review-date row
states its rejection, and a Limits bullet no longer contradicts the one above
it. Three stay as they are: the GitHub update-branch row copies prose that
conflicts with the automatic merge exemption in the Git workflow policy, which
needs its own change; a build refusal names no check; and the remaining
statements describe behaviour rather than rules. The provider capability
Limits names a gap the policy states, which does not contradict its next
bullet.

#### W144 research, audit and data references

The research, audit and data reference forms move to the core research, audit
and data-reference roles: the Registry profiles and templates carry the core
sections, the research sources table, the audit findings table and the data
schema table, and the three roles are bound. All 23 research members move
section by section; no audit or data member exists. Writing agents drafted,
from each member only, its Versions and Dates text, its core sources table
(266 rows, by the member's own source IDs where it has them) and text for
required sections the member left empty, saying where it records nothing. The
drafts were applied in the main checkout, because a request brief cannot be
bound in an agent worktree. Compared with `main`, the members and the 0002
pack README lost no line; the 17 changed lines are 11 anchor repoints and
6 corrected section names or directions. An independent review found a stale section name,
sources-table cells the member does not support, Related Documents links under
unrelated labels, a Question section without the member's question, Versions
and Dates text wider than its table, and pointers left facing the wrong way;
each is corrected from the member's own text.

#### W145 agent instructions and skills

The folder agent guide and canonical skill forms move to the core
agent-instructions and skill roles, and both roles are bound. All 9 folder
`AGENTS.md` guides and 24 skills move section by section. Each guide gains an
Instruction Precedence text that says the owner of a summarized rule wins, as
the documentation protocol states, and links the bootstrap precedence order;
each skill gains a Limits text written from its own statements. Skill inputs
sit under Procedure as an H4 after the gates, and canonical sources sit under
Intake. Generated `CLAUDE.md` import shims and provider skill adapters name no
section, so the provider surface renderer reports no drift. The drafts were
applied in the main checkout. An independent review found that the first
precedence sentence ranked every Intake source, provider adapters included,
above the guide, and that protected actions which are not secrets or external
effects sat under Secrets and External Effects; both are corrected, and those
actions now sit under Authority beside Stop and Escalate. Compared with `main`,
the guides and skills lost no line except the one renamed section reference.

#### W146 requirements, architecture and decisions

The Requirement Package, Architecture Description and ADR forms move to the
core requirement, architecture and decision roles, and the three roles are
bound. All 18 Requirement Packages, 27 Architecture Descriptions and 30 ADRs
move section by section. The owner directed an in-place amendment of the 30
accepted ADRs for the move, and each records it in Follow-up with its decision
text unchanged. Each package gains a requirements table whose Statement repeats
its declaration exactly; the owner decided on 2026-11-17 that a declaration
without a modal verb binds as `must`, and the protocol and template record that
rule. Five packages gain a quality table; descriptions gain Trade-offs text and
interface tables; ADRs gain options tables; each is written from the document,
saying where it records nothing. A new check fails when the requirements table
and the declarations name different IDs. The core architecture and decision
forms have no Traceability section, so, following the prompt's rule that a
requirement and a conflicting policy change together, a retirement summary now
goes to the owner's lineage section: Traceability in a Requirement Package,
Decisions and Adoption / Adoption Boundaries in an Architecture Description and
Decision / Authority and Effect in an ADR; the protocol, glossary, REQ-0026,
ADR-0051, AD-0030 and two READMEs say so. An independent review found prose
still naming Traceability, Statements that differed from their declarations,
interface cells beyond the document, PATCH bumps for contract changes and no
Task record; each is corrected.

#### W145 READMEs

Every README form moves to the core stage, service or root README role, and
the README roles are bound: the common, documentation, category and research,
audit and data pack READMEs take the stage form, package READMEs the service
form, and the repository and runtime READMEs the root form; the provider
surface renderer writes the runtime READMEs in that form. The incident year
README and the three governance index READMEs had no template role; each now
has its own template role bound to the stage form, because a role carries one
profile. All 216 current READMEs move section by section. Their path tables
sit under the core path headings, and owners, help, audience and excluded
responsibilities come from each README. The core renders a conditional section
whenever it applies, so a README that states its own external interface,
tier READMEs included, gains the service interface table written from its own
text (302 rows in 101 READMEs), and a README that only delegates to its leaves
gains none. Compared with its base, the READMEs changed 43 lines on purpose:
25 prose references and 9 links to removed sections, 3 table headers, 2 lines
naming the old path table and 4 lines that said no template existed. An
independent review found stale template statements, a link into Stage 98,
uneven tier tables, a stale reader comment, missing audit and data old-form
cases, a renamed report heading and cells beyond their README; each is
corrected, and the re-review approved.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0081 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0081 | ready | in-progress | #adoption-design |

### Blockers and Decisions

The owner decided full adoption on 2026-11-17. Moving W143 to W147 changes
current documents, and those changes need the same per-group review.
The owner approved the `mailpit` restart during W143 in this chat on
2026-11-17; no further runtime action is taken for it.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Core comparison baseline | 137 | W142 | role-design-export | Workspace export at `fdb92cd82` through the package `compare_template_contracts.py --workspace-root` | FAIL | MISMATCH for 19 of 19 roles, 20 unmapped forms, exit 1 | required | - |
| Comparison negatives | 137 | W142 | role-design-export-negative | Changed hash, missing digest, inexact revision and declared core with local tables | PASS | Three INVALID_INPUT and one MISMATCH, as designed | required | - |
| Conformance RED | 137 | W142 | role-design-conformance | RoleDesignConformanceTests before the implementation | ERROR | `role_design_findings` did not exist, exit 1 | required | - |
| Conformance GREEN | 137 | W142 | role-design-conformance | test_template_definition with the pinned core and classified roles | PASS | 35 tests, exit 0 | required | Conformance RED |
| Contract wiring | 137 | W142 | document-contracts | check-document-metadata.py --mode check-contracts, then with one byte appended to the core | PASS | 0 violations; the changed core gave `role-design-source-changed`, exit 1; restored | required | - |
| Foundation review | 137 | W142 | independent-review | Commits `c1541ea86` and `9019594c7` | FAIL | CHANGES_REQUIRED: H2-owned tables rejected inside their H3, Stage 99 checks unrecorded, schema unpinned, failure paths and exception rules incomplete | required | - |
| Conformance review fixes | 137 | W142 | role-design-conformance | RoleDesignConformanceTests at `3e30b52ce` with H3 placement, extra and missing tables, H3 requiredness, unknown and unmapped roles, schema-held exception shape and identity | PASS | 13 tests, exit 0 | required | - |
| Foundation regression | 137 | W142 | document-governance-regression | test_registry, test_template_definition, metadata.test_heading, metadata.test_reference, test_metadata_validator and test_taxonomy at `3e30b52ce` | PASS | 374 tests in 363.184 seconds, exit 0 | required | - |
| Foundation corpus | 137 | W142 | document-corpus | check-active, check-contracts, corpus lifecycle, link alignment and governance contract at `3e30b52ce` | PASS | 589 selected and 0 violations; 0 contract, lifecycle and governance findings; alignment PASS | required | - |
| Foundation re-review | 137 | W142 | independent-review | Commits `3e30b52ce` and `f958da1ef` against the first review | PASS | APPROVE; six minor notes, of which the schema-hash test, the two document mentions, these revisions and the duplicate test are applied | required | Foundation review |
| Incident form RED | 137 | W143 | role-design-binding | Bound-role, core column and missing-table tests at `ea786fb86` | FAIL | Neither role bound, columns from `COMMON-DOC-FORM-1`, no `table-missing`, exit 1 | required | - |
| Incident form GREEN | 137 | W143 | role-design-binding | Same tests with incident and postmortem bound, on the tree committed as `1a8fadde6` | PASS | test_template_definition and RegisteredTableContractTests passed, exit 0 | required | Incident form RED |
| Incident regression | 137 | W143 | document-governance-regression | test_registry, test_template_definition, metadata heading, reference and lifecycle, test_metadata_validator, test_taxonomy and test_operations_catalog, on the tree committed as `1a8fadde6` | FAIL | 552 tests, 2 failures: the conforming-body fixture lacked the incident and postmortem table headers | required | - |
| Incident regression rerun | 137 | W143 | document-governance-regression | metadata.test_heading with the fixture adding each bound role's table header; no other module changed after the full run | PASS | 111 tests, exit 0 | required | Incident regression |
| Incident corpus | 137 | W143 | document-corpus | check-active, check-contracts, check-operations-catalog, corpus lifecycle and link alignment at `1a8fadde6` | PASS | 589 selected and 0 violations; contracts, catalog, lifecycle and alignment pass | required | - |
| Incident review | 137 | W143 | independent-review | Commits `1a8fadde6` and `df8b7e8d2` | FAIL | CHANGES_REQUIRED: the protocol still fixed published postmortem columns, the incident misstated two mitigations' steps, and closure read the whole Actions H2 | required | - |
| Review fix RED | 137 | W143 | closure-scope | Prevention-only owner, Registry closure key, core table under another H2, incident table-missing and header-only tests at `df8b7e8d2` | FAIL | 329 tests: 3 failures, and 2 test-helper errors corrected before the H2 test failed with no RegistryError | required | - |
| Review fix GREEN | 137 | W143 | closure-scope | test_template_definition, RegisteredTableContractTests, test_registry and test_operations_catalog on the tree committed as `fc69f689b` | PASS | 357 tests, exit 0 | required | Review fix RED |
| Review fix regression | 137 | W143 | document-governance-regression | metadata heading, reference and lifecycle, test_metadata_validator, test_taxonomy and test_spec_packages on the tree committed as `fc69f689b` | FAIL | 358 tests, 1 failure: test_common_form_paths_come_from_the_registry did not list the new Owners and Checks path | required | - |
| Review fix regression rerun | 137 | W143 | document-governance-regression | That test with the new path, and test_template_definition; no other module changed after the full run | PASS | 44 tests, exit 0 | required | Review fix regression |
| Review fix template version | 137 | W143 | document-corpus | check-contracts after the template prompt change | FAIL | `invalid-template-version`: the prompt edit had bumped the template version, which must stay the registered initial version; reverted | required | - |
| Review fix corpus | 137 | W143 | document-corpus | check-active, check-contracts, check-changed against `origin/main`, check-operations-catalog, link alignment and governance contract | PASS | 589 selected and 0 violations; 0 contract violations; 6 changed and 0 violations; catalog, alignment and governance PASS | required | Review fix template version |
| Incident re-review | 137 | W143 | independent-review | The fix range against the first review | PASS | APPROVE; five minor notes, of which the two Task wordings, these rows and the template Evidence prompt are applied; the Condition notes stay for later role groups | required | Incident review |
| Runbook form RED | 137 | W143 | role-design-binding | Bound runbook role and core steps columns at `57e28c54a` | FAIL | Role unbound and columns from `COMMON-DOC-FORM-1`, exit 1 | required | - |
| Runbook form GREEN | 137 | W143 | role-design-binding | test_template_definition with the runbook template and profile on the core and two old literals updated | PASS | 44 tests, exit 0 | required | Runbook form RED |
| Runbook move fidelity | 137 | W143 | document-move | 78 runbooks moved by the section script; non-heading lines before and after, then each runbook regenerated from base against the authored result | PASS | 0 lines lost or added; 0 runbooks changed beyond the table and Unverified Conditions; 856 rows, every row 4 cells and numbered | required | - |
| Runbook reference tables | 137 | W143 | document-corpus | check-changed against `origin/main` after authoring | FAIL | 14 `table-header-invalid`: 21 reference tables under Procedure/Steps read as the core steps table | required | - |
| Reference table RED | 137 | W143 | table-ownership | A reference table sharing no core label beside the incident Actions table | FAIL | `table-header-invalid`, exit 1 | required | - |
| Reference table GREEN | 137 | W143 | table-ownership | Same test, and a table sharing a core label with other columns | PASS | metadata.test_heading 115 tests, exit 0 | required | Reference table RED |
| Runbook regression | 137 | W143 | document-governance-regression | test_registry, test_template_definition, test_operations_catalog, metadata heading, reference and lifecycle, test_metadata_validator, test_taxonomy and test_spec_packages before the table change | FAIL | 707 tests, 2 failures: two runbook literals in metadata.test_heading named the old form | required | - |
| Runbook regression rerun | 137 | W143 | document-governance-regression | metadata.test_heading with the core literals and the table change; no other module changed after the full run | PASS | 115 tests, exit 0 | required | Runbook regression |
| Runbook corpus | 137 | W143 | document-corpus | check-active, check-contracts, check-changed against `origin/main`, check-operations-catalog, link alignment and markdownlint of the 109 Markdown files in the working-tree diff, while check-changed selects every governed document changed against `origin/main` | PASS | 589 selected and 0 violations; 0 contract violations; 115 changed and 0 violations; catalog and alignment PASS; 0 lint issues | required | Runbook reference tables |
| Runbook review | 137 | W143 | independent-review | Commits `01567d292`, `94c26da36` and `00b8880d0` | FAIL | CHANGES_REQUIRED: n8n and OpenBao window cells contradict or omit their runbooks, stale section names, an empty core table beside an own table passes | required | - |
| Disguise RED | 137 | W143 | table-ownership | A runbook reference table beside its emptied steps table, a reference table without the core table, and an unbound role's table with no shared label | FAIL | 1 failure: no `table-core-empty`; the other two already held | required | - |
| Disguise GREEN | 137 | W143 | table-ownership | Same tests after the change | PASS | metadata.test_heading 119 tests, exit 0 | required | Disguise RED |
| Runbook review corpus | 137 | W143 | document-corpus | check-contracts, check-changed against `origin/main`, check-operations-catalog and link alignment after the fixes | PASS | 0 contract violations; 110 changed and 0 violations after one `runtime-version-literal` in new 0105 prose was reworded; catalog and alignment PASS | required | - |
| Runbook re-review | 137 | W143 | independent-review | Fix range `4f9c142d1`, `7c27251f3` and `a86c266eb` against the review | FAIL | CHANGES_REQUIRED: four n8n no-send cells routed to a DB owner the runbook does not name there; two step references and six Escalation pointers stale | required | - |
| Runbook review approval | 137 | W143 | independent-review | Fix commits `4f9c142d1`, `7c27251f3`, `a86c266eb`, `b49a8a11e` and `ca7e638ec` against the first review | PASS | APPROVE at `ca7e638ec`; every Important and Minor finding fixed | required | Runbook review |
| Runbook re-review approval | 137 | W143 | independent-review | Fix commits `b49a8a11e` and `ca7e638ec` against the re-review | PASS | APPROVE at `ca7e638ec`; R1 to R4 fixed | required | Runbook re-review |
| Guide form RED | 137 | W143 | role-design-binding | Bound guide role at `2e158ecde` | FAIL | Role unbound, exit 1 | required | - |
| Guide form GREEN | 137 | W143 | role-design-binding | test_template_definition with the guide template and profile on the core | PASS | 44 tests, exit 0 | required | Guide form RED |
| Guide move fidelity | 137 | W143 | document-move | 78 guides against base: non-heading lines lost and lines added beyond the authored Audience, Next Action and tables | PASS | 0 lost; only the three prose corrections added; 28 tables with 129 rows | required | - |
| Guide empty titles | 137 | W143 | document-corpus | check-changed against `origin/main` after the drafts were applied | FAIL | 36 `body-section-empty`: old H3 titles kept as H4 with only H4 headings under them | required | - |
| Guide regression | 137 | W143 | document-governance-regression | metadata.test_heading, test_template_definition and test_registry, then test_operations_catalog, then test_metadata_validator, metadata reference and lifecycle, test_spec_packages and test_taxonomy | PASS | 332 tests after the guide literal and one Registry test moved to the core sections; 136; 245; exit 0 | required | - |
| Guide corpus | 137 | W143 | document-corpus | check-changed against `origin/main`, check-contracts, check-operations-catalog, link alignment and markdownlint after the empty titles were removed | PASS | 167 changed and 0 violations; 0 contract violations; catalog and alignment PASS; 0 lint issues | required | Guide empty titles |
| Guide review | 137 | W143 | independent-review | Commits `efd26a4d3`, `da9fc935d` and `2bf4ba56c` | FAIL | CHANGES_REQUIRED: 25 prose lines still name removed sections, a k6 failure outcome as Expected Result, a Storybook row reference off by three, constraints in five cells | required | - |
| Guide review corpus | 137 | W143 | document-corpus | metadata.test_heading with the replaced guide headings, check-changed against `origin/main` and link alignment after the fixes | PASS | 119 tests, exit 0; 80 changed and 0 violations; alignment PASS | required | - |
| Guide review approval | 137 | W143 | independent-review | Fix commits `e8ae10439` and `f94a0d4de` against the guide review | PASS | APPROVE at `f94a0d4de`; I1 to I3 and the applied minors fixed, the rest accepted with reasons | required | Guide review |
| Policy form RED | 137 | W143 | role-design-binding | Bound policy role at `2bf4ba56c` | FAIL | Role unbound, exit 1 | required | - |
| Policy form GREEN | 137 | W143 | role-design-binding | test_template_definition with the policy template and profile on the core | PASS | 44 tests, exit 0 | required | Policy form RED |
| Policy move fidelity | 137 | W143 | document-move | 77 operations policies against base: non-heading lines lost and lines added beyond the authored Limits and tables | PASS | 0 lost and 0 unexplained; 851 rows | required | - |
| Policy lint | 137 | W143 | document-corpus | markdownlint of the changed policies after the drafts were applied | FAIL | MD032 in 15 Limits lists without a blank line before the list | required | - |
| Policy corpus | 137 | W143 | document-corpus | check-changed against `origin/main`, check-contracts, check-operations-catalog, link alignment and markdownlint after the blank lines | PASS | 158 changed and 0 violations, then 78 after rebase; 0 contract violations; catalog and alignment PASS; 0 lint issues | required | Policy lint |
| Policy regression | 137 | W143 | document-governance-regression | test_registry, test_template_definition, metadata heading, reference and lifecycle, test_operations_catalog, test_metadata_validator, test_spec_packages and test_taxonomy | PASS | 713 tests, exit 0 | required | - |
| Policy review | 137 | W143 | independent-review | Commits `b901796e3` and the TSK-0081 record | FAIL | CHANGES_REQUIRED: twelve inverted `금지:` rows, Enforcement cells naming checks the policy does not tie to the rule, rules under subsections missing | required | - |
| Policy redraft verification | 137 | W143 | rule-table-verification | 77 redrafted tables through the verifying apply script, then check-changed, check-contracts, check-operations-catalog, link alignment and markdownlint | PASS | 2415 rows, 0 uncited, 0 negated `금지:`; 0 violations; catalog and alignment PASS; 0 lint issues | required | - |
| Policy re-review | 137 | W143 | independent-review | Fix range `7e23e2acf` and `83fe20401` against the first review | FAIL | CHANGES_REQUIRED: I1 to I3 and M1 to M3 fixed; twenty Limits line citations point at shifted lines | required | - |
| Policy review approval | 137 | W143 | independent-review | Fix commits `7e23e2acf`, `83fe20401`, `3bd9a044c` and `a92dec37c` against the first review | PASS | APPROVE at `a92dec37c`; I1 to I3 and M1 to M3 fixed | required | Policy review |
| Policy re-review approval | 137 | W143 | independent-review | Fix commits `3bd9a044c` and `a92dec37c` against the re-review | PASS | APPROVE at `a92dec37c`; N1, N2 and N4 fixed, N3 left as wording | required | Policy re-review |
| Policy hosted candidate | 137 | W143 | hosted-candidate | PR 1065 candidate-core at `c38dec7de` | FAIL | `test_production_scripts_do_not_reference_tests_tree` flagged `metadata/lifecycle.py`: a comment from the W03-FORMS change named the fixture path literally; it also failed on main at `bbdca00d1` | required | - |
| Policy hosted candidate fix | 137 | W143 | hosted-candidate | tests.validation.test_script_manifest after the comment names the tree in words | PASS | Module passed locally, exit 0; the hosted rerun is the next observation | required | Policy hosted candidate |
| Policy hosted candidate rerun | 137 | W143 | hosted-candidate | PR 1065 checks at `a237c0df4` | PASS | candidate-core, candidate-documents, candidate-quality, candidate-routing, CodeQL and GitGuardian pass; merged as `82cf41b9d` | required | Policy hosted candidate |
| Governance form RED | 137 | W143 | role-design-binding | test_template_definition from the governance branch against `main` at `82cf41b9d` | FAIL | 44 tests, 1 failure: `governance/policy` unbound | required | - |
| Governance form GREEN | 137 | W143 | role-design-binding | Same module with the control template and profile on the core, at `e7fc61911` | PASS | Part of the governance regression below | required | Governance form RED |
| Governance move fidelity | 137 | W143 | document-move | 15 governance policies at `e7fc61911` against `82cf41b9d`: non-heading lines lost and added | PASS | Lost only the 29 frontmatter `version` and `updated` lines; added 29 frontmatter lines, 158 Limits lines and 15 tables | required | - |
| Governance table verification | 137 | W143 | rule-table-verification | Rule rows in the 15 tables at `e7fc61911` | PASS | 768 rows, 0 negated `Forbidden:` rows | required | - |
| Governance profile test | 137 | W143 | document-governance-regression | metadata.test_profile at `2a4331860`, before the profile test change | FAIL | 18 tests, 1 failure: the approval-boundary body test named the old sections | required | - |
| Governance regression | 137 | W143 | document-governance-regression | test_registry, test_template_definition, metadata heading, profile, reference and lifecycle, test_metadata_validator, test_spec_packages, test_taxonomy, test_operations_catalog and test_script_manifest at `e7fc61911` | PASS | 782 tests in 1469 seconds, exit 0 | required | Governance profile test |
| Governance corpus | 137 | W143 | document-corpus | check-changed against `origin/main`, check-contracts, governance contract, provider surface renderer, link alignment and markdownlint at `e7fc61911` | PASS | 16 changed and 0 violations; 0 contract violations; governance contract, renderer and alignment PASS; 0 lint issues | required | - |
| Acceptance record | 137 | W143 | hosted-candidate | PR 1066 at `332efd5bf`, with criterion 137 recorded as accepted | FAIL | candidate-core: Criterion Acceptance cited a phrase, not Evidence rows; candidate-documents lifecycle public tests failed on the same package; candidate-quality aggregates both. With exact citations the local check reported `accepted criterion 137 has an unresolved required observation` (Core comparison baseline) | required | - |
| Acceptance record fix | 137 | W143 | document-corpus | check-changed against `origin/main` and tests.validation.lifecycle.test_public with criterion 137 kept pending and the owner's statement in Decision | PASS | 17 changed and 0 violations; 6 tests, exit 0; the hosted rerun is the next observation | required | - |
| Governance review | 137 | W143 | independent-review | Commits `b020c2dc9`, `2a4331860`, `e7fc61911` and the TSK-0081 record | FAIL | CHANGES_REQUIRED: unsupported Enforcement and Evidence cells, missing Requirements rules, Limits contradicting the table or policy, modality errors, Mechanisms rows in three policies, no governance old-form test, template prompts asking for `manual` | required | - |
| Governance old-form RED | 137 | W143 | role-design-binding | metadata.test_heading old-form test with governance policy cases against `main` at `82cf41b9d` | FAIL | 4 governance subtests failed: the old headings were accepted | required | - |
| Governance old-form GREEN | 137 | W143 | role-design-binding | Same test on the branch, then test_template_definition and test_registry with the template prompts changed, before `c19cb34fe` and `fbb211eeb` | PASS | 1 test, exit 0; 213 tests, exit 0; check-contracts 0 violations | required | Governance old-form RED |
| Governance redraft verification | 137 | W143 | rule-table-verification | 15 redrafted tables through the verifying apply script, then a comparison of every non-table, non-Limits line with `fbb211eeb`, as committed in `bde3d458c` | PASS | 0 problems after one row was completed; 3 warnings where the tying text spans lines; 1131 rows, 0 negated `Forbidden:` rows, 0 other lines changed | required | - |
| Governance review corpus | 137 | W143 | document-corpus | check-changed against `origin/main`, check-contracts, governance contract, provider surface renderer, link alignment and markdownlint at `bde3d458c` | PASS | 18 changed and 0 violations; 0 contract violations; governance contract, renderer and alignment PASS; 0 lint issues | required | - |
| Governance re-review | 137 | W143 | independent-review | Fix commits `c19cb34fe`, `fbb211eeb`, `bde3d458c` and `9c4093232` against the governance review | PASS | APPROVE at `9c4093232`; I1 to I3 and M1 to M4 fixed; seven minor notes, four applied | required | Governance review |
| Governance review regression | 137 | W143 | document-governance-regression | The ten governance modules and test_script_manifest at `9c4093232` in a separate worktree, with the exit code read directly; the later commits change only table cells and this record | PASS | 782 tests in 2490 seconds, exit 0 | required | - |
| References form RED | 137 | W144 | role-design-binding | test_template_definition and metadata.test_heading with only the W144 test changes, at `aa4d100f5` on `82cf41b9d` | FAIL | 163 tests, 2 failures and 8 errors: research unbound and no research-member representative | required | - |
| References form GREEN | 137 | W144 | role-design-binding | The ten governance modules, test_script_manifest, test_links and test_language at `9b1b7f37a` in a separate worktree | PASS | 917 tests in 1847 seconds, exit 0 | required | References form RED |
| References move fidelity | 137 | W144 | document-move | The 23 members and the 0002 pack README at `419717c49`, after the review fixes, against `main`; non-heading lines lost and added | PASS | 0 lines lost beyond the 17 deliberate edits: 11 anchor repoints and 6 corrected section names or directions; 733 lines added | required | - |
| References corpus | 137 | W144 | document-corpus | check-changed against `origin/main`, check-contracts, link alignment, corpus lifecycle and markdownlint at `9b1b7f37a` | PASS | 27 changed and 0 violations; 0 contract and lifecycle violations; alignment PASS; 0 lint issues | required | - |
| References review | 137 | W144 | independent-review | Commits `aa4d100f5` and `9b1b7f37a` | FAIL | CHANGES_REQUIRED: a stale section name, unsupported sources-table cells, no Task record, and seven minor placement and wording findings | required | - |
| References review fix checks | 137 | W144 | document-corpus | check-changed, link alignment and navigation, markdownlint, metadata.test_heading and metadata.test_reference after the fixes, rebased on `3d53456da` | PASS | 27 changed and 0 violations; alignment and navigation PASS; 0 lint issues; tests OK | required | - |
| References re-review | 137 | W144 | independent-review | Fix commit `4752d897d` and the Task record against the references review, at `a0e205ecc` | PASS | APPROVE; I1 to I3 and M1 to M7 fixed; three minor notes applied | required | References review |
| Agent instructions form RED | 137 | W145 | role-design-binding | test_template_definition and metadata.test_heading from the W145 agent instructions branch against `main` at `3d53456da` | FAIL | 163 tests, 9 failures: agent-instructions unbound, old guide and skill sections accepted, the two H2 orders still old | required | - |
| Agent instructions form GREEN | 137 | W145 | role-design-binding | The ten governance modules, test_script_manifest and test_language at `3d7e8dd36` in a separate worktree | PASS | 789 tests in 1613 seconds, exit 0 | required | Agent instructions form RED |
| Agent instructions move fidelity | 137 | W145 | document-move | 9 guides and 24 skills at `3d7e8dd36` against `main`, non-heading lines lost and added | PASS | 0 lines lost beyond one renamed section reference; 105 lines added | required | - |
| Agent instructions corpus | 137 | W145 | document-corpus | check-changed against `origin/main`, check-contracts, link alignment and navigation, corpus lifecycle, governance contract, provider surface renderer and markdownlint at `cbac26d12` | PASS | 36 changed and 0 violations; contracts and lifecycle 0; alignment, navigation, governance contract and renderer PASS; 0 lint issues | required | - |
| Agent instructions review | 137 | W145 | independent-review | Commit `cbac26d12` | FAIL | CHANGES_REQUIRED: the precedence sentence overstated Intake sources, authority rules sat under Secrets and External Effects, no Task record, four minor notes | required | - |
| Agent instructions review fix checks | 137 | W145 | document-corpus | check-changed, check-contracts, link alignment, governance contract, renderer, markdownlint, metadata.test_heading and test_template_definition after the fixes, then check-changed after the rebase on `3d53456da` raised the protocol to 7.4.0 | PASS | 36 changed and 0 violations; contracts 0; alignment, governance contract and renderer PASS; 0 lint issues; tests OK | required | - |
| Agent instructions head checks | 137 | W145 | document-corpus | check-changed and check-contracts at `fc9ae1e02` against `origin/main` `3377e6ecb` | PASS | 37 changed and 0 violations; 0 contract violations | required | - |
| Agent instructions re-review | 137 | W145 | independent-review | Fix range `f971dcf66..fc9ae1e02` against the agent instructions review | PASS | APPROVE; findings 1 to 7 fixed or accepted; two minor notes applied | required | Agent instructions review |
| SDLC forms RED | 137 | W146 | role-design-binding | test_template_definition and metadata.test_heading from the W146 branch against `main` at `3377e6ecb` | FAIL | 163 tests, 16 failures: requirement unbound, old headings accepted, table-missing not expected | required | - |
| SDLC forms move fidelity | 137 | W146 | document-move | 18 Requirement Packages, 27 Architecture Descriptions and 30 ADRs at `110e484d1` against `main` | PASS | 0 lines lost beyond 14 deliberate edits: lineage wording in REQ-0026, ADR-0051 and AD-0030 and five renamed section references; 995 lines added | required | - |
| SDLC forms corpus | 137 | W146 | document-corpus | check-changed against `origin/main` `3377e6ecb`, check-contracts, link alignment and corpus lifecycle at `110e484d1`; navigation, governance contract, renderer and markdownlint at `88d473c69` | PASS | 85 changed and 0 violations; 0 contract and lifecycle violations; alignment, navigation, governance contract and renderer PASS; 0 lint issues | required | - |
| SDLC forms first regression | 137 | W146 | document-governance-regression | The ten governance modules, test_script_manifest, test_requirements, test_relations, test_architecture and test_language at `88d473c69`, before the review fixes | PASS | 841 tests in 1724 seconds, exit 0 | required | - |
| SDLC forms review | 137 | W146 | independent-review | Commits `88d473c69` and `712787db3` | FAIL | CHANGES_REQUIRED: prose still naming Traceability, Statements differing from declarations, inferred Priority, interface cells beyond the document, PATCH bumps for contract changes, no Task record | required | - |
| SDLC forms GREEN | 137 | W146 | role-design-binding | The ten governance modules, test_script_manifest, test_requirements, test_relations, test_architecture and test_language at `110e484d1`, after the review fixes | PASS | 842 tests in 1819 seconds, exit 0 | required | SDLC forms RED |
| SDLC forms review fix checks | 137 | W146 | document-corpus | check-changed against `origin/main` `1b51e0b04` after the rebase raised the protocol to 7.5.0 | PASS | 86 changed and 0 violations | required | - |
| SDLC forms re-review | 137 | W146 | independent-review | Fix range `96112a806..0b55dc47b` against the SDLC forms review | FAIL | CHANGES_REQUIRED: earlier findings 1 to 12 resolved; protocol rule rows R72, R135 and R245 kept the old wording and the new rules had no row; documented recovery text dropped from interface cells; the table check skipped an aligned header; evidence after the rebase was thin | required | - |
| SDLC forms hosted candidate | 137 | W146 | hosted-candidate | PR 1069 at `0b55dc47b` | FAIL | candidate-documents: test_an_unknown_or_unmapped_core_role_is_reported picked `common/documentation-readme`, whose target stage-readme other pending roles share once W144 and W145 merged, so no core role was left unmapped | required | - |
| SDLC forms aligned header RED | 137 | W146 | requirements-table | test_requirements with a column-aligned header and a missing ID, before the label match | FAIL | 29 tests, 1 failure: RequirementPackageError not raised | required | - |
| SDLC forms re-review fix checks | 137 | W146 | document-corpus | check-changed against `origin/main` `1b51e0b04`, check-contracts, governance contract, link alignment, corpus lifecycle and markdownlint; test_requirements, metadata.test_heading and test_template_definition at `3ba5d78b4` | PASS | 86 changed and 0 violations; 0 contract and lifecycle violations; governance contract and alignment PASS; 0 lint issues; 29, 148 and 44 tests OK | required | - |
| SDLC forms aligned header GREEN | 137 | W146 | requirements-table | test_requirements after the header is matched by its cell labels, at `3ba5d78b4` | PASS | 29 tests, exit 0 | required | SDLC forms aligned header RED |
| SDLC forms hosted candidate rerun | 137 | W146 | hosted-candidate | PR 1069 checks at `c01881150`, after the pending-role fixture fix | PASS | candidate-core, candidate-documents, candidate-quality, candidate-routing, CodeQL and GitGuardian pass | required | SDLC forms hosted candidate |
| SDLC forms re-review approval | 137 | W146 | independent-review | Fix ranges `96112a806..0b55dc47b` and `0b55dc47b..c01881150` against the SDLC forms review and re-review | PASS | APPROVE at `c01881150`; findings 1 to 12 and the four re-review findings fixed; nit 5 kept as faithful to the declaration | required | SDLC forms re-review |
| READMEs form RED | 137 | W145 | role-design-binding | test_template_definition and metadata.test_heading with only the README test changes, run by the drafting agent in a scratch clone of `82cf41b9d`, then the follow-up test changes on `424177119` | FAIL | 163 tests, 57 failures (stage-readme unbound, old headings accepted, path tables under the old headings); follow-up 28 tests, 29 subtest failures for the four index profiles | required | - |
| READMEs move fidelity | 137 | W145 | document-move | 216 READMEs at the README branch head against `82cf41b9d`, non-heading lines changed and added | PASS | 43 deliberate changes: 25 prose references and 9 links to removed sections, 3 table headers, 2 lines naming the old path table, 4 lines that said no template existed; 1067 lines added | required | - |
| READMEs first regression | 137 | W145 | document-governance-regression | The ten governance modules, test_script_manifest, test_language and test_lab_controller at `0357d8473`, before the review fixes | PASS | 889 tests in 1713 seconds, exit 0 | required | - |
| READMEs review | 137 | W145 | independent-review | Commits `424177119`, `d1a3a62fd` and `0357d8473` | FAIL | CHANGES_REQUIRED: stale template statements, a link into Stage 98, uneven tier interface tables, and six minor findings | required | - |
| READMEs re-review | 137 | W145 | independent-review | Fix range `0357d8473..2d2f52080` against the READMEs review | PASS | APPROVE; all nine findings fixed; the code-path template pointer in the three `.agents` READMEs accepted; two minor notes applied in `52f6d04c3` | required | READMEs review |
| READMEs corpus | 137 | W145 | document-corpus | check-changed against `origin/main` `a3fbbbd1c`, check-contracts, link alignment and navigation, provider surface renderer and governance contract at `223821638`, after the rebase | PASS | 230 changed and 0 violations; 0 contract violations; alignment, navigation, renderer and governance contract PASS | required | - |

### Resolution Links

Conformance GREEN resolves Conformance RED, and Foundation re-review resolves
Foundation review. Runbook form GREEN, Reference table GREEN, Runbook
regression rerun, Runbook corpus, Disguise GREEN, Runbook review approval,
Runbook re-review approval, Guide form GREEN, Guide corpus, Guide review approval, Policy form GREEN, Policy corpus, Policy review approval, Policy re-review approval, Policy hosted candidate
rerun, Governance form GREEN, Governance regression, Governance old-form GREEN, Governance re-review, Incident regression rerun, Review fix GREEN, Review fix
regression rerun, Review fix corpus and Incident re-review resolve their W143
rows, References form GREEN and References re-review resolve their W144 rows, Agent instructions form GREEN and Agent instructions re-review resolve their W145 rows, and SDLC forms GREEN, SDLC forms aligned header GREEN, SDLC forms hosted candidate rerun and SDLC forms re-review approval resolve their W146 rows, and READMEs re-review resolves its W145 README row. The comparison baseline stays
open until every role group conforms.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 137 | pending | Conformance GREEN, Contract wiring, Foundation re-review, Incident re-review, Runbook review approval, Guide review approval, Policy review approval, Governance regression | Owner @buenhyden stated acceptance on 2026-11-17 in this chat; the validator rejects `accepted` while the required Core comparison baseline is unresolved, and the owner chose to keep it pending until the conforming export resolves that baseline | @buenhyden |

### Remaining Conditions

W145 to W147 still move their role
groups, each with its own review. The comparison baseline is resolved only by
a later export that conforms for every bound role.

## Handoff

### Promotion Receipt

The Registry, the tracked core and its schema, `template_definition.py` and
the contracts check hold the binding. The documentation protocol lists the
role design contract as a version object.

### Next Owner

The implementer owns W143 to W147. Criterion 137 becomes accepted when the conforming export resolves the baseline, as the owner chose.
