---
title: "Dozzle Recovery Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0072"
parent_ids:
- "GDE-0072"
created: "2026-05-17"
---

# Dozzle Recovery Runbook

## When to Use

OIDC/CIDR 거부, 로그 스트림 누락, socket 오류, 설정 손실, 침해 의심 또는 승인된
업그레이드에 사용한다.

### 작업 선택과 복구 전제

변경 전에 정확한 서비스·데이터 경로·승인자·중단 영향을 기록하고 [공통 복구 전제](0021-backup-and-restore.md)를
적용한다. 격리 대상, 복구본 식별자·무결성, 여유 공간, 비밀 보관, 작성자 정지와
승격 승인 중 하나라도 불명확하면 중단한다. config·secret 교체는
[공통 수명주기 정책](../policies/0006-infrastructure-optimization-governance.md)의
단일 파일 bind 재생성과 비밀 비노출 확인을 따른다. 재시작은 데이터 복원이나 자격 증명
폐기 검증을 대신하지 않는다.

## Procedure

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

### Settings recovery and upgrade

Dozzle을 중지하고, bind-backed `/data` 전체를 protected storage로 복사하고, 먼저
production socket이 없는 isolated instance로 복원한다. upgrade 시에는 advisory/
release를 검토하고 해당 copy에서 OIDC, roles/filters, streaming,
actions/shell 기본값을 테스트한다. 비호환 시 image와 settings copy를 함께 롤백한다.

### 승인된 사용·설정 보존·업그레이드

`docker compose --profile admin-logs config --quiet`로 검증하고, CIDR와 OIDC
client/claim을 확인한 다음 Dozzle만 시작한다. 최소 권한 테스트 identity로 로그인을
검증하고 명시적으로 설정하고 승인하지 않았다면 shell/actions가 비활성 상태로
유지되는지 확인한다. 증거를 캡처하기 전에 로그를 정제한다.

`/data`는 설정 연속성을 위해서만 백업한다. 컨테이너 로그는 백업하지 않는다. 일관된
복사를 위해 Dozzle을 중지한다. 프로덕션이 아닌 Docker endpoint에 연결되거나 socket이
없는 격리된 Dozzle에 설정 사본을 복원한다. 업그레이드 전에는 보안 권고/release
노트를 검토하고 OIDC와 필터링된 로그 접근을 테스트한다. 여기서는 백업, 복원,
업그레이드를 실행하지 않았다.

## Evidence

종료 코드·source 커밋·OIDC/CIDR 허용/거부 판정·표시 컨테이너 수·설정 checksum과
최종 socket/service 상태를 기록한다. log 내용은 redact한다.

## Rollback or Recovery

settings restore와 upgrade rehearsal은 **계획되었으나 미실행** 상태이다. Docker
로그는 별도의 logging backend recovery가 필요하며 Dozzle은 이를 복원할 수 없다.

## Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

socket compromise 의심, auth/CIDR bypass, secret exposure, log authority 누락,
settings 비호환이 있으면 중단한다.

## Traceability

- [Guide](../guides/0072-dozzle.md) (`GDE-0072`)
- [Policy](../policies/0072-dozzle.md) (`POL-0072`)
- [Dozzle Compose](../../../infra/06-observability/dozzle/docker-compose.yml)

## Related Documents

- [Dozzle authentication](https://dozzle.dev/guide/authentication)
