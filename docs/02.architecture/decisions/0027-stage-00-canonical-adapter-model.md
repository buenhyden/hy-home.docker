---
status: active
---
<!-- Target: docs/02.architecture/decisions/0027-stage-00-canonical-adapter-model.md -->

# ADR-0027: Stage 00 Canonical Adapter Model

## Overview (KR)

이 문서는 `hy-home.docker`의 AI Agent 거버넌스에서 Stage 00을 유일한 canonical policy/catalog source로 유지하고, `.claude/`, `.codex/`, `.agents/`를 provider-specific adapter로 제한한다는 결정을 기록한다.

## Context

Phase 1 진단은 Stage 00 canonical adapter model이 이미 존재하고 provider runtime surface도 정렬되어 있음을 확인했다. 동시에 Agent Governance, Codex/provider harness, external strategy skill, HADS, Docker/QA/DevOps guidance를 직접 다루는 Stage 01/02 근거 문서가 없다는 traceability gap도 확인했다.

여러 provider가 같은 저장소에서 동작하면 정책 분산 위험이 커진다. Claude Markdown agents, Codex TOML agents, Gemini-compatible `.agents/` surface는 각기 다른 형식을 갖지만, repository 목적과 safety boundary는 동일해야 한다. 따라서 정책 source와 adapter mechanics를 명확히 분리하는 formal decision이 필요하다.

## Decision

- Stage 00 under `docs/00.agent-governance/` is the only canonical source for agent policy, workflow rules, scopes, provider-neutral catalog entries, template expectations, and governance memory contract.
- `.claude/`, `.codex/`, and `.agents/` are provider runtime adapters. They may express Stage 00 catalog entries in provider-native formats, but they must not redefine policy.
- `.codex/agents/*.toml` is the active Codex agent adapter surface. `.codex/agents/*.md` may remain compatibility prompt context but cannot override Stage 00 or validated TOML adapter behavior.
- External strategy skills must be adapted into canonical repository stage paths rather than creating active non-stage specs, plans, or task logs.
- HADS remains advisory until a separate approved rollout changes the template contract.
- Docker hardening, QA, DevOps, and CI/CD strategy additions must distinguish hard repository validators from manual review expectations.

## Explicit Non-goals

- This ADR does not define new provider model IDs or reasoning-effort values.
- This ADR does not retire legacy compatibility prompt files.
- This ADR does not make HADS mandatory.
- This ADR does not mutate Docker runtime, secrets, deployment state, or remote GitHub protection settings.
- This ADR does not replace existing service/tier ARD or ADR documents.

## Consequences

- **Positive**:
  - Provider-specific files remain smaller and easier to regenerate or validate.
  - Agents can resolve authority conflicts by returning to Stage 00.
  - Drift checks can compare provider surfaces against a single catalog.
  - Stage 01/02/04 traceability for agent governance becomes explicit.
- **Trade-offs**:
  - Some provider-native capabilities must be documented as adapter mechanics instead of policy.
  - Broad HADS or Docker hardening changes require additional approval gates.
  - Historical Phase 2/3/4 artifacts remain as evidence and may not reflect the newest wording without targeted updates.

## Alternatives

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
  - Claude and Gemini surfaces would become secondary or stale.
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

- Model selection belongs in `subagent-protocol.md` and provider overlays, not provider adapter files alone.
- Tool gating belongs in Stage 00 rules and hooks; adapters route execution.
- Guardrail strategy is shared across providers and validated by repository scripts.
- Planner/executor patterns map to canonical Stage 04 plan/task documents.
- Fallback model policy requires Stage 00 update and validation before adapter changes.

## Related Documents

- **PRD**: [Agent Governance Standardization Product Requirements](../../01.requirements/2026-06-01-agent-governance-standardization.md)
- **ARD**: [Agent Governance Canonical Adapter ARD](../requirements/0027-agent-governance-canonical-adapter.md)
- **Phase 1 Plan**: [Agent Governance Phase 1 Diagnostic](../../04.execution/plans/2026-06-01-agent-governance-phase1-diagnostic.md)
- **Phase 2 Plan**: [Agent Governance Phase 2 Alignment Plan](../../04.execution/plans/2026-06-01-agent-governance-phase2-alignment.md)
- **Task**: [Agent Governance Stage 01/02 Alignment Task](../../04.execution/tasks/2026-06-01-agent-governance-stage01-02-alignment.md)
- **Related ADR**: [ADR-0026: Standardize infra_net Compose Network](./0026-standardize-infra-net.md)
