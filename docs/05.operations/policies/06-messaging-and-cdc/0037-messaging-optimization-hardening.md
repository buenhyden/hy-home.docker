---
title: "05-Messaging Optimization Hardening Operations Policy"
version: "2.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0037"
parent_ids:
- "AD-0005"
created: "2026-05-10"
next_review_at: "2027-05-13"
---

# 05-Messaging Optimization Hardening Operations Policy

## Purpose and Scope

### Objective

이 정책은 현재 소스 구성을 data protection, security, resource, lifecycle 측면에서 독립적으로 검증 가능한 operator control에 결합한다.

#### Authority

- Artifact: `POL-0037`; parent: `AD-0005`.
- Runtime authority는 연결된 Compose/source file에 남는다; exact pin은
  그곳에 유지된다.

### Applies To

이 정책은 현재 optional Kafka-family 소스와 그 static hardening contract에
적용된다.

#### Exclusions

활성화나 security migration을 승인하지 않는다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0037-R1 | 정상 messaging 변경 | 필수: root Compose validity/explicit profile/health check/resource limit/persistence ownership/`kafka_net`/secret file/실행 가능한 recovery owner를 보존한다 | none | none |
| POL-0037-R2 | `labs/kafka-cluster/docker-compose.yml` 변경 | 필수: 별도 LAB project/network/cluster ID/data directory를 보존한다 | none | none |
| POL-0037-R3 | 항상 | 금지: LAB compose를 root에 포함 | none | none |
| POL-0037-R4 | PLAINTEXT Kafka listener | 금지: sensitive하거나 untrusted된 traffic을 싣는 것 | none | none |
| POL-0037-R5 | TLS/SASL 도입 | 필수: architectural change와 client rollout을 거친다 | none | none |
| POL-0037-R6 | Kafbat | 필수: OIDC와 group RBAC로 native하게 인증한다 | none | none |
| POL-0037-R7 | secret | 필수: Docker secret으로 유지한다 | none | none |
| POL-0037-R8 | local CA | 필수: read-only로 마운트한다 | none | none |
| POL-0037-R9 | Kafbat route | 필수: 표준 gateway chain을 사용한다 | none | none |
| POL-0037-R10 | Kafbat route | 금지: forward-auth header trust | none | none |
| POL-0037-R11 | administrative endpoint/host-published listener | 필수: 명시된 trusted boundary 안에 유지하고 host-published listener는 `127.0.0.1`에만 게시한다 | none | none |
| POL-0037-R12 | evidence | 필수: token/client secret/record payload를 생략한다 | none | none |
| POL-0037-R13 | 정상 broker | 필수: topic/bootstrap과 Connect internal topic의 replication factor를 1로 한다 | none | none |
| POL-0037-R14 | replication factor 3 | 필수: `lab-kafka`만의 topic/bootstrap contract로 한정하고 healthy LAB broker 3개를 요구한다 | none | none |
| POL-0037-R15 | same-host replication | 금지: host availability로 취급 | none | none |
| POL-0037-R16 | 새 workload | 필수: retention/partition/replication/capacity/producer·consumer ownership/RPO·RTO/replay source를 정의한다 | none | none |
| POL-0037-R17 | recovery | 필수: data/topic config/offset/schema/Connect state/KRaft identity를 포함한다 | none | none |
| POL-0037-R18 | promotion 전 | 필수: isolated cluster에서 rehearse한다 | none | none |
| POL-0037-R19 | 정상 `messaging` 검증 | 필수: RUN-0037의 exact root-profile `config --quiet` command로 검증한다 | RUN-0037의 exact root-profile `config --quiet` command | none |
| POL-0037-R20 | LAB 검증 | 필수: `docker compose --env-file labs/.env.example -f labs/kafka-cluster/docker-compose.yml --profile lab-kafka config --quiet`로 별도 렌더링한다 | `docker compose --env-file labs/.env.example -f labs/kafka-cluster/docker-compose.yml --profile lab-kafka config --quiet` | none |
| POL-0037-R21 | LAB 렌더링 후 | 필수: scoped `05-messaging` hardening script를 사용한다 | `bash scripts/hardening/check-all-hardening.sh 05-messaging` | none |
| POL-0037-R22 | 항상 | 금지: static pass를 configuration evidence 이상(runtime 증거)으로 취급 | none | none |
| POL-0037-R23 | runtime startup/OIDC login/load/failover | 필수: 명시적 승인과 기록된 rollback을 갖춘다 | 수동 | none |
| POL-0037-R24 | promotion/cutover 전 | 필수: application-level acceptance를 갖춘 isolated compatible restore를 요구한다 | none | none |
| POL-0037-R25 | 항상 | 필수: 검증되지 않은 runtime property를 명시적으로 기록한다 | none | none |
| POL-0037-R26 | 적용 identity 변경/운영 | 필수: 문서의 정적 검증과 runtime 운영 승인을 분리한다 | none | none |
| POL-0037-R27 | service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 | 필수: 이 Policy와 linked Guide/Runbook을 함께 검토한다 | 수동 | none |
| POL-0037-R28 | engine secret/certificate | 필수: 이 subject의 credential 계약을 따른다 | none | none |
| POL-0037-R29 | 앱 인증 연동 | 필수: 적용되는 `POL-0079`의 통제를 따른다 | none | none |
| POL-0037-R30 | source 반영/재기동 | 필수: `POL-0006`의 적용 통제를 따른다 | none | none |
| POL-0037-R31 | 보존/삭제 | 필수: `POL-0021`의 적용 통제를 따른다 | none | none |
| POL-0037-R32 | exporter/stateless job | 필수: 설정·credential과 그 작업이 변경하는 upstream state를 통제 대상에서 제외하지 않고 포함한다 | none | none |
| POL-0037-R33 | 소유 artifact·복구 지점·expiry가 불명확할 때 | 필수: 삭제/재생성을 중단한다 | none | none |
| POL-0037-R34 | 항상 | 금지: 기존 Exceptions 외의 새 예외를 승인된 것으로 간주 | none | none |

정상 messaging 변경은 root Compose validity, explicit profile, health check,
resource limit, persistence ownership, `kafka_net`, secret file, 실행 가능한
recovery owner를 보존해야 한다. `labs/kafka-cluster/docker-compose.yml` 변경은 별도 LAB
project·network·cluster ID·data directory를 보존하며 root에 포함하지 않는다.
현재 유일한 broker family는 Kafka다.

#### Security policy

- PLAINTEXT Kafka listener는 문서화된 gap이며, sensitive하거나 untrusted된
  traffic을 실어서는 안 된다. TLS/SASL에는 architectural change와 client
  rollout이 필요하다.
- Kafbat은 OIDC와 group RBAC로 native하게 인증한다. secret은 Docker
  secret으로 유지되고, local CA는 read-only로 마운트되며, route는 표준
  gateway chain을 사용한다. 이 route에서는 forward-auth header trust를
  금지한다.
- Administrative endpoint와 host-published listener(`127.0.0.1`에만 게시)는
  명시된 trusted boundary 안에 유지한다. evidence는 token, client secret,
  record payload를 생략해야 한다.
- 정상 broker의 topic/bootstrap과 Connect internal topic은 replication factor
  1이다. replication factor 3은 `lab-kafka`만의 topic/bootstrap contract이며
  healthy LAB broker 3개가 필요하다.

#### Reliability and recovery policy

same-host replication은 host availability가 아니다. 새 workload는
retention, partition, replication, capacity, producer/consumer ownership,
RPO/RTO, replay source를 정의해야 한다. Recovery는 data, topic config,
offset, schema, Connect state, KRaft identity를 포함해야 하며, promotion
전에 isolated cluster에서 rehearsed되어야 한다.

#### Validation contract

정상 `messaging`은 [RUN-0037](../../runbooks/06-messaging-and-cdc/0037-messaging-optimization-hardening.md#steps)의
exact root-profile `config --quiet` command로 검증한다. LAB은
`docker compose --env-file labs/.env.example -f labs/kafka-cluster/docker-compose.yml --profile lab-kafka config --quiet`로
별도 렌더링한 뒤 scoped `05-messaging` hardening script를 사용한다. Static
pass는 configuration evidence일 뿐이다. Runtime startup, OIDC login, load
또는 failover에는 명시적 승인과 기록된 rollback이 필요하다.

#### Accountable lifecycle boundary

적용 identity: 정상 `kafbat-ui`, `kafka-1`, `kafka-exporter`, `kafka-init`; LAB `lab-kafka-1..3`, `lab-kafka-exporter`, `lab-kafka-init`, `lab-schema-registry`, `lab-kafka-connect`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](../03-identity-and-access/0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](../01-common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

### Exceptions

#### Exception Conditions

문서화된 one-shot job exception은 data/security control을 면제하지
않는다. exception은 runtime mutation, plaintext secret, raw active storage
copy, same-host availability 주장을 승인하지 않는다.

#### Approval and Review

profile, image, volume, credential, consumer, retention, upstream
lifecycle 변경 후 검토하며, 보관 중에는 최소 연 1회 검토한다.

## Enforcement

### Mechanisms

RUN-0037의 root/LAB render와 `bash scripts/hardening/check-all-hardening.sh 05-messaging`로 static 구성을 검증한 다음, promotion이나
cutover 전에 application-level acceptance를 갖춘 isolated compatible
restore를 요구한다. 검증되지 않은 runtime property는 명시적으로 기록한다.

### Limits

이 정책에서 이름 붙은 검사는 root/LAB render와 `05-messaging` hardening script뿐이며(검증 행에만 연결), 아래 규칙은 자동 검사 없이 검토·승인에 의존합니다.

- 변경 보존: 자동 검사 없음(none) `POL-0037-R1`, `POL-0037-R2`, `POL-0037-R3`
- 보안: 자동 검사 없음(none) `POL-0037-R4`, `POL-0037-R5`, `POL-0037-R6`, `POL-0037-R7`, `POL-0037-R8`, `POL-0037-R9`, `POL-0037-R10`, `POL-0037-R11`, `POL-0037-R12`, `POL-0037-R13`, `POL-0037-R14`
- 복구: 자동 검사 없음(none) `POL-0037-R15`, `POL-0037-R16`, `POL-0037-R17`, `POL-0037-R18`
- 검증: 자동 검사 없음(none) `POL-0037-R22`, `POL-0037-R24`, `POL-0037-R25`; 수동 검토/승인 `POL-0037-R23`
- lifecycle: 자동 검사 없음(none) `POL-0037-R26`, `POL-0037-R28`, `POL-0037-R29`, `POL-0037-R30`, `POL-0037-R31`, `POL-0037-R32`, `POL-0037-R33`, `POL-0037-R34`; 수동 검토/승인 `POL-0037-R27`
- 정책이 밝힌 공백: PLAINTEXT Kafka listener는 문서화된 gap이다.
- 정책이 밝힌 공백: static pass는 configuration evidence일 뿐이며 runtime startup/OIDC login/load/failover 증거는 이 정책에 없다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter `owner`에 기록된 @buenhyden이다.

### Review Triggers

- [Domain catalog](../../README.md)
- [Kafka policy](0036-kafka.md)
- [Kafka security](https://kafka.apache.org/documentation/#security)
- [Hardening runbook](../../runbooks/06-messaging-and-cdc/0037-messaging-optimization-hardening.md)
