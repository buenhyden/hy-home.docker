# Phase 2 ADR: Decisions on Automation & Integration

## ADR-005: Sidecar-Driven Resource Initialization

### Status

Accepted

### Context

Manual bucket creation or database initialization is error-prone and prevents "immutable infra" patterns.

### Decision

Adopt the `init-container` (sidecar) pattern in Docker Compose. A one-off container SHALL run mc/sql commands against the core service.

---

## ADR-006: External `project_net` Convention

### Status

Accepted

### Context

Apps and Infra often reside in separate repositories. Hardcoding internal IP addresses is brittle.

### Decision

Use a standard external network named `project_net`. All infra services needing app integration MUST join this network with a known alias.

---

## ADR-007: Mandatory Resource Limiting (Reservations)

### Status

Accepted

### Context

Local machines can experience "thrashing" when containers consume all CPU/RAM during startup.

### Decision

Standardize `deploy.resources.reservations`. Every service MUST define a floor for memory to prevent over-allocation.
