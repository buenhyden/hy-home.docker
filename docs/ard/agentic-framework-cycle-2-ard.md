---
layer: agentic
---
# Agentic Framework Architecture (Cycle 2)

- **Status**: Implementation
- **Owner**: buenhyden
- **Scope**: master
- **layer:** agentic
- **Reference PRD**: `[../prd/refactor-cycle-2-prd.md]`

**Overview (KR):** AI Agent의 효율적인 리소스 로딩과 무제한 스킬 활용을 위한 아키텍처 데시전을 정의합니다.

## 1. Discovery Gateway Protocol

Agent entrypoints act as shims. Content discovery happens through:

1. **Trigger Phase**: Agent detects task category and loads `[LOAD:RULES:<TICKER>]`.
2. **Expansion Phase**: Gateway map in `docs/agentic/gateway.md` points to specific instruction sets.

## 2. Skill Autonomy Invariant

- **Policy**: No skill is restricted logically.
- **Enforcement**: Behavioral instructions MUST NOT contain negative constraints on tool usage (e.g., "don't use browser").

## 3. Path Standards

Authority = Singular; Execution = Plural.

- Correct: `docs/adr/`, `docs/plans/`.
- Incorrect: `docs/adrs/`, `docs/plan/`.

## Related

- [../adr/README.md]
- [../prd/README.md]
