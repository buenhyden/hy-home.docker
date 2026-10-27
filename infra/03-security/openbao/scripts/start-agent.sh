#!/bin/sh
# The sink belongs to this process generation; old tokens cannot signal readiness.
set +x
set -eu

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
export BAO_ADDR="$VAULT_ADDR" BAO_CACERT="$VAULT_CACERT"
unset BAO_TOKEN VAULT_TOKEN
rm -f /openbao/agent/token
# The Agent skips rewriting an unchanged destination, so a changed template
# perms would never reach an existing file. Apply agent.hcl's perms here.
templates=$(awk '
  /^template[[:space:]]*\{/ { inside = 1; seen++; destination = ""; perms = ""; next }
  inside && $1 == "destination" { destination = $3; gsub(/"/, "", destination) }
  inside && $1 == "perms" { perms = $3; gsub(/"/, "", perms) }
  inside && /^\}/ { if (destination != "" && perms != "") { print perms, destination; printed++ } inside = 0 }
  END { if (seen != printed) exit 1 }
' /openbao/config/agent.hcl 2>/dev/null)
while read -r perms destination; do
  case "$perms" in 0[0-7][0-7][0-7]) ;; *) exit 1 ;; esac
  case "$destination" in /openbao/out/*/*) ;; *) exit 1 ;; esac
  case "$destination" in *..*) exit 1 ;; esac
  [ ! -L "$destination" ] || exit 1
  [ ! -f "$destination" ] || chmod "$perms" "$destination"
done <<EOF_TEMPLATES
$templates
EOF_TEMPLATES
exec bao agent -config=/openbao/config/agent.hcl
