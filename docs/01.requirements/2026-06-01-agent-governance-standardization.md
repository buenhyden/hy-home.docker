---
status: active
---
<!-- Target: docs/01.requirements/2026-06-01-agent-governance-standardization.md -->

# Agent Governance Standardization Product Requirements

## Overview (KR)

이 문서는 `hy-home.docker`의 AI Agent 거버넌스 표준화 요구사항을 정의한다. 목표는 Stage 00을 공통 정책과 catalog의 SSoT로 유지하면서 Claude, Codex, Gemini 및 호환 agent surface가 같은 규칙, 작업 흐름, 검증 기준을 따르도록 하는 것이다.

## Vision

`hy-home.docker`의 모든 AI Agent는 provider와 runtime 형식이 달라도 같은 repository 목적, stage-gated documentation lifecycle, Docker Compose 운영 경계, QA/CI/CD 검증 기준을 공유해야 한다.

이 표준화는 agent가 빠르게 작업하는 것보다 안전하고 추적 가능한 변경을 우선한다. 상위 요구사항, 아키텍처 근거, 실행 계획, 작업 증거가 끊기지 않아야 하며, provider별 adapter는 공통 정책을 재정의하지 않아야 한다.

## Problem Statement

Phase 1 진단 결과, Stage 00 canonical adapter model과 provider runtime surface는 이미 존재하지만 이를 직접 뒷받침하는 Stage 01 PRD와 Stage 02 ARD/ADR가 없었다. 그 결과 Phase 2 계획은 Stage 04에서 구현 방향을 설명하지만, agent governance 자체가 왜 필요한지와 어떤 아키텍처 결정으로 유지되어야 하는지의 상위 traceability가 약했다.

또한 외부 strategy skill, HADS, Docker best practice, DevOps/CI/CD, QA 전략이 여러 문서에 흩어져 있어, 무엇이 active policy이고 무엇이 advisory strategy인지 명확히 구분되어야 한다.

## Personas

- **Repository Maintainer**: 여러 provider와 agent surface가 같은 정책을 따르는지 검토하고, drift를 작게 유지해야 한다.
- **AI Agent / Subagent**: 작업 시작 전 어떤 규칙, scope, stage, skill, 검증 절차를 따라야 하는지 명확히 알아야 한다.
- **Infrastructure Operator**: agent 변경이 Docker runtime, secrets, deployment, remote GitHub state에 미치는 위험을 통제해야 한다.
- **Documentation Reviewer**: Stage 01 -> 02 -> 03 -> 04 -> 05 traceability와 template contract 준수를 확인해야 한다.

## Key Use Cases

- **STORY-01**: Maintainer는 agent governance 변경 전에 PRD, ARD, ADR, plan, task evidence를 따라가며 왜 변경이 필요한지 확인한다.
- **STORY-02**: Codex, Claude, Gemini adapter는 같은 Stage 00 catalog를 provider-specific 형식으로 노출하되 별도 정책을 만들지 않는다.
- **STORY-03**: Agent는 Superpowers, HADS, Docker, QA, DevOps strategy를 사용할 때 active repository stage path와 검증 절차로 변환한다.
- **STORY-04**: Reviewer는 Phase 2/3 같은 governance work가 Docker runtime, secrets, deployment, remote GitHub state를 변경하지 않았음을 evidence로 확인한다.

## Functional Requirements

- **REQ-AGG-FUN-01**: Stage 00은 agent catalog, function catalog, workflow rules, provider overlays, memory/progress rules의 canonical source of truth여야 한다.
- **REQ-AGG-FUN-02**: `.claude/`, `.codex/`, `.agents/` provider adapters는 Stage 00 catalog의 role, scope, name set, policy intent를 보존해야 한다.
- **REQ-AGG-FUN-03**: Codex adapter는 `.codex/agents/*.toml`만 active provider adapter로 취급하고, `.codex/agents/*.md` prompt files는 retired 상태로 유지해야 한다.
- **REQ-AGG-FUN-04**: External strategy outputs는 canonical repository stages인 `docs/01`-`docs/05`, `docs/90`, `docs/99`로 귀속되어야 한다.
- **REQ-AGG-FUN-05**: HADS mandatory profile은 `docs/90.references/hads/`의 non-README reference documents에만 적용하고, 그 밖의 active templates나 stage docs에는 broad HADS block tag를 요구하지 않아야 한다.
- **REQ-AGG-FUN-06**: Docker/Compose best-practice guidance는 hard validator와 manual review boundary를 구분해야 한다.
- **REQ-AGG-FUN-07**: QA/CI/CD evidence는 docs-only, policy-only, behavior change, runtime change를 구분해 최소 검증 명령과 skipped-check rationale을 기록해야 한다.
- **REQ-AGG-FUN-08**: Node/npm/rtk 기반 automation은 `/home/hy/.local/bin` toolchain 존재를 활용할 수 있으나, non-interactive agent PATH 차이를 명시적으로 처리해야 한다.

## Non-functional Requirements

- **REQ-AGG-NFR-01**: Governance text must remain deterministic, concise, and free of contradictory provider-specific policy forks.
- **REQ-AGG-NFR-02**: Stage 00 governance files must remain English-only; human-facing stage execution evidence may use Korean where appropriate.
- **REQ-AGG-NFR-03**: Repository checks must be able to detect adapter drift, template drift, unsupported statuses, and traceability gaps.
- **REQ-AGG-NFR-04**: Graphify may support navigation, but completion claims must be corroborated by tracked docs and validation scripts when graph health is advisory.
- **REQ-AGG-NFR-05**: Documentation changes must remove or archive historical content when it conflicts with current tracked implementation truth.

## Success Criteria

- **REQ-AGG-MET-01**: Agent governance PRD, ARD, ADR, Phase 1 diagnostic, and Phase 2 alignment plan are cross-linked.
- **REQ-AGG-MET-02**: `check-repo-contracts.sh`, `check-doc-traceability.sh`, provider surface sync, LLM Wiki freshness, and diff hygiene pass after changes.
- **REQ-AGG-MET-03**: No Docker runtime, secrets, deployment state, remote GitHub settings, or user-global Codex settings are changed during governance documentation alignment.
- **REQ-AGG-MET-04**: Future implementation work can identify whether a proposed governance change belongs in Stage 00 policy, provider adapter mechanics, Stage 04 evidence, or advisory memory.

## Scope and Non-goals

- **In Scope**:
  - Agent governance requirements for Stage 00 and provider adapters.
  - Skill/workflow strategy mapping to canonical repository stages.
  - Documentation and validation requirements for Phase 2/3 governance work.
  - Node/npm/rtk automation assumptions as design input.
- **Out of Scope**:
  - Docker runtime start/stop/recreate, image rebuilds, deployment, migrations, or live network changes.
  - Secret values, private tokens, shell history, or user-global Codex credentials.
  - Remote GitHub branch protection mutation.
  - Broad rewrite of historical artifacts that remain semantically aligned with current implementation.
- **Non-goals**:
  - Do not broaden the HADS mandatory profile beyond `docs/90.references/hads/` in this requirement.
  - Do not recreate `.codex/agents/*.md` compatibility prompt files.
  - Do not create a new non-stage documentation taxonomy.

## Risks, Dependencies, and Assumptions

- Stage 00 provider adapter policy must remain aligned with `providers/agents-md.md` and `subagent-protocol.md`.
- The repository may have graphify advisory findings; these are navigation signals, not proof of completion.
- `/home/hy/.local/bin/node`, `npm`, and `rtk` exist, but command wrappers should not assume every non-interactive shell has that path loaded.
- Future hard validators outside the current infrastructure hardening gate or bounded HADS reference profile require separate approval because they can create broad churn.

## AI Agent Requirements (If Applicable)

- **Allowed Actions**:
  - Read Stage 00, Stage 01/02, templates, provider adapter docs, and validation scripts.
  - Add or update canonical stage documents when explicitly requested.
  - Run non-destructive repository validation commands.
- **Disallowed Actions**:
  - Read or expose secrets, credentials, private keys, shell history, or token-bearing logs.
  - Mutate Docker runtime, deployment state, remote GitHub settings, or user-global Codex settings without explicit approval.
  - Treat provider adapter files as a separate policy source.
- **Human-in-the-loop Requirement**:
  - Required before broad HADS rollout outside `docs/90.references/hads/`, new Docker/runtime mutation, deployment, or remote protection change.
- **Evaluation Expectation**:
  - Every governance implementation task must record validation commands, pass/fail outcomes, skipped-check rationale, and Graphify advisory status when used.

## Related Documents

- **ARD**: [Agent Governance Canonical Adapter ARD](../02.architecture/requirements/0027-agent-governance-canonical-adapter.md)
- **ADR**: [ADR-0027 Stage 00 Canonical Adapter Model](../02.architecture/decisions/0027-stage-00-canonical-adapter-model.md)
- **Current Plan**: [Agent Governance Decision Items and Attachment-Gap Plan](../04.execution/plans/2026-06-02-agent-governance-decision-items-plan.md)
- **Current Task**: [Agent Governance Missing Items Implementation Task](../04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md)
- **Stage 00 Governance Hub**: [Agent governance](../00.agent-governance/README.md)
