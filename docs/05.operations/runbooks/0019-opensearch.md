---
title: "OpenSearch Recovery Runbook"
version: "1.1.3"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0019"
parent_ids:
- "GDE-0019"
created: "2026-05-17"
---

# OpenSearch Recovery Runbook

## Overview

> Scope: OpenSearch primary stack readiness, HTTPS health check, `opensearch-cluster` topology evidence.

이 런북은 OpenSearch primary stack(`opensearch` profile) 또는 three-node topology(`opensearch-cluster` profile)의 health/readiness 문제가 있을 때 사용한다. Primary stack은 `opensearch`; three-node topology는 `opensearch-node1..3` service names를 사용한다.

### Purpose

- HTTPS와 Docker Secret 기반 healthcheck를 사용한다.
- primary stack과 cluster variant를 혼동하지 않는다.
- index/shard 작업 전 snapshot or escalation evidence를 확보한다.

## When to Use

- primary `opensearch` healthcheck가 실패할 때
- Dashboards가 OpenSearch에 연결할 수 없을 때
- `opensearch-cluster` topology에 unhealthy node나 shard allocation 문제가 있을 때

## Procedure

### Checklist

- [ ] `data` 단독인지 `opensearch-cluster`까지 선택했는지 기록했다.
- [ ] admin password is read securely and not persisted.
- [ ] index or shard mutation requires owner approval.

### Steps

1. primary compose file과 repo-local 문서 계약을 확인한다.

   ```bash
   test -f infra/04-data/analytics/opensearch/docker-compose.yml
   python3 scripts/validation/check-document-links.py --mode all
   ```

2. primary health를 HTTPS로 확인한다.

   ```bash
   read -rsp "OpenSearch admin password: " OPENSEARCH_ADMIN_PASSWORD; echo
   curl -fsSk -u "admin:${OPENSEARCH_ADMIN_PASSWORD}" "https://opensearch:9200/_cluster/health?pretty"
   unset OPENSEARCH_ADMIN_PASSWORD
   ```

3. Logs를 확인한다.

   ```bash
   docker compose --profile opensearch logs --tail 100 opensearch opensearch-dashboards
   ```

4. cluster 구성은 같은 compose 파일의 `opensearch-cluster` profile로 확인한다.

   ```bash
   docker compose --profile opensearch-cluster config --quiet
   docker compose --profile opensearch-cluster logs --tail 100 opensearch-node1 opensearch-node2 opensearch-node3
   ```

### Verification Steps

- [ ] health endpoint가 primary stack에 대해 최소 yellow 상태를 반환한다.
- [ ] Dashboards health endpoint가 compose healthcheck가 허용하는 `200` 또는 `401`을 반환한다.
- [ ] 최종 evidence에 primary 또는 cluster variant 중 어느 것을 점검했는지 명시한다.

### Observability and Evidence Sources

- **Logs**: OpenSearch와 Dashboards compose log
- **Metrics**: 별도 exporter가 실행 중이지 않으면 N/A
- **Evidence**: health 응답, 선택한 compose file, service log 요약, secret boundary 확인

### Planned isolated snapshot restore

이 절차는 upstream guidance를 바탕으로 문서화된 것이며 **이 task에서 실행되지 않았다**.

1. 선택한 topology, cluster UUID/version, index inventory, shard health, repository plugin/configuration, encryption과 credential owner, 가용 disk, 승인된 restore 목적지를 기록한다. tracked security configuration과 certificate는 별도로 보존한다.
2. least-privilege credential로 live data volume 밖의 repository를 등록하거나 검증한다. `.opendistro_security`를 제외한 named snapshot을 만들고 `SUCCESS`를 기다린 뒤 포함된 index와 실패 내역을 기록한다. live data-directory copy에 의존하지 않는다.
3. 빈 volume, 별도의 cluster 이름, production router 없이 호환되는 새 isolated primary 또는 cluster topology를 준비한다. credential을 노출하지 않고 동일한 repository를 등록한다.
4. 선택한 application index를 임시 이름으로 또는 빈 target에 복원한다. 검토된 security configuration은 별도로 적용하며, security index를 맹목적으로 복원하지 않는다.
5. 상황에 맞게 green/yellow cluster health, shard allocation, 예상 index/document count, 대표 검색, Dashboards 연결성, TLS, role, 예기치 않은 write alias 부재를 확인한다.
6. restore 또는 security validation이 실패하면 isolated volume만 중지하고 폐기한 뒤 변경되지 않은 snapshot에서 재시도한다. 강제 복구를 위해 shard를 reroute하거나 active index를 덮어쓰지 않는다.
7. cutover, alias 변경, snapshot 삭제, active-cluster restore는 별도 approval이 필요하다. rehearsal이 성공을 기록하기 전까지 restore는 검증되지 않은 상태다.

## Evidence

- compose file, service 이름, health 상태, 로그 요약, escalation 결정을 기록한다.
- password 값은 기록하지 않는다.

## Rollback or Recovery

rehearsal의 rollback은 source cluster와 snapshot을 변경하지 않은 채 isolated topology를 폐기하는 것이다. cutover plan은 source를 유지하고 alias/DNS 전환을 별도로 정의해야 한다.

## Escalation

health가 계속 red/unavailable이거나, shard 변경이 필요하거나, secret이나 cert가 없거나, primary와 cluster variant evidence가 충돌할 때 escalation한다.

## Traceability

- Declared parent: [OpenSearch Usage Guide](../guides/0019-opensearch.md) (`GDE-0019`)
- Governing authority: [Analytics Tier Architecture Description](../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Guide](../guides/0019-opensearch.md) (`GDE-0019`), [Policy](../policies/0019-opensearch.md) (`POL-0019`)

## Related Documents

- [Compose implementation: infra/04-data/analytics/opensearch/docker-compose.yml](../../../infra/04-data/analytics/opensearch/docker-compose.yml)
- [Custom image source: infra/04-data/analytics/opensearch/Dockerfile](../../../infra/04-data/analytics/opensearch/Dockerfile)

- [OpenSearch snapshot and restore](https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/)
- [Compose implementation](../../../infra/04-data/analytics/opensearch/docker-compose.yml)

- [Operations runbooks index](../README.md)
- [Usage guide](../guides/0019-opensearch.md)
- [Operations policy](../policies/0019-opensearch.md)
