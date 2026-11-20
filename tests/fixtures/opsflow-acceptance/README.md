---
title: "Opsflow acceptance synthetic fixtures"
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

# Opsflow 수용 계약 합성 입력

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

기존 P04 게시 adapter와 P05 통지 계약을 연결하는 오프라인 시험 입력입니다.
소스 revision과 내용 hash는 합성 문자열이며 실제 원문 검증 결과가 아닙니다.

###### Scope
<!-- core-payload-level:4 -->

SDK·driver는 기존 시험 double을 재사용합니다. PostgreSQL·S3·Airflow·n8n·SMTP에
접속하지 않으며 DB claim·발송·복원·운영 권한을 모의 구현하지 않습니다.
P05 결과 함수는 기존 합성 oracle이며 실제 lease·outbox 상태의 증거가 아닙니다.
Wiki·학습 앱·LAB runtime은 대상에 포함하지 않습니다.

###### Structure
<!-- core-payload-level:4 -->

- `manifest.valid.json`: 합성 문서 한 건과 결정적인 게시 identity 입력.
- `cases.json`: 경로·partition 거부, ack 유실·잘못된 receipt·재시도 경계.
  UUID와 숫자는 합성 caller 입력이며 실제 lease나 소비자 식별자가 아닙니다.

##### Interfaces

###### Inputs and Outputs
<!-- core-payload-level:4 -->

입력은 `manifest.valid.json`(합성 문서 한 건과 게시 identity 입력)과 `cases.json`(경로·partition 거부, ack 유실, 잘못된 receipt, 재시도 경계)이며 실제 서비스 출력은 없다.

###### Security Boundary
<!-- core-payload-level:4 -->

소스 revision과 내용 hash는 합성 문자열이고 UUID와 숫자는 합성 caller 입력이다. 실제 DB, S3, SMTP 접속과 secret이 없다.

#### Usage

##### Prerequisites

기존 Python 시험 double을 재사용하는 오프라인 시험 입력이며 PostgreSQL, S3, Airflow, n8n, SMTP에 접속하지 않는다.

##### Selected Start

저장소 root에서 실행합니다.

```sh
python3 -m unittest tests.validation.test_opsflow_e2e_acceptance -v
```

조건부 객체 생성·readback 후 게시, DB 실패 뒤 객체 보존·재사용, 게시 identity의
다섯 필드 통지 projection, 성공을 허용하지 않는 실패 결과와 필수 CI 등록을
검증합니다. 잘못된 객체 내용이 있어도 덮어쓰지 않고 게시를 차단합니다.
현재 native binding이 비어 있으면 합성 게시 성공 이후에도 native 실행은 보류됩니다.

#### Checks

##### Readiness

검증은 Selected Start의 저장소 root 시험으로 수행하며 합성 oracle 통과는 실제 lease·outbox 상태의 증거가 아니다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [합성 fixture family](../README.md)
- [P04 배치](../../../infra/07-workflow/airflow/workloads/manifest-pipeline/README.md)
- [P05 통지](../../../infra/07-workflow/n8n/workloads/manifest-outbox-notifier/README.md)
- [문서 탐색](../../../docs/README.md): 진행 정본은 `SPEC-0204-TSK-0016`입니다.

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
