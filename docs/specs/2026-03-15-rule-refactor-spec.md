---
layer: agentic
---
# Agent Rule Implementation and Refactor Specification

**Overview (KR):** 에이전트 전용 규칙(Rules)의 구조를 리팩토링하고 신규 트리거를 적용하는 명세입니다.

> **Status**: Canonical
> **Scope**: master
> **layer:** product
> **Related PRD**: `[../prd/2026-03-15-rule-implementation-prd.md]`
> **Related Architecture**: `[../ard/2026-03-15-doc-taxonomy-ard.md]`
> **Decision Record**: `[../adr/0020-intent-based-triggers.md]`

**Overview (KR):** 본 명세서는 루트 파일에서 지침을 직접 로드하기 위한 구체적인 트리거 형식과 `docs/agentic/`의 디렉토리 구조를 확정합니다.

## Technical Baseline

Root files act as the initial prompt context for AI agents. By placing explicit markers here, we hook into the agent's pre-task analysis phase.

## Contracts

- **Trigger Contract**: Markers must be nested in a Markdown table under a `## Rules` or `## Intent-Based Selection` header.
- **Path Contract (Strict)**:
  - No `docs/plans/`; use `docs/plans/`.
  - No nested `docs/operations/postmortems/subdir/`; keep it flat.
- **Skill Contract**: Agents MUST be notified that "Full Skill Autonomy" is granted.

## Component Breakdown

### Root Files

- **`AGENTS.md`**: Update with `[LOAD:RULES:REFACTOR]`, `[LOAD:RULES:DOCS]`, etc.
- **`GEMINI.md`**: Update with instructions to prioritize Reasoner persona and rule triggers.

### Agentic Subsystem

- **`docs/agentic/instructions.md`**: Finalize as the shared "Behavioral Standard" imported by all rules.
- **`docs/agentic/rules/refactor-rule.md`**: Refine for strict metadata and path checking.

## Verification

```bash
## Verify no 'plans' directory exists
ls docs/plans && exit 1 || echo "Success: 'plan' path in use"
## Verify root triggers
grep "\[LOAD:RULES:" AGENTS.md GEMINI.md
```
