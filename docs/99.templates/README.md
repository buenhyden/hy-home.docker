# 99.templates

## 목적

이 폴더는 문서 템플릿을 저장한다. 새 문서는 이 폴더의 템플릿을 복사해 시작한다.

## 템플릿 목록

- `agent-design.template.md`
- `data-model.template.md`
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
- `task.template.md`
- `guide.template.md`
- `operation.template.md`
- `runbook.template.md`
- `incident.template.md`
- `postmortem.template.md`
- `reference.template.md`
- `readme.template.md`

## 사용 원칙

1. 템플릿의 Target 경로를 실제 저장 위치와 맞춘다.
2. Placeholder는 모두 제거한다.
3. 상대 경로만 사용한다.
4. PRD/ARD/ADR/Spec/Plan/Task의 추적성을 유지한다.
5. Agent 기능은 Role, Tool, Guardrail, Eval, Fallback을 빠뜨리지 않는다.

## 템플릿-폴더 매핑

| Folder | Template |
| --- | --- |
| `01.prd/` | `prd.template.md` |
| `02.ard/` | `ard.template.md` |
| `03.adr/` | `adr.template.md` |
| `04.specs/` | `spec.template.md` |
| `04.specs/<feature-id>/api-spec.md` | `api-spec.template.md` |
| `05.plans/` | `plan.template.md` |
| `06.tasks/` | `task.template.md` |
| `07.guides/` | `guide.template.md` |
| `08.operations/` | `operation.template.md` |
| `09.runbooks/` | `runbook.template.md` |
| `10.incidents/` | `incident.template.md` |
| `11.postmortems/` | `postmortem.template.md` |
| `90.references/` | `reference.template.md` |

## API Spec 템플릿 위치

API 계약 문서는 별도 유형이 아니라 `04.specs/` 아래에서 사용하는 하위 템플릿이다.

- 올바른 위치: `docs/04.specs/<feature-id>/api-spec.md`
- 잘못된 패턴: `docs/api/...`

## README 템플릿

각 폴더 README도 반복적으로 재사용되는 문서 유형이므로 별도 README 템플릿을 함께 제공한다.

## Spec 하위 보조 문서 템플릿

`04.specs/<feature-id>/` 아래에서 반복적으로 사용하는 보조 설계 문서와 계약 파일용 템플릿을 함께 제공한다.
