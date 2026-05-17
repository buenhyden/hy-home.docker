# Glossary References

> reference stage의 stable vocabulary와 문서 경계 용어를 관리하는 category

## Overview

`docs/90.references/glossary`는 여러 stage 문서가 반복해서 사용하는 용어를 안정적으로 설명합니다. 이 폴더는 정책 원문이나 실행 절차가 아니라, 문서 작성자와 AI Agent가 같은 단어를 같은 의미로 해석하도록 돕는 reference 공간입니다.

## Category Role

`docs/90.references/glossary`는 `docs/90.references`의 stage boundary와 source 해석 용어를 설명합니다. 실제 정책은 `docs/00.agent-governance/`, 운영 절차는 `docs/05.operations/`, runtime truth는 `infra/`, `scripts/`, registry 파일이 담당합니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 문서 stage와 reference boundary에서 반복해서 쓰는 용어
- stable context, runtime truth, source-backed reference 같은 해석 용어
- Graphify와 generated index 같은 advisory evidence의 경계

### Out of Scope

- active policy 본문
- 운영 runbook 또는 incident timeline
- Docker Compose runtime 설정 원문
- secret 값, credential, token

## Structure

```text
docs/90.references/glossary/
├── README.md                  # This file
└── stable-reference-terms.md  # Reference-stage boundary terms
```

## Current References

- [stable-reference-terms.md](./stable-reference-terms.md) - shared terms for reference-stage boundaries

## How to Work in This Area

1. 용어가 여러 stage 문서에서 반복되는지 먼저 확인합니다.
2. active policy나 절차가 필요하면 glossary가 아니라 canonical stage 문서로 연결합니다.
3. 새 non-README reference는 [reference.template.md](../../99.templates/reference.template.md)를 기준으로 작성합니다.
4. 새 glossary 문서를 추가하면 이 README와 [90.references](../README.md)를 함께 갱신합니다.
5. 변경 후 `bash scripts/validation/check-repo-contracts.sh`를 실행합니다.

## Related Documents

- [90.references](../README.md)
- [stable reference terms](./stable-reference-terms.md)
- [docs index](../../README.md)
- [reference template](../../99.templates/reference.template.md)
- [documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
