---
status: superseded
---
<!-- Target: docs/90.references/data/learning/roadmap-v1.md -->

# Reference: CS, CE & SE Self-Learning Roadmap (v1)

## Overview

This reference preserves the initial version of the `hy-home.docker` infrastructure learning roadmap. The current baseline is `roadmap.md`.

## Purpose

Preserve context for the initial learning roadmap and later roadmap changes.

## Repository Role

This archived reference is history/context for comparing the initial learning categories with changes in the current roadmap. It does not replace current learning criteria, operations procedures, or runtime truth.

## Scope

### In Scope

- Initial CS/CE/SE learning topics
- Initial repo-local infrastructure mapping
- Reference history that can be compared with the current roadmap

### Out of Scope

- SSoT for active learning criteria
- live operations procedures
- incident timeline or postmortem
- secret values, credentials, tokens

## Definitions / Facts

- This document is an archived reference and does not replace active policy or runbooks.
- The active learning roadmap is `roadmap.md`.
- External links are learning sources from the archive point and must be rechecked before current decisions.
- Repository analysis and exercise items are 2026-03-30 snapshot history. Do not use them as current runtime state, support scope, operations procedures, or learning criteria.

## Source Rules

- Use this document only as archive history and check current learning criteria in `roadmap.md`.
- Repo-local examples are initial mapping context; runtime decisions are checked in `infra/`, registry files, and validators.
- External paper and standard links are sources for preserving theoretical background.
- Volatile external facts such as release status, pricing, and support policy are not asserted as live facts in this archived document.

## Reference Body

## 📝 Describe Changes

- **Initial Version**: Synthesized from the 2026-03-30 `hy-home.docker` infrastructure audit snapshot.
- **Consensus Focus**: Added Patroni/etcd (Raft) mapping to Distributed Systems theory.
- **AI Focus**: Added Qdrant (HNSW) mapping to Vector Search theory.
- **Hands-on**: Added "Custom Controller" and "Vector RAG" mini-projects.

## 🔍 Repository Analysis

Archived 2026-03-30 snapshot. Preserve this section as historical context only; use [active learning roadmap](./roadmap.md), [infra index](../../../../infra/README.md), and validators for live interpretation.

- **Component Overview Snapshot**: A multi-tiered Docker-based private cloud infrastructure covering Gateway, Auth, Database Clusters, Messaging, and AI services.
- **Learning Complexity Snapshot**: The archived analysis mapped Patroni, Valkey Cluster, Qdrant, and Ollama to intermediate-to-architect learning topics. It is not a live maturity rating.

---

## 🏛️ Tier 1: Computer Science (Theory)

Distributed Systems, Algorithms, and Protocols.

- **Topic Name**: **Distributed Consensus (Raft/Paxos)**
  - **Conceptual Root**: Distributed systems require a way to agree on shared state despite network partitions or failures (CAP Theorem).
  - **Repo Connection**: See **Patroni** and **etcd** in `infra/04-data/relational/postgresql-cluster/`.
  - **Learning Objective**: Master how nodes elect a leader and maintain a consistent write-ahead log.

- **Topic Name**: **Vector Space Modeling & Similarity Search**
  - **Conceptual Root**: Representing unstructured data as multi-dimensional vectors and searching for semantic neighbors using graph algorithms.
  - **Repo Connection**: See **Qdrant** in `infra/04-data/specialized/qdrant/`.
  - **Learning Objective**: Master the **HNSW (Hierarchical Navigable Small World)** indexing algorithm.

- **Topic Name**: **Authentication & Identity Protocols**
  - **Conceptual Root**: Stateless identity verification using JSON Web Tokens (JWT) and social federation via OIDC/SAML.
  - **Repo Connection**: See **Keycloak** in `infra/02-auth/keycloak/`.
  - **Learning Objective**: Master the OAuth2 Authorization Code Flow with PKCE.

## 🚜 Tier 2: Computer Engineering (Hardware/OS)

Kernel, Memory, Virtualization, and Network stack.

- **Topic Name**: **Kernel Resource Isolation (Namespaces/Cgroups)**
  - **Technical Root**: The OS kernel provides logical isolation of processes' view of the system (Namespaces) and physical resource limits (Cgroups).
  - **Repo Connection**: See the `docker-compose.yml` and `common-optimizations.yml` mapping CPU and memory limits.
  - **Learning Objective**: Master how Linux sandboxes processes and prevents resource starvation.

- **Topic Name**: **Storage I/O & Persistent State**
  - **Technical Root**: The interaction between block storage, file systems, and database write-ahead logging (WAL).
  - **Repo Connection**: See the PostgreSQL/Valkey persistence mounts in `infra/04-data/`.
  - **Learning Objective**: Master the trade-offs between local volume mounting and network-attached storage performance.

## 🛠️ Tier 3: Software Engineering (Practice)

Patterns, CI/CD, Observability, and Security.

- **Topic Name**: **Observability & SRE Golden Signals**
  - **Pattern Root**: Measuring system health through Latency, Traffic, Errors, and Saturation.
  - **Repo Connection**: See the **Prometheus** and **Grafana** stack in `infra/06-observability/`.
  - **Learning Objective**: Master how to build alerting rules that separate "signal" from "noise".

- **Topic Name**: **Secret Management & Zero Trust**
  - **Pattern Root**: Centralized, encrypted storage of sensitive values that are dynamically injected into services.
  - **Repo Connection**: See **HashiCorp Vault** in `infra/03-security/vault/`.
  - **Learning Objective**: Master the AppRole authentication method and rotation patterns.

---

## 🏗️ Tier 4: Archived Sandboxed Learning Exercises

Archived exercise ideas. These are not implementation tasks, operations runbooks, or backlog items. If reused for learning, keep them in throwaway sandbox environments with synthetic data only. Do not use live Docker sockets, mutate existing Valkey/etcd clusters, or any private PDFs, secrets, credentials, tokens.

### Exercise 1: **Custom Controller Simulation**

- **Objective**: Study reconciliation loops with static fixtures that model desired and observed container state.
- **Theory**: Control Loop theory used in Kubernetes and automation brokers.

### Exercise 2: **Distributed Lock Concept Lab**

- **Objective**: Study mutual exclusion and lease expiry with a toy in-memory or disposable local service.
- **Theory**: Mutual Exclusion in distributed environments.

### Exercise 3: **Vector Retrieval Thought Experiment**

- **Objective**: Study retrieval and answer grounding with public toy text and fake embeddings.
- **Theory**: Retrieval-Augmented Generation (RAG) architecture.

---

## 📚 Evidence & References

- **[Raft Paper]**: [https://raft.github.io/raft.pdf](https://raft.github.io/raft.pdf) - Theoretical foundation for etcd and Patroni leadership election.
- **[HNSW Paper]**: [https://arxiv.org/abs/1603.09320](https://arxiv.org/abs/1603.09320) - Algorithmic basis for Qdrant's high-performance search.
- **[OIDC Specs]**: [https://openid.net/developers/specs/](https://openid.net/developers/specs/) - Standard foundation for Keycloak security.

## 🪜 Deep-Dive Topics

- Routing/DNS patterns
- Kernel isolation
- CAP/ACID/Distributed Transactions
- Cryptography/Vaults/RBAC
- Golden Signals/OpenTelemetry
- Vector Search/RAG
- EDA/Saga/At-Least-Once Delivery

## Sources

- [Active learning roadmap](./roadmap.md) - active learning roadmap reference
- [infra index](../../../../infra/README.md) - infrastructure entrypoint for verifying archived repo-state claims
- Linked external references already present in this document

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Archived; review only when links break or archive context becomes misleading
- **Update Trigger**: Update only for link repair or archive-context correction

## Related Documents

- [Learning reference index](./README.md)
- [Active learning roadmap](./roadmap.md)
- [90.references](../../README.md)
- [stable reference terms](../glossary/stable-reference-terms.md)
- [docs index](../../README.md)
