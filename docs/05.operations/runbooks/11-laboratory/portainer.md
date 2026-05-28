---
status: active
---
<!-- Target: docs/05.operations/runbooks/11-laboratory/portainer.md -->

# Portainer Runbook

## Overview (KR)

이 런북은 Portainer 관리 계정 접근 불능 사유 발생 시 비밀번호를 초기화하거나, 서비스 시작 불능 상황을 복구하는 절차를 제공한다.

## Portainer Procedure

> 관리자 비밀번호 복구 및 서비스 장애 해결 절차.

---

## Procedure

### 1. Admin Password Reset

Portainer 내부 DB의 관리자 비밀번호를 수동으로 재설정해야 하는 경우 다음을 수행한다.

1. Portainer 컨테이너 중지:

   ```bash
   docker compose down
   ```

2. 비밀번호 초기화 헬퍼 도구 실행 (데이터 볼륨 사용):

   ```bash
   docker run --rm -v portainer_data:/data portainer/helper-reset-password
   ```

   *참고: 출력되는 임시 비밀번호를 기록한다.*

#### 3. Stack Deployment

1. 'Stacks' 메뉴에서 Docker Compose 파일을 직접 업로드하거나 붙여넣어 배포할 수 있다.

#### Implementation Snippet

#### Service Configuration

 Issues

Portainer가 로컬 Docker 환경에 연결하지 못하는 경우:

1. `docker-compose.yml`의 볼륨 섹션에서 `/var/run/docker.sock` 매핑 여부를 확인한다.
2. 호스트의 socket 권한 확인: `ls -l /var/run/docker.sock`.
3. Portainer 로그 확인: `docker| Storage |`portainer_data` | Persistent volume for config |

#### Traefik Integration

데이터베이스 오염으로 인해 실행되지 않는 경우:

1. 백업된 `${DEFAULT_MANAGEMENT_DIR}/portainer` 데이터를 복원한다.
2. 기존 볼륨을 삭제하고 새 데이터를 배치한 뒤 재시작한다.

### Verification Steps

- [ ] `https://portainer.${DEFAULT_URL}` 로그인 후 'Home' 대시보드에 로컬 환경이 'Active' 상태인지 확인.
- [ ] 'Containers' 목록이 정상적으로 업데이트되는지 확인.

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
- [Usage guide](../../guides/11-laboratory/portainer.md)
- [Operations policy](../../policies/11-laboratory/portainer.md)
- [Operations template](../../../99.templates/operation.template.md)
