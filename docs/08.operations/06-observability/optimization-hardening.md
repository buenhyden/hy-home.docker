# 06-Observability Optimization Hardening Operations Policy

## Overview (KR)

이 문서는 `06-observability` 계층의 최적화/하드닝 운영 정책을 정의한다. 게이트웨이 경계 보안, health 기반 의존성, 커스텀 이미지 런타임 하드닝, CI 기준선 검증, 카탈로그 확장 승인 조건을 통제한다.

## Policy Scope

- `infra/06-observability/docker-compose.yml`
- `infra/06-observability/loki/{Dockerfile,docker-entrypoint.sh}`
- `infra/06-observability/tempo/{Dockerfile,docker-entrypoint.sh}`
- `scripts/check-observability-hardening.sh`

## Applies To

- **Systems**: Prometheus, Alertmanager, Grafana, Loki, Tempo, Alloy, Pushgateway, Pyroscope, cAdvisor
- **Agents**: Infra/DevOps/Operations agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - 공개 라우터는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
  - `depends_on`은 핵심 백엔드에 대해 `service_healthy`를 우선 사용한다.
  - host observer(cAdvisor)는 healthcheck를 필수로 가진다.
  - Loki/Tempo 커스텀 이미지는 non-root 실행을 강제한다.
  - entrypoint는 secret 파일 존재를 선검증한다.
  - 관측성 변경은 `observability-hardening` CI 게이트를 통과해야 한다.
  - 문서(PRD~Runbook)는 optimization-hardening 링크를 유지해야 한다.
- **Allowed**:
  - 카탈로그 기반 단계 확장(샘플링/retention/pipeline module)
  - 운영상 필요한 profile 기반 선택 기동
- **Disallowed**:
  - 무검증 라우터 middleware 변경
  - root 실행 커스텀 이미지 재도입
  - 정책 미연계 확장 실행

## Exceptions

- 긴급 장애 대응 시 일시적으로 인증 경계 완화가 필요할 수 있다.
- 단, 동일 릴리스 내 원상 복구 및 검증 증적 확보가 필수다.

## Verification

- `bash scripts/check-observability-hardening.sh`
- `bash scripts/check-template-security-baseline.sh`
- `bash scripts/check-doc-traceability.sh`
- `docker compose -f infra/06-observability/docker-compose.yml config`

## Review Cadence

- 월 1회 정기 검토
- 관측성 주요 버전 변경/보안 이슈 발생 시 수시 검토

## Catalog Expansion Approval Gates

- **Prometheus 승인 조건**:
  - scrape budget 및 rule evaluation 지연 예산 정의
  - remote_write 계층화 운영 절차 준비
- **Loki/Tempo 승인 조건**:
  - cardinality/sampling 가드레일 문서화
  - retention/compaction 정책과 복구 절차 연동
- **Alloy 승인 조건**:
  - 신규 서비스 온보딩 템플릿 표준화
  - 파이프라인 모듈 경계와 소유권 명시

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: N/A
- **Eval / Guardrail Threshold**: `observability-hardening` + 공통 기준선 통과 필수
- **Log / Trace Retention**: 06-observability 기본 retention 정책 준수
- **Safety Incident Thresholds**: 대량 scrape 실패, trace/log ingestion 지연 급증, 관리경로 인증 실패 급증 시 runbook 즉시 전환

## Related Documents

- **PRD**: [../../01.prd/2026-03-28-06-observability-optimization-hardening.md](../../01.prd/2026-03-28-06-observability-optimization-hardening.md)
- **ARD**: [../../02.ard/0021-observability-optimization-hardening-architecture.md](../../02.ard/0021-observability-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md](../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/06-observability/spec.md](../../04.specs/06-observability/spec.md)
- **Plan**: [../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md](../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/06-observability/optimization-hardening.md](../../07.guides/06-observability/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/06-observability/optimization-hardening.md](../../09.runbooks/06-observability/optimization-hardening.md)
- **Catalog**: [../12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)
