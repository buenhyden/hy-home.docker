#!/usr/bin/env bash
# Daily HOME backup orchestrator (run by systemd/hyhome-backup.service).
#   1. single-run lock and cross-disk preflight
#   2. pgBackRest physical backup of mng-pg (full on Sunday, else differential)
#   3. consistent exports: PostgreSQL globals, Valkey RDB, SQLite stores
#   4. Restic backup and check of both repositories
#   5. remove the plaintext exports from staging, on success or failure
# Paths come from the rendered Compose model; .env is never sourced.
set -euo pipefail
umask 077

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$repo_root"
compose=(docker compose --profile backup)

rendered="$("${compose[@]}" config --format json restic)"
mount_source() {
    python3 -c 'import json,sys
cfg = json.loads(sys.stdin.read())
for volume in cfg["services"]["restic"]["volumes"]:
    if volume["target"] == sys.argv[1]:
        print(volume["source"]); break
else:
    raise SystemExit("mount not found: " + sys.argv[1])' "$1" <<<"$rendered"
}
state_repo="$(dirname "$(mount_source /repo/state)")"
host_repo="$(dirname "$(mount_source /repo/host)")"
volumes_root="$(mount_source /src/state/volumes)"
max_gib="$(python3 -c 'import json,sys
print(json.loads(sys.stdin.read())["services"]["restic"]["environment"]["BACKUP_STATE_MAX_GIB"])' <<<"$rendered")"
[[ "$max_gib" =~ ^[1-9][0-9]*$ ]] || { echo "invalid BACKUP_STATE_MAX_GIB" >&2; exit 64; }
staging="$state_repo/staging"

device_of() { stat -c %d -- "$1"; }
for dir in "$state_repo/restic" "$state_repo/pgbackrest" "$host_repo/restic" "$staging"; do
    [[ -d "$dir" && ! -L "$dir" ]] || { echo "missing backup directory: $dir" >&2; exit 64; }
done
# A repository inside a backed-up source would snapshot itself and grow
# without bound, so refuse any such layout.
inside() { [[ "$(realpath -m -- "$1")/" == "$(realpath -m -- "$2")/"* ]]; }
for pair in "$state_repo:$volumes_root" "$state_repo:$repo_root/secrets" \
            "$host_repo:$volumes_root" "$host_repo:$repo_root/secrets"; do
    if inside "${pair%%:*}" "${pair#*:}"; then
        echo "backup repository ${pair%%:*} is inside backed-up source ${pair#*:}" >&2
        exit 64
    fi
done

if [[ "$(device_of "$state_repo")" == "$(device_of "$volumes_root")" ]]; then
    echo "state repository shares a filesystem with the data volumes" >&2
    exit 64
fi
if [[ "$(device_of "$host_repo")" == "$(device_of "$repo_root/secrets")" ]]; then
    echo "host repository shares a filesystem with secrets/" >&2
    exit 64
fi

min_free_kb=$((20 * 1024 * 1024))
free_kb="$(df -Pk -- "$state_repo" | awk 'NR==2 {print $4}')"
if (( free_kb < min_free_kb )); then
    echo "less than 20 GiB free under $state_repo; backup not started" >&2
    exit 64
fi

exec 9>"$state_repo/.hyhome-backup.lock"
flock -n 9 || { echo "another backup run holds the lock" >&2; exit 75; }

# Exports are plaintext; never leave them behind, even after a failure or a
# timeout. The encrypted snapshots hold them once Restic succeeds.
trap 'find "$staging" -mindepth 1 -delete' EXIT

running() { [[ "$(docker inspect -f '{{.State.Running}}' "$1" 2>/dev/null)" == true ]]; }

status=0
if running mng-pg; then
    type="diff"
    [[ "$(date +%u)" == 7 ]] && type="full"
    docker exec -u postgres mng-pg pgbackrest --stanza=mng --type="$type" backup || status=1
    docker exec -u postgres mng-pg sh -c 'pg_dumpall --globals-only -U "$POSTGRES_USER"' \
        >"$staging/mng-pg-globals.sql" || status=1
else
    echo "mng-pg not running: physical backup and globals skipped" >&2
    status=1
fi

if running mng-valkey; then
    docker exec mng-valkey sh -c \
        'REDISCLI_AUTH="$(cat /run/secrets/mng_valkey_password)" valkey-cli --no-auth-warning --rdb -' \
        >"$staging/mng-valkey.rdb" || status=1
else
    echo "mng-valkey not running: RDB export skipped" >&2
    status=1
fi

"${compose[@]}" run --rm --no-deps backup-sqlite-export || status=1

# Size budget, measured after pgBackRest has expired old backups. Above it the
# Restic step adds nothing; deleting snapshots stays a separate approval.
state_kib="$(du -sk -- "$state_repo" | cut -f1)"
if (( state_kib >= max_gib * 1024 * 1024 )); then
    echo "BACKUP_STATE_REPO_DIR uses $((state_kib / 1024)) MiB, at or over the ${max_gib} GiB budget; Restic backup skipped" >&2
    status=1
else
    "${compose[@]}" run --rm --no-deps restic backup || status=1
fi
"${compose[@]}" run --rm --no-deps restic check || status=1

# Size trend for capacity review (journal): repositories grow with retained
# changes only; pgBackRest is bounded by retention, Restic until forget-prune.
du -sh -- "$state_repo/pgbackrest" "$state_repo/restic" "$host_repo/restic" 2>/dev/null || true
exit "$status"
