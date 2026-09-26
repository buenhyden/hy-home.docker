---
title: "IaC Deployment Policy"
version: "1.0.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-26"
layer: "operations"
artifact_id: "POL-0060"
parent_ids:
- "AD-0009"
created: "2026-03-25"
---

# IaC Deployment Policy

## Overview

이 정책은 `09-tooling`의 OpenTofu CLI helper와 Terrakube API/UI/executor를 이용한 IaC 변경의 승인, state, secret, evidence 기준을 정의한다.

## Policy Scope

- **Systems**: `infra/09-tooling/opentofu/docker-compose.yml`, `infra/09-tooling/terrakube/docker-compose.yml`
- **Environments**: local, development, homelab operations

Terraform Compose runtime은 제거되었다. 기존 workspace 이관은 [migration handoff](../guides/0068-terraform.md)를 따른다.

## Controls

- **Required**: IaC 변경은 PR review, plan evidence, apply approval, state backend boundary 기록을 거친다.
- **Required**: OpenTofu helper는 `$HOME/.aws`, `$HOME/.azure` read-only mount와 `workspace/` scope를 벗어나지 않는다.
- **Required**: Terrakube secret material은 Docker Secret names만 문서화하고 값은 노출하지 않는다.
- **Allowed**: 문서/검증 절차의 in-place 보강, state/backend 정책의 보수적 강화, approval gate 추가.
- **Disallowed**: secret 값 노출, 승인 없는 apply, Docker socket 권한 확대, 정책과 절차의 중복 SSoT 생성.

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- `bash scripts/hardening/check-all-hardening.sh 09-tooling`
- `python3 scripts/validation/run-ci-gate.py --profile changed`
- OpenTofu/Terrakube guide/runbook과 compose service names가 일치하는지 검토한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## Traceability

- Declared parent: [Tooling Tier Architecture Description](../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- Subject peers: none — no Guide or Runbook shares number `0060`.

## Related Documents

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [curated version projection](../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../README.md)
- [OpenTofu guide](../guides/0082-opentofu.md)
- [Terraform migration handoff](../guides/0068-terraform.md)
- [Terrakube guide](../guides/0069-terrakube.md)
- [OpenTofu runbook](../runbooks/0082-opentofu.md)
- [Terrakube runbook](../runbooks/0069-terrakube.md)
