---
title: "Agent Evaluation Evidence"
version: "1.4.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-07"
created: "2026-09-03"
---

# .agents/evaluations

## Overview

같은 작업을 Skill 없이 실행한 결과와 Skill을 명시적으로 호출한 결과를 비교하는
증거 영역입니다. 작업 정의, 두 출력 원문, 채점과 집계의 관계를 보존하여 활성
하네스가 선택된 사례에서 더 나은 결과를 내는지 확인합니다. 런타임 동작과 활성
Skill 구성원 계약은 각각의 원본 소유 문서에서 확인합니다.

## Audience

- 승인된 비교 평가를 설계하고 수행하는 담당자
- 출력, 채점 근거와 미검증 범위를 검토하는 reviewer

## Scope

### In Scope

- 대표 비교 증거와 작업·출력·점수·집계의 관계
- 실제 평가 주기의 작성, 보존과 검증 경로

### Out of Scope

- 제품 요구사항, 공개 승인, Vault 변경과 공급자·Hook·검증 동작 정의
- 전체 활성 Skill 목록에 대한 대표 PASS 주장
- 임시 출력을 지속 평가 증거로 대체하거나 점수를 repository 필수 QA로 사용

## Structure

현재 이 범주에는 이 README만 있습니다. 아래는 새 평가 주기에서 등록할 증거의
구조이며, 해당 파일이나 평가가 이미 존재한다는 목록이 아닙니다.

| Planned item | Evidence owner |
| --- | --- |
| `harnesses/<evaluation-id>/task.md` | 같은 비교 작업, 입력 revision, 기준과 시행 조건 |
| `harnesses/<evaluation-id>/baseline.md` | Skill 없는 실제 출력 원문 |
| `harnesses/<evaluation-id>/with-skill.md` | 명시적으로 Skill을 호출한 실제 출력 원문 |
| `harnesses/<evaluation-id>/score.md` | 채점, 부분 점수 이유와 판정 |
| `results.md` | 대표 결과의 점수·상태·검토자·날짜와 원문 참조 |
| `templates/` | 새 작업·출력·채점의 등록된 작성 틀 |

## Tech Stack

상시 합성 출력 채점기와 고정 fixture QA는 폐기했습니다. 비교 평가의 도구, 모델,
시행 수, 권한과 예산은 실행 전에 개별 Task에서 선택합니다. 현재 이 README는
실행 하네스나 채점 자동화를 제공하지 않습니다.

## Validation

이 README에는 현행 문서 profile, frontmatter와 링크 검사를 적용합니다. 새 증거와
작성 틀은 Stage 99에 한정된 평가 증거 profile과 binding을 등록한 뒤 작성합니다.
그 분류는 점수 정확성이나 실행 완료를 증명하지 않습니다. 실제 비교·채점·검토는
출력 원문과 실행 증거를 대조하며 별도의 Task가 수용을 기록합니다.

## Usage

수정 전에 아래 Local Constraints와 [평가 실행 정책](../governance/agentic.md#evaluation-evidence)
에서 소유자와 실행 경계를 확인합니다. 현재 구성원은 [Provider Registry](../governance/providers/registry.yaml)의
등록과 [canonical Skill 소유 규칙](../README.md#scope)에 따라 실제 `skills/<skill_id>/SKILL.md`에서 확인합니다. [Provider model evaluation](../skills/provider-model-evaluation/SKILL.md)은
공식 출처와 native schema 비교의 별도 절차이며 Skill 출력 비교 평가를 대신하지 않습니다.

### Local Constraints

1. 새 평가의 작업·입력·기준과 실제 두 출력이 같은 비교 범위인지 명시합니다.
   모델·도구·설정·권한 또는 시행 조건의 차이는 결과의 한계로 남깁니다.
2. 등록된 작업·채점 틀을 사용합니다. 원문, 채점과 집계는 각각 위 구조의 단일
   소유자에 둡니다. 실행 승인·착수·명령·수용은 Task에만 기록합니다.
3. 실제 평가 주기에서만 출력·점수·집계를 갱신합니다. 기존 원문은 당시 bytes로
   보존하고 새 실행은 별도 revision의 작업 정의와 증거를 사용합니다.
4. 점수 문서는 `Evidence Granularity`, 시행 수, 결과 신호, 채점자와 기준 ID,
   부분 점수 이유와 사람의 보정 상태를 기록합니다. 독립 채점이나 사람의 보정은
   실제 수행한 경우에만 표시합니다.
5. 점수 변경은 집계와 함께 반영합니다. 새 대표 행은 작업·두 출력·점수·집계가
   모두 준비된 뒤 추가합니다. 구성원 변경은 Skill의 canonical source에서 합니다.
6. 합성 사례의 독립 에이전트 응답은 해당 사례만 입증합니다. 네이티브 자동 선택,
   실제 명령 실행, provider entitlement나 운영 성공으로 확대하지 않습니다.
7. 원문과 집계가 충돌하면 실제 산출물 소유자에서 해결하고 README가 낡았다면
   README를 고칩니다. README에는 별도 점수표를 복제하지 않습니다.

제공된 예시의 7개 하네스, `pre-publish-review-current`, `context-handoff-validation`
평가 묶음은 현재 저장소나 전체 ref 이력에서 확인되지 않았습니다. 이 저장소의
대표 결과나 보존 완료로 기록하지 않습니다. 과거 `evals/` 경로는 당시 provenance이며
현재 경로의 실행 지시가 아닙니다. 폐기한 채점기·fixture는 Git history에서 복구할 수 있습니다.

Provider Registry는 현재 이 README만 canonical entry로 등록합니다. 새 증거·template의
분류와 등록은 해당 변경 계약에서 함께 수행하고, 실행 파일은 script manifest의
실제 소비자와 함께 등록합니다. 이 안내는 새로운 실행 파일이나 Skill을 설치하지 않습니다.

## Related Documents

- [Agent execution and evaluation policy](../governance/agentic.md)
- [Quality policy](../governance/quality-standards.md)
- [Canonical Skill ownership](../README.md#scope)
- [Handoff input/output contract](../prompts/handoff.md)
- [Provider model evaluation](../skills/provider-model-evaluation/SKILL.md)
- [Script manifest](../../scripts/manifest.yaml)
- [Root README](../../README.md)
