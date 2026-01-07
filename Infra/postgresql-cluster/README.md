# PostgreSQL HA Cluster

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: Patroni, Etcd, HAProxy를 기반으로 구축된 고가용성(High Availability) PostgreSQL 클러스터입니다.
단일 장애점(SPOF)을 제거하고 자동 복구(Auto Failover) 및 읽기/쓰기 부하 분산을 지원하여 미션 크리티컬한 데이터 처리를 보장합니다.

## 2. 주요 기능 (Key Features)
- **Automatic Failover**: Primary 노드에 장애 발생 시 Standby 노드 중 하나가 자동으로 리더로 승격됩니다.
- **Split-Brain Protection**: Etcd 분산 합의(DCS)를 통해 네트워크 단절 상황에서도 데이터 일관성을 보호합니다.
- **Load Balancing**: HAProxy가 데이터베이스 상태를 실시간으로 감지하여 Write 트래픽은 Primary로, Read 트래픽은 Replica로 라우팅합니다.
- **Self-Healing**: 장애가 복구된 노드는 자동으로 클러스터에 Rejoin하여 동기화를 수행합니다.

## 3. 기술 스택 (Tech Stack)
- **Database**: PostgreSQL 17 (via Spilo)
- **Cluster Manager**: Patroni
- **DCS**: Etcd v3.6.7
- **Router**: HAProxy 3.3.1 (Load Balancer)

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 클러스터 구성도
```mermaid
graph TD
    Client[애플리케이션] -->|Write (5000)| HAProxy
    Client[애플리케이션] -->|Read (5001)| HAProxy
    HAProxy -->|Primary| PG0[(Node 0)]
    HAProxy -->|Replica| PG1[(Node 1)]
    HAProxy -->|Replica| PG2[(Node 2)]
    PG0 --- Etcd[Etcd Cluster]
    PG1 --- Etcd
    PG2 --- Etcd
    subgraph Etcd Cluster
        E1[Etcd-1] --- E2[Etcd-2] --- E3[Etcd-3]
    end
```

### 동작 원리
1.  **Patroni**는 각 PG 노드에서 실행되며 Etcd에 Leader Key를 주기적으로 갱신(TTL)합니다.
2.  **HAProxy**는 Patroni API를 통해 리더 및 레플리카 상태를 확인합니다.
3.  **Client**는 실제 DB IP를 알 필요 없이 HAProxy 포트로 접근합니다.

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
> **초기화 시간**: Etcd 클러스터 구성 및 Patroni 리더 선출 과정으로 인해 서비스 시작 후 약 1~2분 정도 대기 시간이 필요할 수 있습니다.

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 클라이언트 연결
애플리케이션에서는 다음 주소를 사용하여 접속합니다.
- **Master (Read/Write)**: `host=pg-router port=5000`
- **Replica (Read Only)**: `host=pg-router port=5001`
- **User/Pass**: `.env.postgres` 파일 참조 (기본 `postgres` / `postgres`).

### 6.2 HAProxy 통계 확인
- **주소**: `https://pg-haproxy.${DEFAULT_URL}`
- **기능**: 현재 Primary가 누구인지, 각 노드의 상태(UP/DOWN)와 트래픽 통계를 실시간으로 볼 수 있습니다.

## 7. 환경 설정 명세 (Configuration Reference)
### 환경 변수 (Environment Variables)
- `SCOPE`: `pg-ha` (클러스터 이름).
- `ETCD3_HOSTS`: Etcd 노드 연결 정보.
- `PATRONI_POSTGRESQL_LISTEN`: PG 수신 주소.

### 네트워크 포트 (Ports)
- **HAProxy Write**: 5000
- **HAProxy Read**: 5001
- **Stats UI**: 8404 (Traefik 노출)

## 8. 통합 및 API 가이드 (Integration Guide)
**Patroni API**:
각 노드의 8008 포트로 REST API를 제공합니다 (내부망).
- `GET /cluster`: 클러스터 상태 조회.
- `POST /switchover`: 리더 수동 전환.

## 9. 가용성 및 관측성 (Availability & Observability)
**Health Check**:
- **Etcd**: `etcdctl endpoint health`.
- **Postgres**: `pg_isready`.
- **Patroni**: `curl localhost:8008/health` (200=Leader, 503=Replica).

**Monitoring**:
- `pg-0-exporter` 등 각 노드별 Exporter가 배치되어 개별 인스턴스의 상세 메트릭을 수집합니다.

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**장애 복구**:
- **노드 다운**: 별도 조치 불필요. Patroni가 자동으로 Failover 또는 Rejoin 수행.
- **전체 중단**: 데이터 볼륨(`pg*-data`)이 살아있다면 컨테이너 재기동으로 복구 가능.
- **데이터 손상**: 최후의 수단으로 `pg_basebackup`이나 WAL 아카이브를 통한 복구가 필요합니다 (별도 백업 솔루션 구성 권장).

## 11. 보안 및 강화 (Security Hardening)
- **Network Isolation**: DB 인스턴스 직접 접속은 차단하고 HAProxy를 통해서만 접근하도록 제한하는 것이 좋습니다.
- **Etcd Auth**: 프로덕션 환경에서는 Etcd 클라이언트 인증(TLS+Auth)을 활성화해야 합니다.

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Leader Key Expired**: Etcd 부하로 인해 TTL 갱신 실패 시 리더가 강등될 수 있습니다. 디스크 I/O와 네트워크 안정성을 확인하세요.
- **Split Brain**: 네트워크 파티션 발생 시 Etcd 쿼럼(Quorum)이 깨지면 DB는 Read-only로 전환됩니다.

**진단 명령어**:
```bash
# 클러스터 멤버 및 리더 상태 확인
docker exec -it pg-0 patronictl -c /etc/patroni/patroni.yml list
```

---
**관련 프로젝트**: [Zalando Patroni](https://github.com/zalando/patroni)
