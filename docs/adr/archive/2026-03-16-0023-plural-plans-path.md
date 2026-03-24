---
title: 'ADR 0023: Adoption of Plural plans Path'
status: 'Accepted'
date: '2026-03-16'
layer: architecture
---

# ADR 0023: Adoption of Plural plans Path

**Overview (KR):** 문서 트리 구조의 일관성을 위해 단수형인 `plan` 대신 복수형인 `plans` 경로를 표준으로 채택하고 모든 참조를 업데이트합니다.

## Context

To maintain consistency with other plural category roots like `specs`, `runbooks`, and `rules`, the repository will standardize on `docs/plans/`.

## Decision

Standardize on `docs/plans/` for all implementation plans and update all internal references.

## Consequences

- **Positive**: Consistency across the documentation root using plural nouns.
- **Negative**: Requires careful link maintenance during updates.
