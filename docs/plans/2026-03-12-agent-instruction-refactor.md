# Agent Instruction Refactor Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.
> **Status**: In Progress
> **Scope**: domain

**Goal:** Refactor `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and the linked documentation indexes into a 2026-03-current agent-instruction system with accurate provider-specific roots, shared `.claude` guidance, and complete lazy-loading entrypoints.

**Architecture:** Keep `AGENTS.md` as the canonical cross-agent entrypoint, use `.claude/*.md` for shared operational detail, make `CLAUDE.md` a provider-native `@` import shim, make `GEMINI.md` a provider shim with minimal deltas, and repair `docs/*/README.md` so the document families are actually lazy-loadable. The refactor must remove stale template paths, absolute links, and broken spec paths while preserving the repo’s spec-first governance.

**Tech Stack:** Markdown, repository documentation templates, `rg`, `test`

**Overview (KR):** 이 계획은 루트 에이전트 지침 파일을 짧은 진입점으로 줄이고, 공통 정책을 공유 가이드로 이동해 유지보수성을 높이기 위한 문서 작업 절차를 정의한다. 검증은 링크 무결성과 오래된 도구 참조 제거 여부를 중심으로 수행한다.

## Context & Introduction

This repository requires a spec and plan before refactors. The current instruction files and linked indexes contain a useful baseline, but they are incomplete against the 2026-03 provider guidance and the repository’s actual structure. This plan covers the documentation-only work needed to normalize the full instruction surface.

## Tasks

| Task | Description | Files Affected | Target REQ | Validation Criteria |
| ---- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | Capture the refactor contract in a repository-local spec. | `docs/specs/agent-instructions/spec.md` | [REQ-SPC-AGT-002] | Spec exists and states structure, truth, and verification contracts. |
| TASK-002 | Rebuild `.claude` guidance around repo-specific governance and workflow. | `.claude/README.md`, `.claude/core-governance.md`, `.claude/workflow.md` | [REQ-SPC-AGT-002], [REQ-SPC-AGT-005] | Shared guidance exists, is repo-specific, and uses relative links only. |
| TASK-003 | Rewrite `AGENTS.md` as the canonical cross-agent entrypoint. | `AGENTS.md` | [REQ-SPC-AGT-001], [REQ-SPC-AGT-005] | Root file stays concise and exposes the full lazy-loading map. |
| TASK-004 | Rewrite `CLAUDE.md` and `GEMINI.md` as provider shims. | `CLAUDE.md`, `GEMINI.md` | [REQ-SPC-AGT-001], [REQ-SPC-AGT-004], [REQ-SPC-AGT-006] | Provider roots follow the chosen provider models and avoid duplicating shared policy. |
| TASK-005 | Repair linked documentation indexes and add a plans index. | `docs/README.md`, `docs/adr/README.md`, `docs/ard/README.md`, `docs/prd/README.md`, `docs/runbooks/README.md`, `docs/operations/README.md`, `docs/operations/incidents/README.md`, `docs/specs/README.md`, `docs/plans/README.md` | [REQ-SPC-AGT-003], [REQ-SPC-AGT-005] | All doc families are lazy-loadable through stable README entrypoints. |
| TASK-006 | Validate links and remove stale references from the whole instruction set. | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/*.md`, `docs/**/*.md` | [REQ-SPC-AGT-003], [REQ-SPC-AGT-004] | `rg` checks return only the intended matches and `test -f` checks succeed. |

## Verification

- `[VAL-001]` Manually inspect the roots and shared guides and confirm no deprecated runtime-specific instructions remain.
- `[VAL-002]` Run `rg -n "^@" CLAUDE.md` and confirm Claude imports shared guidance.
- `[VAL-003]` Run `rg -n 'file://|templates/(architecture|product|operations)/|\]\(/specs/' AGENTS.md CLAUDE.md GEMINI.md .claude docs` and confirm no stale links remain.
- `[VAL-004]` Run `test -f docs/specs/agent-instructions/spec.md`.
- `[VAL-005]` Run `test -f docs/plans/2026-03-12-agent-instruction-refactor.md`.
- `[VAL-006]` Run `test -f docs/plans/README.md`.

## References

- `../specs/agent-instructions/spec.md`
- `../README.md`
- `../../AGENTS.md`
- `../../CLAUDE.md`
- `../../GEMINI.md`

## 2. Goals & In-Scope

- **Goals:**
  - Make the three root instruction files current, concise, and provider-correct.
  - Centralize shared rules in `.claude/` without losing repo-specific detail.
  - Make ADR, ARD, PRD, specs, plans, runbooks, operations history, and incidents lazy-loadable from stable indexes.
- **In-Scope (Scope of this Plan):**
  - Root instruction files
  - Shared guide documents under `.claude/`
  - Linked `docs/*/README.md` index documents
  - This spec and plan pair

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - Refactoring `.agent/rules/` source material
  - Rewriting non-index product or infrastructure docs
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
| Linked indexes continue to point to obsolete template locations | High | Repair every linked README in the same refactor instead of leaving them for later. |

## 8. Completion Criteria

- [ ] Root files are concise and provider-specific
- [ ] Shared guide bundle exists and is linked from all roots
- [ ] Linked documentation indexes are repaired and plans are lazy-loadable
- [ ] Spec and plan files exist
- [ ] Verification checks pass or any exceptions are documented
