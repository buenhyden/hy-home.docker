---
profile_id: adr
status: superseded
artifact_id: ADR-0027
artifact_type: adr
parent_ids:
  - AD-0027
created: 2026-06-01
updated: 2026-08-22
supersedes: []
superseded_by: ADR-0029
---
# ADR-0027: Stage 00 Canonical Adapter Model

## Overview

이 문서는 `hy-home.docker`의 AI Agent 거버넌스에서 Stage 00을 유일한 canonical policy/catalog source로 유지하고, `.claude/`, `.codex/`, `.agents/`를 provider-specific adapter로 제한한다는 결정을 기록한다.

## Context

Phase 1 진단은 Stage 00 canonical adapter model이 이미 존재하고 provider runtime surface도 정렬되어 있음을 확인했다. 동시에 Agent Governance, Codex/provider harness, external strategy skill, HADS, Docker/QA/DevOps guidance를 직접 다루는 Stage 01/02 근거 문서가 없다는 traceability gap도 확인했다.

여러 provider가 같은 저장소에서 동작하면 정책 분산 위험이 커진다. Claude Markdown agents, Codex TOML agents, and provider-neutral `.agents/` compatibility projections는 각기 다른 형식을 갖지만, repository 목적과 safety boundary는 동일해야 한다. 따라서 정책 source와 adapter mechanics를 명확히 분리하는 formal decision이 필요하다.

## Decision

- Stage 00 under `docs/00.agent-governance/` is the only canonical source for agent policy, workflow states, canonical roles and skills, provider registry, and bounded evidence rules.
- `.claude/`, `.codex/`, and `.agents/` are provider runtime adapters. They may express Stage 00 catalog entries in provider-native formats, but they must not redefine policy.
- `.codex/agents/*.toml` is the only active Codex agent adapter surface. `.codex/agents/*.md` prompt files are retired and must not be recreated.
- External strategy skills must be adapted into canonical repository stage paths rather than creating active non-stage specs, plans, or task logs.
- HADS mandatory validation is bounded to non-README documents under `docs/90.references/data/hads/`; broad HADS conversion outside that path requires a separate approved rollout.
- Docker hardening, QA, DevOps, and CI/CD strategy additions must distinguish hard repository validators from manual review expectations.

## Explicit Non-goals

- This ADR does not define new provider model IDs or reasoning-effort values.
- This ADR does not recreate retired Codex Markdown prompt files.
- This ADR does not broaden HADS mandatory validation beyond `docs/90.references/data/hads/`.
- This ADR does not mutate Docker runtime, secrets, deployment state, or remote GitHub protection settings.
- This ADR does not replace existing service/tier Architecture Description or ADR documents.

## Consequences

- **Positive**:
  - Provider-specific files remain smaller and easier to regenerate or validate.
  - Agents can resolve authority conflicts by returning to Stage 00.
  - Drift checks can compare provider surfaces against a single catalog.
  - Stage 01/02/04 traceability for agent governance becomes explicit.
- **Trade-offs**:
  - Some provider-native capabilities must be documented as adapter mechanics instead of policy.
  - Broad HADS or Docker hardening changes outside the current bounded gates require additional approval.
  - Historical Phase execution artifacts that conflict with current implementation must be archived as tombstones instead of remaining active evidence.

## Options Considered

### Provider-specific policy surfaces

- Good:
  - Each runtime could use its most natural configuration and instruction format.
  - Provider-specific details would be close to the runtime files that need them.
- Bad:
  - Policy drift would be likely.
  - Reviewers would need to inspect multiple directories to know the active rule.
  - Adapter files could silently conflict with Stage 00.

### Codex-centered governance redesign

- Good:
  - The current requested workflow is Codex-heavy, so Codex TOML and hooks could become highly optimized.
  - Codex-specific fields such as reasoning effort could be first-class.
- Bad:
  - Other supported provider surfaces would become secondary or stale.
  - Repository-local governance would be coupled to one provider.
  - Existing Stage 00 provider-neutral catalog would lose authority.

### Mandatory HADS conversion

- Good:
  - AI-readable document blocks could improve targeted reading and summarization.
  - Documentation could become more token-efficient for agent workflows.
- Bad:
  - Hundreds of docs could churn.
  - Existing validators and templates do not require HADS.
  - Mandatory conversion would exceed the Phase 2 alignment scope.

### Preserve current state without formal ADR

- Good:
  - No additional architecture document is needed.
  - Existing Stage 00 text already describes the model.
- Bad:
  - Phase 2 implementation would still lack a Stage 02 decision record.
  - Future agents could treat Stage 04 plan text as the source of the architecture decision.
  - The requirement-to-design trace would remain incomplete.

## Agent-related Example Decisions (If Applicable)

- Model selection belongs in `providers/registry.yaml` and provider overlays, not provider adapter files alone.
- Tool gating belongs in Stage 00 policies and hooks; adapters route execution.
- Guardrail strategy is shared across providers and validated by repository scripts.
- Planner/executor patterns map to canonical Stage 04 plan/task documents.
- Fallback model policy requires Stage 00 update and validation before adapter changes.

## Traceability

이 결정의 확인 근거는 `Related Documents`에 연결된 Architecture Description, Spec, Operations 문서와 현재 저장소 구성으로 한정한다. 별도 실행 증거가 없는 런타임 상태는 주장하지 않는다.

## Decision Drivers

The decision context above records the applicable drivers and evidence.

## Related Documents

- **PRD**: [Agent Governance Standardization Product Requirements](../../01.requirements/0024-agent-governance-standardization.md)
- **Architecture Description**: [Agent Governance Canonical Adapter Architecture Description](../descriptions/0027-agent-governance-canonical-adapter.md)
- **Current Plan**: Agent Governance Decision Items and Attachment-Gap Plan
- **Current Task**: Agent Governance Missing Items Implementation Task
- **Related ADR**: [ADR-0026: Standardize infra_net Compose Network](0026-standardize-infra-net.md)
- **Superseding ADR**: [ADR-0029: Workspace Governance Authority](0029-workspace-governance-authority.md)
