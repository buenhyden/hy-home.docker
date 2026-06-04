<!-- README Target: docs/05.operations/guides/04-data/optimization/README.md -->

# 04-Data Optimization Guides

> 04-data 최적화와 하드닝 사용 가이드를 목적별 하위 폴더에서 관리한다.

## Overview

이 폴더는 `04-data` 계층의 최적화와 하드닝 guide 문서를 보관한다. `guides/04-data` root에는 README만 남기고, 실행 목적이 있는 leaf guide는 이 폴더처럼 명확한 purpose folder 아래에 둔다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- 04-data 최적화/하드닝 사용 맥락과 점검 가이드
- paired policy/runbook으로 이동하기 위한 navigation
- 이 폴더에 속한 guide leaf 인덱스

### Out of Scope

- 운영 통제 기준
- 반복 실행 복구 절차
- secret 값, credential, token, 인증서 원문

## Structure

```text
optimization/
├── optimization-hardening.md
└── README.md
```

## How to Work in This Area

1. 새 guide leaf는 `docs/99.templates/guide.template.md`를 따른다.
2. 문서 이동이나 제목 변경 시 이 README와 `../README.md`를 함께 갱신한다.
3. paired policy와 runbook link를 새 상대 경로 기준으로 검증한다.

## Related Documents

- [04-data guides index](../README.md)
- [Optimization hardening policy](../../../policies/04-data/optimization/optimization-hardening.md)
- [Optimization hardening runbook](../../../runbooks/04-data/optimization/optimization-hardening.md)
