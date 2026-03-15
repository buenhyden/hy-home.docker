# Agentic Platform Architecture Reference Document

- **Status**: Approved
- **Owner**: buenhyden
- **Scope**: master
- **layer:** agentic
- **PRD Reference**: `[../prd/agentic-prd.md]`
- **ADR References**: `[../adr/0001-doc-taxonomy.md]`

**Overview (KR):** AI Agent가 리포지토리의 규칙과 도구를 효과적으로 사용할 수 있도록 하는 지능형 컨텍스트 관리 시스템의 설계를 정의합니다.

## Summary

The Agentic platform provides a rule-based gateway for AI agents to discover project context, apply purpose-fit skills, and execute infrastructure changes safely.

## Boundaries

- **Owns**: AI instruction loading, intent-based rule routing, persona definitions.
- **Consumes**: Repository metadata, tool toolkit, workspace file structure.
- **Does Not Own**: Actual Docker infrastructure implementation (owned by `infra` ARD).

## Ownership

- **Primary owner**: buenhyden
- **Primary artifacts**: `[docs/agentic/]`, `[AGENTS.md]`
- **Operational evidence**: `N/A`

## Related

- `[../prd/agentic-prd.md]`
- `[../specs/agent-gateway-spec.md]`
- `[../adr/0001-doc-taxonomy.md]`
