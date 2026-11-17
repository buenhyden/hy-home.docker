---
title: "Valkey Cluster Operations Policy"
version: "2.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0022"
parent_ids:
- "AD-0004"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Valkey Cluster Operations Policy

## Purpose and Scope

### Objective

이 정책은 현재 source 구성을 데이터 보호, 보안, 자원, 수명주기 통제와 독립적으로 검증 가능한 운영 통제에 묶는다. 대상은 `labs/valkey-cluster/docker-compose.yml`의 LAB 전용 Valkey Cluster이다.

#### Authority

- Runtime source: [Valkey Cluster Compose](../../../../labs/valkey-cluster/docker-compose.yml).
- Artifact: `POL-0022`; parent: `AD-0004`.
- Runtime authority는 연결된 Compose/source 파일에 남는다; 정확한 pin도 그 파일에 있다.

### Applies To

이 policy는 LAB 전용 `valkey-cluster` profile에 적용된다.

#### Exclusions

HOME으로 promotion하거나 `mng-valkey`를 대체하는 것은 승인하지 않는다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0022-R1 | stack 선택 시 | 필수: `labs/valkey-cluster/docker-compose.yml` 독립 Compose project와 정확한 `valkey-cluster` profile로만 선택한다 | none | none |
| POL-0022-R2 | 항상 | 금지: root include에 추가 | none | none |
| POL-0022-R3 | 항상 | 필수: 여섯 개 data volume을 모두 분리해서 유지한다 | none | none |
| POL-0022-R4 | 항상 | 금지: 두 node가 한 디렉터리를 가리키게 함 | none | none |
| POL-0022-R5 | recovery target | 금지: live `nodes.conf` identity 재사용 | none | none |
| POL-0022-R6 | 항상 | 필수: `lab_valkey_password`를 Docker secret custody에 유지한다 | none | none |
| POL-0022-R7 | 항상 | 금지: `lab_valkey_password` 값을 Compose·Markdown·shell history·evidence에 둠 | none | none |
| POL-0022-R8 | 항상 | 필수: LAB host client port(기본 17379-17384)는 `127.0.0.1`에만 게시한다 | none | none |
| POL-0022-R9 | 항상 | 금지: cluster-bus port의 host 게시 | none | none |
| POL-0022-R10 | 활성화 전 | 필수: client·dataset·retention·capacity hypothesis를 기록한다 | none | none |
| POL-0022-R11 | 항상 | 금지: 한 host 위의 세 replica를 host availability로 주장 | none | none |
| POL-0022-R12 | 항상 | 필수: 공유 health check·resource limit·`lab_valkey_core_net`/`lab_valkey_obs_net` boundary를 보존한다 | none | none |
| POL-0022-R13 | backup 시 | 필수: primary 전반에 걸친 조정된 지점, 존재하는 경우 전체 AOF set/manifest, engine version, slot map, 파일·크기·hash의 manifest를 보존한다 | none | none |
| POL-0022-R14 | backup 저장 시 | 필수: 별도의 encrypted destination에 저장한다 | none | none |
| POL-0022-R15 | backup 보존 시 | 필수: 별도 destination에서 daily recovery set은 30일, weekly set은 90일 보존한다 | none | none |
| POL-0022-R16 | 항상 | 필수: planning objective는 RPO 24시간, RTO 8시간이며 isolated rehearsal 전까지 미검증으로 둔다 | none | none |
| POL-0022-R17 | 항상 | 필수: 공유 resource-template limit을 적용한다 | none | none |
| POL-0022-R18 | promotion/removal 시 | 필수: 측정된 demand, data-owner 결정, 검증된 export/restore를 갖춘다 | application-level acceptance를 갖춘 isolated compatible restore 요구(promotion/cutover 전) | none |
| POL-0022-R19 | restore 시 | 금지: backup 파일을 live cluster에 붙임 | none | none |
| POL-0022-R20 | restore 시 | 필수: isolated compatible target에 fresh identity를 만들고 완전한 persistence set을 restore한다 | none | none |
| POL-0022-R21 | restore 후 | 필수: `cluster_state`, slot coverage, replica, key count, application read를 검증한다 | application-level acceptance를 갖춘 isolated compatible restore 요구(promotion/cutover 전) | none |
| POL-0022-R22 | production cutover 또는 data destruction 시 | 필수: 승인을 받는다 | 수동 | none |
| POL-0022-R23 | Pin 변경 시 | 필수: 공식 release-note 검토, client와 persistence 호환성 검토, fresh backup, isolated restore evidence, rollback artifact를 갖춘다 | none | none |
| POL-0022-R24 | membership 변경·resharding·credential rotation 시 | 필수: runtime change로 다루고 명명된 task를 둔다 | none | none |
| POL-0022-R25 | 항상 | 필수: 문서의 정적 검증과 runtime 운영 승인을 분리한다 | none | none |
| POL-0022-R26 | 항상 | 필수: `@buenhyden`이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다 | none | none |
| POL-0022-R27 | service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 | 필수: 이 Policy와 linked Guide/Runbook을 함께 검토한다 | 수동 | none |
| POL-0022-R28 | 항상 | 필수: engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 `POL-0079`를, source 반영·재기동은 `POL-0006`을, 보존·삭제는 `POL-0021`의 적용 통제를 따른다 | none | none |
| POL-0022-R29 | 소유 artifact·복구 지점·expiry가 불명확할 때 | 필수: 삭제/재생성을 중단한다 | none | none |
| POL-0022-R30 | 항상 | 금지: 기존 Exceptions 외의 새 예외를 승인된 것으로 간주 | none | none |

- `labs/valkey-cluster/docker-compose.yml` 독립 Compose project와 정확한 `valkey-cluster` profile로만 stack을 선택한다. root include에는 넣지 않는다.
- 여섯 개 data volume을 모두 분리해서 유지한다. 두 node가 한 디렉터리를
  가리키게 하거나 recovery target에서 live `nodes.conf` identity를 재사용하지
  않는다.
- `lab_valkey_password`를 Docker secret custody에 유지한다. 그 값을
  Compose, Markdown, shell history, evidence에 두지 않는다.
- LAB host client port(기본 17379–17384)는 `127.0.0.1`에만 게시한다. cluster-bus port는
  host에 게시하지 않는다. 현재 source는 authentication을 선언하지만 TLS는
  선언하지 않는다.
- 활성화 전에 client, dataset, retention, capacity hypothesis를 기록한다.
  한 host 위의 세 replica는 topology exercise이지 host availability가
  아니다.
- 공유 health check, resource limit, `lab_valkey_core_net`/`lab_valkey_obs_net` boundary를 보존한다.

#### Data protection

RDB와 AOF는 서로 다른 failure mode를 방어한다. backup은 primary 전반에 걸친
조정된 지점, 존재하는 경우 전체 AOF set/manifest, engine version, slot map,
파일, 크기, hash의 manifest를 보존해야 한다. 별도의 encrypted destination에
저장한다. 별도 destination에서 daily recovery set은 30일, weekly set은 90일
보존한다. planning objective는 RPO 24시간, RTO 8시간이다; 둘 다 isolated
rehearsal 전까지는 미검증 상태로 남는다. 공유 resource-template limit은
필수이며 promotion/removal에는 측정된 demand, data-owner 결정, 검증된
export/restore가 필요하다.

restore는 backup 파일을 live cluster에 붙이면 안 된다. isolated compatible
target에 fresh identity를 만들고, 완전한 persistence set을 restore하며,
`cluster_state`, slot coverage, replica, key count, application read를
검증한다. Production cutover 또는 data destruction은 승인이 필요하다.

#### Change and upgrade policy

Pin 변경은 공식 release-note 검토, client와 persistence 호환성 검토, fresh
backup, isolated restore evidence, rollback artifact가 필요하다. Membership
변경, resharding, credential rotation은 runtime change이며 명명된 task가
필요하다.

#### Accountable lifecycle boundary

적용 identity: `valkey-cluster-exporter`, `valkey-cluster-init`, `valkey-node-0`, `valkey-node-1`, `valkey-node-2`, `valkey-node-3`, `valkey-node-4`, `valkey-node-5`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](../03-identity-and-access/0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](../01-common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

### Exceptions

#### Exception Conditions

명명된 cluster client가 없을 때 LAB cluster는 부재할 수 있다. Exception은
runtime mutation, plaintext secret, active storage의 raw 복사, 또는
same-host availability 주장을 승인하지 않는다.

#### Approval and Review

profile, image, volume, credential, consumer, retention, 또는 upstream
lifecycle 변경 이후, 그리고 보존되는 동안 최소 연 1회 검토한다.

## Enforcement

### Mechanisms

독립 LAB configuration과 scoped static policy check를 검증한 다음, promotion
또는 cutover 전에 application-level acceptance를 갖춘 isolated compatible
restore를 요구한다. 미검증 runtime 속성은 명시적으로 기록한다.

### Limits

다음 규칙은 정책이 이름 있는 자동 검사를 연결하지 않았다.

- 이름 있는 검사 없음(선택): `POL-0022-R1`, `POL-0022-R2`
- 이름 있는 검사 없음(volume): `POL-0022-R3`, `POL-0022-R4`, `POL-0022-R5`
- 이름 있는 검사 없음(secret): `POL-0022-R6`, `POL-0022-R7`
- 이름 있는 검사 없음(port): `POL-0022-R8`, `POL-0022-R9`
- 이름 있는 검사 없음(활성화): `POL-0022-R10`, `POL-0022-R11`
- 이름 있는 검사 없음(경계): `POL-0022-R12`
- 이름 있는 검사 없음(backup): `POL-0022-R13`, `POL-0022-R14`, `POL-0022-R15`, `POL-0022-R16`, `POL-0022-R17`
- 이름 있는 검사 없음(restore): `POL-0022-R19`, `POL-0022-R20`
- 이름 있는 검사 없음(변경): `POL-0022-R23`, `POL-0022-R24`
- 이름 있는 검사 없음(lifecycle): `POL-0022-R25`, `POL-0022-R26`, `POL-0022-R28`, `POL-0022-R29`, `POL-0022-R30`
- 수동 검토·승인에 의존(restore): `POL-0022-R22`
- 수동 검토·승인에 의존(lifecycle): `POL-0022-R27`
- 정책이 스스로 밝힌 한계: RPO 24시간/RTO 8시간은 isolated rehearsal 전까지 미검증 상태다.
- 미검증 runtime 속성은 명시적으로 기록해야 하며, 정책은 정적 검증과 runtime 검증을 분리한다.
- Mechanisms의 독립 LAB configuration 검증과 scoped static policy check는 어느 규칙에 대응하는지 정책이 연결하지 않았다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Review Triggers

- [Domain catalog](../../README.md)
- [Valkey persistence](https://valkey.io/topics/persistence/)
- [Valkey Cluster tutorial](https://valkey.io/topics/cluster-tutorial/)
- [Backup policy](../10-platform-and-backup/0021-backup-and-restore.md)
- [Runbook](../../runbooks/15-labs/0022-valkey-cluster.md)
