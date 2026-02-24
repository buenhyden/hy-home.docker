# Infrastructure Lifecycle Operations

This document defines the lifecycle operations for managing the entire `infra` docker-compose stack.

## 1. Startup Order

While `docker-compose.yml` uses `#include` to load the stack, certain systems have strict dependencies. Services are chained using `depends_on`, but if you need to bring up the stack manually in phases:

1. **Security & Auth**: Keycloak must be up before Traefik can authenticate APIs. (`02-auth`)
2. **Data Tier**: MinIO and PostgreSQL must be up next. The observability stack depends critically on `minio` and auth. (`04-data`)
3. **Gateway**: Traefik must be up to route traffic. (`01-gateway`)
4. **Observability**: Finally, Grafana, Loki, and Prometheus come online. (`06-observability`)

To launch the entire stack:

```bash
docker compose -f docker-compose.yml --profile default up -d
```

## 2. Graceful Shutdown

To ensure WAL logs in PostgreSQL are flushed and Loki flushes log chunks to MinIO:

```bash
docker compose -f docker-compose.yml stop
```

Wait at least 30 seconds for containers to cleanly exit before issuing a `down` command.

## 3. Updating Images

To update specific images without downtime (except for the affected service):

1. Modify the image tag in the specific `docker-compose.yml` file.
2. Run:

```bash
docker compose -f docker-compose.yml pull <service_name>
docker compose -f docker-compose.yml up -d --no-deps --build <service_name>
```

## 4. Recovering from Docker Network Issues

Occasionally, `infra_net` might conflict with host routes.

1. `docker network rm infra_net`
2. Update the subnet inside `docker-compose.yml` `ipam` settings.
3. Bring the stack back up. This requires an IP refresh for static IPs defined in sub-compose files.
