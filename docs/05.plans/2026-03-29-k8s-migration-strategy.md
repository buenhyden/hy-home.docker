# Infrastructure Migration Analysis: Docker Compose to k3s/k3d

이 문서는 현재 infra 폴더의 각 하위 서비스들을 조사하고 분석하여 k3d와 k3s로 구현된 Kubernetes(K8s) 환경으로 이전하기에 적합한 서비스들을 정리한 전략 보고서입니다.

## 분석 개요

현재 `hy-home.docker`는 01-11 계층으로 구성된 Docker Compose 기반의 인프라를 사용 중입니다. 이미 일부 도구(ArgoCD, Kiali)가 k3d 클러스터 상에서 운영되고 있으며, Traefik이 이를 중계하는 구조를 가지고 있습니다.

## 이전 평가 기준

각 서비스의 K8s 이전 적합성은 다음과 같은 기준에 따라 평가되었습니다:
1. **오케스트레이션 이점**: 자동 확장(HPA), 자가 치유(Self-healing), 대규모 롤아웃 전략이 필요한가?
2. **에코시스템 성숙도**: 성숙한 K8s Operator 또는 Helm 차트가 존재하는가? (예: Prometheus, Kafka)
3. **연결성 및 통합**: 다른 K8s 네이티브 워크로드와 밀접한 상호작용이 필요한가?
4. **상태 관리(Stateful)의 난이도**: CSI(Container Storage Interface)를 통한 데이터 영속성 관리가 용이한가?
5. **운영 복잡도 절감**: 이전 시 현재의 관리 방식보다 운영이 단순화되는가?

---

## 서비스 계층별 이전 분석

### Tier 01-03: 핵심 인프라 (Gateway, Auth, Security)

| 서비스 | 이전 상태 | 권장 사항 | 사유 |
| :--- | :--- | :--- | :--- |
| **Traefik** | **심(Shim) 유지** | 기존 Docker 유지 | 현재 Docker와 k3d 전체의 진입점 역할을 수행 중입니다. 전체 서비스가 K8s로 넘어가기 전까지는 현재 위치를 유지하는 것이 안정적입니다. |
| **Keycloak** | **이전 대상 (P2)** | K8s HA 배포 | Quarkus 기반 최신 Keycloak은 K8s에 최적화되어 있습니다. HA 구성 및 K8s Secret 활용 시 보안과 가용성이 향상됩니다. |
| **Vault** | **이전 대상 (P2)** | K8s 통합 | K8s Sidecar Injection 및 전용 인증 방식을 통해 K8s 워크로드에 대한 보안 관리가 매우 용이해집니다. |

### Tier 04: 데이터 계층 (Data Layer)

| 서비스 | 이전 상태 | 권장 사항 | 사유 |
| :--- | :--- | :--- | :--- |
| **PostgreSQL / MongoDB** | **낮은 우선순위** | Docker/외부 유지 | 데이터베이스의 K8s 이전은 강력한 CSI(Storage) 지원이 필수입니다. Longhorn 등 전용 스토리지 솔루션 검증 전까지는 Docker 유지를 권장합니다. |
| **Valkey / Redis** | **낮은 우선순위** | Docker 유지 | 저지연 성능이 중요하며, 단일 노드 운영 시에는 Docker가 관리하기 더 편할 수 있습니다. |
| **MinIO** | **이전 대상 (P3)** | StatefulSet 배포 | K8s 스토리지 오케스트레이션과 잘 어울리지만, 디스크 성능 및 CSI 안정성에 의존합니다. |

### Tier 05-06: 메시징 및 관찰성 (Messaging & Observability) - **핵심 가치**

| 서비스 | 이전 상태 | 권장 사항 | 사유 |
| :--- | :--- | :--- | :--- |
| **Prometheus / Grafana** | **높은 우선순위 (P1)** | K8s Operator 활용 | K8s 모니터링의 표준입니다. K8s 내부로 이전 시 클러스터 자원 메트릭 수집 및 시각화가 비약적으로 향상됩니다. |
| **Kafka / RabbitMQ** | **이전 대상 (P2)** | Strimzi Operator | Kafka의 복잡한 운영을 Strimzi와 같은 K8s Operator가 자동화해주어 관리 효율성이 극대화됩니다. |
| **Loki / Tempo** | **높은 우선순위 (P1)** | K8s 배포 | K8s 로그 및 트레이싱 수집기(Promtail/Alloy)와 긴밀하게 통합됩니다. |

### Tier 07-08: 워크플로우 및 AI (Workflow & AI)

| 서비스 | 이전 상태 | 권장 사항 | 사유 |
| :--- | :--- | :--- | :--- |
| **Airflow** | **높은 우선순위 (P1)** | K8s Executor 적용 | Airflow의 각 Task를 개별 Pod로 실행하여 자원 격리 및 수평적 확장이 가능해집니다. |
| **n8n** | **이전 대상 (P2)** | Queue Mode 적용 | 대규모 워크로드 처리 시 K8s의 자원 관리 이점을 활용할 수 있습니다. |
| **Ollama / Open WebUI** | **이전 대상 (P2)** | GPU 오케스트레이션 | K8s Device Plugin(NVIDIA)을 통해 GPU 자원의 효율적인 스케줄링 및 공유가 가능합니다. |

---

## 단계별 이전 로드맵

### 1단계: 관찰성 및 워크플로우 (운영 효율 극대화)
- **대상**: Prometheus, Grafana, Loki (+ Alloy 통합), Airflow.
- **목표**: K8s 네이티브 모니터링 환경을 구축하고, 대규모 태스크 처리를 위한 워크플로우 엔진 확장성을 확보합니다.

### 2단계: ID 관리 및 메시징 (인프라 확장성)
- **대상**: Keycloak, Kafka, RabbitMQ.
- **목표**: K8s Operator를 활용하여 클러스터링 및 고가용성(HA) 관리 비용을 절감합니다.

### 3단계: 보안 및 AI 하드웨어 가속 (보안성 및 성능)
- **대상**: Vault, Ollama.
- **목표**: 보안 컨텍스트를 강화하고, GPU 자원 스케줄링을 최적화합니다.

## 향후 과제 및 질문

1. **스토리지 계층**: 현재 호스트 환경에서 Longhorn 또는 OpenEBS와 같은 K8s 전용 스토리지 솔루션 도입이 가능한지 확인이 필요합니다.
2. **네트워크 구조**: Traefik을 K8s 내부 Ingress Controller로 완전히 전환할지, 아니면 현재처럼 외부 Shim으로 유지할지 결정이 필요합니다.
3. **GPU 지원**: k3d 클러스터 내에서 NVIDIA Container Toolkit이 정상적으로 인식되도록 하는 추가 설정이 필요합니다.
