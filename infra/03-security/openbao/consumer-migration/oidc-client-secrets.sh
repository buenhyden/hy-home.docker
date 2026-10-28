#!/usr/bin/env bash
# Owner steps of the OIDC client secret batch (README "OIDC client secret 일괄 전환").
# import: first KV write of each client secret from ./secrets, through stdin.
# prepare: the Agent output directories, needed before the main checkout gets the binds.
# cutover/rollback: one service's path variable in .env, recreate, then the verifier.
# No value, hash or length is printed.
set +x
set -uo pipefail

usage() {
  echo "usage: $0 import <token-file>|prepare|cutover <service>|rollback <service>" >&2
  exit 2
}
[ "$#" -ge 1 ] || usage
HOME_ROOT=${OIDC_HOME_ROOT:-/home/hyunyoun/data/hy-home.docker}
here=$(cd "$(dirname "$0")" && pwd)
# KV path, ./secrets file, Agent directory/file.
SECRETS='02-auth/oauth2-proxy auth/oauth2-proxy/oauth2_proxy_client_secret.txt oauth2-proxy/oauth2_proxy_client_secret.txt
05-messaging/kafbat auth/kafbat/kafbat_client_secret.txt kafbat/kafbat_client_secret.txt
06-observability/dozzle auth/dozzle/dozzle_client_secret.txt dozzle/dozzle_client_secret.txt
06-observability/gatus auth/gatus/gatus_oidc_client_secret.txt gatus/gatus_oidc_client_secret.txt
07-workflow/airflow auth/airflow/airflow_client_secret.txt airflow/airflow_client_secret.txt
08-ai/open-webui auth/open-webui/openwebui_oidc_client_secret.txt open-webui/openwebui_oidc_client_secret.txt
12-analytics/superset auth/superset/superset_oidc_client_secret.txt superset/superset_oidc_client_secret.txt'
# Compose service -> .env path variable and Agent file.
service_row() {
  case "$1" in
    oauth2-proxy) echo "OAUTH2_PROXY_CLIENT_SECRET_FILE oauth2-proxy/oauth2_proxy_client_secret.txt" ;;
    opensearch-dashboards) echo "OPENSEARCH_OIDC_CLIENT_SECRET_FILE oauth2-proxy/oauth2_proxy_client_secret.txt" ;;
    kafbat-ui) echo "KAFBAT_CLIENT_SECRET_FILE kafbat/kafbat_client_secret.txt" ;;
    dozzle) echo "DOZZLE_CLIENT_SECRET_FILE dozzle/dozzle_client_secret.txt" ;;
    gatus) echo "GATUS_CLIENT_SECRET_FILE gatus/gatus_oidc_client_secret.txt" ;;
    airflow-apiserver) echo "AIRFLOW_CLIENT_SECRET_FILE airflow/airflow_client_secret.txt" ;;
    open-webui) echo "OPENWEBUI_OIDC_CLIENT_SECRET_FILE open-webui/openwebui_oidc_client_secret.txt" ;;
    superset) echo "SUPERSET_OIDC_CLIENT_SECRET_FILE superset/superset_oidc_client_secret.txt" ;;
    *) usage ;;
  esac
}
compose() { (cd "$HOME_ROOT" && docker compose "$@"); }

case "$1" in
import)
  # A token whose hy-home-operator policy has the seven paths (RUN-0085 W1c).
  # The test-only root override must never choose which files become the first KV version.
  [ -z "${OIDC_HOME_ROOT:-}" ] || { echo "unset OIDC_HOME_ROOT before import" >&2; exit 1; }
  [ "$#" -eq 2 ] || usage
  [ "$(stat -c '%a %h' "$2" 2>/dev/null)" = "600 1" ] || { echo "token file is not 0600 single-link" >&2; exit 1; }
  token_file=$2
  bao_op() { BAO_TOKEN="$(cat "$token_file")" compose exec -T -e BAO_TOKEN openbao bao "$@"; }
  while read -r kv file _; do
    # -cas=0 refuses an existing path, so no other field is overwritten.
    if bao_op kv put -cas=0 "secret/hy-home/$kv" client_secret=- <"$HOME_ROOT/secrets/$file" >/dev/null; then
      echo "put ok $kv"
    else
      echo "put FAIL $kv"
      exit 1
    fi
  done <<<"$SECRETS"
  missing=0
  while read -r kv _; do
    v="$(bao_op kv metadata get -format=json "secret/hy-home/$kv" </dev/null 2>/dev/null | jq -r '.data.current_version')"
    case "$v" in '' | null) echo "metadata MISSING $kv"; missing=1 ;; *) echo "metadata ok $kv v$v" ;; esac
  done <<<"$SECRETS"
  exit "$missing"
  ;;
prepare)
  # Before the main checkout fast-forwards: the binds use create_host_path: false.
  dirs=()
  while read -r _ _ out; do dirs+=("/openbao/out/${out%/*}"); done <<<"$SECRETS"
  docker exec -u 100 openbao-agent mkdir -p -m 0755 "${dirs[@]}" || exit 1
  docker exec openbao-agent ls -ld "${dirs[@]}" | awk '{print $1, $3, $NF}'
  # The new health fails on any group/other-readable file its agent.hcl does not list.
  echo "readable files (expect only the files the running agent.hcl renders):"
  docker exec openbao-agent find /openbao/out -mindepth 1 ! -type d \( -perm -040 -o -perm -004 \)
  ;;
cutover | rollback)
  [ "$#" -eq 2 ] || usage
  # usage inside the substitution exits only the subshell, so stop on its status.
  row="$(service_row "$2")" || exit 2
  read -r var file <<<"$row"
  # A stopped service waits for its next start: --no-deps would start it without its dependencies.
  [ "$(docker inspect -f '{{.State.Running}}' "$2" 2>/dev/null)" = true ] ||
    { echo "$2 is not running; cut it over when it next starts" >&2; exit 1; }
  env="$HOME_ROOT/.env"
  [ -f "$env" ] || exit 1
  # Only this variable's line changes. The copy keeps .env's owner and mode and replaces
  # it in one rename, so a failed write leaves the old .env, never a partial one.
  tmp="$(mktemp "$HOME_ROOT/.env.oidc.XXXXXX")" || exit 1
  trap 'rm -f "$tmp"' EXIT
  grep -v "^$var=" "$env" >"$tmp"
  [ "$?" -le 1 ] || exit 1
  if [ "$1" = cutover ]; then echo "$var=/run/openbao/$file" >>"$tmp" || exit 1; fi
  [ -s "$tmp" ] || [ ! -s "$env" ] || exit 1
  chmod --reference="$env" "$tmp" && chown --reference="$env" "$tmp" && mv -f "$tmp" "$env" || exit 1
  if [ "$1" = cutover ]; then echo "$2: $var=/run/openbao/$file"; else echo "$2: $var unset"; fi
  # An exported value would override .env during interpolation.
  (cd "$HOME_ROOT" && env -u "$var" docker compose up -d --no-deps "$2") || exit 1
  bash "$here/verify-oidc-client-secret.sh" "$2"
  ;;
*) usage ;;
esac
