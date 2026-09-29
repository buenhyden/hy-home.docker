---
title: "03.specs"
version: "1.2.6"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
---

# 03.specs

## Overview

`docs/03.specs`는 범위가 정해진 변경의 명세와 실행 package를 관리합니다.
package마다 Spec이 관찰 가능한 동작과 acceptance를, Plan이 구현 순서와
위험을, Task가 실제 실행·검증·검토 증거를 소유합니다. 오래 유지할 구조와
운영 의미는 Stage 01·02·05의 현재 문서로 승격합니다.

이 README는 현재 package로 가는 길만 안내합니다. package 안의 Spec, Plan,
Task와 그 상태는 각 package가 소유하므로 여기에 옮겨 적지 않습니다.

## Scope

- 포함: 진행 중인 변경, 검증이 끝나 보관 승인을 기다리는 package의
  Spec·Plan·Task와 Spec이 직접 소유하는 실행 가능한 contract.
- 제외: 운영 절차, 감사·조사 데이터, 이미 처분된 package의 본문, 이전 경로의
  복제본과 redirect. 운영·참조 자료는 각 Stage의 현재 owner가, 처분된 실행
  증거는 Stage 98의 보존 package가 소유합니다. Git history는 원본과 복구를
  증명할 뿐, 반드시 보존해야 할 본문을 대신하지 않습니다.

## Structure

package 하나가 직접 하위 디렉터리 하나입니다. 디렉터리 이름은
`<4자리 번호>-<slug>`이며 package 안의 파일 경로와 역할은
[Stage 99 Registry](../99.templates/registry.json)가 소유합니다.
`design.md`, `tests.md`, 단수형 `task.md`는 package 역할이 아닙니다.

### 현재 package

| ID | Package | 목적 |
| --- | --- | --- |
| SPEC-0182 | [HOME Residual Backlog](./0182-home-residual-backlog/) | SPEC-0180 잔여 작업: 저장소 후속, 런타임과 legacy data, 복구·인증 acceptance |
| SPEC-0192 | [Backup and Host Alerting](./0192-backup-and-host-alerting/) | 백업이 오래 성공하지 못하거나 시스템 디스크 여유가 부족하면 알림을 보내고, n8n이 DB 연결을 잃으면 health check가 실패하게 함 · 보관 승인 대기 |

처분된 package는 [Stage 98 README](../98.archive/README.md)에서 찾습니다.
Spec·Plan이 completed이고 모든 Task가 completed 또는 유효한 cancelled이면
현재 표의 목적에 `보관 승인 대기`를 표시합니다. 이는 계산된 탐색 구분이며
새 lifecycle 상태나 처분 승인이 아닙니다. 대기 중인 package에서 새 실행을
시작하지 않습니다.

### 역할 계약

| 역할 | 책임 |
| --- | --- |
| Spec | 범위가 정해진 관찰 가능한 동작, 범위, 실패 모드, acceptance 계약 |
| Plan | 승인된 실행 순서, 위험, rollback, 완료 기준 |
| Task | 실제 작업 기록, 명령 결과, 검토, commit, 이연 증거 |
| Contract | Spec이 소유하는 등록된 실행 가능 인터페이스 |

## How to Work in This Area

1. 관련 Requirement, Architecture Description, ADR을 먼저 읽습니다.
2. 등록된 Spec template으로 `spec.md`를 만들거나 고칩니다.
3. 승인된 변경에만 Plan과 번호가 붙은 Task를 추가합니다.
4. 실제 작업은 현재 Task에만 기록합니다.
5. acceptance 대응과 승격 기록은 현재 Task에 남기고 Stage 01·02·05의 오래
   유지할 갱신을 연결하거나 갱신이 필요 없는 이유를 적습니다.
6. metadata, lifecycle, 링크, 구현 정합성, 등록된 gate profile을 검증합니다.
7. 승격과 acceptance 검증 뒤 package를 완료합니다. 별도 보관 승인과
   복구·inbound consumer 확인 뒤 전체 단위를 보존합니다. clarify, analyze, 구현, 검증 순서는
   [SDLC](../../.agents/governance/sdlc.md)를 따릅니다.

### Package 수명주기

- 현재 Requirement와 Architecture가 변경 범위를 이미 다루면 그대로
  재사용합니다.
- Spec·Plan·Task의 정확한 상태와 전이는 Registry가 소유합니다.
- 완료 전에 acceptance와 실제 검증 결과를 연결하고 오래 유지할 의미를 현재
  Stage 01·02·05 owner로 승격합니다. 승격 근거는 현재 Task의
  `Verification Evidence` 한 곳에 기록합니다.
- 완료된 package는 일관된 종결 상태로 보관 승인을 기다릴 수 있습니다.
  별도 승인을 받은 뒤 Spec·Plan·모든 Task를 Stage 98로 함께 옮깁니다.
  Git 복구만 믿고 실행 본문을 지우거나 동결된 내용을 다시 쓰지 않습니다.
  철회와 완료의 처분 기록은
  [문서 보존 정책](../../.agents/governance/documentation-protocol.md#document-retention-and-retirement)을
  따릅니다.

## Related Documents

- [Requirements](../01.requirements/README.md)
- [Architecture](../02.architecture/README.md)
- [Operations](../05.operations/README.md)
- [Stage authoring matrix](../../.agents/governance/stage-authoring-matrix.md)
- [Document Registry](../99.templates/registry.json)
