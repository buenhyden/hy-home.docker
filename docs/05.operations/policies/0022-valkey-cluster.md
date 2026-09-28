---
title: "Valkey Cluster Operations Policy"
version: "1.0.3"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0022"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# Valkey Cluster Operations Policy

## Overview

이 policy는 현재 source configuration을 data protection, security, resource,
lifecycle, 독립적으로 검증 가능한 operator control에 묶는다.

## Policy Scope

이 policy는 LAB 전용 `valkey-cluster` profile에 적용된다. HOME으로 promotion하거나
`mng-valkey`를 대체하는 것은 승인하지 않는다.

## Controls

- root Compose project와 정확한 `valkey-cluster` profile을 통해서만 stack을
  선택한다. Leaf rendering은 지원되지 않는다.
- 여섯 개 data volume을 모두 분리해서 유지한다. 두 node가 한 디렉터리를
  가리키게 하거나 recovery target에서 live `nodes.conf` identity를 재사용하지
  않는다.
- `service_valkey_password`를 Docker secret custody에 유지한다. 그 값을
  Compose, Markdown, shell history, evidence에 두지 않는다.
- 공개된 client와 cluster-bus port를 trusted-network exposure로 취급한다.
  현재 source는 authentication을 선언하지만 TLS는 선언하지 않는다.
- 활성화 전에 client, dataset, retention, capacity hypothesis를 기록한다.
  한 host 위의 세 replica는 topology exercise이지 host availability가
  아니다.
- 공유 health check, resource limit, `lab_net` boundary를 보존한다.

### Data protection

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

### Change and upgrade policy

Pin 변경은 공식 release-note 검토, client와 persistence 호환성 검토, fresh
backup, isolated restore evidence, rollback artifact가 필요하다. Membership
변경, resharding, credential rotation은 runtime change이며 명명된 task가
필요하다.

## Exceptions

명명된 cluster client가 없을 때 LAB cluster는 부재할 수 있다. Exception은
runtime mutation, plaintext secret, active storage의 raw 복사, 또는
same-host availability 주장을 승인하지 않는다.

## Verification

root configuration과 scoped static policy check를 검증한 다음, promotion
또는 cutover 전에 application-level acceptance를 갖춘 isolated compatible
restore를 요구한다. 미검증 runtime 속성은 명시적으로 기록한다.

## Review Cadence

profile, image, volume, credential, consumer, retention, 또는 upstream
lifecycle 변경 이후, 그리고 보존되는 동안 최소 연 1회 검토한다.

## Traceability

- Runtime source: [Valkey Cluster Compose](../../../infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml).
- Artifact: `POL-0022`; parent: `AD-0004`.
- Runtime authority는 연결된 Compose/source 파일에 남는다; 정확한 pin도 그 파일에 있다.

### References

- [Valkey persistence](https://valkey.io/topics/persistence/)
- [Valkey Cluster tutorial](https://valkey.io/topics/cluster-tutorial/)
- [Backup policy](0021-backup-and-restore.md)
- [Runbook](../runbooks/0022-valkey-cluster.md)

## Related Documents

- [Domain catalog](../README.md)
