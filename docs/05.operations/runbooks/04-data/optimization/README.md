<!-- README Target: docs/05.operations/runbooks/04-data/optimization/README.md -->

# 04-Data Optimization Runbooks

> 04-data 최적화와 하드닝 복구 절차를 목적별 하위 폴더에서 관리한다.

## Overview

이 폴더는 `04-data` 계층의 optimization/hardening runbook 문서를 보관한다. 데이터 tier root의 파일/폴더 혼재를 막고, leaf runbook은 paired guide/policy와 같은 purpose folder 이름으로 정리한다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- 04-data 하드닝 회귀 대응 절차
- evidence capture, verification, escalation 기준
- paired guide/policy로 이동하기 위한 navigation

### Out of Scope

- 사용 온보딩
- 장기 운영 통제 정책
- secret 값, credential, token, 인증서 원문

## Structure

```text
optimization/
├── optimization-hardening.md
└── README.md
```

## How to Work in This Area

1. 새 runbook leaf는 `docs/99.templates/runbook.template.md`를 따른다.
2. 문서 이동이나 제목 변경 시 이 README와 `../README.md`를 함께 갱신한다.
3. rollback/recovery 절차가 검증되지 않았으면 N/A와 escalation 기준을 명시한다.

## Related Documents

- [04-data runbooks index](../README.md)
- [Optimization hardening guide](../../../guides/04-data/optimization/optimization-hardening.md)
- [Optimization hardening policy](../../../policies/04-data/optimization/optimization-hardening.md)
