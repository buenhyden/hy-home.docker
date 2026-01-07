# Observability Stack (LGTM)

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 시스템 전반의 상태를 감시하고 분석하기 위한 통합 관측성(Observability) 플랫폼입니다.  
**LGTM 스택**(Loki, Grafana, Tempo, Prometheus/Mimir)을 기반으로 메트릭, 로그, 트레이스를 통합 수집 및 시각화합니다.

## 2. 주요 기능 (Key Features)
- **Unified Visualization**: Grafana를 통해 모든 데이터(Metrics, Logs, Traces)를 하나의 대시보드에서 시각화.
- **Metrics Collection**: Prometheus가 인프라 및 애플리케이션의 시계열 데이터를 수집.
- **Log Aggregation**: Loki가 분산된 컨테이너 로그를 중앙에서 수집하고 인덱싱 (Label 기반).
- **Distributed Tracing**: Tempo가 마이크로서비스 간의 요청 흐름(Trace)을 추적.
- **Telemetry Collection**: Grafana Alloy(구 Agent)가 OpenTelemetry(OTel) 데이터를 수집하여 처리.

## 3. 기술 스택 (Tech Stack)
- **Visualization**: `grafana/grafana:12.3.1`
- **Metrics**: `prom/prometheus:v3.8.1`, `prom/pushgateway:v1.11.2`, `gcr.io/cadvisor`
- **Logs**: `grafana/loki:3.5.9`
- **Traces**: `grafana/tempo:2.9.0`
- **Collector**: `grafana/alloy:v1.12.1`
- **Alerting**: `prom/alertmanager:v0.30.0`

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 데이터 파이프라인
1.  **Sources**:
    - **Containers**: cAdvisor가 리소스 사용량 수집.
    - **Applications**: Alloy(OTLP) 또는 Prometheus SDK를 통해 메트릭/로그/트레이스 전송.
2.  **Collectors**:
    - **Prometheus**: Pull 방식으로 Exporter(Node, Redis, PG 등)에서 메트릭 수집.
    - **Alloy**: OTel 데이터를 받아 Tempo(Trace)와 Loki(Log)로 분배.
3.  **Storage**:
    - **Prometheus**: 시계열 DB (TSDB).
    - **Loki**: 로그 청크 저장소.
    - **Tempo**: 트레이스 저장소.
4.  **UI**: Grafana가 위 저장소들을 DataSource로 연결하여 대시보드 제공.

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```

**로그인**:
- Keycloak SSO가 연동되어 있어 `Sign in with Keycloak` 버튼을 통해 로그인합니다.
- 초기 관리자 계정: `GRAFANA_ADMIN_USERNAME` / `GRAFANA_ADMIN_PASSWORD` (SSO 문제 발생 시 사용).

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 Grafana 대시보드
- **접속**: `https://grafana.${DEFAULT_URL}`
- **Provisioning**: `./grafana/provisioning` 디렉토리에 정의된 대시보드가 자동으로 로드됩니다.
- **Data Source**: Prometheus, Loki, Tempo, Alertmanager가 이미 연동되어 있습니다.

### 6.2 모니터링 대상 추가
- **Prometheus**: `prometheus/config/prometheus.yml`의 `scrape_configs`에 타겟 추가.
- **Alloy**: `alloy/config/config.alloy`에서 OTel 리시버 설정 변경.

## 7. 환경 설정 명세 (Configuration Reference)
### 주요 환경 변수
- `GF_AUTH_GENERIC_OAUTH_...`: Grafana의 Keycloak SSO 연동 설정.
- `SMTP_...`: Alertmanager의 이메일 발송 설정.

### 네트워크 포트 (Ports)
- **Grafana**: 3000 (`https://grafana.${DEFAULT_URL}`)
- **Prometheus**: 9090 (`https://prometheus.${DEFAULT_URL}`)
- **Alloy UI**: 12345 (`https://alloy.${DEFAULT_URL}`)
- **Alertmanager**: 9093 (`https://alertmanager.${DEFAULT_URL}`)

### 볼륨 마운트 (Volumes)
- 각 서비스(`grafana`, `prometheus`, `loki`, `tempo`, `alertmanager`)별로 전용 `*-data` 볼륨이 마운트되어 데이터 영속성을 보장합니다.

## 8. 통합 및 API 가이드 (Integration Guide)
**OpenTelemetry (OTLP) Endpoint**:
- gRPC: `alloy:4317`
- HTTP: `alloy:4318`
애플리케이션에서 위 주소로 Trace 및 Metric을 전송하도록 설정하십시오.

## 9. 가용성 및 관측성 (Availability & Observability)
**Health Check**:
- 각 컨테이너는 `wget`을 통한 내부 Healthcheck가 구성되어 있습니다.
- 인프라 전체 상태는 Grafana 대시보드의 "Infrastructure Overview" (예시) 등에서 확인할 수 있습니다.

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**백업 전략**:
- **Grafana**: 대시보드 JSON 파일과 데이터소스 설정은 Git으로 관리(`Provisioning`)하는 것이 가장 안전합니다.
- **Prometheus**: `/prometheus` 볼륨 스냅샷 권장.

## 11. 보안 및 강화 (Security Hardening)
- **Authentication**: Grafana 로그인 폼을 비활성화하고 SSO를 강제하여 보안을 강화했습니다.
- **Network**: 데이터 저장소(Loki, Tempo 등)의 포트는 외부에 노출되지 않고 내부 네트워크에서만 접근 가능합니다.

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **cAdvisor Error**: 윈도우 환경에서 `/dev/kmsg` 관련 에러가 발생할 수 있습니다. 이 경우 `docker-compose.yml`에서 해당 디바이스 매핑을 주석 처리하십시오.
- **Grafana Login Loop**: Keycloak의 Redirect URI 설정이 `https://grafana.${DEFAULT_URL}/login/generic_oauth`로 정확한지 확인하십시오.

---
**공식 문서**: [https://grafana.com/docs/](https://grafana.com/docs/)
