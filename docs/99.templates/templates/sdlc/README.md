---
layer: agentic
---

# SDLC Templates

## Overview

`docs/99.templates/templates/sdlc`는 제품 요구사항부터 실행 증거까지의
SDLC 문서를 위한 복사 가능한 원본을 안내한다.

## Audience

- Documentation Writers
- AI Agents
- Product and Engineering Leads

## Scope

- Stage 01 PRD 원본
- Stage 02 ARD 및 ADR 원본
- Stage 03 parent Spec 원본
- Stage 04 Plan 및 Task 원본

## Structure

| Role | Template |
| --- | --- |
| PRD | [prd.template.md](./prd.template.md) |
| ARD | [ard.template.md](./ard.template.md) |
| ADR | [adr.template.md](./adr.template.md) |
| Spec | [spec.template.md](./spec.template.md) |
| Plan | [plan.template.md](./plan.template.md) |
| Task | [task.template.md](./task.template.md) |

## How to Work in This Area

1. [template selection](../../support/template-selection.md)에서 목적과 대상 경로에 맞는 원본을 찾는다.
2. 선택한 원본의 모든 토큰을 실제 근거가 있는 내용으로 바꾼다.
3. 별도 검토가 필요한 Stage 03 계약은 [Spec contract catalog](../spec-contracts/README.md)에서 찾는다.
4. 일반 작업과 harness 작업은 모두 하나의 Task 원본에 기록하고, 적용되는 승인·검증 증거만 채운다.
5. 변경 후 [template contract](../../support/template-contract.md)와 저장소 검증을 확인한다.

## Related Documents

- [templates catalog](../README.md)
- [Spec contract catalog](../spec-contracts/README.md)
- [template selection](../../support/template-selection.md)
- [SDLC document contract](../../support/sdlc-document-contract.md)
