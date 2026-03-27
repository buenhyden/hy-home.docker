# Management Database (mng-db) Guide

> This document explains how to understand and use the Management Database system.

---

## Overview (KR)

이 문서는 `mng-db` (Management Database) 시스템에 대한 가이드다. `mng-db`는 플랫폼 핵심 서비스(Identity, Automation, Workflow 등)의 메타데이타를 관리하는 PostgreSQL 및 Valkey 인스턴스로 구성되어 있다.

## Guide Type

`system-guide`

## Target Audience

- **Developers**: 플랫폼 서비스 개발 및 DB 연동
- **Operators**: 초기 부트스트랩 및 서비스 상태 가이드 점검
- **AI Agents**: 하위 시스템 의존성 분석

## Purpose

이 가이드는 사용자가 `mng-db`의 구조를 이해하고, 제공되는 각 데이타베이스에 안전하게 연결 및 활용하는 것을 돕는다.

## Prerequisites

- **Docker & Docker Compose**: 로컬 또는 인프라 노드에서 실행 환경 필요.
- **psql / valkey-cli**: 데이타베이스 접속을 위한 클라이언트 도구.
- **Credentials**: `/run/secrets/` 또는 환경 변수에 설정된 패스워드 정보.

## Step-by-step Instructions

### 1. 서비스 가동 및 상태 확인
`mng-db`는 플랫폼 초기화 시 가장 먼저 가동되어야 하는 서비스 중 하나이다.
```bash
# infra/04-data/operational/mng-db 경로에서 실행
docker-compose up -d
docker-compose ps
```

### 2. PostgreSQL 데이타베이스 접근
`mng-pg` 인스턴스 내에는 다음과 같은 논리적 데이타베이스가 생성된다.
- `postgres`: 관리용 루트 DB
- `n8n`: 워크플로우 자동화용
- `keycloak`: 자격 증명 관리용
- `airflow`: 작업 스케줄링용
- `terrakube`: 인프라 관리용
- `sonarqube`: 코드 품질 분석용

접속 예시:
```bash
docker exec -it mng-pg psql -U ${POSTGRES_DEFAULT_USER} -d keycloak
```

### 3. Valkey 캐시 활용
플랫폼 서비스의 빠른 데이타 접근을 위해 공유 캐시를 제공한다.
```bash
docker exec -it mng-valkey valkey-cli -a ${VALKEY_PASSWORD}
```

## Common Pitfalls

- **Persistence**: 바인드 마운트 경로(`${DEFAULT_MANAGEMENT_DIR}`)가 올바르지 않으면 데이타가 유실될 수 있다.
- **Initialization**: `mng-pg-init`은 한 번만 실행되도록 설계되어 있으나, DB가 이미 존재하면 스킵한다.
- **Resource Constraints**: 단일 노드 구성이므로 대규모 트래픽 발생 시 성능 저하가 올바른 아키텍처적 경고(Cluster 사용 권장)로 이어져야 한다.

## Related Documents

- **ARD**: [../02.ard/0004-data-architecture.md](../../../02.ard/0004-data-architecture.md)
- **Spec**: [../04.specs/04-data/spec.md](../../../04.specs/04-data/spec.md)
- **Operation**: [../08.operations/04-data/operational/mng-db.md](../../../08.operations/04-data/operational/mng-db.md)
- **Runbook**: [../09.runbooks/04-data/operational/mng-db.md](../../../09.runbooks/04-data/operational/mng-db.md)
