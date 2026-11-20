---
title: "Document governance synthetic fixtures"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2026-10-11"
---

# 문서 계약 합성 입력

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

#### Service

##### Purpose

문서 경로·정체성 계약을 운영 값 없이 검증하는 합성 입력 모음입니다.

###### Audience
<!-- core-payload-level:4 -->

문서 도구 구현자와 독립 검토 담당자입니다.

###### Scope
<!-- core-payload-level:4 -->

문서 이동·Registry 등록·운영 실행을 수행하지 않습니다. 실제 전수 문서 분류와
승인된 변경 경로는 owning Task가 관리합니다.

###### Structure
<!-- core-payload-level:4 -->

- [operations-moves](operations-moves/README.md): 정확한 경로·ID 매핑과 유형별 LAB
  문서 목적지의 합성 시험 자산입니다.

##### Interfaces

###### Inputs and Outputs
<!-- core-payload-level:4 -->

합성 자료만 추가합니다. 비밀값·개인 식별자·실제 운영 로그를 넣지 않습니다.

###### Security Boundary
<!-- core-payload-level:4 -->

합성 자료만 두며 비밀값, 개인 식별자, 실제 운영 로그를 넣지 않는다. 문서 이동, Registry 등록, 운영 실행을 수행하지 않는다.

#### Usage

##### Prerequisites

기존 Python unittest와 JSON 입력을 사용합니다.

##### Selected Start

하위 폴더 README에서 시험 범위와 입력을 확인합니다. 새 합성 자산은 해당 계약의
시험 소유자가 관리하고 상위 fixture 진입점을 함께 갱신합니다.

#### Checks

##### Readiness

```sh
python3 -m unittest tests.lib.document_governance.test_operations_moves -v
```

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [Fixture 진입점](../README.md)
- [문서 진입점](../../../docs/README.md)

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 실행되는 서비스가 아니라 시험 입력이므로 관측·복구 대상이 없다. 변경은 Git에서 되돌린다.

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
