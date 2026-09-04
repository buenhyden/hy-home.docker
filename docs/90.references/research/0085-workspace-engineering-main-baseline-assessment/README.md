---
title: "Workspace Engineering Main Baseline Assessment"
version: "0.1.0"
type: "reference/research-pack"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-04"
layer: "references"
artifact_id: "RES-0085"
parent_ids: []
created: "2026-09-04"
observed_at: "2026-09-04"
---

# Workspace Engineering Main Baseline Assessment

## Question

What does `buenhyden/hy-home.docker` actually provide on `main` for workspace
engineering, agent governance, spec-driven delivery, infrastructure, CI/CD,
quality, security, documentation, provider integration, context handling, and
runtime operation, and which claims still require direct external evidence?

## Scope

- Repository baseline: `main` at merge commit
  `db21aebf079fcc4e867779861b49c2283b7f8f01`.
- Integration boundary: feature branch and pull request; direct writes to
  `main` are prohibited by the [PR #138 binding request](https://github.com/buenhyden/hy-home.docker/pull/138).
- Repository evidence: tracked policies, contracts, workflows, validators,
  generated provider surfaces, architecture, operations, and README indexes.
- External observations: GitHub repository metadata, PR #138 checks, current
  `main` branch protection, Codex account availability, and local Docker daemon
  metadata observed on 2026-09-04.
- Candidate changes in the SPEC-0172 worktree are evaluated separately from
  the committed `main` baseline and are not presented as merged behavior.

## Method

1. Bound repository claims to the committed `main` tree and record the exact
   baseline commit.
2. Inspect canonical Stage 00 policy, Stage 99 contracts, workflow contracts,
   validators, and current Requirement/Architecture/Spec/Operations owners.
3. Query GitHub through authenticated read-only repository, pull-request,
   Actions, and branch-protection endpoints without reading credential values.
4. Observe Docker engine, Compose project inventory, and container identity
   metadata without reading environment values, logs, secrets, or mutating the
   runtime.
5. Separate tracked adoption, hosted acceptance, provider entitlement, local
   runtime observation, and deployment acceptance. Missing direct evidence is
   recorded as `needs_revalidation`, not inferred as a pass.

## Findings

| Area | Main-baseline evidence | Observed disposition |
| --- | --- | --- |
| Binding and integration | PR #138 added the request scope and was merged as `db21aebf`; the scope requires a feature branch and PR | adopted; direct `main` write prohibited |
| Agent and harness governance | Root adapters route to Stage 00; the committed tree contains 14 canonical roles, 23 canonical skills, provider projections, hooks, and typed provider mappings | tracked adoption; provider runtime acceptance remains separately observed |
| Loop and stop control | Stage 00 workflows define discovery, approval, execution, review, bounded retry, stop, and Task-owned handoff evidence | adopted policy; effectiveness depends on the active provider runtime |
| Spec-driven development | Requirement, Architecture Description, ADR, Spec, Plan, Task, lifecycle, traceability, and archive contracts have executable validators | adopted; candidate semantic convergence is not yet merged |
| Documentation contract | `main` contains `RES-0085/REQUEST-SCOPE.md` without the required package `README.md`; PR #138 `validation-changed` failed on that incomplete package | blocked on `main`; this package supplies the missing canonical envelope on the feature branch |
| CI/CD and QA | Six tracked workflow files and a typed workflow contract exist; PR #138 CodeQL checks passed but `validation-changed` failed and `validation-full` was skipped | hosted CI observed; current branch cannot claim a green quality gate |
| Branch protection | `main` requires strict status checks, one approving review, code-owner review, conversation resolution, and disallows force-push and deletion | observed enabled; configured required contexts must be rechecked against the current workflow job names |
| Security | SHA-pinning, workflow, template, supply-chain, secret-pattern, CodeQL, and governance checks have tracked owners and validators | tracked adoption; no secret value or live security-control mutation was inspected |
| Compose and infrastructure | Compose validation and operations contracts are tracked; Docker Engine 29.7.2 and Compose v5.4.0 were reachable locally | runtime reachable; zero active Compose projects observed |
| Live runtime and deployment | Five `k3d-hyhome` containers were running, but they are not evidence that this repository's Compose stack was deployed or accepted | observed unrelated runtime; repository deployment acceptance remains unverified |
| Provider models | Registry marks Claude and Codex as adopted but `needs_revalidation`; this Codex task had direct account access while no Claude runtime call was made | Codex entitlement observed for this task; Claude entitlement and cross-provider acceptance remain `needs_revalidation` |
| Context, memory, and handoff | Provider hooks include `PreCompact`; Task records own progress and handoff; no separate durable memory authority is defined | bounded context handling adopted; no claim of cross-session semantic memory |
| Cost control | Work profiles select model classes and reasoning effort, while the evaluation contract forbids inferring cost or latency without direct evidence | policy-level control only; cost effectiveness unverified |
| Editor integration | No tracked `.vscode`, `.idea`, or `.devcontainer` authority exists at the baseline commit | not adopted as a repository contract |
| README navigation | Stage and category README files route to canonical owners; generated LLM Wiki outputs provide navigation rather than policy | adopted, subject to freshness and link gates |

## Sources

- [Agent bootstrap policy](../../../00.agent-governance/policies/bootstrap.md)
- [Agentic engineering policy](../../../00.agent-governance/policies/agentic.md)
- [Approval boundaries](../../../00.agent-governance/policies/approval-boundaries.md)
- [Provider registry](../../../00.agent-governance/providers/registry.yaml)
- [Document Registry](../../../99.templates/registry.json)
- [CI Quality Gates workflow](../../../../.github/workflows/ci-quality.yml)
- [Workflow contract](../../../../.github/workflow-contract.yml)
- [Infrastructure index](../../../../infra/README.md)
- [Operations index](../../../05.operations/README.md)
- [SPEC-0172](../../../03.specs/0172-document-contract-convergence/spec.md)
- [SPEC-0172 execution evidence](../../../03.specs/0172-document-contract-convergence/tasks/tsk-0001-document-contract-convergence.md)
- [PR #138](https://github.com/buenhyden/hy-home.docker/pull/138)
- [PR #138 CI run](https://github.com/buenhyden/hy-home.docker/actions/runs/33842556330)

## Implications

- Completing this package removes the known reference-corpus configuration
  blocker but does not by itself make the candidate change mergeable; local and
  hosted gates must be rerun against the feature branch.
- The required status-check names on `main` are not the same names exposed by
  the current `CI Quality Gates` jobs. Protection should be changed only after
  the current workflow contract identifies the exact replacement contexts and
  a recovery path is recorded.
- A reachable Docker daemon and running k3d cluster do not authorize or prove a
  Compose deployment. A deployment needs an explicit target, change set,
  observation plan, and rollback.
- Codex availability in this task is direct evidence for this account and time
  only. It does not validate Claude entitlement, provider quality equivalence,
  cost, latency, or future availability.

## Traceability

- Governance authority: [REQ-0024](../../../01.requirements/0024-agent-governance-standardization.md),
  [AD-0027](../../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md), and
  [ADR-0029](../../../02.architecture/decisions/0029-workspace-governance-authority.md).
- Preservation authority: [REQ-0026](../../../01.requirements/0026-document-retention-and-retirement.md),
  [AD-0030](../../../02.architecture/descriptions/0030-document-lifecycle-governance.md), and
  [ADR-0031](../../../02.architecture/decisions/0031-preserved-archive-record.md).
- Candidate implementation and evidence: [SPEC-0172](../../../03.specs/0172-document-contract-convergence/spec.md)
  and its [Task](../../../03.specs/0172-document-contract-convergence/tasks/tsk-0001-document-contract-convergence.md).
- Operational execution remains owned by [Stage 05](../../../05.operations/README.md)
  and its subject-level runbooks.

## Limitations

- No secret, credential value, private key, environment value, raw log, or
  shell history was inspected.
- No Compose mutation, k3d mutation, deployment, restart, rollout, or recovery
  action was performed.
- No branch-protection, required-check, environment, provider, or repository
  setting was changed.
- No Claude model call was made, and no cross-provider quality or cost
  comparison is claimed.
- Hosted results are point-in-time observations and must be rerun for the
  feature branch and final commit.
