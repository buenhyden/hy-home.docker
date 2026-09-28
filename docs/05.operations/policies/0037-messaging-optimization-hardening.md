---
title: "05-Messaging Optimization Hardening Operations Policy"
version: "1.0.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0037"
parent_ids:
- "AD-0005"
created: "2026-05-10"
---

# 05-Messaging Optimization Hardening Operations Policy

## Overview

이 정책은 현재 소스 구성을 data protection, security, resource, lifecycle,
독립적으로 검증 가능한 operator control에 결합한다.

## Policy Scope

이 정책은 현재 optional Kafka-family 소스와 그 static hardening contract에
적용된다. 활성화나 security migration을 승인하지 않는다.

## Controls

모든 messaging 변경은 root Compose validity, explicit profile, health
check, resource limit, persistence ownership, `kafka_net`, secret file,
실행 가능한 recovery owner를 보존해야 한다. 현재 유일한 broker family는
Kafka다.

### Security policy

- PLAINTEXT Kafka listener는 문서화된 gap이며, sensitive하거나 untrusted된
  traffic을 실어서는 안 된다. TLS/SASL에는 architectural change와 client
  rollout이 필요하다.
- Kafbat은 OIDC와 group RBAC로 native하게 인증한다. secret은 Docker
  secret으로 유지되고, local CA는 read-only로 마운트되며, route는 표준
  gateway chain을 사용한다. 이 route에서는 forward-auth header trust를
  금지한다.
- Administrative endpoint와 host-published listener는 명시된 trusted
  boundary 안에 유지한다. evidence는 token, client secret, record payload를
  생략해야 한다.
- replication factor 3이 선언된 곳에서는 topic/bootstrap 변경에
  three-broker compatibility가 필요하다.

### Reliability and recovery policy

same-host replication은 host availability가 아니다. 새 workload는
retention, partition, replication, capacity, producer/consumer ownership,
RPO/RTO, replay source를 정의해야 한다. Recovery는 data, topic config,
offset, schema, Connect state, KRaft identity를 포함해야 하며, promotion
전에 isolated cluster에서 rehearsed되어야 한다.

### Validation contract

`messaging`과 `messaging-cluster`에 대해 [GDE-0037](../guides/0037-messaging-optimization-hardening.md)에
있는 exact root-profile `config --quiet` command를 사용한 다음, scoped
`05-messaging` hardening script를 사용한다. Static pass는 configuration
evidence일 뿐이다. Runtime startup, OIDC login, load 또는 failover에는
명시적 승인과 기록된 rollback이 필요하다.

## Exceptions

문서화된 one-shot job exception은 data/security control을 면제하지
않는다. exception은 runtime mutation, plaintext secret, raw active storage
copy, same-host availability 주장을 승인하지 않는다.

## Verification

root 구성과 scoped static policy check를 검증한 다음, promotion이나
cutover 전에 application-level acceptance를 갖춘 isolated compatible
restore를 요구한다. 검증되지 않은 runtime property는 명시적으로 기록한다.

## Review Cadence

profile, image, volume, credential, consumer, retention, upstream
lifecycle 변경 후 검토하며, 보관 중에는 최소 연 1회 검토한다.

## Traceability

- Artifact: `POL-0037`; parent: `AD-0005`.
- Runtime authority는 연결된 Compose/source file에 남는다; exact pin은
  그곳에 유지된다.

### References

- [Kafka policy](0036-kafka.md)
- [Kafka security](https://kafka.apache.org/documentation/#security)
- [Hardening runbook](../runbooks/0037-messaging-optimization-hardening.md)

## Related Documents

- [Domain catalog](../README.md)
