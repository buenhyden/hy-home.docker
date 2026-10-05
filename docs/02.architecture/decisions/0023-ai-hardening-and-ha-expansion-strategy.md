---
title: "AI Hardening and HA Expansion Strategy"
version: "1.0.2"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0023"
parent_ids:
- "AD-0023"
created: "2026-03-28"
---
# ADR-0023: AI Hardening and HA Expansion Strategy

## Context

This document records the decision to first carry out immediately applicable hardening (boundary security, GPU concurrency ceilings, stateful template alignment, exporter health-gating, CI gate) for the `08-ai` layer, while pursuing catalog expansion items (model promotion/access separation/log policy) in phases.

The AI tier handles GPU/model resources and user conversation paths at the same time, so an imbalance in security/availability/operational control can quickly lead to failures and policy violations. The catalog requires strengthened operating standards for 08-ai, so a decision that separates short-term stabilization from mid-term expansion is needed.

### Traceability

The verification basis for this decision is limited to the Architecture Description, Spec, and Operations documents linked under `Related Documents`, and the current repository configuration. It does not claim any runtime state without separate execution evidence.

## Decision

- Carry out immediate hardening.
  - Enforce `gateway-standard-chain@file,sso-errors@file,sso-auth@file` on the Ollama/Open WebUI router.
  - Specify `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, and `OLLAMA_MAX_QUEUE` ceilings on Ollama.
  - Align Open WebUI to `template-stateful-med`.
  - Enforce a health-gated `ollama` dependency and a metrics healthcheck on `ollama-exporter`.
  - Introduce `scripts/hardening/check-all-hardening.sh 08-ai` and the CI `infrastructure-hardening` job.
- Carry out catalog expansion in phases.
  - Establish an Ollama model promotion (experimental -> production) procedure
  - Establish an Open WebUI model access permission separation policy
  - Establish a conversation log retention/masking policy

### Decision Drivers

The decision context above records the applicable drivers and evidence.

## Alternatives

### Alternatives

### Options Considered

### Implement all catalog expansion immediately

- Good:
  - Functional expansion can be felt quickly
- Bad:
  - Increased change scope raises stabilization/rollback complexity

### Update documentation only, hold off on runtime/CI hardening

- Good:
  - Reduces short-term implementation cost
- Bad:
  - Cannot automatically block policy violations/regressions

## Consequences

- **Positive**:
  - The AI public path security policy aligns with the gateway standard.
  - Lowers the chance of GPU resource overrun and raises service stability.
  - AI tier regressions can be automatically blocked at the PR stage.
  - Catalog expansion items become executable at the document/task level.
- **Trade-offs**:
  - Introducing concurrency ceilings may limit short-term throughput.
  - Strengthened SSO/access control requires adjusting existing temporary test paths.

### Explicit Non-goals

- Immediately building a multi-node Ollama cluster
- Immediately standardizing multiple external commercial LLM providers
- Changing the Qdrant data model itself

### Agent-related Example Decisions

- Guardrail strategy: The AI public path requires the gateway+SSO chain
- Tool gating: Apply `check-all-hardening.sh 08-ai` as a required policy gate before merging into the AI tier

## Related Documents

- **PRD**: [../01.requirements/0009-ai.md](../../01.requirements/0009-ai.md)
- **Architecture Description**: [../02.architecture/descriptions/0023-ai-optimization-hardening-architecture.md](../descriptions/0023-ai-optimization-hardening-architecture.md)
- **Spec**: [../03.specs/009-ai/spec.md](../descriptions/0008-ai-architecture.md)
- **Related ADR**: [ADR-0008](0008-ollama-openwebui-local-ai.md)
