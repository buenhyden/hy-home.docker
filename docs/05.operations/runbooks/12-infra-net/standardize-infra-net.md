---
status: active
---
<!-- Target: docs/05.operations/runbooks/12-infra-net/standardize-infra-net.md -->

# 0012 Standardize Infra Net Runbook

## infra_net IP Mapping Validation and Update Procedure

> Scope: 신규 서비스 추가 또는 기존 서비스 IP 변경 시 `infra_net` mapping과 compose 구조를 검증한다.

### Overview

이 런북은 `infra_net` 서브넷 내 신규 서비스 추가 및 기존 서비스 IP 변경 시의 운영 절차를 정의한다. 서브넷 정합성 유지와 충돌 방지가 주 목적이다.

### Purpose

신속하고 정확하게 서브넷 내 고정 IP를 할당하거나 기존 설정의 오구성을 수정한다.

### Canonical References

- [../../../02.architecture/requirements/0026-standardize-infra-net.md](../../../02.architecture/requirements/0026-standardize-infra-net.md)
- [../../../02.architecture/decisions/0026-standardize-infra-net.md](../../../02.architecture/decisions/0026-standardize-infra-net.md)
- [../../../03.specs/098-standardize-infra-net/spec.md](../../../03.specs/098-standardize-infra-net/spec.md)
- [../../../04.execution/plans/2026-04-01-standardize-infra-net.md](../../../04.execution/plans/2026-04-01-standardize-infra-net.md)
- [../../policies/12-infra-net/standardize-infra-net.md](../../policies/12-infra-net/standardize-infra-net.md)
- [../../guides/12-infra-net/standardize-infra-net.md](../../guides/12-infra-net/standardize-infra-net.md)

## When to Use

- 서비스의 `networks` 설정을 표준 딕셔너리 포맷으로 전환할 때.
- 신규 인프라 서비스를 인공지능 홈 시스템에 통합할 때.
- 네트워크 충돌 발생 시 원인 분석 및 IP 재배치.

## Procedure

### Checklist

- [ ] 대상 서비스의 `infra/` 내 `docker-compose.yml` 경로 확인.
- [ ] 현재 서브넷(`172.19.0.0/16`) 내 가용 IP 대역 확인 (Plan/Spec 참조).
- [ ] 중복 사용 여부 사전 검증 (`rg -n "ipv4_address:" infra docker-compose.yml`).
- [ ] 런타임 환경을 조회하거나 변경해야 하는 경우 승인된 test/staging 대상인지 확인.

### Steps

1. **IP 선정**: `docs/03.specs/098-standardize-infra-net/spec.md`의 **Assigned IP Mapping Table (Authoritative)**에서 비어있는 영역을 선택함.
2. **Compose 파일 수정**:

   ```yaml
   networks:
     infra_net:
       ipv4_address: 172.19.0.7 # registry example from the authoritative table
   ```

3. **대상 IP 치환 확인**: 실제 변경 대상에는 registry 예시 값을 남기지 않고 authoritative table의 해당 서비스 IP를 사용했는지 확인한다.
4. **구문 검증**: repository root에서 `bash scripts/validation/validate-docker-compose.sh`를 실행하여 root `infra_net` 컨텍스트에서 YAML 유효성을 확인.
5. **Profile 검증**: 변경한 tier가 기본 `core` profile 밖이면 `HYHOME_COMPOSE_PROFILES`에 해당 profile을 지정해 검증을 반복한다.
6. **런타임 검증**: 승인된 test/staging 환경에서 이미 실행 중인 컨테이너만 `docker inspect <container_name>`으로 실제 할당 결과와 authoritative table을 대조한다.

### Verification Steps

- [ ] `bash scripts/validation/validate-docker-compose.sh` 결과가 성공한다.
- [ ] 변경한 profile 검증 결과가 성공한다.
- [ ] 승인된 실행 환경에서 `docker network inspect infra_net` 결과가 authoritative table과 일치한다.

### Evidence

- **Signals**: compose validation 실패, runtime IP 충돌, `docker inspect` 결과와 authoritative table의 불일치.
- **Evidence to Capture**: validation 명령과 결과, `rg -n "infra_net|ipv4_address:" infra docker-compose.yml` 결과, runtime 검증을 수행한 경우 `docker network inspect infra_net` 요약.

### Safe Rollback or Recovery Procedure

- [ ] 변경 전 Git diff 또는 commit 기준으로 해당 compose/network 변경을 되돌린다.
- [ ] runtime 검증 중 충돌이 확인되면 추가 변경을 멈추고 evidence를 보존한다.
- [ ] 네트워크/volume 삭제가 필요한 상황은 이 런북에서 직접 처리하지 않고 incident 절차로 승격한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- Capture command output, timestamps, changed file paths, authoritative mapping row, operator or agent actions, and any runtime inspection summary used during this runbook.

## Rollback or Recovery

- Use only the Git-managed rollback or recovery steps already documented in `### Safe Rollback or Recovery Procedure`.
- If runtime state was changed under a separate approval, restore the previous committed compose/network configuration and re-run validation before any additional runtime action.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/12-infra-net/standardize-infra-net.md)
- [Operations policy](../../policies/12-infra-net/standardize-infra-net.md)
- [infra_net spec](../../../03.specs/098-standardize-infra-net/spec.md)
