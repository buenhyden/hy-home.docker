---
title: "Harness / Agent-first Engineering Operations Policy"
version: "1.3.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0004"
parent_ids:
- "SPEC-0094"
created: "2026-06-04"
---

# Harness / Agent-first Engineering Operations Policy

## Overview

이 운영 정책은 `hy-home.docker`의 하네스 엔지니어링과 Agent-first Engineering 계약을 유지하기 위한 통제 기준을 정의한다.

canonical agent governance는 `.agents/`에 있다: governance policy가 규칙을 소유하고,
Provider Registry가 provider identity, model, permission translation을 소유하며,
role이 각자의 tier와 work profile을 소유한다. 이 문서는 운영 측면만 소유한다 —
하네스 실행·검증의 승인 경계와 실패 보고 기준이다. 실제 순서는 Runbook이 소유한다.

아래 표는 canonical 규칙의 소유자로 연결한다. 모델·permission·scope를 이 문서에
별도 값으로 복제하지 않는다.

## Scope

이 정책은 다음 대상에 적용한다.

- Agent entry shim.
- Governance policy, role, skill, provider registry.
- Claude runtime mirror.
- Codex hook/context surface.
- Stage documentation과 validator.
- `AGENTS.md`, `CLAUDE.md`
- `.claude/**`
- `.codex/**`
- `.agents/**`
- `docs/03.specs/**`
- `docs/03.specs/[0-9][0-9][0-9][0-9]-*/plan.md`
- `docs/03.specs/[0-9][0-9][0-9][0-9]-*/tasks/tsk-[0-9][0-9][0-9][0-9]-*.md`
- `docs/05.operations/guides/[0-9][0-9][0-9][0-9]-*.md`
- `docs/05.operations/policies/[0-9][0-9][0-9][0-9]-*.md`
- `docs/05.operations/runbooks/[0-9][0-9][0-9][0-9]-*.md`
- `scripts/validation/check-*.sh`, `scripts/hardening/check-all-hardening.sh`, `scripts/validation/validate-docker-compose.sh`

## Rules

| Control | Requirement |
| --- | --- |
| Thin root shims | Root 파일은 상세 policy를 `.agents/`와 runtime overlay에 위임한다. |
| Runtime mirror parity | Native role adapter와 thin Claude skill pointer는 authored `.agents` source와 동기화 상태를 유지한다; canonical 파일은 renderer output이 되지 않는다. |
| Runtime parity scope | Repository check는 catalog, model, scope import, protocol-reference parity를 증명한다; 모든 runtime 문서의 semantic parity를 증명하지는 않는다. |
| Model selection | role의 `work_profile`과 Provider Registry의 provider mapping을 따른다. 현재 모델·계층·개수를 별도로 선언하지 않는다. |
| Scope imports | 각 runtime agent는 정확히 하나의 primary scope를 import한다. |
| Hook safety | Runtime hook은 shell command substitution 부작용 없이 실제 payload shape를 파싱해야 한다. |
| Codex boundary | Governance는 Codex catalog를 채택했다: Provider Registry가 native agent pattern을 선언하고 renderer가 role당 하나의 adapter를 hook configuration 옆에 작성한다. Codex surface가 무엇을 담는지는 이 문서가 아니라 registry가 결정한다. |
| Template-first docs | 새 stage 문서는 `docs/99.templates/`를 사용하고 parent README 파일을 갱신한다. |
| Source-label prevention | Active runtime/governance 파일은 외부 harness source label을 참조하지 않아야 한다. |
| Graph context health | Graphify는 health가 clean할 때만 navigation aid가 된다; contaminated output은 advisory로 남으며 tracked source 및 canonical 문서와 대조 검증해야 한다. |
| Infra validation scope | 적용 gate의 현재 선택 범위를 기록한다. Compose validator와 baseline script의 기본 범위가 다르며 범위 밖 remediation은 별도 승인한다. |
| AI Agent limits | [Agentic Engineering Policy](../../../.agents/governance/agentic.md#execution-rules)가 소유하며, Graphify의 경우 [Environment Constraints](../../../.agents/governance/environment-constraints.md#4-graphify)가 소유한다. |

자동 답변 점수 QA와 완료 사건의 전용 증명은 현재 delivery gate가 아니다.
현재 문서·Docker 계약과 이를 지원하는 회귀의 허용 범위, 폐기 순서, 단계별 실행은
[quality policy](../../../.agents/governance/quality-standards.md)가 소유한다.
정적 source나 수동 비교를 native 호출·복구 성공으로 기록하지 않는다.
Docker·실제 환경 접근은 해당 Task의 승인 범위에서 실행하며 미실행은 성공이 아니다.

## Exceptions

- 과거 Stage 90 또는 Stage 98 evidence는 명확히 non-authoritative일 때 이전 source label을 언급할 수 있다.
- `bash scripts/knowledge/report-graphify-health.sh`는 `status=advisory`를 보고할 수 있다; 이는 repository validation 실패가 아니라 신뢰도 하향 evidence다.
- CLI를 사용할 수 없을 때 `graphify` refresh를 건너뛸 수 있지만 건너뛴 사실은 보고해야 한다.
- `rtk`는 active shell에서 사용할 수 없을 때 우회할 수 있다.
- 승인되지 않은 Compose/include/IP remediation은 이 하네스 점검의 실행 범위가 아니다.

### Verification

변경 영향에 맞춰 quality policy와 canonical public plan이 선택한 검사만 수행한다.
[Runbook](../runbooks/0004-harness-agent-first-engineering.md#procedure)은 승인된
관측의 실행 경로를 안내하며 모든 변경에 전체 hook/runtime bundle을 요구하지 않는다.

### Review Cadence

- 현재 owner나 계약이 바뀌면 영향받는 소비자와 필요한 회귀를 검토한다.
- 완료 여부는 현재 Task의 실제 필수 증거와 독립 검토로 판정하며 같은 입력의 aggregate QA를 반복하지 않는다.
- `.claude`, `.codex`, 또는 canonical agent governance role/skill catalog가 바뀌면 이 policy를 검토한다.
- scope 밖 infra profile 실패는 HAFE acceptance criteria를 조용히 확장하는 대신 별도로 기록한다.

### Traceability

- 과거 구현 출처: [Harness and Agent-first Engineering Outcome](../../98.archive/completed/03.specs/0094-harness-agent-first-engineering/spec.md) (`SPEC-0094`)
- 같은 주제: [Guide](../guides/0004-harness-agent-first-engineering.md) (`GDE-0004`), [Runbook](../runbooks/0004-harness-agent-first-engineering.md) (`RUN-0004`)

## Related Documents

- [Operations index](../README.md)
- [Usage guide](../guides/0004-harness-agent-first-engineering.md)
