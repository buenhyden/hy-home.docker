---
title: "v14.7 W05 Validator Alignment Task"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-14"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0064"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-14"
---

# v14.7 W05 Validator Alignment Task

## Scope

### Objective and Parent

#### Objective

Own W122/criterion 117, the v14.7 W05 run for this workspace: make the
checkers enforce the rules the W00 to W04 Tasks handed to W05 where a checker
can hold them, each with a test that fails without the change, and record a
verdict and owner for every W05 handoff left open.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [W00 v14.7 intake](tsk-0059-w00-v14-7-intake.md)
- [W01 governance](tsk-0060-w01-v14-7-governance.md)
- [Pre-W04 conformance](tsk-0062-pre-w04-conformance.md)
- [W04 SDLC and promotion](tsk-0063-w04-sdlc-promotion.md)

### Inputs and Authority

The owner's request of 2026-11-14 runs the W05 prompt of the v14.7 revision
package (`_workspace/workspace_execution_tasks_v14_7_revision_20261113_r1/`,
read as reference data). It names the remaining W05 work for this workspace:
document-level link type enforcement, removal of unreachable Incident and
Postmortem retirement entries with a reachability check, an automated
glossary-to-contract comparison, the two TemplateDefinition empty-rule gaps,
and the existing validator handoffs. TSK-0059 to TSK-0063 are completed and
accepted; this run did not repeat them.

On 2026-11-14 the owner chose, for the glossary comparison, to follow the
requirement ("요구사항대로"): an automated comparison that runs in the
repository's own tests, against the adopted contract pinned in the Registry.
The same day the owner chose tool enforcement of link types with a policy
change ("도구로 집행(정책 수정)"), with the type carried in the link title and
an untitled link staying Normative or Navigation, and asked for every
remaining W05 handoff to proceed. Later that day the owner asked for the
W00 to W04 residue to be audited and fixed against the requirements, approved
commit, push, pull request and merge, and chose three options: the
repository-vocabulary contract is versioned 1.0.0 from package label `v14.5`
and 1.1.0 with the eight SemVer terms, while Registry `schema_version` stays
the integer Registry Schema Version (D1); GOV-07 stays a review rule (D2);
the workflow contracts `sdlc.md` and `workflows.md` are a role of their own
with their own form (D3).

The request authorizes the Registry, schema, validator, test and policy text
changes named here, and this Task with criterion 117 and W122. Push, pull
request, merge and runtime operations are not authorized by it.

## Execution Log

### Work Performed

#### W05 run 2026-11-14

Started from `main` `0eaf76cc0` on branch `feat/w05-validator-alignment`.
The changes below are commits `cf690ff0c` (link types), `62b3e434b` (Registry, schema, validator and
policy text), `97a40d35c` (TemplateDefinition) and `88d9e465b` (operations
currency) on that branch, plus the record commit with this Task.

- Disposition reachability. Of the 41 governed profiles, 39 entries listed a
  status their lifecycle cannot reach (for example `requirements-package`
  listed `completed` and `cancelled`; the `requirement` lifecycle reaches
  only `draft`, `in-review` and `approved`). Such a status never occurs, so
  it never admitted a document. Each entry now lists only reachable statuses
  and the Incident and Postmortem entries are empty, so no document's
  eligibility changed. The schema gives the list its own
  `dispositionStatusList` definition; where a schema declares it,
  `registry.py` allows an empty entry and reports
  `archive-disposition-unreachable` and `archive-disposition-never-retire`.
  The never-retire rule keys on the `incident` and `postmortem` lifecycles,
  so a renamed profile is still caught. Historical Registries keep the older
  rule through their own schema.
- TemplateDefinition empty rules. The section contract gives an H2 the role
  rule and one empty rule that includes a body that is only a template
  guidance comment, and an H3 the role rule and the stand-in rule.
  `template_definition.py` gave an H2 two empty rules without the comment
  case and repeated them on every H3. It now emits the single contract rule
  on an H2 and none on an H3. The validator already treats a comment-only
  section as empty (`test_heading.py` L1112 and L1141): KEEP.
- Glossary comparison (as first committed; D1 later made the pin 1.1.0 with
  41 terms and `source_label` `v14.5`). The Registry `common.vocabulary_contract` pinned the
  adopted contract `repository-vocabulary` v14.5: source SHA-256
  `b03ae3c0…2fce`, glossary path and the 33 Term ID to Term pairs, without
  definitions. `vocabulary_contract_findings` compares the glossary's
  Repository Vocabulary rows outside code fences with it (missing,
  unregistered, renamed, reordered, wrong Contract Version, and a common ID
  under Local Extensions). The current glossary matches. Meaning stays a
  review: the contract is Korean and the glossary is an English rendering.
- Release role guard (TSK-0059 H-12). The guard matched only the profile ID
  `release`. It now rejects a profile whose ID, type, template ID or path
  pattern, or a template role whose ID, source or target path, has a
  `release` or `releases` name token. A slug such as `prereleased-notes`
  stays allowed.
- Operations currency (TSK-0063 H-W04-3). `stale-active` required a
  `reviewed_at` that no profile requires, so it never fired. It now fires for
  an active Guide, Operations Policy or Runbook whose `next_review_at` has
  passed without a `reviewed_at` on or after it, as the documentation
  protocol states. No current document sets `next_review_at`.
- Review fixes: the Release guard also reads a profile's additional path
  patterns and paths and no longer names a template `target_path`, which no
  valid role has; criterion 117, the protocol and the finding message say a
  `release` name token is rejected and other names stay a review; a
  duplicate contract Term ID is rejected; the tests now cover a Release ID
  alone, an additional path, Guide and Policy currency and a non-operations
  type. The raw-JSON `list` checks stay, as the rest of `registry.py` uses
  them. Verified after the review: every status removed from a disposition
  entry was unreachable on `main`, and no Registry revision in history has a
  `release` name token, so no historical load changes.
- Link types (commit `cf690ff0c`). The documentation protocol (3.22.0) now
  says an inline link's title carries its type, an untitled link is
  Normative or Navigation, and an `evidence` link is a commit-pinned
  `https://` URL. Link alignment reports `link-type-unknown` and
  `link-evidence-unpinned`; `LINK_TYPES` equals the Registry `link_types`
  by test. No tracked Markdown used link titles before, so no existing link
  changed meaning. Choosing the right type stays a review.
- Delegated units, each built in an isolated worktree and cherry-picked
  here after its checks: SemVer (`fc4a34ca6`): both schema version patterns
  accepted a trailing newline, now rejected; the release tag regex was
  already correct; no code compares versions, so no precedence comparator
  was added. H-W01-2 (`99625243f`): the Registry `common.common_form_contract`
  names the common-form revision (`COMMON-DOC-FORM-1/1.0.0` since
  `3f485ab34`) and `template_definition.py` reads it.
  H-W01-1 and H-W01-5 (`f13f9daa4`): the real PreToolUse hook denies a
  `main` push whatever approval claim the command carries, and lets an
  in-scope reversible edit through unasked. H-W01-4 (`2ba9bc47b`): an
  OPEN-NN ID stays an unresolved parent, and a KEEP or approval marker in
  the Registry is a schema error; both pass today as regression guards.
  H-W02-1 (`34ac206d5`): the uncalled migration-manifest subgraph, 2,289
  lines, removed after an AST and `git grep` proof that none of the 16 roots
  had a caller. H-08 (`9a56e787b`): three manifest rows without consumers and
  two missing test mappings fixed, and an empty test package removed.
- H-08 measurement: of 235 test modules, 178 run in hosted CI and 57 only
  in the local `full` profile, including every document-governance library,
  metadata, lifecycle and hook-rule test; `check-document-links.py` is
  local-only too. Of 311 other code files none is dead: 86 are documented
  operator commands and 67 run at runtime. Hosted CI wiring is W06's
  (H-W05-1).
- OPEN-11: the `Resolves` cell is now at SPEC-0204 TSK-0011 L1307. It names
  the L1306 metadata and document-library exit-124 FAIL, but the PASS ran the
  supply and integrity leaves, a different guarantee, and the Task itself
  says so at L335. The FAIL stays unresolved; criterion 17 is still
  `pending`, so nothing accepted relied on it. TSK-0011 is not edited here.
- Review of the integrated branch (FAIL, three Important): I-1, I-2, M-1 and
  M-9 in the Spec Package reader went back to their writer; I-3, Plan
  restatements left at SPEC-0204 L325-329, L532 and L722-725 and SPEC-0218
  L104-110, went back to the Plan writer. Fixed here: the readiness report
  survives a load failure (`e34801578`); the link-title check reads whole
  paragraphs, bracketed link text and reference definitions, and the
  protocol says it runs locally only (`33188136f`); the KEEP-marker test
  names its schema error; the source hash rejects a trailing newline; the
  glossary calls `v14.5` a package label. M-6: the eight 1.1.0 terms come
  from the v14.7 `SEMVER-POLICY.md` section 6 (SHA-256
  `921d2fba…c06c`), which the Registry `source_sha256` (the `v14.5`
  vocabulary file) does not cover; 1.1.0 is this workspace's adoption on D1,
  and the other three workspaces adopt it themselves (W11 checks adoption).
- Review fixes returned (`91663f1f9`): a decision row is re-checked when a
  row it cites or its live Plan pairs change (I-1); Promotion targets match
  by full path, a bare name only when unique (I-2); cancelled Tasks' receipts
  count for nothing (M-9); a git-fixture test runs the real gate route
  (M-1). The remaining Plan restatements were replaced by Task links
  (`3e8fc2cd0`). Two protocol lines that `check-operations-catalog` read as
  a Release document role were reworded (`46ff5e55c`); that checker had not
  been in this Task's local selection, and the hosted candidate caught it.
- Known limits from the re-review, each with an owner: a Registry
  generation change between base and head would re-flag older decisions
  whose cited rows are `optional` (N-2, the next generation's migration
  owner); Q-07 renumbering changes the identities the comparison keys on,
  so the Q-07 rehearsal must map old to new identities (N-3, DOC-12 and
  Q07); a changed PASS row the decision does not cite escapes the
  comparison, bounded by the completion check that needs a PASS for every
  pair (N-4, review); prose such as `(see [x](y) (note))` could read as a
  link titled `note` (N-6, none in the corpus today, review).
- Readiness entrypoint (`e34801578`): `check-document-corpus-lifecycle.py
  --readiness` reports each package without changing the exit code. On the
  current tree SPEC-0248, 0249, 0250, 0260, 0264 and 0265 report ready,
  exactly the H-W04-7 removal list for W02. This corrects TSK-0057 L245,
  which said no CLI or gate derives readiness.
- Pre-W05 items done now: TSK-0063 H-W04-8 and H-W04-9, the glossary
  entries for Structural Ownership, Constraint, Change Impact, the
  Traceability heading and the older sense of "promote" (`85d6c39db`).
- Policy text now states the enforcement that exists: the documentation
  protocol (3.21.0) for the disposition and Release rules, and the glossary
  Provenance (0.6.1) for the comparison.

#### W00 to W04 conformance audit 2026-11-14

On the owner's request of 2026-11-14 a fresh-context rules-engineer audited
W00 to W04 against the r1 revision prompts and contracts, reading files
rather than Task prose. This is the r1 delta assessment for W00 to W03,
which TSK-0058 to TSK-0060 ran against the earlier package. Nothing in W00
to W04 blocks W05. Findings and actions:

| Finding | Class | Action |
| --- | --- | --- |
| SemVer 0.y.z rule absent from the protocol | CONFLICT | Fixed: the protocol states it (`265a49a3c`); no checker compares version increments, so the rule is held by review |
| Version-object inventory absent | MISSING | Fixed: protocol `Version objects` (`265a49a3c`) |
| `v14.5` written as a contract version, integer `schema_version` without a SemVer mapping | CONFLICT | Fixed on D1 (`8875aa404`): contract 1.1.0 with `source_label` `v14.5`, SemVer required by the schema; `schema_version` recorded as the integer Registry Schema Version |
| Eight SemVer terms (Public Contract to Baseline Namespace) absent from the glossary | MISSING | Fixed on D1 (`8875aa404`): common rows at 1.1.0, pinned in the Registry |
| Common form revision serialized `COMMON-DOC-FORM-1 1.0.0`, shared contract writes `COMMON-DOC-FORM-1/1.0.0` | CONFLICT (QA-C01) | Fixed (`3f485ab34`) |
| SPEC-0204 Plan restates Task status (SDLC-04, `sdlc.md` L75-77) | CONFLICT | Fixed in the SPEC-0204 and SPEC-0218 Plans (`9270ffcbd`, cherry-picked); sentences that state a rule, such as "remains NOT_RUN unless separately authorized", were kept as rules |
| Writers: TSK-0063 wrote the Registry, schema and `registry.py`; this Task wrote the glossary and Registry pins | CONFLICT (process) | Attested here: for those hunks TSK-0063 acted as the W03 writer and this Task as the W01 and W03 writer, one writer per file at a time; no other wave wrote them |
| DOC-08 DEFER in TSK-0058 has no owner | MISSING (owner) | Closed on its recorded basis (TSK-0058 L114): the facts there hold, no change needed |
| Skill Gates bullets held in TSK-0058 L444-446 | MISSING (owner) | W07, with the Skill `Completion and Handoff` section |
| W05-built fixes for W00 to W04 handoffs had no review row | UNREVIEWED | An independent review of the integrated branch is required before criterion 117 is accepted |
| H-W01-6 (GOV-07) left review-only | UNCONFIRMED | Confirmed on D2: a review rule |
| `sdlc.md` and `workflows.md` keep a workflow form, not the Policy form | UNCONFIRMED | Confirmed on D3: a separate role; the Registry already keeps it outside the 16 common roles, so TSK-0060 "16 of 16 roles" holds |
| `sdlc.md` said the reader did not yet check the 1.9.0 rules | Stale after H-W04-1 | Fixed (`e35700381`, 1.9.1): it names what the corpus check applies and that no entrypoint runs readiness |
| Document `version` allows release values only | UNCONFIRMED | Kept: no document uses a prerelease, and SemVer format rules apply where one is used; recorded here as the decision basis |
| H-W04-7 removal of 0248, 0249, 0250, 0260, 0264, 0265 | REMAINING | W02, after the H-W04-2 promotion check |
| SPEC-DISPOSITION per-criterion depth, Stage 02 currency, OPEN-07 | UNVERIFIED | W11 |
| R147-07 SDLC and document-stage binding rows; Git cells | UNVERIFIED | Rows: W11 check; Git cells: W06 (H-09) |
| OPEN-08, OPEN-10 live operations | UNVERIFIED | W10 |
| OPEN-12; OPEN-13, OPEN-14, H-W01-3 | REMAINING | TSK-0052; W06 |
| DOC-12 Q-07 isolated rehearsal | REMAINING | W03 preparation before Q07, after W11 |

Corrections to terminal Tasks, recorded here because their bodies are
immutable: TSK-0063 L196-197 and L241 name W01 for H-W04-8 and H-W04-9,
which this Task completed (`85d6c39db`), and L261 says "H-W04-1 to H-W04-8"
where L241 says "to H-W04-9"; TSK-0059 L367 calls H-05 done while L197
lists it open, and H-05 stays UNVERIFIED here; TSK-0060 L195 "16 of 16
roles" holds only if the workflow-form decision keeps `sdlc.md` and
`workflows.md` a separate role.

#### Handoff Verdicts

| ID | Source | Verdict | Action and owner |
| --- | --- | --- | --- |
| Disposition entries and reachability | TSK-0062 | PASS | Done here |
| TemplateDefinition empty rules | TSK-0062 | PASS | Done here; enforcement KEEP |
| Glossary comparison | TSK-0062, H-W01-4 | PASS (structure) | Done here; meaning is a review. It runs in `test_registry`, in the local-only `leaf.document-governance-library-regressions`; hosted CI wiring is W06's |
| H-12 Release guard | TSK-0059 | PASS | Done here for `release` name tokens; other names and a generator are checked by review |
| H-W04-3 `stale-active` | TSK-0063 | PASS | Done here |
| Document-level link types | TSK-0062 | PASS | Owner chose tool enforcement on 2026-11-14; done here (title marker, untitled default); choosing the type stays a review |
| Reverse lookups and Change Impact derivation | TSK-0062 | PASS (W123, criterion 118) | `relation_lookup` and the report-only `check-document-links.py --impact`; telling an untitled navigation link from a normative one stays a review |
| `template_roles[*].consumer_paths` manual reverse lookup | TSK-0062 | PASS (W123, criterion 118) | Owner 2026-11-14: as the W05 prompt's TemplateDefinition contract writes it, an enumeration of consumers found, where a `role:` token is not file evidence; `test_registry` requires each entry to be a tracked file; whether each still reads the role is review (13 entries name neither the role, its source nor its profiles) |
| H-W04-1 acceptance rules | TSK-0063 | PASS | `fc639081c`: applied by the corpus lifecycle check to Criterion Acceptance rows new or changed against the lifecycle base, so the 8 criteria accepted before 1.9.0 in six Tasks stand as recorded; merged-PR-note fixture included |
| H-W04-2 promotion check | TSK-0063 | PASS (code-span targets) | `ef049ad37`, `91663f1f9`: full-path match in non-cancelled receipts, reported by `--readiness` (`e34801578`); prose targets stay with review; CI route is W06's |
| H-W04-4 untested branches | TSK-0063 | PASS | `4bee2c348`; the duplicate-Task message is unreachable because `_load_tasks` rejects the duplicate first |
| H-W01-4 other fixtures | TSK-0060 | PASS | OPEN ID and KEEP marker done here; merged PR read as Acceptance with H-W04-1 |
| H-W01-1, H-W01-5 | TSK-0060 | PASS | Done here for the hook layer; no hook gates a deployment command, and a transition-override `approval` string is recorded, not authenticated (both stay review) |
| H-W01-6 (GOV-07) | TSK-0060 | PASS (owner decision D2) | A review rule in `quality-standards.md`; no checker |
| H-W01-2 consumer revision check | TSK-0060 | PASS | Registry names both adopted revisions and the consumer reads them |
| H-05 H3 model in `heading.py` | TSK-0059 | PASS (KEEP) | Reassessed at `91663f1f9`: H3 is read under its parent H2 and missing, duplicate, unregistered and out-of-order subsections are rejected (`heading.py` L829-887, 33 subsection tests); empty sections fail at every level and a same-named stand-in is `body-heading-repeated`; whether a conditional H3's condition applies and prohibited prose stay review |
| H-08 unwired code and tests | TSK-0059 | PASS (measurement and manifest) | Hosted CI wiring of the 57 local-only modules, the link checker and candidate preflight is W06's (H-W05-1) |
| OPEN-11 TSK-0011 L1307 Resolves | TSK-0059 | FAIL (verdict) | Invalid: different leaves; a fresh metadata and document-library PASS is needed before criterion 17 can be accepted |
| H-W02-1 dead subgraph in `lifecycle/contract.py` | TSK-0057 | PASS | Done here |
| SemVer tests | v14.7 W05 prompt | PASS | Done here; no comparator, since nothing orders versions |
| H-W04-8, H-W04-9 glossary entries | TSK-0063 | PASS | Done here before W05 closes |

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0064 | draft | ready | #w05-run-2026-11-14 |
| SPEC-0212-TSK-0064 | ready | in-progress | #w05-run-2026-11-14 |

### Blockers and Decisions

- Link types: the owner's 2026-11-14 choice replaced the protocol rule that
  no link carries a marker; the title is the marker and untitled links keep
  their meaning, so about 8,600 existing links were not retyped.
- H-W05-1, handed to W06 with one writer: wire into hosted CI the local-only
  leaves `leaf.document-governance-library-regressions`,
  `leaf.local-document-metadata-tests`,
  `leaf.local-document-corpus-lifecycle-tests`, `leaf.local-hook-rule-tests`,
  `leaf.supply-chain-fixture-policy` and the gate and release regression
  leaves, plus `check-document-links.py` (`leaf.docs-traceability`) and
  `check-candidate-preflight.sh`, sharded or in their own job because the
  `candidate-quality` job's 30-minute limit is below the 45-minute
  document-governance leaf; and a `leaf.project-registration` route for
  `check-project-registration.py`. Until then every W05 check above is
  local-executed evidence.
- The glossary comparison pin is identity, version, hash and Term pairs only,
  so the glossary stays the single meaning owner.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Disposition RED | 117 | W122 | red-green-proof | New `DispositionReachabilityTests` against `0eaf76cc0` code and Registry, Python 3.12 local | FAIL | 39 entries with unreachable statuses; no never-retire finding | required | - |
| Disposition GREEN | 117 | W122 | red-green-proof | `test_registry` and `test_relations` on the uncommitted tree | PASS | 148 tests OK, including the historical Registries at `2bba11baa`, `8b85e88fe` and `73b1705b6` | required | Disposition RED |
| TemplateDefinition RED | 117 | W122 | red-green-proof | Updated `test_sections_carry_their_role_prohibited_content` against the `0eaf76cc0` deriver | FAIL | 22 subtests: 3 rules where the contract has 2 | required | - |
| TemplateDefinition GREEN | 117 | W122 | red-green-proof | `test_template_definition` and `metadata.test_heading` on the uncommitted tree | PASS | 115 tests OK | required | TemplateDefinition RED |
| Vocabulary RED | 117 | W122 | red-green-proof | New `VocabularyContractTests` before `vocabulary_contract_findings` existed | FAIL | 8 errors: no such function | required | - |
| Vocabulary GREEN | 117 | W122 | red-green-proof | `test_registry`, `test_relations`, `test_template_definition` on the uncommitted tree | PASS | 177 tests OK | required | Vocabulary RED |
| Currency RED | 117 | W122 | red-green-proof | New `OperationsCurrencyTests` against the `0eaf76cc0` rule | FAIL | 2 failures: `stale-active` never fired | required | - |
| Currency GREEN | 117 | W122 | red-green-proof | `metadata.test_lifecycle`, `test_reference`, `test_profile` on the uncommitted tree | PASS | 53 tests OK | required | Currency RED |
| Release RED | 117 | W122 | red-green-proof | New `ReleaseRoleGuardTests` against the `0eaf76cc0` guard | FAIL | 5 failures: renamed roles raised other findings, not `retired-profile` | required | - |
| Release GREEN | 117 | W122 | red-green-proof | `test_registry`, `test_relations`, `test_template_definition` on the uncommitted tree, after a misplaced template-role loop was moved out of the profile loop (it had made 5 path-pattern tests fail) | PASS | 181 tests OK | required | Release RED |
| W05 review | 117 | W122 | independent-review | Fresh-context code-reviewer of the uncommitted tree (read only, no tests run) | FAIL | CHANGES_REQUIRED: criterion 117 said a Release role is rejected under any name; Minor: additional path fields unchecked, a `target_path` no role can have, the ID subtest fired on the type, a stale message, Guide and Policy currency untested, duplicate contract IDs accepted, the comparison is local-only; unverified: eligibility unchanged and historical Release loads | required | - |
| W05 review fixes | 117 | W122 | red-green-proof | `ReleaseRoleGuardTests`, `VocabularyContractTests`, `OperationsCurrencyTests` after the fixes | PASS | 18 tests OK | required | - |
| W05 re-review | 117 | W122 | independent-review | Same reviewer, the fixed tree (read only) | FAIL | Every earlier finding resolved or accepted as recorded; new Important: a blank line split the Results table, so the two review rows fell outside it | required | - |
| Integrated checks | 117 | W122 | document-checks | Uncommitted tree before the review fixes, Python 3.12 local: `check-document-corpus-lifecycle`, `check-document-metadata --mode check-changed --base-ref main`, `check-document-links --mode alignment` and `--mode commands`, `check-agent-governance-contract`, `check-script-manifest`, `test_surface_ownership` | PASS | lifecycle and occupancy violations=0; metadata selected=5 violations=0; links failures=0 in both modes (908 documents, 8,623 links); governance PASS; manifest valid; 8 tests OK | required | - |
| Spec Package regression | 117 | W122 | unit-regression | `test_spec_packages` and `test_links` on the same tree | FAIL | 225 tests, 1 error: `test_reconciliation_rows_are_unique_and_append_only` loads this Task and raised `registered evidence table must be contiguous` (the blank line the re-review also found) | required | - |
| Spec Package regression rerun | 117 | W122 | unit-regression | That test with `test_registry`, `test_relations`, `test_template_definition`, `metadata.test_lifecycle` and `metadata.test_heading` on the fixed tree | PASS | 290 tests OK | required | Spec Package regression |
| W05 final review | 117 | W122 | independent-review | Same reviewer, the fixed Results table and test docstring (read only, no tests run) | PASS | Table contiguous with nine columns per row; no open finding | required | W05 review, W05 re-review |
| gstack verify | 117 | W122 | unit-regression-gstack | `gstack-checks run` on the fixed tree after the owner trusted the repo | NOT_RUN | ENV: the pregate runner needs `pytest`, which is not installed; the repository's `unittest` suites above cover the same 74 selected modules' changed tests | optional | - |
| Pre-commit | 117 | W122 | precommit-local-staged | `run-ci-precommit.sh --mode local-staged` on the staged Registry unit, then the commit hooks of the currency unit | FAIL | `ruff format` would reformat 4 changed files; later `ruff check` UP017 in `lifecycle.py` (`datetime.UTC`) | required | - |
| Pre-commit rerun | 117 | W122 | precommit-local-staged | Same route after `ruff format` on the six changed Python files and the UP017 fix; `OperationsCurrencyTests` rerun OK | PASS | exit 0; every hook passed at commits `62b3e434b`, `97a40d35c` and `88d9e465b` | required | Pre-commit |
| Link type RED | 117 | W122 | red-green-proof | New `LinkTypeTitleTests` against `88d9e465b` | FAIL | 3 failures and 1 error: no title check and no `LINK_TYPES` | required | - |
| Link type GREEN | 117 | W122 | red-green-proof | `LinkTypeTitleTests` and `check-document-links --mode alignment` at `cf690ff0c`; pre-commit local-staged exit 0 | PASS | 5 tests OK; alignment PASS, 909 documents, 8,629 links | required | Link type RED |
| SemVer RED | 117 | W122 | red-green-proof | New schema version tests in an agent worktree at `0eaf76cc0` | FAIL | 2 subtests: `1.2.3\n` and `0.1.0\n` accepted | required | - |
| SemVer GREEN | 117 | W122 | red-green-proof | `test_registry`, `test_release` at agent commit `43a3e759c`; corpus metadata check-active and lifecycle | PASS | 131 and 18 tests OK; selected=535 violations=0 | required | SemVer RED |
| Common form pin RED | 117 | W122 | red-green-proof | New `test_template_definition` tests in an agent worktree at `cf690ff0c` | FAIL | 22 subtests: the definition kept the code constant `1.0.0` | required | - |
| Common form pin GREEN | 117 | W122 | red-green-proof | Agent commit `92c869d95`: `test_registry`, `test_template_definition`, `metadata.test_lifecycle`, `test_agent_governance_ci_routing` | PASS | 272 tests OK | required | Common form pin RED |
| Approval hook RED | 117 | W122 | red-green-proof | Agent mutation: the dispatcher skipped denial on an approval claim, and a rule blocked every `tests/` edit | FAIL | 8 subtests and 1 assertion failed as intended; both mutations reverted | required | - |
| Approval hook GREEN | 117 | W122 | red-green-proof | Agent commit `f6c5396b7`, the real hook | PASS | Both tests OK | required | Approval hook RED |
| Dead subgraph removal | 117 | W122 | unit-regression | Agent commit `34ac206d5`: lifecycle suite, generation 6 and 7, surface ownership, script manifest, corpus lifecycle | PASS | 18, 39 and 8 tests OK; manifest valid; violations=0 | required | - |
| Manifest wiring | 117 | W122 | unit-regression | Agent commit `9a56e787b`: script manifest, `test_surface_ownership`, `test_script_manifest`, `test_ci_gate_plan` | PASS | 119 tests OK; manifest valid | required | - |
| Integration rerun | 117 | W122 | unit-regression | Branch after cherry-picks `fc4a34ca6` to `9a56e787b`'s pick: `test_registry`, `test_template_definition`, `metadata.test_lifecycle`, `test_agent_governance_ci_routing`, `test_release`, surface, generation 6 and 7, script manifest; metadata check-active; corpus lifecycle | PASS | 292, 47 and 59 tests OK; selected=535 violations=0; violations=0 | required | - |
| Acceptance rule RED | 117 | W122 | red-green-proof | `AcceptanceDecisionTests` against a stub `_acceptance_findings` in an agent worktree at `cf690ff0c` | FAIL | 5 of 7 failed: the expected `acceptance-unsupported` findings were missing | required | - |
| Acceptance rule GREEN | 117 | W122 | red-green-proof | Agent commits `3ebf50def` to `10bc6b249`: `test_spec_packages`, corpus lifecycle; the unscoped rule was first measured to fail 8 accepted criteria | PASS | 134 tests OK; violations=0 | required | Acceptance rule RED |
| Promotion readiness RED | 117 | W122 | red-green-proof | `PromotionReadinessTests` before `10bc6b249` | FAIL | `test_a_target_in_no_receipt_keeps_the_package_unready` missed its finding | required | - |
| Promotion readiness GREEN | 117 | W122 | red-green-proof | `PromotionReadinessTests`, `test_generation6`, `test_generation7` at `10bc6b249` | PASS | 43 tests OK | required | Promotion readiness RED |
| Form serialization RED | 117 | W122 | red-green-proof | `test_a_malformed_common_form_pin_is_rejected` with the space form added, before `3f485ab34` | FAIL | `COMMON-DOC-FORM-1 1.0.0` accepted | required | - |
| Form serialization GREEN | 117 | W122 | red-green-proof | `test_template_definition`, `test_registry` at `3f485ab34` | PASS | 176 tests OK | required | Form serialization RED |
| Vocabulary 1.1.0 RED | 117 | W122 | red-green-proof | Updated `VocabularyContractTests` before `8875aa404` | FAIL | 6 failures: `v14.5` accepted as a version, 33 terms, rows citing `v14.5` | required | - |
| Vocabulary 1.1.0 GREEN | 117 | W122 | red-green-proof | `test_registry`, `test_template_definition` at `8875aa404`; links alignment; markdownlint | PASS | 177 tests OK; PASS; 0 issues | required | Vocabulary 1.1.0 RED |
| Readiness RED | 117 | W122 | red-green-proof | `ReadinessReportTests` before `e34801578` | FAIL | `--readiness` was an unrecognized argument | required | - |
| Readiness GREEN | 117 | W122 | red-green-proof | `tests.validation.lifecycle.test_public` at the `e34801578` change; the load-failure test was added after the review and its RED was not witnessed | PASS | 5 tests OK; then the failure test OK | required | Readiness RED |
| Integrated review | 117 | W122 | independent-review | Fresh-context code-reviewer of `323891aaf..e35700381` (read only, no tests run) | FAIL | CHANGES_REQUIRED: I-1 a cited row or Plan pair could change under an unchanged decision row; I-2 Promotion targets matched by file name; I-3 Plan restatements left; nine Minor | required | - |
| Link title RED | 117 | W122 | red-green-proof | `test_wrapped_bracketed_and_reference_links_are_checked` before `33188136f` | FAIL | 5 subtests: wrapped, bracketed and reference titles unchecked | required | - |
| Link title GREEN | 117 | W122 | red-green-proof | `LinkTypeTitleTests`, `test_registry`, links alignment at `33188136f` | PASS | 6 and 153 tests OK; alignment PASS | required | Link title RED |
| Review fixes GREEN | 117 | W122 | red-green-proof | Agent commit `a1c431e06` (picked as `91663f1f9`): new I-1, I-2 and M-9 tests failed before the fix (`1 != 0`, a README name collision, `2 != 0`); M-1 proved by removing the call and by breaking the generation guard; full `test_spec_packages`, corpus lifecycle against two bases | PASS | 139 tests OK; violations=0 | required | - |
| Integrated re-review | 117 | W122 | independent-review | Same reviewer, `91663f1f9` (read only, no tests run) | PASS | I-1 to I-3 and M-1 to M-9 resolved or accepted as recorded; Minor N-1 and N-5 fixed after it, N-2 to N-4 and N-6 recorded with owners | required | Integrated review |
| Local changed gate | 117 | W122 | ci-gate-local | `run-ci-gate.py --profile changed` at `91663f1f9`, Python 3.12.3 | NOT_RUN | Fails closed by design: the local toolchain differs from hosted Python 3.14.8; the uv 3.14.8 interpreter lacks the dependencies, which were not installed | optional | - |
| Remote candidate 996 | 117 | W122 | remote-ci | PR #996 head `91663f1f9` | PASS | candidate-quality (11m23s), CodeQL, GitGuardian and triage passed; an earlier head `3e8fc2cd0` had failed candidate-quality on the two protocol lines | required | - |
| Remote candidate 996 final | 117 | W122 | remote-ci | PR #996 final head `6e57d3dc7`, merged as `5a1aa4b98` | PASS | candidate-quality (13m16s), CodeQL, GitGuardian and triage passed; main-security skipped as on every PR | required | - |
| Relation lookup RED | 118 | W123 | red-green-proof | New `RelationLookupTests` against `a8526720c` | FAIL | 6 errors (no `relation_lookup`) and 1 failure (`--impact` unrecognized) | required | - |
| Relation lookup GREEN | 118 | W123 | red-green-proof | `test_links` on the uncommitted tree; ruff format and check | PASS | 117 tests OK; ruff clean; `--impact` on the SPEC-0212 Spec reports 2 children, 72 consumers, 838 in the closure | required | Relation lookup RED |
| W123 review | 118 | W123 | independent-review | Fresh-context code-reviewer of the uncommitted tree (read only, no tests run) | FAIL | CHANGES_REQUIRED: Important, folder links never counted as consumers; a wrong path printed an empty report with exit 0. Minor: escaped titled links hid untitled ones; `--impact` skipped input-error handling; untested successors, self links and missing IDs; Resolution Links prose | required | - |
| W123 review fixes | 118 | W123 | red-green-proof | Four new `RelationLookupTests`; with the folder mapping and escape skip removed, 2 failed; restored: 9 tests OK; `--impact docs/no.md` exits 2 | PASS | Folder links reach the README; escaped links skipped; input errors exit 1; a non-document path exits 2 | required | - |
| Consumer paths RED | 118 | W123 | red-green-proof | New `test_template_role_consumers_are_tracked_files` with one entry replaced by `role:registry-reader` | FAIL | 1 failure | required | - |
| Consumer paths GREEN | 118 | W123 | red-green-proof | Same test on the real Registry | PASS | OK | required | Consumer paths RED |
| W123 re-review | 118 | W123 | independent-review | Same reviewer, the fixed tree (read only, no tests run) | PASS | Every earlier finding fixed or recorded as a limit; Minor: help text, exit-1 wording and one more limit, fixed after it | required | W123 review |
| W123 regression | 118 | W123 | unit-regression | `test_registry`, `test_links`, `test_surface_ownership` on the fixed tree; corpus lifecycle; links alignment and commands; metadata check-changed; governance contract; script manifest | PASS | 283 tests OK; violations=0; PASS; selected=4 violations=0; PASS; valid | required | - |

### Resolution Links

Disposition RED is resolved by Disposition GREEN, TemplateDefinition RED by
TemplateDefinition GREEN, Vocabulary RED by Vocabulary GREEN, and Currency RED
by Currency GREEN, and Release RED by Release GREEN. Pre-commit is resolved
by its rerun, and Link type RED by Link type GREEN. SemVer RED, Common form pin RED,
Approval hook RED, Acceptance rule RED, Promotion readiness RED, Form
serialization RED, Vocabulary 1.1.0 RED, Readiness RED, Link title RED,
Relation lookup RED and Consumer paths RED are resolved by their GREEN rows,
and the W123 review FAIL by the W123 re-review. The Integrated review FAIL is resolved by
the Integrated re-review. The W05 review and
W05 re-review FAILs are resolved by the W05 final review, and the Spec Package
regression by its rerun.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 117 | accepted | Disposition GREEN, TemplateDefinition GREEN, Vocabulary 1.1.0 GREEN, Release GREEN, Link title GREEN, Currency GREEN, SemVer GREEN, Integrated checks, Integrated re-review, Remote candidate 996 final | Owner @buenhyden accepted on 2026-11-14 in this chat, after #996 merged; hosted CI wiring of the local-only leaves stays with H-W05-1 (W06) | SPEC-0212 TSK-0064 |
| 118 | pending | - | The derivation passes its tests; the independent review, the remote candidate and the owner's acceptance remain | SPEC-0212 TSK-0064 |

### Remaining Conditions

Criterion 117 is accepted and criterion 118 is pending: the remote
candidate and the owner's acceptance remain. The UNVERIFIED rows
name their waves. Limits: a reference definition used twice, or an
angle-bracket destination with a space, can count a titled link as a
consumer, an unused titled reference definition can hide an untitled link to
the same file, and a duplicate `artifact_id` keeps the last path (the metadata
check rejects duplicates); a reviewer checks these.
Q-07 runs only after W11.

## Handoff

### Promotion Receipt

| Criterion | Work Unit | Task result | Target | Consumer update and check |
| --- | --- | --- | --- | --- |
| 117 | W122 | Disposition GREEN, Vocabulary GREEN, Release GREEN, W05 final review | `docs/99.templates/registry.json`, the profile schema, `registry.py`, `documentation-protocol.md`, the glossary Provenance (commit `62b3e434b`) | `test_registry`; Integrated checks and Spec Package regression rerun rows |
| 117 | W122 | TemplateDefinition GREEN | `template_definition.py` (commit `97a40d35c`) | `test_template_definition`, `metadata.test_heading` |
| 117 | W122 | Currency GREEN | `metadata/lifecycle.py` (commit `88d9e465b`) | `metadata.test_lifecycle` |
| 118 | W123 | Relation lookup GREEN | `.agents/governance/documentation-protocol.md` (Relations derivation, Change Impact row; commit pending) | `test_links`; links alignment |

The commits reached `main` through PR #996, merged as `5a1aa4b98` with a
merge commit, so the promotion condition (merge) is met. Acceptance row:
criterion 117, `accepted`.

### Next Owner

The current owner is @buenhyden. Resume from `main` with the two GAP rows;
W06 takes H-W05-1.
