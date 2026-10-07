---
title: "IaC Deployment Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-07"
layer: "operations"
artifact_id: "POL-0060"
parent_ids:
- "AD-0009"
created: "2026-03-25"
---

# IaC Deployment Policy

## Overview

### Overview

이 정책은 `09-platform-ops`의 OpenTofu CLI helper와 Terrakube API/UI/executor를 이용한 IaC 변경의 승인, state, secret, evidence 기준을 정의한다.

## Scope

### Policy Scope

- **Systems**: `infra/09-platform-ops/opentofu/docker-compose.yml`, `infra/09-platform-ops/terrakube/docker-compose.yml`
- **Environments**: local, development, homelab operations

Terraform Compose runtime은 제거되었다. 기존 workspace 이관은 [migration handoff](../guides/0068-terraform.md)를 따른다.

### Traceability

- 상위 문서: [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- 동일 주제 문서: 없음 — `0060`은 독립 정책이며 같은 번호의 Guide/Runbook은 없다.

## Rules

### Controls

- **Required**: IaC 변경은 PR review, plan evidence, apply approval, state backend boundary 기록을 거친다.
- **Required**: OpenTofu helper는 `$HOME/.aws`, `$HOME/.azure` read-only mount와 `workspace/` scope를 벗어나지 않는다.
- **Required**: Terrakube secret material은 Docker Secret names만 문서화하고 값은 노출하지 않는다.
- **Allowed**: 문서/검증 절차의 in-place 보강, state/backend 정책의 보수적 강화, approval gate 추가.
- **Disallowed**: secret 값 노출, 승인 없는 apply, Docker socket 권한 확대, 정책과 절차의 중복 SSoT 생성.

### Verification

- `bash scripts/hardening/check-all-hardening.sh 09-platform-ops`
- 원격 PR public `changed` 검사 ([quality policy](../../../.agents/governance/quality-standards.md#canonical-delivery-phase-matrix))
- OpenTofu/Terrakube guide/runbook과 compose service names가 일치하는지 검토한다.

### Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

### 책임과 구현 제한

승인·예외 및 복구 판단 책임자는 `@buenhyden`이다. Terrakube executor의 Docker
socket 권한과 외부 도구 선택은 OpenTofu의 읽기 전용 cloud credential mount와
다르다. [Terrakube 정책](0069-terrakube.md)의 실행 경로 제한을 해소하기 전에는
브라우저 로그인이나 정적 검증으로 IaC 실행이 가능하다고 승인하지 않는다.

## Exceptions

### Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Related Documents

- 실행 버전의 원본은 Compose/Dockerfile 선언이며, [파생 버전 목록](../../../infra/tech-stack.versions.json)은 변경 누락 검증에 사용한다.

- [Operations index](../README.md)
- [OpenTofu guide](../guides/0082-opentofu.md)
- [Terraform migration handoff](../guides/0068-terraform.md)
- [Terrakube guide](../guides/0069-terrakube.md)
- [OpenTofu runbook](../runbooks/0082-opentofu.md)
- [Terrakube runbook](../runbooks/0069-terrakube.md)
