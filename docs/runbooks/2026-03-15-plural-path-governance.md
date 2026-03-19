---
layer: ops
title: 'Plural Path Governance Runbook'
status: 'Active'
owner: 'buenhyden'
tags: ['runbook', 'governance']
layer: ops
---
layer: ops

# Plural Path Governance Runbook

n**Overview (KR):** 표준화된 복수형 경로 규칙이 올바르게 적용되었는지 점검하고 강제하는 가버넌스 절차입니다.

**Overview (KR):** 저장소의 평면적 복수형 경로 구조를 유지하기 위한 가이드라인입니다.

## Procedures

### 1. New Path Creation

Always use plural form for document category roots:

- `docs/plans/` (v) vs `docs/plans/` (x)
- `docs/specs/` (v) vs `docs/spec/` (x)

### 2. Implementation Plan Creation

Agents must strictly create new plans in `docs/plans/` using the `plan-template.md`.

### 3. Verification

Verify before completion:

```bash
ls docs/plans/ # Should error
ls docs/plans/ # Should succeed
```
