# Tooling Operations & Troubleshooting

> **Components**: `sonarqube`, `terraform`, `terrakube`

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
- **"State Locking Issues"**: Verify connection to `mng-redis` (Valkey). Check `terrakube-api` logs for Redis connection errors.
