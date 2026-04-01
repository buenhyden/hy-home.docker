# 03-Security Vault Guide

## Overview (KR)

이 문서는 `03-security` Vault 운영/개발 가이드다. Vault Agent 템플릿 경로 규약, AppRole 부트스트랩, 렌더 출력 확인 절차를 중심으로 optimization/hardening 기준을 설명한다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Security Operators
- Infra/DevOps Engineers
- Service Developers

## Purpose

- `secret/data/hy-home/...` 시크릿 경로/키 계약을 일관되게 사용한다.
- Vault Agent 렌더링 결과를 서비스에 안전하게 연결한다.
- 하드닝 회귀를 사전 검증한다.

## Prerequisites

- `infra/03-security/vault` 구성 파일 접근
- Vault 초기화/Unseal 가능한 운영 권한
- AppRole RoleID/SecretID 발급 권한

## Step-by-step Instructions

1. Vault 기본 상태 확인
   - `docker compose -f infra/03-security/vault/docker-compose.yml config`
   - `docker compose -f infra/03-security/vault/docker-compose.yml up -d vault vault-agent`
   - `docker exec vault vault status`
2. AppRole bootstrap
   - `bash scripts/bootstrap-vault-approle.sh`를 실행하여 Agent 인증 및 접근 권한 설정
   - token sink(`/vault/agent/token`) 생성 확인
3. 시크릿 경로 규약 적용
   - `secret/data/hy-home/04-data/mng-db` -> `password`
   - `secret/data/hy-home/02-auth/keycloak` -> `db_password`, `admin_username`, `admin_password`
   - `secret/data/hy-home/02-auth/oauth2-proxy` -> `client_secret`, `cookie_secret`
   - `secret/data/hy-home/06-observability/grafana` -> `admin_password`, `db_password`, `grafana_client_secret`
4. 렌더 출력 확인
   - `docker exec vault-agent ls -la /vault/out`
   - 서비스별 파일 존재/권한(0600) 점검
5. 정적 하드닝 검증
   - `bash scripts/check-security-hardening.sh`
   - `bash scripts/check-template-security-baseline.sh`

## Common Pitfalls

- placeholder 경로(`secret/data/example`)를 템플릿에 남겨두는 실수
- KV 경로와 키 이름 불일치로 빈 렌더 파일 생성
- `role_id`/`secret_id` 누락으로 Agent 인증 실패

## Related Documents

- **Spec**: [../../04.specs/03-security/spec.md](../../04.specs/03-security/spec.md)
- **Plan**: [../../05.plans/2026-03-28-03-security-optimization-hardening-plan.md](../../05.plans/2026-03-28-03-security-optimization-hardening-plan.md)
- **Task**: [../../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- **Operation**: [../../08.operations/03-security/vault.md](../../08.operations/03-security/vault.md)
- **Runbook**: [../../09.runbooks/03-security/vault.md](../../09.runbooks/03-security/vault.md)
