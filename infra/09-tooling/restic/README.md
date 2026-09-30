---
title: "Restic Backup Jobs"
version: "1.2.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-30"
---

# Restic Backup Jobs

## Overview

HOME 상태를 서로 다른 물리 디스크에 있는 두 개의 암호화된 Restic 저장소로
스냅샷하고, 두 저장소를 오프사이트의 Cloudflare R2 저장소 하나로 복사하는
1회성 작업입니다(ADR-0041). `mng-pg`의 pgBackRest도 함께 구동하는 호스트
오케스트레이터와 타이머를 포함합니다.

## Audience

백업을 실행·검증·복구하는 운영자와 백업 경계를 검토하는 담당자.

## Scope

범위 내: [`sets/state-include.txt`](sets/state-include.txt)에 allowlist로
등록된 파일 안전 data-disk 트리, 일관된 내보내기 결과(PostgreSQL globals,
Valkey RDB, SQLite 데이터베이스 세 개), `secrets/`와 `.env`.
범위 외: allowlist에 없는 모든 것, 특히 POL-0021에 별도 방식이 정의된 live
엔진 디렉터리. pgBackRest 저장소는 state Restic 저장소에 담겨 R2로 갑니다
(원격 RPO 하루). pgBackRest가 S3로 직접 보내는 저장소는 없습니다.

## Structure

```text
restic/
├── docker-compose.yml     # restic, restic-offsite, backup-sqlite-export (profile backup)
├── backup.sh              # snapshots | init | backup | check | forget-prune | cmd
├── offsite.sh             # R2: snapshots | init | copy | check | cmd (no deletes)
├── export_sqlite.py       # Online Backup API copies with integrity check
├── sets/                  # state-include, state-exclude, host-exclude
├── bin/hyhome-backup.sh   # host orchestrator (lock, disk preflight, order)
└── systemd/               # hyhome-backup.service and .timer
```

## Tech Stack

Restic과 Python 이미지는 [`docker-compose.yml`](docker-compose.yml)에 고정되어
있으며 pgBackRest는
[`mng-pg` 이미지](../../04-data/operational/mng-db/pg/backup/Dockerfile)에
고정되어 있습니다.

## Configuration

- 프로필 `backup` (분류는 automation이며 HOME이 아님). `restic`은 기본값이
  `snapshots`이므로 `up`을 실행해도 아무것도 바뀌지 않습니다.
- `restic`은 `DAC_OVERRIDE`만 가진 root로 실행되며 `network_mode: none`이고
  모든 소스는 읽기 전용으로 마운트됩니다. `/repo/state`와 `/repo/host`만
  쓰기 가능합니다. 저장소와 staging은 `create_host_path: false`를 사용합니다.
- `backup-sqlite-export`는 WAL 리더가 `-shm` 파일을 필요로 하기 때문에만
  Grafana, Gatus, Open WebUI 데이터 디렉터리를 쓰기 가능하게 마운트하며
  UID 1000이 소유하는 0600 복사본을 staging에 씁니다.
- `restic`은 저장소 인덱스와 tmpfs 캐시에 `mem_limit: 1g`를 가지며 `cmd`는
  `forget`/`prune`을 거부하고 이는 `forget-prune`을 통해서만 실행됩니다.
- 환경 변수 키: `BACKUP_STATE_REPO_DIR`, `BACKUP_HOST_REPO_DIR`,
  `BACKUP_STATE_MAX_GIB`,
  `DEFAULT_MOUNT_VOLUME_PATH`, `DEFAULT_OBSERVABILITY_DIR`, `DEFAULT_AI_MODEL_DIR`,
  `SECRETS_GID`. Secret: `restic_password` (BKP-002).
- 오케스트레이터는 경로를 `docker compose config`에서 읽고 `.env`를 직접
  소싱하지 않으며 `flock` 잠금을 사용합니다(사용 중이면 종료 코드 75).
  여유 공간이 20 GiB 미만이거나 저장소가 소스와 같은 파일시스템을
  공유(또는 그 안에 위치)하면 종료 코드 64를 반환하고 pgBackRest 만료 이후
  `BACKUP_STATE_REPO_DIR`가 `BACKUP_STATE_MAX_GIB`(5) 이상이면 Restic 단계를
  건너뛰고 실패 처리하며 종료 시 항상 staging을 비웁니다.
- `restic-offsite`만 외부로 나가는 네트워크(`restic_offsite_net`)를 가진
  백업 작업입니다. 로컬 저장소 두 개만 읽기 전용(`DAC_READ_SEARCH`)으로
  마운트하고, `restic copy --no-lock --from-repo`로
  `s3:https://<BACKUP_OFFSITE_R2_ACCOUNT_ID>.r2.cloudflarestorage.com/<BACKUP_OFFSITE_R2_BUCKET>`에
  복사합니다. secret은 `restic_password`(원본), `restic_offsite_password`
  (BKP-003), `r2_access_key_id`(BKP-004), `r2_secret_access_key`(BKP-005)이며,
  스크립트는 R2 키를 출력하지 않고 환경 변수로만 넘깁니다. 두 키 중 하나라도
  비어 있으면 오케스트레이터는 이 단계를 건너뜁니다. 로컬 backup과 check가
  성공한 뒤 `copy`를 실행하고, 일요일에는 `check --read-data-subset 10%`도
  실행합니다. 실패하면 unit도 실패합니다.
- `mng-pg`는 로컬 빌드이며 레지스트리가 없습니다. pull에는
  `docker compose pull --ignore-buildable`을 사용합니다.

## Validation

```bash
python3 -m unittest tests.validation.test_compose_baseline_gates.BackupContractTests
HYHOME_BACKUP_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.BackupRestoreRehearsalTests
systemd-analyze verify infra/09-tooling/restic/systemd/hyhome-backup.service infra/09-tooling/restic/systemd/hyhome-backup.timer
```

## How to Work in This Area

새 소스를 추가할 때는 먼저 일관된 방식을 결정합니다. 파일 안전 트리는
allowlist 한 줄을 추가하고, live 엔진은 `bin/hyhome-backup.sh`에 내보내기
단계를 추가하며 안전하게 복사할 수 있게 되기 전까지는 줄을 추가하지
않습니다. 삭제는 `forget-prune`의 확인 변수 뒤에 유지합니다. 설정, 실행,
복구는 백업 Runbook을 따릅니다.

## Related Documents

[documentation entry point](../../../docs/README.md)를 통해 Stage 05 대상
`04-data/0021-backup-and-restore`(GDE/POL/RUN-0021)로 이동합니다. 오프사이트
대상 결정은 `docs/02.architecture/decisions/0041-offsite-backup-target.md`(ADR-0041)를 참고합니다.
