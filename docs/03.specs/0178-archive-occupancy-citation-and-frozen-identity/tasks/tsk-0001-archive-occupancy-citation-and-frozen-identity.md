---
title: "Archive Occupancy, Route Citation, and Frozen Identity Execution"
version: "0.8.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-16"
layer: "specs"
artifact_id: "SPEC-0178-TSK-0001"
parent_ids:
- "SPEC-0178"
- "SPEC-0178-PLAN-0001"
created: "2026-09-16"
---

# Archive Occupancy, Route Citation, and Frozen Identity Execution

## Objective

Record the execution of SPEC-0178, from its review to its completion.

## Inputs

- Operator approval of 2026-09-16 to take SPEC-0177 and SPEC-0178 forward and to
  resolve RES-0096 item A11, which had no owner.
- Authorization: local edits, commits, and a direct push to `main` for each
  integration, as the operator chose on 2026-09-16. A pull request is the
  default route to `main` under `.agents/governance/github-governance.md`, so
  each push is recorded as a rule bypass rather than as the policy route.
- Position is read from Git: `git rev-parse HEAD` and
  `git log --oneline origin/main..HEAD`.

## Work Log

### W1: A11 added and the Spec put to review (2026-09-16, local-executed)

The draft excluded an Incident's `resolved_at` and recorded it as open. The
operator assigned it to this package, so Behavior Contract 10 and criterion 9
now require a nonempty `resolved_at` at `resolved`. The Registry already
enforces a status-conditional field for `postmortem`, where
`required_frontmatter_by_status` makes `reviewed_at` required at `published` and
rejects a null or empty value, so the requirement needs one Registry entry and
no check.

The draft's Open Question asked whether a container other than a Stage 03
package needs the `completed`-member admission. RES-0096 found none, and the
Spec now says so.

The precondition sentence said the Spec stays `draft` or `review` until
SPEC-0177 completes. That would have blocked the approval integration the
operator's sequence places before SPEC-0177's completion, and approval changes
no check, so the sentence now bars activation instead.

The Spec moves from `draft` to `review`, and this Plan and Task are added as
drafts.

### W2: The approval review and the amendments it forced (2026-09-16, local-executed)

The review ran against the three package documents and the repository state
SPEC-0177 W7 had just produced. It returned BLOCK with three high, six medium,
and two low findings. Ten were accepted and one was rejected on evidence.

The three high findings shared one shape: the package stated an obligation whose
owner or whose authorized surface it had not declared.

- Criterion 6 requires `ADR-0035`'s inbound links repointed when it moves to
  `superseded/`, but the in-scope list named none of the documents that hold
  them. `grep` over the active tree finds eight such links, six of them outside
  Stage 98, so W7 would have failed its own changed gate. The scope list and
  Plan W7 now name every active document that links `ADR-0035` by path or labels
  its status, with the current enumeration marked as the state the rule found
  rather than an expected set, which keeps REQ-0026-NFR-0006.
- Behavior Contract 10 requires `resolved_at` at `resolved`, but `ADR-0036` had
  four Decisions and none of them concerned incident closure, so a
  machine-enforced rule would have had a Stage 03 Spec as its only authority
  against REQ-0026-FR-0005. `ADR-0036` gains Decision 5 and a matching
  Consequence, and the scope list and Plan W7 name a new `REQ-0026` functional
  requirement as the Stage 01 owner, amended in the acceptance tree.
- The completion-ordering rule, that a completing change writes its final
  evidence in the commit before the move, existed only inside this Spec. After
  preservation it would be readable only from a frozen body, against the
  `REQ-0026` Acceptance Criterion that preservation rules are readable from
  `.agents/` without loading a Spec Package. The scope list and Plan W7 now name
  the policy's Retention by status section and
  `.agents/governance/task-checklists.md`.

The accepted medium and low findings were corrected in place: the undefined
"integration report" is replaced by the completing commit's own pre-commit
changed gate, which is an artifact rather than an assertion; the Plan's
recording rule is bounded to the commit that holds every content change; W1 and
W2 are stated to carry no acceptance criterion; criterion 6 names `git grep -n`
over `docs/` and `.agents/` excluding the retention classes; the Stage 98 README
byte-identity sentence joins the scope; the Plan's Dependencies state each
document's status path across the four integrations, which the registered `task`
lifecycle makes exactly `draft`, `ready`, `in-progress`, `completed`; and the
stale tense in this Spec's Traceability row and in SPEC-0177's Overview is
corrected. The `(proposed)` label for `ADR-0035` in `REQ-0026` Traceability was a
SPEC-0177 W7 residue and was corrected there.

| Finding | Severity | Disposition |
| --- | --- | --- |
| 1 Inbound links outside the declared scope | high | Accepted. Scope list and Plan W7 extended |
| 2 Behavior Contract 10 has no Stage 01 or 02 owner | high | Accepted. `ADR-0036` Decision 5 added; a `REQ-0026` requirement named in scope |
| 3 Completion-ordering rule has no canonical owner | high | Accepted. Policy and task checklist named in scope |
| 4 "Integration report" is not a defined artifact | medium | Accepted. Replaced by the completing commit's changed gate |
| 5 Plan recording rule contradicts the frozen-Task design | medium | Accepted. Bounded to the pre-move commit |
| 6 Criterion 6's completeness test is judgment | medium | Accepted. Named as a `git grep -n` run recorded in this Task |
| 7 A byte-identity statement sits outside scope | medium | Accepted. Added to scope |
| 8 The integration budget omits the Task's three-hop lifecycle | medium | Accepted. Status paths stated in the Plan |
| 9 Criterion 5 binds the package to an impossible comparison | medium | Rejected on evidence. Behavior Contract 7 already admits an added `superseded_by`, and criterion 3 already requires that case to pass. `git cat-file -p 677a6e513:docs/02.architecture/decisions/0033-full-spec-package-preservation.md` against the preserved copy differs in exactly two ways: the `status` value, which the registered field list carries, and an added `superseded_by`. The row passes as designed. The advisory to run the comparison against the real row before activation is kept as a W5 obligation |
| 10 Stale tense about SPEC-0177 and `ADR-0035` | low | Accepted. Corrected here and in SPEC-0177 |
| 11 W1 and W2 appear in no criterion row | medium | Accepted. Stated in the Plan's Verification |

A second review read the amendment surface, as SPEC-0177 did when its own
approval review needed a second round. It returned no high finding, five medium
and five low, and named three as required before approval.

| Finding | Severity | Disposition |
| --- | --- | --- |
| 1 Criterion 7 rests on an inference rather than an artifact | medium | Accepted. The completing tree's evidence is the hosted CI Quality Gates run on the integration commit, `validation-changed` for a pull request and `validation-full` for a direct push. A local hook result cannot be proven from a commit, which `.claude/provider.md` already states of hook trust |
| 2 The scope rule would rewrite a dated Stage 90 observation | medium | Accepted. The rule binds a statement of current authority, and a dated observation states what was true at its observed commit |
| 3 Criterion 8 was unbounded while criterion 7 was bounded | medium | Accepted. Criterion 8 names the content tree and what bounds the remaining delta |
| 4 This Spec's link to SPEC-0177 breaks when that package is preserved | medium | Accepted with a different owner. The breakage happens in SPEC-0177's own completion, so its Task carries the repointing as a W8 consumer cutover and this Spec's Traceability row says so |
| 5 The decisions index summary of `ADR-0036` omitted Decision 5 | medium | Accepted |
| 6 "No edge that skips a state" is false of the cancel and supersede edges | low | Accepted. The Plan says no forward edge |
| 7 The new `ADR-0036` Consequence claimed an effect on the preservation move | low | Accepted. It states the status effect only and puts the move rule outside its scope |
| 8 SPEC-0177's Overview still read as a current claim about `ADR-0035` | low | Accepted |
| 9 The scope list presupposed a policy statement that does not exist | low | Accepted. It names a new statement and a new checklist item |
| 10 Two Technical Approach sentences assert opposite Task states | low | Accepted. The first is conditional on Behavior Contract 2 |

The review had no shell and asked whether `REQ-0026` and SPEC-0177's Spec
carried version bumps for their corrections. `REQ-0026` did not: `1.5.0` was
already committed at SPEC-0177 W7, so removing the stale label needed `1.5.1`,
which it now carries. SPEC-0177's Spec did, at `1.2.2`.

With no high finding open, the Spec moves from `review` to `approved`, this Plan
from `draft` to `approved`, and this Task from `draft` to `ready`, which the
registered lifecycles make the only forward edge from each current status. No
check this package adds is live until W3.

### W3: Stage 03 occupancy judged per package (2026-09-16, local-executed)

`validate_active_stage_occupancy` read every tracked Markdown file under the five
active stage prefixes and reported any terminal status, one document at a time.
Behavior Contracts 1 to 3 make Stage 03 a package judgment and leave the other
four stages per document, so the check now groups Stage 03 paths by package and
keeps the old loop for everything else.

Package membership is read from the Registry `spec`, `plan`, and `task` path
patterns through `path_matches_pattern`, not from a second path shape written in
the check, so a pattern change cannot split the two silently. `_catalog_registry`
already exists for exactly this: it reads the repository Registry rather than one
the checked root supplies, which is what lets a fixture root carry only the
switch.

A package whose Spec is terminal keeps no member in an active stage, which is
Behavior Contract 2's closing sentence. Otherwise a terminal Spec or Plan is a
finding, a `completed` Task is admitted because a finished Task says so with its
own status while the package still moves whole, and every other terminal Task
status stays a finding.

The test was written first and failed first at the admitted case, reporting
`docs/03.specs/0001-example/tasks/tsk-0001-example.md: completed document remains
in an active stage`, which is the report this unit removes.

| Check | Result |
| --- | --- |
| The new test before the implementation | FAIL at the admitted case, an empty tuple against one finding |
| `python3 -m unittest` over `test_archive` and `test_spec_packages` | exit 0, 91 tests, including the Stage 02 per-document guard |
| `validate_active_stage_occupancy` on the repository | `()` |
| `python3 scripts/validation/check-document-corpus-lifecycle.py` | exit 0, `violations=0`, counts unchanged |
| `python3 scripts/validation/check-document-metadata.py --mode check-changed` | exit 0, merge base `f5651fba8`, `violations=0` |
| `ruff check` and `ruff format --check` on both edited files | exit 0 |

### W4: Route records closed to every source (2026-09-16, local-executed)

The archive boundary exempted `operation/incident` and `operation/postmortem`
from `active-archive-link` for every path under `docs/98.archive/`, route records
included. That exception exists to reach preserved evidence, and a route record
holds no body, so it has nothing to reach. The boundary now rejects a
route-record target before the profile exception applies, which is Behavior
Contract 4 and the whole behavioral change of this unit.

The test was written first and failed first at four subtests, the two exempt
profiles against each of the two route dispositions, each reporting an empty
finding set where the rule requires `active-archive-link`.

Criterion 2 asks for the full grid and the suite did not hold it: the six
dispositions were covered for an ordinary source, and the exempt profiles only
against `retired`. A matrix test now runs each of the four source kinds against
each of the six dispositions and the index, so Behavior Contracts 4 and 5 are
proven as stated rather than in the corner the older tests happened to cover.

| Check | Result |
| --- | --- |
| The new route-record test before the implementation | FAIL at four subtests, incident and postmortem against `tombstones/` and `migrations/` |
| `python3 -m unittest` over `test_links` | exit 0, 59 tests |
| `python3 scripts/validation/check-document-links.py --mode all` | exit 0, `documents=889 links=6688 failures=0` |
| `ruff check` and `ruff format --check` on the edited files | exit 0 |

### W6: A closure date on a resolved Incident (2026-09-16, local-executed)

The `incident` profile carried `resolved_at` as optional frontmatter and no
status-conditional rule, so a record could reach `resolved` without saying when
it closed. `resolved/` is the retention class that names its closure evidence, so
the profile now requires `resolved_at` at `resolved` through
`required_frontmatter_by_status`, which the `postmortem` profile already uses for
`reviewed_at` at `published`. That is one Registry entry and no new check, as the
Spec's Technical Approach states.

The test was written first and failed first at three subtests: the key absent,
null, and empty. The empty case reported `empty-optional-frontmatter` alone,
which is the existing rule for an empty optional value, and the registered
requirement now adds `status-frontmatter-required` beside it rather than
replacing it.

| Check | Result |
| --- | --- |
| The new test before the implementation | FAIL at three subtests, the key absent, null, and empty |
| `python3 -m unittest` over `test_registry` | exit 0, 91 tests |
| `python3 scripts/validation/check-document-corpus-lifecycle.py` | exit 0, `violations=0`, counts unchanged |
| `python3 scripts/validation/check-document-metadata.py --mode check-changed` | exit 0, merge base `f5651fba8`, `violations=0` |
| Tracked Incident records | none, so the rule rejects nothing in the corpus today |

### W5: The comparison, and the row that revealed its premise (2026-09-16, local-executed)

Before writing the comparison, the two rows the Retention Catalog already holds
were compared by hand against their `Source` objects with `git cat-file -p` and
`diff -u`.

| Row | Difference from its `Source` | Verdict |
| --- | --- | --- |
| `superseded/02.architecture/decisions/0033-full-spec-package-preservation.md` | `status` changed and `superseded_by` added, and nothing else | passes Behavior Contract 7 as written |
| `completed/03.specs/0177-archive-disposition-enforcement/` | `spec.md` differs in `version` and `status` only; `plan.md` differs in three lifecycle fields and about 42 body lines; the Task differs in two lifecycle fields and about 27 body lines | fails the comparison |

The body lines that fail are the record of the defects SPEC-0177's own completion
check forced it to fix: the `W4b` token the contract never admitted, the W1 and
W2 units that carried no receipt, and three receipt cells whose shape broke the
contract. That check returns early unless the Spec already reads `completed`, so
its findings can only arrive in the completing tree, and correcting them there is
a body change. The Technical Approach's premise, that a completing commit changes
only lifecycle fields, the move, the two index rows and consumers, therefore
cannot hold for a completion the check itself corrects.

The operator chose non-retroactive scope on 2026-09-16. The comparison covers the
rows this package adds, and a row written before it existed stays a verification
limit rather than a claim. `ADR-0036` Decision 4 already states that principle
for a preserved record without a row, so Behavior Contract 9 extends it rather
than creating an exception, criterion 5 names the bound, and the Spec's Failure
Modes table names the premise that failed. The SPEC-0177 row's difference is
recorded above rather than repaired, because a frozen body is never edited and no
commit holds those bytes at the origin path.

## Verification Evidence

Rows are added as work units land. W1 and W2 carry no acceptance criterion and
are evidenced by their Work Log entries.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W3 | PASS: `test_stage_03_occupancy_is_judged_per_package` was written first and failed first, and now admits a `completed` Task in an unfinished package while rejecting a `cancelled` Task, a terminal Spec, and a terminal Plan; the Stage 02 per-document case stays covered by `test_active_stages_hold_no_terminal_document` | [test_archive.py](../../../../tests/lib/document_governance/test_archive.py) |
| 2 | W4 | PASS: `test_route_records_are_closed_to_every_source` was written first and failed first at the two exempt profiles against both route dispositions, and `test_every_source_profile_against_every_disposition_and_the_index` runs each of the four source kinds against each of the six dispositions and the index | [test_links.py](../../../../tests/lib/document_governance/test_links.py) |
| 9 | W6 | PASS: `test_resolved_incident_requires_a_closure_date` was written first and failed first, and now accepts `mitigated` without the key, rejects `resolved` with the key absent, null, or empty, and accepts `resolved` with a date-time value | [test_registry.py](../../../../tests/lib/document_governance/test_registry.py) |
| 4 | W5 | PASS: `test_frozen_transition_fields_are_a_declared_contract` was written first and failed first with a `KeyError`, and the Registry now declares `status`, `version`, `updated` and `superseded_by` while the schema lists the key in `common.required`, so a Registry without it does not load | [test_registry.py](../../../../tests/lib/document_governance/test_registry.py) |

## Review Evidence

### Independent approval review (2026-09-16, local-executed)

Recorded in the W2 Work Log entry above, with every finding, its severity, and
its disposition. The one rejected finding carries the command that disproves it.

## Commit Ledger

| Commit | Scope |
| --- | --- |
| `24f7bb507` | W1: this package put to review with RES-0096 item A11, and this Plan and Task drafted |

## Deferred Items

| Item | Blocking input or reason |
| --- | --- |
| W3 to W7 | SPEC-0177 completed and preserved |
| W8 | One integration after W3 to W7 |
| The source comparison run against the one existing Retention Catalog row | W5, which is where `common.frozen_transition_fields` and the comparison land. Review finding 9 asked for it before activation; the row is shown by hand to differ only in the `status` value and an added `superseded_by`, both admitted, so it is an obligation rather than a block |
