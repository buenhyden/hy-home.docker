---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-25-home-docker-revalidation-deferred-follow-up.md -->

# Home Docker Revalidation Deferred Follow-up Implementation Plan

## Overview (KR)

이 문서는 2026-05-25 `hy-home.docker` workspace audit 결과를 current local branch에서 재검증하고, deferred 항목을 값·런타임 변경 없이 별도 follow-up 산출물로 고정하는 실행 계획서다.

## Context

Local `main` already contains the 2026-05-25 workspace audit improvement commits and is ahead of `origin/main`. The approved follow-up scope is “Revalidate + Deferred”: re-check the existing audit baseline, run independent reviewer passes, preserve no-touch boundaries, and document residual risks without changing runtime or value-bearing surfaces.

## Goals & In-Scope

- **Goals**:
  - Revalidate the completed 2026-05-25 audit baseline against live repo checks.
  - Capture six reviewer-pass findings in a single evidence trail.
  - Preserve a metadata-only env/secrets drift record.
  - Keep deferred runtime/operator/GitHub/cleanup items explicit and reviewable.
- **In Scope**:
  - `docs/03.specs/home-docker-revalidation-deferred-follow-up/spec.md`
  - `docs/04.execution/plans/2026-05-25-home-docker-revalidation-deferred-follow-up.md`
  - `docs/04.execution/tasks/2026-05-25-home-docker-revalidation-deferred-follow-up.md`
  - Parent README links under `docs/03.specs/`, `docs/04.execution/plans/`, and `docs/04.execution/tasks/`
  - `docs/00.agent-governance/memory/progress.md`
  - `docs/05.operations/runbooks/00-workspace/release-management.md` for doc-only tag/changelog gate clarification if reviewer evidence proves a mismatch
  - Generated LLM Wiki index only if repo tooling requires it after intentional files are staged

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - No service API, Docker Compose, port, network, volume, secret value, `.env` value, deployment, or remote GitHub setting changes.
  - No broad historical docs normalization or deletion cleanup.
- **Out of Scope**:
  - `projects/storybook/mcp/` changes.
  - Actual `.env` sync for `QDRANT_GRPC_PORT`.
  - Secret registry value or metadata mutation.
  - `.agents/skills` compatibility mirror updates.
  - ARD/ADR template-frontmatter cleanup across 46 architecture leaves.
  - Storybook coverage threshold enforcement or `storybook-coverage` required-check changes.
  - Docker runtime start/stop, deployment, permissions, ports, and file deletions.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create follow-up spec/plan/task artifacts from approved templates | Stage 03/04 docs | REV-2026-05-25 | Template contracts and README links pass |
| PLN-002 | Run six reviewer passes and integrate findings as evidence inputs | Task artifact | REV-2026-05-25 | Reviewer ledger captures findings and authority boundary |
| PLN-003 | Record metadata-only `.env` and secret registry comparisons | Task artifact only | REV-2026-05-25 | Counts/drift names recorded without values |
| PLN-004 | Re-run repo-native validation suite | Task artifact | REV-2026-05-25 | Pass/advisory/deferred results recorded |
| PLN-005 | Refresh generated LLM Wiki index if required by repo tooling | `docs/90.references/llm-wiki/index.md` if changed | REV-2026-05-25 | Generator check passes |
| PLN-006 | Update governance progress log | `docs/00.agent-governance/memory/progress.md` | REV-2026-05-25 | Progress entry links this follow-up |
| PLN-007 | Clarify release tag changelog gate discovered by CI/CD review | `docs/05.operations/runbooks/00-workspace/release-management.md` | REV-2026-05-25 | Runbook matches tag workflow guard |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Baseline | Confirm branch and no-touch state | `git status --short --branch` | Branch is follow-up branch; only approved docs plus pre-existing no-touch path appear |
| VAL-PLN-002 | Hygiene | Check whitespace | `git diff --check HEAD` | No whitespace errors |
| VAL-PLN-003 | Generated index | Check LLM Wiki freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Pass or generated index refreshed |
| VAL-PLN-004 | Governance | Validate repo contracts | `bash scripts/validation/check-repo-contracts.sh` | Pass |
| VAL-PLN-005 | Traceability | Validate docs links/catalog pairs | `bash scripts/validation/check-doc-traceability.sh` | Pass |
| VAL-PLN-006 | Static infra baselines | Validate template/security, QuickWin, hardening, Compose, secrets readiness | See task verification log | Pass |
| VAL-PLN-007 | Graph context | Report Graphify health | `bash scripts/knowledge/report-graphify-health.sh` | Advisory accepted only with corroboration |
| VAL-PLN-008 | Conditional QA | Run Storybook coverage only if QA surface changed | Node 24 coverage command | Pass or documented skip |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Secret or `.env` values leak into evidence | High | Use counts/key names/metadata only; do not store values |
| Reviewer outputs overrule repo truth | Medium | Treat reviewers as evidence inputs and corroborate with tracked files and validators |
| Generated index misses new untracked docs | Medium | Stage only intentional docs before index refresh if the generator requires tracked files |
| Scope expands into runtime or remote operations | High | Keep these items deferred and require separate approval |
| Pre-existing untracked Storybook MCP tree is disturbed | Medium | Keep `projects/storybook/mcp/` unstaged and unmodified |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Repo-native validators in `## Verification Plan`.
- **Sandbox / Canary Rollout**: N/A; documentation/evidence only.
- **Human Approval Gate**: User approved the “Revalidate + Deferred” implementation plan.
- **Rollback Trigger**: Revert this branch's documentation/index changes if validators fail and cannot be repaired within approved scope.
- **Prompt / Model Promotion Criteria**: N/A; no model or runtime prompt behavior changes.

## Completion Criteria

- [x] Follow-up spec, plan, task, README links, and progress log are updated.
- [x] Six reviewer passes are recorded or explicitly marked unavailable.
- [x] Metadata-only env/secret comparison is recorded without values.
- [x] Validation suite results are recorded with exact pass/advisory/deferred status.
- [x] Release runbook reflects the tag workflow requirement that `CHANGELOG.md` contain the exact pushed tag string.
- [x] Runtime, value-bearing, remote, deployment, permission, broad cleanup, and deletion work remains deferred.
- [x] `projects/storybook/mcp/` remains untouched.

## Related Documents

- **Spec**: [home-docker-revalidation-deferred-follow-up spec](../../03.specs/home-docker-revalidation-deferred-follow-up/spec.md)
- **Task**: [2026-05-25 home docker revalidation deferred follow-up task](../tasks/2026-05-25-home-docker-revalidation-deferred-follow-up.md)
- **Baseline Plan**: [2026-05-25 home docker workspace audit improvement plan](./2026-05-25-home-docker-workspace-audit-improvement.md)
- **Baseline Task**: [2026-05-25 home docker workspace audit improvement task](../tasks/2026-05-25-home-docker-workspace-audit-improvement.md)
- **Release Runbook**: [release-management.md](../../05.operations/runbooks/00-workspace/release-management.md)
- **Governance Memory Progress**: [progress.md](../../00.agent-governance/memory/progress.md)
- **Graphify Report**: [GRAPH_REPORT.md](../../../graphify-out/GRAPH_REPORT.md)
