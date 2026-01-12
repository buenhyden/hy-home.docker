# Keycloak

## Overview

Open Source Identity and Access Management.

## Services

- **keycloak**: Keycloak Server.
  - URL: `https://keycloak.${DEFAULT_URL}`

## Configuration

### Environment Variables

- `KC_DB`: Database vendor (`postgres`).
- `KC_DB_URL`: JDBC URL.
- `KC_DB_USERNAME`: Database user.
- `KC_DB_PASSWORD`: Database password.
- `KEYCLOAK_ADMIN`: Admin username.
- `KEYCLOAK_ADMIN_PASSWORD`: Admin password.
- `KC_HOSTNAME`: Public facing URL (`https://keycloak.${DEFAULT_URL}`).
- `KC_PROXY_HEADERS`: `xforwarded` (for Traefik).

## Networks

- `infra_net`
  - IP: `172.19.0.29`

## Traefik Routing

- **Domain**: `keycloak.${DEFAULT_URL}`
