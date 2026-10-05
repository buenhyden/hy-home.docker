---
title: "MongoDB Usage Guide"
version: "2.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "GDE-0027"
parent_ids:
- "POL-0027"
created: "2026-05-10"
---

# MongoDB Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### Overview

이 문서는 [MongoDB Compose 구현](../../../labs/mongodb.yml)의 replica set 사용 기준을 설명한다. 일곱 서비스는 모두 정확히 `mongodb` profile과 선언된 network에서 동작한다. frozen classification은 `LAB`이고 두 data-bearing member와 arbiter가 한 host에 있으므로 host-level HA가 아니다.

### Current implementation

| 항목 | 이 저장소의 구현 결정 |
| --- | --- |
| Consumer와 data 근거 | 확인된 HOME consumer는 없음; LAB replica-set과 document-database 평가용. |
| Source·update 책임 | [Compose](../../../labs/mongodb.yml)가 image source를 소유한다. dependency 자동화 제안은 호환성 검토가 필요하다. |
| 서비스·profile | key generator, data member 2개, arbiter, init, UI, exporter; 정확한 profile은 `mongodb`. |
| 흐름·의존성 | `mongo-init`이 `MyReplicaSet`을 생성한다. client는 두 data member에 접속하며 arbiter는 data 없이 투표한다. |
| 노출·영속성 | Mongo Express에는 이전 Traefik label이 남지만 HOME gateway network와 분리되어 있다. member는 내부에 둔다. data/key는 named volume에 저장한다. |
| 환경 설정·secret | root/UI username은 환경 식별자이고 root/UI password는 Docker Secret이다. keyfile은 `mongo-key`에 생성한다. |
| Health·자원 | member healthcheck, `rs.status()`, init/exporter log; data member는 `template-stateful-high`를 확장한다. |
| 보안 | 내부 keyfile 인증과 secret 기반 root/UI password를 사용한다. 같은 host의 topology는 DR이 아니다. |
| Backup·upgrade | `mongodump --oplog`와 격리된 `--oplogReplay`를 사용한다. upgrade/제거 전에 tool/server 호환성과 restore evidence가 필요하다. |
| License·edition | MongoDB Community에는 SSPL 조건이 적용된다. 이 topology는 Enterprise backup이나 관리 기능을 제공한다고 주장하지 않는다. |

### Identity-specific behavior

rep1/rep2 는 data member, arbiter 는 투표만 담당하며 data backup 이 아니다. mongo-key 는 Docker named volume 이며 key-generator 는 공식 mongo 이미지의 Node crypto로 내부 key를 만들거나 보존한다. mongo-init 는 두 data node와 arbiter health를 기다린 뒤 replica set을 확인한다. ping health 는 credential/replica readiness 가 아니다. express 와 exporter 는 별도 image/client 이고 자체 healthcheck 는 없다.선언 release tag 의 전체 integration 은 미검증이다. source의 credential 전달은 argv를 피하지만 실제 인증은 미검증이다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `mongo-express` | 관리 UI; Basic Auth와 DB credential 경계 분리 | 자체 healthcheck 없음; process와 해당 기능/metrics 별도 확인 | [선택·의존·접속·입력·mount](../../../labs/mongodb.yml) |
| `mongo-init` | replica initialization job; data node와 arbiter health 대기, membership mutation | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../labs/mongodb.yml) |
| `mongo-key-generator` | 내부 인증 key 생성/permission 변경 job | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../labs/mongodb.yml) |
| `mongodb-arbiter` | 투표용 arbiter; data backup member 아님 | healthcheck 선언; replica 투표 기능 별도 확인 | [선택·의존·접속·입력·mount](../../../labs/mongodb.yml) |
| `mongodb-exporter` | Mongo metrics; password env와 credential-free URI | 자체 healthcheck 없음; process와 해당 기능/metrics 별도 확인 | [선택·의존·접속·입력·mount](../../../labs/mongodb.yml) |
| `mongodb-rep1` | data-bearing replica 1; 각각 named data, shared internal key | ping; 인증/replica 상태 별도 | [선택·의존·접속·입력·mount](../../../labs/mongodb.yml) |
| `mongodb-rep2` | data-bearing replica 2; 각각 named data, shared internal key | ping; 인증/replica 상태 별도 | [선택·의존·접속·입력·mount](../../../labs/mongodb.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의2026-10-01 source snapshot과 official version/build 검토는 [W4 Task](../../98.archive/completed/03.specs/0198-operations-documentation-system/tasks/tsk-0004-data-messaging-analytics.md)에 보존했다. 반복OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.

### Usage Type

`system-guide`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

MongoDB replica set의 서비스명, keyfile volume, init job, Mongo Express route, exporter 경계를 현재 compose와 맞춰 사용하도록 한다.

### Prerequisites

이 LAB의 입력은 [예시 환경 파일](../../../labs/.env.example)과 비공개 `labs/.env`가 소유한다. secret 파일은 `LAB_SECRET_DIR`(기본 `../secrets/labs`) 아래의 [LAB별 경로](../../../labs/mongodb.yml)에 둔다. source 반영, 실제 실행, 비밀 파일 이동 완료와 복구 검증은 별도로 확인한다.

- [독립 LAB Compose](../../../labs/mongodb.yml)는 root에 include되지 않으며 모든 서비스는 `mongodb` profile에 속한다.
- `LAB_MONGODB_ROOT_USERNAME`, `LAB_MONGO_EXPRESS_USERNAME`, `lab_mongodb_root_password`, `lab_mongo_express_basicauth_password`가 준비되어 있어야 한다.
- replica set 이름은 compose command에 고정된 `MyReplicaSet` 기준이다. 현재 구현에는 별도 replica-set-name 환경 변수가 없다.

### Step-by-step Instructions

정상 운영 중 점검은 compose profile 렌더링, init job/replica member 상태, `mongodb-rep1` 내부 client의 native password prompt를 통한 `rs.status()` 확인으로 구성된다. 실행 가능한 명령 순서와 기대 결과는 [MongoDB runbook](../runbooks/0027-mongodb.md#steps)을 따른다.

1. 애플리케이션 연결 문자열은 내부 서비스명을 포함한다.

   ```text
   mongodb://<user>:<password>@mongodb-rep1:27017,mongodb-rep2:27017/?replicaSet=MyReplicaSet&authSource=admin
   ```

2. 관리 UI `mongo-express`는 독립 LAB network에만 있다. 기존 Traefik label의 `https://mongo-express.${LAB_BASE_DOMAIN}`는 현재 접속 경로가 아니다. `ME_CONFIG_BASICAUTH=true`로 basic auth가 켜져 있어야 하며(mongo-express 1.x는 이 값 없이 자격 증명을 무시한다), 직접 host port publish는 현재 compose에 없다.

### Common Pitfalls

- `mongodb-arbiter`는 투표 전용 구성원이다. 데이터 보관 노드로 설명하거나 백업 대상으로 취급하지 않는다.
- keyfile은 `mongo-key-generator`가 `mongo-key` named volume에 생성한다. repository 경로의 `configdb/` 디렉터리를 전제로 하지 않는다.
- `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`에 compose healthcheck가 있다. `mongo-init`, `mongo-express`, `mongodb-exporter`의 readiness는 logs와 dependency 상태로 확인한다.
- replica-set backup은 primary에서 authenticated `mongodump --oplog`로 일관성을 잡고 `mongorestore --oplogReplay`로 빈 격리 replica set에 검증한다. arbiter는 data backup 대상이 아니다.

### Common Checks

- `LAB_DATA_DIR=/tmp docker compose --env-file labs/.env.example -f labs/mongodb.yml --profile mongodb config --quiet`
- `docker compose --env-file "$LAB_ENV_FILE" -f labs/mongodb.yml logs mongo-init`
- `rs.status()` 확인은 [MongoDB runbook의 private TTY/native-prompt 절차](../runbooks/0027-mongodb.md#steps)를 따른다. 승인된 custody/실제 TTY가 없으면 중단하고 password를 URL·argv·환경 변수·history·로그에 넣지 않는다.

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [MongoDB runbook](../runbooks/0027-mongodb.md)을 따른다.

### Traceability

- Declared parent: [MongoDB Operations Policy](../policies/0027-mongodb.md) (`POL-0027`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Policy](../policies/0027-mongodb.md) (`POL-0027`), [Runbook](../runbooks/0027-mongodb.md) (`RUN-0027`)

## Related Documents

- [MongoDB backup and restore tools](https://www.mongodb.com/docs/v8.0/tutorial/backup-and-restore-tools/)
- [MongoDB security hardening](https://www.mongodb.com/docs/v8.0/core/security-hardening/)
- [MongoDB Community licensing](https://www.mongodb.com/legal/licensing/community-edition)

- [Operations index](../README.md)
- [Operations policy](../policies/0027-mongodb.md)
- [Recovery runbook](../runbooks/0027-mongodb.md)
- [LAB 설명](../../../labs/mongodb.md)
- [Compose implementation: labs/mongodb.yml](../../../labs/mongodb.yml)
