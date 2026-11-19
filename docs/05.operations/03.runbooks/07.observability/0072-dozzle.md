---
title: "Dozzle Recovery Runbook"
version: "1.2.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "RUN-0072"
parent_ids:
- "GDE-0072"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Dozzle Recovery Runbook

## Trigger and Scope

### Trigger

이 런북은 Dozzle의 OIDC/CIDR 거부, 로그 스트림 누락, socket 오류, 설정 손실, 침해 의심과 승인된 업그레이드를 다루는 절차를 정의한다.

OIDC/CIDR 거부, 로그 스트림 누락, socket 오류, 설정 손실, 침해 의심 또는 승인된
업그레이드에 사용한다.

### Targets

- [Guide](../../01.guides/07.observability/0072-dozzle.md) (`GDE-0072`)
- [Policy](../../02.policies/07.observability/0072-dozzle.md) (`POL-0072`)
- [Dozzle Compose](../../../../infra/06-observability/dozzle/docker-compose.yml)

- [Dozzle authentication](https://dozzle.dev/guide/authentication)

## Preflight

### Authority

책임자는 `@buenhyden`이다. 최소 권한 테스트 identity로 로그인하며, shell/actions는 명시적으로 설정하고 승인하지 않았다면 비활성 상태여야 한다.

### Environment

실행 전 확인할 점검은 아래 항목을 따른다.

#### 작업 선택과 복구 전제

변경 전에 정확한 서비스·데이터 경로·승인자·중단 영향을 기록하고 [공통 복구 전제](../10.platform-and-backup/0021-backup-and-restore.md)를
적용한다. 격리 대상, 복구본 식별자·무결성, 여유 공간, 비밀 보관, 작성자 정지와
승격 승인 중 하나라도 불명확하면 중단한다. config·secret 교체는
[공통 수명주기 정책](../../02.policies/01.common/0006-infrastructure-optimization-governance.md)의
단일 파일 bind 재생성과 비밀 비노출 확인을 따른다. 재시작은 데이터 복원이나 자격 증명
폐기 검증을 대신하지 않는다.

## Procedure

### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | 루트에서 `docker compose --profile admin-logs`로 config 검증, 상태, 로그 점검 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 2 | OIDC issuer/client/secret/CA, CIDR, Docker socket, 대상 컨테이너, log-driver 증상 구분 (raw application log는 기본적으로 캡처하지 않음) | 문서에 기록 없음 | 문서에 기록 없음 |
| 3 | auth bypass나 socket compromise 의심 시 Dozzle 중지, OIDC client secret revoke/rotate, sanitized audit evidence 보존 | 문서에 기록 없음 (`:ro` socket flag는 Docker API mutation 불가의 증거가 아님) | Stop Conditions에 따라 중단 |
| 4 | OIDC/CIDR/socket 통제 검토 후에만 재시작하고 허용/거부 identity/CIDR과 filtered visibility 확인 | OIDC/CIDR 허용/거부 판정이 예상 filtered visibility와 일치 | Stop Conditions에 따라 중단 |

1. 루트에서 validate하고 점검한다.

   ```bash
   docker compose --profile admin-logs config --quiet
   docker compose --profile admin-logs ps dozzle
   docker compose --profile admin-logs logs --tail=200 dozzle
   ```

2. OIDC issuer/client/secret/CA, CIDR, Docker socket, 대상 컨테이너와 Docker
   log-driver의 증상을 구분한다. 기본적으로 raw application log는 캡처하지 않는다.
3. auth bypass나 socket compromise가 의심되면 Dozzle을 중지하고, OIDC client
   secret을 revoke/rotate하고, sanitized audit evidence를 보존한다. `:ro` socket
   flag가 Docker API mutation이 불가능했다는 증거는 아니다.
4. OIDC/CIDR/socket 통제가 검토된 후에만 재시작한다. 허용/거부된 identity/CIDR과
   예상 filtered visibility를 확인한다.

#### Settings recovery and upgrade

`/data`는 설정 연속성을 위해서만 백업하고 컨테이너 로그는 백업하지 않는다. Dozzle을 중지하고, bind-backed `/data` 전체를 protected storage로 복사하고, 먼저
production socket이 없는 isolated instance로 복원한다. upgrade 시에는 advisory/
release를 검토하고 해당 copy에서 OIDC, roles/filters, streaming,
actions/shell 기본값을 테스트한다. 비호환 시 image와 settings copy를 함께 롤백한다.

#### 승인된 사용

`docker compose --profile admin-logs config --quiet`로 검증하고, CIDR와 OIDC
client/claim을 확인한 다음 Dozzle만 시작한다. 최소 권한 테스트 identity로 로그인을
검증하고 명시적으로 설정하고 승인하지 않았다면 shell/actions가 비활성 상태로
유지되는지 확인한다. 증거를 캡처하기 전에 로그를 정제한다.

### Stop Conditions

socket compromise 의심, auth/CIDR bypass, secret exposure, log authority 누락,
settings 비호환이 있으면 중단한다.

## Verification

### Expected Results

#### Service Checks

OIDC/CIDR 허용/거부 판정이 예상 filtered visibility와 일치하고, 최소 권한 테스트 identity 로그인이 성공하며, shell/actions가 비활성 상태로 유지되어야 한다.

#### Evidence

종료 코드·source 커밋·OIDC/CIDR 허용/거부 판정·표시 컨테이너 수·설정 checksum과
최종 socket/service 상태를 기록한다. log 내용은 redact한다.

### Unverified Conditions

이 런북에서 아직 관찰되었다고 기록되지 않은 항목과, 이를 확인할 관찰은 다음과 같다.

- 재시작 후 접근 통제(4단계): 이 문서에는 실행 결과가 기록되어 있지 않다. 허용/거부 identity와 CIDR 판정, 최소 권한 테스트 identity 로그인 성공을 관찰해야 한다.
- shell/actions 비활성 상태: 명시적으로 설정하고 승인하지 않았다면 비활성이어야 하며, 실제 상태는 로그인 후 수동으로 확인해야 한다.
- `/data` 설정 복원과 upgrade: isolated instance에서의 복원과 OIDC, roles/filters, streaming, actions/shell 기본값 테스트 결과가 이 문서에 기록되어 있지 않다.
- socket compromise 대응(3단계): 실행 결과가 기록되어 있지 않다. 최종 socket/service 상태와 설정 checksum으로 확인한다.

## Escalation

### Next Owner

책임자는 `@buenhyden`이다. Stop Conditions의 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

### Recovery or Forward Repair

settings restore와 upgrade rehearsal은 **계획되었으나 미실행** 상태이다. Docker
로그는 별도의 logging backend recovery가 필요하며 Dozzle은 이를 복원할 수 없다.
