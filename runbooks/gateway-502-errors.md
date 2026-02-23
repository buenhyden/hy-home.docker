# Incident Runbook: Traefik 502 Bad Gateway

**Issue:** End users or internal microservices receive `HTTP 502 Bad Gateway` when hitting Traefik routes.

## Definition

A 502 error from Traefik strictly implies that Traefik successfully captured the request, successfully evaluated the router rules, but the target application container is unreachable or refusing connections.

## Resolution Steps

### 1. Identify the Failing Route

Open the Traefik dashboard (usually at `https://dashboard.local.dev`) and navigate to the HTTP Routers section. Identify which router is failing.

Alternatively, review Traefik access logs:

```bash
docker logs --tail 100 traefik | grep "502"
```

### 2. Check the Target Container

 Traefik routes dynamically via Docker labels. Inspect the target container.

```bash
docker ps | grep <target_service>
docker logs <target_service>
```

If the container is in a `restarting` loop, fix the application error.

### 3. Validate Network Bridges

Ensure the target container is legitimately present on the `infra_net` (or the network Traefik shares).

```bash
docker network inspect infra_net
```

Ensure the target container's IPv4 address matches Traefik's expectations, or if dynamic, ensure the container name resolves.

### 4. Check Internal Port Binding

Make sure the label `traefik.http.services.<name>.loadbalancer.server.port` matches the port the container is *actually* listening on internally, NOT the host-mapped port.

Example: If a container listens on `8080` internally, but exposed to host as `9090`:

- **Correct label:** `...loadbalancer.server.port=8080`
