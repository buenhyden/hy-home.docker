# Observability Runbooks

> LGTM stack and telemetry pipeline incident recovery procedures.

## Overview

이 디렉터리는 `06-observability` 계층 장애 상황에서 즉시 실행할 복구 절차를 제공한다. 정책 정의가 아니라 장애 완화, 원인 확인, 증적 수집, 안전 롤백을 목적으로 한다.

## Audience

이 README의 주요 독자:

- SRE / On-call Operators
- Platform Engineers
- Incident Commander
- AI Agents executing runbooks with human approval

## Scope

### In Scope

- Grafana, Loki, Tempo, Prometheus, Alloy, Pushgateway, Pyroscope, Alertmanager 장애 복구
- 로그/메트릭/트레이스 파이프라인 상태 점검
- 복구 후 검증 및 증적 수집 절차

### Out of Scope

- 운영 정책 및 보존 기준 정의 (08.operations 담당)
- 도구 사용법/온보딩 문서 (07.guides 담당)
- 사고 회고 및 재발 방지 분석 (11.postmortems 담당)

## Structure

```text
06-observability/
├── alertmanager.md        # Alertmanager 장애 및 알림 경로 복구
├── alloy.md               # Grafana Alloy 수집 파이프라인 복구
├── grafana.md             # Grafana UI/API 및 datasource 복구
├── loki.md                # Loki ingestion/query 장애 복구
├── prometheus.md          # Prometheus 서비스 복구
├── prometheus-recovery.md # Prometheus 심화 복구 절차
├── pushgateway.md         # Pushgateway 수집 경로 복구
├── pyroscope.md           # Pyroscope 프로파일 수집 복구
├── tempo.md               # Tempo trace 저장/조회 복구
└── README.md              # This file
```

## How to Work in This Area

1. 장애 신호를 수신하면 대상 서비스 런북을 먼저 선택한다.
2. 명령 실행 전 영향 범위와 롤백 조건을 확인한다.
3. 절차 완료 후 Verification 섹션 기준으로 정상화 여부를 판단한다.
4. 필요 시 Incident/Postmortem 문서로 연결해 후속 조치를 기록한다.

## Related References

- **Guides**: [06-observability Guides](../../07.guides/06-observability/README.md)
- **Operations**: [06-observability Operations](../../08.operations/06-observability/README.md)
- **Incidents**: [Incident Records](../../10.incidents/README.md)
- **Postmortems**: [Postmortems](../../11.postmortems/README.md)
