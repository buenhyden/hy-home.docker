# Cache & Key-Value Stores (04-data/cache-and-kv)

> Distributed Caching and Fast Key-Value Storage Services / 분산 캐싱 및 고성능 키-밸류 저장소 서비스

## Overview

이 디렉터리는 `hy-home.docker` 인프라의 캐싱 및 키-밸류 저장소 서비스를 위한 구성을 포함합니다. 고성능 데이터 액세스와 임시 상태 관리에 최적화된 서비스를 제공합니다.

This directory contains infrastructure configurations for caching and key-value storage services within `hy-home.docker`. These services are optimized for high-performance data access and transient state management.

## Audience

이 README의 주요 독자:
- 인프라를 배포하고 관리하는 **Operators**
- 캐시 서비스를 연동하는 **Developers**
- 자동화된 운영 작업을 수행하는 **AI Agents**

## Scope

### In Scope
- Valkey Cluster (6-node) 구성 및 관리
- 분산 캐싱 인프라 프로비저닝
- 클러스터 헬스체크 및 성능 모니터링 구성

### Out of Scope
- 애플리케이션 레벨의 데이터 모델링
- 캐시 무효화 로직 구현
- 개별(Stand-alone) Valkey 인스턴스 관리

## Structure

```text
cache-and-kv/
├── valkey-cluster/       # 6-node 분산 클러스터 (Primary + Replica)
└── README.md             # This file
```

## How to Work in This Area

1. [valkey-cluster/README.md](./valkey-cluster/README.md)를 통해 세부 클러스터 구성을 확인합니다.
2. 실행 가이드는 [Valkey Cluster Guide](../../../docs/07.guides/04-data/cache-and-kv/valkey-cluster.md)를 참조합니다.
3. 운영 정책은 [Valkey Operations Policy](../../../docs/08.operations/04-data/cache-and-kv/valkey-cluster.md)를 확인합니다.

## Related References

- **Guides**: [docs/07.guides/04-data/cache-and-kv/valkey-cluster.md](../../../docs/07.guides/04-data/cache-and-kv/valkey-cluster.md)
- **Operations**: [docs/08.operations/04-data/cache-and-kv/valkey-cluster.md](../../../docs/08.operations/04-data/cache-and-kv/valkey-cluster.md)
- **Runbooks**: [docs/09.runbooks/04-data/cache-and-kv/valkey-cluster.md](../../../docs/09.runbooks/04-data/cache-and-kv/valkey-cluster.md)

## Tech Stack

| Category   | Technology   | Notes                     |
| ---------- | ------------ | ------------------------- |
| Storage    | Valkey       | Redis-compatible high-perf|
| Topology   | 3P + 3R      | 6-node Cluster            |

## Available Scripts

| Command | Description |
| :--- | :--- |
| `cd valkey-cluster && docker compose up -d` | 클러스터 전체 노드 시작 |
| `cd valkey-cluster && docker compose ps` | 노드별 상태 확인 |
