# Keycloak IAM

## Services

| Service    | Image                            | Role                       | Resources         | Port       |
| :--------- | :------------------------------- | :------------------------- | :---------------- | :--------- |
| `keycloak` | `quay.io/keycloak/keycloak:26.5.4`| Identity & Access Management| 1.0 CPU / 1GB RAM | 8080 (Int) |

## Networking

Exposed via Traefik at `keycloak.${DEFAULT_URL}`.

| Port                         | Purpose                   |
| :--------------------------- | :------------------------ |
| `${KEYCLOAK_MANAGEMENT_PORT}`| Health checks & Metrics   |
| `8080`                       | Internal HTTP Traffic     |

## Persistence

Mounted from `${DEFAULT_AUTH_DIR}/keycloak/`:

- **Config**: `/opt/keycloak/conf`
- **Providers**: `/opt/keycloak/providers`
- **Themes**: `/opt/keycloak/themes`

## Configuration

### Key Variables

| Variable          | Description               | Default/Value                      |
| :---------------- | :------------------------ | :--------------------------------- |
| `KC_DB`           | Database Vendor           | `postgres`                         |
| `KC_DB_URL`       | Database JDBC URL         | `jdbc:postgresql://mng-db:5432/...`|
| `KEYCLOAK_ADMIN`  | Initial Admin User        | `${KEYCLOAK_ADMIN_USER}`           |
