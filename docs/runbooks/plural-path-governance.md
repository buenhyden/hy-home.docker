---
title: 'Plural Path Governance Runbook'
status: 'Active'
owner: 'buenhyden'
tags: ['runbook', 'governance']
layer: 'ops'
---

# Plural Path Governance Runbook

**Overview (KR):** 저장소의 평면적 복수형 경로 구조를 유지하기 위한 가이드라인입니다.

## Procedures

### 1. New Path Creation

Always use plural form for document category roots:

- `docs/plans/` (v) vs `docs/plan/` (x)
- `docs/specs/` (v) vs `docs/spec/` (x)

### 2. Implementation Plan Creation

Agents must strictly create new plans in `docs/plans/` using the `plan-template.md`.

### 3. Verification

Verify before completion:

```bash
ls docs/plan/ # Should error
ls docs/plans/ # Should succeed
```
