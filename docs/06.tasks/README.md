# Implementation Work Units (Tasks)

> 이 경로는 실제 구현 및 검증 작업 단위(Task Table, Evidence)를 관리한다.

## Overview

`docs/06.tasks`는 실행 계획(Plan)에 따라 수행되는 구체적인 작업 단위와 그 결과를 기록한다. 각 태스크의 성패 여부, 증거 자료(Logs, Screenshots), 그리고 발생한 이슈와 해결 과정을 추적한다.

## Audience

이 README의 주요 독자:

- Developers
- QA Engineers
- Product Managers
- AI Agents

## Scope

### In Scope

- 프로젝트별 상세 작업 목록 (Task Table)
- 구현 및 검증 증거 자료 (Evidence)
- 작업 수행 중 발견된 상세 이슈 및 해결 과정 (Issue Tracking)
- 검증 명령어 및 결과 요약 (Validation Summary)

### Out of Scope

- 상위 아키텍처 비전 (ARD 담당)
- 상위 실행 계획 (Plan 담당)
- 기술 스펙 또는 상세 명세 (Spec 담당)
- 중장기 로드맵

## Structure

```text
docs/06.tasks/
├── 2026-03-26-01-gateway-tasks.md
├── 2026-03-26-02-auth-tasks.md
├── 2026-03-26-03-security-tasks.md
├── 2026-03-26-04-data-tasks.md
├── 2026-03-26-05-messaging-tasks.md
├── 2026-03-26-06-observability-tasks.md
├── 2026-03-26-07-workflow-tasks.md
├── 2026-03-26-08-ai-tasks.md
├── 2026-03-26-09-tooling-tasks.md
├── 2026-03-26-10-communication-tasks.md
├── 2026-03-26-11-laboratory-tasks.md
├── 2026-04-01-standardize-infra-net.md  # Latest: infra_net 표준화 작업 기록
└── README.md                               # This file
```

## How to Work in This Area

1. 실제 작업 착수 전 [task.template.md](../99.templates/task.template.md)를 활용하여 작업 목록을 생성함.
2. 각 세부 태스크의 `Status`를 실시간으로 갱신하여 진행 상황을 공유함.
3. 검증 단계에서는 `Validation / Evidence` 항목을 충실히 기입함.
4. 작업 완료 후에는 최종 증거 자료와 함께 상태를 `Done`으로 마무리함.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작한다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.
- 상위 문서와 하위 산출물 간 추적성을 유지한다.

## AI Agent Guidance

1. 이 README를 먼저 읽는다.
2. 실행 시 각 작업 단위의 의존성과 성공 기준을 명확히 이해하고 수행한다.
3. 수행된 모든 작업에 대해 가능한 경우 증거(로그 또는 스크린샷 덤프)를 남긴다.

## Related References

- **Plan**: [../05.plans/README.md]
- **Spec**: [../04.specs/README.md]
- **Runbook**: [../09.runbooks/README.md]
- **Postmortem**: [../11.postmortems/README.md]
