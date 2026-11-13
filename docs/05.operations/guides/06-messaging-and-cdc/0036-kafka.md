---
title: "Kafka Usage Guide"
version: "1.3.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "operations"
artifact_id: "GDE-0036"
parent_ids:
- "POL-0036"
implementation_services:
  infra/05-messaging/kafka/docker-compose.yml:
  - 'kafbat-ui'
  - 'kafka-1'
  - 'kafka-exporter'
  - 'kafka-init'
created: "2026-05-10"
---

# Kafka Usage Guide

## Purpose

### Outcome

이 가이드는 OPTIONAL 이벤트 스트리밍 기능인 Kafka family의 구성, 프로파일, 접근 경계를 설명한다. 정상 root는 단일 KRaft broker와 Kafbat UI, exporter, init job을 정의한다. Schema Registry와 Debezium Connect(CDC)는 2026-11-10 owner 결정(ADR-0062 개정)으로 LAB `labs/kafka-cluster`로 옮겼고, 다중 broker 학습도 독립 LAB이다.

대상 독자는 Kafka family를 켜거나 변경하는 운영자와 개발자다. 목표는 어떤 서비스가 어느 profile에서 선택되는지, 어디까지 보호되는지, 복구가 무엇을 포함하는지 확인하는 것이다. 실행 절차는 [RUN-0036](../../runbooks/06-messaging-and-cdc/0036-kafka.md)이 소유한다.

### Boundaries

- Artifact: `GDE-0036`; 상위 정책: `POL-0036`.
- Runtime authority: `infra/05-messaging/kafka/docker-compose.yml`; CDC 경로는 `labs/kafka-cluster/docker-compose.yml`과
  [Connect image Dockerfile](../../../../labs/kafka-cluster/connect/Dockerfile).

- [Messaging architecture](../../../02.architecture/descriptions/0005-messaging-architecture.md)
- [Apache Kafka operations](https://kafka.apache.org/documentation/#operations)
- [Kafka KRaft](https://kafka.apache.org/documentation/#kraft)
- [Kafka license](https://kafka.apache.org/licensing)
- [Schema Registry migration](https://docs.confluent.io/platform/current/schema-registry/installation/migrate.html)
- [Kafbat configuration](https://ui.docs.kafbat.io/configuration/configuration-file)
- [Kafbat RBAC](https://ui.docs.kafbat.io/configuration/rbac-role-based-access-control)
- [Kafbat license](https://github.com/kafbat/kafka-ui/blob/main/LICENSE)

## Prerequisites

### Environment

Kafka는 OPTIONAL 이벤트 스트리밍 기능이다. 정상 root에는 단일
`kafka-1`만 있고, 다중 broker 학습은 독립 LAB 진입점의 `lab-kafka`
프로파일로 분리했다. 세 LAB broker도 한 Docker host를 공유하므로 host
가용성을 증명하지 않는다. 정상 서비스를 지속 실행해야 한다는 HOME consumer는
현재 확인되지 않았다.

#### Current implementation

[`infra/05-messaging/kafka/docker-compose.yml`](../../../../infra/05-messaging/kafka/docker-compose.yml)은
정상 서비스 4개를 정의한다. [`Kafka LAB 안내`](../../../../labs/kafka-cluster/README.md)와 [`labs/kafka-cluster/docker-compose.yml`](../../../../labs/kafka-cluster/docker-compose.yml)은
LAB 전용 브로커 3개·exporter·init·Schema Registry·Connect 7개를 독립 Compose project로 정의하며 정상 root가 include하지 않는다.

| Service | Role | Selector |
| --- | --- | --- |
| `kafka-1` | 단일 KRaft broker/controller | `messaging`, `messaging-broker`, `messaging-admin` |
| `kafbat-ui` | native OIDC/RBAC 관리 UI | `messaging`, `messaging-admin` |
| `kafka-exporter` | broker/consumer lag 메트릭 | `kafka-1`과 같은 세 profile |
| `kafka-init` | RF1 topic bootstrap | `messaging`, `messaging-broker` |
| `lab-kafka-1/2/3`, `lab-kafka-exporter`, `lab-kafka-init`, `lab-schema-registry`, `lab-kafka-connect` | 독립 RF3 실습 closure(Schema Registry·Debezium Connect 포함) | `lab-kafka` |

정상 `kafka-1-data`는
`${DEFAULT_MESSAGE_BROKER_DIR}/kafka/dev-data`의 별도 bind volume이다. 이전 `kafka-connect-data`(`.../kafka/dev-kafka-connect`)는 선언에서 제거했고 HOME에 남은 volume의 처리는 owner 승인 대상이다. LAB 상태는
`${LAB_DATA_DIR}/kafka/{1,2,3}`에 있고 별도 cluster ID, network, topic·offset을
사용하며 `lab_kafka_net`만 쓰고 host port를 게시하지 않는다. broker PLAINTEXT는 내부 network에서만
사용한다. 정상 `kafka-1`은 별도로 `127.0.0.1`에 external listener(`KAFKA_EXTERNAL_1_HOST_PORT`, 기본 `9092`)와 JMX exporter(`19404`)를 게시한다. 인증 없는 JMX 원격 포트(`19101`)는 소비자가 없어 2026-11-09에 제거했다.

Kafbat은 자체 `auth.type: OAUTH2` 구성을 tmpfs에 렌더링하고,
`kafbat_client_secret`을 읽고, local CA를 신뢰하며, group 기반 RBAC를
적용한다. 이 서비스의 Traefik route는 `gateway-standard-chain@file`을
사용한다. gateway는 전송/헤더 보호를 담당하고, 인증 자체는 Kafbat이 수행한다.
이 native-OIDC route에는 forwarding-auth gateway chain을 붙이면 안 된다.
Kafbat은 schema registry와 Connect cluster를 설정하지 않으며 `kafka-1`에만 의존한다. HOME에는 Connect·Schema Registry route가 없다.

### Permissions

Kafbat UI는 Keycloak OIDC와 group 기반 RBAC로 접근이 제한되며 secret은 `kafbat_client_secret` 이름으로만 다룬다. CDC 등록, `dev-pg` slot 삭제, HOME에 남은 volume의 처리는 별도 승인 대상이다(Actions와 Troubleshooting에 기술).

## Procedure

### Actions

정상 사용과 확인 절차는 아래 항목을 따른다.

#### Identity-specific behavior

Compose에 선언된 Confluent CP 이미지가 정상 단일 broker와 LAB 다중 broker에 쓰인다.
정상 `kafka-init`은 RF1, LAB `lab-kafka-init`은 RF3이며 서로 다른
KRaft identity와 저장소를 사용한다. broker/client/controller 경로의
PLAINTEXT는 TLS·인증을 제공하지 않는다. Schema Registry와 Connect는 LAB에서만
제공한다. JMX 설정·exporter 선언만으로 scrape 성공은 증명되지 않는다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `kafbat-ui` | native OIDC/RBAC UI; tmpfs config | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafka-1` | KRaft combined broker/controller 1; 정상 단일 selector | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafka-exporter` | broker/consumer lag metrics | 선언된 endpoint health; scrape/data 기능 별도 | [선택·의존·접속·입력·mount](../../../../infra/05-messaging/kafka/docker-compose.yml) |
| `kafka-init` | RF1 topic creation job; 단일 broker 필요 | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../../infra/05-messaging/kafka/docker-compose.yml) |
| `lab-kafka-1/2/3`, `lab-kafka-exporter`, `lab-kafka-init`, `lab-schema-registry`, `lab-kafka-connect` | 격리 KRaft RF3 실습(Schema Registry·Connect 포함) | 실제 quorum·topic 상태 미검증 | [LAB 선택·상태](../../../../labs/kafka-cluster/README.md) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의 2026-10-01 source snapshot과 official version/build 검토는 W4 Task에 보존했다. 반복 OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.

#### Images, configuration and resource controls

Compose 파일은 핀된 Confluent Kafka, Kafbat, Kafka
exporter 이미지 계열을 소유한다. 저장소 Renovate가 업데이트를 제안하면 버전
projection은 파생된다. broker 키에는 `CLUSTER_ID`, `KAFKA_PROCESS_ROLES`,
quorum/listener/advertised-listener/log/replication 설정, node ID가 포함된다.
Kafbat은
`KAFKA_CLUSTERS_0_*`, `DYNAMIC_CONFIG_ENABLED`, `KAFBAT_OAUTH_CLIENT_ID`와
client-secret 파일을 사용한다. broker는 high stateful 템플릿을,
Kafbat은 medium infrastructure 템플릿을, exporter는 low를, init
job은 low를 extend한다. 모든 장기 실행 서비스는 healthcheck를 선언한다.

#### Static preflight and profile choice

정적 render 명령은 [RUN-0036 절차](../../runbooks/06-messaging-and-cdc/0036-kafka.md#actions)가 소유한다. 정상 `kafka-init`은 RF1,
LAB `lab-kafka-init`은 RF3이다. LAB의 `LAB_KAFKA_CLUSTER_ID`는 정상
`KAFKA_CLUSTER_ID`와 달라야 한다. 서비스 시작과 topic 생성은 별도 runtime
승인 대상이다.

#### Change data capture (LAB)

CDC 경로(Debezium Connect와 Schema Registry)는 HOME에서 `labs/kafka-cluster`로 옮겼다
([LAB 안내](../../../../labs/kafka-cluster/README.md), ADR-0062 개정 2026-11-10). 근거는 HOME에서
Connect connector 0개, Schema Registry subject 0개, consumer group 0개, `application-logs`·`infra-events`
메시지 0건이었고 CDC 원천 DB `platform_dev`가 없었다는 점이다. `cdc`, `messaging-schema`,
`messaging-connect` profile은 폐기했고 `debezium-db-provision`, 커넥터 샘플(`postgres-connector.json`),
기능 SQL과 secret renderer는 제거했다(Git 이력이 보존한다). HOME에서 CDC를 다시 쓰려면 POL-0107
승격 또는 새 결정이 필요하며, 이때 slot·publication·topic은 새 원천에서 새로 만든다.

LAB의 Connect worker에는 connector, 원천 DB, credential이 선언되어 있지 않다. 등록은 별도 승인이며
상태별 증거는 다음과 같다.

| State | Evidence |
| --- | --- |
| 등록됨 | `GET /connectors/<name>`이 config를 반환함 |
| 실행 중 | `GET /connectors/<name>/status`에서 connector와 task가 `RUNNING`으로 표시됨 |
| Snapshot 완료 | connector metric이나 log에서 초기 snapshot 완료를 확인함 |
| 변경 수집됨 | test 변경이 대상 topic에 나타남 |

중단된 replication slot은 원천 DB의 WAL을 고정할 수 있으므로 원천을 연결하면 lag와 WAL 용량을 별도로 관측한다.
HOME `dev-pg`는 `wal_level=logical`과 slot 한도 선언이 남아 있으나 현재 소비자가 없다.

### Exceptions

예외와 제한 사항은 아래 항목에 정리한다.

#### License and source boundary

Apache Kafka와 Kafbat은 Apache-2.0 프로젝트다. LAB의 Schema Registry와 Connect
이미지는 Confluent가 제공하며 별도의 현재 license/edition 검토가
필요하다. Cluster Linking이나 다른 edition 전용 기능은 선언하지도 가정하지도
않는다.

## Verification

### Expected Result

정확한 root profile, service, health/resource 제어, writable-state 소유권,
secret reference, exposure, 엔진별 복구 경계를 확인한다. static pass는 구성
증거일 뿐이며, runtime과 restore는 별개로 남는다.

### Troubleshooting

- `kafka-1` unhealthy: healthcheck는 `kafka-broker-api-versions --bootstrap-server localhost:19092`다. 실행마다 JVM을 띄워(CPU 약 2.5초) 간격은 60초이고, 시작 중에만 5초다. `${DEFAULT_MESSAGE_BROKER_DIR}/kafka/dev-data` 권한과 `KAFKA_CLUSTER_ID` 일치를 먼저 확인한다.
- `dev-pg` WAL 증가: 과거 Debezium slot(`hyhome_platform_slot`)이 생성된 적이 있다면 WAL을 고정할 수 있다. slot 삭제는 [POL-0036](../../policies/06-messaging-and-cdc/0036-kafka.md)의 재동기화 승인 대상이다.

#### Runbook Handoff

Kafka 복구 범위는 broker 디렉터리보다 넓다. topic 데이터와 config,
partition 수, consumer-group offset, KRaft cluster metadata를 목록으로 정리한다.
LAB에 Schema Registry나 Connect를 쓰면 `_schemas` history/ID와 connector 정의·config/offset/status
topic도 같은 목록에 넣는다. 신뢰할 수 있는 producer source에서 replay하거나,
새로 격리한 cluster로 승인된 cross-cluster replication을 하는 방식을 우선한다.
원시 broker log-directory 재사용과 실행 중인 KRaft identity 재사용은 금지한다.

[RUN-0036](../../runbooks/06-messaging-and-cdc/0036-kafka.md)은 의존 레코드보다 먼저 schema를
복원하고, topic 구성을 재생성하고, offset을 복원/재배치하고, connector를
일시정지 상태로 유지하며, cutover 전에 end offset과 애플리케이션 소비를
증명한다. 이미지나 프로토콜 업그레이드에는 Kafka, Confluent 구성 요소,
Kafbat, 클라이언트, 저장 형식에 대한 공식 호환성 검토와 현재 recovery
artifact 및 rollback이 필요하다.

- [Operations policy](../../policies/06-messaging-and-cdc/0036-kafka.md)
- [Cluster recovery runbook](../../runbooks/06-messaging-and-cdc/0036-kafka.md)
