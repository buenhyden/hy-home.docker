---
layer: infra
---
# Tooling Operations & Troubleshooting

**Overview (KR):** 인프라 관리 도구들의 일반적인 장애 상황 분석 및 해결 방법 오퍼레이션 가이드입니다.

> **Components**: `sonarqube`, `terraform`, `terrakube`, `locust`, `syncthing`, `registry`

## SonarQube Usage

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

### Troubleshooting SonarQube

- **"ElasticSearch did not exit normally"**: Check `vm.max_map_count` on host.
- **"Database connection failed"**: Ensure PostgreSQL is healthy and the `sonarqube` database exists.

---

## Terraform Infrastructure as Code

### Usage

Since Terraform is running inside a container, you use `docker compose run` to execute commands.

```bash
docker compose run --rm terraform init
docker compose run --rm terraform plan
docker compose run --rm terraform apply
docker compose run --rm terraform fmt
```

---

## Terrakube

### Usage

- **URL**: `https://terrakube-ui.${DEFAULT_URL}`
- **Login**: Redirects to Keycloak for authentication.
- **CLI authentication**: Use the output from the UI to configure your Terraform CLI backend or generate Personal Access Tokens (PAT).

### Troubleshooting Terrakube

- **"Executor not picking up jobs"**: Check the `InternalSecret` matches between API and Executor. Ensure `terrakube-executor` can resolve `terrakube-api` (Docker DNS).
- **"State Locking Issues"**: Verify connection to Valkey (`mng-valkey`). Check `terrakube-api` logs for Redis connection errors.
- **"Auth redirect loop"**: Ensure Keycloak realm `hy-home.realm` has the Terrakube client registered and the `DexClientId` env var matches `OAUTH2_PROXY_CLIENT_ID`.
- **"MinIO connection refused"**: Confirm the `minio` service is healthy and `minio_app_user_password` secret is correctly mounted.

---

## Locust Load Testing

### Usage

Locust uses a master-worker architecture. The `locustfile.py` must be placed in the bind-mounted directory before starting.

```bash
# Place locustfile in the mounted data directory first
cp locustfile.py ${DEFAULT_TOOLING_DIR}/locust/locustfile.py

# Start master and workers
docker compose --profile tooling up -d locust-master locust-worker
```

- **Web UI**: `http://localhost:${LOCUST_HOST_PORT:-18089}`
- **Workers**: 2 replicas connect automatically to the master.

### Troubleshooting Locust

- **"No locustfile found"**: Ensure `locustfile.py` exists in `${DEFAULT_TOOLING_DIR}/locust/`.
- **"InfluxDB connection refused"**: Confirm `influxdb` service is healthy and `influxdb_api_token` secret is present.
- **Workers not connecting**: Check `locust-master` healthcheck passes before workers start.

---

## Syncthing File Sync

### Usage

- **Web GUI**: `https://syncthing.${DEFAULT_URL}`
- **Initial Setup**: On first start, configure remote devices via the Web GUI. The admin password is managed via `syncthing_password` Docker secret.

### Troubleshooting Syncthing

- **"GUI not reachable"**: Verify Traefik is routing port 8384. Check `syncthing` healthcheck endpoint `/rest/noauth/health`.
- **"Sync not working"**: Confirm sync port `22000` is accessible through firewall. Check remote device IDs match.
- **"Permission denied on files"**: Verify `PUID`/`PGID` (default 1000) match the host user owning `${DEFAULT_RESOURCES_DIR}`.

---

## Container Registry

### Usage

```bash
# Push a custom image to the local registry
docker tag my-image:latest localhost:${REGISTRY_PORT:-5000}/my-image:latest
docker push localhost:${REGISTRY_PORT:-5000}/my-image:latest

# Pull from the registry within Docker
docker pull registry:${REGISTRY_PORT:-5000}/my-image:latest
```

### Troubleshooting Registry

- **"HTTP response to HTTPS client"**: The registry runs plain HTTP. Docker daemon must have `localhost:${REGISTRY_PORT}` in `insecure-registries` for local pulls.
- **"No healthy upstream"**: Check `${DEFAULT_REGISTRY_DIR}` exists and is writable.
