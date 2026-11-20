---
title: "05.operations/incidents/2026"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
---

# 05.operations/incidents/2026

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Responsibility

##### Purpose

###### Purpose and Readers
<!-- core-payload-level:4 -->

2026년에 열린 사고 기록을 사고별 폴더로 안내합니다. 각 폴더에는 사고 사실
기록(`incident.md`)과, 작성된 경우 사후 분석(`postmortem.md`)이 함께 있습니다.

###### Inputs and Outputs
<!-- core-payload-level:4 -->

이 문서는 2026년 사고 기록의 직접 경로만 안내합니다.

##### Excluded Responsibilities

상태와 결론은 각 기록이 소유하며 이 README는 옮겨 적지 않습니다.

#### Current Contents

##### Paths

###### Current Items
<!-- core-payload-level:4 -->

| Path | Purpose |
| --- | --- |
| [inc-0002-airflow-keycloak-native-auth/](inc-0002-airflow-keycloak-native-auth/) | `inc-2026-0002` Airflow Keycloak Native Authentication Migration 사고 기록과 사후 분석 |

###### Classification
<!-- core-payload-level:4 -->

분류 단위는 사고별 폴더이며, `incident.md`가 사고 사실의 정본이고 `postmortem.md`는 작성된 경우의 사후 분석으로 `parent_ids`로 Incident를 연결합니다.

##### Owners

이 README의 소유자는 frontmatter `owner`의 `@buenhyden`입니다. 목록에 있는 각 항목의 소유자는 이 README가 따로 기록하지 않습니다.

#### Usage

##### Entry Points

###### Upstream and Downstream
<!-- core-payload-level:4 -->

- [Incidents](../README.md)

###### Policy and Templates
<!-- core-payload-level:4 -->

- [문서 언어 규칙](../../../00.workspace/03.process/documentation-protocol.md#document-language)
- [README 템플릿](../../../99.templates/02.templates/93.common/readme-incident-year.template.md): 이 README의 양식 원본이며 형식은 Stage 99 Registry의 profile이 소유합니다

##### Checks

###### Create and Review
<!-- core-payload-level:4 -->

사고 ID를 따라 해당 폴더를 열고 `incident.md`를 확인합니다. 사후 분석이 있으면
같은 폴더의 `postmortem.md`에서 확인합니다.

###### Transition and Exit
<!-- core-payload-level:4 -->

이 폴더의 사고는 Incident 수명주기를 따르며(open → investigating → mitigated 또는 resolved, resolved에서만 closed), Incident 번호는 연도마다 다시 시작해 `inc-2026-NNNN` 형식으로 이 폴더에서만 발급합니다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
