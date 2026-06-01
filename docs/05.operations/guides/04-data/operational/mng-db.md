---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/operational/mng-db.md -->

# Management Database Usage Guide

## Usage

### Overview (KR)

이 문서는 `mng-db` (Management Database) 시스템에 대한 가이드다. `mng-db`는 플랫폼 핵심 서비스(Identity, Automation, Workflow 등)의 메타데이타를 관리하는 PostgreSQL 및 Valkey 인스턴스로 구성되어 있다.
>
> This document explains how to understand and use the Management Database system.

---

### Common Pitfalls

- guide에 policy control이나 복구 절차를 직접 섞어 목적 프로파일을 흐리는 경우
- target-relative link를 템플릿 위치 기준으로 계산하는 경우
- 검증 명령 실행 결과 없이 운영 가능 상태를 단정하는 경우

### Usage Type

`system-guide`

### Target Audience

- **Developers**: 플랫폼 서비스 개발 및 DB 연동
- **Operators**: 초기 부트스트랩 및 서비스 상태 가이드 점검
- **AI Agents**: 하위 시스템 의존성 분석

### Purpose

이 가이드는 사용자가 `mng-db`의 구조를 이해하고, 제공되는 각 데이타베이스에 안전하게 연결 및 활용하는 것을 돕는다.

### Prerequisites

- **Docker & Docker Compose**: 로컬 또는 인프라 노드에서 실행 환경 필요.
- **psql / valkey-cli**: 데이타베이스 접속을 위한 클라이언트 도구.
- **Credentials**: `/run/secrets/` 또는 환경 변수에 설정된 패스워드 정보.

### Step-by-step Instructions

#### 1. 서비스 가동 및 상태 확인

`mng-db`는 플랫폼 초기화 시 가장 먼저 가동되어야 하는 서비스 중 하나이다.

```bash

## infra/04-data/operational/mng-db 경로에서 실행
docker-compose up -d
docker-compose ps
```

### 2. PostgreSQL 데이타베이스 접근

`mng-pg` 인스턴스 내에는 다음과 같은 논리적 데이타베이스가 생성된다.

- `postgres`: 관리용 루트 DB
- `n8n`: 워크플로우 자동화용
- `keycloak`: 자격 증명 관리용
Copyright (c) 2026. Licensed under the MIT License.

---

### Common Pitfalls

- guide 문서에 운영 정책이나 incident timeline을 섞지 않는다.
- secret 값, token, 인증서 원문을 열람하거나 문서화하지 않는다.
- runtime 변경이 필요한 경우 문서 보강과 별도 작업으로 분리한다.

## Common Checks

- Step-by-step Instructions 의 검증 단계를 따른다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../../runbooks/04-data/operational/mng-db.md)을 따른다.

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/04-data/operational/mng-db.md)
- [Recovery runbook](../../../runbooks/04-data/operational/mng-db.md)
