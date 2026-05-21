---
status: active
---

<!-- Target: docs/01.requirements/README.md -->

# Product Requirements Documents (PRD)

> 이 경로는 제품 요구사항 정의(Vision, Use Case, Requirements)를 관리한다.

## Overview

`docs/01.requirements`는 시스템이나 기능의 "Why"와 "What"을 정의하는 문서가 보관되는 장소다. 비즈니스 가치, 사용자 시나리오, 기능적/비기능적 요구사항을 기술하며 모든 설계와 구현의 출발점이 된다.

## Audience

이 README의 주요 독자:

- Developers
- Product Owners
- System Architects
- AI Agents

## Scope

### In Scope

- 제품 비전 및 목표 정의서
- 사용자 스토리 및 유즈케이스 명세
- 기능적 / 비기능적 요구사항 정의 (PRD)
- 핵심 성공 지표 (KPI/Metrics)

### Out of Scope

- 상세 기술 설계 (Spec 담당)
- 아키텍처 참조 모델 (ARD 담당)
- 상세 구현 코드
- 운영 및 유지보수 절차

## Structure

```text
docs/01.requirements/
├── 기초 PRD (2026-03-26)
│   ├── 2026-03-26-01-gateway.md             # Gateway Tier
│   ├── 2026-03-26-02-auth.md                # Auth / IAM Tier
│   ├── 2026-03-26-03-security.md            # Security (Vault) Tier
│   ├── 2026-03-26-04-data.md                # Data Tier (core)
│   ├── 2026-03-26-04-data-analytics.md      # Analytics Sub-tier
│   ├── 2026-03-26-05-messaging.md           # Messaging Tier
│   ├── 2026-03-26-06-observability.md       # Observability Tier
│   ├── 2026-03-26-07-workflow.md            # Workflow Tier
│   ├── 2026-03-26-08-ai.md                  # AI Infrastructure Tier
│   ├── 2026-03-26-09-tooling.md             # Tooling Tier
│   ├── 2026-03-26-10-communication.md       # Communication Tier
│   └── 2026-03-26-11-laboratory.md          # Laboratory Tier
├── 추가 PRD
│   ├── 2026-03-27-08-ai-open-webui.md       # Open WebUI (AI sub-feature)
│   └── 2026-04-01-standardize-infra-net.md  # infra_net 표준화
├── 최적화/하드닝 PRD (2026-03-28)
│   ├── 2026-03-28-02-auth-optimization-hardening.md
│   ├── 2026-03-28-03-security-optimization-hardening.md
│   ├── 2026-03-28-04-data-optimization-hardening.md
│   ├── 2026-03-28-05-messaging-optimization-hardening.md
│   ├── 2026-03-28-06-observability-optimization-hardening.md
│   ├── 2026-03-28-07-workflow-optimization-hardening.md
│   ├── 2026-03-28-08-ai-optimization-hardening.md
│   ├── 2026-03-28-09-tooling-optimization-hardening.md
│   └── 2026-03-28-11-laboratory-optimization-hardening.md
│   # NOTE: 01-gateway, 10-communication 하드닝 PRD는 backlog/deferred 항목이며 별도 승인 전까지 새 PRD를 만들지 않음
└── README.md                                # This file
```

## How to Work in This Area

1. 새 기능 제안 시 [prd.template.md](../99.templates/prd.template.md)를 사용하여 문서를 생성함.
2. 상위 비전이나 비즈니스 목표와 일치하는지 검토함.
3. 문서 상태(`draft`, `approved`, `deprecated`)를 frontmatter의 `status` 필드로 관리함.
4. 승인 후에는 관련 `ARD`, `Spec`, `Plan` 문서를 생성하여 추적성을 유지함.

## PRD Contract

PRD는 문제와 요구사항의 SSoT입니다. 구현 방법, 실행 순서, 운영 절차는 이 stage에 두지 않습니다.

| PRD Must Define | Downstream Owner |
| --- | --- |
| 사용자 또는 운영자 문제 | ARD/ADR이 해결 구조와 trade-off를 설명 |
| 기능 요구사항과 비기능 요구사항 | Spec이 interface와 verification contract로 변환 |
| Scope, out-of-scope, non-goals | Plan이 실행 범위와 risk gate로 변환 |
| Success criteria와 acceptance criteria | Task가 검증 evidence로 기록 |

새 PRD의 `## Related Documents` 링크는 `docs/01.requirements/`에 복사된 PRD 파일 위치 기준으로 계산합니다. 예를 들어 architecture requirements는 `../02.architecture/requirements/...`, technical spec은 `../03.specs/...`, execution plan은 `../04.execution/plans/...`로 연결합니다.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작한다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.
- 상위 문서와 하위 산출물 간 추적성을 유지한다.

## AI Agent Guidance

이 영역을 수정하기 전에 Agent는 다음을 먼저 수행해야 한다.

1. 이 README를 먼저 읽는다.
2. 기존 PRD 문서를 확인하여 중복 기능 정의를 피한다.
3. 요구사항 변경 시 연관된 `Spec`과 `Plan` 문서도 함께 검토하여 불일치를 방지한다.

### Allowed Outputs

- PRD 문서 (`prd.template.md` 기반, 날짜-슬러그 파일명 형식. 예: `2026-05-21-feature-name.md`)
- 기존 PRD의 `status` 갱신 (`draft` → `approved` → `deprecated`)

### Guardrails

- `prd.template.md` 없이 새 PRD 형식을 임의로 만들지 않는다.
- 기존 구조 확인 없이 새 파일을 만들지 않는다.
- 추적성 링크(`ARD`, `Spec`, `Plan`, `ADR`)가 필요한 영역에서 상위/하위 문서 연결을 누락하지 않는다.
- `2026-03-26-04-data.md`와 `2026-03-26-04-data-analytics.md`는 별도 PRD이므로 혼용하지 않는다.

### Validation

- 새 PRD 생성 후 `Related Documents` 링크가 실제 존재하는 파일을 가리키는지 확인한다.
- `bash scripts/validation/check-doc-traceability.sh` 실행으로 추적성 검증.

## Related Documents

- [ARD README](../02.architecture/requirements/README.md)
- [Spec README](../03.specs/README.md)
- [Plan README](../04.execution/plans/README.md)
