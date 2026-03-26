# Keycloak System Guide

> Identity and Access Management (IAM) & SSO Provider (02-auth)

---

## Overview (KR)

이 문서는 `hy-home.docker` 플랫폼의 핵심 인증 엔진인 Keycloak에 대한 시스템 가이드다. Keycloak은 Quarkus 기반의 오픈소스 IAM(Identity and Access Management) 솔루션으로, 플랫폼 전반의 사용자 인증, 권한 부여, SSO(Single Sign-On)를 담당한다.

## Guide Type

`system-guide`

## Target Audience

- **Developers**: 애플리케이션 인증 연동 및 OIDC 클라이언트 설정
- **Operators**: Keycloak 인스턴스 관리, 렐름 구성, 보안 정책 수립
- **Agent-tuner**: 인증 흐름 자동화 및 보안 감사 모니터링

## Purpose

Keycloak 시스템의 아키텍처를 이해하고, 초기 구축부터 서비스 연동, 운영 유지보수에 필요한 지식을 습득한다.

## Prerequisites

- **Gateway**: `infra/01-gateway` (Traefik) 서비스가 정상 가동 중이어야 함.
- **Database**: `infra/04-data/mng-db` (PostgreSQL) 서비스가 필요함.
- **Secrets**: `scripts/gen-secrets.sh`를 통해 `keycloak_admin_user`, `keycloak_admin_password`, `keycloak_db_password`가 생성되어야 함.

## Step-by-step Instructions

### 1. 서비스 실행 및 초기 확인

```bash
cd infra/02-auth/keycloak
docker compose up -d
```

- `https://keycloak.${DEFAULT_URL}` 접속 및 관리자 로그인 확인.

### 2. 하이브리드 빌드 (Custom Extensions)

이 프로젝트는 `Dockerfile`을 통해 최적화된 Keycloak 이미지를 빌드한다.

- **Self-signed Certs**: 내부 통신용 keystore 자동 생성.
- **Providers**: `providers/` 디렉터리에 JAR 파일을 배치하여 기능을 확장 가능.
- **Themes**: `themes/` 디렉터리에 사용자 정의 UI 테마 배포 가능.

### 3. 주요 설정 항목 (conf/)

- `keycloak.conf`: Quarkus 기반 설정 (HTTP/HTTPS, Proxy mode, Database 등).
- `docker-compose.yml`: 리소스 제한, 네트워크 및 볼륨 바인딩 정의.

## Common Pitfalls

- **Proxy Mode**: Traefik 뒤에서 작동하므로 `KC_PROXY=edge` (또는 Quarkus 설정에 따른 `KC_PROXY_HEADERS=xforwarded`) 설정이 필수적임.

- **Database Connectivity**: PostgreSQL 시작 전 Keycloak이 실행될 경우 연결 실패가 발생할 수 있으므로 `depends_on` 및 healthcheck 확인 필수.
- **Cookie Security**: HTTPS 환경에서 `Secure` 속성 누락 시 인증 루프가 발생할 수 있음.

## Related Documents

- **Spec**: `[../../04.specs/02-auth/spec.md]`
- **Operation**: `[../../08.operations/02-auth/keycloak.md]`
- **Runbook**: `[../../09.runbooks/02-auth/keycloak.md]`
