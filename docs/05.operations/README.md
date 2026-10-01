---
title: "Operations"
version: "2.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
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

- 운영자
- 개발자
- SREs
- 보안 담당자
- AI 에이전트

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

### Find by operating scope

| 탐색 범위 | 시작 경로 | 다음 선택 |
| --- | --- | --- |
| 전체 시스템 | [Guide 공통 분류](guides/README.md#cross-cutting-system-and-lifecycle) | 시스템 운영 설명, 백업·복구, 업데이트 이해 |
| 공통 통제 | [Policy 공통 분류](policies/README.md#cross-cutting-system-and-lifecycle) | profile 선택, 자원·보안, 백업, 버전 변경의 허용 경계 |
| 시스템 절차 | [Runbook 공통 분류](runbooks/README.md#cross-cutting-system-and-lifecycle) | 기동·재부팅, 여러 서비스 동시 장애 진단, 용량·복구·업데이트 |
| 티어 | [Guide](guides/README.md), [Policy](policies/README.md), [Runbook](runbooks/README.md)의 01–12 분류 | 해당 티어 서비스 subject와 역할별 책임 |
| 개별 서비스 | 각 역할 인덱스의 subject 행 | 구현 소유 Guide → 적용 Policy → 실행 Runbook |
| 작업 공간·공통 연결 | 각 역할 인덱스의 번호 없는 공통 분류 | 개발·운영 도구, network·외부 연계 |

시스템 Guide가 요청·인증·데이터 경로와 티어 의존성을 설명한다. 09는 플랫폼
도구, 10은 운영 메일, 11은 Quality이며 관리·실험 도구는 기능별 tier에서 찾는다. 티어 번호는
기동 순서가 아니며 공통 주제를 임의 티어에 넣지 않는다. 인증 장애는 시스템
진단에서 앱 자체 로그인과 proxy 인증으로 나누고, 실제 복구는 해당 서비스
절차로 넘긴다. 사건 기록은 [Incidents](incidents/README.md)를 사용한다.

`####`는 문서 자신의 artifact 번호다(`GDE-####`, `POL-####`, `RUN-####`).
같은 slug는 역할 디렉터리를 넘어 같은 subject를 가리킨다. 도메인은 경로가
아니라 각 역할 인덱스의 분류다.

### Artifact Boundaries

- Guide는 정상 운영 맥락과 이해를 소유하고 실행 절차는 같은 slug의
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
사용한다. [Release Runbook](runbooks/README.md)(`0009-release-management.md`)은
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
6. Compose 서비스가 연결된 subject는 Guide/Policy/Runbook 세 역할을 모두
   유지한다. 서비스 연결이 없는 시스템·공통·작업 공간 subject는 필요한 역할만
   등록하고 빈 문서를 만들지 않는다. 공통 내용은 소유 문서로 연결하고 각 서비스의
   적용 조건·예외·차이는 해당 역할 문서에 남긴다.
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
