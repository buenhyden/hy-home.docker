---
title: "04-Data Optimization Hardening Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0030"
parent_ids:
- "AD-0004"
created: "2026-05-10"
---

# 04-Data Optimization Hardening Operations Policy

## Overview

이 정책은 현재 소스 구성을 데이터 보호, 보안, 리소스, 생명주기와 독립적으로 검증 가능한
운영 통제에 묶는다.

## Policy Scope

모든 data 서비스는 명시적 disposition/profile, 쓰기 가능한 모든 state 경로에
대한 owner 하나, health check나 문서화된 예외, 공유 리소스 제한, 의도된
network/노출 경계, credential이 존재하는 경우 secret-file 보관, engine별
복구 방법을 가져야 한다.

## Controls

- Root Compose project를 통해 검증한다. Root network, secret, `extends` 경로가
  렌더링된 모델을 바꾸기 때문에 서비스 로컬 project 렌더링은 허용하지 않는다.
- HOME, OPTIONAL, LAB state 디렉터리를 구분해서 유지한다. 동일 host replica는
  host 가용성이나 backup이 아니라 topology test다.
- Secret을 절대 하드코딩하거나 출력하지 않는다. Gateway TLS는 내부 TLS나
  backup 암호화를 성립시키지 않는다. 각 경계를 소스로부터 문서화한다.
- Engine이 지원하는 export/snapshot 절차와 별도의 암호화된 destination을
  요구한다. Active database/object-store 디렉터리를 그대로 복사하는 것은
  금지한다.
- 승격이나 cutover 전에 isolated compatible restore, application 수준 검증,
  관측된 RPO/RTO, rollback을 요구한다.
- Pin 변경 전에 upstream 보안, upgrade, license 출처를 검토한다. 현재 image
  선언은 지원되는 lifecycle을 증명하지 않는다.

### Validation and evidence

영향받는 정확한 profile에 대한 root `config --quiet`와
`scripts/hardening/check-all-hardening.sh 04-data`는 필수 static check다.
Evidence는 command, source revision, exit status, scope, 미해결 gap을
credential이나 data 없이 기록한다. Runtime check는 별도로 승인되며 static
성공에서 추론해서는 안 된다.

### Failure handling

실패한 health, resource, secret, network, persistence, recovery 통제를
우회하지 않는다. 승인된 범위 안에서 patch하거나 소유 architecture와 운영
subject로 escalate한다. Data 삭제, volume 재사용, 파괴적 restore는 명시적
승인을 요구한다.

## Exceptions

문서화된 job/health 예외는 소유 profile과 복구 evidence를 요구한다. 예외는
runtime mutation, plaintext secret, raw active storage 복사, 동일 host
가용성 주장을 허용하지 않는다.

## Verification

Root 구성과 범위가 지정된 static policy check를 검증한 뒤, 승격이나 cutover
전에 application 수준 acceptance를 갖춘 isolated compatible restore를
요구한다. 검증되지 않은 runtime 속성은 명시적으로 기록한다.

## Review Cadence

Profile, image, volume, credential, consumer, retention 또는 upstream
lifecycle 변경 후, 그리고 보관되는 동안 최소 연 1회 검토한다.

## Traceability

- Artifact: `POL-0030`; parent: `AD-0004`.
- Runtime 권한은 연결된 Compose/소스 파일에 남아 있으며, 정확한 pin도 그곳에 있다.

## Related Documents

- [Usage guide](../guides/0030-data-optimization-hardening.md)
- [Runbook](../runbooks/0030-data-optimization-hardening.md)
- [Backup policy](0021-backup-and-restore.md)
