---
status: active
---
<!-- Target: docs/05.operations/runbooks/11-laboratory/open-notebook.md -->

# Open Notebook Runbook

## Open Notebook Procedure

> Scope: Open Notebook and SurrealDB

---

### Overview (KR)

이 런북은 `open-notebook` UI 접속 실패, SurrealDB 의존성 장애, secret 또는 볼륨 문제를 진단하고 복구하기 위한 실행 절차를 정의한다.

### Purpose

Open Notebook 관리/실험 작업 환경의 가용성을 회복하고, 데이터 손상이나 secret 노출 없이 문제를 좁혀 복구한다.

### Canonical References

- [../../../infra/11-laboratory/open-notebook/docker-compose.yml](../../../../infra/11-laboratory/open-notebook/docker-compose.yml)
- [../../03.specs/11-laboratory/spec.md](../../../03.specs/11-laboratory/spec.md)
- [../../05.operations/11-laboratory/open-notebook.md](../../policies/11-laboratory/open-notebook.md)
- [../../05.operations/11-laboratory/open-notebook.md](../../policies/11-laboratory/open-notebook.md)

## When to Use

- `https://open-notebook.${DEFAULT_URL}` 접속이 실패한다.
- `open_notebook` 컨테이너가 재시작 루프에 빠진다.
- `surrealdb` healthcheck가 실패한다.
- 로그인 또는 credential storage 오류가 발생한다.
- 관리 데이터 볼륨 경로 또는 권한 문제가 의심된다.

## Procedure

### Checklist

- [ ] `open_notebook`과 `surrealdb`가 같은 profile에서 resolve되는가?
- [ ] `surrealdb` healthcheck가 `healthy` 상태인가?
- [ ] `open_notebook_password`, `open_notebook_encryption_key`, `surreal_db_password` secret 파일이 존재하는가?
- [ ] `open_notebook_encryption_key` secret과 `SURREALDB_*` 환경값이 비어 있지 않은가?
- [ ] Traefik route와 middleware chain이 유지되는가?

### Steps

#### Case 1: UI 접속 실패

1. Compose config가 서비스와 Traefik label을 정상 resolve하는지 확인한다.

   ```bash
   docker compose --profile admin config
   ```

2. 서비스 상태를 확인한다.

   ```bash
   docker compose --profile admin ps open_notebook surrealdb
   ```

3. `open_notebook` 로그에서 password, token, key 값이 출력되지 않도록 주의하며 오류 유형만 확인한다.

   ```bash
   docker compose --profile admin logs --tail=100 open_notebook
   ```

##### Case 2: SurrealDB 준비 실패

1. `surrealdb` 컨테이너 health 상태와 로그를 확인한다.

   ```bash
   docker compose --profile admin ps surrealdb
   docker compose --profile admin logs --tail=100 surrealdb
   ```

2. `surreal_db_password` secret 파일 존재 여부와 `SURREALDB_USERNAME` 값을 확인한다. secret 값 자체는 출력하지 않는다.
3. `DEFAULT_MANAGEMENT_DIR` 하위 SurrealDB data path의 존재와 쓰기 권한을 확인한다.

##### Case 3: 로그인 또는 credential storage 오류

1. `open_notebook_password` secret 파일이 존재하는지 확인한다.
2. `open_notebook_encryption_key` secret 파일이 존재하고 비어 있지 않은지 확인한다.
3. 키를 변경한 직후라면 기존 credential storage와 호환되지 않을 수 있으므로 운영 정책에 따라 복구 또는 재초기화 여부를 결정한다.

### Verification Steps

- [ ] `docker compose --profile admin ps open_notebook surrealdb`에서 두 서비스가 정상 상태다.
- [ ] `https://open-notebook.${DEFAULT_URL}` 접속과 로그인이 성공한다.
- [ ] 새 노트북 생성/저장이 성공한다.
- [ ] `bash scripts/hardening/check-all-hardening.sh 11-laboratory`가 통과한다.

### Observability and Evidence Sources

- **Signals**: container status, SurrealDB healthcheck, Traefik route status, Open Notebook UI login result
- **Evidence to Capture**: command names, service states, redacted log snippets, changed environment key names

### Safe Rollback or Recovery Procedure

- [ ] 이미지 갱신 후 장애가 발생하면 직전 검증된 image tag 또는 local image로 되돌린다.
- [ ] secret/key 변경 후 장애가 발생하면 변경 전 secret inventory 기록을 기준으로 복구하되 값은 문서화하지 않는다.
- [ ] 데이터 볼륨 손상이 의심되면 사용자의 명시적 승인 없이 삭제하거나 재초기화하지 않는다.

### Agent Operations

- **Prompt Rollback**: Open Notebook 내부 prompt 또는 model setting 변경은 별도 변경 기록이 있을 때만 되돌린다.
- **Model Fallback**: 외부 AI provider 장애 시 로컬/오프라인 모드로 degrade하고 secret 노출 없이 원인을 기록한다.
- **Tool Disable / Revoke**: 공개 route 노출 또는 credential leak 의심 시 Open Notebook 외부 접근을 먼저 차단한다.
- **Eval Re-run**: AI 기능 변경 후 prompt injection, secret leakage, credential persistence 검토를 재실행한다.
- **Trace Capture**: secret 값 없이 service state, route, profile, image tag만 기록한다.

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
- [Usage guide](../../guides/11-laboratory/open-notebook.md)
- [Operations policy](../../policies/11-laboratory/open-notebook.md)
- [Operations template](../../../99.templates/operation.template.md)
