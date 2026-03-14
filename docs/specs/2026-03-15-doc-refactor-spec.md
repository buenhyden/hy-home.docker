# Documentation and Agent Refactor Specification

> **Status**: Canonical
> **Scope**: master
> **layer:** product
> **Related PRD**: `[../prd/doc-refactor-prd.md]`
> **Related Architecture**: `[../ard/doc-refactor-ard.md]`
> **Decision Record**: `[../adr/0001-lazy-loading-protocol.md]`

**Overview (KR):** 본 명세서는 문서 리팩토링의 상세 구현 방안을 정의합니다. YAML Frontmatter 표준, 문서 경로 규칙, Agent Gateway의 지침 로드 방식을 규정합니다.

## Technical Baseline

The repository uses Markdown for all documentation. Agent instructions are loaded via filesystem reads.

## Contracts

- **Metadata Contract**: Every `.md` file MUST start with a YAML frontmatter containing `layer: <layer_name>`.
- **Path Contract**:
  - ADR: `docs/adr/`
  - ARD: `docs/ard/`
  - Spec: `docs/specs/`
  - Plan: `docs/plans/`
  - PRD: `docs/prd/`
  - Runbook: `docs/runbooks/`
  - Incident: `docs/operations/incidents/`
  - Postmortem: `docs/operations/postmortems/`
- **Gateway Contract**: `docs/agentic/gateway.md` must be the first file loaded. It must contain the section `## Intent-Based Discovery`.

## Component Breakdown

- **`ARCHITECTURE.md`**: Update links to `docs/` subdirectories.
- **`OPERATIONS.md`**: Update links to `docs/operations/incidents/` and `docs/operations/postmortems/`.
- **`docs/agentic/gateway.md`**: Update to include the new path contract and clearer lazy-loading triggers.
- **`docs/agentic/instructions.md`**: Explicitly state that agents have full skill autonomy and should use them purpose-fitly.

## Verification

```bash
# Check layers
head -n 5 *.md docs/**/*.md | grep "layer:"
# Check links
rg "\]\(" docs/**/*.md | grep -v "http"
```
