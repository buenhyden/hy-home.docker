---
title: 'Postmortem: Rule Discovery Latency'
status: 'Completed'
date: '2026-03-15'
incident_reference: './incidents/2026-03-15-rule-trigger-integration.md'
owner: 'buenhyden'
tags: ['postmortem', 'rules']
layer: 'ops'
---

# Postmortem: Rule Discovery Latency

**Overview (KR):** 에이전트가 올바른 지침을 찾는 데 걸리는 시간(Latency)과 부정확한 컨텍스트 로딩으로 인한 비효율을 분석하고, 루트 트리거 도입을 통한 해결 방안을 정리한 보고서입니다.

## timeline

- **Issue**: Session start required manual gateway navigation.
- **Fix**: Direct triggers implemented in root files.
- **Verification**: Agents now correctly identify `[LOAD:RULES:REFACTOR]` for refactoring tasks.

## Lessons Learned

- Root files are the first thing an agent sees; they must contain actionable triggers.

## Action Items

- [x] Standardize rule triggers across all agent entrypoints.
- [x] Remove tool use restrictions from behavioral instructions.
