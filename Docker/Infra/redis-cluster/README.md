# Redis Cluster

**Redis Cluster**는 데이터를 여러 노드에 자동으로 분산(Sharding)하여 저장하는 고가용성 인메모리 데이터 구조 저장소입니다.
이 구성은 **3 Master + 3 Replica** 총 6개의 노드로 구성됩니다.

## 🚀 서비스 구성

| 서비스명 | 역할 | 포트 |
| --- | --- | --- |
| **redis-node-0 ~ 5** | Redis 클러스터 노드 | `6379` (Node 0만 호스트 노출) |
| **redis-cluster-init** | 클러스터 초기화 스크립트 (1회성) | - |
| **redis-exporter** | Prometheus용 메트릭 Exporter | `9121` |
| **redisinsight** | Redis 관리 GUI | `8001` |

## 🛠 설정 및 환경 변수

- **비밀번호**: Docker Secret(`redis_password`)을 통해 관리됩니다.
- **RedisInsight**: `http://localhost:8001` 접속.

## 📦 볼륨 마운트

- `redis-data-0` ~ `redis-data-5`: 각 노드의 데이터 저장소

## 🏃‍♂️ 실행 방법

```bash
docker compose up -d
```
- `redis-cluster-init` 컨테이너가 자동으로 클러스터를 구성합니다 (`cluster create`).

## ⚠️ 주의사항
- **접속**: 클러스터 모드이므로 클라이언트는 클러스터 모드를 지원해야 합니다.
- **포트**: 호스트에서는 `localhost:6379`로 Node 0에만 접근 가능합니다.
