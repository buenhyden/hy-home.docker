---
goal: 'Refactor documentation and agent instructions'
version: '1.0'
date_created: '2026-03-15'
last_updated: '2026-03-15'
owner: 'buenhyden'
status: 'Planned'
scope: 'master'
tags: ['implementation', 'planning']
layer: agentic
---

# Documentation and Agent Refactor Plan

> **Status**: Planned
> **Scope**: master
> **layer:** product

**Overview (KR):** 본 계획은 저장소의 모든 핵심 문서를 새로운 분류 체계에 맞게 재정리하고, AI Agent가 지침을 효율적으로 로드할 수 있도록 지침 체계를 리팩토링하는 과정을 단계별로 정의합니다.

## Context & Introduction

This plan executes the requirements defined in `docs/prd/2026-03-15-doc-refactor-prd.md` and follows the architecture in `docs/ard/doc-refactor-ard.md`.

## Tasks

| Task     | Description                                         | Files Affected                       | Target REQ   | Validation Criteria          |
| -------- | --------------------------------------------------- | ------------------------------------ | ------------ | ---------------------------- |
| TASK-001 | Update core root files with metadata and links      | `ARCHITECTURE.md`, `README.md`, etc. | REQ-PRD-02   | `layer:` present in head     |
| TASK-002 | Refactor `docs/agentic/gateway.md`                  | `docs/agentic/gateway.md`            | REQ-PRD-05   | Discovery protocol updated   |
| TASK-003 | Update `docs/agentic/instructions.md`               | `docs/agentic/instructions.md`       | REQ-PRD-06   | Skill autonomy mentioned     |
| TASK-004 | Reorganize `docs/operations/` subdirectories        | `docs/operations/`                   | REQ-PRD-01   | Flat taxonomy implemented    |
| TASK-005 | Verify all links and metadata                       | All modified files                   | REQ-PRD-02   | No broken links              |

## Verification

- `[VAL-001]` Run `rg 'layer:'` to ensure all core files have metadata.
- `[VAL-002]` Verify relative links between docs.
- `[VAL-003]` Test agent discovery flow by simulating a new session.

## References

- `[../prd/2026-03-15-doc-refactor-prd.md]`
- `[../ard/doc-refactor-ard.md]`
- `[../adr/0001-lazy-loading-protocol.md]`
