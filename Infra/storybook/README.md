# Design System Storybook

## Overview

Hosts the static build of the Design System's Storybook documentation. This service is a **Custom Build** requiring source code (provided in `react-ts` or `react-js` examples).

## Services

| Service | Image | Role |
| :--- | :--- | :--- |
| `storybook` | `design-system-storybook:latest` (Local Build) | Documentation Host (Nginx) |

## Networking

Service runs on `infra_net` using **Dynamic** IP assignment.

| Service | IP Address | Internal Port | Traefik Domain |
| :--- | :--- | :--- | :--- |
| `storybook` | *(Dynamic)* | `80` | `design.${DEFAULT_URL}` |

## Persistence

This service is stateless. Documentation is baked into the Docker image during build.

## Configuration

Configuration is primarily handled via `docker-compose.yml` labels and the `Dockerfile` build process.

## Traefik Integration

Services are exposed via Traefik with TLS and SSO authentication.

- **Domain**: `design.${DEFAULT_URL}`
- **Middleware**: `sso-auth@file` (Keycloak Protected)

## Usage

1. **Select Context**: Navigate to `react-ts` (recommended) or `react-js`.
2. **Build & Run**:

   ```bash
   cd react-ts
   docker-compose up -d --build
   ```

3. **Access**: Navigate to `https://design.${DEFAULT_URL}`.
