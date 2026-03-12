# Agent Instruction Refactor Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.
> **Status**: Completed
> **Scope**: domain

**Goal:** Refactor `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` into a progressive-disclosure instruction set with accurate provider-specific roots and shared linked guidance directly under `.claude/`.

**Architecture:** Keep root files as stable entrypoints, move shared universal policy directly under `.claude/`, and keep the repository-local spec and plan under `docs/` so the refactor still satisfies the repo's spec-first governance. The resulting structure should remove stale tool references and keep all links relative.

**Tech Stack:** Markdown, repository documentation templates, `rg`, `test`

**Overview (KR):** 이 계획은 루트 에이전트 지침 파일을 짧은 진입점으로 줄이고, 공통 정책을 공유 가이드로 이동해 유지보수성을 높이기 위한 문서 작업 절차를 정의한다. 검증은 링크 무결성과 오래된 도구 참조 제거 여부를 중심으로 수행한다.

## Context & Introduction

This repository requires a spec and plan before refactors. The current instruction files contain a useful baseline, but they mix shared governance with provider-specific directives and reference tools that are not available in the active Codex runtime. This plan covers the documentation-only work needed to normalize those files.

## Tasks

| Task | Description | Files Affected | Target REQ | Validation Criteria |
| ---- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | Capture the refactor contract in a repository-local spec. | `docs/specs/agent-instructions/spec.md` | [REQ-SPC-AGT-002] | Spec exists and states structure, truth, and verification contracts. |
| TASK-002 | Create a shared guide bundle for common governance and workflow rules. | `.claude/README.md`, `.claude/core-governance.md`, `.claude/workflow.md` | [REQ-SPC-AGT-002] | Guide files exist and use relative links only. |
| TASK-003 | Rewrite `AGENTS.md` as the minimal universal entrypoint. | `AGENTS.md` | [REQ-SPC-AGT-001] | Root file stays concise and links to the shared guides. |
| TASK-004 | Rewrite `CLAUDE.md` and `GEMINI.md` to keep only provider-specific directives. | `CLAUDE.md`, `GEMINI.md` | [REQ-SPC-AGT-001], [REQ-SPC-AGT-004] | Provider roots no longer contain deprecated runtime assumptions or duplicated universal policy. |
| TASK-005 | Validate links and remove stale references from the whole instruction set. | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/*.md` | [REQ-SPC-AGT-003], [REQ-SPC-AGT-004] | `rg` checks return only the intended matches and `test -f` checks succeed. |

## Verification

- `[VAL-001]` Manually inspect the roots and shared guides and confirm no deprecated runtime-specific instructions remain.
- `[VAL-002]` Run `rg -n "\\.claude/(core-governance|workflow)" AGENTS.md CLAUDE.md GEMINI.md` and confirm each root links to the shared guide bundle.
- `[VAL-003]` Run `test -f docs/plans/2026-03-12-agent-instruction-refactor.md`.
- `[VAL-004]` Run `test -f docs/specs/agent-instructions/spec.md`.

## References

- `../specs/agent-instructions/spec.md`
- `../README.md`
- `../../AGENTS.md`
- `../../CLAUDE.md`
- `../../GEMINI.md`

## 2. Goals & In-Scope

- **Goals:**
  - Make the three root instruction files shorter and more truthful.
  - Centralize shared rules so future maintenance happens in one place.
  - Preserve provider-specific guidance without duplicating repository governance.
- **In-Scope (Scope of this Plan):**
  - Root instruction files
  - Shared guide documents under `.claude/`
  - This spec and plan pair

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - Refactoring `.agent/rules/` source material
  - Updating unrelated repository documentation
- **Out-of-Scope:**
  - Command automation beyond simple validation
  - Runtime or code changes outside documentation

## 4. Requirements & Constraints

- **Requirements:**
  - `[REQ-PLN-001]`: Keep all repository-internal links relative.
  - `[REQ-PLN-002]`: Do not reference tools or artifacts absent from the current runtime.
  - `[REQ-PLN-003]`: Preserve provider-specific guidance while reducing duplication.
- **Constraints:**
  - The worktree is already dirty; unrelated changes must remain intact.
  - Verification must rely on commands available in the current environment.

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Shared guide placement feels unnatural to future maintainers | Medium | Use `.claude/README.md` as an obvious entrypoint and link from all roots. |
| Root files become too sparse to be useful | Medium | Keep high-signal quick-reference bullets in each root. |
| Deprecated runtime-specific instructions remain in migrated content | High | Use targeted inspection before completion and keep roots/provider files tightly scoped. |

## 8. Completion Criteria

- [x] Root files are concise and provider-specific
- [x] Shared guide bundle exists and is linked from all roots
- [x] Spec and plan files exist
- [x] Verification checks pass or any exceptions are documented
