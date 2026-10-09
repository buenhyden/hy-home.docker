---
title: "05-Messaging Optimization Hardening Operations Policy"
version: "2.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0037"
parent_ids:
- "AD-0005"
created: "2026-05-10"
---

# 05-Messaging Optimization Hardening Operations Policy

## Overview

이 정책은 현재 소스 구성을 data protection, security, resource, lifecycle 측면에서 독립적으로 검증 가능한 operator control에 결합한다.

## Scope

이 정책은 현재 optional Kafka-family 소스와 그 static hardening contract에
적용된다. 활성화나 security migration을 승인하지 않는다.

## Rules

정상 messaging 변경은 root Compose validity, explicit profile, health check,
resource limit, persistence ownership, `kafka_net`, secret file, 실행 가능한
recovery owner를 보존해야 한다. `labs/kafka-cluster.yml` 변경은 별도 LAB
project·network·cluster ID·data directory를 보존하며 root에 포함하지 않는다.
현재 유일한 broker family는 Kafka다.

### Security policy

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

### Reliability and recovery policy

same-host replication은 host availability가 아니다. 새 workload는
retention, partition, replication, capacity, producer/consumer ownership,
RPO/RTO, replay source를 정의해야 한다. Recovery는 data, topic config,
offset, schema, Connect state, KRaft identity를 포함해야 하며, promotion
전에 isolated cluster에서 rehearsed되어야 한다.

### Validation contract

정상 `messaging`은 [GDE-0037](../guides/0037-messaging-optimization-hardening.md)의
exact root-profile `config --quiet` command로 검증한다. LAB은
`docker compose --env-file labs/.env.example -f labs/kafka-cluster.yml --profile lab-kafka config --quiet`로
별도 렌더링한 뒤 scoped `05-messaging` hardening script를 사용한다. Static
pass는 configuration evidence일 뿐이다. Runtime startup, OIDC login, load
또는 failover에는 명시적 승인과 기록된 rollback이 필요하다.

### Accountable lifecycle boundary

적용 identity: 정상 `debezium-db-provision`, `kafbat-ui`, `kafka-1`, `kafka-connect`, `kafka-exporter`, `kafka-init`, `kafka-rest-proxy`, `schema-registry`; LAB `lab-kafka-1..3`, `lab-kafka-exporter`, `lab-kafka-init`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

## Exceptions

문서화된 one-shot job exception은 data/security control을 면제하지
않는다. exception은 runtime mutation, plaintext secret, raw active storage
copy, same-host availability 주장을 승인하지 않는다.

### Verification

root 구성과 scoped static policy check를 검증한 다음, promotion이나
cutover 전에 application-level acceptance를 갖춘 isolated compatible
restore를 요구한다. 검증되지 않은 runtime property는 명시적으로 기록한다.

### Review Cadence

profile, image, volume, credential, consumer, retention, upstream
lifecycle 변경 후 검토하며, 보관 중에는 최소 연 1회 검토한다.

### Traceability

- Artifact: `POL-0037`; parent: `AD-0005`.
- Runtime authority는 연결된 Compose/source file에 남는다; exact pin은
  그곳에 유지된다.

## Related Documents

- [Domain catalog](../README.md)
- [Kafka policy](0036-kafka.md)
- [Kafka security](https://kafka.apache.org/documentation/#security)
- [Hardening runbook](../runbooks/0037-messaging-optimization-hardening.md)
