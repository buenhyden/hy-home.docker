---
title: "OpenSearch Usage Guide"
version: "1.0.6"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0019"
parent_ids:
- "POL-0019"
implementation_services:
  infra/04-data/opensearch/docker-compose.yml:
  - 'opensearch'
  - 'opensearch-dashboards'
  - 'opensearch-node1'
  - 'opensearch-node2'
  - 'opensearch-node3'
created: "2026-05-10"
---

# OpenSearch Usage Guide

## Usage

`opensearch-node2`는 두 번째 cluster node이다. 이 node는 optional clustered topology에 속하며 single-node OPTIONAL topology에는 필요하지 않다.

### Overview

이 문서는 `infra/04-data/opensearch`의 OpenSearch 사용 가이드다. compose 파일 하나가 두 topology를 담는다. `opensearch` profile은 `opensearch`와 `opensearch-dashboards`를, `opensearch-cluster` profile은 `opensearch-node1`부터 `opensearch-node3`까지와 dashboards를 선택하며, cluster topology는 별도로 검증한다.

### Current implementation

| Field | Primary / cluster contract |
| --- | --- |
| Classification | `opensearch`는 OPTIONAL이다. 동일 host의 세 node와 공유 Dashboards path는 LAB이다. 동일 host node 수는 host HA가 아니다. |
| Source and updater | [Compose](../../../infra/04-data/opensearch/docker-compose.yml)와 그 [Dockerfile](../../../infra/04-data/opensearch/Dockerfile)가 engine build를 소유한다. Compose가 Dashboards를 소유하고 Renovate가 update 제안을 소유한다. |
| Network and exposure | 모든 service는 선언된 network에 join한다. Primary API와 Dashboards는 Traefik과 `gateway-standard-chain@file`을 통해 TLS backend를 사용한다. cluster variant는 node1에서 Performance Analyzer port `9600`도 `127.0.0.1`에만 publish한다. |
| Persistence | Primary는 bind-backed `opensearch-data`를 사용한다. Dashboards는 `opensearch-dashboards-data`를 사용한다. cluster node는 `opensearch-data1..3`을 사용한다. certificate와 security configuration은 별도의 read-only mount이다. |
| Credentials | admin, Dashboards, exporter, cookie, OAuth client secret이 해당되는 경우 선언된다. health check는 admin secret을 출력하지 않고 사용한다. |
| Health and resources | engine health는 yellow 이상이 필요하다. Dashboards는 `200` 또는 `401`을 수용한다. Primary는 2 CPU/2 GiB를 상속한다. 각 cluster node도 2 CPU/2 GiB를 상속하므로 선택 시 resource 부담이 크다. |
| Backup and upgrade | 등록된 repository와 함께 snapshot API를 사용한다. security index는 제외하고 security configuration은 별도로 보존한다. 호환되는 격리 topology로 restore한 뒤 security config를 신중하게 적용한다. engine/Dashboards 버전을 변경하기 전에 문서화된 upgrade path를 검토한다. |


### Identity-specific behavior

OpenSearch custom FROM3.8.0 에 exporter3.5.0.0 을 설치하므로 공식 exact patch 호환 규칙과 불일치한다. 네 built node 모두 source nonconformance 이며 현재 build/monitoring 을 정상으로 인정하지 않는다. 기본 opensearch 만 copied secret-rendering wrapper 를 사용한다. cluster node1/2/3 는 base entrypoint 와 별도 bash command 이며 node1 의 certificate mount 와 node2/3 의 부재가 다르다. cluster 의 `./config/userdict_ko.txt` 참조는 tracked `opensearch/config/userdict_ko.txt`와 불일치한다. cluster data 는 Docker named volume 이며 primary bind 와 다르다. Dashboards 의 기본 backend 는 primary opensearch 다; cluster profile 만 켜도 자동 전환되지 않는다. 같은 router 이름의 두 topology 를 동시에 활성화하지 않는다. private host security config 와 실제 certificate/readiness 는 미확인이다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `opensearch` | single-node search; custom secret renderer | 선언된 HTTP health; build/plugin/config 충족은 미검증 | [선택·의존·접속·입력·mount](../../../infra/04-data/opensearch/docker-compose.yml) |
| `opensearch-dashboards` | UI; 기본 backend는 primary이며 cluster 전환 별도 | 선언된 HTTP health; build/plugin/config 충족은 미검증 | [선택·의존·접속·입력·mount](../../../infra/04-data/opensearch/docker-compose.yml) |
| `opensearch-node1` | cluster 1; base entrypoint, 개별 named data; node1만 cert mount | 선언된 HTTP health; build/plugin/config 충족은 미검증 | [선택·의존·접속·입력·mount](../../../infra/04-data/opensearch/docker-compose.yml) |
| `opensearch-node2` | cluster 2; base entrypoint, 개별 named data; node1만 cert mount | 선언된 HTTP health; build/plugin/config 충족은 미검증 | [선택·의존·접속·입력·mount](../../../infra/04-data/opensearch/docker-compose.yml) |
| `opensearch-node3` | cluster 3; base entrypoint, 개별 named data; node1만 cert mount | 선언된 HTTP health; build/plugin/config 충족은 미검증 | [선택·의존·접속·입력·mount](../../../infra/04-data/opensearch/docker-compose.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의2026-10-01 source snapshot과 official version/build 검토는 [W4 Task](../../03.specs/0198-operations-documentation-system/tasks/tsk-0004-data-messaging-analytics.md)에 보존했다. 반복OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.


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
- `infra/04-data/opensearch/docker-compose.yml`

### Step-by-step Instructions

1. Primary compose contract 위치를 확인한다.

   ```bash
   test -f infra/04-data/opensearch/docker-compose.yml
   ```

2. Cluster health는 HTTPS와 admin secret으로 확인한다.

   인증된 cluster 읽기는 [해당 Runbook](../runbooks/0019-opensearch.md)의 private TTY/client prompt 절차를 따른다. source build/config 한계를 해결·검증하기 전 성공을 가정하지 않는다.

3. Dashboards route는 `opensearch-dashboard.${DEFAULT_URL}` Traefik host rule을 사용한다.

### Common Pitfalls

- primary service name `opensearch`와 cluster variant service names `opensearch-node1..3`을 혼용하는 경우
- HTTP로 `9200`을 호출하는 경우
- admin password를 command line literal이나 문서에 남기는 경우

- 인덱스는 도메인별 패턴을 따른다(예: `logs-*-*`).


## Common Checks

- `test -f infra/04-data/opensearch/docker-compose.yml`
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

- Runtime pins: Compose/Dockerfile 선언이 authoritative하며, [derived Compose image projection](../../../infra/tech-stack.versions.json)이 drift 검증을 제공한다.

- [Operations guides index](../README.md)
- [Operations policy](../policies/0019-opensearch.md)
- [Recovery runbook](../runbooks/0019-opensearch.md)
- [Infra README](../../../infra/04-data/opensearch/README.md)
- [Compose implementation: infra/04-data/opensearch/docker-compose.yml](../../../infra/04-data/opensearch/docker-compose.yml)
