---
title: "Backup and Restore Runbook"
version: "1.4.6"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-04"
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
복원하거나, Restic에서 파일을 복원하거나, 오래된 snapshot을 삭제하거나,
R2 오프사이트 사본을 설정하거나 그 사본에서 복원할 때 사용한다. service를 재시작하거나 repository에 쓰거나 snapshot을 삭제하는
모든 단계는 target을 명시한 별도의 approval이 필요하다.

### Execution and stop boundary

대상: `restic`, `restic-offsite`, `backup-sqlite-export`. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../guides/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

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

### 2. Switch `mng-pg` to the pgBackRest image (approval: interrupts shared management-DB access)

전제 조건: owner가 공유 DB interruption, image 호환성, cipher custody와 복구 지점을 승인한다. consumer 자동 재시작을 기대하지 않는다. 최소 20 GiB preflight만으로 dump/scratch 용량을 충족한다고 가정하지 않는다. Logical dump는 기존 파일을 덮어쓰지 않는 새 소유 파일에 만든다. 아래는 승인된 운영 예시이며 W4에서 실행하지 않았다.

```bash
umask 077
dump_file="$(mktemp -p "${DUMP_ROOT:?approved private data-disk directory}" pre-pgbackrest.XXXXXXXX.sql)" || exit 1
test "$(stat -c '%a:%u' "$dump_file")" = "600:$(id -u)" || exit 1
if ! docker exec mng-pg sh -c 'pg_dumpall -U "$POSTGRES_USER"' > "$dump_file"; then
  echo 'dump failed; preserve owned incomplete artifact and stop' >&2
  exit 1
fi
test -s "$dump_file" && test "$(stat -c '%a:%u' "$dump_file")" = "600:$(id -u)" || exit 1
```

실패·빈 결과는 복구 지점이 아니다. SQL 내용은 출력하지 않고 성공 종료·hash·도구/server version만 보호된 evidence에 기록한다.

```bash
docker compose build mng-pg
docker compose up -d --no-deps mng-pg
docker exec -u postgres mng-pg pgbackrest --stanza=mng stanza-create
docker exec -u postgres mng-pg pgbackrest --stanza=mng check
```

기대 결과: `mng-pg`가 healthy이고, `stanza-create`와 `check`가 `completed
successfully`로 끝나며, `SHOW archive_mode`가 `on`을 반환한다.
`stanza-create`가 성공하기 전처럼 일반적인 archive 실패에서는 WAL이
`pg_wal`에 남는다. 그러나
`archive-push-queue-max`를 넘으면 pgBackRest는 disk 고갈을 피하려고 WAL을
폐기하고 archive 성공을 보고할 수 있다. 이 경우 연속 WAL chain이 끊어져
point-in-time recovery에 공백이 생긴다. Queue 한도는 [pgBackRest 설정](../../../infra/04-data/mng-db/pg/backup/pgbackrest.conf)이 소유한다.
WAL drop/queue 초과가 확인되면 해당 chain의 복구 가능성 판정을 중단하고
증거를 보존해 @buenhyden에게 escalation한다. Archive 성공만으로 연속성을
주장하지 않으며 원인 수정 후 새로운 유효 backup과 그 이후의 연속 WAL을
검증하기 전까지 새 PITR 기준점으로 인정하지 않는다.
Rollback은 원래 PG major/extension와 data format 호환성을 확인한 image/config에 한해 별도 승인한다. Git revert가 data downgrade를 수행하지 않는다. repository를 사용할 수 없고 WAL 공간 위험이 있으면 RUN-0035로 전달하며 `archive_mode=off` 변경은 archive 중단과 RPO 손실을 승인받은 경우에만 한다.

### 3. Initialize Restic and install the timer (once)

```bash
docker compose --profile backup run --rm --no-deps restic init
sudo install -m 0644 infra/09-platform-ops/restic/systemd/hyhome-backup.service /etc/systemd/system/
sudo install -m 0644 infra/09-platform-ops/restic/systemd/hyhome-backup.timer /etc/systemd/system/
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

이 절차의 action readiness는 **BLOCKED**다. 실행 전에 @buenhyden이 정확한 source backup label, recovery timestamp/timezone, 연속 WAL 범위, 원래 PostgreSQL major/extension/pgBackRest와 호환되는 보존 image digest, 빈 target과 충분한 data-disk capacity를 정하고 stateful recovery 검토를 받아야 한다. 현재 Compose image를 원래 backup image로 추정하지 않는다. W4에서는 source 문서만 수정했고 runtime은 NOT_RUN이다.

승인된 구현의 순서는 다음과 같다. 이는 아직 소유 target이 지정되지 않은 실행 명령이 아니다.

1. data disk의 승인된 `SCRATCH_ROOT`에서 `mktemp -d -p`로 새 target을 만들고 소유 UID/mode/device/inode를 보존한다. 기존 경로·container·network 이름 충돌은 중단한다. recovery copy에는 UID70만 쓰게 하고 원본 repository는 read-only로 연결한다.
2. 첫 pgBackRest restore container는 `--network none`으로 실행한다. custom image의 기본 secret-aware entrypoint를 유지하고 **command**로 `sh -ec`를 전달한다. `--entrypoint sh`로 우회하거나 cipher include를 직접 생성하지 않는다. `/run/secrets/pgbackrest_cipher_pass`를 read-only로 연결하면 wrapper가 `/tmp/pgbackrest/conf.d`의0600 include를 준비한다.
3. `gosu postgres pgbackrest`의 `--stanza=mng`, 검토된 `--set=<backup-label>`, `--type=time`, `--target=<approved-time>`, `--target-action=promote`, `--archive-mode=off`를 사용한다. 정확한2.58 옵션과 repository/WAL 가용성을 먼저 검토한다. command 실패·chain 누락·version 불일치면 재시도/승격하지 않는다.
4. 복원본 server 검증에만 새 이름의 `--internal` network를 사용한다. 원본 네트워크/host port와 연결하지 않는다. 같은 보존 image/entrypoint/cipher와 read-only repository, `PGDATA=/var/lib/postgresql/data/pgdata`를 사용하고 `postgres -c archive_mode=off`로 archive 재유입을 막는다.
5. 로그의 target 도달/timeline, recovery 완료, role/extension/schema/sequence와 승인된 application invariants를 비교한다. 단순 시작이나 `selected new timeline`만으로 시점 정합성을 인정하지 않는다. dump·row·credential은 evidence에 출력하지 않는다.
6. 실패 시 target을 중지하고 scratch/evidence를 보존한다. cleanup은 기록한 identity와 label을 재검증한 **정확한 소유 artifact만** 별도 승인 후 삭제한다. source·backup은 보존한다. live cutover는 별도 승인된 절차다.

기존 synthetic test의 network/entrypoint 예시는 이 강화된 계약의 충족 증거가 아니다. source test 수정과 새 격리 검증은 별도 구현 작업이다.

#### 5a. Selected-backup immediate consistency rehearsal

SPEC-0201-TSK-0002의 제안 경로는 step 5의 time-target PITR와 별개다. 실행은 별도 소유자 승인 전 **BLOCKED**이고, 백업 종료 뒤의 WAL 시점·5분 RPO·관리 앱 복구를 증명하지 않는다. 승인된 현재 backup set에 대해 `pgbackrest verify --set=<label>`가 exit 0인 후에만 같은 set을 `--type=immediate --target-action=promote --archive-mode=off`로 새 격리 target에 복원한다. 원본 repository와 BKP-001 secret은 기존 bind를 read-only로 소비한다. backup scheduler의 host lock, 정확한 scratch identity, image/PG major/pgBackRest 호환성, Docker context, 자원·시간 상한, 실패 보존을 먼저 검토한다.

Clone은 `--network none`, host port 없음, 원본 PGDATA와 분리된 scratch만 사용하고 archive를 끈다. 선택 set의 DB 목록과 원본 cluster system ID는 clone과 정확히 같아야 하며 `app_db`, `mlflow`, 추적된 heartbeat·dbt 객체는 존재해야 한다. 복구된 local socket 관리 연결은 `docker exec --user 70`과 복원된 관리자 role을 사용하고 실패하면 중단한다. Clone 안에 직접 grant와 membership이 `CONNECT,TEMP`뿐인 일회성 LOGIN을 만들고, `app_db`·`public` schema·시험 객체의 유효 `PUBLIC` 권한이 영속 객체 변경을 허용하면 중단한다. 내부 loopback `127.0.0.1:5432` TCP로 실제 인증한다. 이 role은 `app_db`의 임시 테이블 생성·합성 행 insert·count 1·rollback을 확인한 뒤 임시 객체와 LOGIN 모두 부재를 확인한다. 비밀번호 평문은 프로세스 밖에 보존하지 않는다. 실제 행·비밀값·원문 로그는 증거에 남기지 않는다. 지정된 관리 테이블 count는 동일 snapshot에서 두 번 동일한 비음수 값을 반환해야 하며 원본의 다른 시점 count와 같다고 가정하지 않는다. Extension과 sequence inventory는 관측값으로 기록하고 backup 시점 비교 자료가 없으면 같음을 주장하지 않는다. Clone이 일관성 상태에 도달하면 host lock을 해제하고, 성공과 실패 모두 정확히 소유한 임시 container 이름과 생성 ID를 대조해 멈추고 제거한다. 실패 경로에서는 아직 보유한 lock도 해제한다. scratch PGDATA는 mode 0700으로 보존하고 증거 수집 시점부터 7일 안에 @buenhyden이 검토한다. 기한을 넘기면 owner에게 상향 보고하며 삭제는 별도 identity·owner 승인이 필요하다. HOME cutover·서비스 중단·time-target PITR는 이 분기의 범위 밖이다.

### 6. Restore files from Restic

승인 전 정확한 Restic snapshot ID, host/tag/time/source revision, 암호 키 custody, include 경로와 대상 owner를 선택한다. `latest`를 자동 선택하지 않는다. state와 host는 같은 성공 실행에 속하는 snapshot pair인지 확인한다. 일반 restore container는 data-disk의 새 소유 scratch, local repository read-only, `--network none`을 사용한다. hardened backup job은 ownership 재적용 권한이 없으므로 restore 도구와 UID/mode 복원 계약을 별도로 검토한다.

Restic0.19.1의 `restore <reviewed-snapshot-id> --target <owned-scratch>`로 승인된 include만 추출한다. state export는 `/src/state/exports`, host repository의 `.env`·secret은 `/src/host` 아래다. hash·mode·UID와 원래 application recovery point를 확인하고 검토된 파일만 별도 승인으로 복사한다. scratch도 secret artifact이며0600 파일과 제한된 디렉터리 권한을 유지한다.

SeaweedFS는 같은 state snapshot의 `/src/state/volumes/data/seaweedfs`와 `/src/state/exports/seaweedfs-filer.meta`를 함께 복원한다. [RUN-0024](0024-seaweedfs.md)의 빈 filer store, volume/master tree, `fs.meta.load` 계약을 따른다. restore 실패·identity 충돌·include 부재는 중단하며 자동 cleanup하지 않는다.

### 7. Delete old snapshots (approval: irreversible)

```bash
docker compose --profile backup run --rm --no-deps \
  -e HYHOME_PRUNE_CONFIRM=delete-old-snapshots restic forget-prune
```

세트당 daily 30개, weekly 13개, monthly 12개의 snapshot을 유지한다.
pgBackRest는 자체 backup을 `repo1-retention-full=2`로 만료시킨다.

### 8. Offsite copy (R2)

`restic-offsite`는 로컬 Restic repository 두 개의 snapshot을 Cloudflare R2의
Restic repository 하나로 복사한다(ADR-0041). state set에 `pgbackrest/`가
들어 있으므로 PostgreSQL도 이 경로로 오프사이트에 가며 원격 RPO는 하루다.
pgBackRest의 S3 repository는 따로 두지 않는다. state set은 이제
`forget-prune` 전까지 본 모든 pgBackRest 파일을 담고 이 크기는
`BACKUP_STATE_MAX_GIB`에 포함되므로, 로그의 크기를 지켜본다.

#### 8.1 Owner 1회 설정 (approval: 새 credential과 첫 업로드)

Cloudflare dashboard에서:

1. **R2 → Create bucket**: 이름은 예를 들어 `hyhome-restic`, location은
   automatic, storage class는 Standard로 한다(Infrequent Access는 최소 보관
   기간과 읽기에 요금을 매긴다).
2. **Bucket → Settings → Bucket lock rules → Add rule**: 보관 기간 30일의
   규칙을 prefix `data/`, `snapshots/`, `keys/`, `config`에 하나씩 만든다.
   `locks/`에는 걸지 않는다. Restic이 자기 lock 파일을 지워야 한다. `index/`에도
   걸지 않는다. 8.5의 `prune`은 옛 index 파일을 지우고 새로 쓰는데, 지우지 못한
   index가 이미 지운 pack을 가리키면 이후 copy가 그 데이터를 올리지 않고 건너뛸 수
   있다. index를 잃어도 `restic repair index`가 pack에서 다시 만든다.
3. **R2 → Manage API tokens → Create Account API token**: 사람 계정에 묶인 User
   API token은 그 사용자가 계정에서 빠지면 멈추므로, 계정에 묶인 Account API
   token을 쓴다. 권한은 **Object Read & Write**, 적용 대상은 그 bucket 하나,
   Admin 권한은 주지 않는다. 이 token은
   bucket을 관리하거나 지우지 못하고, bucket lock은 잠긴 object의 삭제를
   거부한다. Access Key ID와 Secret Access Key(한 번만 표시된다), S3 endpoint
   `https://<account-id>.r2.cloudflarestorage.com`의 account ID를 적어 둔다.

host의 repository root에서, 값을 출력하지 않고:

```bash
umask 077
bash scripts/operations/gen-secrets.sh --sync-metadata   # .env에 BACKUP_OFFSITE_R2_* 키 추가
bash scripts/operations/gen-secrets.sh                   # BKP-003 restic_offsite_password.txt 생성
IFS= read -rs r2 && printf '%s' "$r2" > secrets/backup/restic/r2_access_key_id.txt; unset r2       # BKP-004
IFS= read -rs r2 && printf '%s' "$r2" > secrets/backup/restic/r2_secret_access_key.txt; unset r2   # BKP-005
```

`.env`에 `BACKUP_OFFSITE_R2_ACCOUNT_ID`(16진수 32자)와
`BACKUP_OFFSITE_R2_BUCKET`을 넣는다. BKP-003, BKP-004, BKP-005, account ID,
bucket 이름을 BKP-001/BKP-002 옆의 offline custody에 복사한다. host를 잃은
뒤의 복구가 OpenBao에 기대면 안 되므로 OpenBao에는 절대 두지 않는다. 그다음
state repository의 chunker 설정으로 원격을 초기화하고 첫 copy를 한다:

```bash
docker compose --profile backup run --rm --no-deps restic-offsite init
docker compose --profile backup run --rm --no-deps restic-offsite copy
docker compose --profile backup run --rm --no-deps restic-offsite check
```

`init`은 이미 초기화된 repository를 건너뛴다. Rollback: `.env`의 두 키를
비우면 매일의 run이 오프사이트 단계를 건너뛴다.

#### 8.2 매일의 동작

`.env` 키 중 하나라도 비어 있으면 orchestrator는 `offsite copy not
configured (BACKUP_OFFSITE_R2_*); skipped`를 남기고 unit 결과는 바뀌지 않는다.
설정되면 로컬 Restic backup과 check가 성공한 뒤(staging을 비우고 SeaweedFS
vacuum을 재개한 다음) `restic-offsite copy`를 실행한다. 원격에 없는 snapshot만
올리고 `R2 latest snapshots:` 아래에 set마다 한 줄을, `R2 repository size:`에
저장된 byte 수를 남긴다. orchestrator는 이 값을 성공 timestamp와 같은 파일에
`hyhome_backup_offsite_repo_bytes`로 쓴다. 일요일에는 원격에
`restic check --read-data-subset 10%`도 실행한다. copy나 check가 실패하면
`offsite copy to R2 failed` 또는 `offsite check of R2 failed`를 남기고 다른 단계의
실패처럼 unit이 exit 1로 끝난다. 로컬 snapshot의 전체 export 포함 여부는 별도 확인한다. 로컬 Restic backup/check가 실패하면 `offsite copy skipped`다. 그러나 앞선 pgBackRest/globals/Valkey/SQLite/SeaweedFS 실패는 `restic_ok`를 내리지 않아 partial snapshot과 원격 copy가 진행될 수 있다. 이는 전체 복구 세트 성공이 아니며 unit exit1과 성공 timestamp 부재를 유지한다. 원격이
초기화되지 않았거나 닿지 않으면 exit 65다. 오프사이트까지 성공한 run만
step 4의 성공 timestamp를 쓴다.

#### 8.3 R2에서 복원

host를 잃은 뒤에는 Docker·보존 source revision과 image identity, BKP-001~005 offline custody, account/bucket 외에 root Compose 렌더링에 필요한 non-secret inputs 및 명시적 directory/mount 준비가 필요하다. `.env` 두 키만으로 root Compose bootstrap이 된다고 가정하지 않는다. 복원한 private 설정은 출력하지 않는다.

승인된 새 data-disk scratch에 먼저 원격 snapshot 목록의 metadata만 조사한다. 원격 snapshot ID는 local과 다르므로 host/tag/time과 전체 성공 실행 기록으로 host/state pair를 고정한다. 원격 접근에 필요한 전용 network와 R2 credential을 최소 범위로 제공하고, 기본 bridge·전체 secret 디렉터리 공유를 암묵적으로 사용하지 않는다.

`restic restore <host-id> --tag hyhome-host --target <owned-host-scratch>`와 `restic restore <state-id> --tag hyhome-state --target <owned-state-scratch>`의 정확한 ID를 검토한 후 실행한다. `latest`와 기본 `/tmp`는 사용하지 않는다. host의 `/src/host`에서 설정/custody를 복원하고 state의 `/src/state/pgbackrest`는 별도 승인된 repository 경로에 owner70:70/mode0750로 준비한다. 실제 database 복원은 step5의 backup label/WAL target 계약을 따른다. 원격 copy가 담은 마지막 WAL 이후의 복구는 보장되지 않는다.

로컬 repository를 다시 만드는 경우에도 빈 target과 원격 snapshot scope를 검토한다. `restic init --copy-chunker-params --from-repo` 후 승인된 ID를 `copy`하며, 기존 repository를 덮어쓰거나 전체 tag를 무조건 복사하지 않는다. encrypted snapshot 존재만으로 key custody와 application restore가 검증되지는 않는다. 실패 artifact는 보존하고 cleanup/cutover는 별도 승인한다.

#### 8.4 Verification

- `journalctl -u hyhome-backup.service`에 오늘 날짜의 state 줄과 host 줄이 있는
  `R2 latest snapshots:`가 보이고 unit이 exit 0으로 끝났다.
- `docker compose --profile backup run --rm --no-deps restic-offsite snapshots`가
  두 set을 모두 나열한다. 일요일 run에는 원격의 `no errors were found`가 있다.
- dashboard에 bucket lock rule 네 개(`data/`, `snapshots/`, `keys/`, `config`)와
  token의 단일 bucket 범위가 보인다.
- 오프사이트 복구를 검증했다고 말하기 전에, R2에서 scratch 디렉터리로의 복원
  리허설(8.3)을 소요 시간과 함께 기록한다.
- 원격 snapshot 삭제는 8.5의 확인 절차로만 한다. 매일의 run은 지우지 않는다.

#### 8.5 원격 forget-prune (owner-run, approval: 원격 삭제)

R2에는 로컬의 `forget-prune`이 닿지 않으므로, 이 단계 없이는 올린 것이 계속
쌓인다. 로컬 state 디렉터리는 2026-09-23 429 MiB에서 2026-09-30 1679 MiB로
하루 약 180 MiB 늘었다. 원격도 비슷하게 늘면 1.5~2개월이면 무료 한도
10 GB를 넘는다. 한 달에 한 번, 또는 `HyhomeOffsiteRepoNearFreeTier`가 뜨면
실행한다:

```bash
docker compose --profile backup run --rm --no-deps \
  -e HYHOME_PRUNE_CONFIRM=delete-old-remote-snapshots restic-offsite forget-prune
```

최근 30일의 snapshot은 모두 두고, 그보다 오래된 것은 한 달에 하나씩 12개월치만
남긴다(`--keep-within 30d --keep-monthly 12`, host와 tag별). 이는 snapshot timestamp 기준이며 object 생성 시각·R2 lock 만료와 같지 않다. remote prune/lock 조합은 현재 미검증이다. 삭제/repack이 잠금에 거부되면 중단하고 owner에게 전달하며 다음 달 자동 해소나 index 안전을 가정하지 않는다. 잠금을 약화하거나 object 일부를 직접 삭제하지 않는다. 성공 후에도 `restic-offsite check`로 `no errors were found`를 확인한다.
Evidence에는 실행 시각, 지운 snapshot 수, 전후 `R2 repository size`를 적는다.

#### 8.6 R2 비용과 무료 한도 검토

2026-09-30 확인한 [R2 pricing](https://developers.cloudflare.com/r2/pricing/)
기준: 무료 한도는 계정 단위로 Standard storage 10 GB-month, Class A 100만,
Class B 1000만 건이다. storage는 날마다의 최대값을 한 달 평균한 값으로 매긴다.
Infrequent Access에는 무료 한도가 없다. `DeleteObject`와
`AbortMultipartUpload`는 무료다.

| 항목 | 예상 사용량 | 관리 |
| --- | --- | --- |
| Storage | 첫 copy 약 1.8 GB, 이후 하루 약 180 MiB | 8.5를 매달 실행; 8 GB에서 `HyhomeOffsiteRepoNearFreeTier` |
| Class A (PutObject, ListObjects 등) | 하루 copy 한 번에 pack, index, snapshot, lock 업로드와 list 수십 건, 한 달 수천 건 | 실측 operation과 계정 전체 사용량 검토 |
| Class B (GetObject, HeadObject 등) | copy의 index 읽기, 일요일 check의 10% pack 읽기, 한 달 수천 건 | 실측 operation과 계정 전체 사용량 검토 |

Cloudflare에는 사용을 멈추는 지출 상한이 없다. 대신 다음을 지킨다:

1. bucket의 storage class는 Standard로 두고, Infrequent Access로 옮기는
   lifecycle rule을 만들지 않는다.
2. object를 나이로 지우는 lifecycle rule을 만들지 않는다. Restic repository의
   일부만 지우면 repository가 깨진다. 새 bucket에 기본으로 있는 "multipart
   upload 7일 뒤 중단" 규칙은 그대로 둔다.
3. **Manage Account → Billing → Billable Usage → Create budget alert**에서
   허용되는 가장 낮은 금액(예: 1 USD)으로 budget alert를 만든다. 이 알림은 계정
   전체의 사용량 기반 요금이 그 금액을 넘으면 email을 한 번 보낼 뿐, 사용을
   멈추지 않는다. Pay-as-you-go 계정에서만 쓸 수 있다.
4. 한 달에 한 번 bucket의 **Metrics** 탭에서 storage와 operation 수를 보고, 8.5의
   Evidence 옆에 적는다.

### 개발 PostgreSQL 편입 및 복구 전제

1. 승인된 Docker context/프로젝트·정확한 image ID·새 PGDATA·별도
   `${BACKUP_STATE_REPO_DIR}/dev-pgbackrest` identity와 용량을 확인합니다.
   source bind의 `create_host_path: false` 때문에 디렉터리를 미리 승인된 범위로
   준비해야 하며, 관리 repository를 개발 경로에 다시 연결하지 않습니다.
2. `dev_pgbackrest_cipher_pass`의 읽기 전용 secret mount와 보관 책임자를
   확인합니다. 운영 stanza-create/check·최초 full backup·WAL 활성화·retention·
   재시작·예약 백업은 각각 구체적 승인 후 수행합니다. 현재 archive_mode=off
   상태에서 online check 실패를 우회하거나 synthetic offline 결과로 대체하지 않습니다.
3. 기존 scheduler는 개발 check 후 backup, globals/schema export와 image/infra
   revision metadata를 생성합니다. globals는 자격 증명 hash를 포함할 수 있으므로
   출력하지 않으며 기존0700 staging·종료 cleanup과 encrypted Restic에만 둡니다.
   첫 differential은 기존 full이 필요하므로 최초 full 준비 없이 일정을 켜지 않습니다.
4. 복구 대상 backup label과 WAL 범위를 고정하고 별도 project/volume·network none,
   정확히 호환되는 개발 이미지 및 `dev_pgbackrest_cipher_pass` read-only mount를
   검토합니다. dev entrypoint의 기본 credential 소비 경로를 유지하며 명령은
   `pgbackrest --stanza=dev --set=<approved-label> restore` 형태로 승인된 빈 target에만
   실행합니다. `latest`, management stanza, 기존 PGDATA 재사용은 금지합니다.
   archive_mode가 승인되어 연속 WAL을 검증하기 전에는 PITR를 주장하지 않습니다.
5. physical catalog의 extension version과 migration 이력, 별도 globals/schema,
   외부 앱 migration source revision을 대조하고 runtime/reader 권한 거절·업무
   기능을 검증합니다. 성공 label/WAL 범위·image·시간·종료 코드만 기록합니다.
   rollback은 source revert와 운영 중단/cutover 승인을 구분하며 실패 scratch와
   원본 repository는 보존합니다. cleanup·데이터 삭제는 별도 승인입니다.

이 절차의 HOME 실행·offsite/운영 실복구는 NOT_RUN입니다. 합성 scheduler shim은
분기와 실패 전달만 검증합니다. 별도로 2026-10-04 새 합성 DB를 정지해 offline
full backup하고 현재 Restic state chain으로 snapshot/복원한 repository에서
선택 label을 새 빈 볼륨에 복구했습니다. row·extension·migration·role 비교와
reader 읽기 허용/쓰기·DDL 거절이 통과했으며 missing source exit3·unknown label
exit75도 거절했습니다. 이 결과는 WAL/PITR·HOME·R2 복구나 RPO/RTO가 아닙니다.

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
잃어버렸을 때 @buenhyden에게 escalation한다.

## Traceability

- Guide: [GDE-0021](../guides/0021-backup-and-restore.md); Policy: [POL-0021](../policies/0021-backup-and-restore.md)
- Alerts: [host backup rules](../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.infra.yml)
- Runtime pins: [Restic Compose](../../../infra/09-platform-ops/restic/docker-compose.yml)
  and the [`mng-pg` image](../../../infra/04-data/mng-db/pg/backup/Dockerfile)
- Rehearsal: `HYHOME_BACKUP_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.BackupRestoreRehearsalTests`

소스 경로를 `09-platform-ops`로 이전해도 호스트에 복사해 설치한
`hyhome-backup.service`는 예전 ExecStart 경로를 유지할 수 있습니다. 운영 배포 시
다음 예약 백업에 의존하기 전에 소유자가 기존 설치 절차에 따라 정확한 unit을
갱신하고 daemon-reload 적용을 확인해야 합니다. timer 이름·일정과 사용자·그룹은
그대로 유지하며, 활성화·catch-up 실행·수동 백업은 별도 승인 대상입니다.
이 저장소 변경은 설치된 unit 갱신이나 실제 백업 성공을 뜻하지 않습니다.

## Related Documents

- [pgBackRest user guide](https://pgbackrest.org/user-guide.html)
- [Restic: preparing a repository](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html)
- [Restic: removing snapshots](https://restic.readthedocs.io/en/stable/060_forget.html)
