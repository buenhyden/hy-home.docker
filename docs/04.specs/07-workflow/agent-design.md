---
status: draft
---
<!-- Target: docs/04.specs/07-workflow/agent-design.md -->

# Workflow Cross-Validation Agent Design

## Overview (KR)

이 문서는 인프라 변경 직후 `security-auditor`와 `iac-reviewer`를 순차 호출하는 workflow cross-validation 에이전트 설계를 정의한다. 목적은 infra 변경 검증을 canonical stage 문서로 관리하고, 보안·드리프트·성능 검증 결과를 일관된 메시지 계약과 메모리 규칙으로 기록하는 것이다.

## Parent Documents

- **Spec**: [./spec.md](./spec.md)
- **PRD**: 전용 PRD는 없으며 workflow 계층의 상위 맥락은 [../../01.prd/2026-03-28-07-workflow-optimization-hardening.md](../../01.prd/2026-03-28-07-workflow-optimization-hardening.md)를 따른다.
- **ARD**: 전용 ARD는 없으며 구조적 상위 맥락은 [../../02.ard/0022-workflow-optimization-hardening-architecture.md](../../02.ard/0022-workflow-optimization-hardening-architecture.md)를 따른다.
- **Related ADRs**: 전용 ADR은 없으며 agent governance는 [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)와 [../../00.agent-governance/subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)를 따른다.

## Scope & Non-goals

- **Covers**:
  - infra 변경 후 cross-validation orchestration
  - agent-to-agent handoff contract
  - audit result persistence and reporting rules
  - memory/context strategy for the workflow
- **Does Not Cover**:
  - 개별 infra 서비스 구현 세부
  - 새로운 PRD/ARD/ADR stage 생성
  - 글로벌 스킬 저장소 수정

## Agent Role

- **Primary Role**: infra 변경 후 독립 검증 체인을 안전하게 오케스트레이션하는 cross-validation coordinator
- **Primary User / Caller**: `infra-implementer` 또는 이를 라우팅하는 `workflow-supervisor`
- **Success Definition**: post-flight 이후 `security-auditor`와 `iac-reviewer`가 정해진 순서와 메시지 계약으로 실행되고, 결과가 `_workspace/` 및 `docs/00.agent-governance/memory/progress.md`에 일관되게 기록된다.

## Inputs / Outputs

- **Inputs**:
  - 변경된 파일 목록
  - `infra-validate` pre/post 결과
  - active governance context (`AGENTS.md`, `documentation-protocol.md`, relevant scopes)
  - downstream agent responses
- **Outputs**:
  - `"audit-request: <file-list>"`
  - `"validate-request: <file-list>"`
  - `"validate-complete: PASS|WARN <summary>"`
  - `"BLOCK: <reason>"`
  - `_workspace/cross-validate_<YYYY-MM-DD>.md`
  - `docs/00.agent-governance/memory/progress.md` append entry
- **Expected Structured Format**:
  - message payloads are plain-text, deterministic, and severity-coded as `PASS`, `WARN`, or `BLOCK`

## Orchestration Model

- `handoff`
- **Why this model**:
  - 기존 agent catalog가 이미 역할별 책임을 분리하고 있어 중앙 orchestrator보다 ordered handoff가 더 작고 명확하다.
  - `security-auditor`와 `iac-reviewer`는 서로 다른 검증 책임을 가지므로 단계적 위임이 적합하다.
- **Escalation / Handoff rules**:
  - `infra-implementer` → `security-auditor`: post-flight 성공 후 `"audit-request"`
  - `security-auditor` → `infra-implementer`: critical finding 시 `"BLOCK"`
  - `security-auditor` → `iac-reviewer`: critical clear 시 `"validate-request"`
  - `iac-reviewer` → `infra-implementer`: `"validate-complete: PASS|WARN <summary>"`
  - `BLOCK`는 즉시 사용자 escalation 대상이다.

## Tools & Permissions

| Tool | Purpose | Allowed Actions | Forbidden Actions | Failure Handling |
| --- | --- | --- | --- | --- |
| `docker compose config` | Compose static validation | Read-only config expansion | Applying infra mutations | Stop and report validation failure |
| `docker compose ps` | Post-flight health check | Read service health | Restarting or tearing down services | Record missing health evidence |
| `docker image ls` | Image audit evidence | Inspect image tag/digest state | Pulling or retagging images | Downgrade to WARN when audit evidence is partial |
| `docker inspect` | Drift/performance inspection | Read container config and limits | Modifying live containers | Report unreachable target as validation gap |
| `bash scripts/check-*.sh` | Policy gate execution | Run approved repository validation scripts | Running unrelated mutation scripts | Attach stderr/stdout summary to report |
| `Read` / workspace file writes | Evidence persistence | Write `_workspace/` report and progress note | Writing plaintext secrets | Redact and halt on secret exposure |

## Prompt / Policy Contract

- **System Instruction Summary**:
  - root shims stay thin
  - governance lives in `docs/00.agent-governance/`
  - active docs must use canonical stage paths only
- **Policy Constraints**:
  - never create active spec/plan content under `docs/superpowers/`
  - never store plaintext secrets in reports or memory
  - keep provider-specific behavior out of generic governance files
- **Versioning Rule**:
  - canonical agent behavior changes belong in `docs/04.specs/<feature-id>/agent-design.md`
  - execution sequencing changes belong in `docs/05.plans/`

## Context & Memory Strategy

- **Session Context**:
  - changed file set
  - current post-flight validation result
  - active scope/rule documents for infra and docs layers
  - latest agent responses in the current validation chain
- **Retrieval Strategy**:
  - filter by layer (`infra`, `docs`) and artifact type before reading broader history
  - prefer canonical stage docs (`docs/04.specs`, `docs/05.plans`) over ad-hoc notes
  - use `progress.md` only for durable outcome recall, not as a source of full design detail
- **Persistent Memory Rule**:
  - persist only stable outcomes: changed file list summary, severity, blocking reason, follow-up requirement
  - keep transient reasoning inside the current session; do not store speculative notes
- **Privacy / Retention Notes**:
  - never store secret values, tokens, or raw credentials
  - reports may reference secret mount paths or policy names, but not materialized secret contents

## Guardrails

- **Input Guardrails**:
  - cross-validation starts only after `infra-validate(post)` success
  - changed file list must be explicit and traceable
- **Output Guardrails**:
  - every terminal state must be one of `PASS`, `WARN`, or `BLOCK`
  - every warning or block must include evidence and next action
- **Blocked Conditions**:
  - post-flight validation absent or failed
  - plaintext secret exposure detected
  - destructive rollback or infra mutation required without user-authorized path
  - active design or plan attempts to use non-stage `docs/*` paths
- **Human Escalation Rule**:
  - any `BLOCK`, ambiguous rollback decision, or permissions gap escalates to the user immediately

## Failure Modes & Fallback

- **Failure Mode 1**: `security-auditor` unreachable or returns incomplete response
- **Fallback 1**: record agent response gap in `_workspace/` and escalate to user without fabricating audit completion
- **Failure Mode 2**: `iac-reviewer` can inspect drift but lacks performance evidence
- **Fallback 2**: return `WARN` with explicit missing evidence instead of `PASS`
- **Failure Mode 3**: legacy references point to removed non-stage docs
- **Fallback 3**: treat as documentation defect, rewrite to canonical path, and fail verification until fixed

## Evaluation Plan

- **Offline Evals**:
  - clean infra change path: audit passes and reviewer returns `PASS`
  - critical finding path: auditor emits deterministic `BLOCK`
  - partial evidence path: reviewer emits `WARN`
- **Online Signals**:
  - `_workspace/cross-validate_<date>.md` created
  - `progress.md` receives durable summary
  - no active references remain to removed `docs/superpowers` artifacts
- **Acceptance Thresholds**:
  - 100% deterministic terminal status vocabulary
  - 0 active spec/plan documents in non-stage paths
  - 0 broken related-document links in changed files
- **Linked Task / Eval Docs**: [../../05.plans/2026-04-10-infra-team-agent-cross-validation.md](../../05.plans/2026-04-10-infra-team-agent-cross-validation.md)

## Observability

- **Trace fields**:
  - `task_id`
  - `changed_files`
  - `audit_phase`
  - `severity`
  - `report_path`
- **Logs / Events**:
  - audit request sent
  - audit decision received
  - drift/performance review completed
  - durable memory append completed
- **Redaction / Privacy Rules**:
  - redact secret values and tokens
  - log only policy names, paths, and high-level findings

## Related Documents

- **Workflow Spec**: [./spec.md](./spec.md)
- **Implementation Plan**: [../../05.plans/2026-04-10-infra-team-agent-cross-validation.md](../../05.plans/2026-04-10-infra-team-agent-cross-validation.md)
- **Operations**: [../../08.operations/07-workflow/optimization-hardening.md](../../08.operations/07-workflow/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/07-workflow/optimization-hardening.md](../../09.runbooks/07-workflow/optimization-hardening.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Subagent Protocol**: [../../00.agent-governance/subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
