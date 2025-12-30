# InfluxDB Infrastructure

## 1. 개요 (Overview)
이 디렉토리는 시계열 데이터베이스인 InfluxDB(v2.7)를 정의합니다. 메트릭 데이터 수집 및 모니터링 용도로 사용됩니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **influxdb** | Time Series DB | 시계열 데이터 저장소입니다. 초기 실행 시 지정된 버킷과 조직, 사용자를 자동 설정합니다. |

## 3. 구성 및 설정 (Configuration)

### 초기 설정 (Initialization)
컨테이너 최초 실행 시 환경 변수를 통해 자동 설정(`setup` 모드)이 수행됩니다.
- `DOCKER_INFLUXDB_INIT_MODE`: setup
- `DOCKER_INFLUXDB_INIT_USERNAME`: 초기 관리자 ID
- `DOCKER_INFLUXDB_INIT_PASSWORD`: 초기 관리자 PW
- `DOCKER_INFLUXDB_INIT_ORG`: 초기 조직(Org) 이름
- `DOCKER_INFLUXDB_INIT_BUCKET`: 기본 버킷 이름

### 데이터 볼륨
- `influxdb-data`: `/var/lib/influxdb2` 경로에 매핑되어 데이터 영속성을 보장합니다.

### 로드밸런싱 (Traefik)
- **URL**: `https://influxdb.${DEFAULT_URL}`
- Traefik을 통해 외부에서 HTTPS로 접근 가능합니다.
