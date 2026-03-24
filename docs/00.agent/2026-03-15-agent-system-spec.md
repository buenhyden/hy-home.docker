---
title: 'Agent Instruction Refactor Specification'
status: 'Implementation'
version: '1.0'
owner: 'buenhyden'
scope: 'domain'
prd_reference: 'N/A'
arch_reference: 'N/A'
tags: ['spec', 'documentation', 'agents']
layer: agentic
---

# Agent Instruction Refactor Specification

> **Status**: Implementation
> **Scope**: domain
> **Parent Master Spec**: N/A
> **Related PRD**: N/A (documentation maintenance task)
> **Related Architecture**: N/A (documentation maintenance task)
> **Decision Record**: N/A

**Overview (KR):** 이 명세는 루트 에이전트 지침 파일과 관련 인덱스 문서를 2026년 3월 기준 최신 provider 가이드와 저장소 실태에 맞게 재편하는 계약을 정의한다. 주요 위험은 오래된 템플릿 경로, 절대 링크, 불완전한 lazy-loading 구조를 남겨 에이전트가 잘못된 문서를 우선 참조하는 것이다.

## Technical or Platform Baseline

The repository currently exposes three root instruction files: `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`. It also relies on `docs/agentic/*.md` and `docs/*/README.md` as linked context. The current documents are partially refactored but still too thin at the root, too generic in `docs/agentic/`, and inconsistent across documentation indexes.

## Contracts

- **Governance Contract**: `AGENTS.md` remains the canonical root entrypoint for universal agent rules, but it must only contain rules that apply to every task.
- **Provider Contract**: `CLAUDE.md` and `GEMINI.md` retain only provider-specific execution or reasoning behavior, with `CLAUDE.md` using `@` imports.
- **Shared Documentation Contract**: Common guidance lives in `docs/agentic/` and is linked or imported from the root files using relative paths only.
- **Truth Contract**: No instruction file may reference unavailable tools, imaginary artifacts, or unsupported repository paths.
- **Maintenance Contract**: The refactor must keep the repository-local spec and plan current and include documentation-only verification steps.

## Verification

```bash
rg -n "^@" CLAUDE.md
rg -n 'file://|docs/templates/(architecture|product|operations)/|\]\(/specs/' AGENTS.md CLAUDE.md GEMINI.md .claude docs
test -f docs/plans/2026-03-12-agent-instruction-refactor.md
test -f docs/specs/agent-instructions/spec.md
test -f docs/agentic/README.md
test -f docs/plans/README.md
```

## 1. Technical Overview & Architecture Style

This is a documentation-only refactor. The target architecture is a progressive-disclosure model:

- `AGENTS.md` is the cross-agent canonical entrypoint.
- Shared operational details live in `docs/agentic/*.md`.
- Provider-specific files remain focused on the differences that matter during execution.
- `docs/*/README.md` files act as stable lazy-loading indexes for the documentation families.

- **Component Boundary**: Root agent entrypoints, shared `docs/agentic/*.md` guidance, and documentation-family README indexes under `docs/`.
- **Key Dependencies**: `docs/README.md`, `docs/templates/spec-template.md`, `docs/templates/plan-template.md`, `.agent/rules/0000-Agents/`, `.agent/rules/2100-Documentation/`
- **Tech Stack**: Markdown, relative links, shell validation with `rg` and `test`

## 2. Coded Requirements (Traceability)

| ID | Requirement Description | Priority | Parent PRD REQ |
| -- | ----------------------- | -------- | -------------- |
| **[REQ-SPC-ADN-001]** | The three root files must become concise entrypoints rather than long-form policy stores. | High | N/A |
| **[REQ-SPC-ADN-002]** | Shared policy must live in repository-local guidance under `docs/agentic/`. | High | N/A |
| **[REQ-SPC-ADN-003]** | All new and updated links must be relative and resolve to existing files. | Critical | N/A |
| **[REQ-SPC-ADN-004]** | Stale references to unavailable tools and artifacts must be removed. | Critical | N/A |
| **[REQ-SPC-ADN-005]** | Documentation indexes must expose ADR, ARD, PRD, specs, plans, runbooks, operations history, and incidents as lazy-loadable entrypoints. | High | N/A |
| **[REQ-SPC-ADN-006]** | `CLAUDE.md` must use provider-native `@` imports instead of duplicating shared guidance. | High | N/A |

## 3. Data Modeling & Storage Strategy

- **Database Engine**: None
- **Schema Strategy**: Markdown-only documentation split between root entrypoints and guide documents
- **Migration Plan**: Rewrite the roots in place, rebuild `docs/agentic/*.md` around repo-specific guidance, repair linked docs indexes, and add a plans index without changing product code

## 4. Interfaces & Data Structures

### 4.1 Core Interfaces

```typescript
type ProviderRoot = "AGENTS.md" | "CLAUDE.md" | "GEMINI.md";

interface InstructionGuideLink {
  source: ProviderRoot;
  target: string;
  purpose: "governance" | "workflow" | "provider-specific";
}
```

## 5. Component Breakdown

- `AGENTS.md`: Minimal universal policy and rule-map entrypoint
- `CLAUDE.md`: Claude-specific shim using `@` imports
- `GEMINI.md`: Gemini-specific shim with provider notes and shared references
- `docs/agentic/README.md`: Shared guidance index
- `docs/agentic/core-governance.md`: Repo-specific governance, personas, and lazy-loading policy
- `docs/agentic/workflow.md`: Repo-specific execution workflow and validation commands
- `docs/README.md`: Canonical docs lazy-loading gateway
- `docs/plans/README.md`: Tactical plans index
- `docs/plans/2026-03-12-agent-instruction-refactor.md`: Execution plan for this refactor

## 6. Domain-Specific Contract Sections

### Anti-Patterns

- Root files duplicating the same guidance
- References to tools that do not exist in the active runtime
- Absolute file-system links inside repository documentation
- Provider files restating generic repository governance instead of linking to it

## 7. Edge Cases & Error Handling

- **Missing shared guide path**: If the required `docs/agentic/` guide files are missing, root files must not be updated to link or import non-existent targets.
- **Index drift**: If a doc family has content but no stable README/index, add or repair the index before relying on that family in lazy-loading guidance.
- **Dirty worktree overlap**: If unrelated user edits touch the same files, preserve their intent and layer the refactor around the current content rather than reverting.

## 8. Verification Plan (Testing & QA)

- **[VAL-SPC-AGT-001] Structural review**: Confirm each root file reads as an entrypoint, not a full handbook.
- **[VAL-SPC-AGT-002] Link review**: Validate all new relative links with targeted `rg` and `test` commands.
- **[VAL-SPC-AGT-003] Truth review**: Manually inspect the roots and shared guides to confirm deprecated runtime-specific instructions no longer appear.
- **[VAL-SPC-AGT-004] Provider review**: Confirm `CLAUDE.md` imports and `GEMINI.md` link semantics match the chosen provider models.
- **[VAL-SPC-AGT-005] Evidence capture**: Record command results after edits before declaring completion.

## 9. Non-Functional Requirements (NFR) & Scalability

- **Performance / Latency**: No runtime behavior change
- **Throughput**: N/A
- **Scalability Strategy**: The guide bundle must support additional provider-specific roots without repeating shared policy

## 10. Operations & Observability

- **Deployment Strategy**: Documentation-only change merged through normal repository workflow
- **Monitoring & Alerts**: N/A
- **Logging**: Verification is captured through command output during the refactor
- **Sensitive Data Handling**: No secrets or environment values may be introduced into the new documents
