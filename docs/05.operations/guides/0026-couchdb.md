---
title: "CouchDB Usage Guide"
version: "1.0.5"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0026"
parent_ids:
- "POL-0026"
implementation_services:
  infra/04-data/couchdb/docker-compose.yml:
  - 'couchdb-1'
  - 'couchdb-2'
  - 'couchdb-3'
  - 'couchdb-cluster-init'
created: "2026-05-10"
---

# CouchDB Usage Guide

## Usage

### Overview

이 문서는 [CouchDB Compose 구현](../../../infra/04-data/couchdb/docker-compose.yml)의 3노드 클러스터 사용 기준을 설명한다. `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`는 정확히 `couchdb` profile과 선언된 network에서 동작한다. frozen classification은 `LAB`이며 세 노드는 한 Docker host에 있으므로 host-level HA가 아니다.

### Current implementation

| 항목 | 이 저장소의 구현 결정 |
| --- | --- |
| Consumer와 data 근거 | 확인된 HOME consumer는 없음; LAB document/replication 평가용. |
| Source·update 책임 | [Compose](../../../infra/04-data/couchdb/docker-compose.yml)가 image source를 소유한다. dependency 자동화 제안은 운영자 검토가 필요하다. |
| 서비스·profile | node 3개와 `couchdb-cluster-init`; 정확한 profile은 `couchdb`. |
| 흐름·의존성 | init은 node join/system DB 생성을 시도하지만 실패를 억제한다. exit0은 membership 수용 검증이 아니다. client는 Traefik sticky routing을 사용한다. |
| 노출·영속성 | HTTPS gateway만 사용하며 node별로 bind 기반 data volume을 둔다. |
| 환경 설정·secret | `COUCHDB_USERNAME`과 node 이름을 사용하며 admin password와 Erlang cookie는 Docker Secret이다. |
| Health·자원 | `/_up`, `/_membership`, init log; node는 `template-stateful-med`를 확장한다. |
| 보안 | admin/cookie secret mount와 database `_security` object를 사용하며 직접 노출한 host port는 없다. |
| Backup·upgrade | replication을 우선한다. file backup은 쓰기를 멈춘 일관된 상태에서 생성해야 한다. 격리된 restore evidence를 확보한 후에만 upstream upgrade 순서를 따른다. |
| License·edition | Apache CouchDB source에는 Apache-2.0이 적용되며 상용 clustering 기능을 가정하지 않는다. |

### Identity-specific behavior

couchdb-1/2/3 는 각각 NODENAME/IP/bind data 가 다르며 common cookie/admin secret 을 읽는 startup command 를 공유한다. `_up`은 membership/quorum 확인이 아니다. curl8.22 init 는 일부 HTTP 오류/command 실패를 `|| true`로 무시하고 마지막 echo 로 종료하므로 exit0 을 bootstrap 성공으로 인정하지 않는다. `_membership`의 all_nodes/cluster_nodes 와 system DB 를 별도 검증한다. profile 의 3nodes 는 한 host 이며 host HA 가 아니다. 재실행은 cluster setup mutation 으로 사전 승인한다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `couchdb-1` | CouchDB member 1; 고유 NODENAME/address/bind data | _up; membership/system DB 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/couchdb/docker-compose.yml) |
| `couchdb-2` | CouchDB member 2; 고유 NODENAME/address/bind data | _up; membership/system DB 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/couchdb/docker-compose.yml) |
| `couchdb-3` | CouchDB member 3; 고유 NODENAME/address/bind data | _up; membership/system DB 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/couchdb/docker-compose.yml) |
| `couchdb-cluster-init` | HTTP cluster setup job; 오류 무시 때문에 exit0만으로 성공 판정 금지 | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../infra/04-data/couchdb/docker-compose.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의2026-10-01 source snapshot과 official version/build 검토는 [W4 Task](../../03.specs/0198-operations-documentation-system/tasks/tsk-0004-data-messaging-analytics.md)에 보존했다. 반복OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.

### Usage Type

`system-guide`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

CouchDB HTTP API, cluster-init job, Traefik sticky routing, Docker Secret 기반 admin/cookie 설정을 현재 compose 이름과 맞춰 사용할 수 있게 한다.

### Prerequisites

- 루트 [docker-compose.yml](../../../docker-compose.yml)는 CouchDB 파일을 include하며, 네 서비스는 모두 `couchdb` profile에 속한다.
- `DEFAULT_DATA_DIR`, `DEFAULT_URL`, `COUCHDB_USERNAME`, `couchdb_password`, `couchdb_cookie`가 준비되어 있어야 한다.
- 로컬 점검은 승인된 credential custody와 비공개 실제 TTY를 준비한 뒤 client의 native password prompt를 사용한다. 준비되지 않으면 중단한다.

### Step-by-step Instructions

정상 운영 중 점검은 compose profile 렌더링, 클러스터/init job 상태, `couchdb-1` 내부 client의 native password prompt를 통한 `_up` 및 `_membership` health endpoint 확인으로 구성된다. 외부 접근은 Traefik route `https://couchdb.${DEFAULT_URL}`와 sticky cookie 설정을 전제로 하며 직접 host port publish는 현재 compose에 없다. 실행 가능한 명령 순서와 기대 결과는 [CouchDB runbook](../runbooks/0026-couchdb.md#steps)을 따른다.

### Common Pitfalls

- 서비스명은 `couchdb-1`, `couchdb-2`, `couchdb-3`이다. 예전 node-style 이름을 현재 서비스명처럼 사용하지 않는다.
- Erlang cookie는 legacy shared-secret env var가 아니라 `/run/secrets/couchdb_cookie`에서 읽어 `ERL_FLAGS`에 주입된다.
- 클러스터 init은 [curlimages/curl image declaration](../../../infra/04-data/couchdb/docker-compose.yml) 기반 일회성 job이며, 반복 실패 시 재조인 절차를 임의로 실행하기 전에 runbook evidence를 남겨야 한다.
- backup/restore는 database 단위 replication을 우선한다. file backup이 승인되면 config와 cluster metadata를 보존하고 upstream 순서대로 index files를 database files보다 먼저 복원한다.

## Common Checks

- `docker compose --profile couchdb config --quiet`
- `docker compose logs couchdb-cluster-init`
- `_membership` 확인은 [CouchDB runbook의 private TTY/native-prompt 절차](../runbooks/0026-couchdb.md#steps)를 따른다. Password를 URL·argv·환경 변수·history·로그에 넣지 않으며 custody/TTY가 없으면 중단한다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [CouchDB runbook](../runbooks/0026-couchdb.md)을 따른다.

## Traceability

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
- [Infra README](../../../infra/04-data/couchdb/README.md)
