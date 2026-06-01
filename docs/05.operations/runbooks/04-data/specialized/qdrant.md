---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/specialized/qdrant.md -->

# Qdrant Runbook

## Overview (KR)

이 런북은 Qdrant 데이터베이스의 스냅샷 생성, 복원 및 클러스터 상태 복구 절차를 정의한다. 데이터 손상 또는 유실 시 단계별 조치 지침을 제공한다.

## Qdrant Recovery Procedure

> Scope: Qdrant Vector Database

> Procedure for snapshot management and disaster recovery for Qdrant within the `04-data/specialized` tier.

### Purpose

벡터 컬렉션의 무결성을 유지하고 장애 시 신속한 서비스 복원을 지원한다.

### Canonical References

- [Data architecture ARD](../../../../02.architecture/requirements/0004-data-architecture.md)
- [Qdrant operations policy](../../../policies/04-data/specialized/qdrant.md)
- [Qdrant infra README](../../../../../infra/04-data/specialized/qdrant/README.md)

## When to Use

- 컬렉션 단위의 스냅샷 생성이 필요할 때.
- 특정 시점의 스냅샷으로 데이터를 복원해야 할 때.
- 서비스 응답 지연 또는 `/readyz` 실패 시 조치.

## Procedure

### Checklist

- [ ] 관련 policy, guide, runbook handoff를 확인한다.
- [ ] 현재 상태와 변경 범위를 기록한다.

### 1. Collection Snapshot Execution

실행 중인 상태에서 컬렉션별 스냅샷을 생성한다.

1. 스냅샷 요청:

   ```bash
   curl -X POST "https://qdrant.${DEFAULT_URL}/collections/my_collection/snapshots"
   ```

2. 생성 결과 확인: `/qdrant/storage/snapshots` 디렉토리 내 `.snapshot` 파일 생성 여부 점검.

#### 2. Restoration from Snapshot

1. 컬렉션 삭제 (필요시): `curl -X DELETE "https://qdrant.${DEFAULT_URL}/collections/my_collection"`
2. 스냅샷 복원 요청:

   ```bash
   curl -X POST "https://qdrant.${DEFAULT_URL}/collections/my_collection/snapshots/recover" \
        -H "Content-Type: application/json" \
        --data '{ "location": "file:///qdrant/storage/snapshots/my_collection_snapshot.snapshot" }'
   ```

   `file://` 값은 Qdrant snapshot recovery API가 컨테이너 내부 스냅샷 파일을 가리키기 위해 받는 `location` URI다. 문서 링크나 호스트 파일 경로로 해석하지 않는다.

#### 3. Emergency Health Recovery

1. 로그 확인: `docker compose logs -f qdrant`
2. 데이터 디렉토리 권한 점검: `1000:1000` (Unprivileged user) 소유 확인.
3. 임시 파일 정리: `/tmp` (tmpfs) 용량 확인 및 정리.

### Steps

1. 이 runbook의 trigger와 checklist를 확인한다.
2. 기존 절차가 문서에 포함되어 있으면 그 순서대로 수행한다.
3. 실행 중 생성된 명령 출력과 판단 근거를 evidence로 남긴다.
4. 검증 실패, secret exposure 위험, 파괴적 변경 필요 시 즉시 중단하고 `## Escalation`으로 이동한다.

### Verification Steps

- [ ] `curl https://qdrant.${DEFAULT_URL}/readyz` 호출 시 `200 OK` 확인.
- [ ] 컬렉션 인벤토리 확인: `curl https://qdrant.${DEFAULT_URL}/collections`.

### Observability and Evidence Sources

- **Signals**: Qdrant Telemetry, Traefik Dashboard.
- **Evidence to Capture**: 컬렉션 현황 캡처, 스냅샷 파일 목록.

### Safe Rollback or Recovery Procedure

- 스냅샷 복원 실패 시, 호스트 레벨의 `${DEFAULT_DATA_DIR}/qdrant/data` 전체 백업 본을 사용하여 볼륨 데이터 전체를 교체한다.

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

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/specialized/qdrant.md)
- [Operations policy](../../../policies/04-data/specialized/qdrant.md)
