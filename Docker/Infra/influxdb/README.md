# InfluxDB

**InfluxDB**는 시계열 데이터(Time Series Data)를 저장하고 조회하는 데 최적화된 데이터베이스입니다.
모니터링 메트릭, IoT 센서 데이터 등을 저장하는 데 사용됩니다.

## 🚀 서비스 구성

| 서비스명 | 역할 | 포트 |
| --- | --- | --- |
| **influxdb** | InfluxDB 서버 | `8086` |

## 🛠 설정 및 환경 변수

- **이미지**: `bitnami/influxdb:latest`
- **초기 설정**:
    - `INFLUXDB_ADMIN_USER`: 관리자 계정
    - `INFLUXDB_ADMIN_USER_PASSWORD`: 관리자 비밀번호
    - `INFLUXDB_ADMIN_ORG`: 초기 조직(Org) 이름
    - `INFLUXDB_ADMIN_BUCKET`: 초기 버킷(Bucket) 이름

## 📦 볼륨 마운트

- `influxdb-node1-volume`: 데이터 저장소 (`/bitnami/influxdb`)

## 🏃‍♂️ 실행 방법

```bash
docker compose up -d
```

## ⚠️ 주의사항
- **버전**: InfluxDB v2를 사용합니다. (Flux 쿼리 언어 사용)
