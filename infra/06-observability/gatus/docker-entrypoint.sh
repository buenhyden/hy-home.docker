#!/bin/sh
set -eu

umask 077

fail() {
  printf 'gatus-oidc-entrypoint: %s\n' "$1" >&2
  exit 1
}

require_readable_file() {
  label="$1"
  path="$2"
  [ -f "$path" ] && [ -r "$path" ] && [ -s "$path" ] ||
    fail "$label is missing, unreadable, or empty"
}

secret_file="${GATUS_OIDC_CLIENT_SECRET_FILE:-/run/secrets/gatus_oidc_client_secret}"
root_ca_file="${GATUS_ROOT_CA_FILE:-/etc/ssl/certs/hy-home-rootCA.pem}"
public_ca_file="${GATUS_PUBLIC_CA_FILE:-/etc/ssl/certs/ca-certificates.crt}"

require_readable_file "OIDC client secret" "$secret_file"
require_readable_file "local root CA certificate" "$root_ca_file"
require_readable_file "public CA bundle" "$public_ca_file"
[ -n "${DEFAULT_URL:-}" ] || fail "DEFAULT_URL is empty"
[ -n "${GATUS_OIDC_ALLOWED_SUBJECT:-}" ] ||
  fail "GATUS_OIDC_ALLOWED_SUBJECT is empty"

oauth_client_secret="$(cat "$secret_file")"
[ -n "$oauth_client_secret" ] || fail "OIDC client secret is empty"
secret_line_count="$(awk 'END { print NR }' "$secret_file")"
[ "$secret_line_count" -le 1 ] || fail "OIDC client secret must contain one line"
case "$oauth_client_secret" in
  *"$(printf '\r')"*) fail "OIDC client secret must not contain carriage returns" ;;
esac

ca_bundle="${TMPDIR:-/tmp}/gatus-ca-bundle.pem"
[ ! -d "$ca_bundle" ] || fail "CA bundle path is a directory"
ca_bundle_temp="$(mktemp "${ca_bundle}.XXXXXX")" ||
  fail "could not create temporary CA bundle"
cleanup() {
  rm -f -- "$ca_bundle_temp"
}
trap cleanup EXIT HUP INT TERM

{
  cat "$public_ca_file"
  printf '\n'
  cat "$root_ca_file"
  printf '\n'
} >"$ca_bundle_temp"
chmod 0600 "$ca_bundle_temp"
mv -f -- "$ca_bundle_temp" "$ca_bundle"

export GATUS_OIDC_CLIENT_SECRET="$oauth_client_secret"
export SSL_CERT_FILE="$ca_bundle"

exec "$@"
