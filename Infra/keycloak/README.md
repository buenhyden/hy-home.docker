# Keycloak

## Overview

Keycloak is an open-source Identity and Access Management (IAM) solution. This deployment runs in dev mode (`start-dev`) and uses PostgreSQL as the database.

## Service Details

- **Image**: `quay.io/keycloak/keycloak:26.5.0`
- **Command**: `start-dev`
- **Exposed Port**: `${KEYCLOAK_MANAGEMENT_PORT}`
- **Network**: `infra_net` (Static IP: `172.19.0.29`)

## Environment Variables

- **Database**:
  - `KC_DB`: Database vendor (e.g., `postgres`).
  - `KC_DB_URL`: JDBC connection URL.
  - `KC_DB_USERNAME` / `KC_DB_PASSWORD`: Capabilities.
- **Admin**:
  - `KEYCLOAK_ADMIN`: Admin username.
  - `KEYCLOAK_ADMIN_PASSWORD`: Admin password.
- **Hostname**:
  - `KC_HOSTNAME`: `https://keycloak.${DEFAULT_URL}`
  - `KC_PROXY_HEADERS`: `xforwarded`

## Traefik Configuration

- **Domain**: `keycloak.${DEFAULT_URL}`
- **Port**: `8080` (Internal)
- **Entrypoint**: `websecure`
- **TLS**: Enabled
