# Cache and KV Operations

> 분산 캐시 및 Key-Value 저장소 운영 정책.

## Overview

이 경로는 Valkey, Redis 등 캐시 및 KV 저장소 계층의 서비스들에 대한 운영 표준과 보안 정책을 포함한다.

## Structure

```text
cache-and-kv/
├── valkey-cluster.md    # Valkey Cluster 운영 정책
└── README.md            # 이 파일
```

## Available Policies

- [Valkey Cluster Operations Policy](./valkey-cluster.md): 백업, 보안, 리소스 관리 표준.

## Related References

- **Implementation**: [../../../../infra/04-data/cache-and-kv/README.md](../../../../infra/04-data/cache-and-kv/README.md)
- **Guide**: [../../07.guides/04-data/cache-and-kv/README.md](../../07.guides/04-data/cache-and-kv/README.md)
- **Runbook**: [../../09.runbooks/04-data/cache-and-kv/README.md](../../09.runbooks/04-data/cache-and-kv/README.md)
