---
layer: ops
---
# Postmortem: Documentation Path Inconsistency

**Overview (KR):** 문서 경로의 불일치로 인한 AI Agent의 탐색 실패 사건을 분석하고, 재발 방지를 위한 평탄화된 세금 노미(Taxonomy) 적용을 결정했습니다.

## 1. Incident Summary

| Field                 | Value                                   |
| --------------------- | --------------------------------------- |
| **Incident ID**       | `INC-20260315-001`                      |
| **Incident Date**     | `2026-03-15`                            |
| **Analysis Date**     | `2026-03-15`                            |
| **Duration**          | `30m`                                   |
| **Severity**          | `SEV-2`                                 |
| **Status**            | `Resolved`                              |
| **Incident Document** | `[../incidents/2026-03-15-doc-path-inconsistency.md]` |
| **layer:**            | architecture                            |

## 2. Root Cause Analysis

### Primary Root Cause

Lack of a strictly enforced documentation taxonomy led to mixed singular/plural directory naming across different project phases.

## 3. Action Items

| Action        | Owner | Priority | Ticket / Reference | Status  |
| ------------- | ----- | -------- | ------------------ | ------- |
| Apply ADR 0001| hy    | High     | `docs/adr/0001.md` | Done    |
| Audit README  | hy    | Medium   | N/A                | Done    |

## 4. Prevention and Verification

- Enforce plural naming for implementation artifacts.
- Use `layer:` metadata for automated auditing.
