#!/usr/bin/env bash
# P06 consumer check for the Keycloak admin password. Compares the Agent-
# rendered bytes with the file Keycloak reads and logs in with kcadm.sh.
# Prints check names, PASS/FAIL, the KV version and the login result only: no
# value, hash or length leaves the containers or reaches the terminal.
set -uo pipefail

agent=${OPENBAO_AGENT_CONTAINER:-openbao-agent}
keycloak=${KEYCLOAK_CONTAINER:-keycloak}
rendered=/openbao/out/auth/keycloak_admin_password
failed=0

result() {
  if [ "$2" = 0 ]; then echo "PASS $1${3:+ $3}"; else echo "FAIL $1${3:+ $3}"; failed=1; fi
}

[ "$#" -eq 0 ] || { echo "usage: $0 (no arguments)" >&2; exit 2; }
port=${KEYCLOAK_PORT:-8080}
# A port such as "8080@host" would send the password elsewhere.
case "$port" in ''|*[!0-9]*) echo "KEYCLOAK_PORT must be digits" >&2; exit 2 ;; esac
for name in "$agent" "$keycloak"; do
  case "$name" in [a-zA-Z0-9]*) ;; *) echo "invalid container name" >&2; exit 2 ;; esac
done
# The entrypoint reads the file through tr -d '\r\n': every CR and LF is dropped.
strip() { tr -d '\r\n'; }

# Keycloak can take about 4 minutes to become healthy after a recreate that
# rebuilds (HOME, 2026-10-27), so wait up to 360 s.
tries=${VERIFY_HEALTH_TRIES:-72}
for i in $(seq 1 "$tries"); do
  health=$(timeout 10 docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{end}}' "$keycloak" 2>/dev/null)
  [ "$health" = healthy ] && break
  [ "$i" = 1 ] && echo "WAIT keycloak_healthy"
  [ "$i" = "$tries" ] || sleep "${VERIFY_HEALTH_SLEEP:-5}"
done
[ "$health" = healthy ] || { result keycloak_healthy 1 "state=${health:-none}"; exit 1; }
result keycloak_healthy 0

# The file Keycloak actually reads: its Compose secret or the Agent directory bind.
mounted=$(timeout 10 docker exec "$keycloak" printenv KEYCLOAK_ADMIN_PASSWORD_FILE 2>/dev/null)
case "$mounted" in
  /run/secrets/keycloak_admin_password|/run/openbao/auth/keycloak_admin_password.txt)
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
  <(timeout 10 docker exec "$keycloak" cat "$mounted" 2>/dev/null | strip)
status=$?
# Two empty values would compare equal, so require a non-empty rendered value.
size=$(timeout 10 docker exec "$agent" cat "$rendered.txt" 2>/dev/null | strip | wc -c)
[ "$size" -gt 0 ] || status=1
result mounted_equals_rendered "$status"

# Keycloak has no curl. kcadm.sh takes the password from KC_CLI_PASSWORD, set
# inside the container, never from argv; its token goes to a removed temp file.
# Prints ok, invalid (the server rejected the credentials) or error.
login() {
  # shellcheck disable=SC2016 # expands inside the container, not here
  timeout 90 docker exec -e KEYCLOAK_PORT="$port" -e MOUNTED="$mounted" "$keycloak" sh -c '
    config=$(mktemp) || { echo error; exit 0; }
    trap "rm -f \"\$config\"" EXIT
    KC_CLI_PASSWORD=$(tr -d "\r\n" <"$MOUNTED") || { echo error; exit 0; }
    export KC_CLI_PASSWORD
    # The inner timeout stops kcadm itself, so no attempt outlives its retry.
    if out=$(timeout 80 /opt/keycloak/bin/kcadm.sh config credentials --config "$config" \
        --server "http://127.0.0.1:$KEYCLOAK_PORT" --realm master \
        --user "$KC_BOOTSTRAP_ADMIN_USERNAME" 2>&1); then
      echo ok
    else
      case "$out" in *invalid_grant*) echo invalid ;; *) echo error ;; esac
    fi
  ' 2>/dev/null
}
# Retry only when the server gave no answer; a rejection is final so a wrong
# password never counts against brute-force protection twice.
for attempt in 1 2 3; do
  code=$(login)
  case "$code" in ok|invalid) break ;; esac
  [ "$attempt" = 3 ] || sleep "${VERIFY_RETRY_SLEEP:-10}"
done
[ "$code" = ok ]
result admin_login $? "kcadm=${code:-none}"

exit "$failed"
