---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-25-home-docker-workspace-audit-improvement.md -->

# Home Docker Workspace Audit Improvement Implementation Plan

> 2026-05-25 workspace audit update plan for low-risk documentation, index, and governance-discoverability fixes.

## Overview

This document is the implementation plan for the `hy-home.docker` workspace audit/update workflow. It cleans up only the stale generated index and audit evidence/discoverability gaps within a low-risk scope, without changing Runtime API, Compose port, Docker network, secret value, `.env` value, or deployment behavior.

## Context

Read-only audit evidence found one blocking local gate: `bash scripts/validation/check-repo-contracts.sh` failed because `docs/90.references/llm-wiki/index.md` was stale. Six reviewer outputs also identified documentation discoverability gaps around supervisor skill routing, Storybook QA commands, hook validation examples, and release/tag readiness evidence. Reviewer outputs are used as evidence inputs, not as sole authority; tracked repository files and local validators remain the source of truth.

## Goals & In-Scope

- **Goals**:
  - Restore the local repo-contract gate by regenerating the LLM Wiki index.
  - Add execution artifacts that preserve audit evidence, deferrals, and verification results.
  - Improve documentation discoverability for the workspace audit skill, Storybook test commands, hook validation behavior, and release-management readiness.
- **In Scope**:
  - `docs/04.execution/plans/2026-05-25-home-docker-workspace-audit-improvement.md`
  - `docs/04.execution/tasks/2026-05-25-home-docker-workspace-audit-improvement.md`
  - Parent execution README links under `docs/04.execution/plans/` and `docs/04.execution/tasks/`
  - `docs/00.agent-governance/memory/progress.md`
  - Generated `docs/90.references/llm-wiki/index.md`
  - `docs/00.agent-governance/agents/agents/workflow-supervisor.md`
  - `projects/storybook/nextjs/README.md`
  - `scripts/README.md`
  - `docs/05.operations/runbooks/00-workspace/release-management.md` and runbook README link

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - No runtime service API, Compose port, Docker network, secret value, `.env` value, deployment, or CI behavior changes.
  - No cleanup of unrelated untracked files or uncertain deletion candidates.
- **Out of Scope**:
  - ARD/ADR template-frontmatter cleanup across 46 architecture leaves.
  - `.agents/skills` compatibility mirror drift (closed by the later 2026-05-25
    runtime skill mirror formatting follow-up; no runtime behavior change).
  - Storybook coverage threshold policy (closed by the later expanded
    authored SSoT follow-up with repo-local 90% threshold enforcement).
  - Remote branch protection and `storybook-coverage` required-check enforcement
    (verified later by read-only GitHub API read-back; no remote mutation in this pass).
  - Actual `.env` sync, secret metadata mutation, secret value work, Docker runtime start/stop, deployments, ports, permissions, and file deletions.
  - Pre-existing untracked `projects/storybook/mcp/`.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create dated execution plan and task artifacts from approved templates | `docs/04.execution/plans/*`, `docs/04.execution/tasks/*` | AUD-2026-05-25 | Parent links exist and doc traceability passes |
| PLN-002 | Regenerate LLM Wiki index after staged path additions | `docs/90.references/llm-wiki/index.md` | AUD-2026-05-25 | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` passes |
| PLN-003 | Register workspace audit revalidation routing in the supervisor catalog | `docs/00.agent-governance/agents/agents/workflow-supervisor.md` | AUD-2026-05-25 | Repo contract check passes |
| PLN-004 | Document Storybook test and coverage commands | `projects/storybook/nextjs/README.md` | AUD-2026-05-25 | Storybook coverage command passes |
| PLN-005 | Clarify hook validation no-payload behavior and Hookify supported events | `scripts/README.md` | AUD-2026-05-25 | Repo contract check passes |
| PLN-006 | Add release-management runbook for manual release/tag readiness and rollback evidence | `docs/05.operations/runbooks/00-workspace/release-management.md`, `docs/05.operations/runbooks/README.md` | AUD-2026-05-25 | Operations purpose profile contract passes |
| PLN-007 | Record safe metadata-only comparisons and deferrals | task artifact, progress log | AUD-2026-05-25 | No secret values or `.env` values are printed or edited |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Hygiene | Check whitespace and patch hygiene | `git diff --check` | No whitespace errors |
| VAL-PLN-002 | Generated index | Confirm LLM Wiki index freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Pass |
| VAL-PLN-003 | Governance | Run repo contracts | `bash scripts/validation/check-repo-contracts.sh` | Pass |
| VAL-PLN-004 | Traceability | Check plan/task/operations links | `bash scripts/validation/check-doc-traceability.sh` | Pass |
| VAL-PLN-005 | Baselines | Check template, QuickWin, hardening, Compose, and secrets readiness | See task verification log | Pass or documented advisory/deferred result |
| VAL-PLN-006 | Graph context | Report Graphify health as advisory navigation only | `bash scripts/knowledge/report-graphify-health.sh` | Advisory accepted only when corroborated with tracked files |
| VAL-PLN-007 | Frontend QA | Run Storybook coverage with repo-approved Node path and `/tmp` temp dirs | `env PATH=/home/hy/.nvm/versions/node/v24.14.0/bin:$PATH TMPDIR=/tmp TEMP=/tmp TMP=/tmp npm run coverage --prefix projects/storybook/nextjs` | Pass |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Generated LLM Wiki misses new files if run before staging | Medium | Stage only intentional new files before regenerating the index because the generator uses `git ls-files` |
| Secret or `.env` value exposure | High | Record key counts and metadata-only drift; do not print values or edit actual `.env`/secret files |
| Scope creep into runtime operations | High | Defer Docker start/stop, deployment, permissions, ports, remote GitHub, and secret value actions |
| Graphify inferred edges mistaken for authority | Medium | Treat Graphify as advisory and corroborate with tracked source files and validators |
| Unrelated untracked Storybook MCP tree disturbed | Medium | Keep `projects/storybook/mcp/` unstaged and unmodified |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Repo validators and Storybook coverage listed in `## Verification Plan`.
- **Sandbox / Canary Rollout**: N/A; documentation and generated index only.
- **Human Approval Gate**: This plan was approved by the user as the implementation scope.
- **Rollback Trigger**: Revert this branch's documentation/index changes if validators fail and cannot be repaired within scope.
- **Prompt / Model Promotion Criteria**: N/A; no model, prompt, or runtime agent behavior change beyond documentation routing.

## Completion Criteria

- [x] Scoped documents and generated index updated.
- [x] Metadata-only env and secret comparisons recorded without values.
- [x] Runtime, remote, deployment, permission, and deletion work remains deferred.
- [x] Required validation commands executed and recorded in the task artifact.
- [x] Only intentional files are staged and committed; `projects/storybook/mcp/` remains untracked.

## Related Documents

- **Task**: [2026-05-25 home docker workspace audit improvement task](../tasks/2026-05-25-home-docker-workspace-audit-improvement.md)
- **Operations**: [Operations index](../../05.operations/README.md)
- **Release Management Runbook**: [release-management.md](../../05.operations/runbooks/00-workspace/release-management.md)
- **LLM Wiki Generated Index**: [index.md](../../90.references/llm-wiki/index.md)
- **Workflow Supervisor**: [workflow-supervisor.md](../../00.agent-governance/agents/agents/workflow-supervisor.md)
- **Scripts README**: [scripts README](../../../scripts/README.md)
- **Storybook Next.js README**: [Storybook Next.js README](../../../projects/storybook/nextjs/README.md)
