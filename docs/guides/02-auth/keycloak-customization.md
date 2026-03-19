# Keycloak Customization and Build Optimizations

This guide documents the customization and build-time optimization strategy for Keycloak in the `hy-home.docker` environment.

## Build-time vs. Runtime Configuration

Keycloak 26.x (Quarkus-based) distinguishes between build-time and runtime configurations. Optimizing the build significantly reduces container startup time and memory footprint.

### Key Build Arguments (Dockerfile)

The local `infra/02-auth/keycloak/Dockerfile` uses the following optimized build-time settings:

| Argument | Value | Description |
| :--- | :--- | :--- |
| `KC_HEALTH_ENABLED` | `true` | Enables health check endpoints. |
| `KC_METRICS_ENABLED` | `true` | Enables Prometheus metrics endpoints. |
| `KC_DB` | `postgres` | Sets the database vendor at build time. |
| `KC_FEATURES` | `token-exchange,scripts` | Enables specific optional features. |

### Build Process

The `docker-compose.yml` is configured to build the image locally:

```yaml
services:
  keycloak:
    build:
      context: .
      dockerfile: Dockerfile
```

This triggers the multi-stage build in the `Dockerfile` which runs `bin/kc.sh build` to create an optimized server image.

## Custom Themes and Providers

To add custom themes or JAR providers:
1. **Themes**: Place theme folders in `infra/02-auth/keycloak/themes/`. Update the `Dockerfile` to copy this directory:
```dockerfile
COPY themes/ /opt/keycloak/themes/
```
2. **Providers**: Place `.jar` files in `infra/02-auth/keycloak/providers/`. Update the `Dockerfile`:
```dockerfile
COPY providers/ /opt/keycloak/providers/
RUN /opt/keycloak/bin/kc.sh build
```

## Development SSL Wrapper

For development convenience, the `Dockerfile` includes a generation step for a self-signed certificate if not provided. This allows Keycloak to start in `https` mode even without a full production certificate chain in local environments.

> [!IMPORTANT]
> Always verify the `docker compose build keycloak` output after changing build arguments or adding providers.
