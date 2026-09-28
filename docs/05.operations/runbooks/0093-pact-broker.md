---
title: "Pact Broker Recovery Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0093"
parent_ids:
- "GDE-0093"
created: "2026-09-23"
---

# Pact Broker Recovery Runbook

## When to Use

프로비저닝 실패, 비정상 broker, 인가되어야 할 클라이언트에 대한 401 오류,
데이터베이스 손실, 크리덴셜 교체 시 사용한다.

## Procedure

1. 점검한다.

   ```bash
   docker compose --profile core --profile contract-testing config --quiet
   docker compose --profile core --profile contract-testing ps pact-broker pact-broker-db-provision
   docker compose --profile core --profile contract-testing logs --tail=100 pact-broker-db-provision pact-broker
   curl -s http://127.0.0.1:${PACT_BROKER_HOST_PORT:-19292}/diagnostic/status/heartbeat
   ```

2. 프로비저닝 `64` 종료는 어떠한 변경도 일어나기 전의 입력 문제다. `3` 종료는
   거부 사유(관리자 역할, 이 작업이 생성하지 않은 역할, 다른 소유자를 가진
   데이터베이스)를 명시한다. 원인을 수정하고 `pact-broker-db-provision`을
   재실행한다. 이는 수렴한다.
3. Broker `64` 종료는 크리덴셜 시크릿이 존재하지만 비어 있음을 의미한다. `1`
   종료는 없거나 읽을 수 없음을 의미한다. 시작 후 데이터베이스 연결 오류는
   대개 역할 비밀번호와 시크릿이 어긋났음을 의미한다.
   `pact-broker-db-provision`을 재실행해 시크릿에서 역할 비밀번호를
   재설정한 뒤 `pact-broker`를 재시작한다.
4. 클라이언트에 대한 401은 그 사용자 이름이나 비밀번호가
   `PACT_BROKER_BASIC_AUTH_USERNAME`과 `pact_broker_basic_auth_password`
   시크릿과 다름을 의미한다.

### Credential rotation

등록된 워크플로로 시크릿을 교체한다. `pact_broker_db_password`의 경우
`pact-broker-db-provision`을 재실행하고 broker를 재시작한다.
`pact_broker_basic_auth_password`의 경우 broker를 재시작하고 게시 및 검증하는
모든 클라이언트를 업데이트한다.

## Evidence

종료 코드, heartbeat 상태, pacticipant와 pact 개수, 소스 커밋을 기록한다.
크리덴셜이나 pact 본문은 절대 기록하지 않는다.

## Rollback or Recovery

broker 데이터베이스가 유일한 상태다. 이는 `mng-pg` pgBackRest 백업의
일부이며(RUN-0021), `mng-pg`를 복원하면 함께 복원된다. 이를 잃으면
`can-i-deploy`가 의존하는 검증 이력을 잃지만, 컨슈머는 pact를 다시 게시할 수
있고 provider는 다시 검증할 수 있다. 데이터베이스를 삭제하는 것은 승인이
필요한 데이터 변경이다.

## Escalation

basic auth 비활성화, 공개 읽기 허용, loopback 밖으로 포트 노출, 역할에
자신의 데이터베이스 이상의 권한 부여 요청이 있으면 중단한다.

## Traceability

- [Guide](../guides/0093-pact-broker.md) (`GDE-0093`)
- [Policy](../policies/0093-pact-broker.md) (`POL-0093`)
- [Pact Broker Compose](../../../infra/09-tooling/pact-broker/docker-compose.yml)

## Related Documents

- [관리 데이터베이스 런북](0028-management-database.md)
- [백업 및 복원 런북](0021-backup-and-restore.md) (`RUN-0021`)
