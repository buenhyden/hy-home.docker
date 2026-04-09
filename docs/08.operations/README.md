# Operations Policies

> 이 경로는 시스템 운영 정책 및 거버넌스(Controls, Policy, Monitoring)를 관리한다.

## Overview

`docs/08.operations`는 시스템의 안정적인 운영과 보안을 보장하기 위한 정책 문서를 보관한다. 기술적인 세부 사항보다는 통제 기준, 승인 프로세스, 예외 처리 및 법규 준수 등을 정의한다.

## Audience

이 README의 주요 독자:

- Operators
- Security Officers
- System Architects
- AI Agents

## Scope

### In Scope

- 권한 및 계정 관리 정책
- 자원 할당 및 백업 정책
- 보안 및 암호화 거버넌스
- 네트워크 IP 할당 및 관리 정책 (Operation)

### Out of Scope

- 실시간 장애 복구 단계 (Runbook 담당)
- 일반적인 사용자 사용법 (Guide 담당)
- 상세 설계 명세 (Spec 담당)
- 특정 사고의 사후 분석 (Postmortem 담당)

## Structure

```text
docs/08.operations/
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
├── standardize-infra-net.md  # Latest: infra_net 운영 정책
└── README.md                 # This file
```

## How to Work in This Area

1. 정책 제안 시 [operation.template.md](../99.templates/operation.template.md)를 활용함.
2. 적용 범위(Applies To)와 통제 항목(Controls)을 명확히 정의함.
3. 문서 상태(`proposed`, `enforced`, `archived`)를 관리함.
4. 주기적인 점검(Review Cadence) 주기를 명시하여 실효성을 확보함.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작한다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.
- 상위 문서와 하위 산출물 간 추적성을 유지한다.

## AI Agent Guidance

1. 이 README를 먼저 읽는다.
2. 인프라 변경 시 이 영역의 운영 정책에 위배되지 않는지 사전에 검토한다.
3. 정책 준수 여부를 정기적으로 확인하고 위반 사례가 있을 경우 보고한다.

## Related References

- **ARD**: [../02.ard/README.md]
- **Plan**: [../05.plans/README.md]
- **Runbook**: [../09.runbooks/README.md]
- **Postmortem**: [../11.postmortems/README.md]
