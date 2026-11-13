---
title: "Manifest Pipeline Synthetic Fixtures"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# Manifest Pipeline Synthetic Fixtures

## Purpose

### Service Role

#### Overview

외부 원문·실제 자격 증명이 없는 공개 합성 예시입니다.

#### Scope

Manifest hash는 형식 시험용이며 Git/content authenticity를 증명하지 않습니다.
접속 예시의 null credential은 보호된 worker 파일에서만 실제 제공해야 합니다.

#### Structure

- [2026-10-10.json](2026-10-10.json): 초기 source/UTC date의 합성 문서 목록.
- [pg-connection.example.json](pg-connection.example.json): ingest 전용 PG 설정 모양.
- [s3-connection.example.json](s3-connection.example.json): 전용 bucket·prefix 설정 모양.

### Supported Environment

없음: 이 폴더는 공개 합성 데이터와 값 없는 접속 예시만 포함하며 런타임을 선언하지 않는다. 포함 항목은 `2026-10-10.json`, `pg-connection.example.json`, `s3-connection.example.json`이다.

## Interfaces

### Inputs and Outputs

`2026-10-10.json`은 합성 manifest이고, `pg-connection.example.json`과 `s3-connection.example.json`은 접속 파일 형식의 값 없는 예시이다. 자체 포트는 없다.

### Security Boundary

접속 예시에는 자격 증명 값을 두지 않으며 실제 `pg.json`, `s3.json`은 worker 전용 보호 폴더(`OPSFLOW_SECRET_DIR`)에서 주입한다.

## Development

### Local Workflow

#### Usage

합성시험만 수행하며 게시 prefix 업로드는 W38 검토 후의 별도 동작입니다.
Null 값을 실제 비밀로 채운 파일을 Git·argv·env export·출력에 남기지 않습니다.

### Checks

없음: 이 폴더 자체의 검사 명령은 없다.

## Operations

### Runbook Links

이 서비스의 런북은 다음과 같다.

- RUN-0050: `docs/05.operations/runbooks/08-workflows-and-automation/0050-airflow.md`

#### Related Documents

- [배치](../README.md)
- [Adapter](../workflow_lib/README.md)

### Observability and Recovery

없음: 정적 fixture이며 헬스체크나 관측 대상이 없다.
