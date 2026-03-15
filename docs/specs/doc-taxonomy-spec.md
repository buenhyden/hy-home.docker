# Documentation Taxonomy Specification

- **Status**: Implementation
- **Scope**: master
- **layer:** architecture
- **Related PRD**: `[../prd/agentic-prd.md]`
- **Related Architecture**: `[../ard/agentic-ard.md]`

**Overview (KR):** 평탄화된 문서 구조를 구현하기 위한 기술적 명세와 파일 처리 규칙을 정의합니다.

## Technical Baseline

The system relies on a flat directory hierarchy where each subdirectory of `docs/` represents a specific document type.

## Contracts

- **Metadata Contract**: Every Markdown file must have a YAML frontmatter with the `layer` key.
- **Routing Contract**: `AGENTS.md` and `CLAUDE.md`/`GEMINI.md` must point to `docs/agentic/gateway.md`.

## Verification

```bash
# Verify layer metadata
grep -r "layer:" docs/
```
