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

분류 단위는 사고별 폴더이며, `incident.md`가 사고 사실의 정본이고 `postmortem.md`는 작성된 경우의 사후 분석으로 `parent_ids`로 Incident를 연결합니다.

## Workflow

### Create and Review

사고 ID를 따라 해당 폴더를 열고 `incident.md`를 확인합니다. 사후 분석이 있으면
같은 폴더의 `postmortem.md`에서 확인합니다.

### Transition and Exit

이 폴더의 사고는 Incident 수명주기를 따르며(open → investigating → mitigated 또는 resolved → closed), Incident 번호는 연도마다 다시 시작해 `inc-2026-NNNN` 형식으로 이 폴더에서만 발급합니다.

## Related Documents

### Upstream and Downstream

- [Incidents](../README.md)

### Policy and Templates

- [문서 언어 규칙](../../../../.agents/governance/documentation-protocol.md#document-language)
- 전용 템플릿 없음: Registry의 `incident-year-readme` profile(`docs/99.templates/registry.json`)이 형식을 소유합니다.
