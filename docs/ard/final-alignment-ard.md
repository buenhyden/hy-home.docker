---
title: 'ARD: Final Path and Agentic Architecture Alignment'
status: 'Approved'
layer: 'architecture'
prd_reference: '../prd/final-alignment-prd.md'
---

# ARD: Final Path and Agentic Architecture Alignment

**Overview (KR):** 최종 문서 계층 구조와 에이전트 상호작용 레이어를 확정합니다.

## Architecture

```mermaid
graph TD
    Root[Root Files] -->|Direct Triggers| Rules[docs/agentic/rules/*.md]
    Root -->|Gateway| Gateway[docs/agentic/gateway.md]
    Documentation[docs/] -->|Path Standard| Plans[plans/]
    Documentation -->|Path Standard| Operations[operations/incidents/, operations/postmortems/]
```

## Standards

- **Plurality**: Plans are stored in `plans/`.
- **Metadata**: `layer` key is mandatory in frontmatter.
- **Autonomy**: High-trust model for agent skill usage.
