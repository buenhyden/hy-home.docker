#!/bin/sh
# Restic entrypoint for the two repositories.
#   state: allowlisted data-disk trees, consistent exports and the pgBackRest
#          repository                                        -> BACKUP_STATE_REPO_DIR
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

# Registered mutations receive a one-operation stdin admission only after the
# host has persisted capacity. This prevents accidental direct entrypoint use;
# an operator with arbitrary Docker access can still bypass the entrypoint.
require_memory_admission() {
    IFS= read -r admission || { echo "memory capacity admission absent" >&2; exit 64; }
    [ "${#admission}" -le 256 ] || { echo "invalid memory capacity admission" >&2; exit 64; }
    actual="$(printf '%s\n' "$admission" | sha256sum | cut -d' ' -f1)"
    if [ -z "${HYHOME_MEMORY_ADMISSION_SHA256:-}" ] ||
        [ "$actual" != "$HYHOME_MEMORY_ADMISSION_SHA256" ]; then
        echo "memory capacity admission mismatch" >&2; exit 64;
    fi
    case "$admission" in
        'HYHOME_MEMORY_BUDGET_V1 state '*) ;;
        *) echo "memory capacity admission target mismatch" >&2; exit 64 ;;
    esac
    IFS=' ' read -r protocol target request nonce extra <<EOF
$admission
EOF
    if [ "$protocol" != HYHOME_MEMORY_BUDGET_V1 ] || [ "$target" != state ] ||
        [ -n "$extra" ] || [ "${#request}" -ne 64 ] || [ "${#nonce}" -ne 64 ]; then
        echo "invalid memory capacity admission fields" >&2; exit 64
    fi
    case "$request$nonce" in *[!0-9a-f]*) echo "invalid memory capacity admission fields" >&2; exit 64 ;; esac
    MEMORY_OPERATION_TAG="memory-op-$request"
    unset protocol target request nonce extra
    unset admission actual HYHOME_MEMORY_ADMISSION_SHA256
}

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
        echo "use agent_memory.py backup-run --target state" >&2
        exit 64
        ;;
    budget-backup)
        require_memory_admission
        for set in $SETS; do
            require_initialized "$set"
        done
        # state: only allowlisted file-safe trees plus the export staging;
        # host: the whole secrets/ and .env mount.
        list=/tmp/state-paths
        : >"$list"
        grep -v -e '^#' -e '^$' "$SETS_DIR/state-include.txt" | while read -r rel; do
            case "$rel" in /* | *..*) echo "invalid include: $rel" >&2; exit 64 ;; esac
            case "$rel" in
            ai/ollama/models/*) src=/src/state/ollama-models/${rel#ai/ollama/models/} ;;
            *) src=/src/state/volumes/$rel ;;
            esac
            if [ -e "$src" ]; then
                printf '%s\n' "$src" >>"$list"
            else
                echo "include not present, skipped: $rel"
            fi
        done
        echo /src/state/exports >>"$list"
        echo /src/state/pgbackrest >>"$list"
        echo /src/state/dev-pgbackrest >>"$list"
        RESTIC_REPOSITORY="$(repo_for state)" restic backup \
            --host hy-home --tag hyhome-state --tag "$MEMORY_OPERATION_TAG" \
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
        # Mutations go through their owned entrypoint, never generic cmd.
        case "${1:-}" in
            snapshots | stats | ls | cat | find | check | diff | dump | list | version) ;;
            *)
                echo "cmd runs read-only commands only; use the owned operation" >&2
                exit 64
                ;;
        esac
        RESTIC_REPOSITORY="$(repo_for "$set_name")" exec restic --no-lock "$@"
        ;;
    *)
        echo "unknown action: $action" >&2
        exit 64
        ;;
esac
