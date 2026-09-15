---
title: "Archive Disposition Enforcement Execution"
version: "0.4.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0177-TSK-0001"
parent_ids:
- "SPEC-0177"
- "SPEC-0177-PLAN-0001"
created: "2026-09-15"
---

# Archive Disposition Enforcement Execution

## Objective

Record the execution of SPEC-0177: the change that applied the Stage 98
disposition model to governance, and each later integration that moves a
registered check onto it.

## Inputs

- Operator request of 2026-09-15 supplying the Stage 98 disposition text and the
  archive link rule, with three decisions taken the same day. `ADR-0038` and
  `Spec 0079` in the supplied text are mapped to the next issued identifiers,
  `ADR-0035` and `SPEC-0177`, because neither identifier exists here. The model is
  applied in stages: governance text now, validators under this package. Sealed
  Tombstones and Migrations keep their recorded form, and only records created
  after acceptance take the new contract.
- Authorization: local edits, commits, integration into `main`, push, and branch
  and worktree cleanup. A pull request is the default route to `main` under
  `.agents/governance/github-governance.md`; the operator directed a direct
  push, which GitHub reports as a rule bypass and this Task records as such.
- Position is read from Git: `git rev-parse --abbrev-ref HEAD`,
  `git rev-parse HEAD`, and `git log --oneline origin/main..HEAD`.

## Work Log

### W1: The model applied to governance, and the checks that lag it (2026-09-15, local-executed)

The operator supplied the Stage 98 model as text and asked for it to be applied
to the archive's governance, structure, policy and rules. Three facts about the
text were measured before any edit, and each was put to the operator as a
decision rather than resolved by guess.

The text names `ADR-0038` and `Spec 0079`. Neither exists here: the Registry's
`adr` identity space stood at high water 34 and `spec` at 176, and no commit on
any ref mentions `ADR-0038` or `Retention Envelope`. The operator chose the next
issued identifiers, so `ADR-0035` holds the decision and this package holds the
validator move.

The text also contradicts six registered contracts. The operator chose to apply
it in stages: the policy, the Stage 98 README, `REQ-0026`, `AD-0030` and the
knowledge members state the model now, with a transition paragraph naming each
check that lags, and this package moves the checks. The third decision keeps
every sealed Tombstone and Migration in the form it was written in.

| Contract | Where it is enforced | Model |
| --- | --- | --- |
| Links from outside Stage 98 | `links.py` `_CITABLE_ARCHIVE_PREFIX` admits only `completed/` and the index | Also `resolved/` |
| Tombstone sections | `archive.py` requires `Recovery Commit`; the template carries it | No recovery commit |
| Tombstone pairing | `archive.py` reports a `retired/` body with no Tombstone and a Tombstone on a `completed/` or `superseded/` record | No pairing |
| Migration sections | Registry requires `Path Mapping` and `Recovery` | Moved scope and current owner |
| `resolved/` subtree | `load_archive` admits only the registered preservation subtrees, so creating it fails the loader | A retention class created with its first record |
| Retention Envelope | Not defined; a Tombstone carries the withdrawal reason | Names the source Git object once |
| Git-history-only disposition | No profile registered; `REQ-0026`'s Constraint and ADR-0033 Decision 5 keep every preserved body out of Git alone | Allowed where the profile says so |

The Stage 98 README contradicted itself before this change. Its boundary section
admitted only `completed/`, and a later paragraph said an active document may
link `superseded/` bodies directly. The validator enforced the first. The
rewrite removes the second.

The consumers the link rule's transition clause enumerates were measured over
every tracked Markdown file and `llms.txt` with `build_document_graph`. Outside
Stage 98 there were 94 links into the archive: 90 into `completed/` from 32
documents and 4 to the index from 3 documents. None pointed into `superseded/`,
`retired/`, `tombstones/` or `migrations/`. The new boundary therefore breaks no
current link, and the enumerated consumers are the 32 documents that cite
`completed/`, all of which the model admits:

- `docs/01.requirements/0023-standardize-infra-net.md`
- `docs/01.requirements/0024-agent-governance-standardization.md`
- `docs/02.architecture/decisions/0026-standardize-infra-net.md`
- `docs/02.architecture/decisions/0032-canonical-agent-governance-home.md`
- `docs/02.architecture/decisions/0033-full-spec-package-preservation.md`
- `docs/02.architecture/decisions/0034-canonical-knowledge-and-prompt-surfaces.md`
- `docs/02.architecture/descriptions/0026-standardize-infra-net.md`
- `docs/03.specs/0176-stale-fact-convergence/spec.md`
- `docs/03.specs/0176-stale-fact-convergence/tasks/tsk-0001-stale-fact-convergence.md`
- `docs/03.specs/README.md`
- `docs/05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/guide.md`
- `docs/05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/policy.md`
- `docs/05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/runbook.md`
- `docs/05.operations/catalog/00-workspace/0008-new-service-onboarding/guide.md`
- `docs/05.operations/catalog/00-workspace/0009-release-management/runbook.md`
- `docs/05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/README.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0002-agent-model-selection.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0004-automation-pipeline-workflow.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0005-docker-compose-infrastructure.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0008-harness-engineering.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0010-loop-engineering.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0012-provider-implementation-comparison.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0015-scope-application-matrix.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0017-security-governance.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0019-verification-validation.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0020-workspace-baseline.md`
- `docs/90.references/research/0084-github-actions-platform/README.md`
- `docs/90.references/research/0084-github-actions-platform/m0001-platform-mechanics.md`
- `docs/90.references/research/0085-workspace-engineering-main-baseline-assessment/README.md`
- `docs/90.references/research/0085-workspace-engineering-main-baseline-assessment/m0001-request-scope.md`
- `docs/README.md`

The list is dated 2026-09-15. SPEC-0176 completed later that day, and its two
entries now sit under `docs/98.archive/completed/03.specs/`, where a preserved
body's outbound links are not checked.

Writing the change exposed one guard worth recording. A bare child identifier
such as `FR-0013` in a Requirement or an active Spec is rejected by
`_BARE_CHILD_ID`, so every requirement reference here uses its full
`REQ-0026-FR-####` form.

Allocating `ADR-0035` also required one line outside the documents: the
`ADR_TO_AD` table in `tests/lib/document_governance/test_taxonomy.py` lists every
decision identity with its parent Description, and the test failed with
`ADR-0035` missing until the row naming `AD-0030` was added. The Registry's
`adr` and `spec` identity spaces moved to 35 and 177, and `REQ-0026.FR` to 15
for the three new functional requirements.

### W2: The four Open Questions answered, and the Spec put to review (2026-09-15, local-executed)

The operator asked for SPEC-0177 to be reviewed and taken forward. Reviewing it
showed that nothing past W2 could start in this integration. The Spec is
`draft`, each document admits one transition per integration, and
`_validate_execution_states` in `spec_packages.py` requires an `active` Spec for
an `active` Plan or an `in-progress` Task. Implementation therefore waits for
the Spec to reach `active`, which is two integrations after this one.

The four Open Questions were design choices, so they went to the operator with
a recommendation each, and each recommendation was taken.

| Question | Answer | Reason it was recommended |
| --- | --- | --- |
| Where the Retention Envelope lives | A Retention Catalog table in the Stage 98 README | The operator's text calls it the catalog's envelope and routes frozen records through the index; a README table needs no change to the Stage 98 root allowlist |
| Where a withdrawn body's reason is named | In the same catalog row, as the value its class must name | A frozen body cannot be edited, and one row per record keeps every class obligation in one place a check can read |
| Which profiles are Git-history-only | None in this package | Registering one would amend `REQ-0026` and `ADR-0033` Decision 5 as well, which widens the package for a need nothing has shown |
| How acceptance treats `ADR-0033` | `ADR-0035` supersedes it and restates its full-package unit | Supersession here is whole-document, and one decision should own Stage 98 disposition |

The Spec is amended to the answers and moves from `draft` to `review`. The Plan
and this Task stay `draft`, because the governance rule adds a Plan and Tasks
only for an approved change, and advancing them now would not reach `active`
any sooner. The policy, the Stage 98 README, `AD-0030` and `ADR-0035` now say
that this package moves five of the six lagging contracts and registers no
Git-history-only profile.

### W2 continued: The approval review, and the design it forced (2026-09-15, local-executed)

The operator asked for SPEC-0177 to be taken forward on the day its Spec reached
`review`. An independent reviewer read the Spec, the Plan, the policy, the
Stage 98 README, `ADR-0035`, `REQ-0026`, `ADR-0033`, and the code the package
changes, and blocked approval with ten findings, every one a text change.

The finding that shaped the rest was that nothing said how a check tells a
record created after acceptance from a sealed one. The reviewer proposed keying
Tombstones and Migrations on identity numbers above their high water at
acceptance. That leaves preserved bodies, which carry no number, without a rule,
and a recorded cutoff is the fixed input REQ-0026-NFR-0006 excludes. The Spec
instead keys on shape and on the comparison base. A record's headings say which
contract it follows, a change that adds a record must use the new shape, and a
full-corpus run admits every tracked record in the shape it was written in. The
second choice follows from the operator's link rule, which conditions the new
boundary on both acceptance and the validator move: every new rule sits behind
one Registry switch that W7 flips in the same result tree that accepts
`ADR-0035`, so no integration makes a policy sentence false.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | high | No rule said how a check knows a record was created after acceptance | Accepted. Shape and comparison-base keying behind the `common.archive_disposition_model` switch, with the reasoning above |
| 2 | high | The catalog row's columns, unit, and `Source` validation were unstated | Accepted. Behavior Contract 7 names the columns, one row per package or standalone document, and the ancestor, origin-path, and object-type rules, and says why `Source` is the one permitted Git object |
| 3 | high | `_recorded_retirements` and `_ordinary_preserved_paths` would still fail a retired package with only a catalog row | Accepted. Both are in scope, and Behavior Contract 9 restates REQ-0026-FR-0003 for the new record |
| 4 | high | The Registry holds one section list per profile, so new shapes would reject sealed records | Accepted. `sealed_section_shapes` added, with the swap at W7 and the base condition for a sealed shape |
| 5 | high | Superseding `ADR-0033` would drop its owner transfer, atomic transition, Git-only exclusion, and handoff rules | Accepted. `ADR-0035` now restates them, and only the Tombstone pairing changes |
| 6 | medium | Landing the link boundary or `resolved/` before W7 would falsify transition sentences | Accepted. Every new rule reads the switch, and W7 changes the switch and the text together |
| 7 | medium | Removing the transition paragraph would leave `REQ-0026` clauses that mandate the pairing | Accepted. Criterion 9 names each clause and the in-place amendment route |
| 8 | medium | Three sites name the older dispositions literally, and nothing moves a closed Incident to `resolved/` | Accepted. The sites are in W6, and the missing move trigger is recorded as out of scope |
| 9 | low | The Plan mapped no work unit to a criterion and named no files | Accepted. The Plan carries the map and the files per unit |
| 10 | low | "Moves unchanged" contradicted the status change, and the lint file sat in scope while its change was deferred | Accepted. Criterion 8 uses the ADR-0031 precedent wording, and the lint exclusion is out of scope as the creating change's obligation |

The Stage 98 README said "SPEC-0177이 수락되면", which named a Spec where the
acceptance belongs to `ADR-0035`, and it now names the decision. With the
findings settled, the Spec and the Plan move to `approved` and this Task to
`ready`. W3 to W6 start when the Spec is `active`, which is the next
integration.

A second reviewer read the amended package against the code and approved it
with eight text amendments, applied before this integration.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A | high | No check was named for Behavior Contracts 4 and 6, and the hosts that would run them receive no comparison base | Accepted. The Technical Approach names `check-document-corpus-lifecycle.py` and `check-document-metadata.py --mode check-changed` with the base each passes, and W4 and W5 list those files |
| B | medium | A test reading `ADR-0035` at its active path would fail once the decision is itself superseded | Accepted. The binding finds `ADR-0035` by identity in Stage 02 or Stage 98 |
| C | medium | Criterion 9 missed text that also conditions a rule on the transition | Accepted. The policy's Retirement preconditions item 4, Tombstone scope, and "Until SPEC-0177 completes" sentence, REQ-0026's first two Constraints, and four more surfaces are named |
| D | medium | `ADR-0035` dropped "completion and supersession create no Tombstone" and the rule that frozen records are never extended | Accepted. Both are restated, and Behavior Contract 5 decides that a new-shape Tombstone may name any class's route |
| E | low | `_ordinary_preserved_paths` was in scope with no contract changing it | Accepted. Removed from scope |
| F | low | The Plan's file map was incomplete | Accepted. As A |
| G | low | The Spec said REQ-0026-NFR-0006 requires a base, which it does not | Accepted. It now says a base is not a fixed input |
| H | low | The receipt note still called the package `draft` | Accepted |

### W3: The Registry switch, and the link boundary behind it (2026-09-15, local-executed)

The operator asked for SPEC-0177 to be taken forward after the approval
integration reached `origin/main` at `d04c8cf51`. This integration moves the
Spec and the Plan to `active` and this Task to `in-progress`, and lands W3 to W6
with the switch at `transition`.

The tests came first and failed first: seven new tests ran against the
unchanged code with four failures and one import error. The switch is
`common.archive_disposition_model` in the Registry. The Registry schema closes
`common` with `additionalProperties: false`, so the key is also declared there,
as an enum of `transition` and `adopted` and a required member. The schema is
not in the Plan's W3 file list, and without it every Registry load fails.

`registry.archive_disposition_model(root)` reads the value from the Registry
under a repository root. The link and archive checks work from a root and not
from a loaded Registry, and a fixture root carries none, so absence reads as
`transition`. A value outside the pair raises instead of choosing a model.

`links.py` asks the root for the model in `check_alignment` and
`check_commands`. At `adopted`, `resolved/` joins `completed/` as a citable
target and joins the preserved prefixes whose outbound links are not checked.
At `transition`, both lists are the ones the module had before. The binding test
finds `ADR-0035` by `artifact_id` in Stage 02 or under any Stage 98 class, and
requires `accepted` or `superseded` at `adopted` and `proposed` at `transition`.

| Check | Result |
| --- | --- |
| `python3 -m unittest tests.lib.document_governance.test_links tests.lib.document_governance.test_registry` | exit 0, 147 tests |
| `python3 scripts/validation/check-document-links.py --mode all` before the change, on a stash | `documents=885 links=6655 archive_direct_links_total=61 failures=0` |
| The same command after the change | The same counts, `failures=0` |

### W6: `resolved` registered behind the switch (2026-09-15, local-executed)

W6 ran before W4 and W5 because the catalog and the withdrawal rule read the
disposition list it changes. Four tests came first and failed first: three
failures and one error.

`PRESERVED_DISPOSITIONS` now names `resolved`, and the Registry holds an
unmanaged `archive-record-resolved` profile with the shape of the other three
retention classes. `admitted_preserved_dispositions(model)` returns the full
list at `adopted` and drops `resolved` at `transition`. `load_archive` reads the
model from the root two levels above the archive and admits a `resolved/`
subtree only when it is adopted. `links.py` derives its preserved prefixes from
the same function, so the explicit adopted tuple W3 added is gone.

The Spec names three sites that listed the older dispositions literally. The
search found a fourth, the preserved Stage 02 loader in `architecture.py`.
All four read the constant now, and a test rejects the literal in any module
other than `registry.py`. `validate_preservation_boundary` rejects a sealed
Tombstone on every retention class other than `retired`, which now includes
`resolved`. No `resolved/` directory was created.

| Check | Result |
| --- | --- |
| `python3 -m unittest` over `test_archive`, `test_links`, `test_registry`, `metadata.test_reference`, `test_architecture` | exit 0, 218 tests |
| `python3 scripts/validation/check-document-corpus-lifecycle.py` before W6, on a stash, and after | Both `violations=0` and `migrations=3 tombstones=140 preserved=200 decisions=286 recovery_rows=374 violations=0` |
| `python3 scripts/validation/check-document-links.py --mode all` before and after | Both `PASS` |

After the W6 commit `a012dcae6`, on a clean tree,
`python3 scripts/validation/run-ci-gate.py --profile changed` exited
`GATE_EXIT=0` with no FAIL line other than the `AOE-CATALOG` negative markers.

### W4: The Retention Catalog check and the row a change must add (2026-09-15, local-executed)

Ten tests came first and failed first, each on a missing function. They build
a Git fixture with a source commit and a preserving commit, so every `Source`
rule runs against real objects.

`archive.validate_retention_catalog(root)` reads the table under
`## Retention Catalog` in the Stage 98 index and reports, by code, a missing
section, a wrong header or separator, a malformed row, a duplicate `Record`, a
`Record` that is not a package directory or a standalone document, a `Record`
the tree does not hold, a `Class` that differs from the `Record`'s first
segment, `Names` that are empty or, outside `retired`, carry no artifact
identifier, and a `Source` that is not one commit and path. For the source it
also checks that the path is `preserved_origin_path` of the `Record`, that
`git merge-base --is-ancestor` accepts the commit against `HEAD`, and that
`git cat-file -t` names a tree for a package and a blob for a document.
`archive.validate_catalog_coverage(root, base)` lists `docs/98.archive` at the
base with `git ls-tree` and reports each preserved unit a change adds without
its row. A new file inside a package that already has a row needs no second
row.

`archive.validate_retention(root, base)` returns nothing unless the model is
`adopted`, and `lifecycle/recovery.run` now takes the base and reports its
findings as violations. `check-document-corpus-lifecycle.py` resolves the base
with `resolve_lifecycle_base` only when the model is `adopted`, so the
transition route resolves nothing it did not resolve before. The lifecycle
equivalence test stubbed `run_recovery` with one parameter, and its stub now
accepts the base.

| Check | Result |
| --- | --- |
| `python3 -m unittest tests.lib.document_governance.test_archive tests.validation.lifecycle.test_equivalence tests.lib.document_governance.metadata.test_reference` | exit 0, 69 tests |
| `python3 scripts/validation/check-document-corpus-lifecycle.py` after W4 | exit 0, `violations=0`, and the same recovery counts as before W6 |

## Verification Evidence

No acceptance criterion is complete. Rows record each criterion and work-unit
pair as its unit lands.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W3 | PASS: the corpus link run reports the same counts and no failure before and after W3, and `test_transition_model_keeps_resolved_outside_the_boundary` proves the boundary inert at `transition` | [test_links.py](../../../../tests/lib/document_governance/test_links.py) |
| 2 | W3 | PASS: `test_adopted_model_admits_resolved_and_rejects_other_dispositions`, `test_adopted_model_keeps_the_incident_and_postmortem_exception`, and `test_resolved_body_outbound_links_are_skipped_only_when_adopted` | [test_links.py](../../../../tests/lib/document_governance/test_links.py) |
| 1 | W6 | PASS: the corpus lifecycle and link runs report the same output before and after W6, and `test_resolved_subtree_is_admitted_only_when_the_model_is_adopted` proves the loader unchanged at `transition` | [test_archive.py](../../../../tests/lib/document_governance/test_archive.py) |
| 3 | W6 | PASS: `test_resolved_is_a_registered_retention_class`, `test_resolved_subtree_is_admitted_only_when_the_model_is_adopted`, `test_resolved_record_must_not_carry_a_sealed_tombstone`, and `test_no_module_names_the_preserved_dispositions_literally` | [test_archive.py](../../../../tests/lib/document_governance/test_archive.py) |
| 1 | W4 | PASS: the corpus lifecycle run reports the same output after W4, and `test_retention_rules_are_inert_at_transition` proves the catalog rules inert at `transition` | [test_archive.py](../../../../tests/lib/document_governance/test_archive.py) |
| 4 | W4 | PASS: `RetentionCatalogTests` covers the header, one row per unit, the class match, the class value, and each `Source` rule, including an orphaned commit and a path that differs from the origin | [test_archive.py](../../../../tests/lib/document_governance/test_archive.py) |
| 7 | W4 | PASS: `test_an_added_preserved_record_needs_its_row` | [test_archive.py](../../../../tests/lib/document_governance/test_archive.py) |

## Review Evidence

### Independent review of W1 (2026-09-15, local-executed)

One reviewer, not the author, reviewed `fb29286b2` against the operator's text
and the tracked checks. It read the new policy sections, the Stage 98 README,
ADR-0035, REQ-0026, AD-0030 and this package in full, reproduced the link-graph
counts, and read the lagging code in `links.py` and `archive.py`. Disposition
`block`. The SPEC-0176 findings it also raised are recorded in that Task.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | high | `docs/README.md` still allowed citing `superseded/` bodies and described Stage 98 in the old terms | Accepted. Both passages restate the admitted targets and the two kinds |
| 2 | high | `REQ-0026`'s Constraint and ADR-0033 Decision 5 forbid leaving a body in Git alone, against the Git-history-only disposition, and neither transition note named them | Accepted. The policy, REQ-0026 and ADR-0035 name the conflict, and the Spec makes it an Open Question whose answer amends both |
| 3 | high | REQ-0026-FR-0003, FR-0008, FR-0012, NFR-0007 and the namespace acceptance criterion still read as unconditional | Accepted. The REQ-0026 transition constraint names each |
| 5 | medium | The policy said five lagging places, the README, Spec and Task four, and AD-0030 a third set | Accepted. All five surfaces now name the same six |
| 6 | medium | The transition omitted that the loader rejects a `resolved/` subtree and that `archive.py` rejects a Tombstone on `completed/` or `superseded/` | Accepted. Both are in the six, and the Spec and Plan W6 own the loader change |
| 7 | medium | The Tombstone namespace sentence stayed unconditional against create-on-first-use | Accepted. The first Tombstone's change creates the namespace, and the rest is scoped to the transition |
| 8 | medium | The policy said this Task lists the pre-acceptance consumers, and it gave only counts | Accepted. The 32 documents are listed |
| 9 | medium | The Spec added that the Envelope names the withdrawal reason and each class obligation | Accepted. The Envelope names the source Git object only, and where the reason lives is an Open Question |
| 10 | low | The policy's stage list and its citability paragraph were not in the reviewer's summary of the text | Not a defect. Both are the operator's own wording, which the reviewer saw only as a summary |
| 11 | low | The repository map called `resolved/` citable with no qualifier | Accepted. The row names what is admitted today |
| 12 | low | The incident skill said "the one profile" and named two | Accepted |
| 13 | low | Criterion 2's lint half could not be observed inside a package that never creates `resolved/` | Accepted. Criterion 2 now needs a fixture test, and the lint exclusion stays an obligation of the creating change |
| 14 | low | The authorization named direct integration and push while the GitHub governance policy makes a pull request the default | Accepted in part. The operator's direction stands, and the Spec and this Task now record that a direct push is a reported rule bypass, not the policy route |

The changed profile ran on the clean tree at `fb29286b2` before these
corrections: `python3 scripts/validation/run-ci-gate.py --profile changed`
exited `GATE_EXIT=0`, and every FAIL line was an `AOE-CATALOG` negative marker.
The corrections move the path set, so that run is not evidence for the tree they
leave.

## Commit Ledger

| Commit | Scope |
| --- | --- |
| `fb29286b2` | W1 Stage 98 model applied to governance and the package opened |
| `e7ec6e78b` | W1 review corrections naming the six lagging contracts on every surface |
| `a9a13c5f3` | W2 Open Question answers and the Spec at `review` |
| `d174fc50b` | SPEC-0176 completion, which dated this Task's consumer list |

## Rulings

- No sealed Tombstone, Migration, or frozen body is edited.
- Unexecuted checks are recorded as NOT_RUN or BLOCKED and never promoted to PASS.

## Deferred Items

| Item | Blocking input or reason |
| --- | --- |
| W4 to W8 | W4 to W6 land in this integration after W3, with the switch at `transition`; W7 and W8 take one integration each |
