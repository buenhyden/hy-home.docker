---
title: "OpenTofu Runbook"
version: "0.2.1"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0082"
parent_ids:
- "POL-0082"
created: "2026-09-19"
---

# OpenTofu Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### When to Use

검토된 plan, lock 실패, 보호된 state backup/recovery, 또는 런타임/provider upgrade에
사용한다. 저장소 루트에서 작업한다. backend/provider에 접근하는 명령은 아래 명시된 승인이
필요하다.

## Procedure

### Procedure

1. configuration commit, 정확한 workspace 디렉터리, 선택한 OpenTofu workspace, backend,
   account, 명령 클래스, rollback 담당자를 기록한다. 다른 writer가 활성 상태가 아님을
   확인한다.
2. 아래 첫 명령은 설정 검증이다. 두 번째는 cloud credential·workspace를 마운트한
   컨테이너 생성이므로 해당 실행이 승인된 경우에만 수행한다.

   ```bash
   docker compose --profile iac config --quiet
   docker compose --profile iac run --rm --no-deps opentofu version
   ```

3. 승인된 plan에서는 정확한 workspace를 초기화하고 의도한 OpenTofu workspace를 선택한 뒤,
   저장할 plan을 생성하기 전에 validation을 실행한다. plan은 제한된 권한으로 Git 외부에
   저장한다. digest와 resource action 개수만 기록한다.
4. `apply` 전에 중단한다. 검토자는 저장된 plan digest, account, 예상 변경 사항을 명시적
   apply 승인과 묶어야 한다. 이 경계를 `-auto-approve`로 대체하지 않는다.

### State backup and recovery

1. local 또는 remote backend를 판별하고 활성 writer/lock owner가 없음을 증명한다.
2. local state의 경우 state와 backup 파일을 mode `0600`으로 보호된 디렉터리에 복사한다.
   remote state의 경우 backend의 atomic/버전 스냅샷을 우선한다. `tofu state pull`을 사용할
   경우 보호된 파일로 직접 redirect하고 화면에 표시하지 않는다.
3. checksum, backend/workspace 식별자, 보호된 보존 상태를 검증한다. 파일이 있다고 해서
   restore가 증명되지는 않는다.
4. 먼저 외부 provider/network 접근이 비활성화된 격리 backend에서 복원한다. lineage, serial,
   `state list`를 비공개로 비교한다.
5. `tofu state push`는 최후 수단이며 별도로 승인받은 쓰기다. 먼저 현재 remote 스냅샷을 보존하고,
   승인이 정확히 그 손실 수용 사례를 명시하지 않는 한 lineage나 serial 보호를 우회하기 위해
   `-force`를 사용하지 않는다.

### Lock and upgrade recovery

- lock 오류의 경우 보유자를 확인하고 writer를 기다리거나 중단시킨다. `force-unlock`은 운영자
  본인의 방치된 lock ID에만 사용한다.
- upgrade 전에 위의 state backup을 수행하고, 중간 upgrade 노트를 읽고, local 이미지를
  재빌드하고, backend 설정을 바꾸지 않고 초기화한 뒤, 적용하지 않은 plan을 비교한다.
  호환성이 실패하면 이미지/빌드를 롤백한다. upgrade가 state를 변경한 경우에만 검증된
  backup에서 state를 롤백한다.

### 상태 보존과 변경 전 검토

upgrade나 state 작업 전에 backend를 확인한다. 로컬 state의 경우 모든 writer를
멈추고 state와 backup 파일을 mode-0600으로 복사한다. 원격 backend의 경우
atomic/versioned backup 기능이나 `tofu state pull`을 보호된 파일로 사용하며,
그 출력을 터미널이나 채팅으로 보내지 않는다. 신뢰하기 전에 분리된/테스트용
backend로 격리된 restore를 검증한다. 중간의 모든 OpenTofu upgrade 노트를
검토하고 apply하지 않고 저장된 plan workflow를 테스트한다. 이 문서를 변경하면서
plan, state backup, restore, provider 호출은 실행하지 않았다.

## Verification

### Evidence

exit, 버전, configuration/plan digest, backend/workspace 식별자, 정제된 action 개수, lock
owner 결정, 최종 처리 상태를 기록한다. state, plan 본문, credential, 또는 secret을 포함한
provider 응답은 절대 기록하지 않는다.

## Rollback and Escalation

### Rollback or Recovery

Git이나 이미지를 되돌려도 remote resource는 되돌아가지 않는다. resource rollback에는 새로
검토된 plan이 필요하다. state restore와 upgrade 리허설은 현재 이 저장소에서 **계획됨,
미실행** 상태다.

### Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

알 수 없는 backend/workspace, 보호된 backup 부재, 활성 lock owner, lineage/serial 불일치,
파괴적 plan, 또는 credential/account 모호성이 있으면 중단한다.

### Traceability

- [Guide](../guides/0082-opentofu.md) (`GDE-0082`)
- [Policy](../policies/0082-opentofu.md) (`POL-0082`)
- [OpenTofu Compose](../../../infra/09-platform-ops/opentofu/docker-compose.yml)

## Related Documents

- [OpenTofu state locking](https://opentofu.org/docs/language/state/locking/)
- [OpenTofu upgrading](https://opentofu.org/docs/intro/upgrading/)
- [운영 인덱스](../README.md)
