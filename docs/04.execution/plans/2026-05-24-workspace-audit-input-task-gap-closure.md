---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-24-workspace-audit-input-task-gap-closure.md -->

# Workspace Audit Input Task Gap Closure Plan

> Follow-up implementation plan for closing input-task evidence gaps in the
> completed Home Docker Workspace Audit and Improvement artifacts.

## Overview (KR)

This plan audits the completed workspace audit artifacts against the original
user-provided audit task list, identifies input tasks that were weakly reflected,
and closes those gaps with documentation-only evidence updates.

## Context

The completed workspace audit already implemented the low-risk documentation,
example, validator, Hookify metadata, runbook guardrail, LLM Wiki, and Graphify
refresh work. A follow-up review was requested to determine whether any tasks
from the original input were not explicitly reflected in the plan/task evidence.

This pass is intentionally bounded to evidence and traceability. It does not
change Docker runtime behavior, actual `.env` values, secret values, remote
GitHub state, deployment behavior, permissions, or untracked Storybook files.

## Goals & In-Scope

- **Goals**:
  - `WAI-GAP-001`: Compare the completed audit artifacts against the original
    input task list.
  - `WAI-GAP-002`: Add missing or weak evidence for target-path coverage,
    reviewer baselines, and Graphify update execution.
  - `WAI-GAP-003`: Preserve metadata-only env and secrets handling, including
    role/purpose metadata without value output.
  - `WAI-GAP-004`: Verify the updated artifacts and create a local
    task-sized commit.
- **In Scope**:
  - This dated Plan and sibling Task artifact.
  - Parent execution README links.
  - The completed workspace audit task artifact.
  - LLM Wiki index refresh after new execution artifacts.
  - Progress log update.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not reopen the completed runtime, secrets, deployment, or deletion
    decisions.
  - Do not rewrite the completed audit into a new report format.
  - Do not change commit history on `main`.
- **Out of Scope**:
  - Actual `.env` value edits.
  - Secret value reads, edits, or output.
  - Compose YAML behavior changes, Docker runtime checks, port exposure
    changes, volume changes, or permission changes.
  - Push, PR creation, remote GitHub branch-protection checks, deployment, or
    release automation.
  - Changes under the pre-existing untracked `projects/storybook/mcp/` tree.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-WAI-GAP-001 | Audit original input tasks against completed Plan/Task evidence | New Task artifact | WAI-GAP-001 | Input requirement matrix identifies proven, weak, and closed items |
| PLN-WAI-GAP-002 | Add target-path ledger and reviewer baseline ledger | `docs/04.execution/tasks/2026-05-24-workspace-audit-improvement.md` | WAI-GAP-002 | Ledger sections exist and reference current counts/evidence |
| PLN-WAI-GAP-003 | Record Graphify update and metadata-only parser evidence | `docs/04.execution/tasks/2026-05-24-workspace-audit-improvement.md` | WAI-GAP-002, WAI-GAP-003 | Verification rows include Graphify update and role/purpose-safe metadata compare |
| PLN-WAI-GAP-004 | Register the new artifacts in execution READMEs and LLM Wiki | Execution READMEs, LLM Wiki index | WAI-GAP-004 | Links are present and generated index is fresh |
| PLN-WAI-GAP-005 | Verify and commit locally | Changed docs and validators | WAI-GAP-004 | Required local checks pass; no push or PR is created |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-WAI-GAP-001 | Structure | Confirm the new Plan/Task and README links exist | `rg -n "workspace-audit-input-task-gap-closure" docs/04.execution` | Expected plan/task links are present |
| VAL-WAI-GAP-002 | Contract | Run repository docs contract checks | `bash scripts/validation/check-repo-contracts.sh` | exit code 0 |
| VAL-WAI-GAP-003 | Traceability | Run execution traceability checks | `bash scripts/validation/check-doc-traceability.sh` | exit code 0 |
| VAL-WAI-GAP-004 | LLM Wiki | Confirm generated LLM Wiki index freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | exit code 0 |
| VAL-WAI-GAP-005 | Diff Hygiene | Confirm whitespace hygiene | `git diff --check` | exit code 0 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Follow-up artifacts imply new runtime work | Medium | Keep scope documentation-only and keep deferred runtime items deferred |
| Secret metadata comparison leaks values | High | Extract only ID, automation flag, type, env key, path, and purpose/role metadata |
| Completed audit evidence is over-rewritten | Medium | Add narrow addenda instead of replacing historical evidence |
| Untracked Storybook tree is accidentally staged | Low | Check `git status --short` and stage only tracked docs generated by this pass |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: input requirement matrix confirms all original input
  tasks are proven, closed, or explicitly deferred.
- **Sandbox / Canary Rollout**: documentation-only edits on a local Codex
  branch.
- **Human Approval Gate**: required before any runtime, secret value, actual
  `.env`, remote, deployment, permission, or deletion work.
- **Rollback Trigger**: any edit requires touching runtime Compose behavior or
  value-bearing local files.
- **Prompt / Model Promotion Criteria**: not applicable.

## Completion Criteria

- [x] New Plan and Task artifacts exist.
- [x] Original input-task gaps are identified.
- [x] Target-path ledger is added to the completed audit task artifact.
- [x] Reviewer baseline ledger is added to the completed audit task artifact.
- [x] Graphify update execution and role/purpose-safe metadata comparison are
      recorded.
- [x] Parent README and LLM Wiki links are fresh.
- [x] Required local checks pass.

## Related Documents

- **Parent Audit Plan**: [Workspace audit improvement plan](./2026-05-24-workspace-audit-improvement.md)
- **Task**: [Workspace audit input task gap closure task](../tasks/2026-05-24-workspace-audit-input-task-gap-closure.md)
- **Parent Audit Task**: [Workspace audit improvement task](../tasks/2026-05-24-workspace-audit-improvement.md)
- **Grill review plan**: [Workspace audit grill review plan](./2026-05-24-workspace-audit-grill-review.md)
- **Grill review task**: [Workspace audit grill review task](../tasks/2026-05-24-workspace-audit-grill-review.md)
- **Plans README**: [Execution plans README](./README.md)
- **Tasks README**: [Execution tasks README](../tasks/README.md)
- **Stage authoring matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Task checklists**: [Task checklists](../../00.agent-governance/rules/task-checklists.md)
- **Graphify report**: [Graph report](../../../graphify-out/GRAPH_REPORT.md)
