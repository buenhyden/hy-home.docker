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
  - 문서(PRD~Procedure)는 optimization-hardening 링크를 유지해야 한다.
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
- **Usage**: [../../07.operations/06-observability/optimization-hardening.md](../../07.operations/06-observability/optimization-hardening.md)
- **Procedure**: [../../07.operations/06-observability/optimization-hardening.md](../../07.operations/06-observability/optimization-hardening.md)
- **Catalog**: [../12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

## Usage

> Migrated from `docs/07.operations/06-observability/optimization-hardening.md` during the 2026-05-10 operations taxonomy consolidation.

### 06-Observability Optimization Hardening Usage

#### Overview (KR)

이 문서는 `06-observability` 계층의 최적화/하드닝 항목을 운영자/개발자가 재현 가능하게 적용하기 위한 가이드다. gateway 체인+SSO 정렬, health 기반 의존성, 커스텀 이미지 하드닝, CI 검증 절차를 제공한다.

#### Usage Type

`system-guide | how-to`

#### Target Audience

- SRE / Platform Operator
- DevOps Engineer
- Observability Maintainer

#### Purpose

- 관측성 관리 경로를 게이트웨이 표준 정책에 정렬한다.
- 초기 기동 안정성과 회귀 차단 능력을 강화한다.
- 카탈로그 기반 확장(샘플링/retention/pipeline module) 준비 상태를 확보한다.

#### Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/06-observability` 및 `scripts/` 수정 권한
- Traefik `gateway-standard-chain` 및 `sso-*` middleware 준비

#### Step-by-step Instructions

1. 변경 전 정적 상태 점검
   - `docker compose -f infra/06-observability/docker-compose.yml config`
2. Gateway/SSO 경계 정렬
   - 공개 라우터(`prometheus`, `alloy`, `grafana`, `alertmanager`, `pushgateway`, `loki`, `tempo`, `pyroscope`)에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
3. 의존성/헬스 보강
   - Alloy/Grafana의 Loki/Tempo 의존성을 `service_healthy`로 설정한다.
   - cAdvisor healthcheck(`/healthz`)를 추가한다.
4. 커스텀 이미지 하드닝
   - Loki/Tempo Dockerfile에 non-root user(`10001`)를 강제한다.
   - entrypoint에서 MinIO secret 존재를 선검증한다.
5. 자동 검증 및 CI 반영
   - `bash scripts/check-observability-hardening.sh`
   - CI workflow에 `observability-hardening` job 반영 여부 확인
6. 문서 추적성 동기화
   - PRD~Procedure optimization-hardening 문서 링크를 점검한다.

#### Common Pitfalls

- 일부 라우터만 SSO 체인을 적용해 관리 경로 노출이 발생하는 실수
- `service_started` 의존성으로 부팅 race condition을 남기는 실수
- custom 이미지에 root 실행 경로를 재도입하는 실수
- 하드닝 스크립트/README 인덱스를 함께 갱신하지 않는 실수

#### Related Documents

- **PRD**: [../../01.prd/2026-03-28-06-observability-optimization-hardening.md](../../01.prd/2026-03-28-06-observability-optimization-hardening.md)
- **Spec**: [../../04.specs/06-observability/spec.md](../../04.specs/06-observability/spec.md)
- **Plan**: [../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md](../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)
- **Operation**: [../../07.operations/06-observability/optimization-hardening.md](../../07.operations/06-observability/optimization-hardening.md)
- **Procedure**: [../../07.operations/06-observability/optimization-hardening.md](../../07.operations/06-observability/optimization-hardening.md)
- **Catalog**: [../../07.operations/12-infra-service-optimization-catalog.md](../../07.operations/12-infra-service-optimization-catalog.md)

## Procedure

> Migrated from `docs/07.operations/06-observability/optimization-hardening.md` during the 2026-05-10 operations taxonomy consolidation.

### 06-Observability Optimization Hardening Procedure

: Observability Gateway/Compose Baseline Recovery

#### Overview (KR)

이 런북은 `06-observability` 하드닝 항목에서 발생할 수 있는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. gateway/SSO 체인 누락, health 의존성 회귀, 커스텀 이미지 런타임 하드닝 누락, CI 기준선 실패를 중심으로 점검/복구한다.

#### Purpose

- 관측성 관리 경로의 보안/가용성 기준을 신속히 복구한다.
- compose/CI 회귀를 조기에 차단하고 안정 상태로 복원한다.

#### Canonical References

- [Spec](../../04.specs/06-observability/spec.md)
- [Operations Policy](../../07.operations/06-observability/optimization-hardening.md)
- [Plan](../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- [Tasks](../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)

#### When to Use

- `observability-hardening` CI가 실패할 때
- 관측성 UI/API가 Traefik 경유로 비정상 응답할 때
- 스택 부팅 시 Alloy/Grafana 의존성 대기로 장애가 반복될 때
- Loki/Tempo custom image 런타임 실패가 발생할 때

#### Procedure or Checklist

##### Checklist

- [ ] 실패 항목(middleware/depends_on/healthcheck/image/script/doc) 식별
- [ ] 최근 변경 커밋과 영향 범위 확인
- [ ] 운영 영향도(수집/조회/알림 경로) 평가

##### Procedure

1. 정적 구성 점검
   - `docker compose -f infra/06-observability/docker-compose.yml config`
2. 하드닝 기준 점검
   - `bash scripts/check-observability-hardening.sh`
3. 증상별 복구
   - middleware 누락:
     - 대상 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file` 재적용
   - 의존성 race:
     - Alloy/Grafana의 Loki/Tempo `depends_on`을 `service_healthy`로 복원
   - 호스트 수집기 신호 불량:
     - cAdvisor `/healthz` healthcheck 복원
   - custom image 회귀:
     - Loki/Tempo Dockerfile `USER 10001:10001` 복원
     - entrypoint secret guard 복원
4. 재검증
   - `bash scripts/check-observability-hardening.sh`
   - `bash scripts/check-template-security-baseline.sh`
   - `bash scripts/check-doc-traceability.sh`

#### Verification Steps

- [ ] observability compose `config` 검증 통과
- [ ] `check-observability-hardening` 실패 0건
- [ ] optimization-hardening 문서 링크/README 인덱스 최신화 확인

#### Observability and Evidence Sources

- **Signals**: CI `observability-hardening` 상태, Traefik 라우터 상태, container health
- **Evidence to Capture**:
  - 변경 전후 `check-observability-hardening.sh` 출력
  - compose `config` 결과
  - 관련 compose/Dockerfile/docs diff

#### Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/06-observability/docker-compose.yml`
  - `infra/06-observability/loki/{Dockerfile,docker-entrypoint.sh}`
  - `infra/06-observability/tempo/{Dockerfile,docker-entrypoint.sh}`
  - `scripts/check-observability-hardening.sh`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 운영 정책/가이드/태스크 문서 링크 재확인

#### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: 관측성 자동화 변경 작업 일시 중지(승인 필요)
- **Eval Re-run**: `check-observability-hardening`, `check-template-security-baseline`, `check-doc-traceability`
- **Trace Capture**: CI logs + compose config output + health 상태

#### Related Operational Documents

- **Usage**: [../../07.operations/06-observability/optimization-hardening.md](../../07.operations/06-observability/optimization-hardening.md)
- **Operation**: [../../07.operations/06-observability/optimization-hardening.md](../../07.operations/06-observability/optimization-hardening.md)
- **Catalog**: [../../07.operations/12-infra-service-optimization-catalog.md](../../07.operations/12-infra-service-optimization-catalog.md)
