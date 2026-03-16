---
title: 'ADR 0025: Intent-Based Lazy Loading for Agent Rules'
status: 'Accepted'
date: '2026-03-14'
authors: ['buenhyden']
deciders: ['buenhyden']
tags: ['adr', 'agentic', 'lazy-loading']
layer: agentic
---

# ADR 0025: Intent-Based Lazy Loading for Agent Rules

- **Status:** Accepted
- **Date:** 2026-03-14
- **Scope:** master
- **layer:** architecture
- **Authors:** buenhyden
- **Deciders:** buenhyden

**Overview (KR):** 초기에 모든 규칙을 로드하는 대신, AI 에이전트가 수행하려는 작업의 의도(Intent)에 따라 필요한 규칙 파일만 동적으로 로드하는 방식을 도입하여 효율성을 높입니다.

## Context

Prior to this decision, AI agents were often loaded with the entire `AGENTS.md` and monolithic instruction sets, leading to high token usage and increased risk of "Lost in the Middle" syndrome. Fragmentation across root docs and `docs/` made it difficult to find the authoritative rule for a specific task.

## Decision

- **Implement a Gateway-driven loading protocol**: Agents MUST load `docs/agentic/gateway.md` first.
- **Modularize Rules**: Break down large rule sets into granular files under `docs/agentic/rules/`.
- **Use Intent Markers**: Map categories of work to specific rule files using `[LOAD:RULES:<CATEGORY>]` markers.
- **Thin Root Shims**: Reduce `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` to minimal pointers.

## Consequences

- **Positive**: Reduced token consumption, improved precision of agent actions, clearer ownership of rules.
- **Trade-off**: Agents must perform one extra step (loading the gateway) at the start of a session.

## Related

- `[../specs/2026-03-15-agent-rule-lazy-loading-spec.md]`
- `[../ard/2026-03-15-doc-taxonomy-ard.md]`
- `[./0024-lazy-loading-agent-rules.md]` (Reference to earlier concepts)
