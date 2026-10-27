#!/usr/bin/env bash
# P06 consumer check for Grafana's Keycloak OIDC client secret. Compares the
# Agent-rendered bytes with the file Grafana reads and with the secret Keycloak
# holds for the client. Prints check names, PASS/FAIL, the KV version and the
# file path only: no value, hash or length leaves the containers or reaches the
# terminal.
set +x
set -uo pipefail

agent=${OPENBAO_AGENT_CONTAINER:-openbao-agent}
grafana=${GRAFANA_CONTAINER:-grafana}
keycloak=${KEYCLOAK_CONTAINER:-keycloak}
rendered=/openbao/out/observability/grafana_client_secret.txt
# The client secret shares the Grafana KV path and its version sentinel.
version_file=/openbao/out/observability/grafana_admin_password.version
failed=0

result() {
  if [ "$2" = 0 ]; then echo "PASS $1${3:+ $3}"; else echo "FAIL $1${3:+ $3}"; failed=1; fi
}

[ "$#" -eq 0 ] || { echo "usage: $0 (no arguments)" >&2; exit 2; }
port=${KEYCLOAK_PORT:-8080}
realm=${KEYCLOAK_REALM:-hy-home.realm}
case "$port" in ''|*[!0-9]*) echo "KEYCLOAK_PORT must be digits" >&2; exit 2 ;; esac
case "$realm" in ''|*[!a-zA-Z0-9._-]*) echo "invalid realm" >&2; exit 2 ;; esac
for name in "$agent" "$grafana" "$keycloak"; do
  case "$name" in [a-zA-Z0-9]*) ;; *) echo "invalid container name" >&2; exit 2 ;; esac
done
# Grafana's __FILE read drops trailing newlines only; CR and inner bytes count.
strip() { sed -z 's/\n*$//'; }

tries=${VERIFY_HEALTH_TRIES:-36}
for i in $(seq 1 "$tries"); do
  health=$(timeout 10 docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{end}}' "$grafana" 2>/dev/null)
  [ "$health" = healthy ] && break
  [ "$i" = 1 ] && echo "WAIT grafana_healthy"
  [ "$i" = "$tries" ] || sleep "${VERIFY_HEALTH_SLEEP:-5}"
done
[ "$health" = healthy ] || { result grafana_healthy 1 "state=${health:-none}"; exit 1; }
result grafana_healthy 0

mounted=$(timeout 10 docker exec "$grafana" printenv GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET__FILE 2>/dev/null)
case "$mounted" in
  /run/secrets/grafana_client_secret|/run/openbao/observability/grafana_client_secret.txt)
    result consumed_file 0 "path=$mounted" ;;
  *) result consumed_file 1; exit 1 ;;
esac
client=$(timeout 10 docker exec "$grafana" printenv GF_AUTH_GENERIC_OAUTH_CLIENT_ID 2>/dev/null)
case "$client" in ''|*[!a-zA-Z0-9._-]*) result client_id 1; exit 1 ;; esac

version=$(timeout 10 docker exec "$agent" cat "$version_file" 2>/dev/null)
case "$version" in
  ''|0|*[!0-9]*) result rendered_version 1 ;;
  *) result rendered_version 0 "version=$version" ;;
esac

# Bytes stay in the pipes; only a byte count reaches this shell, never printed.
cmp -s \
  <(timeout 10 docker exec "$agent" cat "$rendered" 2>/dev/null | strip) \
  <(timeout 10 docker exec "$grafana" cat "$mounted" 2>/dev/null | strip)
status=$?
size=$(timeout 10 docker exec "$agent" cat "$rendered" 2>/dev/null | strip | wc -c)
[ "$size" -gt 0 ] || status=1
result mounted_equals_rendered "$status"

# Grafana's file goes to Keycloak on stdin and is compared there with the secret
# Keycloak holds for the client, so Keycloak's copy never leaves its container.
# kcadm.sh logs in once as the admin through KC_CLI_PASSWORD, never argv; its
# token file is removed on exit. Prints one word: match, mismatch, empty,
# invalid (admin login rejected; do not re-run before finding why) or error.
keycloak_compare() {
  # shellcheck disable=SC2016 # expands inside the container, not here
  timeout 10 docker exec "$grafana" cat "$mounted" 2>/dev/null |
    timeout 180 docker exec -i -e KEYCLOAK_PORT="$port" -e REALM="$realm" -e CLIENT="$client" "$keycloak" sh -c '
      mounted=$(cat)
      [ -n "$mounted" ] || { echo empty; exit 0; }
      config=$(mktemp) || { echo error; exit 0; }
      trap "rm -f \"\$config\"" EXIT
      KC_CLI_PASSWORD=$(tr -d "\r\n" <"$KEYCLOAK_ADMIN_PASSWORD_FILE") || { echo error; exit 0; }
      export KC_CLI_PASSWORD
      kcadm() { timeout 50 /opt/keycloak/bin/kcadm.sh "$@" --config "$config"; }
      if ! out=$(kcadm config credentials --server "http://127.0.0.1:$KEYCLOAK_PORT" --realm master \
          --user "$KC_BOOTSTRAP_ADMIN_USERNAME" 2>&1); then
        case "$out" in *invalid_grant*) echo invalid ;; *) echo error ;; esac
        exit 0
      fi
      id=$(kcadm get clients -r "$REALM" -q clientId="$CLIENT" --fields id --format csv --noquotes 2>/dev/null)
      case "$id" in ""|*[!a-zA-Z0-9-]*) echo error; exit 0 ;; esac
      secret=$(kcadm get "clients/$id/client-secret" -r "$REALM" --fields value --format csv --noquotes 2>/dev/null) ||
        { echo error; exit 0; }
      [ -n "$secret" ] || { echo empty; exit 0; }
      # Command substitution drops trailing newlines on both sides, as Grafana does.
      if [ "$secret" = "$mounted" ]; then echo match; else echo mismatch; fi
    ' 2>/dev/null
}
word=$(keycloak_compare)
case "$word" in match|mismatch|empty|invalid|error) ;; *) word=none ;; esac
[ "$word" = match ]
result keycloak_client_matches $? "client=$client kcadm=$word"

exit "$failed"
