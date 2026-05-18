---
status: archived
---

# Reference: CS, CE & SE Self-Learning Roadmap (v1)

## Overview (KR)

이 문서는 `hy-home.docker` 인프라 학습 로드맵의 초기 버전을 보존하는 reference 문서다. 현재 기준은 `roadmap.md`를 우선한다.

## Purpose

초기 학습 로드맵과 이후 로드맵 변화의 맥락을 보존한다.

## Repository Role

이 archived reference는 초기 학습 분류와 현재 roadmap의 변화 맥락을 비교하기 위한 history/context로 사용한다. 현재 학습 기준, 운영 절차, runtime truth를 대체하지 않는다.

## Scope

### In Scope

- 초기 CS/CE/SE 학습 주제
- 초기 repo-local infrastructure mapping
- 현재 roadmap과 비교할 수 있는 reference history

### Out of Scope

- active learning 기준의 SSoT
- 실시간 운영 절차
- incident timeline 또는 postmortem
- secret 값, credential, token

## Definitions / Facts

- 이 문서는 archived reference이며 active policy나 runbook을 대체하지 않는다.
- active learning roadmap은 `roadmap.md`다.
- 외부 링크는 archive 시점의 학습 출처이며, 현재 의사결정에 사용하기 전에는 다시 확인해야 한다.
- Repository analysis와 exercise 항목은 2026-03-30 snapshot history다. 현재 runtime 상태, 지원 범위, 운영 절차, 학습 기준으로 사용하지 않는다.

## Source Rules

- 이 문서는 archive history로만 사용하고 현재 학습 기준은 `roadmap.md`에서 확인한다.
- repo-local 예시는 초기 mapping context이며, runtime 판단은 `infra/`, registry 파일, validators에서 확인한다.
- 외부 논문과 표준 링크는 이론적 배경을 보존하기 위한 source다.
- release 상태, 가격, 지원 정책처럼 변하기 쉬운 외부 사실은 이 archived 문서에서 live fact로 주장하지 않는다.

## Reference Body

## 📝 Describe Changes

- **Initial Version**: Synthesized from the 2026-03-30 `hy-home.docker` infrastructure audit snapshot.
- **Consensus Focus**: Added Patroni/etcd (Raft) mapping to Distributed Systems theory.
- **AI Focus**: Added Qdrant (HNSW) mapping to Vector Search theory.
- **Hands-on**: Added "Custom Controller" and "Vector RAG" mini-projects.

## 🔍 Repository Analysis

Archived 2026-03-30 snapshot. Preserve this section as historical context only; use [active learning roadmap](./roadmap.md), [infra index](../../../infra/README.md), and validators for live interpretation.

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
- [infra index](../../../infra/README.md) - infrastructure entrypoint for verifying archived repo-state claims
- Linked external references already present in this document

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Archived; review only when links break or archive context becomes misleading
- **Update Trigger**: Update only for link repair or archive-context correction

## Related Documents

- [Learning reference index](./README.md)
- [Active learning roadmap](./roadmap.md)
- [90.references](../README.md)
- [stable reference terms](../glossary/stable-reference-terms.md)
- [docs index](../../README.md)
