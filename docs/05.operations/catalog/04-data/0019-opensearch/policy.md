---
title: "OpenSearch Operations Policy"
version: "1.0.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-15"
layer: "operations"
artifact_id: "POL-0019"
parent_ids:
- "AD-0012"
created: "2026-05-17"
---

# OpenSearch Operations Policy

## Overview

이 문서는 `infra/04-data/analytics/opensearch`의 OpenSearch 운영 정책을 정의한다. current implementation은 OpenSearch 3.x custom build primary stack과 OpenSearch Dashboards 3.8.0을 사용하며, three-node cluster topology는 같은 Compose 파일에서 `opensearch-cluster` profile이 선택한다.

## Policy Scope

- **Systems**: `opensearch`, `opensearch-dashboards`, and `opensearch-node1..3` under the `opensearch-cluster` profile
- **Secrets**: `opensearch_admin_password`, `opensearch_dashboard_password`, `opensearch_exporter_password`, `opensearch_security_cookie`, `oauth2_proxy_client_secret`
- **Persistence**: `opensearch-data`, `opensearch-dashboards-data`, `opensearch-cluster` profile node volumes
- **Environments**: repo-local, development, homelab, and production-like rehearsals

## Controls

- **Required**: OpenSearch API checks must use HTTPS and secret-backed admin authentication.
- **Required**: primary stack operations must target `opensearch`; cluster-variant operations must explicitly target `opensearch-node1..3`.
- **Required**: secret values and generated internal user material must not be copied into docs or command history.
- **Allowed**: cluster topology validation when the command selects the `opensearch-cluster` profile.
- **Disallowed**: unauthenticated bulk load, HTTP-only health checks, or claims that a replica policy exists without index/ISM evidence.

## Exceptions

Temporary index settings, cluster variant experiments, or security config changes require owner approval and before/after health evidence.

## Verification

- `test -f infra/04-data/analytics/opensearch/docker-compose.yml`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Review Cadence

- On image/build, certificate, secret, security config, or cluster topology change
- Quarterly for documented recovery evidence

## Traceability

- Declared parent: [Analytics Tier Architecture Description](../../../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Guide](guide.md) (`GDE-0019`), [Runbook](runbook.md) (`RUN-0019`)

## Related Documents

- [Operations policies index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
- [Infra README](../../../../../infra/04-data/analytics/opensearch/README.md)
