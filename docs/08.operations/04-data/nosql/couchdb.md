<!-- Target: docs/08.operations/04-data/nosql/couchdb.md -->

# CouchDB Operation Policy

> Operational standards for managing a 3-node CouchDB cluster with replication focus.

---

## Overview (KR)

이 문서는 CouchDB 클러스터의 데이터 정합성 유지, 디스크 최적화(Compaction), 그리고 멀티 마스터 복제 환경에서의 운영 정책을 정의한다.

## Policy Type

`operational-standard`

## Target Audience

- Operator
- SRE
- Developer

## Purpose

클러스터 내 데이터 불일치를 방지하고, 지속적인 서비스 가용성을 보장하며, 리소스 효율적인 안정 운영을 목표로 한다.

## Service Level Objectives (SLO)

- **Availability**: 99.9% (Cluster consensus maintained)
- **Data Integrity**: Zero loss during node rotation
- **API Response**: 99th percentile < 500ms for standard requests

## Operational Procedures

### 1. Monitoring & Health Check

- **Endpoint**: `https://couchdb.${DEFAULT_URL}/_membership` 호출을 통해 모든 노드가 클러스터에 참여 중인지 확인한다.
- **Alerts**: 특정 노드의 `_up` 상태가 1분 이상 지속되지 않을 경우 경고 발생.

### 2. Disk Management (Compaction)

CouchDB는 Append-only 데이터베이스이므로 정기적인 압축 작업이 필수적이다.
- **Auto-compaction**: 배포 시 설정된 자동 압축 정책(Fragmentation threshold 30%)이 정상 작동하는지 모니터링한다.
- **Manual Trigger**: 디스크 부족 경고 시 `/database/_compact` API를 통해 강제 압축을 수행한다.

### 3. Backup & DR

- **CouchDB Replication**: 중요한 데이터베이스는 별도의 오프사이트(Off-site) CouchDB 인스턴스로 실시간 또는 정기 복제를 설정한다.
- **Metadata Backup**: `_users`, `_replicator` 시스템 데이터베이스를 정기적으로 백업한다.

## Common Pitfalls

- **Revision Sprawl**: 너무 잦은 업데이트는 `_rev` 기록을 방대하게 만들어 뷰 인덱싱 성능을 저하시킨다. 정기적인 리비전 제한 수(`revs_limit`) 설정을 검토한다.
- **Shared Secret Conflict**: 클러스터 노드 간 `COUCHDB_SECRET`이 일치하지 않으면 노드 간 통신 및 복제가 실패한다.

## Related Documents

- **Infrastructure**: [CouchDB Infrastructure](../../../infra/04-data/nosql/couchdb/README.md)
- **Guide**: [CouchDB Cluster Guide](../../../docs/07.guides/04-data/nosql/couchdb.md)
- **Runbook**: [CouchDB Recovery Runbook](../../../docs/09.runbooks/04-data/nosql/couchdb.md)
