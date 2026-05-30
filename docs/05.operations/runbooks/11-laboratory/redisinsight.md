---
status: active
---
<!-- Target: docs/05.operations/runbooks/11-laboratory/redisinsight.md -->

# RedisInsight Runbook

## Overview (KR)

이 런북은 RedisInsight의 연결 오류, 설정 초기화, 그리고 서비스 성능 저하 상황 발생 시 조치 방법을 안내한다.

## RedisInsight Procedure

> RedisInsight 연결 장애 및 설정 복구 절차.

---

## Procedure

### 1. Connection Failure Troubleshooting

Redis 서버에 연결할 수 없는 경우:

1. 네트워크 확인: `docker exec redisinsight ping <redis_service_name>`.
2. Redis 서버 상태 확인: `docker logs redis`.
3. RedisInsight 설정에서 호스트명과 포트(6379)가 올바른지 재확인한다.

#### 2. Configuration Reset

잘못된 설정으로 인해 UI가 비정상적인 경우:

1. 서비스를 중단한다: `docker compose down`.
2. `${DEFAULT_MANAGEMENT_DIR}/redisinsight` 내의 설정 파일을 백업한 뒤 삭제한다.
3. 서비스를 다시 시작하여 설정을 초기화한다: `docker compose up -d`.

#### 3. Log Inspection

작업 중 오류 발생 시:

1. `docker logs -f redisinsight`를 통해 실시간 에러 로그를 확인한다.
2. 브라우저 개발자 도구의 'Console' 섹션에서 JS 에러 여부를 확인한다.

### Verification Steps

- [ ] `https://redisinsight.${DEFAULT_URL}` 접속 및 메인 대시보드 로드 확인.
- [ ] 'Browser' 탭에서 키 목록이 지연 없이 조회되는지 확인.

### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

### Canonical References

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

## When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

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
- [Usage guide](../../guides/11-laboratory/redisinsight.md)
- [Operations policy](../../policies/11-laboratory/redisinsight.md)
