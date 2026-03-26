# Alloy Operational Policy

> Telemetry Pipeline Governance and Performance Standards

---

## Overview (KR)

이 정책은 `hy-home.docker` 가시성 플랫폼의 핵심 수집기인 Grafana Alloy의 운영 기준을 정의한다. 파이프라인 안정성과 데이터 무결성을 유지하기 위한 가이드라인을 제공한다.

## Target Audience

- Operator
- SRE
- AI Agents

## Operational Standards

### 1. Ingestion Protocol Tier
- **Tier 1 (Preferred)**: OTLP gRPC/HTTP. 모든 신규 서비스는 OTLP를 통한 직접 전송을 원칙으로 한다.
- **Tier 2 (Legacy/Infra)**: Docker socket discovery + Scraping. 자동 메타데이터 주입이 필요한 인프라 컴포넌트에 사용한다.

### 2. Data Reliability & Performance
- **Batching Strategy**: 
    - `send_batch_size`: 통상 1,000 ~ 2,000 레코드 유지.
    - `timeout`: 1s ~ 5s 유지하여 지연 시간 제어.
- **Memory Management**: Alloy 인프라 메모리 사용량이 80%를 초과할 경우 배치 사이즈를 조정하거나 스케일 업을 검토한다.

### 3. Labeling and Taxonomy
- 모든 텔레메트리에는 다음 필수 레이블이 포함되어야 한다.
    - `service_name`: 서비스 명칭
    - `env`: dev, staging, prod 등 환경 정보
    - `scope`: infra (플랫폼 구성 요소) 또는 app (사용자 서비스)

## Monitoring and Alerting

### Key Metrics to Monitor
- `alloy_component_health`: 컴포넌트의 정상 작동 여부 (UI에서 확인 가능)
- `otelcol_processor_batch_dropped_spans_total`: 배치 처리 중 소실된 트레이스 수
- `loki_write_errors_total`: Loki 전송 에러 발생률

### Alerting Rules
- **P0 (Critical)**: Alloy 프로세스 중단 또는 OTLP 포트 수신 불가.
- **P1 (Warning)**: 전송 에러(`forward_to` failure)가 5분간 지속될 경우.
- **P2 (Info)**: 배치 처리 지연 시간이 설정값을 반복적으로 초과할 경우.

## Configuration Governance

- 모든 설정 변경은 `infra/06-observability/alloy/config/config.alloy`를 통해 관리한다.
- 대규모 변경 시 Alloy UI의 Graph View를 통해 의도하지 않은 파이프라인 단절이 없는지 사전 검증해야 한다.

## Related Documents

- **Guide**: [../../07.guides/06-observability/alloy.md](../../07.guides/06-observability/alloy.md)
- **Runbook**: [../../09.runbooks/06-observability/alloy.md](../../09.runbooks/06-observability/alloy.md)
