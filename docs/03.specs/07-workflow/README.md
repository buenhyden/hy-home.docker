# 07-workflow Specifications

> 워크플로우 오케스트레이션 서비스 기술 사양

## Overview

`docs/03.specs/07-workflow`는 Airflow 및 n8n 기반 워크플로우 오케스트레이션 서비스의 기술 사양을 포함합니다.

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

## Related Documents

- [spec.md](./spec.md)
- [agent-design.md](./agent-design.md)
- [docs/03.specs/README.md](../README.md)
- [infra/07-workflow/README.md](../../../infra/07-workflow/README.md)
- [docs/05.operations/guides/07-workflow/](../../05.operations/guides/07-workflow/)
