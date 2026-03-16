---
layer: agentic
---
# Agentic Platform Architecture Reference Document (ARD)

- **Status**: Approved
- **Owner**: buenhyden
- **Scope**: master
- **layer:** agentic
- **PRD Reference**: `[../prd/refactor-prd.md]`

**Overview (KR):** 리포지토리의 AI Agent 운영 방침과 규칙 로딩 아키텍처를 정의합니다.

## Summary

The Agentic layer is a meta-layer that manages how AI assistants interact with the codebase. It implements a decoupled, rule-based approach to minimize session noise.

## Boundaries

- **Owns**: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` shims, and `docs/agentic/` instructions.
- **Consumes**: Project metadata and global architecture rules (`ARCHITECTURE.md`).
- **Does Not Own**: Infrastructure configuration or application logic.

## Ownership

- **Primary owner**: buenhyden
- **Primary artifacts**: `[docs/agentic/]`, `[AGENTS.md]`

## 1. Architecture Decisions

### 1.1 Intent-Based Discovery

Agents are not given a monolithic prompt. Instead, they use `[LOAD:RULES:<CATEGORY>]` triggers to pull in specific instructions.

### 1.2 Path Invariants

All implementation plans reside in `docs/plans/`. All technical specifications reside in `docs/specs/`. No exceptions.

## 2. Source-of-Truth Map

| Scope   | Canonical Document                            | Role                             |
| ------- | --------------------------------------------- | -------------------------------- |
| master  | `docs/ard/agentic-ard.md`                     | Layer authority                  |
| domain  | `docs/agentic/gateway.md`                     | Operational entrypoint           |
| feature | `docs/specs/refactor-spec.md`                 | Implementation detail            |
