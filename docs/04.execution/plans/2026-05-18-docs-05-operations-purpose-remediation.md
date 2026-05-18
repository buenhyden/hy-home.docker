---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-18-docs-05-operations-purpose-remediation.md -->

# docs/05.operations Purpose Remediation Plan

## Overview (KR)

이 문서는 `docs/05.operations`를 guide, policy, runbook 목적에 맞게 정리하고, 같은 drift를 repository contract로 막기 위한 실행 계획이다.

## Context

`docs/05.operations`는 guide, policy, runbook, incident를 분리해 관리하는 canonical operations stage다. 2026-05-18 audit에서 일부 leaf 문서가 wrong bucket heading을 유지하거나, policy/runbook profile 필수 heading을 빠뜨린 상태가 확인되었다.

## Goals & In-Scope

- **Goals**:
  - operations leaf 문서를 guide/policy/runbook 목적 profile에 맞춘다.
  - DAG deployment policy를 guide bucket에서 policy bucket으로 이동한다.
  - LLM Wiki maintenance guide/policy/runbook을 목적별 profile로 분리한다.
  - repo contract에 operations purpose profile 검증을 추가한다.
  - LLM Wiki generated index를 최신화한다.
- **In Scope**:
  - `docs/05.operations/**`
  - `docs/99.templates/operation.template.md`
  - `scripts/validation/check-repo-contracts.sh`
  - `docs/90.references/llm-wiki/index.md`
  - `docs/04.execution/plans/README.md`
  - `docs/04.execution/tasks/README.md`
  - `docs/00.agent-governance/memory/progress.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not create new PRD, ARD, ADR, or Spec documents.
  - Do not change Docker Compose, service runtime, secrets, or infrastructure behavior.
  - Do not rewrite historical operations content beyond purpose-profile alignment.
- **Out of Scope**:
  - `projects/storybook/mcp/`
  - Deployment, PR creation, publishing, or incident/postmortem creation

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| OPS-001 | Move DAG deployment policy into policy bucket and fix references | `docs/05.operations/{guides,policies,runbooks}/07-workflow/**` | OPS-PURPOSE-001 | No references to `guides/07-workflow/01.dag-deployment.md` remain outside regenerated indexes |
| OPS-002 | Normalize LLM Wiki maintenance guide/policy/runbook profiles | `docs/05.operations/*/llm-wiki-maintenance.md` | OPS-PURPOSE-002 | Guide has `## Usage`; policy has controls and verification; runbook has procedure and evidence |
| OPS-003 | Add missing policy and runbook profile headings | `docs/05.operations/policies/**`, `docs/05.operations/runbooks/**` | OPS-PURPOSE-003 | Purpose profile scan reports `guides=0`, `policies=0`, `runbooks=0` |
| OPS-004 | Remove nested duplicate Related Documents sections | `docs/05.operations/guides/**` | OPS-PURPOSE-004 | `#### Related Documents` scan returns no matches |
| OPS-005 | Enforce the profile contract | `docs/99.templates/operation.template.md`, `scripts/validation/check-repo-contracts.sh` | OPS-PURPOSE-005 | Repo contract fails on missing or cross-profile headings |
| OPS-006 | Refresh generated indexes and evidence | `docs/90.references/llm-wiki/index.md`, progress log | OPS-PURPOSE-006 | LLM Wiki check and repo validators pass |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-OPS-001 | Structural | Check operations profile headings | Custom Python scan over `docs/05.operations/{guides,policies,runbooks}` | `guides=0`, `policies=0`, `runbooks=0` flagged |
| VAL-OPS-002 | References | Check moved DAG policy references | `rg -n "guides/07-workflow/01\\.dag-deployment\|01\\.dag-deployment\\.md" docs/05.operations README.md AGENTS.md CLAUDE.md GEMINI.md infra scripts` | No stale active references |
| VAL-OPS-003 | Traceability | Verify execution/operations traceability | `bash scripts/validation/check-doc-traceability.sh` | PASS |
| VAL-OPS-004 | LLM Wiki | Verify generated index freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS |
| VAL-OPS-005 | Repository Contract | Verify repo contracts including new operations profile gate | `bash scripts/validation/check-repo-contracts.sh` | PASS |
| VAL-OPS-006 | Diff Hygiene | Check whitespace and conflict markers | `git diff --check` | PASS |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Mechanical heading insertion changes operational meaning | Medium | Only add scope, verification, and escalation scaffolding; preserve existing controls and procedures |
| Moved DAG policy leaves stale links | Medium | Run targeted `rg` and regenerate LLM Wiki index |
| Validator becomes too broad and flags templates or README files | High | Limit profile gate to leaf Markdown under `guides`, `policies`, and `runbooks`; exclude README and incidents |
| Untracked Storybook MCP files are touched | High | Do not edit or stage `projects/storybook/mcp/`; verify with `git status` |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Structural profile scan and stale reference scan must pass before full repository validators.
- **Sandbox / Canary Rollout**: Not applicable; documentation-only remediation.
- **Human Approval Gate**: The user approved the remediation plan in conversation.
- **Rollback Trigger**: Revert only scoped operations/template/validator/index/progress changes if validators cannot pass without broad runtime edits.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [x] Operations purpose profile scan reports zero flagged guide, policy, and runbook files.
- [x] DAG deployment policy lives under `docs/05.operations/policies/07-workflow/`.
- [x] Parent READMEs and direct references use the new DAG policy path.
- [x] Operation template documents the profile contract.
- [x] Repo contract enforces the profile contract.
- [x] LLM Wiki generated index is fresh.
- [x] Progress log records final evidence.

## Related Documents

- **Operations index**: [../../05.operations/README.md](../../05.operations/README.md)
- **Operations template**: [../../99.templates/operation.template.md](../../99.templates/operation.template.md)
- **Task record**: [../tasks/2026-05-18-docs-05-operations-purpose-remediation.md](../tasks/2026-05-18-docs-05-operations-purpose-remediation.md)
- **Documentation protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage authoring matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
