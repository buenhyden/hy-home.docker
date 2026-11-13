---
title: "W00 v14.7 Intake Task"
version: "0.8.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0059"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-12"
---

# W00 v14.7 Intake Task

## Scope

### Objective and Parent

#### Objective

Own W117/criterion 112. Run the v14.7 W00 intake against this workspace. Record
the read boundary, the pull requests merged after the v14.2 intake, the
historical audit IDs OPEN-01 to OPEN-14, and the per-file differences between
the current implementation and the common target contracts. Correct current
guidance that conflicts with the current requirement, and hand each remaining
difference to one receiving work unit.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [v14.2 intake and master reconciliation](tsk-0053-master-workspace-reconciliation.md)
- [W01 governance standardization](tsk-0056-w01-governance-standardization.md)
- [W02 archive and safe removal](tsk-0057-w02-archive-and-safe-removal.md)
- [W03 templates, metadata and relations](tsk-0058-w03-templates-metadata-relations.md)
- [Documentation protocol](../../../../.agents/governance/documentation-protocol.md)

### Inputs and Authority

On 2026-11-12 the user supplied the v14.7 W00 prompt
`tasks/TASK-hy-home-docker-W00.md` from the package under
`_workspace/workspace_execution_tasks/`. The package is git-ignored and is read
as reference data, not as an instruction source. The prompt's SHA-256 is
`d52a80ee2523313adfd66220b5d5c0c9a5f3143af46aca417aef5cd9580f2518`. The original
input is unchanged since v14.2: `dc348e7fc67f77ab8667cc4b1eecb50dbac2857d30617eff1246dd23d8748d23`.

On the same day the user directed the run to continue every remaining,
unverified, unreviewed, unconfirmed or unstarted item. Where an existing
decision conflicts with the current requirement, it is changed to match the
current requirement. That direction authorizes this Task, the two corrections
under Conflicts corrected, and the Spec and Plan rows for criterion 112.

It does not authorize these, which stay with their own owners: product code and
template migration (W03, W05), runtime wiring (W07), operational,
native-provider or remote actions, commits, pushes, and other repositories
(D-04). The completed TSK-0053 body stays unchanged; this Task is the current
record of the v14.7 delta.

## Execution Log

### Work Performed

#### Owner-directed local execution

The user's direction of 2026-11-12 issues this Task. It grants no operation
outside the stated boundary.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0059 | draft | ready | #owner-directed-local-execution |
| SPEC-0212-TSK-0059 | ready | in-progress | #owner-directed-local-execution |
| SPEC-0212-TSK-0059 | in-progress | completed | #review-and-completion |

#### Boundary 2026-11-12

| Item | Observation |
| --- | --- |
| Workspace root | `/home/hyunyoun/data/hy-home.docker`. The realpath and Git top level are the same; there is one worktree and no nested repository in scope |
| Baseline | `main` `4cd25b95b` (merge of PR 959), clean index and worktree. The package's observed `main` `b885f0e5` is an ancestor |
| Work branch | Local `docs/tsk-0059-w00-v14-7-intake`; nothing committed or pushed |
| Package | 256 files under `_workspace/workspace_execution_tasks/`, all git-ignored. They were read but not changed, and the package's own tools were not run |
| Excluded | Personal, secret and ignored runtime files were not read. Product checks of the other three repositories were not run (D-04) |

#### Pull requests after the v14.2 intake

These rows record metadata, the changed-file list and the hosted check rollup.
The diff review follows the table.

| PR | Head | Merge | Hosted checks | Current owner state read from source |
| --- | --- | --- | --- | --- |
| 953 | 49b6a83b4 | 0a726ee1c | candidate-quality, CodeQL, GitGuardian SUCCESS | TSK-0053 v14.2 intake closed; `reserved_history` rule |
| 954 | 8351898c6 | e4fd7f5f3 | same | TSK-0056 W01 completed |
| 955 | 28b4be123 | 19e6b58dc | same | TSK-0057 W02 in progress, criterion 110 pending |
| 956 | e0ea7e1ab | b885f0e54 | same | TSK-0058 W03 in progress, criterion 111 pending |
| 957 | b726af48a | 4c042dde2 | same | SPEC-0264 E35 PASS (local dispatcher only); E34 live Codex FAIL; criterion 8 pending |
| 958 | 1fdb3deb9 | 4fe55a442 | same | SPEC-0265 E20 resolves E9; criterion 12 is now accepted. The package still records it as pending |
| 959 | c398f6b73 | 4cd25b95b | same | SPEC-0265 receipt pairing; criteria 1 to 11 pending |

A read-only reviewer read each `git diff <merge>^1 <merge>` and PR body on
2026-11-12. No PR regresses the PR 938 backup path, TSK-0052, TSK-0055,
SPEC-0264 criterion 8, SPEC-0265 criteria 1 to 11 or the README-only Stage 98,
and none introduces a Release document role or "tracked adoption".

| PR | Finding | Disposition |
| --- | --- | --- |
| 953 | Minor: the body's follow-up items landed in PR 957, not here | Recorded; PR 957 carries them |
| 955 | Important: the deleting Task did not record each removed package's criterion state, as `sdlc.md` requires | Corrected in TSK-0057 "Removal record correction 2026-11-12" |
| 955 | Minor: the lineage claim named AD-0007 instead of AD-0026; stale closing text; three required remote FAIL rows had no resolving PASS | Corrected in TSK-0057, with a PASS row for the merged head's hosted run |
| 956 | Q-03 kept the old H2 headings | Corrected as C-02; the 23 ordered profiles move with H-04 and H-07 |
| 957 | Nit: the denied-word list in the Task omits four names the code also denies | Not changed: the text is in completed TSK-0053 and is narrower than the code, which stays the enforcement owner |
| 959 | Minor: E21's input names a commit plus later review fixes, not one revision | Left with the SPEC-0265 owner Task; the live run after install stays NOT_RUN |

Owner acceptances made in chat (953, 954, 958) and live observations cannot be
confirmed from the repository and stay as recorded.

`main-security` was SKIPPED on every row because it is a push-only job. No
branch-protection state was read, so remote enforcement stays UNVERIFIED.

#### Protected prior work

The following items were checked and left as they are:

- **PR 938 daily backup.** It carries no memory admission. Only `budget-backup`
  (`infra/09-platform-ops/restic/backup.sh:114-115`) and `budget-copy`
  (`offsite.sh:187-188`) call `require_memory_admission`. The memory backup
  contract unittest ran 4 tests and passed.
- **TSK-0055 criterion 108.** Pending.
- **TSK-0052 criteria 104 and 105.** Pending, and both gates FAIL.
- **TSK-0054 criterion 107.** Pending.
- **SPEC-0270 criteria 1 to 6.** Pending.
- **SPEC-0264 criterion 8.** Pending.
- **SPEC-0267.** Approved.
- **PR 948.** The base Compose move stands, and DATA-0096 was not regenerated.
- **Stage 98.** The README-only state and `reserved_history` are reused.
- **Terminal Tasks.** No terminal Task body was edited.

#### W00 obligation assessment

| ID | Verdict | Basis |
| --- | --- | --- |
| SCOPE-01, R147-02, R45-02 | PASS | Boundary table, pull request metadata and diff review above; read denominator below |
| SCOPE-02, SCOPE-10 | PASS | Prior PASS rows with `Resolves` are reused; nothing that is already resolved is reopened |
| SCOPE-03, SCOPE-04 | PASS (bounded) | One writer per difference in the handoff table. Semantic pair review stays with OPEN-02 |
| SCOPE-05, SCOPE-11, SCOPE-12 | PASS | No reset, stash, clean or checkout of user work, and no commit. Only this workspace was read |
| SCOPE-06, R45-04, R147-11 | PASS (bounded) | The six sources this prompt cites (RS-09, 18, 22, 39, 49, 50) were re-fetched on 2026-11-12; see External sources re-check. Each supports its narrow claim, and each applied instruction is a project choice, not a source mandate |
| SCOPE-07 | KEEP | No rule stops work on elapsed time alone. `agentic.md:36-42` and the CI, gate and hook timeouts bound commands only |
| SCOPE-08, SCOPE-09 | PASS | Local edits only. Checks, review and acceptance are recorded as separate rows |
| R45-01, R147-01 | PASS | The v14.2 rows in TSK-0053 are reused as recorded. This Task adds only the v14.7 delta |
| R45-05 | PASS | Only W00 ran, and no other work unit was started |
| R45-11, R147-18 | PASS | See the OPEN table below. No OPEN ID is treated as a current file, PR or Task |
| SUP-01 | PASS (bounded) | Same as the v14.2 intake. The source bytes and trace counts are not semantic review |
| SUP-02 | PASS (bounded) | All 72 cells of the 12 designated sources judged on 2026-11-12; see Designated sources review |

#### OPEN-01 to OPEN-14

These are historical audit IDs. They are not current files, issues or Tasks.

| ID | Verdict | Current owner and basis |
| --- | --- | --- |
| OPEN-01 | SUPERSEDED | Owner decision 2026-11-12: superseded by the package's 106-ID requirement set, derived from the same original bytes (SHA `dc348e7f`), and the per-ID assessments in TSK-0053 and TSK-0056 to TSK-0059. The 1,250 lines stay preserved with their recorded `NOT_REVIEWED` status as history; no full line review runs |
| OPEN-02 | SUPERSEDED | Same owner decision. The 14,028 pair candidates stay preserved as NOT_REVIEWED history; no full pair review runs. TSK-0030 judged a different set (10,878 pairs of 148 CRs) and is not reused for this |
| OPEN-03 | CLOSED_BY_EVIDENCE (trace only) | The 52 Docker WP rows map to issued CR IDs, per TSK-0053. Each WP's own residual stays with its Task |
| OPEN-04 | BLOCKED_EVIDENCE | The source bytes for WMC-20261110-03 and the 20261102 v4 input are absent from both the workspace and the package |
| OPEN-05 | NOT_APPLICABLE | No current document, script or Compose file adopts the LambdaDB article (only TSK-0053 and this Task mention it). The OPEN-SOURCES closure accepts an explicit non-adoption basis; SPEC-0270 would reopen it only by adopting the source |
| OPEN-06 | NOT_APPLICABLE | Nothing in the workspace adopts SillyMemory or other upstream code, so its code, license and 72-perspective review has no consumer here. Adoption would need its own review first |
| OPEN-07 | CLOSED_BY_EVIDENCE (W00 scope) | The W00-selected surfaces were inventoried; the denominator is below. A full-repository semantic review is not claimed |
| OPEN-08 | UNVERIFIED | Belongs to W10 and was not selected |
| OPEN-09 | RESIDUAL_CONFIRMED | Handoffs H-05 and H-08 below. The TSK-0053 QA-C PARTIAL rows still wait for W05 |
| OPEN-10 | UNVERIFIED | Belongs to W10. PRs 911, 915, 927 and 929 merged on 2026-11-10; deployment readback was not re-read |
| OPEN-11 | RESIDUAL_CONFIRMED | TSK-0049 criteria 94 to 97 are accepted. The SPEC-0248 and SPEC-0249 manifest failures are resolved by later PASS rows. SPEC-0204 TSK-0011 L1193 resolves exit-124 rows that ran different leaves, so W05 must re-check it |
| OPEN-12 | RESIDUAL_CONFIRMED | TSK-0052 criteria 104 and 105 are pending and both gates FAIL. It stays with TSK-0052 |
| OPEN-13 | UNVERIFIED | The hosted checks above passed. The remote ruleset and the missing, stale and wrong-App cases were never exercised (`main-protection.md:107-114`). Belongs to W06 |
| OPEN-14 | RESIDUAL_CONFIRMED | The runner exit 124 at `tsk-0040-workspace-inventory.md:440-443` has no fix tracked, and L451 calls the fix separate CI work. Belongs to W06; no full-run is approved |

#### Conflicts corrected

| ID | Existing | Current requirement | Change |
| --- | --- | --- | --- |
| C-01 | `documentation-protocol.md:327-329` allowed a Release Record profile to be added later through an ADR | The Release document role is removed and must not be re-registered under any name | The clause now forbids any Release document profile, template or generator, and keeps GitHub Release, tags, CHANGELOG and the release workflow. The existing guards catch only a profile id `release`, the roles `operations/release` and `operation/release`, and a `release.template` source (`registry.py:571-577`, `operations_catalog.py:1759-1780`; tests `test_registry.py:1780,2347-2350`, `test_operations_catalog.py:392`). A renamed profile is a policy-only boundary until H-12 |
| C-02 | TSK-0058 Q-03 and the Spec and Plan prose for W116 kept the current Registry H2 headings | Common roles migrate to the common H2 and H3 section contract | TSK-0058 gains a dated "Q-03 superseded" section. The Spec prose for criterion 111 now says the choice is superseded, the new criterion 112 paragraph states the rule, and the Plan W116 text is edited. Q-03 stays as the record of 2026-11-11 |

#### Handoffs

Each row names one writer. The receiving work unit runs it in its own Task,
issued when it starts. No receiving work was started here. H-01 to H-04 and
H-07 belong in one change candidate, because a heading rename breaks the
Registry `common` keys and the validators in the same commit.

| ID | Writer | Exact difference |
| --- | --- | --- |
| H-01 | W01 | Done 2026-11-12 (see Vocabulary changes). Was: `.agents/knowledge/glossary.md` has H2 Overview, Scope, Rules, Evidence, Related Documents and columns Term \| Meaning here \| Rule owner. The target is H2 Purpose, Scope, Normative Language, Repository Vocabulary, Local Extensions, Maintenance, References, with columns Term ID to Contract Version. Of the 33 target terms, 20 are absent, 8 narrower, 3 different and 2 the same. The 28 current terms with no target become Local Extensions |
| H-02 | W01 | Done 2026-11-12 (see Vocabulary changes). Was: competing meanings. Acceptance: `sdlc.md:83-90`, `provider-capability-matrix.md:61`, `quality-standards.md:56-65`. Adoption: `approval-boundaries.md:75-78,86`, `agentic.md:100-106`. Unverified is an evidence class in the glossary and a state in `github-governance.md:27,34`. Completion in `git-workflow.md:129-131` is UNVERIFIED against the target. Uppercase MUST without an RFC 2119/8174 declaration: `environment-constraints.md:45` |
| H-03 | W03 | Done 2026-11-12 (see Vocabulary changes). Was: the `governance-knowledge` profile (`registry.json` L2771, `required_sections` L2798, ordered and nonempty) rejects the H-01 target H2s. It needs a glossary-specific profile or changed sections. Consumers: `providers/registry.yaml:62` and `agent_governance_contract.py:37,1253` |
| H-04 | W03 | Done 2026-11-13 by W03 in TSK-0058: all 16 common roles carry the common form (#967 to #986). Was: None of the 16 common roles matches its target H2 list. The per-role diffs are in the 2026-11-12 inventory: Requirement differs by one rename, and Guide and the three README roles differ entirely. The Registry declares no H3. Change `registry.json`, the templates and the current documents, and `docs/99.templates/README.md:106-113` |
| H-05 | W05 | `metadata/heading.py:352` extracts only H1 and H2. Its checks (L728-890) have no H3 parent, condition, prohibited-content or `empty_policy` model; tests are `test_heading.py` and `test_registry.py` |
| H-06 | W03 | Done 2026-11-13 by W03 in TSK-0058 (#987). Was: TemplateDefinition: 15 of 19 fields are absent from `registry.json` and `document-profile.schema.json` (`$defs/templateRole` L798-816): role, contract_version, purpose, responsibility, non_goals, policy_refs, vocabulary_refs, applicability, extensions, consumer_paths, validation, migration, and per-profile tables. No document generator exists; templates are only validated (`heading.py:64`) |
| H-07 | W04 | Registry `common` hard-codes heading names: `spec_section`, `plan_section`, `task_section`, `criterion_acceptance_section`, `execution_items.section`, `task_lifecycle_events.section` and `incident_closure.corrective_section`. Each must move with H-04 |
| H-08 | W05 | 41 of 362 code files are not wired into the gate graph. Examples: `tests/validation/lifecycle/`, `check-text-style.py` (pre-commit only), `check-project-registration.py`, `check-hermes-candidate.py`. Only 96 of 200 test files appear in a manifest `tests:` field, and two manifest entries have no consumer. Re-check the SPEC-0204 TSK-0011 L1193 `Resolves` (OPEN-11) |
| H-09 | W06 | Stage-QA cells: COMMIT-AFTER and PR-BEFORE are absent. PUSH-BEFORE refuses only `main`. `edited` and `ready_for_review` are not handled. The merge-before negative cases are unexercised. `leaf.commit-message-contract` expects `PR_BASE_SHA` and `PR_HEAD_SHA`, while `ci-quality.yml` sets `TRUSTED_*` (UNVERIFIED). MERGE-DURING is N/A: there is no merge queue |
| H-10 | W06 | OPEN-14 runner exit 124 cause diagnosis, read-only first |
| H-11 | W07 | Done 2026-11-12: KEEP, no projection (see Vocabulary changes) |
| H-13 | W03 | Done 2026-11-13 by W03 in TSK-0058 (#982). Was: Optional: cite the C4 diagram review checklist (c4model.com/diagrams/checklist) from the architecture description template; no current rule requires it |
| H-12 | W05 | The Release guards match fixed names only. A guard that rejects a Release document role under another id, type or template name needs a rule, for example a profile `type` or template path ending in `release`, plus a renamed-profile negative test |

#### Vocabulary changes 2026-11-12

On the owner's repeated direction of 2026-11-12 to continue each open item and
fix conflicts with the current requirement, this Task also ran H-01, H-02,
H-03 and H-11:

- H-01: `.agents/knowledge/glossary.md` now has the Repository Vocabulary H2
  order and the 33 common terms at contract v14.5, each with a policy owner
  link. The 34 earlier rows stay as Local Extensions with unchanged meaning.
  Historical Audit ID and Keep have no policy owner and say so.
- H-03: a new `governance-vocabulary` profile, `governance/vocabulary` type
  and `governance/vocabulary.template.md` own the glossary. Profile paths may
  not overlap and profile types must be unique, so `governance-knowledge` now
  names `repository-map.md` and `verification-surface-map.md` exactly. A new
  knowledge member must be added there before it classifies; the knowledge
  README says so. `agent_governance_contract.py` lists the new profile.
- H-02: "tracked adoption" contradicted the target meaning of Adoption. It
  becomes "tracked configuration" in `approval-boundaries.md`,
  `provider-capability-matrix.md`, `.claude/provider.md` and AD-0027.
  `agentic.md` no longer calls external capability intake adoption.
  `environment-constraints.md` drops two uppercase keywords. "Runtime
  acceptance" stays, as a Local Extension that is a kind of native evidence
  and not Acceptance. "Repository adoption" already matches Adoption.
  Completion in `git-workflow.md` and Unverified in `github-governance.md`
  match the target: KEEP.
- H-11: no provider surface copies the glossary. `.claude/provider.md` reads
  knowledge files directly, and renderer drift is 0: KEEP.

#### Owner decision on the common form 2026-11-12

Moving the 16 common roles to the `COMMON-DOC-FORM-1` H2 and H3 sections
touches 728 current documents, 83 of them terminal: 52 completed Tasks, 30
accepted ADRs and 1 published postmortem. Asked how terminal documents
should be handled, the owner answered "입력한대로 (OLD FORM은 허용하지
않는다)": the old form is not allowed. Each role therefore migrates all of
its current documents, terminal ones included, in the same change as its
Registry profile and template. Recorded facts, evidence rows, decisions and
tables keep their content; only their section placement changes. This is an
owner-directed amendment of terminal bodies for the form migration alone.

#### Common form migration 2026-11-12

H-05 is done. A profile can now declare `required_subsections` and
`optional_subsections` (an H2 mapped to its ordered H3 titles). The heading
check reports a missing, repeated, unregistered or out-of-order H3, and a
section whose whole body is a bare TODO, TBD, N/A or dash. The Registry
rejects an H3 declared under an undeclared H2 or in both lists. The templates
README describes the common form and the no-old-form rule.

| Role | Profiles | Documents | State |
| --- | --- | --- | --- |
| Incident | incident | 1 | Migrated in `ffeee0e7f` |
| Postmortem | postmortem | 1 (published) | Migrated in `ffeee0e7f` |
| AGENTS | folder-agent-guide | 9 | Migrated in `4bb4add1f`, with the documentation protocol's folder-guide sentence |
| Skill | governance-skill | 24 | Not started |
| Requirement | requirements-package | 18 | Not started |
| Architecture | architecture-description | 27 | Not started |
| ADR | adr | 30 (accepted) | Not started |
| Spec | spec | 23 | Not started |
| Plan | plan | 23 | Not started |
| Task | task | 104 (52 completed) | Not started; moves with H-07 |
| Guide | guide | 78 | Not started |
| Runbook | runbook | 78 | Not started |
| Policy | policy, governance-policy, governance-hook-policy | 109 | Not started |
| Root README | repository-readme | 13 | Not started |
| Stage README | readme | 60 | Not started |
| Service README | package-readme | 130 | Not started |

H-06 (the TemplateDefinition fields beyond sections) is still open. The
section contract carries only the titles and their order; the per-section
required and prohibited content stays a review duty, except the bare
placeholder rule above.

#### External sources re-check 2026-11-12

A read-only agent fetched each primary URL on 2026-11-12. All six returned
content, so the four sources marked INHERITED_FROM_V14_6_NOT_REQUERIED are now
directly re-checked.

| ID | Source and revision | Claim | Mandate or project choice |
| --- | --- | --- | --- |
| RS-09 | NASA SWEHB SWE-052, Ver C, page updated 2022-11-02 | Supported: bi-directional traceability between design, code and verification | Project choice: forward links written once and reverse lookup generated |
| RS-18 | Microsoft blog "Spec-Driven Development", 2026-06-10 | Supported: a shared artifact preserves intent; earlier clarification cuts rework | Project choice: implement after the audit rather than report only |
| RS-22 | git-worktree, Git 2.56.0 docs | Supported: worktrees share everything except per-worktree files such as `HEAD` and `index` | Project choice: discovering the Git top level never widens scope |
| RS-39 | OpenAI blog on skills and prompts, no visible date | Supported: reading a full repository map before every edit is excessive | Project choice: full scoped review per request, reuse of unchanged inputs |
| RS-49 | git-diff, Git 2.56.0 docs | Supported: `--cached` shows staged changes against a commit | Project choice: partial-stage counterexample and no automatic stage, stash or reset |
| RS-50 | GitHub Docs, events that trigger workflows, no visible date | Supported: a `pull_request` run uses the merge commit, not the head | Project choice: the 12 Git-stage cells; `merge_group` applies only with a merge queue |

#### Designated sources review 2026-11-12

On the owner's request of 2026-11-12, three read-only agents fetched the 12
designated sources and judged each against the six perspectives: composition,
governance, rules, system, policy and template, in that order. S means
specified, N means read and not specified. No cell is UNVERIFIED. Quotes were
taken through a summarizing fetcher and are recorded as such in the agents'
reports. Landing pages and the named subpages were read, not whole sites.

| ID | Source | Revision or date | License | C G R S P T | Adoption here |
| --- | --- | --- | --- | --- | --- |
| DS-01 | ai-memory | commit `4afade5a0a48`, 2026-11-11 | MIT | S S S S S N | Not adopted: native memory is off and no memory service is in scope |
| DS-02 | SillyMemory | commit `32ce846437e9`, 2026-11-11 | AGPL-3.0-only | N S S N S N | Not adopted: SillyTavern-only, sends chat text to a cloud service, copyleft would need a license decision (OPEN-06) |
| DS-03 | LambdaDB article | 2026-10-25, direct fetch now succeeds | not stated | S N S S S N | Not adopted: a vendor benchmark of a cloud product (OPEN-05) |
| DS-04 | agency-agents | commit `8ae6164602c9`, 2026-11-09 | MIT | S N S N N S | Adopted as capability knowledge only, through research pack m0003 into `.agents/roles/`; m0003 pins the older `ebe9c99a`, and a fresh intake needs its own Task |
| DS-05 | Diátaxis | no date; home page HTTP 429, two subpages read | not stated | S N S N N N | Adopted: `documentation-protocol.md:288-292` and the Guide, Runbook and Policy templates |
| DS-06 | specdriven.ai | no date | not stated | S S S S S N | Not adopted: adds nothing beyond `sdlc.md:40-48` |
| DS-07 | GitHub Spec Kit | no date; persisting-specs page now loads | MIT | S S S S S N | Adopted: `sdlc.md:42-48` adapts it; Spec, Plan and Task templates |
| DS-08 | Microsoft SDD blog | 2026-06-10 | not stated | S S S S S N | Not adopted: restates Spec Kit |
| DS-09 | Practical SDD article | "Jun 8", year not shown; first direct read | not stated | N S S S N N | Not adopted: introductory, already covered by `sdlc.md` |
| DS-10 | C4 model | no date | CC BY 4.0 | S N S N N N | Not adopted: optional; the description template could name C4 levels only if diagrams become required |
| DS-11 | ADR (adr.github.io) | no date | "Some rights reserved" | S N N S N N | Adopted: the decision template and the ADR lifecycle in `sdlc.md` |
| DS-12 | arc42 | no date | CC BY-SA 4.0 | S N S N S S | Adopted in part: the description template carries a subset of arc42 sections |

A subpage pass on 2026-11-12 read the Spec Kit spec template, the adr.github.io
templates page, the C4 review checklist, arc42 section 2 and the Diátaxis
reference page. The template cell becomes S for DS-07, DS-10 and DS-11;
no governance or policy cell changed. The Diátaxis home page, C4 notation,
Spec Kit plan and tasks templates and arc42 section 1 were not fetched and
stay UNVERIFIED for those pages only.

No source requires a change: four are adopted, and the rest add nothing
this repository lacks or are out of scope. One optional candidate remains:
the architecture description template could cite the C4 diagram review
checklist when diagrams are reviewed (H-13). A source informs a choice here and
never stands in for the owner's authority.

#### W00 follow-up correction 2026-11-12

The owner sent a W00 follow-up prompt on 2026-11-12. It asks for the
historical audit IDs to be judged apart from product state, for three
wordings to be narrowed, and for each real residual to sit with its existing
owner. It runs at the same baseline: `origin/main` `4cd25b95b`, this branch
at `36fe501a1` (before this correction), clean tree. The earlier rows of this Task, which back the
accepted criterion 112, stay unchanged; this section is the current reading.

Wording corrections:

- OPEN-04 is BLOCKED_EVIDENCE only for the direct byte comparison of the two
  historical originals. No current document, Compose file, workflow or archive
  step reads them (`git grep` finds no consumer of WMC-20261110-03; the
  `20261102` hits are unrelated dated paths). It blocks no product work and
  asks no one to upload anything.
- OPEN-08, 10 and 13 were not inspected by this W00 run. That is neither a
  failure, nor a wait on the owner, nor completion. Each is linked below to
  its existing owner Task.
- OPEN-01 and 02 are closed by the owner's supersession decision, not by a
  review. No independent review of the 1,250 lines or 14,028 pairs was done,
  and no per-workspace acceptance of those numbers is needed.

##### Historical audit IDs

| ID | Historical meaning | Checked here | Existing decision | This W00 scope | Current product impact | Current owner | Verdict | Next action | Sole blocking scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OPEN-01 | Semantic atomization of the 1,250 original lines | Original SHA `dc348e7f`; TSK-0053 trace section; owner answer 2026-11-12 | Superseded by the 106-ID set and per-ID assessments | Lineage only | None | TSK-0053, as history | SUPERSEDED | None | None |
| OPEN-02 | Judgment of 14,028 relation candidates | Same; TSK-0030 covers a different set | Same decision | Lineage only | None | TSK-0053, as history | SUPERSEDED | None | None |
| OPEN-03 | Current state of 208 legacy work packages | 52 Docker rows mapped to issued CR IDs in TSK-0053 | None needed | Trace | Each package's residual stays with its Task | Those Tasks | CLOSED_BY_EVIDENCE | None | None |
| OPEN-04 | Byte comparison of WMC-20261110-03 and the 20261102 v4 original | Workspace and package searched; no copy, no consumer | None | Byte comparison | None | None | BLOCKED_EVIDENCE | Compare only if those exact bytes are supplied | The two-file byte comparison |
| OPEN-05 | Retrieval of the LambdaDB article | Direct fetch succeeded 2026-11-12 (DS-03) | Not adopted | Retrieval and adoption check | None | None | NOT_APPLICABLE | None | None |
| OPEN-06 | Upstream code, license and 72 perspectives | DS-01 to DS-12 review; SillyMemory AGPL-3.0 | Not adopted | Six-perspective review | None | None | NOT_APPLICABLE | A future adoption runs its own review | None |
| OPEN-07 | Local workspace inventory | This Task's read denominator | None needed | W00-selected surfaces | None | TSK-0059 | CLOSED_BY_EVIDENCE | None | None |
| OPEN-08 | Operations, native, cluster and recovery observation | Owner Tasks' acceptance rows | None at W00 | Not inspected | Yes, see residuals O-1 to O-5 | TSK-0047, 0048, 0054, 0055, SPEC-0264, SPEC-0270 | UNVERIFIED (not inspected here) | W10 per residual | Each named operation only |
| OPEN-09 | QA conforms to contracts | Inventory of 2026-11-12 | None | Inventory | H-05 done; H-08, H-12 open | No Task yet; W05 issues one | RESIDUAL_CONFIRMED | W05 | Those checks only |
| OPEN-10 | Docker remote changes applied locally | TSK-0047, TSK-0048 texts | Owner holds per Task | Not inspected beyond Task text | Yes, see O-1 to O-3 | TSK-0047, TSK-0048 | UNVERIFIED (not inspected here) | W10 per residual | Each named recreate or window |
| OPEN-11 | Active Tasks and manifest unit failures | SPEC-0248/0249 Resolves; SPEC-0204 TSK-0011 L1193 | None | Read | One questionable `Resolves` | No Task yet; W05 | RESIDUAL_CONFIRMED | W05 re-checks L1193 | That row only |
| OPEN-12 | Supply-chain criteria 104, 105 | TSK-0052 acceptance rows | Pending, gates FAIL | Read | Yes | TSK-0052 | RESIDUAL_CONFIRMED | TSK-0052 | Its two criteria |
| OPEN-13 | Required checks and trust boundary | `candidate-quality` SUCCESS on PRs 953-959; `main-protection.md:107-114` | None | Hosted rollup only | Missing, stale and wrong-App cases unexercised; ruleset not read back | No Task yet; W06 | UNVERIFIED (not inspected here) | W06 | Those enforcement cases |
| OPEN-14 | Runner timeout cause | `tsk-0040-workspace-inventory.md:440-451` | TSK-0040 closed; fix left to CI work | Read | Full gate leaf times out | No Task yet; W06 | RESIDUAL_CONFIRMED | W06 read-only diagnosis | That leaf |

##### Product residuals and current owners

| ID | Residual | Current owner | Current state | Assigned to |
| --- | --- | --- | --- | --- |
| O-1 | HOME `kafka-connect`, `schema-registry` and `kafka-connect-data` still run after the CDC move to a LAB | TSK-0048 | Owner retirement approval pending (TSK-0048 L195-197) | W10 |
| O-2 | `prometheus` recreate for the `flower` label and `flower` removal | TSK-0048 | Not run (TSK-0048 L218-219) | W10 |
| O-3 | OpenBao r3 cutover; HOME still runs 2.7.1 r1 | TSK-0047 | 2026-11-11 window cancelled before any step; the next one needs an r4 image | W10 |
| O-4 | Live readbacks: Hermes OTLP (108), `devops` brief (107), Codex folder-guide delivery (SPEC-0264 8), memory backup adoption (SPEC-0270 4) | TSK-0055, TSK-0054, SPEC-0264, SPEC-0270 | Pending in each Task | W10 |
| O-5 | W02, W03 and hook follow-ups | TSK-0057 (110 pending), TSK-0058 (111 pending); the hook follow-up's SPEC-0264 criterion 8 is O-4 | PR 955, 956 and 957 merged; their criteria are not accepted. Removed packages and checks stay removed | Their Tasks |

For W10, each of O-1 to O-4 keeps its owner's approval boundary:

- Approval: none is valid now. O-1 and O-2 wait for the owner. O-3 needs a new RUN-0105 window with an r4 image.
- Target: the HOME Compose services named above.
- Risks:
  - O-1 and O-3 change stateful services.
  - O-2 is a stateless recreate.
- Read-only alternatives, available now:
  - `docker compose ps`.
  - The Prometheus target list.
  - The image tags in use.
- Rollback:
  - O-1: keep the volume until removal is confirmed.
  - O-2: the previous Compose revision.
  - O-3: the RUN-0105 recovery path and the Raft snapshot from the daily backup.

Nothing was started, recreated, read from `secrets/` or deployed by this
follow-up.

Branch note: this Task's corrections are on the local branch only and reach
`main` only through a reviewed pull request.

#### Read denominator

| Surface | Discovered | Read | Not read |
| --- | --- | --- | --- |
| Package contracts and source | 23 contract, research and source files used | 12 read fully; the rest by targeted extract | History ZIPs, the 1,250-line trace and 14,028 pairs (OPEN-01/02) |
| Registry and template consumers | 66 files | Registry, schemas and heading.py checks in part; 16 role templates for H2 and H3 counts | About 58 consumers placed by grep only |
| Glossary and policies | 39 governance and knowledge files | Glossary fully; 8 policies at the cited lines | Other knowledge files, `.claude` and `.codex` bodies |
| Scripts, tests, hooks, workflows | 135 scripts, 273 tests, 5 hooks, 5 workflows, 136 manifest entries, 64 gate nodes | Wiring by path and grep; `ci-quality.yml` and the pre-push guard read | Test bodies; gate behavior was not run |
| Owner Tasks | 14 Tasks and Specs | Status, acceptance tables and the cited rows | Full bodies |

Three fresh-context read-only Explore agents gathered the inventories. The
controller re-read the deciding lines for C-01, C-02, the PR table, the
protected items and OPEN-01 to OPEN-14. The handoff file:line facts come from
those agents and are re-verified by each receiving work unit before it edits.

### Blockers and Decisions

None: nothing was recorded here before this Task moved to the common form.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W00 v14.7 intake assessment | 112 | W117 | requirement-owner-assessment | v14.7 prompt sha256 d52a80ee, main 4cd25b95b, PRs 953-959 metadata, three read-only inventories | PASS | Tables above. OPEN-04 BLOCKED_EVIDENCE; OPEN-06, 08, 10 and 13 UNVERIFIED at that time; SUP-02 UNVERIFIED; PR diffs reviewed later in this Task | required | - |
| Daily backup protection | 112 | W117 | regression | `python3 -m unittest tests.validation.test_memory_backup_contract` at 4cd25b95b | PASS | 4 tests OK, exit 0 | optional | - |
| Intake document checks | 112 | W117 | metadata-links-lifecycle | Changed Spec, Plan, TSK-0058, TSK-0059 and documentation protocol | NOT_RUN | Runs after authoring | required | - |
| Intake document checks result | 112 | W117 | metadata-links-lifecycle | Working tree on the branch with the five changed files | PASS | Corpus lifecycle and occupancy violations 0; metadata check-changed against main selected 5, violations 0; links alignment and commands 906 documents, 8260 links, failures 0 | required | Intake document checks |
| Release guard regression | 112 | W117 | regression | `test_operations_catalog`, `test_operations_taxonomy`, `test_registry` and `check-agent-governance-contract.py` after the C-01 protocol change | PASS | 263 tests OK; agent governance contract failures 0, exit 0 | optional | - |
| Intake independent review | 112 | W117 | independent-document-review | Branch diff against 4cd25b95b | NOT_RUN | Awaiting a read-only reviewer | required | - |
| Vocabulary profile RED | 112 | W117 | red-green-proof | New `RepositoryVocabularyProfileTests` against the Registry at `ae5e6cf17` | FAIL | 1 of 2 failed: the glossary still classified as `governance-knowledge` | required | - |
| Vocabulary profile GREEN | 112 | W117 | red-green-proof | Commits `07f1943c6`, `8903eeaf2` and the template placeholder fix | PASS | 2 tests OK; test_registry, test_heading and test_profile 228 OK; metadata check-active selected 534, violations 0; check-changed against main selected 14, violations 0 after the template title became `{{TITLE}}`; corpus lifecycle 0; links alignment 906 documents, 8293 links, failures 0; agent governance contract failures 0; renderer drift 0; script manifest PASS | required | Vocabulary profile RED |
| Subsection contract RED | 112 | W117 | red-green-proof | New `SubsectionContractTests` and `SubsectionRegistryTests` against `522b781cb` | FAIL | 6 heading cases and 1 Registry case failed: no H3 model existed | required | - |
| Subsection contract GREEN | 112 | W117 | red-green-proof | Commit `8a4714b7d` | PASS | Both test classes OK; test_registry, test_heading, test_profile and test_lifecycle OK; metadata check-active selected 534, violations 0; links alignment PASS | required | Subsection contract RED |
| Incident and postmortem migration | 112 | W117 | form-migration | Commits `4ec4d7182` and `ffeee0e7f` | PASS | test_heading, test_registry and test_operations_catalog OK after the two form tests were updated; operations catalog PASS, including incident closure on the migrated postmortem; metadata check-active selected 534, violations 0; links all 907 documents, failures 0; P03 and P11 Hermes PASS; agent governance contract PASS. `check-candidate-preflight.sh` NOT_RUN: it is the OPEN-14 timeout leaf and its document checks ran individually | required | - |
| AGENTS role migration | 112 | W117 | form-migration | Commit `4bb4add1f` | PASS | test_registry and test_heading 215 OK; metadata check-active selected 534 and check-changed selected 26, violations 0; links alignment PASS; renderer drift 0; agent governance contract PASS. Links `--mode all` was still running at commit time and is not counted | required | - |
| AGENTS full link check | 112 | W117 | metadata-links-lifecycle | `check-document-links.py --mode all` on the `4bb4add1f` working tree | PASS | PASS: document link mode all; renderer drift 0 | optional | - |
| External sources re-check | 112 | W117 | research-recheck | RS-09, RS-18, RS-22, RS-39, RS-49 and RS-50 primary URLs fetched 2026-11-12 | PASS | All six retrieved; each narrow claim supported with a quoted sentence; applied instructions are project choices | optional | - |
| PR 953-959 diff review | 112 | W117 | pull-request-diff-review | First-parent diffs and bodies of merges `0a726ee1c` to `4cd25b95b` | PASS | Review completed; no protected-work regression; one Important record gap and minor mismatches dispositioned in the table above | required | - |
| Designated sources review | 112 | W117 | research-review | 12 designated sources fetched 2026-11-12 by three read-only agents | PASS | 72 of 72 cells judged S or N, none UNVERIFIED; adoption recorded per source; DS-05 home page HTTP 429, judged from two subpages | required | - |
| Designated sources subpage pass | 112 | W117 | research-review | Five subpages fetched 2026-11-12 | PASS | Template cell S for DS-07, DS-10, DS-11; adoption unchanged except optional H-13; five pages not fetched, recorded | optional | - |
| Follow-up correction review | 112 | W117 | independent-document-review | Fresh-context code-reviewer of commit `968076235` | PASS | APPROVED; all seven claims confirmed; three minor findings fixed (SPEC-0264 counted once, bare verdict values, baseline note); earlier evidence and acceptance rows unchanged by `git diff 36fe501a1 968076235` | optional | - |
| Intake independent review result | 112 | W117 | independent-document-review | Fresh-context code-reviewer of `7f1c82ab9` and `ce56a7256` contents | PASS | APPROVED. Three minor findings fixed: a `main-protection.md` line citation, the superseded Spec prose for criterion 111, and the overstated guard coverage (H-12 added). 9 of 10 citations spot-checked matched | required | Intake independent review |
| W00 remote candidate | 112 | W117 | remote-candidate-quality | PR #960 head `a4b6c327f`, hosted run 43169451623, check rollup read on 2026-11-12 | PASS | `candidate-quality` SUCCESS; CodeQL, GitGuardian and triage SUCCESS; `main-security` and the greeting SKIPPED as designed for a PR | optional | - |

### Resolution Links

None: nothing was recorded here before this Task moved to the common form.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 112 | accepted | W00 v14.7 intake assessment, Intake document checks result, Intake independent review result, PR 953-959 diff review, Designated sources review | Owner accepted on 2026-11-12 in this chat. Handoffs H-04 (13 roles), H-06 to H-10 and H-12, OPEN-04 (BLOCKED_EVIDENCE) and OPEN-08, 10, 13 (UNVERIFIED) stay with their named owners | SPEC-0212 TSK-0059 |

### Remaining Conditions

None for this Task. The owner accepted criterion 112 on 2026-11-12, and the
common form migration this Task started finished in W03 (TSK-0058, pull
requests #967 to #987). Each remaining item has a named receiving owner and runs in that
owner's own Task:

- H-07 (W04): the Registry `common` heading-name keys.
- H-05 is done; H-08 and H-12 (W05); H-09 and H-10 (W06).
- OPEN-09 and OPEN-11 (W05), OPEN-12 (TSK-0052), OPEN-13 and OPEN-14 (W06),
  OPEN-08 and OPEN-10 (W10, UNVERIFIED, not inspected here).
- OPEN-04: BLOCKED_EVIDENCE for the two-file byte comparison only; no product
  work depends on it.

#### Review and Completion

Closed on 2026-11-13, before W04 starts. Criterion 112 is accepted and every
required non-PASS observation is resolved by a later PASS, so the Task closes
as `completed`. TSK-0058's W03 close-out called this Task terminal while it
was still in progress; this update makes that true and records H-04, H-06 and
H-13 as done.

## Handoff

### Promotion Receipt

The intake and its corrections landed in #960. Its W03 handoffs landed in
pull requests #967 to #987, recorded in TSK-0058.

### Next Owner

The current owner is @buenhyden. W04 owns H-07, W05 owns H-08, H-12, OPEN-09
and OPEN-11, W06 owns H-09, H-10, OPEN-13 and OPEN-14, and W10 owns OPEN-08
and OPEN-10.
