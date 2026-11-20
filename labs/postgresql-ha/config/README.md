---
title: "PostgreSQL HA LAB 설정"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2026-10-12"
---

# PostgreSQL HA LAB 설정

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

HAProxy의 비밀값 없는 template와 LAB 전용 Prometheus 경보 규칙을 보관합니다. service 정의는 상위 [docker-compose.yml](../docker-compose.yml)에 있으며 실제 실행·비밀값·데이터를
이 문서나 source 이동으로 변경하지 않습니다.

###### Audience
<!-- core-payload-level:4 -->

LAB source 관리자와 정적 검토자입니다.

###### Scope
<!-- core-payload-level:4 -->

추적된 source의 위치와 소비 관계만 설명합니다. 실제 기동, 초기화, 삭제, 회전과
복구는 승인된 별도 실행 범위를 요구합니다. HOME 자료를 소비하거나 수정하지 않습니다.

###### Structure
<!-- core-payload-level:4 -->

- [haproxy.cfg.tpl](haproxy.cfg.tpl): LAB router가 runtime secret reference로 렌더하는 template입니다.
- [prometheus-alert-rules.yml](prometheus-alert-rules.yml): 복제 지연 경보 등 LAB 전용 Prometheus 규칙입니다. HOME Prometheus는 읽지 않으며, LAB 관측 계약이 승인되면 그 LAB의 Prometheus가 읽습니다.

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| `haproxy.cfg.tpl` | 이 디렉터리 | LAB router | runtime secret reference로 렌더하는 비밀값 없는 template이다. | 실행과 복구는 RUN-0031 PostgreSQL 클러스터 Runbook을 따른다. |
| `prometheus-alert-rules.yml` | 이 디렉터리 | LAB 관측 계약 승인 후 그 LAB의 Prometheus | 복제 지연 경보 등 LAB 전용 규칙이며 HOME Prometheus는 읽지 않는다. | 실행과 복구는 RUN-0031 PostgreSQL 클러스터 Runbook을 따른다. |

###### Inputs and Outputs
<!-- core-payload-level:4 -->

상위 LAB Compose와 wrapper의 기존 변수·secret reference·volume·network 계약을
보존합니다. 비밀값이나 실제 `.env`를 이 디렉터리에 저장하지 않습니다.

###### Security Boundary
<!-- core-payload-level:4 -->

이 디렉터리에는 비밀값과 실제 `.env`를 저장하지 않으며 포트 게시와 network 선언이 없다. 비밀은 상위 LAB Compose의 secret reference로만 전달된다.

#### Usage

##### Prerequisites

없음: 이 디렉터리는 실행 환경이 없는 source 조각이다. 소비하는 Compose와 런타임 버전은 상위 LAB이 소유한다.

##### Selected Start

source와 소비하는 Compose를 함께 검토하며 실행 entrypoint는 상위 LAB 안내를
따릅니다.

#### Checks

##### Readiness

정적 구성 검사는 source 경로와 참조만 검증합니다. runtime 성공이나 복구를
입증하지 않습니다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [상위 LAB source](../README.md)

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 이 디렉터리는 전용 런북이 없는 설정 조각이며 상위 LAB의 런북을 따른다. 실행과 복구는 [상위 LAB README](../README.md)와 [15-labs runbooks](../../../docs/05.operations/03.runbooks/15.labs/README.md)의 RUN-0031 PostgreSQL 클러스터 Runbook를 따른다.

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
