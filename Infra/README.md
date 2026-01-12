# Infrastructure Platform

## 1. 서비스 개요 (Service Overview)

**서비스 정의**: 개발 및 운영에 필요한 핵심 인프라 서비스들을 Docker Compose 기반으로 통합 관리하는 플랫폼입니다.  
인증, 모니터링, 데이터베이스, 메시징 큐 등 모듈화된 마이크로서비스 아키텍처를 제공하며, `include` 기능을 통해 유연한 구성이 가능합니다.

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)

**시스템 구조도**:

```mermaid
graph TD
    User[사용자] -->|HTTPS/443| Traefik[Traefik Gateway]
    Traefik -->|Auth Check| OAuth2[OAuth2 Proxy]
    OAuth2 -->|Validate| Keycloak[Keycloak IAM]
    Traefik -->|Route| App[애플리케이션 서비스]
    Traefik -->|Route| Tools[운영 도구 (Grafana/Kibana 등)]
    
    subgraph Observability
        App -->|Metrics| Prometheus
        App -->|Logs| Loki
        App -->|Traces| Tempo
        Prometheus & Loki & Tempo --> Grafana
    end

    subgraph Data Layer
        App --> Postgres[PostgreSQL Cluster]
        App --> Redis[Redis/Valkey Cluster]
        App --> Kafka[Kafka Cluster]
    end
```

## 3. 시작 가이드 (Getting Started)

**사전 요구사항**:

- **Docker**: v24.0.0+
- **Docker Compose**: v2.20.0+ (필수)

**실행 방법**:

```bash
# 전체 인프라 실행
docker compose up -d

# 개별 서비스 실행 (예: DB만)
docker compose -f mng-db/docker-compose.yml up -d
```

## 4. 서비스 문서 목록 (Service Documentation)

각 서비스별 상세 문서는 아래 링크를 참조하십시오.

### Gateway & Auth

- [**Traefik**](./traefik/README.md): Edge Router & Ingress Controller.
- [**Keycloak**](./keycloak/README.md): Identity Access Management (IAM).
- [**OAuth2 Proxy**](./oauth2-proxy/README.md): Authentication Gateway.
- [**Nginx**](./nginx/README.md): Reverse Proxy & Auth Gateway.

### Databases & Storage

- [**PostgreSQL Cluster**](./postgresql-cluster/README.md): HA PostgreSQL 17 Cluster (Patroni + Etcd).
- [**Redis Cluster**](./redis-cluster/README.md): HA Redis 8.x Cluster (6 Nodes).
- [**Valkey Cluster**](./valkey-cluster/README.md): HA Valkey 9.x Cluster (Redis Fork).
- [**Mng-DB**](./mng-db/README.md): Shared Monitoring DB (Postgres/Valkey).
- [**CouchDB**](./couchdb/README.md): NoSQL Database Cluster.
- [**InfluxDB**](./influxdb/README.md): Time Series Database.
- [**MinIO**](./minio/README.md): S3 Compatible Object Storage.
- [**Qdrant**](./qdrant/README.md): Vector Database for AI/RAG.

### Messaging & Streaming

- [**Kafka**](./kafka/README.md): Event Streaming Platform (KRaft mode).
- [**KSQL**](./ksql/README.md): Stream Processing for Kafka.
- [**Airflow**](./airflow/README.md): Workflow Orchestration Platform.
- [**n8n**](./n8n/README.md): Workflow Automation Tool.

### Observability & AI

- [**Observability**](./observability/README.md): LGTM Stack (Prometheus, Loki, Tempo, Grafana, Alloy, Alertmanager).
- [**OpenSearch**](./opensearch/README.md): Distributed Search & Analytics Engine.
- [**Ollama**](./ollama/README.md): LLM Inference Engine & Open WebUI.

### DevOps & Utilities

- [**Harbor**](./harbor/README.md): Container Registry.
- [**SonarQube**](./sonarqube/README.md): Static Code Analysis & Code Quality.
- [**Storybook**](./storybook/README.md): Design System Component Explorer.
- [**Mail**](./mail/README.md): MailHog (Email Testing) & Stalwart.

## 5. 트러블슈팅 (Troubleshooting)

**공통 진단 가이드**:

1. **컨테이너 상태 확인**: `docker compose ps`
2. **로그 확인**: `docker compose logs -f [service_name]`
3. **네트워크 확인**: `docker network inspect infra_net`

---
**유지보수**: 본 문서는 인프라 변경 시마다 업데이트되어야 합니다.
