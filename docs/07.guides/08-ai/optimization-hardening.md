# 08-AI Optimization Hardening Guide

## Overview (KR)

이 문서는 `08-ai` 계층의 최적화/하드닝 변경을 운영자와 개발자가 재현 가능하게 적용하기 위한 가이드다. gateway 경계 보안, GPU concurrency 제어, stateful 템플릿 일관성, health 기반 검증 절차를 제공한다.

## Guide Type

`system-guide | how-to`

## Target Audience

- SRE / Platform Operator
- DevOps Engineer
- AI Platform Owner

## Purpose

- Ollama/Open WebUI 공개 경로를 gateway+SSO 정책에 정렬한다.
- Ollama GPU 자원 보호를 위한 concurrency/queue 상한을 적용한다.
- Open WebUI stateful 운영 일관성을 확보한다.
- AI 하드닝 회귀를 script/CI로 조기 차단한다.
- 카탈로그 확장 항목(모델 승격/접근 분리/로그 정책)을 운영 기준으로 반영한다.

## Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/08-ai` 수정 권한
- Traefik middleware(`gateway-standard-chain`, `sso-errors`, `sso-auth`) 준비

## Step-by-step Instructions

1. 정적 구성 점검
   - `docker compose -f infra/08-ai/ollama/docker-compose.yml config`
   - `docker compose -f infra/08-ai/open-webui/docker-compose.yml config`
2. Gateway/SSO 경계 정렬
   - Ollama/Open WebUI 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
3. Ollama 리소스 보호 적용
   - `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_MAX_QUEUE` 상한을 확인/조정한다.
4. Open WebUI stateful 일관성 확인
   - Open WebUI가 `template-stateful-med`를 사용하도록 확인한다.
5. Exporter 안정성 강화 확인
   - `ollama-exporter`가 `ollama` `service_healthy`에 의존하는지 확인한다.
   - metrics healthcheck(`http://localhost:${OLLAMA_EXPORTER_PORT:-11435}/metrics`)를 확인한다.
6. 기준선 검증 실행
   - `bash scripts/check-ai-hardening.sh`
   - `bash scripts/check-template-security-baseline.sh`
   - `bash scripts/check-doc-traceability.sh`
7. 카탈로그 확장 운영 기준 반영
   - 모델 승격 절차(실험 -> 운영)를 tasks/operations에 반영한다.
   - Open WebUI 모델 접근 권한 분리 기준을 반영한다.
   - 대화 로그 보존/마스킹 정책을 반영한다.

## Common Pitfalls

- middleware 체인을 일부 라우터에만 적용하는 실수
- Ollama 상한 없이 고동시성 부하를 허용해 GPU OOM을 유발하는 실수
- Open WebUI를 stateless 템플릿으로 운용해 상태 드리프트를 유발하는 실수
- exporter health 계약 없이 모니터링 신뢰도를 낮추는 실수

## Related Documents

- **PRD**: [../../01.prd/2026-03-28-08-ai-optimization-hardening.md](../../01.prd/2026-03-28-08-ai-optimization-hardening.md)
- **Spec**: [../../04.specs/08-ai/spec.md](../../04.specs/08-ai/spec.md)
- **Plan**: [../../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md](../../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)
- **Operation**: [../../08.operations/08-ai/optimization-hardening.md](../../08.operations/08-ai/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/08-ai/optimization-hardening.md](../../09.runbooks/08-ai/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
