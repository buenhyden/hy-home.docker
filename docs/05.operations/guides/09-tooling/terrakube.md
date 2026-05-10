<!-- [ID:09-tooling:terrakube] -->
# Operations: Terrakube Policy

> Operational guidelines and governance for the centralized Terrakube IaC platform.

## Governance Overview

Terrakube serves as the authoritative source for infrastructure state. Strict access control and operational hygiene are required to prevent data loss or unauthorized provisioning.

## Access Control Policy

### 1. Workspace RBAC

- **Admin**: Full control over organization settings and workspace secrets (Senior DevOps only).
- **Maintainer**: Can trigger plans and applies for specific workspaces.
- **Reader**: View-only access to execution logs.

### 2. SSO Authentication

- All users must authenticate via Keycloak.
- Local admin accounts are disabled in production to ensure auditability.

## Resource & Execution Policy

| Policy Type | Setting | Description |
| :--- | :--- | :--- |
| **Execution Timeout** | 60 minutes | Jobs exceeding this limit are killed to prevent resource leaks. |
| **Max Concurrency** | 5 jobs | Maximum simultaneous executors per node. |
| **Log Retention** | 30 days | Execution logs are purged from the DB after one month. |

## Registry Maintenance

- **Module Versioning**: All modules must follow Semantic Versioning (SemVer).
- **Audit**: Monthly review of unused modules and old versions to reclaim storage.

## Security Standards

- **Secret Scanning**: All Git repositories integrated with Terrakube must undergo pre-commit scanning.
- **Sensitive Variables**: Mandatory encryption for all cloud provider secrets hosted within Terrakube.

## Routine Maintenance

### Weekly

- Monitor `terrakube-api` logs for worker drift or storage connectivity errors.
- Verify `tfstate` bucket health in MinIO.

### Monthly

- Perform a manual backup of the Terrakube metadata database (PostgreSQL).
- Update the base Docker images for executors to include the latest security patches.

## Related References

- **Infrastructure**: [Terrakube Platform](../../../../infra/09-tooling/terrakube/README.md)
- **Usage**: [Terrakube System Usage](./terrakube.md)
- **Procedure**: [Terrakube Recovery Procedure](./terrakube.md)

---

## Overview (KR)

이 문서는 `docs/05.operations/09-tooling/terrakube.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

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

> Migrated from `docs/05.operations/09-tooling/terrakube.md` during the 2026-05-10 operations taxonomy consolidation.

<!-- [ID:09-tooling:terrakube] -->
### Usage: Terrakube Platform

> User guide for managing infrastructure automation workflows via the Terrakube platform.

#### Overview

Terrakube is an open-source alternative to Terraform Cloud, providing a centralized control plane for Infrastructure as Code (IaC). It manages workspaces, variables, team access, and private modules.

#### Getting Started

##### 1. Initial Login

Access the UI at `https://terrakube-ui.${DEFAULT_URL}`. Authentication is integrated with Keycloak; use your engineering credentials.

##### 2. Organizations and Workspaces

- **Organizations**: High-level groups (e.g., `prod`, `dev`, `shared`).
- **Workspaces**: Individual projects mapped to a specific Git repository and set of variables.

#### Feature Breakdown

##### Private Module Registry

Terrakube allows you to host internal Terraform modules.

- To publish: Tag your module repository (e.g., `terraform-aws-s3-v1.0.0`).
- To consume: Reference the module using the Terrakube API URL in your `.tf` code.

##### Variable Management

- **Environment Variables**: For provider credentials (AWS_ACCESS_KEY, etc.).
- **Terraform Variables**: For specific infrastructure parameters.
- **Sensitive Variables**: Marked as "Sensitive" are stored encrypted and never displayed in logs.

##### UI-Driven Workflows

- **Plan**: Trigger a `terraform plan` to view proposed changes in the UI logs.
- **Apply**: Manual or automatic approval of plans to execute changes.

#### Integration Details

##### Remote State (MinIO)

Terrakube automatically manages its own internal state storage in the `tfstate` bucket of MinIO. Manual configuration of the `s3` backend in your `.tf` files is not required when running through the platform.

##### Executor Model

The `terrakube-executor` spins up ephemeral Docker containers for every job. It requires access to `/var/run/docker.sock` on the host to manage these child containers.

#### Troubleshooting

##### Executor Timeout

If a job is stuck in "Pending" status, verify that the `terrakube-executor` container is healthy:

```bash
docker compose logs -f terrakube-executor
```

##### SSO Failures

If OIDC logout occurs frequently, check the token expiration settings in the `hy-home.realm` of Keycloak.

#### Related References

- **Infrastructure**: [Terrakube Platform](../../../../infra/09-tooling/terrakube/README.md)
- **Operation**: [Terrakube Operations Policy](./terrakube.md)
- **Procedure**: [Terrakube Recovery Procedure](./terrakube.md)

---

#### Overview (KR)

이 문서는 `docs/05.operations/09-tooling/terrakube.md` 주제의 사용 가이드다. 기존 본문을 기준으로 작업자가 필요한 배경, 절차, 주의사항을 빠르게 찾도록 보강한다.

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

> Migrated from `docs/05.operations/09-tooling/terrakube.md` during the 2026-05-10 operations taxonomy consolidation.

<!-- [ID:09-tooling:terrakube] -->
### Procedure: Terrakube Recovery (P2)

> Procedures for recovering the Terrakube platform from executor failures, sync drift, and database corruption.

#### Symptoms

- UI shows jobs stuck in "Pending" or "Running" for hours.
- Login redirection loops between Terrakube and Keycloak.
- "Error: S3 Storage not reachable" in API logs.
- Workspace state is "Locked" permanently in the UI.

#### Diagnostic Steps

##### 1. Check API and Executor Health

Terrakube provides Spring Actuator endpoints for health checks.

```bash
curl -I https://terrakube-api.${DEFAULT_URL}/actuator/health
```

##### 2. Verify Docker Socket Access

The executor requires a healthy Docker socket to spawn Terraform runs.

```bash
docker exec terrakube-executor docker info
```

#### Recovery Procedures

##### 1. Cleaning Up Hung Executors

If the UI shows a job as running but the host has no associated container:

1. Locate the `terrakube-executor` logs to find the orphan job ID.
2. Manually kill the subprocess if it exists on the host.
3. Restart the executor service to reset internal queue state:

   ```bash
   cd ${DEFAULT_TOOLING_DIR}/terrakube
   docker compose restart terrakube-executor
   ```

##### 2. Resolving OIDC / DEX Auth Loops

If users cannot login despite valid Keycloak credentials:

1. Check the `terrakube-api` log for "Invalid Token" or "JWK extraction failure".
2. Ensure the `OAUTH2_PROXY_CLIENT_ID` and Secrets match between Keycloak and the `docker-compose.yml`.
3. Restart the API server to refresh the OIDC configuration.

##### 3. Manual Workspace Unlock

If a workspace is stuck in a locked state and "Force Unlock" in the UI fails:

1. Connect to the `terrakube` database in PostgreSQL.
2. Update the workspace record status manually.

   ```sql
   UPDATE workspace SET locked = false WHERE name = '<workspace_name>';
   ```

> [!WARNING]
> Manual DB modifications are high-risk. Always back up the `terrakube` database before running raw SQL.

#### Escalation Policy

- **P1**: Total loss of the `tfstate` bucket content in MinIO -> Follow Disaster Recovery Plan.
- **P2**: Intermittent executor failures or UI sync issues -> Follow manual restart and queue cleanup.

#### Related References

- **Infrastructure**: [Terrakube Platform](../../../../infra/09-tooling/terrakube/README.md)
- **Usage**: [Terrakube System Usage](./terrakube.md)
- **Operation**: [Terrakube Operations Policy](./terrakube.md)

---

#### Overview (KR)

이 런북은 `docs/05.operations/09-tooling/terrakube.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

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
