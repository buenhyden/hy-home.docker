# Cache and KV Runbooks

> 분산 캐시 및 Key-Value 저장소 장애 복구 런북.

## Overview

이 경로는 Valkey, Redis 등 캐시 및 KV 저장소 계층의 서비스들에서 발생할 수 있는 장애 상황에 대응하기 위한 실행 지침을 포함한다.

## Structure

```text
cache-and-kv/
├── valkey-cluster.md    # Valkey Cluster 장애 복구 런북
└── README.md            # 이 파일
```

## Available Runbooks

- [Valkey Cluster Runbook](./valkey-cluster.md): 노드 장애, 슬롯 오류 복구 절차.

## Related References

- **Implementation**: [../../../../infra/04-data/cache-and-kv/README.md](../../../../infra/04-data/cache-and-kv/README.md)
- **Guide**: [../../07.guides/04-data/cache-and-kv/README.md](../../07.guides/04-data/cache-and-kv/README.md)
- **Operation**: [../../08.operations/04-data/cache-and-kv/README.md](../../08.operations/04-data/cache-and-kv/README.md)
