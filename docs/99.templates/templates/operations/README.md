---
layer: agentic
---

# Operations Templates

## Overview

이 디렉터리는 Stage 05의 사용 안내, 운영 통제, 실행 절차, 사고 대응,
회고, 실제 릴리스 증거를 위한 복사 가능 양식을 제공한다. 역할과 경로
선택 규칙은 이 카탈로그가 아니라 Stage 99 support가 소유한다.

## Audience

- Documentation Writers
- Operations/SRE Engineers
- Incident Responders
- Release Owners
- AI Agents

## Scope

이 카탈로그는 여섯 Operations 양식의 위치와 역할만 안내한다. 메타데이터,
선택, lifecycle, 승인, 이관 및 검증 규칙은 support 문서를 따른다.

## Structure

| 역할 | 양식 |
| --- | --- |
| 일상 사용 맥락과 공통 점검 | [guide.template.md](./guide.template.md) |
| 필수·금지 통제와 예외 | [policy.template.md](./policy.template.md) |
| 순서화된 절차, 증거, 복구, escalation | [runbook.template.md](./runbook.template.md) |
| 사고 영향, 시간선, 대응 상태 | [incident.template.md](./incident.template.md) |
| 원인, 교훈, 재발 방지 조치 | [postmortem.template.md](./postmortem.template.md) |
| 실제 릴리스 산출물과 결과 증거 | [release.template.md](./release.template.md) |

## How to Work in This Area

1. [template selection](../../support/template-selection.md)에서 문서 목적과
   대상 경로를 확인한다.
2. 해당 양식을 복사하고 모든 토큰을 주제별 근거로 교체한다.
3. [template contract](../../support/template-contract.md)와 활성 Stage 04
   Task에 검증 및 검토 증거를 기록한다.

## Related Documents

- [templates catalog](../README.md)
- [template selection](../../support/template-selection.md)
- [template contract](../../support/template-contract.md)
- [SDLC document contract](../../support/sdlc-document-contract.md)
- [template governance](../../support/template-governance.md)
