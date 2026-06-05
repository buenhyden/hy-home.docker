---
status: active
---
<!-- Target: docs/05.operations/policies/04-data/analytics/opensearch.md -->

# OpenSearch Operations Policy

## Overview

이 문서는 `infra/04-data/analytics/opensearch`의 OpenSearch 운영 정책을 정의한다. current implementation은 OpenSearch 3.x custom build primary stack과 OpenSearch Dashboards 3.6.0을 사용하며, three-node cluster compose는 optional variant다.

## Policy Scope

- **Systems**: `opensearch`, `opensearch-dashboards`, optional `opensearch-node1..3`
- **Secrets**: `opensearch_admin_password`, `opensearch_dashboard_password`, `opensearch_exporter_password`, `opensearch_security_cookie`, `oauth2_proxy_client_secret`
- **Persistence**: `opensearch-data`, `opensearch-dashboards-data`, optional cluster node volumes
- **Environments**: repo-local, development, homelab, and production-like rehearsals

## Controls

- **Required**: OpenSearch API checks must use HTTPS and secret-backed admin authentication.
- **Required**: primary stack operations must target `opensearch`; cluster-variant operations must explicitly target `opensearch-node1..3`.
- **Required**: secret values and generated internal user material must not be copied into docs or command history.
- **Allowed**: optional cluster variant validation when the command names `docker-compose.cluster.yml`.
- **Disallowed**: unauthenticated bulk load, HTTP-only health checks, or claims that a replica policy exists without index/ISM evidence.

## Exceptions

Temporary index settings, cluster variant experiments, or security config changes require owner approval and before/after health evidence.

## Verification

- `test -f infra/04-data/analytics/opensearch/docker-compose.yml`
- `test -f infra/04-data/analytics/opensearch/docker-compose.cluster.yml`
- `bash scripts/validation/check-repo-contracts.sh`

## Review Cadence

- On image/build, certificate, secret, security config, or cluster topology change
- Quarterly for documented recovery evidence

## Related Documents

- [Operations policies index](../../../README.md)
- [Usage guide](../../../guides/04-data/analytics/opensearch.md)
- [Recovery runbook](../../../runbooks/04-data/analytics/opensearch.md)
- [Infra README](../../../../../infra/04-data/analytics/opensearch/README.md)
