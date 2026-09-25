#!/bin/sh
# Restic entrypoint for the two repositories.
#   state: allowlisted data-disk trees and consistent exports -> BACKUP_STATE_REPO_DIR
#   host:  secrets/ and .env on the system disk              -> BACKUP_HOST_REPO_DIR
# Usage: backup.sh {snapshots|init|backup|check|forget-prune|cmd <state|host> <restic args...>}
set -eu

SETS="state host"
SETS_DIR=/opt/hyhome/sets

repo_for() {
    case "$1" in
        state | host) printf '/repo/%s' "$1" ;;
        *) echo "unknown set: $1" >&2; exit 64 ;;
    esac
}

initialized() {
    RESTIC_REPOSITORY="$(repo_for "$1")" restic cat config >/dev/null 2>&1
}

require_initialized() {
    if ! initialized "$1"; then
        echo "repository '$1' is not initialized; run: backup.sh init" >&2
        exit 65
    fi
}

action="${1:-snapshots}"
[ "$#" -gt 0 ] && shift

case "$action" in
    snapshots)
        for set in $SETS; do
            if initialized "$set"; then
                RESTIC_REPOSITORY="$(repo_for "$set")" restic snapshots --compact
            else
                echo "repository '$set' is not initialized"
            fi
        done
        ;;
    init)
        # Never re-initialize: an existing repository keeps its key and data.
        for set in $SETS; do
            if initialized "$set"; then
                echo "repository '$set' already initialized; skipped"
            else
                RESTIC_REPOSITORY="$(repo_for "$set")" restic init
            fi
        done
        ;;
    backup)
        for set in $SETS; do
            require_initialized "$set"
        done
        # state: only allowlisted file-safe trees plus the export staging;
        # host: the whole secrets/ and .env mount.
        list=/tmp/state-paths
        : >"$list"
        grep -v -e '^#' -e '^$' "$SETS_DIR/state-include.txt" | while read -r rel; do
            case "$rel" in /* | *..*) echo "invalid include: $rel" >&2; exit 64 ;; esac
            if [ -e "/src/state/volumes/$rel" ]; then
                printf '/src/state/volumes/%s\n' "$rel" >>"$list"
            else
                echo "include not present, skipped: $rel"
            fi
        done
        echo /src/state/exports >>"$list"
        RESTIC_REPOSITORY="$(repo_for state)" restic backup \
            --host hy-home --tag hyhome-state \
            --exclude-file "$SETS_DIR/state-exclude.txt" --exclude-caches \
            --files-from-verbatim "$list"
        RESTIC_REPOSITORY="$(repo_for host)" restic backup \
            --host hy-home --tag hyhome-host \
            --exclude-file "$SETS_DIR/host-exclude.txt" /src/host
        ;;
    check)
        for set in $SETS; do
            require_initialized "$set"
            RESTIC_REPOSITORY="$(repo_for "$set")" restic check
        done
        ;;
    forget-prune)
        # Deletes snapshots and data. Runs only with an explicit, separately
        # approved confirmation (RUN-0021).
        if [ "${HYHOME_PRUNE_CONFIRM:-}" != "delete-old-snapshots" ]; then
            echo "forget-prune needs HYHOME_PRUNE_CONFIRM=delete-old-snapshots" >&2
            exit 64
        fi
        for set in $SETS; do
            require_initialized "$set"
            RESTIC_REPOSITORY="$(repo_for "$set")" restic forget --prune \
                --tag "hyhome-$set" --keep-daily 30 --keep-weekly 13 --keep-monthly 12
        done
        ;;
    cmd)
        set_name="${1:?cmd needs a set}"
        shift
        # Deletions go only through forget-prune and its confirmation.
        case "${1:-}" in
            forget | prune)
                echo "use forget-prune for '$1'" >&2
                exit 64
                ;;
        esac
        RESTIC_REPOSITORY="$(repo_for "$set_name")" exec restic "$@"
        ;;
    *)
        echo "unknown action: $action" >&2
        exit 64
        ;;
esac
