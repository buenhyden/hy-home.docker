# 🎓 Self-Learning Guide: CS, CE & SE Roadmap (v1)

## 📝 Describe Changes

- **Initial Version**: Synthesized from the current `hy-home.docker` infrastructure audit (2026-03-30).
- **Consensus Focus**: Added Patroni/etcd (Raft) mapping to Distributed Systems theory.
- **AI Focus**: Added Qdrant (HNSW) mapping to Vector Search theory.
- **Hands-on**: Added "Custom Controller" and "Vector RAG" mini-projects.

## 🔍 Repository Analysis

- **Component Overview**: A multi-tiered Docker-based private cloud infrastructure covering Gateway, Auth, Database Clusters, Messaging, and AI services.
- **Current Complexity Level**: **Intermediate to Architect**. The stack uses production-grade cluster patterns (Patroni, Valkey Cluster) and advanced AI infrastructure (Qdrant, Ollama).

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
  - **Pattern Root**: Centralized, encrypted storage of credentials that are dynamically injected into services.
  - **Repo Connection**: See **HashiCorp Vault** in `infra/03-security/vault/`.
  - **Learning Objective**: Master the AppRole authentication method and secret rotation.

---

## 🏗️ Tier 4: Hands-on Mini-Projects (Implementation)

Verified learning through coding.

### Project 1: **Custom Controller Implementation**

- **Objective**: Build a simple reconciliation loop in Python or Go that monitors the Docker API and automatically performs an action (e.g., tagging resources or cleaning dangling volumes).
- **Theory**: Control Loop theory used in Kubernetes and automation brokers.

### Project 2: **Distributed Lock Service**

- **Objective**: Using the existing **Valkey** or **etcd** cluster, implement a service that prevents concurrent execution of a specific task across multiple containers.
- **Theory**: Mutual Exclusion in distributed environments.

### Project 3: **Vector RAG Pipeline Builder**

- **Objective**: Create a script that picks a directory of PDF files, converts them to embeddings using **Ollama**, stores them in **Qdrant**, and allows querying through a simple CLI.
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

## Related Documents

- [Learning reference index](README.md)
- [90.references](../README.md)

---

## Overview (KR)

이 문서는 `docs/90.references/learning/roadmap-v1.md`에 대한 참고 문서다. 느리게 변하는 기준 정보와 관련 출처를 정리한다.

## Purpose

운영 문서와 구현 문서가 참고할 수 있는 안정적인 배경 정보를 제공한다.

## Scope

- 포함: 용어, 기준, roadmap, 외부 또는 repo-local 참고 정보
- 제외: 실시간 운영 절차, incident timeline, secret 값

## Definitions / Facts

- 이 문서는 active policy나 runbook을 대체하지 않는다.
- 변경 시 관련 stage 문서의 링크를 함께 확인한다.

## Sources

- Repository-local docs and README files
- Linked references already present in this document
