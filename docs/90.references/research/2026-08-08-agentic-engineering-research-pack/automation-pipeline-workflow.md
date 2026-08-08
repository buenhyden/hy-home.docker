---
status: draft
artifact_id: reference:agentic-engineering-research:automation-pipeline-workflow
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-08
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

| Layer | What Task 7 can establish | What remains outside the evidence |
| --- | --- | --- |
| Tracked configuration | Exact YAML/JSON, gate registrations, roots, pins, permissions, scripts, and tests at the baseline commit. | Execution, hosted-run success, secret availability, and applied settings. |
| Local static validation | `check-github-workflow-contract.py` passed; local list mode expanded the registered profile without executing gates. | Results for the 34 listed leaves and GitHub-only behavior. |
| Declared CI | The jobs and steps GitHub would evaluate after a matching event reaches this revision. | Whether that event occurred, the effective runner state, logs, artifacts, and conclusions. |
| Remote control plane | No current authorized observation was performed. | Rulesets, required checks, branch protection, runs, environments, deployments, promotions, secrets, releases, and rollback are **UNVERIFIED**. |

The Graphify report was built from `f8a72211` and is stale. It was used only as
navigation; every fact below was re-derived from tracked owners.

### Measured typed topology

| Registry surface | Count | Derivation and interpretation |
| --- | ---: | --- |
| Workflows | 7 | `workflows` object and sorted `.github/workflows/*.yml` inventory. |
| Jobs | 23 | Job mappings across all seven workflow definitions. |
| Gate nodes | 80 | 48 `leaf`, 26 `aggregate`, 6 `setup`; kinds are not interchangeable. |
| Required-quality job roots | 16 | Each names the CI root or ordered leaves admitted for one job. |
| Local profile records | 3 | `local-script-backed`, `local-harness`, and `local-all-profiles`. |
| External Actions | 8 | Registered external repositories; no tracked `.github/actions/` directory exists. |
| Resolved Action references | 32 | YAML-anchor-aware parse; 17 literal `uses:` lines become 32 references. All 32 use full 40-character SHAs. |

`python3 scripts/validation/check-github-workflow-contract.py` returned
`PASS: GitHub workflow contract (workflows=7, jobs=23, actions=8)`. This proves
the static contract at the observed worktree only.

### Workflow and job inventory

| Workflow | Trigger | Jobs | Class and mutation boundary |
| --- | --- | ---: | --- |
| `ci-quality.yml` | Push/PR to `main`; manual dispatch | 16 | Required-quality definition. Read-only by default; `zizmor` adds `actions: read` and `security-events: write` for SARIF. |
| `document-corpus-lifecycle.yml` | Weekly schedule; manual dispatch | 1 | Non-gating read-only lifecycle checks and advisory reports. |
| `generate-changelog.yml` | `v*.*.*` tag push | 1 | Verifies a pre-existing changelog entry; it does not generate a changelog, release, or deployment. |
| `greetings.yml` | First opened issue/PR | 2 | Non-gating issue/PR comment mutation with job-scoped token permissions. |
| `pr-labeler.yml` | Opened/synchronized/reopened PR to `main` | 1 | Non-gating PR-label mutation. |
| `stale.yml` | Daily schedule | 1 | Non-gating issue/PR label and close mutation. |
| `tech-stack-version-sync.yml` | Relevant Compose/version-registry PR paths | 1 | Read-only drift check; it does not auto-commit or deploy. |

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

| Profile | Registered roots | Ordered executable expansion | Evidence boundary |
| --- | ---: | ---: | --- |
| `local-script-backed` | 18 | 34 leaves | Default local script-backed set. Task 7 used `--list`, which executed none. |
| `local-harness` | 16 | 32 leaves | Omits tech-stack drift, QuickWin, and all-profile Compose. |
| `local-all-profiles` | 19 | 35 leaves | Adds all-profile Compose validation. |
| `ci` | 16 job roots | 38 nodes: 32 leaves + 6 setup | GitHub-oriented expansion; includes dependency setup and GitHub-only leaves. |

`run-local-qa-gates.sh` is a 63-line dispatcher into the typed runner. It does
not contain a second hand-maintained command list. Its help text excludes SARIF
upload, protected-branch enforcement, hosted required-check status, and the
separately controlled Agent all-files pre-commit route.

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

| Scope | Automation implication |
| --- | --- |
| `agentic` | Use typed roots and sanitized Task evidence; provider hooks and local orchestration do not prove hosted CI or remote enforcement. |
| `architecture` | Any CD, promotion, artifact, or rollback design starts with explicit targets, trust boundaries, failure modes, and an approved architecture contract. |
| `backend` | No current backend delivery surface is established; future service pipelines require a backend Spec, tests, artifacts, environment, and rollback owner. |
| `common` | Shared diff, syntax, metadata, and review gates apply, but one shared profile must not erase surface-specific checks. |
| `docs` | Document changes use metadata, traceability, implementation-alignment, and repository-contract owners; Stage 90 analysis does not make a check remote-required. |
| `entry` | Gateway changes require configuration, security, and recovery gates tied to the tracked entry surface; no deployment route is currently evidenced. |
| `frontend` | Frontend quality and Storybook coverage are CI roots; their build output is not a promoted or attested release artifact. |
| `infra` | Compose and hardening gates validate tracked configuration only; live apply, promotion, environment secrets, and rollback remain separately authorized operations. |
| `meta` | The schema, DAG, profile, root, environment-key, action, and validator contracts are the automation metadata owners; counts must be re-derived from them. |
| `mobile` | No mobile source or delivery workflow is established, so mobile automation and promotion are not applicable until an approved surface exists. |
| `ops` | Operations owns future deployment verification, observability, rollback, recovery, and release evidence; current workflows provide no production event proof. |
| `product` | Product intent defines release value and acceptance; a green build or tag-string check is not evidence of user delivery. |
| `qa` | QA maps changed surfaces to ordered local and CI gates and records skips; current remote check conclusions remain unverified. |
| `security` | Enforce least privilege, SHA pins, secret-safe output, dependency/workflow scanning, and explicit promotion approvals without treating scanner success as complete security. |

## Sources

| Source | Accessed | Class | Verification state |
| --- | --- | --- | --- |
| [GitHub Actions workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions) | 2026-08-08T17:45:01+09:00 | External mutable | Verified official page; prescribed route redirected to current workflow-syntax reference; trigger, permission, job, environment, timeout, and step semantics used. |
| [GitHub secure use reference](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) | 2026-08-08T17:45:01+09:00 | External mutable | Verified official page; prescribed route redirected to current secure-use reference; least privilege and full-SHA pinning used. |
| [Using `GITHUB_TOKEN`](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication) | 2026-08-08T17:45:01+09:00 | External mutable | Verified official page; prescribed route redirected to current tutorial; job/workflow permission minimization used. |
| [Managing deployment environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments) | 2026-08-08T17:45:01+09:00 | External mutable | Verified direct official page; protection, reviewer, branch/tag, and secret timing capability only; local adoption not inferred. |
| [Viewing deployment history](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/view-deployment-history) | 2026-08-08T17:45:01+09:00 | External mutable | Verified direct official page; history/commit/log/status capability only; no repository observation. |
| [Workflow artifacts](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-what-your-workflow-does/storing-and-sharing-data-from-a-workflow) | 2026-08-08T17:45:01+09:00 | External mutable | Verified official page; route redirected to current tutorial; upload/download/retention/digest capability only. |
| [Artifact attestations](https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations) | 2026-08-08T17:45:01+09:00 | External mutable | Verified official page; prescribed route redirected to current how-to; provenance capability only. |
| [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) | 2026-08-08T17:45:01+09:00 | External mutable | Verified direct official page; active/disabled enforcement and layering capability do not prove this repository's settings. |
| [Monitoring workflows](https://docs.github.com/en/actions/how-tos/monitor-workflows) | 2026-08-08T17:45:01+09:00 | External mutable | Verified direct official page; graph, status, timing, and log capability only; no Task 7 run observed. |
| [Typed workflow registry](../../../../.github/workflow-contract.yml) | 2026-08-08 | Workspace tracked | Complete registry parsed at `c57d33f`; exact topology, roots, profiles, action pins, and environment-key bounds. |
| [Tracked workflows](../../../../.github/workflows/ci-quality.yml) | 2026-08-08 | Workspace tracked | All seven files read; 23 jobs, triggers, permissions, concurrency, steps, and absence claims re-derived. |
| [Workflow contract checker](../../../../scripts/validation/check-github-workflow-contract.py) | 2026-08-08 | Workspace tracked/local execution | Static check PASS; no hosted run or control-plane proof. |
| [Local QA dispatcher](../../../../scripts/validation/run-local-qa-gates.sh) | 2026-08-08 | Workspace tracked/local list execution | `--list` printed 34 ordered leaves and executed none. |
| [Desired main protection proposal](../../../../.github/rulesets/main-protection.md) | 2026-08-08 | Workspace tracked proposal | Sixteen desired check names; explicitly not applied-state evidence. |
| [Public control-plane snapshot](../../data/governance/github-actions-control-plane-observation.yaml) | 2026-08-08 | Historical retained observation | Dated 2026-07-26; current rules, failure cause, and remote enforcement remain `UNVERIFIED`. |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md) | 2026-08-08 | Workspace tracked stale/advisory | Built from `f8a72211`; corroborated and not used as current proof. |

## Maintenance

Re-run the focused workflow contract checker and re-derive kind, root, profile,
job, and resolved-Action counts whenever the registry or workflow set changes.
Reopen the mutable GitHub pages when workflow syntax, security guidance,
environment/deployment behavior, artifacts, attestations, rulesets, or
monitoring change. Record authenticated remote observations separately with
target and timestamp; never promote tracked intent to applied state.

## Related Documents

- [Quality, CI, and formatting](./quality-ci-formatting.md)
- [Workspace baseline](./workspace-baseline.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Harness engineering](./harness-engineering.md)
- [Loop engineering](./loop-engineering.md)
- [Spec-driven SDLC](./spec-driven-sdlc.md)
- [GitHub governance](../../../00.agent-governance/rules/github-governance.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
