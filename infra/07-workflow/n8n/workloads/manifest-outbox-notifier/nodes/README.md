---
title: "제한된 manifest 통지 노드"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
---

# 제한된 manifest 통지 노드

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

manifest outbox의 개발 캡처 통지를 위한 credential-aware 노드 소스입니다.
이 폴더에는 공통 이미지·Compose·node 등록을 변경하는 설치기가 없습니다.

###### Audience
<!-- core-payload-level:4 -->

P05 작성자, SEC01 이미지 담당자, P03 접속 계약 담당자와 검토자입니다.

###### Scope
<!-- core-payload-level:4 -->

공개 소스와 합성 시험에 한정합니다. 설치 이미지 호환성, workflow import,
실제 DB·SMTP 통지·예약 실행·회전·복구는 `NOT_RUN`입니다.

###### Structure
<!-- core-payload-level:4 -->

- [OpsflowSmtp](OpsflowSmtp/README.md): 고정 캡처 대상과 닫힌 입력을 가진 노드 패키지.

##### Interfaces

###### Inputs and Outputs
<!-- core-payload-level:4 -->

실행 대상과 이미지 등록은 총괄·P03·SEC01의 통합 계약 이후 확정합니다.
공개 소스에 실제 credential ID·값·DB lease capability를 넣지 않습니다.

###### Security Boundary
<!-- core-payload-level:4 -->

공개 소스에 실제 credential ID·값·DB lease capability를 넣지 않습니다. 이 폴더에는 공통 이미지·Compose·node 등록을 바꾸는 설치기가 없어 운영 서비스에 영향을 주지 않으며, 접근 경계의 세부는 [노드 패키지](OpsflowSmtp/README.md)가 소유합니다.

#### Usage

##### Prerequisites

TypeScript, n8n native SMTP credential API와 Nodemailer를 사용합니다.
정확한 build dependency는 노드 패키지의 `package.json`과
`package-lock.json`이 소유하며 [패키지 안내](OpsflowSmtp/README.md)에서 확인합니다.

##### Selected Start

[노드 패키지 절차](OpsflowSmtp/README.md)를 통해 재현합니다.

#### Checks

##### Readiness

패키지의 합성 build·transport 시험을 실행합니다. 실제 서비스 접속 증거로
취급하지 않습니다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [workload](../README.md)
- [노드 패키지와 합성 시험 안내](OpsflowSmtp/README.md)

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 소스 폴더라 헬스체크·지표가 없고 설치 이미지·workflow import·실제 통지는 `NOT_RUN`입니다. 복구할 런타임 상태가 없으며 Git 변경을 되돌립니다.

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
