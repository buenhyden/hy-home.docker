# Operations Runbooks

> 복구, 검증, 반복 실행 절차를 명령과 evidence 중심으로 관리한다.

## Overview

`docs/05.operations/runbooks`는 장애 대응, 반복 검증, 변경 실행 절차처럼 순서와 중단 기준이 필요한 문서를 관리합니다.

## Scope

### In Scope

- 장애 복구 절차
- 검증 및 점검 절차
- 반복 실행 명령과 rollback 또는 escalation 기준

### Out of Scope

- 일반 사용 가이드 (`../guides/` 담당)
- 정책과 승인 기준 (`../policies/` 담당)
- 사고 기록과 postmortem (`../incidents/` 담당)

## Structure

```text
runbooks/
├── 04-data/
├── 06-observability/
├── ...
└── README.md
```

## Related References

- [../README.md](../README.md)
- [../guides/README.md](../guides/README.md)
- [../policies/README.md](../policies/README.md)
