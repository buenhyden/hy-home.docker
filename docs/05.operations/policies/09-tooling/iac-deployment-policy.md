---
status: active
---
<!-- Target: docs/05.operations/policies/09-tooling/iac-deployment-policy.md -->

# IaC Deployment Policy

## Overview (KR)

이 정책은 `09-tooling`의 Terraform CLI helper와 Terrakube API/UI/executor를 이용한 IaC 변경의 승인, state, secret, evidence 기준을 정의한다.

## Policy Scope

- **Systems**: `infra/09-tooling/terraform/docker-compose.yml`, `infra/09-tooling/terrakube/docker-compose.yml`
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**: IaC 변경은 PR review, plan evidence, apply approval, state backend boundary 기록을 거친다.
- **Required**: Terraform helper는 `$HOME/.aws`, `$HOME/.azure` read-only mount와 `workspace/` scope를 벗어나지 않는다.
- **Required**: Terrakube secret material은 Docker Secret names만 문서화하고 값은 노출하지 않는다.
- **Allowed**: 문서/검증 절차의 in-place 보강, state/backend 정책의 보수적 강화, approval gate 추가.
- **Disallowed**: secret 값 노출, 승인 없는 apply, Docker socket 권한 확대, 정책과 절차의 중복 SSoT 생성.

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- `bash scripts/hardening/check-all-hardening.sh 09-tooling`
- `bash scripts/validation/check-repo-contracts.sh`
- Terraform/Terrakube guide/runbook과 compose service names가 일치하는지 검토한다.

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

- [Operations index](../../README.md)
- [Terraform guide](../../guides/09-tooling/terraform.md)
- [Terrakube guide](../../guides/09-tooling/terrakube.md)
- [Terraform runbook](../../runbooks/09-tooling/terraform.md)
- [Terrakube runbook](../../runbooks/09-tooling/terrakube.md)
