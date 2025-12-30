# PostgreSQL High Availability Cluster (Patroni)

## 1. 개요 (Overview)
이 디렉토리는 **Patroni**를 사용하여 고가용성(HA)을 보장하는 PostgreSQL 클러스터를 정의합니다. **Etcd**를 분산 코디네이터(DCS)로 사용하며, 3개의 PostgreSQL 노드가 클러스터를 이룹니다. **HAProxy**가 앞단에서 리더(Leader)와 레플리카(Replica)를 구분하여 트래픽을 라우팅합니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **etcd-1, 2, 3** | DCS (Distributed Consensus) | 클러스터의 상태 정보와 리더 선출(Leader Election)을 관리하는 분산 키-값 저장소입니다. |
| **pg-0, 1, 2** | PostgreSQL Nodes | Zalando spilo 이미지를 사용하는 실제 DB 노드입니다. Patroni 에이전트가 내장되어 있습니다. |
| **pg-router** | Load Balancer (HAProxy) | DB 요청을 받아 현재 리더 노드(Write) 또는 레플리카 노드(Read)로 라우팅합니다. |
| **pg-*-exporter** | Metrics Exporter | 각 DB 노드의 메트릭을 수집합니다. |

## 3. 구성 및 설정 (Configuration)

### 아키텍처
1. **Etcd Cluster**: 3개의 노드로 쿼럼을 형성하여 클러스터 상태를 저장합니다.
2. **Patroni**: 각 `pg-*` 컨테이너 내부에서 실행되며 Etcd와 통신하여 리더를 선출하고 복제를 관리합니다.
3. **Routing (HAProxy)**:
    - **Write Port** (Primary): `${POSTGRES_WRITE_HOST_PORT}` -> 리더 노드로 연결
    - **Read Port** (Replica): `${POSTGRES_READ_HOST_PORT}` -> 복제본 노드로 로드밸런싱

### 로드밸런싱 (Traefik) (Stats)
- **HAProxy Stats**: `https://pg-haproxy.${DEFAULT_URL}` 주소로 HAProxy 상태 페이지(Stat)에 접근할 수 있습니다.

### 데이터 볼륨
- `pg*-data`: 각 DB 노드의 데이터
- `etcd*-data`: Etcd 상태 데이터

### 주의 사항
- 애플리케이션에서는 개별 DB 노드(`pg-0` 등)에 직접 붙지 않고, 반드시 `pg-router`가 제공하는 포트를 통해 접속해야 HA 기능이 동작합니다.
