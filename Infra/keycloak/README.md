# Keycloak IAM

## Overview

Keycloak is an open-source Identity and Access Management (IAM) solution. This deployment runs in **Development Mode** (`start-dev`) but is configured with production-grade database settings.

## Service Details

- **Service Name**: `keycloak`
- **Image**: `quay.io/keycloak/keycloak:26.5.0`
- **Command**: `start-dev`
- **Exposed Port**: `${KEYCLOAK_MANAGEMENT_PORT}` (Management)

## Networking

- **Network**: `infra_net`
- **Static IPv4**: `172.19.0.29`
- **Hostname**: `keycloak`

## Environment Variables

### Core Configuration

- `KC_HOSTNAME`: `https://keycloak.${DEFAULT_URL}`
- `KC_PROXY_HEADERS`: `xforwarded` (Trusts reverse proxy headers)
- `KEYCLOAK_ADMIN`: Admin username.
- `KEYCLOAK_ADMIN_PASSWORD`: Admin password.

### Database (PostgreSQL)

- `KC_DB`: `postgres` (implied by connection)
- `KC_DB_URL`: `jdbc:postgresql://${POSTGRES_HOSTNAME}:${POSTGRES_PORT}/${KEYCLOAK_DBNAME}`
- `KC_DB_USERNAME`: `${KEYCLOAK_DB_USER}`
- `KC_DB_PASSWORD`: `${KEYCLOAK_DB_PASSWORD}`

### Connection Pooling (Performance & Stability)

To prevent stale connections and manage load:

- `KC_DB_POOL_INITIAL_SIZE`: `1`
- `KC_DB_POOL_MIN_SIZE`: `1`
- `KC_DB_POOL_MAX_SIZE`: `10`
- `KC_METRICS_ENABLED`: `true`
- `KC_HEALTH_ENABLED`: `true`

### Java Options (Agroal / Quarkus)

Additional JVM options are set to enforce strict connection validation:

```bash
-Dquarkus.datasource.jdbc.idle-removal-interval=5M 
-Dquarkus.datasource.jdbc.background-validation-interval=1M
```

*checks connections strictly to avoid "Connection is closed" errors during idle periods.*

## Traefik Configuration

- **Domain**: `keycloak.${DEFAULT_URL}`
- **Entrypoint**: `websecure` (TLS Enabled)
- **Service Port**: `8080` (Internal HTTP port)

## Usage

### Accessing the Admin Console

- **URL**: `https://keycloak.<your-domain>`
- **Login**: `${KEYCLOAK_ADMIN}` / `${KEYCLOAK_ADMIN_PASSWORD}`

### Realm Configuration

On first login, you should:

1. Create a new **Realm**.
2. Configure **Clients** (for your applications).
3. Set up **Users** and **Roles**.
