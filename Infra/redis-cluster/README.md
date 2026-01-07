# Redis Cluster

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 고성능과 수평 확장성을 제공하는 **Redis Cluster**입니다.  
총 6개의 노드(3 Master, 3 Replica)로 구성되어 데이터가 여러 노드에 자동 분산(Sharding)되며, 특정 마스터 노드 장애 시 레플리카가 즉시 승격되는 고가용성 아키텍처입니다.

## 2. 주요 기능 (Key Features)
- **Data Sharding**: 16,384개의 해시 슬롯을 여러 노드에 나누어 저장하므로 단일 노드의 메모리 한계를 극복할 수 있습니다.
- **High Availability**: Sentinel 없이 클러스터 자체적으로 장애 감지 및 Failover를 수행합니다.
- **Self-Healing**: 초기화 컨테이너(`redis-cluster-init`)가 클러스터 구성을 자동화하며, 재시작 시 기존 상태를 유지합니다.

## 3. 기술 스택 (Tech Stack)
- **Image**: `redis:8.4.0-bookworm`
- **Architecture**: Redis Cluster (Multi-Master)
- **Monitoring**: Redis Exporter

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 클러스터 토폴로지
- **Master Nodes**: `redis-node-0`, `redis-node-1`, `redis-node-2` (데이터 쓰기/읽기)
- **Replica Nodes**: `redis-node-3`, `redis-node-4`, `redis-node-5` (데이터 복제 및 Failover 대기)

### 초기화 프로세스
1.  각 Redis 노드가 독립적으로 실행됨.
2.  `redis-cluster-init` 컨테이너가 시작되어 모든 노드가 `Ready` 상태인지 확인.
3.  `redis-cli --cluster create` 명령을 수행하여 6개 노드를 하나의 클러스터로 묶고 슬롯을 할당.

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
> **참고**: `redis-cluster-init` 컨테이너가 종료(Exited 0)되면 클러스터 구성이 완료된 것입니다.

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 클라이언트 연결
Redis Cluster를 지원하는 라이브러리(Java Redisson, Node.js ioredis, Python redis-py 등)를 사용해야 합니다.
- **Connection URI**: `redis://redis-node-0:6379,redis-node-1:6379,...` (여러 시드 노드를 지정하는 것을 권장)
- **Password**: Docker Secret(`redis_password`)에 정의된 값.

### 6.2 수동 관리 (CLI)
특정 노드에 접속하여 클러스터 상태를 확인할 수 있습니다.
```bash
# 클러스터 노드 정보 확인
docker exec -it redis-node-0 redis-cli -a "$REDIS_PASSWORD" cluster nodes

# 클러스터 정보 요약
docker exec -it redis-node-0 redis-cli -a "$REDIS_PASSWORD" cluster info
```

## 7. 환경 설정 명세 (Configuration Reference)
### 환경 변수 (Environment Variables)
- `REDIS_PASSWORD`: 보안을 위한 클러스터 패스워드.
- `PORT`: 각 컨테이너 내부 포트 (기본 6379).
- `NODE_NAME`: 각 노드의 식별자.

### 네트워크 포트 (Ports)
- **Client Port**: 6379 (내부), 호스트 포트는 `.env` 파일에 정의됨(예: 63791~63796).
- **Bus Port**: 16379 (Cluter Gossip 통신용).

## 8. 통합 및 API 가이드 (Integration Guide)
**Redis Exporter**:
- `redis-exporter` 컨테이너가 배포되어 있으며, Prometheus가 이를 통해 메트릭을 수집합니다.
- 특정 노드 하나(`redis-node-0`)에 접속하여 `CLUSTER INFO` 등의 전역 메트릭을 수집하도록 설정되어 있습니다.

## 9. 가용성 및 관측성 (Availability & Observability)
**Health Check**:
- 각 노드마다 `redis-cli ping`을 주기적으로 수행하여 상태를 점검합니다.
- `redis-cluster-init` 컨테이너는 모든 노드가 Healthy 상태일 때만 동작을 시작합니다.

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**Persistence**:
- 모든 노드는 AOF(`appendonly yes`) 설정이 켜져 있어, 데이터 변경 사항이 디스크에 즉시 기록됩니다.
- 볼륨(`redis-data-*`)은 영구 보존되므로 컨테이너 재배포 시에도 데이터는 유지됩니다.

## 11. 보안 및 강화 (Security Hardening)
- **Password Auth**: 클러스터 내 모든 통신 및 클라이언트 접속 시 비밀번호 인증이 강제됩니다.
- **Network Isolation**: 호스트 포트 매핑은 디버깅 목적(`redis-node-0`)을 제외하고는 최소화하는 것이 좋습니다.

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **MOVED Error**: 클러스터 모드를 지원하지 않는 일반 Redis 클라이언트로 접속했을 때 발생합니다. 클러스터 호환 클라이언트를 사용하십시오.
- **Cluster Down**: 과반수 이상의 마스터 노드가 동시에 다운되면 클러스터 전체가 멈춥니다. 분산 배치 전략이 필요합니다.

---
**공식 문서**: [https://redis.io/docs/manual/scaling/](https://redis.io/docs/manual/scaling/)
