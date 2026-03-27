<!-- Target: docs/03.adr/0016-open-webui-implementation.md -->

# ADR-0016: Open WebUI as Primary AI/RAG Interface

---

## Overview (KR)

이 문서는 Open WebUI를 `hy-home.docker` 에코시스템의 기본 AI 인터페이스 및 RAG(Retrieval-Augmented Generation) 오케스트레이터로 선정함에 따른 아키텍처 결정 기록이다.

## Context

Local LLM interaction requires a user-friendly, feature-complete interface that supports document-based knowledge expansion (RAG). We need a solution that integrates natively with Ollama and Qdrant while supporting modern web standards and security (SSO).

## Decision

- Use **Open WebUI** (formerly Ollama WebUI) as the primary entry point for AI chat.
- **Decision 1**: Deploy Svelte-based Open WebUI for premium frontend.
- **Decision 2**: Use SQLite for state persistence (chat history).
- **Decision 3**: Integrate with Traefik SSO middleware for auth.
- **Decision 4**: Use Ollama as primary inference engine.

## Related ADRs
performance.

## Explicit Non-goals

- Custom development of a chat UI from scratch.
- Real-time multi-modal streaming without local model support.

## Consequences

- **Positive**:
    - Unified, aesthetic interface for all local models.
    - Out-of-the-box support for RAG with PDF/Text/Web sources.
    - Active community and frequent updates.
- **Trade-offs**:
    - Increased GPU/System memory consumption for the Svelte/Python backend.
    - Dependency on external vector stores for production-grade scaling.

## Alternatives

### [LibreChat]
- Good: Highly customizable, supports many providers.
- Bad: More complex setup for local RAG compared to Open WebUI's native Ollama integration.

### [Ollama CLI]
- Good: Extremely lightweight.
- Bad: No visual RAG, no multi-user history, high barrier for non-technical users.

## Related Documents

- **PRD**: `[../01.prd/2026-03-27-08-ai-open-webui.md]`
- **ARD**: `[../02.ard/0013-open-webui-architecture.md]`
- **Spec**: `[../04.specs/08-ai/open-webui.md]`
- **Plan**: `[../05.plans/2026-03-27-08-ai-open-webui-plan.md]`
