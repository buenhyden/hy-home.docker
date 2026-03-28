# 02-Auth Keycloak Guide

## Overview (KR)

이 문서는 `02-auth`의 Keycloak 운영 구성 방법을 설명한다. DB/관리자 시크릿 주입 방식, 헬스체크 점검, OIDC 클라이언트 정합 확인 절차를 중심으로 다룬다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Infra/DevOps Engineers
- Operators
- Contributors

## Purpose

- Keycloak의 시크릿/헬스체크 계약을 안정적으로 유지한다.
- OAuth2 Proxy 연동을 위한 OIDC issuer/redirect 정합성을 보장한다.

## Prerequisites

- Docker/Docker Compose 사용 가능
- `infra/02-auth/keycloak/docker-compose.yml` 접근 가능
- `mng-pg` 서비스 준비됨

## Step-by-step Instructions

1. Compose 설정 확인
   - `service: template-infra-med` 적용 여부 확인
   - `KC_DB_PASSWORD_FILE`, `keycloak_db_password`, `keycloak_admin_password` 연결 확인
2. 헬스체크 계약 확인
   - 관리 포트 readiness 체크(`/health/ready`) 설정 확인
3. OIDC 발급자 URL 확인
   - Realm issuer와 OAuth2 Proxy `OAUTH2_PROXY_OIDC_ISSUER_URL`가 동일한 도메인 규칙을 따르는지 확인
4. 정적 검증
   - `docker compose -f infra/02-auth/keycloak/docker-compose.yml config`
   - `bash scripts/check-auth-hardening.sh`

## Common Pitfalls

- Keycloak realm URL과 OAuth2 Proxy issuer URL 불일치
- DB 시크릿 파일 경로 오타
- 초기 기동 시간보다 짧은 헬스체크 판단으로 인한 오탐

## Related Documents

- **Spec**: [../../04.specs/02-auth/spec.md](../../04.specs/02-auth/spec.md)
- **Operation**: [../../08.operations/02-auth/keycloak.md](../../08.operations/02-auth/keycloak.md)
- **Runbook**: [../../09.runbooks/02-auth/keycloak.md](../../09.runbooks/02-auth/keycloak.md)
- **Plan**: [../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md](../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)
