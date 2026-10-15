---
title: "R13 Reconciliation Follow-up Task"
version: "0.2.2"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0009"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-16"
---

# R13 Reconciliation Follow-up Task

## Overview

### Objective

Revalidate r13 P01-P08 current-source findings and complete the bounded source
corrections assigned by W25. This Task owns criterion 20 only. It does not
reopen TSK-0007's completed P01-P08 execution or its accepted criteria 11-18.

## Inputs and Authorization

The direct r13 request is the attached text with SHA-256
`3a3205dd8787e2a65f1f9eb735be46f2530581af2b8333a79925f800f3775745`.
The source baseline is `e6807a7d16d8b9e180ff58456ab64e4ee721ca69`.

The user initially directed this work to proceed separately and preserve the
existing infrastructure worktree and staged SPEC-0212 Spec, Plan, and TSK-0008
changes. At the `e6807a7` baseline, criterion 19/W24 therefore were not
imported or accepted here. Published main later incorporated those three
documents at `5a88c7937bf427021f2fd0441e04b1011ecd28a9`; this local merge
preserves W24/TSK-0008 alongside W25/TSK-0009 without changing either Task's
acceptance decision.
At the initial snapshot, this Task authorized no remote write, deployment,
credential operation, live service action, or deletion. Those boundaries
remained with the named owner.

The user subsequently authorized the next bounded delivery phase: push the
current branch, open a draft pull request, and observe hosted checks. Before
any main-protection rule change, the delivery owner must observe the actual
required-check identity and review that scoped change. No data, secret,
restart, deployment, or restore target is named by this authorization. The
current host's Docker services are authorized read-only verification targets,
and a non-secret diagnostic may observe native-off effects; those observations
remain with their leaf owners and cannot be inferred from a hosted result.

## Work Log

### Current routing

P02 document-contract, link, lifecycle, and retained-asset findings use the
Stage 99 and document-governance owners. P03 evidence-state findings retain
SPEC-0236, SPEC-0237, SPEC-0241, and SPEC-0243 as their leaf owners. P04 does
not retire archived material without a current consumer, assurance, hold, and
authorization assessment. P08 retains OpenBao runtime, maintenance-window, and
recovery acceptance with SPEC-0243 and its named operations owners.

W25 is the single new Plan assignment for this Task. W16-W23 remain assigned
to completed TSK-0007, so their criteria and evidence are not copied here.
The only source changes in W25 are the demonstrated same-input link-graph
duplicate, repository-file revision binding, CLI shared-store identity, and
immutable legacy-archive binding transport. Workflow-contract amendments are
limited to the one-line changed-path map owned by the W25 memory writer.
The doc-writer exception owns only `.agents/governance/environment-constraints.md`
and `docs/05.operations/runbooks/10-platform-and-backup/0021-backup-and-restore.md`;
it clarifies the full-commit/current-byte source pin without changing a policy
schema, runtime procedure, or historical record.

After an actual required-check readback and scoped review, the doc-writer
exception also owns only `.github/rulesets/main-protection.md` for the
canonical observed protection state. It does not authorize a ruleset mutation.

### Hosted validation authorization and plan

The approved Spec and Plan, completed local source receipts, and the observed
user authorization make this single Task ready for its delivery phase. The
delivery owner will push the current branch, create a draft pull request, and
record the hosted check results against its exact head. It will separately read
the real required-check identity before proposing any main-protection setting.
Hosted checks do not accept criterion 20, select a native-memory target, or
prove a live service, recovery, data, secret, restart, deployment, or restore
operation. The current host's Docker services may be read-only verified, and
native-off effects may be non-secret diagnostically observed; neither result
changes a leaf-owner acceptance decision.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0009 | draft | ready | #hosted-validation-authorization-and-plan |
| SPEC-0212-TSK-0009 | ready | in-progress | #draft-pull-request-and-observational-boundaries |

### Draft pull request and observational boundaries

Draft PR [#506](https://github.com/buenhyden/hy-home.docker/pull/506) was
observed with head `0c598de264c0302f5032738b14ffbefe36b53cc7`, base
`5a88c7937bf427021f2fd0441e04b1011ecd28a9`, and candidate-quality run
`38818745829` / check `116709839952` in progress. This observed direct edge
starts the delivery work; it neither accepts criterion 20 nor records a hosted
result.

Read-only current-host Docker observation found the five named services healthy,
OpenBao status exit `0`, and public health HTTP `200` with TLS verification
`0`. Traefik had the read-only CA mount; Prometheus and Gatus lacked their
declared CA mounts, so their maintenance-window integration is NOT_DEPLOYED.
No secret, raw configuration, log, database, restart, deployment, restore, or
unseal action was performed.

The public Codex CLI feature diagnostic reported `memories=false`; this is only
an effective public CLI feature-boundary observation. It does not establish
desktop-app internal memory-off, project-trust application, or individual native
event delivery. Claude's tracked project declaration was observed, but its
merged effective memory-off remains UNVERIFIED. Sanitized Git resolution gave
the separate worktree and main checkout the same store target path without
opening the database. A proposed `claude doctor` diagnostic was automatically
rejected because it could report authentication state; it was not run.

### Local delivery ledger

| Commit | Logical unit | Actual delivery |
| --- | --- | --- |
| `15ffbca5c28a11dba034757640df597bad779ce9` | Link selection and immutable archive-binding transport | `fix(docs): Preserve archive proofs and parse each source once`; local commit only |
| `141c963cb6bc8677d5b1e4d0098c50ba660b2063` | Repository-file provenance and sanitized Git-context isolation | `fix(memory): Bind provenance and isolate Git context`; local commit only |
| `ff6d33ffaac3215543b2f64e2bf4336e703cbf71` | Published W24/TSK-0008 and W25/TSK-0009 document integration | `chore(merge): Preserve published infrastructure audit records`; local merge only |

The pending Task record and its separate document-only receipt are not a remote
delivery, merge, release, or deployment claim.

### Initial findings

The current source still shows draft authority in SPEC-0236, SPEC-0237,
SPEC-0241, and SPEC-0243 while their Task bodies distinguish stored accepted,
pending, and runtime-unverified evidence. That is an explicit state model, not
a defect by itself. No status normalization follows from this record.

The completed P04 consumer trace identifies SPEC-0240 as an archived,
superseded record with current provenance consumers and retained OpenBao
assurance checks. No one-shot asset is a deletion candidate based only on age,
name, or completed history.

The recorded current inventory contains 2,280 tracked paths, including 1,371
Markdown paths and 386 script/code candidates. This is a classified inventory,
not a semantic audit of every body; the r13 attachment's 573 figure is not
treated as a current exhaustive-audit result. Script-manifest and operations
catalog checks retain all 106 manifest entries and the catalog respectively,
supporting P04 retention without a deletion claim.

Static inspection of `scripts/lib/ops/memory_sources.py` shows that a
repository-file reference's `revision` must be nonempty but is not bound to a
Git object: currentness compares only the worktree content digest. W25 must
reject a bogus revision while preserving the existing digest, tracked-file,
and no-symlink protections. The link selection regression reproduced the
earlier full-superset parse and now proves disjoint current and historical
inputs with exact graph equality.

Static inspection of `scripts/operations/agent_memory.py` shows that
`_common_dir` invokes ambient `git rev-parse --git-common-dir` for the CLI's
own and caller paths. That can resolve a foreign repository and select another
store. W25 must route both resolutions through the sanitized Git runner and
cover that shared-store identity without reading a memory store.

Before correction, the reproduced changed-document metadata failure had a separate source cause:
`_validate_repository_contracts` computes immutable legacy-archive binding, but
`_GenerationBindings` does not return it to the later relation-impact
`validate_record` call. The record is byte- and metadata-identical when bound,
but reports a type mismatch when unbound. W25 transports the existing proof
through `metadata/reference.py`, as confirmed by `Scoped-metadata-GREEN`; it does not modify
the 145 archived records or introduce a new immutable-binding rule.

| ID | P | Path@SHA | Classification | Problem | Disposition | Owner | AC | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R13-001 | P01 | `docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0007-r10-reconciliation.md@e6807a7` | recorded | Criteria 11-18 are already accepted in the completed r10 record. | retain | SPEC-0212 TSK-0007 | 20 | TSK-0007 criterion acceptance rows |
| R13-002 | P02 | `scripts/validation/check-document-links.py@e6807a7` | reproduced | Earlier all-mode selection parsed a full superset after current input. | changed with regression | document-governance link owner | 20 | W25 Link selection RED/GREEN and graph equivalence |
| R13-003 | P03 | `docs/03.specs/{0236,0237,0241,0243}@e6807a7` | static | Draft package status and stored Task acceptance have distinct lifecycle meanings. | retain | each package owner | 20 | current frontmatter and Task records |
| R13-004 | P04 | `docs/98.archive/superseded/03.specs/0240-unseal-backup-exclusion@e6807a7` | recorded | Archived OpenBao history has current provenance consumers and retained assurance checks. | retain | REQ-0026 / SPEC-0242 | 20 | TSK-0007 P04 consumer trace |
| R13-005 | P05 | `scripts/hooks/pre-push-guard.sh@e6807a7` | recorded | Installed-hook and real-push observations remain separate. | retain boundary | hook owner | 20 | TSK-0007 supported dispatcher probe |
| R13-006 | P06 | `.github/rulesets/main-protection.md@e6807a7` | recorded | Protection has strict status enabled but no named contexts; no remote mutation is authorized. | retain boundary | GitHub governance owner | 20 | current read-only protection observation |
| R13-007 | P07 | `scripts/lib/ops/memory_sources.py@e6807a7` | reproduced | Baseline static inspection found `revision` unbound; the old helper accepted a bogus revision in the focused RED check. | changed with regression | W25 memory writer | 20 | Memory revision RED/GREEN |
| R13-008 | P08 | `docs/03.specs/0243-openbao-window-readiness/tasks/tsk-0001-openbao-window-readiness.md@e6807a7` | recorded | Source acceptance does not replace maintenance-window, recovery, or live-service proof. | retain boundary | SPEC-0243 | 20 | existing W0 prerequisites |
| R13-009 | P07 | `scripts/operations/agent_memory.py@e6807a7` | static | CLI common-directory lookup uses ambient Git resolution and can select a foreign repository's store. | changed with regression | W25 memory writer | 20 | shared-store identity regression after sanitized-runner implementation |
| R13-010 | P02/P05 | `scripts/lib/document_governance/metadata/reference.py@e6807a7` | reproduced | Changed-record validation lost an already-computed immutable legacy-archive binding and reported 145 false type mismatches. | changed with regression | W25 metadata QA writer | 20 | focused bound/unbound reference regression; Scoped-metadata-GREEN |

### Local and PR producer map

The link CLI and `test_links.py` are local W25 producers. The memory helper,
`agent_memory.py`, and `test_agent_memory.py` are local producers; the
changed-path map routes their source and `test_agent_governance_ci_routing.py` regression to the
focused agent-governance CI leaf. A clean `--explain` run has no changed-path
selection and is only a routing observation, not an implementation result.
PR-leaf results remain NOT_RUN until the final changed set is evaluated by the
configured workflow. The metadata reference module and its focused test are
local W25 producers; `Scoped-metadata-GREEN` records the final
changed-document metadata result. The final merged metadata receipt is
recorded below; the final PR selector explanation selected three leaves but did
not execute a PR leaf.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Isolated source baseline | 20 | W25 | `git rev-parse HEAD`; worktree and concurrent-worktree read | `e6807a7d16d8b9e180ff58456ab64e4ee721ca69` | PASS | r13 isolated worktree | required | - |
| Active-document baseline | 20 | W25 | `check-document-metadata.py --mode check-active` | `e6807a7d16d8b9e180ff58456ab64e4ee721ca69`; selected 576 | PASS | r13 isolated worktree | required | - |
| Workflow contract baseline | 20 | W25 | Workflow-contract validation | Current source: workflows 5, jobs 7, actions 8 | PASS | r13 isolated worktree | required | - |
| Clean changed-gate observation | 20 | W25 | `run-ci-gate changed local --explain` | Clean isolated worktree | NOT_APPLICABLE | No changed-path selection; routing observation only | optional | - |
| Protection and hook observation | 20 | W25 | Read-only remote and Git configuration inspection | `origin/main` `e6807a7`; strict protection with no contexts; hooksPath and init.templateDir unset | PASS | r13 isolated worktree | optional | - |
| Advisory graph availability | 20 | W25 | Graphify CLI and report discovery | Current source environment | NOT_APPLICABLE | No tracked report or CLI found | optional | - |
| Draft PR observation | 20 | W25 | Read-only pull-request and check observation | PR #506 draft; head `0c598de264c0302f5032738b14ffbefe36b53cc7`; base `5a88c7937bf427021f2fd0441e04b1011ecd28a9`; candidate-quality run `38818745829` / check `116709839952` in progress | PASS | Hosted observation | required | - |
| Current-host Docker observation | 20 | W25 | Read-only current-host Docker preflight | Five named services healthy; OpenBao status exit 0; public health HTTP 200/TLS 0; Traefik CA mount present; Prometheus/Gatus declared CA mounts absent and NOT_DEPLOYED | PASS | Sanitized runtime observation | required | - |
| Native memory boundary observation | 20 | W25 | Public CLI and static native-memory observation | Codex public CLI feature boundary `memories=false`; Claude merged effective setting and provider native-event delivery UNVERIFIED; store target paths equal without database open | PASS | Sanitized native observation | required | - |
| Rejected native diagnostic | 20 | W25 | Proposed `claude doctor` observation | DEFER: automatic review rejected possible authentication-state reporting; command not run | NOT_RUN | Sanitized native observation | required | - |
| Script-manifest observation | 20 | W25 | Script-manifest validation | 106 manifest paths active or retained | PASS | r13 isolated worktree | optional | - |
| Operations-catalog observation | 20 | W25 | Operations catalog validation | Current catalog | PASS | r13 isolated worktree | optional | - |
| Inventory-scope observation | 20 | W25 | Tracked-path inventory | 2,280 tracked paths; 1,371 Markdown; 386 script/code candidates; classification only, not whole-body semantic audit | PASS | r13 isolated worktree | optional | - |
| Pre-merge scoped metadata GREEN | 20 | W25 | `check-document-metadata.py --mode check-changed` | Merge base `e6807a7d16d8b9e180ff58456ab64e4ee721ca69`; selected 5, violations 0, legacy exceptions 0, transition overrides 0 | PASS | r13 isolated worktree | required | - |
| Pre-merge document link alignment | 20 | W25 | Three-document link alignment | SPEC-0212 Spec, Plan, and TSK-0009: 0 findings | PASS | r13 isolated worktree | required | - |
| Pre-merge PR selector explanation | 20 | W25 | Three-leaf PR selector `--explain` | PASS explanation only; no PR leaf executed | PASS | r13 isolated worktree | optional | - |
| Final document integration review | 20 | W25 | Independent document integration review | APPROVED; 0 findings | PASS | r13 isolated worktree | required | - |
| Final merged scoped metadata | 20 | W25 | `check-document-metadata.py --mode check-changed` | HEAD `ff6d33ffaac3215543b2f64e2bf4336e703cbf71`; ref and merge base `5a88c7937bf427021f2fd0441e04b1011ecd28a9`; selected 5, violations 0, legacy exceptions 0, transition overrides 0 | PASS | r13 isolated worktree | required | - |
| Final document corpus lifecycle | 20 | W25 | `check-document-corpus-lifecycle.py --base-ref 5a88c7937bf427021f2fd0441e04b1011ecd28a9` | Violations 0; migrations 5, tombstones 140, preserved 354, decisions 286, recovery rows 374 | PASS | r13 isolated worktree | required | - |
| Final PR selector explanation | 20 | W25 | Three-leaf PR selector `--explain` | PASS explanation; same three leaves selected; no PR leaf executed | PASS | r13 isolated worktree | optional | - |
| Memory revision RED | 20 | W25 | Focused bogus-revision source-pin regression | Earlier helper accepts an invalid revision | FAIL | W25 memory slice | required | - |
| Memory revision GREEN | 20 | W25 | Focused bogus-revision source-pin regression | Current W25 memory slice | PASS | W25 memory slice | required | Memory revision RED |
| Memory helper regression | 20 | W25 | Focused agent-memory tests | 24 tests; 5.273 s | PASS | W25 memory slice | required | - |
| Memory route regression | 20 | W25 | Focused agent-governance route selection | 3 tests; 0.148 s | PASS | W25 memory slice | required | - |
| CI-plan regression | 20 | W25 | Focused CI-plan contract | 45 tests; 14.012 s | PASS | W25 memory slice | required | - |
| Installed hook regression | 20 | W25 | Focused installed-hook tests | 12 tests | PASS | W25 memory slice | required | - |
| Provider renderer regression | 20 | W25 | Provider renderer check | 2 providers; 0 drift | PASS | W25 memory slice | required | - |
| Changed-path route RED | 20 | W25 | CI-plan routing selection | Earlier map: 6 suites, 33 local leaves, 35 PR leaves | FAIL | W25 memory slice | required | - |
| Changed-path route GREEN | 20 | W25 | CI-plan routing selection | Current map: 2 suites, 4 local leaves, 5 PR leaves; PR intentionally omits unittest | PASS | W25 memory slice | required | Changed-path route RED |
| Link selection RED | 20 | W25 | `LinkSelectionScopeTests.test_all_mode_parses_disjoint_current_and_historical_inputs` | Earlier `--mode all` parsed a full superset after current input | FAIL | W25 link slice | required | - |
| Link selection GREEN | 20 | W25 | `LinkSelectionScopeTests.test_all_mode_parses_disjoint_current_and_historical_inputs` | One test passed; 0.261 s | PASS | W25 link slice | required | Link selection RED |
| Link graph validation | 20 | W25 | `check-document-links.py --mode all` | Tracked source: 1,310 documents, 11,677 links, 0 failures, 1 warning (`historical-links-unrecorded`, 2,870), 59 historical documents | PASS | W25 link slice; elapsed 66.09 s, user 52.39 s, sys 5.04 s, max RSS 81,692 KiB | required | - |
| Link graph equivalence | 20 | W25 | One-shot old/new exact graph comparison | `graph_equal=True`; current 1,310, historical superset 1,369, delta 59; parser inputs 2,679 to 1,369 (48.9% fewer) | PASS | W25 link slice | required | - |
| New Task link alignment | 20 | W25 | `build_document_graph(Taskonly) + check_alignment` | TSK-0009: 6 links, 0 findings | PASS | TSK-0009 | required | - |
| W25-style-RED | 20 | W25 | Focused Ruff check | FAIL: unused import/I001 in the link CLI and one link-test formatting finding | FAIL | W25 link slice | required | - |
| W25-style-GREEN | 20 | W25 | Focused Ruff check | Link CLI and link tests pass after formatting correction | PASS | W25 link slice | required | W25-style-RED |
| Documentation commit hooks RED | 20 | W25 | Normal git commit hooks | Initial documentation commit attempt: markdownlint MD029 expected criterion 19, found independently numbered criterion 20 | FAIL | W25 documentation slice | required | - |
| Documentation commit hooks GREEN | 20 | W25 | Normal git commit hooks | Narrow MD029 exception preserved the initial independent allocation; normal hooks passed for `bc6d4990e88bcdbd38789aa840bbc1dcc0134bc0` | PASS | W25 documentation slice | required | Documentation commit hooks RED |
| W25 source security review | 20 | W25 | Independent security review | FAIL: ambient Git, replace-ref, lazy-fetch, and bounded-subprocess helper findings; one narrow memory retry also needs remediation | FAIL | W25 source slices | required | - |
| W25 source security review GREEN | 20 | W25 | Independent security review | Final re-review PASS after shared sanitized Git runner correction | PASS | W25 source slices | required | W25 source security review |
| Memory helper regression final | 20 | W25 | Focused agent-memory tests | 28 tests; 2.938 s; source SHA-256: `memory_sources.py` `86179a3d6690a82d50d2c63dbad1f6250f1c50521dd06704370af78af9a95f5f`, `agent_memory.py` `843a6f414b3682de17d46a42ed1f7f264c8525449bb2712f43032ecc30dfa3f8`, tests `91a38b2565afb8d1931f49a5ddfaf413983e41b7fe34883166d54570fe388b50` | PASS | W25 memory slice | required | - |
| Link full regression | 20 | W25 | `python3 -m unittest tests.lib.document_governance.test_links -v` | 119 tests; 186.254 s | PASS | W25 link slice | required | - |
| Scoped metadata validation | 20 | W25 | `check-document-metadata.py --mode check-changed` | Root final run: 147 failures, including this Task's prior evidence-pair and initial-status contract failures; unchanged frozen archive payloads account for the remaining type mismatches | FAIL | r13 isolated worktree | required | - |
| Scoped-metadata-GREEN | 20 | W25 | `check-document-metadata.py --mode check-changed` | Same five paths; baseline `e6807a7d16d8b9e180ff58456ab64e4ee721ca69`; selected 5, violations 0 | PASS | r13 isolated worktree | required | Scoped metadata validation |
| Metadata full diagnostic cancellation | 20 | W25 | `python3 -m unittest tests.lib.document_governance.metadata.test_reference -v` | Initial full attempt cancelled at 120 s | CANCELLED | W25 metadata QA slice | optional | - |
| Metadata full regression | 20 | W25 | `python3 -m unittest tests.lib.document_governance.metadata.test_reference -v` | 28 tests; 539.585 s; reference source Git blob `7f5b9ce162283caf519db7c981f5d213817ea69c`, test blob `a70eaf6d2b37ac8d12d2986b97c41201b849fd5b` | PASS | W25 metadata QA slice | required | - |
| Metadata targeted regression | 20 | W25 | Targeted propagation, raw-blob-tamper, and lifecycle regressions | 3 tests; 2.410 s | PASS | W25 metadata QA slice | required | - |
| Tool-version observation | 20 | W25 | Local tool version inspection | Python 3.12.3; Ruff 0.16.10; pre-commit 4.6.2; Git 2.43.0 | PASS | r13 isolated worktree | optional | - |
| Remote main observation | 20 | W25 | Read-only `origin/main` diff inspection | `origin/main` advanced to `5a88c7937bf427021f2fd0441e04b1011ecd28a9` by PR #504; only SPEC-0212 Spec, Plan, and TSK-0008 changed, with no source/checker change | PASS | remote observation; separate from e680 baseline | optional | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 20 | pending | Scoped-metadata-GREEN, Memory helper regression final, Link full regression, W25 source security review GREEN, Metadata full regression | Source checks are recorded; this ready Task awaits remote selected-check execution and criterion acceptance. | SPEC-0212 TSK-0009 |

## Review and Completion

This ready Task does not convert static inspection, stored Task evidence,
a merged change, or an unavailable runtime target into acceptance. It completes
only after the required W25 checks pass with the final source input; runtime,
remote, and leaf-owner acceptance stay separate.

The local hook boundary follows [Git hooks](https://git-scm.com/docs/githooks)
and [pre-commit](https://pre-commit.com/); it does not prove a real push.
The no-context protection observation follows GitHub's
[required-status-check semantics](https://docs.github.com/en/pull-requests/reference/status-checks),
which also does not show a selected leaf executed. The link slice preserves
[CommonMark](https://spec.commonmark.org/0.31.2/) and
[GFM](https://github.github.com/gfm/) syntax handling. SQLite backup and page
limits remain source contracts described by the
[online backup API](https://www.sqlite.org/backup.html) and
[PRAGMA reference](https://www.sqlite.org/pragma.html), not proof that a
provider-native memory setting or a live restore has been observed.

The direct user authorization covers local source and documentation correction,
logical commits, branch push, draft pull request, and hosted checks. A protected
main merge remains outside this Task until its required checks and review are
observed. No new skill is required:
available procedure reads were `superpowers` 6.4.2 and `ponytail` 5.2.0;
skill-stocktake, skill-improver, Harness:Evolve, and Harness:Harness were not
available and are not claimed.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Completed r10 Task](tsk-0007-r10-reconciliation.md)
- [Shared memory Task](../../0236-shared-agent-memory/tasks/tsk-0001-shared-agent-memory.md)
- [Hook Task](../../0241-hook-outputs-and-main-push-guard/tasks/tsk-0001-hook-outputs-and-main-push-guard.md)
- [OpenBao window Task](../../0243-openbao-window-readiness/tasks/tsk-0001-openbao-window-readiness.md)
