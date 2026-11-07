#!/bin/sh
# Renders the DEV datastore scrape targets with the operator's declared
# expected state, then starts Prometheus (SPEC-0224).
#
# PROMETHEUS_DEV_DATA_EXPECTED=on|off says whether the dev-data profile is
# meant to run. The targets are always scraped; the expected_state label lets
# alerts treat a DEV target that is down while declared off as an intentional
# stop and one that is down while declared on as a failure. Any other value
# stops the start, so a typo never silences DEV alerts.
set -eu

state=${PROMETHEUS_DEV_DATA_EXPECTED:-}
case "$state" in
  on | off) ;;
  *)
    printf '%s\n' 'prometheus: PROMETHEUS_DEV_DATA_EXPECTED must be on or off' >&2
    exit 64
    ;;
esac

# A full-plan overlay declares the expected DEV state without changing it.
# Legacy starts without an overlay retain the original contract.
declared=${P07_DECLARED_DEV_EXPECTED:-}
if [ -n "$declared" ] && [ "$declared" != "$state" ]; then
  printf '%s\n' 'prometheus: declared DEV selection conflicts with configured expectation' >&2
  exit 64
fi

valid_port() {
  case "$1" in '' | *[!0-9]*) return 1 ;; esac
  [ "${#1}" -le 5 ] && [ "$1" -ge 1 ] && [ "$1" -le 65535 ]
}

openbao_port=${OPENBAO_PORT:-8200}
keycloak_port=${KEYCLOAK_MANAGEMENT_PORT-9000}
valid_port "$openbao_port" || exit 64
valid_port "$keycloak_port" || exit 64

dir=${PROMETHEUS_TARGETS_DIR:-/etc/prometheus/targets}
mkdir -p "$dir"
tmp=
trap '[ -z "$tmp" ] || rm -f -- "$tmp"' 0
trap '[ -z "$tmp" ] || rm -f -- "$tmp"; exit 1' 1 2 3 15

render() {
  # $1 job and file name, $2 target, $3 db_engine. Written beside the final
  # file and renamed, so file discovery never reads a partial file.
  tmp=$(mktemp "$dir/.$1.XXXXXX")
  printf '%s\n' \
    "- targets: [\"$2\"]" \
    '  labels:' \
    '    cluster: "hy-home"' \
    '    namespace: "hy-home"' \
    '    domain: "datastores"' \
    '    db_scope: "dev"' \
    "    db_engine: \"$3\"" \
    "    expected_state: \"$state\"" > "$tmp"
  mv -f "$tmp" "$dir/$1.yml"
  tmp=
}

render dev-pg-exporter dev-pg-exporter:9187 postgresql
render dev-valkey-exporter dev-valkey-exporter:9121 valkey

tmp=$(mktemp "$dir/.openbao.XXXXXX")
printf '%s\n' \
  "- targets: [\"openbao:$openbao_port\"]" \
  '  labels:' \
  '    cluster: "hy-home"' \
  '    namespace: "hy-home"' \
  '    domain: "security"' > "$tmp"
mv -f "$tmp" "$dir/openbao.yml"
tmp=

tmp=$(mktemp "$dir/.keycloak.XXXXXX")
printf '%s\n' \
  "- targets: [\"keycloak-management:$keycloak_port\"]" \
  '  labels:' \
  '    cluster: "hy-home"' \
  '    namespace: "hy-home"' \
  '    domain: "auth"' \
  '    container: "keycloak"' > "$tmp"
mv -f "$tmp" "$dir/keycloak.yml"
tmp=
trap - 0 1 2 3 15

exec "${PROMETHEUS_BIN:-/bin/prometheus}" "$@"
