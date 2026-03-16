---
layer: ops
title: 'Agent Rule Maintenance Runbook'
status: 'Active'
owner: 'buenhyden'
tags: ['runbook', 'agentic']
layer: 'ops'
---
layer: ops

# Agent Rule Maintenance Runbook
n**Overview (KR):** 에이전트 규칙(Rules)의 무결성을 점검하고 최신 표준에 맞춰 업데이트하는 운영 절차입니다.

**Overview (KR):** 에이전트용 지침 규칙(`docs/agentic/rules/`)과 루트 파일의 트리거 체계를 관리하고 동기화하기 위한 가이드입니다.

## Procedures

### 1. Adding a New Rule

1. Create a file in `docs/agentic/rules/`.
2. Define its intent and load markers.
3. Update the rule matrix in `AGENTS.md` and `GEMINI.md`.

### 2. Validating Triggers

Run specialized grep to find unregistered markers:

```bash
grep -C 2 "\[LOAD:RULES:" AGENTS.md GEMINI.md
```

### 3. Enforcing Skill Autonomy

Ensure any new behavioral guideline does not contain "Do not use tool X" without an ADR-backed security reason.
