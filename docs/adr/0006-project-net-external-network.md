---
layer: infra
---
# ADR 0006: Project-Net External Network
n**Overview (KR):** 모든 서비스가 공유하는 외부 네트워크(`project_net`)를 정의하여 컨테이너 간 통신 표준을 수립합니다.

: External `project_net` Convention

- **Status:** Accepted
- **Date:** 2026-02-26
- **Authors:** Network Architect
- **Deciders:** Platform Team

## 1. Context and Problem Statement

Applications often reside in separate repositories from the core infrastructure. Hardcoding internal Docker bridge IPs is brittle, and exposing every database port to localhost leads to port collisions. We need a way for external projects to reliably reach shared infrastructure services.

## 2. Decision Drivers

- **Interoperability**: Easy bridging between infra and external apps without exposure.
- **Security**: Control which containers can "talk" to the infra network.
- **Simplicity**: Standardized DNS alias names across disconnected projects.

## 3. Decision Outcome

**Chosen option: "External `project_net` Bridge"**, because using a pre-existing Docker network with a consistent name allows external projects to connect to infrastructure services using stable DNS aliases without exposing them globally.

### 3.1 Core Engineering Pillars Alignment

- **Security**: Preserves isolation by avoiding “expose everything on localhost” and limiting cross-repo connectivity to a deliberate shared network.
- **Observability**: Prevents accidental access to internal observability backends by default (external apps must opt-in).
- **Compliance**: Provides a consistent, reviewable pattern for cross-repo integration (no ad-hoc port exposures).
- **Performance**: Avoids port-forward overhead and reduces host port collisions.
- **Documentation**: Standardizes external connectivity instructions across repos (one network name, DNS-based access).
- **Localization**: Not applicable (network convention).

### 3.2 Positive Consequences

- Unified discovery mechanism for all development tools.
- Dramatic reduction in host port conflicts.

### 3.3 Negative Consequences

- Requires the network to be manually created once on the host.

## 4. Alternatives Considered (Pros and Cons)

### Global Network (Infra_net)

Connect all external apps directly to the internal infra network.

- **Good**, because it is extremely simple.
- **Bad**, because it breaks isolation; external apps could see all internal metrics/logs backends.

## 5. Confidence Level & Technical Requirements

- **Confidence Rating**: High
- **Notes**: Common pattern for platform-as-a-service styles.
- **Technical Requirements Addressed**: REQ-PRD-AUT-FUN-03

## 6. Related Documents (Traceability)

- **Feature PRD**: [Infrastructure Automation PRD](../prd/2026-02-27-infra-automation-prd.md)
- **Feature Spec**: [Infrastructure Automation Spec](../specs/2026-02-27-infra-automation-spec.md)
- **Repository Blueprint**: [ARCHITECTURE.md](../../ARCHITECTURE.md)
