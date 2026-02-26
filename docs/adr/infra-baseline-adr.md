# ADR: Architectural Decisions

## ADR-001: Root Orchestration with `include`

### Status

Accepted

### Context

Managing 30+ services in a single `docker-compose.yml` is unmaintainable and prone to merge conflicts.

### Decision

Utilize the Docker Compose `include` feature. The root `docker-compose.yml` SHALL serve as the registry, importing service-specific Compose files from `infra/`.

### Consequences

- **Positive**: Modular service management, cleaner diffs, isolated tiers.
- **Negative**: Requires Docker Compose v2.20+.

---

## ADR-002: Secrets-First Management

### Status

Accepted

### Context

Hardcoding seeds/passwords in `.env` leads to repository leakage and poor security posture.

### Decision

ALL sensitive credentials MUST be stored in `secrets/**/*.txt` and injected via Docker Secrets. `.env` is PROHIBITED for sensitive values.

### Consequences

- **Positive**: Hardened security, compatible with Swarm/K8s patterns.
- **Negative**: Requires manual file creation (automated via scripts).

---

## ADR-003: Spec-Driven Development (SDD)

### Status

Accepted

### Context

Ad-hoc infrastructure changes often lack documentation and verification.

### Decision

Implement "NO SPEC, NO CODE". Every change MUST have an approved specification in `specs/` before implementation.

### Consequences

- **Positive**: High traceability, documentation as code, reduced drift.
- **Negative**: Slightly slower delivery for trivial changes.

---

## ADR-004: Tiered Directory Structure

### Status

Accepted

### Context

Flat directory structures for service definitions become chaotic as the stack grows.

### Decision

Organize `infra/` using a 2-digit prefix (e.g., `01-gateway`) to enforce a logical dependency and layering order.

### Consequences

- **Positive**: Clear dependency hierarchy, intuitive navigation.
- **Negative**: Moving services requires updating root `include`.
