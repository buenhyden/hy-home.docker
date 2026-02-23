# Authentication Stack Guide

> Setup and operational configurations for the local Keycloak and OAuth2-Proxy stack.

## 1. Introduction

The identity provisioning and SSO functionalities are housed within `infra/02-auth/`. It uses Keycloak as the OIDC Identity Provider (IdP), and OAuth2-Proxy to protect applications lacking native SSO integrations (like Kafka UI, Prometheus, etc.).

## 2. Keycloak Bootstrap

Upon initial deployment (`docker compose -f infra/02-auth/keycloak/docker-compose.yml up -d`), Keycloak spins up an empty master realm.

### Initial Configuration Steps

1. Navigate to `https://keycloak.${DEFAULT_URL}`.
2. Login with the initial credentials defined in `.env.infra` (`KEYCLOAK_ADMIN`/`KEYCLOAK_ADMIN_PASSWORD`).
3. **Realm Creation:** Create a new realm named `internal-dev` or import from the `./config/realm-export.json` if available.
4. **Client Setup:** Add a new OpenID Connect Client named `oauth2-proxy`.
   - Set "Client authentication" to `On`.
   - Set "Valid redirect URIs" to `https://auth.${DEFAULT_URL}/oauth2/callback`.
5. **Users & Credentials:** Add your standard administrator user under the new realm and assign roles.

## 3. OAuth2 Proxy Settings

OAuth2-Proxy bridges incoming requests via Traefik middleware to Keycloak for authentication validation.

- It shares stateless operation rules, with session state backed tightly by `mng-valkey`.

**Key Environment Adjustments:**

- `OAUTH2_PROXY_CLIENT_ID`: The client ID you created in Keycloak (e.g., `oauth2-proxy`).
- `OAUTH2_PROXY_CLIENT_SECRET`: The secret auto-generated when configuring the client in Keycloak.
- `OAUTH2_PROXY_COOKIE_SECRET`: Ensure this is a securely generated random string (`openssl rand -base64 32 | tr -d '\n'`).
- `OAUTH2_PROXY_OIDC_ISSUER_URL`: The realm url `http://keycloak:8080/realms/internal-dev` in standard setups.

> [!TIP]
> Do not attempt to update the configuration file in runtime without bouncing the container. As OAuth2 proxy runs as `read_only: true`, state injections must occur via container arguments/env reloads exclusively.
