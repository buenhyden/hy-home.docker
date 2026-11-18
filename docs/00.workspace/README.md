---
title: "00.workspace"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-18"
created: "2026-11-18"
layer: "workspace"
---

# 00.workspace

## Responsibility

### Purpose

#### Purpose and Readers

Stage 00은 사람과 agent가 함께 따르는 작업공간 공통 업무 정책(W 계층)을 담습니다.
프로젝트 책임 지도, SDLC·문서·Git·승인 절차, 품질과 완료 기준이 여기에 있습니다.
agent만의 실행 규칙(진입, 역할 선택, 위임, 컨텍스트, 중단)은
[agent governance](../../.agents/README.md)에 남습니다.

소유자가 2026-11-18에 SDD-WOWNER 결정으로 이 위치를 채택했습니다. 책임 계층의 정의는
[Stage 저작 매트릭스](01.project/stage-authoring-matrix.md#responsibility-layers)가
소유합니다.

#### Audience

변경을 계획하거나 검토하는 운영자, 리뷰어, AI agent가 공통 규칙을 찾을 때 읽습니다.

### Excluded Responsibilities

- 비소유: 정책 본문(각 문서가 소유), agent 실행 규칙, hookify 기계 규칙과 native
  바인딩, 문서 경로와 profile 계약(Stage 99)

## Current Contents

### Paths

| Path | Purpose |
| --- | --- |
| `01.project/stage-authoring-matrix.md` | 책임 계층과 Stage별 소유자 |
| `02.process/sdlc.md` | 요구에서 인수까지의 공통 수명주기 |
| `02.process/documentation-protocol.md` | 문서 권위, 언어, 링크, 은퇴 |
| `02.process/git-workflow.md` | 브랜치, 커밋, 통합 |
| `02.process/github-governance.md` | 저장소 보호와 GitHub 운영 |
| `02.process/approval-boundaries.md` | 사람·agent 공통 승인 범위 |
| `03.quality/quality-standards.md` | 품질 게이트와 검증 매트릭스 |
| `03.quality/task-checklists.md` | 시작·완료 점검 |

### Owners

`@buenhyden`이 변경을 승인하고 `rules-engineer`가 검토합니다.

## Usage

### Entry Points

[bootstrap](../../.agents/governance/bootstrap.md)이 읽기 순서를 정하고, 각 Stage
문서와 [agent governance](../../.agents/README.md)가 이 정책을 소비합니다. 같은
의미를 다른 계층에 복제하지 않습니다.

### Checks

정책 변경은 해당 Spec Package Task에 증거를 남기고 문서 metadata, 링크, agent
governance contract 검사를 통과해야 합니다.
