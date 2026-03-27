# Cache and KV Runbooks (04-data/cache-and-kv)

> Incident Response and Recovery for Caching Services / 분산 캐시 및 Key-Value 저장소 장애 복구 런북

## Overview (KR)

이 경로는 Valkey, Redis 등 캐시 및 KV 저장소 계층의 서비스들에서 발생할 수 있는 장애 상황에 대응하기 위한 실행 지침을 포함한다. 신속한 서비스 복구와 데이터 무결성 유지를 목적으로 한다.

This path contains operational instructions for responding to failure situations that may occur in services in the cache and KV storage layer, such as Valkey and Redis. It aims for rapid service recovery and maintenance of data integrity.

## Audience

이 README의 주요 독자:
- 긴급 장애 조치를 수행하는 **Operators / SRE**
- 복구 절차를 학습하는 **AI Agents**
- 시스템 안정성을 검증하는 **QA Engineers**

## Scope

### In Scope
- Valkey Cluster 노드 장애 복구
- 클러스터 슬롯 불일치 해결 절차
- 네트워크 파티션 및 정족수 복구

### Out of Scope
- 관계형 DB 복구 (relational/ 참조)
- 애플리케이션 코드 버그 수정
- 클라우드 인프라(AWS/GCP) 레벨 복구

## Structure

```text
cache-and-kv/
├── valkey-cluster.md    # Valkey Cluster 장애 복구 런북
└── README.md            # 이 파일
```

## How to Work in This Area

1. 장애 발생 시 [valkey-cluster.md](./valkey-cluster.md)의 진단 단계를 즉시 수행합니다.
2. 모든 복구 작업은 수행 전후로 [Operations](../../08.operations/04-data/cache-and-kv/README.md) 정책을 준수하는지 확인합니다.

## Available Runbooks

- [Valkey Cluster Runbook](./valkey-cluster.md): 노드 장애, 슬롯 오류 복구 절차.

## Related References

- **Implementation**: [infra/04-data/cache-and-kv/README.md](../../../../infra/04-data/cache-and-kv/README.md)
- **Guide**: [04-data Guides](../../07.guides/04-data/cache-and-kv/README.md)
- **Operation**: [04-data Operations](../../08.operations/04-data/cache-and-kv/README.md)
