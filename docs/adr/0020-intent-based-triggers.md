---
title: 'ADR 0002: Intent-Based Rule Triggers and Lazy Loading'
status: 'Accepted'
date: '2026-03-15'
authors: ['buenhyden']
deciders: ['buenhyden']
tags: ['adr', 'agentic', 'rules']
layer: 'architecture'
---

# ADR 0020: Intent-Based Rule Triggers and Lazy Loading

- **Status:** Accepted
- **Date:** 2026-03-15
- **Scope:** master
- **layer:** architecture

**Overview (KR):** AI Agent가 작업 의도(Intent)에 따라 필요한 지침만 선택적으로 로드할 수 있도록 `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`에 명시적인 규칙 트리거를 정의합니다.

## Context

The current `AGENTS.md` and related files mandate loading the gateway but do not provide specific triggers for individual rule sets. This requires the agent to manually navigate the gateway every time.

## Decision

We will implement explicit **Intent-Based Rule Triggers** in the root agent files.

- Each root file (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) will contain a "Rule Matrix" or "Lazy Loading Map".
- Triggers will use the format `[LOAD:RULES:<CATEGORY>]`.
- Agents must identify their task category and load the corresponding rule from `docs/agentic/rules/`.

## Consequences

- **Positive**: More direct and efficient instruction loading, reduced ambiguity for the agent.
- **Negative**: Redundancy across root files if not managed carefully (shared via `docs/agentic/gateway.md`).

## Related

- `[../prd/rule-implementation-prd.md]`
- `[../specs/2026-03-15-rule-refactor-spec.md]`
