#!/bin/sh
# Read-only host preflight; never prints certificates, keys, hashes or tool errors.
set +x
set -eu
umask 077
fail() { printf 'TLS_MATERIAL FAIL check=%s\n' "$1"; exit 1; }
[ "$#" -eq 2 ] || fail arguments
material=$1
[ "$2" = openbao/openbao:2.6.2 ] || fail image
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
# No network, persistent writes, pull or target service changes. Exact read-only files only.
timeout 20 docker run --rm --pull=never --network=none --user=100:1000 --read-only \
  --cap-drop=ALL --security-opt=no-new-privileges \
  --mount "type=bind,src=$material/ca.pem,dst=/tls/ca.pem,readonly" \
  --mount "type=bind,src=$material/server.pem,dst=/tls/server.pem,readonly" \
  --mount "type=bind,src=$material/server-key.pem,dst=/tls/server-key.pem,readonly" \
  --entrypoint /bin/sh "$2" -c 'for f in /tls/ca.pem /tls/server.pem /tls/server-key.pem; do [ -r "$f" ] && [ -s "$f" ] || exit 1; done' \
  >/dev/null 2>&1 || fail native-user-read
printf 'TLS_MATERIAL PASS checks=expiry,chain,SAN,key-match,native-user-read\n'
