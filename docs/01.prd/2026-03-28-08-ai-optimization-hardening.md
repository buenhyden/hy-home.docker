# 08-AI Optimization & Hardening Product Requirements

## Overview (KR)

이 문서는 `infra/08-ai` 계층(Ollama, Open WebUI)의 최적화/하드닝 요구사항을 정의한다. 목표는 gateway 경계 보안 표준화, GPU 자원 보호를 위한 동시성 제어, health 기반 안정성 강화, 그리고 카탈로그 기반 확장 정책(모델 승격, 접근 통제, 로그 보존/마스킹)의 실행 로드맵 수립이다.

## Vision

AI 계층을 "기본적으로 안전하고, 리소스 폭주에 강하며, 운영 승격 기준이 명확한" 로컬 추론 플랫폼으로 표준화한다.

## Problem Statement

- AI 라우터 middleware가 gateway 표준 체인을 완전하게 포함하지 않아 경계 보안 일관성이 떨어질 수 있다.
- Ollama 동시 처리 상한이 명시되지 않으면 VRAM/queue 폭주로 지연 및 장애 전파 위험이 커진다.
- Open WebUI는 상태 저장 서비스임에도 배포 템플릿이 stateful 정책과 불일치해 drift 위험이 있다.
- Exporter 관측 경로의 health 기반 검증이 약하면 모니터링 신뢰도가 저하될 수 있다.
- 카탈로그가 요구한 모델 승격, 접근 권한 분리, 대화 로그 보존/마스킹 정책이 운영 실행 문서로 완결되지 않았다.

## Personas

- **Platform SRE**: AI 계층의 가용성과 보안을 동시에 보장해야 한다.
- **DevOps Engineer**: Compose/CI 하드닝 기준선을 지속 유지해야 한다.
- **AI Platform Owner**: 모델 도입/승격, 사용자 접근, 로그 정책을 통제해야 한다.

## Key Use Cases

- **STORY-AI-01**: 운영자는 Ollama/Open WebUI 경로가 gateway+SSO 정책을 준수하는지 검증한다.
- **STORY-AI-02**: 엔지니어는 Ollama 동시성/큐 상한을 조정해 GPU 폭주를 방지한다.
- **STORY-AI-03**: CI는 AI tier 하드닝 회귀를 PR 단계에서 자동 차단한다.
- **STORY-AI-04**: 팀은 모델 승격 절차와 Open WebUI 접근/로그 정책을 운영 기준으로 추적한다.

## Functional Requirements

- **REQ-PRD-AI-FUN-01**: Ollama/Open WebUI 공개 라우터는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용해야 한다.
- **REQ-PRD-AI-FUN-02**: Ollama는 동시성/모델 로딩/큐 상한(`OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_MAX_QUEUE`)을 명시해야 한다.
- **REQ-PRD-AI-FUN-03**: Open WebUI는 stateful 템플릿 계약을 사용해야 한다.
- **REQ-PRD-AI-FUN-04**: `ollama-exporter`는 health 기반 dependency와 metrics healthcheck를 제공해야 한다.
- **REQ-PRD-AI-FUN-05**: `scripts/check-ai-hardening.sh`와 CI `ai-hardening` job을 제공해야 한다.
- **REQ-PRD-AI-FUN-06**: `docs/01~09` optimization-hardening 문서 세트와 README 인덱스를 동기화해야 한다.
- **REQ-PRD-AI-FUN-07**: 카탈로그 기준으로 모델 승격 절차, Open WebUI 모델 접근 권한 분리, 대화 로그 보존/마스킹 정책을 Plan/Tasks/Operations에 반영해야 한다.

## Success Criteria

- **REQ-PRD-AI-MET-01**: `bash scripts/check-ai-hardening.sh` 실패 0건.
- **REQ-PRD-AI-MET-02**: AI compose 정적 검증 통과.
- **REQ-PRD-AI-MET-03**: AI optimization-hardening 문서 간 양방향 링크 정합성 확보.
- **REQ-PRD-AI-MET-04**: 카탈로그 08-ai 확장 항목이 Plan/Tasks/Operations에 반영.

## Scope and Non-goals

- **In Scope**:
  - `infra/08-ai/ollama/docker-compose.yml`
  - `infra/08-ai/open-webui/docker-compose.yml`
  - `scripts/check-ai-hardening.sh`
  - `.github/workflows/ci-quality.yml`
  - `docs/01~09` AI optimization-hardening 문서 및 README 인덱스
- **Out of Scope**:
  - 실제 모델 학습/파인튜닝 파이프라인 구축
  - Qdrant 자체 인프라 아키텍처 변경
- **Non-goals**:
  - 즉시 멀티노드 Ollama 클러스터 전환
  - 외부 상용 LLM API 표준화 작업 동시 추진

## Risks, Dependencies, and Assumptions

- SSO/미들웨어 강화는 기존 테스트 스크립트/자동화 접근 경로 조정이 필요할 수 있다.
- AI tier는 `01-gateway` Traefik, `02-auth` SSO, `04-data` Qdrant 및 PostgreSQL 설정에 의존한다.
- 모델 승격/접근 정책은 운영 승인 체계를 전제로 하며, 단일 릴리스에서 완전 자동화하지 않는다.

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: compose/script/docs/ci 하드닝 변경과 정적 검증 실행
- **Disallowed Actions**: 인증 우회, unpinned 이미지 도입, 무검증 포트 확장
- **Human-in-the-loop Requirement**: 접근제어 완화, 로그 보존 완화, 모델 승격 정책 예외는 승인 필수
- **Evaluation Expectation**: `check-ai-hardening` + 공통 기준선 + 문서 추적성 통과

## Related Documents

- **ARD**: [../02.ard/0023-ai-optimization-hardening-architecture.md](../02.ard/0023-ai-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/08-ai/spec.md](../04.specs/08-ai/spec.md)
- **Plan**: [../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md](../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- **ADR**: [../03.adr/0023-ai-hardening-and-ha-expansion-strategy.md](../03.adr/0023-ai-hardening-and-ha-expansion-strategy.md)
- **Tasks**: [../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md](../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/08-ai/optimization-hardening.md](../07.guides/08-ai/optimization-hardening.md)
- **Operation**: [../08.operations/08-ai/optimization-hardening.md](../08.operations/08-ai/optimization-hardening.md)
- **Runbook**: [../09.runbooks/08-ai/optimization-hardening.md](../09.runbooks/08-ai/optimization-hardening.md)
