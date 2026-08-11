---
status: active
---

<!-- README Target: docs/05.operations/README.md -->

# Operations

> 도메인별로 Guide, Policy, Runbook을 함께 찾고 사고와 릴리스 증거로 연결하는 canonical Stage 05 인덱스

## Overview

`docs/05.operations/`는 운영자가 서비스 사용 맥락, 통제 기준, 실행 절차를
같은 stable subject identity 아래에서 찾는 canonical operations stage다. 최종
탐색 구조는 domain-first이며, 역할별 병렬 인덱스를 발행하지 않는다.

## Audience

- Operators
- Developers
- SREs
- Security Officers
- AI Agents

## Scope

### In Scope

- 서비스 사용, 설정, 온보딩 Guide
- 운영 통제, 예외, 검토 주기를 정의하는 Policy
- 검증, 복구, rollback, escalation을 위한 Runbook
- 실제 사고 packet과 사후 분석
- 실제 릴리스 artifact, 승인, rollout/rollback, 결과 증거

### Out of Scope

- 요구사항 정의 (`docs/01.requirements/`)
- 아키텍처 요구사항과 결정 기록 (`docs/02.architecture/`)
- 상세 기술 명세, Plan, Task (`docs/03.specs/`)
- secret, credential, token, 인증서 원문

## Structure

| Domain | Operations subjects |
| --- | --- |
| [00 Workspace](./00-workspace/README.md) | workspace-level setup, controls, release, and shared procedures |
| [01 Gateway](./01-gateway/README.md) | edge routing, proxy, certificate, and access operations |
| [02 Auth](./02-auth/README.md) | authentication and identity services |
| [03 Security](./03-security/README.md) | security controls, scanning, and response procedures |
| [04 Data](./04-data/README.md) | databases, storage, backup, and data services |
| [05 Messaging](./05-messaging/README.md) | messaging and notification services |
| [06 Observability](./06-observability/README.md) | monitoring, metrics, logs, and alerting |
| [07 Workflow](./07-workflow/README.md) | workflow and automation services |
| [08 AI](./08-ai/README.md) | AI services and model operations |
| [09 Tooling](./09-tooling/README.md) | testing, registry, synchronization, and IaC tooling |
| [10 Communication](./10-communication/README.md) | mail operations |
| [11 Laboratory](./11-laboratory/README.md) | dashboard and laboratory support services |
| [12 Infra Net](./12-infra-net/README.md) | infrastructure network standardization |
| [Incidents](./incidents/README.md) | incident packets and postmortems |
| [릴리스](./releases/README.md) | executed release evidence |

각 domain `README.md`가 subject navigation을 소유하며, subject 폴더에는
`README.md`를 만들지 않는다. subject의 기존 역할만
`<domain>/ops-<id>-<subject>/{guide,policy,runbook}.md`에 둔다.

## How to Work in This Area

1. 위 domain 인덱스에서 stable `ops-<id>-<subject>`를 찾는다.
2. 정상 사용 맥락과 common checks는 `guide.md`에 둔다.
3. 필수·금지 통제, 예외, 검토 주기는 `policy.md`에 둔다.
4. 순서 있는 절차, 기대 증거, rollback 또는 recovery, escalation은
   `runbook.md`에 둔다.
5. Guide의 `## Runbook Handoff`는 실제 sibling Runbook이 있고 그 절차로
   넘겨야 할 때만 작성한다. Runbook의 `## Automation Handoff`도 실제
   자동화 artifact와 검증 가능한 link가 있을 때만 작성한다.
6. 모든 subject가 세 역할을 모두 가질 필요는 없다. frozen inventory에
   존재하거나 별도 승인된 역할만 추가한다.
7. 사고는 `incidents/inc-<id>-<slug>/`, 실제 릴리스는
   `releases/rel-<id>-<slug>/` 아래에 기록한다.
8. 문서를 추가, 이동, 삭제하면 owning domain `README.md`와 관련 inbound
   link를 함께 갱신한다.

## Documentation Standards

- 한 leaf 문서는 하나의 primary role만 수행한다.
- Guide는 절차를 복제하지 않고 필요할 때 sibling Runbook으로 handoff한다.
- Policy는 명령 순서를 소유하지 않는다.
- Runbook은 evidence, rollback/recovery, escalation 기준을 포함한다.
- root와 domain README만 active Operations subject index를 발행한다.
- archive, generated summary, migration ledger의 immutable provenance는 current
  path rewrite 대상으로 취급하지 않는다.

## Related Documents

- [Docs index](../README.md)
- [Requirements](../01.requirements/README.md)
- [Architecture](../02.architecture/README.md)
- [Specs, Plans, and Tasks](../03.specs/README.md)
- [Operations templates](../99.templates/templates/operations/README.md)
- [Documentation protocol](../00.agent-governance/rules/documentation-protocol.md)
- [Stage authoring matrix](../00.agent-governance/rules/stage-authoring-matrix.md)
