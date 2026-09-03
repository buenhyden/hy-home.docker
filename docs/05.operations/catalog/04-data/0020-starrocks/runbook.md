---
title: StarRocks Recovery Runbook
version: 1.0.0
type: operation/runbook
layer: operations
status: active
owner: "@buenhyden"
artifact_id: RUN-0020
parent_ids:
  - GDE-0020
created: 2026-05-17
updated: 2026-08-11
---
<!-- Target: docs/05.operations/catalog/04-data/0020-starrocks/runbook.md -->

# StarRocks Recovery Runbook

## Overview

> Scope: StarRocks FE/BE readiness, BE registration evidence, and load retry boundaries.

이 런북은 `starrocks-fe` 또는 `starrocks-be` healthcheck가 실패하거나 BE registration/load job 상태 확인이 필요할 때 사용한다. 현재 compose는 단일 FE/BE pair를 제공한다.

### Purpose

- FE/BE service status를 current compose hostnames로 확인한다.
- BE registration command와 healthcheck evidence를 보존한다.
- load retry와 metadata mutation을 owner approval 없이 수행하지 않는다.

## When to Use

- `SHOW FRONTENDS` or `SHOW BACKENDS` health evidence fails
- `starrocks-be` fails to register with FE
- stream load retry is required

## Procedure

### Checklist

- [ ] compose config renders for warehouses stack.
- [ ] FE and BE logs are preserved before restart.
- [ ] load retry or metadata changes have owner approval.

### Steps

1. Compose file과 repo-local 문서 계약을 확인한다.

   ```bash
   test -f infra/04-data/analytics/warehouses/docker-compose.yml
   python3 scripts/validation/check-document-links.py --mode alignment
   ```

2. FE/BE health evidence를 확인한다.

   ```bash
   mysql -u root -h starrocks-fe -P 9030 -e "SHOW FRONTENDS;"
   mysql -u root -h starrocks-fe -P 9030 -e "SHOW BACKENDS;"
   ```

3. Logs를 확인한다.

   ```bash
   docker logs starrocks-fe --tail 100
   docker logs starrocks-be --tail 100
   ```

4. Restart is allowed only after evidence capture.

   ```bash
   docker restart starrocks-be
   ```

### Verification Steps

- [ ] `SHOW FRONTENDS` reports FE alive.
- [ ] `SHOW BACKENDS` reports `starrocks-be` alive.
- [ ] final evidence records whether restart or escalation was used.

### Observability and Evidence Sources

- **Logs**: `starrocks-fe` and `starrocks-be` logs
- **Metrics**: N/A - no separate exporter is declared in current compose.
- **Evidence**: FE/BE SQL status, logs summary, compose command class

### Safe Rollback or Recovery Procedure

- N/A - no verified FE metadata or data rollback procedure is documented here.
- Metadata restore, backend drop/add, and destructive cleanup must escalate.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: rerun docs validation after docs-only changes.

## Evidence

- Capture FE/BE status, service logs summary, restart decision, and any load label involved.

## Rollback or Recovery

N/A - no verified generic rollback procedure can restore StarRocks metadata or table data from this runbook. Use owner-approved backup or service-specific recovery evidence.

## Escalation

Escalate when FE metadata appears inconsistent, BE registration repeatedly fails, load retry may duplicate data, or destructive data/metadata changes are required.

## Traceability

- Declared parent: [StarRocks Usage Guide](guide.md) (`GDE-0020`)
- Governing authority: [Analytics Tier Architecture Description](../../../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Guide](guide.md) (`GDE-0020`), [Policy](policy.md) (`POL-0020`)

## Related Documents

- [Operations runbooks index](../../../README.md)
- [Usage guide](guide.md)
- [Operations policy](policy.md)
