# Design System Storybook

## Overview

Hosts the static build of the Design System's Storybook documentation.

## Service Details

- **Image**: `your-registry/design-system-storybook:latest` (Custom/Placeholder image)
- **Container Name**: `mng-storybook`

## Network

Configured with **Dynamic IP** assignment on the `infra_net` network.

| Service | IP Address |
| :--- | :--- |
| `storybook` | Dynamic (DHCP) |

## Traefik Configuration

- **Domain**: `design.${DEFAULT_URL}`
- **Entrypoint**: `websecure` (TLS enabled)
- **Middleware**: `sso-auth@file` (Protected by Keycloak)
