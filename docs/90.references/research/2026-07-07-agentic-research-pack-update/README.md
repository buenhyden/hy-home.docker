---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/README.md -->

# Agentic Engineering Research Pack (2026-07-07 Update)

> `hy-home.docker`의 하네스 엔지니어링, 루프 엔지니어링, provider adapter, SDLC, QA/CI 및 에이전트 카탈로그 기준을 상세하게 분석한 source-backed reference pack

## Overview

`docs/90.references/research/2026-07-07-agentic-research-pack-update`는 `hy-home.docker`의 agent-first engineering 체계를 심층적으로 연구하고 외부 자료(`msitarzewski/agency-agents` 등)와 비교 분석하기 위한 리서치 팩입니다. 이 팩은 현재 저장소의 아키텍처적 특성, QA 및 CI/CD 파이프라인, 포맷팅 및 스타일 린팅 규칙, 보안 체계, 바이브코딩 현황, 그리고 AI 에이전트 설계 및 지침을 다룹니다.

이 팩은 active policy가 아닙니다. 발견된 부족한 요소와 개선안은 `Potential Follow-up / Gap`으로 기록하며, 실제 저장소의 환경 구성이나 정책 변경은 공식 stage-gate 절차에 따라 별도 승인된 execution plan에서 추진됩니다.

## Category Role

본 리서치 팩은 워크스페이스 내의 하네스 엔지니어링(Harness Engineering)과 루프 엔지니어링(Loop Engineering)을 중심으로 한 reference 문서 집합입니다. 이 카테고리는 현재 provider 설정 및 CI/CD 흐름을 이해하기 위한 보조 도구이며, Stage 00 정책, Stage 04 실행 이력, Stage 05 운영 절차를 대체하지 않습니다.

## Audience

이 README의 주요 독자:

- 개발자 (Developers)
- 인프라 및 운영 엔지니어 (Operators)
- 문서화 작성자 (Documentation Writers)
- AI 에이전트 (AI Agents)

## Scope

### In Scope

- 워크스페이스의 목적, 역할, 계약 조건에 대한 baseline 분석
- 하네스 엔지니어링(Harness Engineering) 구성 요소 및 에이전트 바인딩 연구
- 루프 엔지니어링(Loop Engineering) 피드백 루프 체계 및 검증 방식 분석
- Claude, Codex, Gemini 각각에 대한 하네스/루프 엔지니어링 현황 및 비교
- 공통 provider-neutral 환경, 규칙, 체계의 설계 방향 분석
- 스펙 주도(spec-driven) 개발 방식과 SDLC(요구사항 -> 아키텍처 -> 스펙 -> 실행 -> 운영) 매핑
- CI/CD 파이프라인, QA 게이트, 포맷팅, 스타일 검사(Linting) 및 문법 오류 제어 체계
- 보안(Security) 프레임워크 및 바이브코딩(Vibe Coding)의 규칙적 통제 방안 연구
- `msitarzewski/agency-agents` 외부 에이전트 카탈로그와 이 워크스페이스의 에이전트 카탈로그 비교 분석 및 추가 제안

### Out of Scope

- `docs/00.agent-governance/` 정책 직접 변경
- `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/` 콘텐츠 직접 수정
- 런타임 인프라 환경 변수 설정값 직접 변경
- 실제 비밀값, 크리덴셜, 프라이빗 키 등 민감 정보 취급

## Structure

```text
2026-07-07-agentic-research-pack-update/
├── README.md                            # 본 파일 (연구 팩 인덱스)
├── workspace-baseline.md                # 워크스페이스 기본 환경, 규칙, SDLC, QA, 포맷팅, 보안, 바이브코딩 정의
├── harness-engineering.md               # 하네스 엔지니어링 구성 요소 및 3대 LLM(Claude, Codex, Gemini) 하네스 분석
├── loop-engineering.md                  # 에이전트 피드백 루프, 자동화 파이프라인, 워크플로 루프 분석
├── provider-implementation-comparison.md # Claude, Codex, Gemini의 하네스/루프 비교 및 공통 체계 구축 방안
└── ai-agent-catalogs.md                  # agency-agents 외부 카탈로그 비교, AI agent instruction 분석 및 추가 에이전트 제안
```

## Current References

- [workspace-baseline.md](./workspace-baseline.md) - 워크스페이스 목적, 역할, 규칙, SDLC, QA, 포맷팅, 보안, 바이브코딩의 기본 기준
- [harness-engineering.md](./harness-engineering.md) - 하네스 엔지니어링의 정의, 아키텍처 및 3대 LLM 하네스 현황
- [loop-engineering.md](./loop-engineering.md) - 루프 엔지니어링의 에이전트 루프, CI 루프, 휴먼 피드백 루프 및 워크플로 자동화
- [provider-implementation-comparison.md](./provider-implementation-comparison.md) - Claude, Codex, Gemini의 구현 방식 비교 및 공통 환경 체계 요소
- [ai-agent-catalogs.md](./ai-agent-catalogs.md) - agency-agents 비교 분석, instruction 구조 및 워크스페이스 필수 추가 에이전트 제안

## Reading Order

1. [workspace-baseline.md](./workspace-baseline.md)에서 이 워크스페이스의 규칙적 체계와 기본 기준을 파악합니다.
2. [harness-engineering.md](./harness-engineering.md)와 [loop-engineering.md](./loop-engineering.md)에서 하네스와 피드백 루프의 설계 방향을 분석합니다.
3. [provider-implementation-comparison.md](./provider-implementation-comparison.md)에서 세 가지 LLM 어댑터의 런타임 특성을 대조합니다.
4. [ai-agent-catalogs.md](./ai-agent-catalogs.md)에서 `msitarzewski/agency-agents`와의 카탈로그 매핑을 검토하고 에이전트 인스트럭션 추가 기회를 발견합니다.

## How to Work in This Area

1. 본 연구 팩의 문서는 직접적인 활성 정책이 아닌, 참조용(Reference) 연구 자료 성격을 유지합니다.
2. 새로운 문서를 추가할 때 반드시 마크다운 표준 헤더 스펙을 준수해야 합니다.
3. 작업 변경 사항이 생기면 이 README 파일의 링크 상태를 재확인하고, 상위 README에도 등록해야 합니다.

## Related Documents

- [research references](../README.md)
- [90.references](../../README.md)
- [agent governance hub](../../../00.agent-governance/README.md)
- [HAFE specification](../../../03.specs/094-harness-agent-first-engineering/spec.md)
- [HAFE operations guide](../../../05.operations/guides/00-workspace/harness-agent-first-engineering.md)
