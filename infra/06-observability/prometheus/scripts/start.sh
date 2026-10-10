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

port=${OPENBAO_PORT:-8200}
case "$port" in '' | *[!0-9]*) exit 64 ;; esac
[ "${#port}" -le 5 ] && [ "$port" -ge 1 ] && [ "$port" -le 65535 ] || exit 64

dir=${PROMETHEUS_TARGETS_DIR:-/etc/prometheus/targets}
mkdir -p "$dir"

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
}

render dev-pg-exporter dev-pg-exporter:9187 postgresql
render dev-valkey-exporter dev-valkey-exporter:9121 valkey

tmp=$(mktemp "$dir/.openbao.XXXXXX")
printf '%s\n' \
  "- targets: [\"openbao:$port\"]" \
  '  labels:' \
  '    cluster: "hy-home"' \
  '    namespace: "hy-home"' \
  '    domain: "security"' > "$tmp"
mv -f "$tmp" "$dir/openbao.yml"

exec "${PROMETHEUS_BIN:-/bin/prometheus}" "$@"
