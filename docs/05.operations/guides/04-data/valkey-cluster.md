# Valkey Cluster Usage Guide

## Usage
>
> `docs/05.operations/04-data/valkey-cluster.md`에 대한 안내 문서입니다.

---

### Overview (KR)

이 문서는 Valkey Cluster의 아키텍처, 설정 및 사용 방법에 대한 기술 가이드입니다. 6노드 기반의 고가용성 캐시 클러스터를 이해하고 애플리케이션에 통합하는 데 필요한 정보를 제공합니다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- Agent-tuner

### Purpose

애플리케이션 개발자와 시스템 운영자가 Valkey Cluster의 구조를 이해하고, 클라이언트를 올바르게 연결하며, 성능 최적화 기법을 적용할 수 있도록 돕습니다.

### Prerequisites

- `infra/04-data/cache-and-kv/valkey-cluster`에 대한 기본 지식
- Docker 및 Docker Compose 실행 환경
- Redis Cluster 호환 프로토콜 사용 가능 클라이언트 라이브러리

### Step-by-step Instructions

#### 1. 클러스터 초기화 및 상태 확인

클러스터는 처음 배포 시 `valkey-cluster-init` 컨테이너에 의해 자동으로 구성됩니다.

```bash
## 클러스터 구성 상태 확인
read -rsp "Valkey password: " VALKEY_PASSWORD; echo
docker exec valkey-node-0 valkey-cli -a "$VALKEY_PASSWORD" cluster info
unset VALKEY_PASSWORD
```

#### 2. 클라이언트 연결 설정 (Cluster Mode)

Valkey Cluster는 샤딩된 환경이므로 모든 노드 정보를 클라이언트에 제공해야 합니다.

- **Seed Nodes**: `valkey-node-0:6379`, `valkey-node-1:6380`, `valkey-node-2:6381`, `valkey-node-3:6382`, `valkey-node-4:6383`, `valkey-node-5:6384`
- **Auth**: Docker Secrets에 정의된 패스워드를 사용합니다.
- **Redirection**: 클라이언트는 `MOVED` 또는 `ASK` 응답을 처리할 수 있어야 합니다.

#### 3. 데이터 파티셔닝 이해

총 16,384개의 해시 슬롯이 3개의 마스터 노드에 분산되어 있습니다.

- Node 0: `0 - 5460`
- Node 1: `5461 - 10922`
- Node 2: `10923 - 16383`

### Common Pitfalls

- **Single Node Access**: 클러스터 지원이 없는 라이브러리로 특정 노드에만 접속할 경우, 슬롯 불일치 시 `MOVED` 오류가 발생하며 작업이 거부됩니다.
- **Large Keys / Operations**: 클러스터 전체 성능 저하를 방지하기 위해 단일 Key에 과도한 데이터를 담거나 `KEYS *` 등의 전체 스캔 명령은 금지합니다.
- **Network Isolation**: 노드 간 통신(6379+10000 포트 등)이 막히면 슬롯 소유권 확인이 불가능해져 클러스터가 `fail` 상태로 전환됩니다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/04-data/valkey-cluster.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/04-data/valkey-cluster.md)
- [Recovery runbook](../../runbooks/04-data/valkey-cluster.md)
- [Operations template](../../../99.templates/operation.template.md)
