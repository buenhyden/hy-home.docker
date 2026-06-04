---
status: active
---
<!-- Target: docs/05.operations/runbooks/05-messaging/kafka.md -->

# Kafka Cluster Runbook

## Overview (KR)

이 런북은 `hy-home.docker`의 Kafka 인프라(05-messaging)에서 발생할 수 있는 주요 장애 상황의 비파괴 점검, evidence capture, escalation 절차를 정의한다. Root-included dev Kafka는 단일 broker이며, full 3 broker Kafka compose는 root network/secret context가 필요한 service-local compose다.

## Kafka Recovery & Maintenance Procedure (05-messaging)

> Scope: Kafka Infrastructure

> Step-by-step procedures for broker recovery, partition rebalancing, and system maintenance.

---

### Purpose

이 런북은 브로커 다운, 메시지 지연(Lag), 복제본 불일치 및 스키마 등록 오류를 신속히 해결하고 클러스터 상태를 정상으로 복구하는 것을 목적으로 한다.

### Canonical References

- [../../../02.architecture/requirements/0005-messaging-architecture.md](../../../02.architecture/requirements/0005-messaging-architecture.md)
- [../../../03.specs/05-messaging/spec.md](../../../03.specs/05-messaging/spec.md)
- [../../policies/05-messaging/kafka.md](../../policies/05-messaging/kafka.md)

## When to Use

- broker health가 `unhealthy` 또는 `starting` 상태에 오래 머물 때
- `UnderReplicatedPartitions` 지표가 0보다 클 때
- Schema Registry 또는 Kafka Connect healthcheck가 실패할 때
- Kafbat UI에서 topic/consumer group 조회가 실패할 때

## Procedure

### Checklist

- [ ] root profile 검증 결과를 확인한다.
- [ ] Kafka 관련 컨테이너 health 상태를 확인한다.
- [ ] 최근 compose, secret, route, topic 변경 여부를 확인한다.
- [ ] 데이터 영향 작업(delete topic, retention 축소, partition reassignment)이 필요한지 판단한다.

### Steps

1. 정적 baseline을 확인한다.

   ```bash
   HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh
   bash scripts/hardening/check-all-hardening.sh 05-messaging
   ```

2. 컨테이너 상태와 health evidence를 캡처한다.

   ```bash
   docker compose ps kafka-1 schema-registry kafka-connect kafka-rest-proxy kafbat-ui kafka-exporter kafka-init
   docker inspect --format '{{json .State.Health}}' kafka-1
   docker inspect --format '{{json .State.Health}}' schema-registry
   docker inspect --format '{{json .State.Health}}' kafka-connect
   ```

3. Broker API와 topic 상태를 확인한다.

   ```bash
   docker exec kafka-1 kafka-broker-api-versions --bootstrap-server localhost:19092
   docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --describe --under-replicated-partitions
   docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --list
   ```

4. 로그를 확인한다.

   ```bash
   docker logs kafka-1 --tail 100
   docker logs schema-registry --tail 100
   docker logs kafka-connect --tail 100
   ```

5. 단일 service health가 비정상이고 최근 설정 변경이 없다면 해당 서비스만 재시작한다.

   ```bash
   docker compose restart kafka-1
   docker compose restart schema-registry
   docker compose restart kafka-connect
   ```

6. Full 3 broker compose에서 partition reassignment, preferred leader election, topic deletion, retention 축소가 필요하면 이 런북에서 실행하지 말고 `## Escalation`으로 전환한다.

### Verification Steps

- [ ] `docker exec kafka-1 kafka-broker-api-versions --bootstrap-server localhost:19092` 실행 성공
- [ ] `UnderReplicatedPartitions` 조회가 실패 없이 완료
- [ ] `schema-registry`, `kafka-connect`, `kafbat-ui` health 상태가 정상 또는 개선 추세
- [ ] Root messaging profile validation 및 hardening baseline 통과

### Observability and Evidence Sources

- **Signals**: Grafana Alert (UnderReplicatedPartitions > 0), Kafbat UI Health Indicator.
- **Evidence to Capture**: `docker logs kafka-1`, `docker logs schema-registry`, `kafka-topics --describe`, `docker inspect` health 출력.

### Safe Rollback or Recovery Procedure

- [ ] 문서 또는 compose 변경 직후 발생한 장애라면 해당 diff를 검토하고 변경 전 상태와 현재 compose render를 비교한다.
- [ ] 검증된 workload-independent Kafka data rollback procedure는 아직 문서화되어 있지 않다.
- [ ] `_schemas` topic, offset, retention, partition reassignment를 변경해야 하는 경우 destructive/data-impact escalation으로 전환한다.

### Agent Operations

- **Tool Disable**: 메시징 오류 시 AI Agent의 생산 도구(Tool) 실행을 일시적으로 비활성화.
- **Trace Capture**: `docs/05.operations/incidents`에 자동으로 장애 타임라인과 로그 캡처본을 기록.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- Capture command output, timestamps, and operator or agent actions for any execution of this runbook.
- Record failed checks, observed symptoms, and the final recovery or escalation state in the related task or incident evidence.

## Rollback or Recovery

N/A - no verified generic Kafka data rollback procedure is documented yet. Use this runbook for non-destructive inspection and service restart only. Escalate for replay, topic deletion, retention changes, schema topic mutation, partition reassignment, or full 3 broker recovery.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/05-messaging/kafka.md)
- [Operations policy](../../policies/05-messaging/kafka.md)
