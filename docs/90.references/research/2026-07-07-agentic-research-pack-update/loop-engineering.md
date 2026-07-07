---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/loop-engineering.md -->

# Reference: Loop Engineering and Feedback Systems

## Overview

본 참조 문서는 AI 에이전트의 연속적인 상태 변경과 검증 과정을 통제하는 루프 엔지니어링(Loop Engineering) 체계 및 저장소 내 피드백 자동화 구조를 정리한 분석 문서입니다.

## Purpose

에이전트가 작업을 계획하고 실행한 후, 어떤 자동화된 검증 파이프라인과 승인 절차를 거치며 순환(Iteration)하는지를 정의합니다.

## Repository Role

본 문서는 루프 엔지니어링의 참조 문서이며, 실제 런타임 CI 검증 스크립트나 GitHub Actions 워크플로 파일의 코드를 대체하지 않습니다.

---

## 1. 루프 엔지니어링의 정의 및 아키텍처

**루프 엔지니어링 (Loop Engineering)** 이란 에이전트가 단발성 출력을 던지고 끝내는 것이 아니라, 스스로 상태를 관찰하고(Observe) 수정 계획을 세우며(Plan) 이를 적용하고(Execute) 검증 결과에 따라 피드백을 반영하는(Verify & Refine) 피드백 루프(Feedback Loop) 시스템을 체계화하는 엔지니어링 기법을 의미합니다.

### 루프의 구성 요소
1. **에이전트 내부 루프 (Agent Inner Loop)**: 에이전트가 단일 태스크 내에서 프롬프트에 기재된 체크리스트를 따라 순차 실행하는 자체적인 실행 루프.
2. **검증 루프 (Validation Loop)**: 로컬 검증 스크립트(예: `check-repo-contracts.sh`, `validate-docker-compose.sh`)가 실행되어 변경 코딩의 표준 계약 위반 여부를 에이전트에게 리턴해 주는 정규식/규칙 검증 루프.
3. **CI 루프 (CI/CD Quality Loop)**: 원격 레포지토리에 푸시할 때 동작하는 GitHub Actions 파이프라인. 전체 테스트 스위트와 컨테이너 무결성을 보장합니다.
4. **휴먼 피드백 루프 (Human-in-the-loop Approval)**: 계획 단계(`implementation_plan.md` 승인) 및 풀 리퀘스트 단계에서 최종 사용자가 코드 및 아키텍처 결정을 심사하는 단계 게이트.

## 2. Claude, Codex, Gemini 각각에 대한 루프 엔지니어링 현황

어시스턴트 프로바이더별로 피드백 루프를 작동시키는 연결 방식이 상이합니다.

### A. Claude Code Loop
- **실행 루프**: 도구 호출 결과를 파싱하여 에러가 있을 시 내부적으로 수정 도구를 재실행하는 ReAct 패턴이 고도화되어 있습니다.
- **로컬 훅 연계**: 도구 실행 성공 혹은 수정이 발생하면 `agent-event-hook.sh`를 통해 로컬 파이프라인이 자동 실행되어 결과를 에이전트의 컨텍스트로 바로 피드백합니다.

### B. Codex Loop
- **실행 루프**: `.codex/hooks.json`에 정의된 훅 이벤트에 따라 에이전트가 작업을 마칠 때 자동으로 로컬 validator를 수행합니다.
- **피드백 파싱**: 검증 스크립트 실패 메시지를 에이전트가 즉각 파싱하여 "오류 수정 계획"을 수립하도록 인스트럭션이 설계되어 있습니다.

### C. Gemini Loop
- **실행 루프**: 주로 텍스트 컨텍스트 유입이 많고 쉘 명령 실행 시 명시적인 권한 승인이 필요하여, 타 프로바이더에 비해 휴먼 피드백 루프의 빈도가 높습니다.
- **Parity 보완**: Gemini 환경에서는 툴 레벨의 자동화된 pre/post 훅 실행 기능이 약하므로, 작업 종료 시 사용자가 수동으로 검증을 트리거하거나 에이전트가 자발적으로 검증 스크립트를 호출하도록 프롬프트 수준에서 제어 루프를 보완합니다.

## 3. 루프 엔지니어링의 구현 현황 및 부족한 요소

- **구현 현황**:
  - `implementation_plan.md` -> user approval -> `task.md` 진행 -> `walkthrough.md` 및 `progress.md` 업데이트로 이어지는 정밀한 휴먼-에이전트 협업 루프가 가동 중입니다.
  - CI 품질 게이트(`ci-quality.yml`)를 통과하지 못하면 PR 병합이 차단되므로 루프의 안정성이 보장됩니다.
- **부족한 요소 (Gaps)**:
  - **시맨틱 평가 루프의 부재 (Lack of Semantic Evaluation)**: 현재의 검증 루프는 마크다운 구조, 정규식 매칭, 린터 등 구문론적(Syntactic) 정합성에 치중되어 있습니다. 에이전트가 수립한 설계의 타당성이나 아키텍처 결정(ADR)의 타당성을 평가하는 의미론적(Semantic) 에이전트 평가(Eval) 피드백 루프가 아직 완성되지 않았습니다. (로컬에 데모용 advisory runner만 존재함)
  - **훅 실행의 비균질성**: 로컬 환경 및 사용하는 IDE 프로바이더에 따라 `agent-event-hook.sh`가 생략되거나 누락되는 경우가 있어 피드백 전달의 일관성이 부족합니다.

## Related Documents

- [README.md](./README.md)
- [workspace-baseline.md](./workspace-baseline.md)
- [harness-engineering.md](./harness-engineering.md)
