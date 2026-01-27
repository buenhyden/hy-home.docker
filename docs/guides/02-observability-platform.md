# 📊 Observability Platform Guide

LGTM(Loki, Grafana, Tempo, Mimir/Prometheus) 스택을 활용한 통합 모니터링 환경 가이드입니다.

## 1. Unified Dashboard (Grafana)

모든 데이터의 시각화를 담당하는 허브입니다.

- **접속 주소**: `https://grafana.${DEFAULT_URL}`
- **로그인**: Keycloak SSO와 연동되어 있습니다 (초기 설정 시 admin 계정 필요).

### 등록된 데이터 소스

- **Prometheus**: 시스템 및 서비스 메트릭 (지표)
- **Loki**: 모든 컨테이너의 표준 출력 로그
- **Tempo**: 마이크로서비스 간의 분산 추적 (Traces)
- **InfluxDB**: 시계열 분석용 데이터

## 2. Telemetry Collector (Grafana Alloy)

이 프로젝트는 기존의 `Promtail`이나 `OTel Collector` 대신 최신 **Grafana Alloy**를 단일 에이전트로 사용합니다.

- **역할**: 로그 수집, OTLP 데이터 변환, Prometheus 메트릭 스크래핑.
- **설정**: `infra/observability/alloy/config.alloy` 파일을 통해 수집 규칙을 정의합니다.

## 3. Metric Aggregation (Prometheus)

컨테이너 리소스 사용량, DB 성능 지표 등을 수집합니다.

- **Targets**: `https://prometheus.${DEFAULT_URL}/targets`에서 수집 대상들의 상태를 확인할 수 있습니다.
- **Exporters**: `node-exporter` (호스트 지표), `cadvisor` (컨테이너 지표), `postgres-exporter` (DB 지표)가 사전 구성되어 있습니다.

## 4. Log Aggregation (Loki)

로그 파일 없이 대량의 로그 데이터를 효율적으로 저장하고 검색(LogQL)할 수 있게 합니다.

### 로그 검색 팁

Grafana의 **Explore** 탭에서 다음과 같이 쿼리하세요:

- `{container_name="traefik"}`: Traefik 컨테이너 로그 보기
- `{level="error"}`: 시스템 내 모든 에러 로그 필터링

## 5. Distributed Tracing (Tempo)

서비스 간의 요청 흐름을 시각적으로 추적하여 병목 지점을 찾습니다.

- **OTLP**: 애플리케이션에서 `172.19.0.34:4317` (Alloy) 주소로 트레이스 데이터를 전송하면 Tempo로 전달됩니다.
