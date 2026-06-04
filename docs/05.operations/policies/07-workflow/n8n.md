---
status: active
---
<!-- Target: docs/05.operations/policies/07-workflow/n8n.md -->

# n8n Operations Policy

## Overview (KR)

이 문서는 n8n 서비스의 안정적인 운영을 위한 정책과 통제 항목을 정의한다. 현재 구현은 `n8n`, `n8n-worker`, `n8n-task-runner`, `n8n-task-runner-worker` queue-mode 구성을 기준으로 하며, root-included dev compose는 `mng-valkey`, service-local compose는 `n8n-valkey`를 사용한다.

## Policy Scope

- **Systems**: n8n main/worker/task runner, PostgreSQL metadata DB connection, Valkey queue broker, Docker Secrets, Traefik route
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**:
  - `EXECUTIONS_MODE: queue`와 external runner mode를 유지한다.
  - n8n credential material은 Docker Secrets 또는 n8n encrypted Credentials에만 둔다.
  - root-included dev compose와 service-local compose의 broker 차이(`mng-valkey` vs `n8n-valkey`)를 운영 문서에 명시한다.
  - workflow 변경 전/후 root validator와 hardening gate 결과를 기록한다.
- **Allowed**:
  - UI Export/API 기반 workflow JSON 백업 절차 문서화.
  - `./custom` 경로를 통한 사용자 정의 노드 추가, 단 보안 검토와 재검증 후 적용.
  - n8n workflow Git backup/Vault credential 연계의 단계적 강화.
- **Disallowed**:
  - plaintext credential, token, workflow secret 원문 문서화.
  - 승인 없는 gateway/SSO middleware 완화.
  - root network/secrets context 없이 service-local compose 단독 `config` 결과를 CI evidence로 주장.

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다. 긴급 장애 복구 절차는 [n8n recovery runbook](../../runbooks/07-workflow/n8n.md)을 따른다.

## Verification

- `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 07-workflow`
- Runtime이 실행 중이면 `docker compose exec n8n wget -qO- http://localhost:${N8N_PORT:-5678}/healthz`

## Review Cadence

- 서비스 구성 변경 시 검토
- n8n/core runner version 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: workflow compose validation과 hardening gate를 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/07-workflow/n8n.md)
- [Recovery runbook](../../runbooks/07-workflow/n8n.md)
