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

외부 원문·실제 자격 증명이 없는 공개 합성 예시입니다.

Manifest hash는 형식 시험용이며 Git/content authenticity를 증명하지 않습니다.
접속 예시의 null credential은 보호된 worker 파일에서만 실제 제공해야 합니다.

#### Structure

- [2026-10-10.json](2026-10-10.json): 초기 source/UTC date의 합성 문서 목록.
- [pg-connection.example.json](pg-connection.example.json): ingest 전용 PG 설정 모양.
- [s3-connection.example.json](s3-connection.example.json): 전용 bucket·prefix 설정 모양.

### Supported Environment

없음: 이 디렉터리에는 Compose 파일이나 Dockerfile이 없어 독립 런타임 환경을 선언하지 않는다. 포함 항목은 `2026-10-10.json`, `pg-connection.example.json`, `s3-connection.example.json`이다.

## Interfaces

### Inputs and Outputs

없음: 이 폴더는 자체 포트나 네트워크 인터페이스를 선언하지 않으며 `2026-10-10.json`, `pg-connection.example.json`, `s3-connection.example.json`만 둔다.

### Security Boundary

없음: 이 폴더에는 Compose 서비스와 secret 정의가 없으며, secret 값을 저장소에 두지 않는다.

## Development

### Local Workflow

합성시험만 수행하며 게시 prefix 업로드는 W38 검토 후의 별도 동작입니다.
Null 값을 실제 비밀로 채운 파일을 Git·argv·env export·출력에 남기지 않습니다.

### Checks

없음: 이 폴더는 자체 테스트나 검증 스크립트를 두지 않는다.

## Operations

### Runbook Links

#### Related Documents

- [배치](../README.md)
- [Adapter](../workflow_lib/README.md)

### Observability and Recovery

없음: 이 폴더에는 헬스체크나 관측 대상 선언이 없다.
