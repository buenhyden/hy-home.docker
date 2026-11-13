---
title: "05.operations/incidents/2026"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "operations"
---

# 05.operations/incidents/2026

## Stage Responsibility

### Purpose and Readers

2026년에 열린 사고 기록을 사고별 폴더로 안내합니다. 각 폴더에는 사고 사실
기록(`incident.md`)과, 작성된 경우 사후 분석(`postmortem.md`)이 함께 있습니다.
상태와 결론은 각 기록이 소유하며 이 README는 옮겨 적지 않습니다.

### Inputs and Outputs

이 문서는 2026년 사고 기록의 직접 경로만 안내합니다.

## Contents

### Current Items

| Path | Purpose |
| --- | --- |
| [inc-0002-airflow-keycloak-native-auth/](inc-0002-airflow-keycloak-native-auth/) | `inc-2026-0002` Airflow Keycloak Native Authentication Migration 사고 기록과 사후 분석 |

### Classification

이 폴더의 분류 단위는 사고별 폴더이며, 각 폴더는 사고 사실 기록 `incident.md`와 작성된 경우 사후 분석 `postmortem.md`로 구성됩니다. 상태와 결론은 각 기록이 소유합니다.

## Workflow

### Create and Review

사고 ID를 따라 해당 폴더를 열고 `incident.md`를 확인합니다. 사후 분석이 있으면
같은 폴더의 `postmortem.md`에서 확인합니다.

### Transition and Exit

이 README는 `navigation` 수명주기의 `active` 상태만 가지며 다른 상태로 전이하지 않습니다. 목록 항목을 추가·이동·삭제할 때 이 문서를 함께 갱신하고, 삭제한 항목의 이력은 Git이 기록합니다.

## Related Documents

### Upstream and Downstream

- [Incidents](../README.md)

### Policy and Templates

- [문서 언어 규칙](../../../../.agents/governance/documentation-protocol.md#document-language)
- 전용 템플릿 없음: Registry의 `incident-year-readme` profile(`docs/99.templates/registry.json`)이 형식을 소유합니다.
