---
title: "메시징 계층 (05-messaging)"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2025-11-12"
---

# 05 메시징

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

###### Overview
<!-- core-payload-level:4 -->

이 tier는 현재 [`kafka`](kafka/README.md) 패키지 하나를 포함합니다. OPTIONAL
Kafka-family 이벤트 스트리밍 surface이며 두 번째 broker family는 없습니다.

###### Audience
<!-- core-payload-level:4 -->

이 패키지 맵은 messaging tier의 operator와 maintainer를 위한 것입니다.

###### Scope
<!-- core-payload-level:4 -->

현재 Kafka 패키지와 그 루트 Compose selector를 다룹니다.

###### Structure
<!-- core-payload-level:4 -->

이 tier의 leaf 패키지는 [`kafka`](kafka/README.md) 하나입니다.

##### Interfaces

###### Configuration
<!-- core-payload-level:4 -->

루트 include는 정상 선택형 구성만 포함합니다.

###### Security Boundary
<!-- core-payload-level:4 -->

없음: 이 디렉터리는 Compose 서비스나 secret 참조를 직접 선언하지 않으며, 하위 `kafka/`가 각자 선언한다.

#### Usage

##### Prerequisites

###### Tech Stack
<!-- core-payload-level:4 -->

정상 Kafka와 주변 서비스의 이미지 선언은 [`kafka/`](kafka/README.md)가 소유합니다.

##### Selected Start

###### Usage
<!-- core-payload-level:4 -->

정확한 루트 selector는 `messaging`, `messaging-broker`,
`messaging-admin`입니다. 각 selector가 선택하는 서비스는 패키지 맵을
참고하십시오. 활성화 전에는 named producer/consumer, retention/capacity
계획, plaintext-listener 위험 수용, 완전한 복구 계획이 필요합니다.

#### Checks

##### Readiness

###### Validation
<!-- core-payload-level:4 -->

정상 선택자를 Compose 렌더로 확인하고, 실제 기동 결과는 별도로 기록합니다.

##### Failure Handling

###### Related Documents
<!-- core-payload-level:4 -->

[문서 진입점](../../docs/README.md)을 사용해 Stage 05 Messaging subject
`docs/05.operations/01.guides/06.messaging-and-cdc/0036-kafka.md`와
`docs/05.operations/01.guides/06.messaging-and-cdc/0037-messaging-optimization-hardening.md`을
찾으십시오.

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 이 디렉터리는 자체 헬스체크나 관측 대상을 선언하지 않으며, 하위 `kafka/`가 각자 선언한다.

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
