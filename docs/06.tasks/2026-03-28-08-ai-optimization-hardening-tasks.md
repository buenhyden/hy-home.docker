# Task: 08-AI Optimization Hardening

## Overview (KR)

이 문서는 `08-ai` 최적화/하드닝 실행 태스크를 추적한다. compose hardening, CI 게이트, 문서 추적성, 카탈로그 확장 정책(모델 승격/접근 분리/로그 마스킹)을 작업 단위로 관리한다.

## Inputs

- **Parent Spec**: [../04.specs/08-ai/spec.md](../04.specs/08-ai/spec.md)
- **Parent Plan**: [../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md](../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md)

## Working Rules

- AI 구성 변경은 compose static validation + hardening script 결과를 남긴다.
- gateway/auth 영향이 있는 변경은 보안 경계 영향도를 기록한다.
- 문서 변경은 PRD~Runbook 링크와 README 인덱스를 동시 갱신한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-AI-001 | Ollama/Open WebUI middleware를 gateway+SSO 체인으로 정렬 | impl | Contracts / Config | PLN-AI-001 | compose label 확인 | DevOps | Done |
| T-AI-002 | Ollama concurrency/queue 상한 환경 변수 추가 | impl | Contracts / Config | PLN-AI-002 | env contract 확인 | DevOps | Done |
| T-AI-003 | Open WebUI stateful 템플릿 정렬 | impl | Contracts / Config | PLN-AI-003 | template 확인 | DevOps | Done |
| T-AI-004 | exporter health-gated dependency + healthcheck 추가 | impl | Contracts / Config | PLN-AI-004 | dependency/healthcheck 확인 | DevOps | Done |
| T-AI-005 | AI hardening script 추가/수정 | ops | Governance Contract | PLN-AI-005 | `bash scripts/check-ai-hardening.sh` | DevOps | Done |
| T-AI-006 | CI `ai-hardening` job 추가 | ops | Governance Contract | PLN-AI-005 | workflow job 확인 | DevOps | Done |
| T-AI-007 | scripts inventory/usage README 갱신 | doc | Related Docs | PLN-AI-005 | README 항목 반영 | Docs | Done |
| T-AI-008 | PRD/ARD/ADR/Plan/Task/Guide/Ops/Runbook 문서 생성 | doc | Related Docs | PLN-AI-006 | 링크/인덱스 동기화 | Docs | Done |
| T-AI-009 | Ollama 모델 승격 절차 정의(실험 -> 운영) | doc | Catalog-aligned Expansion | PLN-AI-007 | operations/tasks 반영 | AI Owner | Done |
| T-AI-010 | Open WebUI 모델 접근 권한 분리 기준 정의 | doc | Catalog-aligned Expansion | PLN-AI-007 | operations/tasks 반영 | AI Owner | Done |
| T-AI-011 | Open WebUI 대화 로그 보존/마스킹 정책 정의 | doc | Catalog-aligned Expansion | PLN-AI-007 | operations/tasks 반영 | Security/AI Owner | Done |
| T-AI-012 | 정적 검증 실행 및 결과 기록 | test | Verification | PLN-AI-001~007 | compose/script/baseline/traceability 체크 | DevOps | Done |
| T-AI-013 | runtime 기동 리허설 및 성능 튜닝 증적 수집 | test | Verification | PLN-AI-001~007 | health/latency/gpu metrics 기록 | DevOps | Planned |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-AI-001
- [x] T-AI-002
- [x] T-AI-003
- [x] T-AI-004
- [x] T-AI-005
- [x] T-AI-006
- [x] T-AI-007

### Phase 2

- [x] T-AI-008
- [x] T-AI-009
- [x] T-AI-010
- [x] T-AI-011
- [x] T-AI-012
- [ ] T-AI-013

## Verification Summary

- **Test Commands**:
  - `docker compose -f infra/08-ai/ollama/docker-compose.yml config`
  - `docker compose -f infra/08-ai/open-webui/docker-compose.yml config`
  - `bash scripts/check-ai-hardening.sh`
  - `bash scripts/check-template-security-baseline.sh`
  - `bash scripts/check-doc-traceability.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: 로컬 검증 로그 + CI `ai-hardening` job

## Related Documents

- **PRD**: [../01.prd/2026-03-28-08-ai-optimization-hardening.md](../01.prd/2026-03-28-08-ai-optimization-hardening.md)
- **ARD**: [../02.ard/0023-ai-optimization-hardening-architecture.md](../02.ard/0023-ai-optimization-hardening-architecture.md)
- **ADR**: [../03.adr/0023-ai-hardening-and-ha-expansion-strategy.md](../03.adr/0023-ai-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md](../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- **Guide**: [../07.guides/08-ai/optimization-hardening.md](../07.guides/08-ai/optimization-hardening.md)
- **Operation**: [../08.operations/08-ai/optimization-hardening.md](../08.operations/08-ai/optimization-hardening.md)
- **Runbook**: [../09.runbooks/08-ai/optimization-hardening.md](../09.runbooks/08-ai/optimization-hardening.md)
