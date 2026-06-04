---
status: active
---
<!-- Target: docs/05.operations/runbooks/09-tooling/terraform.md -->

# Terraform Runbook

<!-- [ID:09-tooling:terraform] -->

## Overview (KR)

이 런북은 `infra/09-tooling/terraform`의 컨테이너 기반 Terraform 실행 중 state lock,
state 손상, provider credential 오류가 발생했을 때 사용하는 복구 절차다. 정상 사용 배경은
guide에, 운영 통제 기준은 policy에 남기고, 이 문서는 반복 가능한 진단·복구·증거 수집만 다룬다.

## When to Use

- Terraform 실행에서 `Error acquiring the state lock`가 발생한 경우
- `Failed to load state` 또는 state corruption 의심 오류가 발생한 경우
- provider credential 만료, `AccessDenied`, `No valid credentials found` 오류가 발생한 경우
- Terraform 작업 전후 evidence capture가 필요한 경우

## Procedure

### 1. Confirm Execution Context

저장소 루트에서 Terraform compose 경로로 이동하고 compose 구성이 해석되는지 확인한다.

```bash
cd infra/09-tooling/terraform
docker compose config
```

### 2. Verify Remote Backend Access

원격 backend를 사용하는 경우, backend 서비스가 현재 compose 기준으로 해석되는지 확인한다.

```bash
docker compose -f ../../04-data/lake-and-object/minio/docker-compose.yml config
docker compose -f ../../04-data/lake-and-object/minio/docker-compose.yml ps
```

### 3. Force Unlocking State

이전 Terraform 실행이 비정상 종료되어 lock이 남아 있고, 다른 운영자 또는 자동화가 현재 apply를
수행 중이 아님을 확인한 뒤에만 lock을 해제한다.

```bash
: "${TERRAFORM_LOCK_ID:?Set TERRAFORM_LOCK_ID from the Terraform error output}"
docker compose run --rm terraform force-unlock "$TERRAFORM_LOCK_ID"
```

### 4. Restore Corrupted Local State

로컬 state 파일이 손상되었고 원격 backend 또는 최신 backup이 없는 경우에만 로컬 backup을 사용한다.

```bash
test -f terraform.tfstate.backup
mv terraform.tfstate terraform.tfstate.corrupted
cp terraform.tfstate.backup terraform.tfstate
docker compose run --rm terraform plan
```

### 5. Refresh Provider Credentials

호스트에 mount되는 cloud credential을 갱신한다. AWS SSO는 `AWS_PROFILE`을 사용하며, 별도 지정이
없으면 `default` profile을 사용한다.

```bash
AWS_PROFILE="${AWS_PROFILE:-default}"
aws sso login --profile "$AWS_PROFILE"
docker compose run --rm terraform init
```

Azure credential을 사용하는 작업이면 호스트에서 `az login`을 수행한 뒤 Terraform container를
다시 실행한다.

### 6. Verify Terraform Health

복구 후 format, validation, plan을 순서대로 확인한다.

```bash
docker compose run --rm terraform fmt -check
docker compose run --rm terraform validate
docker compose run --rm terraform plan
```

## Evidence

- 발생한 오류 메시지와 lock ID 또는 state 파일 증상을 기록한다.
- 실행한 명령, 종료 코드, `plan` 요약, operator/agent 이름, timestamp를 task evidence에 남긴다.
- credential 갱신은 값이 아니라 profile 이름, provider 종류, 성공 여부만 기록한다.

## Rollback or Recovery

- `force-unlock` 후에도 같은 lock이 반복되면 추가 unlock을 중단하고 active Terraform 실행 주체를 확인한다.
- 로컬 state 복구가 실패하면 `terraform.tfstate.corrupted`와 backup 파일을 보존하고 원격 backend 또는 백업 담당자에게 이관한다.
- 문서 변경만 있었다면 직전 diff 단위로 되돌리고 `bash scripts/validation/run-local-qa-gates.sh`를 재실행한다.
- runtime, secret value, remote deployment 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

## Escalation

- 원격 state가 손상되었거나 backup이 없으면 Infrastructure Architect에게 즉시 escalation한다.
- credential 오류가 권한 축소, 계정 잠금, MFA 실패와 연결되면 Security/Ops owner에게 escalation한다.
- 복구 절차가 현재 관측된 장애와 맞지 않으면 변경을 멈추고 evidence를 보존한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/09-tooling/terraform.md)
- [Operations policy](../../policies/09-tooling/terraform.md)
