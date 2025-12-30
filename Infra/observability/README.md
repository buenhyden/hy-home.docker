# Observability Infrastructure (LGTM Stack)

## 1. 개요 (Overview)
이 디렉토리는 시스템의 모니터링, 로깅, 트레이싱을 담당하는 통합 관제 스택(LGTM: Loki, Grafana, Tempo, Mimir/Prometheus)을 정의합니다. 시스템의 상태를 가시화하고 문제를 진단하는 핵심 인프라입니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **prometheus** | Metrics Storage | 서비스들로부터 메트릭을 수집(Pull)하고 저장하는 시계열 데이터베이스입니다. |
| **loki** | Log Aggregation | 애플리케이션 및 시스템 로그를 수집하고 쿼리할 수 있게 해주는 로그 시스템입니다. |
| **tempo** | Distributed Tracing | 마이크로서비스 간의 요청 흐름(Trace)을 추적하고 시각화하는 백엔드입니다. |
| **grafana** | Visualization | 모든 데이터(Metrics, Logs, Traces)를 하나의 대시보드에서 시각화하는 UI 도구입니다. |
| **alloy** | Telemetry Collector | OpenTelemetry 등을 통해 데이터를 수집하여 각 backend(Prometheus, Loki, Tempo)로 전송하는 수집기입니다. |
| **cadvisor** | Container Metrics | 실행 중인 Docker 컨테이너의 리소스 사용량(CPU, RAM 등) 메트릭을 제공합니다. |
| **alertmanager** | Alerting | Prometheus 등에서 감지된 경보를 라우팅하고 알림(Slack, Email 등)을 발송합니다. |
| **pushgateway** | Push Metrics | 배치 작업 등 짧은 수명 주기를 가진 작업이 메트릭을 Push 할 수 있도록 돕는 게이트웨이입니다. |

## 3. 구성 및 설정 (Configuration)

### Grafana & Keycloak 연동
Grafana는 Keycloak과 OAuth2로 연동되어 있습니다.
- **Auto Login**: `GF_AUTH_OAUTH_AUTO_LOGIN=true` (로그인 화면 스킵)
- **Role Mapping**: Keycloak의 그룹 정보(`/admins`, `/editors`)를 기반으로 Grafana의 Admin/Editor 권한을 자동 부여합니다.

### 수집 파이프라인
- **Logs**: Alloy 또는 Docker Logging Driver -> Loki
- **Metrics**: Exporters -> Prometheus (Scraping)
- **Traces**: App(OTel SDK) -> Alloy -> Tempo

### 로드밸런싱 (Traefik)
각 서비스는 Traefik을 통해 서브도메인으로 노출됩니다.
- `grafana.${DEFAULT_URL}`
- `prometheus.${DEFAULT_URL}`
- `alertmanager.${DEFAULT_URL}`
- `alloy.${DEFAULT_URL}`
- `pushgateway.${DEFAULT_URL}`

### 데이터 볼륨
각 스토리지 서비스는 영구 볼륨을 사용하여 데이터를 보존합니다.
- `prometheus-data`, `loki-data`, `tempo-data`, `grafana-data`, `alertmanager-data`
