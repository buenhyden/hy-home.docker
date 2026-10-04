---
title: "05.operations/incidents/2026"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
layer: "operations"
---

# 05.operations/incidents/2026

## Overview

2026년에 열린 사고 기록을 사고별 폴더로 안내합니다. 각 폴더에는 사고 사실
기록(`incident.md`)과, 작성된 경우 사후 분석(`postmortem.md`)이 함께 있습니다.
상태와 결론은 각 기록이 소유하며 이 README는 옮겨 적지 않습니다.

## Scope

이 문서는 2026년 사고 기록의 직접 경로만 안내합니다. 사고의 상태, 조치, 승인,
사후 분석은 각 사고 기록이 소유합니다.

## Structure

| ID | 사고 |
| --- | --- |
| inc-2026-0002 | [Airflow Keycloak Native Authentication Migration](inc-0002-airflow-keycloak-native-auth/) |

## Usage

사고 ID를 따라 해당 폴더를 열고 `incident.md`를 확인합니다. 사후 분석이 있으면
같은 폴더의 `postmortem.md`에서 확인합니다.

## Related Documents

- [Incidents](../README.md)
- [문서 언어 규칙](../../../../.agents/governance/documentation-protocol.md#document-language)
