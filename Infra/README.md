# Infrastructure Services

이 디렉토리는 시스템 전체를 구성하는 다양한 인프라 서비스들의 Docker Compose 구성과 설정을 담고 있습니다. 각 디렉토리는 특정 목적이나 기술 스택에 따른 서비스 그룹을 나타냅니다.

## 📂 디렉토리 구조 및 서비스 요약

| 디렉토리 | 주요 서비스 | 설명 및 역할 |
|---|---|---|
| **[airflow](./airflow)** | Airflow (Web, Scheduler, Worker) | 데이터 파이프라인 및 워크플로우 오케스트레이션 (Celery Executor + Redis/Postgres) |
| **[arangodb](./arangodb)** | (Empty) | (현재 미구성) ArangoDB 구성을 위한 플레이스홀더 |
| **[couchdb](./couchdb)** | CouchDB (3-Node Cluster) | 멀티 노드 문서형 데이터베이스 클러스터 (Sticky Session 로드밸런싱 적용) |
| **[harbor](./harbor)** | Harbor Registry | 프라이빗 도커 이미지 및 헬름 차트 저장소 |
| **[influxdb](./influxdb)** | InfluxDB | 시계열 데이터 저장소 (v2.x) |
| **[kafka](./kafka)** | Kafka (KRaft), Connect, UI | 3-Node KRaft 모드 Kafka 클러스터 및 관련 에코시스템 (Schema Registry, Connect, REST Proxy) |
| **[keycloak](./keycloak)** | Keycloak | 통합 인증/인가(IAM) 및 SSO 서버 (OIDC/OAuth2 지원) |
| **[ksql](./ksql)** | KsqlDB | Kafka 스트림 데이터 처리를 위한 KSQL 엔진 |
| **[mail](./mail)** | MailHog | 개발/테스트용 SMTP 서버 및 Web UI (Stalwart는 비활성 상태) |
| **[minio](./minio)** | MinIO | S3 호환 오브젝트 스토리지 & 자동 버킷 생성 |
| **[mng-db](./mng-db)** | PostgreSQL, Redis, RedisInsight | 관리형 공용 데이터베이스 및 Redis GUI 도구 모음 |
| **[n8n](./n8n)** | n8n (Main, Worker) | 워크플로우 자동화 도구 (Queue 모드 - 대규모 처리용) |
| **[nginx](./nginx)** | Nginx | 정적 서빙 및 리버스 프록시 (MinIO 연동 등) |
| **[oauth2-proxy](./oauth2-proxy)** | OAuth2 Proxy | Keycloak과 연동하여 애플리케이션에 인증 미들웨어를 제공하는 프록시 |
| **[observability](./observability)** | LGTM Stack (Loki, Grafana, Tempo, Prometheus) | 통합 관제 스택: 로그, 메트릭, 트레이싱 수집 및 시각화 (Alloy, cAdvisor, Alertmanager 포함) |
| **[ollama](./ollama)** | Ollama, Qdrant, Open WebUI | 로컬 LLM 실행, 벡터 DB(RAG), 챗봇 인터페이스 |
| **[opensearch](./opensearch)** | OpenSearch, Dashboards | 검색 엔진 및 데이터 분석/시각화 플랫폼 |
| **[postgresql-cluster](./postgresql-cluster)** | Patroni, Etcd, HAProxy | 고가용성(HA)을 보장하는 PostgreSQL 클러스터 (자동 페일오버 지원) |
| **[redis-cluster](./redis-cluster)** | Redis (6-Node Cluster) | 데이터 샤딩을 지원하는 Redis Cluster (3 Master + 3 Replica) |
| **[traefik](./traefik)** | Traefik | 시스템의 모든 트래픽을 관리하는 엣지 라우터 및 리버스 프록시 |

## 🚀 아키텍처 개요

모든 서비스는 `infra_net`이라는 공통 Docker 네트워크를 통해 서로 통신합니다. 외부에서의 접근은 **Traefik**이 담당하며, 도메인 기반 라우팅(`*.${DEFAULT_URL}`)을 수행합니다.

- **Gateway**: Traefik
- **Auth**: Keycloak + OAuth2 Proxy
- **Observability**: Prometheus(Metrics), Loki(Logs), Tempo(Traces) -> Grafana
- **Data Stores**: Postgres Cluster, Redis Cluster, MinIO, CouchDB, Kafka, OpenSearch

## 🔗 빠른 시작

각 디렉토리 내의 `README.md`를 참고하여 `docker-compose up -d` 명령으로 서비스를 실행할 수 있습니다. 대부분의 서비스는 `.env` 파일에 정의된 환경 변수를 필요로 합니다.
