---
title: "P00 Current Workspace Reconciliation Task"
version: "0.2.2"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-24"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0098"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-20"
---

# P00 Current Workspace Reconciliation Task

## Scope

### Objective and Parent

Own criterion 154 and W170 under the [Spec](../spec.md) and [Plan](../plan.md):
reconcile current Docker implementation, exclude evidenced completed work and
route remaining work. This is the existing Spec Package's execution record,
not a separate completion ledger. TSK-0097 owns a different pending criterion
and is preserved.

### Inputs and Authority

The current direct P00-RECONCILE 1.1.0 request authorizes this bounded
reconciliation and its commit, push, PR and merge after checks. Current external
inputs come only from `_workspace/workspace_governance_remediation_1_1_0_20261120/`:
README, P00, manifest, execution contract, confirmed decisions, questions,
sources, D00, baseline-4.2.0 and Docker profile/findings. Its decision-update,
retention policy and D01 inform the changed-scope and P01-maintenance comparison.
No other workspace profile, live repository, previous package or original ZIP
is required or read for this pass. Supplied external research summaries are
reused; no new web investigation or native runtime probe is needed for P00.

The following initial observations and E01–E16 describe the earlier 1.0.0
reconciliation. They remain dated evidence, not current state or new authority.

Observed root: `/home/hyunyoun/data/hy-home.docker`; Git common directory:
`/home/hyunyoun/data/hy-home.docker/.git`; branch: `main`; HEAD and Docker
profile baseline: `ef7b6eed51de19da72fb2c8230b02428333218dc`. Initial tracked
and untracked Git status was empty; ignored active inputs remain present.
`git log <profile-sha>..HEAD` returned no commits. No checkout, clone or reset
was performed. Installed CLI versions: Codex 0.169.0, Claude Code 2.1.328;
these version reads do not observe native hook or worker behavior.

The native request revision is `54a8b51511bf6bda22fa23270bb26252`, session
`01a1f47d-2e14-7c32-b0f7-008007421623`. Brief `P00-RECONCILE-docker` has
revision 1 and covers only this Task, the Spec and Plan. The first bind
could not write the local consistency state in the restricted environment;
the approved local retry succeeded. This binding records scope consistency,
not authorization or a new SHA approval requirement.

Current root and common directory are unchanged. The actual input branch is
`codex/p01-ci-evidence`, HEAD `b8ddeee632ed44dc4ecb2cda0e29d3c586618e1f`,
with no staged, unstaged or untracked Git changes. Remote main read-back matches
that HEAD. The branch's existing ahead marker is the integrated merge commit,
not uncommitted work. Preserve the current checkout; publish this P00 logical
diff under remote delivery ref `codex/p00-reconcile-1-1-0`, without checkout,
clone, reset or force push.

Current request revision `8a47b6f389dc93e35b40e013be777bfd`, session
`01a1f47d-2e14-7c32-b0f7-008007421623`, brief
`P00-RECONCILE-docker-1.1.0` revision 1 binds only this Task, Spec and Plan.
One document writer owns those paths; the two decision/keep investigators
were read-only. `decision_revision: "2026-11-20"` applies to this actual P00
comparison. It does not stamp unperformed later stages as reviewed or accepted.
Fresh version reads still report Codex CLI 0.169.0 and Claude Code 2.1.328.
Codex warned that PATH aliases could not be created in the restricted read-only
location but returned its version with exit 0; no native feature success or
trust state is inferred from either version command.
After commit `51d0c460f15b89ca994d61814766a3c2d8f3e680`, brief revision 2
binds a result-only update to this Task. The reviewed Spec/Plan and all runtime
source are unchanged; no parallel writer or temporary progress file exists.

## Execution Log

### Work Performed

#### Baseline and PR reconciliation

The initial authenticated GitHub reads confirmed PRs 1124 and 1125 merged; PR 1125's
merge commit equals local HEAD. Its reported venv run passed 210 modules;
that is prior repository/PR evidence, not a new test run. PR 1125 completes
the environment and maintenance document creation and the fenced-heading
link fix; neither needs rebuilding. PR 1124's 558 moves and later acceptance
of criterion 152 do not activate the final identity baseline.

The current open PR search returned 1047 (container digests) and 1048
(AWS CLI image). Their changed-file lists cover infrastructure images,
backup images, the update ledger and version projection. Neither changes
P00 documents or the analysis implementation. Recheck their installed/runtime
impact before P14/P16 observations; an open proposal is not local source.
No remote state was changed.

Current authenticated reads additionally confirm PR1126 and PR1127 merged.
They integrate the P00 prerequisite and P01 implementation/corrections, then
the P01 receipt; only 26 tracked paths differ from profile `ef7b6eed`.
[TSK-0099](tsk-0099-p01-ci-routing.md) E33–E35 records actual hosted validation
and delivery, including run 44576522487 and merge receipts 16d2be3f/b8ddeee6.
Its criterion 155 remains pending owner acceptance; that is not an unfinished
implementation. Current open PRs remain 1047/1048. Fresh changed-file reads show
only images, Compose declarations, update ledger and version projection, with
no P00 document overlap. They remain separate proposals, not current runtime.

#### Source ownership and consumers

Tracked paths were enumerated with `git ls-files`/`rg --files`; only relevant
owners and consumers were read. These routes identify the current surfaces,
not a claim of semantic review or successful execution of every service.
Paths below are repository-relative.

| Surface and actual owner | Consumers and P00 disposition |
| --- | --- |
| `docs/00.workspace/01.project/glossary.md`, `02.architecture/01.descriptions/0027-agent-governance-canonical-adapter.md`, `0030-document-lifecycle-governance.md`; `02.architecture/02.decisions/0063-numbered-folders-and-workspace-ownership.md` | Bootstrap, agent knowledge, Registry and document parsers; retain completed workspace/product separation and numbered paths. |
| Workspace `03.process/{sdlc,documentation-protocol,git-workflow,github-governance}.md` and `04.quality/{quality-standards,approval-boundaries,task-checklists}.md` | Humans, agents, gate controller and validators; P03/P05 reconcile rule-owner wording and new cleanup meaning in place. |
| Workspace `05.environment/onboarding.md`, `06.maintenance/harness-maintenance.md` | Locked venv onboarding and memory/session/forecast/dispatch/observe operators; retain content, route draft promotion and executable authority to P03/P05. |
| `docs/01.requirements/0024-agent-governance-standardization.md`, `0026-document-retention-and-retirement.md`, `0027-home-development-host.md`; product `docs/02.architecture/01.descriptions/0031-home-development-host.md` | SPEC-0212, architecture and product operators; preserve live-service, confidentiality, recovery and evidence boundaries. |
| SPEC-0212 Spec, Plan and Tasks 0076–0099 | Gate, delivery, brief, memory, capture, analysis, forecast, dispatch, review, observe, cleanup and acceptance evidence; this Task routes only current deltas and reuses P01's completed implementation. |
| Stage 05 Guide/Policy/Runbook 0021 under domain `10.platform-and-backup`, including `docs/05.operations/03.runbooks/10.platform-and-backup/0021-backup-and-restore.md` | `scripts/manifest.yaml` and mutating operational CLIs; RUN-0021 retains runtime authority until a valid workspace owner is admitted. Product backup and memory exclusion remain here. |
| `docs/90.references/{01.research,02.audits,03.data}/`, `docs/98.archive/README.md` | Dated evidence and disposition navigation; no new normative owner, no Stage 98 body or historical rewrite. |
| `docs/99.templates/registry.json`, `01.contracts/{document-profile.schema,document-frontmatter.schema,document-role-design}.json`, `02.templates/03.specs/{spec,plan,task}.template.md` | Metadata, links, lifecycle, identity and template consumers; reuse existing forms, leave prepared baseline inactive until P17. |
| `.agents/governance/{bootstrap,agentic,workflows,environment-constraints}.md`, Provider Registry and canonical roles/skills/knowledge/prompts | `.claude/provider.md`, `.codex/provider.md`, provider renderer, generated role/hook consumers; preserve canonical ownership and actual runtime limitations. |
| `scripts/manifest.yaml`, `scripts/lib/document_governance/`, `scripts/validation/check-script-manifest.py` | Existing metadata, link, corpus, manifest and gate entrypoints; P01/P03/P05/P17 update affected consumers with their owner changes. |
| `.github/workflow-contract.yml`, `.github/workflows/ci-quality.yml`, `scripts/lib/gate/`, `.pre-commit-config.yaml`, `scripts/hooks/{agent-event-hook,pre-push-guard}.sh`, `scripts/lib/hooks/` | CI candidate selection, local hook chain, brief and capture; preserve candidate provenance and fail-closed results, repair only measured/confirmed deltas. |
| `scripts/operations/{agent_memory,session_analysis,task_forecast,work_dispatch,lab,observe}.py`, `scripts/lib/ops/memory_cli.py` | Hook adapters, maintenance commands, scheduled units and focused tests; exclusions and repair scope follow the findings below. |

#### Findings and exclusions

Keep means the same requirement, consumer and authority boundary already
exists. Prior native evidence is explicitly repository-recorded. A source
defect below remains repair work even if its earlier criterion was accepted.

| Finding | Disposition and current source | Reused implementation and verification; remaining delta |
| --- | --- | --- |
| F-DKR-001 | Supplement: confirmed defect, `session_capture.py:70`, `session_analysis.py:121–140,309–325` | Keep redaction, retention, lease fencing and existing analysis tests. Second-resolution `captured_at > start` loses later same-second events. P10 adds nonreused ingest sequence, fixed high watermark and atomic cursor; test late/concurrent insert, clock reversal, retention, retry, failure and cancellation. |
| F-DKR-002 | Supplement: confirmed defect, `session_analysis.py:238–279` | Keep candidate decisions and lease handling (`test_session_analysis.py`). Frequency accumulates while source IDs are replaced by the latest window's capped list. P10 supplies unique candidate/event provenance and retention/promotion semantics, with multiwindow and duplicate tests. |
| F-DKR-003 | Keep; `.github/workflow-contract.yml`, `ci-quality.yml`, gate/document libraries and TSK-0099 | PR1126/1127 deliver five consumer regression groups, shared authenticated candidate plan, changed/inbound checks, immutable parsing/history reuse and exact optional Hermes bindings. TSK-0099 E33 records routing/core/documents/aggregate PASS in run 44576522487; E11 retains same-input selection/parse measurements without total-speedup or p95 claims. Exclude P01 reimplementation. Owner acceptance remains pending. |
| F-DKR-004 | Unobserved, `.pre-commit-config.yaml`, `pre-push-guard.sh` | Existing staged hooks and outgoing-ref guard do not require full tests. P02 measures the actual user's hook/tool/transport delays before assigning a fix; partial staging, new/multiple/deleted refs and empty changes stay protected. |
| F-DKR-005 | Supplement, `_workspace/README.md:61–70`, TSK-0094 | Clean bootstrap without the old package is prior evidence. Retaining completed outputs and a fixed scaffold count do not satisfy the new rule. P15 removes only completed task-owned temporary outputs; preserve active inputs, tracked scaffold and durable memory; P17 removes this package last. |
| F-DKR-006 | Supplement, quality standards `:237,648–652`, current glossaries | Keep the completed taxonomy and meaningful vocabulary. `.agents`-only `rule_owner` prose conflicts with actual docs00 owners. P03 assigns common vocabulary to target `.agents/knowledge/glossary.md` and workspace terms to docs00, updates every consumer, and retires the replaced agent-only owner without an alias authority. Target glossary is currently absent. |
| F-DKR-007 | Supplement, draft onboarding/maintenance, `check-script-manifest.py:292–301,1083`, TSK-0097 | Keep created guides and locked venv instructions; 210-module success is prior TSK-0097 evidence. P03/P05 define/admit an active workspace maintenance owner before switching manifest authority; RUN-0021 remains valid meanwhile. Reject draft authority and verify active resolution. |
| F-DKR-008 | Keep completed moves; new final transition, TSK-0096 and Registry identity namespace | Preserve 558 moves, criterion 152 acceptance and current service meaning. `baseline-1` is active, `baseline-2` prepared; SPEC-0001 was only rehearsed. P17 consolidates valid obligations, then renumbers/resets allocation and validates current consumers. Confirmed Q-01 adds removal of selected obsolete content from manageable remote-ref history and related local Git residue, with D17 rehearsal/expected-ref safeguards; ref names and valid product meaning survive. |
| F-DKR-009 | Keep core, `agent_memory.py:30,124–150`, TSK-0082 evidence `:227–230` | Schema 3, common-dir store, CAS, source pin/invalidity, capacity and rollback journal have tests in `test_agent_memory.py` and repository-recorded Claude→Codex→Claude/stale-write evidence. Exclude core rewrite. P09/P10 implement only new promotion/provenance, session lifetime and supported native seams under Q-02/Q-03; reviewed current memory validity is separate from session TTL. P17 handles the active baseline. |
| F-DKR-010 | Unobserved current external state; preserve recorded failure, TSK-0095 runtime remainders | The last record for 138 lists 30 locked R2 copies and snapshot-content observation; 148 requires a daily successful backup within budget. Those are historical counts/conditions, not fresh external observations. Prior deletion was FAIL, not missing implementation. P16 reads current metadata/results; Q-01 does not extend to locked backups. Never bypass locks or infer success from elapsed time. |
| F-DKR-011 | Supplement, `task_forecast.py:257–316`, TSK-0089 | Keep ordered P30/P50/P80, immutable prestart forecast, censoring, pinball/Wilson and sample disclosure (`test_task_forecast.py`). Type-only score filtering mixes time basis/reference class; policy edition is absent. P11 separates those axes and tests small N. Twenty observations are not an implementation-completion gate. |
| F-DKR-012 | Keep shell core; supplement new scope; native route unobserved, TSK-0090 | Keep DAG, leases, worktrees, cancellation and patch-integrity tests. Actual shell observations were 36.7/40.9 seconds, N=1 each, with cancellation; they prove no general speedup or OS isolation. Confirmed Q-03 adds supported Codex/Claude provider interfaces, real workers and aggregate budgets in P12; the past shell-only choice is not a current exemption. |
| F-DKR-013 | Keep review rules, `.agents/governance/workflows.md:64–94`, TSK-0091 and provider adapter | High independent, medium nonimplementer and low author review plus changed-slice rereview already exist. Preserve enforced read-only-parent controls and prior P01 review evidence for its unchanged scope. P06 checks the new Q-03 provider boundary and review timing. Known spawned/desktop write failures remain failures; historical criterion 135 not-required does not exempt the new native obligations. |
| F-DKR-014 | Keep selection; supplement aggregate admission; live LAB unobserved, `lab.py:644,712–766`, TSK-0093 | Existing negative cases, 108 regressions and 89/89 closure comparison are recorded evidence. Keep explicit service closure, running union, wildcard/whole-stack refusal and LAB limit. P07/P12/P14-DOCKER add shared admission across workers; existing tests do not prove concurrent admission. Live LAB was declined, not accepted. |
| F-DKR-015 | Keep, documentation protocol, `semver.py`, `document-role-design.json` | Numeric document X.X.X and Release Record removal already have Registry/SemVer tests. Exclude reimplementation. P04 repairs only actual form/section/link drift; preserve the distinct product tag, CHANGELOG and release workflow purposes. |

#### Obligations and dispositions

The old stage names in `baseline-4.2.0.md` map to the ordered sequence below;
their prompt receipt is not completion. No old prompt needs replaying.
TSK-0095's accepted criteria 134, 139–147, 149–150 and prior accepted
122–133/136–137 remain dated decisions. Criterion 141's scheduled catch-up
was observed, but does not waive the newly confirmed cursor/provenance bugs.
Criteria 138/148 retain their separate operational conditions. Criterion
135's withdrawal and the shell-only worker choice remain dated user decisions,
but no longer exempt the newly expanded Q-03 scope. Declined live LAB is not
silently accepted or converted into whole-stack execution; memory backup
exclusion remains valid. TSK-0097's criterion 153 and
CodeQL dismissal remain with its owner; P00 neither closes nor retries them.

Older ID-preservation and Q07-wait language describes prior phases. The
current request assigns final consolidation/identity reset to P17, after
surviving obligations are promoted; P00 changes no IDs or allocators. Earlier
permission to keep completed temporary outputs is superseded only for this
request's cleanup scope, through P15/P17. P03/P05 own maintenance-authority
and glossary conflicts, P10 owns confirmed analysis defects. No obligation is
dropped by retiring its former document. Other active product Tasks remain
outside this unit; another repository's work is not copied or accepted here.

The previous corpus readiness report also keeps SPEC-0204, SPEC-0212,
SPEC-0218 and SPEC-0263 not-ready. SPEC-0212 retains older in-progress Tasks,
unaccepted criteria, unresolved required evidence and missing promotion
receipts for the two document schema contracts. Each obligation stays with
its existing Task and durable owner: P05 reconciles disposition and promotion,
P16 verifies current evidence, and P17 retires only after that handoff. This
Task does not turn those packages green or create a replacement ledger.
Its historical FAIL rows for owner-withdrawn criterion 135 do not revoke that
historical not-required decision. The new Q-03 native-review obligation is
separately routed to P06/P07/P16, using enforced routes and equivalent existing
evidence where valid, rather than reopening or rewriting terminal Tasks.

All declared source paths in the fifteen matching findings still exist.
Git comparison with profile `ef7b6eed` shows only F-DKR-003's declared paths
changed. The other source evidence is reused for unchanged consumers, with
the Q-01–Q-03 semantic changes below explicitly added. The requested eleven
previously merged work items are not replayed; concrete existing Task and
acceptance receipts determine reuse, not a new fixed-count completion test.
Native support, external lock state and new retention behavior are not proved
by this source comparison or by the package checker.

#### Ordered follow-up

Use the Docker order from the matching manifest. Each row is planned work,
not an executed prompt or a new standing completion gate. The listed role
owns its bounded change; later Tasks record actual checks and acceptance.

| Order / owner role | Exact starting consumers and changed scope | Verification and boundary |
| --- | --- | --- |
| P01-CI-ROUTING / ci-cd-engineer | Maintained implementation and current TSK-0099 source/evidence; F003; no implementation delta in matching D01 | Reuse actual tests/review/run 44576522487 and PR1126/1127 receipts. Owner acceptance stays pending; do not rerun the prompt or unchanged regression suites. |
| P02-LOCAL-FEEDBACK / qa-engineer | Pre-commit config, pre-push guard and actual installed hook chain; F004 | Measure cold/warm local stages without content exposure; preserve ref and partial-stage failures. |
| P03-OWNERSHIP / doc-writer with rules-engineer review | Existing docs00/agent/provider owners, target glossary, manifest owner contract; F006/007 | Semantic single ownership, real links/anchors, rule-owner resolution and provider parity. |
| P04-TEMPLATES / doc-writer | Stage 99 Registry/forms, metadata/link consumers and common document contract | Actual profile/section/version/link behavior; retain F015 core and product release semantics. |
| P05-DOCS-SDLC / doc-writer | Existing requirements/architecture/Spec/operations owners and maintenance authority | Preserve obligations and acceptance axes; draft-authority rejection then active consumer resolution. |
| P06-INDEPENDENT-REVIEW / rules-engineer | Workflows, quality policy, authored provider adapters and supported actual review route; F013/Q-03 | Preserve risk-based review; prove permitted reads, enforced forbidden-write refusal and actual result on the supported native path. Equivalent valid evidence may be reused; no universal two-reviewer rule. |
| P07-ENVIRONMENT / infra-implementer | Workspace environment/maintenance, `lab.py`, work-dispatch admission; F014 | Cross-worker resource/lease refusal and explicit dependency closure; only necessary isolated services. |
| P08-NATIVE-BRIEF / hook-developer | Existing request brief, tool payload, dispatcher and provider hook consumers | Request updates, withheld actions, resume/compact and actual supported event delivery; synthetic and native reported separately. |
| P09-MEMORY / hook-developer | Existing shared memory/CLI, source validity, reviewed promotion seam and Q-02/Q-03 consumer changes; F009 | Preserve engine/CAS and equivalent cross-provider evidence; verify only changed promotion, content-expiry and actual native seams. |
| P10-SESSIONS / hook-developer | Capture policy/schema, analysis cursor/candidates, scheduled-unit names, reviewed promotion; F001/002 and Q-02/Q-03 | Repair known cursor/provenance defects; selected redacted request/final-response/needed tool results, bounded summaries, 30/90-day policy and actual native/scheduler results. New periodic external-analysis budget is zero; do not confuse it with bounded Q-03 observations. |
| P11-FORECAST / eval-engineer | `task_forecast.py` and its existing tests; F011 | Separate type/time basis/reference class/policy edition; honest small N, no forced corpus/sample count. |
| P12-PARALLEL / hook-developer | `work_dispatch.py`, supported Codex/Claude adapters and shared admission; F012/014/Q-03 | Preserve shell core; verify real native workers, actual permissions/results, cancellation, integration and aggregate limits under current account/model/finite bounds. |
| P13-OBSERVABILITY / eval-engineer | `observe.py`, native capture/analysis/dispatch/forecast and review/gate evidence; Q-02/Q-03 | Connect real events and failures without raw transcript copies; distinguish billed unknowns, estimates and observed costs. |
| P14-DOCKER / infra-implementer | Current explicit service controller, affected Compose dependencies and worktree/environment consumers | Recheck open image PR impact, static render first, scoped service failures and cleanup; no whole-stack start. |
| P15-CLEANUP / doc-writer | `_workspace/README.md`, current maintenance owner and task-owned temporary artifacts; F005/Q-01 | Ownership-scoped cleanup and final deletion classification; preserve permanent memory, active tasks and required package until P17. |
| P16-ACCEPT / workflow-supervisor | This sequence's actual Tasks and TSK-0082/0092/0095 remainders; F010 and changed decisions | Check every remaining required native/runtime obligation and 138/148 current metadata/results; failures cannot be waived or hidden as observation-only deferral. No P17 readiness while required residuals remain. |
| P17-FINAL-CUTOVER / doc-writer with rules-engineer review | Valid active owners, Registry/identity/history/link consumers, memory baseline and confirmed Q-01 remote/local Git scope; F008 | After required preparation/acceptance, promote obligations, renumber and verify current state; rehearse exact history removals, preserve ref names/current product meaning, apply expected-ref updates and freshly verify remote refs, then related local residue and package cleanup. Hosting/fork/locked-backup copies are separate. |

### Blockers and Decisions

No unresolved additional conflict blocks P00. Q-01–Q-04 are confirmed by the
matching `decisions-20261120.md`; do not reask their basic choices or revive
OPEN01–14. This Task updates reconciliation only; later owners implement
the changed durable policy and consumer behavior together.

- Q-01: final P17 includes selected obsolete content in manageable remote Git
  history and related local residue. Preserve branch/tag names and valid tip
  meaning. D17 requires isolated rehearsal, exact refs/expected OIDs, scoped
  application and fresh verification. PR bodies/reviews/comments, blanket tag
  deletion, Actions artifacts, other hosts/forks and locked backups are excluded.
  Hosting-managed PR refs/caches/server objects are a separate reported boundary.
- Q-02: P09/P10 implement selected redacted requests/corrections/final responses
  and necessary tool results; redact before persistence, summarize wider output
  and recheck it, and create no extra raw transcript copy. Body retention is
  30 days, summary/metadata 90 days, with stricter compatible limits retained;
  current-memory validity is separate. `session-retention-policy.json` is
  designed, not deployed. Current ENVIRONMENT-CONSTRAINTS-R136–R138 still limit
  capture to prompts/metadata, forbid replies/tool I/O and use one 90-day rule:
  this is explicit P09/P10 correction work, not a new question or success.
  Preserve local deterministic analysis; new external periodic-analysis
  incremental budget is zero. That is distinct from Q-03 native observations.
- Q-03: the previous shell-only and native-observation deferrals do not exempt
  current supported Codex/Claude briefing, enforced read-only review, common
  memory, capture, real parallel workers and event/result correlation. Reuse
  equivalent valid observations; later P06–P10/P12/P13 use current accounts,
  installed models and finite limits. No new account/subscription, unlimited
  calls, permission bypass or whole-stack start is authorized by implication.
  Known permission failures must be repaired, not renamed unobserved.
- Q-04: the Blog generic-example/actual-internal-reference decision has no
  Docker publication implementation scope. Do not import another workspace's code.

Only an actually discovered protected-ref/signature/consumer conflict, an
out-of-account paid capability or ownership conflict would need a new scoped
question. None was found in this P00 read-only comparison.

#### Lifecycle Events

The initial Task started at draft. This 1.1.0 pass reuses that nonterminal
record; no terminal Task body or historical acceptance is rewritten. The
work and checks remain separate from the still-pending owner acceptance.

## Verification Evidence

### Results

Shell checks run through `rtk`; document validators use the existing locked
venv. Inline assertions compare the matching findings and Docker manifest
order with this Task and check actual source paths. The future glossary
target is explicitly absent, rather than treated as an existing input.
SPEC-0212 uses the Registry's recorded generation 7: its evidence and
acceptance columns remain the registered nine/five-column forms. The current
template's expanded columns apply to packages starting at SPEC-0271. Tool,
exit and observation method are retained in Location for this package.

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 154 | W170 | pwd; git rev-parse; git status --short; git log profile-sha..HEAD | Initial HEAD ef7b6eed51de19da72fb2c8230b02428333218dc | PASS | Git observation, exit 0: same baseline, empty status | required | - |
| E02 | 154 | W170 | Search open/merged PRs; inspect 1124/1125; list 1047/1048 files | Current GitHub PR metadata and changed-file lists | PASS | Authenticated connector observation; no process exit: Baseline and PR reconciliation | required | - |
| E03 | 154 | W170 | Inline P00 source-path, finding-coverage and Docker-order assertions | Initial Task working copy | FAIL | Python 3.12.3, exit 1: wrong guessed RUN-0021 domain; actual tracked path is 10.platform-and-backup | required | - |
| E04 | 154 | W170 | Inline P00 source-path, finding-coverage and Docker-order assertions | Corrected Task and matching manifest/findings | PASS | Python 3.12.3, exit 0: all findings, current evidence paths and exact Docker follow-up order; future glossary target explicitly absent | required | E03 |
| E05 | 154 | W170 | .venv/bin/python scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD --changed-path docs/03.specs/0212-request-baseline-and-reconciliation/spec.md --changed-path docs/03.specs/0212-request-baseline-and-reconciliation/plan.md --changed-path docs/03.specs/0212-request-baseline-and-reconciliation/01.tasks/tsk-0098-p00-reconcile.md | Initial three-file working copy over HEAD ef7b6eed | FAIL | Locked venv Python 3.12.3, exit 1: invalid W170 dependency text and non-draft initial Task; corrected | required | - |
| E06 | 154 | W170 | .venv/bin/python scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD --changed-path docs/03.specs/0212-request-baseline-and-reconciliation/spec.md --changed-path docs/03.specs/0212-request-baseline-and-reconciliation/plan.md --changed-path docs/03.specs/0212-request-baseline-and-reconciliation/01.tasks/tsk-0098-p00-reconcile.md | Corrected dependency/lifecycle, expanded Task tables | FAIL | Locked venv Python 3.12.3, exit 1: expanded evidence columns belong to generation 8, not this recorded generation 7 package; corrected to registered columns | required | - |
| E08 | 154 | W170 | .venv/bin/python scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD --changed-path docs/03.specs/0212-request-baseline-and-reconciliation/spec.md --changed-path docs/03.specs/0212-request-baseline-and-reconciliation/plan.md --changed-path docs/03.specs/0212-request-baseline-and-reconciliation/01.tasks/tsk-0098-p00-reconcile.md | Corrected three-file working copy over HEAD ef7b6eed | PASS | Locked venv Python 3.12.3, exit 0: selected 3, violations 0, transition overrides 0 | required | E05, E06 |
| E07 | 154 | W170 | .venv/bin/python scripts/validation/check-document-corpus-lifecycle.py --readiness | Initial Plan/Task working copy | FAIL | Locked venv Python 3.12.3, exit 3: invalid Spec Package; readiness unavailable | required | - |
| E09 | 154 | W170 | .venv/bin/python scripts/validation/check-document-links.py --mode all | Corrected three-file working copy | PASS | Locked venv Python 3.12.3, exit 0: zero failures/warnings; alignment and commands also independently passed | required | - |
| E10 | 154 | W170 | .venv/bin/python scripts/validation/run-ci-gate.py --profile changed --explain | Local documentation diff | PASS | Locked venv Python 3.12.3, exit 0: metadata, candidate preflight, links, lifecycle and existing P03/P11 Hermes integrity leaves selected; explanation executes no leaf | required | - |
| E11 | 154 | W170 | Review P00 contract, finding coverage, owner paths, evidence and corrected lifecycle/dependency delta | git diff HEAD plus new Task; corrected delta reviewed separately | PASS | Independent code-reviewer in behavioral read-only scope; corrected delta approved, no actionable finding; checks and acceptance stay separate | required | - |
| E12 | 154 | W170 | graphify update . | Current local source | PASS | Installed Graphify AST-only, exit 0: navigation rebuilt; SQL/HCL parser dependencies missing, no semantic document refresh; graph is not source authority | optional | - |
| E13 | 154 | W170 | git diff --check | Current local documentation diff | PASS | Git, exit 0: no whitespace errors; exactly two tracked edits and the new Task, with no initial user edit to overwrite | required | - |
| E14 | 154 | W170 | .venv/bin/python scripts/validation/check-document-corpus-lifecycle.py --readiness | Corrected dependency/lifecycle, before generation-7 table correction | FAIL | Locked venv Python 3.12.3, exit 3: invalid Spec Package; readiness unavailable; equivalent corrected rerun follows | required | - |
| E15 | 154 | W170 | .venv/bin/python scripts/validation/check-document-corpus-lifecycle.py --readiness | Corrected generation-7 three-file working copy | PASS | Locked venv Python 3.12.3, exit 0: corpus and active-stage occupancy violations 0; existing packages, including SPEC-0212, remain not-ready for retirement | required | E07, E14 |
| E16 | 154 | W170 | Inline final Task record, resolution-reference, finding/path-coverage, Docker-order and package-retention assertions using existing registered readers | Corrected Task, Registry and matching remediation inputs | PASS | Locked venv Python 3.12.3, exit 0: registered evidence/acceptance shapes and resolving Check/Work Unit references valid; all findings and follow-up order match; package and next prompt present | required | - |
| E17 | 154 | W170 | Current Git/PR/source/owner reconciliation and installed version reads | HEAD b8ddeee6; matching 1.1.0 Docker inputs | PASS | Clean tracked/untracked state, remote main matches; PR1126/1127 merged and open1047/1048 files do not overlap. All relevant tracked groups enumerated and finding paths exist; only F003 declared source paths changed since profile. Codex0.169.0/Claude2.1.328 version reads exited0; no native claim | required | - |
| E18 | 154 | W170 | python3 tools/check_package.py in matching package root | Remediation1.1.0 manifest, dependencies and confirmed decisions | PASS | Exit0; package links/order/hash and decision propagation valid. This is package verification, not another workspace or native acceptance | required | - |
| E19 | 154 | W170 | Inline finding/path/decision/order/ownership assertions | Initial 1.1.0 three-file diff | FAIL | Exit1; generic path assertion mistakenly required the explicitly absent future .agents/knowledge/glossary.md target to exist. No product-source failure; diagnostic expectation corrected | required | - |
| E20 | 154 | W170 | Inline finding/path/decision/order/ownership assertions | Same three-file scope; declared future target checked absent | PASS | Exit0; every finding has one disposition, actual source paths exist, reviewed decision revision and maintained P01 are explicit, exact Docker order/next P02 and owned files valid. No fixed corpus-count gate or persistent test file created | required | E19 |
| E21 | 154 | W170 | .venv/bin/python scripts/validation/check-document-metadata.py --mode check-changed --base-ref b8ddeee632ed44dc4ecb2cda0e29d3c586618e1f | P00 1.1.0 Spec/Plan/Task diff | PASS | Exit0; selected100 affected records, violations0, transition overrides0. Observed selection, not a fixed-count test | required | - |
| E22 | 154 | W170 | .venv/bin/python scripts/validation/check-document-links.py --mode all --changed --base-ref b8ddeee632ed44dc4ecb2cda0e29d3c586618e1f | P00 1.1.0 changed/inbound graph | PASS | Exit0; selected111 documents, failures0/warnings0. Existing parser/index inputs and P01 scope are reused unchanged | required | - |
| E23 | 154 | W170 | .venv/bin/python scripts/validation/check-document-corpus-lifecycle.py --readiness | P00 1.1.0 current corpus | PASS | Exit0; corpus/occupancy violations0. SPEC0204/0212/0218/0263 remain not-ready with existing obligations and missing receipts; not retirement, service or owner acceptance | required | - |
| E24 | 154 | W170 | Independent review of P00 1.1.0 logical diff | Three owned files over b8ddeee6 and matching decisions | PASS | Fresh-context read-only review: specification/quality PASS, no actionable finding, one logical review round. Dispatch/return clock times and internal wait were not captured. Behavioral read-only investigation is not a P06 native permission probe | required | - |
| E25 | 154 | W170 | .venv/bin/python scripts/validation/run-ci-gate.py --profile changed --explain; git diff --check | Three-file P00 documentation diff | PASS | Both exit0; metadata/preflight/changed-links/lifecycle selected, no irrelevant Hermes or full repository regression. Explanation executes no leaf. No unowned file edit | required | - |
| E26 | 154 | W170 | Hosted P00 candidate-quality and current PR read-back | Commit51d0c460; authenticated merge candidate66faa102; PR1128 run44585803946 | PASS | Routing/core/required aggregate succeeded; documents regression shard correctly unselected/skipped, not executed PASS. Current PR head/base read-back matches51d0c460/b8ddeee6. This is P00's new hosted observation, separate from reused P01 evidence and owner acceptance | required | - |
| E27 | 154 | W170 | Matching tools/next_prompt.py plan with in-memory evidence-backed results | Current P00 comparison/checks complete and P01 retained; no other stage marked performed | PASS | Python exit0; NEXT prompts/P02-LOCAL-FEEDBACK.md, with no earlier entered/runtime-deferral workaround. P00 has actual decision_revision2026-11-20; P01 reuse cites TSK0099/PR1126/1127. No progress file, package mutation or next-prompt execution | required | - |

### Resolution Links

E04 resolves E03's incorrect path assertion; E08 resolves E05/E06's
dependency, lifecycle and table-shape failures; E15 resolves E07/E14's
corpus-load failures. No operational failure was retried; E01/E02 do not
resolve original Task failures.
E20 resolves E19's diagnostic error for the declared future path. E17–E25
describe the current 1.1.0 comparison/checks; older rows remain dated evidence.
P01's actual hosted PASS is reused for unchanged implementation, not relabelled
as a new P00 run or a new native observation.
E26 is the observed PR check of the frozen three-file reconciliation unit;
the result-only receipt receives ordinary document/PR checks without replaying
unchanged implementation tests or independent review.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 154 | accepted | E17, E18, E20, E21, E22, E23, E24, E25, E26, E27 | Owner @buenhyden accepted on 2026-11-24 in this chat during P16 (TSK-0114). | @buenhyden |

### Remaining Conditions

The earlier P00 documentation and focused checks remain dated evidence. This
1.1.0 pass implements only the three owned reconciliation documents; focused
and hosted verification are complete as recorded above. The final delivery
state is read from PR1128 rather than inferred from this receipt. Criterion 154
still awaits owner acceptance. F003/P01 implementation and hosted verification
are maintained, with criterion 155 acceptance separately pending. Confirmed
cursor/provenance and forecast-axis defects remain P10/P11 repair work, not
observation-only deferrals. New capture/retention/native/history obligations
are assigned to their later stages, not claimed implemented by this P00.

## Handoff

### Promotion Receipt

W170/criterion 154 and this existing Task are reused. The original P00 commit
`5b02e40df` was subsequently integrated by PR1126; P01 source and receipt
were integrated by PR1126/1127. This current 1.1.0 change updates the Spec's
current applicability/criterion 154, Plan W170 and this Task's finding,
decision and follow-up map. Requested delivery is a checked Conventional
Commit, push, PR and merge for these three files only. Actual outcomes are
reported separately; no owner acceptance is inferred from delivery.

Current delivery receipt: source commit `51d0c460` is published in
[PR1128](https://github.com/buenhyden/hy-home.docker/pull/1128), with actual
required-check success in
[run44585803946](https://github.com/buenhyden/hy-home.docker/actions/runs/44585803946).
The final result-only receipt uses that same PR. Read back its current-head
checks and merge result at delivery; this does not create another approval
ledger or infer owner acceptance. No one-off progress/QA file was persisted;
the matching package remains available for P02 through final P17.

There is no new runtime or permanent policy body to promote from P00. The
ordered follow-up identifies existing workspace, agent, product and Stage 99
owners that must receive the changed durable meaning with their consumers.

### Next Owner

P01 is maintained using current source and TSK-0099's actual verification and
delivery receipts. The next unperformed input is
`_workspace/workspace_governance_remediation_1_1_0_20261120/prompts/P02-LOCAL-FEEDBACK.md`.
It consumes this P00 decision revision, maintained P01 routing and their actual
results/exclusions. Do not skip unperformed P02–P05 to jump to the decision
update's P06 native sequence, and do not execute any next prompt automatically.

Retain the matching 1.1.0 package through final P17. This pass creates no new
permanent ledger, wrapper or regression script. Remove only any P00-owned
one-off diagnostic/progress file after use; preserve durable memory, existing
tests, unrelated active work and required inputs. No external history or
locked-backup deletion occurs during this P00 reconciliation.
