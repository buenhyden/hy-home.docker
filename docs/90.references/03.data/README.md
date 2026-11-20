---
title: "Data Packages"
version: "3.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "references"
created: "2026-07-02"
---

# Data Packages

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

저장소 인벤토리, 생성된 navigation 산출물, 구조화된 데이터셋, 용어집,
안정적인 참고 사실입니다.

Stage 90 authority boundary와 package lifecycle 규칙은
[References index](../README.md)와 Stage 99 Registry가 정의합니다.

###### Inputs and Outputs
<!-- core-payload-level:4 -->

이 README는 현재 data package 경로와 은퇴한 package의 번호 기록을 안내합니다. dataset의
사실과 consumer 관계는 해당 package와 canonical consumer가 소유합니다.

현재 tree가 package 집합을 정의합니다: package는 README가 존재하고 자신의
Stage 99 profile을 만족할 때 존재합니다. 필요한 의미를 canonical owner로
옮기고 모든 inbound consumer를 갱신하고 아래 표의 행을 제거하고
그 번호를 Registry `reserved_history`에 추가하는 같은 변경에서 제거되어
은퇴합니다. 은퇴한 `DATA-` 번호는 다시 발급하지 않습니다.

##### Excluded Responsibilities

dataset의 사실과 consumer 관계는 이 README가 아니라 해당 package와 canonical consumer가 소유합니다.

#### Current Contents

##### Paths

###### Current Items
<!-- core-payload-level:4 -->

현재 package는 없습니다.

열세 개 package가 2026-09-10에 은퇴했고, DATA-0096은 날짜가 고정된 조사 결과여서 오프라인에서 재현하거나 최신성을 증명할 수 없어 2026-11-14에 은퇴했습니다. SPEC-0173은 이 범주가 따르는
규칙을 명시합니다: Stage 90 데이터는 "현재 consumer가 존재하는 동안만
현재성을 유지한다." 이 package들을 살아 있게 만들던 모든 consumer,
곧 등록된 generator, freshness gate, 해당 경로를 적어 두던 metadata
allow-list가 같은 변경에서 제거되어 더 이상 읽는 이가 남지 않았습니다.
삭제된 각 본문은 Git 이력에 있으며, 그 번호는 Registry `reserved_history`가
보관합니다.

DATA-0067은 Migration 0003의 복구 비교가 마지막 consumer였습니다. SPEC-0248이
그 비교를 제거했고 SPEC-0249가 package를 삭제했으므로, 그 본문은 Git 이력에만
있습니다.

이곳의 새 package는 만들기 전에 현재 consumer가 먼저 지정되어야 하며,
만든 뒤에 지정해서는 안 됩니다.

###### Classification
<!-- core-payload-level:4 -->

열세 개 package가 2026-09-10에, DATA-0096이 2026-11-14에 은퇴해 현재 tree에는 없으며, 은퇴한 `DATA-` 번호는 Registry `reserved_history`가 보관하고 본문은 Git 이력에만 있는 비권위 기록입니다.

##### Owners

이 README의 소유자는 frontmatter `owner`의 `@buenhyden`입니다. 목록에 있는 각 항목의 소유자는 이 README가 따로 기록하지 않습니다.

#### Usage

##### Entry Points

###### Upstream and Downstream
<!-- core-payload-level:4 -->

- [References index](../README.md)

###### Policy and Templates
<!-- core-payload-level:4 -->

- [Stage 99 Registry](../../99.templates/registry.json)
- [문서 작성 계약](../../00.workspace/03.process/documentation-protocol.md#readme-and-agentsmd): README와 AGENTS.md의 역할 구분
- [README 템플릿](../../99.templates/02.templates/93.common/readme-category.template.md): 이 README의 양식 원본이며 형식은 Stage 99 Registry의 profile이 소유합니다

##### Checks

###### Create and Review
<!-- core-payload-level:4 -->

package는 `data/####-<slug>/` 아래에만 만들고, 대응하는 Stage 99
템플릿을 사용합니다. 관찰 날짜, 인용, provenance, 활성 owner
Traceability를 보존합니다.

###### Transition and Exit
<!-- core-payload-level:4 -->

package는 필요한 의미를 canonical owner로 옮기고 모든 inbound consumer를 갱신하며 이 README의 표에서 행을 제거하고 번호를 Registry `reserved_history`에 추가하는 같은 변경에서 은퇴합니다. 은퇴한 `DATA-` 번호는 다시 발급하지 않습니다.

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
