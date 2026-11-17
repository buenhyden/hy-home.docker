---
title: "IaC Deployment Policy"
version: "1.3.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0060"
parent_ids:
- "AD-0009"
created: "2026-03-25"
next_review_at: "2027-05-13"
---

# IaC Deployment Policy

## Purpose and Scope

### Objective

이 정책은 `09-platform-ops`의 OpenTofu CLI helper와 Terrakube API/UI/executor를 이용한 IaC 변경의 승인, state, secret, evidence 기준을 정의한다.

#### Authority

- 상위 문서: [Platform Operations·Quality 아키텍처](../../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)

- 실행 버전의 원본은 Compose/Dockerfile 선언이며, [파생 버전 목록](../../../../infra/tech-stack.versions.json)은 변경 누락 검증에 사용한다.

### Applies To

- **Systems**: `infra/09-platform-ops/opentofu/docker-compose.yml`, `infra/09-platform-ops/terrakube/docker-compose.yml`
- **Environments**: 단일 HOME/DEV 호스트의 `iac` profile(온디맨드 DEV)

Terraform Compose runtime은 제거되었다. 기존 workspace 이관은 [Terraform 이관](../../guides/10-platform-and-backup/0082-opentofu.md#terraform-이관)을 따른다.

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0060-R1 | IaC 변경 시 | 필수: PR review, plan evidence, apply approval, state backend boundary 기록을 거친다 | 원격 PR public `changed` 검사 / 수동 | PR review와 plan/task evidence |
| POL-0060-R2 | 항상 | 필수: OpenTofu helper는 `$HOME/.aws`, `$HOME/.azure` read-only mount와 `workspace/` scope를 벗어나지 않는다 | `bash scripts/hardening/check-all-hardening.sh 09-platform-ops` | hardening 검사 결과 |
| POL-0060-R3 | 항상 | 필수: Terrakube secret은 Docker Secret 이름만 문서화하고 값은 노출하지 않는다 | 수동 | none |
| POL-0060-R4 | 항상 | 허용: 문서/검증 절차의 in-place 보강, state/backend 정책 강화, approval gate 추가 | 수동 | none |
| POL-0060-R5 | 항상 | 금지: secret 값 노출, 승인 없는 apply, Docker socket 권한 확대, 정책과 절차의 중복 SSoT 생성 | 수동 / hardening 검사 | 승인 기록 |

- **Required**: IaC 변경은 PR review, plan evidence, apply approval, state backend boundary 기록을 거친다.
- **Required**: OpenTofu helper는 `$HOME/.aws`, `$HOME/.azure` read-only mount와 `workspace/` scope를 벗어나지 않는다.
- **Required**: Terrakube secret material은 Docker Secret names만 문서화하고 값은 노출하지 않는다.
- **Allowed**: 문서/검증 절차의 in-place 보강, state/backend 정책의 보수적 강화, approval gate 추가.
- **Disallowed**: secret 값 노출, 승인 없는 apply, Docker socket 권한 확대, 정책과 절차의 중복 SSoT 생성.

#### 책임과 구현 제한

승인·예외 및 복구 판단 책임자는 `@buenhyden`이다. Terrakube executor의 Docker
socket 권한과 외부 도구 선택은 OpenTofu의 읽기 전용 cloud credential mount와
다르다. [Terrakube 정책](0069-terrakube.md)의 실행 경로 제한을 해소하기 전에는
브라우저 로그인이나 정적 검증으로 IaC 실행이 가능하다고 승인하지 않는다.

### Exceptions

#### Exception Conditions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

#### Approval and Review

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## Enforcement

### Mechanisms

- `bash scripts/hardening/check-all-hardening.sh 09-platform-ops`
- 원격 PR public `changed` 검사 ([quality policy](../../../../.agents/governance/quality-standards.md#canonical-delivery-phase-matrix))
- OpenTofu/Terrakube guide/runbook과 compose service names가 일치하는지 검토한다.

### Limits

정책은 hardening 검사와 PR 검사를 지정하지만 아래 항목은 기계적으로 강제되지 않는다.

- PR review, plan evidence, apply approval, state backend boundary 기록은 승인 절차에 의존하며 전용 검사가 없다.
- 마운트 범위, Docker Secret 비노출, 문서 중복 SSoT 금지는 수동 검토에 의존한다.
- guide/runbook과 compose service names 일치는 검토로 확인한다.
- Terrakube 실행 경로 제한이 해소되기 전에는 브라우저 로그인이나 정적 검증으로 IaC 실행 가능을 승인하지 않는다.

## Ownership

### Owner

책임 소유자는 frontmatter `owner`인 **@buenhyden**이다.

### Review Triggers

- 동일 주제 문서: 없음 — `0060`은 독립 정책이며 같은 번호의 Guide/Runbook은 없다.

- [Operations index](../../README.md)
- [OpenTofu guide](../../guides/10-platform-and-backup/0082-opentofu.md)
- [Terrakube guide](../../guides/10-platform-and-backup/0069-terrakube.md)
- [OpenTofu runbook](../../runbooks/10-platform-and-backup/0082-opentofu.md)
- [Terrakube runbook](../../runbooks/10-platform-and-backup/0069-terrakube.md)
