---
title: "OpenSearch Usage Guide"
version: "2.1.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "GDE-0019"
parent_ids:
- "POL-0019"
implementation_services:
  infra/04-data/opensearch/docker-compose.yml:
  - 'opensearch'
  - 'opensearch-dashboards'
created: "2026-05-10"
---

# OpenSearch Usage Guide

## Overview

정상 `opensearch`는 선택형 단일 노드다. 정상 root는 `infra/04-data/opensearch/docker-compose.yml`의 `opensearch`와 `opensearch-dashboards`만 include한다. 세 노드 학습 구성과 전용 Dashboard는 별도 [LAB Compose](../../../labs/opensearch-cluster.yml)와 [LAB 설명](../../../labs/opensearch-cluster.md)에만 있고 HOME 서비스가 아니다. 소스 분리는 실행 중인 서비스를 중지하거나 복구하지 않는다.

## Audience and Goal

개발자, 운영자, 보안 검토자, AI 에이전트를 위한 문서다. 목표는 다음과 같다.

- 정상 root의 단일 구성과 별도 LAB project의 세 노드를 구분한다.
- HTTPS, Docker Secrets, Traefik route, Dashboards route를 이해한다.
- index 작업 전에 policy와 runbook 인계 지점을 확인한다.

## Usage

### Current implementation

| 항목 | 정상 단일 구성 | 별도 LAB |
| --- | --- | --- |
| 선택 | root `opensearch` profile: `opensearch`, `opensearch-dashboards` | standalone `labs/opensearch-cluster.yml`의 `opensearch-cluster` profile: node1-3, `lab-opensearch-dashboards` |
| 네트워크 | `edge_net`, `obs_net`; 기존 Traefik HTTPS API/Dashboard route | `lab_opensearch_core_net`만 사용; gateway 및 host port 없음 |
| 데이터 | 기존 bind-backed `opensearch-data`, `opensearch-dashboards-data` 보존 | `${LAB_DATA_DIR}/opensearch-cluster/` bind 4개; 정상 데이터 미공유 |
| 인증 | 기존 정상 secret, `${DEFAULT_CERT_DIR}`, OIDC 연동 | 별도 LAB secret과 `${LAB_OPENSEARCH_CERT_DIR}`; 기본 내부 인증만 |
| 구현 | [정상 Compose](../../../infra/04-data/opensearch/docker-compose.yml) | [LAB Compose](../../../labs/opensearch-cluster.yml)와 [LAB 설명](../../../labs/opensearch-cluster.md) |

정상 custom Dockerfile은 OpenSearch 기본 이미지와 exporter plugin을 함께 설치한다. LAB도 같은 Dockerfile을 재사용한다. 양쪽의 실제 이미지 빌드, 인증서 신뢰, health, Dashboard 연결, snapshot/restore는 정적 render로 검증되지 않았다 (미검증). 별도 실행 증거가 나오기 전에는 runtime 준비 상태를 주장하지 않는다. 선택한 service의 resource template과 각 Compose override를 함께 읽고, 같은 호스트의 세 LAB node를 호스트 HA로 간주하지 않는다.

### 준비물과 사용

- Docker Secrets: `opensearch_admin_password`, `opensearch_dashboard_password`, `opensearch_security_cookie`
- 정상 인증서 bind 경로와 별도 LAB 인증서 경로
- `infra/04-data/opensearch/docker-compose.yml`, `labs/opensearch-cluster.yml`

1. 선택한 Compose entrypoint 위치를 확인한다.

   ```bash
   test -f infra/04-data/opensearch/docker-compose.yml
   test -f labs/opensearch-cluster.yml
   ```

2. Cluster health는 HTTPS와 admin secret으로 확인한다. 인증된 cluster 읽기는 [해당 Runbook](../runbooks/0019-opensearch.md#procedure)의 private TTY/client prompt 절차를 따른다. source build/config 한계를 해결·검증하기 전에는 성공을 가정하지 않는다.
3. 정상 Dashboards만 `opensearch-dashboard.${DEFAULT_URL}` Traefik host rule을 사용한다. LAB Dashboard에는 그 route가 없다.
4. 인덱스는 도메인별 패턴을 따른다(예: `logs-*-*`).

### 주의점

- 정상 project의 `opensearch`와 별도 LAB project의 `opensearch-node1..3`을 혼용하지 않는다.
- HTTP로 `9200`을 호출하지 않는다.
- admin password를 command line literal이나 문서에 남기지 않는다.

### Common Checks

- `test -f infra/04-data/opensearch/docker-compose.yml`
- `test -f labs/opensearch-cluster.yml`
- `docker compose -f labs/opensearch-cluster.yml --profile opensearch-cluster config --quiet`
- 원격 PR public `changed` 검사 ([quality policy](../../../.agents/governance/quality-standards.md#canonical-delivery-phase-matrix))

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0019-opensearch.md)을 따른다.

### Traceability

- Declared parent: [OpenSearch Operations Policy](../policies/0019-opensearch.md) (`POL-0019`)
- Governing authority: [Analytics Tier Architecture Description](../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Policy](../policies/0019-opensearch.md) (`POL-0019`), [Runbook](../runbooks/0019-opensearch.md) (`RUN-0019`)

## Related Documents

- [OpenSearch snapshot and restore](https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/)
- [OpenSearch upgrade guidance](https://docs.opensearch.org/latest/install-and-configure/upgrade-opensearch/index/)
- [OpenSearch source and Apache-2.0 licence](https://github.com/opensearch-project/OpenSearch)
- Runtime pins: Compose/Dockerfile 선언이 authoritative하며, [derived Compose image projection](../../../infra/tech-stack.versions.json)이 drift 검증을 제공한다.
- [Operations guides index](../README.md)
- [Operations policy](../policies/0019-opensearch.md)
- [Recovery runbook](../runbooks/0019-opensearch.md)
- [Infra README](../../../infra/04-data/opensearch/README.md)
- [Compose implementation: infra/04-data/opensearch/docker-compose.yml](../../../infra/04-data/opensearch/docker-compose.yml)
- [LAB Compose implementation](../../../labs/opensearch-cluster.yml)
- [LAB 설명](../../../labs/opensearch-cluster.md)
