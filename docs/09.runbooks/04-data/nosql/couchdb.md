<!-- Target: docs/09.runbooks/04-data/nosql/couchdb.md -->

# CouchDB Recovery Runbook

> Emergency recovery procedures for CouchDB Cluster and node synchronization issues.

---

## Overview (KR)

이 문서는 CouchDB 클러스터 정족수 상실, 노드 간 복제 중단, 또는 데이터 정합성 이슈 발생 시의 복구 절차를 정의한다.

## Runbook Type

`incident-response`

## Target Audience

- On-call Engineer
- SRE
- AI-Agent

## Purpose

CouchDB 클러스터의 고가용성 상태를 복구하고, 노드 간 데이터 불일치를 해결하여 안정적인 문서 동기화 환경을 재구축한다.

## Pre-remediation Checklist

- [ ] `https://couchdb.${DEFAULT_URL}/_membership` 결과 분석
- [ ] 노드 간 HTTP 통신(Port 5984) 및 Cluster 통신(Port 4369, 5986) 확인
- [ ] `couchdb_secret`이 모든 노드에서 동일한지 확인

## Remediation Steps

### Scenario 1: Node Out-of-Sync (Re-joining Cluster)

클러스터에서 이탈한 노드를 다시 조인시킨다.

1. 로그 확인: `docker logs couchdb-node1`
2. 노드 재시작:
   ```bash
   docker-compose restart couchdb-node1
   ```
3. 클러스터 수동 조인 (필요 시):
   (Setup API를 통해 이탈한 노드의 IP/Port를 다시 추가)

### Scenario 2: High Fragmentation (Manual Compaction)

디스크 부족으로 인한 쓰기 거부 시 압축을 수행한다.

1. 모든 데이터베이스 목록 확인:
   ```bash
   curl -u ${USER}:${PASS} https://couchdb.${DEFAULT_URL}/_all_dbs
   ```
2. 특정 DB 압축 실행:
   ```bash
   curl -H "Content-Type: application/json" -X POST -u ${USER}:${PASS} \
        https://couchdb.${DEFAULT_URL}/<db_name>/_compact
   ```

## Verification Steps

1. 클러스터 동기화 지연 확인:
   ```bash
   curl -u ${USER}:${PASS} https://couchdb.${DEFAULT_URL}/_scheduler/docs
   ```
2. 특정 문서 리비전 일치 여부 확인 (각 노드별 직접 쿼리).

## Post-remediation Tasks

- `revs_limit` 정책 적정성 검토
- 디스크 자동 확장 트리거 점검
- 공유 시크릿(Secret) 관리 상태 재확인

## Related Documents

- **Guide**: [CouchDB Cluster Guide](../../../docs/07.guides/04-data/nosql/couchdb.md)
- **Operation**: [CouchDB Operation Policy](../../../docs/08.operations/04-data/nosql/couchdb.md)
