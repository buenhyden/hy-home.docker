---
profile_id: architecture-description
status: active
artifact_id: AD-0027
artifact_type: architecture-description
parent_ids:
  - REQ-0024
created: 2026-06-01
updated: 2026-09-01
---
# Agent Governance Canonical Adapter Architecture

## Context and Stakeholders

여러 AI provider가 같은 저장소를 수정하더라도 정책, 역할, skill, SDLC,
승인 경계는 하나여야 한다. Maintainer는 Stage 00에서 규범을 검토하고,
Agent는 provider adapter를 통해 동일한 규범을 native runtime 형식으로
소비하며, reviewer는 projection drift를 독립적으로 검증한다.

## System Boundaries

- Stage 00은 policy, workflow, canonical roles/skills, provider boundary를
  소유한다.
- Stage 99는 docs profile, path, identity, lifecycle, template의 typed contract를
  소유한다.
- `.claude/`, `.codex/`, `.agents/`는 projection 또는 runtime mechanics를
  소유하지만 정책을 정의하지 않는다.
- Current Task는 실행 결과를, Git은 diff와 삭제 본문의 recovery를 소유한다.
- User-global configuration, credential, provider availability, deployment
  state는 이 아키텍처 밖이다.

## Components

| Component | Responsibility |
| --- | --- |
| Stage 00 bootstrap and policies | authority resolution, safety, workflow |
| Stage 00 roles and skills | reusable provider-neutral behavior |
| Provider Registry | provider identity and translation facts |
| Provider adapters | native prompt/config/hook projection |
| Stage 99 Registry | document shape and lifecycle machine contract |
| Validators and suites | focused predicate execution and routing |

## Data Flow

Bootstrap은 root shim에서 Stage 00 policy와 해당 provider adapter로 이동한다.
요청에 필요한 canonical role/skill과 active Spec/Task만 선택적으로 로드한다.
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
- **Security**: adapter는 Stage 00 approval boundary를 완화할 수 없다.
- **Maintainability**: policy, provider translation, document schema는 각각
  하나의 owner만 가진다.
- **Efficiency**: bootstrap은 전체 corpus가 아닌 request-relevant context를
  로드한다.
- **Recoverability**: 별도 snapshot이나 SHA pin 없이 Git diff와 history를
  사용한다.

## Traceability

- [REQ-0024 Agent Governance Standardization](../../01.requirements/0024-agent-governance-standardization.md)
- [ADR-0029 Workspace Governance Authority](../decisions/0029-workspace-governance-authority.md)
- [Stage 00 bootstrap](../../00.agent-governance/policies/bootstrap.md)
- [Stage 99 Registry](../../99.templates/registry.json)
