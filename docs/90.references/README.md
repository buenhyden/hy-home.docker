# 90.references

> 느리게 변하는 기준 지식, 표준, 인벤토리, 용어, 학습 로드맵을 관리하는 reference stage

## Overview

`docs/90.references`는 active stage 문서를 보조하는 안정적인 참고 지식 공간입니다. 이 stage는 요구사항, 아키텍처, 명세, 실행 계획, 운영 문서가 반복해서 참조하는 배경 지식과 기준 정보를 관리합니다.

Reference 문서는 결정을 내리거나 절차를 실행하는 문서가 아닙니다. 정책은 `docs/00.agent-governance/` 또는 `docs/05.operations/policies/`, 실행 절차는 `docs/05.operations/runbooks/`, 최신 runtime truth는 `infra/`, `scripts/`, registry 파일이 담당합니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 느리게 변하는 개념, 표준, glossary, FAQ
- 외부 표준이나 논문에 대한 짧은 요약과 source links
- repo-local inventory 또는 version-drift 설명 문서
- 학습 로드맵과 이론 배경
- active stage 문서가 반복해서 참조하는 stable context

### Out of Scope

- 현재 진행 중인 요구사항, 설계 결정, 실행 계획, task evidence
- 운영 정책, runbook, incident timeline, postmortem
- 최신 runtime 설정 원문, Compose 파일의 대체본, secret 값
- 빠르게 변하는 외부 뉴스, 가격, 릴리스 상태의 무검증 복사본

## Structure

```text
docs/90.references/
├── docker/       # Docker image/version drift, registry, runtime reference rules
├── learning/     # CS/CE/SE learning roadmap and theory references
└── README.md     # This file
```

## Authoring Contract

Reference 문서는 다음 조건을 만족해야 합니다.

- `docs/99.templates/reference.template.md`의 필수 섹션을 따른다.
- `status`, `Overview (KR)`, `Purpose`, `Scope`, `Definitions / Facts`, `Sources`, `Maintenance`, `Related Documents`를 포함한다.
- source가 외부 문서라면 링크와 함께 어떤 사실을 가져왔는지 요약한다.
- source가 repo-local 파일이라면 상대 경로를 사용한다.
- active policy나 runbook을 대체하는 문장을 쓰지 않는다.
- 민감값, token, credential, private key, shell history, raw secret log를 쓰지 않는다.

README 파일은 `docs/99.templates/readme.template.md`의 기본 구조를 따르고, 하위 reference 문서를 찾기 위한 index 역할을 합니다.

## Placement Rules

| Content | Correct Location |
| --- | --- |
| Stable background or glossary | `docs/90.references/<category>/` |
| Architecture requirement | `docs/02.architecture/requirements/` |
| Architecture decision | `docs/02.architecture/decisions/` |
| Technical implementation contract | `docs/03.specs/` |
| Implementation plan or evidence | `docs/04.execution/` |
| Operational policy, guide, or runbook | `docs/05.operations/` |
| Incident record or postmortem | `docs/05.operations/incidents/` |

## Current References

- [docker/README.md](./docker/README.md) - Docker image/version drift, registry, and runtime reference rules
- [learning/README.md](./learning/README.md) - Docker-based infrastructure learning roadmap and theory references

## How to Work in This Area

1. Confirm the content is stable reference material, not active policy or procedure.
2. Start new non-README reference docs from [reference.template.md](../99.templates/reference.template.md).
3. Link to authoritative sources and related active-stage documents.
4. Update this README and the category README when adding, moving, or deleting reference docs.
5. Run `bash scripts/check-repo-contracts.sh` after changing reference docs or templates.

## Related Documents

- [docs index](../README.md)
- [reference template](../99.templates/reference.template.md)
- [README template](../99.templates/readme.template.md)
- [documentation protocol](../00.agent-governance/rules/documentation-protocol.md)
- [stage authoring matrix](../00.agent-governance/rules/stage-authoring-matrix.md)
