#!/usr/bin/env bash
# Daily HOME backup orchestrator (run by systemd/hyhome-backup.service).
#   1. single-run lock and cross-disk preflight
#   2. pgBackRest physical backup of mng-pg (full on Sunday, else differential)
#   3. consistent exports: PostgreSQL globals, Valkey RDB, SQLite stores,
#      SeaweedFS filer metadata (vacuum paused until the run ends)
#   4. Restic backup and check of both repositories
#   5. remove the plaintext exports from staging, on success or failure
#   6. offsite: restic copy of both repositories to Cloudflare R2 once the
#      owner has set BACKUP_OFFSITE_R2_* (ADR-0041); weekly remote check
# Paths come from the rendered Compose model; .env is never sourced.
set -euo pipefail
umask 077

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$repo_root"
compose=(docker compose --profile backup)

rendered="$("${compose[@]}" config --format json restic restic-offsite)"
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
running() { [[ "$(docker inspect -f '{{.State.Running}}' "$1" 2>/dev/null)" == true ]]; }
# A failed weed shell command may still exit 0, so its output is checked too.
# Ports are the Compose defaults (SEAWEEDFS_MASTER_HTTP_PORT, _FILER_HTTP_PORT).
seaweed_shell() {
    local out
    out="$(docker exec -i seaweedfs-master /bin/sh /opt/hyhome/hyhome-seaweedfs.sh shell \
        -master=localhost:9333 -filer=seaweedfs-filer:8888 2>&1)" || { printf '%s\n' "$out" >&2; return 1; }
    if grep -qiE 'error|fail' <<<"$out"; then
        printf '%s\n' "$out" >&2
        return 1
    fi
}
seaweed_vacuum_paused=false
cleanup() {
    if [[ "$seaweed_vacuum_paused" == true ]]; then
        printf 'lock\nvolume.vacuum.enable\nunlock\n' | seaweed_shell >/dev/null ||
            echo "SeaweedFS vacuum could not be re-enabled; run volume.vacuum.enable" >&2
        seaweed_vacuum_paused=false
    fi
    find "$staging" -mindepth 1 -delete
}
trap cleanup EXIT

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

# SeaweedFS: needles are append-only, so filer metadata saved before Restic
# reads the volume files refers to bytes the snapshot contains, except objects
# overwritten or deleted inside the Restic window (RUN-0024). Vacuum, which
# rewrites .dat files, stays off until the EXIT trap; a SIGKILLed run leaves it
# off until volume.vacuum.enable or a master restart.
if running seaweedfs-master && running seaweedfs-filer; then
    # A leftover export from a killed run must never pass as this run's.
    docker exec seaweedfs-master rm -f /tmp/filer.meta || status=1
    if printf 'lock\nvolume.vacuum.disable\nunlock\n' | seaweed_shell; then
        seaweed_vacuum_paused=true
        if printf 'fs.meta.save -o /tmp/filer.meta /\n' | seaweed_shell &&
            docker exec seaweedfs-master sh -c 'test -s /tmp/filer.meta && cat /tmp/filer.meta' \
                >"$staging/seaweedfs-filer.meta" && [[ -s "$staging/seaweedfs-filer.meta" ]]; then
            :
        else
            echo "SeaweedFS filer metadata export failed" >&2
            status=1
        fi
        docker exec seaweedfs-master rm -f /tmp/filer.meta || true
    else
        echo "SeaweedFS vacuum could not be paused; metadata export skipped" >&2
        status=1
    fi
elif running seaweedfs-master || running seaweedfs-filer; then
    echo "SeaweedFS is partly running: filer metadata export skipped" >&2
    status=1
else
    echo "SeaweedFS not running: filer metadata export skipped"
fi

# Size budget, measured after pgBackRest has expired old backups. Above it the
# Restic step adds nothing; deleting snapshots stays a separate approval.
# Repository contents belong to UID 70 (pgBackRest) and root (Restic), so the
# host user measures through a read-only, networkless container.
restic_image="$(python3 -c 'import json,sys
print(json.loads(sys.stdin.read())["services"]["restic"]["image"])' <<<"$rendered")"
size_kib() {
    docker run --rm --network none -v "$1:/m:ro" --entrypoint du "$restic_image" -sk /m | cut -f1
}
if ! state_kib="$(size_kib "$state_repo")"; then
    echo "cannot measure $state_repo; Restic backup skipped" >&2
    state_kib=$((max_gib * 1024 * 1024))
    status=1
fi
restic_ok=true
if (( state_kib >= max_gib * 1024 * 1024 )); then
    echo "BACKUP_STATE_REPO_DIR uses $((state_kib / 1024)) MiB, at or over the ${max_gib} GiB budget; Restic backup skipped" >&2
    status=1
    restic_ok=false
else
    "${compose[@]}" run --rm --no-deps restic backup || { status=1; restic_ok=false; }
fi
"${compose[@]}" run --rm --no-deps restic check || { status=1; restic_ok=false; }

# Size trend for capacity review (journal): repositories grow with retained
# changes only; pgBackRest is bounded by retention, Restic until forget-prune.
echo "repository sizes: state=$(( $(size_kib "$state_repo") / 1024 ))MiB (budget ${max_gib}GiB) host=$(( $(size_kib "$host_repo/restic") / 1024 ))MiB" || true

# Offsite (ADR-0041). Staging is emptied and vacuum resumed first, so neither
# waits for the upload. Unconfigured: logged and skipped. Configured: a failed
# copy or check fails the unit like any other step, local results stay valid.
cleanup
offsite_configured="$(python3 -c 'import json,sys
env = json.loads(sys.stdin.read())["services"]["restic-offsite"]["environment"]
print("yes" if env.get("BACKUP_OFFSITE_R2_ACCOUNT_ID") and env.get("BACKUP_OFFSITE_R2_BUCKET") else "no")' <<<"$rendered")"
if [[ "$offsite_configured" != yes ]]; then
    echo "offsite copy not configured (BACKUP_OFFSITE_R2_*); skipped"
elif [[ "$restic_ok" == true ]]; then
    "${compose[@]}" run --rm --no-deps restic-offsite copy || { echo "offsite copy to R2 failed" >&2; status=1; }
    if [[ "$(date +%u)" == 7 ]]; then
        "${compose[@]}" run --rm --no-deps restic-offsite check || { echo "offsite check of R2 failed" >&2; status=1; }
    fi
else
    echo "local Restic backup or check failed; offsite copy skipped" >&2
fi
exit "$status"
