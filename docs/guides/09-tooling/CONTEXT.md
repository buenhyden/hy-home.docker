---
layer: infra
---
# Tooling — System Context

**Overview (KR):** `09-tooling` 카테고리의 모든 서비스에 대한 시스템 컨텍스트 — 서비스 인벤토리, 외부 의존성, 시크릿 테이블, 네트워크 노출 및 데이터 흐름을 기술합니다.

## Service Inventory

| Service              | Container Name       | Image                        | Profile   | Access                                         |
| -------------------- | -------------------- | ---------------------------- | --------- | ---------------------------------------------- |
| SonarQube            | `sonarqube`          | `sonarqube:10.7.0-community` | `tooling` | `https://sonarqube.${DEFAULT_URL}`             |
| Terrakube API        | `terrakube-api`      | `azbuilder/api-server:2.29.0`| `tooling` | `https://terrakube-api.${DEFAULT_URL}`         |
| Terrakube UI         | `terrakube-ui`       | `azbuilder/terrakube-ui:2.29.0` | `tooling` | `https://terrakube-ui.${DEFAULT_URL}`       |
| Terrakube Executor   | `terrakube-executor` | `azbuilder/executor:2.29.0`  | `tooling` | `https://terrakube-executor.${DEFAULT_URL}`    |
| Terraform            | `terraform`          | `hashicorp/terraform:1.14.4` | `tooling` | Job mode (`docker compose run`)                |
| Locust (Master)      | `locust-master`      | custom (locustio/locust:2.43.2) | `tooling` | `http://localhost:${LOCUST_HOST_PORT:-18089}` |
| Locust (Worker ×2)   | `locust-worker`      | custom (locustio/locust:2.43.2) | `tooling` | Internal only                                 |
| Syncthing            | `syncthing`          | `syncthing/syncthing:2.0.13` | `tooling` | `https://syncthing.${DEFAULT_URL}`             |
| Registry             | `registry`           | `registry:2`                 | `tooling` | `localhost:${REGISTRY_PORT:-5000}` (HTTP only) |

## External Dependencies

| Dependency     | Service Path             | Used By                                          |
| -------------- | ------------------------ | ------------------------------------------------ |
| Keycloak       | `infra/02-auth/keycloak` | Terrakube (OIDC via DEX for all authenticated endpoints) |
| PostgreSQL MNG | `infra/04-data/mng-db`   | SonarQube (schema `${SONARQUBE_DBNAME}`), Terrakube (schema `terrakube`) |
| MinIO          | `infra/04-data/minio`    | Terrakube (state bucket `tfstate`, plan output logs) |
| Valkey MNG     | `infra/04-data/mng-db`   | Terrakube (job queue distributed locking)        |
| InfluxDB       | `infra/06-observability` | Locust (metrics write-target for load test results) |
| Traefik        | `infra/01-gateway`       | SonarQube, Terrakube (API/UI/Exec), Syncthing    |

## Secrets Table

| Docker Secret              | Consuming Service(s)      | Description                                        |
| -------------------------- | ------------------------- | -------------------------------------------------- |
| `sonarqube_db_password`    | SonarQube                 | PostgreSQL password for `${SONARQUBE_DB_USER}`.    |
| `terrakube_db_password`    | terrakube-api             | PostgreSQL password for `${TERRAKUBE_DB_USERNAME}`.|
| `terrakube_pat_secret`     | terrakube-api             | JWT signing secret for Personal Access Tokens.     |
| `terrakube_internal_secret`| terrakube-api, executor   | Shared secret between API and Executor nodes.      |
| `terrakube_valkey_password`| terrakube-api, executor   | Password for management Valkey (Redis-compat).     |
| `minio_app_user_password`  | terrakube-api, executor   | MinIO app-user password for `tfstate` bucket.      |
| `influxdb_api_token`       | locust-master, locust-worker | InfluxDB write token for metrics.               |
| `syncthing_password`       | syncthing                 | Web GUI admin password.                            |

## Network Exposure

```text
Internet → Traefik (01-gateway)
  ├── sonarqube.${DEFAULT_URL}     → sonarqube:9000       (HTTPS via Traefik)
  ├── terrakube-api.${DEFAULT_URL} → terrakube-api:8080   (HTTPS via Traefik)
  ├── terrakube-ui.${DEFAULT_URL}  → terrakube-ui:3000    (HTTPS via Traefik)
  ├── terrakube-executor.${DEFAULT_URL} → terrakube-executor:8090 (HTTPS via Traefik)
  └── syncthing.${DEFAULT_URL}     → syncthing:8384       (HTTPS via Traefik)

Host Direct Ports:
  ├── localhost:18089  → locust-master:8089   (Locust Web UI, no proxy)
  ├── localhost:5000   → registry:5000        (Docker Registry, HTTP only)
  ├── 0.0.0.0:22000  → syncthing:22000       (Sync protocol TCP+UDP)
  └── 0.0.0.0:21027  → syncthing:21027       (Discovery broadcast UDP)
```

## Data Flow Diagram

```text
Developer → sonarqube.${DEFAULT_URL}
             └── SonarQube ──────────── mng-pg (schema: sonarqube)
                  └── reads code from local scanner CLI

Developer → terrakube-ui.${DEFAULT_URL}
             └── Terrakube UI → Keycloak (OIDC login)
                              → Terrakube API (REST)
                                  ├── mng-pg (schema: terrakube)
                                  ├── MinIO / tfstate bucket
                                  ├── Valkey (job queue lock)
                                  └── Terrakube Executor (job dispatch via HTTP)

Operator → docker compose run terraform ...
             └── Terraform CLI → MinIO (S3 backend) or local workspace/

Load Test → localhost:18089 (Locust Web UI)
             └── Locust Master → Locust Workers (fan-out load)
                              └── Target service (via host-gateway)
                              └── InfluxDB (metrics write)

Peer Device ← Syncthing ↔ ${DEFAULT_RESOURCES_DIR} (host filesystem)

Build Pipeline → registry:5000
                  └── Docker Distribution → ${DEFAULT_REGISTRY_DIR}
```

## Host Requirements

- **SonarQube Elasticsearch**: `vm.max_map_count >= 524288` on the Docker host. Set with:

  ```bash
  sysctl -w vm.max_map_count=524288
  echo "vm.max_map_count=524288" >> /etc/sysctl.conf
  ```

- **Locust**: Requires pre-created `locustfile.py` at `${DEFAULT_TOOLING_DIR}/locust/locustfile.py`.
- **Registry**: Docker daemon needs `"insecure-registries": ["localhost:5000"]` in `/etc/docker/daemon.json` for local pushes.
