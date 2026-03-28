# 06-Observability Optimization Hardening Architecture Reference Document (ARD)

## Overview (KR)

이 문서는 `06-observability` 계층의 최적화/하드닝 참조 아키텍처를 정의한다. 게이트웨이 경계 보안, health 기반 의존성, 커스텀 이미지 런타임 하드닝, 카탈로그 기반 확장 전략을 아키텍처 관점에서 정리한다.

## Summary

관측성 계층은 데이터 평면(수집/저장)과 관리 평면(UI/API)을 분리해 운영한다. 관리 평면은 Traefik TLS 종료 지점에서 표준 미들웨어+SSO 체인을 적용하고, 데이터 평면은 `infra_net` 내부 통신으로 유지한다.

## Boundaries & Non-goals

- **Owns**:
  - 관측성 서비스 라우팅/인증 경계 계약
  - health 기반 부팅 순서 및 런타임 하드닝 계약
  - observability 하드닝 검증 자동화 계약
- **Consumes**:
  - `01-gateway` Traefik middleware chain
  - `02-auth` Keycloak 기반 SSO
  - `04-data` MinIO object storage
- **Does Not Own**:
  - 애플리케이션 계측 코드(OTel SDK)
  - 비관측성 티어 라우팅 정책
- **Non-goals**:
  - 즉시 multi-cluster/multi-region observability 도입
  - 샘플링 정책 전면 재설계

## Quality Attributes

- **Performance**: 게이트웨이 표준 체인으로 burst 제어/과부하 완화
- **Security**: TLS 종료 + SSO + 비루트 컨테이너 실행
- **Reliability**: `service_healthy` 의존성으로 부팅 안정성 향상
- **Scalability**: catalog 기반 확장(샘플링/retention/long-term storage) 준비
- **Observability**: cAdvisor health + stack health 통합 검증
- **Operability**: 스크립트 기반 회귀 차단 + runbook 표준 절차

## System Overview & Context

- Storage/Query Plane:
  - Prometheus, Loki, Tempo, Pyroscope
- Control/Presentation Plane:
  - Grafana, Alertmanager, Pushgateway, Alloy UI
- Gateway Path:
  - Client -> Traefik(`websecure`) -> `gateway-standard-chain` + `sso-*` -> target service
- Internal Path:
  - OTLP/log/trace traffic over `infra_net`

## Data Architecture

- **Key Entities / Flows**:
  - Metrics, logs, traces, profiles
- **Storage Strategy**:
  - Prometheus local TSDB
  - Loki/Tempo object storage via MinIO
  - Pyroscope local storage
- **Data Boundaries**:
  - 장기 보존/리텐션 정책은 operations 계층에서 관리

## Infrastructure & Deployment

- **Runtime / Platform**:
  - Docker Compose + `infra/common-optimizations.yml`
- **Deployment Model**:
  - single-node observability core + optional horizontal expansion
- **Operational Evidence**:
  - `scripts/check-observability-hardening.sh`
  - CI `observability-hardening` job

## Catalog-aligned Expansion Targets

- Prometheus: scrape budget + remote_write 계층화
- Loki: label cardinality budget + retention/compactor 분리 운영
- Tempo: service/endpoint별 샘플링 정책 + span 폭주 보호
- Alloy: 온보딩 템플릿화 + 수집 파이프라인 모듈화

## Related Documents

- **PRD**: [../01.prd/2026-03-28-06-observability-optimization-hardening.md](../01.prd/2026-03-28-06-observability-optimization-hardening.md)
- **Spec**: [../04.specs/06-observability/spec.md](../04.specs/06-observability/spec.md)
- **Plan**: [../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md](../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- **ADR**: [../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md](../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md)
- **Tasks**: [../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md](../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/06-observability/optimization-hardening.md](../07.guides/06-observability/optimization-hardening.md)
- **Operation**: [../08.operations/06-observability/optimization-hardening.md](../08.operations/06-observability/optimization-hardening.md)
- **Runbook**: [../09.runbooks/06-observability/optimization-hardening.md](../09.runbooks/06-observability/optimization-hardening.md)
