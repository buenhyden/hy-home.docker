---
title: "CouchDB Usage Guide"
version: "2.1.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "operations"
artifact_id: "GDE-0026"
parent_ids:
- "POL-0026"
created: "2026-05-10"
---

# CouchDB Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### Overview

이 문서는 [CouchDB Compose 구현](../../../labs/couchdb.yml)의 3노드 클러스터 사용 기준을 설명한다. `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`는 정확히 `couchdb` profile과 선언된 network에서 동작한다. frozen classification은 `LAB`이며 세 노드는 한 Docker host에 있으므로 host-level HA가 아니다.

### Current implementation

| 항목 | 이 저장소의 구현 결정 |
| --- | --- |
| Consumer와 data 근거 | 확인된 HOME consumer는 없음; LAB document/replication 평가용. |
| Source·update 책임 | [Compose](../../../labs/couchdb.yml)가 image source를 소유한다. dependency 자동화 제안은 운영자 검토가 필요하다. |
| 서비스·profile | node 3개와 `couchdb-cluster-init`; 정확한 profile은 `couchdb`. |
| 흐름·의존성 | init은 node join과 system DB를 확인하고 HTTP 실패를 거절한다. exit0만으로 실제 membership 수용 검증은 아니다. Traefik 관련 label은 남아 있으나 독립 LAB network에서 HOME Traefik과 연결되지 않는다. |
| 노출·영속성 | 직접 host port 없이 LAB 전용 network에서 동작하며 node별로 bind 기반 data volume을 둔다. |
| 환경 설정·secret | `LAB_COUCHDB_USERNAME`과 node 이름을 사용하며 admin password와 Erlang cookie는 Docker Secret이다. |
| Health·자원 | `/_up`, `/_membership`, init log; node는 `template-stateful-med`를 확장한다. |
| 보안 | admin/cookie secret mount와 database `_security` object를 사용하며 직접 노출한 host port는 없다. |
| Backup·upgrade | replication을 우선한다. file backup은 쓰기를 멈춘 일관된 상태에서 생성해야 한다. 격리된 restore evidence를 확보한 후에만 upstream upgrade 순서를 따른다. |
| License·edition | Apache CouchDB source에는 Apache-2.0이 적용되며 상용 clustering 기능을 가정하지 않는다. |

### Identity-specific behavior

couchdb-1/2/3 는 각각 NODENAME/IP/bind data 가 다르며 common cookie/admin secret 을 읽는 startup command 를 공유한다. `_up`은 membership/quorum 확인이 아니다. init은 HTTP 오류에서 실패하고 재실행 때 system DB를 다시 확인한다. exit0 뒤에도 `_membership`의 all_nodes/cluster_nodes와 system DB를 별도 확인한다. `_membership`의 all_nodes/cluster_nodes 와 system DB 를 별도 검증한다. profile 의 3nodes 는 한 host 이며 host HA 가 아니다. 재실행은 cluster setup mutation 으로 사전 승인한다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `couchdb-1` | CouchDB member 1; 고유 NODENAME/address/bind data | _up; membership/system DB 별도 | [선택·의존·접속·입력·mount](../../../labs/couchdb.yml) |
| `couchdb-2` | CouchDB member 2; 고유 NODENAME/address/bind data | _up; membership/system DB 별도 | [선택·의존·접속·입력·mount](../../../labs/couchdb.yml) |
| `couchdb-3` | CouchDB member 3; 고유 NODENAME/address/bind data | _up; membership/system DB 별도 | [선택·의존·접속·입력·mount](../../../labs/couchdb.yml) |
| `couchdb-cluster-init` | HTTP cluster setup job; 실패는 nonzero, exit0 뒤 실제 membership 확인 | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../labs/couchdb.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의2026-10-01 source snapshot과 official version/build 검토는 [W4 Task](../../98.archive/completed/03.specs/0198-operations-documentation-system/tasks/tsk-0004-data-messaging-analytics.md)에 보존했다. 반복OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.

### Usage Type

`system-guide`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

CouchDB HTTP API, cluster-init job, 독립 LAB network, Docker Secret 기반 admin/cookie 설정을 현재 compose 이름과 맞춰 사용할 수 있게 한다.

### Prerequisites

이 LAB의 입력은 [예시 환경 파일](../../../labs/.env.example)과 비공개 `labs/.env`가 소유한다. secret 파일은 `LAB_SECRET_DIR`(기본 `../secrets/labs`) 아래의 [LAB별 경로](../../../labs/couchdb.yml)에 둔다. source 반영, 실제 실행, 비밀 파일 이동 완료와 복구 검증은 별도로 확인한다.

- [독립 LAB Compose](../../../labs/couchdb.yml)는 root에 include되지 않으며 네 서비스는 `couchdb` profile에 속한다.
- `LAB_DATA_DIR`, `LAB_COUCHDB_HOST_PORT`, `LAB_COUCHDB_USERNAME`, `lab_couchdb_password`, `lab_couchdb_cookie`가 준비되어 있어야 한다.
- 로컬 점검은 승인된 credential custody와 비공개 실제 TTY를 준비한 뒤 client의 native password prompt를 사용한다. 준비되지 않으면 중단한다.

### Step-by-step Instructions

별도 승인 후 상태 점검은 LAB Compose 렌더링, 클러스터/init job 상태, `couchdb-1` 내부 client의 native password prompt를 통한 `_up` 및 `_membership` 확인으로 구성된다. 현재 독립 network는 HOME Traefik과 연결되지 않으므로 label의 route와 sticky cookie는 동작 경로가 아니다. 직접 host port publish도 없다. 실행 가능한 명령 순서와 기대 결과는 [CouchDB runbook](../runbooks/0026-couchdb.md#steps)을 따른다.

### Common Pitfalls

- 서비스명은 `couchdb-1`, `couchdb-2`, `couchdb-3`이다. 예전 node-style 이름을 현재 서비스명처럼 사용하지 않는다.
- Erlang cookie는 legacy shared-secret env var가 아니라 `/run/secrets/lab_couchdb_cookie`에서 읽어 `ERL_FLAGS`에 주입된다.
- 클러스터 init은 [curlimages/curl image declaration](../../../labs/couchdb.yml) 기반 일회성 job이며, 반복 실패 시 재조인 절차를 임의로 실행하기 전에 runbook evidence를 남겨야 한다.
- backup/restore는 database 단위 replication을 우선한다. file backup이 승인되면 config와 cluster metadata를 보존하고 upstream 순서대로 index files를 database files보다 먼저 복원한다.

### Common Checks

- `LAB_DATA_DIR=/tmp docker compose --env-file labs/.env.example -f labs/couchdb.yml --profile couchdb config --quiet`
- `docker compose --env-file "$LAB_ENV_FILE" -f labs/couchdb.yml logs couchdb-cluster-init`
- `_membership` 확인은 [CouchDB runbook의 private TTY/native-prompt 절차](../runbooks/0026-couchdb.md#steps)를 따른다. Password를 URL·argv·환경 변수·history·로그에 넣지 않으며 custody/TTY가 없으면 중단한다.

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [CouchDB runbook](../runbooks/0026-couchdb.md)을 따른다.

### Traceability

- Declared parent: [CouchDB Operations Policy](../policies/0026-couchdb.md) (`POL-0026`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Policy](../policies/0026-couchdb.md) (`POL-0026`), [Runbook](../runbooks/0026-couchdb.md) (`RUN-0026`)

## Related Documents

- [CouchDB backup guidance](https://docs.couchdb.org/en/stable/maintenance/backups.html)
- [CouchDB upgrade guidance](https://docs.couchdb.org/en/stable/install/upgrading.html)
- [CouchDB database security](https://docs.couchdb.org/en/stable/api/database/security.html)
- [Apache CouchDB source and license](https://github.com/apache/couchdb)

- [Operations index](../README.md)
- [Operations policy](../policies/0026-couchdb.md)
- [Recovery runbook](../runbooks/0026-couchdb.md)
- [LAB 설명](../../../labs/couchdb.md)
