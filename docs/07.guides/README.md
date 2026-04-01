# System Guides

> 이 경로는 시스템 가이드(Onboarding, How-to, Style-Guide)를 관리한다.

## Overview

`docs/07.guides`는 프로젝트의 사용자와 관리자가 시스템을 올바르게 이해하고 작업을 수행하는 데 필요한 지침을 제공한다. 단계별 절차와 예제, 모범 사례를 포함하여 지식의 전파를 돕는다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Contributors
- AI Agents

## Scope

### In Scope

- 서비스별 초기 설정 및 온보딩 가이드 (Onboarding)
- 특정 작업 수행을 위한 단계별 매뉴얼 (How-to)
- 코드 스타일 또는 문서 작성 표준 (Style-Guide)
- 일반적인 장애 및 이슈 해결 지침 (Troubleshooting-Guide)
- 네트워크 표준화 구현 가이드 (Guide)

### Out of Scope

- 실시간 장애 복구 절차 (Runbook 담당)
- 공식 운영 정책 (Operations 담당)
- 상세 제품 요구사항 (PRD 담당)
- 시스템 구현 명세 (Spec 담당)

## Structure

```text
docs/07.guides/
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
├── 0012-standardize-infra-net.md  # Latest: infra_net 표준 구현 가이드
└── README.md                       # This file
```

## How to Work in This Area

1. 새로운 가이드 작성 시 [guide.template.md](../99.templates/guide.template.md)를 상속받음.
2. 대상 독자(Audience)를 명확히 정의하고 눈높이에 맞게 서술함.
3. 문서 상태(`draft`, `stable`, `archived`)를 관리함.
4. 예제 코드와 스크린샷 덤프 등 시각적 자료를 충실히 활용함.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작한다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.
- 상위 문서와 하위 산출물 간 추적성을 유지한다.

## AI Agent Guidance

1. 이 README를 먼저 읽는다.
2. 특정 작업을 요청받았을 때, 이 가이드 문서를 먼저 검색하여 표준화된 절차를 따른다.
3. 가이드 문서의 절차가 최신 상태가 아니라고 판단될 경우 즉시 갱신을 제안한다.

## Related References

- **Spec**: [../04.specs/README.md]
- **Operation**: [../08.operations/README.md]
- **Runbook**: [../09.runbooks/README.md]
