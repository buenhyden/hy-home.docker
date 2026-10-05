---
title: "Open WebUI as Primary AI/RAG Interface"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0016"
parent_ids:
- "AD-0013"
created: "2026-03-27"
---
# ADR-0016: Open WebUI as Primary AI/RAG Interface

## Context

This document records the architecture decision for selecting Open WebUI as the default AI interface and RAG (Retrieval-Augmented Generation) orchestrator of the `hy-home.docker` ecosystem.

Local LLM interaction requires a user-friendly, feature-complete interface that supports document-based knowledge expansion (RAG). We need a solution that integrates natively with Ollama and Qdrant while supporting modern web standards and security (SSO).

### Follow-up

performance.

### Traceability

The verification basis for this decision is limited to the Architecture Description, Spec, and Operations documents linked under `Related Documents`, and the current repository configuration. It does not claim any runtime state without separate execution evidence.

## Decision

- Use **Open WebUI** (formerly Ollama WebUI) as the primary entry point for AI chat.
- **Decision 1**: Deploy Svelte-based Open WebUI for premium frontend.
- **Decision 2**: Use SQLite for state persistence (chat history).
- **Decision 3**: Integrate with Traefik SSO middleware for auth.
- **Decision 4**: Use Ollama as primary inference engine.

### Decision Drivers

The decision context above records the applicable drivers and evidence.

## Alternatives

### Alternatives

### Options Considered

### [LibreChat]

- Good: Highly customizable, supports many providers.
- Bad: More complex setup for local RAG compared to Open WebUI's native Ollama integration.

### [Ollama CLI]

- Good: Extremely lightweight.
- Bad: No visual RAG, no multi-user history, high barrier for non-technical users.

## Consequences

- **Positive**:
  - Unified, aesthetic interface for all local models.
  - Out-of-the-box support for RAG with PDF/Text/Web sources.
  - Active community and frequent updates.
- **Trade-offs**:
  - Increased GPU/System memory consumption for the Svelte/Python backend.
  - Dependency on external vector stores for production-grade scaling.

### Explicit Non-goals

- Custom development of a chat UI from scratch.
- Real-time multi-modal streaming without local model support.

## Related Documents

- **PRD**: [../../01.requirements/0013-ai-open-webui.md](../../01.requirements/0013-ai-open-webui.md)
- **Architecture Description**: [../descriptions/0013-open-webui-architecture.md](../descriptions/0013-open-webui-architecture.md)
- **Spec**: [../../03.specs/009-ai/open-webui.md](../descriptions/0008-ai-architecture.md)
