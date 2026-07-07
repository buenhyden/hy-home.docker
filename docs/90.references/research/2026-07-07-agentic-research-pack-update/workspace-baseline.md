---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/workspace-baseline.md -->

# Reference: Agentic Engineering Workspace Baseline

## Overview

본 참조 문서는 `hy-home.docker` 워크스페이스의 목적, 규칙, 환경적 조건, 그리고 SDLC 전반에 걸친 품질(Formatting, Linting, Syntax) 및 보안 통제 요소를 정리한 리서치 베이스라인입니다.

## Purpose

이 문서는 외부 에이전틱 엔지니어링 설계 모델과 비교 분석을 수행하기 전, 저장소의 구조와 동작 규칙을 명확히 함으로써 일관성 있고 근거에 기반한 격차 분석(Gap Analysis)을 지원합니다.

## Repository Role

이 문서는 저장소의 상태를 확인하기 위한 참고용 데이터이며, 공식 정책 문서(`docs/00.agent-governance/`의 규칙 및 범위 등)를 우회하거나 대체하지 않습니다.

## Scope

### In Scope

- 워크스페이스의 목적 및 규칙 체계
- SDLC(Software Development Life Cycle)와 스펙 주도(Spec-driven) 개발 구조
- 포맷팅(Formatting), 스타일 검사(Linting), 문법 오류 제어 현황
- 자동화(pipeline, workflow) 및 CI/CD 파이프라인
- 보안(Security) 환경 제약 및 바이브코딩(Vibe Coding)의 규칙화 방안

### Out of Scope

- 실 런타임 코드 파일 및 Docker Compose 구성의 임의 수정
- 비밀번호, 토큰 등 민감한 자격 증명 취급
- 본 문서를 정책으로 강제하는 행위

---

## 1. 워크스페이스 목적 및 체계 규칙

`hy-home.docker` 워크스페이스는 Docker Compose 기반의 홈/개발 인프라 서비스 스택과 AI 에이전트 전용 거버넌스 프레임워크가 결합된 "AI Agent-first Engineering Workspace"입니다.

- **목적**: 인프라 설계와 에이전트 협업 체계의 통합.
- **체계 규칙**: AI 에이전트를 단순한 일회성 생성 툴이 아닌, 명확한 역할과 검증 단계를 갖춘 가상 작업자(first-class engineering worker)로 격상시켜 관리합니다.
- **거버넌스 허브**: `docs/00.agent-governance/`를 단일 진실 공급원(SSOT)으로 삼아 에이전트의 실행 지침, 모델 위상 정책, 승인 경계를 강제합니다.

## 2. SDLC 및 스펙 주도 개발 체계

본 워크스페이스는 아래와 같은 엄격한 단계별 문서 흐름(Stage-gated structure)을 따르는 SDLC를 수립하고 있습니다.

```text
Stage 00 (Governance)  ──>  Stage 01 (Requirements) ──> Stage 02 (Architecture)
                                                                 │
Stage 05 (Operations)  <──  Stage 04 (Execution)    <── Stage 03 (Specifications)
```

1. **Stage 00. Agent Governance**: 에이전트 규약, 범위, 템플릿 계약 관리.
2. **Stage 01. Requirements**: 제품 및 아키텍처 요구사항 문서화.
3. **Stage 02. Architecture**: 시스템 아키텍처 의사결정(ADR) 및 기술 참조 모델.
4. **Stage 03. Specifications**: 구체적이고 구현 가능한 기술 스펙(Spec) 정의.
5. **Stage 04. Execution**: 실행 계획(Plan) 수립, 사용자 승인 획득, 그리고 실행 작업(Task) 결과 및 검증 증적(Evidence) 저장.
6. **Stage 05. Operations**: 런타임 운영 가이드, 런북, 사고 이력 관리.
7. **Stage 90. References & Stage 99. Templates**: 범용 참조 정보 및 표준 문서 템플릿 보관.

**스펙 주도 개발 (Spec-driven Development)**: 모든 기능 구현 및 수정 작업은 사전에 Stage 03에 구체적인 스펙을 문서화하고, Stage 04에 실행 계획을 세운 후, 검증 단계를 명시하여 "계약 준수" 형태로 작업을 수행합니다.

## 3. QA, 포맷팅, 스타일 검사(Linting) 및 문법 오류 제어

코드와 문서의 무결성을 원격 및 로컬에서 통제하기 위해 다차원 QA 게이트를 구성하고 있습니다.

- **포맷팅(Formatting)**: 코드 및 마크다운 파일들의 공백, 포맷 일관성을 검사하기 위해 로컬 `git diff --check`, 그리고 pre-commit 플러그인을 활용합니다. 변경 파일의 스타일 정상화는 런타임 훅인 `scripts/hooks/post-tool-validate.sh`에 의해 강제됩니다.
- **코드 스타일 검사(Linting)**: `.pre-commit-config.yaml`에 정의된 린터와 CI 파이프라인(`ci-quality.yml`)을 통해 스크립트(Shellcheck), 프론트엔드 코드(ESLint), 구성 파일(YAML lint) 등의 스타일 일관성을 자동 점검합니다.
- **문법 오류 제어**: 코드 파서 및 구성 파일 검증 스크립트(`validate-docker-compose.sh` 등)를 통해 런타임 배포 전에 파싱 레벨의 구문 오류를 걸러냅니다.

## 4. 자동화, 파이프라인 및 CI/CD

지속적 통합 및 배포 흐름은 GitHub Actions와 로컬 훅 파이프라인을 연계하여 작동합니다.

- **로컬 훅(Local Hooks)**: 에이전트 도구 호출 종료 후 동작하는 `agent-event-hook.sh`, 파일 변동을 감시하는 validation script들이 개발 주기 내부에서 실시간 피드백을 제공합니다.
- **CI/CD 파이프라인**: GitHub Actions의 `ci-quality.yml`은 원격 리포지토리에 푸시되거나 PR이 생성될 때 실행됩니다. 문서 추적성 검사(`check-doc-traceability.sh`), 저장소 표준 계약 검사(`check-repo-contracts.sh`), 컨테이너 인프라 검증, 보안 강화 검증(`check-all-hardening.sh`) 등을 병렬 수행하여 통제력을 유지합니다.

## 5. 보안(Security) 및 비밀값 관리

에이전트가 로컬 파일에 접근하거나 명령어를 제어할 때 발생할 수 있는 보안적 위험을 최소화합니다.

- **비밀 정보 경계**: 패스워드, API 토큰, 프라이빗 키 등은 환경 변수 예시 파일(`.env.example`) 및 `secrets/` 디렉토리 하위의 마운트 구조로 통제하며, 실제 비밀값은 형상 관리에 절대로 노출되지 않도록 `validate-docker-compose.sh --preflight` 등이 모니터링합니다.
- **권한 제한**: 에이전트의 쓰기/읽기 권한은 지정된 워크스페이스 폴더로 엄격히 제한되며, 승인 영역을 벗어나는 위험 행동(예: git reset --hard, 원격 push 등)은 실행 전에 제약받습니다.

## 6. 바이브코딩(Vibe Coding)의 규칙화 방안

**바이브코딩(Vibe Coding)** 이란 AI 에이전트에게 명확한 설계나 검증 계획 없이 감각적(Intuition-based)으로 코드를 연속 작성하게 하여 소스 코드 품질을 흐리는 무질서한 코딩 형태를 뜻합니다.

- **위험성**: 설계 명세서 없는 아키텍처 오염, 중복 코드 대량 양산, 테스트 검증 없는 기능 배포로 인한 사이드 이펙트 유발.
- **규칙적 통제**:
  1. **사전 계획 명시화**: 변경 전 반드시 `implementation_plan.md`와 `task.md`를 통해 변경 범위와 의도된 코드를 구체화하고 사용자의 승인을 받음.
  2. **원자적이고 surgical한 수정**: 요구된 범위 외부의 인접 코드를 임의로 리팩토링하거나 변경하지 않도록 차단.
  3. **검증 스크립트(Automated Validators)**: 모든 수정 완료 단계에서 반드시 validator 스크립트 실행 결과를 검증 증적으로 제출하게 하여 감각적 신뢰를 기술적 신뢰로 전환.

## Related Documents

- [README.md](./README.md)
- [harness-engineering.md](./harness-engineering.md)
- [loop-engineering.md](./loop-engineering.md)
- [../README.md](../README.md)
