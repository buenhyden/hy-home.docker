#!/bin/sh
# Offsite Restic entrypoint (ADR-0041): one Cloudflare R2 repository that
# receives the snapshots of both local repositories (state and host).
# Usage: offsite.sh {snapshots|init|copy|check|forget-prune|cmd <restic args...>}
# The daily run never deletes. forget-prune is the owner-run, separately
# confirmed monthly procedure that keeps the remote inside the R2 free tier
# (RUN-0021); it keeps every snapshot within the 30-day bucket lock.
set -eu

SETS="state host"

account="${BACKUP_OFFSITE_R2_ACCOUNT_ID:-}"
bucket="${BACKUP_OFFSITE_R2_BUCKET:-}"
if ! printf '%s' "$account" | grep -qE '^[0-9a-f]{32}$' ||
    ! printf '%s' "$bucket" | grep -qE '^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$'; then
    echo "BACKUP_OFFSITE_R2_ACCOUNT_ID and BACKUP_OFFSITE_R2_BUCKET are unset or malformed" >&2
    exit 64
fi
export RESTIC_REPOSITORY="s3:https://$account.r2.cloudflarestorage.com/$bucket"

# Restic's S3 backend reads credentials only from the environment. The values
# come from secret files and are never printed.
secret() {
    value="$(tr -d '\r\n' <"/run/secrets/$1")"
    [ -n "$value" ] || { echo "secret $1 is empty" >&2; exit 64; }
    printf '%s' "$value"
}
AWS_ACCESS_KEY_ID="$(secret r2_access_key_id)"
AWS_SECRET_ACCESS_KEY="$(secret r2_secret_access_key)"
export AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY

require_initialized() {
    if ! restic cat config >/dev/null; then
        echo "R2 repository is not initialized or not reachable; see RUN-0021 (Offsite copy)" >&2
        exit 65
    fi
}

action="${1:-snapshots}"
[ "$#" -gt 0 ] && shift

case "$action" in
    snapshots)
        require_initialized
        restic snapshots --compact
        ;;
    init)
        # Never re-initialize. The chunker parameters follow the state
        # repository so its snapshots deduplicate in the remote.
        if restic cat config >/dev/null 2>&1; then
            echo "R2 repository already initialized; skipped"
        else
            restic init --from-repo /repo/state --copy-chunker-params
        fi
        ;;
    copy)
        require_initialized
        # copy skips snapshots the remote already has. --no-lock applies to
        # the read-only source only; the orchestrator's flock excludes writers.
        for set in $SETS; do
            restic copy --no-lock --from-repo "/repo/$set"
        done
        echo "R2 latest snapshots:"
        restic snapshots --compact --latest 1
        # Stored (compressed) bytes, which R2 bills; the orchestrator turns
        # this line into hyhome_backup_offsite_repo_bytes.
        size="$(restic stats --mode raw-data --json | sed -n 's/.*"total_size":\([0-9]*\).*/\1/p')"
        echo "R2 repository size: ${size:-unknown} bytes"
        ;;
    check)
        # Weekly: structure plus a random tenth of the pack data.
        require_initialized
        restic check --read-data-subset 10%
        ;;
    forget-prune)
        # Deletes remote snapshots and data. Owner-run only, with an explicit,
        # separately approved confirmation (RUN-0021 8.5). Everything younger
        # than the 30-day bucket lock stays, so no locked object is removed;
        # older history keeps one snapshot per month for a year.
        if [ "${HYHOME_PRUNE_CONFIRM:-}" != "delete-old-remote-snapshots" ]; then
            echo "forget-prune needs HYHOME_PRUNE_CONFIRM=delete-old-remote-snapshots" >&2
            exit 64
        fi
        require_initialized
        restic forget --prune --group-by host,tags --keep-within 30d --keep-monthly 12
        size="$(restic stats --mode raw-data --json | sed -n 's/.*"total_size":\([0-9]*\).*/\1/p')"
        echo "R2 repository size: ${size:-unknown} bytes"
        ;;
    artifact)
        # RUN-0085 W3b: store the W3 OpenBao snapshot and its receipt, mounted
        # read-only at /artifact, then read both back from R2 and compare.
        # Prints only names, sizes, SHA-256 and the snapshot ID; no retry.
        # A failed restic must fail the pipe, not hide behind sed or sha256sum.
        # shellcheck disable=SC3040 # busybox ash in the restic image supports it.
        set -o pipefail
        require_initialized
        files="raft-pre-upgrade.snap raft-pre-upgrade.snap.receipt.json"
        for name in $files; do
            if [ ! -f "/artifact/$name" ] || [ -L "/artifact/$name" ] ||
                [ ! -s "/artifact/$name" ]; then
                echo "missing, empty or non-regular /artifact/$name" >&2
                exit 64
            fi
        done
        # The snapshot must be the one the W3 receipt names.
        snap_sum="$(sha256sum <"/artifact/raft-pre-upgrade.snap" | cut -d' ' -f1)"
        if ! grep -q "\"sha256\": *\"$snap_sum\"" /artifact/raft-pre-upgrade.snap.receipt.json; then
            echo "snapshot SHA-256 differs from its W3 receipt" >&2
            exit 64
        fi
        set --
        for name in $files; do set -- "$@" "/artifact/$name"; done
        id="$(restic backup --json --host hy-home-openbao-window \
            --tag hy-home-openbao-w3 "$@" |
            sed -n 's/.*"message_type":"summary".*"snapshot_id":"\([0-9a-f]\{64\}\)".*/\1/p')"
        [ -n "$id" ] || { echo "R2 backup returned no snapshot ID" >&2; exit 65; }
        entries=""
        for name in $files; do
            local_sum="$(sha256sum <"/artifact/$name" | cut -d' ' -f1)"
            remote_sum="$(restic dump "$id" "/artifact/$name" | sha256sum | cut -d' ' -f1)" || {
                echo "R2 read-back failed for $name in snapshot $id" >&2
                exit 65
            }
            size="$(wc -c <"/artifact/$name" | tr -d ' ')"
            if [ "$local_sum" != "$remote_sum" ]; then
                echo "R2 bytes differ for $name in snapshot $id" >&2
                exit 65
            fi
            entries="$entries${entries:+,}{\"name\":\"$name\",\"bytes\":$size,\"sha256\":\"$local_sum\"}"
        done
        echo "{\"state\":\"W3B_STORED\",\"snapshot_id\":\"$id\",\"tag\":\"hy-home-openbao-w3\",\"files\":[$entries]}"
        ;;
    cmd)
        case "${1:-}" in
            forget | prune | unlock)
                echo "'$1' is not run directly; use forget-prune (RUN-0021 8.5)" >&2
                exit 64
                ;;
        esac
        exec restic "$@"
        ;;
    *)
        echo "unknown action: $action" >&2
        exit 64
        ;;
esac
