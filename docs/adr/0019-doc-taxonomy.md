---
layer: agentic
---
# ADR 0019: Document Taxonomy and Pluralization Standards

- **Status:** Accepted
- **Date:** 2026-03-15
- **Scope:** master
- **layer:** architecture
- **Authors:** buenhyden

**Overview (KR):** 문서 분류체계의 일관성을 확보하기 위해 권위 있는 문서는 단수(adr, ard, prd), 실행 문서는 복수(plans, specs, runbooks) 폴더명을 사용하도록 결정했습니다.

## Context

Initial setup had mixed singular (`plan`, `spec`) and plural directory names. This caused routing errors for agents and confusion for maintainers.

## Decision

1. **Directories**:
   - Authority: `docs/adr/`, `docs/ard/`, `docs/prd/`
   - Implementation/Ops: `docs/plans/`, `docs/specs/`, `docs/runbooks/`, `docs/operations/`
2. **Metadata**: Every file MUST contain `layer` in YAML frontmatter.
3. **Links**: Use relative paths exclusively.

## Consequences

- **Positive**: Predictable pathing for automated audits.
- **Limitation**: Requires a one-time migration of all existing internal links.

## Related

- `[../prd/refactor-prd.md]`
- `[../ard/agentic-ard.md]`
