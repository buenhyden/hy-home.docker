# Nginx Gateway

Nginx acts as an optional, path-based reverse proxy or standalone gateway for specific sub-services.

## Services

| Service | Image            | Role              | Resources       | Profile  |
| :------ | :--------------- | :---------------- | :-------------- | :------- |
| `nginx` | `nginx:alpine`   | Lightweight Proxy | 0.5 CPU / 512MB | `nginx`  |

## Networking

- **Static IP**: `172.19.0.13` (Shares IP with Traefik, do not run concurrently).
- **Ports**: `${HTTP_HOST_PORT}:${HTTP_PORT}`, `${HTTPS_HOST_PORT}:${HTTPS_PORT}`.
- **Configuration**: Uses `./config/nginx.conf` for routing rules.

## Persistence

- **Certs**: `nginx_certs` volume mapped to `${DEFAULT_DOCKER_PATH}/secrets/certs`.

## File Map

| Path               | Description                           |
| ------------------ | ------------------------------------- |
| `docker-compose.yml` | Nginx service and volume mounts.    |
| `config/`          | Virtual host and proxy configurations. |
| `README.md`        | Service overview and routing rules.   |
