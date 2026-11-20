---
title: "Kafka Cluster LAB"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2026-10-03"
---

# Kafka 다중 broker LAB

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Service

##### Purpose

[`docker-compose.yml`](docker-compose.yml)은 독립 Compose project
`hy-home-lab-kafka`입니다. 정상 root는 이 파일을 include하지 않습니다.
`lab-kafka-1/2/3` KRaft broker/controller, `lab-kafka-exporter`,
`lab-kafka-init`, `lab-schema-registry`, `lab-kafka-connect`가 전체 closure이며 모두 `lab-kafka`
프로파일에 속합니다. Schema Registry와 Debezium plugin Connect는 2026-11-10 owner 결정(ADR-0062 개정)으로
HOME `05-messaging`에서 옮겼습니다(HOME에서 connector 0개, subject 0개). 세 broker가 한 호스트를
공유하므로 호스트 장애 가용성 실험은 아닙니다.

###### Audience
<!-- core-payload-level:4 -->

독립 Kafka 토폴로지를 검토하는 개발자와 운영자.

###### Scope
<!-- core-payload-level:4 -->

학습용 세 broker의 독립 Compose, 네트워크, 저장소와 정적 검증을 다룬다. 실제 실행과 데이터 이관은 별도 승인이다.

###### Structure
<!-- core-payload-level:4 -->

```text
labs/kafka-cluster/
├── docker-compose.yml # 독립 LAB entrypoint
├── promotion.yaml     # SPEC-0263 승격 manifest
├── connect/Dockerfile # Connect worker image (Debezium PostgreSQL plugin)
├── dashboards/        # HOME에서 옮긴 kafka-connect.json, schema-registry.json
└── README.md          # 서비스 README
```

| Dashboard | UID | Source |
| --- | --- | --- |
| [`kafka-connect.json`](./dashboards/kafka-connect.json) | `hyhome-kafka-connect` | confluentinc/jmx-monitoring-stacks@f376263fc6d7 jmxexporter-prometheus-grafana/assets/grafana/provisioning/dashboards/kafka-connect-cluster.json |
| [`schema-registry.json`](./dashboards/schema-registry.json) | `hyhome-schema-registry` | confluentinc/jmx-monitoring-stacks@f376263fc6d7 jmxexporter-prometheus-grafana/assets/grafana/provisioning/dashboards/schema-registry-cluster.json |

HOME Grafana는 `infra/06-observability/grafana/dashboards/`만 provisioning하므로
이 대시보드는 HOME에 표시되지 않고, HOME Prometheus는 LAB 서비스를 수집하지 않습니다.

`docker-compose.yml`이 전체 LAB closure를 정의하고 이 문서가 사용·복구 경계를 소유한다.
[promotion manifest](promotion.yaml)는 HOME 단일 broker를 같은 형태로 대체하는 승격 계획이다.

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| `lab-kafka-1/2/3` PLAINTEXT(`lab_kafka_net`) | `lab-kafka-1`, `lab-kafka-2`, `lab-kafka-3` | `lab-kafka-init`, `lab-schema-registry`, `lab-kafka-connect` | PLAINTEXT 접근은 LAB network 내부에 한정되며 호스트 port·`kafka_net`·secret을 연결하지 않는다. | 복구는 RUN-0108 Kafka cluster LAB Runbook을 따른다. |
| topic `lab-events`, `lab-logs` | `lab-kafka-init` | 이 README는 소비자를 기록하지 않는다. | 세 broker가 healthy일 때 replication factor 3으로 생성한다. | 생성 job 성공과 실제 topic 상태는 별개로 확인해야 한다. |
| `lab-schema-registry`, `lab-kafka-connect` | `lab-schema-registry`, `lab-kafka-connect` | 이 README는 소비자를 기록하지 않는다. | `lab_kafka_net` 안에서만 도달하고 gateway route가 없으며 Connect는 connector 없이 Debezium worker만 제공한다. | subject·connector 정의와 `_schemas`·`_connect-*` 상태도 복구 범위에 포함된다. |

###### Inputs and Outputs
<!-- core-payload-level:4 -->

| Field | Evidence |
| --- | --- |
| Project | `hy-home-lab-kafka` |
| Services | `lab-kafka-1`, `lab-kafka-2`, `lab-kafka-3`, `lab-kafka-init`, `lab-kafka-exporter`, `lab-schema-registry`, `lab-kafka-connect` |

- 필수 `LAB_KAFKA_CLUSTER_ID`는 정상 `KAFKA_CLUSTER_ID`와 달라야 하며 KRaft 형식에 맞아야 합니다. 기존 cluster의 metadata·offset·broker 디렉터리를 재사용하지 않습니다.
- broker별 bind 상태는 `${LAB_DATA_DIR}/kafka/{1,2,3}`이고 정상 `${DEFAULT_MESSAGE_BROKER_DIR}`와 분리합니다. 호스트 디렉터리를 미리 만들고 실제 UID/GID와 용량을 확인한 뒤에만 실행합니다.
- `lab_kafka_net`은 이 project 내부 network입니다. 호스트 port, 정상 `kafka_net`, secret은 연결하지 않습니다. Schema Registry와 Connect도 이 network 안에서만 도달하며 gateway route가 없습니다. PLAINTEXT 접근은 LAB network 내부에 한정합니다.
- `lab-kafka-connect`는 Debezium PostgreSQL plugin을 담은 worker(`connect/Dockerfile`)만 제공합니다. connector, 원천 DB, credential은 선언하지 않으며(HOME의 `platform_dev` 원천도 없었습니다) 등록은 별도 승인입니다. 상태는 broker의 `_connect-*`와 `_schemas` topic에 있고 별도 volume이 없습니다.
- 동봉한 [대시보드](dashboards/)는 HOME 시절 JMX 지표용이며 이 LAB은 JMX agent를 쓰지 않으므로 그대로는 데이터가 없습니다.
- `lab-kafka-init`은 세 broker가 healthy일 때 LAB topic `lab-events`, `lab-logs`를 replication factor 3으로 생성합니다. 생성 job의 성공과 실제 topic 상태는 별개로 확인해야 합니다.

###### Security Boundary
<!-- core-payload-level:4 -->

`lab_kafka_net`은 project 내부 network이며 호스트 port, 정상 `kafka_net`, secret을 연결하지 않는다. Schema Registry와 Connect는 이 network 안에서만 도달하고 gateway route가 없다.

#### Usage

##### Prerequisites

KRaft 모드 broker 3개와 Schema Registry, Debezium PostgreSQL plugin Connect가 Compose project `hy-home-lab-kafka`의 `lab-kafka` profile로 실행된다. 세 broker가 한 호스트를 공유하므로 호스트 장애 가용성은 검증하지 않는다.

##### Selected Start

저장소 루트에서 합성된 LAB 경로와 정상 cluster와 다른 LAB ID를 공급하여 다음 명령을 실행합니다. 이 명령은 서비스를 시작하지 않습니다.

```bash
LAB_DATA_DIR=/tmp/hyhome-lab-kafka-synthetic LAB_KAFKA_CLUSTER_ID=MkU3OEVBNTcwNTJENDM2Qk docker compose --env-file labs/.env.example -f labs/kafka-cluster/docker-compose.yml --profile lab-kafka config --quiet
```

실행 전 Docker context, project name, 모든 port·network·volume, 가용 CPU/RAM/디스크, host bind UID/GID와 정확한 정리 대상이 별도로 승인되어야 합니다. 기동·종료는 `python3 scripts/operations/lab.py up kafka-cluster --purpose "<목적>" --lease <기간>`과 `lab.py down kafka-cluster`로 하며 충돌·예산 검사와 정리 대상 ledger를 남깁니다. 이 문서 갱신에서 LAB를 실행·정지하거나 상태를 삭제하지 않았습니다. `down -v` 또는 volume prune은 사용하지 않습니다. source 선언만으로 이전 정상 root의 broker 2/3 컨테이너가 정지되지는 않습니다.

#### Checks

##### Readiness

검증 명령은 Selected Start의 정적 render(`docker compose ... --profile lab-kafka config --quiet`)이며 서비스를 시작하지 않는다. render 통과는 broker 기동이나 topic 생성의 증거가 아니다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [Kafka LAB Compose](docker-compose.yml)
- [운영 가이드 목록](../../docs/05.operations/01.guides/README.md)
- [15-labs runbooks](../../docs/05.operations/03.runbooks/15.labs/README.md): RUN-0108 kafka-cluster, RUN-0107 lab-promotion
- [06-messaging-and-cdc runbooks](../../docs/05.operations/03.runbooks/06.messaging-and-cdc/README.md): RUN-0036 kafka

###### Observability and Recovery
<!-- core-payload-level:4 -->

`lab-kafka-init`은 세 broker가 healthy일 때 topic `lab-events`, `lab-logs`를 만들며 생성 job 성공과 실제 topic 상태는 별개로 확인해야 한다. 복구는 [15-labs runbooks](../../docs/05.operations/03.runbooks/15.labs/README.md)의 RUN-0108 Kafka cluster LAB Runbook를 따른다.

복구에는 topic record/config, partition, consumer offset와 KRaft metadata를
포함합니다. Schema Registry·Connect의 subject, connector 정의와
`_schemas`·`_connect-*` 내부 상태도 같은 복구 범위입니다. 승인된 replay/replication으로 새
격리 cluster에 복원하며 기존 KRaft identity나 개별 broker directory를 그대로
재사용하지 않습니다. source 안내 갱신은 실제 복구 검증이 아닙니다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
