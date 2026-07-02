---
status: active
---
<!-- Target: docs/90.references/data/learning/roadmap.md -->

# Reference: CS, CE & SE Self-Learning Roadmap (v2)

## Overview

This document is a roadmap reference for studying `hy-home.docker` infrastructure through CS, CE, and SE lenses. It connects slow-moving theory background with repo-local examples.

## Purpose

Provide stable learning background that operations and implementation documents can reference repeatedly.

## Repository Role

This reference is stable context that links Docker-based home infrastructure to learning topics. It does not replace operating procedures, implementation plans, task evidence, or runtime truth.

## Scope

### In Scope

- Theory-oriented learning map for Docker-based home infrastructure
- Links between CS/CE/SE topics and repo-local service tiers
- External paper, standard, and book links

### Out of Scope

- Real-time operating procedures
- Incident timelines or postmortems
- Secret values, credentials, or tokens
- Unverified copies of external release state, pricing, or support policy

## Definitions / Facts

- This document does not replace active policy or runbooks.
- Repo-local links are examples for learning. Runtime truth is owned by `infra/` and related validators.
- External links identify learning sources and must be rechecked before use in current decisions.
- Repository analysis entries are learning context from the 2026-04-02 snapshot. Recheck linked sources and validators before judging current runtime state or support scope.

## Source Rules

- Use repo-local examples as learning pointers, and verify runtime judgments in `infra/`, registry files, and validators.
- Use external paper, standard, and book links as sources for theoretical background.
- Do not treat mutable external facts such as release state, pricing, or support policy as live facts in this document.
- Do not use this roadmap as work instruction, an operations runbook, or an implementation plan.

## Reference Body

## 📝 Snapshot Notes

- **Infrastructure learning roadmap (v2)**: Summarizes learning connections for `hy-home.docker` infrastructure from the 2026-04-02 snapshot.
- **Distributed systems theory reinforcement**: Maps PostgreSQL (Patroni) to Raft consensus concepts and Kafka to distributed segment-log concepts.
- **Network virtualization theory addition**: Links the `infra_net` static IP allocation policy to L2/L3 network isolation concepts.
- **AI infrastructure deep dive**: Adds Qdrant HNSW indexing and Ollama hardware acceleration (CUDA/ROCm) learning context.

## 🔍 Repository Analysis Snapshot

- **Component overview**: In the 2026-04-02 snapshot, the [infra index](../../../../infra/README.md) provides gateway, identity, security, data, messaging, observability, workflow, AI, tooling, communication, and laboratory tiers as learning entrypoints.
- **Learning difficulty context**: This snapshot includes high-availability, event-streaming, vector-search, and local-inference examples such as the [Patroni/etcd PostgreSQL cluster](../../../../infra/04-data/relational/postgresql-cluster/README.md), [Kafka](../../../../infra/05-messaging/kafka/README.md), [Qdrant](../../../../infra/04-data/specialized/qdrant/README.md), and [Ollama](../../../../infra/08-ai/ollama/README.md).

---

## 🏛️ Tier 1: Computer Science (Theory)

Distributed systems, algorithms, and protocol design.

- **Distributed Consensus (Raft)**
  - **Theoretical root**: Algorithms for keeping state consistent in distributed environments despite network partitions or node failures, aligning with the CP side of CAP trade-offs.
  - **Repository connection**: **Patroni** and **etcd** in the [PostgreSQL cluster](../../../../infra/04-data/relational/postgresql-cluster/README.md).
  - **Learning objective**: Understand leader election and log replication, then analyze real failover behavior.

- **Log-Structured Merge Trees (LSM-Trees) vs Write-Ahead Logging (WAL)**
  - **Theoretical root**: Storage structures that maximize sequential write performance (LSM) and history recording that preserves transaction atomicity (WAL).
  - **Repository connection**: [Kafka](../../../../infra/05-messaging/kafka/README.md) and the [PostgreSQL cluster](../../../../infra/04-data/relational/postgresql-cluster/README.md).
  - **Learning objective**: Understand performance differences between Kafka segment-log design and RDBMS WAL-based transaction processing.

- **Vector Similarity Search (HNSW Algorithm)**
  - **Theoretical root**: Graph-based indexing algorithms for approximate nearest neighbor (ANN) search in high-dimensional vector spaces.
  - **Repository connection**: [Qdrant](../../../../infra/04-data/specialized/qdrant/README.md).
  - **Learning objective**: Study how hierarchical navigable small-world graph structures support near O(log N) search behavior at scale.

## 🚜 Tier 2: Computer Engineering (Hardware/OS)

Kernel, memory, virtualization, and network stack topics.

- **Kernel Resource Isolation (Linux Namespaces & Cgroups)**
  - **Technical root**: Kernel features that isolate the logical system view available to a process (namespaces) and control physical resource usage (cgroups).
  - **Repository connection**: `deploy.resources` settings in [common optimizations](../../../../infra/common-optimizations.yml) and Docker container isolation structure.
  - **Learning objective**: Analyze how containers provide isolated execution environments with lower overhead than virtual machines (VMs).

- **Network IPAM and Virtualization (Static IPs & Overlay Networks)**
  - **Technical root**: Traffic routing between virtual network interfaces and IP Address Management (IPAM) policy.
  - **Repository connection**: The [infra index](../../../../infra/README.md) and the isolated `infra_net` network in Compose files.
  - **Learning objective**: Learn static routing and IP management techniques for strengthening service-to-service communication security in Docker bridge networks.

- **Storage I/O and Persistence (Block Storage & WAL Layout)**
  - **Technical root**: Storage I/O optimization across operating-system filesystems and database layers.
  - **Repository connection**: Volume mount policy and data persistence layout in the [data tier](../../../../infra/04-data/README.md).
  - **Learning objective**: Analyze local volume mount performance benefits and the effect of synchronous writes (`fsync`) on database consistency.

## 🛠️ Tier 3: Software Engineering (Practice)

Design patterns, CI/CD, observability, and security.

- **Observability and SRE Golden Signals**
  - **Pattern root**: System health measurement through the four core signals: latency, traffic, errors, and saturation.
  - **Repository connection**: The **LGTM Stack** (Loki, Grafana, Tempo, Prometheus) in the [observability tier](../../../../infra/06-observability/README.md).
  - **Learning objective**: Understand modern monitoring that analyzes distributed traces (Tempo), logs (Loki), and metrics (Prometheus) through integrated dashboards.

- **Zero Trust and Centralized Authentication (OIDC/OAuth2)**
  - **Pattern root**: Architecture that verifies every request at the external gateway under a "never trust, always verify" principle.
  - **Repository connection**: [Keycloak](../../../../infra/02-auth/keycloak/README.md) and [OAuth2 Proxy](../../../../infra/02-auth/oauth2-proxy/README.md).
  - **Learning objective**: Explain the roles of Authorization Code Flow and PKCE in microservice authentication and authorization systems.

---

## 🏗️ Tier 4: Sandboxed Learning Exercises

This section is a learning-idea reference, not an implementation plan or task backlog. Every exercise is limited to throwaway sandboxes, synthetic data, and local-only sample configuration. Do not use live Docker sockets, existing Valkey/etcd cluster mutation, private PDFs, secrets, credentials, or tokens.

### Exercise 1: **Distributed Lock Concept Lab**

- **Goal**: Observe mutual exclusion and TTL-based lock expiry with a toy in-memory or disposable local service.
- **Theory**: Mutual exclusion and TTL-based lock-expiry strategies in distributed environments.

### Exercise 2: **Controller Loop Simulation**

- **Goal**: Practice control-loop thinking by reading a static fixture that imitates a container list and comparing desired state with observed state.
- **Theory**: Kubernetes reconciliation-loop principles.

### Exercise 3: **Vector Retrieval Thought Experiment**

- **Goal**: Explain retrieval, ranking, and answer-grounding flow with public toy text and fake embeddings.
- **Theory**: Retrieval-Augmented Generation architecture.

---

## 📚 Evidence and References

- **[Raft Paper]**: [https://raft.github.io/raft.pdf](https://raft.github.io/raft.pdf) - theoretical foundation for leader election patterns used by systems such as etcd and Patroni.
- **[HNSW Paper]**: [https://arxiv.org/abs/1603.09320](https://arxiv.org/abs/1603.09320) - academic basis for high-performance vector search algorithms used by systems such as Qdrant.
- **[OIDC Specs]**: [https://openid.net/developers/specs/](https://openid.net/developers/specs/) - modern authentication security standards.
- **[Google SRE Book]**: [https://sre.google/sre-book/monitoring-distributed-systems/](https://sre.google/sre-book/monitoring-distributed-systems/) - Golden Signals theory.

## 🪜 Deep-Dive Topics

- Routing and DNS patterns
- Kernel isolation techniques
- CAP, ACID, and distributed transactions
- Encryption and identity management
- Golden Signals and distributed tracing
- Vector search and RAG design
- EDA and Saga patterns

## Sources

- [infra index](../../../../infra/README.md) - tier overview and service entrypoints used for the repository-analysis snapshot
- [data tier](../../../../infra/04-data/README.md) - PostgreSQL, Qdrant, and data-tier learning examples
- [PostgreSQL cluster](../../../../infra/04-data/relational/postgresql-cluster/README.md) - Patroni/etcd learning example
- [Kafka](../../../../infra/05-messaging/kafka/README.md) - event streaming learning example
- [observability tier](../../../../infra/06-observability/README.md) - LGTM learning example
- [AI tier](../../../../infra/08-ai/README.md) - Ollama/Open WebUI learning context
- Linked external references already present in this document

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when infrastructure tiers, learning goals, or major reference sources change
- **Update Trigger**: Update when active infrastructure docs add or remove major systems that affect the learning map

## Related Documents

- [Learning reference index](./README.md)
- [90.references](../../README.md)
- [stable reference terms](../glossary/stable-reference-terms.md)
- [docs index](../../README.md)
