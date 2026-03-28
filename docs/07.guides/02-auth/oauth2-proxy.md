# 02-Auth OAuth2 Proxy Guide

## Overview (KR)

이 문서는 OAuth2 Proxy를 `ForwardAuth` 표준으로 운영하는 방법을 설명한다. 시크릿 엔트리포인트 주입, non-root 실행, 도메인 파라미터화, 세션 정책 점검 절차를 포함한다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Infra/DevOps Engineers
- Operators
- Contributors

## Purpose

- 인증 프록시를 표준 하드닝 상태로 유지한다.
- 신규 서비스의 SSO 연동 시 회귀를 줄인다.

## Prerequisites

- `infra/02-auth/keycloak` 정상 동작
- `infra/02-auth/oauth2-proxy` 구성 파일 접근
- `mng-valkey` 세션 저장소 준비

## Step-by-step Instructions

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
   - `bash scripts/check-auth-hardening.sh`

## Common Pitfalls

- `DEFAULT_URL`과 Keycloak realm/callback 도메인 불일치
- 세션 비밀 변경 후 기존 쿠키 재사용으로 인한 인증 실패
- `/ping` 헬스체크 통과 전 트래픽 유입

## Related Documents

- **Spec**: [../../04.specs/02-auth/spec.md](../../04.specs/02-auth/spec.md)
- **Operation**: [../../08.operations/02-auth/oauth2-proxy.md](../../08.operations/02-auth/oauth2-proxy.md)
- **Runbook**: [../../09.runbooks/02-auth/oauth2-proxy.md](../../09.runbooks/02-auth/oauth2-proxy.md)
- **Plan**: [../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md](../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)
