# ADR 0001: Standardized Documentation Taxonomy

- **Status:** Accepted
- **Date:** 2026-03-15
- **Scope:** master
- **layer:** architecture
- **Authors:** buenhyden

**Overview (KR):** 리포지토리의 문서 구조를 일관되게 유지하기 위해 평탄화된 계층 구조와 명확한 폴더 명명 규칙을 적용하기로 결정했습니다.

## Context

The repository had inconsistent path naming (singular vs plural) and nested structures that made discovery difficult for AI agents. A standardized, flat taxonomy is needed for efficient lazy-loading.

## Decision

- Apply a flat directory structure under `docs/`.
- Use singular names for authority docs: `adr`, `ard`, `prd`.
- Use plural names for implementation/operational docs: `plans`, `specs`, `runbooks`.
- Mandatory `layer:` metadata in all Markdown files.

## Consequences

- Improved agent performance through predictable pathing.
- Easier maintenance of index files.
- Consistency between root shims and detailed guides.

## Related

- `[../specs/infra-spec.md]`
- `[../ard/infra-baseline-ard.md]`
- `[../plans/2026-03-15-doc-refactor.md]`
