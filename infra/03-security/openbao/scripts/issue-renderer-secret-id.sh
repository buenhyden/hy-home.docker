#!/bin/sh
# Explicit operator action: issuer token on stdin, wrapped result to one Agent volume.
set +x
set -eu
exec >/dev/null 2>&1

[ "$#" -eq 4 ] || exit 1
server_container=$1
agent_volume=$2
image=$3
agent_container=$4
for target in "$server_container" "$agent_volume" "$agent_container"; do
  case "$target" in
    ''|[!a-zA-Z0-9]*|*[!a-zA-Z0-9_.-]*) exit 1 ;;
  esac
done
[ "$image" = openbao/openbao:2.6.2 ] || exit 1
image_id=$(timeout 5 docker image inspect --format '{{.Id}}' "$image") || exit 1
case "$image_id" in sha256:*) ;; *) exit 1 ;; esac
image_digest=${image_id#sha256:}
[ "${#image_digest}" -eq 64 ] || exit 1
case "$image_digest" in *[!0-9a-f]*) exit 1 ;; esac
timeout 5 docker volume inspect "$agent_volume" || exit 1
server_binding=$(timeout 5 docker inspect --type=container --format \
  '{{.Image}} {{.State.Running}}' "$server_container") || exit 1
[ "$server_binding" = "$image_id true" ] || exit 1
agent_binding=$(timeout 5 docker inspect --type=container --format \
  '{{.Image}} {{.State.Running}} {{range .Mounts}}{{if eq .Destination "/openbao/agent"}}{{.Type}} {{.Name}}{{end}}{{end}}' \
  "$agent_container") || exit 1
[ "$agent_binding" = "$image_id false volume $agent_volume" ] || exit 1
issuer_token=''
IFS= read -r issuer_token || [ -n "$issuer_token" ] || exit 1
case "$issuer_token" in
  ''|*[!a-zA-Z0-9._-]*) exit 1 ;;
esac

# Expand credentials only inside the receiving process, never in Docker argv.
# shellcheck disable=SC2016
wrapped_token=$(printf '%s\n' "$issuer_token" | timeout 20 docker exec -i "$server_container" sh -c '
  set +x
  set -eu
  IFS= read -r BAO_TOKEN
  export BAO_TOKEN
  unset VAULT_TOKEN
  case "${BAO_ADDR:-}" in https://?*) ;; *) exit 1 ;; esac
  [ -n "${BAO_CACERT:-}" ] && [ -r "$BAO_CACERT" ] || exit 1
  [ -z "${BAO_SKIP_VERIFY:-}${VAULT_SKIP_VERIFY:-}" ] || exit 1
  timeout 10 bao write -wrap-ttl=60s -field=wrapping_token -f auth/approle/role/hy-home-renderer/secret-id
') || exit 1
unset issuer_token
case "$wrapped_token" in
  ''|*[!a-zA-Z0-9._-]*) exit 1 ;;
esac
# A temporary file inside the exact mounted volume is atomically promoted.
# Refuse symlink targets and clean the private partial on any delivery failure.
# shellcheck disable=SC2016
printf '%s\n' "$wrapped_token" | timeout 20 docker run --rm --pull=never --network=none -i \
  --user=100:1000 --cap-drop=ALL --security-opt=no-new-privileges \
  --read-only --mount "type=volume,source=$agent_volume,target=/openbao/agent" \
  --entrypoint sh "$image" -c '
    set +x
    set -eu
    umask 077
    [ -d /openbao/agent ] && [ ! -L /openbao/agent ] || exit 1
    [ ! -L /openbao/agent/secret_id ] || exit 1
    partial=$(mktemp /openbao/agent/.wrapped-secret-id.XXXXXX)
    trap '\''rm -f "$partial"'\'' EXIT
    trap '\''exit 1'\'' HUP INT TERM
    IFS= read -r wrapped
    case "$wrapped" in '\'''\''|*[!a-zA-Z0-9._-]*) exit 1 ;; esac
    printf %s "$wrapped" >"$partial"
    chmod 600 "$partial"
    mv -f "$partial" /openbao/agent/secret_id
  ' || exit 1
