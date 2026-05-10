# Operations

> 서비스 사용 가이드, 운영 정책, 반복 실행 절차, 사고 기록을 분리해 관리하는 운영 지식 베이스

## Overview

`docs/05.operations`는 운영자가 서비스를 이해하고, 통제 기준을 확인하고, 복구 절차를 실행하고, 사고 기록을 남기기 위한 canonical operations stage입니다.

이 경로는 하나의 긴 operations 문서로 guide, policy, runbook을 섞지 않습니다. 목적별 하위 폴더를 사용해 사람과 AI Agent가 필요한 문서를 빠르게 찾도록 합니다.

## Audience

이 README의 주요 독자:

- Operators
- Developers
- SREs
- Security Officers
- AI Agents

## Scope

### In Scope

- 서비스 사용, 설정, 온보딩 가이드
- 운영 정책, 통제 기준, 예외 처리 기준
- 장애 복구, 정기 점검, 반복 실행 절차
- 사고 기록과 사후 분석
- AI Agent가 참조할 canonical operations context

### Out of Scope

- 요구사항 정의 (`docs/01.requirements` 담당)
- 아키텍처 요구사항과 결정 기록 (`docs/02.architecture` 담당)
- 상세 기술 명세 (`docs/03.specs` 담당)
- 실행 계획과 작업 증거 (`docs/04.execution` 담당)

## Structure

```text
docs/05.operations/
├── guides/       # 서비스 사용, 설정, 온보딩 가이드
├── policies/     # 운영 통제, 보안/가용성 정책, 예외 기준
├── runbooks/     # 복구, 검증, 반복 실행 절차
├── incidents/    # 사고 기록, postmortem, 재발 방지 대책
└── README.md     # This file
```

## How to Work in This Area

1. 서비스 사용법이나 배경 설명은 `guides/<tier>/<service>.md`에 둡니다.
2. 운영 통제, 예외, 보안/가용성 기준은 `policies/<tier>/<topic>.md`에 둡니다.
3. 명령 순서, 기대 결과, 실패 시 중단 기준이 있는 절차는 `runbooks/<tier>/<topic>.md`에 둡니다.
4. 실제 사고 기록과 postmortem은 `incidents/`에 둡니다.
5. 새 operations 문서는 `../99.templates/operation.template.md`를 기본 템플릿으로 사용합니다.

모든 서비스가 guide, policy, runbook을 모두 가질 필요는 없습니다. 소비자가 실제로 구분해서 찾아야 하는 문서만 추가합니다.

## Documentation Standards

- operations 하위 문서는 목적별 폴더를 기준으로 배치합니다.
- 서비스 README는 `infra/...` 원본 구성과 `docs/05.operations/...` 문서를 연결하는 launchpad 역할을 합니다.
- 반복 실행 절차에는 명령, 기대 결과, 실패 시 중단 기준, rollback 또는 escalation 기준을 포함합니다.
- 사고 기록은 secret, token, credential, private key 원문을 포함하지 않습니다.

## Related References

- **Docs Index**: [../README.md](../README.md)
- **Plans**: [../04.execution/plans/README.md](../04.execution/plans/README.md)
- **Tasks**: [../04.execution/tasks/README.md](../04.execution/tasks/README.md)
- **Templates**: [../99.templates/README.md](../99.templates/README.md)
