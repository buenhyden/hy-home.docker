# Migrated Infra Configuration & Setup

<!-- MIGRATED CONTENT BELOW -->

## Context: Hy-Home Infrastructure (infra/) (README.md)

##

# Hy-Home Infrastructure (infra/)

이 디렉토리는 `Docker Compose`로 구축된 홈 서버/개발 환경 인프라의 **서비스 정의**를 관리합니다. 각 서비스는 `infra/<번호-카테고리>/<서비스명>/docker-compose.yml`에 분리되어 있으며, **저장소 루트의 `docker-compose.yml`에서 `include`** 기능으로 통합됩니다.

## Context: Hy-Home Infrastructure (infra/) (README.md)

## 🏗️ 전체 구조

```text
infra/
├── 01-gateway/               # Edge/Gateway
│   └── traefik/
├── 02-auth/                  # 인증/SSO
│   └── keycloak/
├── 03-security/              # 시크릿/보안
│   └── vault/
├── 04-data/                  # DB/Storage
│   └── postgresql-cluster/
├── 05-messaging/             # 메시징/스트리밍
│   └── kafka/
├── 06-observability/         # LGTM 스택
│   ├── docker-compose.yml
│   └── prometheus/
├── 07-workflow/              # 워크플로우
│   └── n8n/
├── 08-ai/                    # AI/LLM
│   └── ollama/
├── 09-tooling/               # DevOps/QA/TF
│   └── terrakube/
└── 10-communication/         # Mail
    └── mail/
```

## Context: Hy-Home Infrastructure (infra/) (README.md)

## 🧭 실행 흐름

> **실행 진입점은 저장소 루트의 `docker-compose.yml`입니다.**

```bash
# 저장소 루트에서
cp .env.example .env
docker compose up -d
```

- `.env`와 `secrets/` 값은 루트 기준으로 관리됩니다.
- 특정 서비스만 실행하려면:

```bash
docker compose up -d traefik
```

## Context: Hy-Home Infrastructure (infra/) (README.md)

## 🧩 정리 기준 (분류 원칙)

infra 하위 폴더는 실행 방식에 따라 다음 4가지로 분류합니다.

1. **Core (Include)**: 루트 `docker-compose.yml`에 `include`된 기본 스택.
2. **Optional (Profile)**: `include`는 되어 있으나 `profiles`로 켜는 스택.
3. **Standalone**: 루트 `include`에 없으며 폴더 단위로 별도 실행.
4. **Placeholder**: 문서만 존재하며 실행 정의가 아직 없음.

### 분류 요약

- **Core (Include)**: traefik, mng-db, oauth2-proxy, observability, minio, keycloak, n8n, qdrant, postgresql-cluster, kafka, valkey-cluster, opensearch
- **Optional (Profile)**: airflow, influxdb, couchdb, mail, nginx, ollama, open-webui, sonarqube, vault, terrakube, redis-cluster, ksql
- **Standalone**: supabase
- **Placeholder**: rabbitmq

## Context: Hy-Home Infrastructure (infra/) (README.md)

## 🛠️ 주요 컴포넌트

현재 구성된 인프라는 다음과 같은 서비스들을 포함하고 있습니다.

### 1. Gateway & Security

- **Traefik**: 리버스 프록시 및 대시보드. SSL 종료 및 부하 분산 처리.
- **Keycloak**: 인증 및 인가 (SSO) 관리를 위한 중앙 인증 서버.
- **OAuth2 Proxy**: 인프라 서비스에 대한 통합 인증 계층 가동.
- **Nginx**: 경로 기반 라우팅/캐시가 필요한 경우 사용하는 보조 프록시 (옵션).
- **Vault**: 비밀번호, 토큰 등 민감 정보를 관리하는 보안 저장소 (옵션).

### 2. Databases (Persistence)

- **PostgreSQL Cluster**: Patroni를 사용한 고가용성 PG 클러스터.
- **Managed DB (mng-db)**: 관리용 PostgreSQL + Valkey + RedisInsight.
- **Valkey Cluster**: 고성능 인메모리 데이터 구조 저장소 클러스터.
- **Redis Cluster**: Redis 기반 클러스터 (옵션).
- **InfluxDB**: 시계열 데이터 저장소 (옵션).
- **CouchDB**: 문서형 NoSQL DB (옵션).
- **MinIO**: S3 호환 오브젝트 스토리지.
- **OpenSearch**: 검색/분석 및 대시보드.
- **Qdrant**: 벡터 데이터베이스 (RAG).
- **Supabase**: 자체 호스팅 BaaS 스택 (별도 실행).

### 3. Message Broker

- **Kafka Cluster**: 분산 스트리밍 플랫폼.
  - Kafka UI, Schema Registry, Rest Proxy, Connect, Exporter 포함.
- **ksqlDB**: Kafka 스트림 SQL 엔진.

### 4. Observability Stack

- **Prometheus**: 지표 수집 및 시계열 데이터베이스.
- **Grafana**: 지표 및 로그 시각화 대시보드.
- **Loki & Tempo**: 로그 및 분산 추적 데이터 처리.
- **Alloy**: 에이전트 기반 데이터 수집 도구.
- **Alertmanager**: 알림 정책 및 전송 관리.

### 5. AI & Workflow

- **Ollama**: 로컬 LLM 구동 엔진.
- **Open WebUI**: Ollama 연동 웹 UI (프로파일: `ollama`).
- **Qdrant**: 벡터 데이터베이스 (RAG 구축용).
- **n8n / Airflow**: 워크플로우 자동화 및 데이터 파이프라인 관리.

### 6. Others

- **SonarQube**: 코드 품질 검사 도구 (옵션).
- **Storybook**: 디자인 시스템 템플릿 (`projects/storybook`).
- **Terraform / Terrakube**: IaC 실행 및 오케스트레이션.
- **MailHog**: 개발용 SMTP 테스트 서버 (옵션).
- **RabbitMQ**: 메시지 브로커 (구성 예정).

## Context: Hy-Home Infrastructure (infra/) (README.md)

## 📌 서비스 인덱스

| 서비스             | 프로파일        | 경로                               | 요약                                  |
| ------------------ | --------------- | ---------------------------------- | ------------------------------------- |
| Traefik            | -               | `infra/01-gateway/traefik`         | Edge Router, TLS, 라우팅/미들웨어     |
| Keycloak           | -               | `infra/02-auth/keycloak`           | 중앙 인증/인가 (SSO)                  |
| OAuth2 Proxy       | -               | `infra/02-auth/oauth2-proxy`       | ForwardAuth SSO 게이트                |
| Nginx              | `nginx`         | `infra/01-gateway/nginx`           | 보조 리버스 프록시                    |
| Vault              | `vault`         | `infra/03-security/vault`          | 시크릿/키 관리                        |
| mng-db             | -               | `infra/04-data/mng-db`             | PostgreSQL + Valkey + RedisInsight    |
| PostgreSQL Cluster | -               | `infra/04-data/postgresql-cluster` | Patroni HA + HAProxy                  |
| Valkey Cluster     | -               | `infra/04-data/valkey-cluster`     | 6노드 인메모리 클러스터               |
| Redis Cluster      | `redis-cluster` | `infra/04-data/redis-cluster`      | Redis 클러스터 (옵션)                 |
| InfluxDB           | `influxdb`      | `infra/04-data/influxdb`           | TSDB (옵션)                           |
| CouchDB            | `couchdb`       | `infra/04-data/couchdb`            | 3노드 CouchDB (옵션)                  |
| MinIO              | -               | `infra/04-data/minio`              | S3 오브젝트 스토리지                  |
| OpenSearch         | -               | `infra/04-data/opensearch`         | 검색/대시보드/Exporter                |
| Qdrant             | -               | `infra/04-data/qdrant`             | 벡터 DB                               |
| Kafka              | -               | `infra/05-messaging/kafka`         | KRaft + Confluent 스택                |
| ksqlDB             | `ksql`          | `infra/05-messaging/ksql`          | 스트림 SQL (예제 데이터 포함)         |
| Observability      | -               | `infra/06-observability`           | Prometheus + Grafana + Loki + Tempo   |
| n8n                | -               | `infra/07-workflow/n8n`            | 워크플로우 자동화 (Queue)             |
| Airflow            | `airflow`       | `infra/07-workflow/airflow`        | 워크플로우 오케스트레이션             |
| Ollama             | `ollama`        | `infra/08-ai/ollama`               | 로컬 LLM                              |
| Open WebUI         | `ollama`        | `infra/08-ai/open-webui`           | Ollama Web UI                         |
| SonarQube          | `sonarqube`     | `infra/09-tooling/sonarqube`       | 코드 품질 분석                        |
| Terraform          | -               | `infra/09-tooling/terraform`       | Terraform CLI 컨테이너                |
| Terrakube          | `terrakube`     | `infra/09-tooling/terrakube`       | Terraform 오케스트레이션              |
| Mail               | `mail`          | `infra/10-communication/mail`      | MailHog 테스트 SMTP                   |
| Supabase           | -               | `infra/04-data/supabase`           | 자체 호스팅 Supabase 스택 (별도 실행) |
| RabbitMQ           | -               | `infra/05-messaging/rabbitmq`      | Placeholder (구성 예정)               |

## Context: Hy-Home Infrastructure (infra/) (README.md)

## ⚙️ 설정 가이드

### 서비스 실행

메인 디렉토리에서 아래 명령어를 사용하여 전체 인프라를 구동할 수 있습니다.

```bash
docker compose up -d
```

특정 서비스만 실행하려면 메인에서 서비스를 지정할 수 있습니다.

### 프로파일(Profiles)로 선택 실행

일부 스택은 **프로파일로 비활성화**되어 있으며 필요할 때만 켤 수 있습니다.

```bash
# 예: Airflow와 Ollama만 켜기
docker compose --profile airflow --profile ollama up -d
```

현재 사용 중인 프로파일:

- `airflow` (기본 Airflow 스택)
- `debug` (Airflow 디버그 구성)
- `flower` (Airflow 모니터링 UI)
- `influxdb`
- `couchdb`
- `mail`
- `nginx`
- `ollama`
- `sonarqube`
- `vault`
- `terrakube`
- `redis-cluster`
- `ksql` (KSQL/예제 스택)

## Context: Hy-Home Infrastructure (infra/) (README.md)

## ➕ 서비스 추가 방법

1. `infra/<번호-카테고리>/<서비스명>/` 디렉토리를 생성하고 `docker-compose.yml`을 작성합니다.
2. 필요 시 `profiles`를 지정해 선택 실행 가능한 스택으로 분리합니다.
3. 루트 `docker-compose.yml`의 `include`에 새 서비스를 추가합니다.
4. 환경 변수가 필요하면 루트 `.env.example`에 추가하고, 민감 값은 `secrets/`에 `*.txt`로 분리합니다.
5. 문서 반영: `infra/README.md`에 서비스 요약을 추가하고 `docs/README.md` 및 `docs/ops/README.md`에 관련 내용을 업데이트합니다.

## Context: Hy-Home Infrastructure (infra/) (README.md)

## 📝 참고 사항

- **환경 파일**: `.env.example`와 `.env`는 저장소 루트에서 관리됩니다.
- **볼륨 경로**: 반드시 호스트 컴퓨터의 실제 경로를 `.env` 파일에 지정해야 데이터가 유실되지 않습니다.
- **네트워크**: `infra_net`이라는 브리지 네트워크를 통해 내부 서비스 간 통신이 이루어집니다.
  - `INFRA_SUBNET`, `INFRA_GATEWAY`로 네트워크 대역을 변경할 수 있습니다.

### 운영 헬퍼 스크립트 (PowerShell)

```powershell
# 예: 프로파일 포함 기동
.\scripts\infra-compose.ps1 -Action up -Profiles airflow,ollama

# 로그 확인
.\scripts\infra-compose.ps1 -Action logs -Args "-f" -Services alertmanager

# 특정 서비스만 기동
.\scripts\infra-compose.ps1 -Action up -Profiles observability -Services prometheus,grafana
```

## Context: Observability Stack (LGTM + Alloy) (06-observability)

##

# Observability Stack (LGTM + Alloy)

## Context: Observability Stack (LGTM + Alloy) (06-observability)

## Services

| Service                                    | Image                       | Role                                     | Resources       |
| :----------------------------------------- | :-------------------------- | :--------------------------------------- | :-------------- |
| [`prometheus`](./prometheus/README.md)     | `prom/prometheus:v3.9.0`    | Metrics DB & Alerting Engine             | 1.0 CPU / 1GB   |
| [`loki`](./loki/README.md)                 | `grafana/loki:3.6.3`        | Scalable Log Aggregation                 | 1.0 CPU / 1GB   |
| [`tempo`](./tempo/README.md)               | `grafana/tempo:2.9.0`       | Distributed Tracing Backend              | 1.0 CPU / 1GB   |
| [`grafana`](./grafana/README.md)           | `grafana/grafana:12.3.1`    | Unified Visualization & SSO Portal       | 0.5 CPU / 512MB |
| [`alloy`](./alloy/README.md)               | `grafana/alloy:v1.12.1`     | OTel Collector & Scraper (Unified Agent) | 0.5 CPU / 512MB |
| `cadvisor`                                 | `cadvisor:v0.55.1`          | Real-time Container Resource Analysis    | 0.5 CPU / 512MB |
| [`alertmanager`](./alertmanager/README.md) | `prom/alertmanager:v0.30.0` | Notification Routing & Deduplication     | 0.5 CPU / 256MB |
| [`pushgateway`](./pushgateway/README.md)   | `prom/pushgateway:v1.11.2`  | Short-lived Job Metrics Endpoint         | 0.2 CPU / 128MB |

## Context: Observability Stack (LGTM + Alloy) (06-observability)

## Networking (Static IPs)

Services utilize the `172.19.0.3X` block on `infra_net` for deterministic internal routing.

| Service        | Static IP     | Port    | Traefik Domain                |
| :------------- | :------------ | :------ | :---------------------------- |
| `prometheus`   | `172.19.0.30` | `9090`  | `prometheus.${DEFAULT_URL}`   |
| `loki`         | `172.19.0.31` | `3100`  | -                             |
| `tempo`        | `172.19.0.32` | `3200`  | -                             |
| `grafana`      | `172.19.0.33` | `3000`  | `grafana.${DEFAULT_URL}`      |
| `alloy`        | `172.19.0.34` | `12345` | `alloy.${DEFAULT_URL}`        |
| `alertmanager` | `172.19.0.36` | `9093`  | `alertmanager.${DEFAULT_URL}` |
| `pushgateway`  | `172.19.0.37` | `9091`  | `pushgateway.${DEFAULT_URL}`  |

## Context: Observability Stack (LGTM + Alloy) (06-observability)

## Authentication (Keycloak SSO)

Grafana is integrated with **Keycloak** via Generic OAuth2 for secure, centralized access.

### Role Mapping Logic

Roles are dynamically assigned based on Keycloak groups (`groups` claim):

- **Grafana Admin**: Users in `/admins` group.
- **Grafana Editor**: Users in `/editors` group.
- **Grafana Viewer**: Default for all other authenticated users.

### Config Snippet

```yaml
GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH: "contains(groups[*], '/admins') && 'Admin' || contains(groups[*], '/editors') && 'Editor' || 'Viewer'"
GF_AUTH_GENERIC_OAUTH_STRICT: 'true'
```

## Context: Observability Stack (LGTM + Alloy) (06-observability)

## Alertmanager Integration

Supports multi-channel notifications with deduplication and grouping logic.

| Channel   | Requirement                       | Usage                                     |
| :-------- | :-------------------------------- | :---------------------------------------- |
| **Slack** | `SLACK_ALERTMANAGER_WEBHOOK_URL`  | Critical/Warning alerts to OPS channels   |
| **Email** | `SMTP_USERNAME` / `SMTP_PASSWORD` | Daily summaries and high-priority outages |

## Context: Observability Stack (LGTM + Alloy) (06-observability)

## See Also

- [Grafana Alloy Dashboard Guide](./alloy/README.md)
- [Prometheus Alerting Rules Reference](./prometheus/README.md)

## Context: Observability Stack (LGTM + Alloy) (06-observability)

## File Map

| Path                 | Description                                                 |
| -------------------- | ----------------------------------------------------------- |
| `docker-compose.yml` | LGTM + Alloy stack definition.                              |
| `alertmanager/`      | Alert routing config (`config/config.yml`).                 |
| `alloy/`             | Unified telemetry collector config (`config/config.alloy`). |
| `grafana/`           | Provisioned dashboards and datasources.                     |
| `loki/`              | Loki storage and ingestion config.                          |
| `prometheus/`        | Scrape configs and alert rules.                             |
| `pushgateway/`       | Pushgateway service README.                                 |
| `tempo/`             | Tempo trace storage config.                                 |
| `README.md`          | Stack topology and integration notes.                       |

## Context: Prometheus (prometheus)

##

# Prometheus

Prometheus is an open-source systems monitoring and alerting toolkit. It collects metrics from configured targets at given intervals, evaluates rule expressions, displays the results, and can trigger alerts if some condition is observed to be true.

## Context: Prometheus (prometheus)

## ⚙️ Configuration

The configuration files are located in the `config/` directory.

### Setup

1. **Copy the example configuration:**

   ```bash
   cp prometheus.yml.example prometheus.yml
   cp alert_rules.yml.example alert_rules.yml
   ```

2. **Edit `prometheus.yml`:**
   - Review `scrape_configs` to ensure all target services are correctly defined.
   - If using external services or custom ports, update the `targets`.

3. **Edit `alert_rules.yml`:**
   - Define your recording rules and alerting rules here.

### Scrape Jobs

This configuration includes monitoring for various infrastructure components:

- **Self**: Prometheus, Alertmanager, Cadvisor, Alloy.
- **Databases**: PostgreSQL Cluster, Redis Cluster, MongoDB (Mng), CouchDB.
- **Middleware**: Kafka, Traefik, HAProxy.
- **Applications**: Keycloak, MinIO, N8n, Qdrant, Ollama.

### Kafka Metrics (JMX Exporter)

Kafka broker metrics are scraped from JMX Exporter endpoints on port `9404`.
Grafana Kafka dashboards in this repo filter by `job="kafka"`, so the Prometheus scrape job **must** use:

```yaml
- job_name: 'kafka'
  scrape_interval: 30s
  static_configs:
    - targets: ['kafka-1:9404', 'kafka-2:9404', 'kafka-3:9404']
```

If Kafka dashboards show no data while the brokers are healthy, check Prometheus targets:

```bash
wget -qO- 'http://localhost:9090/api/v1/query?query=up%7Bjob%3D%22kafka%22%7D'
```

Empty results typically mean the Kafka scrape job is named differently (for example, `kafka-broker-jmx`).

## Context: Prometheus (prometheus)

## 🔔 Alerting

- **Alertmanager**: Configured to send alerts to `alertmanager:9093`.
- **Rules**: Loaded from `alert_rules.yml`.

## Context: Prometheus (prometheus)

## 🔗 Integration

- **Grafana**: Uses Prometheus as a primary data source for dashboards.
- **Tempo**: Receives trace-related metrics via remote write (if configured).

## Context: Prometheus (prometheus)

## 🛠 Directory Structure

```text
prometheus/
├── config/
│   ├── alert_rules.yml          # Alerting rules (Ignored by Git)
│   ├── alert_rules.yml.example  # Template rules
│   ├── prometheus.yml           # Main configuration (Ignored by Git)
│   └── prometheus.yml.example   # Template configuration
└── README.md
```

## Context: Grafana (grafana)

##

# Grafana

Grafana is the open-source analytics & monitoring solution for every database. It provides charts, graphs, and alerts for the web when connected to supported data sources.

## Context: Grafana (grafana)

## ⚙️ Configuration

Grafana is configured primarily through **Environment Variables** in `docker-compose.yml` and **Provisioning files**.

### 1. Environment Variables (Authentication)

Authentication (Keycloak OAuth2) is configured via environment variables in `infra/observability/docker-compose.yml`.
Key variables include:

- `GF_AUTH_GENERIC_OAUTH_CLIENT_ID`: OAuth2 Client ID (from `.env`)
- `GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET`: OAuth2 Client Secret (from `.env`)
- `GF_SECURITY_ADMIN_USER` / `PASSWORD`: Initial admin credentials.

### 2. Provisioning

Grafana uses "Provisioning" to automatically configure datasources and dashboards on startup, avoiding manual setup.

- **Datasources**: `provisioning/datasources/datasource.yml`
  - **Prometheus**: Metrics backend.
  - **Loki**: Logs backend.
  - **Tempo**: Traces backend (includes links to Loki for Trace-to-Log correlation).
  - **Alertmanager**: Alert handling.

- **Dashboards**: `provisioning/dashboards/dashboard.yml`
  - Loads JSON dashboards from the `dashboards/` directory.

## Context: Grafana (grafana)

## 📊 Dashboards

Pre-configured dashboards are stored in `dashboards/*.json`:

- **Infrastructure**: Node Exporter, cAdvisor.
- **Databases**: PostgreSQL, Redis, MongoDB.
- **Apps**: Keycloak, MinIO, N8n, Traefik, etc.

## Context: Grafana (grafana)

## 🔗 Integration

- **Traefik**: Exposed via `grafana.${DEFAULT_URL}` (HTTPS).
- **Keycloak**: SSO Login enabled.

## Context: Grafana (grafana)

## 🛠 Directory Structure

```text
grafana/
├── dashboards/                  # JSON files for dashboards
│   ├── *.json
├── provisioning/
│   ├── dashboards/
│   │   └── dashboard.yml        # Config to load dashboards from filesystem
│   └── datasources/
│   │   └── datasource.yml       # Config for Prometheus, Loki, Tempo
└── README.md
```

## Context: Loki (loki)

##

# Loki

Loki is a horizontally scalable, highly available, multi-tenant log aggregation system inspired by Prometheus. It is designed to be very cost-effective and easy to operate. It does not index the contents of the logs, but rather a set of labels for each log stream.

## Context: Loki (loki)

## ⚙️ Configuration

The configuration file is located at `config/loki-config.yaml`.

### Setup

1. **Copy the example configuration:**

   ```bash
   cp loki-config.yaml.example loki-config.yaml
   ```

2. **Edit `loki-config.yaml`:**
   - **Storage (S3/MinIO)**: This setup uses MinIO for object storage.
     - `endpoint`: `http://minio:9000`
     - `access_key_id`: `${MINIO_APP_USERNAME}` (환경변수로 주입)
     - `secret_access_key`: `${MINIO_APP_USER_PASSWORD}` (환경변수로 주입)
     - `-config.expand-env=true` 옵션으로 환경변수 치환이 활성화됩니다.

### Key Features

- **S3 Backend**: Configured to use MinIO for storing chunks and indices.
- **Compactor**: Manages retention and deduplication of logs.
- **Ruler**: Configured to send alerts to Alertmanager (`http://alertmanager:9093`).

## Context: Loki (loki)

## 📦 Storage

Loki requires an Object Store (like AWS S3 or MinIO).

- **Bucket**: `loki-bucket` (must be created in MinIO).
- **Volume**: `loki-data` (Docker volume).

## Context: Loki (loki)

## 🔗 Integration

- **Promtail / Alloy**: Agents push logs to Loki.
- **Grafana**: Queries Loki for log visualization (Data Source: Loki).

## Context: Loki (loki)

## 🛠 Directory Structure

```text
loki/
├── config/
│   ├── loki-config.yaml          # Environment variable 기반 설정
│   └── loki-config.yaml.example  # Template configuration
└── README.md
```

## Context: Grafana Alloy (alloy)

##

# Grafana Alloy

Grafana Alloy is a vendor-neutral OpenTelemetry Collector distribution with a programmable configuration setup. It serves as the central telemetry collector, receiving logs, metrics, and traces, and forwarding them to the respective backends (Loki, Prometheus, Tempo).

## Context: Grafana Alloy (alloy)

## ⚙️ Configuration

The configuration file is located at `config/config.alloy`.

### Setup

1. **Copy the example configuration:**

   ```bash
   cp config.alloy.example config.alloy
   ```

2. **Edit `config.alloy`:**
   - Review the pipelines. The default configuration sets up:
     - **Logging**: Collects Docker logs and pushes to Loki (`http://loki:3100`).
     - **Metrics**: Scrapes itself and pushes to Prometheus (`http://prometheus:9090`).
     - **Tracing**: Receives OTLP traces (gRPC/HTTP) and forwards to Tempo (`tempo:4317`).

### Pipelines

- **Logging Pipeline**:
  - `discovery.docker`: Discovers running containers.
  - `loki.source.docker`: Reads logs from containers.
  - `loki.write`: Sends logs to Loki.
- **Metrics Pipeline**:
  - `prometheus.exporter.self`: Exposes internal Alloy metrics.
  - `prometheus.remote_write`: Sends metrics to Prometheus.
- **Tracing Pipeline**:
  - `otelcol.receiver.otlp`: Listens on ports 4317/4318.
  - `otelcol.processor.batch`: Batches traces for efficiency.
  - `otelcol.exporter.otlp`: Sends traces to Tempo.

## Context: Grafana Alloy (alloy)

## 🔗 Integration

- **Traefik**: Exposed via `alloy.${DEFAULT_URL}` (HTTPS) for debugging pipelines.
- **Backends**: Connects to Loki, Prometheus, and Tempo.

## Context: Grafana Alloy (alloy)

## 🛠 Directory Structure

```text
alloy/
├── config/
│   ├── config.alloy          # Actual configuration (Ignored by Git)
│   ├── config.alloy.example  # Template configuration
└── README.md
```

## Context: Tempo (tempo)

##

# Tempo

Grafana Tempo is an open-source, easy-to-use, and high-scale distributed tracing backend. Tempo is cost-efficient, requiring only object storage (S3/MinIO) to operate, and is deeply integrated with Grafana, Prometheus, and Loki.

## Context: Tempo (tempo)

## ⚙️ Configuration

The configuration file is located at `config/tempo.yaml`.

### Setup

1. **Copy the example configuration:**

   ```bash
   cp tempo.yaml.example tempo.yaml
   ```

2. **Edit `tempo.yaml`:**
   - **Storage (S3/MinIO)**: This setup uses MinIO for trace storage.
     - `endpoint`: `minio:9000`
     - `access_key`: `${MINIO_APP_USERNAME}` (환경변수로 주입)
     - `secret_key`: `${MINIO_APP_USER_PASSWORD}` (환경변수로 주입)
     - `-config.expand-env=true` 옵션으로 환경변수 치환이 활성화됩니다.
   - **Remote Write**:
     - The `metrics_generator` sends metrics to `http://prometheus:9090/api/v1/write`. Ensure Prometheus is reachable.

### Key Features

- **S3 Backend**: Stores traces in MinIO buckets (`tempo-bucket`).
- **Metrics Generator**: Derives metrics (RED method) from spans and sends them to Prometheus (Service Graphs).
- **OTLP Support**: Accepts traces via OpenTelemetry Protocol (gRPC/HTTP).

## Context: Tempo (tempo)

## 📦 Storage

Tempo requires an Object Store.

- **Bucket**: `tempo-bucket` (must be created in MinIO).
- **Volume**: `tempo-data` (Docker volume, mostly for WAL).

## Context: Tempo (tempo)

## 🔗 Integration

- **Applications**: Send traces (spans) to Tempo via OTLP.
- **Grafana**: Visualizes traces. Can correlate with Logs (Loki) and Metrics (Prometheus).

## Context: Tempo (tempo)

## 🛠 Directory Structure

```text
tempo/
├── config/
│   ├── tempo.yaml          # Environment variable 기반 설정
│   └── tempo.yaml.example  # Template configuration
└── README.md
```

## Context: Alertmanager (alertmanager)

##

# Alertmanager

Alertmanager handles alerts sent by client applications such as Prometheus server. It takes care of deduplicating, grouping, and routing them to the correct receiver integration such as email, Slack, PagerDuty, or OpsGenie.

## Context: Alertmanager (alertmanager)

## ⚙️ Configuration

The configuration file is located at `config/config.yml`.

### Setup

1. **Copy the example configuration:**

   ```bash
   cp config.yml.example config.yml
   ```

2. **Edit `config.yml`:**
   - Update email settings (`smtp_auth_username`, `smtp_auth_password`) if you want email notifications.
   - Slack Webhook은 파일에 직접 넣지 않고 `SLACK_ALERTMANAGER_WEBHOOK_URL`로 주입합니다.
   - Ensure the `route.receiver` matches your desired default receiver.

### Key Settings

- **`global`**: Contains SMTP configuration for email alerts.
- **`route`**: Defines how alerts are grouped and routed.
- **`receivers`**: Defines notification channels (Email, Slack, etc.).

## Context: Alertmanager (alertmanager)

## 🔐 Secrets Management

**⚠️ CAUTION:** `config.yml` may contain sensitive information (SMTP passwords).

- **Do not commit `config.yml` to Git.**
- The `.gitignore` should already exclude `config.yml`.
- Slack Webhook은 `SLACK_ALERTMANAGER_WEBHOOK_URL` 환경변수로 주입됩니다.

## Context: Alertmanager (alertmanager)

## 🔗 Integration

- **Prometheus**: Sends fired alerts to Alertmanager.
- **Traefik**: Exposed via `alertmanager.${DEFAULT_URL}` (HTTPS).

## Context: Alertmanager (alertmanager)

## 🛠 Directory Structure

```text
alertmanager/
├── config/
│   ├── config.yml          # Template (SLACK_ALERTMANAGER_WEBHOOK_URL 치환)
│   └── config.yml.example  # Template configuration
└── README.md
```

## Context: Pushgateway (pushgateway)

##

# Pushgateway

The Prometheus Pushgateway exists to allow ephemeral and batch jobs to expose their metrics to Prometheus. Since these jobs may not exist long enough to be scraped, they can push their metrics to the Pushgateway. Prometheus then scrapes the metrics from the Pushgateway.

## Context: Pushgateway (pushgateway)

## ⚙️ Configuration

Pushgateway is a simple binary and usually doesn't require a complex configuration file. It keeps the metrics in memory.

- **Persistence**: In this setup, persistence is **not enabled** by default (no `--persistence.file` flag turned on in `docker-compose.yml`), meaning metrics are lost on restart. This is typical for ephemeral job caching.

## Context: Pushgateway (pushgateway)

## 🔗 Integration

- **Client Apps**: Scripts or batch jobs send `POST` requests to `http://pushgateway:9091/metrics/job/...`.
- **Prometheus**: Scrapes Pushgateway (usually configured as a target in `prometheus.yml`, though specifically not listed in the default jobs unless added).
- **Traefik**: Exposed via `pushgateway.${DEFAULT_URL}` (HTTPS).

## Context: Pushgateway (pushgateway)

## ⚠️ When to use

**Reference**: [Prometheus Documentation - When to use the Pushgateway](https://prometheus.io/docs/practices/pushing/)

- **Do not use** Pushgateway to turn Prometheus into a push-based monitoring system.
- **Use it** for service-level batch jobs that need to report status after completion.

## Context: Pushgateway (pushgateway)

## 🛠 Directory Structure

```text
pushgateway/
└── README.md
```

## Context: Messaging (05-messaging) (05-messaging)

##

# Messaging (05-messaging)

## Context: Messaging (05-messaging) (05-messaging)

## Services

| Service  | Profile    | Path         | Notes                                     |
| -------- | ---------- | ------------ | ----------------------------------------- |
| Kafka    | (core)     | `./kafka`    | KRaft cluster + Schema Registry + Connect |
| ksqlDB   | `ksql`     | `./ksql`     | Stream SQL engine (optional profile)      |
| RabbitMQ | `rabbitmq` | `./rabbitmq` | AMQP 0-9-1 broker + Management UI         |

## Context: Messaging (05-messaging) (05-messaging)

## Notes

- **ksqlDB** depends on Kafka and Schema Registry.
- **RabbitMQ** includes a management interface on port `15672`.

## Context: Messaging (05-messaging) (05-messaging)

## File Map

| Path        | Description                                    |
| ----------- | ---------------------------------------------- |
| `kafka/`    | Kafka cluster and Confluent stack.             |
| `ksql/`     | ksqlDB server/CLI and example datagen.         |
| `rabbitmq/` | RabbitMQ service definition and documentation. |
| `README.md` | Category overview.                             |

## Context: RabbitMQ (05-messaging/rabbitmq) (rabbitmq)

##

# RabbitMQ (05-messaging/rabbitmq)

## Context: RabbitMQ (05-messaging/rabbitmq) (rabbitmq)

## Features

- **Version**: `4.2.3-management-alpine`
- **Management UI**: `15672` 포트를 통해 접근 가능합니다.
- **Static IP**: `172.19.0.21` (on `infra_net`)
- **Healthcheck**: `rabbitmq-diagnostics`를 사용하여 연동 상태를 주기적으로 체크합니다.
- **Resource Limits**: CPU 0.5CORE / Memory 512MB 할당.

## Context: RabbitMQ (05-messaging/rabbitmq) (rabbitmq)

## Configuration (.env)

| Variable                        | Default Value | Description           |
| ------------------------------- | ------------- | --------------------- |
| `RABBITMQ_PORT`                 | `5672`        | AMQP 기본 포트        |
| `RABBITMQ_HOST_PORT`            | `5672`        | 호스트 노출 AMQP 포트 |
| `RABBITMQ_MANAGEMENT_PORT`      | `15672`       | 관리 UI 내부 포트     |
| `RABBITMQ_MANAGEMENT_HOST_PORT` | `15672`       | 관리 UI 호스트 포트   |
| `RABBITMQ_DEFAULT_USER`         | `admin`       | 초기 관리자 계정 명   |
| `RABBITMQ_DEFAULT_PASS`         | `<password>`  | 초기 관리자 비밀번호  |
| `DEFAULT_RABBITMQ_DATA_DIR`     | (Path)        | 데이터 영속화 경로    |

## Context: RabbitMQ (05-messaging/rabbitmq) (rabbitmq)

## File Map

| Path                 | Description                  |
| -------------------- | ---------------------------- |
| `docker-compose.yml` | RabbitMQ 서비스 및 볼륨 정의 |
| `README.md`          | 서비스 설명 및 운영 가이드   |

## Context: RabbitMQ (05-messaging/rabbitmq) (rabbitmq)

## Notes

- 관리 UI 접속 주소: `http://localhost:15672` (또는 로컬 도메인 설정 시 `http://rabbitmq.${DEFAULT_URL}`)
- 초기 로그인 후 보안을 위해 비밀번호를 변경하는 것을 권장합니다.

## Context: Kafka Cluster (KRaft Mode) (kafka)

##

# Kafka Cluster (KRaft Mode)

## Context: Kafka Cluster (KRaft Mode) (kafka)

## Services

| Service            | Image                                   | Role                           | Resources       |
| :----------------- | :-------------------------------------- | :----------------------------- | :-------------- |
| `kafka-{1,2,3}`    | `confluentinc/cp-kafka:8.1.1`           | Combined Broker & Controller   | 1 CPU / 1GB     |
| `schema-registry`  | `confluentinc/cp-schema-registry:8.1.1` | Schema Management (Avro/Proto) | 512MB RAM       |
| `kafka-connect`    | `confluentinc/cp-kafka-connect:8.1.1`   | Distributed Connector Worker   | 1 CPU / 1.5GB   |
| `kafka-rest-proxy` | `confluentinc/cp-kafka-rest:8.1.1`      | HTTP API for Kafka             | 0.5 CPU / 512MB |
| `kafka-ui`         | `provectuslabs/kafka-ui:v0.7.2`         | Web Management Interface       | 0.5 CPU / 512MB |
| `kafka-exporter`   | `danielqsj/kafka-exporter:v1.9.0`       | Prometheus Metrics Exporter    | 0.1 CPU / 128MB |

## Context: Kafka Cluster (KRaft Mode) (kafka)

## Networking

Services run on `infra_net` with static IPs (`172.19.0.2X`).

| Service            | Static IP     | Port (Internal) | Port (Host)                       | Traefik Domain                   |
| :----------------- | :------------ | :-------------- | :-------------------------------- | :------------------------------- |
| `kafka-1`          | `172.19.0.20` | `19092`, `9093` | `${KAFKA_CONTROLLER_1_HOST_PORT}` | -                                |
| `kafka-2`          | `172.19.0.21` | `19092`, `9093` | `${KAFKA_CONTROLLER_2_HOST_PORT}` | -                                |
| `kafka-3`          | `172.19.0.22` | `19092`, `9093` | `${KAFKA_CONTROLLER_3_HOST_PORT}` | -                                |
| `schema-registry`  | `172.19.0.23` | `8081`          | `${SCHEMA_REGISTRY_PORT}`         | `schema-registry.${DEFAULT_URL}` |
| `kafka-connect`    | `172.19.0.24` | `8083`          | -                                 | `kafka-connect.${DEFAULT_URL}`   |
| `kafka-rest-proxy` | `172.19.0.25` | `8082`          | -                                 | `kafka-rest.${DEFAULT_URL}`      |
| `kafka-ui`         | `172.19.0.26` | `8080`          | `${KAFKA_UI_PORT}`                | `kafka-ui.${DEFAULT_URL}`        |
| `kafka-exporter`   | `172.19.0.27` | `9308`          | -                                 | -                                |

## Context: Kafka Cluster (KRaft Mode) (kafka)

## Configuration

### KRaft Environment Variables

| Variable                         | Description       | Value                              |
| :------------------------------- | :---------------- | :--------------------------------- |
| `CLUSTER_ID`                     | Unique Cluster ID | `${KAFKA_CLUSTER_ID}`              |
| `KAFKA_PROCESS_ROLES`            | Server Role       | `broker,controller`                |
| `KAFKA_CONTROLLER_QUORUM_VOTERS` | Voter List        | `1@kafka-1:9093,2@kafka-2:9093...` |
| `KAFKA_HEAP_OPTS`                | JVM Heap          | `-Xms512m -Xmx512m`                |

### Replication Defaults

- **Replication Factor**: `3` (High Availability)
- **Min In-Sync Replicas**: `2` (Data Durability)
- **Log Directions**: `/var/lib/kafka/data`

## Context: Kafka Cluster (KRaft Mode) (kafka)

## Observability (Prometheus + Grafana)

Kafka broker metrics are exposed via **JMX Exporter** on port `9404` (inside `infra_net`).
Prometheus scrapes those endpoints and Grafana dashboards expect the **job label** to be `kafka`.

- **Prometheus targets**: `kafka-1:9404`, `kafka-2:9404`, `kafka-3:9404`
- **Prometheus job name**: `kafka`
- **Grafana**: Kafka dashboards query with `job="kafka"`

If metrics are not visible in Grafana, first confirm the Prometheus job label matches:

```bash
# Inside the Prometheus container
wget -qO- 'http://localhost:9090/api/v1/query?query=up%7Bjob%3D%22kafka%22%7D'
```

If the response is empty but JMX targets are up, the scrape job name is likely mismatched.
Update `infra/06-observability/prometheus/config/prometheus.yml` to use `job_name: "kafka"` and reload Prometheus.

## Context: Kafka Cluster (KRaft Mode) (kafka)

## File Map

| Path                 | Description                                             |
| -------------------- | ------------------------------------------------------- |
| `docker-compose.yml` | KRaft Kafka cluster + Confluent components + exporters. |
| `README.md`          | Architecture, ports, and operations.                    |

## Context: ksqlDB (ksql)

##

# ksqlDB

## Context: ksqlDB (ksql)

## Profile

This stack is **optional** and runs under the `ksql` profile.

```bash
docker compose --profile ksql up -d ksqldb-server
```

## Context: ksqlDB (ksql)

## Services

| Service         | Image                                 | Role                                     | Notes                                |
| --------------- | ------------------------------------- | ---------------------------------------- | ------------------------------------ |
| `ksqldb-server` | `confluentinc/cp-ksqldb-server:8.0.3` | ksqlDB Engine (REST + Stream Processing) | `${KSQLDB_HOST_PORT}:${KSQLDB_PORT}` |
| `ksqldb-cli`    | `confluentinc/cp-ksqldb-cli:8.0.3`    | Interactive CLI Client                   | Internal-only                        |
| `ksql-datagen`  | `confluentinc/ksqldb-examples:8.0.3`  | Example data generator                   | Enabled via `ksql` profile           |

## Context: ksqlDB (ksql)

## Networking

- **Network**: `infra_net`
- **Static IP**: _None assigned_ (Dynamic IP allocation)
- **Traefik**: **Not Configured**. This service is currently **internal only** within the docker network, or accessible via the exposed host port.

## Context: ksqlDB (ksql)

## Configuration

| Variable                 | Description   | Default                                                                                        |
| :----------------------- | :------------ | :--------------------------------------------------------------------------------------------- |
| `KSQL_BOOTSTRAP_SERVERS` | Kafka Brokers | `kafka-1:${KAFKA_INTERNAL_PORT},kafka-2:${KAFKA_INTERNAL_PORT},kafka-3:${KAFKA_INTERNAL_PORT}` |

## Context: ksqlDB (ksql)

## Persistence

- **Data Persistence**: `ksqldb-data-volume` matches `/var/lib/ksql` inside the container.
- **Host Path**: Mapped to `${DEFAULT_DATABASE_DIR}/ksqldb/node1`

## Context: ksqlDB (ksql)

## File Map

| Path                 | Description                                    |
| -------------------- | ---------------------------------------------- |
| `docker-compose.yml` | ksqlDB server + CLI + example datagen profile. |
| `README.md`          | Service overview and usage notes.              |

## Context: Gateway (01-gateway) (01-gateway)

##

# Gateway (01-gateway)

## Context: Gateway (01-gateway) (01-gateway)

## Services

| Service | Profile | Path        | Purpose                                             |
| ------- | ------- | ----------- | --------------------------------------------------- |
| Traefik | (core)  | `./traefik` | Primary reverse proxy, TLS, routing, SSO middleware |
| Nginx   | `nginx` | `./nginx`   | Optional standalone proxy (path-based routing)      |

## Context: Gateway (01-gateway) (01-gateway)

## Notes

- **Traefik and Nginx both use static IP `172.19.0.13`** on `infra_net`. Do not run them together unless you change one of the IPs.
- TLS assets are shared from `secrets/certs`.

## Context: Gateway (01-gateway) (01-gateway)

## File Map

| Path        | Description                        |
| ----------- | ---------------------------------- |
| `traefik/`  | Traefik router and dynamic config. |
| `nginx/`    | Optional standalone Nginx gateway. |
| `README.md` | Category overview.                 |

## Context: Traefik Edge Router (traefik)

##

# Traefik Edge Router

## Context: Traefik Edge Router (traefik)

## Services

| Service   | Image            | Role            | Resources     |
| :-------- | :--------------- | :-------------- | :------------ |
| `traefik` | `traefik:v3.6.6` | Ingress Gateway | 1.0 CPU / 1GB |

## Context: Traefik Edge Router (traefik)

## Networking

Traefik occupies the static IP suffix `.13` on `infra_net` and listens on standard web ports.

| Service   | Static IP     | Ports                                                                  | Host Aliases                       |
| :-------- | :------------ | :--------------------------------------------------------------------- | :--------------------------------- |
| `traefik` | `172.19.0.13` | `80` (HTTP)<br>`443` (HTTPS)<br>`8080` (Dashboard)<br>`8082` (Metrics) | `keycloak.*`, `auth.*`, `whoami.*` |

## Context: Traefik Edge Router (traefik)

## Persistence

| Volume                 | Mount Point                | Description                                                   |
| :--------------------- | :------------------------- | :------------------------------------------------------------ |
| `./config/traefik.yml` | `/etc/traefik/traefik.yml` | **Static Config**: Entrypoints, Providers, Tracing            |
| `./dynamic/`           | `/dynamic/`                | **Dynamic Config**: TLS Stores, Middlewares (BasicAuth, etc.) |
| `secrets/certs/`       | `/certs/`                  | **Certificates**: Custom CA or wildcard certs                 |
| `/var/run/docker.sock` | `/var/run/docker.sock`     | **Docker Socket**: For Service Discovery                      |

## Context: Traefik Edge Router (traefik)

## Configuration

### Static Configuration (`traefik.yml`)

Defines the entrypoints (`web`, `websecure`, `metrics`) and enables the Docker provider.

### Dynamic Configuration (`dynamic/`)

Contains runtime configuration that can be updated without restarting Traefik.

- **Middlewares**: `dashboard-auth` (Basic Auth), `sso-auth` (ForwardAuth to OAuth2 Proxy).
- **TLS options**: default cipher suites, certificate files.

### Dashboard

The Traefik Dashboard is enabled and exposed with Basic Auth protection.

- **URL**: `https://dashboard.${DEFAULT_URL}`
- **Auth Middleware**: `dashboard-auth@file`

## Context: Traefik Edge Router (traefik)

## File Map

| Path                         | Description                                               |
| ---------------------------- | --------------------------------------------------------- |
| `docker-compose.yml`         | Traefik edge router service definition.                   |
| `config/traefik.yml`         | Static config (entrypoints, providers, metrics, tracing). |
| `config/traefik.yml.example` | Template for static config.                               |
| `dynamic/middleware.yml`     | ForwardAuth, basic auth, and rate-limit middlewares.      |
| `dynamic/tls.yaml`           | TLS store and default cert config.                        |
| `dynamic/*.example`          | Template files for dynamic config.                        |
| `secrets/certs/`             | TLS certificates and root CA (shared).                    |
| `README.md`                  | Usage and routing notes.                                  |

## Context: Nginx Standalone Proxy (nginx)

##

# Nginx Standalone Proxy

## Context: Nginx Standalone Proxy (nginx)

## Services

| Service | Image          | Role                               | Resources       |
| :------ | :------------- | :--------------------------------- | :-------------- |
| `nginx` | `nginx:alpine` | Standalone Ingress / Reverse Proxy | 0.5 CPU / 512MB |

## Context: Nginx Standalone Proxy (nginx)

## Networking

This service runs on the `infra_net` network and exposes ports directly to the host to act as a standalone gateway.

| Service | Static IP     | Protocol | Internal Port | Host Port            |
| :------ | :------------ | :------- | :------------ | :------------------- |
| `nginx` | `172.19.0.13` | HTTP     | `80`          | `${HTTP_HOST_PORT}`  |
|         |               | HTTPS    | `443`         | `${HTTPS_HOST_PORT}` |

## Context: Nginx Standalone Proxy (nginx)

## Notes

- Nginx and Traefik both use static IP `172.19.0.13`. Do not run both without changing one of the IPs.

## Context: Nginx Standalone Proxy (nginx)

## Persistence

| Volume                | Mount Point             | Description                                               |
| :-------------------- | :---------------------- | :-------------------------------------------------------- |
| `./config/nginx.conf` | `/etc/nginx/nginx.conf` | **Main Config**: Server blocks, Upstreams, SSL, SSO Logic |
| `secrets/certs/`      | `/etc/nginx/certs`      | **Certificates**: SSL/TLS certs and trusted CAs           |

## Context: Nginx Standalone Proxy (nginx)

## Configuration & SSO Workflow

This Nginx instance is configured to support **Single Sign-On (SSO)** via **OAuth2 Proxy**.

### SSO Flow (Forward Auth)

1. **Request**: Client requests a protected path (e.g., `/app/`).
2. **Auth Check**: Nginx uses the `auth_request` module to send a sub-request to the OAuth2 Proxy (`/_oauth2_auth_check`).
3. **Result**:
   - If `401 Unauthorized`, Nginx redirects the user to `/oauth2/sign_in`.
   - If `200 OK`, Nginx proceeds to proxy the request to the upstream application, passing user information in headers (`X-User`, `X-Email`).

### Routing Path Map

| Path              | Destination         | Description                                      |
| :---------------- | :------------------ | :----------------------------------------------- |
| `/oauth2/`        | `oauth2-proxy:4180` | Authentication endpoints (Login, Callback, etc.) |
| `/keycloak/`      | `keycloak:8080`     | Identity Provider Admin Console                  |
| `/minio/`         | `minio:9000`        | S3-Compatible Storage API                        |
| `/minio-console/` | `minio:9001`        | MinIO Management UI                              |
| `/app/`           | _(Internal App)_    | Protected application path (SSO enforced)        |

## Context: Nginx Standalone Proxy (nginx)

## File Map

| Path                 | Description                                         |
| -------------------- | --------------------------------------------------- |
| `docker-compose.yml` | Standalone Nginx service with host port exposure.   |
| `config/nginx.conf`  | Reverse proxy rules, SSL, OAuth2 auth_request flow. |
| `secrets/certs/`     | TLS certificates for HTTPS termination (shared).    |
| `README.md`          | Usage and routing notes.                            |

## Context: Data (04-data) (04-data)

##

# Data (04-data)

## Context: Data (04-data) (04-data)

## Services

| Service            | Profile         | Path                   | Notes                                     |
| ------------------ | --------------- | ---------------------- | ----------------------------------------- |
| mng-db             | (core)          | `./mng-db`             | Shared PostgreSQL + Valkey + RedisInsight |
| postgresql-cluster | (core)          | `./postgresql-cluster` | Patroni-based HA PostgreSQL               |
| valkey-cluster     | (core)          | `./valkey-cluster`     | 6-node Valkey cluster                     |
| minio              | (core)          | `./minio`              | S3-compatible object storage              |
| opensearch         | (core)          | `./opensearch`         | Search + Dashboards + exporter            |
| qdrant             | (core)          | `./qdrant`             | Vector database (RAG)                     |
| redis-cluster      | `redis-cluster` | `./redis-cluster`      | Optional Redis cluster                    |
| influxdb           | `influxdb`      | `./influxdb`           | Optional time-series DB                   |
| couchdb            | `couchdb`       | `./couchdb`            | Optional CouchDB cluster                  |
| supabase           | (standalone)    | `./supabase`           | Self-hosted Supabase stack                |

## Context: Data (04-data) (04-data)

## Notes

- Secrets and shared settings are managed at the repo root (`.env`, `secrets/`).
- Many services assume the shared Docker network `infra_net`.

## Context: Data (04-data) (04-data)

## File Map

| Path                  | Description                                |
| --------------------- | ------------------------------------------ |
| `mng-db/`             | Shared PostgreSQL + Valkey + RedisInsight. |
| `postgresql-cluster/` | Patroni HA PostgreSQL.                     |
| `valkey-cluster/`     | Valkey cluster.                            |
| `redis-cluster/`      | Optional Redis cluster.                    |
| `minio/`              | S3-compatible storage.                     |
| `opensearch/`         | OpenSearch + Dashboards.                   |
| `qdrant/`             | Vector DB.                                 |
| `influxdb/`           | InfluxDB v2.                               |
| `couchdb/`            | CouchDB cluster.                           |
| `supabase/`           | Standalone Supabase stack.                 |
| `README.md`           | Category overview.                         |

## Context: InfluxDB (influxdb)

##

# InfluxDB

## Context: InfluxDB (influxdb)

## Services

| Service    | Image          | Role                             | Resources     |
| :--------- | :------------- | :------------------------------- | :------------ |
| `influxdb` | `influxdb:2.8` | Time-Series Database / Dashboard | 1.0 CPU / 1GB |

## Context: InfluxDB (influxdb)

## Networking

This service is optional and uses a fixed IP for reliable internal telemetry collection without DNS dependency.

| Service    | Static IP     | Internal Port | Traefik Domain            |
| :--------- | :------------ | :------------ | :------------------------ |
| `influxdb` | `172.19.0.11` | `9999`        | `influxdb.${DEFAULT_URL}` |

## Context: InfluxDB (influxdb)

## Persistence

| Volume          | Mount Point          | Description                                          |
| :-------------- | :------------------- | :--------------------------------------------------- |
| `influxdb-data` | `/var/lib/influxdb2` | Stores TSM data, metadata, and engine configuration. |

## Context: InfluxDB (influxdb)

## Configuration (Auto-Initialization)

The container is configured for automated setup on the first start using `DOCKER_INFLUXDB_INIT_MODE=setup`.

| Variable             | Description          | Initial Value           |
| :------------------- | :------------------- | :---------------------- |
| `INFLUXDB_USERNAME`  | Admin Username       | `${INFLUXDB_USERNAME}`  |
| `INFLUXDB_PASSWORD`  | Admin Password       | `${INFLUXDB_PASSWORD}`  |
| `INFLUXDB_ORG`       | Default Organization | `${INFLUXDB_ORG}`       |
| `INFLUXDB_BUCKET`    | Default Data Bucket  | `${INFLUXDB_BUCKET}`    |
| `INFLUXDB_API_TOKEN` | Initial Admin Token  | `${INFLUXDB_API_TOKEN}` |

## Context: InfluxDB (influxdb)

## File Map

| Path                 | Description                                    |
| -------------------- | ---------------------------------------------- |
| `docker-compose.yml` | InfluxDB v2 service definition with auto-init. |
| `README.md`          | Usage and configuration notes.                 |

## Context: Management Databases Infrastructure (mng-db)

##

# Management Databases Infrastructure

## Context: Management Databases Infrastructure (mng-db)

## Services

| Service               | Image                        | Role                             | Resources       |
| :-------------------- | :--------------------------- | :------------------------------- | :-------------- |
| `mng-valkey`          | `valkey/valkey:9.0.2-alpine` | **Cache & Broker** (Redis Comp.) | 0.5 CPU / 512MB |
| `mng-pg`              | `postgres:17-bookworm`       | **Metadata Database**            | 1 CPU / 1GB     |
| `redisinsight`        | `redis/redisinsight:3.0.1`   | Valkey UI Management             | 0.5 CPU / 512MB |
| `mng-pg-init`         | `postgres:17-alpine`         | DB Initializer                   | 0.5 CPU / 128MB |
| `mng-valkey-exporter` | `oliver006/redis_exporter`   | Prometheus Metrics               | 0.1 CPU / 128MB |
| `mng-pg-exporter`     | `postgres-exporter`          | Prometheus Metrics               | 0.1 CPU / 128MB |

## Context: Management Databases Infrastructure (mng-db)

## Networking

Services run on `infra_net` with static IPs.

| Service        | Static IP     | Port (Internal) | Host Port          | Traefik Domain                |
| :------------- | :------------ | :-------------- | :----------------- | :---------------------------- |
| `mng-valkey`   | `172.19.0.70` | `6379`          | -                  | -                             |
| `mng-pg`       | `172.19.0.72` | `5432`          | `${POSTGRES_PORT}` | -                             |
| `redisinsight` | `172.19.0.68` | `5540`          | -                  | `redisinsight.${DEFAULT_URL}` |

## Context: Management Databases Infrastructure (mng-db)

## Persistence

| Volume              | Mount Point                | Description                |
| :------------------ | :------------------------- | :------------------------- |
| `mng-valkey-data`   | `/data`                    | Valkey AOF/RDB files       |
| `mng-pg-data`       | `/var/lib/postgresql/data` | PostgreSQL Data files      |
| `redisinsight-data` | `/db`                      | RedisInsight user settings |

## Context: Management Databases Infrastructure (mng-db)

## Configuration

### PostgreSQL Initialization

The `mng-pg-init` container runs automatically on startup.

- **Source**: `./init-scripts/init_users_dbs.sql`
- **Action**: Creates databases and users defined in the SQL file.
- **Dependency**: Waits for `mng-pg` to be healthy.

### Secrets and Environment

**Valkey:**

- Password managed via Docker Secret `valkey_password`.
- Configured with `appendonly yes` for durability.

**PostgreSQL:**

- **User**: `${POSTGRES_USER}`
- **Superuser Password**: `${PGPASSWORD_SUPERUSER}`
- **Shared Memory**: `256mb` (Optimized for Docker)

## Context: Management Databases Infrastructure (mng-db)

## Traefik Integration

### RedisInsight

- **URL**: `https://redisinsight.${DEFAULT_URL}`
- **Security**: Protected by **SSO** (`sso-auth` middleware).

## Context: Management Databases Infrastructure (mng-db)

## File Map

| Path                                      | Description                                            |
| ----------------------------------------- | ------------------------------------------------------ |
| `docker-compose.yml`                      | Management Valkey + PostgreSQL (default).              |
| `docker-compose.redis.yml`                | Redis-based alternative stack.                         |
| `init-scripts/init_users_dbs.sql`         | Initial DB/user bootstrap (runs once on empty volume). |
| `init-scripts/init_users_dbs.sql.example` | Template for bootstrap SQL.                            |
| `README.md`                               | Service overview and connection notes.                 |

## Context: Qdrant Vector Database (qdrant)

##

# Qdrant Vector Database

## Context: Qdrant Vector Database (qdrant)

## Services

| Service  | Image                   | Role                 | Resources   |
| :------- | :---------------------- | :------------------- | :---------- |
| `qdrant` | `qdrant/qdrant:v1.16.3` | Vector Search Engine | 1 CPU / 1GB |

## Context: Qdrant Vector Database (qdrant)

## Networking

Service runs on `infra_net` with a static IP.

| Service  | Static IP     | Port (Internal)                | Host Port             | Traefik Domain          |
| :------- | :------------ | :----------------------------- | :-------------------- | :---------------------- |
| `qdrant` | `172.19.0.41` | `6333` (HTTP)<br>`6334` (gRPC) | `${QDRANT_HOST_PORT}` | `qdrant.${DEFAULT_URL}` |

## Context: Qdrant Vector Database (qdrant)

## Persistence

| Volume        | Mount Point       | Description                 |
| :------------ | :---------------- | :-------------------------- |
| `qdrant-data` | `/qdrant/storage` | Vector indices and payloads |

## Context: Qdrant Vector Database (qdrant)

## Configuration

### Environment Variables

| Variable                     | Description | Value   |
| :--------------------------- | :---------- | :------ |
| `QDRANT__TELEMETRY_DISABLED` | Telemetry   | `false` |

## Context: Qdrant Vector Database (qdrant)

## File Map

| Path                 | Description                            |
| -------------------- | -------------------------------------- |
| `docker-compose.yml` | Qdrant single-node service definition. |
| `README.md`          | Usage and integration notes.           |

## Context: Supabase (supabase)

##

# Supabase

## Context: Supabase (supabase)

## 개요

이 디렉토리는 자체 호스팅 Supabase 스택을 실행하기 위한 Docker Compose 구성을 포함합니다. Auth, Realtime, Storage, Studio 대시보드와 같은 모든 핵심 서비스를 포함합니다.

> 이 스택은 현재 루트 `docker-compose.yml`의 `include` 대상이 아니므로 `infra/04-data/supabase`에서 별도로 실행합니다.

## Context: Supabase (supabase)

## 실행 (Standalone)

```bash
cd infra/04-data/supabase
docker compose up -d
```

## Context: Supabase (supabase)

## 서비스

- **studio**: Supabase 대시보드.
- **kong**: API 게이트웨이.
- **auth**: 인증 서비스 (GoTrue).
- **rest**: PostgREST 서비스.
- **realtime**: 리얼타임 서버.
- **storage**: 스토리지 API.
- **imgproxy**: 이미지 변환 서비스.
- **meta**: Postgres 메타 서비스.
- **functions**: 엣지 함수 런타임.
- **analytics**: 분석 서비스 (Logflare).
- **db**: PostgreSQL 데이터베이스 (Supabase용 커스텀).
- **vector**: 벡터 로그 수집기.
- **supavisor**: 연결 풀러.

## Context: Supabase (supabase)

## 필수 조건

- Docker 및 Docker Compose 설치.
- `infra/04-data/supabase/.env` 파일.

## Context: Supabase (supabase)

## 설정

이 서비스는 다음을 포함하여 `.env`에 정의된 다수의 환경 변수를 사용합니다:

- **키**: `ANON_KEY`, `SERVICE_ROLE_KEY`, `JWT_SECRET`.
- **데이터베이스**: `POSTGRES_PASSWORD`, `POSTGRES_DB`.
- **포트**: `KONG_HTTP_PORT`, `KONG_HTTPS_PORT`.

## Context: Supabase (supabase)

## 사용법

서비스 시작:

```bash
docker compose up -d
```

## Context: Supabase (supabase)

## 접속

- **Supabase Studio**: `http://localhost:3000` (기본값, 변경된 경우 `docker-compose.yml` 확인).
- **API Gateway**: `http://localhost:${KONG_HTTP_PORT}`

## Context: Supabase (supabase)

## 볼륨

- 데이터베이스, 스토리지, 설정 데이터의 영구 보존을 위해 다수의 볼륨이 사용됩니다.

## Context: Supabase (supabase)

## File Map

| Path                 | Description                          |
| -------------------- | ------------------------------------ |
| `.env`               | Supabase 스택 전용 환경 변수 파일.   |
| `docker-compose.yml` | Supabase self-hosted 전체 스택 정의. |
| `README.md`          | 서비스 구성 및 사용 안내.            |

## Context: Valkey Cluster (valkey-cluster)

##

# Valkey Cluster

## Context: Valkey Cluster (valkey-cluster)

## Services

| Service               | Image                        | Role                | Resources       |
| :-------------------- | :--------------------------- | :------------------ | :-------------- |
| `valkey-node-{0..5}`  | `valkey/valkey:9.0.2-alpine` | Data Node (Sharded) | 0.5 CPU / 512MB |
| `valkey-cluster-init` | `valkey/valkey:9.0.2-alpine` | Bootstrap Script    | 0.1 CPU / 128MB |
| `valkey-exporter`     | `oliver006/redis_exporter`   | Prometheus Metrics  | 0.1 CPU / 128MB |

## Context: Valkey Cluster (valkey-cluster)

## Networking

Services run on `infra_net` with static IPs (`172.19.0.6X`).

| Service               | Static IP     | Internal Port             | Host Port                      |
| :-------------------- | :------------ | :------------------------ | :----------------------------- |
| `valkey-node-0`       | `172.19.0.60` | `${VALKEY0_PORT}`         | `${VALKEY0_PORT}`              |
| `valkey-node-1`       | `172.19.0.61` | `${VALKEY1_PORT}`         | `${VALKEY1_PORT}`              |
| `valkey-node-2`       | `172.19.0.62` | `${VALKEY2_PORT}`         | `${VALKEY2_PORT}`              |
| `valkey-node-3`       | `172.19.0.63` | `${VALKEY3_PORT}`         | `${VALKEY3_PORT}`              |
| `valkey-node-4`       | `172.19.0.64` | `${VALKEY4_PORT}`         | `${VALKEY4_PORT}`              |
| `valkey-node-5`       | `172.19.0.65` | `${VALKEY5_PORT}`         | `${VALKEY5_PORT}`              |
| `valkey-cluster-init` | `172.19.0.66` | -                         | -                              |
| `valkey-exporter`     | `172.19.0.67` | `${VALKEY_EXPORTER_PORT}` | `${VALKEY_EXPORTER_HOST_PORT}` |

## Context: Valkey Cluster (valkey-cluster)

## Persistence

| Volume                 | Description                             |
| :--------------------- | :-------------------------------------- |
| `valkey-data-{0..5}`   | Persists AOF/RDB data mapped to `/data` |
| `./config/valkey.conf` | Shared configuration file (Bind Mount)  |
| `./scripts/`           | Startup and Init scripts (Bind Mount)   |

## Context: Valkey Cluster (valkey-cluster)

## Configuration

- **Compatibility**: Valkey maintains 100% wire compatibility with Redis 7.2.4+.
- **Sharding**: Auto-provisioned by `valkey-cluster-init.sh` using `valkey-cli --cluster create`.
- **Password**: Managed via Docker Secret `valkey_password`.

## Context: Valkey Cluster (valkey-cluster)

## File Map

| Path                             | Description                                         |
| -------------------------------- | --------------------------------------------------- |
| `docker-compose.yml`             | 6-node Valkey cluster + init + exporter.            |
| `config/valkey.conf`             | Base Valkey cluster config (AOF/RDB, cluster mode). |
| `config/valkey.conf.example`     | Template config for Valkey.                         |
| `scripts/valkey-start.sh`        | Node entrypoint wrapper (announce/cluster ports).   |
| `scripts/valkey-cluster-init.sh` | Cluster creation once nodes are healthy.            |
| `README.md`                      | Architecture and usage notes.                       |

## Context: MinIO Object Storage (minio)

##

# MinIO Object Storage

## Context: MinIO Object Storage (minio)

## Services

| Service                | Image                               | Role        | Resources       |
| :--------------------- | :---------------------------------- | :---------- | :-------------- |
| `minio`                | `minio/minio:RELEASE.2025-09-07...` | S3 Server   | 1 CPU / 1GB     |
| `minio-create-buckets` | `minio/mc:RELEASE.2025-08-13...`    | Init Script | 0.1 CPU / 128MB |

## Context: MinIO Object Storage (minio)

## Networking

Services run on `infra_net` with static IPs.

| Service | Static IP     | API Port                 | Console Port                     | Traefik Domain                                           |
| :------ | :------------ | :----------------------- | :------------------------------- | :------------------------------------------------------- |
| `minio` | `172.19.0.12` | `9000` (`${MINIO_PORT}`) | `9001` (`${MINIO_CONSOLE_PORT}`) | `minio.${DEFAULT_URL}`<br>`minio-console.${DEFAULT_URL}` |

## Context: MinIO Object Storage (minio)

## Persistence

| Volume       | Mount Point | Description         |
| :----------- | :---------- | :------------------ |
| `minio-data` | `/data`     | Object storage data |

## Context: MinIO Object Storage (minio)

## Configuration

### Secrets

Credentials are managed via Docker Secrets for security.

| Secret                    | Description                    |
| :------------------------ | :----------------------------- |
| `minio_root_user`         | Admin Username                 |
| `minio_root_password`     | Admin Password                 |
| `minio_app_user`          | Application User (for buckets) |
| `minio_app_user_password` | Application Password           |

### Environment Variables

| Variable                     | Description     | Value                   |
| :--------------------------- | :-------------- | :---------------------- |
| `MINIO_PROMETHEUS_AUTH_TYPE` | Metrics Auth    | `public` (for scraping) |
| `MINIO_API_ROOT_ACCESS`      | Root API Access | `on`                    |

## Context: MinIO Object Storage (minio)

## Initialization Process

The `minio-create-buckets` container runs on startup to:

1. Wait for MinIO to be healthy.
2. Authenticate as Root.
3. Create `minio_app_user` and assign `readwrite` policy.
4. Create required buckets:
   - `tempo-bucket`
   - `loki-bucket`
   - `cdn-bucket` (Set to Public)

## Context: MinIO Object Storage (minio)

## File Map

| Path                          | Description                                      |
| ----------------------------- | ------------------------------------------------ |
| `docker-compose.yml`          | Single-node MinIO with bucket init sidecar.      |
| `docker-compose.cluster.yaml` | Multi-node (distributed) MinIO cluster template. |
| `README.md`                   | Usage and initialization notes.                  |

## Context: CouchDB Cluster (couchdb)

##

# CouchDB Cluster

## Context: CouchDB Cluster (couchdb)

## Services

| Service                | Image                    | Role                       | Resources       |
| :--------------------- | :----------------------- | :------------------------- | :-------------- |
| `couchdb-1`            | `couchdb:3.5.1`          | Seed & Management Node     | _(Implicit)_    |
| `couchdb-2..3`         | `couchdb:3.5.1`          | Cluster Data Member        | _(Implicit)_    |
| `couchdb-cluster-init` | `curlimages/curl:8.18.0` | Setup Assistant (One-shot) | 0.1 CPU / 128MB |

## Context: CouchDB Cluster (couchdb)

## Networking

All nodes communicate internally via Erlang's distributed protocol on the `infra_net` network.

| Service        | Host Alias            | Database Port     | Cluster Ports (Internal)   |
| :------------- | :-------------------- | :---------------- | :------------------------- |
| `couchdb-1..3` | `couchdb-X.infra_net` | `5984` (HTTP API) | `4369` (EPMD), `9100-9200` |

## Context: CouchDB Cluster (couchdb)

## Initialization Process

The cluster is automatically bootstrapped by the `couchdb-cluster-init` container:

1. **Readiness**: Waits for all 3 nodes to be healthy.
2. **Enable Cluster**: Configures nodes to participate in a cluster.
3. **Join Nodes**: Joins `couchdb-2` and `couchdb-3` to the seed node (`couchdb-1`).
4. **Finalize**: Completes the setup and creates standard system databases (`_users`, `_replicator`, `_global_changes`).

## Context: CouchDB Cluster (couchdb)

## Persistence

Each node maintains its own independent data volume to ensure multi-node redundancy:

- **Mount Point**: `/opt/couchdb/data`
- **Volume Type**: Docker Named Volumes (`couchdbX-data`)

## Context: CouchDB Cluster (couchdb)

## Traefik Integration & Sticky Sessions

CouchDB requires **Sticky Sessions** (Session Affinity) to maintain consistency for certain request sequences when accessed via a load balancer.

- **URL**: `https://couchdb.${DEFAULT_URL}`
- **Router**: `couchdb` (TLS Enabled)
- **Service**: `couchdb-cluster` (Load Balancer)
- **Affinity**: Traefik uses a cookie (`couchdb_sticky`) to ensure a client stays with the same node during their session.

## Context: CouchDB Cluster (couchdb)

## File Map

| Path                 | Description                           |
| -------------------- | ------------------------------------- |
| `docker-compose.yml` | 3-node CouchDB cluster + initializer. |
| `README.md`          | Cluster topology and access notes.    |

## Context: OpenSearch Cluster (opensearch)

##

# OpenSearch Cluster

## Context: OpenSearch Cluster (opensearch)

## Services

| Service                 | Image                                                | Role                           | Status   | Resources       |
| :---------------------- | :--------------------------------------------------- | :----------------------------- | :------- | :-------------- |
| `opensearch-node1`      | `opensearchproject/opensearch:3.4.0`                 | Cluster Manager, Data, Ingest  | Active   | 1 CPU / 1GB     |
| `opensearch-node2`      | `opensearchproject/opensearch:3.4.0`                 | Cluster Manager, Data, Ingest  | Optional | 1 CPU / 1GB     |
| `opensearch-node3`      | `opensearchproject/opensearch:3.4.0`                 | Cluster Manager, Data, Ingest  | Optional | 1 CPU / 1GB     |
| `opensearch-dashboards` | `opensearchproject/opensearch-dashboards:3.4.0`      | Visualization UI (Kibana fork) | Active   | 0.5 CPU / 512MB |
| `opensearch-exporter`   | `prometheuscommunity/elasticsearch-exporter:v1.10.0` | Prometheus Metrics             | Active   | 0.1 CPU / 128MB |

## Context: OpenSearch Cluster (opensearch)

## Networking

All services run on `infra_net` with static IPs in the `172.19.0.4X` range.

| Service                 | Static IP     | Port   | Host Port                  | Traefik Domain                        |
| :---------------------- | :------------ | :----- | :------------------------- | :------------------------------------ |
| `opensearch-node1`      | `172.19.0.44` | `9200` | -                          | `opensearch.${DEFAULT_URL}`           |
| `opensearch-node2`      | `172.19.0.45` | `9200` | -                          | -                                     |
| `opensearch-node3`      | `172.19.0.46` | `9200` | -                          | -                                     |
| `opensearch-dashboards` | `172.19.0.47` | `5601` | `${KIBANA_HOST_PORT}`      | `opensearch-dashboard.${DEFAULT_URL}` |
| `opensearch-exporter`   | `172.19.0.48` | `9114` | `${ES_EXPORTER_HOST_PORT}` | -                                     |

## Context: OpenSearch Cluster (opensearch)

## Persistence

| Volume             | Mount Point                          | Description                              |
| :----------------- | :----------------------------------- | :--------------------------------------- |
| `opensearch-data1` | `/usr/share/opensearch/data`         | Node 1 Data                              |
| `opensearch-data2` | `/usr/share/opensearch/data`         | Node 2 Data (Optional)                   |
| `opensearch-data3` | `/usr/share/opensearch/data`         | Node 3 Data (Optional)                   |
| `secrets/certs/`   | `/usr/share/opensearch/config/certs` | SSL/TLS Certificates (Read-only, shared) |

## Context: OpenSearch Cluster (opensearch)

## Configuration

### Environment Variables

| Variable                  | Description    | Default                    |
| :------------------------ | :------------- | :------------------------- |
| `ELASTIC_PASSWORD`        | Admin Password | Provided via `.env`        |
| `OPENSEARCH_JAVA_OPTS`    | JVM Heap Size  | `-Xms1g -Xmx1g`            |
| `OPENSEARCH_CLUSTER_NAME` | Cluster Name   | `docker-cluster`           |
| `discovery.type`          | Discovery Mode | `single-node` (for 1 node) |

### Performance Tuning

- **Memory Locking**: `bootstrap.memory_lock=true` is enabled to prevent swapping.
- **Ulimits**: `nofile` (65536) and `memlock` (unlimited) are configured.
- **SHM Size**: `1g` shared memory is allocated for Performance Analyzer.

## Context: OpenSearch Cluster (opensearch)

## Custom Build (Plugins)

A `Dockerfile` is provided to build a custom image with plugins pre-installed.

**Included Plugins:**

- `analysis-nori`: Korean morphological analyzer
- `ingest-attachment`: Tika-based document processor
- `mapper-annotated-text`: Indexing annotated text
- `mapper-murmur3`: Murmur3 field mapper
- `mapper-size`: \_size field mapper

**To use custom build:**
Uncomment the `build` section in `docker-compose.yml` and comment out `image`.

## Context: OpenSearch Cluster (opensearch)

## Exporter Metrics (Prometheus)

`opensearch-exporter` collects cluster metrics and requires read-only monitor permissions.
Because the built-in `readall` role is reserved/static, use a dedicated role and mapping:

- Role definition: `infra/opensearch/opensearch/config/opensearch-security/roles.yml` (`exporter_role`)
- Role mapping: `infra/opensearch/opensearch/config/opensearch-security/roles_mapping.yml` (map user `exporter`)

### Apply security changes (REST API)

`securityadmin.sh` may fail if the client certificate does not allow TLS client auth. Use the REST API instead:

```bash
docker exec opensearch bash -lc '
cat <<'"'"'JSON'"'"' >/tmp/exporter_role.json
{
  "cluster_permissions": ["cluster:monitor/*"],
  "index_permissions": [
    {
      "index_patterns": ["*"],
      "allowed_actions": [
        "indices:monitor/*",
        "indices:admin/get",
        "indices:admin/aliases/get",
        "indices:data/read/*"
      ],
      "fls": [],
      "masked_fields": []
    }
  ]
}
JSON

curl -ks -u admin:${OPENSEARCH_ADMIN_PASSWORD} \
  -H "Content-Type: application/json" \
  -XPUT https://localhost:9200/_plugins/_security/api/roles/exporter_role \
  -d @/tmp/exporter_role.json
'

docker exec opensearch bash -lc '
cat <<'"'"'JSON'"'"' >/tmp/exporter_role_mapping.json
{
  "users": ["exporter"]
}
JSON

curl -ks -u admin:${OPENSEARCH_ADMIN_PASSWORD} \
  -H "Content-Type: application/json" \
  -XPUT https://localhost:9200/_plugins/_security/api/rolesmapping/exporter_role \
  -d @/tmp/exporter_role_mapping.json
'
```

### Verify

```bash
docker exec opensearch bash -lc "curl -ks -u exporter:${OPENSEARCH_EXPORTER_PASSWORD} https://localhost:9200/_cluster/health"
curl http://localhost:${ES_EXPORTER_HOST_PORT}/metrics
```

## Context: OpenSearch Cluster (opensearch)

## Security Initialization (Required Once)

If you see:

```text
OpenSearch Security not initialized. (you may need to run securityadmin)
```

initialize the security index with an **admin client certificate**.

### 1. Ensure admin client certs exist

Expected files in `secrets/certs/`:

- `admin-ca.pem`
- `admin-ca-key.pem`
- `admin.pem`
- `admin-key.pem`

If they are missing, generate them:

```bash
openssl req -x509 -newkey rsa:2048 -days 3650 -nodes \
  -subj "/CN=hy-home-admin-ca/O=hy-home" \
  -keyout secrets/certs/admin-ca-key.pem \
  -out secrets/certs/admin-ca.pem

openssl req -newkey rsa:2048 -nodes \
  -subj "/CN=opensearch-admin/O=hy-home" \
  -keyout secrets/certs/admin-key.pem \
  -out /tmp/opensearch-admin.csr

cat > /tmp/opensearch-admin-ext.cnf <<'EOF'
extendedKeyUsage = clientAuth
keyUsage = digitalSignature, keyEncipherment
basicConstraints = CA:FALSE
EOF

openssl x509 -req -in /tmp/opensearch-admin.csr \
  -CA secrets/certs/admin-ca.pem -CAkey secrets/certs/admin-ca-key.pem -CAcreateserial \
  -out secrets/certs/admin.pem -days 3650 -extfile /tmp/opensearch-admin-ext.cnf
```

### 2. Trust admin CA and allow admin DN

Append the admin CA to `secrets/certs/rootCA.pem` and ensure the DN exists:

```yaml
plugins.security.authcz.admin_dn:
  - 'O=hy-home,CN=opensearch-admin'
  - 'CN=opensearch-admin, O=hy-home'
```

Then restart:

```bash
docker compose up -d --force-recreate opensearch
```

### 3. Initialize security index

```bash
docker exec opensearch bash -lc '
/usr/share/opensearch/plugins/opensearch-security/tools/securityadmin.sh \
  -cd /usr/share/opensearch/config/opensearch-security \
  -icl -nhnv -h localhost -p 9200 \
  -cacert /usr/share/opensearch/config/certs/rootCA.pem \
  -cert /usr/share/opensearch/config/certs/admin.pem \
  -key /usr/share/opensearch/config/certs/admin-key.pem
'
```

### 4. Restart Dashboards (if needed)

```bash
docker compose up -d --force-recreate opensearch-dashboards
```

### 5. If admin login fails

Update the admin hash to match `.env`:

```bash
docker exec opensearch bash -lc \
  '/usr/share/opensearch/plugins/opensearch-security/tools/hash.sh -p "${OPENSEARCH_ADMIN_PASSWORD}"'
```

Replace the `admin.hash` in `opensearch/config/opensearch-security/internal_users.yml`, then re-run `securityadmin.sh`.

## Context: OpenSearch Cluster (opensearch)

## File Map

| Path                                                             | Description                                                     |
| ---------------------------------------------------------------- | --------------------------------------------------------------- |
| `docker-compose.yml`                                             | Single-node OpenSearch + Dashboards + exporter.                 |
| `docker-compose.cluster.yml`                                     | 3-node HA cluster definition (optional).                        |
| `Dockerfile`                                                     | Custom OpenSearch build with plugins.                           |
| `opensearch/config/opensearch.yml`                               | Core node config (network, TLS, security plugin).               |
| `opensearch/config/opensearch.yml.example`                       | Template OpenSearch config.                                     |
| `opensearch/config/userdict_ko.txt`                              | Korean user dictionary for `analysis-nori`.                     |
| `opensearch/config/opensearch-security/*.yml`                    | Security plugin config (users/roles/mappings/tenants).          |
| `secrets/certs/`                                                 | Shared TLS certificates (mounted into OpenSearch + Dashboards). |
| `opensearch-dashboards/config/opensearch_dashboards.yml`         | Dashboards config.                                              |
| `opensearch-dashboards/config/opensearch_dashboards.yml.example` | Template Dashboards config.                                     |
| `README.md`                                                      | Cluster usage and security notes.                               |

## Context: PostgreSQL HA Cluster (postgresql-cluster)

##

# PostgreSQL HA Cluster

## Context: PostgreSQL HA Cluster (postgresql-cluster)

## Services

| Service           | Image                     | Role                           | Resources       |
| :---------------- | :------------------------ | :----------------------------- | :-------------- |
| `etcd-{1,2,3}`    | `coreos/etcd:v3.6.7`      | DCS (Distributed Config Store) | 256MB RAM       |
| `pg-{0,1,2}`      | `zalando/spilo-17:4.0-p3` | PostgreSQL 17 + Patroni Agent  | 1 CPU / 2GB     |
| `pg-router`       | `haproxy:3.3.1`           | SQL Traffic Router             | 0.5 CPU / 256MB |
| `pg-cluster-init` | `postgres:17-alpine`      | Schema Initializer (One-off)   | 0.5 CPU / 128MB |
| `pg-*-exporter`   | `postgres-exporter`       | Metrics Sidecar                | 0.1 CPU / 128MB |

## Context: PostgreSQL HA Cluster (postgresql-cluster)

## Networking

Services run on `infra_net` with static IPs (`172.19.0.5X`).

| Service     | Static IP     | Port (Internal)      | Host Port                                                           | Traefik Domain              |
| :---------- | :------------ | :------------------- | :------------------------------------------------------------------ | :-------------------------- |
| `etcd-1`    | `172.19.0.50` | `2379`               | `${ETCD_CLIENT_PORT}`                                               | -                           |
| `etcd-2`    | `172.19.0.51` | `2379`               | `${ETCD_CLIENT_PORT}`                                               | -                           |
| `etcd-3`    | `172.19.0.52` | `2379`               | `${ETCD_CLIENT_PORT}`                                               | -                           |
| `pg-0`      | `172.19.0.53` | `5432`               | `${POSTGRES_PORT}`                                                  | -                           |
| `pg-1`      | `172.19.0.54` | `5432`               | `${POSTGRES_PORT}`                                                  | -                           |
| `pg-2`      | `172.19.0.55` | `5432`               | `${POSTGRES_PORT}`                                                  | -                           |
| `pg-router` | `172.19.0.56` | W: `5432`, R: `5433` | W: `${POSTGRES_WRITE_HOST_PORT}`<br>R: `${POSTGRES_READ_HOST_PORT}` | `pg-haproxy.${DEFAULT_URL}` |

## Context: PostgreSQL HA Cluster (postgresql-cluster)

## Persistence

Data is isolated in named volumes for each node.

| Volume                   | Description                                               |
| :----------------------- | :-------------------------------------------------------- |
| `etcd1-data`, `etcd2...` | Consensus state data                                      |
| `pg0-data`, `pg1...`     | PostgreSQL data files (mapped to `/home/postgres/pgdata`) |
| `haproxy.cfg`            | Configuration bind mount                                  |

## Context: PostgreSQL HA Cluster (postgresql-cluster)

## Configuration

### Patroni & Spilo

The `zalando/spilo` image encapsulates Postgres and Patroni. Key configuration via environment variables:

- `SCOPE`: Cluster name (`pg-ha`). All nodes with the same scope form a cluster.
- `ETCD3_HOSTS`: Connection string for the DCS.
- `PATRONI_NAME`: Unique identifier for the instance.

### Initialization (`pg-cluster-init`)

This container creates users and databases _after_ the cluster is healthy.

- **Wait Logic**: Polls `pg_router` until it accepts connections.
- **Execution**: Runs `./init-scripts/init_users_dbs.sql`.
- **Target**: Connects to the **Cluster/Router**, not an individual node, ensuring metadata is replicated.

## Context: PostgreSQL HA Cluster (postgresql-cluster)

## Traefik Integration

The HAProxy Stats dashboard is exposed via Traefik.

- **URL**: `https://pg-haproxy.${DEFAULT_URL}`
- **Metrics**: Allows verifying which node is currently the Leader.

## Context: PostgreSQL HA Cluster (postgresql-cluster)

## File Map

| Path                                      | Description                                     |
| ----------------------------------------- | ----------------------------------------------- |
| `docker-compose.yml`                      | Patroni + etcd + HAProxy cluster definition.    |
| `.env.postgres`                           | Local env values for cluster bootstrap.         |
| `.env.postgres.example`                   | Template env values.                            |
| `config/haproxy.cfg`                      | HAProxy routing for write/read split and stats. |
| `config/haproxy.cfg.example`              | Template HAProxy config.                        |
| `init-scripts/init_users_dbs.sql`         | Initial DB/user bootstrap (runs once).          |
| `init-scripts/init_users_dbs.sql.example` | Template bootstrap SQL.                         |
| `README.md`                               | HA cluster usage and troubleshooting.           |

## Context: Workflow (07-workflow) (07-workflow)

##

# Workflow (07-workflow)

## Context: Workflow (07-workflow) (07-workflow)

## Services

| Service | Profile   | Path        | Notes                               |
| ------- | --------- | ----------- | ----------------------------------- |
| n8n     | (core)    | `./n8n`     | Workflow automation with queue mode |
| Airflow | `airflow` | `./airflow` | Orchestrator (CeleryExecutor)       |

## Context: Workflow (07-workflow) (07-workflow)

## Notes

- Airflow can also enable `flower` and `debug` profiles for monitoring and debug services.
- Both stacks typically rely on shared DB/queue services from `infra/04-data`.

## Context: Workflow (07-workflow) (07-workflow)

## File Map

| Path        | Description                   |
| ----------- | ----------------------------- |
| `n8n/`      | n8n worker/queue setup.       |
| `airflow/`  | Airflow CeleryExecutor stack. |
| `README.md` | Category overview.            |

## Context: n8n (Workflow Automation) (n8n)

##

# n8n (Workflow Automation)

## Context: n8n (Workflow Automation) (n8n)

## Services

| Service               | Image                        | Role                             | Resources       |
| :-------------------- | :--------------------------- | :------------------------------- | :-------------- |
| `n8n`                 | `n8nio/n8n:2.3.0`            | Main Node (UI, API, Webhooks)    | 1.0 CPU / 2GB   |
| `n8n-worker`          | `n8nio/n8n:2.3.0`            | Worker Node (Workflow Execution) | 1.0 CPU / 2GB   |
| `n8n-valkey`          | `valkey/valkey:9.0.2-alpine` | High-Performance Job Queue       | 0.5 CPU / 256MB |
| `n8n-valkey-exporter` | `oliver006/redis_exporter`   | Prometheus Metrics               | 0.1 CPU / 128MB |

## Context: n8n (Workflow Automation) (n8n)

## Networking

All services are connected to the `infra_net` network with static IPs for consistent metrics collection and internal communication.

| Service               | Static IP     | Internal Port        | Traefik Domain       |
| :-------------------- | :------------ | :------------------- | :------------------- |
| `n8n`                 | `172.19.0.14` | `${N8N_PORT}` (5678) | `n8n.${DEFAULT_URL}` |
| `n8n-worker`          | `172.19.0.17` | -                    | -                    |
| `n8n-valkey`          | `172.19.0.15` | `6379`               | -                    |
| `n8n-valkey-exporter` | `172.19.0.16` | `9121`               | -                    |

## Context: n8n (Workflow Automation) (n8n)

## Persistence

| Volume            | Mount Point              | Description                                                                   |
| :---------------- | :----------------------- | :---------------------------------------------------------------------------- |
| `n8n-data`        | `/home/node/.n8n`        | Stores workflows, credentials, and binary files.                              |
| `n8n-custom`      | `/home/node/.n8n/custom` | (Bind Mount) Local `infra/n8n/custom` directory for developing Private Nodes. |
| `n8n-valkey-data` | `/data`                  | Redis-compatible AOF persistence for the job queue.                           |

## Context: n8n (Workflow Automation) (n8n)

## Configuration

### Queue Mode & Secrets

n8n uses **Valkey** (Redis-compatible) as the message broker for Bull queues. The connection is secured via Docker Secrets.

- **Queue Host**: `n8n-valkey`
- **Secret**: `valkey_password` (mounted at `/run/secrets/valkey_password`)

### Database (PostgreSQL)

A dedicated `n8n` database on the management PostgreSQL instance is used for operational data.

- **Host**: `${POSTGRES_HOSTNAME}`
- **Database**: `n8n`

## Context: n8n (Workflow Automation) (n8n)

## Custom Build (Fonts & Dependencies)

This directory features a custom **Multi-stage Dockerfile** designed to overcome the limitations of the official distroless image.

### Multi-stage Build Workflow

1. **Stage 1 (Builder)**: Uses `alpine:3.21` to install TTF fonts (`font-noto`, `ttf-dejavu`, etc.) and build caches.
2. **Stage 2 (Final)**:
   - Copies pre-compiled fonts from the builder.
   - Installs **Python 3** and build dependencies (`make`, `g++`, etc.) for `Execute Command` nodes.
   - Installs `n8n-cli` globally.
   - Sets up the `custom/` directory for **Private Custom Nodes**.
3. **Result**: A production-ready image with Korean fonts, Python runtime, and custom node support.

### Build and Run

```bash
# Build custom image with fonts
docker compose build n8n

# Start the full stack
docker compose up -d
```

## Context: n8n (Workflow Automation) (n8n)

## File Map

| Path                       | Description                                             |
| -------------------------- | ------------------------------------------------------- |
| `docker-compose.yml`       | n8n + Valkey queue stack (default).                     |
| `docker-compose.redis.yml` | Redis-based alternative stack.                          |
| `Dockerfile`               | Custom n8n image (fonts, Python, n8n-cli).              |
| `custom/`                  | Private/custom nodes (bind-mounted into the container). |
| `README.md`                | Queue-mode architecture and operations.                 |

## Context: Apache Airflow (airflow)

##

# Apache Airflow

## Context: Apache Airflow (airflow)

## Services

| Service                   | Role                           | Resources       | Port                     |
| :------------------------ | :----------------------------- | :-------------- | :----------------------- |
| `airflow-apiserver`       | Web UI & API Server            | 1 CPU / 1GB     | `${AIRFLOW_PORT}` (8080) |
| `airflow-scheduler`       | Schedules tasks to be executed | 1 CPU / 1GB     | -                        |
| `airflow-worker`          | Executes the tasks (Celery)    | 1 CPU / 1GB     | -                        |
| `airflow-triggerer`       | Async execution support        | 1 CPU / 1GB     | -                        |
| `airflow-dag-processor`   | Parses DAG files               | 1 CPU / 1GB     | -                        |
| `flower`                  | Celery monitoring tool         | 1 CPU / 1GB     | `${FLOWER_PORT}` (5555)  |
| `airflow-statsd-exporter` | Metrics for Prometheus         | 0.1 CPU / 128MB | 9102 (HTTP)              |

## Context: Apache Airflow (airflow)

## Networking

All services run on `infra_net` and rely on shared infrastructure.

| Service             | Static IP | Traefik Domain           |
| :------------------ | :-------- | :----------------------- |
| `airflow-apiserver` | Dynamic   | `airflow.${DEFAULT_URL}` |
| `flower`            | Dynamic   | `flower.${DEFAULT_URL}`  |

### External Dependencies

- **PostgreSQL**: Metadata Database (via `postgresql-cluster` or `mng-db`)
- **Redis/Valkey**: Celery Message Broker (via `valkey-cluster` or `mng-valkey`)

## Context: Apache Airflow (airflow)

## Persistence

| Volume                        | Mount Point            | Description                 |
| :---------------------------- | :--------------------- | :-------------------------- |
| `airflow-dags`                | `/opt/airflow/dags`    | DAG definition files        |
| `airflow-plugins`             | `/opt/airflow/plugins` | Custom plugins              |
| `airflow-logs`                | `/opt/airflow/logs`    | Task and scheduler logs     |
| `airflow-config`              | `/opt/airflow/config`  | Airflow configuration files |
| `./config/statsd_mapping.yml` | `/tmp/mappings.yml`    | Metrics mapping config      |

## Context: Apache Airflow (airflow)

## Configuration

### Core Environment Variables

| Variable                                     | Description       | Default                          |
| :------------------------------------------- | :---------------- | :------------------------------- |
| `AIRFLOW__CORE__EXECUTOR`                    | Execution Mode    | `CeleryExecutor`                 |
| `AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION` | Auto-pause DAGs   | `true`                           |
| `AIRFLOW__CORE__LOAD_EXAMPLES`               | Load Example DAGs | `true`                           |
| `AIRFLOW__WEBSERVER__BASE_URL`               | Public URL        | `https://airflow.${DEFAULT_URL}` |
| `AIRFLOW_UID`                                | Process User ID   | `50000`                          |

### Database & Broker

| Variable                              | Description                                                     |
| :------------------------------------ | :-------------------------------------------------------------- |
| `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` | `postgresql+psycopg2://${USER}:${PASS}@${HOST}:${PORT}/airflow` |
| `AIRFLOW__CELERY__BROKER_URL`         | `redis://:${PASS}@${HOST}:${PORT}/0`                            |

### Metrics (StatsD)

Airflow pushes metrics to the local `airflow-statsd-exporter` via UDP, which exposes them for Prometheus.

- `AIRFLOW__METRICS__STATSD_ON`: `true`
- `AIRFLOW__METRICS__STATSD_HOST`: `airflow-statsd-exporter`
- `AIRFLOW__METRICS__STATSD_PORT`: `8125`

## Context: Apache Airflow (airflow)

## File Map

| Path                        | Description                                    |
| --------------------------- | ---------------------------------------------- |
| `docker-compose.yml`        | Airflow CeleryExecutor stack (default broker). |
| `docker-compose.redis.yml`  | Alternate compose with Redis-specific wiring.  |
| `config/statsd_mapping.yml` | StatsD → Prometheus metric mapping rules.      |
| `README.md`                 | Architecture, config, and usage notes.         |

## Context: Security (03-security) (03-security)

##

# Security (03-security)

## Context: Security (03-security) (03-security)

## Services

| Service | Profile | Path      | Purpose                                |
| ------- | ------- | --------- | -------------------------------------- |
| Vault   | `vault` | `./vault` | Secret management, encryption, and PKI |

## Context: Security (03-security) (03-security)

## Notes

- Vault requires **initialization and unseal** before it can be used.
- TLS assets can be mounted from `secrets/certs` for HTTPS.

## Context: Security (03-security) (03-security)

## File Map

| Path        | Description               |
| ----------- | ------------------------- |
| `vault/`    | Vault service and config. |
| `README.md` | Category overview.        |

## Context: HashiCorp Vault Integration Guide (vault)

##

# HashiCorp Vault Integration Guide

## Context: HashiCorp Vault Integration Guide (vault)

## 2. 도입 목적 및 분석 (Objectives & Analysis)

현재 `hy-home.docker`는 Docker Secrets와 `.env` 파일을 사용하여 비밀번호를 관리하고 있습니다. Vault 도입 시 다음과 같은 이점을 얻을 수 있습니다.

### 2.1 주요 이점

1. **Centralized Secret Management**: 분산된 `.env` 파일의 비밀값을 한 곳에서 안전하게 관리.
2. **Dynamic Secrets (동적 시크릿)**:
   - PostgreSQL, MongoDB 등 데이터베이스 접근 시 **일회용 자격 증명(TTL 포함)** 을 발급하여 보안성 극대화.
   - 애플리케이션이 DB 패스워드를 몰라도 됨.
3. **Data Encryption (Transit Engine)**:
   - 민감 개인정보(PII)를 DB에 저장하기 전 Vault를 통해 암호화. (Application-level Encryption)
4. **PKI Management**:
   - 내부 서비스 간 mTLS 통신을 위한 인증서 발급 및 갱신 자동화 (Traefik, Kafka 등과 연동).
5. **Audit Logging**: 누가, 언제, 어떤 비밀값에 접근했는지에 대한 완벽한 감사 로그 제공.

### 2.2 적합성 분석

`hy-home.docker`는 마이크로서비스 아키텍처(MSA)를 지향하고 있으며, Spring Boot, Go, Python 등 다양한 언어 스택을 사용합니다. Vault는 이들 언어에 대한 SDK와 통합 라이브러리(Spring Cloud Vault 등)를 훌륭하게 지원하므로 매우 적합합니다.

---

## Context: HashiCorp Vault Integration Guide (vault)

## 4. 상세 구성 가이드 (Configuration Guide)

### 4.1 Docker Compose 정의

`infra/vault/docker-compose.yml` 참조.
`hashicorp/vault` 최신 이미지를 사용하며, `IPC_LOCK` capability를 추가하여 메모리 스왑을 방지합니다.

### 4.2 초기 설정 프로세스 (Initialization)

Vault는 처음 실행 시 **Sealed** 상태로 시작됩니다. 데이터를 읽고 쓰기 위해서는 **Unseal** 과정이 필요합니다.

1. **Initialize**: 초기화 및 키 생성

   ```bash
   docker compose exec vault vault operator init
   ```

   - **출력된 Unseal Key 5개와 Root Token을 반드시 안전한 곳(`infra/.env` 등)에 저장하세요.**
   - 예시:

     ```text
     Unseal Key 1: UZ59...
     Unseal Key 2: +jR3...
     ...
     Initial Root Token: hvs....
     ```

2. **Unseal**: 봉인 해제 (3개의 키 필요)

   ```bash
   docker compose exec vault vault operator unseal "${VAULT_UNSEAL_KEY_1}"
   docker compose exec vault vault operator unseal "${VAULT_UNSEAL_KEY_2}"
   docker compose exec vault vault operator unseal "${VAULT_UNSEAL_KEY_3}"
   ```

3. **Login**: 루트 로그인

   ```bash
   docker compose exec vault vault login "${VAULT_ROOT_TOKEN}"
   ```

### 4.3 권장 엔진 활성화

1. **KV (Key-Value) v2**: 일반적인 API Key, 설정값 저장.

   ```bash
   vault secrets enable -path=secret kv-v2
   ```

2. **Database**: PostgreSQL/MongoDB 동적 계정 연동.

   ```bash
   vault secrets enable database
   ```

3. **PKI**: 내부 인증서 발급.

   ```bash
   vault secrets enable pki
   ```

---

## Context: HashiCorp Vault Integration Guide (vault)

## 5. 애플리케이션 연동 패턴

### 5.1 Spring Boot (Spring Cloud Vault)

`bootstrap.yml` 또는 `application.yml` 설정을 통해 애플리케이션 시작 시점에 Vault에서 설정을 주입받음.

```yaml
spring:
  cloud:
    vault:
      host: vault
      port: 8200
      scheme: http
      authentication: APPROLE
      app-role:
        role-id: ${VAULT_ROLE_ID}
        secret-id: ${VAULT_SECRET_ID}
```

### 5.2 Go / Python / Node.js

공식 Vault 클라이언트 라이브러리를 사용하여 API 호출.

---

## Context: HashiCorp Vault Integration Guide (vault)

## 6. 운영 및 보안 고려사항

### 6.1 보안 (Security)

- **Production Hardening**: 프로덕션 환경에서는 반드시 **TLS**를 적용해야 합니다. (Traefik이 TLS를 처리하더라도 내부 통신 암호화 권장)
- **Auto Unseal**: 현재 구성은 수동 Unseal 방식입니다. 서버 재시작 시마다 수동으로 Unseal 해야 합니다. 프로덕션 레벨에서는 AWS KMS, GCP KMS 등을 이용한 Auto Unseal 구성을 권장합니다.
  - _Local 개발 환경에서는 스크립트를 통해 자동화할 수 있으나, Unseal Key가 노출되지 않도록 주의해야 합니다._
- **Access Control**: Root Token은 초기 설정 및 비상용으로만 사용하고, 평소에는 정책(Policy)이 적용된 사용자 Token이나 AppRole을 사용하세요.

### 6.2 백업 (Backup)

- Raft Storage의 스냅샷 기능을 이용하여 주기적으로 데이터를 백업해야 합니다.

  ```bash
  vault operator raft snapshot save /vault/file/backup.snap
  ```

---

## Context: HashiCorp Vault Integration Guide (vault)

## 7. Vault CLI & Docker 연동 가이드

### 7.1 Docker 컨테이너 내부 실행 (권장)

```bash
docker compose exec vault vault status
```

주요 명령어:

- `vault status`: 상태 확인 (Sealed 여부 등)
- `vault kv put secret/my-app/config key=value`: 시크릿 저장
- `vault kv get secret/my-app/config`: 시크릿 조회

### 7.2 로컬 호스트(PC)에서 실행

로컬 PC에 Vault CLI가 설치된 경우:

1. 환경 변수 설정 (Windows PowerShell)

   ```powershell
   $env:VAULT_ADDR="http://127.0.0.1:8200"
   ```

2. 명령어 실행

   ```bash
   vault status
   ```

### 7.3 문제 해결 (Troubleshooting)

- **Sealed Status**: 컨테이너 재시작 후 `Vault is sealed` 상태가 됩니다. 4.2절의 Unseal 과정을 다시 수행해야 합니다.
- **Connection Refused**: 포트 8200이 열려있는지, 컨테이너가 정상 실행 중인지 확인하세요.
- **Permission Denied**: 볼륨 마운트 경로(`.config`, `vault-data`)의 권한을 확인하세요.

## Context: HashiCorp Vault Integration Guide (vault)

## 8. File Map

| Path                       | Description                                                |
| -------------------------- | ---------------------------------------------------------- |
| `docker-compose.yml`       | Vault service definition (IPC_LOCK, ports, volumes).       |
| `config/vault.hcl`         | Vault server configuration (storage, listener, telemetry). |
| `config/vault.hcl.example` | Template config.                                           |
| `secrets/certs/`           | TLS materials for Vault (optional, shared).                |
| `README.md`                | Integration and operational guidance.                      |

## Context: Tooling (09-tooling) (09-tooling)

##

# Tooling (09-tooling)

## Context: Tooling (09-tooling) (09-tooling)

## Services

| Service       | Profile      | Path          | Notes                             |
| ------------- | ------------ | ------------- | --------------------------------- |
| Terraform CLI | (standalone) | `./terraform` | Local Terraform runner container  |
| Terrakube     | `terrakube`  | `./terrakube` | Terraform orchestration platform  |
| SonarQube     | `sonarqube`  | `./sonarqube` | Code quality and security scanner |

## Context: Tooling (09-tooling) (09-tooling)

## File Map

| Path         | Description              |
| ------------ | ------------------------ |
| `terraform/` | Terraform CLI container. |
| `terrakube/` | Terrakube stack.         |
| `sonarqube/` | SonarQube service.       |
| `README.md`  | Category overview.       |

## Context: SonarQube (sonarqube)

##

# SonarQube

## Context: SonarQube (sonarqube)

## Services

| Service     | Image                               | Role                | Resources       |
| :---------- | :---------------------------------- | :------------------ | :-------------- |
| `sonarqube` | `sonarqube:26.1.0.118079-community` | Code Quality Server | 0.5 CPU / 512MB |

## Context: SonarQube (sonarqube)

## Networking

Service runs on `infra_net` using **Dynamic** IP assignment (DHCP).

| Service     | IP Address  | Internal Port              | Traefik Domain             |
| :---------- | :---------- | :------------------------- | :------------------------- |
| `sonarqube` | _(Dynamic)_ | `${SONARQUBE_PORT}` (9000) | `sonarqube.${DEFAULT_URL}` |

## Context: SonarQube (sonarqube)

## Persistence

| Volume                  | Mount Point           | Description               |
| :---------------------- | :-------------------- | :------------------------ |
| `sonarqube-data-volume` | `/opt/sonarqube/data` | Plugins, embedded ES data |
| `sonarqube-logs-volume` | `/opt/sonarqube/logs` | Access and error logs     |

## Context: SonarQube (sonarqube)

## Configuration

### Database Connection

SonarQube requires a dedicated PostgreSQL database. In this infrastructure, it connects to the shared Management DB (`infra/mng-db`) or a dedicated instance.

| Variable              | Description       | Value                                                                         |
| :-------------------- | :---------------- | :---------------------------------------------------------------------------- |
| `SONAR_JDBC_URL`      | Connection String | `jdbc:postgresql://${POSTGRES_HOSTNAME}:${POSTGRES_PORT}/${SONARQUBE_DBNAME}` |
| `SONAR_JDBC_USERNAME` | DB User           | `${SONARQUBE_DB_USER}`                                                        |
| `SONAR_JDBC_PASSWORD` | DB Password       | `${SONARQUBE_DB_PASSWORD}`                                                    |

### Kernel Requirements (Important)

SonarQube includes an embedded ElasticSearch instance which requires specific host kernel settings. If the container exits immediately with code 78, ensure:

```bash
# On Host Machine (Linux/WSL2)
sysctl -w vm.max_map_count=262144
```

To make it permanent in `/etc/sysctl.conf`:

```properties
vm.max_map_count=262144
```

## Context: SonarQube (sonarqube)

## File Map

| Path                 | Description                                 |
| -------------------- | ------------------------------------------- |
| `docker-compose.yml` | SonarQube service definition and DB wiring. |
| `README.md`          | Usage and configuration notes.              |

## Context: Terraform Infrastructure as Code (terraform)

##

# Terraform Infrastructure as Code

**Terraform** is an open-source infrastructure as code software tool that provides a consistent CLI workflow to manage hundreds of cloud services.

In the `hy-home.docker` environment, we run Terraform within a Docker container to ensure consistency across different development environments and to avoid polluting the host system.

## Context: Terraform Infrastructure as Code (terraform)

## Getting Started

### Prerequisites

- Docker and Docker Compose installed.
- Access to `infra_net` network (created by the main infrastructure stack).

### Project Structure

```text
/infra/terraform/
├── docker-compose.yml  # Defines the Terraform container
├── README.md           # This documentation
└── workspace/          # Mount point for .tf files and local state
```

## Context: Terraform Infrastructure as Code (terraform)

## State Management

By default, the `terraform.tfstate` file is stored in the local directory (since we mount `./:/workspace`).
**For production-grade setups**, configure a remote backend (like S3, GCS, or Consul) in your `.tf` files to store the state securely and enable collaboration.

## Context: Terraform Infrastructure as Code (terraform)

## Best Practices

- **Modules**: Use modules to organize configurations.
- **Variables**: Do not hardcode secrets. Use `terraform.tfvars` (ensure it's `.gitignore`d) or environment variables.
- **Version Control**: Commit your `.tf` and `.lock.hcl` files. **Do NOT** commit `.tfstate` or `.tfvars` containing secrets.

## Context: Terraform Infrastructure as Code (terraform)

## File Map

| Path                 | Description                                                     |
| -------------------- | --------------------------------------------------------------- |
| `docker-compose.yml` | Runs Terraform CLI in a container with cloud credential mounts. |
| `workspace/`         | Working directory for Terraform configurations and state.       |
| `README.md`          | Usage and workflow guidance.                                    |

## Context: Terrakube (terrakube)

##

# Terrakube

## Context: Terrakube (terrakube)

## Services

| Service              | Image                           | Role                          | Port (Internal)              |
| :------------------- | :------------------------------ | :---------------------------- | :--------------------------- |
| `terrakube-api`      | `azbuilder/api-server:2.29.0`   | Core Logic & State Management | `8080`                       |
| `terrakube-ui`       | `azbuilder/terrakube-ui:2.29.0` | Web Dashboard                 | `${TERRAKUBE_UI_PORT}`       |
| `terrakube-executor` | `azbuilder/executor:2.29.0`     | Runner (Executes Terraform)   | `${TERRAKUBE_EXECUTOR_PORT}` |

## Context: Terrakube (terrakube)

## Networking

All services run on `infra_net` with **Dynamic IPs**.

| Service      | Host Rule                           | Internal Port                |
| :----------- | :---------------------------------- | :--------------------------- |
| **API**      | `terrakube-api.${DEFAULT_URL}`      | `8080`                       |
| **UI**       | `terrakube-ui.${DEFAULT_URL}`       | `${TERRAKUBE_UI_PORT}`       |
| **Executor** | `terrakube-executor.${DEFAULT_URL}` | `${TERRAKUBE_EXECUTOR_PORT}` |

## Context: Terrakube (terrakube)

## Dependencies (External)

Terrakube relies heavily on shared infrastructure services:

- **Database**: `mng-pg` (Shared PostgreSQL in `infra/mng-db`)
- **Cache**: `mng-redis` (Shared Valkey in `infra/mng-db`)
- **Storage**: `minio` (S3 Compatible Storage in `infra/minio`)
- **Identity**: `keycloak` (via Dex protocols)

## Context: Terrakube (terrakube)

## Configuration

### Environment Variables

| Component    | Variable                      | Description                           |
| :----------- | :---------------------------- | :------------------------------------ |
| **Common**   | `InternalSecret`              | Shared secret for inter-service comms |
| **API**      | `ApiDataSourceType`           | `POSTGRESQL`                          |
|              | `StorageType`                 | `AWS` (MinIO S3)                      |
|              | `GroupValidationType`         | `DEX` (Identity Provider)             |
| **UI**       | `REACT_APP_TERRAKUBE_API_URL` | Public Endpoint for API               |
| **Executor** | `ExecutorFlagBatch`           | `false` (Run as daemon)               |

### Executor Privileges

The Executor mounts `/var/run/docker.sock` to spawn ephemeral Terraform runner containers or to manage Docker resources directly.

## Context: Terrakube (terrakube)

## File Map

| Path                 | Description                                    |
| -------------------- | ---------------------------------------------- |
| `docker-compose.yml` | Terrakube API/UI/Executor stack definition.    |
| `secrets/certs/`     | TLS assets (if enabled for internal services). |
| `README.md`          | Usage and dependency notes.                    |

## Context: Auth (02-auth) (02-auth)

##

# Auth (02-auth)

## Context: Auth (02-auth) (02-auth)

## Services

| Service      | Profile | Path             | Purpose                                    |
| ------------ | ------- | ---------------- | ------------------------------------------ |
| Keycloak     | (core)  | `./keycloak`     | IAM provider (SSO, realms, users, clients) |
| OAuth2 Proxy | (core)  | `./oauth2-proxy` | ForwardAuth gateway for protected services |

## Context: Auth (02-auth) (02-auth)

## Dependencies

- **Database**: Keycloak uses PostgreSQL (via `infra/04-data/postgresql-cluster` or `infra/04-data/mng-db`).
- **Gateway**: Traefik routes `keycloak.${DEFAULT_URL}` and `auth.${DEFAULT_URL}`.

## Context: Auth (02-auth) (02-auth)

## File Map

| Path            | Description                                       |
| --------------- | ------------------------------------------------- |
| `keycloak/`     | Keycloak service and optional custom image build. |
| `oauth2-proxy/` | OAuth2 Proxy service and config.                  |
| `README.md`     | Category overview.                                |

## Context: OAuth2 Proxy (SSO) (oauth2-proxy)

##

# OAuth2 Proxy (SSO)

## Context: OAuth2 Proxy (SSO) (oauth2-proxy)

## Services

| Service                        | Image                                       | Role            | Resources       |
| :----------------------------- | :------------------------------------------ | :-------------- | :-------------- |
| `oauth2-proxy`                 | `quay.io/oauth2-proxy/oauth2-proxy:v7.13.0` | Auth Gateway    | 0.5 CPU / 256MB |
| `oauth2-proxy-valkey`          | `valkey/valkey:9.0.2-alpine`                | Session Storage | 0.5 CPU / 256MB |
| `oauth2-proxy-valkey-exporter` | `oliver006/redis_exporter`                  | Metrics         | .1 CPU / 128MB  |

## Context: OAuth2 Proxy (SSO) (oauth2-proxy)

## Networking

Services run on `infra_net` with static IPs.

| Service               | Static IP     | Port (Internal)               | Endpoint              |
| :-------------------- | :------------ | :---------------------------- | :-------------------- |
| `oauth2-proxy`        | `172.19.0.28` | `${OAUTH2_PROXY_PORT}` (4180) | `auth.${DEFAULT_URL}` |
| `oauth2-proxy-valkey` | `172.19.0.18` | `${VALKEY_PORT}`              | -                     |

## Context: OAuth2 Proxy (SSO) (oauth2-proxy)

## Configuration

### Config File (`config/oauth2-proxy.cfg`)

Contains the core logic for OIDC integration. Key settings typically include:

- `provider = "keycloak-oidc"`
- `oidc_issuer_url`: Keycloak realm URL (configured to `https://keycloak.127.0.0.1.nip.io/realms/hy-home.realm`)
- `redirect_url`: `https://auth.127.0.0.1.nip.io/oauth2/callback`
- `scope`: `openid email profile offline_access groups`
- `cookie_domains`: `.127.0.0.1.nip.io`
- `email_domains = "*"`, `whitelist_domains = "*.127.0.0.1.nip.io"`
- `upstreams = [ "static://200" ]` (auth-only response)

### Environment Variables

| Variable                     | Description    | Value                           |
| :--------------------------- | :------------- | :------------------------------ |
| `OAUTH2_PROXY_CLIENT_ID`     | OIDC Client ID | (In .cfg or env)                |
| `OAUTH2_PROXY_CLIENT_SECRET` | OIDC Secret    | `${OAUTH2_PROXY_CLIENT_SECRET}` |
| `OAUTH2_PROXY_COOKIE_SECRET` | Cookie Config  | `${OAUTH2_PROXY_COOKIE_SECRET}` |
| `SSL_CERT_FILE`              | Trusted CA     | `/etc/ssl/certs/rootCA.pem`     |

### SSL/TLS

The proxy mounts `secrets/certs/rootCA.pem` to trust internal HTTPS connections (e.g., to Keycloak) if self-signed certificates are used in development.

## Context: OAuth2 Proxy (SSO) (oauth2-proxy)

## File Map

| Path                              | Description                                                   |
| --------------------------------- | ------------------------------------------------------------- |
| `docker-compose.yml`              | OAuth2 Proxy + Valkey session store (default).                |
| `docker-compose.redis.yml`        | OAuth2 Proxy + Redis session store (alternative).             |
| `config/oauth2-proxy.cfg`         | Active Keycloak OIDC configuration (issuer, cookies, scopes). |
| `config/oauth2-proxy.cfg.example` | Template config.                                              |
| `secrets/certs/`                  | Shared CA and TLS materials for IdP trust.                    |
| `README.md`                       | SSO wiring and usage notes.                                   |

## Context: Keycloak IAM (keycloak)

##

# Keycloak IAM

## Context: Keycloak IAM (keycloak)

## Services

| Service    | Image                              | Role         | Resources   | Port       |
| :--------- | :--------------------------------- | :----------- | :---------- | :--------- |
| `keycloak` | `quay.io/keycloak/keycloak:26.5.0` | IAM Provider | 1 CPU / 1GB | 8080 (Int) |

## Context: Keycloak IAM (keycloak)

## Networking

Services run on `infra_net` with static IPs.

| Service    | Static IP     | Endpoint                  | Host Port                     |
| :--------- | :------------ | :------------------------ | :---------------------------- |
| `keycloak` | `172.19.0.29` | `keycloak.${DEFAULT_URL}` | `${KEYCLOAK_MANAGEMENT_PORT}` |

## Context: Keycloak IAM (keycloak)

## Persistence

Data is stored in the external **PostgreSQL** database (typically `postgres-cluster` or `management-db`). Keycloak itself is stateless except for the database connection.

- **Database**: `jdbc:postgresql://${POSTGRES_HOSTNAME}:${POSTGRES_PORT}/${KEYCLOAK_DBNAME}`

## Context: Keycloak IAM (keycloak)

## Configuration

### Core Environment Variables

| Variable           | Description     | Value                             |
| :----------------- | :-------------- | :-------------------------------- |
| `KC_DB`            | Database Vendor | `postgres`                        |
| `KEYCLOAK_ADMIN`   | Admin Username  | `${KEYCLOAK_ADMIN_USER}`          |
| `KC_HOSTNAME`      | Public URL      | `https://keycloak.${DEFAULT_URL}` |
| `KC_PROXY_HEADERS` | Proxy Mode      | `xforwarded` (Trusts Traefik)     |

### Performance & Usage

- **Metrics**: `KC_METRICS_ENABLED=true` (Scraped by Prometheus)
- **Health**: `KC_HEALTH_ENABLED=true`
- **Connection Pool**: Min 1, Max 10 connections to DB.
- **JVM Options**: Configured for aggressive idle connection removal (`-Dquarkus.datasource.jdbc.idle-removal-interval=5M`).

## Context: Keycloak IAM (keycloak)

## Custom Build

This directory contains a `Dockerfile` for building a custom Keycloak image. This is required for:

1. **Pre-installing Providers**: Adding custom SPI JARs to `/opt/keycloak/providers/`.
2. **Custom Themes**: Adding branding to `/opt/keycloak/themes/`.
3. **Database Drivers**: If switching from Postgres (though not recommended here).

**To use custom build:**

1. Uncomment `build: .` in `docker-compose.yml`.
2. Comment out `image: ...`.
3. Run `docker compose build keycloak`.

## Context: Keycloak IAM (keycloak)

## Traefik Integration

Services are exposed via Traefik with TLS enabled.

- **Rule**: `Host(keycloak.${DEFAULT_URL})`
- **Entrypoint**: `websecure`
- **TLS**: Enabled

## Context: Keycloak IAM (keycloak)

## Advanced Configuration Guides

### 1. Group Membership Mapping

To map Keycloak groups to OIDC token claims (useful for RBAC):

1. **Client Scopes** > Create `groups` scope.
2. **Mappers** > Add `Group Membership` mapper.
   - Token Claim Name: `groups`
3. **Clients** > Your App > Client Scopes > Add `groups` as Default.

### 2. Social Login (Identity Providers)

#### Google

1. Create OAuth2 Client in GCP Console.
2. In Keycloak: **Identity Providers** > **Google**.
3. Paste Client ID/Secret.

#### Naver (OIDC)

- **Auth URL**: `https://nid.naver.com/oauth2.0/authorize`
- **Token URL**: `https://nid.naver.com/oauth2.0/token`
- **User Info**: `https://openapi.naver.com/v1/nid/me`

#### Kakao (OIDC)

- **Auth URL**: `https://kauth.kakao.com/oauth/authorize`
- **Token URL**: `https://kauth.kakao.com/oauth/token`
- **User Info**: `https://kapi.kakao.com/v2/user/me`

### Redirect URI

```text
http://keycloak.${DEFAULT_URL}/auth/realms/hy-home.realm/protocol/openid-connect/auth
https://vault.${DEFAULT_URL}/ui/vault/auth/oidc/oidc/callback
https://vault.${DEFAULT_URL}/oidc/callback
https://grafana.${DEFAULT_URL}/login/generic_oauth
https://auth.${DEFAULT_URL}/oauth2/callback
https://grafana.${DEFAULT_URL}/login
```

### Valid post logout redirect URIs

```text
https://keycloak.${DEFAULT_URL}/realms/hy-home.realm/protocol/openid-connect/logout?post_logout_redirect_uri=https://grafana.${DEFAULT_URL}/login
https://grafana.${DEFAULT_URL}/login
```

## Context: Keycloak IAM (keycloak)

## File Map

| Path                 | Description                                                 |
| -------------------- | ----------------------------------------------------------- |
| `docker-compose.yml` | Keycloak service definition and env wiring.                 |
| `Dockerfile`         | Optional custom Keycloak build (health/metrics, providers). |
| `README.md`          | IAM setup and integration notes.                            |

## Context: Communication (10-communication) (10-communication)

##

# Communication (10-communication)

## Context: Communication (10-communication) (10-communication)

## Services

| Service | Profile | Path     | Notes                     |
| ------- | ------- | -------- | ------------------------- |
| MailHog | `mail`  | `./mail` | SMTP test server + web UI |

## Context: Communication (10-communication) (10-communication)

## File Map

| Path        | Description                                  |
| ----------- | -------------------------------------------- |
| `mail/`     | MailHog stack and commented Stalwart config. |
| `README.md` | Category overview.                           |

## Context: Mail Server Infrastructure (mail)

##

# Mail Server Infrastructure

## Context: Mail Server Infrastructure (mail)

## Profile

This stack is **optional** and runs under the `mail` profile.

```bash
docker compose --profile mail up -d mailhog
```

## Context: Mail Server Infrastructure (mail)

## Services

### Active: MailHog

- **Service Name**: `mailhog`
- **Image**: `mailhog/mailhog:v1.0.1`
- **Role**: Email testing tool for developers
- **Internal SMTP Port**: `1025`
- **Web UI Port**: `${MAILHOG_UI_PORT}`

### Inactive: Stalwart

> **Note**: A fully commented-out configuration for **Stalwart Mail Server** exists in `docker-compose.yml` for future production use.

- **Role**: All-in-one Mail Server (SMTP, IMAP, JMAP)
- **Features**: Protocols (SMTP, SMTPS, IMAPS), ManageSieve, Web Admin UI.
- **Persistence**: Uses `stalwart-data` volume and `secrets/certs/` directory.

## Context: Mail Server Infrastructure (mail)

## Networking

- **Network**: `infra_net`
- **MailHog Internal Host**: `mailhog`
- **MailHog Internal Port**: `1025` (No auth required)

## Context: Mail Server Infrastructure (mail)

## Configuration

### MailHog

MailHog is configured primarily via command flags and does not require complex environment variables for this setup.

### Stalwart (Inactive)

Check `docker-compose.yml` comments for:

- `STALWART_ADMIN_USER`
- `STALWART_ADMIN_PASSWORD`

## Context: Mail Server Infrastructure (mail)

## Traefik Integration

The Web UI for MailHog is exposed with security enabled:

- **Domain**: `mail.${DEFAULT_URL}`
- **Entrypoint**: `websecure` (TLS Enabled)
- **Service Port**: `${MAILHOG_UI_PORT}`
- **Authentication**: **SSO Enabled** (via `sso-auth` middleware)

## Context: Mail Server Infrastructure (mail)

## File Map

| Path                 | Description                                                      |
| -------------------- | ---------------------------------------------------------------- |
| `docker-compose.yml` | MailHog active stack + commented Stalwart Mail Server blueprint. |
| `secrets/certs/`     | TLS materials for Stalwart (cert.pem, key.pem, rootCA.pem).      |
| `README.md`          | Service overview and usage notes.                                |

## Context: AI (08-ai) (08-ai)

##

# AI (08-ai)

## Context: AI (08-ai) (08-ai)

## Services

| Service    | Profile  | Path           | Notes                       |
| ---------- | -------- | -------------- | --------------------------- |
| Ollama     | `ollama` | `./ollama`     | LLM inference server        |
| Open WebUI | `ollama` | `./open-webui` | Chat UI + RAG orchestration |

## Context: AI (08-ai) (08-ai)

## Notes

- Open WebUI expects Qdrant (`infra/04-data/qdrant`) for vector storage.
- GPU usage requires NVIDIA container tooling on the host.

## Context: AI (08-ai) (08-ai)

## File Map

| Path          | Description                  |
| ------------- | ---------------------------- |
| `ollama/`     | Ollama inference + exporter. |
| `open-webui/` | Open WebUI service.          |
| `README.md`   | Category overview.           |

## Context: Ollama & Open WebUI (open-webui)

##

# Ollama & Open WebUI

## Context: Ollama & Open WebUI (open-webui)

## Services

| Service           | Image                                 | Role                       | Resources               |
| :---------------- | :------------------------------------ | :------------------------- | :---------------------- |
| `ollama`          | `ollama/ollama:0.13.5`                | LLM Inference Server       | 4 CPU / 8GB RAM / 1 GPU |
| `open-webui`      | `ghcr.io/open-webui/open-webui:main`  | Chat UI & RAG Orchestrator | 1 CPU / 1GB RAM         |
| `ollama-exporter` | `lucabecker42/ollama-exporter:latest` | Metrics Exporter           | 0.1 CPU / 128MB         |

## Context: Ollama & Open WebUI (open-webui)

## Networking

Services run on `infra_net` with static IPs.

| Service           | Static IP     | Port (Internal) | Host Port                      | Traefik Domain          |
| :---------------- | :------------ | :-------------- | :----------------------------- | :---------------------- |
| `ollama`          | `172.19.0.40` | `11434`         | `${OLLAMA_PORT}`               | `ollama.${DEFAULT_URL}` |
| `open-webui`      | `172.19.0.42` | `8080`          | -                              | `chat.${DEFAULT_URL}`   |
| `ollama-exporter` | `172.19.0.43` | `11434` (Mock)  | `${OLLAMA_EXPORTER_HOST_PORT}` | -                       |

## Context: Ollama & Open WebUI (open-webui)

## Persistence

| Volume         | Mount Point         | Description                                  |
| :------------- | :------------------ | :------------------------------------------- |
| `ollama-data`  | `/root/.ollama`     | Stores downloaded model globs.               |
| `ollama-webui` | `/app/backend/data` | Chat history, login data, uploaded RAG docs. |

## Context: Ollama & Open WebUI (open-webui)

## Configuration

### Hardware Requirements

- **GPU**: NVIDIA GPU with `nvidia-container-toolkit` installed on host.
- **CPU**: AVX2 support required if running CPU-only mode.
- **RAM**: At least 8GB dedicated to Docker recommended for 7B models.

### Environment Variables

| Variable                 | Service | Description           | Value                          |
| :----------------------- | :------ | :-------------------- | :----------------------------- |
| `OLLAMA_HOST`            | Ollama  | Listen address        | `0.0.0.0:${OLLAMA_PORT}`       |
| `NVIDIA_VISIBLE_DEVICES` | Ollama  | GPU Isolation         | `all`                          |
| `OLLAMA_BASE_URL`        | WebUI   | Connection to backend | `http://ollama:${OLLAMA_PORT}` |
| `VECTOR_DB_URL`          | WebUI   | Connection to Qdrant  | `http://qdrant:${QDRANT_PORT}` |
| `RAG_EMBEDDING_ENGINE`   | WebUI   | Embedding Provider    | `ollama`                       |

## Context: Ollama & Open WebUI (open-webui)

## RAG Workflow (Retrieval Augmented Generation)

1. **Ingestion**: User uploads a PDF/TXT to Open WebUI.
2. **Embedding**: WebUI sends text chunks to Ollama (`qwen3-embedding`) to convert text to vectors.
3. **Storage**: Vectors are stored in Qdrant (`172.19.0.41`).
4. **Retrieval**: When User asks a question, WebUI searches Qdrant for relevant context.
5. **Generation**: context + question is sent to Ollama (`llama3`) to generate the answer.

## Context: Ollama & Open WebUI (open-webui)

## File Map

| Path                 | Description                           |
| -------------------- | ------------------------------------- |
| `docker-compose.yml` | Ollama + Open WebUI + exporter stack. |
| `README.md`          | Model/RAG usage and GPU notes.        |

## Context: Ollama & Open WebUI (ollama)

##

# Ollama & Open WebUI

## Context: Ollama & Open WebUI (ollama)

## Services

| Service           | Image                                 | Role                       | Resources               |
| :---------------- | :------------------------------------ | :------------------------- | :---------------------- |
| `ollama`          | `ollama/ollama:0.13.5`                | LLM Inference Server       | 4 CPU / 8GB RAM / 1 GPU |
| `open-webui`      | `ghcr.io/open-webui/open-webui:main`  | Chat UI & RAG Orchestrator | 1 CPU / 1GB RAM         |
| `ollama-exporter` | `lucabecker42/ollama-exporter:latest` | Metrics Exporter           | 0.1 CPU / 128MB         |

## Context: Ollama & Open WebUI (ollama)

## Networking

Services run on `infra_net` with static IPs.

| Service           | Static IP     | Port (Internal) | Host Port                      | Traefik Domain          |
| :---------------- | :------------ | :-------------- | :----------------------------- | :---------------------- |
| `ollama`          | `172.19.0.40` | `11434`         | `${OLLAMA_PORT}`               | `ollama.${DEFAULT_URL}` |
| `open-webui`      | `172.19.0.42` | `8080`          | -                              | `chat.${DEFAULT_URL}`   |
| `ollama-exporter` | `172.19.0.43` | `11434` (Mock)  | `${OLLAMA_EXPORTER_HOST_PORT}` | -                       |

## Context: Ollama & Open WebUI (ollama)

## Persistence

| Volume         | Mount Point         | Description                                  |
| :------------- | :------------------ | :------------------------------------------- |
| `ollama-data`  | `/root/.ollama`     | Stores downloaded model globs.               |
| `ollama-webui` | `/app/backend/data` | Chat history, login data, uploaded RAG docs. |

## Context: Ollama & Open WebUI (ollama)

## Configuration

### Hardware Requirements

- **GPU**: NVIDIA GPU with `nvidia-container-toolkit` installed on host.
- **CPU**: AVX2 support required if running CPU-only mode.
- **RAM**: At least 8GB dedicated to Docker recommended for 7B models.

### Environment Variables

| Variable                 | Service | Description           | Value                          |
| :----------------------- | :------ | :-------------------- | :----------------------------- |
| `OLLAMA_HOST`            | Ollama  | Listen address        | `0.0.0.0:${OLLAMA_PORT}`       |
| `NVIDIA_VISIBLE_DEVICES` | Ollama  | GPU Isolation         | `all`                          |
| `OLLAMA_BASE_URL`        | WebUI   | Connection to backend | `http://ollama:${OLLAMA_PORT}` |
| `VECTOR_DB_URL`          | WebUI   | Connection to Qdrant  | `http://qdrant:${QDRANT_PORT}` |
| `RAG_EMBEDDING_ENGINE`   | WebUI   | Embedding Provider    | `ollama`                       |

## Context: Ollama & Open WebUI (ollama)

## RAG Workflow (Retrieval Augmented Generation)

1. **Ingestion**: User uploads a PDF/TXT to Open WebUI.
2. **Embedding**: WebUI sends text chunks to Ollama (`qwen3-embedding`) to convert text to vectors.
3. **Storage**: Vectors are stored in Qdrant (`172.19.0.41`).
4. **Retrieval**: When User asks a question, WebUI searches Qdrant for relevant context.
5. **Generation**: context + question is sent to Ollama (`llama3`) to generate the answer.

## Context: Ollama & Open WebUI (ollama)

## File Map

| Path                 | Description                           |
| -------------------- | ------------------------------------- |
| `docker-compose.yml` | Ollama + Open WebUI + exporter stack. |
| `README.md`          | Model/RAG usage and GPU notes.        |
