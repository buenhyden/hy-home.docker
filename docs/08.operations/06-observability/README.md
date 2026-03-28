# Observability Operations Policy (08.operations/06-observability)

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

- 단계별 장애 복구 실행 절차 (-> `09.runbooks/06-observability`)
- 개발자 튜토리얼/사용 가이드 (-> `07.guides/06-observability`)

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

이 경로는 "무엇을 허용/금지하는가"를 정의하는 정책 계층이다. 구체 실행 절차는 `09.runbooks`를 참조한다.

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

- **Runbooks**: [../../09.runbooks/06-observability/README.md](../../09.runbooks/06-observability/README.md)
- **Guides**: [../../07.guides/06-observability/README.md](../../07.guides/06-observability/README.md)

## SSoT References

- **PRD**: [../../01.prd/2026-03-28-06-observability-optimization-hardening.md](../../01.prd/2026-03-28-06-observability-optimization-hardening.md)
- **ARD**: [../../02.ard/0021-observability-optimization-hardening-architecture.md](../../02.ard/0021-observability-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md](../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/06-observability/spec.md](../../04.specs/06-observability/spec.md)
- **Plan**: [../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md](../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/06-observability/optimization-hardening.md](../../07.guides/06-observability/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/06-observability/optimization-hardening.md](../../09.runbooks/06-observability/optimization-hardening.md)
- **Catalog**: [../12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

## AI Agent Guidance

1. observability 경로 변경 시 `optimization-hardening.md` 정책을 최우선 기준으로 적용한다.
2. Required 통제를 compose 변경에서 누락하면 안 된다.
