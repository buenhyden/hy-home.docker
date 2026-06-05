---
status: active
---
<!-- Target: docs/90.references/learning/roadmap.md -->

# Reference: CS, CE & SE Self-Learning Roadmap (v2)

## Overview

이 문서는 `hy-home.docker` 인프라를 CS, CE, SE 관점으로 학습하기 위한 로드맵 참고 문서다. 느리게 변하는 이론 배경과 repo-local 예시를 연결한다.

## Purpose

운영 문서와 구현 문서가 반복해서 참고할 수 있는 안정적인 학습 배경을 제공한다.

## Repository Role

이 reference는 Docker 기반 홈 인프라를 학습 주제와 연결하는 stable context로 사용한다. 운영 절차, 구현 계획, task evidence, runtime truth를 대체하지 않는다.

## Scope

### In Scope

- Docker 기반 홈 인프라의 이론 학습 지도
- CS/CE/SE 주제와 repo-local service tier의 연결
- 외부 논문, 표준, 책 링크

### Out of Scope

- 실시간 운영 절차
- incident timeline 또는 postmortem
- secret 값, credential, token
- 외부 릴리스 상태, 가격, 지원 정책의 무검증 복사본

## Definitions / Facts

- 이 문서는 active policy나 runbook을 대체하지 않는다.
- repo-local 연결은 학습을 돕기 위한 예시이며, runtime truth는 `infra/`와 관련 validators가 담당한다.
- 외부 링크는 학습 출처를 가리키며, 현재 의사결정에 사용하기 전에는 다시 확인해야 한다.
- Repository analysis 항목은 2026-04-02 snapshot 기준 학습 맥락이다. 현재 runtime 상태나 지원 범위를 판단할 때는 linked source와 validators를 다시 확인한다.

## Source Rules

- repo-local 예시는 학습 연결을 위한 pointer로 사용하고, runtime 판단은 `infra/`, registry 파일, validators에서 확인한다.
- 외부 논문, 표준, 책 링크는 이론적 배경을 뒷받침하는 source로 사용한다.
- release 상태, 가격, 지원 정책처럼 변하기 쉬운 외부 사실은 이 문서에서 live fact로 주장하지 않는다.
- 이 roadmap을 작업 지시, 운영 runbook, implementation plan으로 사용하지 않는다.

## Reference Body

## 📝 Snapshot Notes

- **인프라 학습 로드맵 (v2)**: 2026-04-02 snapshot 기준 `hy-home.docker` 인프라의 학습 연결을 정리.
- **분산 시스템 이론 강화**: PostgreSQL(Patroni)의 Raft 합의 알고리즘과 Kafka의 분산 세그먼트 로그 이론 매핑.
- **네트워크 가상화 이론 추가**: `infra_net`의 정적 IP 할당 정책과 L2/L3 네트워크 격리 이론 연결.
- **AI 인프라 심층 분석**: Qdrant의 HNSW 인덱싱 및 Ollama의 하드웨어 가속(CUDA/ROCm) 이론 추가.

## 🔍 Repository Analysis Snapshot

- **컴포넌트 개요**: 2026-04-02 snapshot 기준으로 [infra index](../../../infra/README.md)는 gateway, identity, security, data, messaging, observability, workflow, AI, tooling, communication, laboratory tier를 학습 entrypoint로 제공한다.
- **학습 난이도 맥락**: 이 snapshot은 [Patroni/etcd PostgreSQL cluster](../../../infra/04-data/relational/postgresql-cluster/README.md), [Kafka](../../../infra/05-messaging/kafka/README.md), [Qdrant](../../../infra/04-data/specialized/qdrant/README.md), [Ollama](../../../infra/08-ai/ollama/README.md) 같은 고가용성, event streaming, vector search, local inference 예시를 포함한다.

---

## 🏛️ Tier 1: Computer Science (이론)

분산 시스템, 알고리즘 및 프로토콜 설계.

- **분산 합의 알고리즘 (Distributed Consensus - Raft)**
  - **이론적 뿌리**: 분산 환경에서 네트워크 파티션이나 노드 장애에도 불구하고 상태를 일관되게 유지하기 위한 알고리즘(CAP 정리의 CP 모델).
  - **저장소 연결**: [PostgreSQL cluster](../../../infra/04-data/relational/postgresql-cluster/README.md)의 **Patroni**와 **etcd**.
  - **학습 목표**: 리더 선출(Leader Election)과 로그 복제(Log Replication)의 원리를 이해하고 실제 장애 조치(Failover) 프로세스를 분석합니다.

- **로그 구조 머지 트리 (LSM-Trees) vs Write-Ahead Logging (WAL)**
  - **이론적 뿌리**: 순차적 쓰기 성능을 극대화하기 위한 저장 구조(LSM)와 트랜잭션 원자성을 보장하기 위한 이력 기록(WAL).
  - **저장소 연결**: [Kafka](../../../infra/05-messaging/kafka/README.md)와 [PostgreSQL cluster](../../../infra/04-data/relational/postgresql-cluster/README.md).
  - **학습 목표**: Kafka의 세그먼트 로그 기반 설계와 RDBMS의 WAL 기반 트랜잭션 처리의 성능 차이를 이해합니다.

- **벡터 유사도 검색 (HNSW Algorithm)**
  - **이론적 뿌리**: 고차원 벡터 공간에서 근사 근접 이웃(Approximate Nearest Neighbor, ANN)을 찾기 위한 그래프 기반 인덱싱 알고리즘.
  - **저장소 연결**: [Qdrant](../../../infra/04-data/specialized/qdrant/README.md).
  - **학습 목표**: 다중 계층 그래프(Hierarchical Navigable Small World) 구조가 대규모 데이터에서 어떻게 O(log N) 수준의 검색 속도를 보장하는지 학습합니다.

## 🚜 Tier 2: Computer Engineering (하드웨어/OS)

커널, 메모리, 가상화 및 네트워크 스택.

- **커널 자원 격리 (Linux Namespaces & Cgroups)**
  - **기술적 뿌리**: 프로세스가 시스템을 바라보는 논리적 뷰를 격리(Namespaces)하고, 물리적 자원 사용량을 제어(Cgroups)하는 커널 기능.
  - **저장소 연결**: [common optimizations](../../../infra/common-optimizations.yml)의 `deploy.resources` 설정 및 Docker 컨테이너 격리 구조.
  - **학습 목표**: 컨테이너가 가상 머신(VM)과 달리 어떻게 시스템 오버헤드를 최소화하면서 독립적인 실행 환경을 가지는지 분석합니다.

- **네트워크 IPAM 및 가상화 (Static IPs & Overlay Networks)**
  - **기술적 뿌리**: 가상 네트워크 인터페이스 간의 트래픽 라우팅과 IP 주소 관리(IP Address Management) 정책.
  - **저장소 연결**: [infra index](../../../infra/README.md)와 Compose files의 `infra_net` 격리 네트워크.
  - **학습 목표**: Docker 브리지 네트워크 내에서 서비스 간 통신 보안을 강화하기 위한 정적 라우팅 및 IP 관리 기법을 익힙니다.

- **스토리지 I/O 및 영속성 (Block Storage & WAL Layout)**
  - **기술적 뿌리**: 운영체제의 파일 시스템과 데이터베이스 레이어 간의 스토리지 입출력 최적화.
  - **저장소 연결**: [data tier](../../../infra/04-data/README.md)의 볼륨 마운트 정책 및 데이터 영속화 레이아웃.
  - **학습 목표**: 로컬 볼륨 마운트의 성능 이점과 동기적 쓰기(Fsync)가 데이터베이스 일관성에 미치는 영향을 분석합니다.

## 🛠️ Tier 3: Software Engineering (실무)

디자인 패턴, CI/CD, 관측 가능성 및 보안.

- **관측 가능성 및 SRE Golden Signals**
  - **패턴 뿌리**: Latency, Traffic, Errors, Saturation 네 가지 핵심 지표를 통한 시스템 건전성 측정.
  - **저장소 연결**: [observability tier](../../../infra/06-observability/README.md)의 **LGTM Stack** (Loki, Grafana, Tempo, Prometheus).
  - **학습 목표**: 분산 트레이싱(Tempo)과 로그(Loki), 메트릭(Prometheus)을 하나의 대시보드에서 통합 분석하는 현대적 모니터링 체계를 이해합니다.

- **Zero Trust 및 중앙 집중식 인증 (OIDC/OAuth2)**
  - **패턴 뿌리**: "결코 신뢰하지 말고 항상 검증하라"는 원칙하에 외부 게이트웨이에서 모든 요청의 신원을 확인하는 아키텍처.
  - **저장소 연결**: [Keycloak](../../../infra/02-auth/keycloak/README.md)과 [OAuth2 Proxy](../../../infra/02-auth/oauth2-proxy/README.md).
  - **학습 목표**: Authorization Code Flow와 PKCE가 마이크로서비스 인증 및 인가 체계에서 맡는 역할을 설명할 수 있게 한다.

---

## 🏗️ Tier 4: Sandboxed Learning Exercises

이 섹션은 implementation plan이나 task backlog가 아니라 학습 아이디어 reference다. 모든 exercise는 throwaway sandbox, synthetic data, local-only sample config로 제한한다. live Docker socket, 기존 Valkey/etcd cluster mutation, private PDFs, secrets, credentials, tokens를 사용하지 않는다.

### Exercise 1: **Distributed Lock Concept Lab**

- **목표**: toy in-memory or disposable local service로 mutual exclusion과 TTL-based lock expiry를 관찰한다.
- **이론**: 분산 환경에서의 상호 배제 및 TTL 기반 락 만료 전략.

### Exercise 2: **Controller Loop Simulation**

- **목표**: container 목록을 모사한 static fixture를 읽고 desired state와 observed state를 비교하는 control-loop 사고방식을 연습한다.
- **이론**: Kubernetes의 조정(Reconciliation) 루프 원리.

### Exercise 3: **Vector Retrieval Thought Experiment**

- **목표**: public toy text와 fake embeddings로 retrieval, ranking, answer grounding의 흐름을 설명한다.
- **이론**: 검색 증강 생성(Retrieval-Augmented Generation) 아키텍처.

---

## 📚 증거 및 참고 문헌 (Evidence & References)

- **[Raft Paper]**: [https://raft.github.io/raft.pdf](https://raft.github.io/raft.pdf) - etcd 및 Patroni의 리더 선출 이론적 기초.
- **[HNSW Paper]**: [https://arxiv.org/abs/1603.09320](https://arxiv.org/abs/1603.09320) - Qdrant 고성능 검색 알고리즘의 학술적 근거.
- **[OIDC Specs]**: [https://openid.net/developers/specs/](https://openid.net/developers/specs/) - 현대적 인증 보안 표준.
- **[Google SRE Book]**: [https://sre.google/sre-book/monitoring-distributed-systems/](https://sre.google/sre-book/monitoring-distributed-systems/) - Golden Signals 이론.

## 🪜 심층 분석 주제 (Deep-Dive Topics)

- 라우팅 및 DNS 패턴
- 커널 격리 기술
- CAP/ACID/분산 트랜잭션
- 암호화 및 신원 관리
- Golden Signals 및 분산 트레이싱
- 벡터 검색 및 RAG 설계
- EDA 및 Saga 패턴

## Sources

- [infra index](../../../infra/README.md) - tier overview and service entrypoints used for the repository-analysis snapshot
- [data tier](../../../infra/04-data/README.md) - PostgreSQL, Qdrant, and data-tier learning examples
- [PostgreSQL cluster](../../../infra/04-data/relational/postgresql-cluster/README.md) - Patroni/etcd learning example
- [Kafka](../../../infra/05-messaging/kafka/README.md) - event streaming learning example
- [observability tier](../../../infra/06-observability/README.md) - LGTM learning example
- [AI tier](../../../infra/08-ai/README.md) - Ollama/Open WebUI learning context
- Linked external references already present in this document

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when infrastructure tiers, learning goals, or major reference sources change
- **Update Trigger**: Update when active infrastructure docs add or remove major systems that affect the learning map

## Related Documents

- [Learning reference index](./README.md)
- [90.references](../README.md)
- [stable reference terms](../glossary/stable-reference-terms.md)
- [docs index](../../README.md)
