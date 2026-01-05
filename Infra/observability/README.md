# LGTM Observability Stack

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 시스템의 모든 영역을 모니터링하기 위한 풀스택 관측성 플랫폼입니다. Grafana Labs의 LGTM(Loki, Grafana, Tempo, Mimir/Prometheus) 스택을 기반으로 합니다.

**주요 기능 (Key Features)**:
- **Metrics**: Prometheus가 수치 데이터 수집 및 쿼리.
- **Logs**: Loki가 로그 데이터 집계 및 인덱싱.
- **Traces**: Tempo가 분산 트레이싱 데이터 저장.
- **Visualization**: Grafana를 통해 통합 대시보드 제공.
- **Collector**: Alloy(구 Agent)가 OTel 데이터 수집 및 전송.

**기술 스택 (Tech Stack)**:
- **Viz**: Grafana 12.3.1
- **Metrics**: Prometheus v3.8.1, cAdvisor v0.54.1, Pushgateway
- **Logs**: Loki 3.5.9
- **Traces**: Tempo 2.9.0
- **Alerting**: Alertmanager v0.30.0

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)
**데이터 흐름**:
1. **수집**: cAdvisor(컨테이너), Alloy(OTel), Exporters -> Prometheus/Loki/Tempo.
2. **저장**: 각 전용 저장소(TSDB, Log store 등)에 저장.
3. **시각화**: Grafana가 각 데이터 소스를 쿼리하여 대시보드에 표출.

## 3. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```

## 4. 환경 설정 명세 (Configuration Reference)
**볼륨 마운트**:
- `prometheus-data`, `loki-data`, `tempo-data`, `grafana-data`: 각 서비스의 데이터 영속화.
- `./grafana/provisioning`: 대시보드 및 데이터소스 자동 프로비저닝 설정.

**주요 계정 설정 (Grafana)**:
- 관리자 계정: `${GRAFANA_ADMIN_USERNAME}` / `${GRAFANA_ADMIN_PASSWORD}`
- **SSO**: Keycloak 연동이 설정되어 있어 `Sign in with Keycloak` 버튼을 통해 로그인합니다.

## 5. 통합 및 API 가이드 (Integration Guide)
**엔드포인트 명세**:
- **Grafana**: `https://grafana.${DEFAULT_URL}`
- **Prometheus**: `https://prometheus.${DEFAULT_URL}`
- **Alertmanager**: `https://alertmanager.${DEFAULT_URL}`
- **Alloy UI**: `https://alloy.${DEFAULT_URL}`

**SSO 통합**:
- Grafana는 `GF_AUTH_GENERIC_OAUTH_...` 환경 변수를 통해 Keycloak과 연동됩니다.
- Keycloak의 `groups` 클레임을 읽어 Grafana의 `Admin`/`Editor`/`Viewer` 권한을 자동으로 매핑합니다.

## 6. 가용성 및 관측성 (Availability & Observability)
**상태 확인**:
- 각 서비스별 `/ready`, `/-/healthy`, `/api/health` 등 헬스체크 엔드포인트 존재.

## 7. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 백업**:
- 중요 데이터(Prometheus TSDB, Grafana DB)는 볼륨 백업 필요.
- Grafana 대시보드는 Git(`provisioning` 폴더)으로 관리하여 코드 기반 복구 가능.

## 8. 보안 및 강화 (Security Hardening)
- Grafana 로그인 폼(`GF_AUTH_DISABLE_LOGIN_FORM=true`)을 비활성화하여 SSO를 강제합니다.
- 익명 사용자 접근은 차단되어 있습니다.

## 9. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **OOM Killed**: Loki나 Prometheus는 메모리 사용량이 높으므로 리소스 제한 확인 필요.
- **cAdvisor Error**: 윈도우 환경에서 `kmsg` 또는 `machine-id` 마운트 에러 발생 시 docker-compose 파일 수정.
