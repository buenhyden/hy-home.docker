---
title: "Reference: Automation Pipeline and Workflow Topology"
version: "1.2.1"
type: "reference/research"
status: "published"
owner: "@buenhyden"
updated: "2026-09-27"
layer: "references"
artifact_id: "RES-0002-m0004"
parent_ids:
- "RES-0002"
created: "2026-08-23"
observed_at: "2026-09-05"
reviewed_at: "2026-09-05"
review_cycle: "on-source-change"
---

# Reference: Automation Pipeline and Workflow Topology

## Current External Research

Question: which automation mechanisms establish repeatable checks and controlled
delivery without confusing actors, costs or authority? External sources were
checked on 2026-09-27. Repository baseline:
`f30b168e2fbb0959e4a31749935568fd5b3942f1`. Internal implementation, account,
hosted CI, protection and deployment status: **Not assessed in this run**.

### Integration and delivery boundaries

AWS distinguishes preparing a tested release from automatic production
deployment without explicit approval (C-m0004-01). This pack uses CI for
integration feedback; delivery for maintaining an identified release candidate;
deployment for applying it to a named target. In the pack's interpretation,
test evaluates behavior, build creates output, package defines a distributable,
publish changes a registry, promotion advances a candidate, and rollback
restores an accepted prior state. These are distinct effects and permissions.

**Recommendation:** begin with deterministic checks. Add delivery automation
only with artifact identity, target, consumer, acceptance signal, recovery
condition and accountable approver. Promote the same verified digest where
practical; rebuilding creates a new candidate. A tag, upload, green job and
required check answer different questions. [V&V](m0019-verification-validation.md)
owns evidence; [security](m0017-security-governance.md) owns trust decisions.

### Actions execution and state

| Mechanism | Conditional design choice | Evidence and trade-off |
| --- | --- | --- |
| Workflow/job/step | Name event, runner, ordered work, dependencies and failure behavior. | C-m0004-02; definition is not execution. |
| Event/path filter | Keep required results producible, including merge queues when used. | C-m0004-03; filtered-out required workflows can stay pending. |
| Reusable workflow/composite action | Reuse multi-job contracts or repeated step bundles respectively. | C-m0004-04; different runner/log/secret boundaries; no one-consumer abstraction needed. |
| Matrix/concurrency | Select supported combinations, bound parallel work, cancel obsolete feedback, serialize mutations. | C-m0004-05; cancellation is neither retry nor rollback. |
| Cache/artifact | Cache reproducible dependencies; identify durable outputs and their producer. | C-m0004-06–07; transport digest warnings are not trusted release verification. |
| Required checks/environment | Separate merge restrictions from release approval and secret access. | C-m0004-08–09; eligibility/effective settings need future evidence. |
| OIDC/token | Minimize scopes and constrain cloud subject/audience. | C-m0004-10; obtaining an ID token grants no cloud privilege by itself. |

Current cache guidance qualifies older unlimited-cache descriptions:
low-trust default-branch events default read-only, but write-capable
`cache-mode` can opt out. Checkout's safer fork defaults neither upgrade an old
SHA nor protect every custom fetch path (C-m0004-11–12). These are versioned
improvements, not authorization to run untrusted code in a privileged job.
Runner/PR threats are owned by [m0017](m0017-security-governance.md).

### Hooks and editor actors

| Actor | Execution and authority | Failure/mutation boundary |
| --- | --- | --- |
| Git hook | Git invokes a local executable at a Git event. | Can refuse selected operations but is bypassable; inherits local process authority. Generated message is a draft, not commit/push approval. C-m0004-13. |
| pre-commit | Framework selects hooks by stage, filters and invocation. | Auto-fixes need diff review/rerun; installed/configured/executed differ. Pin reviewed code. C-m0004-14. |
| Editor action/inline edit | Language service, extension or assistant edits a buffer at an explicit action/configured save. | Preview/diff before acceptance; OS/keymap/extensions affect shortcuts. C-m0004-15. |
| Provider lifecycle hook | Provider delivers native events and interprets outputs. | Blocking, async, failure and trust semantics remain [provider-specific](m0012-provider-implementation-comparison.md). |
| CI event | GitHub schedules a runner under scoped identity. | Metadata/code from untrusted sources remain data; local success is not hosted execution or enforced protection. C-m0004-02–03. |

**Recommendation:** keep synchronous hooks deterministic and short. A
documentation hook may propose impacted sections/links; a generator needs a
named owner and check mode. Network-dependent review/test generation needs
opt-in execution, timeouts and explicit failure, not hidden save/commit
dependencies. Review auto-modifications before recording success.

### Automated reviews and test generation

Current Copilot documentation makes approvals and cloud-agent fix handoff
public preview. Default review does not satisfy required approvals; opt-in
preview can change that. Effort, automatic push triggers and skills/MCP context
change work and expense (C-m0004-16). Billing now describes AI Credits plus
Actions minutes, with legacy annual request-based rules separately documented
(C-m0004-17). No account entitlement or charge was observed.

**Recommendation:** begin with advisory review on a bounded diff. Authorize
comments, approving reviews, edits, commits, pushes and PR creation separately.
Cap files, attempts, time, model spend and runner minutes; stop on repeated
unchanged findings. Generation can draft tests (C-m0004-18), but independent
requirements/oracles and a demonstrated failing case establish usefulness.
Measure accepted findings and defect detection, not comments/tests produced.
[Quality](m0014-quality-ci-formatting.md) owns test controls.

## Claims and Sources

Every linked source was opened on **2026-09-27**. `Not supplied` means no
visible publication/update date; mutable documentation has no inferred release
date. Feature state is the official label where given, otherwise documented.

| Claim ID | Claim | Source ID / detailed location | Published/updated | Checked | Product/version/channel; state | Kind | Limit / recheck |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C-m0004-01 | Delivery prepares tested releases; deployment removes explicit production approval. | S-aws-continuous-delivery; Overview, Delivery vs Deployment | Not supplied | 2026-09-27 | AWS practice guidance; no product channel | Fact | Terminology, not local delivery evidence. |
| C-m0004-02 | Jobs, steps, needs, permissions, timeout and failure controls have separate keys. | S-github-workflow-syntax; corresponding keys | Not supplied | 2026-09-27 | Actions current docs; documented | Fact | Shell/platform semantics vary. |
| C-m0004-03 | Branch/path filters combine; skipping a required workflow can leave pending checks; merge_group is separate. | S-github-workflow-syntax; on filters; S-github-workflow-events; merge_group | Not supplied | 2026-09-27 | Actions current docs; documented | Fact | Check settings live outside YAML. |
| C-m0004-04 | Reusable workflows contain jobs; composite actions bundle steps; nested permission cannot increase. | S-github-reusing-configurations; comparison; S-github-reuse-workflows; nesting | Not supplied | 2026-09-27 | Actions current docs; documented | Fact | Secret forwarding must be considered explicitly. |
| C-m0004-05 | Matrix fail-fast defaults true; max-parallel bounds jobs; queue:max and cancel-in-progress:true conflict. | S-github-job-variations; failure/parallelism; S-github-workflow-syntax; concurrency | Not supplied | 2026-09-27 | Actions current docs; documented | Fact | Capacity still constrains jobs. |
| C-m0004-06 | Low-trust default-branch cache defaults read-only with explicit write-mode opt-out. | S-github-dependency-cache; restrictions/cache-mode; S-github-cache-mode-change | Change 2026-09-10; docs not supplied | 2026-09-27 | Actions github.com; released | Fact | Cache contents remain untrusted; verify enterprise parity. |
| C-m0004-07 | Artifact download compares SHA256 digest and warns on mismatch. | S-github-workflow-artifacts; Validating artifacts | Not supplied | 2026-09-27 | Actions artifact tutorial; documented | Fact | Warning does not establish trusted identity/provenance. |
| C-m0004-08 | Rulesets can require checks, expected App source and strict base freshness. | S-github-ruleset-rules; Require status checks | Not supplied | 2026-09-27 | GitHub rulesets; documented | Fact | Enforcement needs readback. |
| C-m0004-09 | Environment rules delay secrets; only one listed reviewer must approve; plan restrictions apply. | S-github-manage-environments; reviewers/secrets | Not supplied | 2026-09-27 | GitHub environments; documented | Fact | Prevent-self-review/bypass settings are separate. |
| C-m0004-10 | id-token:write enables requesting JWT, not other resource writes. | S-github-oidc; Required permission, subject examples | Not supplied | 2026-09-27 | GitHub OIDC; documented | Fact | Cloud trust needs its own evidence. |
| C-m0004-11 | June cache restriction covers low-trust default-branch events. | S-github-read-only-cache-change; affected runs | 2026-06-26 | 2026-09-27 | github.com/Data Residency; released | Fact | September override qualifies historical default. |
| C-m0004-12 | Checkout v7 blocks common fork patterns; old SHA pins do not inherit backports. | S-github-checkout-safety-change; scope/exclusions/editor note | 2026-06-18; note 2026-07-15 | 2026-09-27 | checkout v7 GA; backport enforcement July 20 | Fact | Custom git/gh fetching remains outside protection. |
| C-m0004-13 | pre-commit/commit-msg can abort operations and can be bypassed by no-verify. | S-git-githooks; Description, named hooks, prepare-commit-msg | Manual last change 2.54.0, 2026-04-20 | 2026-09-27 | Git manual; documented | Fact | Bypass capability is not local permission. |
| C-m0004-14 | Stages/filters/modified files control pre-commit outcomes. | S-precommit-documentation; stages, filtering, creating hooks, frozen revisions | Not supplied | 2026-09-27 | pre-commit project docs; documented | Fact | Bootstrap/network/local installs differ from CI. |
| C-m0004-15 | Code Actions use language services/extensions; save modes explicit/always/never differ. | S-vscode-refactoring-source; Code Actions on save, Preview, Keyboard shortcuts | DateApproved 2026-09-16 | 2026-09-27 | VS Code docs main; documented; boolean values planned deprecated | Fact | Official web route later timed out; raw authored source opened. |
| C-m0004-16 | Default review does not satisfy approvals; approval and cloud-agent handoff features are preview. | S-github-copilot-review; approvals, agentic capabilities, triggers | Not supplied | 2026-09-27 | Copilot github.com; named features public preview | Fact | No local setting/seat/review assessed. |
| C-m0004-17 | Code review bills AI Credits plus Actions minutes; legacy annual rules differ. | S-github-copilot-pricing; review costs/legacy annual; S-github-copilot-billing-change | Change 2026-06-01; docs not supplied | 2026-09-27 | Copilot usage billing; released/mutable | Fact | No universal per-review price; recheck rates/plans. |
| C-m0004-18 | Copilot can draft unit tests from code/context. | S-github-copilot-write-tests; generating/improving tests | Not supplied | 2026-09-27 | Copilot tutorial; illustrative | Fact | Output is not test sufficiency evidence. |
| C-m0004-19 | Bound AI review/generation by attempt, time, cost and mutation authority. | C-m0004-16–18 and linked quality/V&V owners | 2026-09-27 analysis | 2026-09-27 | Conditional pack proposal | Recommendation | Separate adoption task required. |

| Source ID | Opened source |
| --- | --- |
| S-aws-continuous-delivery | [AWS delivery](https://aws.amazon.com/devops/continuous-delivery/) |
| S-github-workflow-syntax | [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) |
| S-github-workflow-events | [Workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows) |
| S-github-reusing-configurations | [Reuse/composite comparison](https://docs.github.com/en/actions/concepts/workflows-and-actions/reusing-workflow-configurations) |
| S-github-reuse-workflows | [Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows) |
| S-github-job-variations | [Job variations](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations) |
| S-github-dependency-cache | [Dependency cache](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching) |
| S-github-cache-mode-change | [September cache-mode](https://github.blog/changelog/2026-09-10-control-github-actions-cache-access-with-cache-mode/) |
| S-github-read-only-cache-change | [June read-only cache](https://github.blog/changelog/2026-06-26-read-only-actions-cache-for-untrusted-triggers/) |
| S-github-workflow-artifacts | [Artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data) |
| S-github-ruleset-rules | [Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) |
| S-github-manage-environments | [Environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments) |
| S-github-oidc | [OIDC](https://docs.github.com/en/actions/reference/security/oidc) |
| S-github-checkout-safety-change | [Checkout safety and corrected backport note](https://github.blog/changelog/2026-06-18-safer-pull_request_target-defaults-for-github-actions-checkout/) |
| S-git-githooks | [Git hooks](https://git-scm.com/docs/githooks) |
| S-precommit-documentation | [pre-commit](https://pre-commit.com/) |
| S-vscode-refactoring-source | [Microsoft refactoring source](https://raw.githubusercontent.com/microsoft/vscode-docs/main/docs/editing/refactoring.md) |
| S-github-copilot-review | [Copilot review](https://docs.github.com/en/copilot/concepts/agents/code-review) |
| S-github-copilot-pricing | [Copilot pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing) |
| S-github-copilot-billing-change | [June billing release](https://github.blog/changelog/2026-06-01-updates-to-github-copilot-billing-and-plans/) |
| S-github-copilot-write-tests | [Copilot tests](https://docs.github.com/en/copilot/tutorials/write-tests) |

## Future Internal Checks

Surface candidates are historically named routes, not inspected implementation
owners; new consumer/budget/editor surfaces below are hypothetical.

| Topic / claims | Analysis scope | Applicability condition | Future surface candidate | Concrete question | Required evidence | Future method | Pass / fail criterion | Additional authority / risk | Expected owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pipeline C-m0004-01–03 | repository/task/CI; architecture/QA | Check/delivery proposed | Historical workflow contract/YAML; hypothetical promotion record | Does each stage identify candidate, event, inputs and result? | Versioned plan, selected leaves, exit outcomes | Authorized static review then named run | Pass: no inferred execution/hidden soft failure; fail: missing result | Hosted run separately authorized | CI/QA | Not assessed in this run |
| Reuse/matrix/concurrency C-m0004-04–05 | package/CI; common/QA | Repeated logic/supported combinations | Workflow candidates; hypothetical shared workflow | Can cancellation interrupt mutation or omit required combinations? | Dependency graph, cancellation/matrix cases | Approved isolated workflow fixture | Pass: all required results accounted for; fail: cancellation masks failure | Remote runs/runner spend | CI engineer | Not assessed in this run |
| Cache/artifact C-m0004-06–07,11–12 | CI/environment; security/QA | Cross-run data consumed | Cache-mode/restore candidates; hypothetical artifact consumer | Can low-trust output reach privileged execution; is required verification fail-closed? | Trust map, exact pins, tamper fixtures | Static flow review and approved isolated fixture | Pass: explicit producer trust/verifier; fail: warning-only release acceptance | No production poisoning; registry access needs approval | Security/CI | Not assessed in this run |
| Checks/environment/OIDC C-m0004-08–10 | CI/provider; governance/ops | Merge/cloud release designed | Historical protection proposal; hypothetical environment/cloud trust | Do effective settings match target, App, subject and approver? | Redacted readback and denied-subject fixture | Approved readback/isolated auth test | Pass: intended subject/approver only; fail: declared-only/broadened grant | Remote settings, credential exchange/deployment separately authorized | Security/ops | Not assessed in this run |
| Hooks/editor/docs C-m0004-13–15 | user/repository/session; common/docs | Local automation selected | Historical pre-commit config; hypothetical editor/provider hooks | Who executes/mutates; are changes and failed runs re-reviewed? | Event contract, filters, versions, before/after diff | Metadata inspection and safe fixture | Pass: explicit actor/outcome/review; fail: bypass called enforcement | Executable hooks/extensions trusted code; global settings approval | DevEx/docs | Not assessed in this run |
| AI review/tests C-m0004-16–19 | task/provider/CI; product/QA/security | Paid reviewer/generator selected | Hypothetical policy/budget/test-design record | Can approval/mutation escape authority; do tests catch independent defects? | Policy modes, budget, bounded attempts, failing case | Approved non-sensitive trial and independent review | Pass: stop bounds/meaningful oracle; fail: unlimited/self-confirming loop | Billing/comments/approvals/PRs each separately authorized | QA/product/security | Not assessed in this run |

### Limitations and preservation decision

Reopen sources after feature, billing, action, runner or trust-policy changes.
No numerical limit is carried forward as timeless authority.
[RES-0084](../0084-github-actions-platform/README.md) retains distinct dated
platform/hosted/remote observations. This member owns new external automation
analysis; the quotation below preserves the complete predecessor body without
reassessing apparently conflicting remote states observed at different times.

## Historical workspace observations — not reassessed in this run

> Historical evidence (not current authority; source: Git history):
>
> Current routing (2026-09-08): [canonical agent governance](../../../../.agents/README.md) and
> [ADR-0032](../../../02.architecture/decisions/0032-canonical-agent-governance-home.md) own the active source location.
> Earlier Stage 00 paths, inventories, provider projections, and check results
> below remain dated observations, not current instructions or new runtime
> acceptance evidence. Source links now navigate to current owners; the
> original `observed_at`, `reviewed_at`, status, and measured facts are preserved.
>
> <div id="overview"></div>
>
> ## Overview
>
> **Historical baseline notice.** The counts and remote-state conclusion in this
> section describe the named Task 7 and 2026-08-14 observations. They are
> preserved evidence, not current topology. The current interpretation below
> routes to the workflow contract, protection policy and dated Task evidence.
>
> At Task 7 baseline `c57d33f37843802f7692261c50801f0dd966d7cb`,
> the tracked GitHub automation surface contains 7 workflow files and 23 jobs.
> The typed registry in `.github/workflow-contract.yml` contains 80 gate nodes:
> 48 leaves, 26 aggregates, and 6 setup nodes. Sixteen required-quality jobs
> have registered roots, three local profiles have registered root lists, and
> eight distinct external Actions are registered at full commit SHAs.
>
> Those figures describe tracked configuration. They do not prove a workflow
> ran, a required check is remotely enforced, an environment exists, a secret is
> configured, or a deployment succeeded. Task 7 performed no authenticated
> control-plane readback and no workflow dispatch, so all current remote state is
> `UNVERIFIED`.
>
> Re-verified independently at `ece3eda9c3e1a603c6495dd55caba7df1c29ef6c` on
> 2026-08-14: the workflow count, job count, gate-node kind counts (48/26/6),
> job-root count, and profile-root counts (18/16/19) are unchanged from the Task
> 7 baseline, and `check-github-workflow-contract.py` still returns
> `PASS: GitHub workflow contract (workflows=7, jobs=23, actions=8)`. A fresh
> `grep` across all seven tracked workflow files found zero occurrences of
> `continue-on-error`, `needs:`, `matrix:`, or `workflow_call`, and zero
> non-SHA (`@main`/`@master`/floating-tag) `uses:` references. That absence is
> itself load-bearing evidence, not a gap by omission — see "Reusable
> workflows, OIDC, and `continue-on-error`" below.
>
> <div id="purpose"></div>
>
> ## Purpose
>
> Support REQ-24 and REQ-25 by documenting the exact automation topology,
> ordered gate expansion, permissions, action pinning, failure behavior, and
> delivery boundary without reducing a multi-leaf job to a false one-job/
> one-command rule or presenting continuous integration as continuous delivery.
>
> <div id="repository-role"></div>
>
> ## Repository Role
>
> This Stage 90 reference is advisory analysis. The tracked workflow registry,
> workflow YAML, scripts, canonical agent governance governance, and any separately authorized
> remote GitHub readback remain the evidence owners. This document neither
> changes those owners nor authorizes dispatch, push, promotion, deployment,
> ruleset, environment, secret, release, or rollback actions.
>
> <div id="scope"></div>
>
> ## Scope
>
> <div id="in-scope"></div>
>
> ### In scope
>
> - The seven tracked workflows, twenty-three jobs, typed gate DAG, registered
>   profiles, and external Action inventory.
> - Trigger, permission, pinning, concurrency, timeout, ordering, failure, retry,
>   observability, and remote-enforcement boundaries.
> - The distinction among local configuration, local execution, declared CI,
>   and observed remote state.
> - CI/CD, promotion, deployment, artifact, attestation, and rollback gaps.
> - Adoption rules, evidence limitations, owners, and all fourteen scopes.
>
> <div id="out-of-scope"></div>
>
> ### Out of scope
>
> - Running a local QA profile beyond list mode or dispatching any workflow.
> - Authenticated inspection or mutation of rulesets, branch protection, runs,
>   environments, deployments, releases, secrets, variables, or artifacts.
> - Changing workflows, actions, scripts, contracts, provider surfaces, or
>   generated outputs.
> - Treating the stale Graphify report or the 2026-07-26 public snapshot as
>   current control-plane truth.
>
> <div id="definitions--facts"></div>
>
> ## Definitions / Facts
>
> <div id="evidence-layers"></div>
>
> ### Evidence layers
>
> | Layer                   | What Task 7 can establish                                                                                            | What remains outside the evidence                                                                                                              |
> | ----------------------- | -------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
> | Tracked configuration   | Exact YAML/JSON, gate registrations, roots, pins, permissions, scripts, and tests at the baseline commit.            | Execution, hosted-run success, secret availability, and applied settings.                                                                      |
> | Local static validation | `check-github-workflow-contract.py` passed; local list mode expanded the registered profile without executing gates. | Results for the 34 listed leaves and GitHub-only behavior.                                                                                     |
> | Declared CI             | The jobs and steps GitHub would evaluate after a matching event reaches this revision.                               | Whether that event occurred, the effective runner state, logs, artifacts, and conclusions.                                                     |
> | Remote control plane    | No current authorized observation was performed.                                                                     | Rulesets, required checks, branch protection, runs, environments, deployments, promotions, secrets, releases, and rollback are **UNVERIFIED**. |
>
> The Graphify report was built from `f8a72211` and is stale. It was used only as
> navigation; every fact below was re-derived from tracked owners.
>
> <div id="measured-typed-topology"></div>
>
> ### Measured typed topology
>
> | Registry surface           | Count | Derivation and interpretation                                                                              |
> | -------------------------- | ----: | ---------------------------------------------------------------------------------------------------------- |
> | Workflows                  |     7 | `workflows` object and sorted `.github/workflows/*.yml` inventory.                                         |
> | Jobs                       |    23 | Job mappings across all seven workflow definitions.                                                        |
> | Gate nodes                 |    80 | 48 `leaf`, 26 `aggregate`, 6 `setup`; kinds are not interchangeable.                                       |
> | Required-quality job roots |    16 | Each names the CI root or ordered leaves admitted for one job.                                             |
> | Local profile records      |     3 | `local-script-backed`, `local-harness`, and `local-all-profiles`.                                          |
> | External Actions           |     8 | Registered external repositories; no tracked `.github/actions/` directory exists.                          |
> | Resolved Action references |    32 | YAML-anchor-aware parse; 17 literal `uses:` lines become 32 references. All 32 use full 40-character SHAs. |
>
> `python3 scripts/validation/check-github-workflow-contract.py` returned
> `PASS: GitHub workflow contract (workflows=7, jobs=23, actions=8)`. This proves
> the static contract at the observed worktree only.
>
> <div id="gate-node-schema"></div>
>
> ### Gate node schema
>
> Each of the 80 `gate_nodes` records is a typed object, not a bare string.
> Parsing the registry directly (`yaml.safe_load` over
> `.github/workflow-contract.yml`) shows the exact shape:
>
> ```json
> {
>   "gate_id": "ci.agent-output-eval-fixture-gate",
>   "kind": "aggregate",
>   "profiles": ["ci", "local-script-backed", "local-harness", "local-all-profiles"],
>   "opaque": false,
>   "children": ["leaf.agent-output-eval-fixture-regressions", "leaf.agent-output-eval-fixture-gate"]
> }
> ```
>
> `kind` is one of `leaf` (48, an actual command/check), `aggregate` (26, a
> named group whose ordered `children` expand to leaves/setup nodes), or
> `setup` (6, dependency/environment preparation that precedes leaves but is
> not itself a check). `profiles` lists which of the four profiles
> (`ci`, `local-script-backed`, `local-harness`, `local-all-profiles`) may
> select that node; a node absent from `ci` cannot appear in the hosted
> expansion no matter how the workflow YAML is edited, because the focused
> checker verifies the expansion against this registry, not against workflow
> prose. `job_roots` is a separate 16-entry list, each record binding one
> `workflow` path, one `job_id`, one `root_gate_id`, and a `classification`
> (all 16 are `required-quality`); its `job_id` sequence is
> `docs-traceability, docs-implementation-alignment, repo-contracts,
> agent-output-eval-fixture-gate, supply-chain-fixture-policy,
> dependency-vulnerability-audit, git-flow-contract, compose-validation,
> compose-all-profiles-validation, infrastructure-hardening,
> template-security-baseline, quickwin-baseline, pre-commit, frontend-quality,
> storybook-coverage, zizmor`. `profile_roots` is a third list keyed by
> `profile` with a `root_gate_ids` array (18/16/19 entries respectively).
> These three lists are structurally independent; the checker's job is to
> prove each expands into the ordered executable set claimed above without
> duplicating or omitting a leaf.
>
> <div id="workflow-and-job-inventory"></div>
>
> ### Workflow and job inventory
>
> | Workflow                        | Trigger                                    | Jobs | Class and mutation boundary                                                                                              |
> | ------------------------------- | ------------------------------------------ | ---: | ------------------------------------------------------------------------------------------------------------------------ |
> | `ci-quality.yml`                | Push/PR to `main`; manual dispatch         |   16 | Required-quality definition. Read-only by default; `zizmor` adds `actions: read` and `security-events: write` for SARIF. |
> | `document-corpus-lifecycle.yml` | Weekly schedule; manual dispatch           |    1 | Non-gating read-only lifecycle checks and advisory reports.                                                              |
> | `generate-changelog.yml`        | `v*.*.*` tag push                          |    1 | Verifies a pre-existing changelog entry; it does not generate a changelog, release, or deployment.                       |
> | `greetings.yml`                 | First opened issue/PR                      |    2 | Non-gating issue/PR comment mutation with job-scoped token permissions.                                                  |
> | `pr-labeler.yml`                | Opened/synchronized/reopened PR to `main`  |    1 | Non-gating PR-label mutation.                                                                                            |
> | `stale.yml`                     | Daily schedule                             |    1 | Non-gating issue/PR label and close mutation.                                                                            |
> | `tech-stack-version-sync.yml`   | Relevant Compose/version-registry PR paths |    1 | Read-only drift check; it does not auto-commit or deploy.                                                                |
>
> All seven workflows explicitly declare top-level permissions. Four declare
> concurrency groups with `cancel-in-progress: true`; cancellation replaces an
> obsolete in-flight run, not a retry policy. Every registered job has a timeout
> of 5, 10, 15, or 20 minutes.
>
> <div id="ordered-expansion-is-the-executable-contract"></div>
>
> ### Ordered expansion is the executable contract
>
> The 16 required-quality jobs are roots into a DAG, not sixteen shell commands.
> The direct runner lists 38 CI executable nodes after ordered expansion: 32
> leaves and 6 setup nodes. For example:
>
> - `ci.repo-contracts` expands to metadata-base verification, Python dependency
>   setup, changed-document metadata, five Python regression leaves, one shell
>   regression leaf, workflow-contract validation, and repository contracts.
> - `ci.frontend-quality` expands to Node dependency setup, lint, typecheck,
>   Next.js build, and Storybook build.
> - `ci.storybook-coverage` expands to Node dependency setup, Playwright browser
>   setup, and the coverage leaf.
> - `docs-implementation-alignment` deliberately invokes
>   `leaf.docs-implementation-alignment` and then
>   `leaf.docs-qa-gate-recommendations`; the second uses `if: always()` so the
>   advisory summary is attempted even when alignment fails.
>
> The last case is why “one job, one command” is false. The typed root owns two
> ordered leaves, and the workflow spells them as two static invocations to
> preserve the `always()` behavior. The focused contract checker validates the
> ordered projection rather than requiring one textual `run:` step.
>
> No tracked job declares `needs:`, a matrix, or a deployment environment. CI
> therefore fans out across independent jobs; ordering exists inside each job's
> root expansion, not as a repository-wide staged pipeline.
>
> <div id="local-profiles"></div>
>
> ### Local profiles
>
> | Profile               | Registered roots |  Ordered executable expansion | Evidence boundary                                                            |
> | --------------------- | ---------------: | ----------------------------: | ---------------------------------------------------------------------------- |
> | `local-script-backed` |               18 |                     34 leaves | Default local script-backed set. Task 7 used `--list`, which executed none.  |
> | `local-harness`       |               16 |                     32 leaves | Omits tech-stack drift, QuickWin, and all-profile Compose.                   |
> | `local-all-profiles`  |               19 |                     35 leaves | Adds all-profile Compose validation.                                         |
> | `ci`                  |     16 job roots | 38 nodes: 32 leaves + 6 setup | GitHub-oriented expansion; includes dependency setup and GitHub-only leaves. |
>
> `run-ci-gate.py` is the single public dispatcher into the typed runner. Its
> profile and gate expansion come from the workflow contract rather than a
> second hand-maintained shell command list. Hosted-only evidence, protected-
> branch enforcement, and the separately controlled Agent all-files pre-commit
> route remain outside local execution claims.
>
> <div id="promotion-path-local-check-to-required-remote-check"></div>
>
> ### Promotion path: local check to required remote check
>
> > Historical evidence (not current authority; source: Git history): Recorded source path at the document observation baseline.
> > Adding, changing, or retiring a required-quality job is a coupled three-surface
> > change, not a single-file edit. `docs/00.agent-governance/rules/
> > github-governance.md` §8 states the constraint explicitly: `.github/
> > workflow-contract.yml` (typed root/registration), `.github/workflows/
> > ci-quality.yml` (the actual `run:` step invoking `run-ci-gate.py --profile ci
> > --gate <id>`), and `.github/rulesets/main-protection.md` (the desired-state
> > Required Status Checks list) must change together, followed by an update to
> > the explanatory table in that same governance file.
>
> Re-deriving both sides today confirms the desired state is currently
> consistent: the 16 `job_id` values in `workflow-contract.yml`'s `job_roots`
> and the 16 check names listed under "Required Status Checks" in
> `main-protection.md` are the same 16 strings in the same order
> (`docs-traceability` through `zizmor`). That structural match is
> `Workspace tracked` evidence that the _desired_ remote contract is internally
> coherent — it is not evidence that GitHub enforces it. `main-protection.md`
> says so directly: "Until that separately approved readback succeeds, all 16
> checks above remain tracked desired state rather than evidence of remote
> enforcement," and names the exact commands
> (`gh api repos/<org>/<repo>/rulesets --paginate`,
> `gh api repos/<org>/<repo>/branches/main/protection`) that would close the
> gap. Neither command was run by this leaf.
>
> The full promotion path a change must complete before a local check becomes a
> remote-required check is therefore:
>
> 1. **Local static validation** — the gate exists in `workflow-contract.yml`
>    and passes `check-github-workflow-contract.py`.
> 2. **Declared CI** — the same gate ID is invoked from a `run:` step inside a
>    job in `ci-quality.yml`, and the ordered expansion matches the registry.
> 3. **Desired remote contract** — the job's name is added to
>    `main-protection.md`'s Required Status Checks list (`Workspace tracked`
>    proposal only).
> 4. **Applied remote ruleset** — a repository owner applies the ruleset or
>    branch-protection rule through the GitHub UI or an audited `gh api` call,
>    per `main-protection.md`'s "Application Boundary" — this step is outside
>    any tracked file and requires separate human/authorized-agent action.
> 5. **Verified remote enforcement** — an authenticated readback (the two `gh
> api` commands above, or equivalent) confirms the rule is live and lists
>    which checks it actually requires.
>
> Steps 1-3 are what this repository's tracked files can establish today. Steps
> 4-5 are `UNVERIFIED` for every one of the 16 gates; no Task in this pack has
> performed an authenticated ruleset or branch-protection readback. A job
> appearing in `main-protection.md` is therefore necessary but not sufficient
> evidence that GitHub will actually block a merge without it.
>
> <div id="reusable-workflows-oidc-and-continue-on-error-absent-not-merely-unverified"></div>
>
> ### Reusable workflows, OIDC, and `continue-on-error`: absent, not merely unverified
>
> Three GitHub Actions capabilities relevant to pipeline maturity are entirely
> unused in this repository today, confirmed by direct grep over all seven
> workflow files at `ece3eda9` on 2026-08-14:
>
> - **Reusable workflows** (`workflow_call` triggers and cross-file `uses:
> ./.github/workflows/<file>.yml` or `owner/repo/.github/workflows/
> <file>.yml@<ref>` job-level calls) let one workflow definition be shared
>   across callers, with inputs/secrets passed explicitly or via `secrets:
> inherit`, and with permissions only reducible (never elevatable) through a
>   call chain up to 10 levels deep. Zero occurrences of `workflow_call` exist
>   here; each of the seven workflows is self-contained. There is currently
>   nothing to reuse across repositories or across the seven local workflows
>   that would justify one, since none share job bodies beyond the checkout
>   step already factored into a YAML anchor (`&checkout` in `ci-quality.yml`).
> - **OIDC** (`permissions: id-token: write` plus a cloud-side trust policy
>   keyed on the token's `sub`/`repo`/`ref`/`environment`/`actor` claims) lets a
>   workflow exchange a short-lived, auto-rotated token for cloud credentials
>   instead of storing a long-lived secret. Zero occurrences of `id-token` or
>   any `id-token: write` permission exist here. This is consistent with the
>   independently confirmed fact that no non-GitHub credential or deployment
>   secret is declared in any of the seven workflows: there is no cloud target
>   to authenticate to yet, so OIDC is not a current gap, only a prerequisite
>   the moment a cloud deployment job is proposed.
> - **`continue-on-error`** lets a step or job fail without failing the
>   workflow (`steps.[id].outcome` still records `failure`, but
>   `steps.[id].conclusion` and the job/workflow conclusion report success).
>   Zero occurrences exist here, corroborating the leaf's existing "Failure
>   propagation" finding: every registered gate is a hard, non-soft-failing
>   check, with no experimental or best-effort job silently masking a red
>   result as green.
>
> None of these three absences is itself a defect; they are the correct
> baseline for a repository with no current cloud-deployment or cross-repository
> workflow-sharing surface. They become adoption prerequisites, not optional
> polish, the moment a future Spec proposes a deployment job: that job would
> need OIDC (not a stored cloud secret) under GitHub's current secure-use
> guidance, and any shared step logic extracted for a second workflow or
> repository would need `workflow_call` rather than copy-paste duplication.
>
> <div id="action-permission-and-secret-boundaries"></div>
>
> ### Action, permission, and secret boundaries
>
> The registry records eight external Actions with pinned manifest URLs,
> `runtime: node24`, retrieval date `2026-07-28`, consumers, and an approved
> tracked disposition. All 32 resolved uses are full-SHA pins, consistent with
> GitHub's current secure-use guidance. The registry and checker cannot prove
> that a remote Action remained uncompromised after review.
>
> `ci-quality.yml` defaults to `contents: read`; only `zizmor` elevates the
> permissions needed for SARIF. Greetings and labeling use `GITHUB_TOKEN` with
> job-scoped write grants. No non-GitHub credential or deployment secret is
> declared in the seven workflow files. Whether any repository/environment
> secret exists remotely is `UNVERIFIED` and was not queried.
>
> <div id="failure-propagation-retry-and-observation"></div>
>
> ### Failure propagation, retry, and observation
>
> - The typed runner executes the unique ordered expansion and returns on the
>   first non-zero child. The local wrapper uses `set -euo pipefail`.
> - No workflow or registered gate declares retry, backoff, attempt count, or
>   `continue-on-error`. A human or authorized GitHub actor must correct the
>   owner and rerun; that operational rerun is not encoded as an automatic loop.
> - The alignment job's `if: always()` recommendation step does not neutralize
>   the preceding failure. It preserves bounded diagnostic output.
> - GitHub documents run graphs, job/step status, timings, and downloadable logs
>   as monitoring surfaces. No current Task 7 run or log was observed.
> - The tracked public snapshot dated 2026-07-26 records a failed remote run but
>   explicitly marks its root cause and control-plane verification unverified;
>   it cannot establish current state.
>
> <div id="ci-is-implemented-cd-is-not-established"></div>
>
> ### CI is implemented; CD is not established
>
> No tracked workflow declares `environment:`, deployment jobs, artifact upload
> for a releasable build, artifact attestations, promotion stages, or rollback
> commands. The SARIF upload is security-analysis output, not a deployable
> release artifact. The tag workflow verifies changelog coverage only.
>
> GitHub environments can gate environment secrets and jobs behind reviewer,
> branch/tag, wait-timer, and custom protection rules; deployment history can
> link environments, commits, workflow logs, URLs, and statuses. Artifact
> attestations can establish build provenance. None of those upstream
> capabilities is tracked as adopted delivery behavior here, and current remote
> environment/deployment state is `UNVERIFIED`.
>
> <div id="adoption-rules-gaps-and-follow-up-route"></div>
>
> ### Adoption rules, gaps, and follow-up route
>
> 1. Extend the typed registry, workflow YAML, desired required-check proposal,
>    and explanatory governance together for any required-job change.
> 2. Keep every external Action full-SHA pinned, registered, manifest-reviewed,
>    runtime-classified, and permission-minimal.
> 3. Preserve ordered expansion and failure semantics; never infer one command
>    from one job or collapse setup/leaf distinctions.
> 4. Record local static validation, local execution, declared CI, observed run,
>    and applied remote enforcement as separate evidence.
> 5. A future delivery design must name artifact identity, provenance, target
>    environments, promotion approvals, deployment verification, rollback
>    trigger/action/evidence, observability, secret boundary, and recovery owner
>    in Stage 03/04 before workflow adoption.
> 6. Remote readback or mutation requires separate user approval for the named
>    repository and surface. This reference supplies no such authority.
>
> <div id="evidence-ladder-and-adoption-mechanics"></div>
>
> ### Evidence ladder and adoption mechanics
>
> Use the narrowest accurate state: **configured** for tracked YAML or a gate
> registry, **selected** for an approved plan naming a job, **executed** and
> **passed** only for recorded command evidence, **hosted** only for an observed
> GitHub run, and **enforced** only for observed branch/ruleset/environment
> controls. These states do not imply one another.
>
> The local path is a developer-controlled check or hook. The pull-request and
> push paths are separately declared workflow triggers; a tag check has its own
> trigger. A job should expose the immutable revision, command, inputs, result,
> and owner in its durable task evidence. If the change adds an action, token,
> artifact, dependency, or deployment path, inspect pinning, least privilege,
> provenance, protected-secret timing, approval authority, and recovery before
> calling it a promotion path.
>
> No current configuration proves a required check, a branch rule, a successful
> hosted job, an artifact attestation, dependency provenance, OIDC exchange, or
> a deployment. A workflow filename or YAML `permissions` block is therefore not
> permission to mutate a remote target.
>
> | Control | Declared mechanics | Exact local investigation target | Limit |
> | --- | --- | --- | --- |
> | Action pinning | Workflow `uses:` declarations use full commit SHAs. | `.github/workflows/*.yml` and `.github/workflow-contract.yml` | A pin does not prove the action executed or is sufficient for a particular threat. |
> | Least privilege | Workflow and job `permissions` declarations bound token scopes. | `ci-quality.yml`, `document-corpus-lifecycle.yml`, and workflow registry | YAML does not reveal effective repository defaults or token use at runtime. |
> | Environment approval / protected secrets | GitHub environments can defer access until protection rules pass. | `.github/workflows/*.yml` for `environment:` and `.github/workflow-contract.yml` | No environment declaration, secret value, approval, or remote protection was observed. |
> | Artifact and attestation | Artifact/attestation steps would identify and publish a build output and provenance. | `.github/workflows/*.yml`; `scripts/validation/github_workflow_contract.py` | No tracked hosted artifact or attestation proves a supply-chain result. |
> | Dependency provenance | Dependency/audit gates can bound a declared dependency set. | `projects/storybook/nextjs/package-lock.json`, `ci-quality.yml` | A lockfile or audit-job definition is not registry resolution, SBOM, or deployed-image evidence. |
> | Reuse and OIDC | Reusable workflow and OIDC mechanisms need job-level use and explicit `id-token: write`. | `.github/workflows/*.yml` | Neither mechanism is declared by the measured workflow set. |
> | Local / PR / push separation | Hooks are local; CI Quality declares `pull_request` and `push` on `main`; changelog checking is tag-triggered. | `.pre-commit-config.yaml`, `ci-quality.yml`, `generate-changelog.yml` | Definitions do not show which path ran or whether a PR was merged. |
>
> <div id="scope-implications"></div>
>
> ## Scope Implications
>
> | Scope          | Automation implication                                                                                                                                                       |
> | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | `agentic`      | Use typed roots and sanitized Task evidence; provider hooks and local orchestration do not prove hosted CI or remote enforcement.                                            |
> | `architecture` | Any CD, promotion, artifact, or rollback design starts with explicit targets, trust boundaries, failure modes, and an approved architecture contract.                        |
> | `backend`      | No current backend delivery surface is established; future service pipelines require a backend Spec, tests, artifacts, environment, and rollback owner.                      |
> | `common`       | Shared diff, syntax, metadata, and review gates apply, but one shared profile must not erase surface-specific checks.                                                        |
> | `docs`         | Document changes use metadata, traceability, implementation-alignment, and repository-contract owners; Stage 90 analysis does not make a check remote-required.              |
> | `entry`        | Gateway changes require configuration, security, and recovery gates tied to the tracked entry surface; no deployment route is currently evidenced.                           |
> | `frontend`     | Frontend quality and Storybook coverage are CI roots; their build output is not a promoted or attested release artifact.                                                     |
> | `infra`        | Compose and hardening gates validate tracked configuration only; live apply, promotion, environment secrets, and rollback remain separately authorized operations.           |
> | `meta`         | The schema, DAG, profile, root, environment-key, action, and validator contracts are the automation metadata owners; counts must be re-derived from them.                    |
> | `mobile`       | No mobile source or delivery workflow is established, so mobile automation and promotion are not applicable until an approved surface exists.                                |
> | `ops`          | Operations owns future deployment verification, observability, rollback, recovery, and release evidence; current workflows provide no production event proof.                |
> | `product`      | Product intent defines release value and acceptance; a green build or tag-string check is not evidence of user delivery.                                                     |
> | `qa`           | QA maps changed surfaces to ordered local and CI gates and records skips; current remote check conclusions remain unverified.                                                |
> | `security`     | Enforce least privilege, SHA pins, secret-safe output, dependency/workflow scanning, and explicit promotion approvals without treating scanner success as complete security. |
>
> <div id="sources"></div>
>
> ## Sources
>
> <!-- Historical evidence table (not current authority; source: Git history). -->
> | Source                                                                                                                                                       | Accessed                           | Class                                  | Verification state                                                                                                                                                                                                                          |
> | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | [GitHub Actions workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions)                                    | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified official page; prescribed route redirected to current workflow-syntax reference; trigger, permission, job, environment, timeout, and step semantics used.                                                                          |
> | [GitHub secure use reference](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)          | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified official page; prescribed route redirected to current secure-use reference; least privilege and full-SHA pinning used.                                                                                                             |
> | [Using `GITHUB_TOKEN`](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication)                        | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified official page; prescribed route redirected to current tutorial; job/workflow permission minimization used.                                                                                                                         |
> | [Managing deployment environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)                   | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified direct official page; protection, reviewer, branch/tag, and secret timing capability only; local adoption not inferred.                                                                                                            |
> | [Viewing deployment history](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/view-deployment-history)                     | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified direct official page; history/commit/log/status capability only; no repository observation.                                                                                                                                        |
> | [Workflow artifacts](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-what-your-workflow-does/storing-and-sharing-data-from-a-workflow) | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified official page; route redirected to current tutorial; upload/download/retention/digest capability only.                                                                                                                             |
> | [Artifact attestations](https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations)                                          | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified official page; prescribed route redirected to current how-to; provenance capability only.                                                                                                                                          |
> | [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)               | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified direct official page; active/disabled enforcement and layering capability do not prove this repository's settings.                                                                                                                 |
> | [Monitoring workflows](https://docs.github.com/en/actions/how-tos/monitor-workflows)                                                                         | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified direct official page; graph, status, timing, and log capability only; no Task 7 run observed.                                                                                                                                      |
> | [Reusing workflows](https://docs.github.com/en/actions/sharing-automations/reusing-workflows)                                                                | 2026-08-14                         | External mutable                       | Verified official page; `workflow_call`, `uses:` at job level, SHA-pin recommendation, 10-level nesting, and permission-reduction-only-through-chain semantics used; this repository uses none of it.                                       |
> | [OpenID Connect reference](https://docs.github.com/en/actions/reference/security/oidc)                                                                       | 2026-08-14                         | External mutable                       | Verified official page; `permissions: id-token: write`, `sub`/`repo`/`ref`/`environment`/`actor` claims, and subject-condition guidance used; this repository declares no `id-token` permission.                                            |
> | `continue-on-error` step/job semantics                                                                                                                       | 2026-08-14                         | External mutable                       | GitHub workflow-syntax documentation corroborated by secondary technical sources; step-level masks `conclusion` to success while `outcome` still records failure, job-level masks the workflow conclusion; this repository uses it nowhere. |
> | [Typed workflow registry](../../../../.github/workflow-contract.yml)                                                                                         | 2026-08-08; re-verified 2026-08-14 | Workspace tracked                      | Complete registry re-parsed with `yaml.safe_load` at `ece3eda9`: 80 `gate_nodes` (48 leaf/26 aggregate/6 setup), 16 `job_roots`, 3 `profile_roots` (18/16/19), 8 `actions`, all unchanged from the `c57d33f` baseline.                      |
> | [Tracked workflows](../../../../.github/workflows/ci-quality.yml)                                                                                            | 2026-08-08; re-verified 2026-08-14 | Workspace tracked                      | All seven files re-read at `ece3eda9`; 23 jobs, triggers, permissions, concurrency, steps confirmed; grep confirmed zero `continue-on-error`/`needs:`/`matrix:`/`workflow_call` occurrences.                                                |
> | [Workflow contract checker](../../../../scripts/validation/check-github-workflow-contract.py)                                                                | 2026-08-08; re-run 2026-08-14      | Workspace tracked/local execution      | Static check PASS re-run directly at `ece3eda9`; no hosted run or control-plane proof.                                                                                                                                                      |
> | [Typed validation dispatcher](../../../../scripts/validation/run-ci-gate.py)                                                                                 | 2026-08-08; current route re-verified 2026-09-04 | Workspace tracked/local list execution | The historical `--list` observation executed no leaves; the current dispatcher derives its ordered expansion from the typed workflow contract.                                                                                                                                                |
> | [Desired main protection proposal](../../../../.github/rulesets/main-protection.md)                                                                          | 2026-08-08; re-verified 2026-08-14 | Workspace tracked proposal             | Sixteen desired check names re-read; confirmed byte-for-byte identical set and order to `job_roots`' 16 `job_id` values; explicitly not applied-state evidence.                                                                             |
> | [GitHub governance policy](../../../../.agents/governance/github-governance.md)                                                                          | 2026-08-14                         | Workspace tracked policy               | §8 "CI/CD Job Taxonomy" read in full; three-surface coupling constraint, `pre-commit` job's exact pinned-dependency install path, and non-gating workflow table used.                                                                       |
> | Public control-plane snapshot (retired DATA-0071)                                                         | 2026-08-08                         | Historical retained observation        | Dated 2026-07-26; current rules, failure cause, and remote enforcement remain `UNVERIFIED`.                                                                                                                                                 |
> | Graphify report (`graphify-out/GRAPH_REPORT.md`, untracked local output since 2026-09-08)                                                                                                  | 2026-08-08                         | Workspace tracked stale/advisory       | Built from `f8a72211`; corroborated and not used as current proof.                                                                                                                                                                          |
>
> <div id="scope-application"></div>
>
> ## Scope Application
>
> | Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
> | --- | --- | --- | --- | --- |
> | agentic | applies | Route automated agent work through an approved Task and gate. | Inspect Task evidence and gate name. | Dispatch is not hosted execution. |
> | architecture | applies | Review automation boundaries when a system contract changes. | Inspect approved design/change record. | No architecture change is proposed. |
> | common | applies | Keep shared workflow triggers and permissions explicit. | Inspect registry/YAML correspondence. | Static match is not enforcement. |
> | docs | applies | Use documentation checks for changed documentation. | Record the exact validator result. | A check result is not content acceptance. |
> | infra | applies | Require a target-specific delivery contract before deployment automation. | Inspect approved environment/recovery evidence. | No environment is observed. |
> | ops | applies | Assign release/rollback ownership before remote mutation. | Inspect an approved runbook and event record. | No release event is claimed. |
> | qa | applies | Select a named CI gate for the stated oracle. | Inspect gate contract and result. | CI configuration alone is not a pass. |
> | security | applies | Review actions, permissions, secrets, provenance, and approvals. | Inspect pinned action and permission declarations. | OIDC, attestations, and protection remain unobserved. |
>
> <div id="2026-09-05-revalidation"></div>
>
> ## 2026-09-05 Revalidation
>
> Baseline: `main@4c6d211129615eab372d720ebd209b6c27618c86`.
> The current CI contract projects registered leaves through two aggregate jobs:
> `validation-changed` for pull requests and `validation-full` for push/manual
> full execution. SPEC-0172 records Hosted success for both routes and the
> approved 2026-09-05 `main` protection read-back.
>
> | Capability | Repository implementation | Evidence depth | Gap | Verification route |
> | --- | --- | --- | --- | --- |
> | Local/Hosted CI | Typed gate DAG and two aggregate workflow jobs | Repository-enforced, Hosted-executed | Future runs remain mutable | public gate plus Actions run evidence |
> | Required checks | `strict=true`; both aggregate checks bound to app ID 15368 | Remote-verified on 2026-09-05 | Later control-plane drift possible | authenticated protection read-back |
> | CD/promotion | Sample delivery rehearsal and rollback contracts exist | Defined, Configured rehearsal | No named live target, tag, or release | separate deployment Spec and acceptance |
>
> That checkpoint's recommendation to restore twelve retired checks is withdrawn.
> Current recovery follows the approved field-level procedure below.
> Official basis:
> [GitHub ruleset checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
>
> <div id="current-interpretation-2026-09-08"></div>
>
> ### Current interpretation (2026-09-08)
>
> The [workflow contract](../../../../.github/workflow-contract.yml) retains two
> quality jobs. The [protection policy](../../../../.github/rulesets/main-protection.md)
> names only `validation-changed` as the PR required status; `validation-full`
> provides independent push/manual evidence. The standalone tech-stack drift job
> is removed locally because the required drift leaf already covers every PR.
> This local definition change is not evidence of a hosted run.
>
> Use a fresh authenticated read-back and separately approved field-level changes
> for protection recovery. Do not restore obsolete check lists from this member.
> [Task 0006](../../../98.archive/completed/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0006-generated-evidence-and-final-verification.md)
> owns the actual current remote observations and local verification. The dated
> inventories and 2026-09-05 result above remain historical observations.
>
> <div id="maintenance"></div>
>
> ## Maintenance
>
> Re-run the focused workflow contract checker and re-derive kind, root, profile,
> job, and resolved-Action counts whenever the registry or workflow set changes.
> Reopen the mutable GitHub pages when workflow syntax, security guidance,
> environment/deployment behavior, artifacts, attestations, rulesets, or
> monitoring change. Record authenticated remote observations separately with
> target and timestamp; never promote tracked intent to applied state.

## Related Documents

- [Research pack](README.md)
- [Verification and validation](./m0019-verification-validation.md)
- [Quality, CI, and formatting](./m0014-quality-ci-formatting.md)
- [Workspace baseline](./m0020-workspace-baseline.md)
- [Scope application matrix](./m0015-scope-application-matrix.md)
- [Harness engineering](./m0008-harness-engineering.md)
- [Loop engineering](./m0010-loop-engineering.md)
- [Spec-driven SDLC](./m0018-spec-driven-sdlc.md)
- [GitHub governance](../../../../.agents/governance/github-governance.md)
- Execution Task (retired path: `../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`)
