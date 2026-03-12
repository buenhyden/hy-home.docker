---
title: 'Agent Instruction Refactor Specification'
status: 'Validated'
version: '1.0'
owner: 'buenhyden'
scope: 'domain'
prd_reference: 'N/A'
arch_reference: 'N/A'
tags: ['spec', 'documentation', 'agents']
---

# Agent Instruction Refactor Specification

> **Status**: Validated
> **Scope**: domain
> **Parent Master Spec**: N/A
> **Related PRD**: N/A (documentation maintenance task)
> **Related Architecture**: N/A (documentation maintenance task)
> **Decision Record**: N/A

**Overview (KR):** 이 명세는 루트 에이전트 지침 파일을 점진적 공개 구조로 재편하되, 공통 정책은 `.claude/agent-instructions/`로 이동하고 공급자별 차이만 루트에 남기기 위한 기준을 정의한다. 주요 위험은 잘못된 공유 지침 위치를 유지해 에이전트가 기대한 탐색 경로를 따르지 못하게 만드는 것이다.

## Technical or Platform Baseline

The repository currently exposes three root instruction files: `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`. Those files already contain useful governance, reasoning, and execution rules, but they mix universal guidance with provider-specific details and reference tools or artifacts that are not guaranteed to exist in the current runtime.

## Contracts

- **Governance Contract**: `AGENTS.md` remains the canonical root entrypoint for universal agent rules, but it must only contain rules that apply to every task.
- **Provider Contract**: `CLAUDE.md` and `GEMINI.md` retain only provider-specific execution or reasoning behavior.
- **Shared Documentation Contract**: Common guidance moves into `.claude/agent-instructions/` and is linked from the root files using relative paths only.
- **Truth Contract**: No instruction file may reference unavailable tools, imaginary artifacts, or unsupported repository paths.
- **Maintenance Contract**: The refactor must create a repository-local spec and plan and include documentation-only verification steps.

## Verification

```bash
rg -n "\\.claude/agent-instructions" AGENTS.md CLAUDE.md GEMINI.md
test -f docs/plans/2026-03-12-agent-instruction-refactor.md
test -f docs/specs/agent-instructions/spec.md
test -f .claude/agent-instructions/README.md
```

## 1. Technical Overview & Architecture Style

This is a documentation-only refactor. The target architecture is a progressive-disclosure model:

- Root files stay small and stable.
- Shared operational details live in linked guides.
- Provider-specific files remain focused on the differences that matter during execution.

- **Component Boundary**: Root agent entrypoints plus a shared guide bundle under `.claude/agent-instructions/`.
- **Key Dependencies**: `docs/README.md`, `templates/spec-template.md`, `templates/plan-template.md`, `.agent/rules/0000-Agents/`, `.agent/rules/2100-Documentation/`
- **Tech Stack**: Markdown, relative links, shell validation with `rg` and `test`

## 2. Coded Requirements (Traceability)

| ID | Requirement Description | Priority | Parent PRD REQ |
| -- | ----------------------- | -------- | -------------- |
| **[REQ-SPC-AGT-001]** | The three root files must become concise entrypoints rather than long-form policy stores. | High | N/A |
| **[REQ-SPC-AGT-002]** | Shared policy must move into repository-local linked guides under `.claude/agent-instructions/`. | High | N/A |
| **[REQ-SPC-AGT-003]** | All new and updated links must be relative and resolve to existing files. | Critical | N/A |
| **[REQ-SPC-AGT-004]** | Stale references to unavailable tools and artifacts must be removed. | Critical | N/A |

## 3. Data Modeling & Storage Strategy

- **Database Engine**: None
- **Schema Strategy**: Markdown-only documentation split between root entrypoints and guide documents
- **Migration Plan**: Rewrite the roots in place, move the shared guide bundle into `.claude/agent-instructions/`, and remove the obsolete shared-guide files without changing repository code

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
- `CLAUDE.md`: Claude-specific execution rules
- `GEMINI.md`: Gemini-specific reasoning rules
- `.claude/agent-instructions/README.md`: Shared guide index
- `.claude/agent-instructions/core-governance.md`: Universal governance details moved out of the root
- `.claude/agent-instructions/workflow.md`: Shared operating workflow and maintenance checks
- `docs/plans/2026-03-12-agent-instruction-refactor.md`: Execution plan for this refactor

## 6. Domain-Specific Contract Sections

### Anti-Patterns

- Root files duplicating the same guidance
- References to tools that do not exist in the active runtime
- Absolute file-system links inside repository documentation
- Provider files restating generic repository governance instead of linking to it

## 7. Edge Cases & Error Handling

- **Missing shared guide path**: If `.claude/agent-instructions/` is missing, root files must not be updated to link to non-existent targets.
- **Dirty worktree overlap**: If unrelated user edits touch the same files, preserve their intent and layer the refactor around the current content rather than reverting.

## 8. Verification Plan (Testing & QA)

- **[VAL-SPC-AGT-001] Structural review**: Confirm each root file reads as an entrypoint, not a full handbook.
- **[VAL-SPC-AGT-002] Link review**: Validate all new relative links with targeted `rg` and `test` commands.
- **[VAL-SPC-AGT-003] Truth review**: Manually inspect the roots and shared guides to confirm deprecated runtime-specific instructions no longer appear.
- **[VAL-SPC-AGT-004] Evidence capture**: Record command results after edits before declaring completion.

## 9. Non-Functional Requirements (NFR) & Scalability

- **Performance / Latency**: No runtime behavior change
- **Throughput**: N/A
- **Scalability Strategy**: The guide bundle must support additional provider-specific roots without repeating shared policy

## 10. Operations & Observability

- **Deployment Strategy**: Documentation-only change merged through normal repository workflow
- **Monitoring & Alerts**: N/A
- **Logging**: Verification is captured through command output during the refactor
- **Sensitive Data Handling**: No secrets or environment values may be introduced into the new documents
