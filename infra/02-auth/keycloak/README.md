# Keycloak IAM

## Services

| Service    | Image / Build                              | Role                       | Resources         | Port       |
| :--------- | :----------------------------------------- | :------------------------- | :---------------- | :--------- |
| `keycloak` | `quay.io/keycloak/keycloak:26.5.4` (base) → custom `Dockerfile` build | Identity & Access Management | 1.0 CPU / 1GB RAM | 8080 (Int) |

## Networking

Exposed via Traefik at `keycloak.${DEFAULT_URL}`.

| Port                         | Purpose                   |
| :--------------------------- | :------------------------ |
| `${KEYCLOAK_MANAGEMENT_PORT}`| Health checks & Metrics   |
| `8080`                       | Internal HTTP Traffic     |

## Persistence

Mounted from `${DEFAULT_AUTH_DIR}/keycloak/`:

- **Config**: `/opt/keycloak/conf` (Static configuration)
- **Providers**: `/opt/keycloak/providers` (Custom JARs/SPIs)
- **Themes**: `/opt/keycloak/themes` (Custom UI themes)

## Operations

### Health Verification

Keycloak exposes a dedicated management interface for health checks.

```bash
# Verify readiness (Quarkus health extension)
docker exec keycloak curl -f http://localhost:9000/health/ready
```

### Key Configuration

| Variable                      | Description                   | Default/Value                        |
| :---------------------------- | :---------------------------- | :----------------------------------- |
| `KC_DB`                       | Database vendor               | `postgres`                           |
| `KC_DB_URL`                   | Database JDBC URL             | `jdbc:postgresql://mng-pg:5432/...`  |
| `KC_BOOTSTRAP_ADMIN_USERNAME` | Initial admin username        | `${KEYCLOAK_ADMIN_USER}`             |
| `KC_BOOTSTRAP_ADMIN_PASSWORD` | Initial admin password        | Read from `keycloak_admin_password` secret |
| `KC_DB_PASSWORD`              | Database password             | Read from `keycloak_db_password` secret |

## Documentation References

- **Setup Guide**: [auth-procedural.md](../../../docs/guides/02-auth/auth-procedural.md)
- **System Context**: [auth-context.md](../../../docs/guides/02-auth/auth-context.md)
- **Recovery**: [2026-03-15-auth-lockout.md](../../../docs/runbooks/2026-03-15-auth-lockout.md)
- **Customization**: [keycloak-customization.md](../../../docs/guides/02-auth/keycloak-customization.md)
