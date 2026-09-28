---
title: "04-Data Optimization Hardening Usage Guide"
version: "1.0.3"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0030"
parent_ids:
- "POL-0030"
created: "2026-05-17"
---

# 04-Data Optimization Hardening Usage Guide

## Usage

이 subject는 data tier 전반의 static 제어를 검증한다: root profile 유효성,
명시적 persistence 소유권, secret, healthcheck, 리소스, 네트워크 경계, 복구
소유권. service 활성화, 데이터 접근, cleanup, migration, tuning을 승인하지
않는다.

### Root validation

leaf 파일이 root가 소유하는 네트워크, secret, 공유 템플릿에 의존하므로 저장소
루트에서 실행한다. leaf 파일을 직접 렌더링하는 대신 대표적인 현재 profile을
선택한다.

root `.env.example`로 각 대표 현재 profile을 렌더링하고 이 tier의 공유
hardening 확인 스크립트를 실행한다. 정확한 명령 순서는
[04-Data Optimization Hardening runbook](../runbooks/0030-data-optimization-hardening.md#procedure)이
소유한다.

치환된 비공개 값을 출력하지 않고 렌더링된 서비스를 점검한다. classification/
profile 정합성, 고유한 writable volume, 선언된 네트워크, secret 파일,
healthcheck, CPU/메모리 제한, 의도된 포트 게시, 엔진별 backup/restore
소유자를 확인한다.

### Interpretation

static pass는 parse와 정책 준수만 증명한다. runtime health, storage 용량,
backup 완전성, 복구 시간, encryption at rest, 애플리케이션 호환성, 동일 host
가용성은 증명하지 않는다. 범위를 정한 runtime test나 격리된 rehearsal로
증거를 확보하기 전까지는 이들을 unverified로 기록한다.

### Correction workflow

승인된 task 안에서 소유하는 leaf Compose source나 공유 템플릿을 수정한 뒤
동일한 root profile을 다시 렌더링한다. 범위를 정한 hardening 확인을
재실행하고 정확한 diff를 점검한다. 복구에는 엔진 runbook을 사용하며, 일반
data-copy나 cleanup 명령을 적용하지 않는다.

## Common Checks

정확한 root profile, service, health/resource 제어, writable-state 소유권,
secret reference, exposure, 엔진별 복구 경계를 확인한다. static pass는 구성
증거일 뿐이며, runtime과 restore는 별개로 남는다.

## Traceability

- Artifact: `GDE-0030`; 거버넌스 정책: `POL-0030`.
- Runtime authority: `root Compose plus scripts/hardening/check-all-hardening.sh`.

## Related Documents

- [Hardening policy](../policies/0030-data-optimization-hardening.md)
- [Hardening runbook](../runbooks/0030-data-optimization-hardening.md)
- [Backup policy](../policies/0021-backup-and-restore.md)
- [Storage exhaustion runbook](../runbooks/0035-storage-exhaustion.md)
