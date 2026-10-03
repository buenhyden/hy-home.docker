---
title: "Valkey Cluster Usage Guide"
version: "2.0.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-02"
layer: "operations"
artifact_id: "GDE-0022"
parent_ids:
- "POL-0022"
created: "2026-05-10"
---

# Valkey Cluster Usage Guide

## Usage

이 package는 optional한 six-node Valkey Cluster laboratory를 설명한다. 모든
node가 Docker host 하나를 공유하므로 M0021은 모든 service를 **LAB**으로
분류한다. 이는 HOME workflow broker가 아니며, Airflow와 n8n은 기본적으로
`mng-valkey`를 사용한다.

### Current implementation

[`labs/valkey-cluster.yml`](../../../labs/valkey-cluster.yml)은 독립 LAB Compose project이며 root는 이를 include하지 않는다. 정확한 profile `valkey-cluster`는 `valkey-node-0`부터
`valkey-node-5`까지, one-shot `valkey-cluster-init`, `valkey-cluster-exporter`를
선택한다. initializer는 `lab_valkey_core_net`에 primary 3개와 replica 3개를 구성한다.

각 node는 `${LAB_DATA_DIR}/valkey-cluster/data-0`부터 `data-5`까지에 resolve되는
bind-backed volume `valkey0-data`부터 `valkey5-data`까지를 하나씩 소유한다.
node는 기본 17379–17384의 LAB 전용 loopback host port를 내부 6379–6384에 매핑하고 cluster-bus port 16379–16384를
expose한다. startup, init, exporter path는 공유 `lab_valkey_password`
Docker secret을 읽는다. tracked configuration은 주기적인 RDB snapshot과
`appendfsync everysec`을 사용하는 AOF를 모두 활성화한다. `/data/nodes.conf`는
node-local cluster identity이다. resource limit과 health check는 공유
Compose template에서 오며 선택하기 전에 렌더링된 LAB configuration에서
점검해야 한다.

### Identity-specific behavior

노드 0/1/2/3/4/5 는 각 PORT·announce address·bind volume·client/bus port 가 다르고 같은 template/security 를 공유한다. init script 는 내부 6379~6384 를 고정 사용한다. `LAB_VALKEY*_HOST_PORT`는 loopback host port만 바꾸며 실제 cluster slot·client 연결은 격리 실행 전까지 미검증이다. 비정상 또는 이미 비어 있지 않은 nodes 상태는 init이 실패하도록 수정했다. init 성공만으로 slot16384/replica 건강을 보장하지 않는다. exporter 는 node0 하나를 target 한다. engine9.1.2 와 exporter1.91.1 release 는 별개이며 AOF/RDB 와 fresh cluster identity 복원 계약은 유지한다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `valkey-cluster-exporter` | node0 target exporter; dependency6개와 scrape 범위 구분 | 선언된 endpoint health; scrape/data 기능 별도 | [선택·의존·접속·입력·mount](../../../labs/valkey-cluster.yml) |
| `valkey-cluster-init` | one-shot cluster create; 비정상 기존 상태는 실패 | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../labs/valkey-cluster.yml) |
| `valkey-node-0` | cluster node 0; 고유 port/announce/node-local persistence | 인증 PING; cluster slot/queue 정합성 별도 | [선택·의존·접속·입력·mount](../../../labs/valkey-cluster.yml) |
| `valkey-node-1` | cluster node 1; 고유 port/announce/node-local persistence | 인증 PING; cluster slot/queue 정합성 별도 | [선택·의존·접속·입력·mount](../../../labs/valkey-cluster.yml) |
| `valkey-node-2` | cluster node 2; 고유 port/announce/node-local persistence | 인증 PING; cluster slot/queue 정합성 별도 | [선택·의존·접속·입력·mount](../../../labs/valkey-cluster.yml) |
| `valkey-node-3` | cluster node 3; 고유 port/announce/node-local persistence | 인증 PING; cluster slot/queue 정합성 별도 | [선택·의존·접속·입력·mount](../../../labs/valkey-cluster.yml) |
| `valkey-node-4` | cluster node 4; 고유 port/announce/node-local persistence | 인증 PING; cluster slot/queue 정합성 별도 | [선택·의존·접속·입력·mount](../../../labs/valkey-cluster.yml) |
| `valkey-node-5` | cluster node 5; 고유 port/announce/node-local persistence | 인증 PING; cluster slot/queue 정합성 별도 | [선택·의존·접속·입력·mount](../../../labs/valkey-cluster.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의2026-10-01 source snapshot과 official version/build 검토는 [W4 Task](../../98.archive/completed/03.specs/0198-operations-documentation-system/tasks/tsk-0004-data-messaging-analytics.md)에 보존했다. 반복OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.

### Images, configuration and resource controls

고정된 `valkey/valkey`와 `oliver006/redis_exporter` image의 기준은 Compose
파일이다. repository Renovate 설정이 update를 제안할 수 있으며
`infra/tech-stack.versions.json`은 파생된 drift 증거이다. `PORT`와
`NODE_NAME`이 node를 구성하고, LAB의 `LAB_VALKEY*_HOST_PORT`와 `LAB_VALKEY_EXPORTER_PORT` key가 exposure를 제어한다. node는
`template-stateful-med`를, init은 `template-job-low`를, exporter는
`template-infra-readonly-low`를 extend한다. one-shot initializer를 제외하고
각각 health check를 선언한다. client는 cluster-aware node endpoint에 직접
접속하고 exporter의 `-redis.addr`는 node0 하나다. 여섯 healthy dependency는 여섯 scrape target을 뜻하지 않는다. 전체 node/slot 상태는 별도 cluster-aware 점검이 필요하다.

### Static preflight and normal use

이 LAB의 입력은 [예시 환경 파일](../../../labs/.env.example)과 비공개 `labs/.env`가 소유한다. secret 파일은 `LAB_SECRET_DIR`(기본 `../secrets/labs`) 아래의 [LAB별 경로](../../../labs/valkey-cluster.yml)에 둔다. source 반영, 실제 실행, 비밀 파일 이동 완료와 복구 검증은 별도로 확인한다.

repository root에서 독립 `labs/valkey-cluster.yml`을 지정한다. `labs/.env.example`은 정적 검증용이며, 실제 실행 전에 승인된 `labs/.env`와 `LAB_DATA_DIR`, LAB secret root를 준비한다.

```bash
LAB_DATA_DIR=/tmp docker compose --env-file labs/.env.example -f labs/valkey-cluster.yml --profile valkey-cluster config --quiet
LAB_DATA_DIR=/tmp docker compose --env-file labs/.env.example -f labs/valkey-cluster.yml --profile valkey-cluster config --services
```

profile을 시작하거나, test key를 쓰거나, membership을 변경하거나, node를
중지하는 것은 runtime action이며 별도로 승인된 task가 필요하다. 선택할 때는
cluster-aware client 호환성, 의도된 dataset, retention, capacity와 함께
same-host replica가 host 손실을 막지 못한다는 점을 기록한다.

### Backup, restore and upgrade boundary

[RUN-0022](../runbooks/0022-valkey-cluster.md)를 사용한다. 사용 가능한
backup은 모든 primary(및 의도적으로 유지되는 replica)의 조율된 persistence
set, AOF 사용 시 전체 multi-part AOF directory와 manifest, RDB checkpoint,
engine version, slot ownership, checksum을 포함해야 한다. 서로 다른 시점의
파일을 섞거나 `nodes.conf`를 이식 가능한 identity로 취급하지 않는다.

restore는 격리된 호환 six-node target에서 리허설한다. cluster identity를
재생성하고, 완전한 persistence set을 restore하고, 모든 slot과 replica
link를 검증하고, cutover 전에 key count/application read를 비교한다.
upgrade는 release note, client 호환성, rollback을 포함한 별도 계획을
따른다. 이 가이드는 in-place major jump를 승인하지 않는다.

### Security and license

password secret은 transport encryption을 제공하지 않는다. client port는
`127.0.0.1`에만 게시하며 cluster-bus port는 host에 게시하지 않는다. Valkey
자체 안내는 Cluster가 trusted network용으로 설계되었다고 경고한다. Valkey는
BSD 3-Clause license를 사용하며, client와 image는 자체 license를 유지한다.

### Official references

- [Valkey persistence](https://valkey.io/topics/persistence/)
- [Valkey Cluster tutorial and security boundary](https://valkey.io/topics/cluster-tutorial/)
- [Valkey security](https://valkey.io/topics/security/)
- [Valkey license](https://github.com/valkey-io/valkey/blob/unstable/COPYING)

## Common Checks

정확한 LAB profile, service, health/resource control, writable-state
ownership, secret reference, exposure, engine별 recovery boundary를 확인한다.
static pass는 configuration 증거일 뿐이다. runtime과 restore는 별개로 남는다.

## Traceability

- Artifact: `GDE-0022`; governing policy: `POL-0022`.
- Runtime authority: `labs/valkey-cluster.yml`.

## Related Documents

- [Operations policy](../policies/0022-valkey-cluster.md)
- [Health and recovery runbook](../runbooks/0022-valkey-cluster.md)
- [Data backup policy](../policies/0021-backup-and-restore.md)
