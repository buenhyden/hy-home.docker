# Keycloak IAM

## Overview

Keycloak is an open-source Identity and Access Management (IAM) solution. This
deployment runs in **Development Mode** (`start-dev`) but is configured with
production-grade database settings.

## Service Details

- **Service Name**: `keycloak`
- **Image**: `quay.io/keycloak/keycloak:26.5.0`
- **Command**: `start-dev`
- **Exposed Port**: `${KEYCLOAK_MANAGEMENT_PORT}` (Management)

## Custom Build

This directory contains a `Dockerfile` that allows for a custom Keycloak build, following the [official Container guide](https://www.keycloak.org/server/containers). This is useful for:

- **Optimization**: Pre-building Keycloak to reduce startup time (optimizing for specific providers).
- **Customization**: Adding custom themes, SPIs (Service Provider Interfaces), or scripts.
- **Development**: Embedding self-signed certificates for development (as demonstrated in the Dockerfile).

### Customization Examples

1. **Adding a Custom Theme**:
    - Place your theme directory in logical folder (e.g., `themes/my-theme`).
    - Add `COPY themes/my-theme /opt/keycloak/themes/my-theme` to the `Dockerfile`.

2. **Adding a Provider (SPI)**:
    - Place your jar file in `providers/`.
    - Add `COPY providers/my-provider.jar /opt/keycloak/providers/` to the `Dockerfile`.
    - Run `RUN /opt/keycloak/bin/kc.sh build` to optimize.

### How to use

1. Open `docker-compose.yml`.
2. Comment out the `image` instruction.
3. Add/Uncomment the `build` instruction:

```yaml
services:
  keycloak:
    # image: quay.io/keycloak/keycloak:26.5.0
    build:
      context: .
      dockerfile: Dockerfile
```

1. Rebuild the container: `docker-compose up -d --build keycloak`.

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

## Configuration Reference

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
| `KC_DB_POOL_INITIAL_SIZE` | Initial DB pool size | `1` |
| `KC_DB_POOL_MIN_SIZE` | Min DB pool size | `1` |
| `KC_DB_POOL_MAX_SIZE` | Max DB pool size | `10` |
| `KC_METRICS_ENABLED` | Enable metrics endpoint | `true` |
| `KC_HEALTH_ENABLED` | Enable health endpoint | `true` |
| `JAVA_OPTS_APPEND` | Extra JVM options | *See above* |

*Checks connections strictly to avoid "Connection is closed" errors during
idle periods.*

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

## Advanced Configuration

### 1. Group Membership Mapping

To include user groups in the JWT token (e.g., for RBAC in applications):

1. Go to **Client Scopes** > **Create client scope**.
   - Name: `groups`
   - Protocol: `OpenID Connect`
   - Include in Token Scope: `On`
2. Configure **Mappers** for the new scope:
   - Add Mapper > **By Configuration** > **Group Membership**.
   - Name: `group-mapper`
   - **Token Claim Name**: `groups` (or `realm_access.roles` depending on app need).
   - Full group path: `Off` (optional, for simple names).
   - Add to ID/Access Token: `On`.
3. Assign to Client:
   - Go to **Clients** > Select your client > **Client Scopes**.
   - **Add client scope** > Select `groups` > Add as **Default** or **Optional**.

### 2. Social Login Integration

Configure external Identity Providers (IdP) for SSO.

#### Google (Standard OIDC)

1. **GCP Console**: Create OAuth2 Credentials.
   - Redirect URI: `https://keycloak.${DEFAULT_URL}/broker/google/endpoint`
2. **Keycloak**: Identity Providers > **Google**.
   - Client ID: `[From GCP]`
   - Client Secret: `[From GCP]`

#### Naver (Community OIDC)

Naver does not strictly follow standard OIDC discovery, so manual configuration
is needed using the "User-defined" provider.

1. **Naver Developers**: Create Application.
   - Callback URL: `https://keycloak.${DEFAULT_URL}/broker/naver/endpoint`
2. **Keycloak**: Identity Providers > **User-defined**.
   - **Alias**: `naver`
   - **Display Name**: `Naver Login`
   - **Endpoints**:
     - Authorization URL: `https://nid.naver.com/oauth2.0/authorize`
     - Token URL: `https://nid.naver.com/oauth2.0/token`
     - User Info URL: `https://openapi.naver.com/v1/nid/me`
   - **Client Config**:
     - Client ID: `[Client ID]`
     - Client Secret: `[Client Secret]`
     - Client Authentication: `Client secret sent as post`
   - **Scopes**: `profile email` (ensure these match Naver app permissions).

#### Kakao (Community OIDC)

1. **Kakao Developers**: Create App > Kakao Login.
   - Redirect URI: `https://keycloak.${DEFAULT_URL}/broker/kakao/endpoint`
2. **Keycloak**: Identity Providers > **User-defined**.
   - **Alias**: `kakao`
   - **Display Name**: `Kakao Login`
   - **Endpoints**:
     - Authorization URL: `https://kauth.kakao.com/oauth/authorize`
     - Token URL: `https://kauth.kakao.com/oauth/token`
     - User Info URL: `https://kapi.kakao.com/v2/user/me`
   - **Client Config**:
     - Client ID: `[REST API Key]`
     - Client Secret: `[Client Secret]` (if enabled in Kakao)
     - Client Authentication: `Client secret sent as post` (if secret enabled)
