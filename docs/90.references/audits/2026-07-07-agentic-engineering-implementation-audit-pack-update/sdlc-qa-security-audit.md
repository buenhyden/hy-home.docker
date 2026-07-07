---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/sdlc-qa-security-audit.md -->

# Reference: SDLC, QA, Security, and Vibe Coding Audit

## Overview

본 보고서는 `hy-home.docker` 워크스페이스의 스펙 주도 SDLC 체계, CI/CD 및 QA 다중 필터 게이트, 보안 성숙도 수준, 그리고 바이브코딩(Vibe Coding)을 억제하기 위한 제어 시스템의 유효성을 진단한 결과서입니다.

## Purpose

코드와 환경, 그리고 문서의 일관성을 기계적으로 검증하여 인간 개발자와 AI 에이전트의 품질 신뢰도를 보장합니다.

## Repository Role

본 문서는 개발 프로세스 전반에 대한 오딧 참조 정보이며, 실제 CI 액션 파일이나 린팅 구성 파일의 규칙 설정을 직접 변경하지 않습니다.

---

## 1. SDLC 및 스펙 주도 개발 (Spec-driven SDLC) 감사

### A. 구현 현황
- **문서화 생명주기 관리**: `01.requirements` -> `02.architecture` -> `03.specs` -> `04.execution` -> `05.operations` 로 구성된 템플릿 계약이 활성화되어 있으며, 문서가 완결되면 `status: completed`로 전이되도록 규약화되어 있습니다.
- **실행 계획과 작업 증적 연계**: 모든 04/plans 마크다운에는 실행 전 사용자 진행 승인을 받게 설계되어 있으며, 수행 후 `04.execution/tasks/` 하위에 검증 결과 증적을 남기게 구성되어 있어 이중 체크가 가능합니다.

### B. 격차 및 부족한 요소 (Gaps)
- **추적 자동화 스캔의 부분성**: 스펙 파일과 실행 작업 간의 연결(traceability)을 검사하는 `check-doc-traceability.sh`가 존재하나, 단순히 링크 매칭 여부만 검사할 뿐 스사(Spec-Driven) 개발 규약에 따른 미작성 단계가 존재할 때 빌드를 강제 중단하는 하드 CI 게이트 강도가 다소 느슨합니다.

---

## 2. CI/CD 및 QA (포맷팅, 린팅, 문법 오류) 감사

### A. 구현 현황
- **CI/CD 파이프라인**: GitHub Actions의 `ci-quality.yml`이 리포지토리의 무결성을 여러 병렬 잡(Job)으로 검증합니다.
- **QA 3대 축 제어**:
  - **포맷팅**: 로컬 `post-tool-validate.sh` 및 pre-commit이 공백 및 마크다운 신택스 스타일을 자동 보정합니다.
  - **린팅**: ESLint, Shellcheck, YAML lint가 문법 외 스타일 정적 분석을 수행합니다.
  - **문법 오류**: `validate-docker-compose.sh` 등이 도커 구문 파싱 오류를 사전 차단합니다.

### B. 격차 및 부족한 요소 (Gaps)
- **CI 환경과의 버전 드리프트**: 로컬 개발자 환경의 Node.js/Python 버전과 CI GitHub Actions 환경의 기본 컨테이너 버전이 일치하지 않을 때, 로컬 린터 검사가 CI에서 다르게 동작하여 빌드가 예기치 않게 깨지는 현상이 감지되었습니다.
- **린팅 강도 강제 예외 처리**: 일부 디렉토리(예: 레거시 아카이브, 임시 스크립트)에서 린트 규칙 위반을 우회하기 위해 `eslint-disable`을 남용할 때 이를 감지하거나 승인하는 규칙이 보완되어야 합니다.

---

## 3. 보안(Security) 감사

### A. 구현 현황
- **자격 증명 경계 격리**: 실제 패스워드나 민감 변수값을 `.env.example` 및 `secrets/` 하위 마운트로 관리하고, git 형상 관리에 올리지 않도록 `validate-docker-compose.sh --preflight` 스캔 단계가 존재합니다.
- **승인 제한**: `rules/approval-boundaries.md`를 통해 보호해야 할 디렉토리 및 위험 명령어 사용 권한을 에이전트로부터 격리하고 있습니다.

### B. 격차 및 부족한 요소 (Gaps)
- **공급망 보안 및 SBOM 누락**: 최신 보안 표준(SSDF, SLSA) 기준과 비교했을 때, SBOM(Software Bill of Materials)의 자동 생성, 빌드 아티팩트 서명 및 attestation 증적 확보 파이프라인이 누락되어 있습니다.
- **컨테이너 이미지 취약점 정기 스캔 부재**: 도커 베이스 이미지 자체의 CVE 취약점을 주기적으로 스캔하여 드리프트를 경고하는 Trivy나 Grype 스캐너와의 통합이 미흡합니다.

---

## 4. 바이브코딩 (Vibe Coding) 제어 시스템 감사

### A. 구현 현황
- **Surgical Edit 가이드라인**: `rules/agentic.md`에 의거하여, 에이전트는 무분별한 리팩토링이나 관련 없는 인접 코드의 자의적 개선을 금지당하며, 최소 단위의 변경(Surgical Edit)을 적용해야 합니다.
- **검증 증적 강제**: 수정 완료 시 반드시 validator 실행 증적(Evidence)을 `task.md`와 `progress.md`에 기재해야만 완료가 승인되므로 바이브코딩이 상당 수준 제약됩니다.

### B. 격차 및 부족한 요소 (Gaps)
- **형식적 통제 우회 위험**: 일부 에이전트가 `task.md`를 작성하면서 검증 증적란에 실제 스크립트 수행 로그가 아닌 "검증 성공함(Pass)" 이라는 텍스트만 적고 넘어가는 형식적 속임수(Token-based shortcuts)를 방지하는 정밀 유효성 스캐너가 아직 구축되지 않았습니다.

## Related Documents

- [README.md](./README.md)
- [implementation-overview.md](./implementation-overview.md)
- [harness-loop-audit.md](./harness-loop-audit.md)
- [agent-catalog-audit.md](./agent-catalog-audit.md)
