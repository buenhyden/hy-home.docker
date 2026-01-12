# Service Catalog

Complete reference of all infrastructure services with access details.

## Active Services

### Observability & Monitoring

| Service | URL | Port | Purpose |
|:---|:---|:---|:---|
| **Grafana** | <https://grafana.127.0.0.1.nip.io> | - | Unified observability dashboard |
| **Prometheus** | <https://prometheus.127.0.0.1.nip.io> | - | Metrics collection |
| **Alertmanager** | <https://alertmanager.127.0.0.1.nip.io> | - | Alert management |
| **Alloy** | <https://alloy.127.0.0.1.nip.io> | - | Telemetry collector |

### Database Management UIs

| Service | URL | Port | Purpose |
|:---|:---|:---|:---|
| **RedisInsight** | <https://redisinsight.127.0.0.1.nip.io> | - | Valkey cluster management (Redis-compatible) |
| **Kafka UI** | <https://kafka-ui.127.0.0.1.nip.io> | - | Kafka cluster management |
| **MinIO Console** | <https://minio-console.127.0.0.1.nip.io> | - | S3 storage management |
| **InfluxDB UI** | <https://influxdb.127.0.0.1.nip.io> | - | Time-series DB UI |

### Applications

| Service | URL | Port | Purpose |
|:---|:---|:---|:---|
| **n8n** | <https://n8n.127.0.0.1.nip.io> | - | Workflow automation |
| **Ollama WebUI** | <https://chat.127.0.0.1.nip.io> | - | LLM chat interface |
| **Keycloak Admin** | <https://keycloak.127.0.0.1.nip.io/admin> | - | IAM administration |
| **Traefik Dashboard** | <https://dashboard.127.0.0.1.nip.io> | - | Reverse proxy dashboard |
| **SonarQube** | <https://sonarqube.127.0.0.1.nip.io> | - | Code quality |

## Direct Database Access

### PostgreSQL (HA Cluster)

**Write Connection (HAProxy)**:

```
Host: localhost
Port: 5000
User: postgres
Password: <secrets/postgres_password.txt>
Database: postgres
```

**Read Connection (HAProxy)**:

```
Host: localhost
Port: 5001
User: postgres
Password: <secrets/postgres_password.txt>
```

**CLI Access**:

```bash
psql -h localhost -p 5000 -U postgres
```

### Valkey Cluster (Redis Compatible)

**Connection**:

```
Host: localhost
Port: 6379, 6380, 6381, 6382, 6383, 6384 (Cluster Nodes)
Password: <secrets/valkey_password.txt>
```

**CLI Access**:

```bash
docker exec -it valkey-node-0 valkey-cli -p 6379 -a $(cat secrets/valkey_password.txt)
```

### Kafka Cluster

**Bootstrap Servers**:

```
localhost:9092,localhost:9093,localhost:9094
```

**Schema Registry**:

```
http://localhost:8081
```

## Service Details

### Reverse Proxy & Security

| Component | Image | Version | Notes |
|:---|:---|:---|:---|
| Traefik | `traefik` | 3.3 | Dynamic routing |
| OAuth2 Proxy | `quay.io/oauth2-proxy/oauth2-proxy` | v7.8.1 | Forward auth |
| Keycloak | `quay.io/keycloak/keycloak` | 26.5.0 | SSO/IAM |

### Data Storage

| Component | Image | Version | Type |
|:---|:---|:---|:---|
| PostgreSQL | `bitnami/postgresql` | 17 | Relational DB (HA) |
| Valkey | `valkey/valkey` | 9.0.1 | Distributed Cache (Redis Fork) |
| InfluxDB | `influxdb` | 2.8 | Time-series |
| MinIO | `minio/minio` | latest | Object storage |
| Qdrant | `qdrant/qdrant` | latest | Vector DB |

### Messaging & Streaming

| Component | Image | Version | Notes |
|:---|:---|:---|:---|
| Kafka | `confluentinc/cp-kafka` | 8.1.1 | KRaft mode |
| Schema Registry | `confluentinc/cp-schema-registry` | 8.1.1 | Schema management |
| Kafka Connect | `confluentinc/cp-kafka-connect` | 8.1.1 | Integrations |
| ksqlDB | `confluentinc/ksqldb-server` | 0.29.0 | Stream processing |

### Observability Stack

| Component | Image | Version | Notes |
|:---|:---|:---|:---|
| Prometheus | `prom/prometheus` | latest | Metrics DB |
| Grafana | `grafana/grafana` | latest | Dashboards |
| Loki | `grafana/loki` | latest | Log aggregation |
| Tempo | `grafana/tempo` | latest | Tracing |
| Alloy | `grafana/alloy` | latest | OTel collector |
| cAdvisor | `gcr.io/cadvisor/cadvisor` | latest | Container metrics |

### Applications

| Component | Image | Version | Purpose |
|:---|:---|:---|:---|
| n8n | `n8nio/n8n` | latest | Workflow automation |
| Ollama | `ollama/ollama` | latest | LLM inference |
| Open WebUI | `ghcr.io/open-webui/open-webui` | main | LLM chat UI |
| SonarQube | `sonarqube` | community | Code quality |
| Harbor | `bitnami/harbor-*` | 2 | Registry |

## Optional / Disabled Services

These services are available in the `infra/` directory but are commented out in the main `docker-compose.yml` by default to save resources.

- **MailHog**: Email testing (`infra/mail`)
- **Airflow**: Workflow orchestration (`infra/airflow`)
- **OpenSearch**: Search engine (`infra/opensearch`)
- **CouchDB**: NoSQL DB (`infra/couchdb`)
- **Redis Cluster**: Legacy Redis implementation (replaced by Valkey) (`infra/redis-cluster`)
- **Nginx**: Web server (`infra/nginx`)
- **Storybook**: Component testing (`infra/storybook`)

## Port Mappings

| Service | Host Port | Container Port | Protocol |
|:---|:---|:---|:---|
| Traefik HTTP | 80 | 80 | HTTP |
| Traefik HTTPS | 443 | 443 | HTTPS |
| PostgreSQL Write | 5000 | 5000 | TCP |
| PostgreSQL Read | 5001 | 5001 | TCP |
| Valkey Node 0 | 6379 | 6379 | TCP |
| Kafka Broker 1 | 9092 | 9092 | TCP |
| Kafka Broker 2 | 9093 | 9092 | TCP |
| Kafka Broker 3 | 9094 | 9092 | TCP |

## Authentication

### Protected Services (SSO via OAuth2 Proxy)

**Active Services:**

- Grafana
- RedisInsight
- Kafka UI

**Optional/Disabled Services:**

- Storybook
- Stalwart (MailHog replacement)
- Flower (Airflow UI)

Login via Keycloak when accessing these services.

### Self-Authenticated Services

These services have their own authentication systems:

- Keycloak (IAM with own login)
- n8n (built-in authentication)
- Ollama WebUI (built-in authentication)
- SonarQube (built-in authentication)

### Public Services

- Traefik Dashboard (accessible without authentication)

## Resource Requirements

See [System Architecture](../architecture/system-architecture.md) for detailed resource requirements.

## See Also

- [Environment Variables Reference](./environment-variables.md)
- [Network Topology](../architecture/network-topology.md)
- [Deployment Guide](../guides/deployment-guide.md)
