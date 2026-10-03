---
title: "Backup and Restore Guide"
version: "1.1.4"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "GDE-0021"
parent_ids:
- "POL-0021"
implementation_services:
  infra/09-platform-ops/restic/docker-compose.yml:
  - restic
  - restic-offsite
  - backup-sqlite-export
created: "2026-09-22"
---

# Backup and Restore Guide

## Usage

### What owns which copy

| 도구 | 소유 범위 | 소유하지 않는 범위 |
| --- | --- | --- |
| `mng-pg` 내부 pgBackRest | management PostgreSQL cluster의 physical backup, 연속적인 WAL archive, point-in-time recovery | 다른 모든 engine; database별 logical export |
| Restic (`restic` job) | `sets/state-include.txt`에 allowlist된 file-safe tree의 encrypted, deduplicated snapshot, consistent export, `secrets/`와 `.env` | allowlist되지 않은 모든 것, 특히 live engine directory(PostgreSQL, Valkey, Kafka, OpenBao Raft, TSDB, log, search, LAB store)와 ComfyUI model |
| `restic-offsite` job | 로컬 Restic repository 두 개(state set의 `pgbackrest/`와 `dev-pgbackrest/` 포함)를 Cloudflare R2 repository 하나로 `restic copy`, 원격 `check` | 로컬 쓰기, 자동 원격 snapshot 삭제(owner-run 승인 prune는 RUN-0021) |
| `backup-sqlite-export` job | Online Backup API를 통한 Grafana, Gatus, Open WebUI SQLite database의 consistent copy | 다른 SQLite 파일 |
| Host orchestrator `hyhome-backup.sh` | 순서, single-run lock, cross-disk preflight, PostgreSQL globals와 Valkey RDB export | retention delete (`forget-prune`) |

실행 중인 PostgreSQL data directory의 복사본은 database backup이 아니다.
구현된 자동 PostgreSQL 경로는 pgBackRest이며 database별 logical 복구 요구를 대체하지 않는다.

### Destinations

두 repository는 서로 다른 physical disk에 두어야 한다. source의 `st_dev` 비교는 filesystem 구분만 확인하며 별도 partition/LVM이 같은 physical disk일 가능성을 배제하지 못한다. 실제 disk mapping은 owner 확인이 필요하다.

- `BACKUP_STATE_REPO_DIR` (system SSD): 관리 pgBackRest repository `pgbackrest/`, 개발 repository `dev-pgbackrest/`,
  data-disk state용 Restic repository `restic/`, export staging `staging/`.
  `BACKUP_STATE_MAX_GIB`(5)는 pgBackRest/export 후, Restic 전 검사 기준이다. quota나 실행 중 크기 제한이 아니며 이후 Restic 쓰기로 초과할 수 있다.
- `BACKUP_HOST_REPO_DIR` (data disk): SSD에 있는 `secrets/`와 `.env`용 Restic
  repository `restic/`.

orchestrator는 자신이 보호하는 데이터와 같은 filesystem이나 그 내부에 있는
repository를 거부한다. 오프사이트로는 로컬 Restic backup/check가 성공하면(앞선 export 실패 여부와 별개로)
`restic-offsite`가 두 Restic repository(state set에 `pgbackrest/`와 `dev-pgbackrest/` 포함)를
Cloudflare R2 repository 하나로 복사한다(ADR-0041). owner가
[RUN-0021](../runbooks/0021-backup-and-restore.md) 8단계의 R2 설정을 마치기
전까지는 모든 복사본이 한 host에 있어 offsite recovery를 할 수 없다.

### Schedule and load

`hyhome-backup.timer`는 매일 KST 03:30에 최대 30분의 random delay를 두고
실행되며 4시간이 지나면 실행이 중단된다. pgBackRest는 일요일에 full backup을,
다른 날에는 differential backup을 수행한다. `archive_timeout=300`은 WAL segment 전환을 유도하며 successful archive를 5분 이내로 보장하지 않는다. 4 GiB archive queue 한도 초과로 segment가 폐기되면 새 유효 backup 전 PITR chain이 끊긴다. unit은 idle I/O class와 `Nice=10`으로 실행되고
Restic은 낮은 block-I/O weight를 받는다. Spark table maintenance(일요일 05:00)와 겹칠 수 있다. `Persistent=true`의 catch-up도 시간대를 바꾸며 `flock`은 backup끼리만 직렬화한다. Renovate/Spark와의 상호 배제는 구현되어 있지 않다.

### Capacity and growth (measured 2026-09-22)

| 저장소 | 측정한 입력 | 범위·한계 |
| --- | --- | --- |
| pgBackRest (SSD) | 전체 database 96 MB; WAL 약 14 MB/h (압축 전 330 MB/day; `archive_timeout`마다 강제 전환되는 segment는 zstd가 제거하는 0으로 채워짐) | full backup 2개와 그 differential 및 WAL(약 2주); 계획 추정치는 2 GB 미만이며 기록된 크기로 대체될 예정 |
| Restic state (SSD) | allowlist된 tree 약 0.3 GB (registry 236 MB, Open WebUI upload, Airflow DAG/config/plugin) 및 export 약 10 MB | deduplicated; `forget-prune`까지 일일 변경분만큼 증가하며 2026-09-22 당시 연간 5 GB 미만 추정; 09-30 관측으로 폐기된 예측 |
| Restic host (data disk) | `secrets/`와 `.env`, 수 킬로바이트 | 무시할 수준 |
| Staging | 실행 중에만 export | 종료마다 비워짐 |

증가율은 workload와 retention에 따라 달라진다. 동일 chunk는 deduplicate되지만 pgBackRest 변경 파일은 새 chunk가 될 수 있으며,
orchestrator는 backup 대상 소스 내부의 repository를 거부한다. Airflow
log(175 MB, 약 64 MB/day)와 cache는 의도적으로 allowlist에서 제외한다. 각
실행은 세 repository 크기를 journal에 기록한다. 예산 검사는 다음 Restic 실행만 막는다. pgBackRest가
오래된 backup을 만료시킨 후 orchestrator가 `BACKUP_STATE_REPO_DIR`을 측정하고
`BACKUP_STATE_MAX_GIB` 이상이면 아무것도 삭제하지 않고 Restic 단계를
건너뛰며 실행을 실패시킨다. 위 3 GB 미만 합계는 당시 추정이며 현재 보장이 아니다. 2026-09-23 429 MiB → 09-30 1679 MiB(약 180 MiB/day) 기록으로 대체한다. 20 GiB free-space floor는 state repository filesystem의 실행 전 검사이며 host repository·scratch·실행 중 여유를 보장하지 않는다.

### Development database handoff

개발 repository는 별도 stanza `dev`와 `dev_pgbackrest_cipher_pass`를 사용하며
관리 repository·PGDATA와 공유하지 않습니다. Restic은 이 경로를 읽기 전용으로
state set에 포함하여 기존 offsite copy와 전체 state 예산에 함께 계산합니다.
배포 전 두 repository 디렉터리와 용량·키 보관·일정 승인이 필요합니다.
개발 stanza `check`(300초), physical backup(1800초), globals/schema export(각
300초)는 제한 시간 내 종료해야 합니다. 개발 서버 중단·check 실패·부분 export는
unit 실패를 유지하고 성공 timestamp를 갱신하지 않습니다. 기존 동작대로 partial
Restic snapshot/offsite copy는 남을 수 있으므로 전체 성공 실행과 구분합니다.

schema export는 DB별 extension 선언과 권한을, physical backup의 catalog는
설치된 extension version과 적용 migration 이력을 보존합니다. 별도 image ID와
infra revision도 staging에 기록합니다. 외부 앱의 정확한 migration source revision과
restore 후 역할/extension/migration 대조는 앱 소유자가 제공합니다. infra revision이
앱 revision을 대신하지 않습니다. 현재 `archive_mode=off`이므로 online backup/PITR
활성화와 실제 복구는 아직 검증되지 않았습니다.

### Keys

`secrets/backup/mng-pg/pgbackrest_cipher_pass.txt`(BKP-001)는 pgBackRest repository를
암호화하고, `secrets/backup/restic/restic_password.txt`(BKP-002)는 두 Restic
repository를 암호화한다. 이 값들은 host repository 내부에도 backup되는데, 그
repository를 열려면 같은 Restic password가 필요하므로 두 값의 offline
복사본을 이 host 밖에 보관한다. 이를 잃으면 모든 backup을 읽을 수 없게 된다.

### Identity-specific behavior

restic/restic-offsite 는 기본 snapshots job 이고 backup/check/copy/prune 는 각각 다른 쓰기 효과다. SQLite helper 는 세 DB Online Backup API 와 integrity check 로 staging 을 만들며 원본 WAL/SHM 처리를 위해 source mount 가 rw 다. local restic 은 network none, offsite 만 전용 outbound network 다. 전체 성공은 unit exit0·모든 export 와 check·timestamp 로 판단하고 partial snapshot/copy 는 실패를 지우지 않는다. detailed recovery/capacity/custody 는 RUN/POL-0021 의 계약을 따른다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `restic` | local snapshot/check job; 두 encrypted repository write | HTTP health 없음; 종료 코드와 읽기/검증 결과 확인 | [선택·의존·접속·입력·mount](../../../infra/09-platform-ops/restic/docker-compose.yml) |
| `restic-offsite` | remote copy/check/prune job; local repository read-only | HTTP health 없음; 종료 코드와 읽기/검증 결과 확인 | [선택·의존·접속·입력·mount](../../../infra/09-platform-ops/restic/docker-compose.yml) |
| `backup-sqlite-export` | 세 SQLite online export job; source WAL/SHM rw 예외 | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../infra/09-platform-ops/restic/docker-compose.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의2026-10-01 source snapshot과 official version/build 검토는 [W4 Task](../../98.archive/completed/03.specs/0198-operations-documentation-system/tasks/tsk-0004-data-messaging-analytics.md)에 보존했다. 반복OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.

## Common Checks

backup data를 변경하지 않는 점검이다(Restic은 여전히 짧게 유지되는 lock을 기록한다):

```bash
docker exec -u postgres mng-pg pgbackrest --stanza=mng info
docker compose --profile backup run --rm --no-deps restic snapshots
systemctl list-timers hyhome-backup.timer
journalctl -u hyhome-backup.service -n 50 --no-pager
```

정상이면 output에 최근 backup과 WAL archive range가 담긴 `status: ok`,
최근 `hyhome-state`와 `hyhome-host` snapshot, 성공한 마지막 실행이 나온다.

## Runbook Handoff

초기 설정, manual 실행, restore, point-in-time recovery, retention delete
절차는 [RUN-0021](../runbooks/0021-backup-and-restore.md)에 있다.

## Traceability

- Policy: [POL-0021](../policies/0021-backup-and-restore.md)
- Implementation: [Restic Compose](../../../infra/09-platform-ops/restic/docker-compose.yml),
  [Restic package](../../../infra/09-platform-ops/restic/README.md),
  [pgBackRest image](../../../infra/04-data/mng-db/pg/backup/Dockerfile)

## Related Documents

- [Management database runbook](../runbooks/0028-management-database.md)
- [Storage exhaustion runbook](../runbooks/0035-storage-exhaustion.md)
