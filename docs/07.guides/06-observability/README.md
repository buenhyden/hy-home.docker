# Observability Guides (07.guides/06-observability)

> Developer/operator guides for LGTM stack operation and optimization hardening.

## Overview

이 디렉터리는 `06-observability` 계층의 사용/운영 가이드를 제공한다. 서비스별 가이드와 optimization-hardening 적용 절차를 함께 관리한다.

## Audience

이 README의 주요 독자:

- Developers
- SRE / Platform Operators
- DevOps Engineers
- AI Agents

## Scope

### In Scope

- Prometheus/Grafana/Loki/Tempo/Alloy/Alertmanager/Pushgateway/Pyroscope 가이드
- LGTM 아키텍처 가이드
- 관측성 optimization-hardening 적용 가이드

### Out of Scope

- 운영 통제 정책 정의 (-> `08.operations/06-observability`)
- 즉시 실행 장애 복구 절차 (-> `09.runbooks/06-observability`)

## Structure

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

## How to Work in This Area

1. 새 가이드는 `docs/99.templates/guide.template.md`를 기반으로 작성한다.
2. 절차 문서는 Prerequisites와 Step-by-step Instructions를 포함한다.
3. 관련 Spec/Operation/Runbook 링크를 문서 하단에 유지한다.
4. 가이드 추가/변경 시 README Structure와 SSoT 링크를 즉시 갱신한다.

## Documentation Standards

- 가이드는 정책 문서가 아닌 재현 가능한 how-to/system guide여야 한다.
- 상대 경로 링크만 사용한다.
- 한국어 `Overview (KR)` 요약을 포함한다.

## SSoT References

- **PRD**: [../../01.prd/2026-03-28-06-observability-optimization-hardening.md](../../01.prd/2026-03-28-06-observability-optimization-hardening.md)
- **ARD**: [../../02.ard/0021-observability-optimization-hardening-architecture.md](../../02.ard/0021-observability-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md](../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/06-observability/spec.md](../../04.specs/06-observability/spec.md)
- **Plan**: [../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md](../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)
- **Operation**: [../../08.operations/06-observability/optimization-hardening.md](../../08.operations/06-observability/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/06-observability/optimization-hardening.md](../../09.runbooks/06-observability/optimization-hardening.md)

## AI Agent Guidance

1. 가이드 변경 시 optimization-hardening 문서와 상호 링크를 유지한다.
2. gateway/SSO 설명은 `08.operations` 정책과 충돌하지 않아야 한다.
