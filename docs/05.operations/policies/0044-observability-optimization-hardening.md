---
title: "Observability Optimization Hardening Policy"
version: "1.0.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0044"
parent_ids:
- "AD-0006"
created: "2026-05-10"
---

# Observability Optimization Hardening Policy

## Overview

### Overview

이 문서는 `06-observability` 계층의 최적화/하드닝 운영 정책을 정의한다. 게이트웨이 경계 보안, health 기반 의존성, 커스텀 이미지 런타임 하드닝, CI 기준선 검증, 카탈로그 확장 승인 조건을 통제한다.

## Scope

### Policy Scope

- `infra/06-observability/docker-compose.yml`
- `infra/06-observability/loki/{Dockerfile,docker-entrypoint.sh}`
- `infra/06-observability/tempo/{Dockerfile,docker-entrypoint.sh}`
- `scripts/hardening/check-all-hardening.sh`
- `scripts/validation/check-template-security-baseline.sh`
- `.github/workflow-contract.yml` `leaf.infrastructure-hardening` gate (`ci-quality.yml`의 `validation-changed`/`validation-full` job이 실행)

- **Systems**: Prometheus, Alertmanager, Grafana, Loki, Tempo, Alloy, Pushgateway, Pyroscope, cAdvisor
- **Environments**: 로컬·개발·홈랩 운영과 운영 환경에 준하는 검증

### Traceability

- Declared parent: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0044-observability-optimization-hardening.md) (`GDE-0044`), [Runbook](../runbooks/0044-observability-optimization-hardening.md) (`RUN-0044`)

## Rules

### Controls

- **Required**:
  - Native OIDC routers `grafana`/`gatus`는
    `gateway-standard-chain@file`만 적용하고 application login/role mapping을
    유지한다.
  - Proxy-protected observability routers는
    `gateway-standard-chain@file,sso-errors@file,sso-auth@file`을 유지한다.
  - `depends_on`은 핵심 백엔드에 대해 `service_healthy`를 우선 사용한다.
  - host observer(cAdvisor)는 healthcheck를 필수로 가진다.
  - Pyroscope는 `obs`와 `dev` profile 어느 쪽으로 선택되든 route, service port,
    persistent volume, healthcheck 기준을 동일하게 유지한다.
  - Loki/Tempo 커스텀 이미지는 non-root 실행을 강제한다.
  - entrypoint는 secret 파일 존재를 선검증한다.
  - 관측성 변경은 `infrastructure-hardening` CI 게이트를 통과해야 한다.
  - 관측성 변경은 `check-template-security-baseline.sh`,
    `check-document-links.py --mode traceability`, 관련 compose validation 결과를 함께 확인한다.
  - log/trace/profile retention 변경은 [retention policy](0048-telemetry-retention.md)와
    서비스별 policy/runbook에 함께 반영한다.
  - 대량 scrape 실패, trace/log ingestion 지연 급증, 관리경로 인증 실패 급증은
    runbook handoff 조건으로 취급한다.
  - 문서(PRD~Procedure)는 optimization-hardening 링크를 유지해야 한다.
- **Allowed**:
  - 카탈로그 기반 단계 확장(샘플링/retention/pipeline module)
  - 운영상 필요한 profile 기반 선택 기동
- **Disallowed**:
  - 무검증 라우터 middleware 변경
  - root 실행 커스텀 이미지 재도입
  - secret guard가 없는 Loki/Tempo object storage 연결
  - 정책 미연계 확장 실행

### Catalog Expansion Approval Gates

- **Prometheus 승인 조건**:
  - scrape budget 및 rule evaluation 지연 예산 정의
  - remote_write 계층화 운영 절차 준비
- **Loki/Tempo 승인 조건**:
  - cardinality/sampling 가드레일 문서화
  - retention/compaction 정책과 복구 절차 연동
- **Alloy 승인 조건**:
  - 신규 서비스 온보딩 템플릿 표준화
  - 파이프라인 모듈 경계와 소유권 명시

### Lifecycle and data controls

- 두 exporter의 HOME 분류를 유지하고 host PID·privileged·device/host mount 확대에는 보안 검토를 요구한다.
- node-exporter는 내부 전용, cAdvisor는 보호 route를 유지하며 무관한 secret이나 writable host mount를 추가하지 않는다.
- 별도 영속 exporter backup은 없다. 추적 Compose로 복구한 뒤 target과 series 연속성을 검증한다.
- 자원/cardinality 변경에는 scrape/host 영향 측정이 필요하다. 제거에는 rule/dashboard 의존성 검토와 관측 공백 승인이 필요하다.

### cAdvisor and static-check limits

cAdvisor는 읽기 전용 filesystem/device mount와 `/dev/kmsg`를 사용하는 privileged 관측기다. 공통 template이 capability를 제거한다고 격리를 보장하지 않는다. Disk metric 등 제외 collector, container label/cardinality와 보호 route를 유지한다. Health는 process 응답만 확인하므로 Prometheus target과 예상 container series를 따로 검증한다. 자체 애플리케이션 데이터나 Docker Secret은 없고 복구 대상은 승인된 image/config와 telemetry 기준이다.

관측 hardening 함수는 일부 문자열·파일만 검사하며 모든 Dockerfile, retention 시행, 인증 거부, 전달, host 호환성이나 용량을 증명하지 않는다. Loki/Tempo LAN 접근은 POL-0096의 기존 예외이고 retention 결함은 POL-0048에 남는다. Grafana/Gatus native 인증에 일괄 proxy SSO를 붙이지 않는다. 검사 통과만으로 통제를 완료하거나 privileged 권한 확대를 승인하지 않는다.

### Verification

- `bash scripts/hardening/check-all-hardening.sh 06-observability`
- `bash scripts/validation/check-template-security-baseline.sh`
- `python3 scripts/validation/check-document-links.py --mode traceability`
- `HYHOME_COMPOSE_PROFILES=obs bash scripts/validation/validate-docker-compose.sh`
- Service-local compose 검증은 root network/secret context 또는 임시 overlay 포함

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Cadence

- 월 1회 정기 검토
- 관측성 주요 버전 변경/보안 이슈 발생 시 수시 검토

## Exceptions

### Exceptions

- 긴급 장애 대응 시 일시적으로 인증 경계 완화가 필요할 수 있다.
- 단, 동일 릴리스 내 원상 복구 및 검증 증적 확보가 필수다.

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0044-observability-optimization-hardening.md)
- [Recovery runbook](../runbooks/0044-observability-optimization-hardening.md)
- [Retention policy](0048-telemetry-retention.md)
