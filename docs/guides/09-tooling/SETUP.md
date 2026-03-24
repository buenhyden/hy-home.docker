---
layer: infra
---
# Tooling — Lifecycle & Procedures

**Overview (KR):** `09-tooling` 서비스들의 시작 순서, 초기 설정, 시크릿 관리, 업그레이드 및 운영 절차를 기술합니다.

## Prerequisites

Before starting any tooling service, ensure these external services are healthy:

```bash
# Verify management database is ready
docker inspect --format='{{.State.Health.Status}}' mng-pg

# Verify MinIO is ready (required by Terrakube)
docker inspect --format='{{.State.Health.Status}}' minio

# Verify Keycloak is ready (required by Terrakube)
docker inspect --format='{{.State.Health.Status}}' keycloak

# Verify InfluxDB is ready (required by Locust)
docker inspect --format='{{.State.Health.Status}}' influxdb
```

## Startup Order

Services can start individually or all at once with the `tooling` profile. Due to cross-service dependencies being disabled in compose files (commented `depends_on`), verify external deps manually before starting.

```bash
# Start all tooling services
docker compose --profile tooling up -d

# Or start individually (recommended order for first-time setup)
docker compose up -d registry        # No dependencies
docker compose up -d syncthing       # No dependencies
docker compose up -d sonarqube       # Depends on: mng-pg
docker compose up -d terrakube-api   # Depends on: mng-pg, minio, keycloak, mng-valkey
docker compose up -d terrakube-ui    # Depends on: terrakube-api
docker compose up -d terrakube-executor  # Depends on: terrakube-api
docker compose up -d locust-master   # Depends on: influxdb
docker compose up -d locust-worker   # Depends on: locust-master
```

## Initial Setup Procedures

### SonarQube — First Login

1. Navigate to `https://sonarqube.${DEFAULT_URL}`.
2. Log in with default credentials: `admin` / `admin`.
3. **Change the password immediately** when prompted.
4. Create analysis tokens via **My Account → Security → Generate Tokens**.
5. Use the token with the scanner CLI:

   ```bash
   docker run --rm \
     -e SONAR_HOST_URL="https://sonarqube.${DEFAULT_URL}" \
     -e SONAR_TOKEN="<your-token>" \
     -v "${PWD}:/usr/src" \
     sonarsource/sonar-scanner-cli
   ```

> **Host Requirement**: Set `vm.max_map_count >= 524288` on the Docker host:
>
> ```bash
> sysctl -w vm.max_map_count=524288
> # Persist: echo "vm.max_map_count=524288" >> /etc/sysctl.conf
> ```

### Terrakube — Keycloak Client Setup

Terrakube authenticates via Keycloak using OpenID Connect (DEX mode). On first deploy:

1. Log in to Keycloak Admin at `https://keycloak.${DEFAULT_URL}`.
2. Select the `hy-home.realm` realm.
3. Create a new client with:
   - **Client ID**: value of `${OAUTH2_PROXY_CLIENT_ID}` (same as used in `DexClientId`)
   - **Valid Redirect URIs**: `https://terrakube-ui.${DEFAULT_URL}/*`
   - **Web Origins**: `https://terrakube-ui.${DEFAULT_URL}`
4. Create a group called `TERRAKUBE_ADMIN` and add your user.
5. Navigate to `https://terrakube-ui.${DEFAULT_URL}` and authenticate.

### Terrakube — MinIO Bucket Setup

The `tfstate` bucket in MinIO must exist before the Terrakube API starts successfully:

1. Log in to MinIO at `https://minio.${DEFAULT_URL}`.
2. Create a bucket named `tfstate`.
3. Create an app-user with access to `tfstate` and store the password in the `minio_app_user_password` secret, update `MINIO_APP_USERNAME` in `.env`.

### Locust — Locustfile Preparation

Before starting Locust services, place a `locustfile.py` in the bind-mounted directory:

```bash
mkdir -p ${DEFAULT_TOOLING_DIR}/locust
cat > ${DEFAULT_TOOLING_DIR}/locust/locustfile.py << 'EOF'
from locust import HttpUser, task

class MyUser(HttpUser):
    @task
    def hello(self):
        self.client.get("/")
EOF
```

### Registry — Insecure Registry Configuration

For local Docker pushes/pulls, add the registry to Docker daemon:

```bash
# Edit /etc/docker/daemon.json
{
  "insecure-registries": ["localhost:5000"]
}
sudo systemctl restart docker
```

## Shutdown

```bash
# Stop all tooling services
docker compose --profile tooling down

# Stop individual service
docker compose stop sonarqube
```

## Upgrade Procedures

### SonarQube

1. Check release notes at [SonarQube Downloads](https://www.sonarsource.com/products/sonarqube/downloads/).
2. Update `image: sonarqube:NEW_VERSION` in `infra/09-tooling/sonarqube/docker-compose.yml`.
3. Validate: `docker compose -f infra/09-tooling/sonarqube/docker-compose.yml config`.
4. Pull and restart:

   ```bash
   docker compose pull sonarqube
   docker compose up -d sonarqube
   ```

5. Monitor startup logs: `docker logs -f sonarqube` — wait for `SonarQube is operational`.

### Terrakube

All three nodes (`terrakube-api`, `terrakube-ui`, `terrakube-executor`) must be on the **same version**.

1. Update all three image tags in `infra/09-tooling/terrakube/docker-compose.yml`.
2. Validate: `docker compose -f infra/09-tooling/terrakube/docker-compose.yml config`.
3. Pull and restart in order:

   ```bash
   docker compose pull terrakube-api terrakube-ui terrakube-executor
   docker compose up -d terrakube-api
   # Wait for terrakube-api to be healthy
   docker compose up -d terrakube-ui terrakube-executor
   ```

### Syncthing

1. Update `image: syncthing/syncthing:NEW_VERSION` in `infra/09-tooling/syncthing/docker-compose.yml`.
2. Restart: `docker compose up -d syncthing`.

## Secret Rotation

| Secret                   | Rotation Procedure                                               |
| :---                     | :---                                                             |
| `sonarqube_db_password`  | Change in PostgreSQL + update secret file + restart sonarqube.  |
| `terrakube_pat_secret`   | Update secret file + restart terrakube-api (invalidates all PATs).|
| `terrakube_internal_secret` | Update on BOTH api and executor + restart both nodes.         |
| `terrakube_valkey_password` | Change in Valkey + update secret file + restart api & executor.|
| `minio_app_user_password`| Rotate in MinIO + update secret file + restart api & executor.  |
| `influxdb_api_token`     | Create new token in InfluxDB + update secret file + restart Locust.|
| `syncthing_password`     | Update secret file + restart syncthing.                          |

## Validate Configuration

Always validate Docker Compose configuration before `up`:

```bash
docker compose -f infra/09-tooling/sonarqube/docker-compose.yml config --quiet
docker compose -f infra/09-tooling/terrakube/docker-compose.yml config --quiet
docker compose -f infra/09-tooling/terraform/docker-compose.yml config --quiet
docker compose -f infra/09-tooling/locust/docker-compose.yml config --quiet
docker compose -f infra/09-tooling/syncthing/docker-compose.yml config --quiet
docker compose -f infra/09-tooling/registry/docker-compose.yml config --quiet
```
