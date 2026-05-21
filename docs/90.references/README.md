<!-- Target: docs/90.references/README.md -->
# 90.references

> 느리게 변하는 기준 지식, 표준, 인벤토리, 용어, 학습 로드맵을 관리하는 reference stage

## Overview

`docs/90.references`는 active stage 문서를 보조하는 안정적인 참고 지식 공간입니다. 이 stage는 요구사항, 아키텍처, 명세, 실행 계획, 운영 문서가 반복해서 참조하는 배경 지식과 기준 정보를 관리합니다.

Reference 문서는 결정을 내리거나 절차를 실행하는 문서가 아닙니다. 정책은 `docs/00.agent-governance/` 또는 `docs/05.operations/policies/`, 실행 절차는 `docs/05.operations/runbooks/`, 최신 runtime truth는 `infra/`, `scripts/`, registry 파일이 담당합니다.

## Repository Role

`docs/90.references`의 역할은 다음 세 가지입니다.

1. **Stable Context Registry**: 여러 active stage 문서가 반복해서 참조하는 느리게 변하는 배경 지식과 용어를 보관합니다.
2. **Source-Backed Reference Index**: 외부 표준, 논문, 책, repo-local canonical 파일이 어떤 사실을 뒷받침하는지 짧게 연결합니다.
3. **Routing Guard**: 요구사항, 설계 결정, 실행 계획, 운영 절차, incident 기록으로 가야 할 내용을 reference stage에 섞지 않도록 분리 기준을 제공합니다.

이 stage는 active decision authority가 아닙니다. 최신 정책, 실행 명령, 운영 절차, runtime 설정 원문은 해당 canonical stage 또는 runtime 파일에서만 관리합니다.

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
├── glossary/     # Stable reference terms and stage-boundary vocabulary
├── kubernetes/   # Kubernetes and k3s/k3d migration reference context
├── learning/     # CS/CE/SE learning roadmap and theory references
├── llm-wiki/     # repo-local LLM navigation map, generated index, and entrypoint reference
└── README.md     # This file
```

## Required Format

Reference 문서는 다음 조건을 만족해야 합니다.

- `docs/99.templates/reference.template.md`의 필수 섹션을 따른다.
- `status`, `Overview (KR)`, `Purpose`, `Repository Role`, `Scope`, `Definitions / Facts`, `Source Rules`, `Sources`, `Maintenance`, `Related Documents`를 포함한다.
- 제목은 `# Reference: <item name>` 형식을 사용한다.
- source가 외부 문서라면 링크와 함께 어떤 사실을 가져왔는지 요약한다.
- source가 repo-local 파일이라면 상대 경로를 사용한다.
- active policy나 runbook을 대체하는 문장을 쓰지 않는다.
- 민감값, token, credential, private key, shell history, raw secret log를 쓰지 않는다.

README 파일은 `docs/99.templates/readme.template.md`의 기본 구조를 따르고, 하위 reference 문서를 찾기 위한 index 역할을 합니다.

## Naming and Lifecycle Rules

- Category folder는 `docs/90.references/{category}/` 형태의 lower-kebab-case를 사용한다.
- Non-README 문서는 `docs/90.references/{category}/{item}.md`에 둔다.
- `status`는 `draft`, `active`, `archived` 중 하나를 사용한다.
- Archived reference는 현재 판단 기준이 아니라 history/context 보존용으로만 둔다.
- 새 category나 reference를 추가하면 이 README와 category README를 함께 갱신한다.
- Redirect 파일이나 compatibility shim은 만들지 않는다.

## Placement Rules

| Content | Correct Location |
| --- | --- |
| Stable background or glossary | `docs/90.references/{category}/` |
| Architecture requirement | `docs/02.architecture/requirements/` |
| Architecture decision | `docs/02.architecture/decisions/` |
| Technical implementation contract | `docs/03.specs/` |
| Implementation plan or evidence | `docs/04.execution/` |
| Operational policy, guide, or runbook | `docs/05.operations/` |
| Incident record or postmortem | `docs/05.operations/incidents/` |

## Current References

- [docker/README.md](./docker/README.md) - Docker image/version drift, registry, and runtime reference rules
- [docker/image-version-interpretation.md](./docker/image-version-interpretation.md) - Docker image/version source interpretation rules
- [glossary/README.md](./glossary/README.md) - stable reference terminology category
- [glossary/stable-reference-terms.md](./glossary/stable-reference-terms.md) - shared terms for reference-stage boundaries
- [kubernetes/README.md](./kubernetes/README.md) - Kubernetes and k3s/k3d migration reference context
- [kubernetes/docker-compose-to-k3s-migration.md](./kubernetes/docker-compose-to-k3s-migration.md) - Docker Compose to k3s/k3d migration suitability snapshot
- [learning/README.md](./learning/README.md) - Docker-based infrastructure learning roadmap and theory references
- [llm-wiki/README.md](./llm-wiki/README.md) - repo-local LLM Wiki entrypoint and tracked-source repository map
- [llm-wiki/index.md](./llm-wiki/index.md) - generated tracked repo-local path index

## How to Work in This Area

1. Confirm the content is stable reference material, not active policy or procedure.
2. Start new non-README reference docs from [reference.template.md](../99.templates/reference.template.md).
3. Link to authoritative sources and related active-stage documents.
4. Update this README and the category README when adding, moving, or deleting reference docs.
5. Run `bash scripts/validation/check-repo-contracts.sh` after changing reference docs or templates.

## Related Documents

- [docs index](../README.md)
- [glossary references](./glossary/README.md)
- [reference template](../99.templates/reference.template.md)
- [README template](../99.templates/readme.template.md)
- [documentation protocol](../00.agent-governance/rules/documentation-protocol.md)
- [stage authoring matrix](../00.agent-governance/rules/stage-authoring-matrix.md)
