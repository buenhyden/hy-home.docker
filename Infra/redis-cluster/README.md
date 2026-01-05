# Redis Cluster

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 6개의 노드(3 Master + 3 Replica)로 구성된 Redis Cluster입니다. 데이터 샤딩(Sharding)과 고가용성을 제공합니다.

**주요 기능 (Key Features)**:
- **Sharding**: 데이터를 여러 노드에 분산 저장하여 메모리 한계 극복.
- **High Availability**: 마스터 장애 시 레플리카가 승격.

**기술 스택 (Tech Stack)**:
- **Image**: `redis:8.4.0-bookworm`
- **Architecture**: Redis Cluster (Non-Sentinel)

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)
- **Nodes**: `redis-node-0` ~ `redis-node-5`
- **Init**: `redis-cluster-init` 컨테이너가 최초 실행 시 클러스터 결성(`--cluster create`).

## 3. 시작 가이드 (Getting Started)
**실행 방법 (Deployment)**:
```bash
docker compose up -d
```
(초기화 스크립트가 자동으로 클러스터를 구성합니다.)

## 4. 환경 설정 명세 (Configuration Reference)
**환경 변수 (Environment Variables)**:
- `REDIS_PASSWORD`: 클러스터 노드 간 인증 암호.

**네트워크 포트 (Network Ports)**:
- **Client Port**: 6379 (각 노드별 포트 매핑 상이, 내부 통신은 컨테이너명 사용)
- **Bus Port**: 16379

## 5. 통합 및 API 가이드 (Integration Guide)
**클라이언트 설정**:
Redis Cluster 모드를 지원하는 클라이언트를 사용해야 합니다.
- **Seed Nodes**: `redis-node-0:6379`, `redis-node-1:6379`, ...

## 6. 가용성 및 관측성 (Availability & Observability)
**모니터링 (Monitoring)**:
- `redis-exporter`가 클러스터 상태를 수집합니다.

## 7. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 백업**:
- AOF(`appendonly yes`) 설정됨.

## 8. 보안 및 강화 (Security Hardening)
- `requirepass`를 통해 비밀번호 인증 강제.

## 9. 트러블슈팅 (Troubleshooting)
**진단 명령어**:
```bash
# 클러스터 상태 정보 확인
docker exec -it redis-node-0 redis-cli -a $PASS cluster info
docker exec -it redis-node-0 redis-cli -a $PASS cluster nodes
```
