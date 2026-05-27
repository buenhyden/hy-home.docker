<!-- Target: docs/03.specs/workspace-audit-2026-05/README.md -->

# workspace-audit-2026-05 Specifications

> 2026년 5월 워크스페이스 전체 감사 및 개선 세션 기술 명세

## Overview

`docs/03.specs/workspace-audit-2026-05`는 2026-05 워크스페이스 감사 세션의 범위, 경계, 계약을 정의하는 기술 사양을 포함합니다. 거버넌스 규칙, 문서 라이프사이클, 스크립트, Docker Compose 인프라, env/secrets 계약을 대상으로 저위험 변경을 구현하고 중/고위험 항목은 deferred로 기록합니다.

## Audience

이 README의 주요 독자:

- Developers
- System Architects
- AI Agents

## Scope

### In Scope

- 2026-05 감사 세션 기술 계약 및 구현 경계
- 저위험 변경 대상과 deferred 항목 명세

### Out of Scope

- 운영 절차 (`docs/05.operations/` 담당)
- 구현 실행 계획 (`docs/04.execution/plans/` 담당)

## Structure

```text
workspace-audit-2026-05/
├── spec.md      # Workspace audit 2026-05 technical specification
└── README.md    # This file
```

## How to Work in This Area

1. 구현 또는 검증 전 [spec.md](./spec.md)를 먼저 확인합니다.
2. 상위 요구사항 맥락은 Related Documents의 PRD 링크에서 추적합니다.
3. 운영 절차, 정책, runbook 내용은 `docs/05.operations/`에 두고 여기에는 구현 계약만 유지합니다.

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
