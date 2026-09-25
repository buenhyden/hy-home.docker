---
title: "Terraform Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-15"
layer: "operations"
artifact_id: "RUN-0068"
parent_ids:
- "GDE-0068"
created: "2026-05-17"
---

# Terraform to OpenTofu Migration Runbook

## When to Use

기존 Terraform workspace를 현재 OpenTofu 운영으로 이관할 때 사용한다. 저장소에는
기동할 Terraform 서비스가 없으므로 과거 Compose 명령을 재실행하지 않는다.

## Procedure

1. state backend와 lock 소유자, provider lock file, module source를 메타데이터로 식별한다.
2. 승인된 절차로 암호화된 state 복구본을 확보하고 복제 workspace를 준비한다.
3. [OpenTofu Runbook](0082-opentofu.md)의 승인 경계에 따라 복제본을 검증한다.
4. 예상하지 않은 resource replacement, backend 이동 또는 schema 변경이 있으면 멈춘다.
5. 검토된 plan과 복구 증거를 확인한 뒤 실제 이관 대상을 별도로 승인받는다.

## Evidence

원본 CLI/source commit, provider/module identity, 비교 결과와 복구 시험 상태만 남긴다.
state, plan 파일 내용, credential과 token은 출력하지 않는다.

## Rollback or Recovery

검증 전 원본 state를 덮어쓰지 않는다. 적용 이후에는 Git 되돌리기만으로 복구하지
말고 원래 CLI/provider의 호환성과 백업을 확인해 별도 복구 계획을 실행한다.

## Escalation

동시 lock, 미검증 provider 또는 복구본 부재는 @buenhyden에게 보고하고 중단한다.

## Traceability

- Governing architecture: [AD-0009](../../02.architecture/descriptions/0009-tooling-architecture.md)
- Retained migration subject: [Guide](../guides/0068-terraform.md), [Policy](../policies/0068-terraform.md), [Runbook](0068-terraform.md)
- Current implementation owner: [OpenTofu](../guides/0082-opentofu.md)

## Related Documents

- [Operations index](../README.md)
- [OpenTofu implementation](../../../infra/09-tooling/opentofu/docker-compose.yml)
- [Version projection](../../../infra/tech-stack.versions.json)
