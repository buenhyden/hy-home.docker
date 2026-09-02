---
title: Architecture Decision Records
type: common/readme
layer: architecture
status: active
owner: "@buenhyden"
---

# Architecture Decision Records

## Overview

`docs/02.architecture/decisions`는 중요한 아키텍처 선택의 맥락과 동인,
고려한 대안, 선택, 근거, 결과, 확인 방법과 supersession을 보존한다.
ADR은 구현 명세나 운영 절차가 아니다.

## Audience

- System Architects
- Developers
- Reviewers
- AI Agents

## Scope

이 디렉터리는 현재 26개의 ADR을 보유한다. 각 ADR은 하나의 material
choice를 소유하고 실제 Architecture Description을 parent로 연결한다.

## Structure

```text
docs/02.architecture/decisions/
├── 0001-traefik-nginx-hybrid.md
├── 0002-keycloak-oauth2-proxy-choice.md
├── ...
├── 0027-stage-00-canonical-adapter-model.md
├── 0028-local-isolated-readiness-evidence.md
├── 0029-workspace-governance-authority.md
├── 0030-tombstone-retirement-record.md
└── README.md
```

## Current Inventory

- `ADR-0001`부터 `ADR-0011`: 기본 tier와 service selection decisions.
- `ADR-0015`부터 `ADR-0026`: analytics, hardening, HA와 network decisions.
- [`ADR-0027`](./0027-stage-00-canonical-adapter-model.md):
  ADR-0029가 supersede한 Stage 00 adapter decision. 이 decision log에 유지한다.
- [`ADR-0028`](./0028-local-isolated-readiness-evidence.md):
  local-isolated readiness evidence strategy.
- [`ADR-0029`](./0029-workspace-governance-authority.md):
  active workspace governance authority decision; ADR-0027을 supersede한다.
- [`ADR-0030`](./0030-tombstone-retirement-record.md):
  은퇴 기록으로서의 Tombstone decision.

## How to Work in This Area

1. 상위 [Architecture Description](../descriptions/README.md)을 확인한다.
2. 기존 ADR이 같은 선택을 이미 소유하는지 확인한다.
3. 새 ADR은 [`adr.template.md`](../../99.templates/templates/architecture/decision.template.md)를 사용한다.
4. 선택, alternatives, rationale와 consequences를 보존한다.
5. 이전 결정을 대체하면 stable `supersedes` metadata와 양방향 문서 링크로
   supersession을 명시한다.

## Documentation Standards

- `<4-digit-id>-<slug>.md`, `artifact_id: ADR-<4-digit-id>`,
  `artifact_type: adr`을 일치시킨다.
- `parent_ids`는 실제 Architecture Description만 포함한다.
- 구현 계약과 검증 기준은 관련 Spec, 운영 절차는 Stage 05에 둔다.
- 결정 확인 근거가 없는 runtime 상태는 주장하지 않는다.

## AI Agent Guidance

Agent는 결정 내용을 요약하면서 alternatives, rationale, consequences 또는
supersession을 삭제하지 않는다. 새 선택이 필요한 경우 기존 ADR을 덮어쓰지
말고 별도 승인된 ADR과 명시적 supersession을 사용한다.

## Related Documents

- [Architecture](../README.md)
- [Architecture Descriptions](../descriptions/README.md)
- [Product Requirements](../../01.requirements/README.md)
- [Specifications](../../03.specs/README.md)
- [Operations](../../05.operations/README.md)
- [ADR Template](../../99.templates/templates/architecture/decision.template.md)
