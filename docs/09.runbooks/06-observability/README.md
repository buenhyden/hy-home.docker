# Observability Runbooks (09.runbooks/06-observability)

> Executable procedures for observability incident response, recovery, and optimization baseline restoration.

## Overview

이 디렉터리는 `06-observability` 계층의 즉시 실행 가능한 운영 절차를 제공한다. 서비스별 복구 절차와 optimization-hardening 회귀 복구 절차를 포함한다.

## Audience

이 README의 주요 독자:

- SRE / On-call Engineers
- DevOps Engineers
- Platform Operators
- AI Agents

## Scope

### In Scope

- Prometheus/Grafana/Loki/Tempo/Alloy/Pushgateway/Pyroscope/Alertmanager 복구 절차
- 관측성 최적화/하드닝 기준선 회귀 복구 절차

### Out of Scope

- 운영 통제 정의 (-> `08.operations/06-observability`)
- 교육용/개념 중심 가이드 (-> `07.guides/06-observability`)

## Structure

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

## How to Work in This Area

1. 런북은 즉시 실행 가능한 절차와 검증 단계를 우선으로 작성한다.
2. `docs/99.templates/runbook.template.md` 형식을 준용한다.
3. 고위험 조치 전 승인 조건과 증적 수집 방법을 명시한다.
4. 문서 추가/변경 시 README 구조와 SSoT 링크를 함께 갱신한다.

## Usage Instructions

장애 유형에 맞는 런북을 선택하고, Checklist -> Procedure -> Verification 순서로 수행한다.

## Verification and Monitoring

- 런북 수행 후 `Verification Steps`를 완료한다.
- 필요 시 다음 검증을 병행한다.
  - `bash scripts/check-observability-hardening.sh`
  - `bash scripts/check-doc-traceability.sh`

## Incident and Recovery Links

- **Operations Policy**: [../../08.operations/06-observability/README.md](../../08.operations/06-observability/README.md)
- **Guides**: [../../07.guides/06-observability/README.md](../../07.guides/06-observability/README.md)

## SSoT References

- **PRD**: [../../01.prd/2026-03-28-06-observability-optimization-hardening.md](../../01.prd/2026-03-28-06-observability-optimization-hardening.md)
- **ARD**: [../../02.ard/0021-observability-optimization-hardening-architecture.md](../../02.ard/0021-observability-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md](../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/06-observability/spec.md](../../04.specs/06-observability/spec.md)
- **Plan**: [../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md](../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)
- **Operation**: [../../08.operations/06-observability/optimization-hardening.md](../../08.operations/06-observability/optimization-hardening.md)

## AI Agent Guidance

1. 고위험 조치(접근제어 완화, 강제 purge, 라우팅 우회) 전 사람 승인 필요.
2. 수행 전후 증적(health, logs, config diff)을 남기고 incident 문서와 연결한다.
