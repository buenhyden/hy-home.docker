---
title: IaC Deployment Policy
type: operations/policy
layer: operations
status: active
owner: "@buenhyden"
artifact_id: POL-0060
parent_ids:
  - SPEC-0010
created: 2026-03-25
updated: 2026-08-11
---
<!-- Target: docs/05.operations/catalog/09-tooling/0060-iac-deployment/policy.md -->

# IaC Deployment Policy

## Overview

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
- `python3 scripts/validation/run-ci-gate.py --profile changed`
- Terraform/Terrakube guide/runbook과 compose service names가 일치하는지 검토한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## Related Documents

- [Operations index](../../../README.md)
- [Terraform guide](../0068-terraform/guide.md)
- [Terrakube guide](../0069-terrakube/guide.md)
- [Terraform runbook](../0068-terraform/runbook.md)
- [Terrakube runbook](../0069-terrakube/runbook.md)
