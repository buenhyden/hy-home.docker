---
title: 'ADR 0003: March 2026 Agentic Standard Adoption'
status: 'Accepted'
date: '2026-03-15'
authors: ['buenhyden']
deciders: ['buenhyden']
tags: ['adr', 'agentic', 'standards']
layer: 'architecture'
---

# ADR 0021: March 2026 Agentic Standard Adoption

- **Status:** Accepted
- **Date:** 2026-03-15
- **layer:** architecture

**Overview (KR):** 2026년 3월 기준의 최신 AI Agent 상호작용 표준을 저장소에 도입하기로 결정했습니다. 이는 명시적인 의도 기반 로딩(Intent-based Loading)과 추론 전용 페르소나(Reasoner Persona)의 우선 활용을 골자로 합니다.

## Context

Current agent instructions are becoming dense. To maintain performance and reduce hallucination, we need a lighter, trigger-based system that allows agents to pull context only when necessary.

## Decision

We will implement the **2026-03 Agentic Standard**:

1. **Direct Root Triggers**: `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` will contain the primary discovery markers (`[LOAD:RULES:*]`).
2. **Persona Prioritization**: `GEMINI.md` will explicitly mandate the "Reasoner" persona for complex infrastructure tasks.
3. **Skill Autonomy Policy**: Remove all specific tool restrictions to allow agents to pick the most efficient tool dynamically.
4. **Flat Taxonomy**: Enforce `docs/<category>/` structure without deep nesting.

## Consequences

- **Positive**: Enhanced agent efficiency, reduced context window bloat, cleaner root documentation.
- **Negative**: Requires discipline from human contributors to update triggers when adding new rules.
