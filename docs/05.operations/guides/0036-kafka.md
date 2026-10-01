---
title: "Kafka Usage Guide"
version: "1.1.4"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0036"
parent_ids:
- "POL-0036"
implementation_services:
  infra/05-messaging/kafka/docker-compose.yml:
  - 'debezium-db-provision'
  - 'kafbat-ui'
  - 'kafka-1'
  - 'kafka-2'
  - 'kafka-3'
  - 'kafka-connect'
  - 'kafka-exporter'
  - 'kafka-init'
  - 'kafka-rest-proxy'
  - 'schema-registry'
created: "2026-05-10"
---

# Kafka Usage Guide

## Usage

Kafka는 OPTIONAL 이벤트 스트리밍 기능이다. Kafka를 지속적으로 실행해야 한다는
근거를 제시한 HOME consumer는 현재 없다. 세 브로커가 하나의 Docker host를
공유하므로 `messaging-cluster` profile은 host 가용성은 제공하지 못하고
KRaft/replication 동작을 테스트한다. 현재 구현에는 두 번째 broker family가
없다.

### Current implementation

[`infra/05-messaging/kafka/docker-compose.yml`](../../../infra/05-messaging/kafka/docker-compose.yml)은
10개 서비스를 정의한다.

| Service | Role | Current selectors |
| --- | --- | --- |
| `kafka-1` | KRaft broker/controller | `messaging`, `messaging-broker`, `messaging-cluster`, `messaging-schema`, `messaging-connect`, `messaging-rest`, `messaging-admin`, `cdc` |
| `kafka-2`, `kafka-3` | 추가 동일 host broker/controller | `messaging-cluster` |
| `schema-registry` | 스키마 저장소/API | `messaging`, `messaging-schema`, `messaging-connect`, `messaging-rest`, `messaging-admin`, `cdc` |
| `kafka-connect` | Debezium PostgreSQL plugin을 갖춘 connector runtime | `messaging`, `messaging-connect`, `messaging-admin`, `cdc` |
| `debezium-db-provision` | CDC source role, `mng-pg`에 대한 grant와 publication | `cdc` |
| `kafka-rest-proxy` | REST producer/consumer API | `messaging`, `messaging-rest` |
| `kafbat-ui` | native OIDC/RBAC를 갖춘 관리 UI | `messaging`, `messaging-admin` |
| `kafka-exporter`, `kafka-init` | 메트릭과 topic bootstrap | `messaging`, `messaging-broker`, `messaging-cluster` |

`kafka-1-data`, `kafka-2-data`, `kafka-3-data`, `kafka-connect-data`는
`${DEFAULT_MESSAGE_BROKER_DIR}/kafka` 아래의 bind-backed named volume이다.
broker listener는 현재 게시된 host listener를 포함해 `PLAINTEXT`이며, broker
인증이나 TLS가 없다. 모든 서비스는 `kafka_net`과 공유 리소스/health
템플릿을 사용한다.

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

Kafka CP8.3.2 는 4.3 family 이며 broker1 은단일/cluster selector, broker2/3 은 cluster 전용이다. RF3 의 kafka-init 는 3healthy brokers 가 필요하여 단일 selector 의완료를 보장하지 않는다. KRaft combined role 와 PLAINTEXT client/controller/JMX 는 TLS/auth 제공이 아니다. exporter 는 lag 관측, Schema Registry 는 schema-ID history, Connect 는내부 offset/config/status, REST 는 HTTP 변환, Kafbat 는 nativeOIDC/RBAC 로 각각 다르다. Debezium helper 는 mng-pg feature grants 를 변경하고 connector JSON 은자동 등록되지 않는다. Connect built3.6.3 PG plugin 만 복사하며 CP8.3 family 정렬은커스텀 통합 인증이 아니다. JMX YAML 이 있어도 agent/JAR 경로와 scrape 성공은별도 확인한다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `debezium-db-provision` | CDC source role/grant/publication provisioning job | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafbat-ui` | native OIDC/RBAC UI; tmpfs config | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafka-1` | KRaft combined broker/controller 1; 일반/cluster selector | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafka-2` | KRaft combined broker/controller 2; cluster selector 전용 | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafka-3` | KRaft combined broker/controller 3; cluster selector 전용 | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafka-connect` | connector worker/internal state; PG Debezium만 copied build | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafka-exporter` | broker/consumer lag metrics | 선언된 endpoint health; scrape/data 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafka-init` | RF3 topic creation job; 세 broker 필요 | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafka-rest-proxy` | HTTP→Kafka 변환; native auth 선언 없음 | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |
| `schema-registry` | schema-ID/history; Kafka state에 의존 | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/05-messaging/kafka/docker-compose.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의2026-10-01 source snapshot과 official version/build 검토는 [W4 Task](../../03.specs/0198-operations-documentation-system/tasks/tsk-0004-data-messaging-analytics.md)에 보존했다. 반복OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.


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

```bash
docker compose --env-file .env.example --profile messaging config --quiet
docker compose --env-file .env.example --profile messaging config --services
docker compose --env-file .env.example --profile messaging-cluster config --quiet
```

저장소 루트에서 실행한다. init job은 replication factor 3으로 `infra-events`와
`application-logs`를 생성하므로, 건강한 broker 3개가 있어야만 bootstrap이
유효하다. 별도로 승인된 fix 없이는 단일 broker `messaging` 선택을 topic
초기화 성공으로 보지 않는다. 서비스 시작, topic 생성, 테스트 레코드 생성은
runtime 작업이다.

### Change data capture (`cdc`)

`cdc`는 broker, Schema Registry, Connect, `mng-pg`, `debezium-db-provision`을
선택한다. 이 job은
[`connect/debezium/provisioning/mng-pg.sql`](../../../infra/05-messaging/kafka/connect/debezium/provisioning/mng-pg.sql)의
feature SQL을 실행한다: superuser는 아니지만 `REPLICATION` 권한을 가진
`debezium` login, 게시된 schema에 대한 `CONNECT`, `USAGE`, `SELECT`(이후
테이블에 대한 default privilege 포함), 하나의 `heartbeat` 테이블을 가진 자체
소유 `debezium_heartbeat` schema, 그리고 정확히 이 두 schema에 대한
`hyhome_app_publication` publication. 이 job은 replication slot을 생성하거나
삭제하지 않으며, 자신이 생성하지 않은 role을 변경하지 않는다(role은
`hy-home:feature:debezium` 주석 마커를 가진다).

Connect는 시작할 때마다 `debezium_postgres_password` secret에서
`/tmp/connect-secrets/debezium.properties`를 렌더링하고(Java-properties
escaping, mode 0600, tmpfs), `FileConfigProvider`를 `allowed.paths`로 해당
디렉터리에 제한한다. connector 정의
[`postgres-connector.json`](../../../infra/05-messaging/kafka/connect/debezium/postgres-connector.json)은
`${file:/tmp/connect-secrets/debezium.properties:password}`를 참조하고
`pgoutput`, slot `hyhome_app_slot`, `publication.autocreate.mode=disabled`를
사용한다. `mng-pg`는 여러 데이터베이스를 호스팅하므로, Keycloak, n8n,
Airflow가 기록하는 WAL은 조용한 `app_db`의 slot을 진행시키지 않는다. 60초마다
connector의 `heartbeat.action.query`가 `debezium_heartbeat.heartbeat`를
upsert한다. 이 변경 덕분에 더 새로운 LSN을 확인할 수 있다. 이 방식은
connector가 실행되는 동안에만 보존된 WAL을 제한한다. 중지되거나 일시정지된
connector는 여전히 `max_slot_wal_keep_size`까지 WAL을 고정한다.

다음 상태는 서로 구분되며 상태마다 자체 증거가 필요하다.

| State | Evidence |
| --- | --- |
| JSON 파일 존재 | Git에만 있으며 아직 등록된 것은 없음 |
| 등록됨 | `GET /connectors/<name>`이 config를 반환함 |
| 실행 중 | `GET /connectors/<name>/status`에서 connector와 task가 `RUNNING`으로 표시됨 |
| Snapshot 완료 | connector metric이나 log에서 초기 snapshot 완료를 확인함 |
| 변경 수집됨 | test 변경이 `hyhome.app.*` topic에 나타남 |

`mng-pg`는 `wal_level=logical`, `max_replication_slots`, `max_wal_senders`,
`max_slot_wal_keep_size`(기본값 2048 MB)를 선언한다. 실행 중인 인스턴스는
승인된 recreate 전까지 이전 command를 그대로 사용한다. recreate하면 Keycloak,
n8n, Airflow 등을 위한 management database가 재시작된다. slot이 존재하면
connector가 확인할 때까지 WAL이 보존되고 그 양은 `max_slot_wal_keep_size`로
제한된다. 이 한도를 넘으면 slot이 무효화되고 새 snapshot이 강제된다. connector
등록, 변경, snapshot 트리거는 connector와 데이터베이스를 명시한 승인이
필요한 runtime 변경이다.

## Runbook Handoff

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

### License and source boundary

Apache Kafka와 Kafbat은 Apache-2.0 프로젝트다. Schema Registry, Connect,
REST 이미지는 Confluent가 제공하며 별도의 현재 license/edition 검토가
필요하다. Cluster Linking이나 다른 edition 전용 기능은 선언하지도 가정하지도
않는다.

### Official references

- [Apache Kafka operations](https://kafka.apache.org/documentation/#operations)
- [Kafka KRaft](https://kafka.apache.org/documentation/#kraft)
- [Kafka license](https://kafka.apache.org/licensing)
- [Schema Registry migration](https://docs.confluent.io/platform/current/schema-registry/installation/migrate.html)
- [Kafbat configuration](https://ui.docs.kafbat.io/configuration/configuration-file)
- [Kafbat RBAC](https://ui.docs.kafbat.io/configuration/rbac-role-based-access-control)
- [Kafbat license](https://github.com/kafbat/kafka-ui/blob/main/LICENSE)


## Common Checks

정확한 root profile, service, health/resource 제어, writable-state 소유권,
secret reference, exposure, 엔진별 복구 경계를 확인한다. static pass는 구성
증거일 뿐이며, runtime과 restore는 별개로 남는다.

## Traceability

- Artifact: `GDE-0036`; 거버넌스 정책: `POL-0036`.
- Runtime authority: `infra/05-messaging/kafka/docker-compose.yml` and the
  [Connect image Dockerfile](../../../infra/05-messaging/kafka/Dockerfile.connect).

## Related Documents

- [Operations policy](../policies/0036-kafka.md)
- [Cluster recovery runbook](../runbooks/0036-kafka.md)
- [Messaging architecture](../../02.architecture/descriptions/0005-messaging-architecture.md)
