# Execution

> 실행 계획과 작업 증거를 함께 라우팅하는 문서 공간

## Overview

`docs/04.execution`은 승인된 요구사항과 명세를 실제 작업 단위로 전환하는 stage입니다.

계획은 `plans/`에 두고, 구현 및 검증 evidence는 `tasks/`에 둡니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Project Maintainers
- AI Agents

## Scope

### In Scope

- 실행 계획, work breakdown, risk control
- 작업 목록, 검증 evidence, 완료 상태
- docs, governance, infra 변경의 추적성
- 관련 spec과 operations 문서로의 연결

### Out of Scope

- 요구사항 정의 (`docs/01.requirements` 담당)
- 아키텍처 요구사항과 결정 기록 (`docs/02.architecture` 담당)
- 상세 기술 명세 (`docs/03.specs` 담당)
- 운영 가이드, 정책, 런북, 사고 기록 (`docs/05.operations` 담당)

## Structure

```text
docs/04.execution/
├── plans/      # Implementation plans and milestones
├── tasks/      # Task evidence and verification records
└── README.md   # This file
```

## How to Work in This Area

1. 실행 전에는 `plans/`에 작업 순서, 리스크, 검증 기준을 남깁니다.
2. 실행 중에는 `tasks/`에 실제 작업, 증거, 검증 결과를 기록합니다.
3. 새 문서는 `../99.templates/plan.template.md` 또는 `../99.templates/task.template.md`를 사용합니다.
4. 관련 spec, operations, README 링크를 함께 갱신합니다.

## Related Documents

- **Requirements**: [../01.requirements/README.md](../01.requirements/README.md)
- **Architecture**: [../02.architecture/README.md](../02.architecture/README.md)
- **Specs**: [../03.specs/README.md](../03.specs/README.md)
- **Plans**: [plans/README.md](plans/README.md)
- **Tasks**: [tasks/README.md](tasks/README.md)
- **Operations**: [../05.operations/README.md](../05.operations/README.md)
