---
title: "02-Auth OAuth2 Proxy Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-09"
layer: "operations"
artifact_id: "GDE-0015"
parent_ids:
- "POL-0015"
created: "2026-05-10"
---

# 02-Auth OAuth2 Proxy Usage Guide

## Usage

### Overview

이 문서는 OAuth2 Proxy를 `ForwardAuth` 표준으로 운영하는 방법을 설명한다. 시크릿 엔트리포인트 주입, non-root 실행, 도메인 파라미터화, 세션 정책 점검 절차를 포함한다.

### Usage Type

`system-guide | how-to`

### Target Audience

- Infra/DevOps Engineers
- Operators
- Contributors

### Purpose

- 인증 프록시를 표준 하드닝 상태로 유지한다.
- 신규 서비스의 SSO 연동 시 회귀를 줄인다.

### Prerequisites

- `infra/02-auth/keycloak` 정상 동작
- `infra/02-auth/oauth2-proxy` 구성 파일 접근
- 공유 `mng-valkey` 또는 `dedicated-valkey` profile의 `oauth2-proxy-valkey` 세션 저장소 준비
- 사용할 저장소에 맞는 `OAUTH2_PROXY_VALKEY_HOST` 및 이미지/entrypoint의 세션 시크릿
  경로 확인. Profile은 서비스를 추가할 뿐 Proxy의 기본 호스트나 이미지를 전환하지 않는다.
  공유 경로는 `dev.Dockerfile`/`docker-entrypoint.dev.sh`의 `mng_valkey_password`,
  전용 경로는 `Dockerfile`/`docker-entrypoint.sh`의 `oauth2_valkey_password`를 사용한다.
  이미지 선택은 기존 `OAUTH2_PROXY_DOCKERFILE` 구성에 따른다.

### Step-by-step Instructions

1. Compose 런타임 계약 확인
   - `template-infra-readonly-med` 사용
   - 기본 경로는 `docker-compose.yml`, `dev.Dockerfile`, `docker-entrypoint.dev.sh`, 공유 `mng-valkey`를 사용
   - `dedicated-valkey` profile은 같은 `docker-compose.yml`에서 `oauth2-proxy-valkey`와 그 exporter를 추가로 선택
   - command가 `--config /etc/oauth2-proxy.cfg`인지 확인
   - `OAUTH2_PROXY_OIDC_ISSUER_URL`, `OAUTH2_PROXY_REDIRECT_URL`, `OAUTH2_PROXY_COOKIE_DOMAINS`, `OAUTH2_PROXY_WHITELIST_DOMAINS` 확인
2. 엔트리포인트 시크릿 주입 확인
   - root-active `docker-entrypoint.dev.sh`에서 `mng_valkey_password`를 읽어 환경 변수에 export하는지 확인
   - local/full `docker-entrypoint.sh`에서 `oauth2_valkey_password`를 읽어 환경 변수에 export하는지 확인
3. 이미지 권한 모델 확인
   - local/full `Dockerfile`에서 UID 100/GID 101을 명시적으로 생성하고 `USER 100:101`을 적용하는지 확인
   - root-active `dev.Dockerfile`에서 `USER oauth2proxy:oauth2proxy`를 적용하는지 확인
4. 정적 검증
   - `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`
   - `bash scripts/hardening/check-all-hardening.sh 02-auth`

### Common Pitfalls

- `DEFAULT_URL`과 Keycloak realm/callback 도메인 불일치
- 세션 비밀 변경 후 기존 쿠키 재사용으로 인한 인증 실패
- `/ping` 헬스체크 통과 전 트래픽 유입

## Common Checks

- `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 02-auth`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](runbook.md)을 따른다.

## Traceability

- Declared parent: [02-Auth OAuth2 Proxy Operations Policy](policy.md) (`POL-0015`)
- Governing authority: [02-Auth Architecture Description](../../../../02.architecture/descriptions/0002-auth-architecture.md) (`AD-0002`)
- Subject peers: [Policy](policy.md) (`POL-0015`), [Runbook](runbook.md) (`RUN-0015`)

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](policy.md)
- [Recovery runbook](runbook.md)
