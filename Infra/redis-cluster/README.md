# Redis Cluster (Sharded) Infrastructure

## 1. 개요 (Overview)
이 디렉토리는 데이터 샤딩(Sharding)과 고가용성을 제공하는 Redis Cluster 모드를 정의합니다. 총 6개의 노드(3 Master + 3 Replica)로 구성되며, 클러스터 생성을 자동화하는 초기화 스크립트를 포함합니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **redis-node-0 ~ 5** | Cluster Nodes | Redis 인스턴스입니다. 각 노드는 서로 통신하며 데이터 슬롯을 분배합니다. |
| **redis-cluster-init** | Cluster Creator | 컨테이너 시작 시 한 번 실행되어 노드들을 메쉬로 묶고 클러스터(`cluster create`)를 구성합니다. |
| **redis-exporter** | Metrics Exporter | Prometheus 메트릭 수집기입니다. `redis-node-0`을 타겟으로 설정하여 클러스터 상태를 모니터링합니다. |

## 3. 구성 및 설정 (Configuration)

### 네트워크
- **Port Mapping**: 각 노드는 서비스 포트(e.g., 6379)와 버스 포트(e.g., 16379)를 호스트 또는 네트워크에 노출합니다. 클러스터 모드에서는 클라이언트가 리다이렉션을 따라가야 하므로 네트워크 구성에 주의해야 합니다.
- **Redis Conf**: `./config/redis.conf` 파일을 모든 노드가 공유합니다.

### 초기화
`redis-cluster-init.sh` 스크립트는 모든 노드가 준비될 때까지 대기한 후, `redis-cli --cluster create ...` 명령을 실행하여 3 Master, 1 Replica/Master 구성을 완료합니다.

### 보안
- **Password**: Docker Secret(`redis_password`)을 통해 모든 노드 접근 시 인증을 요구합니다.
- **Healthcheck**: 헬스 체크 명령에서도 비밀번호를 사용하여 상태를 확인합니다.
