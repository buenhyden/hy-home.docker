# Environment Variables Reference

This document provides a comprehensive reference for all environment variables used across the infrastructure services. These variables are configured in `.env` files or Docker Secrets.

## Global Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `DOMAIN_NAME` | Base domain for services | `127.0.0.1.nip.io` |
| `TZ` | Timezone | `UTC` |

<!-- APPEND_HERE -->

## Infrastructure Services

### Apache Airflow

| Variable | Description | Default |
| :--- | :--- | :--- |
| `AIRFLOW__CORE__EXECUTOR` | Executor Type | `CeleryExecutor` |
| `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` | Metadata DB Connection | `postgresql+psycopg2://...` |
| `AIRFLOW__CELERY__RESULT_BACKEND` | Celery Backend | `db+postgresql://...` |
| `AIRFLOW__CELERY__BROKER_URL` | Celery Broker (Redis) | `redis://...` |
| `AIRFLOW__WEBSERVER__BASE_URL` | External URL | `https://airflow.${DEFAULT_URL}` |
| `_AIRFLOW_WWW_USER_USERNAME` | Admin Username | `${_AIRFLOW_WWW_USER_USERNAME}` |
| `_AIRFLOW_WWW_USER_PASSWORD` | Admin Password | `${_AIRFLOW_WWW_USER_PASSWORD}` |

### CouchDB

| Variable | Description | Default |
| :--- | :--- | :--- |
| `COUCHDB_USER` | Admin username | `${COUCHDB_USERNAME}` |
| `COUCHDB_PASSWORD` | Admin password | `${COUCHDB_PASSWORD}` |
| `COUCHDB_COOKIE` | Erlang magic cookie | `${COUCHDB_COOKIE}` |
| `NODENAME` | Unique Erlang node name | `couchdb-X.infra_net` |

### Harbor

| Variable | Description | Default |
| :--- | :--- | :--- |
| `EXT_ENDPOINT` | External URL | `https://harbor.${DEFAULT_URL}` |
| `HARBOR_ADMIN_PASSWORD` | Admin Password | `${HARBOR_PASSWORD}` |
| `POSTGRESQL_HOST` | DB Host | `${POSTGRES_HOSTNAME}` |
| `POSTGRESQL_DATABASE` | DB Name | `${HARBOR_POSTGRE_DBNAME}` |
| `CORE_SECRET` | Core Service Secret | `${HARBOR_CORE_SECRET}` |
| `JOBSERVICE_SECRET` | Job Service Secret | `${HARBOR_JOBSERVICE_SECRET}` |
| `REGISTRY_HTTP_SECRET` | Registry Secret | `${HARBOR_REGISTRY_HTTP_SECRET}` |

### InfluxDB

| Variable | Description | Default |
| :--- | :--- | :--- |
| `INFLUXDB_DB` | Database Name | `${INFLUXDB_DB_NAME}` |
| `DOCKER_INFLUXDB_INIT_USERNAME` | Initial Admin Username | `${INFLUXDB_USERNAME}` |
| `DOCKER_INFLUXDB_INIT_PASSWORD` | Initial Admin Password | `${INFLUXDB_PASSWORD}` |
| `DOCKER_INFLUXDB_INIT_ORG` | Default Organization Name | `${INFLUXDB_ORG}` |
| `DOCKER_INFLUXDB_INIT_BUCKET` | Default Bucket Name | `${INFLUXDB_BUCKET}` |
| `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN`| Admin API Token | `${INFLUXDB_API_TOKEN}` |

### Kafka (KRaft)

| Variable | Description | Default |
| :--- | :--- | :--- |
| `CLUSTER_ID` | KRaft Cluster ID | `${KAFKA_CLUSTER_ID}` |
| `KAFKA_NODE_ID` | Unique Node identifier | `1`, `2`, `3` |
| `KAFKA_PROCESS_ROLES` | Server Role | `broker,controller` |
| `KAFKA_CONTROLLER_QUORUM_VOTERS`| KRaft Quorum Configuration | `1@kafka-1...` |
| `KAFKA_LISTENERS` | Listener URIs | `PLAINTEXT,CONTROLLER,EXTERNAL` |
| `KAFKA_ADVERTISED_LISTENERS` | Advertised URIs | `kafka-x,localhost` |

### Keycloak

| Variable | Description | Default |
| :--- | :--- | :--- |
| `KC_DB` | Database vendor | `postgres` |
| `KC_DB_URL` | JDBC Connection URL | `jdbc:postgresql://...` |
| `KC_DB_USERNAME` | Database username | `${KEYCLOAK_DB_USER}` |
| `KC_DB_PASSWORD` | Database password | `${KEYCLOAK_DB_PASSWORD}` |
| `KEYCLOAK_ADMIN` | Admin username | `${KEYCLOAK_ADMIN_USER}` |
| `KEYCLOAK_ADMIN_PASSWORD` | Admin password | `${KEYCLOAK_ADMIN_PASSWORD}` |
| `KC_HOSTNAME` | Public hostname | `https://keycloak.${DEFAULT_URL}` |
| `KC_PROXY_HEADERS` | Reverse proxy header mode | `xforwarded` |

### ksqlDB

| Variable | Description | Default |
| :--- | :--- | :--- |
| `KSQL_BOOTSTRAP_SERVERS` | Kafka Brokers | `kafka-1:${KAFKA_PORT}` |

### MinIO

| Variable | Description | Default |
| :--- | :--- | :--- |
| `MINIO_ROOT_USER_FILE` | Path to root user secret | `/run/secrets/minio_root_user` |
| `MINIO_ROOT_PASSWORD_FILE` | Path to root password secret | `/run/secrets/minio_root_password` |
| `MINIO_PROMETHEUS_AUTH_TYPE` | Prometheus scraping auth type | `public` |

### Terrakube

| Variable | Description | Default |
| :--- | :--- | :--- |
| `InternalSecret` | Shared Secret | `${TERRAKUBE_INTERNAL_SECRET}` |
| `TerrakubeRedisHostname` | Redis Host | `${MNG_VALKEY_HOST}` |
| `ApiDataSourceType` | DB Type | `POSTGRESQL` |
| `REACT_APP_TERRAKUBE_API_URL` | API URL | `https://terrakube-api...` |
| `REACT_APP_AUTHORITY` | Auth Authority | `https://keycloak...` |

### Management Databases (Mng-DB)

| Variable | Description | Default |
| :--- | :--- | :--- |
| `POSTGRES_USER` | Valid User | `${POSTGRES_USER}` |
| `POSTGRES_PASSWORD` | Superuser Password | `${PGPASSWORD_SUPERUSER}` |
| `POSTGRES_DB` | Init Database | `${POSTGRES_DB}` |
| `PGPASSWORD_SUPERUSER` | Auth for Script | `${PGPASSWORD_SUPERUSER}` |

### n8n

| Variable | Description | Default |
| :--- | :--- | :--- |
| `EXECUTIONS_MODE` | Execution Mode | `queue` |
| `N8N_ENCRYPTION_KEY` | Encryption Key | `${N8N_ENCRYPTION_KEY}` |
| `WEBHOOK_URL` | Public URL | `https://n8n.${DEFAULT_URL}` |
| `GENERIC_TIMEZONE` | Timezone | `${DEFAULT_TIMEZONE}` |
| `DB_TYPE` | Database Type | `postgresdb` |
| `DB_POSTGRESDB_HOST` | DB Host | `${POSTGRES_HOSTNAME}` |
| `QUEUE_BULL_REDIS_HOST`| Redis/Valkey Host | `${MNG_VALKEY_HOST}` |
| `N8N_METRICS` | Enable Metrics | `true` |

### Nginx (Standalone)

| Variable | Description |
| :--- | :--- |
| `HTTP_HOST_PORT` | Host port (80) |
| `HTTPS_HOST_PORT` | Host port (443) |

### OAuth2 Proxy

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SSL_CERT_FILE` | Trusted Root CA | `/etc/ssl/certs/rootCA.pem` |
| `OAUTH2_PROXY_CLIENT_SECRET` | OAuth2 Client Secret | `${OAUTH2_PROXY_CLIENT_SECRET}` |
| `OAUTH2_PROXY_COOKIE_SECRET` | Cookie encryption secret | `${OAUTH2_PROXY_COOKIE_SECRET}` |
| `OAUTH2_PROXY_REDIS_CONNECTION_URL` | Redis URL | `redis://...` |

### Observability

| Service | Variable | Description | Default |
| :--- | :--- | :--- | :--- |
| **Grafana** | `GF_SERVER_ROOT_URL` | Root URL | `https://grafana.${DEFAULT_URL}` |
| **Grafana** | `GF_SECURITY_ADMIN_USER` | Admin User | `${GRAFANA_ADMIN_USERNAME}` |
| **Grafana** | `GF_SECURITY_ADMIN_PASSWORD` | Admin Password | `${GRAFANA_ADMIN_PASSWORD}` |
| **Grafana** | `GF_AUTH_GENERIC_OAUTH_CLIENT_ID`| OAuth Client ID | `${OAUTH2_PROXY_CLIENT_ID}` |
| **Alertmanager** | `SMTP_USERNAME` | SMTP User | `${SMTP_USERNAME}` |
| **Alertmanager** | `SMTP_PASSWORD` | SMTP Password | `${SMTP_PASSWORD}` |
| **Alertmanager** | `SLACK_ALERTMANAGER_WEBHOOK_URL`| Slack Webhook | `${SLACK_ALERTMANAGER_WEBHOOK_URL}` |

### Ollama & Open WebUI

| Variable | Description | Default |
| :--- | :--- | :--- |
| `OLLAMA_HOST` | Binding Address | `0.0.0.0:${OLLAMA_PORT}` |
| `NVIDIA_VISIBLE_DEVICES` | GPU Isolation | `all` |
| `OLLAMA_BASE_URL` | Connection to Ollama | `http://ollama:${OLLAMA_PORT}` |
| `VECTOR_DB_URL` | Connection to Qdrant | `http://qdrant:${QDRANT_PORT}` |
| `RAG_EMBEDDING_ENGINE` | Embedding Provider | `ollama` |
| `RAG_EMBEDDING_MODEL` | Embedding Model | `qwen3-embedding:0.6b` |

### OpenSearch

| Variable | Description | Default |
| :--- | :--- | :--- |
| `OPENSEARCH_INITIAL_ADMIN_PASSWORD`| Admin Password | `${ELASTIC_PASSWORD}` |
| `OPENSEARCH_JAVA_OPTS` | JVM Options | `-Xms1g -Xmx1g` |
| `OPENSEARCH_HOSTS` | Dashboards target | `["https://opensearch-node1:9200"]` |
| `OPENSEARCH_USERNAME` | Dashboards User | `${ELASTIC_USERNAME}` |
| `OPENSEARCH_PASSWORD` | Dashboards Password | `${ELASTIC_PASSWORD}` |
| `ES_USERNAME` | Exporter User | `${ELASTIC_USERNAME}` |
| `ES_PASSWORD` | Exporter Password | `${ELASTIC_PASSWORD}` |

### PostgreSQL Cluster

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SCOPE` | Patroni Cluster Scope Name | `pg-ha` |
| `ETCD3_HOSTS` | etcd Cluster Endpoints | `etcd-1:2379,etcd-2...` |
| `PATRONI_NAME` | Unique Node Name | `pg-0`, `pg-1`... |
| `POSTGRES_USER` | Init User Name | `${POSTGRES_USER}` |
| `POSTGRES_DB` | Init Database Name | `${POSTGRES_DB}` |
| `POSTGRES_WRITE_PORT`| Router Write Port | `5432` |
| `POSTGRES_READ_PORT` | Router Read Port | `5433` |

### Qdrant

| Variable | Description | Default |
| :--- | :--- | :--- |
| `QDRANT__TELEMETRY_DISABLED` | Disable usage reporting | `false` |

### Redis Cluster

| Variable | Description | Default |
| :--- | :--- | :--- |
| `NODE_NAME` | Node Identity | `redis-node-X` |
| `PORT` | Node Port | `${REDISX_PORT}` |

### SonarQube

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SONAR_JDBC_URL` | JDBC Connection String | `jdbc:postgresql://...` |
| `SONAR_JDBC_USERNAME` | Database Username | `${SONARQUBE_DB_USER}` |
| `SONAR_JDBC_PASSWORD` | Database Password | `${SONARQUBE_DB_PASSWORD}` |

### Storybook

*Configured via Dockerfile build args and labels.*

### Traefik

*Configured via `traefik.yml` and `dynamic/` directory.*

### Valkey Cluster

| Variable | Description | Default |
| :--- | :--- | :--- |
| `NODE_NAME` | Node Identity | `valkey-node-X` |
| `PORT` | Node Port | `${VALKEYX_PORT}` |
