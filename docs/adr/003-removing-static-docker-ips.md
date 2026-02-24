# 003: Removing Static Docker IPs

| Attribute | Detail |
| --- | --- |
| **Status** | Accepted |
| **Date** | 2026-02-23 |
| **Drivers** | Scalability, Predictability, Best Practices |

## Context and Problem Statement

The initial infrastructure composition designated static IPv4 addresses (e.g., `172.19.0.70`, `172.19.0.13`) for crucial containers via the centralized `infra_net` bridge network configuration (`subnet: 172.19.0.0/16`).
While static IPs simplified external routing in legacy designs, in modern Docker environments, hardcoding static IPs is an anti-pattern. It restricts the deployment to single instances, complicates teardowns/rebuilds, and risks IP collisions if multiple developers or automated testing suites (CI/CD) spin up the stack simultaneously.

## Decision

We will remove all explicit `ipv4_address` assignments across the `docker-compose.yml` topography.

Instead, we will rely exclusively on **Docker Internal DNS**. Services will communicate by addressing each other via their explicit `container_name` or defined `aliases` (e.g., `mng-pg:5432`). Detailed network bindings for each service are documented in the [Technical Context Hub](../context/README.md).

## Consequences

### Positive

- **Highly Portable**: The stack can be spun up multiple times on different subnets or parallel networks without modification.
- **Resilient**: Avoids network boot race conditions where an IP hasn't been released gracefully.

### Negative

- **DNS Exclusivity**: Ad-hoc commands or scripts that previously hardcoded these internal IPs will break and must be updated to target the DNS hostname.
