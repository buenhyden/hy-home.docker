---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-05-provider-workspace-artifact-path-parity.md -->

# Provider Workspace Artifact Path Parity Implementation Plan

## Overview

This plan implements the provider/runtime follow-up from the completed
`_workspace` support-surface contract. It aligns active provider adapters,
provider-local skills, Gemini/Antigravity rules, and the workflow agent design
with the new `_workspace/repo-support/` artifact boundary.

## Context

The completed workspace support-surface contract made `_workspace/repo-support/`
the only approved runtime artifact staging path. Stage 00 agent catalog entries
were already updated, but focused provider-surface scans still found active
`.claude`, `.codex`, `.agents`, and workflow-design references to the old root
`_workspace/` artifact path.

## Goals & In-Scope

- **Goals**:
  - Replace active provider/runtime artifact paths with
    `_workspace/repo-support/`.
  - Keep generated Codex skill adapters synchronized with Claude skill
    adapters.
  - Update the active workflow agent design contract that still names
    `_workspace/` as a write target.
  - Add repository validation so provider surfaces do not regress to unsafe
    root `_workspace/` artifact paths.
  - Record validation and closure evidence.
- **In Scope**:
  - `.claude/agents/*.md`
  - `.claude/skills/*/skill.md`
  - `.codex/skills/*/skill.md` generated from Claude skills
  - `.agents/rules/workspace.md`
  - `.agents/workflows/documentation.md`
  - `docs/03.specs/008-workflow/agent-design.md`
  - `scripts/validation/check-repo-contracts.sh`
  - Stage 04 evidence and progress memory

## Non-Goals & Out-of-Scope

- No model-policy, hook behavior, provider runtime configuration, credentials,
  or remote provider changes.
- No secret value reads, raw log preservation, shell history capture, or `.env`
  inspection.
- No broad rewrite of historical plans, tasks, archive tombstones, or completed
  evidence that mention old `_workspace` paths as historical context.

## Work Breakdown

| Task | Description | Files / Docs Affected | Validation Criteria |
| --- | --- | --- | --- |
| PLN-PWAP-001 | Create Stage 04 plan/task evidence. | this plan, task evidence, Stage 04 indexes | Plan and task are linked and active before provider edits. |
| PLN-PWAP-002 | Normalize active provider and workflow artifact paths. | `.claude/**`, `.codex/**`, `.agents/**`, `docs/03.specs/008-workflow/agent-design.md` | Focused `_workspace` scan shows no active provider/workflow root-artifact paths. |
| PLN-PWAP-003 | Add provider path parity validation. | `scripts/validation/check-repo-contracts.sh` | Repo contracts fail on stale provider `_workspace/` artifact paths and pass on current tree. |
| PLN-PWAP-004 | Validate and close evidence. | task evidence, progress memory, generated indexes if needed | Final validation passes with `failures=0`. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PWAP-001 | Hygiene | Check whitespace and conflict markers. | `git diff --check` | No output. |
| VAL-PWAP-002 | Provider sync | Regenerate and verify generated Codex/Gemini surfaces. | `bash scripts/operations/sync-provider-surfaces.sh --write`; `bash scripts/operations/sync-provider-surfaces.sh --check` | Generated surfaces are fresh. |
| VAL-PWAP-003 | Focused drift | Check active provider/workflow surfaces for old root `_workspace` artifact paths. | `rg --pcre2 -n "_workspace/(?!repo-support|README\\.md)" .agents .claude .codex docs/03.specs/008-workflow/agent-design.md --glob '*.md' --glob '*.toml' --glob '*.json'` | No active stale matches. |
| VAL-PWAP-004 | Traceability | Check documentation traceability. | `bash scripts/validation/check-doc-traceability.sh` | `failures=0`. |
| VAL-PWAP-005 | Implementation alignment | Check docs against tracked implementation surfaces. | `bash scripts/validation/check-doc-implementation-alignment.sh` | `failures=0`. |
| VAL-PWAP-006 | Repo contracts | Check full repository contracts. | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Provider adapter text diverges from generated mirrors | Medium | Run provider sync `--write` and `--check`. |
| Historical evidence is rewritten accidentally | Medium | Scope focused scan and edits to active provider/workflow surfaces only. |
| Validator becomes too broad and flags historical context | Medium | Limit the stale `_workspace` hard gate to provider/runtime adapter surfaces and the active workflow agent design. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: N/A; this is documentation/provider-surface contract work.
- **Sandbox / Canary Rollout**: N/A; no runtime service or provider config changes.
- **Human Approval Gate**: User continued the broader provider/document contract cleanup on 2026-07-05.
- **Rollback Trigger**: Revert the latest logical commit if provider sync or repo contracts fail due to this batch.
- **Prompt / Model Promotion Criteria**: N/A.

## Completion Criteria

- [x] Stage 04 evidence exists and is indexed.
- [x] Active provider/runtime artifact paths use `_workspace/repo-support/`.
- [x] Generated Codex skill mirrors are synchronized.
- [x] Repository validation enforces provider workspace path parity.
- [x] Final validation and progress memory are recorded.

## Related Documents

- **Task**: [Provider Workspace Artifact Path Parity Task](../tasks/2026-07-05-provider-workspace-artifact-path-parity.md)
- **Workspace Support Surface Spec**: [Workspace support surface contract](../../03.specs/106-workspace-support-surface-contract/spec.md)
- **Workflow Agent Design**: [Workflow agent design](../../03.specs/008-workflow/agent-design.md)
- **Provider Capability Matrix**: [Provider capability matrix](../../00.agent-governance/rules/provider-capability-matrix.md)
- **Subagent Protocol**: [Subagent protocol](../../00.agent-governance/subagent-protocol.md)
