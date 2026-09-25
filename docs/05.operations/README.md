---
title: "Operations"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-26"
layer: "operations"
---

<!-- README Target: docs/05.operations/README.md -->

# Operations

> 현재 워크스페이스를 안전하게 운영하는 사람이 역할(이해, 통제, 실행, 사건)로 문서를 찾는 Stage 05 인덱스

## Overview

`docs/05.operations/`는 이 워크스페이스를 운영하는 사람을 위한 계층이다.
먼저 무엇이 필요한지로 찾는다. 맥락과 전제를 이해하려면 Guide, 허용 여부와
승인·보안·예외 경계를 확인하려면 Policy, 실행할 명령 흐름이 필요하면
Runbook, 실제 사건의 사실과 원인 분석은 Incident와 Postmortem이다.
구조 결정은 [ADR-0043](../02.architecture/decisions/0043-operations-role-layout.md)이
소유한다.

## Audience

- Operators
- Developers
- SREs
- Security Officers
- AI Agents

## Scope

### In Scope

- 서비스와 작업 공간의 정상 운영 맥락, 전제, 공통 점검 (Guide)
- 허용·금지, 승인, 보안, 예외, 검토 주기 (Policy)
- 사용 조건, 실행 위치, 입력, 명령 순서, 기대 결과, 중단, 검증, 복구,
  에스컬레이션 (Runbook)
- 실제 사고의 사실 기록과, 해결된 사건의 원인 분석과 재발 방지 (Incident, Postmortem)
- 배포 결과는 Task, `CHANGELOG.md`, Git tag와 관련 Runbook evidence로 추적한다.

### Out of Scope

- 요구사항 정의 (`docs/01.requirements/`)
- 아키텍처 요구사항과 결정 기록 (`docs/02.architecture/`)
- 상세 기술 명세, Plan, Task (`docs/03.specs/`)
- 에이전트 실행 규칙 (`.agents/`)
- secret, credential, token, 인증서 원문

## Structure

| Route | Purpose |
| --- | --- |
| [Guides](./guides/README.md) | 정상 운영 이해와 전제 |
| [Policies](./policies/README.md) | 허용·금지, 승인, 보안, 예외, 검토 |
| [Runbooks](./runbooks/README.md) | 실행할 명령 흐름, 검증, 복구, 에스컬레이션 |
| [Incidents](./incidents/README.md) | 사건 사실 기록과 같은 묶음의 Postmortem |

```text
docs/05.operations/
├── guides/####-<slug>.md
├── policies/####-<slug>.md
├── runbooks/####-<slug>.md
└── incidents/<year>/inc-####-<slug>/{incident,postmortem}.md
```

`####`는 문서 자신의 artifact 번호다(`GDE-####`, `POL-####`, `RUN-####`).
같은 slug는 역할 디렉터리를 넘어 같은 subject를 가리킨다. 도메인은 경로가
아니라 각 역할 인덱스의 분류다.

### Artifact Boundaries

- Guide는 정상 운영 맥락과 이해를 소유하고, 실행 절차는 같은 slug의
  Runbook으로 넘긴다.
- Policy는 의무·금지·승인·예외·검토 주기를 소유하고 명령 순서를 소유하지 않는다.
- Runbook은 순서 있는 실행, 관찰 증거, rollback/recovery, escalation을 소유한다.
- Incident는 특정 사건의 관찰·영향·대응 타임라인을, Postmortem은 원인·교훈·
  재발 방지 조치를 소유한다.
- 독자 목적, 역할별 작성 기준, Incident/Postmortem 후속 조치 기준은
  [공통 Agent 거버넌스 작성 정책](../../.agents/governance/documentation-protocol.md#role-specific-authoring)이 소유한다.
  Guide의 주된 독자 필요를 본문에 명시하며 Diátaxis의 technical reference를
  Stage 90의 증거 분류와 혼동하지 않는다.

### External Release Evidence

이 저장소는 [공통 Agent 거버넌스의 external-release-evidence 정책](../../.agents/governance/documentation-protocol.md#release-evidence-boundary)을
사용한다. [Release Runbook](runbooks/0009-release-management.md)은
반복 절차를, 현재 Task는 특정 실행의 검증과 결과를 소유한다. CHANGELOG, tag,
CI 링크는 관찰된 사실의 근거이며 로컬 검증만으로 배포 성공을 주장하지 않는다.
별도 Release 문서 프로필은 도입하지 않는다.

## How to Work in This Area

1. 필요한 역할의 인덱스([Guides](./guides/README.md),
   [Policies](./policies/README.md), [Runbooks](./runbooks/README.md))에서
   도메인 분류로 문서를 찾는다.
2. 정상 운영 맥락과 공통 점검은 `guides/`에 둔다.
3. 필수·금지 통제, 승인, 예외, 검토 주기는 `policies/`에 둔다.
4. 순서 있는 절차, 기대 증거, rollback 또는 recovery, escalation은
   `runbooks/`에 둔다.
5. Guide의 `## Runbook Handoff`는 실제 Runbook이 있고 그 절차로 넘겨야 할
   때만 작성한다. Runbook의 `## Automation Handoff`도 실제 자동화 artifact와
   검증 가능한 link가 있을 때만 작성한다.
6. 모든 subject가 세 역할을 모두 가질 필요는 없다. 현재 운영 책임에 필요한
   역할만 등록된 Stage 99 프로필로 추가하고, 빈 문서를 만들지 않는다.
7. 사고는 `incidents/<year>/inc-####-<slug>/` 아래에 기록한다.
8. 문서를 추가, 이동, 삭제하면 해당 역할 인덱스와 관련 inbound link를 함께
   갱신한다.

### Documentation Standards

- 한 leaf 문서는 하나의 primary role만 수행한다.
- 같은 절차나 통제를 여러 문서에 복제하지 않고 소유 문서로 링크한다.
- 이 README, 세 역할 인덱스, incidents README만 Operations 인덱스를 발행한다.
- 과거 경로와 실행 이력은 Git과 Stage 98에서 찾으며 현재 Operations 권한으로
  사용하지 않는다.

## Related Documents

- [Docs index](../README.md)
- [Requirements](../01.requirements/README.md)
- [Architecture](../02.architecture/README.md)
- [Specs, Plans, and Tasks](../03.specs/README.md)
- [Template catalog](../99.templates/templates/README.md)
- [Documentation protocol](../../.agents/governance/documentation-protocol.md)
- [Stage authoring matrix](../../.agents/governance/stage-authoring-matrix.md)
