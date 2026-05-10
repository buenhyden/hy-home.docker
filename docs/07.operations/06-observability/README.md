# Observability Operations Policy (07.operations/06-observability)

> Governance, reliability standards, and optimization/hardening controls for the observability tier.

## Overview

이 디렉터리는 `06-observability` 계층의 운영 정책 문서를 관리한다. retention/alerting 기본 정책과 서비스별 운영 기준, optimization-hardening 통제를 정의한다.

## Audience

이 README의 주요 독자:

- Operators
- DevOps Engineers
- Architects
- AI Agents

## Scope

### In Scope

- Prometheus/Alertmanager/Grafana/Loki/Tempo/Alloy/Pushgateway/Pyroscope 운영 정책
- Retention 정책
- Observability optimization/hardening 운영 정책
- 카탈로그 연계 확장 승인 기준

### Out of Scope

- 단계별 장애 복구 실행 절차 (-> `07.operations/06-observability`)
- 개발자 튜토리얼/사용 가이드 (-> `07.operations/06-observability`)

## Structure

```text
06-observability/
├── 01.retention.md            # Retention baseline policy
├── alertmanager.md            # Alertmanager operations policy
├── alloy.md                   # Alloy operations policy
├── grafana.md                 # Grafana operations policy
├── loki.md                    # Loki operations policy
├── prometheus.md              # Prometheus operations policy
├── pushgateway.md             # Pushgateway operations policy
├── pyroscope.md               # Pyroscope operations policy
├── tempo.md                   # Tempo operations policy
├── optimization-hardening.md  # Observability optimization/hardening policy
└── README.md                  # This file
```

## How to Work in This Area

1. 정책 문서는 `docs/99.templates/operation.template.md` 기준으로 작성한다.
2. 정책 변경 시 대응 guide/runbook 링크를 함께 갱신한다.
3. 카탈로그 항목과 정책 통제를 매핑해 변경 근거를 남긴다.
4. 변경 후 `scripts/check-doc-traceability.sh`를 실행한다.

## Usage Instructions

이 경로는 "무엇을 허용/금지하는가"를 정의하는 정책 계층이다. 구체 실행 절차는 `07.operations`를 참조한다.

## Verification and Monitoring

- 정책 준수 검증:
  - `bash scripts/check-observability-hardening.sh`
  - `bash scripts/check-template-security-baseline.sh`
  - `bash scripts/check-doc-traceability.sh`
- 운영 지표:
  - scrape success ratio
  - ingestion latency/log backlog
  - query latency/error rate

## Incident and Recovery Links

- **Procedures**: [../../07.operations/06-observability/README.md](../../07.operations/06-observability/README.md)
- **Usages**: [../../07.operations/06-observability/README.md](../../07.operations/06-observability/README.md)

## SSoT References

- **PRD**: [../../01.prd/2026-03-28-06-observability-optimization-hardening.md](../../01.prd/2026-03-28-06-observability-optimization-hardening.md)
- **ARD**: [../../02.ard/0021-observability-optimization-hardening-architecture.md](../../02.ard/0021-observability-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md](../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/06-observability/spec.md](../../04.specs/06-observability/spec.md)
- **Plan**: [../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md](../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)
- **Usage**: [../../07.operations/06-observability/optimization-hardening.md](../../07.operations/06-observability/optimization-hardening.md)
- **Procedure**: [../../07.operations/06-observability/optimization-hardening.md](../../07.operations/06-observability/optimization-hardening.md)
- **Catalog**: [../12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

## AI Agent Guidance

1. observability 경로 변경 시 `optimization-hardening.md` 정책을 최우선 기준으로 적용한다.
2. Required 통제를 compose 변경에서 누락하면 안 된다.

---

## Related References

- [docs/07.operations/README.md](../README.md)
- [docs/07.operations/README.md](../../07.operations/README.md)
- [docs/07.operations/README.md](../../07.operations/README.md)

## Usage

> Migrated from `docs/07.operations/06-observability/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Observability Usages (07.operations/06-observability)

> Developer/operator guides for LGTM stack operation and optimization hardening.

#### Overview

이 디렉터리는 `06-observability` 계층의 사용/운영 가이드를 제공한다. 서비스별 가이드와 optimization-hardening 적용 절차를 함께 관리한다.

#### Audience

이 README의 주요 독자:

- Developers
- SRE / Platform Operators
- DevOps Engineers
- AI Agents

#### Scope

##### In Scope

- Prometheus/Grafana/Loki/Tempo/Alloy/Alertmanager/Pushgateway/Pyroscope 가이드
- LGTM 아키텍처 가이드
- 관측성 optimization-hardening 적용 가이드

##### Out of Scope

- 운영 통제 정책 정의 (-> `07.operations/06-observability`)
- 즉시 실행 장애 복구 절차 (-> `07.operations/06-observability`)

#### Structure

```text
06-observability/
├── 01.lgtm-stack.md           # LGTM architecture guide
├── alertmanager.md            # Alertmanager guide
├── alloy.md                   # Alloy guide
├── grafana.md                 # Grafana guide
├── loki.md                    # Loki guide
├── prometheus.md              # Prometheus guide
├── pushgateway.md             # Pushgateway guide
├── pyroscope.md               # Pyroscope guide
├── tempo.md                   # Tempo guide
├── optimization-hardening.md  # Observability optimization/hardening guide
└── README.md                  # This file
```

#### How to Work in This Area

1. 새 가이드는 `docs/99.templates/operation.template.md`를 기반으로 작성한다.
2. 절차 문서는 Prerequisites와 Step-by-step Instructions를 포함한다.
3. 관련 Spec/Operation/Procedure 링크를 문서 하단에 유지한다.
4. 가이드 추가/변경 시 README Structure와 SSoT 링크를 즉시 갱신한다.

#### Documentation Standards

- 가이드는 정책 문서가 아닌 재현 가능한 how-to/system guide여야 한다.
- 상대 경로 링크만 사용한다.
- 한국어 `Overview (KR)` 요약을 포함한다.

#### SSoT References

- **PRD**: [../../01.prd/2026-03-28-06-observability-optimization-hardening.md](../../01.prd/2026-03-28-06-observability-optimization-hardening.md)
- **ARD**: [../../02.ard/0021-observability-optimization-hardening-architecture.md](../../02.ard/0021-observability-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md](../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/06-observability/spec.md](../../04.specs/06-observability/spec.md)
- **Plan**: [../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md](../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)
- **Operation**: [../../07.operations/06-observability/optimization-hardening.md](../../07.operations/06-observability/optimization-hardening.md)
- **Procedure**: [../../07.operations/06-observability/optimization-hardening.md](../../07.operations/06-observability/optimization-hardening.md)

#### AI Agent Guidance

1. 가이드 변경 시 optimization-hardening 문서와 상호 링크를 유지한다.
2. gateway/SSO 설명은 `07.operations` 정책과 충돌하지 않아야 한다.

---

#### Related References

- [docs/07.operations/README.md](../README.md)
- [docs/07.operations/README.md](../../07.operations/README.md)
- [docs/07.operations/README.md](../../07.operations/README.md)

## Procedure

> Migrated from `docs/07.operations/06-observability/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Observability Procedures (07.operations/06-observability)

> Executable procedures for observability incident response, recovery, and optimization baseline restoration.

#### Overview

이 디렉터리는 `06-observability` 계층의 즉시 실행 가능한 운영 절차를 제공한다. 서비스별 복구 절차와 optimization-hardening 회귀 복구 절차를 포함한다.

#### Audience

이 README의 주요 독자:

- SRE / On-call Engineers
- DevOps Engineers
- Platform Operators
- AI Agents

#### Scope

##### In Scope

- Prometheus/Grafana/Loki/Tempo/Alloy/Pushgateway/Pyroscope/Alertmanager 복구 절차
- 관측성 최적화/하드닝 기준선 회귀 복구 절차

##### Out of Scope

- 운영 통제 정의 (-> `07.operations/06-observability`)
- 교육용/개념 중심 가이드 (-> `07.operations/06-observability`)

#### Structure

```text
06-observability/
├── alertmanager.md            # Alertmanager recovery
├── alloy.md                   # Alloy recovery
├── grafana.md                 # Grafana recovery
├── loki.md                    # Loki recovery
├── prometheus.md              # Prometheus recovery
├── prometheus-recovery.md     # Prometheus advanced recovery
├── pushgateway.md             # Pushgateway recovery
├── pyroscope.md               # Pyroscope recovery
├── tempo.md                   # Tempo recovery
├── optimization-hardening.md  # Observability hardening baseline recovery
└── README.md                  # This file
```

#### How to Work in This Area

1. 런북은 즉시 실행 가능한 절차와 검증 단계를 우선으로 작성한다.
2. `docs/99.templates/operation.template.md` 형식을 준용한다.
3. 고위험 조치 전 승인 조건과 증적 수집 방법을 명시한다.
4. 문서 추가/변경 시 README 구조와 SSoT 링크를 함께 갱신한다.

#### Usage Instructions

장애 유형에 맞는 런북을 선택하고, Checklist -> Procedure -> Verification 순서로 수행한다.

#### Verification and Monitoring

- 런북 수행 후 `Verification Steps`를 완료한다.
- 필요 시 다음 검증을 병행한다.
  - `bash scripts/check-observability-hardening.sh`
  - `bash scripts/check-doc-traceability.sh`

#### Incident and Recovery Links

- **Operations Policy**: [../../07.operations/06-observability/README.md](../../07.operations/06-observability/README.md)
- **Usages**: [../../07.operations/06-observability/README.md](../../07.operations/06-observability/README.md)

#### SSoT References

- **PRD**: [../../01.prd/2026-03-28-06-observability-optimization-hardening.md](../../01.prd/2026-03-28-06-observability-optimization-hardening.md)
- **ARD**: [../../02.ard/0021-observability-optimization-hardening-architecture.md](../../02.ard/0021-observability-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md](../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/06-observability/spec.md](../../04.specs/06-observability/spec.md)
- **Plan**: [../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md](../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)
- **Operation**: [../../07.operations/06-observability/optimization-hardening.md](../../07.operations/06-observability/optimization-hardening.md)

#### AI Agent Guidance

1. 고위험 조치(접근제어 완화, 강제 purge, 라우팅 우회) 전 사람 승인 필요.
2. 수행 전후 증적(health, logs, config diff)을 남기고 incident 문서와 연결한다.

---

#### Related References

- [docs/07.operations/README.md](../README.md)
- [docs/07.operations/README.md](../../07.operations/README.md)
- [docs/10.incidents/README.md](../../10.incidents/README.md)
