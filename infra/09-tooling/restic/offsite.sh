#!/bin/sh
# Offsite Restic entrypoint (ADR-0041): one Cloudflare R2 repository that
# receives the snapshots of both local repositories (state and host).
# Usage: offsite.sh {snapshots|init|copy|check|cmd <restic args...>}
# Deletion is not offered: the bucket lock keeps objects and remote
# forget/prune is a separate, owner-run procedure.
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
        ;;
    check)
        # Weekly: structure plus a random tenth of the pack data.
        require_initialized
        restic check --read-data-subset 10%
        ;;
    cmd)
        case "${1:-}" in
            forget | prune | unlock)
                echo "'$1' is not run from this host; see RUN-0021" >&2
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
