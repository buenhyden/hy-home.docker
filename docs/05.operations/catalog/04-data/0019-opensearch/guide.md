---
title: OpenSearch Usage Guide
version: 1.0.0
type: operation/guide
layer: operations
status: active
owner: "@buenhyden"
artifact_id: GDE-0019
parent_ids:
  - SPEC-0005
created: 2026-05-10
updated: 2026-08-11
---
<!-- Target: docs/05.operations/catalog/04-data/0019-opensearch/guide.md -->

# OpenSearch Usage Guide

## Usage

### Overview

이 문서는 `infra/04-data/analytics/opensearch`의 OpenSearch 사용 가이드다. 현재 primary compose는 `opensearch`와 `opensearch-dashboards`를 제공하며, `docker-compose.cluster.yml`은 optional cluster variant로 별도 검증한다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- Security Reviewer
- AI Agent

### Purpose

- OpenSearch primary stack과 optional cluster variant를 구분한다.
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
- `test -f infra/04-data/analytics/opensearch/docker-compose.cluster.yml`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](runbook.md)을 따른다.

## Related Documents

- [Operations guides index](../../../README.md)
- [Operations policy](policy.md)
- [Recovery runbook](runbook.md)
- [Infra README](../../../../../infra/04-data/analytics/opensearch/README.md)
