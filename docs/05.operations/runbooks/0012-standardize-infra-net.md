---
status: active
---

# 0012 Standardize Infra Net Runbook

## infra_net IP Mapping Validation & Update Procedure

### Overview (KR)

이 런북은 `infra_net` 서브넷 내 신규 서비스 추가 및 기존 서비스 IP 변경 시의 운영 절차를 정의한다. 서브넷 정합성 유지와 충돌 방지가 주 목적이다.

### Purpose

신속하고 정확하게 서브넷 내 고정 IP를 할당하거나 기존 설정의 오구성을 수정한다.

### Canonical References

- [../../02.architecture/requirements/2026-04-01-standardize-infra-net.md](../../02.architecture/requirements/2026-04-01-standardize-infra-net.md)
- [../../02.architecture/decisions/2026-04-01-standardize-infra-net.md](../../02.architecture/decisions/2026-04-01-standardize-infra-net.md)
- [../../03.specs/standardize-infra-net/spec.md](../../03.specs/standardize-infra-net/spec.md)
- [../../04.execution/plans/2026-04-01-standardize-infra-net.md](../../04.execution/plans/2026-04-01-standardize-infra-net.md)

### When to Use

- 서비스의 `networks` 설정을 표준 딕셔너리 포맷으로 전환할 때.
- 신규 인프라 서비스를 인공지능 홈 시스템에 통합할 때.
- 네트워크 충돌 발생 시 원인 분석 및 IP 재배치.

### Procedure or Checklist

#### Checklist

- [ ] 대상 서비스의 `infra/` 내 `docker-compose.yml` 경로 확인.
- [ ] 현재 서브넷(`172.19.0.0/16`) 내 가용 IP 대역 확인 (Plan/Spec 참조).
- [ ] 중복 사용 여부 사전 검증 (`grep -r "ipv4_address" .`).

#### Procedure

1. **IP 선정**: `docs/04.execution/plans/2026-04-01-standardize-infra-net.md`의 IP 맵핑 리스트에서 비어있는 영역을 선택함.
2. **Compose 파일 수정**:

   ```yaml
   networks:
     infra_net:
       ipv4_address: 172.19.0.XXX
   ```

3. **구문 검증**: `docker compose config` 실행하여 YAML 유효성 확인.
4. **런타임 검증**: `docker compose up -d` (Test/Staging 환경) 실행 후 `docker inspect <container_name>`을 통해 실제 할당 결과 대조.

### Verification Steps

- [ ] `docker network inspect infra_net` 실행 시 모든 컨테이너가 의도된 고정 IP를 보유하고 있는지 전수 조사.

### Observability and Evidence Sources

- **Signals**: `docker-compose` 배포 로그의 "Network Conflict" 에러 메시지.
- **Evidence to Capture**: `grep -r "infra_net" infra/` 결과 덤프.

### Safe Rollback or Recovery Procedure

- [ ] 변경 전 `docker-compose.yml` 백업본으로 복구.
- [ ] 충돌이 심각할 경우 해당 서비스를 `infra_net`에서 일시 제외하고 게이트웨이 서비스만 유지.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../README.md)
- [Usage guide](../guides/0012-standardize-infra-net.md)
- [Operations template](../../99.templates/operation.template.md)
