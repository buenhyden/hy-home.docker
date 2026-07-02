---
status: active
---
<!-- Target: docs/90.references/research/README.md -->

# Research References

> 외부 source-backed 조사와 repo-local 분석을 함께 보관하는 reference category

## Overview

`docs/90.references/research`는 active stage 문서를 보조하는 조사형 reference를 관리합니다. 이 폴더의 문서는 외부 표준, 공식 제품 문서, 논문, repo-local canonical 파일을 함께 읽고 느리게 변하는 분석 기준을 제공합니다.

이 category는 정책, 실행 계획, 운영 runbook, task evidence를 대체하지 않습니다. 현재 정책은 `docs/00.agent-governance/`와 `docs/05.operations/policies/`, 실행 계획과 evidence는 `docs/04.execution/`, runtime truth는 `infra/`, `scripts/`, provider runtime surface가 담당합니다.

## Category Role

`docs/90.references/research`는 source-backed research pack을 위한 reference category입니다. 외부 자료와 repo-local evidence를 함께 분석하지만, active stage의 승인된 요구사항, 결정, 계획, 운영 절차, runtime 설정 원문을 대신하지 않습니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 외부 공식 문서와 repo-local evidence를 함께 분석한 reference pack
- 하네스 엔지니어링, 루프 엔지니어링, SDLC, QA, CI/CD, formatting 같은 cross-cutting research
- active stage 문서가 반복해서 참조할 수 있는 source-backed facts
- 다른 stage에서 후속 보완이 필요한 gap 기록

### Out of Scope

- active policy 본문
- implementation plan 또는 task evidence
- 운영 runbook 절차
- 최신 runtime 설정 원문
- secret 값, credential, token, private key, shell history, raw log

## Structure

```text
research/
├── README.md              # This file
└── agentic-engineering/   # Harness, loop, provider, SDLC, QA research pack
```

## Current References

- [agentic-engineering/README.md](./agentic-engineering/README.md) - 하네스/루프/agent-first engineering research pack index

## How to Work in This Area

1. 새 research 문서가 active decision, policy, plan, runbook을 대체하지 않는지 확인합니다.
2. 새 non-README reference는 [reference.template.md](../../99.templates/templates/common/reference.template.md)의 필수 섹션을 따릅니다.
3. 새 non-README reference는 closed-surface contract에 맞춰 영어로 작성합니다.
4. 외부 자료는 공식 vendor docs, 표준 기관 문서, 원 논문, 공식 repository를 우선합니다.
5. source가 빠르게 변하는 제품 문서이면 문서 안에 재검증 필요성을 명시합니다.
6. 새 category나 pack을 추가하면 이 README와 [90.references](../README.md)를 함께 갱신합니다.
7. 변경 후 `bash scripts/validation/check-repo-contracts.sh`를 실행합니다.

## Related Documents

- [90.references](../README.md)
- [docs index](../../README.md)
- [reference template](../../99.templates/templates/common/reference.template.md)
- [documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
