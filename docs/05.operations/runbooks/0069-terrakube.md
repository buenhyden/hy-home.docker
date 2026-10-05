---
title: "Terrakube Recovery Runbook"
version: "1.1.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0069"
parent_ids:
- "GDE-0069"
created: "2026-05-17"
---

# Terrakube Recovery Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### When to Use

API/UI/executor failure, stuck run, OIDC failure, missing state/output, 또는
승인된 backup/restore/upgrade에 사용한다. 저장소 루트에서 작업한다.

### 작업 선택과 복구 전제

변경 전에 정확한 서비스·데이터 경로·승인자·중단 영향을 기록하고 [공통 복구 전제](0021-backup-and-restore.md)를
적용한다. 격리 대상, 복구본 식별자·무결성, 여유 공간, 비밀 보관, 작성자 정지와
승격 승인 중 하나라도 불명확하면 중단한다. config·secret 교체는
[공통 수명주기 정책](../policies/0006-infrastructure-optimization-governance.md)의
단일 파일 bind 재생성과 비밀 비노출 확인을 따른다. 재시작은 데이터 복원이나 자격 증명
폐기 검증을 대신하지 않는다.

## Procedure

### Procedure

1. 새 Terrakube run을 동결한다. workspace/run ID, VCS ref, state key, component
   status, apply 진행 여부를 기록한다. remote effect와 recovery owner를 파악하기
   전에는 active apply를 중지하지 않는다.
2. bounded state를 validate하고 점검한다.

   ```bash
   docker compose --profile iac config --quiet
   docker compose --profile iac ps terrakube-api terrakube-ui terrakube-executor
   docker compose --profile iac logs --tail=200 terrakube-api terrakube-ui terrakube-executor
   ```

3. 재시작 전에 분류한다.
   - UI만: gateway와 OIDC redirect/claim을 점검한다.
   - API DB error: `mng-pg`를 점검한다. migration을 반복적으로 재시도하지 않는다.
   - missing state/output: state를 로그로 다운로드하지 않고 SeaweedFS bucket/key와
     DB reference를 점검한다.
   - stuck execution: Valkey coordination과 executor/Docker access를 점검하고,
     취소나 replay 전에 remote provider action을 확인한다.
4. dependency와 active-run check 후 실패한 component만 재시작한다. job이나 apply를
   replay하려면 별도 authorization이 필요하다.

### Coordinated backup and isolated restore

1. scheduling을 차단하고, active run을 대기하거나 안전하게 해결한 뒤, Terrakube
   writer가 남지 않도록 API/UI와 executor를 중지한다.
2. `tfstate`에 대해서는 PostgreSQL owner의 online logical/physical backup 절차와
   [일일 백업](0024-seaweedfs.md)에 포함되는 SeaweedFS 세트를 사용한다.
   일일 스케줄 자체가 DB와 object의 같은 복구 시점을 보장하지 않으므로 작성자 정지
   구간과 두 캡처의 일관성을 별도로 확인한다. DB backup ID, object
   snapshot/version inventory, source commit, Keycloak/client configuration을
   연결하는 recovery-point receipt 하나를 기록한다. secret/state 내용은 캡처하지 않는다.
3. 두 store를 모두 isolated target으로 복원한다. replacement secret을 사용하고
   provider, VCS webhook, executor egress를 비활성화한다.
4. isolated store에 대해서만 복원된 component set을 시작한다. organization/
   workspace/run count, 참조된 state/output key, OIDC role mapping, non-applying
   plan을 확인한다. 복원된 executor를 live account로 향하게 하지 않는다.
5. 검토 후에만 승격한다. 그렇지 않으면 원본을 그대로 두고 격리된 사본을 진단용으로
   보존한다. 사본 삭제는 보존 의무와 승인 여부를 확인한 뒤 따로 처리한다.

### Upgrade

coordinated backup을 완료하고 모든 migration/release note를 검토하고 복원된
store에서 새 API/UI/executor를 테스트한 뒤, 호환되는 set을 upgrade한다. 실패
시에는 새 set을 중지하고 DB와 object를 이전 image로 함께 복원한다.

### 복구 세트와 버전 변경

복구에는 일관된 세트가 필요하다. Terrakube PostgreSQL 데이터베이스, SeaweedFS
`tfstate` object/버전, 관련 Keycloak client/role 설정, 추적되는 Compose, secret
메타데이터/보관 정보. Valkey는 조정 상태이므로 비어 있거나 정지된 제어 플레인과
일관되어야 한다. 조정된 데이터베이스/object 스냅샷을 찍기 전에 새 실행을 중지하고
API/executor를 정지한다. provider와 webhook egress를 비활성화한 격리 환경에서만
복원하고, DB/state-key 참조 일관성과 적용하지 않는 plan을 검증한다. SeaweedFS
사본 하나나 DB 덤프 하나만으로 복구 가능성을 추정하지 않는다.

업그레이드 전에는 이 조정된 백업을 확보하고, Terrakube release/마이그레이션
노트를 읽고, 복원된 사본에 대해 테스트하고, 컴포넌트 세트 하나를 함께 롤포워드한다.
마이그레이션 이후 데이터베이스/state 롤백 없이 이미지만 롤백하는 것은 안전하지
않다. 이 문서 작업에서는 백업/복원과 업그레이드 리허설을 실행하지 않았다.

## Verification

### Evidence

정제된 컴포넌트 health·run/workspace 개수·백업 ID/checksum·state-key 개수·
release/source 커밋·비적용 plan 결과와 최종 상태를 기록한다.

## Rollback and Escalation

### Rollback or Recovery

이 coordinated backup/restore와 upgrade 단계는 **계획되었으나 미실행** 상태이다.
component restart나 단일 store snapshot으로 recovery했다고 주장하지 않는다.

### Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

active/unknown apply, DB-object 불일치, Docker-socket 예기치 않은 access, auth
모호성, backup 불가, destructive migration이 있으면 중단한다.

### 현재 실행 경로의 제한

추적되는 Compose와 README는 cookie 기반 ForwardAuth가 Terraform CLI/API 토큰
요청 및 공개 API URL을 사용하는 executor 요청을 막는 상태임을 명시한다. 전용
`home-terrakube` client/audience와 RBAC 활성화는 별도 승인된 구현 변경이 필요하다.
현재 gateway 통제는 유지하며 로그인·health 성공을 실행 가능 증거로 기록하지 않는다.
인증 오류를 우회하거나 실제 plan/apply를 재시도하지 말고 `@buenhyden`에게 보고한다.

### Traceability

- [Guide](../guides/0069-terrakube.md) (`GDE-0069`)
- [Policy](../policies/0069-terrakube.md) (`POL-0069`)
- [Terrakube Compose](../../../infra/09-platform-ops/terrakube/docker-compose.yml)

## Related Documents

- [Terrakube documentation](https://docs.terrakube.io/)
- [Operations index](../README.md)
