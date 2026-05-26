---
status: active
---
<!-- Target: docs/05.operations/runbooks/11-laboratory/dashboard.md -->

# Laboratory Dashboard Runbook

## Laboratory Dashboard Procedure: Homer

> Scope: Homer Dashboard Recovery and Configuration Service

---

### Overview (KR)

이 런북은 `11-laboratory` 티어의 서비스 대시보드(Homer)에 대한 장애 복구 및 설정 검증 절차를 정의한다. 설정 오류로 인한 페이지 렌더링 실패나 서비스 접근 불가 상황을 즉시 해결하기 위한 단계별 지침을 제공한다.

### Purpose

- Homer 설정 파일(`config.yml`)의 구문 오류 복구.
- 대시보드 서비스 재시작 및 갱신.
- 대시보드 내 링크 유효성 검사.

### Canonical References

- [../../../../infra/11-laboratory/dashboard/README.md](../../../../infra/11-laboratory/dashboard/README.md)
- [../../guides/11-laboratory/dashboard.md](../../guides/11-laboratory/dashboard.md)
- [../../policies/11-laboratory/dashboard.md](../../policies/11-laboratory/dashboard.md)

## When to Use

- Homer 접속 시 "Internal Server Error" 또는 빈 화면이 출력되는 경우.
- `config.yml` 수정 후 변경 사항이 실시간으로 반영되지 않는 경우.
- 대시보드 내 특정 아이콘이 깨지거나 링크가 동작하지 않는 경우.

## Procedure

### Checklist

- [ ] `infra/11-laboratory/dashboard/config/config.yml` 파일 존재 여부 확인.
- [ ] Homer 컨테이너 실행 상태 확인 (`docker ps | grep homer`).

### Steps

#### 1. Configuration Validation and Recovery

1. 설정 파일의 구문 오류를 확인한다:

   ```bash
   yq eval . infra/11-laboratory/dashboard/config/config.yml
   ```

2. 오류가 발견되면 가장 최근의 백업본으로 복구하거나 오류 지점을 수정한다.
3. 수정 후 파일을 저장한다.

##### 2. Service Refresh

1. Homer는 실시간 반영을 지원하지만, 강제 재시작이 필요한 경우 다음 명령을 수행한다:

   ```bash
   cd infra/11-laboratory/dashboard
   docker compose restart homer
   ```

##### 3. Assets Check

1. 아이콘이나 로고가 표시되지 않는 경우 `dashboard/config/` 폴더 내 이미지 파일의 권한을 확인한다 (644 권한 권장).

### Verification Steps

- [ ] 브라우저에서 `homer.${DEFAULT_URL}` 접속 및 정상 렌더링 확인.
- [ ] 브라우저 콘솔에서 404/500 에러 발생 여부 확인.

### Safe Rollback or Recovery Procedure

- 작업 전: `cp config.yml config.yml.bak`
- 복구 시: `mv config.yml.bak config.yml && docker compose restart homer`

### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

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
- [Usage guide](../../guides/11-laboratory/dashboard.md)
- [Operations policy](../../policies/11-laboratory/dashboard.md)
- [Operations template](../../../99.templates/operation.template.md)
