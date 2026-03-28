# 01-Gateway Traefik Operations Policy

## Overview (KR)

이 문서는 `01-gateway`의 Traefik 운영 정책을 정의한다. 런타임 모델은 `Traefik Primary`이며, 표준 하드닝 강도는 `Balanced`다.

## Policy Scope

- `infra/01-gateway/traefik/docker-compose.yml`
- `infra/01-gateway/traefik/dynamic/middleware.yml`
- Gateway 소유 라우터(`dashboard` 등) 라벨 정책

## Applies To

- **Systems**: Traefik v3 (gateway tier)
- **Agents**: Infra/DevOps/Ops agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - Dashboard 라우터는 `dashboard-auth@file,gateway-standard-chain@file`를 사용해야 한다.
  - `gateway-standard-chain`은 `req-rate-limit`, `req-retry`, `req-circuit-breaker`를 포함해야 한다.
  - `req-rate-limit`은 기본값 `average=100`, `burst=50`을 유지한다.
  - `req-retry`는 `attempts=2`, `initialInterval=100ms`를 사용한다.
  - `req-circuit-breaker`는 `NetworkErrorRatio() > 0.30`을 사용한다.
  - Traefik 서비스는 readonly 템플릿(`template-infra-readonly-med`)을 사용한다.
- **Allowed**:
  - 신규 게이트웨이 소유 라우터에 동일 체인 적용
  - 운영 관측 결과 기반의 임계치 미세 조정(승인 후)
- **Disallowed**:
  - 비게이트웨이 소유 라우터에 전역 강제 적용
  - BasicAuth 제거 또는 평문 인증정보 사용

## Exceptions

- 비상 복구 시 임시 체인 우회 가능. 단, 사후에 원복 커밋과 변경 기록을 남겨야 한다.

## Verification

- `bash scripts/check-gateway-hardening.sh`
- `docker compose -f infra/01-gateway/traefik/docker-compose.yml config`
- `docker compose -f infra/01-gateway/traefik/docker-compose.yml exec traefik traefik healthcheck --ping`

## Review Cadence

- 월 1회 정기 점검
- Traefik 버전 변경/라우터 추가 시 수시 점검

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: N/A
- **Eval / Guardrail Threshold**: gateway-hardening 스크립트 실패 0건
- **Log / Trace Retention**: gateway access/error 로그는 observability 정책 준수
- **Safety Incident Thresholds**: 인증 루프, 대량 429, dashboard 접근 장애 발생 시 즉시 런북 절차 수행

## Related Documents

- **Plan**: [../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md](../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md)
- **Task**: [../../06.tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md)
- **Runbook**: [../../09.runbooks/01-gateway/traefik.md](../../09.runbooks/01-gateway/traefik.md)
- **Guide**: [../../07.guides/01-gateway/traefik.md](../../07.guides/01-gateway/traefik.md)
