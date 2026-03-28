# 08-AI Optimization Hardening Runbook

## Overview (KR)

이 런북은 `08-ai` 하드닝 항목에서 발생하는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. gateway/SSO 체인 누락, Ollama concurrency 설정 누락, Open WebUI stateful 드리프트, exporter health 계약 실패, CI 게이트 실패를 중심으로 점검/복구한다.

## Purpose

- AI 공개 경로 보안과 GPU 안정성 기준을 빠르게 복구한다.
- compose/script/CI 회귀를 표준 절차로 차단한다.

## Canonical References

- [Spec](../../04.specs/08-ai/spec.md)
- [Operations Policy](../../08.operations/08-ai/optimization-hardening.md)
- [Plan](../../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- [Tasks](../../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)

## When to Use

- `ai-hardening` CI가 실패할 때
- Ollama/Open WebUI 경로 접근 정책이 비정상일 때
- Ollama GPU 과부하/OOM 또는 queue 적체가 반복될 때
- exporter metrics 수집이 실패할 때

## Procedure or Checklist

### Checklist

- [ ] 실패 항목(middleware, concurrency, template, healthcheck, script, docs) 식별
- [ ] 최근 변경 커밋 및 영향 범위 확인
- [ ] 운영 영향도(응답 지연, 인증 실패, GPU 사용률 급등) 평가

### Procedure

1. 정적 구성 점검
   - `docker compose -f infra/08-ai/ollama/docker-compose.yml config`
   - `docker compose -f infra/08-ai/open-webui/docker-compose.yml config`
2. 하드닝 기준 점검
   - `bash scripts/check-ai-hardening.sh`
3. 증상별 복구
   - middleware 회귀:
     - Ollama/Open WebUI 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file` 재적용
   - Ollama 과부하/queue 적체:
     - `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_MAX_QUEUE` 보수값으로 복원
   - Open WebUI stateful drift:
     - `template-stateful-med` 재적용
   - exporter metrics 실패:
     - `depends_on` health gating 및 metrics healthcheck 계약 복원
4. 재검증
   - `bash scripts/check-ai-hardening.sh`
   - `bash scripts/check-template-security-baseline.sh`
   - `bash scripts/check-doc-traceability.sh`

## Verification Steps

- [ ] AI compose static validation 통과
- [ ] AI hardening script 실패 0건
- [ ] optimization-hardening 문서 링크/README 인덱스 최신화 확인

## Observability and Evidence Sources

- **Signals**: CI `ai-hardening`, Ollama exporter metrics, Open WebUI health, gateway access logs
- **Evidence to Capture**:
  - 변경 전후 hardening check 결과
  - compose config 결과
  - 관련 compose/script/docs diff

## Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/08-ai/ollama/docker-compose.yml`
  - `infra/08-ai/open-webui/docker-compose.yml`
  - `scripts/check-ai-hardening.sh`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 정책/가이드/태스크 문서 링크 재확인

## Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: 승인된 운영 모델에서 직전 안정 모델로 fallback
- **Tool Disable / Revoke**: AI 자동 배포/승격 파이프라인 일시 중지(승인 필요)
- **Eval Re-run**:
  - `check-ai-hardening`
  - `check-template-security-baseline`
  - `check-doc-traceability`
- **Trace Capture**: CI logs + exporter metrics + compose config

## Related Operational Documents

- **Guide**: [../../07.guides/08-ai/optimization-hardening.md](../../07.guides/08-ai/optimization-hardening.md)
- **Operation**: [../../08.operations/08-ai/optimization-hardening.md](../../08.operations/08-ai/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
