# 02-Auth OAuth2 Proxy Operations Policy

## Overview (KR)

이 문서는 `02-auth` OAuth2 Proxy 운영 정책을 정의한다. 시크릿 주입 경로, 세션/쿠키 표준, fail-closed 및 degraded-mode 운영 통제를 명시한다.

## Policy Scope

- `infra/02-auth/oauth2-proxy/docker-compose.yml`
- `infra/02-auth/oauth2-proxy/docker-entrypoint.sh`
- `infra/02-auth/oauth2-proxy/Dockerfile`
- `infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg`

## Applies To

- **Systems**: OAuth2 Proxy ForwardAuth gateway
- **Agents**: Infra/DevOps/Ops agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - 서비스는 `template-infra-readonly-med`를 사용해야 한다.
  - 런타임 시크릿 주입은 엔트리포인트 스크립트에서 `/run/secrets` 파일로 처리한다.
  - 이미지 실행 계정은 non-root(`oauth2proxy`)여야 한다.
  - 세션 정책은 `cookie_secure=true`, `cookie_httponly=true`, `cookie_samesite=lax`, `cookie_refresh=1h`, `cookie_expire=12h`를 유지한다.
  - 기본 운영 모드는 fail-closed다.
- **Allowed**:
  - 운영 승인 하에 degraded-mode를 제한적으로 수행(원복 절차 필수)
  - 환경별 도메인 변수(`DEFAULT_URL`) 조정
- **Disallowed**:
  - fail-open 상시 운영
  - 시크릿을 Compose/문서에 평문으로 저장

## Exceptions

- OIDC 공급자 장애가 장기화될 때 한시적 degraded-mode 허용 가능.
- 단, 승인자 기록과 종료 조건(원복 기준)을 사전에 명시해야 한다.

## Verification

- `bash scripts/check-auth-hardening.sh`
- `docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml config`
- `docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ping`

## Review Cadence

- 월 1회 정기 점검
- OAuth2 Proxy/Keycloak 버전 변경 시 수시 점검

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: N/A
- **Eval / Guardrail Threshold**: auth-hardening 스크립트 실패 0건
- **Log / Trace Retention**: 인증 요청/에러 로그는 관측성 보존 정책 준수
- **Safety Incident Thresholds**: 로그인 루프, 콜백 실패 급증, `/ping` 실패 지속 시 런북 수행

## Related Documents

- **Plan**: [../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md](../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- **Task**: [../../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)
- **Spec**: [../../04.specs/02-auth/spec.md](../../04.specs/02-auth/spec.md)
- **Runbook**: [../../09.runbooks/02-auth/oauth2-proxy.md](../../09.runbooks/02-auth/oauth2-proxy.md)
- **Guide**: [../../07.guides/02-auth/oauth2-proxy.md](../../07.guides/02-auth/oauth2-proxy.md)
