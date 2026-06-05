---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/analytics/opensearch.md -->

# OpenSearch Recovery Runbook

## OpenSearch Recovery Procedure

> Scope: OpenSearch primary stack readiness, HTTPS health checks, and optional cluster variant evidence.

### Overview

이 런북은 OpenSearch primary stack 또는 optional cluster variant의 health/readiness 문제가 있을 때 사용한다. Primary stack은 `opensearch`; cluster variant는 `opensearch-node1..3` service names를 사용한다.

### Purpose

- HTTPS와 Docker Secret 기반 healthcheck를 사용한다.
- primary stack과 cluster variant를 혼동하지 않는다.
- index/shard 작업 전 snapshot or escalation evidence를 확보한다.

### Canonical References

- **Spec**: [Analytics spec](../../../../03.specs/04-data-analytics/spec.md)
- **Policy**: [OpenSearch policy](../../../policies/04-data/analytics/opensearch.md)
- **Guide**: [OpenSearch guide](../../../guides/04-data/analytics/opensearch.md)

## When to Use

- primary `opensearch` healthcheck fails
- Dashboards cannot connect to OpenSearch
- optional cluster variant has unhealthy node or shard allocation issues

## Procedure

### Checklist

- [ ] primary compose or cluster compose selection is recorded.
- [ ] admin password is read securely and not persisted.
- [ ] index or shard mutation requires owner approval.

### Steps

1. Primary compose file과 repo-local 문서 계약을 확인한다.

   ```bash
   test -f infra/04-data/analytics/opensearch/docker-compose.yml
   bash scripts/validation/check-doc-implementation-alignment.sh
   ```

2. Primary health를 HTTPS로 확인한다.

   ```bash
   read -rsp "OpenSearch admin password: " OPENSEARCH_ADMIN_PASSWORD; echo
   curl -fsSk -u "admin:${OPENSEARCH_ADMIN_PASSWORD}" "https://opensearch:9200/_cluster/health?pretty"
   unset OPENSEARCH_ADMIN_PASSWORD
   ```

3. Logs를 확인한다.

   ```bash
   docker logs opensearch --tail 100
   docker logs opensearch-dashboards --tail 100
   ```

4. Optional cluster variant는 별도 compose로 확인한다.

   ```bash
   test -f infra/04-data/analytics/opensearch/docker-compose.cluster.yml
   ```

### Verification Steps

- [ ] health endpoint returns at least yellow status for primary stack.
- [ ] Dashboards health endpoint returns `200` or `401` as accepted by compose healthcheck.
- [ ] final evidence states whether primary or cluster variant was inspected.

### Observability and Evidence Sources

- **Logs**: OpenSearch and Dashboards compose logs
- **Metrics**: N/A unless a separate exporter is running
- **Evidence**: health response, compose file selected, service logs summary, secret boundary confirmation

### Safe Rollback or Recovery Procedure

- N/A - no verified index/shard rollback procedure is documented here.
- Snapshot, shard routing, or security config changes must escalate before execution.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: stop if secret values appear in output.
- **Eval Re-run**: rerun docs validation after docs-only changes.

## Evidence

- Capture compose file, service names, health status, log summary, and escalation decision.
- Do not capture password values.

## Rollback or Recovery

N/A - no verified generic rollback procedure can restore OpenSearch index or security state from this runbook. Use approved snapshot/security recovery evidence if mutation is required.

## Escalation

Escalate when health remains red/unavailable, shard mutation is needed, secrets or certs are missing, or primary and cluster variant evidence conflict.

## Related Documents

- [Operations runbooks index](../../../README.md)
- [Usage guide](../../../guides/04-data/analytics/opensearch.md)
- [Operations policy](../../../policies/04-data/analytics/opensearch.md)
