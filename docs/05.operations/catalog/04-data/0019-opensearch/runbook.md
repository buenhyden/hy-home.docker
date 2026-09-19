---
title: "OpenSearch Recovery Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0019"
parent_ids:
- "GDE-0019"
created: "2026-05-17"
---

# OpenSearch Recovery Runbook

## Overview

> Scope: OpenSearch primary stack readiness, HTTPS health checks, and `opensearch-cluster` topology evidence.

이 런북은 OpenSearch primary stack(`opensearch` profile) 또는 three-node topology(`opensearch-cluster` profile)의 health/readiness 문제가 있을 때 사용한다. Primary stack은 `opensearch`; three-node topology는 `opensearch-node1..3` service names를 사용한다.

### Purpose

- HTTPS와 Docker Secret 기반 healthcheck를 사용한다.
- primary stack과 cluster variant를 혼동하지 않는다.
- index/shard 작업 전 snapshot or escalation evidence를 확보한다.

## When to Use

- primary `opensearch` healthcheck fails
- Dashboards cannot connect to OpenSearch
- `opensearch-cluster` topology has unhealthy node or shard allocation issues

## Procedure

### Checklist

- [ ] `data` 단독인지 `opensearch-cluster`까지 선택했는지 기록했다.
- [ ] admin password is read securely and not persisted.
- [ ] index or shard mutation requires owner approval.

### Steps

1. Primary compose file과 repo-local 문서 계약을 확인한다.

   ```bash
   test -f infra/04-data/analytics/opensearch/docker-compose.yml
   python3 scripts/validation/check-document-links.py --mode all
   ```

2. Primary health를 HTTPS로 확인한다.

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

- [ ] health endpoint returns at least yellow status for primary stack.
- [ ] Dashboards health endpoint returns `200` or `401` as accepted by compose healthcheck.
- [ ] final evidence states whether primary or cluster variant was inspected.

### Observability and Evidence Sources

- **Logs**: OpenSearch and Dashboards compose logs
- **Metrics**: N/A unless a separate exporter is running
- **Evidence**: health response, compose file selected, service logs summary, secret boundary confirmation

### Planned isolated snapshot restore

This procedure is documented from upstream guidance and **was not executed in this task**.

1. Record the selected topology, cluster UUID/version, index inventory, shard health, repository plugin/configuration, encryption and credential owner, free disk, and an approved restore destination. Preserve the tracked security configuration and certificates separately.
2. Register or verify a repository outside the live data volumes with the least-privilege credential. Create a named snapshot that excludes `.opendistro_security`, wait for `SUCCESS`, and record included indices plus failures. Do not rely on a live data-directory copy.
3. Provision a fresh compatible isolated primary or cluster topology with empty volumes, a distinct cluster name, and no production router. Register the same repository without exposing credentials.
4. Restore selected application indices under temporary names or into the empty target. Apply reviewed security configuration separately; never restore the security index blindly.
5. Verify green/yellow cluster health as appropriate, shard allocation, expected index/document counts, representative searches, Dashboards connectivity, TLS, roles, and absence of unexpected write aliases.
6. If restore or security validation fails, stop and discard only the isolated volumes, then retry from the unchanged snapshot. Do not reroute shards or overwrite active indices to force recovery.
7. Cutover, alias mutation, snapshot deletion, or active-cluster restore requires separate approval. Restore remains unverified until a rehearsal records success.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: stop if secret values appear in output.
- **Eval Re-run**: rerun docs validation after docs-only changes.

## Evidence

- Capture compose file, service names, health status, log summary, and escalation decision.
- Do not capture password values.

## Rollback or Recovery

Rollback from rehearsal is disposal of the isolated topology while the source cluster and snapshot remain unchanged. A cutover plan must retain the source and define alias/DNS reversal independently.

## Escalation

Escalate when health remains red/unavailable, shard mutation is needed, secrets or certs are missing, or primary and cluster variant evidence conflict.

## Traceability

- Declared parent: [OpenSearch Usage Guide](guide.md) (`GDE-0019`)
- Governing authority: [Analytics Tier Architecture Description](../../../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Guide](guide.md) (`GDE-0019`), [Policy](policy.md) (`POL-0019`)

## Related Documents

- [Compose implementation: infra/04-data/analytics/opensearch/docker-compose.yml](../../../../../infra/04-data/analytics/opensearch/docker-compose.yml)
- [Custom image source: infra/04-data/analytics/opensearch/Dockerfile](../../../../../infra/04-data/analytics/opensearch/Dockerfile)

- [OpenSearch snapshot and restore](https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/)
- [Compose implementation](../../../../../infra/04-data/analytics/opensearch/docker-compose.yml)

- [Operations runbooks index](../../../README.md)
- [Usage guide](guide.md)
- [Operations policy](policy.md)
