---
title: "05.operations/incidents/2026"
version: "0.2.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "operations"
---

# 05.operations/incidents/2026

## Responsibility

### Purpose

#### Purpose and Readers

2026년에 열린 사고 기록을 사고별 폴더로 안내합니다. 각 폴더에는 사고 사실
기록(`incident.md`)과, 작성된 경우 사후 분석(`postmortem.md`)이 함께 있습니다.

#### Inputs and Outputs

이 문서는 2026년 사고 기록의 직접 경로만 안내합니다.

### Excluded Responsibilities

상태와 결론은 각 기록이 소유하며 이 README는 옮겨 적지 않습니다.

## Current Contents

### Paths

#### Current Items

| Path | Purpose |
| --- | --- |
| [inc-0002-airflow-keycloak-native-auth/](inc-0002-airflow-keycloak-native-auth/) | `inc-2026-0002` Airflow Keycloak Native Authentication Migration 사고 기록과 사후 분석 |

#### Classification

분류 단위는 사고별 폴더이며, `incident.md`가 사고 사실의 정본이고 `postmortem.md`는 작성된 경우의 사후 분석으로 `parent_ids`로 Incident를 연결합니다.

### Owners

이 README의 소유자는 frontmatter `owner`의 `@buenhyden`입니다. 목록에 있는 각 항목의 소유자는 이 README가 따로 기록하지 않습니다.

## Usage

### Entry Points

#### Upstream and Downstream

- [Incidents](../README.md)

#### Policy and Templates

- [문서 언어 규칙](../../../00.workspace/03.process/documentation-protocol.md#document-language)
- [README 템플릿](../../../99.templates/02.templates/93.common/readme-incident-year.template.md): 이 README의 양식 원본이며 형식은 Stage 99 Registry의 profile이 소유합니다

### Checks

#### Create and Review

사고 ID를 따라 해당 폴더를 열고 `incident.md`를 확인합니다. 사후 분석이 있으면
같은 폴더의 `postmortem.md`에서 확인합니다.

#### Transition and Exit

이 폴더의 사고는 Incident 수명주기를 따르며(open → investigating → mitigated 또는 resolved, resolved에서만 closed), Incident 번호는 연도마다 다시 시작해 `inc-2026-NNNN` 형식으로 이 폴더에서만 발급합니다.
