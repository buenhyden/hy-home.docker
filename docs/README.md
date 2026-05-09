# docs

> 요구사항, 아키텍처, 계획, 작업, 운영 절차, 참고 지식을 stage taxonomy로 관리하는 공식 문서 공간

## Overview

`docs/`는 프로젝트의 모든 요구사항, 아키텍처, 결정 사항, 운영 절차, 참고 지식을 통합 관리하는 표준 공간입니다. 이 체계는 추적성, 검증 가능성, AI Agent 협업 가능성을 중심으로 설계되어 있으며, 활성 문서는 허용된 stage taxonomy 안에서만 관리합니다.

기본 문서 흐름은 `01.prd -> 02.ard -> 03.adr -> 04.specs -> 05.plans -> 06.tasks -> 07.guides / 08.operations / 09.runbooks -> 10.incidents`입니다. 보조 공간으로 `00.agent-governance`, `90.references`, `99.templates`를 사용합니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 공식 stage 문서 taxonomy와 작성 원칙
- 문서 유형별 템플릿 매핑
- 문서 추적성, 검증, README 작성 기준
- Agent governance와 사람 대상 문서의 경계

### Out of Scope

- Docker Compose runtime 설정 원문
- secret 값, credential, token, 인증서 원문
- 임시 scratch 문서나 비표준 active stage 폴더
- 개별 서비스의 상세 운영 절차 본문

## Structure

```text
docs/
├── 00.agent-governance/  # AI Agent 실행 정책, provider 계약, scope, rule, runtime catalog
├── 01.prd/               # 제품 요구사항 정의
├── 02.ard/               # 아키텍처 참조 모델 및 품질 속성 정의
├── 03.adr/               # 기술적 의사결정 기록
├── 04.specs/             # 컴포넌트/기능별 상세 설계 명세
├── 05.plans/             # 실행 계획 및 마일스톤
├── 06.tasks/             # 실제 구현 및 검증 작업 단위
├── 07.guides/            # 사용자와 운영자를 위한 재현 가능한 사용 가이드
├── 08.operations/        # 시스템 운영 정책 및 거버넌스
├── 09.runbooks/          # 반복적 운영 작업의 실행 지침
├── 10.incidents/         # 사고 사실 기록, 사후 분석, 재발 방지 대책
├── 90.references/        # 느리게 변하는 참고 지식, 표준, 학습 로드맵
├── 99.templates/         # stage 문서 작성을 위한 표준 템플릿
└── README.md             # This file
```

## How to Work in This Area

1. 새 문서를 만들기 전에 이 README와 대상 stage의 `README.md`를 먼저 읽습니다.
2. 새 active stage 문서는 반드시 `01.prd`, `02.ard`, `03.adr`, `04.specs`, `05.plans`, `06.tasks`, `07.guides`, `08.operations`, `09.runbooks`, `10.incidents`, `90.references`, `99.templates` 아래에 둡니다.
3. 새 문서는 [99.templates](99.templates/README.md)의 대응 템플릿을 사용하고, README는 [99.templates/readme.template.md](99.templates/readme.template.md)를 따릅니다.
4. 문서 변경 후 상위 README, 관련 stage 문서, traceability 링크를 함께 갱신합니다.
5. secret 값, token, 인증서 원문은 문서에 쓰지 않습니다.

## Documentation Standards

이 영역의 문서는 다음 기준을 따라야 합니다.

- 가능한 경우 승인된 템플릿에서 시작합니다.
- 기존 SSoT 문서를 중복 생성하지 않습니다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성합니다.
- 상위 문서와 하위 산출물 간 추적성을 유지합니다.
- Agent 전용 문서(`docs/00.agent-governance/`, `AGENTS.md` 등)는 영어를 원칙으로 하고, 사람 대상 README/guide/operation/runbook/reference 문서는 한국어를 기본으로 합니다.
- Markdown 링크는 상대 경로를 사용하며 절대 경로나 `file://`를 사용하지 않습니다.

## Traceability Rules

이 영역의 각 문서는 가능한 경우 다음 중 하나 이상과 연결되어야 합니다.

- Product Requirements Document (PRD)
- Architecture Requirements Document (ARD)
- Architecture Decision Record (ADR)
- Specification (Spec)
- Plan
- Task
- Guide
- Operation
- Runbook
- Incident / Postmortem

## Template Usage

| 문서 유형 | 위치 | 템플릿 |
| --- | --- | --- |
| PRD | `01.prd/` | `99.templates/prd.template.md` |
| ARD | `02.ard/` | `99.templates/ard.template.md` |
| ADR | `03.adr/` | `99.templates/adr.template.md` |
| Spec | `04.specs/` | `99.templates/spec.template.md` |
| API Spec | `04.specs/<feature-id>/api-spec.md` | `99.templates/api-spec.template.md` |
| Agent Design | `04.specs/<feature-id>/agent-design.md` | `99.templates/agent-design.template.md` |
| Plan | `05.plans/` | `99.templates/plan.template.md` |
| Task | `06.tasks/` | `99.templates/task.template.md` |
| Guide | `07.guides/` | `99.templates/guide.template.md` |
| Operation | `08.operations/` | `99.templates/operation.template.md` |
| Runbook | `09.runbooks/` | `99.templates/runbook.template.md` |
| Incident | `10.incidents/` | `99.templates/incident.template.md` |
| Postmortem | `10.incidents/` | `99.templates/postmortem.template.md` |
| Reference | `90.references/` | `99.templates/reference.template.md` |
| README | 각 폴더 | `99.templates/readme.template.md` |

템플릿 없이 새 형식을 임의로 추가하기 전에 기존 문서 체계를 먼저 검토합니다. 동일 목적의 문서가 이미 존재하면 새 문서를 만들기보다 기존 문서를 확장하는 방식을 우선합니다.

## Metadata Expectations

- 새 stage 문서는 가능한 경우 front matter `status`를 포함합니다.
- 문서 상단에는 빠른 이해를 위한 한국어 Overview를 둡니다.
- 완료 또는 검증이 필요한 문서는 명령, 결과, evidence 위치를 기록합니다.
- AI Agent가 수정한 문서는 관련 task 또는 plan에 검증 흔적을 남깁니다.

## Document Contract Validation

문서 체계와 repository contract는 다음 검증으로 유지합니다.

```bash
bash scripts/check-repo-contracts.sh
bash scripts/check-doc-traceability.sh
```

`check-repo-contracts.sh`는 허용된 docs top-level 폴더, required README, template inventory, GitHub Actions YAML, script references, Docker image tag policy, tech-stack version drift, runtime catalog 동기화를 확인합니다. `check-doc-traceability.sh`는 plans, operations, runbooks의 추적성 동기화를 확인합니다.

## Current Refresh Evidence

현재 infra/secrets/docs refresh 작업은 기존 spec/plan/task 문서를 in-place로 재사용합니다.

| Evidence | Current State |
| --- | --- |
| Spec | [04.specs/infra-secrets-docs-refresh/spec.md](04.specs/infra-secrets-docs-refresh/spec.md) |
| Plan | [05.plans/2026-05-09-infra-secrets-docs-refresh.md](05.plans/2026-05-09-infra-secrets-docs-refresh.md) |
| Task evidence | [06.tasks/2026-05-09-infra-secrets-docs-refresh.md](06.tasks/2026-05-09-infra-secrets-docs-refresh.md) |
| README audit | 127 README files, heading gaps 0 |
| Stage audit | 208 non-README stage docs, heading gaps 0 |
| Runtime scope | Docker Compose runtime, secret values, cert contents, agent runtime unchanged |

Heading audit 통과는 구조 검증입니다. 문서 품질 검토에서는 중복 legacy/template 블록, 실제 Markdown 링크가 아닌 참조, secret 값을 읽도록 오해될 수 있는 문장, shell history에 민감값을 남길 수 있는 예시를 별도로 확인합니다.

## Related References

- [00.agent-governance/README.md](00.agent-governance/README.md)
- [04.specs/README.md](04.specs/README.md)
- [04.specs/infra-secrets-docs-refresh/spec.md](04.specs/infra-secrets-docs-refresh/spec.md)
- [05.plans/2026-05-09-infra-secrets-docs-refresh.md](05.plans/2026-05-09-infra-secrets-docs-refresh.md)
- [06.tasks/2026-05-09-infra-secrets-docs-refresh.md](06.tasks/2026-05-09-infra-secrets-docs-refresh.md)
- [07.guides/README.md](07.guides/README.md)
- [08.operations/README.md](08.operations/README.md)
- [09.runbooks/README.md](09.runbooks/README.md)
- [90.references/README.md](90.references/README.md)
- [99.templates/README.md](99.templates/README.md)
- [../README.md](../README.md)
- [../infra/README.md](../infra/README.md)
- [../secrets/README.md](../secrets/README.md)
- [../scripts/README.md](../scripts/README.md)
