---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/automation-candidates.md -->

# Reference: Automation Candidates and Implementation Roadmap

## Overview

본 로드맵은 `hy-home.docker` 워크스페이스의 하네스 검증 규칙, 피드백 루프 파이프라인, 그리고 에이전트 오케스트레이션을 보다 견고히 자동화하기 위해 식별한 개선 후보군 목록입니다.

## Purpose

수동 요소를 완전히 배제하고, AI 에이전트의 런타임 통제를 지속 가능하고 강력한 자동화 환경으로 진화시키는 구체적 실행 지침을 제안합니다.

## Repository Role

본 문서는 향후 자동화 적용 후보군을 위한 레퍼런스이며, 현 시점의 자동화 스크립트나 CI 구성을 강제로 갱신하지 않습니다.

---

## 1. 14대 자동화 개선 후보군 목록 (Roadmap)

당 워크스페이스의 성숙도와 요구사항을 토대로 식별된 핵심 자동화 후보들입니다.

| 후보 ID | 자동화 영역 | 제안 내용 | 기대 효과 및 우선순위 |
| :--- | :--- | :--- | :--- |
| **AEA-AUTO-014** | Pipeline | CI 내 Docker 이미지 CVE 취약점 자동 스캔 (Trivy 연동) | 인프라 취약점 선제 탐지 (높음) |
| **AEA-AUTO-015** | Workflow | 다중 에이전트 분산/병렬 작업 오케스트레이터 구축 | 작업 속도 단축 및 분할 실행 (중간) |
| **AEA-AUTO-016** | QA | 문맥적/의미적 에이전트 출력 평가(Semantic Eval) CI 적용 | 설계서와 구현 코드 일치율 자동 검증 (높음) |
| **AEA-AUTO-017** | Harness | 프로바이더 무관 공통 CLI 래퍼 (`antigravity run`) 구현 | 훅 및 포스트 검증의 균일한 강제 (높음) |
| **AEA-AUTO-018** | Security | SBOM(Software Bill of Materials) 빌드 타임 자동 생성 | 소프트웨어 공급망 투명성 확보 (중간) |
| **AEA-AUTO-019** | Security | 빌드 및 배포 산출물 암호화 서명 및 attestation 증적 확보 | 배포본 오염 방지 및 인증 (낮음) |
| **AEA-AUTO-020** | Formatting | 에이전트 지침 텍스트 마크다운-TOML 동종 변환 컴파일러 구축 | Claude/Codex 런타임 지침 불일치 방지 (중간) |
| **AEA-AUTO-021** | Workflow | 스펙 주도 SDLC 문서 간 링크 유효성 상시 데몬 스캔 | Stale 링크 및 깨진 참조 실시간 경고 (낮음) |
| **AEA-AUTO-022** | QA | 코드 스타일 위반 우회 지시(eslint-disable 등) 탐지 필터 | 무분별한 린팅 규칙 우회 시도 탐지 (중간) |
| **AEA-AUTO-023** | Tooling | `graphify update` 명령어의 Git Hook 자동 실행 연동 | 소스 수정 즉시 지식 그래프 리프레시 (중간) |
| **AEA-AUTO-024** | Pipeline | 로컬 개발 도구 버전과 CI 가상 컨테이너 버전 일치 검증 스캔 | 버전 불일치로 인한 빌드 에러 조기 차단 (높음) |
| **AEA-AUTO-025** | Workflow | Stage 04 실행 계획 템플릿 마이그레이션 도구 | 템플릿 필드 개편 시 기존 문서 자동 변환 (낮음) |
| **AEA-AUTO-026** | QA | 검증 증적(Evidence) 란의 무의미한 텍스트 기재 탐지 파서 | 바이브코딩 형식적 승인 우회 차단 (높음) |
| **AEA-AUTO-027** | Tooling | 릴리즈 노트 자동 생성 및 Stage 05 배포 절차 문서 자동화 | 배포 운영 업무 효율화 (낮음) |

## 2. 핵심 추진 권고사항 (Immediate Action Items)

- **우선순위 1단계 (High)**:
  - **AEA-AUTO-016 (Semantic Eval)** 및 **AEA-AUTO-017 (Common CLI Wrapper)**. 이 두 항목은 에이전트의 구문 검사와 의미 검사를 모두 기계적 루프에 편입시켜, 바이브코딩에 대항하는 완벽한 하네스를 만드는 데 가장 중요합니다.
- **우선순위 2단계 (Medium)**:
  - **AEA-AUTO-020 (Instruction Compiler)** 및 **AEA-AUTO-023 (Git Hook Graphify)**. 멀티 프로바이더 운용 중에 발생할 수 있는 지침 동기화 오차와 stale 지식 데이터를 차단합니다.

## Related Documents

- [README.md](./README.md)
- [implementation-overview.md](./implementation-overview.md)
- [harness-loop-audit.md](./harness-loop-audit.md)
- [sdlc-qa-security-audit.md](./sdlc-qa-security-audit.md)
