# ⚡ Cache & Memory DB Guide (Redis/Valkey)

고성능 인메모리 데이터 구조 저장소인 **Redis**와 오픈소스 대안인 **Valkey** 가이드입니다.

## 1. Redis vs Valkey

본 프로젝트는 두 가지를 모두 지원하며, 용도에 따라 선택할 수 있습니다.

- **Redis**: 전통적이고 검증된 생태계를 제공합니다.
- **Valkey**: Linux Foundation 기반의 완전 오픈소스 프로젝트로, Redis 7.2.4 버전에서 포크되어 최신 고속 처리 기능을 개선했습니다. 안정적인 라이선스 환경을 지향한다면 **Valkey**를 권장합니다.

## 2. Deployment Patterns

### Redis Cluster (3 Master / 3 Replica)

대규모 분산 처리가 필요한 데이터(세션, 대용량 캐시)를 위해 6개 노드로 구성된 클러스터 모드를 제공합니다.

- **접속 Endpoint**: `redis-cluster:6379` (자동 샤딩 지원 클라이언트 사용 필수)

### Valkey Cluster

Redis 클러스터와 동일한 구조로 가동되며, 향상된 멀티스레딩 성능을 체감할 수 있습니다.

- **접속 Endpoint**: `valkey-cluster:6379`

### Managed Redis (Standalone)

단일 인스턴스 형태의 `mng-redis`는 인프라 서비스의 간단한 상태값을 저장합니다.

## 3. Visualization & Admin Tools

### Redis Insight

강력한 웹 기반 GUI 도구를 통해 모든 인스턴스를 관리합니다.

- **접속 주소**: `https://redisinsight.${DEFAULT_URL}`
- **기능**: 데이터 브라우징, Memory Analyzer, CLI 실행, 클러스터 노드 상태 시각화.

## 4. Performance Tuning

- **Persistence**: 데이터 유실을 최소화하려면 `Append Only File (AOF)`를 활성화하십시오.
- **Eviction Policy**: 메모리 부족 시 동작 방식(`allkeys-lru` 등)을 워크로드에 맞게 설정하십시오.
- **Resource Limits**: `.env` 파일에서 컨테이너별 메모리 제한을 확인하십시오.

## 5. Troubleshooting Guide

- **CLUSTER DOWN**: 노드 간의 `cluster-bus-port` (6379 + 10000) 통신이 차단되지 않았는지 확인하십시오.
- **OOM (Out Of Memory)**: `info memory` 명령을 통해 호스트 메모리 잔량을 확인하십시오.
- **Auth Failure**: `.github/secrets/redis_password.txt`와 `.env` 파일의 패스워드가 일치하는지 확인하십시오.
