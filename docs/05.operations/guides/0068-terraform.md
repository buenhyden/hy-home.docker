---
title: "Operations: Terraform Policy Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0068"
parent_ids:
- "POL-0068"
created: "2026-05-10"
---

# Terraform to OpenTofu Migration Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

이 주제는 기존 Terraform 사용자의 OpenTofu 이관 맥락을 보존한다. 현재 저장소의
실행 도구는 OpenTofu이며 Terraform Compose 서비스는 존재하지 않는다. 새 작업은
[OpenTofu Guide](0082-opentofu.md)에서 시작한다. Terraform configuration과
state가 자동으로 호환된다고 가정하지 않는다.

### Common Checks

실제 state backend, lock 소유자, provider lock file, module 원본과 원래 CLI를
확인한다. 별도 workspace에서 초기화·검증·plan 차이를 조사한 뒤 이관을 승인한다.
민감한 state와 plan payload는 문서나 로그에 넣지 않는다.

### Runbook Handoff

[이관 Runbook](../runbooks/0068-terraform.md)은 기존 state 보호를, [OpenTofu Runbook](../runbooks/0082-opentofu.md)은 현재 CLI 실행을 소유한다.

### 실행 도구의 적용 범위

독립 Terraform Compose 서비스가 없다는 사실은 Terrakube workspace의 엔진까지
OpenTofu로 고정되었다는 뜻이 아니다. Terrakube executor는 외부 도구·엔진 목록을
참조하므로 이관 대상별 실제 엔진, provider 및 state 호환성을 확인한다. 일반 서비스의
포트·HTTP health·daemon 재시작은 이 이관 주제에 적용되지 않는다.

### Traceability

- 설계 근거: [AD-0009](../../02.architecture/descriptions/0009-tooling-architecture.md)
- 유지되는 이관 주제: [Guide](0068-terraform.md), [Policy](../policies/0068-terraform.md), [Runbook](../runbooks/0068-terraform.md)
- 현재 구현 소유자: [OpenTofu](0082-opentofu.md)

## Related Documents

- [Operations index](../README.md)
- [OpenTofu implementation](../../../infra/09-platform-ops/opentofu/docker-compose.yml)
- [Version projection](../../../infra/tech-stack.versions.json)
