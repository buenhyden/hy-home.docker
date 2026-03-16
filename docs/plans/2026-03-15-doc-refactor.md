---
layer: agentic
---
# Documentation Refactor Plan

> **Status**: In Progress
> **Scope**: master
> **layer:** architecture

**Overview (KR):** 2026년 3월 기준 최신 표준에 맞춰 리포지토리의 전체 문서 구조와 Agent 규칙을 재정비하는 실행 계획입니다.

## Context & Introduction

This work exists to align the repository with the flat taxonomy decision (ADR 0001) and ensure all agents use the trigger-based loading system.

## Tasks

### Phase-style task list

1. Audit root entry points (`AGENTS.md`, etc.).
2. Migrate instructions to `docs/agentic/`.
3. Fix root links and directory tree in `README.md`.
4. Create template-based document examples.

## Verification

- `[VAL-001]` Links in root files work correctly.
- `[VAL-002]` Metadata `layer:` exists in all new files.

## References

- `[../adr/0001-doc-taxonomy.md]`
- `[../ard/agentic-ard.md]`
- `[../specs/infra-spec.md]`
