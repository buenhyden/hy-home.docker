---
title: "Pact Broker Recovery Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
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

### 작업 선택과 복구 전제

변경 전에 정확한 서비스·데이터 경로·승인자·중단 영향을 기록하고 [공통 복구 전제](0021-backup-and-restore.md)를
적용한다. 격리 대상, 복구본 식별자·무결성, 여유 공간, 비밀 보관, 작성자 정지와
승격 승인 중 하나라도 불명확하면 중단한다. config·secret 교체는
[공통 수명주기 정책](../policies/0006-infrastructure-optimization-governance.md)의
단일 파일 bind 재생성과 비밀 비노출 확인을 따른다. 재시작은 데이터 복원이나 자격 증명
폐기 검증을 대신하지 않는다.

## Procedure

1. 점검한다.

   ```bash
   docker compose --profile core --profile contract-testing config --quiet
   docker compose --profile core --profile contract-testing ps pact-broker pact-broker-db-provision
   docker compose --profile core --profile contract-testing logs --tail=100 pact-broker-db-provision pact-broker
   curl -s http://127.0.0.1:${PACT_BROKER_HOST_PORT:-19292}/diagnostic/status/heartbeat
   ```

2. helper의 `64`는 입력 검증 실패 또는 readiness 대기 만료일 수 있다. psql
   오류는 단계·연결·소유권·권한을 구분한다. `ON_ERROR_STOP`은 이미 커밋된 SQL을
   되돌리지 않는다. 다른 소유 role/DB의 인수를 우회하지 말고 적용 범위·복구본을
   확인한 뒤 재실행을 별도로 승인받는다.
3. Broker `64` 종료는 크리덴셜 시크릿이 존재하지만 비어 있음을 의미한다. `1`
   종료는 없거나 읽을 수 없음을 의미한다. 시작 후 데이터베이스 연결 오류는
   대개 역할 비밀번호와 시크릿이 어긋났음을 의미한다.
   단일 원인으로 단정하지 말고 DB 준비·이름·권한·secret 교체 이력을 값 없이 확인한다.
   helper 재실행은 비밀번호뿐 아니라 role·database·grant도 변경하므로 별도 승인과
   아래 회전 절차를 따른다.
4. 401이면 사용자 이름·클라이언트 인증 전달 방식·설정·회전 이력을 확인한다.
   비밀번호 불일치로 단정하거나 secret을 출력하지 않는다.

### Credential rotation

정확한 secret·서비스·클라이언트·중단 영향을 승인받고 등록된 workflow로 교체한다.
공통 단일 파일 bind 정책에 따라 broker를 재생성하며 재시작만으로 교체 반영을
가정하지 않는다. DB 비밀번호는 PG/init 준비와 보호된 복구본을 확인한 뒤
`docker compose --profile core --profile contract-testing run --rm --no-deps pact-broker-db-provision`으로
새 helper를 명시적으로 실행한다. 오류가 나면 부분 변경을 확인하고 자동 반복하지 않는다.
Basic secret은 모든 승인된 client에도 반영한다. 이전 자격 증명 거부, 새 자격 증명의
합성 publish/read-back 및 heartbeat를 각각 확인한다.

### 복원·업그레이드 경계

공유 [백업 런북](0021-backup-and-restore.md)에 포함되는 설정은 복원 성공 증거가
아니다. `mng-pg` 전체 복원은 다른 서비스에도 영향을 주므로 이 broker만의 일반 복구로
실행하지 않는다. writer를 정지하고 검증된 DB 복구본을 격리 대상에 복원한 뒤 pact·
검증 이력·인증을 확인한다. 승인 전 활성 DB를 덮어쓰지 않는다. 업그레이드는 wrapper와
broker 선언 버전의 release/schema 근거 및 이전 이미지·DB 복구점을 함께 검토한다.

## Evidence

종료 코드, heartbeat 상태, pacticipant와 pact 개수, 소스 커밋을 기록한다.
크리덴셜이나 pact 본문은 절대 기록하지 않는다.

## Rollback or Recovery

broker 데이터베이스가 유일한 상태다. 이 데이터베이스는 `mng-pg` pgBackRest 백업에
포함되며(RUN-0021), `mng-pg`를 복원하면 함께 복원된다. 데이터베이스를 잃으면
`can-i-deploy`가 의존하는 검증 이력을 잃지만 컨슈머는 pact를 다시 게시할 수
있고 provider는 다시 검증할 수 있다. 데이터베이스를 삭제하는 것은 승인이
필요한 데이터 변경이다.

## Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

basic auth 비활성화, 공개 읽기 허용, loopback 밖으로 포트 노출, 역할에
자신의 데이터베이스 이상의 권한 부여 요청이 있으면 중단한다.

## Traceability

- [Guide](../guides/0093-pact-broker.md) (`GDE-0093`)
- [Policy](../policies/0093-pact-broker.md) (`POL-0093`)
- [Pact Broker Compose](../../../infra/11-quality/pact-broker/docker-compose.yml)

## Related Documents

- [관리 데이터베이스 런북](0028-management-database.md)
- [백업 및 복원 런북](0021-backup-and-restore.md) (`RUN-0021`)
