---
title: "Backup and Restore Runbook"
version: "1.2.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0021"
parent_ids:
- "GDE-0021"
created: "2026-09-22"
---

# Backup and Restore Runbook

## When to Use

backup repository를 준비하거나, `mng-pg`를 pgBackRest image로 전환하거나,
backup을 실행/검증하거나, PostgreSQL을 isolation 환경에서 특정 시점으로
복원하거나, Restic에서 파일을 복원하거나, 오래된 snapshot을 삭제할 때
사용한다. service를 재시작하거나 repository에 쓰거나 snapshot을 삭제하는
모든 단계는 target을 명시한 별도의 approval이 필요하다.

## Procedure

실행 중인 checkout의 repository root에서 command를 실행한다. secret 파일이나
rendered Compose model을 절대 출력하지 않는다.

### 1. Prepare `.env`, directories and keys (once, before the change is checked out on the host)

먼저 `.env`를 sync한다. `BACKUP_STATE_REPO_DIR`를 설정하기 전에는
`mng-pg`를 재생성하면 repository 경로가 없어 실패한다.

```bash
bash scripts/operations/gen-secrets.sh --sync-metadata
bash scripts/operations/gen-secrets.sh
state=/home/hyunyoun/backups                 # the BACKUP_STATE_REPO_DIR value (SSD)
host=/home/hyunyoun/storage/backups          # the BACKUP_HOST_REPO_DIR value (data disk)
sudo install -d -o 70 -g 70 -m 0750 "$state/pgbackrest"
install -d -m 0700 "$state/restic" "$state/staging" "$host/restic"
install -d -m 0755 "$state/metrics"          # before node-exporter is (re)created
```

Expected: `.env`에 `BACKUP_STATE_REPO_DIR`, `BACKUP_HOST_REPO_DIR`,
`BACKUP_STATE_MAX_GIB`, `POSTGRES_ARCHIVE_TIMEOUT`가 기존 값은 그대로 둔 채
추가된다. 디렉터리는 나열된 owner로 존재하고 BKP-001/BKP-002 파일도
존재한다. 첫 backup 전에 두 key 값을 offline custody로 복사한다. 경로에
이미 자신이 만들지 않은 데이터가 있으면 중단한다.

### 2. Switch `mng-pg` to the pgBackRest image (approval: restarts every management-DB consumer)

전제 조건: 예를 들어
`docker exec mng-pg sh -c 'pg_dumpall -U "$POSTGRES_USER"' > "$state/pre-pgbackrest.sql"`로
0600 파일에 만든 최신 logical dump, 그리고 state 디렉터리 아래 최소 20 GiB의
여유 공간.

```bash
docker compose build mng-pg
docker compose up -d --no-deps mng-pg
docker exec -u postgres mng-pg pgbackrest --stanza=mng stanza-create
docker exec -u postgres mng-pg pgbackrest --stanza=mng check
```

기대 결과: `mng-pg`가 healthy이고, `stanza-create`와 `check`가 `completed
successfully`로 끝나며, `SHOW archive_mode`가 `on`을 반환한다. `stanza-create`가 성공하기 전까지
`archive_command`는 실패하고 WAL은
`pg_wal`에 남는다. `archive-push-queue-max`(4 GiB)를 넘으면 pgBackRest는
disk를 보호하려고 WAL을 폐기하고 그러면 다음 full backup 전까지
point-in-time recovery에 공백이 생긴다.
Rollback: Compose에서 이전 image line을 복원하고 `up -d --no-deps mng-pg`를
실행한다. repository를 사용할 수 없으면 먼저 `archive_mode=off`를 설정한다.

### 3. Initialize Restic and install the timer (once)

```bash
docker compose --profile backup run --rm --no-deps restic init
sudo install -m 0644 infra/09-tooling/restic/systemd/hyhome-backup.service /etc/systemd/system/
sudo install -m 0644 infra/09-tooling/restic/systemd/hyhome-backup.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now hyhome-backup.timer
```

`init`은 이미 있는 repository는 건너뛰고 절대 re-key하지 않는다.

### 4. Run or verify a backup

```bash
sudo systemctl start hyhome-backup.service
journalctl -u hyhome-backup.service -n 80 --no-pager
docker exec -u postgres mng-pg pgbackrest --stanza=mng info
docker compose --profile backup run --rm --no-deps restic snapshots
```

Expected: exit 0, 새 pgBackRest backup, 새 Restic snapshot 두 개, `restic
check` "no errors were found", 빈 `staging/`. exit 75는 다른 run이 lock을
쥐고 있다는 뜻이고, exit 64는 디렉터리 누락, 20 GiB 미만의 여유 공간, 또는
repository가 source와 같은 filesystem 위에 있거나 그 내부에 있다는 뜻이다.
"over the 5 GiB budget; Restic backup skipped"를 로그에 남기는 run은 exit 1로
끝난다. 이때 pgBackRest는 완료되고 Restic은 건드리지 않는다. 기록된 크기를 검토하고
승인된 `forget-prune`(step 7) 또는 더 큰 budget을 요청한다. unit은 4시간 후
정지하는데 그래도 staging은 비워진다. 실행 중인 Restic 프로세스가 없을 때
`restic unlock`으로 stale Restic lock을 해제한다.

`mng-valkey` RDB 내보내기는 컨테이너 안에서 300초 제한으로 실행한다. 제한을
넘기거나 실패하면 "mng-valkey RDB export failed or timed out; export dropped"를
남기고 불완전한 파일을 지운 뒤 나머지 단계와 Restic을 계속 진행하며, run은
exit 1로 끝난다.

SeaweedFS가 실행 중이면 run은 vacuum도 일시 정지하고 filer metadata를
export한다. `weed shell`이 오류 텍스트를 내거나, export가 비었거나, master와 filer 중 하나만
실행 중이면 run은 exit 1로 끝난다(RUN-0024).

exit 0으로 끝난 run만 `$state/metrics/hyhome_backup.prom`에
`hyhome_backup_last_success_timestamp_seconds`를 쓴다. node-exporter는 이
디렉터리를 read-only로 mount하고, Compose는 디렉터리를 만들지 않으므로 없으면
node-exporter가 시작되지 않는다. 이때는 step 1의 `install -d`를 host user로
실행한다. timestamp를 쓰지 못한 run은 "backup succeeded but its success
timestamp was not written"을 남기고 exit 1로 끝난다.

| Alert | 조건 | 대응 |
| --- | --- | --- |
| `HyhomeBackupStale` | 마지막 성공 후 26시간 경과, 또는 metric이 26시간 동안 없음 | `systemctl list-timers hyhome-backup.timer`와 서비스 결과를 보고, journal의 상태 줄로 멈춘 단계를 찾는다. 원인을 고친 뒤 이 step으로 한 번 실행한다. |
| `HostSystemDiskLow` | `/` 여유 공간 25 GiB 미만이 15분 지속 | 20 GiB 아래에서는 다음 run이 exit 64로 멈춘다. `docker system df`로 빌드 캐시와 어떤 container도 쓰지 않는 image를 확인하고, 승인을 받아 정리한다. |

### 5. Point-in-time restore of `mng-pg` into isolation

live `PGDATA` 위가 아닌 새 디렉터리로 복원한다. `SCRATCH_ROOT`를 data disk
위의 디렉터리로 설정한다. `mktemp`만 쓰면 system disk에 만들어지고 full restore가
그 disk를 가득 채울 수 있다. image 이름은 pin을 소유하는 Compose에서 가져온다.

```bash
pg_image="$(docker compose config --images mng-pg)"
target='2026-09-22 06:13:56+00'   # a time after the last wanted commit
scratch="$(mktemp -d -p "${SCRATCH_ROOT:?set to a data-disk directory}")"
chmod 0755 "$scratch"   # the postgres user (UID 70) must traverse it
docker run --rm \
  -v "$PWD/secrets/backup/pgbackrest_cipher_pass.txt:/run/secrets/pgbackrest_cipher_pass:ro" \
  -v "$state/pgbackrest":/var/lib/pgbackrest:ro \
  -v "$scratch:/var/lib/postgresql/data" \
  --entrypoint sh "$pg_image" -ec '
    mkdir -p /tmp/pgbackrest/conf.d
    printf "[global]\nrepo1-cipher-pass=%s\n" "$(cat /run/secrets/pgbackrest_cipher_pass)" > /tmp/pgbackrest/conf.d/cipher.conf
    chown -R postgres /tmp/pgbackrest
    install -d -o postgres -g postgres -m 0700 /var/lib/postgresql/data/pgdata
    gosu postgres pgbackrest --config-include-path=/tmp/pgbackrest/conf.d --stanza=mng \
      --type=time "--target='"$target"'" --target-action=promote --archive-mode=off restore'
```

recovery가 `archive-get`으로 WAL을 읽기 때문에 복원된 copy는 동일한 image
entrypoint, cipher secret, read-only로 mount한 repository를 사용해 internal
network에서 시작한다.

```bash
docker network create --internal restore-check
docker run -d --name mng-pg-restore-check --network restore-check \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -e PGBACKREST_CONFIG_INCLUDE_PATH=/tmp/pgbackrest/conf.d \
  -v "$PWD/secrets/backup/pgbackrest_cipher_pass.txt:/run/secrets/pgbackrest_cipher_pass:ro" \
  -v "$state/pgbackrest":/var/lib/pgbackrest:ro \
  -v "$scratch:/var/lib/postgresql/data" \
  "$pg_image" postgres -c archive_mode=off
```

기대 로그 줄: `recovery stopping before commit`, `selected new timeline
ID`. `psql`로 application row를 확인한 뒤 container와 network를 제거하고
scratch copy를 삭제한다. live cluster 교체는 별도의 승인된 cutover다.

### 6. Restore files from Restic

일반 container로 scratch 디렉터리에 복원한다. hardened job에는 ownership을
다시 적용할 권한이 없다.

```bash
restic_image="$(docker compose --profile backup config --images restic)"
scratch="$(mktemp -d -p "${SCRATCH_ROOT:?set to a data-disk directory}")"
docker run --rm -e RESTIC_PASSWORD_FILE=/pw \
  -v "$PWD/secrets/backup/restic_password.txt:/pw:ro" \
  -v "$state/restic:/repo:ro" -v "$scratch:/out" \
  "$restic_image" -r /repo --no-lock restore latest --target /out --include /src/state/exports
```

`secrets/`와 `.env`에는 `"$host/restic"`을 사용한다.
`sha256sum`으로 비교한 뒤 검토한 파일만 다시 복사한다.

SeaweedFS는 한 세트로 복원한다: 같은 snapshot의
`--include /src/state/volumes/data/seaweedfs`와
`/src/state/exports/seaweedfs-filer.meta`를 함께 사용한 뒤 RUN-0024를
따른다(volume과 master tree가 제자리에 있고 filer store가 비어 있으며
`fs.meta.load`).

### 7. Delete old snapshots (approval: irreversible)

```bash
docker compose --profile backup run --rm --no-deps \
  -e HYHOME_PRUNE_CONFIRM=delete-old-snapshots restic forget-prune
```

세트당 daily 30개, weekly 13개, monthly 12개의 snapshot을 유지한다.
pgBackRest는 자체 backup을 `repo1-retention-full=2`로 만료시킨다.

## Evidence

command, exit status, pgBackRest backup label, Restic snapshot ID, 복원된 row
count 또는 file hash, 소요 시간을 기록한다. key 값, dump 내용, rendered
configuration은 절대 기록하지 않는다.

## Rollback or Recovery

- `archive_command` 실패: `pgbackrest --stanza=mng check`가 원인을 보여준다.
  `pg_wal`이 disk를 채우기 전에 repository 경로나 ownership을 고치거나,
  approval을 받아 `archive_mode=off`를 설정한다([RUN-0035](0035-storage-exhaustion.md)).
- 잘못되었거나 잃어버린 key: pgBackRest `info`가 `status: error`를 보고하고
  Restic은 `wrong password or no key found`를 보고한다. offline custody에서
  key를 복구한다. repository를 읽을 다른 방법은 없다.
- 중단된 Restic run: 다시 실행한다. 다른 Restic 프로세스가 실행 중이 아닌지
  확인한 뒤에만 `restic unlock`한다.

## Escalation

restore rehearsal이 실패하거나, 두 disk 모두 오류를 보고하거나, key를
잃어버렸을 때 owner에게 escalation한다.

## Traceability

- Guide: [GDE-0021](../guides/0021-backup-and-restore.md); Policy: [POL-0021](../policies/0021-backup-and-restore.md)
- Alerts: [host backup rules](../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.infra.yml)
- Runtime pins: [Restic Compose](../../../infra/09-tooling/restic/docker-compose.yml)
  and the [`mng-pg` image](../../../infra/04-data/operational/mng-db/pg/backup/Dockerfile)
- Rehearsal: `HYHOME_BACKUP_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.BackupRestoreRehearsalTests`

## Related Documents

- [pgBackRest user guide](https://pgbackrest.org/user-guide.html)
- [Restic: preparing a repository](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html)
- [Restic: removing snapshots](https://restic.readthedocs.io/en/stable/060_forget.html)
