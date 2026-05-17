---
status: draft
---

<!-- Target: docs/04.execution/plans/2026-05-17-requirements-standardization.md -->

# docs/01.requirements 표준화 Plan

## Overview (KR)

이 문서는 `docs/01.requirements` 폴더의 23개 PRD 파일과 README를 `docs/99.templates/prd.template.md` 및 `readme.template.md` 기준에 완전히 준수시키기 위한 실행 계획서다.

## Context

분석 결과 6가지 유형의 구조적 문제 확인: README 구조 불일치, frontmatter 누락(전체), Target 주석 누락/오위치, H1 형식 불일치(6개), Related Documents 링크 형식 불일치, standardize-infra-net.md 이중 H1.

## Goals & In-Scope

- **Goals**: PRD 파일들이 prd.template.md를 완전히 준수하도록 표준화
- **In Scope**: `docs/01.requirements/` 내 README + PRD 23개

## Non-Goals & Out-of-Scope

- **Out of Scope**: 다른 stage 폴더, PRD 비즈니스 내용(Vision/Requirements) 변경, 신규 PRD 작성

## Work Breakdown

| #   | Task                               | 대상        | 검증                                    |
| --- | ---------------------------------- | ----------- | --------------------------------------- |
| T1  | README.md 전면 개선                | `README.md` | Structure에 실제 파일명, 링크 동작 확인 |
| T2  | frontmatter 일괄 추가              | PRD 23개    | `grep -c "^status:" *.md` = 23          |
| T3  | Target 주석 정규화                 | PRD 23개    | 각 파일 H1 직전에 위치 확인             |
| T4  | H1 형식 통일                       | 5개 파일    | `# ... Product Requirements` 패턴       |
| T5  | Related Documents 링크 형식 통일   | 다수 파일   | backtick 링크 잔존 확인                 |
| T6  | standardize-infra-net.md 구조 완성 | 1개 파일    | 단일 H1, AI Agent Requirements 섹션     |
| T7  | laboratory.md Overview(KR) 추가    | 1개 파일    | `## Overview (KR)` 섹션 존재 확인       |

## Verification Criteria

- `grep -rL "^---" docs/01.requirements/2026-*.md` → 출력 없음 (모든 파일 frontmatter 보유)
- `grep -rL "<!-- Target:" docs/01.requirements/2026-*.md` → 출력 없음
- `grep -rn "\`\[" docs/01.requirements/\*.md` → 출력 없음 (backtick 링크 없음)
- `grep -c "^# PRD" docs/01.requirements/*.md | grep -v ":0"` → 출력 없음 (PRD prefix H1 없음)

## Related Documents

- [PRD README](../../01.requirements/README.md)
- [prd.template.md](../../99.templates/prd.template.md)
- [readme.template.md](../../99.templates/readme.template.md)
