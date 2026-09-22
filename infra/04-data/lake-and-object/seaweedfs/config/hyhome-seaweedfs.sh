#!/bin/sh
# Start one SeaweedFS component with its security configuration built from
# Docker secrets and the mounted gRPC certificates, then exec weed.
#   security.toml: JWT keys for volume and filer HTTP (reads and writes), so
#     neither can be used directly to bypass S3 IAM; mTLS for every gRPC port.
#   s3.json (s3 only): admin plus the bucket-scoped identities in
#     s3-identities.conf; anonymous access exists only where that file grants it.
# Nothing here is written to a mounted path or printed.
# Usage: hyhome-seaweedfs.sh <master|volume|filer|s3|shell> [weed flags...]
set -eu
umask 077

component="${1:?component}"
shift
certs=/certs

read_secret() {
    file="/run/secrets/$1"
    if [ ! -f "$file" ] || [ -L "$file" ]; then
        echo "seaweedfs: secret $1 missing or not a regular file" >&2
        exit 64
    fi
    value="$(tr -d '\r\n' <"$file")"
    case "$value" in
        '' | *[!A-Za-z0-9]*)
            echo "seaweedfs: secret $1 must be non-empty and alphanumeric" >&2
            exit 64
            ;;
    esac
    printf '%s' "$value"
}

for name in ca master volume filer s3 client; do
    for ext in crt key; do
        [ "$name.$ext" = ca.key ] && continue
        if [ ! -f "$certs/$name.$ext" ]; then
            echo "seaweedfs: $certs/$name.$ext missing; run bin/gen-grpc-certs.sh" >&2
            exit 64
        fi
    done
done

volume_key="$(read_secret seaweedfs_jwt_volume_key)"
filer_key="$(read_secret seaweedfs_jwt_filer_key)"
{
    for section in jwt.signing jwt.signing.read; do
        printf '[%s]\nkey = "%s"\nexpires_after_seconds = 10\n' "$section" "$volume_key"
    done
    for section in jwt.filer_signing jwt.filer_signing.read; do
        printf '[%s]\nkey = "%s"\nexpires_after_seconds = 10\n' "$section" "$filer_key"
    done
    printf '[grpc]\nca = "%s/ca.crt"\n' "$certs"
    for name in master volume filer s3; do
        printf '[grpc.%s]\ncert = "%s/%s.crt"\nkey = "%s/%s.key"\n' \
            "$name" "$certs" "$name" "$certs" "$name"
    done
    printf '[grpc.client]\ncert = "%s/client.crt"\nkey = "%s/client.key"\n' "$certs" "$certs"
} >/etc/seaweedfs/security.toml
unset volume_key filer_key

case "$component" in
    s3)
        access="${SEAWEEDFS_S3_ADMIN_ACCESS_KEY:-}"
        case "$access" in
            '' | *[!A-Za-z0-9_-]*)
                echo "seaweedfs: SEAWEEDFS_S3_ADMIN_ACCESS_KEY must be set (letters, digits, _ or -)" >&2
                exit 64
                ;;
        esac
        admin_key="$(read_secret seaweedfs_s3_admin_secret_key)"
        {
            printf '{"identities":[{"name":"admin","credentials":[{"accessKey":"%s","secretKey":"%s"}],"actions":["Admin","Read","Write","List","Tagging"]}' \
                "$access" "$admin_key"
            grep -vE '^[[:space:]]*(#|$)' /opt/hyhome/s3-identities.conf | while read -r name secret actions; do
                case "$name" in '' | *[!a-z0-9-]*) echo "seaweedfs: bad identity name" >&2; exit 64 ;; esac
                case "$actions" in '' | *[!A-Za-z0-9:,.-]*) echo "seaweedfs: bad actions for $name" >&2; exit 64 ;; esac
                list="\"$(printf '%s' "$actions" | sed 's/,/","/g')\""
                if [ "$secret" = - ]; then
                    [ "$name" = anonymous ] || { echo "seaweedfs: only anonymous may have no secret" >&2; exit 64; }
                    printf ',{"name":"anonymous","actions":[%s]}' "$list"
                else
                    key="$(read_secret "$secret")"
                    printf ',{"name":"%s","credentials":[{"accessKey":"%s","secretKey":"%s"}],"actions":[%s]}' \
                        "$name" "$name" "$key" "$list"
                fi
            done
            printf ']}\n'
        } >/etc/seaweedfs/s3.json
        unset admin_key
        exec /usr/bin/weed -logtostderr=true s3 -config=/etc/seaweedfs/s3.json "$@"
        ;;
    master | volume | filer)
        exec /usr/bin/weed -logtostderr=true "$component" "$@"
        ;;
    shell)
        exec /usr/bin/weed shell "$@"
        ;;
    *)
        echo "seaweedfs: unknown component $component" >&2
        exit 64
        ;;
esac
