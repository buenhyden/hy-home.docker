---
title: "Agent Quality and Security Standards"
version: "2.0.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
---

# Agent Quality and Security Standards

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the policy payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose and Scope

##### Objective

Universal quality gate for agent-driven changes in this repository.

###### Authority
<!-- core-payload-level:4 -->

This policy is the canonical owner of change-specific verification, security, reliability, and quality routing under [bootstrap precedence](../../../.agents/governance/bootstrap.md#authority-and-precedence).

##### Applies To

Change-specific verification, security, reliability, generated freshness, and local or hosted quality routing.

###### Exclusions
<!-- core-payload-level:4 -->

None: this document states no exclusion.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| QUALITY-STANDARDS-R1 | Documentation quality grading | Required: grade documentation A-F by the Documentation Quality Rubric | none | none |
| QUALITY-STANDARDS-R2 | Documentation quality grading | Required: hardcoded secrets, broken governance links or contradictory instructions grade F | none | none |
| QUALITY-STANDARDS-R3 | Documentation | Required: instructions are concrete and testable (actionability) | none | none |
| QUALITY-STANDARDS-R4 | Documentation | Forbidden: generic filler (conciseness) | none | none |
| QUALITY-STANDARDS-R5 | Documentation | Required: references match current repository structure (accuracy) | none | none |
| QUALITY-STANDARDS-R6 | Always | Forbidden: committing plaintext credentials | none | none |
| QUALITY-STANDARDS-R7 | Secrets handling | Required: prefer secret managers or mounted secret files | none | none |
| QUALITY-STANDARDS-R12 | Source-controlled configs | Forbidden: plaintext credentials in source-controlled configs | none | none |
| QUALITY-STANDARDS-R17 | npm vulnerability audit | Forbidden: an active npm risk acceptance | CI contract rejects an `npm_audit_acceptance` record | none |
| QUALITY-STANDARDS-R18 | npm vulnerability audit | Required: `leaf.dependency-vulnerability-audit` is the strict `npm audit --audit-level=high` run | none | none |
| QUALITY-STANDARDS-R19 | A new npm acceptance | Required: a reviewed policy amendment naming the advisory, locked chain, owner approval and an expiry no more than 30 days after approval, with negative fixtures | none | none |
| QUALITY-STANDARDS-R20 | Always | Forbidden: treating an acceptance as a vulnerability fix or a branch protection bypass | none | none |
| QUALITY-STANDARDS-R21 | Always | Forbidden: a skipped audit, lower threshold, continue-on-error, blanket package exception or omitted development audit | none | none |
| QUALITY-STANDARDS-R22 | Candidate acceptance | Required: remote PR candidate validation and review by risk own candidate acceptance | none | none |
| QUALITY-STANDARDS-R23 | Main-push security | Required: remains a post-merge observation | none | none |
| QUALITY-STANDARDS-R24 | Recurring QA | Required: cover current document forms, templates, frontmatter, identity, relationships, links, lifecycle and preservation plus the Docker/Compose services, configuration and operations contracts | none | none |
| QUALITY-STANDARDS-R25 | Supporting parser, selector, style controller or release regression | Required: prove one of the current recurring contracts | none | none |
| QUALITY-STANDARDS-R26 | Always | Forbidden: treating an agent answer score, a past migration census or a completed Task's fixed hash as a recurring quality contract | none | none |
| QUALITY-STANDARDS-R27 | Event-specific expectations | Required: remove expectations on a completed document's current status, wording or inventory | none | none |
| QUALITY-STANDARDS-R28 | Retired-symbol assertions | Required: remove contract assertions coupled only to a retired file, helper or symbol | none | none |
| QUALITY-STANDARDS-R29 | Continuing guarantees | Required: current Registry validators and meaningful boundary regressions own them | none | none |
| QUALITY-STANDARDS-R30 | Obsolete expectations | Forbidden: replacing them with another permanent forbidden-name list | none | none |
| QUALITY-STANDARDS-R31 | Generic preserved byte, recovery and compatibility proofs | Required: they remain current contracts | none | none |
| QUALITY-STANDARDS-R32 | Explicit Skill evaluation | Allowed: retain paired task/output/scoring/aggregate evidence outside recurring repository QA | none | none |
| QUALITY-STANDARDS-R33 | Skill evaluation evidence | Required: the evaluation README routes the evidence and agentic policy owns authority and stop conditions | none | none |
| QUALITY-STANDARDS-R34 | Always | Forbidden: treating a representative score as whole-Skill coverage, runtime activation or Task acceptance | none | none |
| QUALITY-STANDARDS-R35 | Behavior changes | Required: focused failure reproduction and regression evidence | none | none |
| QUALITY-STANDARDS-R36 | Wording-only changes | Required: applicable content and style validation | none | none |
| QUALITY-STANDARDS-R37 | Wording-only changes | Allowed: no new implementation tests and no universal coverage percentage | none | none |
| QUALITY-STANDARDS-R38 | Runtime health, live smoke, operator acceptance, backup and restore evidence | Required: it belongs to the approved service Task | none | none |
| QUALITY-STANDARDS-R39 | Always | Forbidden: treating Compose render or static hardening as proof of runtime health, live smoke, operator acceptance, backup or restore | none | none |
| QUALITY-STANDARDS-R40 | SEV1/SEV2 incident | Required: use its incident postmortem | none | none |
| QUALITY-STANDARDS-R41 | Optimizing QA | Required: remove duplicate leaves, separate content checks from validator regression tests, share parsing and Git reads within one run, select by change impact, then reuse only a provably equivalent narrow result matched on the full execution identity | none | none |
| QUALITY-STANDARDS-R42 | Reusing a QA result | Required: a difference in any part of the execution identity makes it a new observation | none | none |
| QUALITY-STANDARDS-R43 | Claiming a QA improvement | Required: compare a reproducible measure before and after | none | none |
| QUALITY-STANDARDS-R44 | Always | Forbidden: calling a change faster without a number | none | none |
| QUALITY-STANDARDS-R45 | Optimizing QA | Forbidden: starting with a large global cache or a new gate | none | none |
| QUALITY-STANDARDS-R46 | A non-functional requirement | Required: name one ISO/IEC 25010 quality characteristic and an ISO/IEC 25023 measure (what, unit, environment, acceptance value) | none | none |
| QUALITY-STANDARDS-R47 | Requirement template | Required: carry the quality characteristic and measure line | none | none |
| QUALITY-STANDARDS-R48 | A characteristic left out | Required: state why it does not apply | none | none |
| QUALITY-STANDARDS-R49 | Always | Forbidden: forcing a threshold on every project | none | none |
| QUALITY-STANDARDS-R50 | Non-functional requirements | Forbidden: adding a separate compliance gate | none | none |
| QUALITY-STANDARDS-R51 | Retiring one-time QA | Required: transfer a continuing guarantee to its current owner, remove callers and registration, remove exclusive helpers, fixtures and tests, then preserve useful actual results in existing Task/history | none | none |
| QUALITY-STANDARDS-R52 | Stage 98 | Required: hold no records; any tracked file there other than the README fails | corpus lifecycle occupancy check | none |
| QUALITY-STANDARDS-R53 | Stage 98 README | Required: check it like any other README | none | none |
| QUALITY-STANDARDS-R54 | Shared libraries under `scripts/lib/` and executable QA owners | Required: retain meaningful test evidence | none | none |
| QUALITY-STANDARDS-R55 | Nonmutating companion library outside the shared surface | Allowed: retain it through a proven current consumer without a dedicated purpose-excluded QA suite | none | none |
| QUALITY-STANDARDS-R56 | Companion library | Forbidden: mutation, missing consumers, unsafe paths or invalid import claims | manifest contract rejects them | none |
| QUALITY-STANDARDS-R57 | Companion library retention | Forbidden: treating it as runtime acceptance | none | none |
| QUALITY-STANDARDS-R58 | Judging library behavioral evidence | Required: use the tracked, admitted test owner and actual API/fixture use | none | none |
| QUALITY-STANDARDS-R59 | Library test organization | Allowed: directory mirroring is the default organization, not a second mandatory evidence source | none | none |
| QUALITY-STANDARDS-R60 | Cross-module or entrypoint test | Allowed: a registered test may own library behavior without a duplicate library smoke | none | none |
| QUALITY-STANDARDS-R61 | Always | Forbidden: source-token bans, test-of-test census scans or retired filename assertions substituting for current mutation, preservation or parser behavior | none | none |
| QUALITY-STANDARDS-R62 | Deleting a check | Forbidden: using age, filenames, test counts or failing results alone as deletion criteria | none | none |
| QUALITY-STANDARDS-R63 | A removed check | Required: has a disposition and any continuing owner | none | none |
| QUALITY-STANDARDS-R64 | Failed required checks | Required: remain failures until repaired or deliberately retired under the approved contract | none | none |
| QUALITY-STANDARDS-R65 | Implementation contradicts its canonical rule | Required: record the conflict, the decision and the change order in the current Task | none | Task record |
| QUALITY-STANDARDS-R66 | Implementation contradicts its canonical rule | Required: change the producer, reader, schema, current guidance and tests in one logical change | none | none |
| QUALITY-STANDARDS-R67 | Implementation contradicts its canonical rule | Forbidden: making the check pass by editing only its test expectation or by only relaxing the rule | none | none |
| QUALITY-STANDARDS-R68 | Always | Forbidden: adopting an unapproved test constant as policy | none | none |
| QUALITY-STANDARDS-R69 | Changing the canonical rule itself | Required: its owner's approval under approval boundaries | none | none |
| QUALITY-STANDARDS-R70 | Authoring | Allowed: explicit formatting may write eligible authored files | none | none |
| QUALITY-STANDARDS-R71 | Authoring | Allowed: focused RED/GREEN and selected read-only lint to diagnose a change | none | none |
| QUALITY-STANDARDS-R72 | Authoring | Required: observe actual installed Git hooks separately from tracked configuration | none | none |
| QUALITY-STANDARDS-R73 | Always | Forbidden: SKIP, fake CI variables or `--no-verify` | none | none |
| QUALITY-STANDARDS-R74 | Local implementation verification | Required: the workflow contract's typed `public_gate.local_only_gate_ids` owns document-library, hook, mocked native and other isolated implementation regressions plus local links | none | none |
| QUALITY-STANDARDS-R75 | Closed hosted-unit set | Required: CI gate-contract, Compose-baseline and repository-integrity regressions run in both selected local verification and hosted candidate validation | none | none |
| QUALITY-STANDARDS-R76 | Inspecting the complementary local-only plan | Required: use `scripts/validation/run-ci-gate.py --profile changed --local-only --explain` | none | none |
| QUALITY-STANDARDS-R77 | A changed owner selects a promoted regression | Required: run `scripts/validation/run-ci-gate.py --profile changed --explain`, then the same command without `--explain` once on the final implementation input | none | none |
| QUALITY-STANDARDS-R78 | Execution route | Required: the shared runner and registered path owners remain the execution route | none | none |
| QUALITY-STANDARDS-R79 | Always | Forbidden: a parallel wrapper or command inventory | none | none |
| QUALITY-STANDARDS-R80 | Result-only Task additions | Required: minimum document checks | none | none |
| QUALITY-STANDARDS-R81 | After commit or push | Forbidden: repeating the local full profile | none | none |
| QUALITY-STANDARDS-R82 | Candidate acceptance | Required: remote PR QA through `scripts/validation/run-ci-gate.py --profile changed` | none | none |
| QUALITY-STANDARDS-R83 | Candidate acceptance | Required: inspect the selected plan and prerequisites before execution | none | none |
| QUALITY-STANDARDS-R84 | Every hosted context | Required: exclude the typed local-only leaves | none | none |
| QUALITY-STANDARDS-R85 | Closed hosted-unit set in hosted contexts | Required: only the PR context admits it; push, initial-push and manual-dispatch contexts exclude it | none | none |
| QUALITY-STANDARDS-R86 | Before installing PR-controlled dependencies | Required: capture the immutable GitHub event and merge SHA, the raw two-parent merge topology, the absolute system Git executable and the configured Python interpreter | none | none |
| QUALITY-STANDARDS-R87 | The capture step | Required: use the fixed system Bash path | none | none |
| QUALITY-STANDARDS-R88 | Prerequisite selection and gate execution | Required: match the captured identity, ignore replacement refs and reject mutable event, SHA or PATH disagreements before contract loading or changed-path selection | none | none |
| QUALITY-STANDARDS-R89 | Always | Forbidden: treating the capture binding as making candidate source, installed dependencies or interpreter files immutable | none | none |
| QUALITY-STANDARDS-R90 | Candidate acceptance | Required: review and the actual hosted result remain acceptance inputs | none | none |
| QUALITY-STANDARDS-R91 | Changes to the workflow contract, Compose baselines, Airflow SQL, n8n workflows and their registered owners | Required: select the applicable hosted regression leaf | none | none |
| QUALITY-STANDARDS-R92 | A selected hosted regression leaf | Required: a nonzero leaf result fails the candidate | none | none |
| QUALITY-STANDARDS-R93 | Remote QA | Required: retain actual document content and catalog, diff/style/commit, machine contracts, selected Docker/security, frontend build/HTTP/browser integration and actual release configuration checks | none | none |
| QUALITY-STANDARDS-R94 | Mocked release/service/supply-chain negative cases | Required: keep them intact and selected locally; hosted PRs do not execute those unit behaviors | none | none |
| QUALITY-STANDARDS-R95 | Optional native Compose cases | Allowed: remain explicit skips or separately authorized observations | none | none |
| QUALITY-STANDARDS-R96 | Hosted Compose-baseline unit leaf | Forbidden: starting HOME resources or turning a skipped native case into a pass | none | none |
| QUALITY-STANDARDS-R97 | Candidate acceptance | Required: production guards and independent exact-source review still apply | none | none |
| QUALITY-STANDARDS-R98 | Mixed unit/corpus commands | Required: distinct registered gate IDs and closed modes | none | none |
| QUALITY-STANDARDS-R99 | Invocation identity | Required: include argv | none | none |
| QUALITY-STANDARDS-R100 | Always | Forbidden: discarding actual corpus checks with a unit leaf | none | none |
| QUALITY-STANDARDS-R101 | Local implementation PASS | Required: it is separate evidence | none | none |
| QUALITY-STANDARDS-R102 | Local implementation PASS | Forbidden: using it to satisfy or bypass the remote candidate | none | none |
| QUALITY-STANDARDS-R103 | Final source input before result-only Task evidence recording | Required: `check-document-links.py --mode all` owns local-only read-only link validation | none | none |
| QUALITY-STANDARDS-R104 | Before submission | Required: record the bound source/base/history and result | none | none |
| QUALITY-STANDARDS-R105 | Remote PR and hosted plans | Required: exclude the link validation leaf | none | none |
| QUALITY-STANDARDS-R106 | Result-only Task additions | Required: minimum document checks and scoped validation of any new or changed link destinations | none | none |
| QUALITY-STANDARDS-R107 | Result-only Task additions | Forbidden: repeating the whole link corpus | none | none |
| QUALITY-STANDARDS-R108 | Local focused feedback | Forbidden: treating it as hosted evidence or a trigger for another candidate aggregate | none | none |
| QUALITY-STANDARDS-R109 | After the reviewed change is staged | Required: the read-only pre-commit and commit-msg hooks observed on a normal `git commit` check the final index, configuration and message | none | none |
| QUALITY-STANDARDS-R110 | Hook installation and execution confirmed | Forbidden: running the same hooks by hand first | none | none |
| QUALITY-STANDARDS-R111 | Installed delivery unconfirmed or separate diagnosis needed | Required: `scripts/validation/run-ci-precommit.sh --mode local-staged` checks an isolated copy of the same registered pins and index | none | none |
| QUALITY-STANDARDS-R112 | Change to the isolated copy, or source or index drift | Required: treat it as a failure | none | none |
| QUALITY-STANDARDS-R113 | Always | Forbidden: bypassing the normal hooks | none | none |
| QUALITY-STANDARDS-R114 | On failure | Required: fix explicitly, review the diff, restage and commit normally again | none | none |
| QUALITY-STANDARDS-R115 | The index changes | Forbidden: reusing an earlier result | none | none |
| QUALITY-STANDARDS-R116 | Always | Required: keep the effective secret guard and the user-global hooks | none | none |
| QUALITY-STANDARDS-R117 | PR candidate | Required: run the same controller with `--mode pr-merge` on its authenticated merge input before accepting selected builds | none | none |
| QUALITY-STANDARDS-R118 | Style controller modes | Required: run every hook on an isolated copy; a fixer without a check mode may change only that copy, which fails the run. In `pr-merge` mode a hook that pre-commit would skip because no changed file matches it is removed before environment installation, using pre-commit's own hook definitions, classifier and changed-file list | none | none |
| QUALITY-STANDARDS-R119 | Always | Forbidden: replacing the server result with a local staged PASS | none | none |
| QUALITY-STANDARDS-R120 | Build steps in the candidate | Required: consume the controller result rather than calling style twice | none | none |
| QUALITY-STANDARDS-R121 | Future deployment | Required: successful server lint/format evidence for its exact promoted revision and configuration before deployment | none | none |
| QUALITY-STANDARDS-R122 | Future deployment with changed inputs | Required: a new server check | none | none |
| QUALITY-STANDARDS-R123 | Both style-controller modes | Required: use a hook's check mode where it has one, run every hook that has input on an isolated copy and preserve source bytes | none | none |
| QUALITY-STANDARDS-R124 | Always | Required: keep formatting and validation as separate purposes | none | none |
| QUALITY-STANDARDS-R125 | Always | Forbidden: direct Agent `pre-commit run` | none | none |
| QUALITY-STANDARDS-R126 | Controlled all-files wrapper | Allowed: use it as an explicitly approved authoring/maintenance lane | none | none |
| QUALITY-STANDARDS-R127 | Controlled all-files wrapper | Forbidden: using it as routine PR QA | none | none |
| QUALITY-STANDARDS-R128 | Identical leaf within one run | Required: deduplicate using input/index/base/history, configuration, toolchain, mode, environment, trust, guarantee and consumer | none | none |
| QUALITY-STANDARDS-R129 | Reusing a result | Required: all identity parts match | none | none |
| QUALITY-STANDARDS-R130 | Always | Forbidden: interchanging staged, PR merge and main/security inputs | none | none |
| QUALITY-STANDARDS-R131 | Within one invocation | Allowed: share parsed immutable Git input | none | none |
| QUALITY-STANDARDS-R132 | Changed inputs or runs | Forbidden: caching working-tree bytes and acceptance | none | none |
| QUALITY-STANDARDS-R133 | Before required execution | Required: Task planning records selected tools, available execution permissions, numeric budget or UNKNOWN, timeout and failure owner | none | Task record |
| QUALITY-STANDARDS-R134 | Missing prerequisites | Required: block that lane | none | none |
| QUALITY-STANDARDS-R135 | A small document-only plan | Forbidden: unrelated tools blocking it | none | none |
| QUALITY-STANDARDS-R136 | Always | Required: preserve bounded process, pipe and descendant cleanup | none | none |
| QUALITY-STANDARDS-R137 | Always | Forbidden: hiding environment failures by skipping cleanup | none | none |
| QUALITY-STANDARDS-R138 | Each Git boundary | Required: use the automatic owner and distinct evidence given in the canonical delivery phase matrix | none | none |
| QUALITY-STANDARDS-R139 | The twelve Git-stage cells | Required: bind each in git-workflow section 7 as Run, Observe, Reuse or Not applicable | none | none |
| QUALITY-STANDARDS-R140 | Always | Required: keep Git event, SDLC stage and document stage as separate axes | none | none |
| QUALITY-STANDARDS-R141 | A check | Required: name the event and revision it binds to | none | none |
| QUALITY-STANDARDS-R142 | A check that runs after its event | Required: it observes and reports | none | none |
| QUALITY-STANDARDS-R143 | A check that runs after its event | Forbidden: blocking that event or describing it as having blocked that event | none | none |
| QUALITY-STANDARDS-R144 | Workflow triggers without an approved merge queue | Forbidden: declaring a `merge_group` trigger | workflow contract rejects the trigger | none |
| QUALITY-STANDARDS-R145 | Job identities, DAG and path-to-root selection | Required: the machine workflow contract owns them | none | none |
| QUALITY-STANDARDS-R146 | Ordinary documents | Required: retain profile, parent and lifecycle/content checks remotely, plus operating catalog checks for operations documents | none | none |
| QUALITY-STANDARDS-R147 | Link validation | Required: belongs only to the local lane | none | none |
| QUALITY-STANDARDS-R148 | Wording changes | Forbidden: selecting Compose, service, hook, tool or implementation regression suites | none | none |
| QUALITY-STANDARDS-R149 | Compose, service, hook, tool or implementation regression suites | Required: follow their actual changed owners | none | none |
| QUALITY-STANDARDS-R150 | Frontend checks | Required: follow the frontend project, not every script or workflow edit | none | none |
| QUALITY-STANDARDS-R151 | Unknown paths | Required: fail closed, including rename/delete evidence | none | none |
| QUALITY-STANDARDS-R152 | Inspecting selection | Allowed: `--explain` without executing a leaf | none | none |
| QUALITY-STANDARDS-R153 | Always | Forbidden: a wrapper creating a second orchestration inventory | none | none |
| QUALITY-STANDARDS-R154 | PR workflow | Required: keep it present without path/commit skips | none | none |
| QUALITY-STANDARDS-R155 | A missing required check | Allowed: remain pending | none | none |
| QUALITY-STANDARDS-R156 | Title edits | Forbidden: cancelling revision validation | none | none |
| QUALITY-STANDARDS-R157 | CodeQL and external security integrations | Forbidden: treating source edits as proof that their server-side settings changed | none | none |
| QUALITY-STANDARDS-R158 | Actual protection settings | Required: approved mutation and authenticated read-back | none | none |
| QUALITY-STANDARDS-R159 | Workflow routing | Required: follow the sole load order in `bootstrap.md#canonical-load-order` | none | none |
| QUALITY-STANDARDS-R160 | Workflow routing | Required: follow repeatable orchestration in `workflows.md` | none | none |
| QUALITY-STANDARDS-R161 | Document language and README navigation | Required: apply the priority in `documentation-protocol.md#document-language` and the `#readme-navigation` rule | none | none |
| QUALITY-STANDARDS-R162 | Write permission | Required: resolve it through `approval-boundaries.md` | none | none |
| QUALITY-STANDARDS-R163 | Completion | Required: use only `task-checklists.md#before-completion` | none | none |
| QUALITY-STANDARDS-R164 | Completion | Required: its conditional harness, evidence, documentation and controlled-gate clauses determine which quality checks apply | none | none |
| QUALITY-STANDARDS-R165 | PR-specific completion | Required: remains owned by the Completion Gate in `github-governance.md` | none | none |
| QUALITY-STANDARDS-R166 | Generated artifacts | Required: regenerate them as part of QA before completion, as a verification step and not an optional cleanup | none | none |
| QUALITY-STANDARDS-R167 | Knowledge graph | Required: keep `graphify-out/` untracked under `.gitignore` | none | none |
| QUALITY-STANDARDS-R168 | Knowledge graph | Required: refresh with one-shot `graphify update .` when the CLI is available and report when it is skipped | none | none |
| QUALITY-STANDARDS-R169 | Knowledge graph | Forbidden: re-tracking `graphify-out/` | none | none |
| QUALITY-STANDARDS-R170 | `pre-commit` file hooks | Required: carry `exclude: '^graphify-out/'` | none | none |
| QUALITY-STANDARDS-R171 | Generated artifact | Forbidden: hand-editing it to pass a check | none | none |
| QUALITY-STANDARDS-R172 | Generated artifact changed | Required: re-run its generator and commit the generated result as a separate logical unit | none | none |
| QUALITY-STANDARDS-R173 | Rendering the public suite-to-validator mapping | Required: use `python3 scripts/validation/run-ci-gate.py --profile changed --explain` without execution | none | none |
| QUALITY-STANDARDS-R174 | Public runner | Forbidden: a duplicated child-command inventory | none | none |
| QUALITY-STANDARDS-R175 | Current operational, architecture and infrastructure README bodies | Forbidden: unjustified runtime-pin duplication | `repo-contracts` gate blocks it | none |
| QUALITY-STANDARDS-R176 | Runtime pins | Required: Compose and Dockerfile declarations own exact runtime pins | none | none |
| QUALITY-STANDARDS-R177 | `infra/tech-stack.versions.json` | Forbidden: treating the curated projection as a second authored authority | none | none |
| QUALITY-STANDARDS-R178 | Narrative documents | Required: link the relevant pin sources | none | none |
| QUALITY-STANDARDS-R179 | Compatibility, advisory, workaround, migration or historical literals | Required: state their concrete reason through the Stage 99 exception contract | none | none |
| QUALITY-STANDARDS-R180 | Current implementation claims | Required: remain subject to drift checks | none | none |
| QUALITY-STANDARDS-R181 | Historical and migration boundaries | Forbidden: rewriting them to match a newer pin | none | none |
| QUALITY-STANDARDS-R182 | Document frontmatter versions | Required: are independent of runtime pins | none | none |
| QUALITY-STANDARDS-R183 | Remote PR QA | Required: use the same public entrypoint and suite manifest; execution context determines leaf eligibility | none | none |
| QUALITY-STANDARDS-R184 | Always | Forbidden: treating a local focused or `full` result as proof of a hosted result | none | none |
| QUALITY-STANDARDS-R185 | Always | Forbidden: faking GitHub environment variables to invoke CI-only wrappers locally | none | none |
| QUALITY-STANDARDS-R186 | Missing tools or unexecuted checks | Required: record them explicitly | none | none |
| QUALITY-STANDARDS-R187 | Always | Forbidden: treating absence or a skipped check as a PASS | none | none |
| QUALITY-STANDARDS-R188 | A LOCAL run | Required: record a result only on the same toolchain as the hosted controller (interpreter version and controller lock packages) | runner toolchain check fails with `ci-gate-local-toolchain` without running | none |
| QUALITY-STANDARDS-R189 | Python build | Required: the build matching hosted is the Ubuntu release from `actions/python-versions` | none | none |
| QUALITY-STANDARDS-R190 | Python build | Forbidden: a build without the memfd seal constants, such as a uv standalone build | none | none |
| QUALITY-STANDARDS-R191 | `--explain` | Allowed: skip the toolchain check because it is not a run | none | none |
| QUALITY-STANDARDS-R192 | Local runner | Required: validate `.github/workflow-contract.yml` and the registered workflow definitions through `scripts/validation/check-github-workflow-contract.py` | none | none |
| QUALITY-STANDARDS-R193 | Every public context | Required: the `leaf.local-tech-stack-version-drift` leaf owns version drift detection | none | none |
| QUALITY-STANDARDS-R194 | Public runner | Required: admit only the authenticated `--mode pr-merge` invocation | none | none |
| QUALITY-STANDARDS-R195 | `--mode local-staged` | Required: keep it separate from aggregate QA and use it when installed hook delivery is unconfirmed or diagnosis is needed | none | none |
| QUALITY-STANDARDS-R196 | Always | Forbidden: isolated wrapper regressions substituting for an observed local or hosted execution | none | none |
| QUALITY-STANDARDS-R197 | `full` | Required: run it only as an explicitly scoped comprehensive audit | none | none |
| QUALITY-STANDARDS-R198 | Always | Forbidden: treating `full` as a commit, feature-push, PR, main or release completion ritual | none | none |
| QUALITY-STANDARDS-R199 | Before running `full` | Required: record selected context, tools, budget or UNKNOWN and approval | none | none |
| QUALITY-STANDARDS-R200 | LOCAL full | Required: include the registered local units and content checks | none | none |
| QUALITY-STANDARDS-R201 | Hosted contexts running full | Required: exclude local-only units and links | none | none |
| QUALITY-STANDARDS-R202 | Always | Forbidden: treating a modeled full plan as proof that a workflow executes it | none | none |
| QUALITY-STANDARDS-R203 | Unknown changed inputs | Required: expand fail-closed within their actual context | none | none |
| QUALITY-STANDARDS-R204 | After successful selected verification | Forbidden: an unconditional full run | none | none |
| QUALITY-STANDARDS-R205 | Final review and evidence-update reuse | Required: follow `workflows.md#review-scope-and-evidence-updates`, including affected-slice revalidation and mandatory protected-surface expertise | none | none |
| QUALITY-STANDARDS-R206 | Evidence-only Task update | Forbidden: creating another independent source-review gate | none | none |
| QUALITY-STANDARDS-R207 | A gate | Required: own one current invariant, not a historical document count, copied command list or Task's observed commit | none | none |
| QUALITY-STANDARDS-R208 | Ownership split | Required: the workflow manifest owns composition, agent governance owns approval and completion policy and Stage 99 owns document structure | none | none |
| QUALITY-STANDARDS-R209 | Provider adapter and PR template | Required: refer to these owners rather than adding another unconditional full run or independent checklist | none | none |
| QUALITY-STANDARDS-R210 | Every leaf in `.github/workflow-contract.yml` | Required: name a resolving canonical policy heading in `rule_owner` under `.agents/governance/` or `docs/00.workspace/01.project/`, `03.process/`, `04.quality/` | workflow contract fails a leaf without a resolving `rule_owner` | `UNOWNED` in `run-ci-gate.py --crosswalk` |
| QUALITY-STANDARDS-R211 | Both public profiles | Required: use one Compose leaf that validates every declared selection independently, including port-collision checks | none | none |
| QUALITY-STANDARDS-R212 | An explicit operator-selected Compose combination | Required: belongs to the standalone Compose validator, not a second required leaf with the same command | none | none |
| QUALITY-STANDARDS-R213 | A current lifecycle, parser or gate contract changes | Allowed: focused fixtures | none | none |
| QUALITY-STANDARDS-R214 | Fixtures for a changed invariant | Required: reuse focused valid/invalid cases | none | none |
| QUALITY-STANDARDS-R215 | Wording-only edits | Forbidden: requiring model execution or a second all-files sweep | none | none |
| QUALITY-STANDARDS-R216 | Always | Required: retain negative cases for authorization, ownership, symlinks and fail-closed execution | none | none |
| QUALITY-STANDARDS-R217 | A smaller suite | Forbidden: missing behavioral coverage | none | none |
| QUALITY-STANDARDS-R218 | Commit time | Required: check end-of-file and trailing whitespace read-only, mixed-line-ending with `--fix=no`, Ruff format with `--check` and markdownlint with `fix: false` | none | none |
| QUALITY-STANDARDS-R219 | A fix is needed | Required: run the existing manual fix hooks, `ruff format` or `markdownlint-cli2 --fix` separately on named files, review the fix diff, restage only the needed files or hunks and commit normally | none | none |
| QUALITY-STANDARDS-R220 | Always | Forbidden: a checker adding unstaged content to the index on its own | none | none |
| QUALITY-STANDARDS-R221 | Always | Forbidden: adding a separate formatting tool | none | none |
| QUALITY-STANDARDS-R222 | Shared formatter and linter invocations | Required: `.pre-commit-config.yaml` owns them and registered project-local package scripts own their package scope | none | none |
| QUALITY-STANDARDS-R223 | Always | Forbidden: treating a config file alone as an executing owner | none | none |
| QUALITY-STANDARDS-R224 | Always | Forbidden: treating a syntax/security check as a formatter | none | none |
| QUALITY-STANDARDS-R225 | File scope | Required: keep one formatting owner per file scope | none | none |
| QUALITY-STANDARDS-R226 | File scope | Allowed: a scope with no formatter | none | none |
| QUALITY-STANDARDS-R227 | Check commands | Required: preserve authored source and use supported check options | none | none |
| QUALITY-STANDARDS-R228 | Agent-invoked all-files pre-commit runs | Required: use the controlled isolated final-QA boundary and report any resulting diff | none | none |
| QUALITY-STANDARDS-R229 | Normal automatic Git commit hooks | Forbidden: bypassing them | none | none |
| QUALITY-STANDARDS-R230 | Explicit fixes | Required: review them separately; a second formatting pass must be unchanged | none | none |
| QUALITY-STANDARDS-R231 | Python | Required: Ruff format is the formatter and `ruff check` the linter, both registered hooks pinned in `ruff.toml` | none | none |
| QUALITY-STANDARDS-R232 | `ruff.toml` | Required: own the format settings and the selected lint rules with the measurement behind each selection and each exception | none | none |
| QUALITY-STANDARDS-R233 | Formatting settings | Required: pin them in the repository, not a tool default or machine version | none | none |
| QUALITY-STANDARDS-R234 | Repository-registered agent editor hook | Required: report formatting defects | none | none |
| QUALITY-STANDARDS-R235 | Repository-registered agent editor hook | Forbidden: rewriting files | none | none |
| QUALITY-STANDARDS-R236 | Explicit fix command | Allowed: format a file only in agreement with the registered owner | none | none |
| QUALITY-STANDARDS-R237 | A hook outside the repository that cannot be registered | Required: state the repository boundary in the tool's ignore file (`.prettierignore` for Prettier) | none | none |
| QUALITY-STANDARDS-R238 | A file type that already has an owner | Forbidden: adding a second tool over it | none | none |
| QUALITY-STANDARDS-R239 | Registered formatter or linter | Required: carry a `files` selector naming the scope it owns | none | none |
| QUALITY-STANDARDS-R240 | Always | Forbidden: a tool reading more file types than its owner declares | none | none |
| QUALITY-STANDARDS-R241 | Validators | Forbidden: depending on where a line breaks | none | none |
| QUALITY-STANDARDS-R242 | An exemption from a line-break-sensitive check | Required: put it on the line as a stated marker | none | none |
| QUALITY-STANDARDS-R243 | Adopting or changing a formatter | Required: reformat the corpus once, in its own commit, after every check the reformatting would break is fixed | none | none |
| QUALITY-STANDARDS-R244 | A change touches a protected surface, changes a policy, role, skill, shared contract or Registry rule, changes validator, gate or hook behavior, or performs a security, secret, remote, runtime or data action | Required: classify it high-risk and give it one independent read-only review by a reviewer who did not implement it, plus any boundary specialist review it needs | none | none |
| QUALITY-STANDARDS-R245 | A change that is not high-risk changes executable code or tests | Required: classify it medium-risk and give it one primary read-only review in a fresh context by a reviewer who did not write it, against the governing criteria and recorded check results | none | none |
| QUALITY-STANDARDS-R246 | Any other change | Allowed: close it as low-risk with its focused checks and an author check that names what was compared and what was not checked; the author check is not called independent review | none | none |
| QUALITY-STANDARDS-R247 | The class is unclear | Required: take the higher class | none | none |

###### 1. Documentation Quality Rubric
<!-- core-payload-level:4 -->

| Grade | Description | Requirements                                                           |
| :---- | :---------- | :--------------------------------------------------------------------- |
| A     | Elite       | Accurate routing, valid commands, no policy conflicts, SSoT alignment  |
| B     | Strong      | Mostly aligned with minor omissions                                    |
| C     | Functional  | Works but has clarity or coverage gaps                                 |
| D     | Weak        | Multiple stale references or ambiguous guidance                        |
| F     | Failing     | Hardcoded secrets, broken governance links, contradictory instructions |

Quality dimensions:

- Actionability: instructions are concrete and testable.
- Conciseness: avoid generic filler.
- Accuracy: references match current repository structure.

###### 2. Security Baseline
<!-- core-payload-level:4 -->

- Never commit plaintext credentials, including in source-controlled configs.
- Prefer secret managers or mounted secret files.

The product's runtime security is owned by the product, not by this workspace
policy. Each former rule keeps its meaning at its product owner:

| Former rule | Product owner |
| --- | --- |
| QUALITY-STANDARDS-R8, R15 (network boundaries and isolation) | [REQ-0023-FR-0001](../../01.requirements/0023-standardize-infra-net.md) and [AD-0026](../../02.architecture/01.descriptions/0026-standardize-infra-net.md) |
| QUALITY-STANDARDS-R9 (least-privilege runtime defaults) | [POL-0006-R43](../../05.operations/02.policies/01.common/0006-infrastructure-optimization-governance.md) |
| QUALITY-STANDARDS-R10 (central authentication) | [REQ-0002-FR-0001 and FR-0002](../../01.requirements/0002-auth.md), with the Keycloak choice in [ADR-0002](../../02.architecture/02.decisions/0002-keycloak-oauth2-proxy-choice.md) |
| QUALITY-STANDARDS-R11 (least-privilege RBAC/ABAC) | [POL-0006-R45](../../05.operations/02.policies/01.common/0006-infrastructure-optimization-governance.md) |
| QUALITY-STANDARDS-R13 (Docker secrets or OpenBao flow) | [REQ-0003-FR-0001 and FR-0002](../../01.requirements/0003-security.md) and [POL-0006-R2](../../05.operations/02.policies/01.common/0006-infrastructure-optimization-governance.md) |
| QUALITY-STANDARDS-R14 (container hardening) | [POL-0006-R44](../../05.operations/02.policies/01.common/0006-infrastructure-optimization-governance.md), still a manual review expectation |
| QUALITY-STANDARDS-R16 (TLS at ingress) | [REQ-0001-FR-0001 and FR-0003](../../01.requirements/0001-gateway.md) |

A change to any of them selects its checks through the
[change-type verification matrix](#5-change-type-verification-matrix); the
retired rule IDs are not reused.

###### Bounded npm risk acceptance
<!-- core-payload-level:5 -->

No npm risk acceptance is active. The single bounded acceptance for
GHSA-vfj7-8cjw-p6xm was retired after GitHub withdrew the advisory on
2026-10-23; `leaf.dependency-vulnerability-audit` is again the strict
`npm audit --audit-level=high` run, and the CI contract rejects an
`npm_audit_acceptance` record. A new acceptance needs a reviewed policy
amendment that names the advisory, locked chain, owner approval and an expiry
no more than 30 days after approval, with negative fixtures. An acceptance is
never a vulnerability fix or a branch protection bypass. Never use a skipped
audit, lower threshold, continue-on-error, blanket package exception or
omitted development audit.

Remote PR candidate validation and review by [risk](#11-review-risk) own candidate acceptance, while
main-push security remains a post-merge observation.

###### 3. Reliability Baseline
<!-- core-payload-level:4 -->

- Recurring QA covers current document forms, templates, frontmatter, identity,
  relationships, links, lifecycle and preservation, plus this workspace's
  Docker/Compose services, configuration and operations contracts.
- A supporting parser, selector, style controller or release regression must
  prove one of those current contracts. An agent answer score, a past migration
  census or a completed Task's fixed hash is not a recurring quality contract.
- Remove event-specific expectations for a completed document's current
  status, wording or inventory, and contract assertions coupled only to a
  retired file, helper or symbol. Current Registry validators and meaningful
  boundary regressions own continuing guarantees; do not replace obsolete
  expectations with another permanent forbidden-name list. Generic preserved
  byte, recovery and compatibility proofs remain current contracts.
- Explicit Skill evaluation may retain paired task/output/scoring/aggregate
  evidence outside recurring repository QA. The evaluation README routes that
  evidence; agentic policy owns authority and stop conditions. A representative
  score is not whole-Skill coverage, runtime activation or Task acceptance.
- Behavior changes require focused failure reproduction and regression evidence.
  Wording-only changes require applicable content and style validation, not new
  implementation tests or a universal coverage percentage.
- Runtime health, live smoke, operator acceptance, backup and restore evidence
  belong to their approved service Task. Compose render or static hardening does
  not prove any of them. A SEV1/SEV2 incident uses its incident postmortem.
- Optimize QA in this order: remove duplicate leaves; separate document
  content checks from validator regression tests; share parsing and Git reads
  within one run; select by change impact; reuse only a provably equivalent
  narrow result, matched on the full execution identity under the Execution
  Boundary; a difference in any part makes it a new observation. Compare a
  reproducible measure before and after (run time, wait, installs, call count,
  CPU, or cost); never call a change faster
  without a number, and do not start with a large global cache or a new gate.
- A non-functional requirement names one ISO/IEC 25010 quality
  characteristic and a measure in the ISO/IEC 25023 sense: what is measured,
  the unit, the environment, and the acceptance value. The Requirement
  template carries that line. A characteristic left out states why it does
  not apply, and no threshold is forced on every project. This adds no
  separate compliance gate.
- Retire one-time QA in this order: transfer a continuing guarantee to its
  current owner; remove callers and registration; remove exclusive helpers,
  fixtures and tests; preserve useful actual results in existing Task/history.
- Stage 98 holds no records, as the
  [documentation protocol](../03.process/documentation-protocol.md#document-retention-and-retirement)
  defines. Its only Stage 98-specific check is corpus lifecycle occupancy,
  which fails on any tracked file there other than the README; the README is
  checked like any other README. No archive integrity, retention, recovery,
  Tombstone, migration-ledger or archive-link check exists.
- Shared implementation libraries under `scripts/lib/` and executable QA
  owners retain meaningful test evidence. A nonmutating companion library
  outside that shared surface may be retained through a proven current
  consumer without creating a dedicated purpose-excluded QA suite. Mutation,
  missing consumers, unsafe paths and invalid import claims remain rejected
  by the manifest contract; this grants no runtime acceptance.
- A library's behavioral evidence is judged by its tracked, admitted test owner
  and actual API/fixture use. Directory mirroring is the default organization,
  not a second mandatory evidence source. A registered cross-module or
  entrypoint test may own that behavior without a duplicate library smoke.
  Source-token bans, test-of-test census scans and retired filename assertions
  do not substitute for current mutation, preservation or parser behavior.
- Age, filenames, test counts and failing results alone are not deletion
  criteria. A removed check must have a disposition and any continuing owner.
  Failed required checks remain failures until repaired or deliberately retired
  under the approved contract.
- When an implementation contradicts its canonical rule, record the conflict,
  the decision and the change order in the current Task, and change the
  producer, reader, schema, current guidance and tests in one logical change.
  Never make the check pass by editing only its test expectation or by only
  relaxing the rule, and never adopt an unapproved test constant as policy.
  Changing the canonical rule itself needs its owner's approval under
  [approval boundaries](approval-boundaries.md#authorization-source-and-records).

###### 4. Execution Boundary
<!-- core-payload-level:4 -->

- **Authoring**: explicit formatting may write eligible authored files. Focused
  RED/GREEN and selected read-only lint help diagnose a change. Observe actual
  installed Git hooks separately; tracked configuration does not change a
  user-global hook. Never use SKIP, fake CI variables or `--no-verify`.
- **Local implementation verification**: the workflow contract's typed
  `public_gate.local_only_gate_ids` owns document-library, hook, mocked native
  and other isolated implementation regressions plus local links. The closed
  hosted-unit set is the exception: CI gate-contract, Compose-baseline and
  repository-integrity regressions run in both selected local verification and
  hosted candidate validation. Use
  `scripts/validation/run-ci-gate.py --profile changed --local-only --explain`
  to inspect the complementary local-only plan. Use
  `scripts/validation/run-ci-gate.py --profile changed --explain` and then the
  same command without `--explain` once on the final implementation input when
  a changed owner selects a promoted regression. The shared runner
  and registered path owners remain the execution route; no parallel wrapper
  or command inventory is created. Result-only Task additions receive minimum
  document checks. Do not repeat the local full profile after commit or push.
- **Candidate acceptance**: the public repository uses remote PR QA through
  `scripts/validation/run-ci-gate.py --profile changed`. Inspect the selected
  plan and prerequisites before execution. Every hosted context excludes the
  typed local-only leaves; only the PR context admits the closed hosted-unit
  set above. Push, initial-push and manual-dispatch contexts exclude it so
  merged-input security observation does not repeat candidate QA.
  Before installing PR-controlled dependencies, the candidate captures the
  immutable GitHub event and merge SHA, the raw two-parent merge topology and
  the absolute system Git executable and the configured Python interpreter;
  the capture step uses the fixed system Bash path. Both prerequisite selection
  and gate execution must match that captured identity, ignore replacement refs and
  reject mutable event, SHA or PATH disagreements before contract loading or
  changed-path selection. This binding prevents later PATH redirection; it does
  not make candidate source, installed dependencies or interpreter files
  immutable, so review and the actual hosted result remain acceptance inputs.
  Changes to the workflow contract, Compose baselines, Airflow SQL, n8n
  workflows and their registered repository owners select the applicable
  hosted regression leaf; a nonzero leaf result fails the candidate. Remote QA retains actual document content and
  catalog, diff/style/commit, machine contracts, selected Docker/security,
  frontend build/HTTP/browser integration and actual release configuration checks.
  Mocked release/service/supply-chain negative cases stay intact and selected
  locally; hosted PRs do not execute those unit behaviors. Optional native
  Compose cases remain explicit skips or separately authorized observations;
  the hosted Compose-baseline unit leaf does not start HOME resources or turn a
  skipped native case into a pass. Production guards
  and independent exact-source review still apply. Mixed unit/corpus commands
  must have distinct registered gate IDs and closed modes; invocation identity
  includes argv, and actual corpus checks cannot be discarded with a unit leaf.
  Local implementation PASS is separate evidence and does not satisfy or bypass the remote candidate.
- **Document links**: `check-document-links.py --mode all` owns local-only
  read-only link validation on the final source input before result-only Task
  evidence recording. Record the bound source/base/history and result before
  submission; remote PR and hosted plans exclude this leaf. Result-only Task
  additions use minimum document checks and scoped validation of any new or
  changed link destinations, without repeating the whole link corpus.
  Local focused feedback does not become hosted evidence or trigger another
  candidate aggregate.
- **Before local commit**: after the reviewed change is staged, the
  read-only pre-commit and commit-msg hooks observed on a normal `git commit`
  check the final index, configuration, and message. Do not run the same
  hooks by hand first once their installation and execution are confirmed.
  When delivery of the installed checks is unconfirmed, or a separate
  diagnosis is needed, `scripts/validation/run-ci-precommit.sh --mode
  local-staged` checks an isolated copy of the same registered pins and
  index. A change to that copy, or source or index drift, is also a failure
  and never a reason to bypass the normal hooks. On failure, fix explicitly,
  review the diff, restage, and commit normally again. When the index changes,
  an earlier result is not reused. Keep the effective secret guard and the
  user-global hooks.
- **Server final defense**: the PR candidate runs the same controller with
  `--mode pr-merge` on its authenticated merge input before accepting selected
  builds. As in local mode, every hook runs on an isolated copy and a fixer
  without a check mode may change only that copy, which fails the run. A hook
  that pre-commit would skip because no changed file matches it is removed
  first, with pre-commit's own hook definitions, classifier and changed-file
  list, so its environment is never installed; a missing or different
  pre-commit module fails the run. Local
  staged PASS cannot replace that server result. Build steps in
  the same candidate consume its result rather than calling style twice.
  A future deployment must require successful server lint/format evidence for
  its exact promoted revision and configuration before deployment; changed
  inputs require a new server check. The repository currently has no deployment
  workflow, so this rule supplies no deployment execution or acceptance.
- **Validation**: both style-controller modes use a hook's check mode where it
  has one, run every hook that has input on an isolated copy, and preserve source bytes.
  Formatting and validation have separate purposes.
  Direct Agent `pre-commit run` is prohibited; the controlled all-files wrapper
  is an explicitly approved authoring/maintenance lane, never routine PR QA.
- **Execution identity**: deduplicate an identical leaf within one run using
  input/index/base/history, configuration, toolchain, mode, environment, trust,
  guarantee and consumer. Reuse a result only when all of these match. Different
  staged, PR merge and main/security inputs are not interchangeable. Parsed
  immutable Git input may be shared within one invocation; working-tree bytes
  and acceptance are not cached across changed inputs or runs.
- **Prerequisites and budget**: Task planning records selected tools, available
  execution permissions, numeric budget or UNKNOWN, timeout and failure owner
  before required execution. Missing prerequisites block that lane; unrelated
  tools must not block a small document-only plan. Preserve bounded process,
  pipe and descendant cleanup; do not hide environment failures by skipping it.

###### Canonical delivery phase matrix
<!-- core-payload-level:5 -->

| Boundary | Automatic owner | Distinct evidence |
| --- | --- | --- |
| Commit | Observed read-only installed pre-commit and commit-msg; the local-staged controller for unconfirmed delivery or diagnosis | Exact index/config and message; effective secret guard |
| Feature push | No repeated public QA | New commits become PR candidate input |
| Agent Stop | Diagnostics only | Working tree; no second aggregate run |
| Before submission | Selected local-only implementation and link leaves once | Final source/index, base/history, tools and actual local result |
| PR to main | One candidate job including pr-merge lint/format before selected builds; excludes local-only leaves | Authenticated base/head/merge, pins, prerequisites and hosted result |
| Main push | Separate security/SARIF observation | Merged SHA and hosted security trust; no candidate suite repeat |
| Release preparation PR | Same candidate owner selects changelog/release checks | Main-targeted CHANGELOG and reviewed source |
| Approved release dispatch | Sole main-only SemVer producer | Exact commit, create-only tag, complete draft assets, publication receipt |
| Future deployment | Server lint/format evidence for exact promoted inputs, then deployment-specific checks | Distinct deployment authority/result; no deployment workflow currently |

The canonical delivery phase matrix above implements the policy meanings of
`QA-STAGES-1` 1.0.0. The twelve Git-stage cells (four actions, each before,
during and after) are bound in
[git-workflow section 7](../03.process/git-workflow.md#7-git-action-stages), each as Run,
Observe, Reuse or Not applicable. A Git
event (commit, push, pull request or merge, each before, during or after), the
SDLC stage and the document stage are separate axes; a check
names the event and revision it binds to. A check that runs after its event,
such as the main-push observation, observes and reports. It does not block that
event and is never described as having blocked it. No workflow declares a
`merge_group` trigger. The remote merge queue was read back as unused on
2026-11-14 (`.github/rulesets/main-protection.md`); the workflow contract
rejects the trigger, and it is added only together with an approved merge queue.

The machine workflow contract owns exact job identities, DAG and path-to-root
selection. Ordinary documents retain profile, parent and lifecycle/content
checks remotely, plus operating catalog checks for operations documents. Link
validation belongs only to the local lane. Wording changes do not select Compose,
service, hook, tool or implementation regression suites; these follow their
actual changed owners. Frontend checks follow the frontend project, not every script or workflow
edit. Unknown paths fail closed, including rename/delete evidence. `--explain`
inspects selection without executing a leaf. No wrapper creates a second
orchestration inventory.

Keep the PR workflow present without path/commit skips; a missing required check
can remain pending. Title edits do not cancel revision validation. See
[GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).
CodeQL and external security integrations are distinct remote observations;
source edits do not prove that their server-side settings changed. Actual
protection settings require approved mutation and authenticated read-back.

###### 8. Workflow and Language Routing
<!-- core-payload-level:4 -->

- Follow the sole load order in `.agents/governance/bootstrap.md#canonical-load-order`.
- Follow repeatable orchestration in `.agents/governance/workflows.md`.
- Apply the document language priority in
  `docs/00.workspace/03.process/documentation-protocol.md#document-language` and the
  README navigation rule in
  `docs/00.workspace/03.process/documentation-protocol.md#readme-navigation`.
- Resolve write permission through `docs/00.workspace/04.quality/approval-boundaries.md`.

###### 9. Completion Routing
<!-- core-payload-level:4 -->

Use only `docs/00.workspace/04.quality/task-checklists.md#before-completion`. Its conditional
harness, evidence, documentation, and controlled-gate clauses determine which
quality checks apply. PR-specific completion remains owned by the Completion
Gate in `docs/00.workspace/03.process/github-governance.md`.

###### 6. Generated-Artifact Freshness
<!-- core-payload-level:4 -->

Some artifacts are generated from repository content and must be regenerated as
part of QA before completion. Treat regeneration as a verification step, not an
optional cleanup.

- **Generated path indexes**: none exist. The repo-local LLM Wiki and its two
  tracked outputs were retired on 2026-09-10 with their generator, so adding,
  removing, or renaming a document no longer carries a regeneration step.
- **Knowledge graph**: `graphify-out/` is local generated intelligence and is
  not tracked. `.gitignore` governs the whole directory, so a rebuild produces
  no diff, needs no commit, and cannot conflict with the `pre-commit`
  intermediate stash. Refresh it with one-shot `graphify update .` when the CLI
  is available, which costs no API tokens, and report when it is skipped. Do not
  re-track it: a rebuild replaced a 148 MiB blob on every graph-touching commit,
  and a clone can regenerate it. The `pre-commit` file hooks still carry
  `exclude: '^graphify-out/'` so a formatter never reaches the working copy.
- **General rule**: never hand-edit a generated artifact to pass a check. Re-run
  its generator and commit the generated result as a separate logical unit.

###### 7. Local QA/CI Orchestration
<!-- core-payload-level:4 -->

Use `python3 scripts/validation/run-ci-gate.py --profile changed --explain` to render the
selected public suite-to-validator mapping without execution. The public runner
exposes `--profile changed`, `--profile full`, and `--explain` routes and contains
no duplicated child-command inventory. These routes do not
upload SARIF, verify remote branch protection, install CI-only dependencies, or
declare protected-branch readiness. The `repo-contracts` gate also blocks
unjustified runtime-pin duplication in current operational, architecture and
infrastructure README bodies. Compose and Dockerfile declarations own exact
runtime pins; `infra/tech-stack.versions.json` is a curated machine-readable projection,
not a second authored authority. Narrative documents link the relevant sources.
Necessary compatibility, advisory, workaround, migration or historical literals
must state their concrete reason through the Stage 99 exception contract. Current
implementation claims remain subject to drift checks; historical and migration
boundaries are not rewritten to match a newer pin. Document frontmatter versions
are independent. The registered metadata validator owns executable enforcement.

Remote PR QA uses the same public entrypoint and suite manifest; execution
context determines leaf eligibility. A local focused or `full` result is never
proof of a hosted result. Do not fake GitHub environment variables to
invoke CI-only wrappers locally. Record missing tools and unexecuted checks
explicitly; neither absence nor a skipped check is a PASS.

A local run records a result only on the same toolchain as the hosted
controller. Before a LOCAL run, the runner checks that the interpreter
version equals the `python-version` pin in `.github/workflows/ci-quality.yml`
and that the active packages in `scripts/requirements-controller.lock` are
installed at the same versions; otherwise it fails with
`ci-gate-local-toolchain` without running. The build that matches hosted is
the Ubuntu release from `actions/python-versions`, and a build without the
memfd seal constants, such as a uv standalone build, is refused. `--explain`
is not a run, so it skips this check.

The local runner validates `.github/workflow-contract.yml` and the registered
workflow definitions through
`scripts/validation/check-github-workflow-contract.py`. The required
`leaf.local-tech-stack-version-drift` owns version drift detection in every
public context. The public runner admits only the authenticated `--mode pr-merge` invocation.
The explicit `--mode local-staged` route is separate from aggregate QA. Use
it to check the staged input when installed hook delivery is unconfirmed or
diagnosis is needed. Isolated wrapper regressions do not substitute for an
observed local or hosted execution.

###### Explicit Full Audit
<!-- core-payload-level:5 -->

`full` is an explicitly scoped comprehensive audit, not a commit, feature-push,
PR, main or release completion ritual. Record its selected context, tools,
budget or UNKNOWN and approval before executing it. LOCAL full includes the
registered local units and content checks; hosted contexts exclude local-only
units and links. A modeled full plan does not prove a workflow executes it.
Unknown changed inputs still expand fail-closed within their actual context.
Do not follow successful selected verification with an unconditional full run.

Final review and evidence-update reuse follow
[Workflows](../../../.agents/governance/workflows.md#review-scope-and-evidence-updates), including affected
slice revalidation and mandatory protected-surface expertise. An evidence-only
Task update does not create another independent source-review gate.

###### Gate and Fixture Ownership
<!-- core-payload-level:5 -->

A gate owns one current invariant, not a historical document count, a copied
command list, or a Task's observed commit. The workflow manifest owns composition;
agent governance owns approval and completion policy; Stage 99 owns document structure.
A provider adapter and a PR template refer to these owners rather than adding
another unconditional full run or independent checklist. Every leaf in
`.github/workflow-contract.yml` names its governing rule in `rule_owner`, a
`<canonical-policy-path>#<heading anchor>` under `.agents/governance/` or
`docs/00.workspace/01.project/`, `03.process/`, `04.quality/` that must
resolve. These are the existing checker's allowed owner classes; a leaf
without one, or one naming a missing document or heading, fails the workflow
contract and shows as `UNOWNED` in `run-ci-gate.py --crosswalk`.

Both public profiles use one Compose leaf. With no inherited profile override,
it validates every declared selection independently, including port-collision
checks. An explicit operator-selected combination belongs to the standalone
Compose validator, not a second required leaf with the same command.

Focused fixtures are appropriate when a current lifecycle, parser or gate
contract changes. Reuse focused valid/invalid cases for the changed invariant; do not
require model execution or a second all-files sweep for wording-only edits.
Retain negative cases for authorization, ownership, symlinks, and fail-closed
execution. A smaller suite must not mean missing behavioral coverage.

###### 10. Formatting and Linting Ownership
<!-- core-payload-level:4 -->

At commit time, end-of-file and trailing whitespace are checked by
read-only checkers, mixed-line-ending runs with `--fix=no`, Ruff format with
`--check`, and markdownlint with `fix: false`. When a fix is needed, run the
existing `end-of-file-fixer` and `trailing-whitespace` manual hooks,
`ruff format`, or `markdownlint-cli2 --fix` separately on named files.
Review the fix diff, restage only the needed files or hunks, and commit
normally. A checker must never add unstaged content to the index on its own,
and no separate formatting tool is added.

- `.pre-commit-config.yaml` owns shared formatter and linter invocations;
  registered project-local package scripts own their actual package scope.
  A config file alone does not establish an executing owner. Formatting rewrites
  bytes; linting reports defects, and a syntax/security check is not a formatter.
  Keep one formatting owner per file scope; a scope can have no formatter.
- Check commands must preserve authored source. Use supported check options;
  Agent-invoked all-files pre-commit runs use the controlled isolated final-QA
  boundary and report any resulting diff. Normal automatic Git commit hooks
  retain their existing authorization and must not be bypassed. Explicit
  fixes are reviewed separately and a second formatting pass must be unchanged.
  Ruff format is the Python formatter and `ruff check` is the Python linter.
  Both are registered hooks and both are pinned in `ruff.toml`, which owns the
  format settings and the selected lint rules with the measurement behind each
  selection and each exception.
- Formatting settings are pinned in the repository, not left to a tool default
  or to whichever version a machine has. `ruff.toml` pins Python.
- A repository-registered agent editor hook reports formatting defects and
  does not rewrite files.
  An explicit fix command may format a file only in agreement with the
  registered owner. Where a hook lives outside the repository and cannot be registered,
  the repository states its own boundary in the tool's ignore file;
  `.prettierignore` does this for Prettier.
- Do not add a second tool over a file type that already has an owner. Two
  formatters on one file type is a conflict, not redundancy.
- A registered formatter or linter carries a `files` selector that names the
  scope it owns. A tool that reads more file types than its owner declares is
  the same defect as a second owner: `ruff format` also reformats Python
  fenced inside Markdown, and invoked without that selector it rewrote a
  frozen archive body. The selector, not the invoker's memory, is the boundary.
- A validator must not depend on where a line breaks. A check that a formatter
  can break was satisfied by typography rather than by content, and the
  exemption belongs on the line as a stated marker.
- Adopting or changing a formatter reformats the corpus once, in its own
  commit, after every check that the reformatting would break is fixed.

###### 11. Review Risk
<!-- core-payload-level:4 -->

Every change gets the review its risk class requires (R244-R247). A change is
high-risk when it touches a
[protected surface](approval-boundaries.md#enforcement), changes a policy,
role, skill, shared contract or Registry rule, changes validator, gate or hook
behavior, or performs a security, secret, remote, runtime or data action. A
change that meets none of those but changes executable code or tests, such as
a new operations command or its tests, is medium-risk. Every other change is
low-risk: an ordinary document or README edit, a Task evidence or acceptance
record, or a Stage 01 to 05 prose correction that changes no rule.

A high-risk change gets one independent review, with any boundary specialist
review it needs. A medium-risk change gets one primary review against the
governing criteria and the recorded check results, with no specialist unless
an actual boundary appears. A low-risk change closes with its focused checks
and an author check. A reviewer does not rerun a check whose input is
unchanged, and an evidence-only commit after review needs no new review. A
review run after merge is recorded as such, and its findings are fixed or
recorded in the owning Task. How an agent selects, dispatches and enforces a
read-only reviewer is the agent procedure in
[workflows](../../../.agents/governance/workflows.md#review-risk).

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

###### Approval and Review
<!-- core-payload-level:4 -->

None: no exception exists to approve.

#### Enforcement

##### Mechanisms

###### 5. Change-Type Verification Matrix
<!-- core-payload-level:4 -->

Use the smallest meaningful selected checks. This is the sole matrix for all
providers; Task evidence names each input, result, acceptance and unexecuted lane.

| Change | Focused authoring feedback | Remote candidate or distinct observation |
| --- | --- | --- |
| Ordinary documents/templates | Local-only registered links; scoped metadata and read-only style feedback | Profile, relationships and lifecycle; operations catalog when applicable; no link or implementation regression rerun |
| Validator/parser/Registry implementation | RED/GREEN, relevant style and selected local-only implementation regressions | Actual content checks; no local implementation suite repeat |
| Gate/workflow/style controller | Selected local-only selection, trust, failure and cleanup regressions | Actual workflow/contract validators; exact hosted job/event evidence |
| Docker/Compose/service configuration | Relevant syntax/render/hardening feedback | Selected configuration checks; live HOME/smoke/restore only for a named exact target |
| Commit/changelog/release implementation | Commitizen and SemVer/changelog/draft-asset regression | PR candidate checks; release publication only for its approved exact version |
| Historical QA retirement | Caller/registration closure and continuing-owner proof | Applicable current document/runner checks |
| Remote setting or high-risk runtime | Concrete approved target, before-state and recovery | Actual read-back or runtime receipt; source-only evidence is insufficient |

A PASS check is not criterion acceptance, authorization, integration or runtime
activation. ACCEPTED_RISK remains a typed security exception with its original
expiry, not a vulnerability fix or live service success. No synthetic fixture
proves arbitrary agent prose or provider performance. Missing required evidence
remains FAIL, BLOCKED, NOT_RUN or unverified as applicable. Independent review
reads the exact diff, contract and actual results; the current Task owns it.

##### Limits

Seven rules name a check that rejects or fails a violation; every other rule names no check.

- Documentation grading and the security baseline (R1-R7, R12) name no check; R8-R11 and R13-R16 moved to their product owners and are not reused.
- npm audit, new acceptances and candidate ownership (R18-R23) name no check; only R17 is tied to the CI contract.
- Reliability scope, Skill evaluation, test evidence, QA optimization and non-functional requirements (R24-R50) name no check.
- QA retirement, Stage 98 README, library evidence, check removal and contradiction handling (R51, R53-R55, R57-R69) name no check; R52 is tied to the corpus lifecycle occupancy check and R56 to the manifest contract, and the policy states that no archive integrity, retention, recovery, Tombstone, migration-ledger or archive-link check exists.
- Authoring and local implementation verification (R70-R81) name no check; tracked configuration does not change a user-global hook.
- Candidate acceptance (R82-R102) names no check; the capture binding prevents later PATH redirection but does not make candidate source, installed dependencies or interpreter files immutable.
- Document links and commit hooks (R103-R116) name no check.
- Server final defense, validation, execution identity and prerequisites (R117-R137) name no check; the repository has no deployment workflow, so R121-R122 supply no deployment execution or acceptance.
- Delivery matrix and selection routing (R138-R143, R145-R158) name no check; only R144 is tied to the workflow contract.
- Workflow, language and completion routing and generated artifacts (R159-R172) name no check.
- Local QA orchestration (R173-R174, R176-R187, R189-R196) names no check; R175 is tied to the `repo-contracts` gate and R188 to the runner toolchain check; the policy says the registered metadata validator owns executable enforcement without naming the rule it checks, and the public runner routes do not upload SARIF, verify remote branch protection, install CI-only dependencies or declare protected-branch readiness.
- Full audit, review reuse and gate ownership (R197-R209, R211-R217) name no check; only R210 is tied to the workflow contract.
- Formatting and linting ownership (R218-R243) names no check.
- Review risk (R244-R247) names no check; the review itself is the evidence.
- Rules stated under Enforcement/Mechanisms (the change-type verification matrix and its acceptance statements) are outside the table.

#### Ownership

##### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

##### Review Triggers

Changes land in place with Task evidence; related documents:

- `docs/00.workspace/03.process/github-governance.md`
- `.agents/governance/agentic.md`
- `docs/00.workspace/03.process/git-workflow.md`

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
