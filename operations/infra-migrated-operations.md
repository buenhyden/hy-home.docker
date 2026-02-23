# Migrated Infra Routine Operations

<!-- MIGRATED CONTENT BELOW -->

## Context: Messaging (05-messaging) (05-messaging)

## Run

```bash
# Core streaming (Kafka)
docker compose up -d kafka

# Stream SQL (optional)
docker compose --profile ksql up -d ksqldb-server

# Message Broker (optional)
docker compose --profile rabbitmq up -d rabbitmq
```

## Context: RabbitMQ (05-messaging/rabbitmq) (rabbitmq)

## Run

이 서비스는 `rabbitmq` 프로파일로 관리됩니다.

```bash
# 서비스 실행
docker compose --profile rabbitmq up -d

# 서비스 중지
docker compose --profile rabbitmq stop
```

## Context: Kafka Cluster (KRaft Mode) (kafka)

## Usage

### 1. Accessing Kafka UI

- **URL**: `https://kafka-ui.${DEFAULT_URL}`
- **Login**: Protected by SSO. Provides full cluster management (Topics, Connectors, Schemas).

### 2. CLI Operations

Create a topic:

```bash
docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 \
  --create --topic my-topic --partitions 3 --replication-factor 3
```

List topics:

```bash
docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --list
```

Consume messages:

```bash
docker exec kafka-1 kafka-console-consumer --bootstrap-server localhost:19092 \
  --topic my-topic --from-beginning
```

### 3. Kafka Connect

Check installed plugins:

```bash
curl http://localhost:8083/connector-plugins | jq
```

Deploy a connector (Example):

```bash
curl -X POST -H "Content-Type: application/json" --data @my-connector.json \
  http://localhost:8083/connectors
```

## Context: ksqlDB (ksql)

## Usage

### Accessing via CLI (Internal)

`ksqldb-cli` 서비스를 통해 접속할 수 있습니다:

```bash
docker exec -it ksqldb-cli ksql http://ksqldb-server:${KSQLDB_PORT}
```

### Checking Logs

```bash
docker logs ksqldb-server
```

## Context: Gateway (01-gateway) (01-gateway)

## Run

```bash
# Core gateway
docker compose up -d traefik

# Optional standalone gateway
docker compose --profile nginx up -d nginx
```

## Context: Traefik Edge Router (traefik)

## Usage

### 1. Adding a New Service

To expose a Docker container via Traefik, add labels to its `docker-compose.yml`:

```yaml
labels:
  - 'traefik.enable=true'
  - 'traefik.http.routers.my-service.rule=Host(`service.${DEFAULT_URL}`)'
  - 'traefik.http.routers.my-service.entrypoints=websecure'
  - 'traefik.http.routers.my-service.tls=true'
  - 'traefik.http.services.my-service.loadbalancer.server.port=3000'
```

### 2. Enabling SSO

To protect a service with Keycloak SSO (via OAuth2 Proxy), add the middleware:

```yaml
- 'traefik.http.routers.my-service.middlewares=sso-auth@file'
```

## Context: Nginx Standalone Proxy (nginx)

## Usage

### 1. Direct Access

Access services via the host machine's IP or DNS mapping using path-based URLs:

- `https://localhost:${HTTPS_HOST_PORT}/keycloak/`
- `https://localhost:${HTTPS_HOST_PORT}/minio-console/`

### 2. Monitoring Logs

```bash
# Monitor access/error logs
docker logs -f nginx
```

## Context: Data (04-data) (04-data)

## Run

```bash
# Core data services (example subset)
docker compose up -d mng-db postgresql-cluster minio qdrant

# Optional stacks
docker compose --profile redis-cluster up -d
docker compose --profile influxdb up -d
docker compose --profile couchdb up -d

# Standalone (not included at root)
cd infra/04-data/supabase
docker compose up -d
```

## Context: InfluxDB (influxdb)

## Usage

### 1. Web UI Dashboard

Access the integrated dashboard at `https://influxdb.${DEFAULT_URL}`.

- Visualize data using Data Explorer (InfluxQL / Flux).
- Manage Buckets, Tokens, and Scrapers.
- Build and share multi-dimensional dashboards.

### 2. Client Connection (Python/Telegraf)

Use the **Internal Address** `http://influxdb:9999` or the **Static IP** `http://172.19.0.11:9999` with the following credentials:

- **Org**: `${INFLUXDB_ORG}`
- **Bucket**: `${INFLUXDB_BUCKET}`
- **Token**: Bearer or API Token authentication.

## Context: Management Databases Infrastructure (mng-db)

## Usage

### 1. Connecting to Valkey

From inside the network:

```bash
valkey-cli -h 172.19.0.70 -a $(cat /run/secrets/valkey_password)
```

### 2. Connecting to PostgreSQL

From host (if port exported):

```bash
psql -h localhost -p 5432 -U postgres
```

From container:

```bash
docker exec -it mng-pg psql -U postgres
```

### 3. RedisInsight Setup

1. Go to `https://redisinsight.${DEFAULT_URL}`.
2. Login via SSO.
3. Add Database:
   - **Host**: `172.19.0.70` (or `mng-valkey`)
   - **Port**: `6379`
   - **Username**: (Empty)
   - **Password**: Copy from `.env` or secret.
   - **Name**: `Production Cache`

## Context: Qdrant Vector Database (qdrant)

## Usage

### 1. Web UI (Dashboard)

- **URL**: `https://qdrant.${DEFAULT_URL}`
- **Features**: View collections, memory usage, and basic point browsing.

### 2. API Operations

**Create a Collection:**

```bash
curl -X PUT "https://qdrant.${DEFAULT_URL}/collections/my_documents" \
     -H "Content-Type: application/json" \
     --data '{
       "vectors": {
         "size": 3,
         "distance": "Cosine"
       }
     }'
```

**Search Vectors:**

```bash
curl -X POST "https://qdrant.${DEFAULT_URL}/collections/my_documents/points/search" \
     -H "Content-Type: application/json" \
     --data '{
       "vector": [0.12, 0.08, 0.94],
       "limit": 3
     }'
```

### 3. Integration with Open WebUI

Open WebUI connects internally via:

- **URL**: `http://qdrant:6333`
- **Context**: Used automatically for RAG when "Docs" are active in a chat.

## Context: Valkey Cluster (valkey-cluster)

## Usage

### Connecting (Internal)

Applications use standard Redis Cluster libraries.
Seed nodes: `valkey-node-0:6379`, `valkey-node-1:6380`, etc.

### Connecting (Debugging)

To manually interact with the cluster from the specific node:

```bash
# Connect to node-0
docker exec -it valkey-node-0 valkey-cli -c -a $(cat /run/secrets/valkey_password) -p 6379
```

_Note: The `-c` flag enables cluster mode redirection._

### Usage from Host

Similar to the Redis Cluster, Host ports are for debugging specific nodes only. Cluster redirection (MOVED errors) will return internal `172.19.x.x` IPs which are unreachable from the host without VPN/Tunneling.

## Context: MinIO Object Storage (minio)

## Usage

### 1. Web Console

- **URL**: `https://minio-console.${DEFAULT_URL}`
- **Login**: Use credentials from `.env` (or secrets).

### 2. S3 Access (Clients)

- **Endpoint**: `https://minio.${DEFAULT_URL}`
- **Region**: `us-east-1` (MinIO default)

### 3. CLI (mc)

You can interact with MinIO using the official client.

**Alias Configuration:**

```bash
mc alias set local http://localhost:${MINIO_HOST_PORT} ROOT_USER ROOT_PASSWORD
```

**Commands:**

```bash
# List buckets
mc ls local

# Upload file
mc cp my-file.txt local/cdn-bucket/

# Set bucket public
mc anonymous set public local/cdn-bucket
```

## Context: CouchDB Cluster (couchdb)

## Usage

### 1. Web UI (Fauxton)

Access the management dashboard at `https://couchdb.${DEFAULT_URL}/_utils`.

### 2. API Access

```bash
# Check cluster status
curl -u ${COUCHDB_USERNAME}:${COUCHDB_PASSWORD} https://couchdb.${DEFAULT_URL}/_membership

# Create a database
curl -X PUT -u ${COUCHDB_USERNAME}:${COUCHDB_PASSWORD} https://couchdb.${DEFAULT_URL}/my_new_db
```

## Context: OpenSearch Cluster (opensearch)

## Usage

### 1. Accessing Dashboards

- **URL**: `https://opensearch-dashboard.${DEFAULT_URL}`
- **Credentials**: user: `${ELASTIC_USERNAME}` / pass: `${ELASTIC_PASSWORD}`

### 2. Accessing API

- **URL**: `https://opensearch.${DEFAULT_URL}`
- **Note**: Self-signed certificate warning is expected.

```bash
curl -k -u admin:${OPENSEARCH_ADMIN_PASSWORD} https://opensearch.${DEFAULT_URL}/_cluster/health?pretty
```

### 3. Scaling to 3 Nodes

1. Edit `docker-compose.yml`:
   - Uncomment `opensearch-node2` and `opensearch-node3`.
   - Comment out `discovery.type=single-node`.
   - Uncomment `discovery.seed_hosts` and `cluster.initial_cluster_manager_nodes`.
2. Deploy:

   ```bash
   docker compose up -d
   ```

## Context: PostgreSQL HA Cluster (postgresql-cluster)

## Usage

### Connecting to the Cluster

Always connect via the **Router** to respect Leader/Replica roles.

**Write Operations (Leader):**

```bash
psql -h localhost -p ${POSTGRES_WRITE_HOST_PORT} -U postgres
```

**Read Operations (Replica):**

```bash
psql -h localhost -p ${POSTGRES_READ_HOST_PORT} -U postgres
```

### Checking Cluster Health

You can check the Patroni API on any node:

```bash
curl http://localhost:8008/cluster
```

## Context: Workflow (07-workflow) (07-workflow)

## Run

```bash
# Core workflow
docker compose up -d n8n

# Airflow stack (optional)
docker compose --profile airflow up -d
```

## Context: n8n (Workflow Automation) (n8n)

## Usage

### 1. Scaling Workers

Scale the execution capacity horizontally if the job queue length grows:

```bash
docker compose up -d --scale n8n-worker=3
```

### 2. Monitoring the Queue

```bash
# Check queue length directly in Valkey
docker exec -it n8n-valkey valkey-cli -a $(cat /run/secrets/valkey_password) LLEN n8n:bull:jobs:wait
```

## Context: Apache Airflow (airflow)

## Usage

### 1. Web Access

- **Airflow UI**: `https://airflow.${DEFAULT_URL}`
  - Credentials: `${_AIRFLOW_WWW_USER_USERNAME}` / `${_AIRFLOW_WWW_USER_PASSWORD}`
- **Flower UI**: `https://flower.${DEFAULT_URL}`
  - Protected by SSO (Traefik middleware) due to lack of built-in auth.

### 2. CLI Commands

Use the `airflow-cli` service or `exec` into `airflow-scheduler` to run commands.

```bash
# List all DAGs
docker compose run --rm airflow-cli airflow dags list

# Trigger a DAG
docker compose run --rm airflow-cli airflow dags trigger example_dag

# Check config
docker compose run --rm airflow-cli airflow config list
```

### 3. Adding DAGs

Place your python DAG files in the global DAGs volume (or mapped host directory if configured).
If using the default volume:

```bash
# Copy local DAG to container volume
docker cp ./my_dag.py airflow-scheduler:/opt/airflow/dags/
```

## Context: Security (03-security) (03-security)

## Run

```bash
docker compose --profile vault up -d vault
```

## Context: Tooling (09-tooling) (09-tooling)

## Run

```bash
# Terrakube / SonarQube (optional)
docker compose --profile terrakube up -d
docker compose --profile sonarqube up -d

# Standalone Terraform (not included at root)
cd infra/09-tooling/terraform
docker compose run --rm terraform version
```

## Context: SonarQube (sonarqube)

## Usage

### 1. Web Dashboard

- **URL**: `https://sonarqube.${DEFAULT_URL}`
- **Default Creds**: `admin` / `admin` (Change on first login)

### 2. Running Analysis (Local)

You can run a scan using Docker without installing the scanner locally:

```bash
docker run \
    --rm \
    -e SONAR_HOST_URL="https://sonarqube.${DEFAULT_URL}" \
    -e SONAR_TOKEN="${SONAR_TOKEN}" \
    -v "${PWD}:/usr/src" \
    sonarsource/sonar-scanner-cli
```

## Context: Terraform Infrastructure as Code (terraform)

## Usage

Since Terraform is running inside a container, you use `docker compose run` to execute commands.

### 1. Initialization

Initialize the Terraform working directory. This downloads providers and modules.

```bash
docker compose run --rm terraform init
```

### 2. Planning

Generate an execution plan.

```bash
docker compose run --rm terraform plan
```

### 3. Applying

Apply the changes required to reach the desired state of the configuration.

```bash
docker compose run --rm terraform apply
```

### 4. Formatting

Rewrites config files to canonical format.

```bash
docker compose run --rm terraform fmt
```

## Context: Terrakube (terrakube)

## Usage

### 1. Web Dashboard

- **URL**: `https://terrakube-ui.${DEFAULT_URL}`
- **Login**: Redirects to Keycloak for authentication.

### 2. CLI authentication

You can use the output from the UI to configure your Terraform CLI backend or generate Personal Access Tokens (PAT).

## Context: Auth (02-auth) (02-auth)

## Run

```bash
docker compose up -d keycloak oauth2-proxy
```

## Context: OAuth2 Proxy (SSO) (oauth2-proxy)

## Usage

### 1. Protecting a Service (Traefik Middleware)

To protect any service with SSO, apply the following Traefik label in its `docker-compose.yml`:

```yaml
labels:
  - 'traefik.http.routers.my-app.middlewares=sso-auth@file'
```

The `sso-auth` middleware (defined in Traefik's dynamic config) forwards requests to `http://auth.${DEFAULT_URL}/oauth2/auth`.

### 2. Manual Sign-In

- **URL**: `https://auth.${DEFAULT_URL}`
- **Action**: Redirects to the configured IdP (e.g., Keycloak).

## Context: Communication (10-communication) (10-communication)

## Run

```bash
docker compose --profile mail up -d mailhog
```

## Context: Mail Server Infrastructure (mail)

## Usage

### Configuring Applications (Internal)

To send emails from other services within the `infra_net` network:

- **Host**: `mailhog`
- **Port**: `1025`
- **Auth**: None (MailHog accepts everything)

### Accessing Web UI

- **URL**: `https://mail.${DEFAULT_URL}`
- **Login**: Authenticate via your SSO provider.

## Context: AI (08-ai) (08-ai)

## Run

```bash
docker compose --profile ollama up -d ollama open-webui
```

## Context: Ollama & Open WebUI (open-webui)

## Usage

### 1. Model Setup (Required First Time)

You must download models before chatting.

**Via CLI**:

```bash
# Chat Model
docker exec -it ollama ollama pull llama3

# Embedding Model (Required for RAG)
docker exec -it ollama ollama pull qwen3-embedding:0.6b
```

**Via Web UI**:
Go to **Admin Panel > Settings > Models** and pull `llama3` and associated embedding models from the interface.

### 2. Accessing Interfaces

- **Chat UI**: `https://chat.${DEFAULT_URL}`
- **API**: `https://ollama.${DEFAULT_URL}`

### 3. GPU Verification

To confirm Ollama is using your GPU:

```bash
docker exec -it ollama nvidia-smi
```

_You should see a process utilizing VRAM._

## Context: Ollama & Open WebUI (ollama)

## Usage

### 1. Model Setup (Required First Time)

You must download models before chatting.

**Via CLI**:

```bash
# Chat Model
docker exec -it ollama ollama pull llama3

# Embedding Model (Required for RAG)
docker exec -it ollama ollama pull qwen3-embedding:0.6b
```

**Via Web UI**:
Go to **Admin Panel > Settings > Models** and pull `llama3` and associated embedding models from the interface.

### 2. Accessing Interfaces

- **Chat UI**: `https://chat.${DEFAULT_URL}`
- **API**: `https://ollama.${DEFAULT_URL}`

### 3. GPU Verification

To confirm Ollama is using your GPU:

```bash
docker exec -it ollama nvidia-smi
```

_You should see a process utilizing VRAM._
