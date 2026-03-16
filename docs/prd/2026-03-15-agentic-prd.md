---
layer: agentic
---
# Agentic Framework PRD

- **Status**: Canonical
- **Owner**: buenhyden
- **layer:** product

**Overview (KR):** 리포지토리의 자동화와 지능형 보조를 위한 AI Agent 운영 프레임워크의 요구사항을 정의합니다.

## Product Context

The project requires a consistent way to interact with AI agents across different providers (Claude, Gemini) while maintaining repository standards and reducing context bloat.

## User Stories

- As a developer, I want to load only the relevant rules for my task to keep the context window clean.
- As a maintainer, I want to ensure agents follow a specific "Discover -> Plan -> Execute" workflow.

## Functional Requirements

- `[REQ-PRD-AGT-FUN-01]` Lazy-loading of rule modules via `[LOAD:RULES:*]` triggers.
- `[REQ-PRD-AGT-FUN-02]` Centralized instruction hub in `docs/agentic/`.
- `[REQ-PRD-AGT-FUN-03]` Support for plural implementation paths (`plans/`, `specs/`).

## Non-Functional Requirements

- `[REQ-PRD-NFR-01]` Gateway file must be under 100 lines for fast loading.
