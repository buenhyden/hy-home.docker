---
status: active
---
<!-- Target: docs/90.references/kubernetes/docker-compose-to-k3s-migration.md -->

# Reference: Docker Compose to k3s/k3d Migration

## Overview

이 문서는 Docker Compose 기반 `hy-home.docker` 인프라를 k3s/k3d 기반 Kubernetes 환경으로 이전할 때 참고할 수 있는 migration suitability snapshot이다. 실행 계획이나 승인된 아키텍처 결정이 아니라, 서비스별 이전 적합성과 판단 기준을 보존하는 reference다.

## Purpose

Kubernetes 이전 논의를 시작할 때 어떤 서비스가 이전 후보인지, 어떤 판단 기준을 사용했는지, 어떤 후속 결정이 필요한지 빠르게 확인할 수 있도록 한다.

## Repository Role

이 reference는 migration planning의 배경 자료다. 최신 runtime truth는 `infra/`, root `docker-compose.yml`, validation scripts가 담당한다. 실제 migration 결정은 ARD/ADR로 승격해야 하며, 실행 순서와 evidence는 `docs/04.execution/`에 별도로 작성해야 한다.

## Scope

### In Scope

- Docker Compose to k3s/k3d migration 평가 기준
- 서비스 계층별 이전 적합성 snapshot
- 단계별 migration 방향성
- 후속 검토 질문

### Out of Scope

- 승인된 migration decision
- active rollout plan 또는 task evidence
- Kubernetes manifest, Helm chart, Operator 설정 원문
- 운영 runbook 또는 incident recovery 절차
- secret 값, credential, token, private key

## Definitions / Facts

### Migration Evaluation Criteria

각 서비스의 Kubernetes 이전 적합성은 다음 기준으로 평가한다.

1. **오케스트레이션 이점**: 자동 확장, 자가 치유, 롤아웃 전략이 필요한가?
2. **에코시스템 성숙도**: 성숙한 Kubernetes Operator 또는 Helm chart가 존재하는가?
3. **연결성 및 통합**: Kubernetes-native workload와 밀접하게 통합되어야 하는가?
4. **상태 관리 난이도**: CSI 기반 데이터 영속성 관리가 가능한가?
5. **운영 복잡도**: 이전 후 현재 Docker Compose 운영보다 단순해지는가?

### Tier 01-03: Gateway, Auth, Security

| Service | Migration Snapshot | Recommendation | Rationale |
| :--- | :--- | :--- | :--- |
| Traefik | Shim 유지 후보 | Docker 유지 | Docker와 k3d 전체 진입점 역할을 하므로 전체 전환 전까지 현재 위치가 안정적이다. |
| Keycloak | 이전 대상 후보 | Kubernetes HA 배포 검토 | Quarkus 기반 Keycloak은 Kubernetes 운영과 HA 구성에 적합하다. |
| Vault | 이전 대상 후보 | Kubernetes 통합 검토 | Sidecar injection과 Kubernetes auth method를 활용할 수 있다. |

### Tier 04: Data

| Service | Migration Snapshot | Recommendation | Rationale |
| :--- | :--- | :--- | :--- |
| PostgreSQL / MongoDB | 낮은 우선순위 | Docker 또는 외부 유지 | 데이터베이스 이전은 안정적인 CSI/storage 검증이 선행되어야 한다. |
| Valkey / Redis | 낮은 우선순위 | Docker 유지 | 단일 노드 운영에서는 Docker가 더 단순할 수 있다. |
| MinIO | 이전 대상 후보 | StatefulSet 배포 검토 | Kubernetes storage orchestration과 맞지만 디스크 성능과 CSI 안정성에 의존한다. |

### Tier 05-06: Messaging and Observability

| Service | Migration Snapshot | Recommendation | Rationale |
| :--- | :--- | :--- | :--- |
| Prometheus / Grafana | 높은 우선순위 후보 | Kubernetes Operator 검토 | Kubernetes monitoring 표준 경로와 잘 맞는다. |
| Kafka / RabbitMQ | 이전 대상 후보 | Strimzi 또는 Operator 검토 | 복잡한 broker 운영을 Operator로 줄일 수 있다. |
| Loki / Tempo | 높은 우선순위 후보 | Kubernetes 배포 검토 | Kubernetes logs/traces 수집기와 긴밀하게 통합된다. |

### Tier 07-08: Workflow and AI

| Service | Migration Snapshot | Recommendation | Rationale |
| :--- | :--- | :--- | :--- |
| Airflow | 높은 우선순위 후보 | Kubernetes Executor 검토 | task별 pod 실행으로 자원 격리와 확장성을 얻을 수 있다. |
| n8n | 이전 대상 후보 | queue mode 검토 | 대규모 workflow 처리 시 Kubernetes 자원 관리 이점을 활용할 수 있다. |
| Ollama / Open WebUI | 이전 대상 후보 | GPU orchestration 검토 | NVIDIA Device Plugin 기반 GPU scheduling을 검토할 수 있다. |

### Migration Roadmap Snapshot

1. **관찰성 및 워크플로우**: Prometheus, Grafana, Loki, Alloy, Airflow를 먼저 검토한다.
2. **ID 관리 및 메시징**: Keycloak, Kafka, RabbitMQ의 Operator/HA 전환 비용을 평가한다.
3. **보안 및 AI 하드웨어 가속**: Vault와 Ollama의 보안/GPU 운영 경계를 평가한다.

### Open Questions

1. 현재 host 환경에서 Longhorn, OpenEBS 같은 Kubernetes storage solution을 안정적으로 도입할 수 있는가?
2. Traefik을 Kubernetes Ingress Controller로 완전히 이전할지, Docker-side shim으로 유지할지 결정이 필요한가?
3. k3d cluster 안에서 NVIDIA Container Toolkit과 GPU device plugin이 필요한 서비스 요구를 충족하는가?

## Source Rules

- 현재 runtime 상태는 `infra/`와 root `docker-compose.yml`에서 다시 확인한다.
- migration 판단을 실행으로 바꾸려면 관련 ARD/ADR과 plan/task 문서를 새로 작성한다.
- external chart, Operator, vendor status는 현재 시점에 다시 확인한다.
- 이 문서는 active policy나 runbook을 대체하지 않는다.

## Sources

- [root README](../../../README.md) - repository purpose, runtime entrypoints, validation gates
- [infra index](../../../infra/README.md) - Compose tier and service entrypoints
- [docs index](../../README.md) - stage taxonomy and migration routing
- [architecture index](../../02.architecture/README.md) - target location for accepted migration architecture decisions
- [execution index](../../04.execution/README.md) - target location for active migration plans and task evidence

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when Kubernetes migration work is actively proposed or when infra tier ownership changes
- **Update Trigger**: Update when a service migration decision is accepted, runtime topology changes, or storage/GPU assumptions change

## Related Documents

- [Kubernetes references](./README.md)
- [90.references](../README.md)
- [docs index](../../README.md)
- [architecture index](../../02.architecture/README.md)
- [execution index](../../04.execution/README.md)
- [operations index](../../05.operations/README.md)
