---
title: 'Final Documentation Path Alignment'
status: 'Canonical'
scope: 'master'
layer: 'product'
related_prd: '../prd/rule-implementation-prd.md'
---

# Final Documentation Path Alignment Specification

**Overview (KR):** 본 명세서는 저장소의 모든 관리 문서와 지침 파일이 사용자 요구사항에 명시된 최종 경로 표준(`docs/plans/`, `docs/operations/incidents/` 등)을 완벽히 충실히 준수하도록 보장합니다.

## Path Standards

| Type | Path |
| :--- | :--- |
| ADR | `docs/adr/` |
| ARD | `docs/ard/` |
| Incident | `docs/operations/incidents/` |
| Postmortem | `docs/operations/postmortems/` |
| Plan | `docs/plans/` |
| Spec | `docs/specs/` |
| PRD | `docs/prd/` |
| Runbook | `docs/runbooks/` |

## Constraint Verification

- `docs/plans/` is strictly forbidden.
- All files must contain `layer:` metadata.
- Links between documents must be relative.
