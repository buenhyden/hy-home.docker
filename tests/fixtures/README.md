---
title: "Synthetic fixture family"
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

# 합성 fixture

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

독립 CLI·schema consumer가 공유하는 비밀값 없는 고정 입력입니다.

###### Audience
<!-- core-payload-level:4 -->

저장소 계약의 구현·검토 담당자입니다.

###### Scope
<!-- core-payload-level:4 -->

운영 secret·dotenv·인증자료·원문 로그는 보관하지 않습니다.

###### Structure
<!-- core-payload-level:4 -->

- [port-contract/](port-contract/README.md): P03 네 위치 포트 선언·합성 config 입력.
- [document_governance/](document_governance/README.md): 문서 경로·정체성 계약의
  비밀값 없는 합성 입력.

- [opsflow-acceptance/](opsflow-acceptance/README.md): P10 게시·통지 seam의
  오프라인 합성 수용 입력.

##### Interfaces

###### Inputs and Outputs
<!-- core-payload-level:4 -->

각 하위 README와 owning Task가 합성 입력의 의미와 허용 경계를 설명합니다.

###### Security Boundary
<!-- core-payload-level:4 -->

비밀값이 없는 고정 입력만 보관하며 운영 secret, dotenv, 인증자료, 원문 로그는 두지 않는다. 포트와 network 선언이 없다.

#### Usage

##### Prerequisites

기존 Python unit/contract 검증을 사용합니다.

##### Selected Start

각 consumer에 필요한 명명된 합성 입력만 선택합니다.

#### Checks

##### Readiness

[검증 진입점](../README.md)의 현재 등록된 시험 owner를 사용합니다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [Test surface](../README.md)

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
