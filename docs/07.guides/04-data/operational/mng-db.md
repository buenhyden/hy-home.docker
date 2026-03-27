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
Copyright (c) 2026. Licensed under the MIT License.
