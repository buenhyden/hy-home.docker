<!-- Target: docs/03.specs/008-workflow/README.md -->

# 07-workflow Specifications

> 워크플로우 오케스트레이션 서비스 기술 사양

## Overview

`docs/03.specs/008-workflow`는 Airflow 및 n8n 기반 워크플로우 오케스트레이션 서비스의 기술 사양을 포함합니다.

## Audience

이 README의 주요 독자:

- Developers
- System Architects
- QA Engineers
- AI Agents

## Scope

### In Scope

- DAG 구조, 태스크 실행 모델, 에이전트 연동 인터페이스 사양
- 시크릿 주입 및 외부 서비스 연동 경계

### Out of Scope

- 운영 절차 (`docs/05.operations/guides/07-workflow/` 담당)

## Structure

```text
07-workflow/
├── spec.md          # Workflow services technical specification
├── agent-design.md  # Agent integration design
└── README.md        # This file
```

## How to Work in This Area

1. 구현 또는 검증 전 [spec.md](./spec.md)를 먼저 확인합니다.
2. Agent orchestration 변경은 [agent-design.md](./agent-design.md)를 함께 확인합니다.
3. 상위 요구사항과 아키텍처 맥락은 Related Documents의 PRD/ARD/ADR 링크에서 추적합니다.
4. 운영 절차, 정책, runbook 내용은 `docs/05.operations/`에 두고 여기에는 구현 계약만 유지합니다.

## Related Documents

- [spec.md](./spec.md)
- [agent-design.md](./agent-design.md)
- [docs/03.specs/README.md](../README.md)
- [infra/07-workflow/README.md](../../../infra/07-workflow/README.md)
- [docs/05.operations/guides/07-workflow/](../../05.operations/guides/07-workflow/)
