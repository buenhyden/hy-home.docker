#!/usr/bin/env bash
set -Eeuo pipefail

umask 077

fail() {
  printf 'open-webui-oidc-entrypoint: %s\n' "$1" >&2
  exit 1
}

require_readable_file() {
  local label="$1"
  local path="$2"
  [[ -f "$path" && -r "$path" && -s "$path" ]] || fail "$label is missing, unreadable, or empty"
}

secret_file="${OPENWEBUI_OIDC_CLIENT_SECRET_FILE:-/run/secrets/openwebui_oidc_client_secret}"
root_ca_file="${OPENWEBUI_ROOT_CA_FILE:-/etc/ssl/certs/hy-home-rootCA.pem}"

require_readable_file "OIDC client secret" "$secret_file"
require_readable_file "local root CA certificate" "$root_ca_file"

declare -a secret_lines=()
mapfile -t secret_lines <"$secret_file"
[[ "${#secret_lines[@]}" -eq 1 ]] || fail "OIDC client secret must contain exactly one line"
oauth_client_secret="${secret_lines[0]}"
unset secret_lines
[[ -n "$oauth_client_secret" ]] || fail "OIDC client secret is empty"
if [[ "$oauth_client_secret" == *$'\r'* ]]; then
  fail "OIDC client secret must not contain carriage returns"
fi

if [[ -n "${OPENWEBUI_PUBLIC_CA_FILE:-}" ]]; then
  public_ca_file="$OPENWEBUI_PUBLIC_CA_FILE"
else
  command -v python >/dev/null 2>&1 || fail "python is unavailable for public CA discovery"
  public_ca_file="$(python -c 'import certifi; print(certifi.where())')" ||
    fail "public CA discovery failed"
fi
require_readable_file "public CA bundle" "$public_ca_file"

ca_bundle="${TMPDIR:-/tmp}/open-webui-ca-bundle.pem"
[[ ! -d "$ca_bundle" ]] || fail "CA bundle path is a directory"
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

export OAUTH_CLIENT_SECRET="$oauth_client_secret"
export SSL_CERT_FILE="$ca_bundle"
export REQUESTS_CA_BUNDLE="$ca_bundle"

if [[ "$#" -eq 0 ]]; then
  set -- bash start.sh
fi

exec "$@"
