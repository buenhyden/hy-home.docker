#!/bin/bash
# Copy MinIO buckets to SeaweedFS through the S3 API (SPEC-0180 S07).
#   BUCKETS=<names>  buckets to copy; each must already exist on SeaweedFS
#   (default)        adds objects SeaweedFS lacks; never overwrites or deletes
#   FINAL=1          with the consumer stopped: overwrite changed objects,
#                    delete objects MinIO no longer has, require identical
#                    key/size listings, then record the cutover marker
# After FINAL a bucket belongs to its consumer: every later run for it is
# refused (marker hyhome-migration/<bucket>.cutover), because a copy would
# replace objects the consumer wrote since. Credentials reach mc through its
# config file, never argv. Only bash built-ins, coreutils and mc are used:
# the MinIO image has no awk, sed or grep.
set -euo pipefail

fail() { echo "seaweedfs-migrate: $*" >&2; exit 64; }
read_secret() {
    [[ -f "$1" && ! -L "$1" ]] || fail "missing secret $1"
    local value
    value="$(tr -d '\r\n' <"$1")"
    [[ -n "$value" && "$value" != *'"'* && "$value" != *\\* ]] || fail "$1 is empty or has a quote or backslash"
    printf '%s' "$value"
}
[[ -n "${BUCKETS:-}" ]] || fail "set BUCKETS"
[[ "${SEAWEEDFS_S3_ADMIN_ACCESS_KEY:-}" =~ ^[A-Za-z0-9_-]+$ ]] || fail "bad admin access key"
final="${FINAL:-0}"

export MC_CONFIG_DIR=/tmp/.mc
mkdir -p "$MC_CONFIG_DIR"
umask 077
src_user="$(read_secret /run/secrets/minio_root_username)"
src_pass="$(read_secret /run/secrets/minio_root_password)"
dst_pass="$(read_secret /run/secrets/seaweedfs_s3_admin_secret_key)"
printf '{"version":"10","aliases":{"src":{"url":"http://minio:9000","accessKey":"%s","secretKey":"%s","api":"s3v4","path":"auto"},"dst":{"url":"http://seaweedfs-s3:8333","accessKey":"%s","secretKey":"%s","api":"s3v4","path":"on"}}}\n' \
    "$src_user" "$src_pass" "$SEAWEEDFS_S3_ADMIN_ACCESS_KEY" "$dst_pass" >"$MC_CONFIG_DIR/config.json"
unset src_user src_pass dst_pass

# Sorted "key<TAB>size" lines; fails when mc fails.
listing() {
    local out line key size
    out="$(mc ls --recursive --json "$1")" || return 1
    while IFS= read -r line; do
        [[ $line == *'"type":"file"'* ]] || continue
        [[ $line =~ \"key\":\"([^\"]*)\" ]] || return 1
        key="${BASH_REMATCH[1]}"
        [[ $line =~ \"size\":([0-9]+) ]] || return 1
        size="${BASH_REMATCH[1]}"
        printf '%s\t%s\n' "$key" "$size"
    done <<<"$out" | sort
}
totals() {
    local count=0 bytes=0 key size
    while IFS=$'\t' read -r key size; do
        [[ -n "$key" ]] || continue
        count=$((count + 1)); bytes=$((bytes + size))
    done <<<"$1"
    printf '%d objects, %d bytes' "$count" "$bytes"
}

mc mb --ignore-existing dst/hyhome-migration >/dev/null
status=0
for bucket in $BUCKETS; do
    if mc stat "dst/hyhome-migration/$bucket.cutover" >/dev/null 2>&1; then
        echo "$bucket: already cut over; refusing to copy over consumer writes" >&2
        status=1
        continue
    fi
    mc stat "dst/$bucket" >/dev/null || fail "$bucket missing on SeaweedFS (run seaweedfs-buckets)"
    flags=(--preserve)
    [[ "$final" == 1 ]] && flags+=(--overwrite --remove)
    mc mirror --quiet "${flags[@]}" "src/$bucket" "dst/$bucket" >/dev/null
    src_list="$(listing "src/$bucket")" || fail "$bucket: MinIO listing failed"
    dst_list="$(listing "dst/$bucket")" || fail "$bucket: SeaweedFS listing failed"
    echo "$bucket: minio $(totals "$src_list"); seaweedfs $(totals "$dst_list")"
    if [[ "$final" == 1 ]]; then
        if [[ "$src_list" != "$dst_list" ]]; then
            echo "$bucket: MISMATCH in keys or sizes; marker not written" >&2
            status=1
            continue
        fi
        printf 'cutover %s\n' "$(date -u +%FT%TZ)" | mc pipe "dst/hyhome-migration/$bucket.cutover" >/dev/null
        echo "$bucket: final copy verified; cutover marker written"
    fi
done
exit "$status"
