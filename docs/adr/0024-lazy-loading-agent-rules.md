---
title: 'ADR 0024: Lazy-Loading Agent Rules'
status: 'Proposed'
date: '2026-03-14'
owner: 'Antigravity'
layer: architecture
---

# ADR 0024: Lazy-Loading Agent Rules

**Overview (KR):** 에이전트가 작업 의도에 맞는 규칙만 동적으로 로드하게 하여 토큰 사용량을 줄이고 정확도를 높이는 지연 로딩 프로토콜을 도입합니다.

## Context

As the repository grows, the "Agents Instruction" (`AGENTS.md`) and the gateway have become congested. Agents load too much context that is irrelevant to their specific task, causing higher token costs and potential confusion (hallucinations).

## Decision

We will implement an "Intent-Based Lazy Loading" protocol.

1. `AGENTS.md` remains the thin entrypoint.
2. `docs/agentic/gateway.md` serves as the map.
3. Every major task type (Refactoring, Deploying, Debugging) will have a dedicated "Rule" file in `docs/agentic/rules/`.
4. Agents must load only the rule corresponding to their current task intent.

## Consequences

- **Positive**: Reduced context overhead, higher precision in task execution, easier maintenance of task-specific rules.
- **Negative**: Adds 1-2 steps to the agent's startup sequence.
