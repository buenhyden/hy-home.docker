---
title: "독립 통지 합성 fixture"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
---

# 독립 통지 합성 fixture

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

[cases.json](cases.json)은 공개 합성 claim·수락/ack 유실·retry/stale lease 기대 결과입니다.

###### Scope
<!-- core-payload-level:4 -->

UUID·run ID·주소는 합성이며 운영 token이나 credential이 아닙니다. DB/SMTP/native 수용 증거를 포함하지 않습니다.

###### Structure
<!-- core-payload-level:4 -->

닫힌 claim, 상태별 기대 결과, 개인정보 누출 검사 marker와 아직 필요한 native 실패·복구 사례를 둡니다.

##### Interfaces

###### Inputs and Outputs
<!-- core-payload-level:4 -->

이 디렉터리 자체의 입력은 없고, `cases.json`이 소비 시험에 합성 claim·수락/ack 유실·retry/stale lease 사례와 기대 결과를 제공합니다.

###### Security Boundary
<!-- core-payload-level:4 -->

없음: UUID·run ID·주소는 합성이며 credential·token을 담지 않고 네트워크 리스너도 없습니다.

#### Usage

##### Prerequisites

별도 런타임이나 이미지가 없습니다. `cases.json`은 전용 Python 상태 시험과 제한된 SMTP node 시험이 읽는 JSON 데이터입니다.

##### Selected Start

전용 Python 상태 시험과 제한된 SMTP node 시험에서 사용합니다. malformed·다중 claim·header injection·
수락 목록·timeout·취소와 원문 오류 누출도 각각 부정 사례로 검사합니다.
lease 만료·동시 claim·attempt cap/dead·공식 requeue는 실제 SQL/native 시험에서 별도
검증합니다. SQL007은 개별 승인마다 한 번의 no-send 추가 claim과 복원 sending의 unknown
격리를 제공하지만 이 fixture 목록 자체가 실제 SQL·SMTP 검증은 아닙니다.

#### Checks

##### Readiness

독립 실행 검사는 없습니다. 이 fixture를 읽는 전용 Python 상태 시험과 [SMTP node 시험](../nodes/OpsflowSmtp/tests/README.md)이 검사 경로입니다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [워크로드](../README.md)
- [초안 계약](../outbox-contract.json)

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 데이터 파일이라 헬스체크·지표가 없고 복구할 상태도 없습니다. 사례가 어긋나면 이를 읽는 시험이 실패하며, 복구는 Git 이력에서 파일 변경을 되돌리는 것입니다.

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
