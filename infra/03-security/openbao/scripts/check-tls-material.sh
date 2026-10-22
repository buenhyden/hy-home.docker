#!/bin/sh
# Read-only host preflight; never prints certificates, keys, hashes or tool errors.
set +x
set -eu
umask 077
fail() { printf 'TLS_MATERIAL FAIL check=%s\n' "$1"; exit 1; }
[ "$#" -eq 2 ] || fail arguments
material=$1
[ "$2" = hy-home/openbao:2.7.1-go1.27.3-net0.60.0-r1@sha256:a58fb1109971e506e9de1a360aec48ae07af7b6ccf409f8bac329e30e8fde8c8 ] || fail image
case "$material" in /*) ;; *) fail absolute-path ;; esac
[ ! -L "$material" ] || fail directory-symlink
for name in ca.pem server.pem server-key.pem; do
  path="$material/$name"
  if [ ! -f "$path" ] || [ ! -r "$path" ] || [ ! -s "$path" ] || [ -L "$path" ]; then
    fail material-file
  fi
done
command -v openssl >/dev/null 2>&1 || fail openssl
command -v timeout >/dev/null 2>&1 || fail timeout
timeout 10 openssl x509 -in "$material/ca.pem" -checkend 0 -noout >/dev/null 2>&1 || fail ca-expiry
timeout 10 openssl x509 -in "$material/server.pem" -checkend 0 -noout >/dev/null 2>&1 || fail server-expiry
timeout 10 openssl verify -CAfile "$material/ca.pem" -purpose sslserver -verify_hostname openbao "$material/server.pem" >/dev/null 2>&1 || fail chain-san
timeout 10 openssl verify -CAfile "$material/ca.pem" -purpose sslserver -verify_ip 127.0.0.1 "$material/server.pem" >/dev/null 2>&1 || fail loopback-san
san=$(timeout 10 openssl x509 -in "$material/server.pem" -noout -ext subjectAltName 2>/dev/null) || fail san
printf '%s\n' "$san" | grep -Eq '(^|[ ,])DNS:openbao([ ,]|$)' || fail san
unset san
cert_public=$(timeout 10 openssl x509 -in "$material/server.pem" -pubkey -noout 2>/dev/null) || fail cert-public
key_public=$(timeout 10 openssl pkey -in "$material/server-key.pem" -pubout -passin pass: 2>/dev/null) || fail key-public
[ -n "$cert_public" ] && [ "$cert_public" = "$key_public" ] || fail key-match
unset cert_public key_public
# Track this invocation independently of --rm, including a timeout before cidfile delivery.
probe_directory=$(mktemp -d /tmp/openbao-tls.XXXXXXXXXX 2>/dev/null) || fail native-user-tracking
probe_name=${probe_directory##*/}
printf '%s\n' "$probe_name" "hyhome.openbao.tls-probe=$probe_name" 2>/dev/null >"$probe_directory/identity" || fail native-user-tracking
owned_container() {
  timeout --kill-after=5 10 docker container ls --all --quiet --no-trunc \
    --filter "name=^/$probe_name$" --filter "label=hyhome.openbao.tls-probe=$probe_name" 2>/dev/null
}
cleanup_probe() {
  owned=$(owned_container) || return 1
  if [ -n "$owned" ]; then
    [ "${#owned}" -eq 64 ] || return 1
    case "$owned" in *[!a-f0-9]*) return 1 ;; esac
    timeout --kill-after=5 10 docker container rm --force "$owned" >/dev/null 2>&1 || return 1
    owned=$(owned_container) || return 1
    [ -z "$owned" ] || return 1
  fi
  # A failed client can leave a daemon create pending after an empty listing.
  [ "$1" -eq 0 ] || return 0
  rm -f "$probe_directory/cid" "$probe_directory/identity" >/dev/null 2>&1 && rmdir "$probe_directory" >/dev/null 2>&1
}
finish_probe() {
  trap - 0 HUP INT TERM
  # Keep tracking metadata on unverified cleanup; never print tool output or material.
  cleanup_probe "$1" || fail native-user-cleanup
  if [ "$1" -ne 0 ]; then
    printf 'TLS_MATERIAL FAIL check=native-user-read cleanup=pending-reconciliation\n'
    exit 1
  fi
  printf 'TLS_MATERIAL PASS checks=expiry,chain,SAN,key-match,native-user-read\n'
  exit 0
}
trap 'finish_probe 1' 0 HUP INT TERM
# No network, persistent data writes, pull or target service changes. Exact read-only files only.
native_status=0
timeout --kill-after=5 60 docker run --rm --cidfile "$probe_directory/cid" \
  --name "$probe_name" --label "hyhome.openbao.tls-probe=$probe_name" \
  --pull=never --network=none --user=100:1000 --read-only \
  --cap-drop=ALL --security-opt=no-new-privileges \
  --mount "type=bind,src=$material/ca.pem,dst=/tls/ca.pem,readonly" \
  --mount "type=bind,src=$material/server.pem,dst=/tls/server.pem,readonly" \
  --mount "type=bind,src=$material/server-key.pem,dst=/tls/server-key.pem,readonly" \
  --entrypoint /bin/sh "$2" -c 'for f in /tls/ca.pem /tls/server.pem /tls/server-key.pem; do [ -r "$f" ] && [ -s "$f" ] || exit 1; done' \
  >/dev/null 2>&1 || native_status=$?
finish_probe "$native_status"
