# InfluxDB (시계열 데이터베이스)

## 시스템 아키텍처에서의 역할

InfluxDB는 **시계열 데이터 저장 전문 데이터베이스**로 IoT 센서, 메트릭, 이벤트 데이터를 효율적으로 저장하고 쿼리합니다.

**핵심 역할:**

- ⏱️ **시계열 데이터**: 시간 기반 메트릭 저장
- 📊 **고성능 쿼리**: Flux 쿼리 언어
- 📈 **다운샘플링**: 자동 데이터 집계
- 🔌 **Telegraf 통합**: 데이터 수집

## 주요 구성 요소

### InfluxDB 2.7

- **컨테이너**: `influxdb`
- **이미지**: `influxdb:2.7`
- **포트**: `${INFLUXDB_PORT}` (기본 8086)
- **Traefik**: `https://influxdb.${DEFAULT_URL}`
- **IP**: 172.19.0.11

**초기 설정:**

- Username: `${INFLUXDB_USERNAME}`
- Organization: `${INFLUXDB_ORG}`
- Bucket: `${INFLUXDB_BUCKET}`
- Token: `${INFLUXDB_API_TOKEN}`

## 환경 변수

```bash
INFLUXDB_PORT=8086
INFLUXDB_HOST_PORT=8086
INFLUXDB_USERNAME=admin
INFLUXDB_PASSWORD=<password>
INFLUXDB_ORG=myorg
INFLUXDB_BUCKET=mybucket
INFLUXDB_API_TOKEN=<token>
INFLUXDB_DB_NAME=mydb
DEFAULT_URL=127.0.0.1.nip.io
```

## 접속 정보

### Web UI

- **URL**: `https://influxdb.127.0.0.1.nip.io`
- **계정**: admin / password

### CLI

```bash
# InfluxDB CLI
docker exec -it influxdb influx

# 쿼리
influx query 'from(bucket:"mybucket") |> range(start: -1h)'
```

## 사용 방법

### 데이터 쓰기 (Line Protocol)

```bash
curl -X POST "https://influxdb.127.0.0.1.nip.io/api/v2/write?org=myorg&bucket=mybucket

" \
  -H "Authorization: Token <token>" \
  -H "Content-Type: text/plain; charset=utf-8" \
  --data-binary "measurement,tag1=value1 field1=100 $(date +%s)000000000"
```

### Flux 쿼리

```flux
from(bucket: "mybucket")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "cpu")
  |> mean()
```

## 참고 자료

- [InfluxDB 문서](https://docs.influxdata.com/influxdb/v2/)
- [Flux 언어](https://docs.influxdata.com/flux/v0/)
