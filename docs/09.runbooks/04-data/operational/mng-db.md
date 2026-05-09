# Management Database (mng-db) Runbook

: Infrastructure Recovery and Maintenance

---

## Overview (KR)

이 런북은 `mng-db` (Management Database)의 가동, 초기화, 건강 상태 점검 및 긴급 복구 절차를 정의한다. 운영자가 즉시 따라 할 수 있는 명령어와 검증 단계를 제공한다.

## Purpose

`mng-db` 서비스의 부재로 인해 상위 관리 서비스(auth, automation 등)가 기동되지 않을 때의 복구 및 사후 관리를 목적으로 한다.

## Canonical References

- **ARD**: [../02.ard/0004-data-architecture.md](../../../02.ard/0004-data-architecture.md)
- **Spec**: [../04.specs/04-data/spec.md](../../../04.specs/04-data/spec.md)
- **Repo**: `infra/04-data/operational/mng-db/`

## When to Use

- 초기 플랫폼 설치 및 부트스트랩 시
- 관리용 DB 또는 캐시 서비스의 불능(unhealthy) 상태 발생 시
- 신규 플랫폼 서비스 추가로 인한 DB 초기화(`mng-pg-init`)가 필요할 때

## Procedure or Checklist

### Checklist

- [ ] `infra_net` 네트워크가 생성되어 있는가?
- [ ] `/run/secrets/` 하위에 필수 비밀번호 파일들이 존재하는가?
- [ ] `${DEFAULT_MANAGEMENT_DIR}` 데이터 볼륨 경로 권한이 올바른가?

### Procedure

1. **서비스 가동**

   ```bash
   cd infra/04-data/operational/mng-db
   docker-compose up -d
   ```

2. **초기화 작업 강제 실행**
   기존에 생성되지 않은 DB 유저나 스키마를 동기화해야 하는 경우 `mng-pg-init`을 재실행한다.

   ```bash
   docker-compose run --rm mng-pg-init
   ```

3. **서비스 로그 감시**

   ```bash
   docker-compose logs -f mng-pg
   docker-compose logs -f mng-valkey
   ```

## Related Operational Documents

- **Operation**: [mng-db.md](../../../08.operations/04-data/operational/mng-db.md)
- **Plan**: [2026-03-26-04-data-standardization.md](../../../05.plans/2026-03-26-04-data-standardization.md)

Copyright (c) 2026. Licensed under the MIT License.

---

## Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

## Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

## Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

## Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.
