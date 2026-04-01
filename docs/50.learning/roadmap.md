# 🎓 Self-Learning Guide: CS, CE & SE Roadmap (v2)

## 📝 변경 사항 요약 (Describe Changes)

- **인프라 통합 가이드 (v2)**: 2026-04-02 기준 `hy-home.docker` 인프라의 최신 상태를 반영.
- **분산 시스템 이론 강화**: PostgreSQL(Patroni)의 Raft 합의 알고리즘과 Kafka의 분산 세그먼트 로그 이론 매핑.
- **네트워크 가상화 이론 추가**: `infra_net`의 정적 IP 할당 정책과 L2/L3 네트워크 격리 이론 연결.
- **AI 인프라 심층 분석**: Qdrant의 HNSW 인덱싱 및 Ollama의 하드웨어 가속(CUDA/ROCm) 이론 추가.

## 🔍 저장소 분석 (Repository Analysis)

- **컴포넌트 개요**: Gateway, Auth, Database Cluster, Messaging, Observability, AI Tier 등 총 11개 레이어로 구성된 Docker 기반 프라이빗 클라우드 인프라.
- **현재 복잡도 레벨**: **Architect (아키텍트)**. Patroni, etcd, Kafka Cluster 등 고가용성(HA) 패턴과 벡터 데이터베이스, LLM 추론 엔진 등 고급 AI 인프라가 통합되어 있음.

---

## 🏛️ Tier 1: Computer Science (이론)

분산 시스템, 알고리즘 및 프로토콜 설계.

- **분산 합의 알고리즘 (Distributed Consensus - Raft)**
  - **이론적 뿌리**: 분산 환경에서 네트워크 파티션이나 노드 장애에도 불구하고 상태를 일관되게 유지하기 위한 알고리즘(CAP 정리의 CP 모델).
  - **저장소 연결**: `infra/04-data/relational/postgresql-cluster/`의 **Patroni**와 **etcd**.
  - **학습 목표**: 리더 선출(Leader Election)과 로그 복제(Log Replication)의 원리를 이해하고 실제 장애 조치(Failover) 프로세스를 분석합니다.

- **로그 구조 머지 트리 (LSM-Trees) vs Write-Ahead Logging (WAL)**
  - **이론적 뿌리**: 순차적 쓰기 성능을 극대화하기 위한 저장 구조(LSM)와 트랜잭션 원자성을 보장하기 위한 이력 기록(WAL).
  - **저장소 연결**: **Kafka** (`infra/05-messaging/kafka/`) vs **PostgreSQL** (`infra/04-data/relational/postgresql-cluster/`).
  - **학습 목표**: Kafka의 세그먼트 로그 기반 설계와 RDBMS의 WAL 기반 트랜잭션 처리의 성능 차이를 이해합니다.

- **벡터 유사도 검색 (HNSW Algorithm)**
  - **이론적 뿌리**: 고차원 벡터 공간에서 근사 근접 이웃(Approximate Nearest Neighbor, ANN)을 찾기 위한 그래프 기반 인덱싱 알고리즘.
  - **저장소 연결**: `infra/04-data/specialized/qdrant/`의 **Qdrant**.
  - **학습 목표**: 다중 계층 그래프(Hierarchical Navigable Small World) 구조가 대규모 데이터에서 어떻게 O(log N) 수준의 검색 속도를 보장하는지 학습합니다.

## 🚜 Tier 2: Computer Engineering (하드웨어/OS)

커널, 메모리, 가상화 및 네트워크 스택.

- **커널 자원 격리 (Linux Namespaces & Cgroups)**
  - **기술적 뿌리**: 프로세스가 시스템을 바라보는 논리적 뷰를 격리(Namespaces)하고, 물리적 자원 사용량을 제어(Cgroups)하는 커널 기능.
  - **저장소 연결**: `infra/common-optimizations.yml`의 `deploy.resources` 설정 및 Docker 컨테이너 격리 구조.
  - **학습 목표**: 컨테이너가 가상 머신(VM)과 달리 어떻게 시스템 오버헤드를 최소화하면서 독립적인 실행 환경을 가지는지 분석합니다.

- **네트워크 IPAM 및 가상화 (Static IPs & Overlay Networks)**
  - **기술적 뿌리**: 가상 네트워크 인터페이스 간의 트래픽 라우팅과 IP 주소 관리(IP Address Management) 정책.
  - **저장소 연결**: `infra_net` 설정을 통한 서비스별 고정 IP 할당 (`172.19.0.0/16`).
  - **학습 목표**: Docker 브리지 네트워크 내에서 서비스 간 통신 보안을 강화하기 위한 정적 라우팅 및 IP 관리 기법을 익힙니다.

- **스토리지 I/O 및 영속성 (Block Storage & WAL Layout)**
  - **기술적 뿌리**: 운영체제의 파일 시스템과 데이터베이스 레이어 간의 스토리지 입출력 최적화.
  - **저장소 연결**: `infra/04-data/` 내의 볼륨 마운트 정책 및 데이터 영속화 레이아웃.
  - **학습 목표**: 로컬 볼륨 마운트의 성능 이점과 동기적 쓰기(Fsync)가 데이터베이스 일관성에 미치는 영향을 분석합니다.

## 🛠️ Tier 3: Software Engineering (실무)

디자인 패턴, CI/CD, 관측 가능성 및 보안.

- **관측 가능성 및 SRE Golden Signals**
  - **패턴 뿌리**: Latency, Traffic, Errors, Saturation 네 가지 핵심 지표를 통한 시스템 건전성 측정.
  - **저장소 연결**: `infra/06-observability/`의 **LGTM Stack** (Loki, Grafana, Tempo, Mimir).
  - **학습 목표**: 분산 트레이싱(Tempo)과 로그(Loki), 메트릭(Prometheus)을 하나의 대시보드에서 통합 분석하는 현대적 모니터링 체계를 구축합니다.

- **Zero Trust 및 중앙 집중식 인증 (OIDC/OAuth2)**
  - **패턴 뿌리**: "결코 신뢰하지 말고 항상 검증하라"는 원칙하에 외부 게이트웨이에서 모든 요청의 신원을 확인하는 아키텍처.
  - **저장소 연결**: **Keycloak** (`infra/02-auth/keycloak/`)과 **OAuth2-Proxy**.
  - **학습 목표**: Authorization Code Flow와 PKCE를 활용하여 마이크로서비스 간 안전한 인증 및 인가 체계를 구현합니다.

---

## 🏗️ Tier 4: Hands-on Mini-Projects (실습)

코드로 증명하는 학습 단계.

### Project 1: **Distributed Lock Service 구현**

- **목표**: **Valkey** (Redis) 또는 **etcd** 클러스터를 활용하여 여러 컨테이너 간에 공유되는 자원에 대해 상호 배제(Mutual Exclusion)를 보장하는 잠금 서비스를 Python으로 구현합니다.
- **이론**: 분산 환경에서의 상호 배제 및 TTL 기반 락 만료 전략.

### Project 2: **Custom Docker Controller 제작**

- **목표**: Docker SDK를 사용하여 특정 라벨이 붙은 컨테이너의 상태를 모니터링하고, 장애 발생 시 자동으로 알림을 보내거나 재시작하는 제어 루프(Control Loop)를 작성합니다.
- **이론**: Kubernetes의 조정(Reconciliation) 루프 원리.

### Project 3: **End-to-End Vector RAG 파이프라인**

- **목표**: PDF 문서를 텍스트로 추출하여 **Ollama** 에지 추론 엔진으로 임베딩을 생성하고, 이를 **Qdrant**에 저장한 뒤 자연어 질문에 답변하는 CLI 도구를 만듭니다.
- **이론**: 검색 증강 생성(Retrieval-Augmented Generation) 아키텍처.

---

## 📚 증거 및 참고 문헌 (Evidence & References)

- **[Raft Paper]**: [https://raft.github.io/raft.pdf](https://raft.github.io/raft.pdf) - etcd 및 Patroni의 리더 선출 이론적 기초.
- **[HNSW Paper]**: [https://arxiv.org/abs/1603.09320](https://arxiv.org/abs/1603.09320) - Qdrant 고성능 검색 알고리즘의 학술적 근거.
- **[OIDC Specs]**: [https://openid.net/developers/specs/](https://openid.net/developers/specs/) - 현대적 인증 보안 표준.
- **[Google SRE Book]**: [https://sre.google/sre-book/monitoring-distributed-systems/](https://sre.google/sre-book/monitoring-distributed-systems/) - Golden Signals 이론.

## 🪜 심층 분석 링크 (Deep-Dive Links)

- [01-network/theory.md](../../.agent/skills/self-learning-guide/references/01-network/theory.md): 라우팅 및 DNS 패턴
- [02-os-virtualization/theory.md](../../.agent/skills/self-learning-guide/references/02-os-virtualization/theory.md): 커널 격리 기술
- [03-data-management/theory.md](../../.agent/skills/self-learning-guide/references/03-data-management/theory.md): CAP/ACID/분산 트랜잭션
- [04-security-identity/theory.md](../../.agent/skills/self-learning-guide/references/04-security-identity/theory.md): 암호화 및 신원 관리
- [05-observability/theory.md](../../.agent/skills/self-learning-guide/references/05-observability/theory.md): Golden Signals 및 분산 트레이싱
- [06-ai-infrastructure/theory.md](../../.agent/skills/self-learning-guide/references/06-ai-infrastructure/theory.md): 벡터 검색 및 RAG 설계
- [07-distributed-messaging/theory.md](../../.agent/skills/self-learning-guide/references/07-distributed-messaging/theory.md): EDA 및 Saga 패턴
