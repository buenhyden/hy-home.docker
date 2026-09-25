---
title: "Architecture Decision Records"
version: "1.5.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-25"
layer: "architecture"
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

이 디렉터리는 현재 유효한 ADR을 보유한다. 각 ADR은 하나의 material
choice를 소유하고 실제 Architecture Description을 parent로 연결한다.
개수는 유지 기준이 아니므로 아래 Current Inventory와 실제 파일 목록이
권위이다.

## Structure

```text
docs/02.architecture/decisions/
├── 0001-traefik-nginx-hybrid.md
├── 0002-keycloak-oauth2-proxy-choice.md
├── ...
├── 0028-local-isolated-readiness-evidence.md
├── 0032-canonical-agent-governance-home.md
├── 0034-canonical-knowledge-and-prompt-surfaces.md
├── 0036-archive-occupancy-citation-and-frozen-identity.md
├── 0037-package-disposition-wait-and-task-cancellation.md
├── 0038-selective-native-oidc-for-native-auth-apps.md
├── 0039-analytics-engines-after-lakehouse-convergence.md
├── 0040-data-hardening-gate-and-staged-expansion.md
├── 0041-offsite-backup-target.md
├── 0042-openbao-unseal-method.md
└── README.md
```

### Current Inventory

- `ADR-0001`부터 `ADR-0011`: 기본 tier와 service selection decisions.
- `ADR-0015`, `ADR-0019`: ADR-0039, ADR-0040이 각각 supersede한 analytics engine과
  04-data hardening decisions.
- `ADR-0016`부터 `ADR-0026`(0019 제외): analytics, hardening, HA와 network decisions.
- `ADR-0027`:
  ADR-0029가 supersede한 Stage 00 adapter decision.
- [`ADR-0028`](./0028-local-isolated-readiness-evidence.md):
  local-isolated readiness evidence strategy.
- `ADR-0029`:
  ADR-0032가 supersede한 이전 workspace governance authority decision.
- `ADR-0030`:
  ADR-0031이 supersede한 Tombstone-only preservation decision.
- `ADR-0031`:
  ADR-0033이 supersede한 Spec-only preservation decision.
- [`ADR-0032`](./0032-canonical-agent-governance-home.md):
  공통 정본의 `.agents` 이전과 native 로딩 경계를 채택한 active decision.
- `ADR-0033`:
  ADR-0035가 supersede한 full package preservation decision. Spec, Plan, 모든
  Task를 보존 단위로 두는 규칙은 ADR-0035가 다시 적어 유지한다.
- [`ADR-0034`](./0034-canonical-knowledge-and-prompt-surfaces.md):
  `.agents/knowledge/`와 `.agents/prompts/`를 canonical category로 도입하는
  accepted decision.
- `ADR-0035`:
  Stage 98을 네 retention class와 두 route disposition으로 나누고 인용
  가능성을 처분의 이름에서 도출한 decision. ADR-0033을 supersede했고, ADR-0036이
  이것을 supersede하며 유지되는 규칙을 다시 적었다.
- [`ADR-0036`](./0036-archive-occupancy-citation-and-frozen-identity.md):
  활성 package 안의 completed Task 허용, route 기록 인용 금지, 보존본과
  catalog `Source`의 기계 비교, 종료된 Incident의 종료 시점을 요구하는 accepted
  decision. ADR-0035를 supersede하며, 그 규칙 가운데 유지되는 것을 다시 적었다.
- [`ADR-0037`](./0037-package-disposition-wait-and-task-cancellation.md):
  모든 구성원이 terminal인 완료 package의 처분 대기와, 구조화된 취소 근거를 가진
  cancelled Task 허용을 제안하는 proposed decision. 수락 시 ADR-0036을
  supersede하며, SPEC-0179가 수락을 소유한다.
- [`ADR-0038`](./0038-selective-native-oidc-for-native-auth-apps.md):
  Keycloak을 중앙 IdP로 유지하면서 Gateway ForwardAuth와 application-native
  OIDC를 서비스별로 선택하고 Airflow/Kafbat UI의 이중 인증을 금지하는
  proposed decision.
- [`ADR-0039`](./0039-analytics-engines-after-lakehouse-convergence.md):
  InfluxDB와 OpenSearch를 유지하고 스트림 처리는 Flink, OLAP은 Iceberg 위의
  Trino가 맡는 accepted decision. ADR-0015를 supersede한다.
- [`ADR-0040`](./0040-data-hardening-gate-and-staged-expansion.md):
  04-data 하드닝 gate와 단계적 확장을 현재 서비스 기준으로 다시 적은 accepted
  decision. ADR-0019를 supersede한다.
- [`ADR-0041`](./0041-offsite-backup-target.md):
  같은 host에만 있는 Restic과 pgBackRest 저장소의 offsite 대상을 고르는
  proposed decision. 옵션 비교와 권고를 담고 owner 결정을 기다린다(SPEC-0182 W10).
- [`ADR-0042`](./0042-openbao-unseal-method.md):
  OpenBao 수동 Shamir unseal을 유지할지 auto-unseal로 바꿀지 고르는 proposed
  decision. 옵션 비교와 권고를 담고 owner 결정을 기다린다(SPEC-0182 W10).

## How to Work in This Area

1. 상위 [Architecture Description](../descriptions/README.md)을 확인한다.
2. 기존 ADR이 같은 선택을 이미 소유하는지 확인한다.
3. 새 ADR은 [`decision.template.md`](../../99.templates/templates/architecture/decision.template.md)를 사용한다.
4. 선택, alternatives, rationale와 consequences를 보존한다.
5. 이전 결정을 대체하면 stable `supersedes` metadata와 양방향 문서 링크로
   supersession을 명시한다.

### Documentation Standards

- `<4-digit-id>-<slug>.md`, `artifact_id: ADR-<4-digit-id>`,
  `type: sdlc/architecture-decision`을 일치시킨다.
- `parent_ids`는 실제 Architecture Description만 포함한다.
- 구현 계약과 검증 기준은 관련 Spec, 운영 절차는 Stage 05에 둔다.
- 결정 확인 근거가 없는 runtime 상태는 주장하지 않는다.

### AI Agent Guidance

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
