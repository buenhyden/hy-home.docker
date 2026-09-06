---
title: "Agent Governance Canonical Adapter Architecture"
version: "1.2.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
layer: "architecture"
artifact_id: "AD-0027"
parent_ids:
- "REQ-0024"
created: "2026-06-01"
---
# Agent Governance Canonical Adapter Architecture

## Context and Stakeholders

여러 AI provider가 같은 저장소를 수정하더라도 정책, 역할, skill, SDLC,
승인 경계는 하나여야 한다. Maintainer는 `.agents/`에서 규범을 검토하고,
Agent는 provider adapter를 통해 동일한 규범을 native runtime 형식으로
소비하며, reviewer는 projection drift를 독립적으로 검증한다.

## System Boundaries

- `.agents/`는 policy, workflow, canonical roles/skills, provider boundary를
  소유한다.
- Stage 99는 docs profile, path, identity, lifecycle, template의 typed contract를
  소유한다.
- `.agents/governance/`, `.agents/roles/`, `.agents/skills/`,
  `.agents/knowledge/`, `.agents/prompts/`는 작성 정본이며 생성물이나
  호환성 복사본이 아니다.
- `.agents/knowledge/`는 정본 소유자로 라우팅하는 검증된 navigational
  knowledge를 소유하고, `.agents/prompts/`는 재사용 prompt의 입력·출력
  계약을 소유한다. 두 category는 의무 규칙과 절차 본문을 복제하지 않으며
  실행 진행 상태를 소유하지 않는다.
- `.claude/provider.md`, `.codex/provider.md`는 각 provider의 로딩·문법 차이를
  소유한다. 생성 README·role·Claude skill adapter와 기존 runtime mechanics는
  공통 정책을 정의하거나 canonical source를 덮어쓰지 않는다.
- Current Task는 실행 결과를 소유한다. 완료 후 Stage 98이 동결 본문을
  보존하며 Git은 source와 recovery history를 증명한다.
- User-global configuration, credential, provider availability, deployment
  state는 이 아키텍처 밖이다.

## Components

| Component | Responsibility |
| --- | --- |
| canonical agent governance bootstrap and policies | authority resolution, safety, workflow |
| canonical agent governance roles and skills | reusable provider-neutral behavior |
| canonical agent governance knowledge | verified surface-to-authority routing and repository vocabulary |
| canonical agent governance prompts | reusable input and output contracts for recurring agent work |
| Provider Registry | provider identity and translation facts |
| Authored native provider documents | provider-specific loading and syntax |
| Generated native adapters | role translation and thin Claude skill pointers |
| Stage 99 Registry | document shape and lifecycle machine contract |
| Validators and suites | focused predicate execution and routing |

## Data Flow

Bootstrap은 root shim에서 공통 Agent 거버넌스 policy와 해당 provider adapter로 이동한다.
요청에 필요한 canonical role/skill과 active Spec/Task만 선택적으로 로드한다.
Canonical `SKILL.md`는 `name`, `description`과 기존 계약을 담은 `metadata`를
사용한다. Codex의 skill-local `allow_implicit_invocation: false`와 Claude의
`disable-model-invocation: true`가 명시적 호출을 요구하며, 검색 자체는 권한이나
관측된 runtime acceptance가 아니다.
Provider Registry의 translation fact가 native surface를 생성·검증하고, Stage 99
Registry가 repository 문서의 profile과 lifecycle을 검증한다. 실행 결과는
current Task와 검토된 Git diff로 되돌아온다.

## Deployment View

구현 surface는 tracked Markdown, YAML, JSON, TOML과 validation scripts다.
Provider sync와 governance tests는 projection freshness를 검사한다. 문서 또는
adapter 변경 자체는 Docker runtime, remote service, secret mutation을 요구하지
않는다.

## Quality Attributes

- **Determinism**: 동일 source와 registry에서 동일 projection과 verdict가
  나와야 한다.
- **Security**: adapter는 공통 Agent 거버넌스 approval boundary를 완화할 수 없다.
- **Maintainability**: policy, provider translation, document schema는 각각
  하나의 owner만 가진다.
- **Efficiency**: bootstrap은 전체 corpus가 아닌 request-relevant context를
  로드한다.
- **Recoverability**: 별도 snapshot이나 SHA pin 없이 Git diff와 history를
  사용한다.

## Traceability

- [REQ-0024 Agent Governance Standardization](../../01.requirements/0024-agent-governance-standardization.md)
- [ADR-0032 Canonical Agent Governance Home](../decisions/0032-canonical-agent-governance-home.md)
- [ADR-0034 Canonical Knowledge and Prompt Surfaces](../decisions/0034-canonical-knowledge-and-prompt-surfaces.md)
- [canonical agent governance bootstrap](../../../.agents/governance/bootstrap.md)
- [Stage 99 Registry](../../99.templates/registry.json)
