# Architecture

> 아키텍처 요구사항과 기술 결정 기록을 함께 라우팅하는 상위 문서 공간

## Overview

`docs/02.architecture`는 시스템 구조를 설명하는 아키텍처 요구사항과, 선택의 배경을 남기는 결정 기록을 함께 묶는 상위 경로입니다.

요구사항 성격의 아키텍처 문서는 `requirements/`에 두고, 결정 기록은 `decisions/`에 둡니다.

## Audience

이 README의 주요 독자:

- System Architects
- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 아키텍처 요구사항과 품질 속성 정의
- 시스템 경계, 데이터 흐름, 통합 구조
- 기술 선택과 결정 기록
- 관련 spec, plan, operations 문서로의 추적성

### Out of Scope

- 제품 요구사항 정의 (`docs/01.requirements` 담당)
- 상세 기술 명세 (`docs/03.specs` 담당)
- 실행 계획과 작업 증거 (`docs/04.execution` 담당)
- 운영 절차 (`docs/05.operations` 담당)

## Structure

```text
docs/02.architecture/
├── requirements/  # Architecture requirements and reference models
├── decisions/     # Architecture decision records
└── README.md      # This file
```

## How to Work in This Area

1. 새 아키텍처 요구사항은 `requirements/`에 작성합니다.
2. 변경할 수 없는 선택이나 주요 tradeoff는 `decisions/`에 ADR로 기록합니다.
3. 새 문서는 `../99.templates/ard.template.md` 또는 `../99.templates/adr.template.md`를 사용합니다.
4. 관련 requirements, specs, plans, operations 링크를 함께 갱신합니다.

## Related References

- **Requirements**: [../01.requirements/README.md](../01.requirements/README.md)
- **Architecture Requirements**: [requirements/README.md](requirements/README.md)
- **Architecture Decisions**: [decisions/README.md](decisions/README.md)
- **Specs**: [../03.specs/README.md](../03.specs/README.md)
- **Execution**: [../04.execution/README.md](../04.execution/README.md)
