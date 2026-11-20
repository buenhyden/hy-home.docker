---
title: "Kafka Cluster LAB Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "RUN-0108"
parent_ids:
- "GDE-0108"
created: "2026-11-05"
next_review_at: "2027-05-13"
---

# Kafka Cluster LAB Runbook

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the runbook payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Trigger and Scope

##### Trigger

Kafka LAB([`labs/kafka-cluster/docker-compose.yml`](../../../../labs/kafka-cluster/docker-compose.yml), project `hy-home-lab-kafka`)의 정적 점검,
`lab.py` 기동·정지, broker 진단과 복구 계획을 다룬다.

Kafka LAB의 정적 검증, 승인된 실험 기동, broker·topic 이상 진단, 승격 전 readiness 확인에 쓴다.

##### Targets

- Runtime source: [Kafka LAB Compose](../../../../labs/kafka-cluster/docker-compose.yml).
- Artifact: `RUN-0108`; parent guide: `GDE-0108`.
- Version projection: [tech-stack versions](../../../../infra/tech-stack.versions.json)는 Compose에서 파생된 drift 증거이며 정확한 pin은 Compose가 소유한다.

- [Kafka LAB guide](../../01.guides/15.labs/0108-kafka-cluster.md)
- [LAB promotion runbook](0107-lab-promotion.md)
- [Domain catalog](../../README.md)

#### Preflight

##### Authority

- 기동 전 Docker context, project 이름, network·volume, 가용 CPU·memory·disk, `${LAB_DATA_DIR}/kafka/`
  의 UID/GID와 정리 대상을 owner가 승인한다.
- 이 런북의 모든 runtime 단계는 별도 승인이 필요하다. 이 문서 작성에서는 아무것도 실행하지 않았다.

##### Environment

- `labs/.env`에 `LAB_DATA_DIR`과 HOME과 다른 `LAB_KAFKA_CLUSTER_ID`가 있다. HOME 입력의
  render는 `NOT_RUN`이다. 2026-11-05 controller 보고에 따르면 `LAB_KAFKA_CLUSTER_ID`가 없다.
  owner가 값을 넣는다.

###### Static check
<!-- core-payload-level:4 -->

repository root에서 합성 입력으로 render한다.

```bash
LAB_DATA_DIR=/tmp/hyhome-lab-kafka-synthetic LAB_KAFKA_CLUSTER_ID=MkU3OEVBNTcwNTJENDM2Qk docker compose --env-file labs/.env.example -f labs/kafka-cluster/docker-compose.yml --profile lab-kafka config --services
```

일곱 서비스 `lab-kafka-1`, `lab-kafka-2`, `lab-kafka-3`, `lab-kafka-exporter`, `lab-kafka-init`,
`lab-schema-registry`, `lab-kafka-connect`가 나와야 한다. 다르면 멈춘다.

#### Procedure

##### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | Start and stop: 승인된 경우에만 `lab.py check/up/down kafka-cluster` 실행 | 충돌과 limit 예산 검사 후 정리 대상을 ledger에 기록, `down`은 volume을 남김 | `down -v`와 volume prune은 쓰지 않음 |
| 2 | Diagnosis: 활성 lease에서 LAB project를 지정해 세 broker와 companion 상태(`ps`) 확인 | 세 broker가 healthy | 중단하고 @buenhyden에게 보고 |
| 3 | Diagnosis: broker unhealthy 시 log에서 cluster ID 불일치, data 디렉터리 권한, quorum 연결 실패 확인 | 문서에 기록 없음 | log 원문은 evidence에 붙이지 않음 |
| 4 | Diagnosis: `lab-kafka-init` 실패 시 세 broker healthy 확인 후 재실행 | 문서에 기록 없음 | init은 `--if-not-exists`이므로 broker 회복 뒤 재실행 가능 |
| 5 | Diagnosis: LAB network 안에서 `kafka-topics --describe`로 partition leader와 ISR 확인 | topic의 partition leader와 ISR이 확인됨 | 문서에 기록 없음 |
| 6 | Diagnosis: `lab-schema-registry`/`lab-kafka-connect` unhealthy 시 세 broker healthy 확인 | 문서에 기록 없음 | broker 데이터를 지우지 않음 |
| 7 | HOME retirement: 변경이 반영된 `kafbat-ui`와 `prometheus` 재생성 (owner 승인 필요) | 제거된 schema registry/Connect 설정과 scrape가 내려감 | LAB project나 소유가 불명확한 후보에는 작업하지 않음 |
| 8 | HOME retirement: HOME `kafka-connect`와 `schema-registry`에서 확인된 ID만 정지/제거 | 문서에 기록 없음 | HOME `kafka-1`/`kafka-init`/`kafka-exporter`는 건드리지 않음 |
| 9 | HOME retirement: `kafka-connect-data` volume은 보존 여부 결정 후에만 정리 | 문서에 기록 없음 | 삭제는 별도 승인 필요 |
| 10 | HOME retirement: 잔여 network와 Keycloak/DNS 항목 정리 | 문서에 기록 없음 | 문서에 기록 없음 |
| 11 | Planned backup and isolated restore: 승인된 window에서 producer 정지 후 topic 목록/설정/partition/consumer offset 기록 | 문서에 기록 없음 | 데이터 소유가 불명확하면 멈추고 @buenhyden에게 보고 |
| 12 | Planned backup and isolated restore: 승인된 replay 또는 replication으로 새 격리 cluster에 복원 | 문서에 기록 없음 | 기존 KRaft identity나 broker 디렉터리를 재사용하지 않음 |
| 13 | Planned backup and isolated restore: topic별 record 수와 offset을 비교하고 Task에 기록 | 결과를 Task에 기록 | 문서에 기록 없음 |
| 14 | Readiness: 승격 전 RUN-0107의 readiness 검사를 `kafka-cluster`로 실행 | 문서에 기록 없음 | RUN-0107에 따름 |

기동·정지, 진단, HOME 퇴역, 복구 계획, readiness 확인은 다음과 같다.

###### Start and stop
<!-- core-payload-level:4 -->

승인된 경우에만 `lab.py`로 기동·정지한다. 이 명령은 HOME·다른 LAB과의 충돌과 선언 limit 예산을 먼저
검사하고 정리 대상을 ledger에 남긴다.

```bash
python3 scripts/operations/lab.py check kafka-cluster
python3 scripts/operations/lab.py up kafka-cluster --purpose "<목적>" --lease <기간>
python3 scripts/operations/lab.py down kafka-cluster
```

`down -v`와 volume prune은 쓰지 않는다. `down`은 volume을 남긴다.

###### Diagnosis
<!-- core-payload-level:4 -->

1. 활성 lease와 승인된 Docker context에서 LAB project를 지정해 세 broker와 companion의 상태를 확인한다.
   `LAB_ENV_FILE`은 그 lease를 시작할 때 사용한 LAB 환경 파일의 경로다.

   ```bash
   docker compose --project-name hy-home-lab-kafka --env-file "$LAB_ENV_FILE" -f labs/kafka-cluster/docker-compose.yml --profile lab-kafka ps
   ```

2. broker가 unhealthy이면 그 broker log에서 cluster ID 불일치, data 디렉터리 권한, quorum 연결
   실패를 찾는다. log 원문은 evidence에 붙이지 않는다.
3. `lab-kafka-init`이 실패하면 세 broker가 healthy인지 먼저 확인한다. init은 `--if-not-exists`이므로
   broker가 회복된 뒤 다시 실행해도 된다.
4. topic 상태는 LAB network 안에서 `kafka-topics --describe`로 partition leader와 ISR을 확인한다.
5. `lab-schema-registry`나 `lab-kafka-connect`가 unhealthy이면 세 broker가 healthy인지 먼저 확인한다.
   Connect는 `lab-schema-registry`가 healthy가 된 뒤에 시작한다. 두 서비스의 상태는 broker topic
   (`_schemas`, `_connect-*`)에 있으므로 broker 데이터를 지우지 않는다.

###### HOME retirement of Schema Registry and Connect (owner approval required)
<!-- core-payload-level:4 -->

ADR-0062 개정(2026-11-10)은 HOME에서 LAB으로 소스만 옮겼다. 당시 HOME의 `kafka-connect`,
`schema-registry` 컨테이너와 `kafka-connect-data` volume은 퇴역 대기였다.
같은 날 PG-025와 Debezium 비밀번호 파일은 소비자 제거 후 별도로 퇴역했다(SPEC-0212-TSK-0048).
현재 컨테이너·volume·router의 존재는 확인되지 않았다. 별도 승인으로 Docker context와 HOME project
`hy-home-infra`의 대상 service label·컨테이너 ID, volume과 router 소유 및 보존 결정을 확인한다.
LAB project나 소유가 불명확한 후보에는 작업하지 않는다. 확인한 대상에만 다음 순서를 적용한다.

1. 변경이 반영된 `kafbat-ui`와 `prometheus`를 재생성해 제거된 schema registry·Connect 설정과 scrape를 내린다.
2. HOME의 `kafka-connect`와 `schema-registry`에서 확인된 ID만 정지·제거한다.
   HOME `kafka-1`, `kafka-init`, `kafka-exporter`는 건드리지 않는다.
3. `kafka-connect-data` volume은 보존 여부를 결정한 뒤에만 정리한다. 삭제는 별도 승인이 필요하다.
4. 잔여 network `kafka_connect_ingress_net`, `schema_registry_ingress_net`과 Keycloak/DNS 항목을 정리한다.

###### Planned backup and isolated restore
<!-- core-payload-level:4 -->

1. 승인된 window에서 producer를 멈추고 topic 목록, 설정, partition, consumer offset을 기록한다.
2. 승인된 replay 또는 replication으로 새 격리 cluster에 복원한다. 기존 KRaft identity나 개별 broker
   디렉터리를 재사용하지 않는다.
3. topic별 record 수와 offset을 비교하고 결과를 Task에 기록한다.

이 절차는 계획이며 실행된 적이 없다.

###### Readiness
<!-- core-payload-level:4 -->

승격 전 [RUN-0107](0107-lab-promotion.md)의 readiness 검사를 `kafka-cluster`로 실행한다.

##### Stop Conditions

render된 서비스가 Static check에 나열한 일곱 서비스와 다르면 멈춘다. HOME 경로가 render에 나타나거나 데이터 소유가 불명확하면 멈추고 @buenhyden에게 보고한다.

#### Verification

##### Expected Results

###### Service Checks
<!-- core-payload-level:4 -->

Static check render에 일곱 서비스가 나오고 세 broker가 healthy이며, topic의 partition leader와 ISR이 확인되어야 한다.

###### Evidence
<!-- core-payload-level:4 -->

source revision, 실행한 명령과 종료 코드, broker health, topic·ISR 요약, 미검증 gap을 기록한다.
secret, raw log와 rendered private 설정은 기록하지 않는다.

##### Unverified Conditions

이 runbook이 아직 관찰하지 못한 항목은 다음과 같다. 문서는 복구 절차가 계획이며 실행된 적이 없다고 적고 있다.

- Planned backup and isolated restore: 이 문서에는 실행 결과가 기록되어 있지 않다. 격리 cluster에서 topic별 record 수와 offset 일치가 관찰되면 검증된다.
- `lab.py up/down kafka-cluster`와 진단 명령(`ps`, `kafka-topics --describe`): 승인된 lease가 필요하며 실행 결과가 기록되어 있지 않다. 세 broker healthy와 partition leader/ISR이 관찰되면 검증된다.
- HOME Schema Registry와 Connect 퇴역: owner 승인이 필요하며 문서는 현재 컨테이너, volume, router의 존재가 확인되지 않았다고 적고 있다. 별도 승인으로 대상 확인이 이뤄지면 검증된다.
- readiness 검사: `kafka-cluster`에 대한 실행 결과가 기록되어 있지 않다.

#### Escalation

##### Next Owner

cluster ID가 HOME과 같거나, HOME 경로가 render에 나타나거나, 데이터 소유가 불명확하면 멈추고
@buenhyden에게 보고한다.

##### Recovery or Forward Repair

LAB은 HOME 소비자가 없으므로 `lab.py down kafka-cluster`로 멈추면 HOME에 영향이 없다. 데이터는
`${LAB_DATA_DIR}/kafka/`에 남는다. 삭제는 별도 승인이다.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
