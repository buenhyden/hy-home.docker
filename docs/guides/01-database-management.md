# 🗄️ Database Management Guide

고가용성 PostgreSQL 클러스터와 인메모리 데이터 저장소(Redis/Valkey)를 관리하는 방법입니다.

## 1. PostgreSQL HA Cluster (Patroni)

이 프로젝트는 **Patroni, etcd, HAProxy**를 조합하여 자동 페일오버가 가능한 Postgres 클러스터를 제공합니다.

### 클러스터 상태 확인

어떤 노드가 리더(Leader)인지, 동기화 상태는 어떠한지 확인하려면 다음 명령어를 사용합니다:

```bash
# pg-0 노드에서 확인 예시
docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml list
```

### 연결 가이드

개별 노드(`pg-0`, `pg-1` 등)에 직접 연결하지 말고, 항상 **HAProxy(Router)**를 통해 연결하십시오.

- **Write (Leader)**: `${POSTGRES_WRITE_HOST_PORT}` (기본 5432)
- **Read (Replica)**: `${POSTGRES_READ_HOST_PORT}` (기본 5433)

### 데이터 백업 및 복구

- 클러스터 전체 백업은 `pg_dumpall`을 리더 노드에 대해 실행합니다.
- 특정 DB 백업은 `pg_dump`를 사용합니다.

## 2. Managed DB (mng-db)

독립적인 형태의 PostgreSQL(`mng-pg`)와 Redis(`mng-redis`) 인스턴스는 인프라 서비스(Keycloak, n8n 등)의 메타데이터 저장용으로 사용됩니다.

- **mng-pg**: `172.19.0.21` (기본 포트 5432)
- **mng-redis**: `172.19.0.22` (기본 포트 6379)

## 3. Redis & Valkey Cluster

대규모 캐시나 세션 관리를 위해 고성능 분산 클러스터를 제공합니다.

- **Valkey**: Redis의 완전 오픈소스 포크 버전으로, 성능과 기능면에서 호환됩니다.
- **Cluster Mode**: 3개의 마스터와 3개의 복제본으로 구성되어 데이터 샤딩을 지원합니다.

### 관리 도구

- **Redis Insight**: 웹 브라우저(`http://redisinsight.${DEFAULT_URL}`)를 통해 클러스터 데이터를 시각적으로 탐색하고 관리할 수 있습니다.

## 4. Time-Series (InfluxDB)

모니터링 지표나 센서 데이터 저장을 위해 최적화된 시계열 데이터베이스입니다.

- **v2 API**: 조직(Org)과 버킷(Bucket) 개념으로 데이터를 관리합니다.
- **UI**: `http://influxdb.${DEFAULT_URL}`에서 쿼리 및 대시보드 작성이 가능합니다.
