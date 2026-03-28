# Execution Tasks (06.tasks)

> System-wide execution tracking and verification governance layer.

## Overview

이 폴더는 `hy-home.docker` 시스템의 실제 구현 및 검증 작업 단위(Task)를 관리한다. Spec과 Plan에서 파생된 구체적인 코드 작성, 테스트, 평가 작업을 추적 가능하게 기록하며, 실행의 진실 원천(Source of Truth) 역할을 수행한다.

## Audience

이 README의 주요 독자:

- Software Engineers
- Implementation Agents
- QA / Testers
- AI Agents

## Scope

### In Scope

- 기능/작업 흐름별 구현·검증 태스크 목록 (`2026-03-26-01-gateway-tasks.md`)
- Task Table을 통한 진행 상태(Todo, In Progress, Done) 추적
- 작업별 검증 증거(Verification / Evidence) 및 결과 기록
- TDD 기반의 테스트 태스크 및 에이전트 평가 태스크

### Out of Scope

- 상위 수준의 실행 전략 (docs/05.plans 담당)
- 상세 기술 설계 및 데이터 모델링 (docs/04.specs 담당)
- 운영 단계의 일상적 절차 (docs/09.runbooks 담당)

## Structure

```text
06.tasks/
├── 2026-03-26-01-gateway-tasks.md    # Gateway standardization tasks
├── 2026-03-26-02-auth-tasks.md       # Auth standardization tasks
├── 2026-03-26-03-security-tasks.md   # Security standardization tasks
├── 2026-03-26-04-data-tasks.md       # Data standardization tasks
├── 2026-03-26-05-messaging-tasks.md  # Messaging standardization tasks
├── 2026-03-26-06-observability-tasks.md # Observability 문서 표준화 작업 현황
├── 2026-03-26-07-workflow-tasks.md      # Workflow 문서 표준화 작업 현황
├── 2026-03-26-11-laboratory-tasks.md      # Laboratory 문서 표준화 작업 현황
├── 2026-03-27-08-ai-open-webui-tasks.md   # Open WebUI 문서 표준화 작업 현황
├── 2026-03-28-01-gateway-optimization-hardening-tasks.md # 01-gateway 최적화/하드닝 작업 현황
├── 2026-03-28-02-auth-optimization-hardening-tasks.md # 02-auth 최적화/하드닝 작업 현황
├── 2026-03-28-03-security-optimization-hardening-tasks.md # 03-security(Vault) 최적화/하드닝 작업 현황
├── 2026-03-28-04-data-optimization-hardening-tasks.md # 04-data 최적화/하드닝 작업 현황
├── 2026-03-28-05-messaging-optimization-hardening-tasks.md # 05-messaging 최적화/하드닝 작업 현황
├── 2026-03-28-06-observability-optimization-hardening-tasks.md # 06-observability 최적화/하드닝 작업 현황
├── 2026-03-28-07-workflow-optimization-hardening-tasks.md # 07-workflow 최적화/하드닝 작업 현황
└── README.md                          # This file
```

## How to Work in This Area

1. [docs/README.md](../README.md)를 먼저 읽어 전체 문서 체계를 이해한다.
2. 새 작업을 시작할 때는 [task.template.md](../99.templates/task.template.md)를 복제하여 사용한다.
3. 모든 태스크는 상위 Spec과 Plan을 참조하여 추적성을 유지한다.
4. 작업 완료 후에는 반드시 `Verification Summary`에 증빙 자료나 커맨드 결과를 기록한다.

## Documentation Standards

이 영역의 문서는 다음 기준을 따라야 한다.

- 모든 태스크는 고유 ID(T-*)를 부여한다.
- 핵심 코드 작업은 TDD(Test-Driven Development) 원칙을 준수한다.
- `Overview (KR)` 섹션을 상단에 배치하여 한국어 요약을 제공한다.

## SSoT References

- [Technical Specs](../04.specs/README.md)
- [Plan Layer](../05.plans/README.md)

---

## AI Agent Guidance

1. 태스크를 생성할 때 실패하는 테스트(Failing Test) 작성을 첫 번째 태스크로 배치한다.
2. 진행 상태를 업데이트할 때마다 `Validation / Evidence` 섹션을 함께 작성한다.
3. 복잡한 작업은 Phase로 나누어 가독성을 높인다.
