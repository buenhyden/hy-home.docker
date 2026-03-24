---
title: '2026-03 Documentation Refactor Specification'
status: 'Accepted'
layer: 'documentation'
---

# 2026-03 Documentation Refactor Specification

**Overview (KR):** 본 문서는 문서 리팩토링의 기술적 사양을 정의합니다. 파일 이동 규칙, 메타데이터 표준, 에이전트 트리거 구현 방식을 상세히 설명합니다.

## 1. Directory Mapping

| Type | Destination Path |
| --- | --- |
| ADR | `docs/adr/` |
| ARD | `docs/ard/` |
| PRD | `docs/prd/` |
| Spec | `docs/specs/` |
| Plan | `docs/plans/` |
| Runbook | `docs/runbooks/` |
| Incident | `docs/operations/incidents/` |
| Postmortem | `docs/operations/postmortems/` |

## 2. Metadata Specification

All files must start with:

```yaml
---
layer: <layer_name>
---
```

Allowed values for `layer`: `entry | core | ops | agentic | meta | common | architecture | backend | frontend | infra | mobile | product | qa | security`.

## 3. Agent Trigger Implementation

Entrypoints (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) will implement the follow pattern:

```markdown
Identify your task and load the required rule module:
- **CATEGORY**: `[LOAD:RULES:<CATEGORY>]`
```

Targeting categories: `REFACTOR`, `DOCS`, `INFRA`, `OPS`.
