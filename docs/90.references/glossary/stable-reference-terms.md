---
status: active
---
<!-- Target: docs/90.references/glossary/stable-reference-terms.md -->

# Reference: Stable Reference Terms

## Overview (KR)

이 문서는 `docs/90.references`와 문서 governance에서 반복해서 쓰는 stable reference 용어를 정리한다. 용어의 의미를 맞추기 위한 reference이며, active policy를 새로 정의하지 않는다.

## Purpose

문서 작성자와 AI Agent가 reference stage, runtime truth, generated evidence의 경계를 같은 방식으로 해석하도록 돕는다.

## Repository Role

이 reference는 문서 stage 간 역할 구분을 설명하는 shared vocabulary다. 정책의 source of truth는 `docs/00.agent-governance/`, 운영 절차의 source of truth는 `docs/05.operations/`, runtime 구성의 source of truth는 `infra/`, `scripts/`, registry 파일이다.

## Scope

### In Scope

- reference stage에서 반복되는 용어 정의
- source-backed reference와 runtime truth의 구분
- advisory graph context와 generated index의 사용 경계

### Out of Scope

- active governance policy 개정
- 운영 절차나 runbook steps
- implementation plan 또는 task evidence
- secret 값, credential, token

## Definitions / Facts

- **Stable reference**: 느리게 변하는 배경 지식, 표준, 용어, source-backed fact를 담는 문서다. 요구사항, 결정, 실행 계획, 운영 절차를 대체하지 않는다.
- **Stable context**: 여러 active stage 문서가 반복해서 참조할 수 있는 배경 정보다. 현재 실행 상태보다 변경 속도가 느려야 한다.
- **Source-backed reference**: repo-local canonical 파일이나 외부 primary source가 어떤 사실을 뒷받침하는지 짧게 연결한 reference다.
- **Runtime truth**: 현재 실행 설정이나 검증 기준을 직접 정의하는 source다. 이 저장소에서는 주로 `infra/`, `scripts/`, registry JSON 파일, Docker Compose 파일, `docs/00.agent-governance/`가 해당한다.
- **Active stage document**: 요구사항, 아키텍처, 명세, 실행, 운영, incident처럼 현재 작업과 판단을 직접 이끄는 문서다.
- **Advisory graph context**: Graphify 산출물처럼 탐색을 돕지만 canonical evidence로 승격하지 않는 보조 자료다.
- **Generated tracked index**: script로 갱신되는 tracked Markdown index다. 수동 편집보다 generator와 freshness check를 우선한다.

## Source Rules

- 용어가 active policy를 바꾸는 순간 이 문서가 아니라 governance rule이나 scope 문서를 수정한다.
- 운영 절차가 필요하면 `docs/05.operations/`로 연결한다.
- runtime 값이나 current config는 `infra/`, `scripts/`, registry 파일로 연결하고 본문에 복제하지 않는다.
- Graphify, generated index, validator output은 navigation/evidence로만 사용하고 canonical source와 함께 확인한다.

## Sources

- [documentation protocol](../../00.agent-governance/rules/documentation-protocol.md) - documentation stage boundaries and DOCS 3 rules
- [stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md) - stage roles and template mapping
- [90.references](../README.md) - reference stage purpose and lifecycle
- [LLM Wiki repository map](../llm-wiki/repository-map.md) - tracked-source boundary and Graphify advisory rules

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when documentation governance, stage taxonomy, or generated evidence boundaries change
- **Update Trigger**: Update when a repeated term causes ambiguity across stage docs

## Related Documents

- [Glossary references](./README.md)
- [90.references](../README.md)
- [docs index](../../README.md)
- [documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
