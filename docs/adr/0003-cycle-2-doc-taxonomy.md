# ADR 0003: Strict Enforcement of Plural Execution Paths

- **Status:** Accepted
- **Date:** 2026-03-15
- **layer:** architecture
- **Reference ARD**: `[../ard/agentic-framework-cycle-2-ard.md]`

**Overview (KR):** 문서 탐색의 일관성을 위해 모든 실행 관련 문서(plans, specs, runbooks)의 경로를 반드시 복수형으로 유지하고, 단수 경로를 영구적으로 제거합니다.

## Context

Previous attempts at standardization left some "singular" relics and internal links. AI agents occasionally hallucinate `docs/plan/` causing session failures.

## Decision

1. **Hard Removal**: Delete all legacy `docs/plan_tmp/` and consolidate contents.
2. **Path Mapping**:
   - `docs/plans/`
   - `docs/specs/`
   - `docs/runbooks/`
3. **Internal Routing**: `docs/agentic/gateway.md` must be the exclusive source of truth for loading these families.

## Consequences

- **Positive**: Eliminates routing ambiguity for agents.
- **Maintenance**: Requires periodic link audits using `grep`.
