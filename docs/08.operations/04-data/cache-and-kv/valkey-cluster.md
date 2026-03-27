# Valkey Cluster Operations Policy

> Performance and Persistence Controls for Distributed Caching / 분산 캐싱을 위한 성능 및 영속성 통제 정책

## Overview (KR)

이 문서는 Valkey Cluster의 운영 표준, 데이터 보호 정책 및 성능 관리 기준을 정의합니다. 시스템의 안정성과 고가용성을 유지하기 위한 통제 항목을 포함합니다.

This document defines the operational standards, data protection policies, and performance management criteria for the Valkey Cluster. It includes control items to maintain system stability and high availability.

## Policy Scope

Valkey 6노드 분산 클러스터의 영속성(Persistence), 메모리 관리, 보안 및 모니터링 정책을 관리합니다.

## Applies To

- **Systems**: `valkey-cluster` (node 0-5)
- **Agents**: Data Infrastructure Agents, SRE Agents
- **Environments**: Production, Staging

## Controls

- **Required**:
  - `appendonly yes`: 데이터 영속성을 위해 AOF 활성화 필수
  - `maxmemory-policy allkeys-lru`: 메모리 부족 시 LRU 기반 키 제거 정책 적용
  - Docker Secrets을 통한 패스워드 주입 및 인증 필수
- **Allowed**:
  - 특정 노드에 대한 Read-only 복제본 추가 확장
- **Disallowed**:
  - 패스워드 없는 노드 노출 금지
  - 승인되지 않은 외부 네트워크에서의 직접 접속 차단

## Exceptions

- 대량 데이터 마이그레이션 시 초기 속도 향상을 위해 일시적으로 AOF를 끌 수 있으나, 작업 완료 후 즉시 재활성화해야 함.

## Verification

- **Metrics**: Grafana 대시보드에서 `cluster_state:ok` 유무를 실시간 감시합니다.
- **Audit**: 정기적으로 `cluster nodes` 명령을 통해 모든 노드의 연결 상태를 확인합니다.

## Review Cadence

- Quarterly (분기별 운영 데이터 및 장애 이력 검토)

## Related Documents

- **ARD**: [Data Architecture Model](../../02.ard/0004-data-architecture.md)
- **Runbook**: [Valkey Recovery Runbook](../../09.runbooks/04-data/cache-and-kv/valkey-cluster.md)
- **Guide**: [Valkey Cluster Guide](../../07.guides/04-data/cache-and-kv/valkey-cluster.md)
