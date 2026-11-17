---
title: "04-Data Optimization Hardening Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0030"
parent_ids:
- "AD-0004"
created: "2026-05-10"
next_review_at: "2027-05-13"
---

# 04-Data Optimization Hardening Operations Policy

## Purpose and Scope

### Objective

이 정책은 현재 소스 구성을 데이터 보호, 보안, 리소스, 생명주기와 독립적으로 검증 가능한
운영 통제에 묶는다.

#### Authority

- Artifact: `POL-0030`; parent: `AD-0004`.
- Runtime 권한은 연결된 Compose/소스 파일에 남아 있으며, 정확한 pin도 그곳에 있다.

### Applies To

모든 data 서비스는 명시적 disposition/profile, 쓰기 가능한 모든 state 경로에
대한 owner 하나, health check나 문서화된 예외, 공유 리소스 제한, 의도된
network/노출 경계, credential이 존재하는 경우 secret-file 보관, engine별
복구 방법을 가져야 한다.

#### Exclusions

애플리케이션 인증 연동은 이 정책이 아니라 [POL-0079](../03-identity-and-access/0079-application-auth-integration.md)가 정한다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0030-R1 | 검증 시 | 필수: Root Compose project를 통해 검증한다 | none | none |
| POL-0030-R2 | 항상 | 금지: 서비스 로컬 project 렌더링 | none | none |
| POL-0030-R3 | 항상 | 필수: HOME/OPTIONAL/LAB state 디렉터리를 구분해서 유지한다 | none | none |
| POL-0030-R4 | 항상 | 금지: 동일 host replica를 host 가용성이나 backup으로 취급 | none | none |
| POL-0030-R5 | 항상 | 금지: secret 하드코딩과 출력 | none | none |
| POL-0030-R6 | 항상 | 금지: Gateway TLS를 내부 TLS나 backup 암호화로 간주 | none | none |
| POL-0030-R7 | 항상 | 필수: 각 경계를 소스로부터 문서화한다 | none | none |
| POL-0030-R8 | 백업 | 필수: engine이 지원하는 export/snapshot 절차와 별도의 암호화된 destination을 요구한다 | none | none |
| POL-0030-R9 | 항상 | 금지: active database/object-store 디렉터리를 그대로 복사 | none | none |
| POL-0030-R10 | 승격/cutover 전 | 필수: isolated compatible restore/application 수준 검증/관측된 RPO·RTO/rollback을 요구한다 | none | none |
| POL-0030-R11 | 항상 | 필수: 검증되지 않은 runtime 속성을 명시적으로 기록한다 | none | none |
| POL-0030-R12 | pin 변경 전 | 필수: upstream 보안/upgrade/license 출처를 검토한다 | 수동 | none |
| POL-0030-R13 | 항상 | 금지: 현재 image 선언을 지원되는 lifecycle의 증명으로 취급 | none | none |
| POL-0030-R14 | 영향받는 profile | 필수: 정확한 profile에 대해 root `config --quiet`를 실행한다(필수 static check) | root `config --quiet` | none |
| POL-0030-R15 | 영향받는 profile | 필수: `scripts/hardening/check-all-hardening.sh 04-data`를 실행한다(필수 static check) | `scripts/hardening/check-all-hardening.sh 04-data` | none |
| POL-0030-R16 | evidence 기록 | 필수: command/source revision/exit status/scope/미해결 gap을 기록한다 | none | none |
| POL-0030-R17 | evidence 기록 | 금지: evidence에 credential이나 data 포함 | none | none |
| POL-0030-R18 | runtime check | 필수: 별도로 승인한다 | 수동 | none |
| POL-0030-R19 | 항상 | 금지: static 성공에서 runtime 속성 추론 | none | none |
| POL-0030-R20 | health/resource/secret/network/persistence/recovery 통제 실패 | 금지: 실패한 통제의 우회 | none | none |
| POL-0030-R21 | 통제 실패 | 필수: 승인된 범위 안에서 patch하거나 소유 architecture와 운영 subject로 escalate한다 | none | none |
| POL-0030-R22 | data 삭제/volume 재사용/파괴적 restore | 필수: 명시적 승인을 받는다 | 수동 | none |
| POL-0030-R23 | 적용 identity 변경/운영 | 필수: 문서의 정적 검증과 runtime 운영 승인을 분리한다 | none | none |
| POL-0030-R24 | service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 | 필수: 이 Policy와 linked Guide/Runbook을 함께 검토한다 | 수동 | none |
| POL-0030-R25 | engine secret/certificate | 필수: 이 subject의 credential 계약을 따른다 | none | none |
| POL-0030-R26 | 앱 인증 연동 | 필수: 적용되는 `POL-0079`의 통제를 따른다 | none | none |
| POL-0030-R27 | source 반영/재기동 | 필수: `POL-0006`의 적용 통제를 따른다 | none | none |
| POL-0030-R28 | 보존/삭제 | 필수: `POL-0021`의 적용 통제를 따른다 | none | none |
| POL-0030-R29 | exporter/stateless job | 필수: 설정·credential과 그 작업이 변경하는 upstream state를 통제 대상에서 제외하지 않고 포함한다 | none | none |
| POL-0030-R30 | 소유 artifact·복구 지점·expiry가 불명확할 때 | 필수: 삭제/재생성을 중단한다 | none | none |
| POL-0030-R31 | 항상 | 금지: 기존 Exceptions 외의 새 예외를 승인된 것으로 간주 | none | none |

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

#### Validation and evidence

영향받는 정확한 profile에 대한 root `config --quiet`와
`scripts/hardening/check-all-hardening.sh 04-data`는 필수 static check다.
Evidence는 command, source revision, exit status, scope, 미해결 gap을
credential이나 data 없이 기록한다. Runtime check는 별도로 승인되며 static
성공에서 추론해서는 안 된다.

#### Failure handling

실패한 health, resource, secret, network, persistence, recovery 통제를
우회하지 않는다. 승인된 범위 안에서 patch하거나 소유 architecture와 운영
subject로 escalate한다. Data 삭제, volume 재사용, 파괴적 restore는 명시적
승인을 요구한다.

#### Accountable lifecycle boundary

적용 identity: GDE-0019/0022/0024/0025/0026/0027/0028/0029/0031/0033/0034/0076/0100의 명명된 data identities. 문서의 정적 검증과 runtime 운영 승인을 분리한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](../03-identity-and-access/0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](../01-common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

### Exceptions

#### Exception Conditions

문서화된 job/health 예외는 소유 profile과 복구 evidence를 요구한다. 예외는
runtime mutation, plaintext secret, raw active storage 복사, 동일 host
가용성 주장을 허용하지 않는다.

#### Approval and Review

Profile, image, volume, credential, consumer, retention 또는 upstream
lifecycle 변경 후, 그리고 보관되는 동안 최소 연 1회 검토한다.

## Enforcement

### Mechanisms

[RUN-0030](../../runbooks/05-databases-and-storage/0030-data-optimization-hardening.md#steps)의 root profile render와 `scripts/hardening/check-all-hardening.sh 04-data`로 static 통제를 검증한 뒤, 승격이나 cutover
전에 application 수준 acceptance를 갖춘 isolated compatible restore를
요구한다. 검증되지 않은 runtime 속성은 명시적으로 기록한다.

### Limits

이 정책에서 이름 붙은 검사는 root `config --quiet`와 `scripts/hardening/check-all-hardening.sh 04-data`뿐이며, 아래 규칙은 자동 검사 없이 검토·승인에 의존합니다.

- 검증 경로: 자동 검사 없음(none) `POL-0030-R2`
- state/경계: 자동 검사 없음(none) `POL-0030-R3`, `POL-0030-R4`, `POL-0030-R5`, `POL-0030-R6`, `POL-0030-R7`
- 백업/복원: 자동 검사 없음(none) `POL-0030-R8`, `POL-0030-R9`, `POL-0030-R10`, `POL-0030-R11`
- pin: 자동 검사 없음(none) `POL-0030-R13`; 수동 검토/승인 `POL-0030-R12`
- 검증/evidence: 자동 검사 없음(none) `POL-0030-R16`, `POL-0030-R17`, `POL-0030-R19`; 수동 검토/승인 `POL-0030-R18`
- 실패 처리: 자동 검사 없음(none) `POL-0030-R20`, `POL-0030-R21`; 수동 검토/승인 `POL-0030-R22`
- lifecycle: 자동 검사 없음(none) `POL-0030-R23`, `POL-0030-R25`, `POL-0030-R26`, `POL-0030-R27`, `POL-0030-R28`, `POL-0030-R29`, `POL-0030-R30`, `POL-0030-R31`; 수동 검토/승인 `POL-0030-R24`
- 정책이 밝힌 공백: runtime check는 별도 승인 대상이며 정적 성공(root render/hardening script)에서 추론할 수 없고, 승격/cutover 전 isolated restore/application 수준 검증/관측 RPO·RTO 증거는 이 정책에 없다.
- POL-0030-R1: 정책이 이 규칙에 묶은 검사를 명시하지 않는다.

## Ownership

### Owner

@buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다.

### Review Triggers

- [Usage guide](../../guides/05-databases-and-storage/0030-data-optimization-hardening.md)
- [Runbook](../../runbooks/05-databases-and-storage/0030-data-optimization-hardening.md)
- [Backup policy](../10-platform-and-backup/0021-backup-and-restore.md)
