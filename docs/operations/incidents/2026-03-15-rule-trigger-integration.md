---
title: 'Incident 0002: Rule Trigger Integration'
status: 'Resolved'
severity: 'SEV-2'
date: '2026-03-15'
owner: 'buenhyden'
tags: ['incident', 'rules']
layer: 'ops'
---

# Incident 0002: Rule Trigger Integration

**Overview (KR):** 에이전트 지침 파일에 직접적인 규칙 트리거가 없어 발생하던 비효율성을 해결하기 위해, 루트 지침 파일에 의도 기반 선택 행렬을 통합하는 과정에서 발생한 구조적 변경 사건입니다.

## Context

AI agents were previously forced to hop through `gateway.md` for every session, increasing latency and error potential.

## Actions Taken

- Integrated `[LOAD:RULES:*]` triggers into `AGENTS.md` and `GEMINI.md`.
- Converted `CLAUDE.md` into a structured entrypoint with explicit skill autonomy.

## Resolution

Agents now load the correct instructions on the first turn.
