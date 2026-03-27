# Cache & Key-Value Stores (04-data/cache-and-kv)

> Distributed Caching and Fast Key-Value Storage Services

## Overview

This directory contains infrastructure configurations for caching and key-value storage services. These services are optimized for high-performance data access and transient state management.

## Structure

```text
cache-and-kv/
├── valkey-cluster/       # 6-node 분산 클러스터 (Primary + Replica)
└── README.md
```

## Documentation

- **Guides**: [valkey-cluster.md](../../../docs/07.guides/04-data/cache-and-kv/valkey-cluster.md)
- **Operations**: [valkey-cluster.md](../../../docs/08.operations/04-data/cache-and-kv/valkey-cluster.md)
- **Runbooks**: [valkey-cluster.md](../../../docs/09.runbooks/04-data/cache-and-kv/valkey-cluster.md)

## Tech Stack

- **Valkey**: 고성능 오픈소스 데이터 저장소 (Redis-compatible).
- **Topology**: 3 Primary + 3 Replica 구성을 통한 고가용성 보장.

---
Copyright (c) 2026. Licensed under the MIT License.
