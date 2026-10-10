#!/bin/sh
# Fetch, exact rendered bytes and KV version; application consumption is separate.
set +x
set -eu
exec >/dev/null 2>&1

[ "$#" -eq 0 ] || exit 1
case "${VAULT_ADDR:-}" in
  https://?*) ;;
  *) exit 1 ;;
esac
case "$VAULT_ADDR" in
  *[[:space:]]*|*@*|*\?*|*\#*) exit 1 ;;
esac
[ -z "${VAULT_SKIP_VERIFY:-}${BAO_SKIP_VERIFY:-}" ] || exit 1
[ -n "${VAULT_CACERT:-}" ] && [ -f "$VAULT_CACERT" ] && [ -r "$VAULT_CACERT" ] || exit 1
[ -f /openbao/agent/token ] && [ ! -L /openbao/agent/token ] && [ -s /openbao/agent/token ] || exit 1
[ "$(stat -c %a /openbao/agent/token)" = 600 ] || exit 1
BAO_TOKEN=$(cat /openbao/agent/token)
case "$BAO_TOKEN" in
  ''|*[!a-zA-Z0-9._-]*) exit 1 ;;
esac
export BAO_TOKEN BAO_ADDR="$VAULT_ADDR" BAO_CACERT="$VAULT_CACERT"
unset VAULT_TOKEN
timeout 3 bao status || exit 1
timeout 3 bao token lookup -format=json || exit 1
timeout 3 bao kv get -field=admin_password secret/hy-home/02-auth/keycloak || exit 1
timeout 3 bao kv get -field=admin_password secret/hy-home/06-observability/grafana || exit 1
for rendered in /openbao/out/auth/keycloak_admin_password /openbao/out/observability/grafana_admin_password; do
  [ -f "$rendered.txt" ] && [ ! -L "$rendered.txt" ] && [ -s "$rendered.txt" ] || exit 1
  [ -f "$rendered.version" ] && [ ! -L "$rendered.version" ] && [ -s "$rendered.version" ] || exit 1
  [ "$(stat -c %a "$rendered.txt")" = 600 ] || exit 1
  [ "$(stat -c %a "$rendered.version")" = 600 ] || exit 1
done
timeout 3 bao kv get -field=admin_password secret/hy-home/02-auth/keycloak | cmp -s - /openbao/out/auth/keycloak_admin_password.txt || exit 1
timeout 3 bao kv get -field=admin_password secret/hy-home/06-observability/grafana | cmp -s - /openbao/out/observability/grafana_admin_password.txt || exit 1
keycloak_version=$(timeout 3 bao read -field=current_version secret/metadata/hy-home/02-auth/keycloak) || exit 1
grafana_version=$(timeout 3 bao read -field=current_version secret/metadata/hy-home/06-observability/grafana) || exit 1
for version in "$keycloak_version" "$grafana_version"; do
  case "$version" in ''|0|*[!0-9]*) exit 1 ;; esac
done
[ "$keycloak_version" = "$(cat /openbao/out/auth/keycloak_admin_password.version)" ] || exit 1
[ "$grafana_version" = "$(cat /openbao/out/observability/grafana_admin_password.version)" ]
