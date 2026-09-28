---
title: "05-Messaging Optimization Hardening Usage Guide"
version: "1.1.3"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0037"
parent_ids:
- "POL-0037"
created: "2026-05-17"
---

# 05-Messaging Optimization Hardening Usage Guide

## Usage

현재 messaging surface는 Kafka 전용이며 OPTIONAL이다. hardening은
root-rendered Kafka family, Kafbat native OIDC, persistence, health, 리소스,
네트워크 exposure를 검증한다. PLAINTEXT broker listener가 안전하다거나 동일
host의 세 broker가 host 가용성을 제공한다고 주장하지 않는다.

### Source-backed checks

저장소 루트에서 root `.env.example`로 현재 messaging selector를 렌더링하고
이 tier의 공유 hardening 확인 스크립트를 실행한다. 정확한 명령 순서는
[05-Messaging Optimization Hardening runbook](../runbooks/0037-messaging-optimization-hardening.md#procedure)이
소유한다. 렌더링된 서비스를 점검하고 다음을 확인한다.

- 정확한 Kafka-family profile과 제거된 broker family가 없는지;
- 분리된 broker/Connect volume과 경로 재사용이 없는지;
- healthcheck와 공유 CPU/메모리 제한;
- `kafka_net`, 의도된 host 포트 게시, PLAINTEXT listener 위험;
- `kafbat_client_secret`, native `auth.type: OAUTH2`, local CA 신뢰, RBAC
  group, forwarding-auth middleware 없는 `gateway-standard-chain@file`;
- topic, offset, schema, connector, KRaft 상태에 대한 backup/restore 소유권.

static 성공은 runtime health, 인증 흐름, 성능, 데이터 내구성, restore를
증명하지 않는다. 이 항목들에는 별도로 승인된 테스트가 필요하다.

### Change workflow

소유하는 leaf 파일과 공유 템플릿에서 source를 수정하고 root profile을 다시
렌더링한다. 범위를 지정한 hardening 확인을 실행하고 diff를 점검한 뒤
[RUN-0037](../runbooks/0037-messaging-optimization-hardening.md)을 따른다.
TLS/SASL, credential 회전, topic 변경, 서비스 재시작 같은 runtime 보안
작업에는 명시된 계획과 rollback이 필요하다.

## Common Checks

정확한 root profile, service, health/resource 제어, writable-state 소유권,
secret reference, exposure, 엔진별 복구 경계를 확인한다. static pass는 구성
증거일 뿐이고 runtime과 restore는 별개 문제로 남는다.

## Traceability

- Artifact: `GDE-0037`; 거버넌스 정책: `POL-0037`.
- Runtime authority: `root Kafka Compose plus scripts/hardening/check-all-hardening.sh`.

### References

- [Kafka security](https://kafka.apache.org/documentation/#security)
- [Kafbat RBAC](https://ui.docs.kafbat.io/configuration/rbac-role-based-access-control)
- [Kafka guide](0036-kafka.md)

## Related Documents

- [Domain catalog](../README.md)
