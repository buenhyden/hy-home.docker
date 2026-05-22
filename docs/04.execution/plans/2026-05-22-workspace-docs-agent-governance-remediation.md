---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-22-workspace-docs-agent-governance-remediation.md -->

# Workspace Docs and Agent Governance Remediation Plan

> Workspace documentation lifecycle, template contract, and agent runtime governance remediation plan.

## Overview (KR)

이 문서는 `hy-home.docker`의 문서 lifecycle, 템플릿 계약, cross-link, AI Agent governance, hook/runtime surface를 현재 워크스페이스 목적에 맞게 정리하기 위한 실행 계획이다.

핵심 방향은 계약 우선 단계형 작업이다. 먼저 `docs/99.templates`, validator, canonical path 기준을 정리한 뒤, 그 기준으로 stage 문서와 agent runtime 문서를 정규화한다.

## Context

이 저장소는 Docker Compose 기반 홈 서버와 개인 개발 인프라를 계층별로 분리하고, 요구사항부터 운영 지식까지 `docs/01`~`docs/05` lifecycle로 연결하는 것을 목표로 한다. 현재 governance hub, templates, runtime hook, agent/function mirror는 이미 존재하지만 다음 drift가 남아 있다.

- `check-repo-contracts.sh`가 stale LLM Wiki index 때문에 실패한다.
- historical stage 문서 중 일부가 현재 template metadata나 heading contract를 완전히 따르지 않는다.
- `docs/02.architecture`에는 canonical `0026-standardize-infra-net.md`와 충돌하는 dated duplicate ARD/ADR 후보가 남아 있다.
- 일부 README와 operation leaf 문서가 `readme.template.md` 또는 `operation.template.md`의 현재 계약과 어긋난다.
- agent runtime 문서에는 stale section reference, unavailable `rtk` guidance, Hookify `.local.md` tracking convention drift가 있다.

## Goals & In-Scope

- **Goals**:
  - `docs/01`~`docs/05`, `docs/90`, `docs/99`의 lifecycle와 template contract를 검증 가능한 상태로 맞춘다.
  - duplicate/non-canonical 문서는 canonical target으로 참조를 이관한 뒤 삭제한다.
  - historical evidence 문서는 삭제하지 않고 현재 template 필수 형식과 규칙을 만족하게 한다.
  - Claude/Codex hook parity와 `.agents` compatibility boundary를 유지한다.
- **In Scope**:
  - `docs/99.templates`, stage README, selected stage leaf docs, generated LLM Wiki index
  - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `RTK.md`, `docs/00.agent-governance/**`
  - `.claude/**`, `.codex/**`, `.agents/**` documentation and hook-related contracts
  - `scripts/validation/check-repo-contracts.sh` full-stage template gate expansion

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Docker runtime behavior, service topology, secrets, or compose service definitions are not changed.
  - Historical evidence content is not rewritten for style only.
  - New active stage taxonomy is not introduced.
- **Out of Scope**:
  - Secret values, private keys, shell history, log databases, and personal runtime settings
  - Existing untracked `projects/storybook/mcp/`
  - Reverting pre-existing `graphify-out/GRAPH_REPORT.md` dirty state

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Add execution plan and task evidence for this remediation | `docs/04.execution/plans/`, `docs/04.execution/tasks/`, execution READMEs | DOC-GOV-001 | Plan/task files follow templates and are linked from parent READMEs |
| PLN-002 | Strengthen template guidance before normalizing target docs | `docs/99.templates/*.template.*`, `docs/99.templates/README.md` | DOC-GOV-002 | Template contract scan passes and no unresolved placeholder leaks into target docs |
| PLN-003 | Normalize README and stage document metadata/heading drift | `README.md`, `docs/**/README.md`, stage leaf docs | DOC-GOV-003 | Full-stage template gate passes |
| PLN-004 | Remove duplicate infra_net ARD/ADR after reference migration | `docs/02.architecture/**`, linked stage docs, validator allowlists | DOC-GOV-004 | No reference to deleted duplicate files remains |
| PLN-005 | Align agent/runtime governance and Hookify tracking exception | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `RTK.md`, `.claude/`, `.codex/`, `.agents/`, governance docs | DOC-GOV-005 | Hook parity and runtime catalog checks pass |
| PLN-006 | Extend validator from changed-file gate to full-stage gate | `scripts/validation/check-repo-contracts.sh` | DOC-GOV-006 | Full repository contract check passes |
| PLN-007 | Refresh generated LLM Wiki index and progress evidence | `docs/90.references/llm-wiki/index.md`, `docs/00.agent-governance/memory/progress.md` | DOC-GOV-007 | LLM Wiki generator check passes |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Syntax | Shell hook and validator syntax check | `bash -n scripts/validation/check-repo-contracts.sh scripts/hooks/agent-event-hook.sh scripts/hooks/post-tool-validate.sh .claude/hooks/*.sh` | exit code 0 |
| VAL-PLN-002 | JSON | Runtime hook JSON validity | `python3 -m json.tool .claude/settings.json` and `python3 -m json.tool .codex/hooks.json` | both exit code 0 |
| VAL-PLN-003 | Contract | Repository docs/runtime contract | `bash scripts/validation/check-repo-contracts.sh` | exit code 0 |
| VAL-PLN-004 | Traceability | Execution and operations traceability | `bash scripts/validation/check-doc-traceability.sh` | exit code 0 |
| VAL-PLN-005 | Security baseline | Template/security baseline | `bash scripts/validation/check-template-security-baseline.sh` | exit code 0 |
| VAL-PLN-006 | Generated docs | LLM Wiki freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | exit code 0 |
| VAL-PLN-007 | Compose | Compose validation when infra README/docs trigger it | `bash scripts/validation/validate-docker-compose.sh` | exit code 0 or explicit not-run reason |
| VAL-PLN-008 | Hook behavior | Stage edit guidance, post-edit validation, Stop gate samples | sample JSON piped to `scripts/hooks/agent-event-hook.sh` | expected guidance/blocking behavior observed |
| VAL-PLN-009 | Diff hygiene | Whitespace and patch sanity | `git diff --check` | exit code 0 |
| VAL-PLN-010 | Graphify | Advisory graph health report | `bash scripts/knowledge/report-graphify-health.sh` | clean or advisory with reason recorded |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Historical document meaning changes during template alignment | High | Add only metadata, required headings, target links, and factual context derived from the same document or canonical linked docs |
| Runbook rollback steps are invented | High | Use factual-only recovery content; when not verified, record explicit N/A reason and escalation path |
| Full-stage validator becomes too strict for intentional historical evidence | Medium | Normalize target docs first, then add named exemptions only for intentional examples or generated docs |
| Duplicate ARD/ADR deletion breaks links | Medium | Run reference search before deletion and remove validator allowlist entries tied to the duplicates |
| Hookify `.local.md` convention is misunderstood | Low | Document tracked team-shared Hookify rule exception in `.claude`/provider guidance |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repository validators and hook smoke tests pass locally.
- **Sandbox / Canary Rollout**: changes remain docs/runtime governance only; no Docker runtime mutation.
- **Human Approval Gate**: this plan is based on the approved user plan and follow-up decisions on legacy cleanup, runbook recovery, Hookify tracking, and full-stage validator scope.
- **Rollback Trigger**: validator cannot pass without deleting historical evidence or inventing operational procedures.
- **Prompt / Model Promotion Criteria**: not applicable; no model or prompt production surface changes.

## Completion Criteria

- [x] Plan/task evidence exists and parent execution READMEs link to both.
- [x] Template guidance matches lifecycle, duplicate cleanup, and factual-only recovery policy.
- [x] README and stage docs satisfy full-stage template gate.
- [x] Duplicate `2026-04-01-standardize-infra-net.md` ARD/ADR files are removed after reference migration.
- [x] Agent/runtime guidance stays thin, current, and provider-aligned.
- [x] LLM Wiki index freshness check passes.
- [x] Required validation commands pass or have explicit not-run reasons.

## Related Documents

- **Task**: [Workspace docs and agent governance remediation task](../tasks/2026-05-22-workspace-docs-agent-governance-remediation.md)
- **Docs index**: [Docs README](../../README.md)
- **Governance hub**: [Agent governance README](../../00.agent-governance/README.md)
- **Documentation protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage authoring matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Templates**: [Template catalog](../../99.templates/README.md)
- **LLM Wiki index**: [Generated LLM Wiki index](../../90.references/llm-wiki/index.md)
