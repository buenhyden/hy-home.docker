#!/bin/sh
# Offsite Restic entrypoint (ADR-0041): one Cloudflare R2 repository that
# receives the snapshots of both local repositories (state and host).
# Usage: offsite.sh {snapshots|init|copy|check|forget-prune|restore <host-id> <state-id>|cmd <restic args...>}
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

# The owner forbids the R2 repository from ever passing 10 GB (2026-10-20).
# Every upload is refused when it could take the stored bytes past 9 GB: the
# gigabyte left covers pack headers, index files and estimate error, and the
# 30-day bucket lock means nothing written can be deleted in time. The
# variable can only lower the cap; tests use it.
max_bytes=9000000000
case "${BACKUP_OFFSITE_MAX_BYTES:-}" in
    '') ;;
    *[!0-9]*) echo "BACKUP_OFFSITE_MAX_BYTES must be a byte count" >&2; exit 64 ;;
    *) [ "$BACKUP_OFFSITE_MAX_BYTES" -lt "$max_bytes" ] && max_bytes="$BACKUP_OFFSITE_MAX_BYTES" ;;
esac

# Bytes of every file in the R2 repository, unused packs included, which is
# what R2 bills. Fails closed: no listing, no number.
stored_bytes() {
    # restic prints this listing on stderr.
    listing="$(restic --no-lock stats --mode debug 2>&1)" || { echo "R2 size listing failed" >&2; exit 65; }
    printf '%s\n' "$listing" | awk '
        /^File Type:/ { file = 1; types++; next }
        file && /^Total Size:/ {
            m = 1
            if ($4 == "KiB") m = 1024
            else if ($4 == "MiB") m = 1048576
            else if ($4 == "GiB") m = 1073741824
            else if ($4 == "TiB") m = 1099511627776
            total += $3 * m
            totals++
            file = 0
        }
        # Every file type must carry its total, or a format change reads as 0.
        END { if (!types || types != totals) exit 1; printf "%.0f\n", total }' || { echo "R2 size listing unreadable" >&2; exit 65; }
}

# "<id> <tree>" for each snapshot of the repository restic is pointed at.
snapshot_trees() {
    json="$(restic snapshots --json "$@")" || { echo "snapshot listing failed" >&2; exit 65; }
    printf '%s' "$json" | grep -oE '"(tree|id)":"[0-9a-f]{64}"' |
        awk -F'"' '$2 == "tree" { tree = $4; next } $2 == "id" && tree != "" { print $4, tree; tree = "" }'
}

# Compressed bytes the given snapshots of a local repository reference.
raw_bytes() {
    out="$(RESTIC_REPOSITORY="$repo" RESTIC_PASSWORD_FILE="$RESTIC_FROM_PASSWORD_FILE" \
        restic --no-lock stats --mode raw-data --json "$@")" || { echo "local size listing failed" >&2; exit 65; }
    value="$(printf '%s' "$out" | sed -n 's/.*"total_size":\([0-9]*\).*/\1/p')"
    [ -n "$value" ] || { echo "local size listing unreadable" >&2; exit 65; }
    echo "$value"
}

# Most a copy of /repo/$1 can add: the data of all its snapshots minus the
# data of those R2 already holds (same tree). Shared blobs only lower it.
pending_bytes() {
    repo="/repo/$1"
    pairs="$(RESTIC_REPOSITORY="$repo" RESTIC_PASSWORD_FILE="$RESTIC_FROM_PASSWORD_FILE" snapshot_trees --no-lock)"
    copied=""
    while read -r id tree; do
        [ -n "$id" ] || continue
        if printf '%s\n' "$remote_trees" | grep -qx "$tree"; then copied="$copied $id"; fi
    done <<EOF
$pairs
EOF
    all="$(raw_bytes)"
    base=0
    # shellcheck disable=SC2086 # one argument per snapshot ID.
    [ -n "$copied" ] && base="$(raw_bytes $copied)"
    echo $((all - base))
}

# Refuse the upload when the stored bytes plus the estimate (+5% for packing)
# could pass the cap. The size line still feeds the alert metric.
guard() {
    stored="$(stored_bytes)"
    projected=$((stored + $1 * 105 / 100))
    if [ "$projected" -gt "$max_bytes" ]; then
        echo "R2 repository size: $stored bytes"
        echo "refused: up to $projected bytes after this upload, cap $max_bytes (owner limit 10 GB)" >&2
        exit 66
    fi
}

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
        # Each step is its own assignment so set -e stops on any failure.
        remote_pairs="$(snapshot_trees)"
        remote_trees="$(printf '%s\n' "$remote_pairs" | cut -d' ' -f2)"
        pending=0
        for set in $SETS; do
            bytes="$(pending_bytes "$set")"
            # Fail closed even in a shell that does not stop on a failed substitution.
            case "$bytes" in '' | *[!0-9-]*) echo "pending size for $set unreadable" >&2; exit 65 ;; esac
            pending=$((pending + bytes))
        done
        guard "$pending"
        for set in $SETS; do
            restic copy --no-lock --from-repo "/repo/$set"
        done
        echo "R2 latest snapshots:"
        restic snapshots --compact --latest 1
        # Stored bytes, which R2 bills; the orchestrator turns this line into
        # hyhome_backup_offsite_repo_bytes.
        size="$(stored_bytes)"
        echo "R2 repository size: $size bytes"
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
        # --max-repack-size 0: prune only deletes whole unused packs and never
        # writes repacked ones, which could outgrow the cap under the lock.
        restic forget --prune --max-repack-size 0 --group-by host,tags --keep-within 30d --keep-monthly 12
        size="$(stored_bytes)"
        echo "R2 repository size: $size bytes"
        ;;
    artifact)
        # RUN-0105 W3b: store the W3 OpenBao snapshot and its receipt, mounted
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
        incoming=0
        for name in $files; do bytes="$(wc -c <"/artifact/$name" | tr -d ' ')"; incoming=$((incoming + bytes)); done
        guard "$incoming"
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
    restore)
        # RUN-0021 8.3: restore one paired host and state snapshot into an
        # owned, empty scratch mounted at /restore. Never writes to R2 (no
        # lock either); run it as the scratch owner (compose run --user).
        # Prints only per-set exit codes, seconds, file counts and bytes.
        if [ "$#" -ne 2 ]; then
            echo "restore needs <host-id> <state-id>" >&2
            exit 64
        fi
        host_id="$1"
        state_id="$2"
        for id in "$host_id" "$state_id"; do
            case "$id" in
                '' | *[!0-9a-f]*) echo "snapshot IDs must be lowercase hex" >&2; exit 64 ;;
            esac
            if [ "${#id}" -lt 8 ] || [ "${#id}" -gt 64 ]; then
                echo "snapshot IDs must be 8 to 64 hex characters" >&2
                exit 64
            fi
        done
        # Root here holds only DAC_READ_SEARCH and cannot write the scratch;
        # test -w would still say yes for uid 0.
        if [ "$(id -u)" -eq 0 ]; then
            echo "run restore as the scratch owner (compose run --user)" >&2
            exit 64
        fi
        if [ ! -d /restore ] || [ -L /restore ] || [ ! -w /restore ] ||
            [ -n "$(ls -A /restore)" ]; then
            echo "/restore must be an empty directory writable by this user" >&2
            exit 64
        fi
        # No cache: the scratch user's cache would be thrown away anyway.
        if ! restic --no-cache --no-lock cat config >/dev/null 2>&1; then
            echo "R2 repository is not initialized or not reachable; see RUN-0021 (Offsite copy)" >&2
            exit 65
        fi
        # An explicit ID bypasses --tag, so check each ID's tag first: a swapped
        # pair must not restore state into host.
        for pair in "$host_id hyhome-host" "$state_id hyhome-state"; do
            # shellcheck disable=SC2086 # two hex/tag words by construction.
            set -- $pair
            if ! restic --no-cache --no-lock snapshots --json --tag "$2" 2>/dev/null |
                grep -qE "\"(short_)?id\":\"$1"; then
                echo "snapshot $1 does not carry tag $2" >&2
                exit 64
            fi
        done
        rc=0
        for pair in "$host_id hyhome-host host" "$state_id hyhome-state state"; do
            # shellcheck disable=SC2086 # three words by construction.
            set -- $pair
            start="$(date +%s)"
            # Paths stay out of the output: restic and find errors are dropped.
            if restic --no-cache --no-lock restore "$1" --tag "$2" --target "/restore/$3" >/dev/null 2>&1; then
                set_rc=0
            else
                set_rc=$?
                rc=1
            fi
            files=0
            bytes=0
            if [ -d "/restore/$3" ]; then
                files="$(find "/restore/$3" -type f 2>/dev/null | wc -l)"
                bytes="$(du -sb "/restore/$3" 2>/dev/null | cut -f1)"
            fi
            echo "restore $3 snapshot=$1 rc=$set_rc seconds=$(($(date +%s) - start)) files=$files bytes=$bytes"
        done
        exit "$rc"
        ;;
    cmd)
        case "${1:-}" in
            forget | prune | unlock)
                echo "'$1' is not run directly; use forget-prune (RUN-0021 8.5)" >&2
                exit 64
                ;;
            snapshots | stats | ls | cat | find | check | diff | dump | list | version) ;;
            *)
                # Uploads go through copy or artifact, which check the cap. This
                # guards against mistakes; anyone with Docker access can still
                # run restic directly.
                echo "'${1:-}' may write to R2; cmd runs read-only commands only" >&2
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
