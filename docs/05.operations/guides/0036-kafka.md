---
title: "Kafka Usage Guide"
version: "1.1.6"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "GDE-0036"
parent_ids:
- "POL-0036"
implementation_services:
  infra/05-messaging/kafka/docker-compose.yml:
  - 'debezium-db-provision'
  - 'kafbat-ui'
  - 'kafka-1'
  - 'kafka-connect'
  - 'kafka-exporter'
  - 'kafka-init'
  - 'kafka-rest-proxy'
  - 'schema-registry'
created: "2026-05-10"
---

# Kafka Usage Guide

## Overview

이 가이드는 OPTIONAL 이벤트 스트리밍 기능인 Kafka family의 구성, 프로파일, 접근 경계를 설명한다. 정상 root는 단일 KRaft broker와 Schema Registry, Connect, REST Proxy, Kafbat UI, exporter, init job을 정의한다. 다중 broker 학습은 독립 LAB으로 분리했다.

## Audience and Goal

대상 독자는 Kafka family를 켜거나 변경하는 운영자와 개발자다. 목표는 어떤 서비스가 어느 profile에서 선택되는지, 어디까지 보호되는지, 복구가 무엇을 포함하는지 확인하는 것이다. 실행 절차는 [RUN-0036](../runbooks/0036-kafka.md)이 소유한다.

## Usage

Kafka는 OPTIONAL 이벤트 스트리밍 기능이다. 정상 root에는 단일
`kafka-1`만 있고, 다중 broker 학습은 독립 LAB 진입점의 `lab-kafka`
프로파일로 분리했다. 세 LAB broker도 한 Docker host를 공유하므로 host
가용성을 증명하지 않는다. 정상 서비스를 지속 실행해야 한다는 HOME consumer는
현재 확인되지 않았다.

### Current implementation

[`infra/05-messaging/kafka/docker-compose.yml`](../../../infra/05-messaging/kafka/docker-compose.yml)은
정상 서비스 8개를 정의한다. [`Kafka LAB 안내`](../../../labs/kafka-cluster.md)와 [`labs/kafka-cluster.yml`](../../../labs/kafka-cluster.yml)은
LAB 전용 브로커 3개·exporter·init 5개를 독립 Compose project로 정의하며 정상 root가 include하지 않는다.

| Service | Role | Selector |
| --- | --- | --- |
| `kafka-1` | 단일 KRaft broker/controller | `messaging`, `messaging-broker`, `messaging-schema`, `messaging-connect`, `messaging-rest`, `messaging-admin`, `cdc` |
| `schema-registry` | Avro schema 저장소/API | `messaging`, `messaging-schema`, `messaging-connect`, `messaging-rest`, `messaging-admin`, `cdc` |
| `kafka-connect` | Debezium connector runtime | `messaging`, `messaging-connect`, `messaging-admin`, `cdc` |
| `debezium-db-provision` | `dev-pg/platform_dev` 일반 테이블·outbox source role·publication; hypertable CDC 미검증 | `cdc` |
| `kafka-rest-proxy` | REST producer/consumer API | `messaging`, `messaging-rest` |
| `kafbat-ui` | native OIDC/RBAC 관리 UI | `messaging`, `messaging-admin` |
| `kafka-exporter`, `kafka-init` | 메트릭과 RF1 topic bootstrap | `messaging`, `messaging-broker` |
| `lab-kafka-1/2/3`, `lab-kafka-exporter`, `lab-kafka-init` | 독립 RF3 실습 closure | `lab-kafka` |

정상 `kafka-1-data`와 `kafka-connect-data`는
`${DEFAULT_MESSAGE_BROKER_DIR}/kafka`의 별도 volume이다. LAB 상태는
`${LAB_DATA_DIR}/kafka/{1,2,3}`에 있고 별도 cluster ID, network, topic·offset을
사용하며 host port를 게시하지 않는다. broker PLAINTEXT는 내부 network에서만
사용한다. 정상 broker의 기존 localhost host listener는 별도로 존재한다.

Kafbat은 자체 `auth.type: OAUTH2` 구성을 tmpfs에 렌더링하고,
`kafbat_client_secret`을 읽고, local CA를 신뢰하며, group 기반 RBAC를
적용한다. 이 서비스의 Traefik route는 `gateway-standard-chain@file`을
사용한다. gateway는 전송/헤더 보호를 담당하고, 인증 자체는 Kafbat이 수행한다.
이 native-OIDC route에는 forwarding-auth gateway chain을 붙이면 안 된다.
Kafka Connect REST route는 이제 `sso-errors`/`sso-auth`를 추가한다. 이 API는
provider 파일을 참조하는 connector를 생성할 수 있으므로, 익명 gateway
접근은 credential-exfiltration 경로였다. `kafka_net` peer(Kafbat 포함)는
여전히 인증 없이 포트 8083에 직접 접근할 수 있다. 이 내부 경로는 기록된
gap이다.

### Identity-specific behavior

Compose에 선언된 Confluent CP 이미지가 정상 단일 broker와 LAB 다중 broker에 쓰인다.
정상 `kafka-init`은 RF1, LAB `lab-kafka-init`은 RF3이며 서로 다른
KRaft identity와 저장소를 사용한다. broker/client/controller 경로의
PLAINTEXT는 TLS·인증을 제공하지 않는다. Schema Registry는 실제 Avro
connector의 schema ID 이력을, Connect는 connector config/offset/status를
소유한다. Debezium source는 `dev-pg/platform_dev`이며 connector JSON은
자동 등록되지 않는다. JMX 설정·exporter 선언만으로 scrape 성공은 증명되지 않는다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `debezium-db-provision` | CDC source role/grant/publication provisioning job | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafbat-ui` | native OIDC/RBAC UI; tmpfs config | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafka-1` | KRaft combined broker/controller 1; 정상 단일 selector | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafka-connect` | connector worker/internal state; PG Debezium만 copied build | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafka-exporter` | broker/consumer lag metrics | 선언된 endpoint health; scrape/data 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafka-init` | RF1 topic creation job; 단일 broker 필요 | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafka-rest-proxy` | HTTP→Kafka 변환; native auth 선언 없음 | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `schema-registry` | schema-ID/history; Kafka state에 의존 | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `lab-kafka-1/2/3`, `lab-kafka-exporter`, `lab-kafka-init` | 격리 KRaft RF3 실습 | 실제 quorum·topic 상태 미검증 | [LAB 선택·상태](../../../labs/kafka-cluster.md) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의2026-10-01 source snapshot과 official version/build 검토는 [W4 Task](../../98.archive/completed/03.specs/0198-operations-documentation-system/tasks/tsk-0004-data-messaging-analytics.md)에 보존했다. 반복OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.

### Images, configuration and resource controls

Compose 파일은 핀된 Confluent Kafka/Schema/Connect/REST, Kafbat, Kafka
exporter 이미지 계열을 소유한다. 저장소 Renovate가 업데이트를 제안하면 버전
projection은 파생된다. broker 키에는 `CLUSTER_ID`, `KAFKA_PROCESS_ROLES`,
quorum/listener/advertised-listener/log/replication 설정, node ID가 포함된다.
Schema, Connect, REST는 각자의 네임스페이스 키를 사용하며, Kafbat은
`KAFKA_CLUSTERS_0_*`, `DYNAMIC_CONFIG_ENABLED`, `KAFBAT_OAUTH_CLIENT_ID`와
client-secret 파일을 사용한다. broker와 Connect는 high stateful 템플릿을,
Schema/REST/Kafbat은 medium infrastructure 템플릿을, exporter는 low를, init
job은 low를 extend한다. 모든 장기 실행 서비스는 healthcheck를 선언한다.

### Static preflight and profile choice

정적 render 명령은 [RUN-0036 절차](../runbooks/0036-kafka.md#procedure)가 소유한다. 정상 `kafka-init`은 RF1,
LAB `lab-kafka-init`은 RF3이다. LAB의 `LAB_KAFKA_CLUSTER_ID`는 정상
`KAFKA_CLUSTER_ID`와 달라야 한다. 서비스 시작과 topic 생성은 별도 runtime
승인 대상이다.

### Change data capture (`cdc`)

`cdc`는 정상 broker·Schema Registry·Connect와 `dev-pg`,
`dev-platform-provision`, `debezium-db-provision`을 선택한다. 기능 SQL
[`dev-pg.sql`](../../../infra/05-messaging/kafka/connect/debezium/provisioning/dev-pg.sql)은
`platform_dev`의 `app` schema 읽기, 별도 `debezium_heartbeat` 쓰기와
`hyhome_platform_publication`을 선언한다. Connector는 독립
`hyhome_platform_slot`, topic prefix `hyhome.platform`을 사용하고 Avro
변환 때문에 Schema Registry를 유지한다. 기존 mng-pg slot·publication·topic과
LSN을 재사용하지 않는다. connector JSON은 자동 등록되지 않으며 등록, snapshot,
writer/reader 전환은 별도 승인이 필요하다.

Connect는 시작할 때 `debezium_postgres_password` secret에서
`/tmp/connect-secrets/debezium.properties`를 tmpfs에 렌더링한다. connector
[`postgres-connector.json`](../../../infra/05-messaging/kafka/connect/debezium/postgres-connector.json)은
`FileConfigProvider`, `pgoutput`, `publication.autocreate.mode=disabled`,
60초 heartbeat action을 선언한다. 중단된 slot은 WAL을 고정할 수 있으므로
실제 lag·WAL 용량은 별도로 관측해야 한다.

다음 상태는 서로 구분되며 상태마다 자체 증거가 필요하다.

| State | Evidence |
| --- | --- |
| JSON 파일 존재 | Git에만 있으며 아직 등록된 것은 없음 |
| 등록됨 | `GET /connectors/<name>`이 config를 반환함 |
| 실행 중 | `GET /connectors/<name>/status`에서 connector와 task가 `RUNNING`으로 표시됨 |
| Snapshot 완료 | connector metric이나 log에서 초기 snapshot 완료를 확인함 |
| 변경 수집됨 | test 변경이 `hyhome.platform.*` topic에 나타남 |

`dev-pg` 소스는 `wal_level=logical`, slot·sender·WAL 보존 한도를
선언한다. 실제 신규 DB provision, replication role, publication, slot,
connector 등록·snapshot·offset 재설정은 아직 실행하지 않았다. 기존 HOME
`mng-pg/app_db` 기술 객체와 이전 topic은 별도 승인 전까지 보존한다.

### License and source boundary

Apache Kafka와 Kafbat은 Apache-2.0 프로젝트다. Schema Registry, Connect,
REST 이미지는 Confluent가 제공하며 별도의 현재 license/edition 검토가
필요하다. Cluster Linking이나 다른 edition 전용 기능은 선언하지도 가정하지도
않는다.

### Common Checks

정확한 root profile, service, health/resource 제어, writable-state 소유권,
secret reference, exposure, 엔진별 복구 경계를 확인한다. static pass는 구성
증거일 뿐이며, runtime과 restore는 별개로 남는다.

### Runbook Handoff

Kafka 복구 범위는 broker 디렉터리보다 넓다. topic 데이터와 config,
partition 수, consumer-group offset, KRaft cluster metadata, Schema Registry
`_schemas` history/ID, Connect connector 정의와 그 config/offset/status
topic을 목록으로 정리한다. 신뢰할 수 있는 producer source에서 replay하거나,
새로 격리한 cluster로 승인된 cross-cluster replication을 하는 방식을 우선한다.
원시 broker log-directory 재사용과 실행 중인 KRaft identity 재사용은 금지한다.

[RUN-0036](../runbooks/0036-kafka.md)은 의존 레코드보다 먼저 schema를
복원하고, topic 구성을 재생성하고, offset을 복원/재배치하고, connector를
일시정지 상태로 유지하며, cutover 전에 end offset과 애플리케이션 소비를
증명한다. 이미지나 프로토콜 업그레이드에는 Kafka, Confluent 구성 요소,
Kafbat, 클라이언트, 저장 형식에 대한 공식 호환성 검토와 현재 recovery
artifact 및 rollback이 필요하다.

### Traceability

- Artifact: `GDE-0036`; 상위 정책: `POL-0036`.
- Runtime authority: `infra/05-messaging/kafka/docker-compose.yml`과
  [Connect image Dockerfile](../../../infra/05-messaging/kafka/Dockerfile.connect).

## Related Documents

- [Operations policy](../policies/0036-kafka.md)
- [Cluster recovery runbook](../runbooks/0036-kafka.md)
- [Messaging architecture](../../02.architecture/descriptions/0005-messaging-architecture.md)
- [Apache Kafka operations](https://kafka.apache.org/documentation/#operations)
- [Kafka KRaft](https://kafka.apache.org/documentation/#kraft)
- [Kafka license](https://kafka.apache.org/licensing)
- [Schema Registry migration](https://docs.confluent.io/platform/current/schema-registry/installation/migrate.html)
- [Kafbat configuration](https://ui.docs.kafbat.io/configuration/configuration-file)
- [Kafbat RBAC](https://ui.docs.kafbat.io/configuration/rbac-role-based-access-control)
- [Kafbat license](https://github.com/kafbat/kafka-ui/blob/main/LICENSE)
