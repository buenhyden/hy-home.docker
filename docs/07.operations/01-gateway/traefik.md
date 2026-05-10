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
- **Procedure**: [../../07.operations/01-gateway/traefik.md](../../07.operations/01-gateway/traefik.md)
- **Usage**: [../../07.operations/01-gateway/traefik.md](../../07.operations/01-gateway/traefik.md)

## Usage

> Migrated from `docs/07.operations/01-gateway/traefik.md` during the 2026-05-10 operations taxonomy consolidation.

### 01-Gateway Traefik Usage

#### Overview (KR)

이 문서는 `Traefik Primary` 모델에서 01-gateway 소유 라우터를 운영하는 방법을 설명한다. 표준 미들웨어 체인 적용과 검증 흐름을 중심으로 다룬다.

#### Usage Type

`system-guide | how-to`

#### Target Audience

- Infra/DevOps Engineers
- Operators
- Contributors

#### Purpose

- Traefik dashboard 라우터 하드닝 정책을 일관되게 적용한다.
- `gateway-standard-chain` 구성요소와 적용 범위를 이해한다.

#### Prerequisites

- Docker/Docker Compose 사용 가능
- `infra/01-gateway/traefik` 구성 파일 접근 가능
- `scripts/check-gateway-hardening.sh` 실행 가능

#### Step-by-step Instructions

1. 미들웨어 파일 확인
   - `infra/01-gateway/traefik/dynamic/middleware.yml`
   - 필수 블록 확인: `req-rate-limit`, `req-retry`, `req-circuit-breaker`, `gateway-standard-chain`
2. 라우터 라벨 확인
   - `infra/01-gateway/traefik/docker-compose.yml`
   - dashboard 라우터에 `dashboard-auth@file,gateway-standard-chain@file` 적용 확인
3. 설정 정적 검증
   - `docker compose -f infra/01-gateway/traefik/docker-compose.yml config`
4. 하드닝 검증
   - `bash scripts/check-gateway-hardening.sh`

#### Common Pitfalls

- `gateway-standard-chain` 이름 오타로 middleware resolve 실패
- dashboard middleware 순서/구분자(`,`) 오류
- 비게이트웨이 소유 라우터까지 무분별하게 체인 확장 적용

#### Related Documents

- **Spec**: [../../04.specs/01-gateway/spec.md](../../04.specs/01-gateway/spec.md)
- **Operation**: [../../07.operations/01-gateway/traefik.md](../../07.operations/01-gateway/traefik.md)
- **Procedure**: [../../07.operations/01-gateway/traefik.md](../../07.operations/01-gateway/traefik.md)
- **Plan**: [../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md](../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md)

## Procedure

> Migrated from `docs/07.operations/01-gateway/traefik.md` during the 2026-05-10 operations taxonomy consolidation.

### 01-Gateway Traefik Procedure

: Traefik Primary Gateway Recovery

#### Overview (KR)

이 런북은 Traefik 미들웨어 회귀, dashboard 접근 장애, 라우팅 이상 상황에서 복구 절차를 정의한다.

#### Purpose

- `gateway-standard-chain` 회귀 시 신속 복구
- Dashboard 인증/접근 장애 진단
- Traefik 서비스 정상성 복원

#### Canonical References

- [Operations Policy](../../07.operations/01-gateway/traefik.md)
- [Plan](../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md)
- [Tasks](../../06.tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md)

#### When to Use

- dashboard 접근 실패(401 loop, 429 burst, 5xx)
- 미들웨어 체인 누락/오타/잘못된 순서
- Traefik healthcheck 실패

#### Procedure or Checklist

##### Checklist

- [ ] `docker compose -f infra/01-gateway/traefik/docker-compose.yml config` 성공
- [ ] `docker compose -f infra/01-gateway/traefik/docker-compose.yml ps`에서 상태 정상
- [ ] `bash scripts/check-gateway-hardening.sh` 실패 원인 확인

##### Procedure

1. 설정 검증
   - `bash scripts/check-gateway-hardening.sh`
   - `docker compose -f infra/01-gateway/traefik/docker-compose.yml config`
2. middleware 회귀 대응
   - `infra/01-gateway/traefik/dynamic/middleware.yml`에서 아래 4개 블록 존재 확인:
     - `req-rate-limit`
     - `req-retry`
     - `req-circuit-breaker`
     - `gateway-standard-chain`
3. dashboard 라우터 체인 확인
   - `infra/01-gateway/traefik/docker-compose.yml`의 dashboard middleware 라벨이
     `dashboard-auth@file,gateway-standard-chain@file`인지 확인
4. 서비스 재기동
   - `docker compose -f infra/01-gateway/traefik/docker-compose.yml up -d traefik`
5. 사후 확인
   - `docker compose -f infra/01-gateway/traefik/docker-compose.yml exec traefik traefik healthcheck --ping`

#### Verification Steps

- [ ] `bash scripts/check-gateway-hardening.sh` 통과
- [ ] dashboard 접근 시 BasicAuth 요구 및 인증 성공
- [ ] 기존 라우팅 규칙 회귀 없음

#### Observability and Evidence Sources

- **Signals**: Traefik healthcheck, gateway access/error logs
- **Evidence to Capture**:
  - `docker compose -f infra/01-gateway/traefik/docker-compose.yml logs --tail=200 traefik`
  - 검증 스크립트 출력

#### Safe Rollback or Recovery Procedure

- [ ] 직전 정상 커밋으로 `infra/01-gateway/traefik/*` 복원
- [ ] `docker compose -f infra/01-gateway/traefik/docker-compose.yml up -d traefik`
- [ ] 롤백 후 `check-gateway-hardening.sh` 재실행

#### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: `bash scripts/check-gateway-hardening.sh`
- **Trace Capture**: Traefik logs + CI job logs

#### Related Operational Documents

- **Usage**: [../../07.operations/01-gateway/traefik.md](../../07.operations/01-gateway/traefik.md)
- **Nginx Procedure**: [./nginx.md](./nginx.md)
