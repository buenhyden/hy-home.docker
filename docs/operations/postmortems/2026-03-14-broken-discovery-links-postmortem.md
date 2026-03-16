---
layer: ops
---

# Postmortem: Broken Documentation Discovery Path
>
> **Overview (KR):** 문서 발견 경로의 유효성 검증 부족으로 인해 발생한 장애의 사후 분석 및 재발 방지 대책입니다.

> **Incident Reference**: `[../incidents/2026-03-14-broken-discovery-links.md]`

## Executive Summary

A SEV-2 incident occurred where AI agents could not locate technical documentation due to stale links in the documentation gateway. The root cause was the manual oversight of link updates during a directory flatting process. Corrective actions involve automated link checking.

## What Went Well

- Incident detected almost immediately during agent task execution.
- Roll-forward fix was simple and effective.

## What Went Wrong

- The `implementation_plan` lacked a specific task for "Verify all relative links in gateway.md".
- No automated validation script was in place to check cross-document integrity.

## Action Items

| Task | Owner | Due Date |
| --- | --- | --- |
| Create `scripts/check-doc-links.sh` | DevOps Agent | 2026-03-15 |
| Update `documentation-maintenance.md` runbook with verification steps | Antigravity | 2026-03-14 |
