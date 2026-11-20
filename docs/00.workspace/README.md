---
title: "00.workspace"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2026-11-18"
layer: "workspace"
---

# 00.workspace

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Responsibility

##### Purpose

###### Purpose and Readers
<!-- core-payload-level:4 -->

Stage 00은 사람과 agent가 함께 따르는 작업공간 공통 업무 정책(W 계층)을 담습니다.
프로젝트 책임 지도, SDLC·문서·Git·승인 절차, 품질과 완료 기준이 여기에 있습니다.
agent만의 실행 규칙(진입, 역할 선택, 위임, 컨텍스트, 중단)은
[agent governance](../../.agents/README.md)에 남습니다.

소유자가 2026-11-18에 SDD-WOWNER 결정으로 이 위치를 채택했습니다. 책임 계층의 정의는
[Stage 저작 매트릭스](01.project/stage-authoring-matrix.md#responsibility-layers)가
소유합니다.

###### Audience
<!-- core-payload-level:4 -->

변경을 계획하거나 검토하는 운영자, 리뷰어, AI agent가 공통 규칙을 찾을 때 읽습니다.

##### Excluded Responsibilities

- 비소유: 정책 본문(각 문서가 소유), agent 실행 규칙, hookify 기계 규칙과 native
  바인딩, 문서 경로와 profile 계약(Stage 99)

#### Current Contents

##### Paths

| Path | Purpose |
| --- | --- |
| `01.project/stage-authoring-matrix.md` | 책임 계층과 Stage별 소유자 |
| `01.project/glossary.md` | Docker workspace 로컬 용어와 정책 바인딩 |
| `02.architecture/01.descriptions/` | workspace 구조 설명(AD-0027 agent governance, AD-0030 문서 생명주기) |
| `02.architecture/02.decisions/` | workspace 구조 결정(ADR-0032·0034·0037·0044·0048·0049·0051·0057·0063) |
| `03.process/sdlc.md` | 요구에서 인수까지의 공통 수명주기 |
| `03.process/documentation-protocol.md` | 문서 권위, 언어, 링크, 은퇴 |
| `03.process/git-workflow.md` | 브랜치, 커밋, 통합 |
| `03.process/github-governance.md` | 저장소 보호와 GitHub 운영 |
| `04.quality/approval-boundaries.md` | 사람·agent 공통 승인 범위와 보호 표면 |
| `04.quality/quality-standards.md` | 품질 게이트, 위험별 리뷰, 검증 매트릭스 |
| `04.quality/task-checklists.md` | 시작·완료 점검 |
| `05.environment/onboarding.md` | 개발 환경 준비와 첫 점검, 환경 경계 |
| `06.maintenance/harness-maintenance.md` | agent 도구(memory, 수집, 분석, 예측, 병렬 실행, 관측) 유지보수 |

제품 AD·ADR은
[Stage 02](../02.architecture/README.md)에 있고, workspace AD·ADR과 같은 번호 공간을
씁니다. 공통 용어와 agent·provider 의미는
[Repository Vocabulary](../../.agents/knowledge/glossary.md)가 소유합니다.

##### Owners

`@buenhyden`이 변경을 승인하고 `rules-engineer`가 검토합니다.

#### Usage

##### Entry Points

[bootstrap](../../.agents/governance/bootstrap.md)이 읽기 순서를 정하고, 각 Stage
문서와 [agent governance](../../.agents/README.md)가 이 정책을 소비합니다. 같은
의미를 다른 계층에 복제하지 않습니다.

##### Checks

정책 변경은 해당 Spec Package Task에 증거를 남기고 문서 metadata, 링크, agent
governance contract 검사를 통과해야 합니다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
