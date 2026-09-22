#!/usr/bin/env bash
# Issue the private CA and certificates for SeaweedFS gRPC mutual TLS.
# The CA trusts only SeaweedFS components; it is not the browser-facing root.
# Existing material is kept unless --rotate is given (every component must be
# restarted after a rotation). Private keys are never printed.
# Usage: bin/gen-grpc-certs.sh [--rotate] [output-dir]
set -euo pipefail
umask 077

rotate=false
if [[ "${1:-}" == "--rotate" ]]; then
    rotate=true
    shift
fi
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
out="${1:-$repo_root/secrets/certs/seaweedfs}"
group="${SECRETS_GID:-$(id -g)}"
days=3650

files=(ca.crt master.crt master.key volume.crt volume.key filer.crt filer.key
       s3.crt s3.key client.crt client.key)
if [[ "$rotate" != true ]]; then
    present=0
    for file in "${files[@]}"; do [[ -e "$out/$file" ]] && present=$((present + 1)); done
    if (( present == ${#files[@]} )); then
        echo "certificates already exist in $out; pass --rotate to replace them"
        exit 0
    elif (( present > 0 )); then
        echo "incomplete certificate set in $out; rerun with --rotate" >&2
        exit 65
    fi
fi
mkdir -p "$out"
work="$(mktemp -d)"
trap 'rm -rf -- "$work"' EXIT

openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:P-256 -nodes \
    -keyout "$work/ca.key" -out "$work/ca.crt" -days "$days" \
    -subj "/CN=hy-home SeaweedFS gRPC CA" \
    -addext "basicConstraints=critical,CA:TRUE" \
    -addext "keyUsage=critical,keyCertSign,cRLSign" 2>/dev/null

for name in master volume filer s3 client; do
    openssl req -newkey ec -pkeyopt ec_paramgen_curve:P-256 -nodes \
        -keyout "$work/$name.key" -out "$work/$name.csr" \
        -subj "/CN=seaweedfs-$name" 2>/dev/null
    printf 'subjectAltName=DNS:seaweedfs-%s,DNS:localhost,IP:127.0.0.1\nextendedKeyUsage=serverAuth,clientAuth\n' \
        "$name" >"$work/$name.ext"
    openssl x509 -req -in "$work/$name.csr" -CA "$work/ca.crt" -CAkey "$work/ca.key" \
        -CAcreateserial -days "$days" -extfile "$work/$name.ext" \
        -out "$work/$name.crt" 2>/dev/null
done

# The CA key signs nothing after issuance; it stays out of the mounted set.
for file in "${files[@]}"; do
    install -m 0640 -g "$group" "$work/$file" "$out/$file"
done
echo "issued SeaweedFS gRPC certificates in $out (CA key discarded)"
