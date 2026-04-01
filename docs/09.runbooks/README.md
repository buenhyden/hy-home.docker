# System Runbooks

> 이 경로는 반복적 운영 작업의 실행 지침(Step-by-step Procedures)을 관리한다.

## Overview

`docs/09.runbooks`는 시스템 장애 복구, 정기 점검, 리소스 확장 등 즉각적으로 실행해야 하는 운영 절차를 보관한다. 운영자가 깊은 고민 없이도 런북의 단계를 따라함으로써 안전하고 신속하게 목표를 달성이 가능하도록 설계되었다.

## Audience

이 README의 주요 독자:

- Operators
- Developers (On-call)
- SREs
- AI Agents

## Scope

### In Scope

- 서비스 자립성 보장을 위한 복구 절차 (Recovery)
- 백업 및 복원 단계별 시나리오 (Checklist)
- 특정 작업 자동화 스크립트 실행 가이드
- 네트워크 IP 할당 검증 및 업데이트 (Runbook)

### Out of Scope

- 운영 정책 정의 (Operations 담당)
- 새로운 아키텍처 제안 (ADR 담당)
- 중장기 작업 계획 (Plan 담당)
- 사고 사후 분석 (Postmortem 담당)

## Structure

```text
docs/09.runbooks/
├── 01-gateway/
├── 02-auth/
├── 03-security/
├── 04-data/
├── 05-messaging/
├── 06-observability/
├── 07-workflow/
├── 08-ai/
├── 09-tooling/
├── 10-communication/
├── 11-laboratory/
├── 0012-standardize-infra-net.md  # Latest: infra_net IP 할당 검증 런북
└── README.md                       # This file
```

## How to Work in This Area

1. 새로운 운영 절차 작성 시 [runbook.template.md](../99.templates/runbook.template.md)를 활용함.
2. 실행 전 체크리스트(Checklist)와 세부 절차(Procedure)를 명확히 구분함.
3. 문서 상태(`draft`, `verified`, `deprecated`)를 관리함.
4. 모든 명령어는 실제 환경에서 검증된 후에 기록해야 함.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작한다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.
- 상위 문서와 하위 산출물 간 추적성을 유지한다.

## AI Agent Guidance

1. 이 README를 먼저 읽는다.
2. 긴급 상황 발생 시 이 영역의 런북을 먼저 검색하여 검증된 복구 절차를 따른다.
3. 런북의 명령어가 실패하거나 기대와 다를 경우 즉시 기록하고 보완을 시도한다.

## Related References

- **ARD**: [../02.ard/README.md]
- **ADR**: [../03.adr/README.md]
- **Spec**: [../04.specs/README.md]
- **Operation**: [../08.operations/README.md]
- **Incident**: [../10.incidents/README.md]
