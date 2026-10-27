#!/usr/bin/env bash
# P06 first-consumer check for the Grafana admin password. Compares the Agent-
# rendered bytes with Grafana's mounted secret and probes the admin login.
# Prints check names, PASS/FAIL, the KV version and the HTTP status only: no
# value, hash or length leaves the containers or reaches the terminal.
set -uo pipefail

agent=${OPENBAO_AGENT_CONTAINER:-openbao-agent}
grafana=${GRAFANA_CONTAINER:-grafana}
rendered=/openbao/out/observability/grafana_admin_password
failed=0

result() {
  if [ "$2" = 0 ]; then echo "PASS $1${3:+ $3}"; else echo "FAIL $1${3:+ $3}"; failed=1; fi
}

[ "$#" -eq 0 ] || { echo "usage: $0 (no arguments)" >&2; exit 2; }
port=${GRAFANA_PORT:-3000}
# A port such as "3000@host" would send the password elsewhere.
case "$port" in ''|*[!0-9]*) echo "GRAFANA_PORT must be digits" >&2; exit 2 ;; esac
for name in "$agent" "$grafana"; do
  case "$name" in [a-zA-Z0-9]*) ;; *) echo "invalid container name" >&2; exit 2 ;; esac
done
# Grafana's __FILE read drops trailing newlines only; CR and inner bytes count.
strip() { sed -z 's/\n*$//'; }

# The file Grafana actually reads: its Compose secret or the Agent directory bind.
mounted=$(timeout 10 docker exec "$grafana" printenv GF_SECURITY_ADMIN_PASSWORD__FILE 2>/dev/null)
case "$mounted" in
  /run/secrets/grafana_admin_password|/run/openbao/observability/grafana_admin_password.txt)
    result consumed_file 0 "path=$mounted" ;;
  *) result consumed_file 1; exit 1 ;;
esac

version=$(timeout 10 docker exec "$agent" cat "$rendered.version" 2>/dev/null)
case "$version" in
  ''|0|*[!0-9]*) result rendered_version 1 ;;
  *) result rendered_version 0 "version=$version" ;;
esac

# Bytes stay in the pipes; only a byte count reaches this shell, never printed.
cmp -s \
  <(timeout 10 docker exec "$agent" cat "$rendered.txt" 2>/dev/null | strip) \
  <(timeout 10 docker exec "$grafana" cat "$mounted" 2>/dev/null | strip)
status=$?
# Two empty values would compare equal, so require a non-empty rendered value.
size=$(timeout 10 docker exec "$agent" cat "$rendered.txt" 2>/dev/null | strip | wc -c)
[ "$size" -gt 0 ] || status=1
result mounted_equals_rendered "$status"

# The value is read and quoted inside Grafana; curl takes it from stdin, not argv.
# shellcheck disable=SC2016 # expands inside the container, not here
code=$(timeout 15 docker exec -e GRAFANA_PORT="$port" -e MOUNTED="$mounted" "$grafana" sh -c '
  q() { sed "s/[\\\\\"]/\\\\&/g"; }
  p=$(q <"$MOUNTED")
  u=$(printf "%s" "$GF_SECURITY_ADMIN_USER" | q)
  printf "user = \"%s:%s\"\n" "$u" "$p" |
    curl -sS -o /dev/null -w "%{http_code}" --max-time 5 -K - "http://127.0.0.1:$GRAFANA_PORT/api/user"
' 2>/dev/null)
[ "$code" = 200 ]
result admin_login $? "http=${code:-none}"

exit "$failed"
