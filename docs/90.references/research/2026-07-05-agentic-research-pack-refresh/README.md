---
status: active
---
<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/README.md -->

# Agentic Engineering Research Pack

> `hy-home.docker`의 하네스 엔지니어링, 루프 엔지니어링, provider adapter, SDLC, QA/CI 기준을 정리한 source-backed reference pack

## Overview

`docs/90.references/research/2026-07-05-agentic-research-pack-refresh`는 `hy-home.docker`의 agent-first engineering 체계를 외부 자료와 비교해 읽기 위한 research pack입니다. 이 pack은 현재 저장소의 목적, 역할, CI/CD, QA, Automation, Formatting, 운영 계약, 템플릿, 스크립트, 통합 가이드, SDLC, 거버넌스, 체계, 규칙을 repo-local evidence로 정리하고, 하네스/루프/스펙 주도 개발/품질 게이트/provider 구현 현황을 외부 source와 연결합니다.

이 pack은 active policy가 아닙니다. 발견된 개선점은 `Potential Follow-up / Gap`으로 남기며, 실제 정책이나 실행 계획 변경은 별도 승인된 canonical stage 문서에서 다룹니다.

## Category Role

`docs/90.references/research/2026-07-05-agentic-research-pack-refresh`는 하네스 엔지니어링과 루프 엔지니어링을 중심으로 한 agent-first workspace research pack입니다. 이 category는 현재 provider/runtime/governance 상태를 설명하는 보조 reference이며, Stage 00 policy, Stage 04 execution evidence, Stage 05 operations procedure를 대체하지 않습니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- repo-local workspace baseline 분석
- 하네스 엔지니어링 구성 요소 분석
- 루프 엔지니어링과 feedback loop 분석
- spec-driven development와 SDLC 분석
- CI/CD, QA, formatting, quality gate 분석
- Docker Compose, infrastructure harness, security governance, automation, pipeline, workflow 분석
- Claude, Codex, Gemini provider 구현 비교
- 공통 provider-neutral 환경과 규칙을 만들기 위한 요소 정리

### Out of Scope

- `docs/00.agent-governance/` 정책 직접 변경
- `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/` 후속 보완
- runtime provider 설정 변경
- secret 값, credential, token, private key, shell history, raw log

## Structure

```text
2026-07-05-agentic-research-pack-refresh/
├── README.md                            # This file
├── workspace-baseline.md                # Repo-local purpose, roles, gates, contracts
├── harness-engineering.md               # Harness components and application analysis
├── loop-engineering.md                  # Agent/eval/CI/human feedback loop analysis
├── spec-driven-sdlc.md                  # Spec-driven development and SDLC mapping
├── quality-ci-formatting.md             # QA, CI/CD, formatting, secure quality gates
├── provider-implementation-comparison.md # Claude, Codex, Gemini comparison
├── docker-compose-infrastructure.md      # Docker Compose and infrastructure harness analysis
├── security-governance.md                # Secure SDLC and security governance analysis
└── automation-pipeline-workflow.md       # Automation, pipeline, and workflow analysis
```

## Current References

- [workspace-baseline.md](./workspace-baseline.md) - workspace 목적, 역할, CI/CD, QA, Automation, 운영 계약, 템플릿, 스크립트, SDLC, 거버넌스 baseline
- [harness-engineering.md](./harness-engineering.md) - test/eval/runtime harness와 저장소 적용 요소 분석
- [loop-engineering.md](./loop-engineering.md) - agent loop, eval loop, CI loop, human approval loop 분석
- [spec-driven-sdlc.md](./spec-driven-sdlc.md) - spec-driven development, SDLC, traceability 분석
- [quality-ci-formatting.md](./quality-ci-formatting.md) - CI/CD, QA, formatting, secure quality gate 분석
- [provider-implementation-comparison.md](./provider-implementation-comparison.md) - Claude, Codex, Gemini provider 현황과 공통 체계 분석
- [docker-compose-infrastructure.md](./docker-compose-infrastructure.md) - Docker Compose, infrastructure harness, profiles, networks, secrets, validation, hardening 분석
- [security-governance.md](./security-governance.md) - secure SDLC reference frameworks, workflow security, secret boundaries, approval evidence 분석
- [automation-pipeline-workflow.md](./automation-pipeline-workflow.md) - automation, pipeline, workflow loop, provider hook, local/remote action boundary 분석

## Reading Order

1. [workspace-baseline.md](./workspace-baseline.md)에서 이 저장소의 현재 체계를 먼저 확인합니다.
2. [harness-engineering.md](./harness-engineering.md)와 [loop-engineering.md](./loop-engineering.md)에서 개념적 구조를 확인합니다.
3. [spec-driven-sdlc.md](./spec-driven-sdlc.md)와 [quality-ci-formatting.md](./quality-ci-formatting.md)에서 stage-gate와 검증 루프를 비교합니다.
4. [docker-compose-infrastructure.md](./docker-compose-infrastructure.md), [security-governance.md](./security-governance.md), [automation-pipeline-workflow.md](./automation-pipeline-workflow.md)에서 targeted reference를 확인합니다.
5. [provider-implementation-comparison.md](./provider-implementation-comparison.md)에서 Claude, Codex, Gemini adapter 차이를 확인합니다.

## How to Work in This Area

1. 이 pack의 문서는 active policy가 아니라 reference라는 경계를 유지합니다.
2. 최신 provider 기능을 인용할 때는 공식 문서를 다시 확인합니다.
3. 새 non-README reference는 closed-surface contract에 맞춰 영어로 작성합니다.
4. repo-local 사실은 root README, Stage 00 governance, provider notes, scripts, CI workflow에서 확인합니다.
5. 다른 stage 수정이 필요하면 이 pack에서 직접 고치지 않고 gap으로 기록합니다.
6. 새 문서를 추가하면 이 README와 상위 [research README](../README.md)를 갱신합니다.
7. 변경 후 `bash scripts/validation/check-repo-contracts.sh`를 실행합니다.

## Related Documents

- [research references](../README.md)
- [90.references](../../README.md)
- [agent governance hub](../../../00.agent-governance/README.md)
- [HAFE specification](../../../03.specs/094-harness-agent-first-engineering/spec.md)
- [HAFE operations guide](../../../05.operations/guides/00-workspace/harness-agent-first-engineering.md)
- [HAFE operations policy](../../../05.operations/policies/00-workspace/harness-agent-first-engineering.md)
