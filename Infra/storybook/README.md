# Design System Storybook

## Overview

Hosts the static build of the Design System's Storybook documentation.

## Service Details

- **Image**: `storybook:latest` (Local build)
- **Container Name**: `design-system-storybook`

## Custom Build

This service is intended to be built from the local source code, as it hosts the documentation for *your* specific Design System.

The `Dockerfile` performs a multi-stage build:

1. **Build Stage**: Installs dependencies and runs `npm run build-storybook`.
2. **Production Stage**: Serves the static files using Nginx.

### How to use

1. Ensure your Design System source code is in this directory (or update the build context).
2. The `docker-compose.yml` includes a `build` section (commented out by default):

```yaml
services:
  storybook:
    build:
      context: .
      dockerfile: Dockerfile
```

1. Start the service: `docker-compose up -d --build storybook`.

## Network

Configured with **Dynamic IP** assignment on the `infra_net` network.

| Service | IP Address |
| :--- | :--- |
| `storybook` | Dynamic (DHCP) |

## Traefik Configuration

- **Domain**: `design.${DEFAULT_URL}`
- **Entrypoint**: `websecure` (TLS enabled)
- **Middleware**: `sso-auth@file` (Protected by Keycloak)
