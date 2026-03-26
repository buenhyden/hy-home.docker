# Observability Technical Specification

> Detailed System Configuration and Integration Spec for the LGTM Stack.

## Overview (KR)

이 문서는 `06-observability` 티어의 기술 명세와 구현 세부 사항을 정의한다. PRD 요구사항을 바탕으로 8개 이상의 개별 서비스(Prometheus, Grafana, Loki, Tempo, Alloy 등)의 포트 매핑, 볼륨 구성, 그리고 상호 서비스 의존성을 구체화한다.

## Strategic Boundaries & Non-goals

- **Owns**: 
    - 텔레메트리 수집기(Alloy) 설정
    - 데이터 저장소(Loki/Tempo/Prometheus) 라이프사이클 관리
    - 시각화(Grafana) 및 알람(Alertmanager) 프로비저닝
- **Does Not Own**: 
    - MinIO 버킷 자체의 관리 (04-data 영역)
    - Keycloak의 SSO 세션 관리 (02-auth 영역)

## Related Inputs

- **PRD**: `[../../01.prd/2026-03-26-06-observability.md]`
- **ARD**: `[../../02.ard/0006-observability-architecture.md]`
- **Related ADRs**: `[../../03.adr/0006-lgtm-stack-selection.md]`

## Contracts

- **Config Contract**: 
    - 모든 설정 파일은 `/etc/<service>/<config>` 경로에 위치하며 읽기 전용(`:ro`)으로 마운트된다.
    - 민감한 정보(비밀번호, 토큰)는 Docker Secrets를 통해 주입된다.
- **Data Contract**: 
    - 텔레메트리 데이터는 OTLP(gRPC/4317, HTTP/4318) 프로토콜을 사용한다.
    - Loki와 Tempo는 MinIO S3 API를 통해 버킷에 접근한다.
- **Governance Contract**: 
    - Grafana 대시보드는 `provisioning/dashboards` 설정을 통해 코드 기반으로 동기화되어야 한다.

## Core Design

### Tech Stack

| Service | Version | Port (Internal) | Port (Host) |
| :--- | :--- | :--- | :--- |
| Prometheus | v3.9.0 | 9090 | 9090 |
| Grafana | 12.3.3 | 3000 | 3000 |
| Loki | 3.6.6 | 3100 | 3100 |
| Tempo | 2.10.1 | 3200 | 3200 |
| Grafana Alloy | v1.13.1 | 12345 (UI) | 12345 |
| Pyroscope | 1.18.1 | 4040 | 4040 |
| Alertmanager | v0.30.0 | 9093 | 9093 |
| cAdvisor | v0.55.1 | 8080 | 8080 |

### Key Dependencies

- **Storage**: MinIO (`04-data`) - Bukets: `loki-data`, `tempo-data`.
- **Auth**: Keycloak (`02-auth`) - Realm: `hy-home.realm`.
- **Network**: `infra_net` 브리지 네트워크 사용.

## Data Modeling & Storage Strategy

- **MinIO S3 Integration**:
    - Loki/Tempo는 MinIO 컨테이너 아이디나 Traefik 엔드포인트를 통해 접근한다.
    - 인증 정보는 `minio_app_user_password` 시크릿을 공유한다.
- **Local Persistence**: 
    - Prometheus TSDB 데이터는 `${DEFAULT_OBSERVABILITY_DIR}/prometheus`에 마운트된다.

## Interfaces & Data Structures

### Alloy OTLP Configuration (Concept)
```hcl
otlp.receiver "default" {
  grpc { endpoint = "0.0.0.0:4317" }
  http { endpoint = "0.0.0.0:4318" }
  output {
    metrics = [prometheus.remote_write.default.receiver]
    logs    = [loki.write.default.receiver]
    traces  = [otelcol.exporter.otlp.tempo.input]
  }
}
```

## Verification

### Service Health Check
```bash
# Prometheus health check
wget -qO- http://localhost:9090/-/healthy

# Loki readiness check
wget -qO- http://localhost:3100/ready

# Grafana API health
wget -qO- http://localhost:3000/api/health
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: 모든 관측 서비스 컨테이너가 `healthy` 상태로 기동되어야 함.
- **VAL-SPC-002**: Grafana UI 접속 시 Keycloak으로 자동 리다이렉션되어야 함.
- **VAL-SPC-003**: cAdvisor 메트릭이 Prometheus를 거쳐 Grafana 대시보드에 가시화되어야 함.

## Related Documents

- **Plan**: `[../../05.plans/2026-03-26-06-observability-standardization.md]`
- **Tasks**: `[../../06.tasks/2026-03-26-06-observability-tasks.md]`
- **Runbook**: `[../../09.runbooks/06-observability/README.md]`
