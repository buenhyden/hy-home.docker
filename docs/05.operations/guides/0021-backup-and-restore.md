---
title: "Backup and Restore Guide"
version: "1.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-30"
layer: "operations"
artifact_id: "GDE-0021"
parent_ids:
- "POL-0021"
implementation_services:
  infra/09-tooling/restic/docker-compose.yml:
  - restic
  - restic-offsite
  - backup-sqlite-export
created: "2026-09-22"
---

# Backup and Restore Guide

## Usage

### What owns which copy

| Tool | Owns | Does not own |
| --- | --- | --- |
| `mng-pg` 내부 pgBackRest | management PostgreSQL cluster의 physical backup, 연속적인 WAL archive, point-in-time recovery | 다른 모든 engine; database별 logical export |
| Restic (`restic` job) | `sets/state-include.txt`에 allowlist된 file-safe tree의 encrypted, deduplicated snapshot, consistent export, `secrets/`와 `.env` | allowlist되지 않은 모든 것, 특히 live engine directory(PostgreSQL, Valkey, Kafka, OpenBao Raft, TSDB, log, search, LAB store)와 ComfyUI model |
| `restic-offsite` job | 로컬 Restic repository 두 개(state set의 `pgbackrest/` 포함)를 Cloudflare R2 repository 하나로 `restic copy`, 원격 `check` | 로컬 쓰기, 원격 snapshot 삭제 |
| `backup-sqlite-export` job | Online Backup API를 통한 Grafana, Gatus, Open WebUI SQLite database의 consistent copy | 다른 SQLite 파일 |
| Host orchestrator `hyhome-backup.sh` | 순서, single-run lock, cross-disk preflight, PostgreSQL globals와 Valkey RDB export | retention delete (`forget-prune`) |

실행 중인 PostgreSQL data directory의 복사본은 database backup이 아니다.
PostgreSQL recovery path는 오직 pgBackRest뿐이다.

### Destinations

두 repository가 host의 서로 다른 physical disk에 나뉘어 있어 disk 하나가
실패해도 복사본 하나는 남는다.

- `BACKUP_STATE_REPO_DIR` (system SSD): pgBackRest repository `pgbackrest/`,
  data-disk state용 Restic repository `restic/`, export staging `staging/`.
  전체 크기는 `BACKUP_STATE_MAX_GIB`(5)로 제한된다.
- `BACKUP_HOST_REPO_DIR` (data disk): SSD에 있는 `secrets/`와 `.env`용 Restic
  repository `restic/`.

orchestrator는 자신이 보호하는 데이터와 같은 filesystem이나 그 내부에 있는
repository를 거부한다. 오프사이트로는 로컬 run이 성공할 때마다
`restic-offsite`가 두 Restic repository(state set에 `pgbackrest/` 포함)를
Cloudflare R2 repository 하나로 복사한다(ADR-0041). owner가
[RUN-0021](../runbooks/0021-backup-and-restore.md) 8단계의 R2 설정을 마치기
전까지는 모든 복사본이 한 host에 있어 offsite recovery를 할 수 없다.

### Schedule and load

`hyhome-backup.timer`는 매일 KST 03:30에 최대 30분의 random delay를 두고
실행되며 4시간이 지나면 실행이 중단된다. pgBackRest는 일요일에 full backup을,
다른 날에는 differential backup을 수행한다. `archive_timeout`은 unarchived
WAL을 5분으로 제한한다. unit은 idle I/O class와 `Nice=10`으로 실행되고
Restic은 낮은 block-I/O weight를 받는다. Renovate(월요일 00:00-01:00)와 Spark
table maintenance(일요일 05:00)는 이 window와 절대 겹치지 않는다.

### Capacity and growth (measured 2026-09-22)

| Repository | Input measured | Bound |
| --- | --- | --- |
| pgBackRest (SSD) | 전체 database 96 MB; WAL 약 14 MB/h (압축 전 330 MB/day; `archive_timeout`마다 강제 전환되는 segment는 zstd가 제거하는 0으로 채워짐) | full backup 2개와 그 differential 및 WAL(약 2주); 계획 추정치는 2 GB 미만이며 기록된 크기로 대체될 예정 |
| Restic state (SSD) | allowlist된 tree 약 0.3 GB (registry 236 MB, Open WebUI upload, Airflow DAG/config/plugin) 및 export 약 10 MB | deduplicated; `forget-prune`까지 일일 변경분만큼 증가하며 연간 5 GB 미만으로 계획 |
| Restic host (data disk) | `secrets/`와 `.env`, 수 킬로바이트 | 무시할 수준 |
| Staging | 실행 중에만 export | 종료마다 비워짐 |

증가는 지수적이 아니라 선형적이다. 이전 backup에서 다시 복사되는 것은 없으며,
orchestrator는 backup 대상 소스 내부의 repository를 거부한다. Airflow
log(175 MB, 약 64 MB/day)와 cache는 의도적으로 allowlist에서 제외한다. 각
실행은 세 repository 크기를 journal에 기록한다. 예산은 강제된다. pgBackRest가
오래된 backup을 만료시킨 후 orchestrator가 `BACKUP_STATE_REPO_DIR`을 측정하고
`BACKUP_STATE_MAX_GIB` 이상이면 아무것도 삭제하지 않고 Restic 단계를
건너뛰며 실행을 실패시킨다. 위 추정치의 합은 3 GB 미만이다(pgBackRest 2 GB
미만, 시작 시점 Restic 약 0.3 GB). 20 GiB free-space floor는 SSD에 적용된다.

### Keys

`secrets/backup/pgbackrest_cipher_pass.txt`(BKP-001)는 pgBackRest repository를
암호화하고, `secrets/backup/restic_password.txt`(BKP-002)는 두 Restic
repository를 암호화한다. 이 값들은 host repository 내부에도 backup되는데, 그
repository를 열려면 같은 Restic password가 필요하므로 두 값의 offline
복사본을 이 host 밖에 보관한다. 이를 잃으면 모든 backup을 읽을 수 없게 된다.

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
- Implementation: [Restic Compose](../../../infra/09-tooling/restic/docker-compose.yml),
  [Restic package](../../../infra/09-tooling/restic/README.md),
  [pgBackRest image](../../../infra/04-data/operational/mng-db/pg/backup/Dockerfile)

## Related Documents

- [Management database runbook](../runbooks/0028-management-database.md)
- [Storage exhaustion runbook](../runbooks/0035-storage-exhaustion.md)
