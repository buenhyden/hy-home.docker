---
layer: ops
---
# Active Incident: INC-20260315-001 / Documentation Path Inconsistency
n**Overview (KR):** 문서 경로 불일치 및 트리거 동작 오류로 인한 시스템 운영 장애 내역입니다.

**Postmortem Link**: `[../postmortems/2026-03-15-doc-path-fix.md]`

**Overview (KR):** 리포지토리의 문서 경로가 단수와 복수로 혼용되어 AI Agent가 문서를 찾지 못하는 장애가 발생했습니다.

## Incident Metadata

| Field                     | Value                                                  |
| ------------------------- | ------------------------------------------------------ |
| **Incident ID**           | `INC-20260315-001`                                     |
| **Severity**              | `SEV-2`                                                |
| **Status**                | `Resolved`                                             |
| **Detection Time**        | `2026-03-15 00:00 UTC`                                 |
| **Primary Service**       | Documentation Hub                                      |
| **Affected Dependencies** | AI Agent Rules                                         |
| **Evidence Source**       | Agent Hallucination Report                             |
| **Runbook Link**          | `[../../runbooks/doc-maintenance.md]`                  |
| **layer:**                | architecture                                           |

## Incident Summary

The discovery gateway was pointing to singular `docs/plan/` while the actual directory was `docs/plans/`, causing template loading failures.

## Impact

- AI agents unable to find implementation plans.
- Broken links in root `README.md`.

## Timeline

| Time (UTC) | Actor  | Detail                                             |
| ---------- | ------ | -------------------------------------------------- |
| 00:00      | System | **[Detection]** Agent failed to load `plan-template`.|
| 00:10      | hy     | **[Investigation]** Path mismatch identified.       |
| 00:30      | hy     | **[Mitigation]** Paths updated to plural.          |
| 09:00      | hy     | **[Verification]** Root files audited and fixed.   |
