---
title: "Operations"
version: "1.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "operations"
---

<!-- README Target: docs/05.operations/README.md -->

# Operations

> 도메인별로 Guide, Policy, Runbook을 함께 찾고 사고 증거로 연결하는 canonical Stage 05 인덱스

## Overview

`docs/05.operations/`는 운영자가 서비스 사용 맥락, 통제 기준, 실행 절차를
같은 stable subject identity 아래에서 찾는 canonical operations stage다. 최종
탐색 구조는 `catalog/` 아래의 domain-first이며, 역할별 병렬 인덱스를
발행하지 않는다. Incident event record는 catalog 밖에 둔다.

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
- 배포 결과는 Task, `CHANGELOG.md`, Git tag와 관련 Runbook evidence로 추적한다.

### Out of Scope

- 요구사항 정의 (`docs/01.requirements/`)
- 아키텍처 요구사항과 결정 기록 (`docs/02.architecture/`)
- 상세 기술 명세, Plan, Task (`docs/03.specs/`)
- secret, credential, token, 인증서 원문

## Structure

| Route | Purpose |
| --- | --- |
| [Catalog](./catalog/README.md) | domain별 current Operations subjects |
| [Incidents](./incidents/README.md) | incident packets and postmortems |

각 domain `README.md`가 subject navigation을 소유하며, subject 폴더에는
`README.md`를 만들지 않는다. subject의 기존 역할만
`catalog/<domain>/####-<subject>/{guide,policy,runbook}.md`에 둔다.

### Artifact Boundaries

- Guide는 정상 사용 맥락과 이해 중심의 안내를 소유한다.
- Policy는 의무·금지·예외·검토 주기 같은 통제를 소유한다.
- Runbook은 순서 있는 실행, 관찰 증거, rollback/recovery, escalation을 소유한다.
- Incident는 특정 사건의 관찰·영향·대응 타임라인을, Postmortem은 원인·교훈·
  재발 방지 조치를 소유한다.
- 독자 목적, 역할별 작성 기준, Incident/Postmortem 후속 조치 기준은
  [Stage 00 작성 정책](../00.agent-governance/policies/documentation-protocol.md#role-specific-authoring)이 소유한다.
  Guide의 주된 독자 필요를 본문에 명시하며 Diátaxis의 technical reference를
  Stage 90의 증거 분류와 혼동하지 않는다.

### External Release Evidence

이 저장소는 [Stage 00의 external-release-evidence 정책](../00.agent-governance/policies/documentation-protocol.md#release-evidence-boundary)을
사용한다. [Release Runbook](catalog/00-workspace/0009-release-management/runbook.md)은
반복 절차를, 현재 Task는 특정 실행의 검증과 결과를 소유한다. CHANGELOG, tag,
CI 링크는 관찰된 사실의 근거이며 로컬 검증만으로 배포 성공을 주장하지 않는다.
별도 Release 문서 프로필은 도입하지 않는다.

## How to Work in This Area

1. [Catalog](./catalog/README.md)의 domain 인덱스에서 stable
   `####-<subject>`를 찾는다.
2. 정상 사용 맥락과 common checks는 `guide.md`에 둔다.
3. 필수·금지 통제, 예외, 검토 주기는 `policy.md`에 둔다.
4. 순서 있는 절차, 기대 증거, rollback 또는 recovery, escalation은
   `runbook.md`에 둔다.
5. Guide의 `## Runbook Handoff`는 실제 sibling Runbook이 있고 그 절차로
   넘겨야 할 때만 작성한다. Runbook의 `## Automation Handoff`도 실제
   자동화 artifact와 검증 가능한 link가 있을 때만 작성한다.
6. 모든 subject가 세 역할을 모두 가질 필요는 없다. 현재 운영 책임에
   필요한 역할만 등록된 Stage 99 프로필로 추가한다.
7. 사고는 `incidents/<year>/inc-####-<slug>/` 아래에 기록한다.
8. 문서를 추가, 이동, 삭제하면 owning domain `README.md`와 관련 inbound
   link를 함께 갱신한다.

### Documentation Standards

- 한 leaf 문서는 하나의 primary role만 수행한다.
- Guide는 절차를 복제하지 않고 필요할 때 sibling Runbook으로 handoff한다.
- Policy는 명령 순서를 소유하지 않는다.
- Runbook은 evidence, rollback/recovery, escalation 기준을 포함한다.
- root, catalog, domain README만 active Operations index를 발행한다.
- 과거 경로와 실행 이력은 Git에서 복구하며 current Operations 권한으로
  사용하지 않는다.

## Related Documents

- [Docs index](../README.md)
- [Requirements](../01.requirements/README.md)
- [Architecture](../02.architecture/README.md)
- [Specs, Plans, and Tasks](../03.specs/README.md)
- [Template catalog](../99.templates/templates/README.md)
- [Documentation protocol](../00.agent-governance/policies/documentation-protocol.md)
- [Stage authoring matrix](../00.agent-governance/policies/stage-authoring-matrix.md)
