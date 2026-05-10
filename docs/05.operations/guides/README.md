# Operations Guides

> 서비스 사용, 설정, 온보딩 문서를 tier/service 구조로 관리한다.

## Overview

`docs/05.operations/guides`는 운영자가 서비스를 이해하고 안전하게 사용할 수 있도록 배경, 구성, 일반 절차를 설명하는 공간입니다.

## Scope

### In Scope

- 서비스별 사용 가이드
- 설정 및 온보딩 절차
- operator-facing background

### Out of Scope

- 승인 기준과 통제 정책 (`../policies/` 담당)
- 장애 복구와 반복 실행 절차 (`../runbooks/` 담당)
- 사고 기록 (`../incidents/` 담당)

## Structure

```text
guides/
├── harness-agent-first-engineering.md
├── 01-gateway/
├── 02-auth/
├── ...
└── README.md
```

## Current Governance Guides

- [Harness / Agent-first Engineering Usage Guide](./harness-agent-first-engineering.md)

## Related References

- [../README.md](../README.md)
- [../policies/README.md](../policies/README.md)
- [../runbooks/README.md](../runbooks/README.md)
