---
title: Workspace Governance Authority
type: sdlc/architecture-decision
layer: architecture
status: active
owner: "@buenhyden"
artifact_id: ADR-0029
parent_ids:
  - AD-0027
created: 2026-08-20
updated: 2026-09-01
supersedes:
  - ADR-0027
superseded_by: null
---
# ADR-0029: Workspace Governance Authority

## Context

Agent 정책, 문서 형식, provider runtime mechanics, validator routing이 서로의
규칙을 중복 소유하면 읽는 경로에 따라 다른 결론이 나온다. 현재 구조에는
정책과 machine contract를 분리하면서도 하나의 SDLC와 검증 interface를
유지하는 명시적 권한 모델이 필요하다.

## Decision Drivers

- 각 규칙은 정확히 하나의 current owner를 가져야 한다.
- Provider별 형식은 공통 정책을 재정의하지 않아야 한다.
- 문서 profile, lifecycle, template은 prose가 아닌 typed contract로 검증되어야
  한다.
- Historical evidence와 branch SHA는 current 규칙의 입력이 되어서는 안 된다.
- 공개 Gate는 작고 안정적인 interface를 유지해야 한다.

## Options Considered

### Distributed authority 유지

변경량은 작지만 adapter, template, validator, historical document 사이의
충돌을 계속 허용한다.

### Stage 00이 모든 문서 mechanics까지 소유

한 위치에 모이지만 AI Agent 정책과 문서 schema/lifecycle이 결합된다.

### Normative policy와 typed document authority 분리

Stage 00은 Agent 거버넌스를, Stage 99는 문서 machine contract를 소유하고
scripts와 provider surface는 각각의 consumer가 된다.

## Decision

분리된 권한 모델을 채택한다.

- Stage 00은 AI Agent 정책, workflow, canonical roles/skills, provider
  boundary의 유일한 규범적 권한이다.
- Stage 99 Registry와 schema는 docs path, profile, stable ID, required section,
  lifecycle, traceability, template의 유일한 machine authority다.
- `.agents/`, `.claude/`, `.codex/`는 generated projection 또는 native runtime
  mechanics이며 정책 소스가 아니다.
- Git의 regular-blob history가 삭제된 본문의 recovery mechanism이다. Current
  authority는 Stage 98 historical record를 입력이나 필수 링크로 사용하지
  않는다.
- validation public interface는 `document-contract`, `document-graph`,
  `document-lifecycle`, `operations`, `agent-governance`,
  `repository-integrity` 여섯 책임 suite다. Manifest가 atomic validator
  inventory를, workflow contract가 CI routing을 소유한다.
- 일반 변경 완료에는 branch SHA pin, corpus snapshot, migration ledger,
  duplicate digest가 필요하지 않다. Current Task와 검토된 Git diff가 실행
  증거와 recovery boundary를 제공한다.

## Consequences

- 충돌은 파일 우선순위가 아니라 concern owner로 판정할 수 있다.
- Provider mechanics와 document schema가 독립적으로 진화할 수 있다.
- Registry와 projection freshness validator는 fail closed해야 한다.
- suite는 focused validator를 조합할 뿐 동일 predicate를 다시 구현할 수
  없다.
- 새로운 public suite 책임이나 authority owner 변경은 별도 ADR이 필요하다.

## Traceability

- [REQ-0024 Agent Governance Standardization](../../01.requirements/0024-agent-governance-standardization.md)
- [AD-0027 Agent Governance Canonical Adapter](../descriptions/0027-agent-governance-canonical-adapter.md)
- [ADR-0027 superseded decision](0027-stage-00-canonical-adapter-model.md)
- [Stage 99 document authority](../../99.templates/README.md)
- [SPEC-0158 lifecycle convergence](../../03.specs/0158-document-governance-lifecycle-convergence/spec.md)
