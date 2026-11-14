---
title: "v14.7 W05 Validator Alignment Task"
version: "0.6.0"
type: "sdlc/task"
status: "completed"
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
| Document `version` allows release values only | CONFLICT | Fixed on the owner's 2026-11-14 choice to follow the W05 SemVer requirement (W125, #1001): full SemVer 2.0.0 accepted and compared by precedence; the earlier "Kept" was an agent judgement, not an owner decision |
| H-W04-7 removal of 0248, 0249, 0250, 0260, 0264, 0265 | REMAINING | Done in W124 (#1003, `ca5dc8f4a`); the post-merge restore passed |
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

#### Package removal 2026-11-14

Approval: on 2026-11-14 the owner, @buenhyden, approved in this chat deleting
exactly SPEC-0248, 0249, 0250, 0260, 0264 and 0265 ("6개 삭제 승인").
`check-document-corpus-lifecycle.py --readiness` reported all six `ready` on the
base `09778b761`. Each package had an approved Spec and Plan and one completed
Task, TSK-0001. W124 removes the six packages whole; no other Task body was edited. Preconditions: (1) readiness lists each
`ready`; (2) each durable meaning is in its owner, with a one-line lineage in
the Stage 01 and 02 Traceability sections (REQ-0026 and AD-0030, REQ-0024 and
AD-0027, REQ-0004, REQ-0005, AD-0004, AD-0031 and ADR-0060; the
ADR-0097 named in the request is a Blog-data ADR with no file here, so it
needed no edit); (3) the editable consumers are updated, and the links in
terminal Tasks stay as they are because the numbers are reserved; (4) the six
numbers are in the Registry Spec `reserved_history`; (5) the last commits
below are ancestors of `origin/main`. SPEC-0212 plan line 150 and
`test_operations_catalog.py` (`_current_owner` now takes SPEC-0212 in a mocked
failure test) were updated. `docs/90.references/data/0096-workspace-inventory/data.yaml`
is a dated scan (`observed_at` 2026-11-07, head `52556b386`) that lists
deleted paths; it was not hand-edited, and a regeneration needs the `_workspace`
review input that this checkout does not carry. Prose that names a retired
SPEC ID for lineage (ADRs 0037, 0044, 0051, 0060, `decisions/README.md`,
`data/README.md`, the 0251 and 0256 Tasks, code comments) stays, as the
protocol allows.

SPEC-0248: criteria 1 to 4 `accepted` (owner accepted 2026-11-12); Task TSK-0001 `completed`; Plan and Spec `approved`.

| Removed file | Last commit | Reachable from `main` |
| --- | --- | --- |
| `docs/03.specs/0248-archive-and-migration-check-retirement/plan.md` | `d18403cccb45` | yes |
| `docs/03.specs/0248-archive-and-migration-check-retirement/spec.md` | `25f280a66906` | yes |
| `docs/03.specs/0248-archive-and-migration-check-retirement/tasks/tsk-0001-archive-and-migration-check-retirement.md` | `ae4df1873b4d` | yes |

SPEC-0249: criteria 1 to 4 `accepted` (owner accepted 2026-11-12); Task TSK-0001 `completed`; Plan and Spec `approved`.

| Removed file | Last commit | Reachable from `main` |
| --- | --- | --- |
| `docs/03.specs/0249-stage98-archive-deletion/plan.md` | `d18403cccb45` | yes |
| `docs/03.specs/0249-stage98-archive-deletion/spec.md` | `25f280a66906` | yes |
| `docs/03.specs/0249-stage98-archive-deletion/tasks/tsk-0001-stage98-archive-deletion.md` | `ae4df1873b4d` | yes |

SPEC-0250: criteria 1 to 4 `accepted` (owner accepted 2026-11-12); Task TSK-0001 `completed`; Plan and Spec `approved`.

| Removed file | Last commit | Reachable from `main` |
| --- | --- | --- |
| `docs/03.specs/0250-finished-spec-package-deletion/plan.md` | `d18403cccb45` | yes |
| `docs/03.specs/0250-finished-spec-package-deletion/spec.md` | `25f280a66906` | yes |
| `docs/03.specs/0250-finished-spec-package-deletion/tasks/tsk-0001-finished-spec-package-deletion.md` | `ae4df1873b4d` | yes |

SPEC-0260: criteria 1 to 4 `accepted` (owner accepted 2026-11-12); Task TSK-0001 `completed`; Plan and Spec `approved`.

| Removed file | Last commit | Reachable from `main` |
| --- | --- | --- |
| `docs/03.specs/0260-spec-0209-0231-retirement/plan.md` | `d18403cccb45` | yes |
| `docs/03.specs/0260-spec-0209-0231-retirement/spec.md` | `25f280a66906` | yes |
| `docs/03.specs/0260-spec-0209-0231-retirement/tasks/tsk-0001-spec-0209-0231-retirement.md` | `ae4df1873b4d` | yes |

SPEC-0264: criteria 1 to 10 `accepted` (owner accepted 2026-11-13); Task TSK-0001 `completed`; Plan and Spec `approved`.

| Removed file | Last commit | Reachable from `main` |
| --- | --- | --- |
| `docs/03.specs/0264-folder-guide-delivery/plan.md` | `d18403cccb45` | yes |
| `docs/03.specs/0264-folder-guide-delivery/spec.md` | `9a0677a4321c` | yes |
| `docs/03.specs/0264-folder-guide-delivery/tasks/tsk-0001-deliver-folder-guides.md` | `89629d0240b3` | yes |

SPEC-0265: criteria 1 to 14 `accepted` (owner accepted 2026-11-11 (12 to 14) and 2026-11-13 (1 to 11)); Task TSK-0001 `completed`; Plan and Spec `approved`.

| Removed file | Last commit | Reachable from `main` |
| --- | --- | --- |
| `docs/03.specs/0265-hermes-report-source-capture/plan.md` | `d18403cccb45` | yes |
| `docs/03.specs/0265-hermes-report-source-capture/spec.md` | `68de09cc3a27` | yes |
| `docs/03.specs/0265-hermes-report-source-capture/tasks/tsk-0001-report-source-capture.md` | `6d092b6dc7ea` | yes |

Post-merge restore and byte comparison (precondition 5): `PASS` after merge
`ca5dc8f4a`; all 18 bodies restored from the commits above match byte for
byte (W124 post-merge restore rerun).

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
| H-W01-1, H-W01-5 | TSK-0060 | PASS | Done here for the hook layer; no hook gates a deployment command, and a transition-override `approval` string is recorded, not authenticated (both stay review); the owner chose on 2026-11-14 to keep deployment approval a review rule, since this repository's hooks do not run deployment commands |
| H-W01-6 (GOV-07) | TSK-0060 | PASS (owner decision D2) | A review rule in `quality-standards.md`; no checker |
| H-W01-2 consumer revision check | TSK-0060 | PASS | Registry names both adopted revisions and the consumer reads them |
| H-05 H3 model in `heading.py` | TSK-0059 | PASS (KEEP) | Reassessed at `91663f1f9`: H3 is read under its parent H2 and missing, duplicate, unregistered and out-of-order subsections are rejected (`heading.py` L829-887, 33 subsection tests); empty sections fail at every level and a same-named stand-in is `body-heading-repeated`; whether a conditional H3's condition applies and prohibited prose stay review |
| H-08 unwired code and tests | TSK-0059 | PASS (measurement and manifest) | Hosted CI wiring of the 57 local-only modules, the link checker and candidate preflight is W06's (H-W05-1) |
| OPEN-11 TSK-0011 L1307 Resolves | TSK-0059 | FAIL (verdict); DELTA | Invalid: different leaves. Owner SPEC-0204 TSK-0011, criterion 17: rerun the same metadata and document-library leaves, then rewrite the Resolves; resume when W06 runs them in hosted CI (H-W05-1) or a local Python 3.14.8 toolchain with the locked dependencies exists. The historical "11 Tasks, 7 manifest failures" counts are not carried: `check-script-manifest.py` passes today and `--readiness` lists each open Task with its owner |
| H-W02-1 dead subgraph in `lifecycle/contract.py` | TSK-0057 | PASS | Done here |
| SemVer tests | v14.7 W05 prompt | PASS (W125) | First pass here kept release-only values; the audit found that a CONFLICT and W125 (#1001) accepts full SemVer 2.0.0 with `compare_semver`; the equal-precedence release refusal is wired, and `check_version_change` for unchanged or lower versions has no caller yet: W06 commit, pull request and tag consumer |
| H-W04-8, H-W04-9 glossary entries | TSK-0063 | PASS | Done here before W05 closes |
| QA-C05 check crosswalk (QA-01, QA-17, QA-ALIGN-01) | TSK-0053, TSK-0059 | PASS (W125, #999) | `run-ci-gate.py --profile full --crosswalk`: leaves=48 unowned=42 local_only=14 unique=12 duplicates=0; every leaf declares `guarantee`. 42 leaves have no rule owner because the contract has no owner field: a W06 contract change (H-W05-1) |
| QA-C07 result reuse | W05 prompt | PASS (W125, #999 and #1002) | Registry- or policy-only diffs select the document suites (characterization); a PASS is refused on a changed source, base or lock digest and, for `security_db: grype` leaves, a changed, seeded, removed or `INVALID` Grype identity. Limits: no leaf runs real Grype, hosted CI records `ABSENT`, the binding is plan equality at `EvidenceStore.open`, and the detector is one hop |
| QA-C08 staged index | W05 prompt | PASS (existing) | `tests/validation/test_run_ci_precommit.sh`; `test_ci_gate_plan` `test_initial_repository_collects_staged_and_untracked_paths`, `test_automatic_pre_commit_sees_index_content_and_untracked_paths`; `test_agent_governance_ci_routing` `test_installed_commit_hook_checks_index_and_preserves_partial_staging` |
| QA-08, WP-26 cost baseline | TSK-0053 | PASS (baseline); WP-26 BLOCKED | Owner chose on 2026-11-14 to measure in W05: see QA-08 timing baseline. Trimming fixtures waits for the runner exit 124 diagnosis (W06, OPEN-14 and H-10) |
| DOCKER-03 QA, supply chain, release and acceptance residue | W05 prompt | DELTA | TSK-0053 L316 keeps it under TSK-0052; criteria 104 and 105 there stay pending with FAIL gates. A CI PASS, the supply-chain ledger and signatures are not rollout or final acceptance. Owner SPEC-0212 TSK-0052 (OPEN-12); rollout W10 |
| WP-23 CI and QA call graph | W05 prompt | DELTA | Closed by the QA-C05 crosswalk (#999); stage QA cells stay with W06 (H-09) |
| WP-24 stage QA and evidence reuse | W05 prompt | DELTA | QA-C07 here; stage QA cells W06 (H-09) |
| WP-25 one-off, legacy and deprecated QA | W05 prompt | DELTA | Owner SPEC-0253 TSK-0001 (in-progress): hosted CI, then criteria 1 to 3 |
| OPEN-09 checks fit contracts | W05 prompt | DELTA | H-05, H-12 and H-08 PASS here, QA-C05/C07/C08 in W125; hosted wiring of the local-only modules is W06 (H-W05-1) |
| TSK-0058 L743 validator work beyond the profile flags | TSK-0058 | PASS | Mapped to H-05 (H3 model) and H-12 (Release guard), both PASS here |

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0064 | draft | ready | #w05-run-2026-11-14 |
| SPEC-0212-TSK-0064 | ready | in-progress | #w05-run-2026-11-14 |
| SPEC-0212-TSK-0064 | in-progress | completed | #criterion-decisions |

### Blockers and Decisions

- Link types: the owner's 2026-11-14 choice replaced the protocol rule that
  no link carries a marker; the title is the marker and untitled links keep
  their meaning, so about 8,600 existing links were not retyped.
- H-W05-1, handed to W06 with one writer. The 14
  `public_gate.local_only_gate_ids`, each with this Task's recommendation:
  wire `leaf.ci-gate-adapter-regressions`, `leaf.ci-gate-runner-regressions`,
  `leaf.document-governance-library-regressions`, `leaf.docs-traceability`
  (`check-document-links.py`), `leaf.local-document-metadata-tests`,
  `leaf.local-document-corpus-lifecycle-tests`, `leaf.release-regressions`,
  `leaf.repo-contracts-control-plane-regressions`,
  `leaf.supply-chain-fixture-policy` and `leaf.workflow-contract-regressions`;
  keep local `leaf.ci-precommit-regressions` (git and pre-commit sandbox),
  `leaf.local-hook-rule-tests` (local agent hooks),
  `leaf.local-candidate-preflight` (local candidate state) and
  `leaf.conftest-policy-tests` (needs the conftest binary until a hosted tool
  image is pinned). Shard the document-governance leaf or give it its own job:
  its modules took 2,283 s locally (QA-08 baseline), above the
  `candidate-quality` job's 30-minute limit. Also: create the
  `leaf.project-registration` route for `check-project-registration.py`; add
  a rule-owner field so the crosswalk's 42 `UNOWNED` leaves get owners; call
  `release.check_version_change` from the commit, pull request and tag
  consumer; and rerun SPEC-0204 TSK-0011's two leaves (OPEN-11). Until then
  every W05 check above is local-executed evidence.
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
| W124 readiness | 119 | W124 | corpus-readiness | `check-document-corpus-lifecycle.py --readiness` on the W124 tree, six packages removed | PASS | The six packages no longer appear in the report; the owner's list was `ready` on the base before removal (TSK-0064 W05 run) | required | - |
| W124 lifecycle | 119 | W124 | corpus-lifecycle | `check-document-corpus-lifecycle.py` on the W124 tree | PASS | document corpus lifecycle violations=0; active stage occupancy violations=0 | required | - |
| W124 links | 119 | W124 | links-alignment | `check-document-links.py --mode alignment` and `--mode commands` on the W124 tree | PASS | alignment documents=891 failures=0; commands documents=891 failures=0 | required | - |
| W124 metadata | 119 | W124 | metadata-check-changed | `check-document-metadata.py --mode check-changed --base-ref origin/main` | PASS | selected=32 violations=0 | required | - |
| W124 governance and manifest | 119 | W124 | governance-contract | `check-agent-governance-contract.py`; `check-script-manifest.py` | PASS | failures=0; script manifest is valid | required | - |
| W124 ruff | 119 | W124 | lint | `ruff format --check` and `ruff check` on `test_operations_catalog.py` | PASS | 1 file already formatted; no findings | required | - |
| W124 unit regression | 119 | W124 | unit-regression | `test_operations_catalog`, `test_identity_history`, `metadata.test_reference`, `test_spec_packages`, `test_registry`, `tests.lib.test_surface_ownership` on the W124 tree | PASS | 492 tests OK | required | - |
| W124 post-merge restore | 119 | W124 | byte-compare-restore | Restore each removed body from its recorded last commit and compare bytes | NOT_RUN | Needs the merge of this change; cannot run before it | required | - |
| Remote candidate 998 | 118 | W123 | remote-ci | PR #998 head `09778b761`, merged as `a4142f99a` with a merge commit | PASS | candidate-quality (4m55s), CodeQL, GitGuardian and triage passed; main-security skipped as on every PR | required | - |
| W124 base readiness | 119 | W124 | corpus-readiness | `check-document-corpus-lifecycle.py --readiness` on base `09778b761`, Python 3.12.3 | PASS | SPEC-0248, 0249, 0250, 0260, 0264 and 0265 each `ready` | required | - |
| W124 folder guide consumer | 119 | W124 | unit-regression | `tests.lib.hooks.test_folder_guides` on the W124 tree after merging main (`821a630ec`) | PASS | OK; the SPEC-0264 receipt's consumer check | required | - |
| W124 removal review | 119 | W124 | independent-review | Fresh-context rules-engineer of `2647ce44c` (read only, no tests run) | PASS | No Critical or Important; Minor: a base readiness row, the folder-guide run, ADR-0060 L172 still names SPEC-0265 (left: an accepted ADR, a follow-up for its owner), a table class value and a long line, all handled here | required | - |
| Crosswalk RED | 120 | W125 | red-green-proof | New `GateCrosswalkTests` before `build_gate_crosswalk` existed | FAIL | 5 errors: no attribute `build_gate_crosswalk` | required | - |
| Crosswalk GREEN | 120 | W125 | red-green-proof | Commits `f913bc225`, `0d8168c60`: `test_ci_gate_contract`, `test_ci_gate_evidence`, `test_ci_gate_plan` | PASS | 61 plan tests OK; contract and evidence OK | required | Crosswalk RED |
| Crosswalk review | 120 | W125 | independent-review | Fresh-context code-reviewer of `feat/w05-check-crosswalk` (read only) | FAIL | CHANGES_REQUIRED: the hand list of unique leaves missed `leaf.changed-style`; the reuse test did not prove the security-DB claim and no such input existed; Minor: twin key, docstring, untested flag rejections | required | - |
| Guarantee RED | 120 | W125 | red-green-proof | `test_every_leaf_is_classified_and_changed_style_is_security`, `test_unclassified_or_unknown_guarantee_fails_closed` before the loader knew `guarantee` | FAIL | 14 contract tests errored on the unknown field | required | - |
| Guarantee GREEN | 120 | W125 | red-green-proof | Commits `511a4e4a9`, `233b927a3`, `d87d28c5f` (a non-string `guarantee` raised `TypeError` before `d87d28c5f`) | PASS | 126 and 34 tests OK; workflow-contract and manifest PASS | required | Guarantee RED |
| Reuse lock digest RED | 120 | W125 | red-green-proof | `_expected_plan` mutated to drop dependency digests | FAIL | `lock-digest` subtest: EvidenceError not raised; restored | required | - |
| Reuse lock digest GREEN | 120 | W125 | red-green-proof | `test_recorded_pass_is_reused_only_for_identical_inputs` at `233b927a3`, with a positive control | PASS | OK; the source, base and selection subtests are characterization of behavior that already held | required | Reuse lock digest RED |
| Crosswalk re-review | 120 | W125 | independent-review | Same reviewer, `233b927a3` (read only) | PASS | Every finding fixed or recorded; Minor: a non-string guarantee, pinned error codes (fixed in `d87d28c5f`), the security-DB gap to record (done here) | required | Crosswalk review |
| Routing suite | 120 | W125 | unit-regression | `tests.validation.test_agent_governance_ci_routing` at `233b927a3`, with other suites running on the host | FAIL | 85 tests, 1 failure, not reproduced | required | - |
| Routing suite rerun | 120 | W125 | unit-regression | Same module and tree, twice, after the load ended | PASS | 85 tests OK both times; the single failure is recorded as a possible load-dependent flake | required | Routing suite |
| Remote candidate 999 | 120 | W125 | remote-ci | PR #999 head `d87d28c5f`, merged as `dd6e4a0e1` | PASS | candidate-quality, CodeQL, GitGuardian and triage passed | required | - |
| SemVer precedence RED | 120 | W125 | red-green-proof | New `test_release` and schema tests before `57d327f12` and `84fa7a812` | FAIL | 45 errors (no `compare_semver` or `check_version_change`); 11 schema failures | required | - |
| SemVer precedence GREEN | 120 | W125 | red-green-proof | Commits `57d327f12` to `144799c5d`: `test_release`, `test_registry`, `test_surface_ownership`; metadata check-active | PASS | 213, then 191 tests OK; selected=535 violations=0; the old-consumer test reads the schema at `57d327f12` | required | SemVer precedence RED |
| SemVer review | 120 | W125 | independent-review | Fresh-context code-reviewer of `feat/w05-semver-precedence` (read only) | FAIL | CHANGES_REQUIRED: the protocol claimed an unwired unchanged and downgrade refusal; Minor: string CHANGELOG duplicates, exact-tag remote check, an in-test old pattern | required | - |
| SemVer re-review | 120 | W125 | independent-review | Same reviewer, `144799c5d` (read only) | PASS | All fixed; hosted checkouts use `fetch-depth: 0`, so the pinned commit stays reachable under merge commits | required | SemVer review |
| Remote candidate 1001 | 120 | W125 | remote-ci | PR #1001 head `6f1a7b5cf` (replaces #1000, whose GitHub update-branch commit failed commitizen), merged as `e249285b2` | PASS | candidate-quality (4m53s), CodeQL and GitGuardian passed | required | - |
| Security DB RED | 120 | W125 | red-green-proof | New seed identity, evidence-row, contract and runner tests before `d922daed0` to `938e24b07` | FAIL | `AttributeError`; 7 failures or errors; 3 errors; `TypeError` | required | - |
| Security DB GREEN | 120 | W125 | red-green-proof | Commits `d922daed0` to `7cd3ed24d` after merging main (`0e35da472`): contract, evidence, execution context, plan, Grype seed and surface suites | PASS | OK; 177 tests before the merge; workflow-contract and manifest PASS | required | Security DB RED |
| Security DB review | 120 | W125 | independent-review | Fresh-context code-reviewer of `feat/w05-security-db-reuse` (read only) | FAIL | CHANGES_REQUIRED: an `INVALID` pointer reopened a PASS; Minor: decode errors, non-ENOENT as ABSENT, root canonicalization, a text detector, the manifest consumer row | required | - |
| Security DB re-review | 120 | W125 | independent-review | Same reviewer, `7cd3ed24d` (read only) | PASS | All fixed; no runner-level test feeds an `INVALID` pointer through execution (it relies on the evidence-store rejection) | required | Security DB review |
| Remote candidate 1002 | 120 | W125 | remote-ci | PR #1002 head `aceffb21c` (after a conventional merge of main), merged as `9e4c8f361` | PASS | candidate-quality (11m35s), CodeQL and GitGuardian passed | required | - |
| W125 record links commands | 120 | W125 | links-commands | `check-document-links.py --mode commands` on this record change, first with a 400 s limit, then without | FAIL | exit 124 at the 400 s limit, no output: the limit, not a finding | required | - |
| W125 record links commands rerun | 120 | W125 | links-commands | Same command and tree without the limit | PASS | documents=891 links=8605 failures=0 in 467 s | required | W125 record links commands |
| W125 record checks | 120 | W125 | document-checks | This record change after merging main: corpus lifecycle, links alignment, governance contract, metadata check-changed, `test_spec_packages` | PASS | violations=0; PASS; failures=0; selected=33 violations=0; `test_spec_packages` OK (count not captured) | required | - |
| Remote candidate 1003 | 119 | W124 | remote-ci | PR #1003 head `95252f0a5`, merged as `ca5dc8f4a` | PASS | candidate-quality (4m27s), CodeQL and GitGuardian passed | required | - |
| W124 post-merge restore rerun | 119 | W124 | byte-compare-restore | After merge `ca5dc8f4a`: each of the 18 removed files restored with `git show <recorded commit>:<path>` and compared by SHA-256 with the body at the merge's first parent `9e4c8f361`; reachability from `main` and absence on `main` checked | PASS | rows=18 restored_equal=18 problems=0 | required | W124 post-merge restore |
| QA-08 timing baseline | 120 | W125 | timing-baseline | Each `tests.lib.document_governance` module timed alone at `09778b761`, Python 3.12.3, with other test runs sharing the host | PASS | 22 modules, 921 tests, 2,283 s in total; slowest `test_spec_packages` 827 s, `metadata.test_reference` 409 s, `test_operations_catalog` 329 s, `test_links` 191 s; host load inflates these, so they are an upper bound | optional | - |

### Resolution Links

Disposition RED is resolved by Disposition GREEN, TemplateDefinition RED by
TemplateDefinition GREEN, Vocabulary RED by Vocabulary GREEN, and Currency RED
by Currency GREEN, and Release RED by Release GREEN. Pre-commit is resolved
by its rerun, and Link type RED by Link type GREEN. SemVer RED, Common form pin RED,
Approval hook RED, Acceptance rule RED, Promotion readiness RED, Form
serialization RED, Vocabulary 1.1.0 RED, Readiness RED, Link title RED,
Relation lookup RED and Consumer paths RED are resolved by their GREEN rows,
and the W123 review FAIL by the W123 re-review. Crosswalk RED, Guarantee RED,
Reuse lock digest RED, SemVer precedence RED and Security DB RED are resolved
by their GREEN rows; the Crosswalk, SemVer and Security DB review FAILs by
their re-reviews; the Routing suite FAIL by its rerun; the W125 record
links commands FAIL by its rerun; and the W124 post-merge restore `NOT_RUN` by
its rerun. The Integrated review FAIL is resolved by
the Integrated re-review. The W05 review and
W05 re-review FAILs are resolved by the W05 final review, and the Spec Package
regression by its rerun.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 117 | accepted | Disposition GREEN, TemplateDefinition GREEN, Vocabulary 1.1.0 GREEN, Release GREEN, Link title GREEN, Currency GREEN, SemVer GREEN, Integrated checks, Integrated re-review, Remote candidate 996 final | Owner @buenhyden accepted on 2026-11-14 in this chat, after #996 merged; hosted CI wiring of the local-only leaves stays with H-W05-1 (W06) | SPEC-0212 TSK-0064 |
| 118 | accepted | Relation lookup GREEN, W123 review fixes, Consumer paths GREEN, W123 re-review, W123 regression, Remote candidate 998 | Owner @buenhyden accepted on 2026-11-14 in this chat, after #998 merged | SPEC-0212 TSK-0064 |
| 119 | accepted | W124 base readiness, W124 lifecycle, W124 links, W124 metadata, W124 unit regression, W124 folder guide consumer, W124 removal review, Remote candidate 1003, W124 post-merge restore rerun | Owner @buenhyden accepted on 2026-11-14 in this chat, after #1003 merged and the restore matched; the 0096 scan and the ADR-0060 mention stay as recorded | SPEC-0212 TSK-0064 |
| 120 | accepted | Crosswalk GREEN, Guarantee GREEN, Reuse lock digest GREEN, Crosswalk re-review, SemVer precedence GREEN, SemVer re-review, Security DB GREEN, Security DB re-review, Remote candidate 999, Remote candidate 1001, Remote candidate 1002 | Owner @buenhyden accepted on 2026-11-14 in this chat, after #999, #1001 and #1002 merged; the rule-owner field, the version-change consumer and hosted wiring stay with H-W05-1 (W06) | SPEC-0212 TSK-0064 |

### Remaining Conditions

Criteria 117 to 120 are accepted and the Task is completed. The UNVERIFIED and DELTA rows name their owners. State per axis:
approval as recorded in each row; acceptance as in Criterion Decisions; merge
as each Remote candidate row records; operation: none, since W05 changed no
runtime. Limits: a reference definition used twice, or an
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
| 118 | W123 | Relation lookup GREEN | `.agents/governance/documentation-protocol.md` (Relations derivation, Change Impact row; commit `64769e71a`) | `test_links`; links alignment |
| 119 | W124 | SPEC-0248, SPEC-0249, SPEC-0250 Promotion Map: archive-check removal, Stage 98 deletion, completed-package deletion | `.agents/governance/documentation-protocol.md`, phrases "no records: only its README remains", "Retired artifact numbers live in the Registry", "recorded exactly when its Spec number is reserved" (commit `c9363fd04`); `docs/99.templates/registry.json` `reserved_history` (commit `218d66934`); `scripts/lib/document_governance/lifecycle/occupancy.py` "Stage 98 holds no records" (commit `9692e4616`); lineage in REQ-0026 and AD-0030 Traceability (this change) | `grep` of each phrase on the base tree; links alignment; corpus lifecycle |
| 119 | W124 | SPEC-0260 Promotion Map: generation 6 proof source | `scripts/lib/document_governance/spec_packages.py` `previous_generation_revision(root, 7)` (commit `3745b3db2`) and the protocol text "reads the generation 5 and 6 migration proofs from the last generation 6 revision" (protocol L572; commit `6c283d395` carried the section, later edits kept it); numbers 209 and 231 reserved; lineage in REQ-0026 and AD-0030 | `test_spec_packages`, `test_registry`, `test_identity_history` |
| 119 | W124 | SPEC-0264 Promotion Map: folder guide delivery | `.claude/provider.md` "import shim" and "reminder naming" (commit `b085cabac`), `.codex/provider.md` `exec` route (commit `80c49cf71`), `scripts/lib/hooks/folder_guides.py` and `scripts/hooks/agent-event-hook.sh` (commit `b3c5345cc`), documentation protocol folder-guide text (commit `7bde84a10`); lineage in REQ-0024 and AD-0027 | `tests.lib.hooks.test_folder_guides` is outside the listed checks and was not run here; the receipt of the removed Task named it as passing on main |
| 119 | W124 | SPEC-0265 Promotion Map: report source capture contract | `infra/07-workflow/n8n/workloads/hermes-blog-ingestion/hermes-plugin/tools.py` (`0600` report file, commit `bce52c6d9`), `deploy/research-submission-prompt.txt` and the workload `README.md` `source_text` meaning (commit `ce760c587`), `docs/02.architecture/decisions/0060-hermes-report-source-contract.md` (commit `13eac2103`); lineage in REQ-0004, REQ-0005, AD-0004, AD-0031 and ADR-0060 | grep of each phrase on the base tree; workload tests were not run (no runtime work) |

| 120 | W125 | Guarantee GREEN, Security DB GREEN | `.github/workflow-contract.yml` (`guarantee` in `511a4e4a9`; `security_db` in `6670c855c`, merged by #1002 as `9e4c8f361`) | `check-github-workflow-contract.py`; `test_ci_gate_contract` |
| 120 | W125 | SemVer precedence GREEN | `docs/99.templates/contracts/document-frontmatter.schema.json` and `docs/99.templates/contracts/document-profile.schema.json` (commit `84fa7a812`); `.agents/governance/documentation-protocol.md` SemVer text (commit `144799c5d`) and Version objects columns (this change) | `test_registry`; metadata check-active |

The W122 commits reached `main` through PR #996, merged as `5a1aa4b98`; W123
through PR #998 (`a4142f99a`); and the W125 commits through PR #999
(`dd6e4a0e1`), PR #1001 (`e249285b2`) and PR #1002 (`9e4c8f361`), all with
merge commits; W124 through PR #1003 (`ca5dc8f4a`).

### Next Owner

The current owner is @buenhyden. No W05 work remains in this Task. W06 takes
H-W05-1 as listed under Blockers and Decisions; SPEC-0204 TSK-0011 takes the
OPEN-11 rerun.
