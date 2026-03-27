# Cache and KV Guides (04-data/cache-and-kv)

> Distributed Caching and Fast Key-Value Storage Usage Guides / 분산 캐시 및 Key-Value 저장소 활용 가이드

## Overview (KR)

이 경로는 Valkey, Redis 등 캐시 및 KV 저장소 계층의 서비스들에 대한 사용자 가이드를 포함한다. 에코시스템 내에서 캐싱 레이어를 효과적으로 활용하기 위한 기술 정보를 제공한다.

This path contains user guides for services in the cache and KV storage layer, such as Valkey and Redis. It provides technical information for effectively utilizing the caching layer within the ecosystem.

## Audience

이 README의 주요 독자:
- 시스템을 연동하는 **Developers**
- 캐시 상태를 점검하는 **Operators**
- 가이드 구조를 파악하는 **AI Agents**

## Scope

### In Scope
- Valkey Cluster 연동 가이드
- Redis 호환 클라이언트 설정 지침
- 캐싱 전략 및 모범 사례

### Out of Scope
- 인프라 배포 스크립트 (infra/ 참조)
- 개별 애플리케이션의 비즈니스 로직
- 데이터베이스 쿼리 튜닝 (relational/ 참조)

## Structure

```text
cache-and-kv/
├── valkey-cluster.md    # Valkey Cluster 활용 가이드
└── README.md            # This file
```

## How to Work in This Area

1. [valkey-cluster.md](./valkey-cluster.md)를 통해 클러스터 모드 연결 방법을 숙지합니다.
2. 새로운 가이드 추가 시 `docs/99.templates/guide.template.md`를 사용합니다.
3. 관련 운영 정책은 [08.operations/04-data/cache-and-kv/README.md](../../08.operations/04-data/cache-and-kv/README.md)를 확인합니다.

## Available Guides

- [Valkey Cluster Guide](./valkey-cluster.md): 6노드 분산 클러스터 연결 및 사용법.

## Related References

- **Implementation**: [infra/04-data/cache-and-kv/README.md](../../../../infra/04-data/cache-and-kv/README.md)
- **Operation**: [04-data Operations](../../08.operations/04-data/cache-and-kv/README.md)
- **Runbook**: [04-data Runbooks](../../09.runbooks/04-data/cache-and-kv/README.md)
