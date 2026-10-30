---
title: "Backup and Restore Runbook"
version: "1.4.28"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-30"
layer: "operations"
artifact_id: "RUN-0021"
parent_ids:
- "GDE-0021"
created: "2026-09-22"
---

# Backup and Restore Runbook

## Overview

pgBackRest, Restic, SQLite export, R2 오프사이트 사본과 공유 에이전트 memory 저장소의 설정·실행·검증·복구 절차를 다룬다. 정책은 [POL-0021](../../policies/10-platform-and-backup/0021-backup-and-restore.md), 설명은 [GDE-0021](../../guides/10-platform-and-backup/0021-backup-and-restore.md)이 소유한다.

## Trigger

backup repository를 준비하거나, `mng-pg`를 pgBackRest image로 전환하거나,
backup을 실행/검증하거나, PostgreSQL을 isolation 환경에서 특정 시점으로
복원하거나, Restic에서 파일을 복원하거나, 오래된 snapshot을 삭제하거나,
R2 오프사이트 사본을 설정하거나 그 사본에서 복원하거나, 공유 에이전트 memory 저장소를
backup·restore할 때 사용한다.

## Prerequisites

### Trigger and Preconditions

service를 재시작하거나 repository에 쓰거나 snapshot을 삭제하는
모든 단계는 target을 명시한 별도의 approval이 필요하다.

### Execution and stop boundary

대상: `restic`, `restic-offsite`, `backup-sqlite-export`. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../../guides/01-common/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../../policies/01-common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

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
point-in-time recovery에 공백이 생긴다. Queue 한도는 [pgBackRest 설정](../../../../infra/04-data/mng-db/pg/backup/pgbackrest.conf)이 소유한다.
Drop은 `pg_stat_archiver.failed_count`에 나타나지 않는다. 확인 신호는 pgBackRest가
PostgreSQL log(Loki로 수집)에 남기는 queue 초과 WARN과 `pgbackrest info`의 WAL
범위 공백이다.
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
"over the 8 GiB budget; Restic backup skipped"를 로그에 남기는 run은 exit 1로
끝난다. 이때 pgBackRest는 완료되고 Restic은 건드리지 않는다. 기록된 크기를 검토하고
승인된 `forget-prune`(step 7) 또는 더 큰 budget을 요청한다. unit은 4시간 후
정지하는데 그래도 staging은 비워진다. 실행 중인 Restic 프로세스가 없을 때
`restic unlock`으로 stale Restic lock을 해제한다.

`mng-valkey` RDB 내보내기는 컨테이너 안에서 300초 제한으로 실행한다. 제한을
넘기거나 실패하면 "mng-valkey RDB export failed or timed out; export dropped"를
남기고 불완전한 파일을 지운 뒤 나머지 단계와 Restic을 계속 진행하며, run은
exit 1로 끝난다.

`dev-valkey`도 같은 방식으로 `devadmin` ACL 사용자가 300초 제한 안에서 RDB를
내보낸다. DEV가 꺼져 있으면 건너뛰고, 실패하면 "dev-valkey RDB export failed or
timed out; export dropped"를 남긴 뒤 run을 exit 1로 끝낸다. RDB는 내보낸 시점의
일관된 snapshot이므로 그 뒤에 들어온 queue 항목은 잃는다.

Valkey 복구는 별도 project의 새 container에서 먼저 시험한다. Restic에서 꺼낸
RDB를 빈 data 디렉터리에 `dump.rdb`로 두고 `--save ''`, `--appendonly no`로
기동한 뒤 key 수와 stream 길이를 확인한다. 소비자 group의 미확인(pending)
항목은 RDB에 남으므로, 새 소비자가 `XAUTOCLAIM`으로 넘겨받아 다시 처리한다.
따라서 복구된 queue는 최소 한 번(at-least-once) 재처리되며 소비자는 멱등이어야
한다. 2026-10-08 합성 데이터로 시험했을 때 key, stream 2건, pending 1건이 그대로
돌아왔고 `XAUTOCLAIM`이 pending 항목을 넘겨받았다. HOME 복구는 별도 승인이다.

Open WebUI는 세 부분을 함께 복구해야 한다. `webui.db`는 SQLite online backup
export로, `uploads/`와 `.webui_secret_key`는 state 허용 목록으로 백업한다. 이 key가
없으면 기존 session과 key로 암호화된 값을 쓸 수 없다. 이전에는 key가 container
layer에 생성돼 재생성마다 바뀌었다. 이제 `WEBUI_SECRET_KEY_FILE`이 data volume을
가리킨다. SPEC-0226 적용 때 실행 중이던 key를 먼저 volume에 복사했으므로 key는
바뀌지 않았고 재로그인도 필요 없었다. 그 뒤로도 재생성 때 유지된다.

OpenBao는 Raft snapshot으로 백업합니다. 최초 snapshot-only periodic token 발급은
[RUN-0105 Maintenance Window Plan의 W1·W2](../04-security-and-secrets/0105-openbao-maintenance-window.md#maintenance-window-plan)가
소유합니다. 독립 검토된 helper가 실제 root identity, 고정 gateway CA·cluster,
정확한 정책과 ordinary-secret denial·renewal을 확인하며, 기존 token을 덮지 않고
`secrets/backup/openbao/snapshot_token.txt`에 0600 single-link로 전달합니다.
정책은 snapshot read와 자기 lookup·renew·revoke만 허용하고 default policy를 붙이지
않습니다. root와 발급 응답은 보호된 custody 밖으로 출력하지 않습니다.

이전 inline 발급 블록은 정책을 무조건 덮고 실패 뒤 발급 identity를 남기며 대상 파일을
강제로 교체할 수 있어 제거했습니다. 파일 삭제는 서버 credential 폐기가 아닙니다.
현재 token·issuance lock이 있거나 결과가 불확실하면 보존하고 실제 identity부터
확인합니다. 재발급과 원래 token 폐기는 같은 작업으로 취급하지 않습니다.

매 run은 token을 stdin으로 넘겨 갱신한 뒤 snapshot을 staging에 받는다. token
파일이 없으면 "OpenBao snapshot token absent: snapshot failed (recovery gap)"을
남기고 이 백업 단위를 실패 처리한다(`status=1`). 시작할 때 이전 staging
snapshot을 제거하므로 오래된 파일을 이번 성공으로 사용할 수 없다. sealed,
잘못된 token, 300초 초과나 빈 snapshot도 실패 처리하며 불완전한 snapshot을
제거한다. 다른 백업 단계는 계속될 수 있지만 최종 실행은 exit 1이며 전체
복구 지점으로 수용하지 않는다. run이 30일 넘게 멈추면 token이 만료되므로 다시 만든다.

snapshot은 barrier 암호화된 상태라 원래 unseal key 없이는 열 수 없다. 따라서
unseal key가 필요하다. 1인 관리자 결정(SPEC-0242)으로 share는 host와 host 백업에 함께 있다. 복구는 새로 초기화한 OpenBao에서
`bao operator raft snapshot restore -force`로 하고, 복구 직후 sealed가 되면 원래
unseal key로 연다. 2026-10-08 격리 시험에서 이 순서로 합성 secret과 원래 root
token이 돌아왔다. HOME 복구는 별도 승인이다.

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
3. `gosu postgres pgbackrest`의 `--stanza=mng`, 검토된 `--set=<backup-label>`, `--type=time`, `--target=<approved-time>`, `--target-action=promote`, `--archive-mode=off`를 사용한다. 정확한 pgBackRest 옵션과 repository/WAL 가용성을 먼저 검토한다. command 실패·chain 누락·version 불일치면 재시도/승격하지 않는다.
4. 복원본 server 검증에만 새 이름의 `--internal` network를 사용한다. 원본 네트워크/host port와 연결하지 않는다. 같은 보존 image/entrypoint/cipher와 read-only repository, `PGDATA=/var/lib/postgresql/data/pgdata`를 사용하고 `postgres -c archive_mode=off`로 archive 재유입을 막는다.
5. 로그의 target 도달/timeline, recovery 완료, role/extension/schema/sequence와 승인된 application invariants를 비교한다. 단순 시작이나 `selected new timeline`만으로 시점 정합성을 인정하지 않는다. dump·row·credential은 evidence에 출력하지 않는다.
6. 실패 시 target을 중지하고 scratch/evidence를 보존한다. cleanup은 기록한 identity와 label을 재검증한 **정확한 소유 artifact만** 별도 승인 후 삭제한다. source·backup은 보존한다. live cutover는 별도 승인된 절차다.

기존 synthetic test의 network/entrypoint 예시는 이 강화된 계약의 충족 증거가 아니다. source test 수정과 새 격리 검증은 별도 구현 작업이다.

#### 5a. Selected-backup immediate consistency rehearsal

SPEC-0201-TSK-0002의 제안 경로는 step 5의 time-target PITR와 별개다. 실행은 별도 소유자 승인 전 **BLOCKED**이고, 백업 종료 뒤의 WAL 시점·5분 RPO·관리 앱 복구를 증명하지 않는다. 승인된 현재 backup set에 대해 `pgbackrest verify --set=<label>`가 exit 0인 후에만 같은 set을 `--type=immediate --target-action=promote --archive-mode=off`로 새 격리 target에 복원한다. 원본 repository와 BKP-001 secret은 기존 bind를 read-only로 소비한다. backup scheduler의 host lock, 정확한 scratch identity, image/PG major/pgBackRest 호환성, Docker context, 자원·시간 상한, 실패 보존을 먼저 검토한다.

Clone은 `--network none`, host port 없음, 원본 PGDATA와 분리된 scratch만 사용하고 archive를 끈다. 선택 set의 DB 목록과 원본 cluster system ID는 clone과 정확히 같아야 하며 `app_db`, `mlflow`, 추적된 heartbeat·dbt 객체는 존재해야 한다. 복구된 local socket 관리 연결은 `docker exec --user 70`과 복원된 관리자 role을 사용하고 실패하면 중단한다. Clone 안에 직접 grant와 membership이 `CONNECT,TEMP`뿐인 일회성 LOGIN을 만들고, `app_db`·`public` schema·시험 객체의 유효 `PUBLIC` 권한이 영속 객체 변경을 허용하면 중단한다. 내부 loopback `127.0.0.1:5432` TCP로 실제 인증한다. 이 role은 `app_db`의 임시 테이블 생성·합성 행 insert·count 1·rollback을 확인한 뒤 임시 객체와 LOGIN 모두 부재를 확인한다. 비밀번호 평문은 프로세스 밖에 보존하지 않는다. 실제 행·비밀값·원문 로그는 증거에 남기지 않는다. 지정된 관리 테이블 count는 동일 snapshot에서 두 번 동일한 비음수 값을 반환해야 하며 원본의 다른 시점 count와 같다고 가정하지 않는다. Extension과 sequence inventory는 관측값으로 기록하고 backup 시점 비교 자료가 없으면 같음을 주장하지 않는다. Clone이 일관성 상태에 도달하면 host lock을 해제하고, 성공과 실패 모두 정확히 소유한 임시 container 이름과 생성 ID를 대조해 멈추고 제거한다. 실패 경로에서는 아직 보유한 lock도 해제한다. scratch PGDATA는 mode 0700으로 보존하고 증거 수집 시점부터 7일 안에 @buenhyden이 검토한다. 기한을 넘기면 owner에게 상향 보고하며 삭제는 별도 identity·owner 승인이 필요하다. HOME cutover·서비스 중단·time-target PITR는 이 분기의 범위 밖이다.

소유자 실행 script는 `scripts/operations/mng-pg-immediate-restore-rehearsal.py`다. 2026-10-30 현재 독립 stateful recovery 검토는 대기 중이고 실행은 **NOT_RUN**이다. 검토 승인과 별도 실행 승인 전에는 실행하지 않는다. script는 Docker 외 도구를 쓰지 않고 `.env`와 `secrets/`를 읽지 않는다. `mng-pg` container의 `docker inspect`에서 image ID, repository bind, cipher secret bind, 관리자 role 이름을 읽는다.

```bash
SCRATCH_ROOT=<승인된 data-disk scratch 경로>   # /tmp 아님, 비어 있고 소유자 소유, mode 0700
install -d -m 0700 "$SCRATCH_ROOT/mng-pg-5a-20261030"
python3 scripts/operations/mng-pg-immediate-restore-rehearsal.py \
  --label 20261024-184214F_20261029-221825D \
  --scratch-root "$SCRATCH_ROOT/mng-pg-5a-20261030" \
  --heartbeat app_db.debezium_heartbeat.heartbeat \
  --dbt app_db.analytics.hyhome_dbt_connectivity \
  --count-table mlflow.public.experiments
```

`--heartbeat`와 `--dbt`는 `DB.SCHEMA` 또는 `DB.SCHEMA.RELATION`, `--count-table`은 반복 가능한 `DB.SCHEMA.TABLE`이다. 위 값은 2026-10-30 `mng-pg`에서 읽기 전용 catalog 조회로 확인한 실제 객체다(`app_db`의 `debezium_heartbeat.heartbeat` table과 `analytics.hyhome_dbt_connectivity` view, `mlflow`의 `public.experiments`). 실행 전에 다시 바뀌었는지 확인한다. 없는 객체는 FAIL이다. script는 `latest`, 형식이 다른 label, `/tmp`·`/var/tmp`·`/dev/shm`, 비어 있지 않거나 소유자 소유가 아닌 target, symlink 경로를 실행 전에 거부한다(exit 2). backup scheduler lock(`$BACKUP_STATE_REPO_DIR/.hyhome-backup.lock`)이 사용 중이면 exit 75다.

기대 출력은 아래 고정 필드뿐이다. 행, 비밀값, 원문 log는 없다. `extension_count`와 `sequence_count`는 관측값이며 이름 목록은 scratch root의 `inventory-observations.json`(0600)에만 있고 원본과 같다고 주장하지 않는다. `elapsed_seconds`는 실행마다 다르다.

```text
result=PASS
reason=none
verify_rc=0
restore_rc=0
elapsed_seconds=<number>
system_id_match=true
db_list_match=true
app_db_present=true
mlflow_present=true
heartbeat_present=true
dbt_present=true
count_stable=true
extension_count=<number>
sequence_count=<number>
probe_result=PASS
scratch_mode_0700=true
cleanup_status=removed
```

`result=FAIL`이면 `reason`이 멈춘 단계(`verify`, `restore`, `identity_mismatch`, `required_object_missing`, `count_unstable`, `probe_privileges`, `probe_auth_not_enforced`, `probe_session`, `probe_cleanup` 등)를 말하고 이후 필드는 `NOT_RUN`이다. `cleanup_status`가 `removed`나 `none_created`가 아니면 이름과 ID가 맞지 않은 container를 건드리지 않았다는 뜻이므로 소유자가 직접 확인한다. 통과해도 scratch PGDATA(UID 70 소유, mode 0700)는 남고 증거 수집 시점부터 7일 안에 @buenhyden가 검토한다. 삭제는 별도 identity·owner 승인이다.

### 6. Restore files from Restic

승인 전 정확한 Restic snapshot ID, host/tag/time/source revision, 암호 키 custody, include 경로와 대상 owner를 선택한다. `latest`를 자동 선택하지 않는다. state와 host는 같은 성공 실행에 속하는 snapshot pair인지 확인한다. 일반 restore container는 data-disk의 새 소유 scratch, local repository read-only, `--network none`을 사용한다. hardened backup job은 ownership 재적용 권한이 없으므로 restore 도구와 UID/mode 복원 계약을 별도로 검토한다.

Restic의 `restore <reviewed-snapshot-id> --target <owned-scratch>`로 승인된 include만 추출한다. state export는 `/src/state/exports`, host repository의 `.env`·secret은 `/src/host` 아래다. hash·mode·UID와 원래 application recovery point를 확인하고 검토된 파일만 별도 승인으로 복사한다. scratch도 secret artifact이며0600 파일과 제한된 디렉터리 권한을 유지한다.

SeaweedFS는 같은 state snapshot의 `/src/state/volumes/data/seaweedfs`와 `/src/state/exports/seaweedfs-filer.meta`를 함께 복원한다. `loki-bucket`·`tempo-bucket` collection의 volume file은 snapshot에 없으므로(SPEC-0228) 복원 뒤 Loki와 Tempo는 빈 상태에서 다시 수집한다. [RUN-0024](../05-databases-and-storage/0024-seaweedfs.md)의 빈 filer store, volume/master tree, `fs.meta.load` 계약을 따른다. restore 실패·identity 충돌·include 부재는 중단하며 자동 cleanup하지 않는다.

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
bucket 이름을 BKP-002와 함께 [RUN-0105](../04-security-and-secrets/0105-openbao-maintenance-window.md#1인-관리자-custody-절차) 1인 관리자 custody의 계정 A에
복사한다. BKP-001은 host `secrets/`에 있어 host 백업으로 함께 복구된다. host를 잃은
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
저장된 byte 수를 남긴다. orchestrator는 run이 실패해도 이 값을 별도 파일
`hyhome_backup_offsite.prom`에 `hyhome_backup_offsite_repo_bytes`로 쓴다. 일요일에는 원격에
`restic check --read-data-subset 10%`도 실행한다. copy나 check가 실패하면
`offsite copy to R2 failed` 또는 `offsite check of R2 failed`를 남기고 다른 단계의
실패처럼 unit이 exit 1로 끝난다. 로컬 snapshot의 전체 export 포함 여부는 별도 확인한다. 로컬 Restic backup/check가 실패하면 `offsite copy skipped`다. 그러나 앞선 pgBackRest/globals/Valkey/SQLite/SeaweedFS 실패는 `restic_ok`를 내리지 않아 partial snapshot과 원격 copy가 진행될 수 있다. 이는 전체 복구 세트 성공이 아니며 unit exit1과 성공 timestamp 부재를 유지한다. 원격이
초기화되지 않았거나 닿지 않으면 exit 65다. 오프사이트까지 성공한 run만
step 4의 성공 timestamp를 쓴다.

R2 repository는 10 GB를 절대 넘지 않는다(owner 2026-10-20). `copy`와 `artifact`는
올리기 전에 지금 저장된 byte(사용하지 않는 pack 포함)에 이번에 올릴 수 있는 최대량의
105%를 더해 보고, 9 GB를 넘을 수 있으면 아무것도 올리지 않는다. 그때는
`refused: up to … bytes after this upload, cap 9000000000`과 exit 66을 남기고 unit이
실패한다. 남는 1 GB는 pack header, index, 추정 오차 몫이다. 30일 bucket lock 때문에 올린
것은 그 안에 지울 수 없으므로 미리 막는다. 거부된 동안에는 새 원격 사본이 없다. 8.5로 lock이
풀린 snapshot을 정리해 9 GB 아래로 내려야 다시 올라간다. 상한을 올리거나 lock을 약화하지
않는다. `cmd`는 읽기 명령(`snapshots`, `stats`, `ls`, `cat`, `find`, `check`, `diff`,
`dump`, `list`, `version`)만 넘긴다. 이 상한은 이 repository의 파일만 센다. 같은 계정의
다른 R2 사용은 8.6에서 따로 확인한다.

#### 8.3 R2에서 복원

host를 잃은 뒤에는 Docker·보존 source revision과 image identity, 계정 A의 BKP-002~005와 account/bucket(BKP-001은 host 백업에서 복구) 외에 root Compose 렌더링에 필요한 non-secret inputs 및 명시적 directory/mount 준비가 필요하다. `.env` 두 키만으로 root Compose bootstrap이 된다고 가정하지 않는다. 복원한 private 설정은 출력하지 않는다.

승인된 새 data-disk scratch에 먼저 원격 snapshot 목록의 metadata만 조사한다. 원격 snapshot ID는 local과 다르므로 host/tag/time과 전체 성공 실행 기록으로 host/state pair를 고정한다. 원격 접근에 필요한 전용 network와 R2 credential을 최소 범위로 제공하고, 기본 bridge·전체 secret 디렉터리 공유를 암묵적으로 사용하지 않는다.

`restic restore <host-id> --tag hyhome-host --target <owned-host-scratch>`와 `restic restore <state-id> --tag hyhome-state --target <owned-state-scratch>`의 정확한 ID를 검토한 후 실행한다. `latest`와 기본 `/tmp`는 사용하지 않는다. host의 `/src/host`에서 설정/custody를 복원하고 state의 `/src/state/pgbackrest`는 별도 승인된 repository 경로에 owner70:70/mode0750로 준비한다. 실제 database 복원은 step5의 backup label/WAL target 계약을 따른다. 원격 copy가 담은 마지막 WAL 이후의 복구는 보장되지 않는다.

R2 scratch 복원 리허설은 wrapper의 `restore` action으로만 한다. 이 action은 R2에 lock을 포함해 아무것도 쓰지 않는다. host와 state snapshot ID 한 쌍(8~64자 소문자 hex)과 `/restore`에 연결한 빈 scratch를 요구하고, 각 ID가 `hyhome-host`·`hyhome-state` tag를 가졌는지 먼저 확인하며, uid 0으로는 실행을 거부한다. 결과로 set별 exit code, 초, 파일 수, byte만 출력한다. container는 root로 실행되지만 `DAC_READ_SEARCH` 외의 capability가 없어 소유자가 다른 0700 scratch에 쓸 수 없으므로, scratch 소유자로 실행한다.

```bash
cd ~/data/hy-home.docker
mkdir -p ~/storage/backups/r2-restore-scratch
SCR=$(mktemp -d -p ~/storage/backups/r2-restore-scratch r2-restore-XXXXXX)
docker compose --profile backup run --rm --no-deps \
  --user "$(id -u):$(id -g)" -v "$SCR:/restore" \
  restic-offsite restore <host-id> <state-id>; echo "rc=$?"
```

host snapshot은 `$SCR/host`, state snapshot은 `$SCR/state`에 복원된다. 소유권은 복원하지 않는다. 결과 줄과 소요 시간을 기록한 뒤, 정확히 그 `$SCR`만 별도 승인을 받아 지운다.

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
남긴다(`--keep-within 30d --keep-monthly 12`, host와 tag별). prune은
`--max-repack-size 0`으로 일부만 쓰이는 pack을 다시 쓰지 않고, 통째로 쓰이지 않는 pack만
지운다. lock 아래에서 repack이 저장량을 늘리지 못하게 하려는 것이다. 이는 snapshot timestamp 기준이며 object 생성 시각·R2 lock 만료와 같지 않다. remote prune/lock 조합은 현재 미검증이다. 삭제/repack이 잠금에 거부되면 중단하고 owner에게 전달하며 다음 달 자동 해소나 index 안전을 가정하지 않는다. 잠금을 약화하거나 object 일부를 직접 삭제하지 않는다. 성공 후에도 `restic-offsite check`로 `no errors were found`를 확인한다.
Evidence에는 실행 시각, 지운 snapshot 수, 전후 `R2 repository size`를 적는다.

#### 8.6 R2 비용과 무료 한도 검토

2026-09-30 확인한 [R2 pricing](https://developers.cloudflare.com/r2/pricing/)
기준: 무료 한도는 계정 단위로 Standard storage 10 GB-month, Class A 100만,
Class B 1000만 건이다. storage는 날마다의 최대값을 한 달 평균한 값으로 매긴다.
Infrequent Access에는 무료 한도가 없다. `DeleteObject`와
`AbortMultipartUpload`는 무료다.

| 항목 | 예상 사용량 | 관리 |
| --- | --- | --- |
| Storage | 2026-10-20 owner가 bucket을 비우고 재초기화(저장소 `f6973d0274`)한 뒤 2026-10-21 03:36 copy 후 5,552,354,483 byte(registry 제외) | 9 GB에서 업로드 거부(8.2); 8 GB에서 `HyhomeOffsiteRepoNearFreeTier`; 8.5 |
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
   확인합니다. 활성화는 아래 순서로만 합니다. 순서를 바꾸면 archive-push가
   stanza 없이 실패하고 WAL이 `pg_wal`에 쌓입니다.
   1. repository 최상위 디렉터리를 `70:70`, `0750`으로 둡니다. r2 이미지
      entrypoint가 시작할 때 이 한 디렉터리만 맞추며, 기존 컨테이너에서는
      `docker exec -u 0 dev-pg sh -c 'chown postgres:postgres /var/lib/pgbackrest && chmod 0750 /var/lib/pgbackrest'`로
      맞춥니다. 소유자와 mode가 모두 맞아야 read-only로 mount하는 복구 컨테이너가
      시작합니다.
   2. `archive_mode=off`인 상태에서
      `docker exec -u postgres dev-pg pgbackrest --stanza=dev stanza-create`를
      실행합니다.
   3. `archive_mode=on` 소스로 `dev-pg`를 다시 만들고
      `pgbackrest --stanza=dev check`가 통과하는지 확인합니다.
   4. `pgbackrest --stanza=dev --type=full backup`으로 최초 full을 만듭니다. 그
      뒤에야 예약 백업의 differential이 기준을 가집니다.
   5. 아래 4번의 격리 restore canary를 실행하고 label·WAL 범위·종료 코드를
      Task에 남깁니다.
   online check 실패를 우회하거나 synthetic offline 결과로 대체하지 않습니다.
3. 기존 scheduler는 개발 check 후 backup, globals/schema export와 image/infra
   revision metadata를 생성합니다. globals는 자격 증명 hash를 포함할 수 있으므로
   출력하지 않으며 기존0700 staging·종료 cleanup과 encrypted Restic에만 둡니다.
   첫 differential은 기존 full이 필요하므로 최초 full 준비 없이 일정을 켜지 않습니다.
4. 복구 대상 backup label과 WAL 범위를 고정하고 별도 project/volume·network none,
   정확히 호환되는 개발 이미지 및 `dev_pgbackrest_cipher_pass` read-only mount를
   검토합니다. dev entrypoint의 기본 credential 소비 경로를 유지하며 명령은
   `pgbackrest --stanza=dev --set=<approved-label> restore` 형태로 승인된 빈 target에만
   실행합니다. `latest`, management stanza, 기존 PGDATA 재사용은 금지합니다.
   restore는 `postgresql.auto.conf`의 `restore_command`에 자신의
   `--config-include-path`를 기록합니다. 복구 컨테이너에서도 entrypoint와 같은
   `/tmp/pgbackrest/conf.d`를 쓰지 않으면 복원된 인스턴스가 WAL을 읽지 못해
   시작하지 못합니다. repository는 read-only로 mount하며, r2 entrypoint는 이미
   `70:70 0750`인 repository를 바꾸지 않습니다.
   복구 컨테이너는 `0640` cipher secret을 읽도록 group 1000에 들어가야 하고,
   복원한 서버는 `dev-pg`와 같은 `max_connections=100`, `max_wal_senders=4`,
   `max_replication_slots=4`로 시작해야 합니다. 이미지 기본값(연결 25)으로
   시작하면 `insufficient parameter settings`로 recovery가 중단됩니다.
   연속 WAL 범위로 선택 시점을 복원해 확인하기 전에는 PITR를 주장하지 않습니다.
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

### 설치된 unit 갱신

소스 경로를 `09-platform-ops`로 이전해도 호스트에 복사해 설치한
`hyhome-backup.service`는 예전 ExecStart 경로를 유지할 수 있습니다. 운영 배포 시
다음 예약 백업에 의존하기 전에 소유자가 기존 설치 절차에 따라 정확한 unit을
갱신하고 daemon-reload 적용을 확인해야 합니다. timer 이름·일정과 사용자·그룹은
그대로 유지하며, 활성화·catch-up 실행·수동 백업은 별도 승인 대상입니다.
이 저장소 변경은 설치된 unit 갱신이나 실제 백업 성공을 뜻하지 않습니다.

### P01 OpenBao failure and trust increment

OpenBao snapshot은 native TLS·검증된 CA를 쓰는 container CLI를 재사용한다. token은
stdin으로만 전달하며 snapshot-only 정책과 주기 갱신을 유지한다. token이 없을 때도
이제 backup unit과 전체 run은 실패한다. 단순히 다른 engine backup이 성공했다고
OpenBao 복구 지점이 있다고 표시하지 않는다. 실제 token 발급/첫 snapshot은 별도
실행 증거다. 빈 대상 restore/unseal은 원본 share와 독립 offsite key, 선정 snapshot의
identity/checksum·일관성·용량·rollback 경계가 확인된 후만 실행한다. P01 synthetic
restore는 HOME/offsite custody를 대신하지 않는다.

### 공유 에이전트 memory 저장소

기본 `get <id>`와 `list`는 검토된 `current` 기억과 caller worktree의 source
pin이 일치할 때만 본문을 반환한다. 새 쓰기는 `candidate`이며, 기존 schema 1의
본문·출처·revision을 삭제하지 않고 pin 없는 기록을 `needs-review`로 표시한다.
보존된 기억은 `get <id> --historical`, `history <id>`, `list --all`, `export`로
명시적으로 조회한다. 역사 본문은 현재 실행·승인·검증 증거가 아니다.
`put --review-state current`는 owner 검토와 아래 구조의 matching source pin이
필요하다. `--source-ref`는 JSON 객체를 인자로 받고 기존 문자열도 보존한다.

```json
{"kind":"repository-file","path":"docs/example.md","revision":"<full Git commit SHA>","hash_algorithm":"sha256","digest":"<64 lowercase hex characters>","context":"검토한 적용 조건"}
```

실제 pin은 완전한 Git commit ID, 그 commit의 같은 상대 경로 일반 blob, caller
worktree의 같은 파일 bytes, 선언한 digest를 함께 결속한다. 어느 하나라도 없거나
다르면 `current`로 취급하지 않는다. tracked 일반 파일의 bytes를 SHA-256으로
pin하며 Git blob ID를 쓰면 `hash_algorithm`은 `git-blob`으로 구분한다. 예시는
실행 가능한 pin이 아니므로 실제 실행에는 해석된 완전 SHA와 digest를 넣는다.
영역 기억은 `--domain-id`, 안전한 재시도는 `--request-key`를 명시한다. 같은 키와
다른 의미 입력은 충돌이며, 충돌 diagnostic의 `stored`와 양쪽 revision을
확인한다. `stored=false`이면 incoming 본문이 보존되었다고 보고하지 않는다.
16 KiB 본문/32 MiB 전체 본문과 계층·영역·metadata·page 상한은 환경 제약 5절이
소유하며, 초과해도 기존 기억을 삭제하지 않는다. 작업 worktree는 이 schema 2
CLI와 helper를 함께 사용한다. 구버전 CLI는 새 재사용/용량 계약을 보장하지 않는다.

Claude와 Codex가 함께 쓰는 memory 저장소(`.workspace-memory/memory.sqlite3`,
규칙은 [환경 제약](../../../../.agents/governance/environment-constraints.md#5-shared-agent-memory))는
Git이 무시하므로 Git으로 복구되지 않는다. 매일 `hyhome-backup.service`가 SQLite
online backup으로 저장소를 staging의 `agent-memory.sqlite3`에 복사하고 Restic
snapshot에 담는다. 저장소가 아직 없는 host에서는 이 단계를 건너뛰고, 백업이
실패하면 부분 파일을 지우고 run을 실패로 남긴다. 그 밖에 따로 백업 파일 하나가
필요하면 저장소 checkout 안에서 다음을 실행한다.

```bash
python3 scripts/operations/agent_memory.py backup --output "$HOME/backups/agent-memory/memory.sqlite3"
```

먼저 `$HOME/backups/agent-memory`를 0700으로 만든다. 0700이 아니거나 심볼릭
링크인 디렉터리, 저장소 자체를 가리키는 출력은 거절한다. 명령은 0600 임시 파일에
쓰고 `integrity_check`를 통과하면 원자적으로 바꾼다. 실패하면 exit 7과
`MEMORY_BACKUP_FAILED`를 남기고 이전 백업을 그대로 둔다. 이 수동 백업 파일은
Restic snapshot에 들어가지 않는다. 일일 snapshot에서 복구하려면 6절 절차대로
검토한 `hyhome-state` snapshot에서 `/src/state/exports/agent-memory.sqlite3`만
소유한 scratch에 꺼내고, 그 파일을 아래 restore의 `--input`으로 쓴다. 일일 실행은
다른 에이전트가 저장소에 5초보다 오래 쓰고 있으면 이 단계를 실패로 기록한다.
동시 백업은 원본 DB inode의 advisory lock을 사용한다. 이미 백업 중이면 exit 7로
거절하고 기존 정상본을 유지한다. snapshot은 schema/identity/revision/provenance와
conflict를 보존하고 검사한 뒤 교체한다. DB/backup/임시 복사본은 64 MiB 예산이며
파일시스템 quota가 아니다. journal의 같은 크기 예산은 관측 대상이다.

복구는 저장소가 없을 때만 한다. 다른 에이전트 세션을 모두 멈춘 뒤 main
checkout의 저장소 root에서 다음을 실행한다. CLI는 현재 디렉터리의 저장소가
스크립트의 저장소와 다르면 거절한다. 저장소가 이미 있으면 exit 3으로 거절하며 기존 기록을 덮어쓰지 않는다.
백업의 schema가 저장소 schema와 다르면 거절하고, 복사가 실패하면 만들던 저장소를
지운다.
원본 main checkout을 이동했다면 Git common directory가 새 main checkout의
실제 `.git`을 가리키고 기존 `.workspace-memory`가 함께 이동했는지 먼저 확인한다.
분리 Git directory와 main checkout이 없는 구조는 `MEMORY_UNAVAILABLE`이며 새
DB를 만들지 않는다. 지원되는 main checkout 구조를 복구하고 검토한 snapshot을
빠진 저장소에만 연결한다. 복원된 기존 `workspace_id`를 이후 쓰기에도 재사용한다.
독립 clone/다른 host가 같은 물리 DB라고 주장하지 않는다. 과거 native migration을
재실행하거나 개인 native 파일을 읽고 지우지 않는다.

```bash
python3 scripts/operations/agent_memory.py restore --input "<수동 백업 또는 Restic에서 꺼낸 agent-memory.sqlite3>"
python3 scripts/operations/agent_memory.py usage
```

복구는 기록만 되살린다. 기록이 무엇이 될 수 없는지는
[환경 제약 5절](../../../../.agents/governance/environment-constraints.md#5-shared-agent-memory)이 정한다.

## Verification

command, exit status, pgBackRest backup label, Restic snapshot ID, 복원된 row
count 또는 file hash, 소요 시간을 기록한다. key 값, dump 내용, rendered
configuration은 절대 기록하지 않는다.

## Failure and Recovery

### Rollback or Recovery

- `archive_command` 실패: `pgbackrest --stanza=mng check`가 원인을 보여준다.
  `pg_wal`이 disk를 채우기 전에 repository 경로나 ownership을 고치거나,
  approval을 받아 `archive_mode=off`를 설정한다([RUN-0035](../05-databases-and-storage/0035-storage-exhaustion.md)).
- 잘못되었거나 잃어버린 key: pgBackRest `info`가 `status: error`를 보고하고
  Restic은 `wrong password or no key found`를 보고한다. offline custody에서
  key를 복구한다. repository를 읽을 다른 방법은 없다.
- 중단된 Restic run: 다시 실행한다. 다른 Restic 프로세스가 실행 중이 아닌지
  확인한 뒤에만 `restic unlock`한다.

### Escalation

restore rehearsal이 실패하거나, 두 disk 모두 오류를 보고하거나, key를
잃어버렸을 때 @buenhyden에게 escalation한다.

## Related Documents

### Traceability

- Guide: [GDE-0021](../../guides/10-platform-and-backup/0021-backup-and-restore.md); Policy: [POL-0021](../../policies/10-platform-and-backup/0021-backup-and-restore.md)
- Alerts: [host backup rules](../../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.infra.yml)
- Runtime pins: [Restic Compose](../../../../infra/09-platform-ops/restic/docker-compose.yml)
  and the [`mng-pg` image](../../../../infra/04-data/mng-db/pg/backup/Dockerfile)
- Rehearsal: `HYHOME_BACKUP_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.BackupRestoreRehearsalTests`

- [pgBackRest user guide](https://pgbackrest.org/user-guide.html)
- [Restic: preparing a repository](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html)
- [Restic: removing snapshots](https://restic.readthedocs.io/en/stable/060_forget.html)
