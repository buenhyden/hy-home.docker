---
status: active
---
<!-- Target: docs/05.operations/guides/02-auth/oauth2-proxy.md -->

# 02-Auth OAuth2 Proxy Usage Guide

## Usage

### Overview (KR)

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
- `mng-valkey` 세션 저장소 준비

### Step-by-step Instructions

1. Compose 런타임 계약 확인
   - `template-infra-readonly-med` 사용
   - command가 `--config /etc/oauth2-proxy.cfg`인지 확인
   - `OAUTH2_PROXY_OIDC_ISSUER_URL`, `OAUTH2_PROXY_REDIRECT_URL`, `OAUTH2_PROXY_COOKIE_DOMAINS`, `OAUTH2_PROXY_WHITELIST_DOMAINS` 확인
2. 엔트리포인트 시크릿 주입 확인
   - `docker-entrypoint.sh`에서 `oauth2_proxy_cookie_secret`, `oauth2_proxy_client_secret`, `mng_valkey_password`를 읽어 환경 변수에 export하는지 확인
3. 이미지 권한 모델 확인
   - Dockerfile의 `USER oauth2proxy:oauth2proxy` 적용 확인
4. 정적 검증
   - `docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml config`
   - `bash scripts/hardening/check-all-hardening.sh 02-auth`

### Common Pitfalls

- `DEFAULT_URL`과 Keycloak realm/callback 도메인 불일치
- 세션 비밀 변경 후 기존 쿠키 재사용으로 인한 인증 실패
- `/ping` 헬스체크 통과 전 트래픽 유입

## Common Checks

- `docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml config`
- `bash scripts/hardening/check-all-hardening.sh 02-auth`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/02-auth/oauth2-proxy.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/02-auth/oauth2-proxy.md)
- [Recovery runbook](../../runbooks/02-auth/oauth2-proxy.md)
