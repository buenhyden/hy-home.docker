---
title: "Kafka Cluster LAB Usage Guide"
version: "0.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-05"
layer: "operations"
artifact_id: "GDE-0108"
parent_ids:
- "POL-0108"
implementation_services:
  labs/kafka-cluster/docker-compose.yml:
  - lab-kafka-1
  - lab-kafka-2
  - lab-kafka-3
  - lab-kafka-exporter
  - lab-kafka-init
created: "2026-11-05"
---

# Kafka Cluster LAB Usage Guide

## Overview

[`labs/kafka-cluster/docker-compose.yml`](../../../../labs/kafka-cluster/docker-compose.yml)은
독립 Compose project `hy-home-lab-kafka`의 세 broker KRaft cluster LAB이다. 정상 root는 이 파일을
include하지 않는다. 세 broker가 한 host를 공유하므로 host 장애 가용성 실험이 아니다.

## Scope

### Audience and Goal

대상 독자: 운영자, 개발자, AI Agent.

목적: Kafka LAB의 구성, 격리 경계, 정적 검증과 승격 계획을 현재 Compose와 맞춰 이해한다. HOME의
단일 broker는 [GDE-0036](../06-messaging-and-cdc/0036-kafka.md)이 다룬다.

## Concepts

`lab-kafka` profile이 전체 closure를 선택한다.

| 서비스 | 역할 | 준비 상태 판단 |
| --- | --- | --- |
| `lab-kafka-1`, `lab-kafka-2`, `lab-kafka-3` | KRaft broker와 controller를 겸하는 node | `kafka-broker-api-versions` healthcheck; topic·ISR 상태는 별도 확인 |
| `lab-kafka-exporter` | `lab-kafka-1`을 target으로 하는 metrics exporter | `/metrics` 응답; scrape 연결은 없음 |
| `lab-kafka-init` | `lab-events`(3 partition)와 `lab-logs`(6 partition)를 replication factor 3으로 만드는 one-shot job | 종료 코드; 실제 topic 상태는 별도 확인 |

- 정확한 image pin, limit과 template은 Compose와
  [공통 template](../../../../infra/common-optimizations.yml)이 소유한다. broker는
  `template-stateful-high`를 extend하고 CPU 0.75, memory 1536m로 제한한다.
- `KAFKA_MIN_INSYNC_REPLICAS`가 2이므로 `acks=all` 쓰기는 broker 하나의 손실을 견딘다.
  topic 자동 생성은 꺼져 있다.
- broker 상태는 `${LAB_DATA_DIR}/kafka/{1,2,3}`의 bind volume이며 HOME
  `${DEFAULT_MESSAGE_BROKER_DIR}`와 분리된다.
- `lab_kafka_net`은 internal network다. host port, HOME `kafka_net`, secret, Schema Registry,
  Connect는 연결하지 않는다. PLAINTEXT 접근은 LAB network 안에 한정한다.

## Usage

### Operator input

`LAB_KAFKA_CLUSTER_ID`는 필수이며 HOME `KAFKA_CLUSTER_ID`와 달라야 하고 KRaft 형식이어야 한다.
HOME 입력의 render는 `NOT_RUN`이다. 2026-11-05 controller 보고에 따르면 `labs/.env`에 이 값이
없다(agent는 그 파일을 읽지 않는다). owner가 `labs/.env`에 값을 넣어야 HOME render, `lab.py check`와 readiness 검사를 실행할 수 있다.

### Static check

repository root에서 합성 LAB 경로와 HOME과 다른 LAB ID로 render한다. 이 명령은 서비스를 시작하지
않는다.

```bash
LAB_DATA_DIR=/tmp/hyhome-lab-kafka-synthetic LAB_KAFKA_CLUSTER_ID=MkU3OEVBNTcwNTJENDM2Qk docker compose --env-file labs/.env.example -f labs/kafka-cluster/docker-compose.yml --profile lab-kafka config --quiet
```

기동과 정지는 [RUN-0108](../../runbooks/15-labs/0108-kafka-cluster.md)의 `lab.py` 절차만 쓴다.
이 LAB은 HOME에서 기동된 기록이 없으므로 runtime 동작, topic 생성과 복구는 미검증이다.

### Promotion

[promotion manifest](../../../../labs/kafka-cluster/promotion.yaml)는 `replace-same`이며 목적지는
`infra/05-messaging/kafka/`, profile `messaging`이다. HOME `kafka-1`, `kafka-exporter`,
`kafka-init`을 은퇴시킨다. 문서 목적지는 `06-messaging-and-cdc` 역할 폴더다. 승격 절차는
[RUN-0107](../../runbooks/15-labs/0107-lab-promotion.md)이 소유한다.

### Common Checks

정확한 profile, 세 data 경로의 분리, internal network, 서로 다른 cluster ID와 limit을 render로
확인한다. 정적 통과는 configuration 증거일 뿐이다.

### Runbook Handoff

정적 점검, 기동·정지와 복구 계획은 [RUN-0108](../../runbooks/15-labs/0108-kafka-cluster.md)을 따른다.

### Traceability

- Artifact: `GDE-0108`; governing policy: `POL-0108`.
- Version projection: [tech-stack versions](../../../../infra/tech-stack.versions.json)는 Compose에서 파생된 drift 증거이며 정확한 pin은 Compose가 소유한다.
- Runtime authority: `labs/kafka-cluster/docker-compose.yml`.

## Troubleshooting

- render가 `set a unique LAB KRaft cluster ID`로 실패하면 `LAB_KAFKA_CLUSTER_ID`가 없다.
- render가 `set isolated LAB data root`로 실패하면 `LAB_DATA_DIR`이 없다.
- broker가 healthy가 되지 않으면 [RUN-0108](../../runbooks/15-labs/0108-kafka-cluster.md)의 진단으로 넘긴다.

## Related Documents

- [Operations policy](../../policies/15-labs/0108-kafka-cluster.md)
- [Kafka LAB README](../../../../labs/kafka-cluster/README.md)
- [Kafka LAB runbook](../../runbooks/15-labs/0108-kafka-cluster.md)
- [LAB promotion policy](../../policies/15-labs/0107-lab-promotion.md)
- [HOME Kafka guide](../06-messaging-and-cdc/0036-kafka.md)
- [Apache Kafka KRaft](https://kafka.apache.org/documentation/#kraft)
