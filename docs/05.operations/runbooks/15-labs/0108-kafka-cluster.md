---
title: "Kafka Cluster LAB Runbook"
version: "0.2.1"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "operations"
artifact_id: "RUN-0108"
parent_ids:
- "GDE-0108"
created: "2026-11-05"
---

# Kafka Cluster LAB Runbook

## Purpose

### Trigger and Outcome

Kafka LAB([`labs/kafka-cluster/docker-compose.yml`](../../../../labs/kafka-cluster/docker-compose.yml), project `hy-home-lab-kafka`)의 정적 점검,
`lab.py` 기동·정지, broker 진단과 복구 계획을 다룬다.

Kafka LAB의 정적 검증, 승인된 실험 기동, broker·topic 이상 진단, 승격 전 readiness 확인에 쓴다.

### Scope

- Runtime source: [Kafka LAB Compose](../../../../labs/kafka-cluster/docker-compose.yml).
- Artifact: `RUN-0108`; parent guide: `GDE-0108`.
- Version projection: [tech-stack versions](../../../../infra/tech-stack.versions.json)는 Compose에서 파생된 drift 증거이며 정확한 pin은 Compose가 소유한다.

- [Kafka LAB guide](../../guides/15-labs/0108-kafka-cluster.md)
- [LAB promotion runbook](0107-lab-promotion.md)
- [Domain catalog](../../README.md)

## Preconditions

### Authority and Access

- 기동 전 Docker context, project 이름, network·volume, 가용 CPU·memory·disk, `${LAB_DATA_DIR}/kafka/`
  의 UID/GID와 정리 대상을 owner가 승인한다.
- 이 런북의 모든 runtime 단계는 별도 승인이 필요하다. 이 문서 작성에서는 아무것도 실행하지 않았다.

### Safety Checks

- `labs/.env`에 `LAB_DATA_DIR`과 HOME과 다른 `LAB_KAFKA_CLUSTER_ID`가 있다. HOME 입력의
  render는 `NOT_RUN`이다. 2026-11-05 controller 보고에 따르면 `LAB_KAFKA_CLUSTER_ID`가 없다.
  owner가 값을 넣는다.

#### Static check

repository root에서 합성 입력으로 render한다.

```bash
LAB_DATA_DIR=/tmp/hyhome-lab-kafka-synthetic LAB_KAFKA_CLUSTER_ID=MkU3OEVBNTcwNTJENDM2Qk docker compose --env-file labs/.env.example -f labs/kafka-cluster/docker-compose.yml --profile lab-kafka config --services
```

일곱 서비스 `lab-kafka-1`, `lab-kafka-2`, `lab-kafka-3`, `lab-kafka-exporter`, `lab-kafka-init`,
`lab-schema-registry`, `lab-kafka-connect`가 나와야 한다. 다르면 멈춘다.

## Steps

### Actions

기동·정지, 진단, HOME 퇴역, 복구 계획, readiness 확인은 다음과 같다.

#### Start and stop

승인된 경우에만 `lab.py`로 기동·정지한다. 이 명령은 HOME·다른 LAB과의 충돌과 선언 limit 예산을 먼저
검사하고 정리 대상을 ledger에 남긴다.

```bash
python3 scripts/operations/lab.py check kafka-cluster
python3 scripts/operations/lab.py up kafka-cluster --purpose "<목적>" --lease <기간>
python3 scripts/operations/lab.py down kafka-cluster
```

`down -v`와 volume prune은 쓰지 않는다. `down`은 volume을 남긴다.

#### Diagnosis

1. `docker compose -p hy-home-lab-kafka ps`로 세 broker의 health를 본다.
2. broker가 unhealthy이면 그 broker log에서 cluster ID 불일치, data 디렉터리 권한, quorum 연결
   실패를 찾는다. log 원문은 evidence에 붙이지 않는다.
3. `lab-kafka-init`이 실패하면 세 broker가 healthy인지 먼저 확인한다. init은 `--if-not-exists`이므로
   broker가 회복된 뒤 다시 실행해도 된다.
4. topic 상태는 LAB network 안에서 `kafka-topics --describe`로 partition leader와 ISR을 확인한다.
5. `lab-schema-registry`나 `lab-kafka-connect`가 unhealthy이면 세 broker가 healthy인지 먼저 확인한다.
   Connect는 `lab-schema-registry`가 healthy가 된 뒤에 시작한다. 두 서비스의 상태는 broker topic
   (`_schemas`, `_connect-*`)에 있으므로 broker 데이터를 지우지 않는다.

#### HOME retirement of Schema Registry and Connect (owner approval required)

ADR-0062 개정(2026-11-10)은 소스만 옮긴다. HOME에는 `kafka-connect`, `schema-registry` 컨테이너, `kafka-connect-data`
volume, 두 Traefik router와 Debezium 비밀번호 파일(`secrets/db/dev-pg/debezium_password.txt`)이 남아 있다.
owner가 승인한 뒤에만 다음 순서를 따른다.

1. 변경이 반영된 `kafbat-ui`와 `prometheus`를 재생성해 제거된 schema registry·Connect 설정과 scrape를 내린다.
2. `kafka-connect`, `schema-registry` 컨테이너를 정지하고 제거한다. HOME `kafka-1`, `kafka-init`, `kafka-exporter`는 건드리지 않는다.
3. `kafka-connect-data` volume과 Debezium 비밀번호 파일은 보존 여부를 결정한 뒤에만 정리한다. 삭제는 별도 승인이 필요하다.
4. 잔여 network `kafka_connect_ingress_net`, `schema_registry_ingress_net`과 Keycloak/DNS 항목을 정리한다.

#### Planned backup and isolated restore

1. 승인된 window에서 producer를 멈추고 topic 목록, 설정, partition, consumer offset을 기록한다.
2. 승인된 replay 또는 replication으로 새 격리 cluster에 복원한다. 기존 KRaft identity나 개별 broker
   디렉터리를 재사용하지 않는다.
3. topic별 record 수와 offset을 비교하고 결과를 Task에 기록한다.

이 절차는 계획이며 실행된 적이 없다.

#### Readiness

승격 전 [RUN-0107](0107-lab-promotion.md)의 readiness 검사를 `kafka-cluster`로 실행한다.

### Stop Conditions

render된 서비스가 Static check에 나열한 일곱 서비스와 다르면 멈춘다. HOME 경로가 render에 나타나거나 데이터 소유가 불명확하면 멈추고 @buenhyden에게 보고한다.

## Validation

### Service Checks

Static check render에 일곱 서비스가 나오고 세 broker가 healthy이며, topic의 partition leader와 ISR이 확인되어야 한다.

### Evidence

source revision, 실행한 명령과 종료 코드, broker health, topic·ISR 요약, 미검증 gap을 기록한다.
secret, raw log와 rendered private 설정은 기록하지 않는다.

## Recovery

### Rollback

LAB은 HOME 소비자가 없으므로 `lab.py down kafka-cluster`로 멈추면 HOME에 영향이 없다. 데이터는
`${LAB_DATA_DIR}/kafka/`에 남는다. 삭제는 별도 승인이다.

### Escalation

cluster ID가 HOME과 같거나, HOME 경로가 render에 나타나거나, 데이터 소유가 불명확하면 멈추고
@buenhyden에게 보고한다.
