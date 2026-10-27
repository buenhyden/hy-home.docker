#!/usr/bin/env bash
# P06 consumer check for one service's Keycloak OIDC client secret. Compares the
# Agent-rendered bytes with the file the service reads and with the secret
# Keycloak holds for the client. Prints check names, PASS/FAIL, the KV version,
# the file path and the client ID only: no value, hash or length leaves the
# containers or reaches the terminal.
set +x
set -uo pipefail

usage() {
  echo "usage: $0 oauth2-proxy|opensearch-dashboards|kafbat-ui|dozzle|gatus|airflow-apiserver|open-webui|superset" >&2
  exit 2
}
[ "$#" -eq 1 ] || usage
service=$1
# Each service: its Compose secret, the Agent directory and file stem, the
# variable that holds the path it reads, and where its client ID comes from.
# Airflow reads the secret through a `cat <path>` command variable.
client_env='' client_id='' command=''
case "$service" in
  oauth2-proxy) secret=oauth2_proxy_client_secret dir=oauth2-proxy stem=oauth2_proxy_client_secret
    path_env=OAUTH2_PROXY_CLIENT_SECRET_FILE client_env=OAUTH2_PROXY_CLIENT_ID ;;
  opensearch-dashboards) secret=oauth2_proxy_client_secret dir=oauth2-proxy stem=oauth2_proxy_client_secret
    path_env=OPENSEARCH_OIDC_CLIENT_SECRET_FILE client_id=realm-home-client ;;
  kafbat-ui) secret=kafbat_client_secret dir=kafbat stem=kafbat_client_secret
    path_env=KAFBAT_CLIENT_SECRET_FILE client_env=KAFBAT_OAUTH_CLIENT_ID ;;
  dozzle) secret=dozzle_client_secret dir=dozzle stem=dozzle_client_secret
    path_env=DOZZLE_AUTH_OIDC_CLIENT_SECRET_FILE client_env=DOZZLE_AUTH_OIDC_CLIENT_ID ;;
  gatus) secret=gatus_oidc_client_secret dir=gatus stem=gatus_oidc_client_secret
    path_env=GATUS_OIDC_CLIENT_SECRET_FILE client_id=home-gatus ;;
  airflow-apiserver) secret=airflow_keycloak_client_secret dir=airflow stem=airflow_client_secret
    path_env=AIRFLOW__KEYCLOAK_AUTH_MANAGER__CLIENT_SECRET_CMD command=cat
    client_env=AIRFLOW__KEYCLOAK_AUTH_MANAGER__CLIENT_ID ;;
  open-webui) secret=openwebui_oidc_client_secret dir=open-webui stem=openwebui_oidc_client_secret
    path_env=OPENWEBUI_OIDC_CLIENT_SECRET_FILE client_env=OAUTH_CLIENT_ID ;;
  superset) secret=superset_oidc_client_secret dir=superset stem=superset_oidc_client_secret
    path_env=SUPERSET_OIDC_CLIENT_SECRET_FILE client_env=SUPERSET_OIDC_CLIENT_ID ;;
  *) usage ;;
esac
agent=${OPENBAO_AGENT_CONTAINER:-openbao-agent}
keycloak=${KEYCLOAK_CONTAINER:-keycloak}
rendered=/openbao/out/$dir/$stem
port=${KEYCLOAK_PORT:-8080}
realm=${KEYCLOAK_REALM:-hy-home.realm}
case "$port" in ''|*[!0-9]*) echo "KEYCLOAK_PORT must be digits" >&2; exit 2 ;; esac
case "$realm" in ''|*[!a-zA-Z0-9._-]*) echo "invalid realm" >&2; exit 2 ;; esac
for name in "$agent" "$keycloak"; do
  case "$name" in [a-zA-Z0-9]*) ;; *) echo "invalid container name" >&2; exit 2 ;; esac
done
failed=0
result() {
  if [ "$2" = 0 ]; then echo "PASS $1${3:+ $3}"; else echo "FAIL $1${3:+ $3}"; failed=1; fi
}
# Only the trailing newlines differ between how the consumers read the file.
strip() { sed -z 's/\n*$//'; }
# One variable from the container configuration; the other variables stay in the pipe.
setting() {
  timeout 10 docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' "$service" 2>/dev/null |
    sed -n "s/^$1=//p" | head -n 1
}
# Read through `docker cp`: some images have no shell or cat.
mounted_bytes() { timeout 10 docker cp "$service:$mounted" - 2>/dev/null | tar -xO 2>/dev/null; }

tries=${VERIFY_HEALTH_TRIES:-72}
for i in $(seq 1 "$tries"); do
  health=$(timeout 10 docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$service" 2>/dev/null)
  case "$health" in healthy|running) break ;; esac
  [ "$i" = 1 ] && echo "WAIT healthy"
  [ "$i" = "$tries" ] || sleep "${VERIFY_HEALTH_SLEEP:-5}"
done
case "$health" in healthy|running) result healthy 0 "service=$service" ;;
  *) result healthy 1 "state=${health:-none}"; exit 1 ;; esac

mounted=$(setting "$path_env")
[ -z "$command" ] || mounted=${mounted#"$command "}
case "$mounted" in
  "/run/secrets/$secret"|"/run/openbao/$dir/$stem.txt") result consumed_file 0 "path=$mounted" ;;
  *) result consumed_file 1; exit 1 ;;
esac
[ -n "$client_id" ] || client_id=$(setting "$client_env")
case "$client_id" in ''|*[!a-zA-Z0-9._-]*) result client_id 1; exit 1 ;; esac

version=$(timeout 10 docker exec "$agent" cat "$rendered.version" 2>/dev/null)
case "$version" in
  ''|0|*[!0-9]*) result rendered_version 1 ;;
  *) result rendered_version 0 "version=$version" ;;
esac

# Bytes stay in the pipes; only a byte count reaches this shell, never printed.
cmp -s <(timeout 10 docker exec "$agent" cat "$rendered.txt" 2>/dev/null | strip) <(mounted_bytes | strip)
status=$?
size=$(timeout 10 docker exec "$agent" cat "$rendered.txt" 2>/dev/null | strip | wc -c)
[ "$size" -gt 0 ] || status=1
result mounted_equals_rendered "$status"

# The service's file goes to Keycloak on stdin and is compared there with the
# secret Keycloak holds for the client, so Keycloak's copy never leaves its
# container. kcadm.sh logs in once as the admin through KC_CLI_PASSWORD, never
# argv. Prints one word: match, mismatch, empty, invalid (admin login rejected;
# do not re-run before finding why) or error.
keycloak_compare() {
  # shellcheck disable=SC2016 # expands inside the container, not here
  mounted_bytes |
    timeout 180 docker exec -i -e KEYCLOAK_PORT="$port" -e REALM="$realm" -e CLIENT="$client_id" "$keycloak" sh -c '
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
      if [ "$secret" = "$mounted" ]; then echo match; else echo mismatch; fi
    ' 2>/dev/null
}
word=$(keycloak_compare)
case "$word" in match|mismatch|empty|invalid|error) ;; *) word=none ;; esac
[ "$word" = match ]
result keycloak_client_matches $? "client=$client_id kcadm=$word"

exit "$failed"
