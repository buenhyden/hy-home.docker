# 08-AI Optimization Hardening Implementation Plan

## Overview (KR)

이 문서는 `infra/08-ai` 최적화/하드닝 실행 계획서다. gateway 경계 보안 정렬, GPU concurrency 보호, Open WebUI stateful 일관성, exporter health 계약, CI 정책 게이트, 카탈로그 확장 정책을 단계적으로 수행한다.

## Context

- 기준 카탈로그: [../08.operations/12-infra-service-optimization-catalog.md](../08.operations/12-infra-service-optimization-catalog.md)
- 상위 우선순위 계획: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- 대상 구성: `infra/08-ai/**/*`, `scripts/`, `.github/workflows/`, `docs/01~09`

## Goals & In-Scope

- **Goals**:
  - Ollama/Open WebUI 공개 경로를 gateway 표준+SSO 정책으로 정렬한다.
  - Ollama GPU 자원 보호를 위한 concurrency/queue 상한을 명시한다.
  - Open WebUI를 stateful 운영 템플릿으로 정렬한다.
  - exporter를 health-gated startup으로 안정화한다.
  - AI 하드닝 회귀를 script/CI로 조기 차단한다.
  - 카탈로그 확장 항목(모델 승격/접근 분리/로그 정책)을 문서/태스크로 실행 가능하게 한다.
- **In Scope**:
  - `infra/08-ai/ollama/docker-compose.yml`
  - `infra/08-ai/open-webui/docker-compose.yml`
  - `scripts/check-ai-hardening.sh`
  - `scripts/README.md`
  - `.github/workflows/ci-quality.yml`
  - `docs/01~09` AI optimization-hardening 문서/README

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 즉시 다중 노드/다중 리전 AI 추론 아키텍처 전환
  - 외부 LLM provider 표준화
- **Out of Scope**:
  - Qdrant 내부 데이터 모델 변경
  - 모델 학습/파인튜닝 파이프라인 구축

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-AI-001 | Ollama/Open WebUI gateway+SSO middleware 정렬 | `infra/08-ai/*/docker-compose.yml` | REQ-PRD-AI-FUN-01 | compose labels 확인 |
| PLN-AI-002 | Ollama concurrency/queue/resource 상한 명시 | `infra/08-ai/ollama/docker-compose.yml` | REQ-PRD-AI-FUN-02 | env contract 확인 |
| PLN-AI-003 | Open WebUI stateful 템플릿 정렬 | `infra/08-ai/open-webui/docker-compose.yml` | REQ-PRD-AI-FUN-03 | `template-stateful-med` 확인 |
| PLN-AI-004 | exporter health-gated dependency 및 healthcheck 보강 | `infra/08-ai/ollama/docker-compose.yml` | REQ-PRD-AI-FUN-04 | `depends_on`/healthcheck 확인 |
| PLN-AI-005 | AI hardening script + CI 게이트 추가 | `scripts/check-ai-hardening.sh`, `.github/workflows/ci-quality.yml`, `scripts/README.md` | REQ-PRD-AI-FUN-05 | script/CI job 확인 |
| PLN-AI-006 | PRD~Runbook 문서 체계 생성 및 상호 링크 | `docs/01~09/**` | REQ-PRD-AI-FUN-06 | 링크 정합성 확인 |
| PLN-AI-007 | 카탈로그 확장 정책 작업 분해(모델 승격/접근 분리/로그 정책) | Plan/Task/Ops/Guide docs | REQ-PRD-AI-FUN-07 | 태스크/정책 반영 확인 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-AI-001 | Structural | Ollama compose 정적 검증 | `docker compose -f infra/08-ai/ollama/docker-compose.yml config` | 오류 없음 |
| VAL-AI-002 | Structural | Open WebUI compose 정적 검증 | `docker compose -f infra/08-ai/open-webui/docker-compose.yml config` | 오류 없음 |
| VAL-AI-003 | Compliance | AI 하드닝 기준선 검증 | `bash scripts/check-ai-hardening.sh` | 실패 0건 |
| VAL-AI-004 | Baseline | 템플릿/보안 기준선 | `bash scripts/check-template-security-baseline.sh` | 실패 0건 |
| VAL-AI-005 | Traceability | 문서 추적성 검증 | `bash scripts/check-doc-traceability.sh` | 실패 0건 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| concurrency 상한 설정 부적합으로 처리량 저하 | Medium | 단계적 튜닝 + exporter 지표 기반 재조정 |
| SSO 강화로 기존 테스트 경로 차단 | Medium | runbook에 예외/복구 절차 반영 |
| 로그 보존/마스킹 정책 미정으로 운영 편차 | Medium | operations/task에 승인 게이트 명시 |
| stateful 템플릿 drift 재발 | Low | AI hardening script로 정책 강제 |

## Completion Criteria

- [x] AI compose/script/ci 하드닝 반영
- [x] AI optimization-hardening 문서 세트 생성
- [x] docs `01~09` README 인덱스 반영
- [ ] runtime 기동/리허설 증적 확보 (환경 허용 시)

## Related Documents

- **PRD**: [../01.prd/2026-03-28-08-ai-optimization-hardening.md](../01.prd/2026-03-28-08-ai-optimization-hardening.md)
- **ARD**: [../02.ard/0023-ai-optimization-hardening-architecture.md](../02.ard/0023-ai-optimization-hardening-architecture.md)
- **ADR**: [../03.adr/0023-ai-hardening-and-ha-expansion-strategy.md](../03.adr/0023-ai-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../04.specs/08-ai/spec.md](../04.specs/08-ai/spec.md)
- **Tasks**: [../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md](../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/08-ai/optimization-hardening.md](../07.guides/08-ai/optimization-hardening.md)
- **Operations**: [../08.operations/08-ai/optimization-hardening.md](../08.operations/08-ai/optimization-hardening.md)
- **Runbooks**: [../09.runbooks/08-ai/optimization-hardening.md](../09.runbooks/08-ai/optimization-hardening.md)
