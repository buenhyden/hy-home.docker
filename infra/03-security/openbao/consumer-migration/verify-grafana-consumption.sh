#!/usr/bin/env bash
# P06 first-consumer check for the Grafana admin password. Compares the Agent-
# rendered bytes with Grafana's mounted secret and probes the admin login.
# Prints check names, PASS/FAIL, the KV version and the HTTP status only: no
# value, hash or length leaves the containers or reaches the terminal.
set -uo pipefail

agent=${OPENBAO_AGENT_CONTAINER:-openbao-agent}
grafana=${GRAFANA_CONTAINER:-grafana}
rendered=/openbao/out/observability/grafana_admin_password
mounted=/run/secrets/grafana_admin_password
failed=0

result() {
  if [ "$2" = 0 ]; then echo "PASS $1${3:+ $3}"; else echo "FAIL $1${3:+ $3}"; failed=1; fi
}

[ "$#" -eq 0 ] || { echo "usage: $0 (no arguments)" >&2; exit 2; }

version=$(timeout 10 docker exec "$agent" cat "$rendered.version" 2>/dev/null)
case "$version" in
  ''|0|*[!0-9]*) result rendered_version 1 ;;
  *) result rendered_version 0 "version=$version" ;;
esac

# Bytes stay in the two pipes; Grafana and Keycloak both strip CR/LF on read.
cmp -s \
  <(timeout 10 docker exec "$agent" cat "$rendered.txt" 2>/dev/null | tr -d '\r\n') \
  <(timeout 10 docker exec "$grafana" cat "$mounted" 2>/dev/null | tr -d '\r\n')
status=$?
# Two empty values would compare equal. The template emits no newline, so a
# non-empty rendered file plus equality proves a non-empty mounted value.
timeout 10 docker exec "$agent" test -s "$rendered.txt" 2>/dev/null || status=1
result mounted_equals_rendered "$status"

# The value is read and quoted inside Grafana; curl takes it from stdin, not argv.
# shellcheck disable=SC2016 # expands inside the container, not here
code=$(timeout 15 docker exec -e GRAFANA_PORT="${GRAFANA_PORT:-3000}" -e MOUNTED="$mounted" "$grafana" sh -c '
  p=$(tr -d "\r\n" <"$MOUNTED" | sed "s/[\\\\\"]/\\\\&/g")
  printf "user = \"%s:%s\"\n" "$GF_SECURITY_ADMIN_USER" "$p" |
    curl -sS -o /dev/null -w "%{http_code}" --max-time 5 -K - "http://127.0.0.1:$GRAFANA_PORT/api/user"
' 2>/dev/null)
[ "$code" = 200 ]
result admin_login $? "http=${code:-none}"

exit "$failed"
