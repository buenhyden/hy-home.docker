<!-- [ID:09-tooling:terraform] -->
# Operations: Terraform Policy

> Operational guidelines and policies for managing infrastructure via Terraform.

## Policy Overview

All infrastructure changes in `hy-home.docker` must be managed via Terraform to ensure auditability and reproducibility.

## State Management Policy

### 1. Remote State Requirement

- For any environment with more than one contributor, a **Remote Backend** (S3/MinIO) is mandatory.
- State locking must be enabled (via DynamoDB or MinIO Object Lock).

### 2. State Backups

- Remote states are automatically versioned by the backend.
- Monthly exports of the `.tfstate` to the `04-data/backups` tier are required for disaster recovery.

## Deployment Workflow

| Step | Action | Mandatory? |
| :--- | :--- | :--- |
| **Validation** | `validate` & `fmt` | Yes |
| **Planning** | `plan -out=tfplan` | Yes |
| **Peer Review** | Review `tfplan` output | Recommended |
| **Execution** | `apply tfplan` | Yes |

> [!IMPORTANT]
> Never use `terraform apply` without a pre-generated plan file in production environments.

## Maintenance Cycles

### Provider Updates

- Check for provider updates (AWS, Docker, Kubernetes) every **quarter**.
- Test updates in a non-production workspace before merging.

### Credential Rotation

- Host-level cloud credentials mounted to the Terraform container must be rotated every **90 days**.

## Compliance & Security

- **Secrets**: Never hardcode credentials in `.tf` files. Use environment variables or secret managers (Vault).
- **Versioning**: Pin all provider and module versions to prevent breaking changes during `init`.

## Related References

- **Infrastructure**: [Terraform Tool](../../../../infra/09-tooling/terraform/README.md)
- **Usage**: [Terraform System Usage](./terraform.md)
- **Procedure**: [Terraform Recovery Procedure](./terraform.md)

---

## Overview (KR)

이 문서는 `docs/05.operations/09-tooling/terraform.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

## Applies To

- **Systems**: 관련 Docker Compose 서비스와 문서화된 운영 자산
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**: 변경 전 관련 README, guide, runbook 확인
- **Allowed**: 문서와 검증 절차의 in-place 보강
- **Disallowed**: secret 값 노출, 승인 없는 runtime 변경, 정책과 절차의 중복 SSoT 생성

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- 관련 repository validation script와 문서 heading audit로 준수 여부를 확인한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Related Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

## Usage

> Migrated from `docs/05.operations/09-tooling/terraform.md` during the 2026-05-10 operations taxonomy consolidation.

<!-- [ID:09-tooling:terraform] -->
### Usage: Terraform System

> Comprehensive guide for managing Infrastructure as Code (IaC) using the containerized Terraform environment.

#### Overview

Terraform is used in `hy-home.docker` to provision and manage cloud resources (AWS, Azure) and local infrastructure (Docker, Kubernetes). To ensure environment parity and eliminate "works on my machine" issues, we use a containerized CLI approach.

#### Key Concepts

##### 1. Job-based Execution

Instead of a long-running service, Terraform is treated as a **job**.

- Always use `docker compose run --rm terraform` to clean up containers after execution.
- Profiles: Ensure the `tooling` profile is active or specified if needed.

##### 2. State Management

- **Local State**: Stored in `infra/09-tooling/terraform/workspace/terraform.tfstate`.
- **Remote Backend**: It is highly recommended to use the `s3` backend (integrated with MinIO in `04-data`) for shared state and locking.

##### 3. Credential Handling

Credentials are not stored in the container. They are mounted from the host:

- AWS: `/root/.aws` maps to your host `$HOME/.aws`.
- Azure: `/root/.azure` maps to your host `$HOME/.azure`.

#### Common Workflows

##### Initializing a Project

```bash
cd infra/09-tooling/terraform
docker compose run --rm terraform init
```

##### Resource Provisioning (Plan & Apply)

Always generate a plan file before applying to prevent accidental changes.

```bash
### 1. Generate plan
docker compose run --rm terraform plan -out=tfplan

### 2. Review the plan
### 3. Apply the plan
docker compose run --rm terraform apply tfplan
```

##### Formating and Validation

Maintain code quality by using built-in tools.

```bash
docker compose run --rm terraform fmt
docker compose run --rm terraform validate
```

#### Troubleshooting

##### Lock File Issues

If Terraform fails with "Error acquiring the state lock", ensure no other group members are applying changes. If a process crashed, refer to the [Procedure](./terraform.md#state-lock-recovery).

##### Network Connectivity

The container uses `infra_net`. If you cannot reach local services (like MinIO), verify the network labels in `docker-compose.yml`.

#### Related References

- **Infrastructure**: [Terraform Tool](../../../../infra/09-tooling/terraform/README.md)
- **Operation**: [IaC Operations Policy](./terraform.md)
- **Procedure**: [Terraform Recovery Procedure](./terraform.md)

---

#### Overview (KR)

이 문서는 `docs/05.operations/09-tooling/terraform.md` 주제의 사용 가이드다. 기존 본문을 기준으로 작업자가 필요한 배경, 절차, 주의사항을 빠르게 찾도록 보강한다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- AI Agent

#### Purpose

관련 인프라 서비스나 문서 영역을 이해하고 안전하게 변경 또는 운영할 수 있도록 돕는다.

#### Prerequisites

- Repository root README 확인
- 관련 `infra/` 서비스 README 확인
- 필요한 경우 대응 operation/runbook 문서 확인

#### Step-by-step Instructions

1. 관련 README와 기존 본문을 먼저 읽는다.
2. 실제 compose/config 경로와 문서 설명이 일치하는지 확인한다.
3. 변경이 필요하면 대응 템플릿과 상위 README 링크를 함께 갱신한다.
4. 관련 검증 스크립트 또는 문서 audit를 실행한다.

#### Common Pitfalls

- guide 문서에 운영 정책이나 incident timeline을 섞지 않는다.
- secret 값, token, 인증서 원문을 열람하거나 문서화하지 않는다.
- runtime 변경이 필요한 경우 문서 보강과 별도 작업으로 분리한다.

#### Related Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

## Procedure

> Migrated from `docs/05.operations/09-tooling/terraform.md` during the 2026-05-10 operations taxonomy consolidation.

<!-- [ID:09-tooling:terraform] -->
### Procedure: Terraform Recovery (P2)

> Procedures for resolving common Terraform execution errors and state lock issues.

#### Symptoms

- "Error acquiring the state lock".
- "Error: Failed to load state: State data is corrupted".
- "Error: No valid credentials found".
- "Error: Error refreshing state: AccessDenied".

#### Diagnostic Steps

##### 1. Check Execution Context

Ensure you are running the command from the correct directory:

```bash
cd ${DEFAULT_TOOLING_DIR}/terraform
```

##### 2. Verify Backend Access

If using a remote backend, verify that MinIO/S3 is up:

```bash
### Check MinIO status if applicable
cd ${DEFAULT_DATA_DIR}/minio
docker compose ps
```

#### Recovery Procedures

##### 1. Force Unlocking State

If a previous execution crashed and left the state locked:

1. Identify the **Lock ID** from the error message.
2. Run the force-unlock command:

   ```bash
   docker compose run --rm terraform force-unlock <LOCK_ID>
   ```

> [!CAUTION]
> Only force-unlock if you are 100% sure that no other person or process is currently modifying the infrastructure.

##### 2. Handling Corrupted Local State

If the `.tfstate` file is unreadable:

1. Check for the `terraform.tfstate.backup` file.
2. If the backup exists and is valid, swap it:

   ```bash
   mv terraform.tfstate terraform.tfstate.corrupted
   cp terraform.tfstate.backup terraform.tfstate
   ```

3. Run `terraform plan` to verify consistency.

##### 3. Resolving Provider Credential Failures

If credentials expired or are invalid:

1. Verify the host mounts in `docker-compose.yml` point to valid directories.
2. Refresh tokens on the host:

   ```bash
   ### For AWS
   aws sso login --profile <your-profile>
   ```

3. Re-run `terraform init`.

#### Escalation Policy

- **P1**: Corrupted remote state with no backup -> Notify Infrastructure Architect immediately.
- **P2**: Stuck state lock or transient network error -> Follow manual recovery steps.

#### Related References

- **Infrastructure**: [Terraform Tool](../../../../infra/09-tooling/terraform/README.md)
- **Usage**: [Terraform System Usage](./terraform.md)
- **Operation**: [IaC Operations Policy](./terraform.md)

---

#### Overview (KR)

이 런북은 `docs/05.operations/09-tooling/terraform.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

#### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

#### Canonical References

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

#### When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

#### Procedure or Checklist

##### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

##### Procedure

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

#### Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

#### Related Operational Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/incidents/README.md](../../incidents/README.md)
