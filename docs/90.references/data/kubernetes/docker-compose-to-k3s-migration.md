---
status: active
---
<!-- Target: docs/90.references/data/kubernetes/docker-compose-to-k3s-migration.md -->

# Reference: Docker Compose to k3s/k3d Migration

## Overview

This document is a migration suitability snapshot for moving Docker Compose-based `hy-home.docker` infrastructure toward k3s/k3d-based Kubernetes environments. It is not an execution plan or an approved architecture decision; it preserves service-level suitability notes and decision criteria as reference context.

## Purpose

Provide a quick reference for Kubernetes migration discussions: which services are migration candidates, which criteria were used, and which follow-up decisions remain open.

## Repository Role

This reference is background material for migration planning. Current runtime truth stays in `infra/`, the root `docker-compose.yml`, and validation scripts. Real migration decisions must be promoted to an ARD/ADR, and execution order plus evidence must be recorded separately under `docs/04.execution/`.

## Scope

### In Scope

- Docker Compose to k3s/k3d migration evaluation criteria
- Service-tier migration suitability snapshot
- Staged migration direction
- Follow-up review questions

### Out of Scope

- Approved migration decision
- Active rollout plan or task evidence
- Kubernetes manifests, Helm charts, or Operator configuration source text
- Operations runbook or incident recovery procedure
- Secret values, credentials, tokens, or private keys

## Definitions / Facts

### Migration Evaluation Criteria

Service-level Kubernetes migration suitability is evaluated with these criteria.

1. **Orchestration benefit**: Does the service need autoscaling, self-healing, or rollout strategies?
2. **Ecosystem maturity**: Is there a mature Kubernetes Operator or Helm chart?
3. **Connectivity and integration**: Does the service need close integration with Kubernetes-native workloads?
4. **State management difficulty**: Can CSI-based data persistence be managed reliably?
5. **Operational complexity**: Does the migration make operations simpler than the current Docker Compose model?

### Tier 01-03: Gateway, Auth, Security

| Service | Migration Snapshot | Recommendation | Rationale |
| :--- | :--- | :--- | :--- |
| Traefik | Shim-retention candidate | Keep on Docker | It serves as the shared entrypoint for Docker and k3d, so its current position is stable until a full transition is accepted. |
| Keycloak | Migration candidate | Review Kubernetes HA deployment | Quarkus-based Keycloak fits Kubernetes operations and HA patterns. |
| Vault | Migration candidate | Review Kubernetes integration | Sidecar injection and the Kubernetes auth method may be useful. |

### Tier 04: Data

| Service | Migration Snapshot | Recommendation | Rationale |
| :--- | :--- | :--- | :--- |
| PostgreSQL / MongoDB | Lower priority | Keep on Docker or externalize | Database migration needs stable CSI/storage validation first. |
| Valkey / Redis | Lower priority | Keep on Docker | Docker can remain simpler for single-node operation. |
| MinIO | Migration candidate | Review StatefulSet deployment | It fits Kubernetes storage orchestration but depends on disk performance and CSI stability. |

### Tier 05-06: Messaging and Observability

| Service | Migration Snapshot | Recommendation | Rationale |
| :--- | :--- | :--- | :--- |
| Prometheus / Grafana | Higher-priority candidate | Review Kubernetes Operator path | They align well with standard Kubernetes monitoring paths. |
| Kafka / RabbitMQ | Migration candidate | Review Strimzi or Operator path | Operators may reduce complex broker operations. |
| Loki / Tempo | Higher-priority candidate | Review Kubernetes deployment | They integrate closely with Kubernetes log and trace collectors. |

### Tier 07-08: Workflow and AI

| Service | Migration Snapshot | Recommendation | Rationale |
| :--- | :--- | :--- | :--- |
| Airflow | Higher-priority candidate | Review Kubernetes Executor | Per-task pod execution can improve resource isolation and scalability. |
| n8n | Migration candidate | Review queue mode | Kubernetes resource management may help with larger workflow throughput. |
| Ollama / Open WebUI | Migration candidate | Review GPU orchestration | NVIDIA Device Plugin-based GPU scheduling may be relevant. |

### Migration Roadmap Snapshot

1. **Observability and workflow**: Review Prometheus, Grafana, Loki, Alloy, and Airflow first.
2. **Identity and messaging**: Evaluate Operator/HA transition cost for Keycloak, Kafka, and RabbitMQ.
3. **Security and AI hardware acceleration**: Evaluate security and GPU operation boundaries for Vault and Ollama.

### Open Questions

1. Can Kubernetes storage solutions such as Longhorn or OpenEBS be introduced reliably in the current host environment?
2. Should Traefik move fully to a Kubernetes Ingress Controller role, or remain as a Docker-side shim?
3. Can NVIDIA Container Toolkit and the GPU device plugin satisfy service requirements inside the k3d cluster?

## Source Rules

- Reconfirm current runtime state in `infra/` and the root `docker-compose.yml`.
- Create the relevant ARD/ADR and plan/task documents before turning migration judgment into execution.
- Recheck external chart, Operator, and vendor status at the time of use.
- This document does not replace active policy or runbooks.

## Sources

- [root README](../../../../README.md) - repository purpose, runtime entrypoints, validation gates
- [infra index](../../../../infra/README.md) - Compose tier and service entrypoints
- [docs index](../../../README.md) - stage taxonomy and migration routing
- [architecture index](../../../02.architecture/README.md) - target location for accepted migration architecture decisions
- [execution index](../../../04.execution/README.md) - target location for active migration plans and task evidence

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when Kubernetes migration work is actively proposed or when infra tier ownership changes
- **Update Trigger**: Update when a service migration decision is accepted, runtime topology changes, or storage/GPU assumptions change

## Related Documents

- [Kubernetes references](./README.md)
- [90.references](../../README.md)
- [docs index](../../../README.md)
- [architecture index](../../../02.architecture/README.md)
- [execution index](../../../04.execution/README.md)
- [operations index](../../../05.operations/README.md)
