---
title: "Terraform Operations Policy"
version: "1.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "POL-0068"
parent_ids:
- "AD-0009"
created: "2026-05-17"
---

# Terraform to OpenTofu Migration Policy

## Overview

Terraform 운영 주제는 MIGRATE 상태의 사용 맥락이며 현재 실행 소유자는 OpenTofu다.

## Policy Scope

기존 Terraform state와 provider/module 계약을 OpenTofu 운영으로 옮기는 작업.

## Controls

- 기존 state와 lock 정보를 보존하고 암호화된 복구본을 먼저 준비한다.
- 복제 workspace에서 provider 및 backend 호환성을 검증한다.
- CLI 교체와 실제 remote resource 변경을 별도 검토한다.
- `apply`, `destroy`, state rewrite와 force-unlock은 정확한 대상 승인을 요구한다.
- 새로운 Terraform 서비스나 병렬 updater를 만들어 소유권을 분산하지 않는다.

## Exceptions

호환성 때문에 기존 CLI가 필요하면 담당자, 대상 workspace, 지원 종료 조건과
검증 계획을 기록한다. 예외는 기존 private state 공개를 허용하지 않는다.

## Verification

원래 plan과 이관 plan의 resource action을 로컬에서 비교하고 변경 개수와 결과만
기록한다. 서비스 부재를 실패한 daemon 상태로 판단하지 않는다.

## Review Cadence

각 state 이관 및 provider/backend 변경 때 검토한다.

## Traceability

- Governing architecture: [AD-0009](../../02.architecture/descriptions/0009-tooling-architecture.md)
- Retained migration subject: [Guide](../guides/0068-terraform.md), [Policy](0068-terraform.md), [Runbook](../runbooks/0068-terraform.md)
- Current implementation owner: [OpenTofu](../guides/0082-opentofu.md)

## Related Documents

- [Operations index](../README.md)
- [OpenTofu implementation](../../../infra/09-tooling/opentofu/docker-compose.yml)
- [Version projection](../../../infra/tech-stack.versions.json)
