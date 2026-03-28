---
layer: infrastructure
title: "CS/CE Learning Roadmap: Infrastructure to Theory Mapping"
description: "A comprehensive learning roadmap mapping hy-home.docker infrastructure implementations to foundational Computer Science and Computer Engineering theories."
---

# CS/CE Learning Roadmap: Infrastructure to Theory Mapping

This document provides a deep-dive audit of the `hy-home.docker` infrastructure, mapping practical "Infrastructure" implementations to their foundational "Computer Science/Engineering Theory" roots.

The roadmap is structured across two dimensions:
1. **Theory Section**: Foundational CS/CE concepts linked to specific parts of the current infrastructure.
2. **Practical Section**: Step-by-step checklist of "Must-know" skills for a professional DevOps/Architect role.

---

## 1. Theory Section: Foundational CS/CE Mapping

This section connects the academic theories of Computer Science (CS) and Computer Engineering (CE) to the live services running in the `infra/` directory.

### 1.1 Networking
**Reference Implementations**: Gateway/VPC Setup (`infra/01-gateway/traefik`, `infra_net` docker networks, `k3d-hyhome`)
* **TCP/IP & OSI Model**: `docker-compose` networks (`infra_net`, `bridge`) implement Layer 2/3 switching and routing. Understanding subnets, CIDR, and packet encapsulation helps troubleshoot container communication.
* **DNS Resolution**: Traefik relies on precise DNS resolution to route requests. Concepts include DNS records (A, CNAME), TTLs, and internal service discovery (Docker embedded DNS).
* **SSL/TLS & Cryptography**: Traefik middleware and Cloudflared handle SSL/TLS termination. Essential concepts include public/private key pairs, certificates, handshakes, and symmetric vs. asymmetric encryption algorithms.
* **Load Balancing Algorithms**: Traefik and HAProxy (routing PostgreSQL) implement load balancing. CS concepts include Round Robin, Least Connections, and Consistent Hashing.

### 1.2 Operating Systems
**Reference Implementations**: Container Environment (`Docker`, `WSL2`, `containerd`, Unix Capabilities in `03-security/vault`)
* **Virtualization vs. Containerization**: Understanding hypervisors (WSL2/Hyper-V) vs. OS-level virtualization.
* **Namespaces and Cgroups**: Docker isolates processes using Linux Namespaces (PID, NET, MNT) and restricts resources using Control Groups (Cgroups). This relates directly to CE concepts of resource allocation and isolation.
* **Process Management & Signals**: How PID 1 operates inside a container. Ensuring graceful shutdowns requires understanding POSIX signals (`SIGTERM`, `SIGKILL`, `SIGINT`).
* **Privileges & Capabilities**: Vault configurations drop root but retain specific capabilities (e.g., `CAP_IPC_LOCK` to prevent swapping memory to disk, `SETUID`/`SETGID` for user switching).

### 1.3 Data Management & Distributed Systems
**Reference Implementations**: Highly Available Databases (`04-data/relational/postgresql-cluster`, `04-data/cache-and-kv/valkey-cluster`, `etcd`)
* **Distributed Consensus (Raft/Paxos)**: The PostgreSQL HA setup uses Patroni, which relies on `etcd`. `etcd` uses the Raft consensus algorithm to elect a leader and maintain a strongly consistent state across nodes.
* **Database Consistency Models (ACID vs. BASE)**:
  * **ACID**: PostgreSQL guarantees Atomicity, Consistency, Isolation, and Durability using Write-Ahead Logging (WAL) and MVCC (Multi-Version Concurrency Control).
  * **BASE**: Eventual consistency concepts seen in clustered caches and search systems.
* **CAP Theorem**: Understanding trade-offs. The `etcd` cluster prioritizes Consistency and Partition Tolerance (CP), ensuring split-brain scenarios do not corrupt data.
* **Data Structures (Indexing & B-Trees)**: SQL query performance relies on B-Tree and Hash indexes. Understanding the Big-O complexity of searching through these structures is critical for database tuning.

---

## 2. Practical Section: Engineering Mastery Checklist

For a DevOps Engineer or Solutions Architect, theory must translate into operational maturity. This section outlines the required engineering skills based on the active patterns in `hy-home.docker`.

### 2.1 Automation & GitOps (IaC)
**Context**: ArgoCD, Terraform (`09-tooling/terrakube`), Docker Compose orchestration.
- [ ] **Declarative Infrastructure**: Master the concept of declaring desired states rather than writing imperative scripts.
- [ ] **GitOps Workflows (ArgoCD)**: Understand the reconciliation loop pattern—automatically syncing a Git repository's infrastructure definitions (YAML/Helm) directly into a cluster state (`k3d`).
- [ ] **Idempotency**: Ensure that automation scripts and CI/CD pipelines can be run multiple times without causing divergent states or side effects.
- [ ] **Immutable Infrastructure**: Avoid SSHing into servers to make manual changes; instead, replace entire container images via the CI pipeline when configurations change.

### 2.2 Security Operations (SecOps)
**Context**: Secret Management (`03-security/vault`), Identity Access (`02-auth/keycloak`).
- [ ] **Dynamic Secrets (Vault)**: Move away from static credentials (`.env` files) to short-lived, dynamically generated PostgreSQL credentials managed by Vault.
- [ ] **Principle of Least Privilege (RBAC)**: Master Role-Based Access Control in both Kubernetes/K3d and Vault. Grant services only the explicit execution scopes they require.
- [ ] **Identity Federation (OIDC/SAML)**: Use Keycloak to broker authentication across services, centralizing identity rather than maintaining fragmented user tables.
- [ ] **Zero Trust Networks**: Assume the internal `infra_net` is hostile. Implement internal network policies and mTLS (mutual TLS) between microservices.

### 2.3 Scalability & Reliability (SRE)
**Context**: HAProxy for Postgres, Patroni cluster failovers, health checks.
- [ ] **High Availability (HA) Patterns**: Understand Active/Passive vs. Active/Active architectures. Learn how Patroni promotes a replica to leader seamlessly during an outage.
- [ ] **Connection Pooling (HAProxy/PgBouncer)**: Architect solutions gracefully handling connection limits. Scale application replicas without exhausting database connection threads.
- [ ] **Disaster Recovery (DR)**: Define RTO (Recovery Time Objective) and RPO (Recovery Point Objective). Master streaming replication and point-in-time recovery (PITR) using tools like WAL-G/pgBackRest.
- [ ] **Observability (LGTM Stack)**: Build dashboards monitoring RED metrics (Rate, Errors, Duration) via Prometheus and Grafana. Set up actionable alerting schemas.

---
*Generated by the Senior Solutions Architect / DevOps Expert via AI reasoning.*
