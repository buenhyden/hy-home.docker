---
layer: agentic
---
# Spec: Cycle 2 Documentation & Agent Optimization
n**Overview (KR):** 문서 강화 2단계 과업의 범위와 기술적 달성 목표를 설명하는 명세입니다.

- **Status**: Review
- **layer:** architecture
- **Related PRD**: `[../prd/refactor-cycle-2-prd.md]`

**Overview (KR):** 리포지토리의 루트 파일들과 AI Agent 운영 지침을 통합하기 위한 기술적 구현 가이드입니다.

## 1. Root Shim Refactoring

`AGENTS.md`, `CLAUDE.md`, `GEMINI.md` must be standardized to:

- Max 15-20 lines.
- No behavioral rules (only pointers).
- Mandatory `[LOAD:RULES:*]` triggers.

## 2. Directory Consolidation

- **Cleanup**: Move all contents from `docs/plans/plan_tmp/` to `docs/plans/`.
- **Naming**: Ensure all file names follow the `YYYY-MM-DD-feature-type.md` pattern where applicable.

## 3. Instruction Merging

Move detailed snippets from `.agent/rules/` into `docs/agentic/instructions.md` if they pertain to general agent behavior.

## 4. Metadata Verification Protocol

Every execution step MUST verify the presence of `layer:` before completing the file write.
