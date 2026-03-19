---
layer: agentic
title: 'Agent Rule Lazy-Loading Specification'
status: 'Canonical'
version: '1.0'
owner: 'buenhyden'
scope: 'master'
prd_reference: '../prd/2026-03-15-doc-refactor-prd.md'
arch_reference: '../ard/2026-03-15-agentic-ard.md'
decision_reference: '../adr/2026-03-15-0026-documentation-structure-and-lazy-loading.md'
tags: ['spec','implementation','agentic']
layer: agentic
---

# Agent Rule Lazy-Loading Specification

**Overview (KR):** 지연 로딩(Lazy-loading) 메커니즘을 통해 에이전트의 효율적인 규칙 로드를 구현하는 사양입니다.

> **Status**: Canonical
> **Scope**: master
> **layer:** architecture

**Overview (KR):** 에이전트 규칙 로딩 메커니즘의 기술적 세부 사항을 정의하며, 게이트웨이 파일과 인텐트 마커를 통한 동적 지침 로드 방식을 명시합니다.

## Technical or Platform Baseline

The system relies on the capabilities of modern AI coding agents (Claude, Gemini) to parse and follow Markdown-based links and markers. The implementation is filesystem-based within the `docs/agentic/` directory.

## Contracts

- **Config Contract**: Every rule file MUST be located in `docs/agentic/rules/` and have a unique marker.
- **Data or Interface Contract**: The marker format is `[LOAD:RULES:<CATEGORY>]`.
- **Archive / Governance Contract**: Changes to rule files must be documented in `docs/agentic/instructions.md`.

## 1. Technical Overview & Architecture Style

Rules are decoupled from the core behavioral instructions. When an agent identifies a task category (e.g., "Refactoring"), it scans the `gateway.md` to find the corresponding rule file and loads it.

- **Component Boundary**: `docs/agentic/gateway.md` (Router), `docs/agentic/rules/*.md` (Modules).
- **Key Dependencies**: `docs/agentic/instructions.md` (Base instructions).

## 2. Coded Requirements (Traceability)

| ID                | Requirement Description | Priority | Parent PRD REQ |
| ----------------- | ----------------------- | -------- | -------------- |
layer: agentic
| **[REQ-SPC-001]** | Gateway-indexed rules   | Critical | REQ-PRD-RD-03 |
| **[REQ-SPC-002]** | Modular rule separation | High | REQ-PRD-RD-01 |

## 8. Verification Plan (Testing & QA)

- **[VAL-SPC-AGT-01] Link Integrity**: All links in `gateway.md` must resolve to existing files.
- **[VAL-SPC-AGT-02] Marker Consistency**: Each `[LOAD:RULES:*]` marker must be unique and documented.
