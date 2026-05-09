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

- **Infrastructure**: [Terrakube Platform](../../../infra/09-tooling/terrakube/README.md)
- **Guide**: [Terrakube System Guide](../../07.guides/09-tooling/terrakube.md)
- **Runbook**: [Terrakube Recovery Runbook](../../09.runbooks/09-tooling/terrakube.md)

---

## Overview (KR)

이 문서는 `docs/08.operations/09-tooling/terrakube.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

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

- [../README.md](../README.md)
- [../../07.guides/README.md](../../07.guides/README.md)
- [../../09.runbooks/README.md](../../09.runbooks/README.md)
