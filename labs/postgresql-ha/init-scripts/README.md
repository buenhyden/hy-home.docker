---
title: "PostgreSQL HA LAB 초기화 SQL"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
created: "2026-10-12"
---

# PostgreSQL HA LAB 초기화 SQL

## Purpose

### Service Role

LAB의 초기화와 복구 의존성이 있는 SQL source를 보관합니다. service 정의는 상위 [docker-compose.yml](../docker-compose.yml)에 있으며 실제 실행·비밀값·데이터를
이 문서나 source 이동으로 변경하지 않습니다.

#### Audience

LAB source 관리자와 정적 검토자입니다.

#### Scope

추적된 source의 위치와 소비 관계만 설명합니다. 실제 기동, 초기화, 삭제, 회전과
복구는 승인된 별도 실행 범위를 요구합니다. HOME 자료를 소비하거나 수정하지 않습니다.

#### Structure

- [init_users_dbs.sql](init_users_dbs.sql): 기존 LAB role·database 초기화 입력입니다. 미사용 자료로 삭제하지 않습니다.

### Supported Environment

없음: 이 디렉터리는 실행 환경이 없는 source 조각이다. 소비하는 Compose와 런타임 버전은 상위 LAB이 소유한다.

## Interfaces

### Inputs and Outputs

상위 LAB Compose와 wrapper의 기존 변수·secret reference·volume·network 계약을
보존합니다. 비밀값이나 실제 `.env`를 이 디렉터리에 저장하지 않습니다.

### Security Boundary

이 디렉터리에는 비밀값과 실제 `.env`를 저장하지 않으며 포트 게시와 network 선언이 없다. 비밀은 상위 LAB Compose의 secret reference로만 전달된다.

## Development

### Local Workflow

source와 소비하는 Compose를 함께 검토하며 실행 entrypoint는 상위 LAB 안내를
따릅니다.

### Checks

정적 구성 검사는 source 경로와 참조만 검증합니다. runtime 성공이나 복구를
입증하지 않습니다.

## Operations

### Runbook Links

- [상위 LAB source](../README.md)

### Observability and Recovery

없음: 이 디렉터리는 전용 런북이 없는 설정 조각이며 상위 LAB의 런북을 따른다. 실행과 복구는 [상위 LAB README](../README.md)와 [15-labs runbooks](../../../docs/05.operations/runbooks/15-labs/README.md)의 RUN-0031 PostgreSQL 클러스터 Runbook를 따른다.
