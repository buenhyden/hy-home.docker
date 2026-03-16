---
title: 'ADR-0026: Documentation Structure and Lazy Loading'
status: 'Accepted'
date: '2026-03-16'
authors: ['Antigravity']
deciders: ['buenhyden']
tags: ['adr', 'documentation', 'lazy-loading']
layer: 'common'
---

# ADR-1001: Documentation Structure and Lazy Loading

- **Status:** Accepted
- **Date:** 2026-03-16
- **Scope:** master
- **layer:** common

**Overview (KR):** 에이전트 지침의 토큰 과다 사용 문제를 해결하기 위해 지침을 모듈화하고 상황에 따라 필요한 지침만 로드하는 Lazy Loading 방식을 도입하며, 문서 구조를 사용자 요구에 맞춰 재정리하기로 결정함.

## Context

The repository has accumulated a large set of AI agent instructions (~39.0k tokens), impacting performance. Additionally, there is a need to standardize the categorization and location of technical documents to match specific organizational paths (e.g., `docs/plans/` instead of `docs/plans/`).

## Decision

- **[DEC-001]** Rename `docs/plans/` to `docs/plans/` to align with the single-noun naming convention for core categories.
- **[DEC-002]** Implement a "Gateway Hub" in `docs/agentic/gateway.md`.
- **[DEC-003]** All specialized rules in `docs/agentic/rules/` will be loaded ONLY when triggered by markers (`[LOAD:RULES:...]`).
- **[DEC-004]** Promoted `CONTRIBUTING.md` and `COLLABORATING.md` to the root directory for standard discovery.

## Consequences

- **Positive**: Improved AI performance (lower latency, better instruction following), clearer document hierarchy.
- **Trade-off**: Agents need to perform an extra discovery step at the start of a session.

## Related

- `../specs/2026-03-16-documentation-refactor-spec.md`
- `../ard/documentation-system-ard.md`
- `../prd/2026-03-16-documentation-standardization-prd.md`
