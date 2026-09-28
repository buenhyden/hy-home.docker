---
title: "Harness / Agent-first Engineering Operations Policy"
version: "1.1.3"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
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
하네스를 언제 실행하는지, 어떻게 점검하는지, 점검이 실패하면 무엇을 하는지.

그래서 아래 통제 항목은 규칙을 다시 서술하는 대신 각 항목의 소유자를 가리킨다.
canonical 규칙을 프로즈로 요약한 통제는 결국 그 규칙과 어긋났다: model row는
Registry가 표현한 적 없는 계층에 이름을 붙였고 Codex row는 Registry가 이미 채택한
카탈로그를 여전히 금지했다. 소유자를 가리키는 통제는 그런 식으로 어긋날 수 없다.

## Policy Scope

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

## Controls

| Control | Requirement |
| --- | --- |
| Thin root shims | Root 파일은 상세 policy를 `.agents/`와 runtime overlay에 위임한다. |
| Runtime mirror parity | Native role adapter와 thin Claude skill pointer는 authored `.agents` source와 동기화 상태를 유지한다; canonical 파일은 renderer output이 되지 않는다. |
| Runtime parity scope | Repository check는 catalog, model, scope import, protocol-reference parity를 증명한다; 모든 runtime 문서의 semantic parity를 증명하지는 않는다. |
| Model selection | 각 role은 `work_profile`을 선언하고 Provider Registry가 그 profile을 provider model에 매핑한다. 이 문서는 매핑을 다시 서술하지 않는다: 매핑을 supervisor model 하나와 worker model 하나로 요약한 결과는 worker 열세 개 중 여섯 개에서 틀렸다. `adversarial-review` role은 supervisor와 같은 tier로 resolve되고 `routine-validation`은 나머지보다 낮은 tier로 resolve되기 때문이다. |
| Scope imports | 각 runtime agent는 정확히 하나의 primary scope를 import한다. |
| Hook safety | Runtime hook은 shell command substitution 부작용 없이 실제 payload shape를 파싱해야 한다. |
| Codex boundary | Governance는 Codex catalog를 채택했다: Provider Registry가 native agent pattern을 선언하고 renderer가 role당 하나의 adapter를 hook configuration 옆에 작성한다. Codex surface가 무엇을 담는지는 이 문서가 아니라 registry가 결정한다. |
| Template-first docs | 새 stage 문서는 `docs/99.templates/`를 사용하고 parent README 파일을 갱신한다. |
| Source-label prevention | Active runtime/governance 파일은 외부 harness source label을 참조하지 않아야 한다. |
| Graph context health | Graphify는 health가 clean할 때만 navigation aid가 된다; contaminated output은 advisory로 남으며 tracked source 및 canonical 문서와 대조 검증해야 한다. |
| Infra validation scope | HAFE completion은 default/core Compose와 지원되는 hardening tier에 의존할 수 있다; `10-communication` 같은 미편입 profile은 별도 infra remediation이 필요하다. |
| AI Agent limits | [Agentic Engineering Policy](../../../.agents/governance/agentic.md#execution-rules)가 소유하며, Graphify의 경우 [Environment Constraints](../../../.agents/governance/environment-constraints.md#4-graphify)가 소유한다. |

## Exceptions

- 과거 Stage 90 또는 Stage 98 evidence는 명확히 non-authoritative일 때 이전 source label을 언급할 수 있다.
- `bash scripts/knowledge/report-graphify-health.sh`는 `status=advisory`를 보고할 수 있다; 이는 repository validation 실패가 아니라 신뢰도 하향 evidence다.
- CLI를 사용할 수 없을 때 `graphify` refresh를 건너뛸 수 있지만 건너뛴 사실은 보고해야 한다.
- `rtk`는 active shell에서 사용할 수 없을 때 우회할 수 있다.
- `10-communication` compose/include/IP remediation은 infra change로 명시적으로 scope되지 않는 한 HAFE 범위 밖이다.

## Verification

[Runbook §Procedure](../runbooks/0004-harness-agent-first-engineering.md#procedure)에 나열된 hook, runtime, repository contract check는 harness 또는 Agent-first change를 승인하기 전에 모두 통과해야 한다.

## Review Cadence

- root, governance, runtime, provider, script, stage documentation change 이후 repository contract check를 실행한다.
- 광범위한 harness 또는 Agent-first migration 완료를 선언하기 전에 전체 verification bundle을 다시 실행한다.
- `.claude`, `.codex`, 또는 canonical agent governance role/skill catalog가 바뀌면 이 policy를 검토한다.
- scope 밖 infra profile 실패는 HAFE acceptance criteria를 조용히 확장하는 대신 별도로 기록한다.

## Traceability

- Declared parent: [Harness and Agent-first Engineering Outcome](../../98.archive/completed/03.specs/0094-harness-agent-first-engineering/spec.md) (`SPEC-0094`)
- Subject peers: [Guide](../guides/0004-harness-agent-first-engineering.md) (`GDE-0004`), [Runbook](../runbooks/0004-harness-agent-first-engineering.md) (`RUN-0004`)

## Related Documents

- [Operations index](../README.md)
- [Usage guide](../guides/0004-harness-agent-first-engineering.md)
