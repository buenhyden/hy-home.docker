---
title: "Archive Occupancy, Route Citation, and Frozen Identity Execution"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
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

`validate_catalog_identity(root, base)` compares each row the change adds. It
reads the row set at the base from `git show <base>:docs/98.archive/README.md`,
skips a record already there, lists the `Source` members with `git ls-tree -r`,
and compares each member's Git mode, its bytes after the frontmatter, and its
frontmatter segments. A segment is a top-level `key:` line with the continuation
lines that belong to it, so a list value changing under an unregistered key is a
difference rather than a line the comparison never sees. Only the keys
`common.frozen_transition_fields` names may differ in value, and only
`superseded_by` may be added.

The current side is read from the filesystem rather than from `HEAD`, because the
change that moves a unit has not committed it yet when the check runs.

One defect was found by self-review after the tests were green:
`validate_retention` called `validate_retention_catalog` and
`validate_catalog_coverage` but not the new function, so the rule existed while
no registered check invoked it. The tests passed because they called the function
directly. The hook was added and
`test_the_registered_check_runs_the_comparison` now proves the wiring, which is
the guard whose absence let the omission through.

| Check | Result |
| --- | --- |
| The seven new comparison tests before the implementation | ERROR, `module ... has no attribute 'validate_catalog_identity'`, with the 15 existing catalog tests still passing |
| `python3 -m unittest` over `test_archive` | exit 0, 65 tests |
| `python3 scripts/validation/check-document-corpus-lifecycle.py` | exit 0, `violations=0`, counts unchanged, which is Behavior Contract 9 holding: both existing rows sit at the base and are not compared |
| `python3 scripts/validation/check-document-metadata.py --mode check-changed` | exit 0, merge base `f5651fba8`, `violations=0` |
| `ruff check` and `ruff format --check` on both edited files | exit 0 |

### W7: `ADR-0036` accepted and the surfaces it changes (2026-09-16, local-executed)

`ADR-0036` is `accepted` at `1.0.0`, names `ADR-0035` in `supersedes`, and restates
the rules of `ADR-0035` that survive, which is every rule except the three this
decision changes: occupancy becomes a package judgment, the route-record citation
ban reaches `operation/incident` and `operation/postmortem`, and frozen identity
becomes a machine comparison with the catalog `Source`. `ADR-0035` moved to
`docs/98.archive/superseded/02.architecture/decisions/` with `status` changed and
`superseded_by` added, and its Retention Catalog row names `ADR-0036` and the
source object `ea8623eaf04efa5b4f32d538cb3dc0e5235831e0`, the last commit where
its origin path existed. That row is the first the comparison W5 added actually
checks, because it is the first row absent from the base.

Seven text surfaces state the new rules: `REQ-0026` with a new
REQ-0026-FR-0016 for incident closure evidence and amendments to
REQ-0026-FR-0009, REQ-0026-FR-0012, REQ-0026-FR-0014, its first Constraint and
its archive-links Acceptance Criterion; the policy's Links into Stage 98, its
occupancy paragraph, its retirement verification sentence, and a new statement
that a completing change writes its evidence in the commit before the move, with
a matching item in `.agents/governance/task-checklists.md`; `AD-0030`'s link
exception; the Stage 98 README boundary section and its byte-identity sentence;
`.agents/skills/incident-response/SKILL.md`; and the Stage 02 decisions index.
Six inbound links to `ADR-0035` became identifier mentions or moved to
`ADR-0036`.

The metadata gate rejected the first attempt with
`configuration-error: requirement identity exceeds allocation high-water:
REQ-0026-FR-0016`, because the clause was written before the identity was
allocated. The `REQ-0026.FR` space now carries `high_water` 16, `next_number` 17,
and 16 in `current_issued`, which is the number `next_number` already pointed at.

A background unit run started before that allocation reported 18 failures and 68
errors naming `identity-allocation-history-incomplete`. It had read the tree
between the two edits the allocation needs, when `high_water` was 16 while
`current_issued` still ended at 15. The settled tree passes; a background check
must not overlap an edit to the state it reads.

| Check | Result |
| --- | --- |
| `python3 -m unittest` over nine governance modules, `test_identity_history` included | exit 0, 352 tests |
| `python3 scripts/validation/check-document-corpus-lifecycle.py` | exit 0, `violations=0`, `preserved=205`, one more than before this unit |
| `python3 scripts/validation/check-document-links.py --mode all` | exit 0, `documents=888 links=6685 failures=0` |
| `python3 scripts/validation/check-document-metadata.py --mode check-changed` | exit 2 before the allocation, then exit 0, `selected=14 violations=0` |

The criterion 6 sweep ran `git grep -n` over `docs` and `.agents`, excluding the
three retention classes, for the replaced occupancy rule
(`until the package migrates`, `cannot be marked .completed. where it stands`),
the unqualified citation exception (`may cite an archive path directly`,
`archive 경로를 직접 인용할 수 있는 것은`) and `byte-identical`. Occupancy returned
nothing, but both of its patterns were English while the rule is also stated in
Korean, so that result measured the patterns rather than the corpus; the W8 entry
records the two surfaces it missed and their correction. Citation returned one
line, the sentence this unit kept and qualified in the next clause. `byte-identical` returned eight lines, judged one by one: the
`REQ-0026` first Constraint was a genuine remaining statement and now defers to
REQ-0026-FR-0012; `ADR-0036` names it twice while describing the rule it
replaces; the SPEC-0178 Overview does the same; RES-0096 carries it as dated
evidence that is not rewritten; one Stage 90 research pack uses the word in an
unrelated domain; and one sealed Migration is never edited.

### W8: completion gate, independent review, corrected sweep (2026-09-16, local-executed)

The changed profile ran as the pre-commit gate of the W7 commit `b3807ab67`,
where `.pre-commit-config.yaml` binds `public-validation-changed` to
`python3 scripts/validation/run-ci-gate.py --profile changed`; that run reports
`Public validation suites (changed) ... Passed`. A later standalone run of the
same command on the clean tree also exited 0, and it is recorded here as vacuous
rather than as evidence: for a local caller `collect_changed_paths` reads only
uncommitted work, so a clean tree yields no changed path. Reproduced through
`select_public_suites`: the clean tree selects one suite, `repository-integrity`,
and no document gate, while the W7 path set selects five suites and the three
document gates `local.document-corpus-lifecycle`, `leaf.repo-document-metadata`
and `leaf.document-lifecycle-regressions`. Only the commit-time run is evidence
for criterion 7. The other six commits were created through the same hook path,
which blocks a commit on failure, but their logs were not captured in this
session, so that is an inference and not an observation.

An independent exact-diff review of `f5651fba8..b3807ab67` returned five items.
Accepted and corrected here: `AD-0030:91` still stated the replaced per-document
occupancy rule in Korean; `docs/02.architecture/README.md:45` still listed the
moved `ADR-0035` inside a `text` fence, where the link checker cannot see it; and
Behavior Contract 7 was tested on two of its four cases, with no test for a key
reordering or for a value change under an unregistered key. Recorded and
deferred: the mode comparison reads the filesystem execute bit rather than the
Git mode, which cannot fire while `core.fileMode=true` and no archive member is
executable or a symlink; and non-retroactivity is expressed as absence from the
base's index rather than as a fixed cut-off, so a base older than `f5651fba8`
would surface the SPEC-0177 difference, which matches the intent of Behavior
Contract 9 but not its absolute phrasing.

That occupancy finding showed the W7 sweep had measured its own patterns: both
were English while the rule is also stated in Korean. A bilingual re-sweep over
`docs` and `.agents`, excluding the four retention classes and the two route
dispositions, found one further survivor, `REQ-0026:147`, now corrected. The
re-sweep returns two occupancy hits and nine byte-identity hits, each of them
either this package naming the rule it replaces or dated Stage 90 evidence that
is not rewritten.

The two new Contract 7 tests were added to behavior that was already correct, so
passing proved nothing by itself. Each guard was neutralized in turn and its test
re-run: with the reorder comparison replaced by `if False` the reorder test exits
1, and with `if key in free` replaced by `if True` the unregistered-value test
exits 1. The module was restored and compared afterwards, `restored_identical:
True`.

While this unit ran, a concurrent session staged twenty-one infrastructure
changes into the shared worktree at 16:03:59, a domain and certificate migration
already applied on another server. They are not this Task's changes and this Task
does not commit them. Because the changed profile collects uncommitted work, the
missing `DEFAULT_CERT_DIR` broke its Compose validation; on the owner's
instruction that variable was applied to the local `.env`, which `.gitignore:56`
excludes, so no tracked file changed.

| Check | Result |
| --- | --- |
| `python3 -m unittest` over four governance modules | exit 0, 243 tests |
| `python3 scripts/validation/check-document-corpus-lifecycle.py` | exit 0, `violations=0`, `preserved=205` |
| `python3 scripts/validation/check-document-links.py --mode all` | exit 0, `documents=888 links=6691 failures=0` |
| `python3 scripts/validation/check-document-metadata.py --mode check-changed` | exit 0, `selected=15 violations=0` |
| `ruff check` and `ruff format --check` on the changed test module | exit 0, already formatted |

## Verification Evidence

Rows are added as work units land. W1 and W2 carry no acceptance criterion and
are evidenced by their Work Log entries.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W3 | PASS: `test_stage_03_occupancy_is_judged_per_package` was written first and failed first, and now admits a `completed` Task in an unfinished package while rejecting a `cancelled` Task, a terminal Spec, and a terminal Plan; the Stage 02 per-document case stays covered by `test_active_stages_hold_no_terminal_document` | [test_archive.py](../../../../tests/lib/document_governance/test_archive.py) |
| 2 | W4 | PASS: `test_route_records_are_closed_to_every_source` was written first and failed first at the two exempt profiles against both route dispositions, and `test_every_source_profile_against_every_disposition_and_the_index` runs each of the four source kinds against each of the six dispositions and the index | [test_links.py](../../../../tests/lib/document_governance/test_links.py) |
| 9 | W6 | PASS: `test_resolved_incident_requires_a_closure_date` was written first and failed first, and now accepts `mitigated` without the key, rejects `resolved` with the key absent, null, or empty, and accepts `resolved` with a date-time value | [test_registry.py](../../../../tests/lib/document_governance/test_registry.py) |
| 3 | W5 | PASS: the Git-fixture tests prove Behavior Contracts 6 to 8 against a unit added over the base. A lifecycle-field difference with an added `superseded_by` passes; an added body line and a changed line ending each report `catalog-source-body-differs`; an added and a removed frontmatter key each report `catalog-source-frontmatter-differs`; a mode change reports `catalog-source-mode-differs`; a member-set difference reports `catalog-source-members-differ`; and a missing object stays `catalog-source-object-invalid` through `test_source_object_must_exist_with_the_unit_type`; a key reordering and a value change under an unregistered key each report `catalog-source-frontmatter-differs`, and each of those two guards was proved by neutralizing it and watching only its own test fail | [test_archive.py](../../../../tests/lib/document_governance/test_archive.py) |
| 5 | W3 | PASS: the corpus lifecycle run reports `violations=0` with unchanged counts after occupancy became a package judgment, and `validate_active_stage_occupancy` returns `()` on the repository | [check-document-corpus-lifecycle.py](../../../../scripts/validation/check-document-corpus-lifecycle.py) |
| 5 | W4 | PASS: the link run reports `failures=0` after the boundary closed route records to every source profile | [check-document-links.py](../../../../scripts/validation/check-document-links.py) |
| 5 | W5 | PASS: the corpus run reports `violations=0` with the comparison live, and both rows written before it stay outside it under Behavior Contract 9, each measured by hand in the W5 entry | [check-document-corpus-lifecycle.py](../../../../scripts/validation/check-document-corpus-lifecycle.py) |
| 5 | W6 | PASS: the corpus and metadata runs report `violations=0`; no tracked Incident record exists, so the new requirement rejects nothing today | [check-document-metadata.py](../../../../scripts/validation/check-document-metadata.py) |
| 5 | W7 | PASS: the corpus run reports `violations=0` with `preserved=205`, and the `ADR-0035` row is the first row the comparison actually checks, differing from its `Source` only in `status` and an added `superseded_by` | [98.archive README](../../../98.archive/README.md) |
| 6 | W7 | PASS: in one result tree `ADR-0036` is `accepted` with `supersedes` naming `ADR-0035` and its surviving rules restated, `ADR-0035` is preserved under `superseded/` with its catalog row and six inbound links repointed, seven text surfaces state the new rules, and a bilingual re-sweep at W8, run after the English-only sweep missed `AD-0030:91` and `REQ-0026:147`, leaves the replaced occupancy and byte-identity rules stated on no surface except where this package describes what it replaces | [documentation-protocol.md](../../../../.agents/governance/documentation-protocol.md) |
| 7 | W8 | PASS: the changed profile ran as the pre-commit gate of `b3807ab67`, the commit holding every content change, and reported `Public validation suites (changed) ... Passed`, with the W8 entry recording both why a later standalone run on the clean tree is not evidence and that the hosted run on the integration commit is the evidence for the completing tree | [run-ci-gate.py](../../../../scripts/validation/run-ci-gate.py) |
| 8 | W8 | PASS: an independent exact-diff review of `f5651fba8..b3807ab67` reported five items, three accepted and corrected at W8 together with one further surface the corrected sweep found, and two recorded as deferred limits with their reasons; none fell outside the recorded authorization | [test_archive.py](../../../../tests/lib/document_governance/test_archive.py) |
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
