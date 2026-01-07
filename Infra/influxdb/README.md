# InfluxDB

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 고성능 시계열 데이터베이스(Time Series Database, TSDB)입니다.  
IoT 디바이스 메트릭, 애플리케이션 모니터링 로그 등 시간 흐름에 따라 발생하는 대량의 데이터를 저장하고 분석하는 데 최적화되어 있습니다.

## 2. 주요 기능 (Key Features)
- **Time Series Optimized**: 높은 쓰기 성능과 시간 기반 쿼리 처리에 특화됨.
- **Flux Language**: 데이터 필터링, 조인, 집계를 위한 강력한 스크립팅 언어 제공.
- **Dashboard**: 웹 기반 UI를 통해 데이터를 시각화하고 대시보드를 생성 기능.
- **Tasks**: 주기적인 데이터 처리 및 알림 작업 예약 가능.

## 3. 기술 스택 (Tech Stack)
- **Image**: `influxdb:2.7`
- **Interface**: HTTP API, Web UI
- **Query Language**: Flux, InfluxQL (Compatibility Mode)

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 데이터 파이프라인
1.  **Ingest**: Telegraf, Client Libraries, API를 통해 데이터 쓰기 요청.
2.  **Storage**: 시계열 데이터를 Bucket 단위로 저장하고 보존 정책(Retention Policy)에 따라 관리.
3.  **Query & Visualize**: Grafana 또는 내장 UI를 통해 시각화하거나 Flux 스크립트로 데이터 가공.

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
> **참고**: `DOCKER_INFLUXDB_INIT_MODE=setup` 설정에 의해 최초 실행 시 Organization, Bucket, Admin User가 자동 생성됩니다.

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 Web UI 사용
1.  **접속**: 브라우저에서 `https://influxdb.${DEFAULT_URL}` 접속.
2.  **로그인**: `INFLUXDB_USERNAME` / `INFLUXDB_PASSWORD` (환경변수 값).
3.  **기능 탐색**:
    - **Data Explorer**: Flux 쿼리를 작성하고 즉시 결과 확인.
    - **Boards**: 메트릭 대시보드 생성.
    - **Load Data**: API Token 발급 및 Telegraf 설정 가이드 확인.

### 6.2 CLI 사용법 (Inside Container)
컨테이너 내부의 `influx` CLI를 사용하여 관리 작업을 수행할 수 있습니다.

```bash
# 컨테이너 접속
docker exec -it influxdb /bin/bash

# 버킷 목록 확인
influx bucket list -o my-org

# 데이터 삭제 (예: 특정 시간 범위)
influx delete --bucket my-bucket --start 2023-01-01T00:00:00Z --stop 2023-01-02T00:00:00Z
```

## 7. 환경 설정 명세 (Configuration Reference)
### 환경 변수 (Environment Variables)
- `DOCKER_INFLUXDB_INIT_MODE`: `setup` (자동 초기화 활성화).
- `DOCKER_INFLUXDB_INIT_USERNAME`: 초기 관리자 아이디.
- `DOCKER_INFLUXDB_INIT_PASSWORD`: 초기 관리자 비밀번호.
- `DOCKER_INFLUXDB_INIT_ORG`: 초기 조직(Organization) 이름.
- `DOCKER_INFLUXDB_INIT_BUCKET`: 초기 버킷(Bucket) 이름.
- `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN`: 초기 관리자 API 토큰 (고정값 사용 시 유용).

### 볼륨 마운트 (Volumes)
- `influxdb-data`: `/var/lib/influxdb2` (데이터 및 메타데이터 저장).

### 네트워크 포트 (Ports)
- **8086**: InfluxDB API 및 Web UI 포트 (`https://influxdb.${DEFAULT_URL}`).

## 8. 통합 및 API 가이드 (Integration Guide)
**API 엔드포인트**:
- **Write URL**: `https://influxdb.${DEFAULT_URL}/api/v2/write?org=...&bucket=...`
- **Query URL**: `https://influxdb.${DEFAULT_URL}/api/v2/query?org=...`

**인증 (Authentication)**:
- HTTP 헤더에 `Authorization: Token <Your-Admin-Token>` 추가.

## 9. 가용성 및 관측성 (Availability & Observability)
**Health Check**:
- `/health` 엔드포인트를 통해 서비스 상태를 확인할 수 있습니다.
- Docker Healthcheck가 설정되어 있지 않다면 추가하는 것을 권장합니다 (`curl -f http://localhost:8086/health` 사용).

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 백업**:
- InfluxDB는 파일 시스템 레벨 복사보다 `influx backup` 명령어를 권장합니다.
- **Backup**:
    ```bash
    influx backup /path/to/backup_dir -t <admin-token>
    ```
- **Restore**:
    ```bash
    influx restore /path/to/backup_dir -t <admin-token>
    ```

## 11. 보안 및 강화 (Security Hardening)
- **Token Management**: 운영 환경에서는 용도별(읽기 전용, 쓰기 전용)로 토큰을 분리하여 발급하고, Admin Token 사용을 최소화하십시오.
- **TLS**: InfluxDB 2.x는 자체 TLS를 지원하지만, 여기서는 Traefik을 통해 TLS를 처리(Termination)하고 내부망은 HTTP로 통신합니다.

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Unauthorized (401)**: 토큰이 올바르지 않거나 조직(Org), 버킷(Bucket) 이름이 일치하지 않을 때 발생합니다.
- **High Memory Usage**: 카디널리티(Cardinality)가 높은 태그(예: UUID)를 사용할 경우 인덱스 크기가 급증할 수 있습니다. 스키마 설계 시 유의하세요.

---
**공식 문서**: [https://docs.influxdata.com/influxdb/v2/](https://docs.influxdata.com/influxdb/v2/)
