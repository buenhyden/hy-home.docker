---
title: "v14.7 W05 Validator Alignment Task"
version: "0.1.0"
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
remaining W05 handoff to proceed.

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
- Glossary comparison. The Registry `common.vocabulary_contract` pins the
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
  names `COMMON-DOC-FORM-1 1.0.0` and `template_definition.py` reads it.
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
- Pre-W05 items done now: TSK-0063 H-W04-8 and H-W04-9, the glossary
  entries for Structural Ownership, Constraint, Change Impact, the
  Traceability heading and the older sense of "promote" (`85d6c39db`).
- Policy text now states the enforcement that exists: the documentation
  protocol (3.21.0) for the disposition and Release rules, and the glossary
  Provenance (0.6.1) for the comparison.

#### Handoff Verdicts

| ID | Source | Verdict | Action and owner |
| --- | --- | --- | --- |
| Disposition entries and reachability | TSK-0062 | PASS | Done here |
| TemplateDefinition empty rules | TSK-0062 | PASS | Done here; enforcement KEEP |
| Glossary comparison | TSK-0062, H-W01-4 | PASS (structure) | Done here; meaning is a review. It runs in `test_registry`, in the local-only `leaf.document-governance-library-regressions`; hosted CI wiring is W06's |
| H-12 Release guard | TSK-0059 | PASS | Done here for `release` name tokens; other names and a generator are checked by review |
| H-W04-3 `stale-active` | TSK-0063 | PASS | Done here |
| Document-level link types | TSK-0062 | PASS | Owner chose tool enforcement on 2026-11-14; done here (title marker, untitled default); choosing the type stays a review |
| Reverse lookups and Change Impact derivation | TSK-0062 | GAP | No tool derives them; W05 next unit, CLI wiring to W06 |
| `template_roles[*].consumer_paths` manual reverse lookup | TSK-0062 | GAP | Same unit as the reverse lookups |
| H-W04-1 acceptance rules, H-W04-2 promotion check, H-W04-4 untested branches | TSK-0063 | GAP | W05 next unit |
| H-W01-4 other fixtures | TSK-0060 | PASS | OPEN ID and KEEP marker done here; merged PR read as Acceptance with H-W04-1 |
| H-W01-1, H-W01-5 | TSK-0060 | PASS | Done here for the hook layer; no hook gates a deployment command, and a transition-override `approval` string is recorded, not authenticated (both stay review) |
| H-W01-6 (GOV-07) | TSK-0060 | GAP | No deterministic checker: a tests-only change is often legitimate; stays a review rule in `quality-standards.md` |
| H-W01-2 consumer revision check | TSK-0060 | PASS | Registry names both adopted revisions and the consumer reads them |
| H-05 H3 model in `heading.py` | TSK-0059 | UNVERIFIED | W03 added H3 checks after H-05 was written; reassess before changing |
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

### Resolution Links

Disposition RED is resolved by Disposition GREEN, TemplateDefinition RED by
TemplateDefinition GREEN, Vocabulary RED by Vocabulary GREEN, and Currency RED
by Currency GREEN, and Release RED by Release GREEN. Pre-commit is resolved
by its rerun, and Link type RED by Link type GREEN. SemVer RED, Common form pin RED and
Approval hook RED are resolved by their GREEN rows. The W05 review and
W05 re-review FAILs are resolved by the W05 final review, and the Spec Package
regression by its rerun.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 117 | pending | - | This run's rules pass their checks and review; the GAP, PARTIAL, UNVERIFIED and CONFLICT handoff rows and the owner's decision remain | SPEC-0212 TSK-0064 |

### Remaining Conditions

The GAP, PARTIAL, UNVERIFIED, CONFLICT and NOT_SELECTED rows under Handoff
Verdicts stay with this Task. The link-type CONFLICT needs the owner's choice.
Q-07 runs only after W11.

## Handoff

### Promotion Receipt

| Criterion | Work Unit | Task result | Target | Consumer update and check |
| --- | --- | --- | --- | --- |
| 117 | W122 | Disposition GREEN, Vocabulary GREEN, Release GREEN, W05 final review | `docs/99.templates/registry.json`, the profile schema, `registry.py`, `documentation-protocol.md`, the glossary Provenance (commit `62b3e434b`) | `test_registry`; Integrated checks and Spec Package regression rerun rows |
| 117 | W122 | TemplateDefinition GREEN | `template_definition.py` (commit `97a40d35c`) | `test_template_definition`, `metadata.test_heading` |
| 117 | W122 | Currency GREEN | `metadata/lifecycle.py` (commit `88d9e465b`) | `metadata.test_lifecycle` |

The commits are on branch `feat/w05-validator-alignment` only: no push, pull
request or merge is authorized, so the promotion condition (merge) is not
met. Acceptance row: criterion 117, `pending`.

### Next Owner

The current owner is @buenhyden. Resume on branch
`feat/w05-validator-alignment`: the owner's choice on the link-type CONFLICT,
then the GAP rows; a push and pull request need the owner's authorization.
