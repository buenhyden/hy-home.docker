---
layer: ops
title: '2026-03 Agentic Maintenance Runbook'
status: 'Active'
owner: 'buenhyden'
tags: ['runbook', 'agentic']
layer: ops
---
layer: ops

# 2026-03 Agentic Maintenance Runbook
n**Overview (KR):** 2026년 3월 표준에 따른 리포지토리의 문서 정렬 상태를 점검하고 수정하는 절차입니다.

**Overview (KR):** 2026년 3월 도입된 의도 기반 규칙 로딩 체계를 유지 관리하고, 에이전트 성능을 최적의 상태로 지속시키기 위한 운영 절차서입니다.

## Maintenance Procedures

### 1. Synchronizing Triggers

Ensure any new rule added to `docs/agentic/rules/` is reflected in:

- `AGENTS.md` (General)
- `GEMINI.md` (Triggers section)
- `docs/agentic/gateway.md` (Matrix)

### 2. Validating Metadata

Run verification on commit:

```bash
grep -L "layer:" docs/**/*.md
```

### 3. Reviewing Persona Efficiency

Periodically verify if complex tasks are being initiated with the **Reasoner** persona as mandated in `GEMINI.md`.
