# Apache Cassandra

**Apache Cassandra**는 높은 확장성과 가용성을 제공하는 분산 NoSQL 데이터베이스입니다.
이 구성은 단일 노드(또는 멀티 노드 확장 가능) 클러스터와 모니터링을 위한 Exporter를 포함합니다.

## 🚀 서비스 구성

| 서비스명 | 역할 | 포트 |
| --- | --- | --- |
| **cassandra-node1** | Cassandra 데이터베이스 노드 | `9042` (Client), `7000` (Inter-node) |
| **cassandra-exporter** | Prometheus용 메트릭 Exporter | `8080` (Default) |

## 🛠 설정 및 환경 변수

- **이미지**: `bitnami/cassandra:latest`
- **인증**: `CASSANDRA_PASSWORD_SEEDER=yes`로 초기 비밀번호 설정.
- **메모리**: `MAX_HEAP_SIZE=2G`, `HEAP_NEWSIZE=200M` (리소스 제한 설정)

## 📦 볼륨 마운트

- `cassandra-node1-volume`: 데이터 저장소 (`/bitnami/cassandra`)

## 🏃‍♂️ 실행 방법

```bash
docker compose up -d
```

## ⚠️ 주의사항
- **초기화**: 첫 실행 시 클러스터 초기화에 시간이 걸릴 수 있습니다.
- **리소스**: Java 기반이므로 힙 메모리 설정에 유의하세요.
