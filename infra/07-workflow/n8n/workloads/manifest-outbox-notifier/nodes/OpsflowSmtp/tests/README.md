---
title: "SMTP 노드 합성 회귀시험"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
---

# SMTP 노드 합성 회귀시험

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

닫힌 claim·credential 경계, 개인정보 제거, SMTP 불확실성과 socket 수명을
합성 fixture로 검증합니다.

###### Audience
<!-- core-payload-level:4 -->

P05 작성자와 code/security 검토자입니다.

###### Scope
<!-- core-payload-level:4 -->

기존 합성 시험과 새 owned loopback STARTTLS 시험을 구분합니다. 후자는 합성 CA·계정과
실제 Nodemailer를 사용하지만 n8n Worker·Mailpit native fixture나 실제 credential·DB를
사용하지 않습니다. 운영·실제 회전·복구 수용은 별도이며 과거 C19/C22를 취소하지 않습니다.

###### Structure
<!-- core-payload-level:4 -->

- [transport.test.cjs](transport.test.cjs): input/privacy/acceptance/deadline 계약.
- [adapter.test.cjs](adapter.test.cjs): 소유 socket의 연결 실패·취소·종료 경계.
- [protocol.test.cjs](protocol.test.cjs): 실제 Nodemailer와 메모리 Duplex SMTP byte.
- [starttls.test.cjs](starttls.test.cjs): 소유 loopback의 CA·이름·인증·downgrade·취소·응답 유실과 socket 정리.
- [node.test.cjs](node.test.cjs): 실제 workflow API 타입·오류와 합성 execution context.

##### Interfaces

###### Inputs and Outputs
<!-- core-payload-level:4 -->

합성 UUID capability와 공개 source/count/run fixture만 사용합니다.
기존 합성 소켓/응답과 STARTTLS의 실제 loopback 소켓은 서로 다른 시험 수준입니다.
양쪽 모두 외부 배달·운영 수신 증거가 아닙니다.

###### Security Boundary
<!-- core-payload-level:4 -->

시험은 자체 생성한 합성 CA·계정·UUID capability와 소유 loopback listener만 쓰며 실제 credential·DB·운영 인증 자료를 사용하지 않습니다.

#### Usage

##### Prerequisites

Node 내장 test/assert/mock timers와 정확히 locked library를 사용합니다.
STARTTLS 시험은 자체 생성 합성 인증서·계정과 소유 loopback listener를 정리합니다.
실제 서비스나 운영 인증 자료는 사용하지 않습니다.

##### Selected Start

accepted·unknown/rejected·응답 손실·취소를 재현합니다. lease/ack/retry의 실제
DB 동시성·복구 시험은 P04 계약 인계 이후 별도 native fixture에 연결합니다.

#### Checks

##### Readiness

부모 패키지에서 `npm run test:coverage`를 실행합니다. compiler build와 모든
시험이 성공하고 compiled source coverage gate가 통과해야 합니다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [노드 패키지](../README.md)
- [노드 탐색](../../README.md)

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 시험 패키지라 헬스체크·지표가 없습니다. 실패는 `npm run test:coverage` 출력과 coverage gate로 확인하며 복구는 Git 변경을 되돌리는 것입니다. 시험이 연 loopback listener와 socket은 시험이 정리합니다.

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
