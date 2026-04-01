# Architecture Decision Records (ADR)

> 이 경로는 기술적 의사결정 기록(Decision, Status, Context, Consequence)을 관리한다.

## Overview

`docs/03.adr`은 프로젝트 전반의 아키텍처 및 기술 스택 선택에 대한 결정 과정을 기록한다. 왜 특정 기술을 선택했는지, 어떤 대안이 있었는지, 그리고 그 결정에 따른 결과가 무엇인지 투명하게 공유하여 히스토리 관리를 용이하게 한다.

## Audience

이 README의 주요 독자:

- System Architects
- Developers
- Reviewers
- AI Agents

## Scope

### In Scope

- 주요 프레임워크 및 라이브러리 선정 결정
- 시스템 통신 프로토콜 결정
- 데이터베이스 엔진 및 스키마 설계 원칙
- 네트워크 표준화 정책 결정 (ADR)

### Out of Scope

- 상세 규격서 (Spec 담당)
- 단순한 코드 변경 로그
- 일반적인 가이드 문서
- 일시적인 트러블슈팅 기록

## Structure

```text
docs/03.adr/
├── 2026-03-26-01-gateway-adr.md
├── 2026-03-26-02-auth-adr.md
├── 2026-03-26-03-security-adr.md
├── 2026-03-26-04-data-adr.md
├── 2026-03-26-05-messaging-adr.md
├── 2026-03-26-06-observability-adr.md
├── 2026-03-26-07-workflow-adr.md
├── 2026-03-26-08-ai-adr.md
├── 2026-03-26-09-tooling-adr.md
├── 2026-03-26-10-communication-adr.md
├── 2026-03-26-11-laboratory-adr.md
├── 2026-04-01-standardize-infra-net.md  # Latest: infra_net 표준화 결정 기록
└── README.md                               # This file
```

## How to Work in This Area

1. 기술적 대안 비교 및 결정이 필요할 때 [adr.template.md](../99.templates/adr.template.md)를 활용함.
2. 각 ADR은 하나의 독립된 결정을 다뤄야 함.
3. 문서 상태(`proposed`, `accepted`, `deprecated`, `superseded`)를 명확히 함.
4. 결정된 사항은 `ARD` 또는 `Spec`에 반영하여 정합성을 유지함.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작한다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.
- 상위 문서와 하위 산출물 간 추적성을 유지한다.

## AI Agent Guidance

1. 이 README를 먼저 읽는다.
2. 특정 기술이나 설계를 제안하기 전에 기존 ADR을 검토하여 시스템의 일관성을 저해하는지 확인한다.
3. 결정된 사항에 반하는 변경을 수행하기 전에는 반드시 새로운 ADR 제안이 선행되어야 한다.

## Related References

- **PRD**: [../01.prd/README.md]
- **ARD**: [../02.ard/README.md]
- **Spec**: [../04.specs/README.md]
