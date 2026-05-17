# Alloy Operational Policy Usage Guide

## Usage
>
> Unified Telemetry Collection and OTLP Pipeline Usage

---

### Overview (KR)

Alloy는 `hy-home.docker` 플랫폼의 모든 텔레메트리(지표, 로그, 트레이스)를 수집하여 적절한 백엔드로 전달하는 통합 에이전트이다. 이 가이드는 Alloy의 파이프라인 구조와 데이터 흐름을 설명한다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- Agent-tuner

### Purpose

이 가이드는 Alloy를 사용하여 시스템의 통합 가시성을 확보하고, 텔레메트리 파이프라인을 효율적으로 관리하는 방법을 설명한다.

### Prerequisites

- OTLP 프로토콜에 대한 기본 이해
- `config.alloy` (HCL) 설정 문법 이해
- Docker 및 컨테이너 메타데이터에 대한 지식

### Step-by-step Instructions

#### 1. Understanding the Pipeline

Alloy의 파이프라인은 다음과 같은 단계로 구성된다.

- **Discovery**: `discovery.docker`를 사용하여 컨테이너 정보를 수집한다.
- **Relabeling**: `discovery.relabel`을 사용하여 메타데이터(service_name, env, scope)를 주입한다.
- **Scraping/Receiving**:
  - Logs: `loki.source.docker`
  - Metrics: `prometheus.scrape`
  - Traces/Metrics: `otelcol.receiver.otlp` (OTLP Ingestion)
- **Processing**: `otelcol.processor.batch` 등을 사용하여 성능을 최적화한다.
- **Exporting**: 각 백엔드(`loki.write`, `prometheus.remote_write`, `otelcol.exporter.otlp`)로 데이터를 전송한다.

#### 2. OTLP Ingestion

애플리케이션은 다음 포트를 통해 데이터를 전송할 수 있다.

- **gRPC**: `alloy:4317`
- **HTTP**: `alloy:4318`

#### 3. Pipeline Debugging (Alloy UI)

- 브라우저에서 `https://alloy.${DEFAULT_URL}`에 접속한다.
- **Graph View**: 컴포넌트 간의 연결 상태를 시각적으로 확인한다.
- **Component Details**: 각 컴포넌트의 상태, 수집된 타겟, 에러 로그를 확인한다.

### Common Pitfalls

- **Relabeling Regex**: 정규표현식이 틀리면 `service_name`이 잘못 지정되거나 `scope`가 `app`으로 오인될 수 있다.
- **Batch Size Tuning**: 배치가 너무 크면 지연 시간이 증가하고, 너무 작으면 백엔드 부하가 증가한다.
- **Docker Socket permissions**: Alloy 컨테이너가 `/var/run/docker.sock`에 접근할 수 있어야 discovery가 작동한다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/06-observability/alloy.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/06-observability/alloy.md)
- [Recovery runbook](../../runbooks/06-observability/alloy.md)
- [Operations template](../../../99.templates/operation.template.md)
