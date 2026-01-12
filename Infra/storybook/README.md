# Design System Storybook

## Overview

Hosts the static build of the Design System's Storybook documentation.

## Service Details

- **Image**: `your-registry/design-system-storybook:latest` (Custom image)
- **Container Name**: `mng-storybook`

## Traefik Configuration

- **Domain**: `design.${DEFAULT_URL}`
- **Entrypoint**: `websecure` (TLS enabled)
- **Middleware**: `sso-auth@file` (Protected by Keycloak)
