# Nginx Gateway

Nginx acts as an optional, path-based reverse proxy or standalone gateway for specific sub-services.

## Services

| Service | Image            | Role              | Resources       | Profile  |
| :------ | :--------------- | :---------------- | :-------------- | :------- |
| `nginx` | `nginx:alpine`   | Lightweight Proxy | 0.5 CPU / 512MB | `nginx`  |

| Host Port | Internal Port | Protocol | Shared with Traefik? |
| :-------- | :------------ | :------- | :------------------- |
| `80`      | `80`          | HTTP     | Yes (Conflict)       |
| `443`     | `443`         | HTTPS    | Yes (Conflict)       |

- **Config**: Mounts `./config/nginx.conf` for fine-grained routing.
- **Traffic**: Redirects all HTTP traffic to HTTPS via TLS.

## Persistence

- **Certs**: `nginx_certs` volume mapped to `${DEFAULT_DOCKER_PROJECT_PATH}/secrets/certs`.

| Path                 | Role                                   |
| :------------------- | :------------------------------------- |
| `docker-compose.yml` | Resource limits (template-infra-low).  |
| `config/nginx.conf`  | Virtual hosts / SSO / Proxy definitions. |

## Routing Patterns

| Path Endpoint      | Upstream Service | Feature           |
| :----------------- | :--------------- | :---------------- |
| `/oauth2/`         | `oauth2-proxy`   | Auth Provider     |
| `/keycloak/`       | `keycloak`       | Identity Server   |
| `/minio/`          | `minio`          | Object Storage    |
| `/minio-console/`  | `minio-console`  | Console Admin UI  |
