# Spec: Infrastructure Hardening and Optimization (SPEC-001)

## 1. Objective

Define the technical implementation details for hardening and optimizing the Docker Compose infrastructure.

## 2. Standards Compliance

- **[REQ-RSK-01]**: High-risk changes (Gateway/Vault) must have rollback verification.
- **[REQ-NET-01]**: All services MUST use the `infra_net` for internal communication.

## 3. Template Definitions (x-config)

We will define global templates in the root `docker-compose.yml`:

```yaml
x-security-hardened: &security-hardened
  security_opt:
    - no-new-privileges:true
  cap_drop:
    - ALL

x-logging-loki: &logging-loki
  driver: loki
  options:
    loki-url: "http://loki:3100/loki/api/v1/push"
    loki-external-labels: "job=infra,container={{.Name}}"
```

## 4. Service-Specific Hardening

### Gateway (Traefik)

- `read_only: true`
- Mount `/tmp` as tmpfs if needed.

### Database (PostgreSQL/Redis)

- Explicit resource limits (e.g., memory reservation 256M, limit 1G).
- Non-root user in container.

## 5. Verification Plan [REQ-SPT-10]

- **AC-1**: Execute `docker inspect` to verify `CapDrop` contains `ALL`.
- **AC-2**: Query Loki API for recent labels; verify all `infra/` services are present.
- **AC-3**: Monitor `docker stats` during peak load to verify limits are respected.
