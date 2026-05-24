---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-24-workspace-audit-improvement.md -->

# Home Docker Workspace Audit and Improvement Implementation Plan

> Completed plan for the approved Home Docker Workspace Audit and Improvement workflow.

## Overview (KR)

This document defines the execution plan for a full `hy-home.docker` workspace audit and improvement pass. It keeps audit evidence, gap analysis, low-risk remediation, and final reporting traceable without expanding into runtime, secret, deployment, or remote GitHub work.

## Context

The approved audit scope covers the current Home Docker workspace across governance, documentation, scripts, infrastructure, environment metadata, secret metadata, QA, CI/CD, hooks, and skills. The task is evidence-first: create an auditable plan and task record, reuse reviewer baseline outputs as an initial baseline, refresh the baseline only through changed-area checks, and treat Graphify as advisory while the health helper reports advisory status.

The worker constraints for this artifact creation are intentionally narrow:

- Do not read or record secret values.
- Do not edit actual `.env` values or secret value files.
- Do not run Docker runtime behavior checks, deployment, push, PR, or remote GitHub operations.
- Do not delete uncertain legacy material.
- Keep all current edits inside the approved documentation artifact paths.

## Goals & In-Scope

- **Goals**:
  - `WAI-001`: Create the dated plan/task execution artifacts for the approved audit.
  - `WAI-002`: Track full audit coverage for Agent Governance, Documentation Lifecycle, Scripts, Infrastructure, Env, Secrets, QA, CI/CD, Hooks, and Skills.
  - `WAI-003`: Record reusable reviewer baseline outputs and require changed-area refresh checks before final reporting.
  - `WAI-004`: Provide compact ledgers for gaps, decisions, verification, deferred risks, legacy/delete/integration findings, and final reporting.
  - `WAI-005`: Keep env and secrets comparison metadata-only, with no value output.
- **In Scope**:
  - Execution plan/task artifacts and parent README links.
  - Progress log entry for the in-progress audit.
  - Low-risk documentation edits.
  - Examples that do not alter runtime behavior.
  - Contract-preserving validator or hook metadata checks.
  - Runbook guardrails that clarify safe handling.
  - Metadata-only env key and secrets key comparison rows for later completion by the main agent.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not implement broad infrastructure changes during this audit pass.
  - Do not treat Graphify output as final authority when health is advisory.
  - Do not convert the task artifact into the final audit report.
- **Out of Scope**:
  - Actual `.env` value edits.
  - Secret value edits, secret value output, credential access, private keys, shell history, and log databases.
  - Docker runtime behavior, live container checks, ports, filesystem permissions, and service startup changes.
  - Remote GitHub operations, deployment, push, PR creation, or publishing.
  - Deletion of uncertain legacy files or integrations without explicit follow-up approval.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-WAI-001 | Create dated plan and task artifacts from execution templates | `docs/04.execution/plans/2026-05-24-workspace-audit-improvement.md`, `docs/04.execution/tasks/2026-05-24-workspace-audit-improvement.md` | WAI-001 | Files exist, contain no template placeholders, and link to each other |
| PLN-WAI-002 | Add parent README links for the new artifacts | `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md` | WAI-001 | Parent READMEs include the new plan/task paths |
| PLN-WAI-003 | Record in-progress audit status | `docs/00.agent-governance/memory/progress.md` | WAI-001 | Current work log has an In Progress row for the audit |
| PLN-WAI-004 | Establish full audit coverage ledger | Task artifact | WAI-002 | All 10 approved target areas have compact coverage rows |
| PLN-WAI-005 | Capture gap, decision, change-scope, verification, skill, env, secrets, deferred-risk, legacy, integration, and final-report scaffolds | Task artifact | WAI-003, WAI-004, WAI-005 | Required sections exist with actionable status rows |
| PLN-WAI-006 | Verify artifact links and repository contract hygiene | Changed artifacts and local validators | WAI-001 | Required local checks pass, or skipped checks have explicit reasons |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-WAI-001 | Structure | Confirm new artifacts and README links exist | `rg -n "2026-05-24-workspace-audit-improvement" docs/04.execution docs/00.agent-governance/memory/progress.md` | Expected paths are found |
| VAL-WAI-002 | Link hygiene | Check changed Markdown links and target paths | Targeted Markdown link scan for changed files | No broken repo-local links in changed files |
| VAL-WAI-003 | Contract | Run repository docs contract check if practical | `bash scripts/validation/check-repo-contracts.sh` | exit code 0 |
| VAL-WAI-004 | Traceability | Run execution traceability check if practical | `bash scripts/validation/check-doc-traceability.sh` | exit code 0 |
| VAL-WAI-005 | Diff hygiene | Confirm patch whitespace is clean | `git diff --check` | exit code 0 |
| VAL-WAI-006 | Graphify | Treat graph navigation as advisory pending health refresh | `bash scripts/knowledge/report-graphify-health.sh` | Clean or advisory reason recorded |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Artifact creation drifts into implementation | Medium | Keep this worker scoped to docs artifacts and parent links only |
| Secret or env values are exposed | High | Record only metadata-only comparison rows and leave value details out |
| Reviewer baseline is over-trusted | Medium | Mark reused baseline as initial only and require changed-area refresh checks |
| Graphify advisory output is treated as authoritative | Medium | Record Graphify as advisory pending health report and corroborate with tracked files |
| Legacy deletion is attempted without certainty | High | Defer uncertain delete decisions to the risk register |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: changed documentation artifacts pass targeted link and diff hygiene checks.
- **Sandbox / Canary Rollout**: documentation-only artifact creation under the owned write scope.
- **Human Approval Gate**: required before actual env value edits, secret value work, Docker runtime changes, deploy, push, PR, or deletion.
- **Rollback Trigger**: any artifact change requires touching files outside the approved owned write scope.
- **Prompt / Model Promotion Criteria**: not applicable.

## Completion Criteria

- [x] Dated plan artifact exists.
- [x] Dated task artifact exists.
- [x] Parent plan/task README links exist.
- [x] Progress log has a completed audit entry.
- [x] Task artifact contains all required audit evidence sections.
- [x] Metadata-only env and secrets rows are filled without values.
- [x] Changed-area verification refreshed reused reviewer baseline outputs.

## Input Task Gap Closure Addendum

The follow-up input-task completeness review found that the completed Task
artifact already proved the main audit implementation, but several original
input requirements were only implicit:

- target-path coverage was present through area coverage and inventories, but
  did not have a dedicated target-path ledger;
- the six reviewer baselines were referenced, but not enumerated;
- Graphify health was recorded, but the `graphify update .` execution was not
  listed as its own verification row;
- the secrets parser evidence skipped values, but did not explicitly name
  purpose/role metadata.

These evidence gaps are closed by the sibling input-task gap closure Plan/Task
and the updated Task addendum. No runtime, secret value, actual `.env`, remote,
deployment, permission, or deletion work was added.

## Related Documents

- **Task**: [Workspace audit improvement task](../tasks/2026-05-24-workspace-audit-improvement.md)
- **Input task gap closure plan**: [Workspace audit input task gap closure plan](./2026-05-24-workspace-audit-input-task-gap-closure.md)
- **Input task gap closure task**: [Workspace audit input task gap closure task](../tasks/2026-05-24-workspace-audit-input-task-gap-closure.md)
- **Plans README**: [Execution plans README](./README.md)
- **Tasks README**: [Execution tasks README](../tasks/README.md)
- **Stage authoring matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Documentation protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Task checklists**: [Task checklists](../../00.agent-governance/rules/task-checklists.md)
- **Progress log**: [Agent progress log](../../00.agent-governance/memory/progress.md)
- **Plan template**: [Plan template](../../99.templates/plan.template.md)
- **Task template**: [Task template](../../99.templates/task.template.md)
- **Graphify report**: [Graph report](../../../graphify-out/GRAPH_REPORT.md)
