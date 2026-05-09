<!-- [ID:09-tooling:terraform] -->
# Runbook: Terraform Recovery (P2)

> Procedures for resolving common Terraform execution errors and state lock issues.

## Symptoms

- "Error acquiring the state lock".
- "Error: Failed to load state: State data is corrupted".
- "Error: No valid credentials found".
- "Error: Error refreshing state: AccessDenied".

## Diagnostic Steps

### 1. Check Execution Context

Ensure you are running the command from the correct directory:

```bash
cd ${DEFAULT_TOOLING_DIR}/terraform
```

### 2. Verify Backend Access

If using a remote backend, verify that MinIO/S3 is up:

```bash
# Check MinIO status if applicable
cd ${DEFAULT_DATA_DIR}/minio
docker compose ps
```

## Recovery Procedures

### 1. Force Unlocking State

If a previous execution crashed and left the state locked:

1. Identify the **Lock ID** from the error message.
2. Run the force-unlock command:

   ```bash
   docker compose run --rm terraform force-unlock <LOCK_ID>
   ```

> [!CAUTION]
> Only force-unlock if you are 100% sure that no other person or process is currently modifying the infrastructure.

### 2. Handling Corrupted Local State

If the `.tfstate` file is unreadable:

1. Check for the `terraform.tfstate.backup` file.
2. If the backup exists and is valid, swap it:

   ```bash
   mv terraform.tfstate terraform.tfstate.corrupted
   cp terraform.tfstate.backup terraform.tfstate
   ```

3. Run `terraform plan` to verify consistency.

### 3. Resolving Provider Credential Failures

If credentials expired or are invalid:

1. Verify the host mounts in `docker-compose.yml` point to valid directories.
2. Refresh tokens on the host:

   ```bash
   # For AWS
   aws sso login --profile <your-profile>
   ```

3. Re-run `terraform init`.

## Escalation Policy

- **P1**: Corrupted remote state with no backup -> Notify Infrastructure Architect immediately.
- **P2**: Stuck state lock or transient network error -> Follow manual recovery steps.

## Related References

- **Infrastructure**: [Terraform Tool](../../../infra/09-tooling/terraform/README.md)
- **Guide**: [Terraform System Guide](../../07.guides/09-tooling/terraform.md)
- **Operation**: [IaC Operations Policy](../../08.operations/09-tooling/terraform.md)

---

## Overview (KR)

이 런북은 `docs/09.runbooks/09-tooling/terraform.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

## Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

## Canonical References

- [../README.md](../README.md)
- [../../08.operations/README.md](../../08.operations/README.md)
- [../../07.guides/README.md](../../07.guides/README.md)

## When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

## Procedure or Checklist

### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

### Procedure

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

## Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

## Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

## Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

## Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Related Operational Documents

- [../README.md](../README.md)
- [../../08.operations/README.md](../../08.operations/README.md)
- [../../10.incidents/README.md](../../10.incidents/README.md)
