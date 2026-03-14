---
title: 'Postmortem: Documentation Structure Mismatch'
status: 'Completed'
date: '2026-03-15'
incident_reference: './incidents/2026-03-15-doc-struct-mismatch.md'
owner: 'buenhyden'
tags: ['postmortem', 'documentation']
layer: 'ops'
---

# Postmortem: Documentation Structure Mismatch

**Overview (KR):** 문서 구조 및 지침 로딩 방식의 한계로 인해 발생한 비효율성을 분석하고, 리팩토링을 통한 개선 결과와 향후 재발 방지 대책을 정리한 사후 분석 보고서입니다.

## Timeline

- **Discovery**: Agents reported high token usage and context noise.
- **Analysis**: identified decentralized docs without a central gateway.
- **Resolution**: Implemented flat taxonomy and Lazy-Loading protocol.

## Root Cause

The repository lacked a formal metadata-driven discovery protocol for AI agents, leading to monolithic context loading.

## Lessons Learned

- Always implement a gateway for agent-intensive repositories.
- Keep documentation taxonomy flat for easier relative linking.

## Action Items

- [x] Standardize YAML frontmatter with `layer:` key.
- [x] Implement `docs/agentic/gateway.md`.
- [x] Move all implementation plans to `docs/plans/`.
