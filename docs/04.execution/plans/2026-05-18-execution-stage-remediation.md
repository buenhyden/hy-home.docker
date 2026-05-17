---
status: draft
---
<!-- Target: docs/04.execution/plans/2026-05-18-execution-stage-remediation.md -->

# Execution Stage Remediation Plan

## Overview (KR)

이 문서는 `docs/04.execution` stage를 목적에 맞게 정리하는 bounded remediation 실행 계획이다. Historical execution evidence는 대량 재작성하지 않고, entrypoint README, template examples, current active artifacts, deferred debt 기록을 정리한다.

## Context

`docs/04.execution`은 plan과 task evidence를 관리하는 stage다. 현재 repository validators는 통과하지만, 2026-05-18 audit에서 오래된 execution artifacts의 template drift가 발견되었다.

이 계획은 오래된 plan/task의 의미를 바꾸지 않는 범위에서 현재 agent와 maintainer가 안전하게 사용할 entrypoint와 template contract를 복구한다.

## Goals & In-Scope

- **Goals**:
  - `docs/04.execution` README entrypoints를 현재 stage purpose에 맞게 정리한다.
  - plan/task template의 Related Documents 예시를 real Markdown links로 바꾼다.
  - current/recent execution docs에 target path guidance를 추가한다.
  - active scripts cleanup plan의 missing section drift를 template-aligned heading으로 정리한다.
  - legacy execution drift는 governance memory note로 기록한다.
- **In Scope**:
  - `docs/04.execution/README.md`
  - `docs/04.execution/plans/README.md`
  - `docs/04.execution/tasks/README.md`
  - `docs/04.execution/plans/2026-05-*.md`
  - `docs/04.execution/tasks/2026-05-*.md`
  - `docs/99.templates/plan.template.md`
  - `docs/99.templates/task.template.md`
  - `docs/00.agent-governance/memory/execution-stage-legacy-debt.md`
  - `docs/00.agent-governance/memory/progress.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not bulk-normalize all 2026-03 historical plan/task artifacts.
  - Do not change PRD, ARD, ADR, Spec, operations, runtime, Docker Compose, or service behavior.
  - Do not extend `scripts/validation/check-repo-contracts.sh` in this pass.
- **Out of Scope**:
  - `projects/storybook/mcp/`
  - Branch history cleanup, commit squashing, PR creation, deployment, or external publishing

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Add bounded remediation plan/task artifacts | `docs/04.execution/plans/2026-05-18-execution-stage-remediation.md`, `docs/04.execution/tasks/2026-05-18-execution-stage-remediation.md` | DOC-EXEC-001 | New docs have frontmatter, Target comments, required sections, and working links |
| PLN-002 | Refresh execution stage README entrypoints | `docs/04.execution/README.md`, `plans/README.md`, `tasks/README.md` | DOC-EXEC-002 | README structure and Related Documents reflect current stage purpose |
| PLN-003 | Fix plan/task template Related Documents examples | `docs/99.templates/plan.template.md`, `docs/99.templates/task.template.md` | DOC-EXEC-003 | Template examples use Markdown links instead of backticked pseudo-links |
| PLN-004 | Normalize recent active execution docs only | `docs/04.execution/plans/2026-05-*.md`, `docs/04.execution/tasks/2026-05-*.md` | DOC-EXEC-004 | Current/recent docs include Target guidance and required sections where edited |
| PLN-005 | Record deferred historical drift | `docs/00.agent-governance/memory/execution-stage-legacy-debt.md`, `progress.md` | DOC-EXEC-005 | Memory note records counts, examples, and bounded disposition |
| PLN-006 | Verify bounded remediation | validation commands | DOC-EXEC-006 | Custom scans and repository validators pass |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-EXEC-001 | Structural | Check touched/current docs for required sections and pseudo-link drift | Custom Python scan over touched `docs/04.execution` docs and `docs/99.templates/{plan,task}.template.md` | No missing required headings in touched/current docs; no backticked Markdown pseudo-links in touched docs |
| VAL-EXEC-002 | Links | Check `docs/04.execution` local Markdown links | Custom Python Markdown link scan | No broken local links and no absolute links |
| VAL-EXEC-003 | Traceability | Verify execution/operations traceability | `bash scripts/validation/check-doc-traceability.sh` | PASS |
| VAL-EXEC-004 | Repository Contract | Verify repository Docker/docs contracts | `bash scripts/validation/check-repo-contracts.sh` | PASS |
| VAL-EXEC-005 | LLM Wiki Freshness | Verify generated LLM Wiki index | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS or regenerate index and rerun |
| VAL-EXEC-006 | Diff Hygiene | Check whitespace and conflict markers | `git diff --check` | PASS |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Historical evidence is accidentally rewritten | High | Limit direct normalization to current/recent docs and record older drift in memory |
| Template examples remain unusable for target-relative links | Medium | Convert plan/task template examples to Markdown links while keeping placeholder target paths |
| Validator changes mix with unrelated work | High | Do not edit `scripts/validation/check-repo-contracts.sh` in this pass |
| Untracked Storybook MCP files are touched | High | Do not edit or stage `projects/storybook/mcp/`; verify with `git status` |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Custom docs/04 scans must pass before repository validators.
- **Sandbox / Canary Rollout**: Not applicable; documentation-only remediation.
- **Human Approval Gate**: The user approved the bounded remediation plan.
- **Rollback Trigger**: Revert only scoped docs/template/memory changes if validators cannot pass without broad historical rewrites.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [ ] New plan/task remediation artifacts exist and are linked from parent READMEs.
- [ ] README entrypoints describe plan/task responsibilities accurately.
- [ ] Plan/task template Related Documents examples are clickable Markdown links.
- [ ] Active/recent docs are normalized without bulk rewriting historical artifacts.
- [ ] Legacy drift is recorded in governance memory.
- [ ] Validation commands pass and evidence is recorded.

## Related Documents

- **Execution README**: [../README.md](../README.md)
- **Execution Task**: [../tasks/2026-05-18-execution-stage-remediation.md](../tasks/2026-05-18-execution-stage-remediation.md)
- **Plan Template**: [../../99.templates/plan.template.md](../../99.templates/plan.template.md)
- **Task Template**: [../../99.templates/task.template.md](../../99.templates/task.template.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Legacy Debt Memory**: [../../00.agent-governance/memory/execution-stage-legacy-debt.md](../../00.agent-governance/memory/execution-stage-legacy-debt.md)
