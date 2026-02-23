# Infrastructure Resource Budgets Specification

**Identifier:** `SPEC-INFRA-01`
**Domain:** Resource Allocation & Performance
**Status:** Active

## Objective

Establish a deterministic mapping of memory and CPU constraints across the core `infra` ecosystem to prevent node starvation, Out-Of-Memory (OOM) kills, and CPU throttling affecting critical path workflows.

## Resource Profiles

All configurations defined in `deploy.resources.limits` and `reservations`.

### Tier 1: Critical Core (Unbounded reservations allowed)

*If these fail, the platform fails.*

| Component | Default CPU Limits | RAM Limit | RAM Reservation | Justification |
| :--- | :--- | :--- | :--- | :--- |
| PostgreSQL (pg-0/1/2) | 1.0 CPU | 2G | 1G | Memory intensive indexing |
| Traefik | 1.0 CPU | 1G | 512M | High I/O routing load |
| Keycloak | 1.5 CPU | 1.5G | 1G | Java JVM heap requirements |
| MinIO | 1.0 CPU | 1G | 512M | Foundation for logs/traces |

### Tier 2: State Handlers & Control Planes

*If these fail, secondary workflows degrade.*

| Component | Default CPU Limits | RAM Limit | RAM Reservation | Justification |
| :--- | :--- | :--- | :--- | :--- |
| Etcd (3x nodes) | 0.5 CPU | 256M | 128M | Patroni split-brain prevention |
| HAProxy (Pg-router) | 0.5 CPU | 256M | 128M | Fast forwarding of PG traffic |
| OAuth2-Proxy | 0.5 CPU | 256M | 128M | Middleware gatekeeper |

### Tier 3: Observability (Best Effort)

*If these fail, we lose visibility but maintain function.*

| Component | Default CPU Limits | RAM Limit | RAM Reservation | Justification |
| :--- | :--- | :--- | :--- | :--- |
| Prometheus | 2.0 CPU | 2G | 1G | High cardinality metrics |
| Loki | 1.0 CPU | 1G | 512M | Ingestion burst |
| Tempo | 1.0 CPU | 1G | 512M | Span buffering |
| Grafana | 0.5 CPU | 512M | 256M | Visualization |
| Alloy | 0.5 CPU | 512M | 256M | Log shipping buffering |

## Enforcement

Any Pull Request attempting to modify these thresholds by > 25% MUST include an Architecture Decision Record (ADR) justifying the memory/CPU expansion based on load or scaling patterns.
