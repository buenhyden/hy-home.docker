---
status: active
---
<!-- Target: docs/05.operations/runbooks/07-workflow/n8n.md -->

# n8n Runbook

## Overview

이 런북은 n8n 서비스 장애 발생 시 운영자가 신속하게 서비스를 복구하기 위한 단계별 절차를 제공한다. 현재 구현은 `n8n`, `n8n-worker`, `n8n-task-runner`, `n8n-task-runner-worker`를 기준으로 하며 root-included dev compose와 service-local compose의 broker 경계를 먼저 식별한다.

## n8n Recovery Procedure

> Scope: n8n (07-workflow)

---

### Purpose

- n8n 서비스의 가용성 조기 회복
- 자동화 워크플로우 중단 시간 최소화
- 시스템 정상 작동 여부 검증

### Canonical References

- ARD: [07-workflow Architecture](../../../02.architecture/requirements/0007-workflow-architecture.md)
- Usage: [n8n System Usage](../../guides/07-workflow/n8n.md)
- Policy: [n8n Operations Policy](../../policies/07-workflow/n8n.md)

## When to Use

- n8n UI 접근 시 "Connection lost" 또는 50x 에러가 발생할 때.
- 워크플로우가 실행되지 않고 `Pending` 또는 `Waiting` 상태에 멈춰 있을 때.
- 워커 컨테이너가 반복적으로 재시작(`Restarting`)될 때.

## Procedure

### Checklist

- [ ] `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`가 통과하는가?
- [ ] 현재 실행 환경이 root-included dev compose인지 service-local compose인지 식별했는가?
- [ ] `n8n_db_password` 시크릿이 올바르게 로드되었는가?

### Steps

#### 시나리오 1: 워커 노드 중단 (Worker Down)

1. 워커 로그 확인: `docker compose logs --tail=50 n8n-worker`
2. 워커 재시작: `docker compose restart n8n-worker`
3. Valkey 큐 상태 확인:
   - root-included dev compose: `docker compose exec mng-valkey sh -lc 'valkey-cli -a "$(cat /run/secrets/mng_valkey_password)" info keyspace'`
   - service-local compose: `docker compose exec n8n-valkey sh -lc 'valkey-cli -a "$(cat /run/secrets/n8n_valkey_password)" info keyspace'`

##### 시나리오 2: 데이터베이스 연결 오류

1. DB 호스트(`POSTGRES_MNG_HOSTNAME`)가 가용한지 확인.
2. n8n 메인 서비스 재시작: `docker compose restart n8n`
3. 시크릿 파일 권한 확인: `docker compose exec n8n ls -l /run/secrets/n8n_db_password`

##### 시나리오 3: 텐서플로우/Task Runner 오류

1. Task Runner 로그 확인: `docker compose logs n8n-task-runner n8n-task-runner-worker`
2. Task Runner 재시작: `docker compose restart n8n-task-runner n8n-task-runner-worker`

### Verification Steps

- [ ] `docker compose exec n8n wget -qO- http://localhost:${N8N_PORT:-5678}/healthz` 호출 시 정상 응답 확인.
- [ ] UI 로그인 후 `Executions` 탭에서 최근 작업의 성공 여부 확인.

### Observability and Evidence Sources

- **Signals**: Grafana n8n Dashboard (Error Rate), Valkey Queue Depth.
- **Evidence**: `docker compose logs --tail=100 n8n`, `n8n-worker`.

### Safe Rollback or Recovery Procedure

- [ ] 서비스를 재시작하기 전, 현재 실행/대기 중 workflow와 DB 백업 상태를 확인하십시오.
- [ ] 만약 `N8N_ENCRYPTION_KEY`가 변경되어 이전 데이터 복호화가 불가능한 경우, 이전 키로 롤백하거나 자격 증명을 재설정해야 합니다.

---

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- Capture command output, timestamps, and operator or agent actions for any execution of this runbook.
- Record failed checks, observed symptoms, and the final recovery or escalation state in the related task or incident evidence.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/07-workflow/n8n.md)
- [Operations policy](../../policies/07-workflow/n8n.md)
