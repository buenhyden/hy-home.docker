---
status: draft
artifact_id: reference:agentic-engineering-research:automation-pipeline-workflow
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-14
review_cycle: on-source-change
---

# Reference: Automation Pipeline and Workflow Topology

## Overview

At Task 7 baseline `c57d33f37843802f7692261c50801f0dd966d7cb`,
the tracked GitHub automation surface contains 7 workflow files and 23 jobs.
The typed registry in `.github/workflow-contract.yml` contains 80 gate nodes:
48 leaves, 26 aggregates, and 6 setup nodes. Sixteen required-quality jobs
have registered roots, three local profiles have registered root lists, and
eight distinct external Actions are registered at full commit SHAs.

Those figures describe tracked configuration. They do not prove a workflow
ran, a required check is remotely enforced, an environment exists, a secret is
configured, or a deployment succeeded. Task 7 performed no authenticated
control-plane readback and no workflow dispatch, so all current remote state is
`UNVERIFIED`.

Re-verified independently at `ece3eda9c3e1a603c6495dd55caba7df1c29ef6c` on
2026-08-14: the workflow count, job count, gate-node kind counts (48/26/6),
job-root count, and profile-root counts (18/16/19) are unchanged from the Task
7 baseline, and `check-github-workflow-contract.py` still returns
`PASS: GitHub workflow contract (workflows=7, jobs=23, actions=8)`. A fresh
`grep` across all seven tracked workflow files found zero occurrences of
`continue-on-error`, `needs:`, `matrix:`, or `workflow_call`, and zero
non-SHA (`@main`/`@master`/floating-tag) `uses:` references. That absence is
itself load-bearing evidence, not a gap by omission — see "Reusable
workflows, OIDC, and `continue-on-error`" below.

## Purpose

Support REQ-24 and REQ-25 by documenting the exact automation topology,
ordered gate expansion, permissions, action pinning, failure behavior, and
delivery boundary without reducing a multi-leaf job to a false one-job/
one-command rule or presenting continuous integration as continuous delivery.

## Repository Role

This Stage 90 reference is advisory analysis. The tracked workflow registry,
workflow YAML, scripts, Stage 00 governance, and any separately authorized
remote GitHub readback remain the evidence owners. This document neither
changes those owners nor authorizes dispatch, push, promotion, deployment,
ruleset, environment, secret, release, or rollback actions.

## Scope

### In scope

- The seven tracked workflows, twenty-three jobs, typed gate DAG, registered
  profiles, and external Action inventory.
- Trigger, permission, pinning, concurrency, timeout, ordering, failure, retry,
  observability, and remote-enforcement boundaries.
- The distinction among local configuration, local execution, declared CI,
  and observed remote state.
- CI/CD, promotion, deployment, artifact, attestation, and rollback gaps.
- Adoption rules, evidence limitations, owners, and all fourteen scopes.

### Out of scope

- Running a local QA profile beyond list mode or dispatching any workflow.
- Authenticated inspection or mutation of rulesets, branch protection, runs,
  environments, deployments, releases, secrets, variables, or artifacts.
- Changing workflows, actions, scripts, contracts, provider surfaces, or
  generated outputs.
- Treating the stale Graphify report or the 2026-07-26 public snapshot as
  current control-plane truth.

## Definitions / Facts

### Evidence layers

| Layer                   | What Task 7 can establish                                                                                            | What remains outside the evidence                                                                                                              |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Tracked configuration   | Exact YAML/JSON, gate registrations, roots, pins, permissions, scripts, and tests at the baseline commit.            | Execution, hosted-run success, secret availability, and applied settings.                                                                      |
| Local static validation | `check-github-workflow-contract.py` passed; local list mode expanded the registered profile without executing gates. | Results for the 34 listed leaves and GitHub-only behavior.                                                                                     |
| Declared CI             | The jobs and steps GitHub would evaluate after a matching event reaches this revision.                               | Whether that event occurred, the effective runner state, logs, artifacts, and conclusions.                                                     |
| Remote control plane    | No current authorized observation was performed.                                                                     | Rulesets, required checks, branch protection, runs, environments, deployments, promotions, secrets, releases, and rollback are **UNVERIFIED**. |

The Graphify report was built from `f8a72211` and is stale. It was used only as
navigation; every fact below was re-derived from tracked owners.

### Measured typed topology

| Registry surface           | Count | Derivation and interpretation                                                                              |
| -------------------------- | ----: | ---------------------------------------------------------------------------------------------------------- |
| Workflows                  |     7 | `workflows` object and sorted `.github/workflows/*.yml` inventory.                                         |
| Jobs                       |    23 | Job mappings across all seven workflow definitions.                                                        |
| Gate nodes                 |    80 | 48 `leaf`, 26 `aggregate`, 6 `setup`; kinds are not interchangeable.                                       |
| Required-quality job roots |    16 | Each names the CI root or ordered leaves admitted for one job.                                             |
| Local profile records      |     3 | `local-script-backed`, `local-harness`, and `local-all-profiles`.                                          |
| External Actions           |     8 | Registered external repositories; no tracked `.github/actions/` directory exists.                          |
| Resolved Action references |    32 | YAML-anchor-aware parse; 17 literal `uses:` lines become 32 references. All 32 use full 40-character SHAs. |

`python3 scripts/validation/check-github-workflow-contract.py` returned
`PASS: GitHub workflow contract (workflows=7, jobs=23, actions=8)`. This proves
the static contract at the observed worktree only.

### Gate node schema

Each of the 80 `gate_nodes` records is a typed object, not a bare string.
Parsing the registry directly (`yaml.safe_load` over
`.github/workflow-contract.yml`) shows the exact shape:

```json
{
  "gate_id": "ci.agent-output-eval-fixture-gate",
  "kind": "aggregate",
  "profiles": ["ci", "local-script-backed", "local-harness", "local-all-profiles"],
  "opaque": false,
  "children": ["leaf.agent-output-eval-fixture-regressions", "leaf.agent-output-eval-fixture-gate"]
}
```

`kind` is one of `leaf` (48, an actual command/check), `aggregate` (26, a
named group whose ordered `children` expand to leaves/setup nodes), or
`setup` (6, dependency/environment preparation that precedes leaves but is
not itself a check). `profiles` lists which of the four profiles
(`ci`, `local-script-backed`, `local-harness`, `local-all-profiles`) may
select that node; a node absent from `ci` cannot appear in the hosted
expansion no matter how the workflow YAML is edited, because the focused
checker verifies the expansion against this registry, not against workflow
prose. `job_roots` is a separate 16-entry list, each record binding one
`workflow` path, one `job_id`, one `root_gate_id`, and a `classification`
(all 16 are `required-quality`); its `job_id` sequence is
`docs-traceability, docs-implementation-alignment, repo-contracts,
agent-output-eval-fixture-gate, supply-chain-fixture-policy,
dependency-vulnerability-audit, git-flow-contract, compose-validation,
compose-all-profiles-validation, infrastructure-hardening,
template-security-baseline, quickwin-baseline, pre-commit, frontend-quality,
storybook-coverage, zizmor`. `profile_roots` is a third list keyed by
`profile` with a `root_gate_ids` array (18/16/19 entries respectively).
These three lists are structurally independent; the checker's job is to
prove each expands into the ordered executable set claimed above without
duplicating or omitting a leaf.

### Workflow and job inventory

| Workflow                        | Trigger                                    | Jobs | Class and mutation boundary                                                                                              |
| ------------------------------- | ------------------------------------------ | ---: | ------------------------------------------------------------------------------------------------------------------------ |
| `ci-quality.yml`                | Push/PR to `main`; manual dispatch         |   16 | Required-quality definition. Read-only by default; `zizmor` adds `actions: read` and `security-events: write` for SARIF. |
| `document-corpus-lifecycle.yml` | Weekly schedule; manual dispatch           |    1 | Non-gating read-only lifecycle checks and advisory reports.                                                              |
| `generate-changelog.yml`        | `v*.*.*` tag push                          |    1 | Verifies a pre-existing changelog entry; it does not generate a changelog, release, or deployment.                       |
| `greetings.yml`                 | First opened issue/PR                      |    2 | Non-gating issue/PR comment mutation with job-scoped token permissions.                                                  |
| `pr-labeler.yml`                | Opened/synchronized/reopened PR to `main`  |    1 | Non-gating PR-label mutation.                                                                                            |
| `stale.yml`                     | Daily schedule                             |    1 | Non-gating issue/PR label and close mutation.                                                                            |
| `tech-stack-version-sync.yml`   | Relevant Compose/version-registry PR paths |    1 | Read-only drift check; it does not auto-commit or deploy.                                                                |

All seven workflows explicitly declare top-level permissions. Four declare
concurrency groups with `cancel-in-progress: true`; cancellation replaces an
obsolete in-flight run, not a retry policy. Every registered job has a timeout
of 5, 10, 15, or 20 minutes.

### Ordered expansion is the executable contract

The 16 required-quality jobs are roots into a DAG, not sixteen shell commands.
The direct runner lists 38 CI executable nodes after ordered expansion: 32
leaves and 6 setup nodes. For example:

- `ci.repo-contracts` expands to metadata-base verification, Python dependency
  setup, changed-document metadata, five Python regression leaves, one shell
  regression leaf, workflow-contract validation, and repository contracts.
- `ci.frontend-quality` expands to Node dependency setup, lint, typecheck,
  Next.js build, and Storybook build.
- `ci.storybook-coverage` expands to Node dependency setup, Playwright browser
  setup, and the coverage leaf.
- `docs-implementation-alignment` deliberately invokes
  `leaf.docs-implementation-alignment` and then
  `leaf.docs-qa-gate-recommendations`; the second uses `if: always()` so the
  advisory summary is attempted even when alignment fails.

The last case is why “one job, one command” is false. The typed root owns two
ordered leaves, and the workflow spells them as two static invocations to
preserve the `always()` behavior. The focused contract checker validates the
ordered projection rather than requiring one textual `run:` step.

No tracked job declares `needs:`, a matrix, or a deployment environment. CI
therefore fans out across independent jobs; ordering exists inside each job's
root expansion, not as a repository-wide staged pipeline.

### Local profiles

| Profile               | Registered roots |  Ordered executable expansion | Evidence boundary                                                            |
| --------------------- | ---------------: | ----------------------------: | ---------------------------------------------------------------------------- |
| `local-script-backed` |               18 |                     34 leaves | Default local script-backed set. Task 7 used `--list`, which executed none.  |
| `local-harness`       |               16 |                     32 leaves | Omits tech-stack drift, QuickWin, and all-profile Compose.                   |
| `local-all-profiles`  |               19 |                     35 leaves | Adds all-profile Compose validation.                                         |
| `ci`                  |     16 job roots | 38 nodes: 32 leaves + 6 setup | GitHub-oriented expansion; includes dependency setup and GitHub-only leaves. |

`run-local-qa-gates.sh` is a 63-line dispatcher into the typed runner. It does
not contain a second hand-maintained command list. Its help text excludes SARIF
upload, protected-branch enforcement, hosted required-check status, and the
separately controlled Agent all-files pre-commit route.

### Promotion path: local check to required remote check

Adding, changing, or retiring a required-quality job is a coupled three-surface
change, not a single-file edit. `docs/00.agent-governance/rules/
github-governance.md` §8 states the constraint explicitly: `.github/
workflow-contract.yml` (typed root/registration), `.github/workflows/
ci-quality.yml` (the actual `run:` step invoking `run-ci-gate.py --profile ci
--gate <id>`), and `.github/rulesets/main-protection.md` (the desired-state
Required Status Checks list) must change together, followed by an update to
the explanatory table in that same governance file.

Re-deriving both sides today confirms the desired state is currently
consistent: the 16 `job_id` values in `workflow-contract.yml`'s `job_roots`
and the 16 check names listed under "Required Status Checks" in
`main-protection.md` are the same 16 strings in the same order
(`docs-traceability` through `zizmor`). That structural match is
`Workspace tracked` evidence that the _desired_ remote contract is internally
coherent — it is not evidence that GitHub enforces it. `main-protection.md`
says so directly: "Until that separately approved readback succeeds, all 16
checks above remain tracked desired state rather than evidence of remote
enforcement," and names the exact commands
(`gh api repos/<org>/<repo>/rulesets --paginate`,
`gh api repos/<org>/<repo>/branches/main/protection`) that would close the
gap. Neither command was run by this leaf.

The full promotion path a change must complete before a local check becomes a
remote-required check is therefore:

1. **Local static validation** — the gate exists in `workflow-contract.yml`
   and passes `check-github-workflow-contract.py`.
2. **Declared CI** — the same gate ID is invoked from a `run:` step inside a
   job in `ci-quality.yml`, and the ordered expansion matches the registry.
3. **Desired remote contract** — the job's name is added to
   `main-protection.md`'s Required Status Checks list (`Workspace tracked`
   proposal only).
4. **Applied remote ruleset** — a repository owner applies the ruleset or
   branch-protection rule through the GitHub UI or an audited `gh api` call,
   per `main-protection.md`'s "Application Boundary" — this step is outside
   any tracked file and requires separate human/authorized-agent action.
5. **Verified remote enforcement** — an authenticated readback (the two `gh
api` commands above, or equivalent) confirms the rule is live and lists
   which checks it actually requires.

Steps 1-3 are what this repository's tracked files can establish today. Steps
4-5 are `UNVERIFIED` for every one of the 16 gates; no Task in this pack has
performed an authenticated ruleset or branch-protection readback. A job
appearing in `main-protection.md` is therefore necessary but not sufficient
evidence that GitHub will actually block a merge without it.

### Reusable workflows, OIDC, and `continue-on-error`: absent, not merely unverified

Three GitHub Actions capabilities relevant to pipeline maturity are entirely
unused in this repository today, confirmed by direct grep over all seven
workflow files at `ece3eda9` on 2026-08-14:

- **Reusable workflows** (`workflow_call` triggers and cross-file `uses:
./.github/workflows/<file>.yml` or `owner/repo/.github/workflows/
<file>.yml@<ref>` job-level calls) let one workflow definition be shared
  across callers, with inputs/secrets passed explicitly or via `secrets:
inherit`, and with permissions only reducible (never elevatable) through a
  call chain up to 10 levels deep. Zero occurrences of `workflow_call` exist
  here; each of the seven workflows is self-contained. There is currently
  nothing to reuse across repositories or across the seven local workflows
  that would justify one, since none share job bodies beyond the checkout
  step already factored into a YAML anchor (`&checkout` in `ci-quality.yml`).
- **OIDC** (`permissions: id-token: write` plus a cloud-side trust policy
  keyed on the token's `sub`/`repo`/`ref`/`environment`/`actor` claims) lets a
  workflow exchange a short-lived, auto-rotated token for cloud credentials
  instead of storing a long-lived secret. Zero occurrences of `id-token` or
  any `id-token: write` permission exist here. This is consistent with the
  independently confirmed fact that no non-GitHub credential or deployment
  secret is declared in any of the seven workflows: there is no cloud target
  to authenticate to yet, so OIDC is not a current gap, only a prerequisite
  the moment a cloud deployment job is proposed.
- **`continue-on-error`** lets a step or job fail without failing the
  workflow (`steps.[id].outcome` still records `failure`, but
  `steps.[id].conclusion` and the job/workflow conclusion report success).
  Zero occurrences exist here, corroborating the leaf's existing "Failure
  propagation" finding: every registered gate is a hard, non-soft-failing
  check, with no experimental or best-effort job silently masking a red
  result as green.

None of these three absences is itself a defect; they are the correct
baseline for a repository with no current cloud-deployment or cross-repository
workflow-sharing surface. They become adoption prerequisites, not optional
polish, the moment a future Spec proposes a deployment job: that job would
need OIDC (not a stored cloud secret) under GitHub's current secure-use
guidance, and any shared step logic extracted for a second workflow or
repository would need `workflow_call` rather than copy-paste duplication.

### Action, permission, and secret boundaries

The registry records eight external Actions with pinned manifest URLs,
`runtime: node24`, retrieval date `2026-07-28`, consumers, and an approved
tracked disposition. All 32 resolved uses are full-SHA pins, consistent with
GitHub's current secure-use guidance. The registry and checker cannot prove
that a remote Action remained uncompromised after review.

`ci-quality.yml` defaults to `contents: read`; only `zizmor` elevates the
permissions needed for SARIF. Greetings and labeling use `GITHUB_TOKEN` with
job-scoped write grants. No non-GitHub credential or deployment secret is
declared in the seven workflow files. Whether any repository/environment
secret exists remotely is `UNVERIFIED` and was not queried.

### Failure propagation, retry, and observation

- The typed runner executes the unique ordered expansion and returns on the
  first non-zero child. The local wrapper uses `set -euo pipefail`.
- No workflow or registered gate declares retry, backoff, attempt count, or
  `continue-on-error`. A human or authorized GitHub actor must correct the
  owner and rerun; that operational rerun is not encoded as an automatic loop.
- The alignment job's `if: always()` recommendation step does not neutralize
  the preceding failure. It preserves bounded diagnostic output.
- GitHub documents run graphs, job/step status, timings, and downloadable logs
  as monitoring surfaces. No current Task 7 run or log was observed.
- The tracked public snapshot dated 2026-07-26 records a failed remote run but
  explicitly marks its root cause and control-plane verification unverified;
  it cannot establish current state.

### CI is implemented; CD is not established

No tracked workflow declares `environment:`, deployment jobs, artifact upload
for a releasable build, artifact attestations, promotion stages, or rollback
commands. The SARIF upload is security-analysis output, not a deployable
release artifact. The tag workflow verifies changelog coverage only.

GitHub environments can gate environment secrets and jobs behind reviewer,
branch/tag, wait-timer, and custom protection rules; deployment history can
link environments, commits, workflow logs, URLs, and statuses. Artifact
attestations can establish build provenance. None of those upstream
capabilities is tracked as adopted delivery behavior here, and current remote
environment/deployment state is `UNVERIFIED`.

### Adoption rules, gaps, and follow-up route

1. Extend the typed registry, workflow YAML, desired required-check proposal,
   and explanatory governance together for any required-job change.
2. Keep every external Action full-SHA pinned, registered, manifest-reviewed,
   runtime-classified, and permission-minimal.
3. Preserve ordered expansion and failure semantics; never infer one command
   from one job or collapse setup/leaf distinctions.
4. Record local static validation, local execution, declared CI, observed run,
   and applied remote enforcement as separate evidence.
5. A future delivery design must name artifact identity, provenance, target
   environments, promotion approvals, deployment verification, rollback
   trigger/action/evidence, observability, secret boundary, and recovery owner
   in Stage 03/04 before workflow adoption.
6. Remote readback or mutation requires separate user approval for the named
   repository and surface. This reference supplies no such authority.

## Scope Implications

| Scope          | Automation implication                                                                                                                                                       |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | Use typed roots and sanitized Task evidence; provider hooks and local orchestration do not prove hosted CI or remote enforcement.                                            |
| `architecture` | Any CD, promotion, artifact, or rollback design starts with explicit targets, trust boundaries, failure modes, and an approved architecture contract.                        |
| `backend`      | No current backend delivery surface is established; future service pipelines require a backend Spec, tests, artifacts, environment, and rollback owner.                      |
| `common`       | Shared diff, syntax, metadata, and review gates apply, but one shared profile must not erase surface-specific checks.                                                        |
| `docs`         | Document changes use metadata, traceability, implementation-alignment, and repository-contract owners; Stage 90 analysis does not make a check remote-required.              |
| `entry`        | Gateway changes require configuration, security, and recovery gates tied to the tracked entry surface; no deployment route is currently evidenced.                           |
| `frontend`     | Frontend quality and Storybook coverage are CI roots; their build output is not a promoted or attested release artifact.                                                     |
| `infra`        | Compose and hardening gates validate tracked configuration only; live apply, promotion, environment secrets, and rollback remain separately authorized operations.           |
| `meta`         | The schema, DAG, profile, root, environment-key, action, and validator contracts are the automation metadata owners; counts must be re-derived from them.                    |
| `mobile`       | No mobile source or delivery workflow is established, so mobile automation and promotion are not applicable until an approved surface exists.                                |
| `ops`          | Operations owns future deployment verification, observability, rollback, recovery, and release evidence; current workflows provide no production event proof.                |
| `product`      | Product intent defines release value and acceptance; a green build or tag-string check is not evidence of user delivery.                                                     |
| `qa`           | QA maps changed surfaces to ordered local and CI gates and records skips; current remote check conclusions remain unverified.                                                |
| `security`     | Enforce least privilege, SHA pins, secret-safe output, dependency/workflow scanning, and explicit promotion approvals without treating scanner success as complete security. |

## Sources

| Source                                                                                                                                                       | Accessed                           | Class                                  | Verification state                                                                                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [GitHub Actions workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions)                                    | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified official page; prescribed route redirected to current workflow-syntax reference; trigger, permission, job, environment, timeout, and step semantics used.                                                                          |
| [GitHub secure use reference](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)          | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified official page; prescribed route redirected to current secure-use reference; least privilege and full-SHA pinning used.                                                                                                             |
| [Using `GITHUB_TOKEN`](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication)                        | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified official page; prescribed route redirected to current tutorial; job/workflow permission minimization used.                                                                                                                         |
| [Managing deployment environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)                   | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified direct official page; protection, reviewer, branch/tag, and secret timing capability only; local adoption not inferred.                                                                                                            |
| [Viewing deployment history](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/view-deployment-history)                     | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified direct official page; history/commit/log/status capability only; no repository observation.                                                                                                                                        |
| [Workflow artifacts](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-what-your-workflow-does/storing-and-sharing-data-from-a-workflow) | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified official page; route redirected to current tutorial; upload/download/retention/digest capability only.                                                                                                                             |
| [Artifact attestations](https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations)                                          | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified official page; prescribed route redirected to current how-to; provenance capability only.                                                                                                                                          |
| [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)               | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified direct official page; active/disabled enforcement and layering capability do not prove this repository's settings.                                                                                                                 |
| [Monitoring workflows](https://docs.github.com/en/actions/how-tos/monitor-workflows)                                                                         | 2026-08-08T17:45:01+09:00          | External mutable                       | Verified direct official page; graph, status, timing, and log capability only; no Task 7 run observed.                                                                                                                                      |
| [Reusing workflows](https://docs.github.com/en/actions/sharing-automations/reusing-workflows)                                                                | 2026-08-14                         | External mutable                       | Verified official page; `workflow_call`, `uses:` at job level, SHA-pin recommendation, 10-level nesting, and permission-reduction-only-through-chain semantics used; this repository uses none of it.                                       |
| [OpenID Connect reference](https://docs.github.com/en/actions/reference/security/oidc)                                                                       | 2026-08-14                         | External mutable                       | Verified official page; `permissions: id-token: write`, `sub`/`repo`/`ref`/`environment`/`actor` claims, and subject-condition guidance used; this repository declares no `id-token` permission.                                            |
| `continue-on-error` step/job semantics                                                                                                                       | 2026-08-14                         | External mutable                       | GitHub workflow-syntax documentation corroborated by secondary technical sources; step-level masks `conclusion` to success while `outcome` still records failure, job-level masks the workflow conclusion; this repository uses it nowhere. |
| [Typed workflow registry](../../../../.github/workflow-contract.yml)                                                                                         | 2026-08-08; re-verified 2026-08-14 | Workspace tracked                      | Complete registry re-parsed with `yaml.safe_load` at `ece3eda9`: 80 `gate_nodes` (48 leaf/26 aggregate/6 setup), 16 `job_roots`, 3 `profile_roots` (18/16/19), 8 `actions`, all unchanged from the `c57d33f` baseline.                      |
| [Tracked workflows](../../../../.github/workflows/ci-quality.yml)                                                                                            | 2026-08-08; re-verified 2026-08-14 | Workspace tracked                      | All seven files re-read at `ece3eda9`; 23 jobs, triggers, permissions, concurrency, steps confirmed; grep confirmed zero `continue-on-error`/`needs:`/`matrix:`/`workflow_call` occurrences.                                                |
| [Workflow contract checker](../../../../scripts/validation/check-github-workflow-contract.py)                                                                | 2026-08-08; re-run 2026-08-14      | Workspace tracked/local execution      | Static check PASS re-run directly at `ece3eda9`; no hosted run or control-plane proof.                                                                                                                                                      |
| [Local QA dispatcher](../../../../scripts/validation/run-local-qa-gates.sh)                                                                                  | 2026-08-08                         | Workspace tracked/local list execution | `--list` printed 34 ordered leaves and executed none.                                                                                                                                                                                       |
| [Desired main protection proposal](../../../../.github/rulesets/main-protection.md)                                                                          | 2026-08-08; re-verified 2026-08-14 | Workspace tracked proposal             | Sixteen desired check names re-read; confirmed byte-for-byte identical set and order to `job_roots`' 16 `job_id` values; explicitly not applied-state evidence.                                                                             |
| [GitHub governance policy](../../../00.agent-governance/rules/github-governance.md)                                                                          | 2026-08-14                         | Workspace tracked policy               | §8 "CI/CD Job Taxonomy" read in full; three-surface coupling constraint, `pre-commit` job's exact pinned-dependency install path, and non-gating workflow table used.                                                                       |
| [Public control-plane snapshot](../../data/governance/ref-0071-github-actions-control-plane-observation.yaml)                                                         | 2026-08-08                         | Historical retained observation        | Dated 2026-07-26; current rules, failure cause, and remote enforcement remain `UNVERIFIED`.                                                                                                                                                 |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)                                                                                                  | 2026-08-08                         | Workspace tracked stale/advisory       | Built from `f8a72211`; corroborated and not used as current proof.                                                                                                                                                                          |

## Maintenance

Re-run the focused workflow contract checker and re-derive kind, root, profile,
job, and resolved-Action counts whenever the registry or workflow set changes.
Reopen the mutable GitHub pages when workflow syntax, security guidance,
environment/deployment behavior, artifacts, attestations, rulesets, or
monitoring change. Record authenticated remote observations separately with
target and timestamp; never promote tracked intent to applied state.

## Related Documents

- [Verification and validation](./verification-validation.md)
- [Quality, CI, and formatting](./quality-ci-formatting.md)
- [Workspace baseline](./workspace-baseline.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Harness engineering](./harness-engineering.md)
- [Loop engineering](./loop-engineering.md)
- [Spec-driven SDLC](./spec-driven-sdlc.md)
- [GitHub governance](../../../00.agent-governance/rules/github-governance.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
