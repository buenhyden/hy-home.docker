# Cache and KV Operations (04-data/cache-and-kv)

> Operations Policies for Distributed Caching and KV Stores / 분산 캐시 및 Key-Value 저장소 운영 정책

## Overview (KR)

이 경로는 Valkey, Redis 등 캐시 및 KV 저장소 계층의 서비스들에 대한 운영 표준과 보안 정책을 포함한다. 데이터 영속성, 메모리 관리, 접근 제어를 규정한다.

This path contains operational standards and security policies for services in the cache and KV storage layer, such as Valkey and Redis. It regulates data persistence, memory management, and access control.

## Audience

이 README의 주요 독자:
- 운영 표준을 관리하는 **Operators**
- 보안 통제를 감사하는 **Security Engineers**
- 정책 준수 가이드를 읽는 **AI Agents**

## Scope

### In Scope
- Valkey Cluster 운영 및 보안 정책
- 캐시 메모리 할당 및 제거(Eviction) 기준
- 데이터 영속성(AOF/RDB) 설정 표준

### Out of Scope
- NoSQL 데이터베이스 정책 (nosql/ 참조)
- 백업 시스템 구현 세부 사항
- 개별 애플리케이션 권한 관리

## Structure

```text
cache-and-kv/
├── valkey-cluster.md    # Valkey Cluster 운영 정책
└── README.md            # 이 파일
```

## How to Work in This Area

1. 전역 데이터 보안 정책은 [backup-policy.md](../backup-policy.md)를 먼저 확인합니다.
2. 정책 위반 사항 발견 시 즉시 담당자에게 보고하고 [Runbook](../../../09.runbooks/04-data/cache-and-kv/README.md)을 참조합니다.

## Available Policies

- [Valkey Cluster Operations Policy](./valkey-cluster.md): 백업, 보안, 리소스 관리 표준.

## Related References

- **Implementation**: [infra/04-data/cache-and-kv/README.md](../../../../infra/04-data/cache-and-kv/README.md)
- **Guide**: [04-data Guides](../../../07.guides/04-data/cache-and-kv/README.md)
- **Runbook**: [04-data Runbooks](../../../09.runbooks/04-data/cache-and-kv/README.md)
