# Nginx Gateway

Nginx acts as an optional, path-based reverse proxy or standalone gateway for specific sub-services.

## Services

| Service | Image            | Role              | Resources       | Port       |
| :------ | :--------------- | :---------------- | :-------------- | :--------- |
| `nginx` | `nginx:alpine`   | Lightweight Proxy | 0.2 CPU / 128MB | 80, 443    |

## Networking

- **Static IP**: `172.19.0.13` (Shares IP with Traefik, do not run concurrently).
- **Configuration**: Uses `config/nginx.conf` for routing rules.

## File Map

| Path               | Description                           |
| ------------------ | ------------------------------------- |
| `docker-compose.yml` | Nginx service and volume mounts.    |
| `config/`          | Virtual host and proxy configurations. |
| `README.md`        | Service overview and routing rules.   |
