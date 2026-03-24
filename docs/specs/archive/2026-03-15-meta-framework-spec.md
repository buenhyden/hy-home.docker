---
title: 'Meta-Framework & Documentation Spec'
status: 'Draft'
version: 'v1.1.0'
owner: 'Antigravity'
layer: agentic
---

# Meta-Framework & Documentation Specification

> **Status**: Draft
> **Scope**: master
> **layer:** agentic
> **Related PRD**: `../prd/2026-03-15-meta-framework-prd.md`
> **Related Architecture**: `../ard/2026-03-15-agentic-ard.md`

**Overview (KR):** 리포지토리 가버넌스와 문서화 프레임워크의 메타 설계를 정의하는 사양입니다.

## 1. Root File Cleanup

- **README.md**: Retain Overview, Features, Tech Stack, and Quick Start. Move Troubleshooting to `docs/guides/troubleshooting.md`. Remove "Project Structure" (covered by `docs/README.md`).
- **ARCHITECTURE.md**: Retain Invariants and Runtime Topology. Move change governance details to `.agent/rules/1900-Architecture_Patterns/1910-architecture-documentation.md`.
- **COLLABORATING.md/CONTRIBUTING.md**: Move content to `docs/manuals/collaboration-guide.md` and `docs/guides/contributing-guide.md`. Replace with short pointers to those files.

## 2. Agent Rule Refactor

- Create `.agent/rules/2100-Documentation/2105-doc-refactor.md`:
  - Definition of refactoring workflow.
  - Required skills (`agent-md-refactor`, `claude-md-improver`).
  - Automated checks.
- Create `.agent/rules/2100-Documentation/2110-doc-core-std.md`:
  - Rules for updating `docs/`.
  - Forced `layer` metadata check.

## 3. Lazy Loading Implementation

Update `docs/agentic/gateway.md` with:

```markdown
| Intent | Entry Point |
| --- | --- |
| Refactoring Documentation | [.agent/rules/2100-Documentation/2106-doc-workflow.md](../../.agent/rules/2100-Documentation/2106-doc-workflow.md) |
| Standard Doc Update | [.agent/rules/2100-Documentation/2110-doc-core-std.md](../../.agent/rules/2100-Documentation/2110-doc-core-std.md) |
```
