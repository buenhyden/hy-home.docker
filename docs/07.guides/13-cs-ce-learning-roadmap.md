# 13-CS-CE-Learning-Roadmap

## 1. Overview (KR)
본 문서는 `hy-home.docker` 인프라스트럭처의 실제 구현 사례를 바탕으로 작성된 **"컴퓨터 공학(CS) 및 컴퓨터 엔지니어링(CE) 학습 로드맵 및 실무 마스터리 가이드"**입니다. 추상적인 학술 이론(네트워킹, OS, 데이터 스토어)이 어떻게 프로덕션 환경(Gateway, Docker, PostgreSQL 등)의 설계에 적용되었는지를 매핑하여, 시니어 엔지니어 및 솔루션 아키텍트로 성장하기 위한 체계적인 학습 경로와 필수 실무 역량 체크리스트를 제공합니다.

## 2. 문서 목적 (Document Purpose)
* **이론과 실무의 가교(Bridge)**: 단순히 도구(Tool)의 사용법을 익히는 것을 넘어, 해당 인프라가 동작하는 기반 원리(CS/CE Theory)를 이해합니다.
* **시니어 역량 강화**: 시스템의 'Why(왜 이렇게 설계되었는가)'를 파악하여, 장애 복구 시 근본 원인(Root Cause)을 도출해내고 확장 가능한 아키텍처를 설계하는 능력을 배양합니다.

## 3. 대상 독자 및 활용법 (Audience and Usage)
* **대상**: 주니어/미들급 클라우드 엔지니어, DevOps 엔지니어, 솔루션 아키텍트 지망생
* **활용법**: 각 인프라 컴포넌트를 운영/트러블슈팅할 때 매핑된 핵심 CS/CE 이론을 먼저 선행 학습하며, 실무 챕터의 평가 체크리스트를 통해 본인의 역량 달성도를 점검하는 지표로 활용합니다.

## 4. 인프라 기반 CS/CE 이론 매핑 (Theory Section)

### 4.1 네트워킹 및 트래픽 라우팅 (Networking)
**관련 인프라**: `01-gateway` (Traefik/Nginx), VPC 네트워크 설계 공간
* **OSI 7계층 구조 (L4 vs. L7)**: Traefik이 어플리케이션(L7) 계층에서 패킷의 헤더(Host, Path)를 분석하여 라우팅하는 반면, TCP/UDP 단순 포워딩은 전송(L4) 계층에서 처리되는 원리를 이해합니다.
* **TCP/IP 통신 및 DNS 분해**: TCP 3-Way Handshake 프로세스, TCP 연결 고갈(TIME_WAIT) 문제 해결 프로세스, 클러스터 내부에서의 DNS Record (A, CNAME) 해석 흐름.
* **보안 통신 구조 (SSL/TLS)**: 대칭키/비대칭키 혼합 암호화 수학적 원리, Certificate Authority(CA) 신뢰망, TLS 핸드셰이크 프로토콜 최적화 방식.
* **로드 밸런싱 동적 알고리즘**: 라운드 로빈(Round Robin), 최소 연결(Least Connections), 일관된 해싱(Consistent Hashing) 이론이 역방향 프록시(Reverse Proxy) 시스템 내에서 어떻게 트래픽 분산과 세션 스티키니스(Sticky Session)를 달성하는지 파악.

### 4.2 운영체제 구조 및 격리 기술 (Operating Systems)
**관련 인프라**: 핵심 도커 엔진 및 WSL2 백엔드 호스트 구동계
* **컴퓨트 모델링 (프로세스와 스레드)**: 운영체제 레벨에서 도커 컨테이너는 별개의 VM이 아니라 커널을 공유하는 경량화된 프로세스 그룹(Process Tree)에 불과하다는 핵심 원리 인지.
* **격리 기술 메커니즘 (Linux Namespaces)**: 패킷 격리를 위한 `net`, 프로세스 격리를 위한 `pid`, 파일시스템 격리를 위한 `mnt` 네임스페이스의 원조와 동작 흐름.
* **시스템 자원 제어 로직 (Cgroups)**: 컨테이너별 메모리 할당, OOM Killer 우선순위 할당, CPU 쿼터 셰어링이 운영체제 스케줄러(CFS) 레벨을 통해 강제되는 구조.
* **파일 시스템 스태킹 (Storage Drivers)**: OverlayFS 구조체를 기반으로 한 Copy-on-Write 메커니즘과 Docker Image 레이어(Layer) 재사용 효율화 정리.

### 4.3 분산 데이터 관리 및 저장소 튜닝 (Data Management)
**관련 인프라**: `04-data` (PostgreSQL 관계형, Valkey/Redis 인메모리, MinIO 객체 스토리지)
* **네트워크 분산 시스템 정리 (CAP & PACELC Theorem)**: PostgreSQL High-Availability(HA) 환경에서의 데이터 일관성(Consistency)과 Valkey 클러스터 캐시의 파티션 허용 및 가용성(Availability) 간의 시스템 트레이드오프 분석.
* **ACID vs BASE 패러다임**: RDBMS 엔진의 엄격한 트랜잭션 무결성과, 분산형 인메모리 엔진이 채택하는 Eventual Consistency (결과적 일관성) 모델 비교.
* **데이터 구조 및 인덱싱 (Indexing)**: 디스크 I/O 최적화를 이뤄내기 위한 B-Tree 트리 구조 삽입 정렬, 해시 인덱스의 공간적 할당.
* **인메모리 캐싱 전략 (Caching Theory)**: Least Recently Used (LRU), Least Frequently Used (LFU) 캐시 퇴출 알고리즘 원리와 Write-through vs Cache-aside 어플리케이션 계층 레이어 튜닝 전략.

## 5. 시니어 엔지니어링 실무 마스터리 (Practical Section)

### 5.1 인프라 시스템 자동화 패턴 (Automation & GitOps)
**관련 인프라**: `07-workflow` (ArgoCD 및 Airflow 파이프라인)
* **Declarative (선언형) vs Imperative (명령형) 관리 패러다임**: 상태를 명시적으로 코딩하고 선언하는 인프라 코드 관리 기법의 강력함 체화.
* **컨트롤러 피드백 루프 (Reconciliation Loop)**: Git 저장소에 서술된 Desired State(이상적 목적 상태)와 클러스터가 동작하고 있는 Actual State(현장 실제 상태)의 괴리(Drift)를 지속 감시하고 일치시키는 ArgoCD 자동화 조정 루프.
* **멱등성 설계 (Idempotency)**: 100번을 재실행하여도 의도치 않은 패널티 시스템 복제나 오류 없이 동일한 설정 상태를 보장하도록 자동화 셋트 템플릿화 능력.

### 5.2 보안 정책 및 식별 접근 체계 (Security & Identity)
**관련 인프라**: `02-auth` (Keycloak), `03-security` (Vault/KMS)
* **탈중앙화 및 제로 트러스트 기조 (Zero Trust Architecture)**: 신뢰할 수 있는 구역(VPN 내부)이라는 경계 기반 보안 사상을 탈피하여, API 간 직접 트래픽마다의 상호 인증 도입 체계.
* **아이덴티티 연합 및 위임 (Identity Federation)**: OIDC/SAML2.0 규칙을 이용한 토큰 기반 중앙 집중 및 위임형 인증 관문(Keycloak) 통합 통제.
* **비밀값 생애주기 관리 (Secret Lifecycle Dynamics)**: 하드코딩 환경 변수를 전면 금지하고, HashiCorp Vault와 같은 암호화 엔진 상에서 동적(Tokenization)으로 자격 증명 풀(Database TLS Credentials 등)을 주입/로테이션 시키고 폐기(Revocation)하는 파이프라인.
* **최소 권한의 원칙 강화 (Principle of Least Privilege)**: 주체(Identities)에 가장 제한된 권한만 부여하는 역할 기반 모델(RBAC, Role-Based Access Control)을 토대로 IAM 관리 정책 고도화.

### 5.3 아키텍처 확장성 및 신뢰도 확보 (Scalability & Reliability)
**관련 인프라**: 클러스터 통합 아키텍쳐 플랫폼 및 `06-observability` 텔레메트리 (Prometheus/Grafana)
* **High-Availability (고가용성) 페일오버 토폴로지**: 리더 선출(Leader Election) 합의 알고리즘 기반 스플릿 브레인(Split-Brain) 증후군 방지 절차와 복제(Replication) 전략.
* **무상태(Stateless) 인스턴스 전가**: 증설과 폐기가 빠른 속도로 발생되는 백엔드 인스턴스에서 세션, 인증 로그 등의 State를 분리해 공유 캐시 레이어(Valkey)로 저장시키는 수평 확장 체계(Horizontal Scaling).
* **풀스택 시인성 및 피드백 지표 (Observability Metrics)**: 단순 리소스 모니터링을 넘어 시스템 병목을 측정하는 4대 황금 신호 (Latency-지연 시간, Traffic-트래픽 부하율, Errors-장애 에러율, Saturation-리소트 포화도) 정의와 SRE형 슬랙 자동화 Pager 구축.

## 6. 역량 평가 체크리스트 (Proficiency Checklist)
수준별 역량 스텝을 통해 본인의 성장 단계를 평가 및 목표 설정할 수 있습니다.

- [ ] **Level 100 (Foundational Engineer)**
   - [ ] Gateway 프록시의 OSI 7계층 별 책임성을 정확히 분리하여 TCP 소켓 로그를 디버그할 수 있다.
   - [ ] 도커 컨테이너가 가상머신(VM)과 근본적으로 어떻게 다른지(Namespaces & Cgroups 관점) 설명하고 커널 파라미터를 식별할 수 있다.
   - [ ] Git 기반의 환경 설정 변경 플로우(IaC)를 따를 수 있으며 인프라 명령어를 직접 실행하는 것을 지양한다.

- [ ] **Level 200 (Intermediate Architect)**
   - [ ] RDBMS B-Tree Indexing 구조 동작 원리와 분산형 Key-Value 인덱스 파티셔닝 전략을 트래픽 성향(Read/Write)에 맞춰 선택 튜닝할 수 있다.
   - [ ] SSL/TLS 인증서 발급과 갱신(Renewal) 라이프사이클 과정을 Traefik Gateway Let's Encrypt를 동원하여 완벽히 무중단 자동화 세팅할 수 있다.
   - [ ] Vault를 연동하여 어플리케이션 Pod 시작 시 실시간으로 발급된 비밀번호가 Secret으로 주입되는 프로비져닝 과정을 설계할 수 있다.

- [ ] **Level 300 (Senior / Principal Solutions Architect)**
   - [ ] 상태 비보존(Stateless) 파이프라인 속에서 클러스터 노드 파티셔닝 현상(Split-Brain) 조치 시 합의 기반 리더(Leader) 선출 원리를 조율 디버깅할 수 있다.
   - [ ] 분산 시스템 환경에서의 CAP 정리 이론을 바탕으로 비즈니스 목표에 맞춘 데이터 일관성 한계치 및 캐싱 퇴거 전략을 능동적으로 계산/튜닝할 수 기 있다.
   - [ ] ArgoCD(GitOps) 프로세스를 심화 반영하여, 수십 개의 통합 인프라 및 마이크로서비스 리볼빙 시 멱등성을 절대 보증하는 점진 개발(Blue-Green / Canary) 배포 프로토콜을 아키텍팅할 수 있다.

## 7. 관련 인프라 문서 (Related Infrastructure Docs)
- [Gateway Overview](../../infra/01-gateway/README.md)
- [Keycloak & Oauth2 Auth](../../infra/02-auth/README.md)
- [Vault Security Setup](../../infra/03-security/README.md)
- [Data Tier Matrix](../../infra/04-data/README.md)
- [Workflow & ArgoCD GitOps](../../infra/07-workflow/README.md)

## 8. 참고 문헌 (References)
- *Designing Data-Intensive Applications* (Martin Kleppmann): 분산 스토어 한계점, 일관성 및 노드 데이터 매핑 (Theory 4.3 Reference)
- *Kubernetes Patterns* (Bilgin Ibryam): 인프라 아키텍팅 멱등성 보장 및 확장성 패턴 (Theory 5.1 & 5.3 Reference)
- *Site Reliability Engineering* (Google SRE, O'Reilly): 확장성 및 관측 가능성(Observability) 골든룰 체계 설계 (Theory 5.3 Reference)
