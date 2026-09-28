---
title: "Documentation Space"
version: "1.2.6"
type: "common/documentation-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
---

# docs

> 단계별 저장소 지식을 위한 공유 harness-engineering 및 agent-first engineering 문서 공간.

## Overview

`docs/`는 shared harness-engineering and agent-first engineering 목적에 맞춰 프로젝트의 요구사항, 아키텍처, 결정 사항, 기술 명세, 실행 증거, 운영 지식을 통합 관리하는 표준 공간입니다. 활성 문서는 허용된 taxonomy 안에서만 관리하며, 검증 스크립트가 이 계약을 강제합니다.

현재 문서 흐름은 `01.requirements -> 02.architecture -> 03.specs -> 05.operations`입니다. Plan과 Task는 별도 stage가 아니라 소유 패키지 안의 `03.specs/{number:4}-{slug}/plan.md`와 `03.specs/{number:4}-{slug}/tasks/`에 함께 놓입니다. 보조 문서 공간으로 `90.references`, `98.archive`, `99.templates`를 사용합니다. 공통 Agent 거버넌스는 문서 stage 밖의 [`.agents/`](../.agents/README.md)가 소유합니다.

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
├── 01.requirements/            # 제품/시스템 요구사항
├── 02.architecture/            # 아키텍처 설명과 결정 기록
├── 03.specs/                   # Spec Package: spec, plan, tasks, contracts 동거
├── 05.operations/              # 운영 가이드, 정책, 런북, 사고 기록
├── 90.references/              # 느리게 변하는 참고 지식, 표준, 학습 로드맵, LLM Wiki
├── 98.archive/                 # frozen 본문을 위한 retention class와 route disposition
├── 99.templates/               # stage 문서 작성을 위한 표준 템플릿
└── README.md                   # 이 파일
```

각 stage 하위의 실제 구조는 그 stage의 README가 소유합니다.

## Routing

| 하려는 작업 | 이동할 곳 |
| --- | --- |
| 사용자 가치나 요구사항을 정의 | `01.requirements/` |
| 아키텍처를 설명 | `02.architecture/descriptions/` |
| 아키텍처 결정을 기록 | `02.architecture/decisions/` |
| 기술 명세를 작성 | `03.specs/####-<slug>/spec.md` |
| 실행 가능한 interface 계약을 선언 | `03.specs/####-<slug>/contracts/` |
| 구현 작업을 계획 | `03.specs/####-<slug>/plan.md` |
| Task 증거를 기록 | `03.specs/####-<slug>/tasks/` |
| 서비스를 운영하거나 설정 | `05.operations/guides/` |
| 운영 통제를 정의 | `05.operations/policies/` |
| 복구나 반복 절차를 실행 | `05.operations/runbooks/` |
| 사고나 사후 분석을 기록 | `05.operations/incidents/<year>/inc-####-<slug>/` |
| LLM 대상 저장소 탐색을 제공 | root `llms.txt`와 각 surface README |
| 보존된 본문이나 그 처분 기록을 확인 | `98.archive/` |

## Migration Map

이전 stage 경로의 이관 매핑은 [Stage 98 README](98.archive/README.md)를
통해 historical Migration에서 찾습니다. 그 기록은 과거 이동의 근거이며
현재 경로나 작성 계약은 Stage 99 Registry가 소유합니다.

## How to Work in This Area

1. 새 문서를 만들기 전에 이 README와 대상 stage의 `README.md`를 먼저 읽습니다.
2. 새 active stage 문서는 반드시 위 Structure에 나열된 canonical 경로 아래에 둡니다.
3. 새 문서는 [99.templates](99.templates/README.md)의 대응 템플릿을 사용하고, README는 그 template catalog의 `templates/common/readme-documentation.template.md`를 따릅니다.
4. 문서 변경 후 상위 README, 관련 stage 문서, traceability 링크를 함께 갱신합니다.
5. secret 값, token, 인증서 원문은 문서에 쓰지 않습니다.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작합니다.
- 기존 SSoT 문서를 중복 생성하지 않습니다.
- 제목과 구조는 사람과 AI Agent 모두가 해석할 수 있도록 명시적으로 작성합니다.
- 상위 문서와 하위 산출물 간 추적성을 유지합니다.
- 문서 언어는 [문서 언어 규칙](../.agents/governance/documentation-protocol.md#document-language)이
  정하며, 각 Registry profile의 `language`가 그 결과를 소유합니다.
- Markdown 링크는 상대 경로를 사용하며 절대 경로나 `file://`를 사용하지 않습니다.

## Documentation Contract

[Stage 99](99.templates/README.md)가 모든 문서 profile, 경로, lifecycle,
identifier, 등록된 template을 소유합니다. [공통 Agent 거버넌스](../.agents/README.md)는
작성 행동과 승인 경계를 소유합니다. 이 index는 탐색 전용입니다.

## Cross-link Rules

- 새 문서와 갱신 문서는 하나의 `## Related Documents` 섹션을 유지합니다.
- 상대 링크는 현재 파일 위치 기준으로 계산합니다.
- 템플릿의 예시 링크는 복사된 target 위치에서 다시 계산한 뒤 실제 문서 경로로 바꿉니다.
- README가 무엇을 목록으로 가질 수 있는지는 [README 탐색 규칙](../.agents/governance/documentation-protocol.md#readme-navigation)을 따릅니다.
- Archive/delete 후보는 [Stage 99 계약](99.templates/README.md)과 [공통 Agent 거버넌스 승인 경계](../.agents/governance/approval-boundaries.md)에 따라 분류하고, 검증된 Git 복구 근거와 독립 검토를 남깁니다.
- Stage 98에서 직접 링크할 수 있는 것은 index와 `completed/`, `resolved/`
  보존본입니다. `superseded/` 대신 후속을, `retired/`, Tombstone, Migration 대신
  현재 route를 인용하고, 이름을 불러야 하는 frozen 기록은 식별자로 부른 뒤
  Stage 98 README에서 찾습니다.

## Template Usage

역할은 [99.templates](99.templates/README.md)의 Registry(`registry.json`)에서
고르고, 그 source는 같은 곳의 template catalog(`templates/README.md`)에서
복사합니다. Spec, Plan, Task, machine contract는 Stage 03에 함께 있습니다.
Requirement 자식 identity는 그 package가 소유하며, Stage 98은 frozen
본문을 담는 retention class와 아무것도 담지 않는 route disposition을
포함합니다.

## Document Contract Validation

문서 체계와 repository contract는 다음 검증으로 유지합니다.

```bash
python3 scripts/validation/run-ci-gate.py --profile changed
python3 scripts/validation/check-document-links.py --mode traceability
```

`run-ci-gate.py`는 허용된 docs top-level 폴더, required README, template inventory, GitHub Actions YAML, script references, Docker image tag policy, tech-stack version drift, runtime agent/function catalog, LLM Wiki contract 동기화와 generated index freshness를 확인합니다. `check-document-links.py --mode alignment`는 현재 소유자 문서와 operations 문서 간 추적성 동기화를 확인합니다.

## Historical Refresh Evidence

이전 infra/secrets/docs refresh의 Spec은 아래 보존 package에 있습니다. 이
package는 Spec만 보존하던 시기에 처분되었으므로 Plan과 Task 본문은 archive에
없습니다. ADR-0033 수락 이후 처분되는 package는 Spec, Plan, 모든 Task를 함께
보존합니다.
현재 구조와 운영 안내는 [infra README](../infra/README.md)와
[Operations](05.operations/README.md)가 소유하며 완료 package를 새 작업 기록으로
재사용하지 않습니다.

<!-- Historical evidence table (not current authority; source: Git history). -->

| Evidence | Current State |
| --- | --- |
| Spec | [98.archive](98.archive/README.md) (`completed/03.specs/0095-infra-secrets-docs-refresh/spec.md`) |
| Plan and Task evidence | 보존되지 않음; 이 package는 ADR-0033이 대체한 Spec-only 모델 아래서 처분되었고 그 Plan과 Task는 Git history만으로 복구할 수 있습니다 |
| Runtime scope | Docker Compose runtime, secret 값, 인증서 내용, agent runtime은 변경되지 않음 |

## LLM Wiki Ownership and Historical Evidence

repo-local LLM Wiki는 2026-09-10에 은퇴했습니다. 그 generator, 세 개의
생성된 index, 이를 유지하던 operations package가 함께 제거되었습니다.
Stage 90 증거는 현재 consumer가 존재하는 동안에만 현재성을 유지하는데 그
index의 모든 consumer가 같은 변경에서 제거되었기 때문입니다.

이제 생성된 경로 index는 존재하지 않습니다. 탐색은 `llms.txt`의 정리된
entry point와 각 surface의 README를 통해 이루어지며 `graphify-out/` 아래의
advisory graph는 advisory로 남고 `.agents/governance/environment-constraints.md`가
그로부터 결론지을 수 있는 것을 소유합니다.

| Evidence | Current State |
| --- | --- |
| Historical implementation | [98.archive](98.archive/README.md) (`completed/03.specs/0096-llm-wiki-agent-first-completion/spec.md`) |
| Plan and Task evidence | 보존되지 않음; 이 package는 ADR-0033이 대체한 Spec-only 모델 아래서 처분되었고 그 Plan과 Task는 Git history만으로 복구할 수 있습니다 |
| Retired indexes | `DATA-0076`, `DATA-0082`, `DATA-0083`, 각각 tombstone으로 기록됨 |
| Retired operations package | `GDE-0007`, `POL-0007`, `RUN-0007`, 각각 tombstone으로 기록됨 |

## Related Documents

- [Agent governance README](../.agents/README.md)
- [01.requirements/README.md](01.requirements/README.md)
- [02.architecture/README.md](02.architecture/README.md)
- [03.specs/README.md](03.specs/README.md)
- [05.operations/README.md](05.operations/README.md)
- [90.references/README.md](90.references/README.md)
- [98.archive/README.md](98.archive/README.md)
- [99.templates/README.md](99.templates/README.md)
- [../README.md](../README.md)
- [../infra/README.md](../infra/README.md)
- [../secrets/README.md](../secrets/README.md)
- [../scripts/README.md](../scripts/README.md)
