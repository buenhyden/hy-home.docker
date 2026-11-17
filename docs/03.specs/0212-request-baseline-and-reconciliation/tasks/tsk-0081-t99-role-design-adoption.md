---
title: "T99 Role Design Adoption Task"
version: "0.5.0"
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

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0081 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0081 | ready | in-progress | #adoption-design |

### Blockers and Decisions

The owner decided full adoption on 2026-11-17. Moving W143 to W147 changes
current documents, and those changes need the same per-group review.
The unapproved `mailpit` restart during W143 awaits the owner's
acknowledgement; no further runtime action is taken for it.

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

### Resolution Links

Conformance GREEN resolves Conformance RED, and Foundation re-review resolves
Foundation review. Runbook form GREEN, Reference table GREEN, Runbook
regression rerun, Runbook corpus, Disguise GREEN, Incident regression rerun, Review fix GREEN, Review fix
regression rerun, Review fix corpus and Incident re-review resolve their W143
rows. The comparison baseline stays
open until every role group conforms.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 137 | pending | Conformance GREEN, Contract wiring | Awaits W143 to W147 and the owner's decision | @buenhyden |

### Remaining Conditions

W143 to W147 move their role groups. The comparison baseline is resolved
only by a later export that conforms for every bound role.

## Handoff

### Promotion Receipt

The Registry, the tracked core and its schema, `template_definition.py` and
the contracts check hold the binding. The documentation protocol lists the
role design contract as a version object.

### Next Owner

The implementer owns W143 to W147. The owner decides criterion 137.
