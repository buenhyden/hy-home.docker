---
title: Stage 00 Canonical Adapter Model
version: 1.0.0
type: sdlc/architecture-decision
layer: architecture
status: superseded
owner: "@buenhyden"
artifact_id: ADR-0027
parent_ids:
  - AD-0027
created: 2026-06-01
updated: 2026-09-01
supersedes: []
superseded_by: ADR-0029
---
# ADR-0027: Stage 00 Canonical Adapter Model

## Context

이 결정은 Stage 00을 AI Agent 정책과 catalog의 정본으로 두고 provider별
directory를 adapter로 제한하는 초기 경계를 채택했다. 이후 문서 profile과
template의 machine authority를 별도로 분리할 필요가 확인되었다.

## Options Considered

- 이 결정을 current authority로 유지한다.
- Stage 00 정책 권한과 Stage 99 문서 계약 권한을 분리한 후속 결정으로
  대체한다.

## Decision

ADR-0029가 이 결정을 supersede한다. 이 문서는 결정 이력만 보존하며 현재
provider 절차, validation 범위, lifecycle 규칙을 정의하지 않는다.

## Consequences

- Stage 00의 provider-neutral 정책 원칙은 후속 결정에 통합되었다.
- 현재 구현과 검증은 ADR-0029 및 AD-0027을 따른다.
- 이 문서의 이전 실행 세부사항은 current guidance로 사용할 수 없다.

## Traceability

- [ADR-0029 Workspace Governance Authority](0029-workspace-governance-authority.md)
- [AD-0027 Agent Governance Canonical Adapter](../descriptions/0027-agent-governance-canonical-adapter.md)
