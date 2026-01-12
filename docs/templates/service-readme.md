# [Service Name]

## Overview

Brief description of the service and its role in the system.

## Service Details

- **Image**: `image:tag`
- **Port**: `Internal Port` (External Port if mapped)
- **Dependencies**: List of dependent services (e.g., PostgreSQL, Redis).

## Configuration

Key environment variables and configuration files.

| Variable | Description | Default |
| :--- | :--- | :--- |
| `VAR_NAME` | Description | `default` |

## Traefik Configuration

- **Domain**: `service.${DEFAULT_URL}`
- **Entrypoint**: `websecure`
- **Middleware**: List middlewares (e.g., `sso-auth`).

## Volumes

- `volume-name`: Purpose of persistence.
