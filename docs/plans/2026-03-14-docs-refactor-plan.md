---
goal: 'Organize repository documentation and enhance agent framework with modular rules and metadata.'
version: '1.0'
date_created: '2026-03-14'
last_updated: '2026-03-14'
owner: 'buenhyden'
status: 'Planned'
scope: 'master'
tags: ['implementation', 'planning']
layer: agentic
---

# Documentation & Agent Framework Refactoring Plan

> **Status**: Planned
> **Scope**: master
> **layer:** architecture

**Overview (KR):** 문서 구조를 카테고리 기 반으로 정돈하고, 에이전트 규칙을 모듈화하여 성능과 관리 효율성을 개선하기 위한 단계별 실행 계획입니다.

## Context & Introduction

This plan covers the implementation phase of the refactoring task, focusing on moving files, updating metadata, and refining the agent instruction loading logic.

## Tasks

| Task     | Description                    | Files Affected                | Target REQ | Validation Criteria      |
| -------- | ------------------------------ | ----------------------------- | ---------- | ------------------------ |
| TASK-001 | Refactor Gateway & Rules       | `docs/agentic/gateway.md`     | REQ-PRD-03 | Links resolve correctly  |
| TASK-002 | Apply `layer:` metadata        | `docs/**/*.md`                | REQ-PRD-02 | `grep` finds `layer:`    |
| TASK-003 | Consolidate shims              | `AGENTS.md`, `README.md`      | REQ-PRD-01 | Links are correct        |
| TASK-004 | Modularize behavioral rules    | `docs/agentic/rules/`         | REQ-PRD-04 | Rules are granular       |

## Verification

- `[VAL-001]` Run `grep -r "layer:" docs/` to ensure full coverage.
- `[VAL-002]` Verify agent session start behavior using the new Gateway.

## References

- `[../prd/2026-03-15-refactor-docs-prd.md]`
- `[../specs/2026-03-15-agent-rule-lazy-loading-spec.md]`
- `[../ard/2026-03-15-doc-taxonomy-ard.md]`
- `[../adr/0025-intent-based-lazy-loading.md]`
