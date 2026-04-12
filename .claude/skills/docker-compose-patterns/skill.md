---
name: docker-compose-patterns
description: >
  Docker Compose service definition patterns, structure best practices, environment separation,
  and anti-patterns guide. Use for 'compose structure', 'service definition', 'multi-service architecture',
  'compose best practices', 'service isolation', 'environment config', 'named volumes', 'compose patterns'.
  Enhances the design capabilities of infra-implementer, iac-reviewer, and drift-detector.
  Note: actual docker compose up/down execution is outside the scope of this skill.
---

# Docker Compose Patterns — Service Definition Design Guide

Patterns and best practices for designing maintainable, secure Docker Compose service stacks.

## File Structure Patterns

### Pattern 1: Single-file with override files

```
project/
├── docker-compose.yml          # Base service definitions (shared)
├── docker-compose.override.yml # Dev overrides (auto-loaded, gitignored for secrets)
├── docker-compose.prod.yml     # Production overrides (explicit -f flag)
└── docker-compose.test.yml     # Test environment overrides
```

### Pattern 2: Service-group separation

```
project/
├── docker-compose.yml          # Shared infrastructure (networks, secrets, volumes)
├── infra/
│   ├── 01-gateway/             # Traefik / Nginx
│   ├── 02-auth/                # Keycloak + DB
│   ├── 03-messaging/           # Kafka + Zookeeper
│   ├── 04-data/                # PostgreSQL, MinIO
│   ├── 05-search/              # OpenSearch
│   └── 06-ai/                  # Ollama, Open-WebUI
└── scripts/
    └── validate-docker-compose.sh
```

## Service Definition Principles

### 1. Single Responsibility Service

```yaml
# Good: each service has one clear role
services:
  keycloak:
    image: quay.io/keycloak/keycloak:24.0.1
    # handles auth only

  postgres-keycloak:
    image: postgres:16.2-alpine
    # handles keycloak DB only

# Avoid: one container handling multiple unrelated functions
```

### 2. Mandatory Security Baseline (every service)

```yaml
services:
  example-service:
    image: example:1.2.3           # Always pin version — never use 'latest'
    security_opt:
      - no-new-privileges:true     # MANDATORY for all containers
    read_only: true                # Prefer read-only root filesystem
    tmpfs:
      - /tmp                       # Allow writes only to tmpfs when needed
    user: "1001:1001"              # Run as non-root
    networks:
      - infra_net                  # MANDATORY — never use default bridge
    restart: unless-stopped        # MANDATORY for stateful services
    mem_limit: 512m                # MANDATORY — always set resource limits
    cpus: "0.5"                    # MANDATORY
    secrets:
      - db_password                # Use secrets block — never env-var plaintext
```

### 3. Secrets Management Pattern

```yaml
secrets:
  db_password:
    file: ./secrets/db_password.txt   # Mounted as /run/secrets/db_password

services:
  postgres:
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password  # Service reads from file
    secrets:
      - db_password

# Never:
# environment:
#   POSTGRES_PASSWORD: mysecretpassword   # PROHIBITED — plaintext in env
```

### 4. Named Volume Convention

```yaml
# Convention: [Service]-[Data]-[Volume]
volumes:
  postgres-main-data:       # PostgreSQL main data volume
    driver: local
    labels:
      backup: "daily"       # Backup policy label
      service: "postgres"

  opensearch-indices-data:  # OpenSearch indices
    driver: local
    labels:
      backup: "weekly"

  minio-objects-data:       # MinIO object storage
    driver: local
    labels:
      backup: "daily"
```

### 5. Health Check Pattern

```yaml
services:
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-postgres}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s     # Allow startup time before health checks begin

  keycloak:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health/ready"]
      interval: 15s
      timeout: 10s
      retries: 3
      start_period: 60s

  # Services that depend on healthy upstream services
  api:
    depends_on:
      postgres:
        condition: service_healthy   # Only start when postgres is healthy
      keycloak:
        condition: service_healthy
```

## Network Isolation Pattern

```yaml
networks:
  infra_net:
    driver: bridge
    name: infra_net
    ipam:
      config:
        - subnet: 172.20.0.0/16

# All services MUST be on infra_net
# External access ONLY via gateway (Traefik/Nginx)
services:
  traefik:
    networks:
      - infra_net
    ports:
      - "80:80"
      - "443:443"   # Only gateway exposes external ports

  internal-service:
    networks:
      - infra_net
    # No ports exposed directly — access via traefik labels
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.internal.rule=Host(`internal.example.com`)"
```

## Environment Separation

| Configuration | Development | Production |
|---------------|-------------|------------|
| Image tags | Can use recent tags | Must pin exact digests |
| Resource limits | Relaxed | Enforced strictly |
| Log level | DEBUG | INFO / WARN |
| Secrets | Can use .env overrides | Docker Secrets only |
| Restart policy | `no` or `on-failure` | `unless-stopped` |
| Replica count | 1 | Defined per service SLO |

```yaml
# docker-compose.override.yml (development only, gitignored)
services:
  api:
    environment:
      LOG_LEVEL: debug
    mem_limit: 1g      # Relaxed for dev
    command: ["npm", "run", "dev"]  # Dev command with hot-reload
```

## Anti-Patterns and Solutions

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `image: service:latest` | Silent updates, non-deterministic builds | Pin exact version: `image: service:1.2.3` |
| Plaintext env secrets | Credentials exposed in `docker inspect` | Docker Secrets + `_FILE` env var convention |
| No `mem_limit` | Container can OOM the host | Set `mem_limit` on every service |
| No health-check | Dependent services start before upstream is ready | Define `healthcheck` + `depends_on: condition: service_healthy` |
| Default network | All containers share broadcast domain | Explicit `infra_net` with `bridge` driver |
| `privileged: true` | Full host access | Use specific `cap_add` only if unavoidable |
| Single massive compose file | Hard to audit, merge conflicts | Split by service group into `infra/` subdirs |
| Anonymous volumes | Data loss on `docker compose down -v` | Named volumes with backup labels |

## Drift-Prevention Checklist

Before applying any compose change, verify:

- [ ] Image tag pinned to specific version (not `latest`)
- [ ] `no-new-privileges: true` present
- [ ] `mem_limit` and `cpus` declared
- [ ] Service on `infra_net` (not default bridge)
- [ ] Secrets use `secrets:` block (not env-var plaintext)
- [ ] Named volume follows `[Service]-[Data]-[Volume]`
- [ ] Health-check defined for stateful services
- [ ] `restart: unless-stopped` on stateful services
- [ ] `depends_on` with `condition: service_healthy` for dependent services
- [ ] Run `bash scripts/validate-docker-compose.sh` before applying
