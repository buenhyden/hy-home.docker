---
title: "OpenSearch Usage Guide"
version: "1.0.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0019"
parent_ids:
- "POL-0019"
implementation_services:
  infra/04-data/analytics/opensearch/docker-compose.yml:
  - 'opensearch'
  - 'opensearch-dashboards'
  - 'opensearch-node1'
  - 'opensearch-node2'
  - 'opensearch-node3'
created: "2026-05-10"
---

# OpenSearch Usage Guide

## Usage

`opensearch-node2` is the second cluster node; it belongs to the optional clustered topology and is not required for the single-node HOME baseline.

### Overview

이 문서는 `infra/04-data/analytics/opensearch`의 OpenSearch 사용 가이드다. compose 파일 하나가 두 topology를 담는다. `opensearch` profile은 `opensearch`와 `opensearch-dashboards`를, `opensearch-cluster` profile은 `opensearch-node1`부터 `opensearch-node3`까지와 dashboards를 선택하며, cluster topology는 별도로 검증한다.

### Current implementation

| Field | Primary / cluster contract |
| --- | --- |
| Classification | `opensearch` is OPTIONAL; the three same-host nodes and shared Dashboards path are LAB. Same-host node count is not host HA. |
| Source and updater | [Compose](../../../infra/04-data/analytics/opensearch/docker-compose.yml) and its [Dockerfile](../../../infra/04-data/analytics/opensearch/Dockerfile) own the engine build; Compose owns Dashboards; Renovate owns update proposals. |
| Network and exposure | All services join the declared networks. Primary API and Dashboards use TLS backends through Traefik and `gateway-standard-chain@file`; the cluster variant also publishes Performance Analyzer port `9600` from node1. |
| Persistence | Primary uses bind-backed `opensearch-data`; Dashboards uses `opensearch-dashboards-data`; cluster nodes use `opensearch-data1..3`. Certificates and security configuration are separate read-only mounts. |
| Credentials | Admin, Dashboards, exporter, cookie, and OAuth client secrets are declared as applicable. Health uses the admin secret without printing it. |
| Health and resources | Engine health requires yellow or better; Dashboards accepts `200` or `401`. Primary inherits 2 CPUs/2 GiB; each cluster node also inherits 2 CPUs/2 GiB, so selection is resource-heavy. |
| Backup and upgrade | Use the snapshot API with a registered repository; exclude the security index and preserve security configuration separately. Restore to a compatible isolated topology, then apply security config deliberately. Review the documented upgrade path before changing engine/Dashboards versions. |

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- Security Reviewer
- AI Agent

### Purpose

- `opensearch` profile의 primary stack과 `opensearch-cluster` profile의 three-node topology를 구분한다.
- HTTPS, Docker Secrets, Traefik route, Dashboards route를 이해한다.
- index 작업 전 policy/runbook handoff를 확인한다.

### Prerequisites

- Docker Secrets: `opensearch_admin_password`, `opensearch_dashboard_password`, `opensearch_security_cookie`
- certificate bind mount under `secrets/certs`
- `infra/04-data/analytics/opensearch/docker-compose.yml`

### Step-by-step Instructions

1. Primary compose contract 위치를 확인한다.

   ```bash
   test -f infra/04-data/analytics/opensearch/docker-compose.yml
   ```

2. Cluster health는 HTTPS와 admin secret으로 확인한다.

   ```bash
   read -rsp "OpenSearch admin password: " OPENSEARCH_ADMIN_PASSWORD; echo
   curl -fsSk -u "admin:${OPENSEARCH_ADMIN_PASSWORD}" "https://opensearch:9200/_cluster/health"
   unset OPENSEARCH_ADMIN_PASSWORD
   ```

3. Dashboards route는 `opensearch-dashboard.${DEFAULT_URL}` Traefik host rule을 사용한다.

### Common Pitfalls

- primary service name `opensearch`와 cluster variant service names `opensearch-node1..3`을 혼용하는 경우
- HTTP로 `9200`을 호출하는 경우
- admin password를 command line literal이나 문서에 남기는 경우

- 인덱스는 도메인별 패턴을 따른다(예: `logs-*-*`).

## Common Checks

- `test -f infra/04-data/analytics/opensearch/docker-compose.yml`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0019-opensearch.md)을 따른다.

## Traceability

- Declared parent: [OpenSearch Operations Policy](../policies/0019-opensearch.md) (`POL-0019`)
- Governing authority: [Analytics Tier Architecture Description](../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Policy](../policies/0019-opensearch.md) (`POL-0019`), [Runbook](../runbooks/0019-opensearch.md) (`RUN-0019`)

## Related Documents

- [OpenSearch snapshot and restore](https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/)
- [OpenSearch upgrade guidance](https://docs.opensearch.org/latest/install-and-configure/upgrade-opensearch/index/)
- [OpenSearch source and Apache-2.0 licence](https://github.com/opensearch-project/OpenSearch)

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations guides index](../README.md)
- [Operations policy](../policies/0019-opensearch.md)
- [Recovery runbook](../runbooks/0019-opensearch.md)
- [Infra README](../../../infra/04-data/analytics/opensearch/README.md)
- [Compose implementation: infra/04-data/analytics/opensearch/docker-compose.yml](../../../infra/04-data/analytics/opensearch/docker-compose.yml)
