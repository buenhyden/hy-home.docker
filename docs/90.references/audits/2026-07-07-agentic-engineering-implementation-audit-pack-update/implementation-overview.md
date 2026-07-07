---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/implementation-overview.md -->

# Reference: Agentic Engineering Implementation Overview (2026-07-07 Update)

## Overview

본 보고서는 사용자가 요청한 23대 핵심 항목에 대한 `hy-home.docker` 워크스페이스의 실제 구현 성숙도를 점검한 종합 현황 분석 리포트입니다.

## Assessment Matrix (23대 항목 일대일 매핑)

| 번호 | 분석 요청 항목 | 구현 성숙도 | 근거 파일 및 매핑 현황 | 부족한 요소 및 개선/수정/보완 사항 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **각 항목 및 세부 항목 정의** | Implemented | [README.md](./README.md) | 전체 구조화는 마쳤으나 정기적인 오딧 주기가 자동 바인딩되지 않음. |
| 2 | **조사한 항목과 비교하여 부족한 요소 등** | Implemented | [Research README](../../research/2026-07-07-agentic-research-pack-update/README.md) | 외부 학술/공학 데이터와의 지속적인 갱신 파이프라인 부재. |
| 3 | **하네스 엔지니어링 구현 현황 및 보완 사항** | Implemented | `harness-implementation-map.md`, `check-repo-contracts.sh` | 로컬 하네스 검증 규칙은 견고하나, 프로바이더별 실행 권한 강제 수준 편차 보완 필요. |
| 4 | **루프 엔지니어링 구현 현황 및 보완 사항** | Partially Implemented | `subagent-protocol.md`, `post-tool-validate.sh` | inner/outer loop는 완성되었으나, 에이전트 설계 타당성에 대한 의미론적(Semantic) eval 평가 루프가 미비함. |
| 5 | **Claude/Codex/Gemini 개별 하네스 및 루프** | Partially Implemented | `providers/claude.md`, `providers/gemini.md`, `providers/codex.md` | Claude/Codex는 자동 훅이 매핑되나, Gemini는 런타임 hook 및 subagent 자동화 수준이 낮아 수동 실행에 의존함. |
| 6 | **Claude/Codex/Gemini 공통 환경 및 규칙** | Implemented | `rules/provider-capability-matrix.md` | 에이전트 인스트럭션과 템플릿 계약은 통합되었으나, 프로바이더에 독립적인 Universal CLI Wrapper가 아직 없음. |
| 7 | **워크스페이스 규칙, 체계, 환경 보완 사항** | Implemented | `rules/bootstrap.md`, `rules/agentic.md` | 규칙 명세는 엄격하나, 에이전트가 예외적 행동을 할 때 실시간 로컬 경고(Warning)를 제공하는 모니터링 데몬 부재. |
| 8 | **워크스페이스 내 자동화(pipeline, workflow 등)** | Partially Implemented | `scripts/validation/run-local-qa-gates.sh` | 로컬 QA 및 index 갱신은 갖추어져 있으나, 단계 전환 시 markdown links 무결성을 주기적으로 스캔하는 자동화 파이프라인 부족. |
| 9 | **스펙 주도(spec-driven) 개발 보완 사항** | Implemented | `docs/03.specs/`, `docs/04.execution/plans/` | Spec -> Plan -> Task -> Evidence 흐름이 잡혀 있으나, 스펙 작성 누락을 자동으로 탐지하는 CI 하드 게이트가 미약함. |
| 10 | **Project Template 보완 사항** | Implemented | `docs/99.templates/` | 표준 템플릿(Plan, Task, Progress 등)이 존재하나, 템플릿 필드가 변경될 때 기존 문서들을 일괄 마이그레이션하는 유틸리티 부재. |
| 11 | **AI agent instruction 보완 사항** | Implemented | `docs/00.agent-governance/agents/` | 15개 에이전트의 Covers/Excludes가 정의되어 있으나, 지침 텍스트를 최신 규칙에 맞춰 기계적으로 동기화하는 컴파일 툴이 없음. |
| 12 | **SDLC 보완 사항** | Implemented | `docs/README.md`, `stage-authoring-matrix.md` | Requirements에서 Operations로 흐르는 SSoT 단계 게이트는 훌륭하나, 단계 간 일관성(Consistency) 검증이 일부 수동 검사 상태임. |
| 13 | **CI/CD 보완 사항** | Implemented | `.github/workflows/ci-quality.yml` | 10여 개의 병렬 검증 액션 파이프라인이 작동 중이나, 로컬 빌드 환경(Node, Python 버전)과 CI 컨테이너 간의 버전 드리프트 차단 보완 필요. |
| 14 | **QA (포맷팅, 린팅, 문법 오류) 보완 사항** | Partially Implemented | `scopes/qa.md`, `.pre-commit-config.yaml` | 개별 스크립트 및 문서 검사는 양호하나, 전체 코드베이스를 포괄하는 에러 및 미사용 임포트 감지 린터 규칙 보완 필요. |
| 15 | **포맷팅(Formatting) 보완 사항** | Implemented | `post-tool-validate.sh`, `.pre-commit-config.yaml` | Markdown, Shell 등의 포맷팅은 통제되나, 다중 에이전트 동시 작업 시 발생하는 공백 포맷 충돌 자동 해결 기능 미흡. |
| 16 | **코드 스타일 검사(Linting) 보완 사항** | Implemented | `.github/workflows/ci-quality.yml` | 린트 경고가 CI 빌드를 실패하게 만들도록 잡혀 있으나, 린팅 규칙 완화 예외 처리의 승인 프로세스 부재. |
| 17 | **Automation 보완 사항** | Partially Implemented | `scripts/README.md` | 로컬 스크립트 기반 검사 자동화는 완성되었으나, 릴리즈 노트 자동 생성 및 도큐멘테이션 배포 자동화와 같은 CD 레이어의 결여. |
| 18 | **pipeline 보완 사항** | Partially Implemented | `.github/workflows/ci-quality.yml` | CI 파이프라인은 잘 돌고 있으나, 컨테이너 보안 이미지 스캔 및 CVE 취약점 분석 파이프라인 보완 필요. |
| 19 | **workflow 보완 사항** | Partially Implemented | `.agents/workflows/` | 에이전트의 작업 시작-끝의 로컬 워크플로가 잡혀 있으나, multi-agent 분산 병렬 작업 워크플로 관리 오케스트레이션 미흡. |
| 20 | **보안(Security) 보완 사항** | Partially Implemented | `rules/approval-boundaries.md`, `SECURITY.md` | 비밀값 마운트 및 git 커밋 차단은 작동 중이나, SBOM 생성 및 SLSA 증적 서명 자동화 같은 공급망 보안 요소 보완 필요. |
| 21 | **바이브코딩(Vibe Coding) 통제 보완 사항** | Implemented | `rules/agentic.md` (Implementation Flow) | Plan 우선 승인 및 최소 변경(Surgical Edit) 강제는 갖췄으나, 검증 결과(Evidence)를 누락하고 맘대로 소스를 덮어쓰는 에이전트 우회 시도 차단 보완 필요. |
| 22 | **워크스페이스 내 필요한 AI Agent 보완 사항** | Implemented | `docs/00.agent-governance/agents/` | 15개 에이전트가 존재하며, 향후 성능 최적화 전문가 등 3종의 전용 에이전트 추가 보완이 요구됨. |
| 23 | **agency-agents 비교 및 에이전트 보완** | Implemented | [ai-agent-catalogs.md](../../research/2026-07-07-agentic-research-pack-update/ai-agent-catalogs.md) | 대규모 페르소나와 비교 완료했으며, 워크스페이스의 15종 에이전트 정의의 구조적 격차 식별 및 추가 제안 작성 완료. |

## Key Findings & Core Recommendations

1. **Gemini Parity Gap**: Claude와 Codex는 에이전트 런타임 제어가 기계적으로 긴밀하나, Gemini는 behavioral pointer(지침 수동 준수)에 과하게 의존합니다. Gemini 환경에서 훅을 강제하기 위한 쉘 수준의 공통 CLI Wrapper(예: `antigravity run`) 도입을 권장합니다.
2. **Semantic Eval System**: 정규식 및 lint 중심의 구문 검사는 튼튼하지만, 에이전트가 생성한 설계의 타당성과 일관성을 판별하는 시맨틱 자동 평가 루프가 아직 부재합니다. advisory 상태인 agent-output-eval runner를 CI의 하드 게이트로 승격할 계획을 수립해야 합니다.
3. **Security Supply Chain (SLSA/SBOM)**: 코드 자체의 보안 점검(`check-template-security-baseline.sh` 등)은 활성화되어 있으나, 공급망 안정성을 위한 SBOM 생성, 바이너리 서명 및 attestation 파이프라인이 누락되어 있어 보완이 시급합니다.

## Related Documents

- [README.md](./README.md)
- [harness-loop-audit.md](./harness-loop-audit.md)
- [sdlc-qa-security-audit.md](./sdlc-qa-security-audit.md)
- [agent-catalog-audit.md](./agent-catalog-audit.md)
