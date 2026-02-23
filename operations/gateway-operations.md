# Gateway Operations Blueprint (Traefik)

> Standard operating procedures for the edge router proxy within `infra_net`.

## 1. Description

This document outlines the operational patterns for Traefik (`infra/01-gateway/traefik/docker-compose.yml`), acting as the main ingress controller for local infrastructure, bridging HTTP/HTTPS requests from the host to individual service containers.

## 2. Dynamic Configurations & Labels

Traefik relies extensively on Docker labels to route traffic effectively. If you are adding a new service, ensure you follow the standard label architecture:

- `traefik.enable=true`
- `traefik.http.routers.<service_name>.rule=Host('<service_name>.${DEFAULT_URL}')`
- `traefik.http.routers.<service_name>.entrypoints=websecure`
- `traefik.http.routers.<service_name>.tls=true`
- `traefik.http.services.<service_name>.loadbalancer.server.port=<port>`

**Config Reloads:**
Because the `/dynamic` directory and `docker.sock` are mounted as read-only (`ro`), Traefik handles file events seamlessly. If you modify file-based configurations in `./dynamic/`, Traefik automatically restarts its router configurations without restarting the container.

## 3. SSL/TLS Certificates

By default, the Traefik deployment heavily utilizes a local certificate generation system (such as `mkcert`).

- Volume Mount: `traefik_certs:/certs:ro`
- To rotate certificates or renew them, replace the files hosted on the Docker Engine volume map (`traefik_certs`) and send a soft reload command or restart the proxy container as a last resort.

## 4. Middleware & Auth Interception

Several core paths require SS0/OAuth2 middleware checks. If adding authentication, always add:

- `traefik.http.routers.<service_name>.middlewares=sso-auth@file`

Ensure that the middleware definition lives within `./dynamic/middlewares.yml`. If proxying to services issuing their own SSL (like OpenSearch), force HTTPS transport proxying:

- `traefik.http.services.<service>.loadbalancer.serversTransport=insecureTransport@file`

## 5. Routine Restarts

> [!CAUTION]
> Restarting Traefik briefly disconnects all incoming traffic streams since it routes the entire `infra_net`. Always notify developers or batch restarts during low-use windows.

```bash
docker compose -f infra/01-gateway/traefik/docker-compose.yml restart
```
