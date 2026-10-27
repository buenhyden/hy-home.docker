#!/bin/sh
# Every agent.hcl template: fetch, exact rendered bytes, KV version and mode.
# Application consumption is separate.
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
# agent.hcl owns the template list; each template names its KV path and field.
templates=$(awk '
  /^template[[:space:]]*\{/ { inside = 1; seen++; source = ""; destination = ""; perms = ""; next }
  inside && $1 == "source" { source = $3; gsub(/"/, "", source) }
  inside && $1 == "destination" { destination = $3; gsub(/"/, "", destination) }
  inside && $1 == "perms" { perms = $3; gsub(/"/, "", perms) }
  inside && /^\}/ { if (source != "" && destination != "" && perms != "") { print perms, destination, source; printed++ } inside = 0 }
  END { if (seen == 0 || seen != printed) exit 1 }
' /openbao/config/agent.hcl)
consumed=" "
while read -r perms destination source; do
  case "$destination$source" in *..*) exit 1 ;; esac
  case "$destination" in /openbao/out/*/*) ;; *) exit 1 ;; esac
  case "$source" in /openbao/config/templates/*.ctmpl) ;; *) exit 1 ;; esac
  [ -f "$destination" ] && [ ! -L "$destination" ] && [ -s "$destination" ] || exit 1
  [ -f "$source" ] && [ ! -L "$source" ] || exit 1
  path=$(sed -n 's|^{{- with secret "secret/data/\(hy-home/[a-z0-9/_-]*\)" -}}$|\1|p' "$source")
  case "$path" in hy-home/?*) ;; *) exit 1 ;; esac
  case "$destination" in
    *.txt)
      # A consumed value is group-readable for its one consumer (P06).
      [ "$perms" = 0640 ] && [ "$(stat -c %a "$destination")" = 640 ] || exit 1
      field=$(sed -n 's/^{{ \.Data\.data\.\([a-z0-9_]*\) }}$/\1/p' "$source")
      [ -n "$field" ] || exit 1
      timeout 3 bao kv get -field="$field" "secret/$path" | cmp -s - "$destination" || exit 1
      consumed="$consumed$destination "
      ;;
    *.version)
      [ "$perms" = 0600 ] && [ "$(stat -c %a "$destination")" = 600 ] || exit 1
      grep -qxF '{{ .Data.metadata.version }}' "$source" || exit 1
      version=$(timeout 3 bao read -field=current_version "secret/metadata/$path") || exit 1
      case "$version" in ''|0|*[!0-9]*) exit 1 ;; esac
      [ "$version" = "$(cat "$destination")" ] || exit 1
      ;;
    *) exit 1 ;;
  esac
done <<EOF_TEMPLATES
$templates
EOF_TEMPLATES
# Consumers bind whole directories: only a listed .txt may be readable by others.
readable=$(find /openbao/out -mindepth 1 ! -type d \( -perm -040 -o -perm -004 \))
while read -r file; do
  [ -z "$file" ] && continue
  case "$consumed" in *" $file "*) ;; *) exit 1 ;; esac
done <<EOF_READABLE
$readable
EOF_READABLE
