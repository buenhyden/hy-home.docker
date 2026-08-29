---
status: active
artifact_id: reference:agentic-engineering-research:automation-pipeline-workflow
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Automation Pipeline Workflow

## Overview

This leaf separates the repository's declared automation topology from local
execution, hosted workflow results, branch protection, deployment, and remote
mutation. It is an advisory routing aid, not a CI/CD policy or run record.

## Purpose

Describe how an author can select the appropriate local, pull-request, or
push-triggered control and retain evidence without treating configuration as
proof that a control ran or was enforced.

## Scope

The review covers the entry-HEAD tracked GitHub workflow registry and YAML,
typed gate dispatch, and local hooks. It excludes GitHub settings, run history,
secrets, environments, artifact contents, deployments, and remote approvals.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `APW-001` | `ci-quality.yml` declares push and pull-request triggers for `main`, manual dispatch, read-oriented default permissions, and 16 named jobs in the tracked contract. | tracked configuration | VERIFIED | `.github/workflows/ci-quality.yml`, `.github/workflow-contract.yml` at `d0d295e1afe75f63e8750fbb7f77a3e7821048a1` | Select the named job/gate for a declared CI path; do not claim a hosted run. |
| `APW-002` | Seven tracked workflow definitions include one required-quality workflow and non-gating lifecycle, changelog-check, label, greeting, stale, and version-sync automation; no tracked workflow declares a deployment environment or `id-token: write`. | tracked configuration | VERIFIED | `.github/workflow-contract.yml`, `.github/workflows/` at entry HEAD | Treat event automation, release-tag checking, and deployment promotion as distinct; deployment enforcement is unobserved. |
| `APW-003` | Retained GitHub guidance separately describes workflow security/pinning, environment protection and artifacts/attestations, and reusable-workflow/OIDC capabilities. | retained official observation | HISTORICAL VERIFIED | Task 0001 delivery ledger plus [dated APW source rows 384–385](../2026-08-08-agentic-engineering-research-pack/automation-pipeline-workflow.md#sources) | A future workflow change needs an explicit target, permission, provenance, secret, approval, and rollback review; the guidance does not establish local adoption. |

### Evidence ladder and adoption mechanics

Use the narrowest accurate state: **configured** for tracked YAML or a gate
registry, **selected** for an approved plan naming a job, **executed** and
**passed** only for recorded command evidence, **hosted** only for an observed
GitHub run, and **enforced** only for observed branch/ruleset/environment
controls. These states do not imply one another.

The local path is a developer-controlled check or hook. The pull-request and
push paths are separately declared workflow triggers; a tag check has its own
trigger. A job should expose the immutable revision, command, inputs, result,
and owner in its durable task evidence. If the change adds an action, token,
artifact, dependency, or deployment path, inspect pinning, least privilege,
provenance, protected-secret timing, approval authority, and recovery before
calling it a promotion path.

No current configuration proves a required check, a branch rule, a successful
hosted job, an artifact attestation, dependency provenance, OIDC exchange, or
a deployment. A workflow filename or YAML `permissions` block is therefore not
permission to mutate a remote target.

| Control | Declared mechanics | Exact local investigation target | Limit |
| --- | --- | --- | --- |
| Action pinning | Workflow `uses:` declarations use full commit SHAs. | `.github/workflows/*.yml` and `.github/workflow-contract.yml` | A pin does not prove the action executed or is sufficient for a particular threat. |
| Least privilege | Workflow and job `permissions` declarations bound token scopes. | `ci-quality.yml`, `document-corpus-lifecycle.yml`, and workflow registry | YAML does not reveal effective repository defaults or token use at runtime. |
| Environment approval / protected secrets | GitHub environments can defer access until protection rules pass. | `.github/workflows/*.yml` for `environment:` and `.github/workflow-contract.yml` | No environment declaration, secret value, approval, or remote protection was observed. |
| Artifact and attestation | Artifact/attestation steps would identify and publish a build output and provenance. | `.github/workflows/*.yml`; `scripts/validation/github_workflow_contract.py` | No tracked hosted artifact or attestation proves a supply-chain result. |
| Dependency provenance | Dependency/audit gates can bound a declared dependency set. | `projects/storybook/nextjs/package-lock.json`, `ci-quality.yml` | A lockfile or audit-job definition is not registry resolution, SBOM, or deployed-image evidence. |
| Reuse and OIDC | Reusable workflow and OIDC mechanisms need job-level use and explicit `id-token: write`. | `.github/workflows/*.yml` | Neither mechanism is declared by the measured workflow set. |
| Local / PR / push separation | Hooks are local; CI Quality declares `pull_request` and `push` on `main`; changelog checking is tag-triggered. | `.pre-commit-config.yaml`, `ci-quality.yml`, `generate-changelog.yml` | Definitions do not show which path ran or whether a PR was merged. |

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `APW-SRC-001` | `APW-001`, `APW-002` | Typed workflow registry / workspace | [.github/workflow-contract.yml](../../../../.github/workflow-contract.yml) | tracked configuration | `d0d295e1afe75f63e8750fbb7f77a3e7821048a1` | 2026-08-28 | Registry describes declared topology, not remote settings or execution. |
| `APW-SRC-002` | `APW-001`, `APW-002` | GitHub workflow definitions / workspace | [.github/workflows](../../../../.github/workflows/) | tracked configuration | `d0d295e1afe75f63e8750fbb7f77a3e7821048a1` | 2026-08-28 | YAML presence does not prove a hosted run, required check, or environment. |
| `APW-SRC-003` | `APW-003` | Workflow syntax and secure use / GitHub | [workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions), [secure use](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) | retained official observation | Task 0001 dated delivery ledger | 2026-08-08T17:45:01+09:00 | Retained trigger, permission, job, and full-SHA guidance; no new request was made. |
| `APW-SRC-004` | `APW-003` | Environments, artifacts, and attestations / GitHub | [environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments), [artifacts](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-what-your-workflow-does/storing-and-sharing-data-from-a-workflow), [attestations](https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations) | retained official observation | Task 0001 dated delivery ledger | 2026-08-08T17:45:01+09:00 | Platform capability only; this repository's environment, artifact, and attestation state was not observed. |
| `APW-SRC-005` | `APW-003` | Reusable workflows and OIDC / GitHub | [reusing workflows](https://docs.github.com/en/actions/sharing-automations/reusing-workflows), [OIDC](https://docs.github.com/en/actions/reference/security/oidc) | retained official observation | [dated APW leaf, source rows 384–385](../2026-08-08-agentic-engineering-research-pack/automation-pipeline-workflow.md#sources) | 2026-08-14 | Retained reuse/OIDC observation from the dated APW leaf; local use remains unobserved. |

## Maintenance

Remeasure the workflow registry, YAML, and gate dispatcher after any workflow,
action, permission, trigger, or gate change. Reopen retained external guidance
only under separately authorized source access. Record remote observations with
their repository, target, timestamp, and authority instead of upgrading local
configuration into remote evidence.

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Route automated agent work through an approved Task and gate. | Inspect Task evidence and gate name. | Dispatch is not hosted execution. |
| architecture | applies | Review automation boundaries when a system contract changes. | Inspect approved design/change record. | No architecture change is proposed. |
| common | applies | Keep shared workflow triggers and permissions explicit. | Inspect registry/YAML correspondence. | Static match is not enforcement. |
| docs | applies | Use documentation checks for changed documentation. | Record the exact validator result. | A check result is not content acceptance. |
| infra | applies | Require a target-specific delivery contract before deployment automation. | Inspect approved environment/recovery evidence. | No environment is observed. |
| ops | applies | Assign release/rollback ownership before remote mutation. | Inspect an approved runbook and event record. | No release event is claimed. |
| qa | applies | Select a named CI gate for the stated oracle. | Inspect gate contract and result. | CI configuration alone is not a pass. |
| security | applies | Review actions, permissions, secrets, provenance, and approvals. | Inspect pinned action and permission declarations. | OIDC, attestations, and protection remain unobserved. |

## Related Documents

- [Quality CI and Formatting](./quality-ci-formatting.md)
- [Verification and Validation](./verification-validation.md)
