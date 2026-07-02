<!-- README Target: docs/05.operations/policies/04-data/optimization/README.md -->

# 04-Data Optimization Policies

> 04-data 최적화와 하드닝 통제 기준을 목적별 하위 폴더에서 관리한다.

## Overview

이 폴더는 `04-data` 계층의 optimization/hardening policy 문서를 보관한다. `04-data` root에는 README와 하위 purpose folder만 두고, leaf policy는 이 폴더 아래에서 paired guide/runbook과 연결한다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- 04-data 최적화/하드닝 required, allowed, disallowed controls
- 검증 기준과 review cadence
- paired guide/runbook으로 이동하기 위한 navigation

### Out of Scope

- 사용 가이드 본문
- 반복 실행 복구 절차
- secret 값, credential, token, 인증서 원문

## Structure

```text
optimization/
├── optimization-hardening.md
└── README.md
```

## How to Work in This Area

1. 새 policy leaf는 `docs/99.templates/templates/operations/policy.template.md`를 따른다.
2. 문서 이동이나 제목 변경 시 이 README와 `../README.md`를 함께 갱신한다.
3. paired guide/runbook link를 새 상대 경로 기준으로 검증한다.

## Related Documents

- [04-data policies index](../README.md)
- [Optimization hardening guide](../../../guides/04-data/optimization/optimization-hardening.md)
- [Optimization hardening runbook](../../../runbooks/04-data/optimization/optimization-hardening.md)
