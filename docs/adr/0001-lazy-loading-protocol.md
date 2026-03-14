---
title: 'ADR 0001: Lazy-Loading Protocol for AI Agents'
status: 'Accepted'
date: '2026-03-15'
authors: ['buenhyden']
deciders: ['buenhyden']
tags: ['adr', 'agentic', 'context']
layer: 'architecture'
---

# ADR 0001: Lazy-Loading Protocol for AI Agents

- **Status:** Accepted
- **Date:** 2026-03-15
- **Scope:** master
- **layer:** architecture

**Overview (KR):** AI Agent가 세션 시작 시 모든 지침을 로드하는 대신, 현재 작업의 의도(Intent)에 따라 필요한 규칙만 선택적으로 로드하는 프로토콜을 도입하여 토큰 효율성을 높이고 컨텍스트 오염을 방지합니다.

## Context

As the repository grows, the number of agent instructions and documentation files increases. Loading all files at once leads to:

1. High token consumption.
2. Context window saturation.
3. "Garbage in, garbage out" due to irrelevant instructions interfering with the task.

## Decision

We will implement a **Lazy-Loading Protocol** anchored in `docs/agentic/gateway.md`.

- Root-level agent files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) will contain minimal information and a mandate to load the gateway first.
- The gateway will categorize documents by type and intent.
- Agents must look up their "Intent" in the gateway and load only the mapped rule file.

## Consequences

- **Positive**: Reduced start-up latency for agents, higher precision in task execution, lower token costs.
- **Negative**: Adds one extra step (loading gateway) at the start of every session.

## Related

- `[../prd/doc-refactor-prd.md]`
- `[../specs/2026-03-15-doc-refactor-spec.md]`
