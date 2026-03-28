# 06-Observability Optimization Hardening Specification

## Overview (KR)

이 문서는 `infra/06-observability` 계층의 최적화/하드닝 구현 계약을 정의한다. 게이트웨이 경계(보안 헤더/SSO), health 기반 의존성, 호스트 수집기 헬스 신호, 커스텀 이미지 런타임 하드닝, CI 기준선 검증을 핵심 범위로 다룬다.

## Strategic Boundaries & Non-goals

- 본 Spec은 관측성 인프라의 관리 경로 하드닝과 운영/문서 추적성 계약을 소유한다.
- 애플리케이션 코드 계측(OTel SDK) 변경은 범위 밖이다.

## Related Inputs

- **PRD**: [../../01.prd/2026-03-28-06-observability-optimization-hardening.md](../../01.prd/2026-03-28-06-observability-optimization-hardening.md)
- **ARD**: [../../02.ard/0021-observability-optimization-hardening-architecture.md](../../02.ard/0021-observability-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../03.adr/0006-lgtm-stack-selection.md](../../03.adr/0006-lgtm-stack-selection.md)
  - [../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md](../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - 관측성 공개 라우터는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
  - Alloy/Grafana는 Loki/Tempo를 `service_healthy`로 의존한다.
  - cAdvisor는 `/healthz` healthcheck를 가진다.
- **Data / Interface Contract**:
  - 수집/저장/조회 트래픽은 `infra_net` 내부 경계를 기본으로 유지한다.
  - 관리 경로 외부 접근은 Traefik `websecure` 진입점에서 통제한다.
- **Governance Contract**:
  - `scripts/check-observability-hardening.sh`를 CI `observability-hardening` job으로 강제한다.
  - 문서 계층(01~09)은 optimization-hardening 문서 세트로 상호 링크를 유지한다.

## Core Design

- **Component Boundary**:
  - `infra/06-observability/docker-compose.yml`
  - `infra/06-observability/loki/{Dockerfile,docker-entrypoint.sh}`
  - `infra/06-observability/tempo/{Dockerfile,docker-entrypoint.sh}`
- **Key Dependencies**:
  - `infra/common-optimizations.yml`
  - Traefik dynamic middleware (`gateway-standard-chain`, `sso-*`)
  - Keycloak SSO
  - MinIO object storage for Loki/Tempo
- **Tech Stack**:
  - Prometheus, Grafana, Loki, Tempo, Alloy, Alertmanager, Pushgateway, Pyroscope, cAdvisor

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Metrics/logs/traces/profiles는 서비스별 retention 정책과 연동해 운영한다.
- **Migration / Transition Plan**:
  - Phase 1: gateway/health/container hardening + CI gate + docs traceability
  - Phase 2: scrape budget/cardinality/sampling 정책 정교화
  - Phase 3: 장기 보관/확장형 HA 운영 모델 적용

## Interfaces & Data Structures

### Core Interfaces

```yaml
observability_gateway_contract:
  routers:
    - prometheus
    - alloy
    - grafana
    - alertmanager
    - pushgateway
    - loki
    - tempo
    - pyroscope
  required_middlewares:
    - gateway-standard-chain@file
    - sso-errors@file
    - sso-auth@file
```

## Catalog-aligned Expansion Targets

- Prometheus:
  - scrape budget, evaluation delay budget, remote_write tiering
- Loki:
  - label cardinality budget, retention/compactor 분리 운영
- Tempo:
  - service/endpoint별 샘플링 정책, span 폭주 보호
- Alloy:
  - 수집 모듈 템플릿화, 신규 서비스 온보딩 표준화

## Edge Cases & Error Handling

- 일부 라우터만 SSO 체인을 적용하면 관리 경로 노출 편차가 발생한다.
- `service_started` 의존성은 부팅 race로 downstream 서비스 오류를 유발할 수 있다.
- 커스텀 이미지 root 실행은 보안 기준선 위반과 런타임 위험을 높인다.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: middleware/depends_on 변경 후 UI/API 접근 실패
- **Fallback**: 직전 안정 compose 계약으로 롤백 후 하드닝 스크립트 재실행
- **Human Escalation**: SRE + Gateway Operator 승인 하에 정책 예외 적용

## Verification

```bash
docker compose -f infra/06-observability/docker-compose.yml config
bash scripts/check-observability-hardening.sh
bash scripts/check-template-security-baseline.sh
bash scripts/check-doc-traceability.sh
```

가능 환경에서 runtime 검증:

```bash
docker compose -f infra/06-observability/docker-compose.yml --profile obs up -d
docker inspect --format '{{json .State.Health}}' infra-prometheus
docker inspect --format '{{json .State.Health}}' infra-grafana
docker inspect --format '{{json .State.Health}}' cadvisor
```

## Success Criteria & Verification Plan

- **VAL-SPC-OBS-001**: `check-observability-hardening` 실패 0건
- **VAL-SPC-OBS-002**: observability compose 정적 검증 통과
- **VAL-SPC-OBS-003**: 공개 라우터 middleware 체인 계약 충족
- **VAL-SPC-OBS-004**: 01~09 optimization-hardening 문서 상호 링크 동기화

## Related Documents

- **Plan**: [../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md](../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/06-observability/optimization-hardening.md](../../07.guides/06-observability/optimization-hardening.md)
- **Operations**: [../../08.operations/06-observability/optimization-hardening.md](../../08.operations/06-observability/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/06-observability/optimization-hardening.md](../../09.runbooks/06-observability/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
