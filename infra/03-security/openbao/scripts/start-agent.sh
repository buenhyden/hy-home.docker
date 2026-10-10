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
exec bao agent -config=/openbao/config/agent.hcl
