---
title: "Manifest Pipeline Synthetic Fixtures"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
---

# Manifest Pipeline Synthetic Fixtures

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

외부 원문·실제 자격 증명이 없는 공개 합성 예시입니다.

###### Scope
<!-- core-payload-level:4 -->

Manifest hash는 형식 시험용이며 Git/content authenticity를 증명하지 않습니다.
접속 예시의 null credential은 보호된 worker 파일에서만 실제 제공해야 합니다.

###### Structure
<!-- core-payload-level:4 -->

- [2026-10-10.json](2026-10-10.json): 초기 source/UTC date의 합성 문서 목록.
- [pg-connection.example.json](pg-connection.example.json): ingest 전용 PG 설정 모양.
- [s3-connection.example.json](s3-connection.example.json): 전용 bucket·prefix 설정 모양.

##### Interfaces

###### Inputs and Outputs
<!-- core-payload-level:4 -->

`2026-10-10.json`은 합성 manifest이고, `pg-connection.example.json`과 `s3-connection.example.json`은 접속 파일 형식의 값 없는 예시이다. 자체 포트는 없다.

###### Security Boundary
<!-- core-payload-level:4 -->

접속 예시에는 자격 증명 값을 두지 않으며 실제 `pg.json`, `s3.json`은 worker 전용 보호 폴더(`OPSFLOW_SECRET_DIR`)에서 주입한다.

#### Usage

##### Prerequisites

없음: 이 폴더는 공개 합성 데이터와 값 없는 접속 예시만 포함하며 런타임을 선언하지 않는다. 포함 항목은 `2026-10-10.json`, `pg-connection.example.json`, `s3-connection.example.json`이다.

##### Selected Start

###### Usage
<!-- core-payload-level:4 -->

합성시험만 수행하며 게시 prefix 업로드는 W38 검토 후의 별도 동작입니다.
Null 값을 실제 비밀로 채운 파일을 Git·argv·env export·출력에 남기지 않습니다.

#### Checks

##### Readiness

없음: 이 폴더 자체의 검사 명령은 없다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

이 서비스의 런북은 다음과 같다.

- RUN-0050: `docs/05.operations/03.runbooks/08.workflows-and-automation/0050-airflow.md`

###### Related Documents
<!-- core-payload-level:4 -->

- [배치](../README.md)
- [Adapter](../workflow_lib/README.md)

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 정적 fixture이며 헬스체크나 관측 대상이 없다.

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
