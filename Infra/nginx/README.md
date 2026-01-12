# Nginx

## Overview

A standalone Nginx instance, possibly serving as an entry point for specific static assets or legacy configurations.

## Service Details

- **Image**: `nginx:alpine`
- **Ports**:
  - HTTP: `${HTTP_HOST_PORT}:${HTTP_PORT}`
  - HTTPS: `${HTTPS_HOST_PORT}:${HTTPS_PORT}`
- **Configuration**: Mapped from `./config/nginx.conf`.
- **Network**: `infra_net` (Static IP: `172.19.0.13`)
- **Dependencies**: Waits for `minio` (suggests it might be proxying S3 content).
