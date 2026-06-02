---
layer: agentic
---

# 99.templates

> stage 문서와 README 작성을 위한 공식 템플릿 원천

## Overview

이 폴더는 문서 템플릿을 저장합니다. 새 stage 문서와 folder README는 이 폴더의 대응 템플릿을 복사해 시작합니다.

## Audience

이 README의 주요 독자:

- Documentation Writers
- AI Agents
- Repository Maintainers

## Scope

### In Scope

- `docs/01`부터 `docs/05`, `docs/90`, `docs/98` stage 문서 템플릿
- `docs/00.agent-governance/memory/`의 memory note와 progress log 템플릿
- `docs/03.specs/<feature-id>/`에서 사용하는 보조 계약 템플릿
- repository-wide README 템플릿
- 템플릿과 stage folder 매핑

### Out of Scope

- 실제 요구사항, 설계, 계획, 작업, 운영, 사고 기록 본문
- 런타임 설정 원문이나 secret 값
- 템플릿을 벗어난 임의 문서 유형

## 템플릿 목록

- `agent-design.template.md`
- `data-model.template.md`
- `service.template.md` — 서비스 런타임 계약 스캐폴드 (03.specs 보조)
- `tests.template.md`
- `openapi.template.yaml`
- `service.template.proto`
- `schema.template.graphql`
- `prd.template.md`
- `ard.template.md`
- `adr.template.md`
- `spec.template.md`
- `api-spec.template.md`
- `plan.template.md`
- `task.template.md` — includes optional approved-surface evidence for high-risk policy/runtime/CI/template/secrets/remote/model/provider work
- `guide.template.md` — 운영 가이드 (단독 프로파일)
- `policy.template.md` — 운영 정책 (단독 프로파일)
- `incident.template.md`
- `postmortem.template.md`
- `runbook.template.md` — 운영 런북 (단독 프로파일)
- `memory.template.md`
- `progress.template.md`
- `reference.template.md`
- `archive.template.md`
- `readme.template.md`

## 사용 원칙

1. 템플릿의 Target 경로를 실제 저장 위치와 맞춘다.
2. Placeholder는 모두 제거한다.
3. 상대 경로만 사용한다.
4. PRD/ARD/ADR/Spec/Plan/Task의 추적성을 유지한다.
5. Agent 기능은 Role, Tool, Guardrail, Eval, Fallback을 빠뜨리지 않는다.
6. `## Related Documents` 예시는 템플릿 파일 위치가 아니라 복사된 대상 파일 위치에서 해석되어야 하며, Markdown 템플릿에서는 가능한 경우 클릭 가능한 Markdown 링크 예시를 사용한다.
7. 운영 문서는 대상 bucket에 맞게 `guide.template.md`, `policy.template.md`, `runbook.template.md` 중 하나를 사용한다.
8. infra service README는 목적, config, compose linkage, network, volume, port, label, secret ref, healthcheck, operations, validation, troubleshooting evidence를 포함한다.
   Folder index README는 service readiness evidence를 억지로 복제하지 않고 하위 문서 routing과 lifecycle만 설명한다.
9. scripts README는 `scripts/validation/`, `scripts/hardening/`, `scripts/hooks/`, `scripts/knowledge/`, `scripts/operations/`, `scripts/lib/` 목적 폴더를 보존하고 root-level wrapper를 만들지 않는다.
10. Markdown 템플릿의 cross-link 예시는 복사된 Target 위치 기준으로 계산하고, YAML/GraphQL/Proto 계약 파일의 cross-link는 parent Markdown Spec 또는 API Spec에서 관리한다.
11. `docs/99.templates/*.template.md` 원본은 `status: draft` frontmatter를 사용한다. 복사된 Target 문서는 대상 stage의 lifecycle에 맞게 `status: draft`, `status: active`, `status: completed`, `status: superseded`, archive tombstone의 `status: archived`, generated metadata, 또는 repository README처럼 no-frontmatter 형태로 조정한다.
12. Template source에 있는 placeholder는 최종 문서에 남기지 않는다. 실제 링크처럼 렌더링되는 placeholder Markdown link와 placeholder command는 target 문서로 복사하기 전에 반드시 삭제하거나 실제 target-relative 값으로 교체한다.
13. README template의 `<!-- Target: ... -->` 주석은 작성 보조 정보다. Target 문서에서 필수 metadata로 취급하지 않으며, 리뷰에 도움이 되는 경우에만 남긴다.
14. Historical evidence 문서는 사실을 재해석하지 않는다. 현재 템플릿 heading과 Related Documents만 최소 보강하고, 검증되지 않은 실행 결과나 원인을 새로 쓰지 않는다.
15. Duplicate 또는 noncanonical 문서는 canonical target, 참조 검색 결과, 보존할 고유 evidence 유무가 확인된 뒤에만 삭제한다. 고유 evidence가 있으면 canonical 문서로 이관하거나 `docs/90.references/`로 이동할 사유를 남긴다.
16. `## Rollback or Recovery`는 factual-only 원칙을 따른다. 검증된 rollback/recovery 단계가 없으면 임의 절차를 만들지 말고, 안전한 `N/A` 사유와 `## Escalation`의 담당 경로를 명시한다.
17. **링크 작성 기준:** 템플릿 내 Markdown 링크는 템플릿 파일 위치
    (`docs/99.templates/`)가 아니라 **복사된 대상 경로**를 기준으로 계산된다.
    예: `spec.template.md` 내 `./api-spec.md`는 `docs/03.specs/<feature>/`를
    기준으로 해석된다. 링크 검증 도구는 이 설계 원칙을 인지하고 템플릿 소스
    파일의 링크를 단순 나이브 검사로 깨진 링크로 표시하면 안 된다.
18. Template deviation은 silent cleanup 대상이 아니다. 대상 문서가 매핑된
    템플릿을 의도적으로 벗어나야 하면 관련 task evidence에 파일, 기대
    템플릿, deviation 요약, 사유, 승인 또는 evidence owner, 검증 결과를
    남긴다.
19. `docs/90.references/hads/` 아래의 non-README reference 문서는 HADS
    profile을 함께 따른다. 즉 `reference.template.md`의 reference 책임 섹션을
    유지하면서 HADS `**Version X.Y.Z**`, `## AI READING INSTRUCTION`, bold block
    tag를 포함해야 한다.

## Template Alignment Note

이 README는 template-to-folder mapping의 canonical catalog다. 같은 매핑을 설명하는
`docs/00.agent-governance/rules/documentation-protocol.md`,
`docs/00.agent-governance/rules/stage-authoring-matrix.md`, 그리고
`scripts/validation/check-repo-contracts.sh`를 바꿀 때는 이 표와 함께 검토한다.

Markdown 템플릿의 placeholder/example 링크는 `docs/99.templates/` 기준으로
존재하는 링크가 아니라, 복사된 target 문서에서 다시 계산할 예시다. 활성 문서
링크 검증은 최종 target 문서를 기준으로 수행하며, 템플릿 원본에서는 예시 링크가
target-relative guidance와 함께 제공되는지를 확인한다.

## Documentation Contract

이 폴더는 새 문서의 구조뿐 아니라 stage 간 책임 경계를 정의하는 계약이다. 새 문서나 갱신 문서는 아래 매핑과 lifecycle을 먼저 확인해야 한다.

| Stage                                | Responsibility                                            | Template                                                                                                           |
| ------------------------------------ | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `docs/01.requirements/`              | 사용자 가치, 문제 정의, 요구사항, acceptance criteria     | `prd.template.md`                                                                                                  |
| `docs/02.architecture/requirements/` | 시스템 경계, 품질 속성, 참조 아키텍처                     | `ard.template.md`                                                                                                  |
| `docs/02.architecture/decisions/`    | 아키텍처 trade-off, 대안, 결정 결과                       | `adr.template.md`                                                                                                  |
| `docs/03.specs/`                     | 기능/시스템별 기술 명세, interface, verification contract | `spec.template.md`                                                                                                 |
| `docs/04.execution/plans/`           | 작업 순서, 리스크, 검증 계획, 완료 기준                   | `plan.template.md`                                                                                                 |
| `docs/04.execution/tasks/`           | 실제 작업 상태, 검증 evidence, deviation, approved-surface 기록 | `task.template.md`                                                                                                 |
| `docs/05.operations/`                | guide, policy, runbook, incident/postmortem 운영 지식     | `guide.template.md`, `policy.template.md`, `runbook.template.md`, `incident.template.md`, `postmortem.template.md` |
| `docs/90.references/`                | 느리게 변하는 reference, glossary, source-backed facts    | `reference.template.md`                                                                                            |
| `docs/98.archive/`                   | active chain에서 제거된 old 문서 tombstone                | `archive.template.md`                                                                                              |
| `README.md` files                    | 폴더 책임, 라우팅, 작업 방식, 관련 문서 index             | `readme.template.md`                                                                                               |

## Lifecycle Rules

1. Requirement: 요구사항과 acceptance criteria를 PRD로 확정한다.
2. Architecture: 시스템 경계는 ARD에, trade-off 결정은 ADR에 기록한다.
3. Specification: 구현자가 지킬 interface, data, config, verification contract를 Spec에 둔다.
4. Execution: 실행 순서는 Plan에 두고, 실제 수행 결과와 evidence는 Task에 둔다.
5. Operations: 반복 가능한 사용법, 통제, 절차, 사고 기록은 `docs/05.operations`의 목적별 bucket에 둔다.
6. Reference: active 판단을 대체하지 않는 안정적 배경 지식만 `docs/90.references`에 둔다.
7. Archive: 현재 구현과 상충해 active chain에서 제거한 whole-document old 문서는 `docs/98.archive` tombstone에 둔다.

## Cross-link Rules

- 모든 Markdown target 문서는 `## Related Documents`를 유지한다.
- 링크는 복사된 target 문서 위치 기준의 target-relative Markdown link로 계산한다.
- `docs/99.templates`에 있는 예시 링크를 target 문서에 그대로 복사하지 않는다.
- repo-local 문서 링크에 absolute filesystem path, `file://` URI, 템플릿 위치 기준 경로를 사용하지 않는다.
- `README.md`는 parent/child index 역할을 하므로 새 파일 추가, 이동, 삭제 시 함께 갱신한다.
- YAML, GraphQL, Proto 같은 machine-readable contract의 cross-link ownership은 parent Markdown Spec 또는 API Spec에서 관리한다.

## Stale Document Rules

- 오래된 문서가 같은 책임의 canonical 문서와 충돌하면 먼저 canonical 문서를 확인한다.
- 의미가 살아 있는 historical evidence는 대량 재작성하지 않고 필요한 최소 구조만 보강한다. 날짜, 명령 결과, 담당자 판단, incident/task evidence는 원문 사실을 보존한다.
- Historical evidence를 현재 템플릿으로 정규화할 때는 누락된 필수 heading, lifecycle status, target-relative Related Documents만 보강하고, 검증되지 않은 성공/실패 원인을 추가하지 않는다.
- Duplicate/noncanonical 문서 삭제 기준: canonical 문서가 존재하고, `rg` 참조 검색 결과가 정리되었고, 고유 evidence가 없거나 이관되었고, 삭제 영향이 계획/작업 evidence에 기록된 경우에만 삭제한다.
- reference/archive 이동은 reference search와 migration note 후에만 수행한다.
- 삭제는 참조 검색, 영향 기록, 사용자 승인 없이는 수행하지 않는다.

## 템플릿-폴더 매핑

| Target Location                                                               | Template                   |
| ----------------------------------------------------------------------------- | -------------------------- |
| `docs/01.requirements/YYYY-MM-DD-<feature-or-system>.md`                      | `prd.template.md`          |
| `docs/02.architecture/requirements/####-<system-or-domain>.md`                | `ard.template.md`          |
| `docs/02.architecture/decisions/####-<short-title>.md`                        | `adr.template.md`          |
| `docs/03.specs/<feature-id>/spec.md`                                          | `spec.template.md`         |
| `docs/03.specs/<feature-id>/agent-design.md`                                  | `agent-design.template.md` |
| `docs/03.specs/<feature-id>/api-spec.md`                                      | `api-spec.template.md`     |
| `docs/03.specs/<feature-id>/data-model.md`                                    | `data-model.template.md`   |
| `docs/03.specs/<feature-id>/service.md`                                       | `service.template.md`      |
| `docs/03.specs/<feature-id>/tests.md`                                         | `tests.template.md`        |
| `docs/03.specs/<feature-id>/contracts/openapi.yaml`                           | `openapi.template.yaml`    |
| `docs/03.specs/<feature-id>/contracts/schema.graphql`                         | `schema.template.graphql`  |
| `docs/03.specs/<feature-id>/contracts/service.proto`                          | `service.template.proto`   |
| `docs/04.execution/plans/YYYY-MM-DD-<feature>.md`                             | `plan.template.md`         |
| `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md`                   | `task.template.md`         |
| `docs/05.operations/guides/**.md`                                             | `guide.template.md`        |
| `docs/05.operations/policies/**.md`                                           | `policy.template.md`       |
| `docs/05.operations/runbooks/**.md`                                           | `runbook.template.md`      |
| `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident-title>.md`            | `incident.template.md`     |
| `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident-title>-postmortem.md` | `postmortem.template.md`   |
| `docs/00.agent-governance/memory/<note>.md`                                   | `memory.template.md`       |
| `docs/00.agent-governance/memory/progress.md`                                 | `progress.template.md`     |
| `docs/90.references/<category>/<item>.md`                                     | `reference.template.md`    |
| `docs/98.archive/<original-stage>/<original-path>.md`                         | `archive.template.md`      |
| `README.md`, `docs/README.md`, and folder `README.md` files                   | `readme.template.md`       |

## API Spec 템플릿 위치

API 계약 문서는 별도 유형이 아니라 `03.specs/` 아래에서 사용하는 하위 템플릿이다.

- 올바른 위치: `docs/03.specs/<feature-id>/api-spec.md`
- 잘못된 패턴: `docs/api/...`

## README 템플릿

각 폴더 README도 반복적으로 재사용되는 문서 유형이므로 별도 README 템플릿을 함께 제공한다.

README 작성 시 먼저 대상이 folder index인지 service leaf인지 판단한다.

- Folder index README: 하위 문서, 서비스, 또는 stage bucket을 찾기 위한 routing 문서다. `Structure`, `How to Work in This Area`, `Related Documents`가 핵심이다.
- Service leaf README: 단일 runtime service나 config bundle의 검증 가능한 readiness evidence를 기록한다. infra service leaf는 `Service Readiness` 표를 포함해야 한다.
- 같은 README에 두 역할을 섞지 않는다. 폴더가 실제 service marker(`docker-compose*.yml`, `compose.yml`, `Dockerfile`)를 가진 경우에만 service leaf readiness를 요구한다.

## Structure

```text
99.templates/
├── *.template.md       # Markdown stage and README templates
├── *.template.yaml     # OpenAPI contract template
├── *.template.graphql  # GraphQL schema template
├── *.template.proto    # Protobuf service contract template
├── archive.template.md # Archive tombstone template
└── README.md           # This file
```

## How to Work in This Area

1. 새 문서를 만들기 전에 [`../00.agent-governance/rules/stage-authoring-matrix.md`](../00.agent-governance/rules/stage-authoring-matrix.md)의 대상 stage row를 확인한다.
2. 대응 템플릿을 복사한 뒤 placeholder를 모두 실제 값으로 교체한다.
3. README는 [`readme.template.md`](./readme.template.md)의 base structure와 경로별 snippet을 조합한다.
4. 템플릿 자체를 바꿀 때는 [`../00.agent-governance/rules/documentation-protocol.md`](../00.agent-governance/rules/documentation-protocol.md)의 DOCS 3 RULES와 repository contract 검증을 함께 확인한다.

## Spec 하위 보조 문서 템플릿

`03.specs/<feature-id>/` 아래에서 반복적으로 사용하는 보조 설계 문서와 계약 파일용 템플릿을 함께 제공한다.

- `agent-design.template.md`는 Agent 역할, IO, tool, guardrail, eval 계약을 정의할 때 사용한다.
- `service.template.md`는 컨테이너 서비스의 런타임 계약(이미지/빌드, 보안 하드닝, 네트워크, 볼륨, secret 참조, healthcheck, 검증)을 정의할 때 사용한다. 복사 가능한 시드는 `examples/sample-web-service/`에 있다.
- `data-model.template.md`와 `tests.template.md`는 같은 feature directory의 supporting Markdown contract다.
- `openapi.template.yaml`, `schema.template.graphql`, `service.template.proto`는 machine-readable contract의 출발점이며, cross-link는 parent Spec 또는 API Spec에서 관리한다.

## 예시

- 새 운영 문서: 대상 bucket에 맞는 `guide.template.md`, `policy.template.md`, `runbook.template.md`를 복사해 `docs/05.operations/<guides|policies|runbooks>/<topic>.md` 또는 `docs/05.operations/<guides|policies|runbooks>/<domain>/<topic>.md`로 작성한다.
- 운영 문서는 `guides/`가 사용 맥락, `policies/`가 통제/예외/검토 기준, `runbooks/`가 순서 있는 절차와 evidence를 담당한다.
- 운영 문서 cross-link는 복사된 Target 기준으로 계산한다. 예: `docs/05.operations/guides/<topic>.md`에서는 `../../02.architecture/...`, `docs/05.operations/guides/<domain>/<topic>.md`에서는 `../../../02.architecture/...`, `docs/05.operations/guides/<domain>/<subdomain>/<topic>.md`에서는 `../../../../02.architecture/...`를 사용한다.
- 새 사고 기록: `incident.template.md`를 복사해 `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident-title>.md`로 작성한다.
- 새 사후 분석: `postmortem.template.md`를 복사해 `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident-title>-postmortem.md`로 작성한다.
- 새 governance memory note: `memory.template.md`를 복사해 `docs/00.agent-governance/memory/<short-title>.md`로 작성한다.
- agent progress log 변경: `progress.template.md`를 기준으로 `docs/00.agent-governance/memory/progress.md`를 갱신한다.
- 새 참고 문서: `reference.template.md`를 복사해 `docs/90.references/<category>/<item>.md`로 작성한다.
- 새 archive tombstone: `archive.template.md`를 복사해 `docs/98.archive/<original-stage>/<original-path>.md`로 작성한다.

## Related Documents

- [docs index](../README.md)
- [archive index](../98.archive/README.md)
- [Documentation protocol](../00.agent-governance/rules/documentation-protocol.md)
- [Stage authoring matrix](../00.agent-governance/rules/stage-authoring-matrix.md)
