---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-22-workspace-governance-bounded-reaudit.md -->

# Workspace Governance Bounded Re-audit Implementation Plan

> Plan for a full workspace governance re-audit with bounded, evidence-backed remediation.

## Overview (KR)

이 문서는 `hy-home.docker`의 문서 lifecycle, 템플릿 계약, cross-link, AI Agent runtime, hook, subagent, memory, rule, scope를 전수 재감사하되 검증 가능한 drift만 수정하기 위한 실행 계획이다.

이번 작업은 새 체계를 다시 만드는 작업이 아니다. 현재 validator 기준선이 통과 중이므로, 완료된 작업을 active로 설명하는 상태 drift, 최신 검증 결과와 충돌하는 memory note, memory edit hook guidance처럼 근거가 확인된 부분만 고친다.

## Context

현재 기준선은 안정적이다.

- `bash scripts/validation/check-repo-contracts.sh`는 `failures=0`으로 통과한다.
- `bash scripts/validation/check-doc-traceability.sh`는 operations/execution traceability 동기화를 통과한다.
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check`는 generated LLM Wiki index가 fresh라고 보고한다.
- `bash scripts/knowledge/report-graphify-health.sh`는 오염은 없지만 `surprising_cross_root_inferred_edges=3` 때문에 advisory 상태다.

감사에서 확인된 실제 drift는 작다. 2026-05-22 완료 plan/task가 parent README에서 `Active`로 설명되고, 일부 memory note가 최신 validator 지표와 충돌하는 legacy debt를 현재 backlog처럼 설명한다. 또한 target-stage docs와 README edits에는 PreToolUse guidance가 있지만 governance memory note edits에는 같은 수준의 guidance가 없다.

## Goals & In-Scope

- **Goals**:
  - `GOV-RA-001`: docs/01~05, docs/90, docs/99, README, root shims, runtime surfaces, hooks, subagents, memory, rules, scopes를 재감사한다.
  - `GOV-RA-002`: 완료된 2026-05-22 execution artifacts를 parent README에서 completed/current evidence로 설명한다.
  - `GOV-RA-003`: stale memory notes를 최신 validator evidence와 맞춘다.
  - `GOV-RA-004`: memory note edits에 대한 hook/Hookify guidance를 추가한다.
  - `GOV-RA-005`: completed execution artifact를 active로 설명하는 README drift를 repository contract에서 잡는다.
- **In Scope**:
  - `docs/04.execution/**` plan/task evidence and indexes
  - `docs/00.agent-governance/memory/**`
  - `scripts/hooks/agent-event-hook.sh`
  - `.claude/hookify.*.local.md`
  - `.codex/README.md`
  - `scripts/validation/check-repo-contracts.sh`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Docker runtime behavior, service topology, ports, networks, images, volumes, or secrets are not changed.
  - Historical evidence is not rewritten for style.
  - Root shims are not expanded into policy documents.
- **Out of Scope**:
  - secret values, credentials, private keys, shell history, log databases, and personal runtime settings
  - existing untracked `projects/storybook/mcp/`
  - broad template normalization when validators already prove normalized coverage

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-GOV-RA-001 | Add plan/task evidence and execution index links | `docs/04.execution/**` | GOV-RA-001 | New evidence is reachable from execution READMEs |
| PLN-GOV-RA-002 | Fix completed 2026-05-22 artifacts described as active | `docs/04.execution/README.md`, `plans/README.md`, `tasks/README.md` | GOV-RA-002 | No completed 2026-05-22 execution file is described as active |
| PLN-GOV-RA-003 | Refresh stale memory notes with current validator evidence | `docs/00.agent-governance/memory/*.md` | GOV-RA-003 | Notes no longer present closed debt as current backlog |
| PLN-GOV-RA-004 | Add memory edit guidance to hooks and Hookify | `scripts/hooks/agent-event-hook.sh`, `.claude/hookify.*`, `.codex/README.md` | GOV-RA-004 | Hook smoke test emits memory guidance |
| PLN-GOV-RA-005 | Add validator coverage for completed-vs-active README drift | `scripts/validation/check-repo-contracts.sh` | GOV-RA-005 | Repository contract fails on completed execution docs labeled active |
| PLN-GOV-RA-006 | Run full verification and record evidence | validators, Graphify, hook samples, progress log | GOV-RA-001 | Required checks pass or advisory reason is recorded |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-GOV-RA-001 | Syntax | Shell syntax and patch hygiene | `git diff --check` and `bash -n scripts/validation/check-repo-contracts.sh scripts/hooks/agent-event-hook.sh scripts/hooks/post-tool-validate.sh .claude/hooks/*.sh` | exit code 0 |
| VAL-GOV-RA-002 | JSON | Hook config validity | `python3 -m json.tool .claude/settings.json` and `python3 -m json.tool .codex/hooks.json` | both exit code 0 |
| VAL-GOV-RA-003 | Contract | Repository docs/runtime contract | `bash scripts/validation/check-repo-contracts.sh` | exit code 0 |
| VAL-GOV-RA-004 | Traceability | Execution and operations traceability | `bash scripts/validation/check-doc-traceability.sh` | exit code 0 |
| VAL-GOV-RA-005 | Security Baseline | Template/security baseline | `bash scripts/validation/check-template-security-baseline.sh` | exit code 0 |
| VAL-GOV-RA-006 | Generated Docs | LLM Wiki freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | exit code 0 |
| VAL-GOV-RA-007 | Compose | Compose static validation | `bash scripts/validation/validate-docker-compose.sh` | exit code 0 |
| VAL-GOV-RA-008 | Hooks | Target-stage, README, memory, and Stop hook smoke tests | sample JSON piped to `scripts/hooks/agent-event-hook.sh` | expected guidance or block decision observed |
| VAL-GOV-RA-009 | Graphify | Graph health status | `bash scripts/knowledge/report-graphify-health.sh` | clean or advisory reason recorded |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Re-audit expands into historical rewrites | High | Fix only validator-backed or evidence-backed drift |
| Memory notes become active policy | Medium | Keep notes advisory and link back to rules/templates |
| Hook guidance duplicates policy | Low | Keep hooks as advisory context and document the policy source |
| Validator overreaches on old active plan frontmatter | Medium | Check only completed execution docs described as active in parent READMEs |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repository validators and hook smoke tests pass locally.
- **Sandbox / Canary Rollout**: docs, governance, hook guidance, and validator only; no Docker runtime mutation.
- **Human Approval Gate**: user explicitly requested implementation of this bounded re-audit plan.
- **Rollback Trigger**: any required validation cannot pass without changing runtime behavior or rewriting historical evidence.
- **Prompt / Model Promotion Criteria**: not applicable.

## Completion Criteria

- [x] Plan/task evidence exists and parent execution READMEs link to both.
- [x] Completed 2026-05-22 artifacts are no longer described as active in execution READMEs.
- [x] Memory notes reflect current validator metrics and closed backlog status.
- [x] Memory edit hook guidance exists and is documented.
- [x] Repository contract catches completed execution docs labeled active in parent README text.
- [x] Required validation commands pass or record a bounded advisory reason.

## Related Documents

- **Task**: [Workspace governance bounded re-audit task](../tasks/2026-05-22-workspace-governance-bounded-reaudit.md)
- **Previous remediation plan**: [Workspace docs and agent governance remediation plan](./2026-05-22-workspace-docs-agent-governance-remediation.md)
- **Lifecycle closure plan**: [Lifecycle README debt closure plan](./2026-05-22-lifecycle-readme-debt-closure.md)
- **Documentation protocol**: [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage authoring matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Memory README**: [Governance memory README](../../00.agent-governance/memory/README.md)
- **Template catalog**: [Template catalog](../../99.templates/README.md)
