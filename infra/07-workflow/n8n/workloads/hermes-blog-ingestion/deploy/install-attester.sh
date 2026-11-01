#!/usr/bin/env bash
# Install the attester release of merged origin/main and start its timer.
# Run from the operator checkout:  sudo bash deploy/install-attester.sh [python]
# The unit's required /etc/hermes-attester/environment is written here from
# DEFAULT_URL in the repository .env; nothing goes to shell rc files.
# Rollback: sudo systemctl disable --now hermes-attester.timer, point
# /opt/hermes-attester/current at the previous release printed below (releases
# are immutable), restore the previous units, sudo systemctl daemon-reload.
set -euo pipefail
[[ $EUID -eq 0 && -n "${SUDO_USER:-}" ]] || { echo "run with sudo from your user" >&2; exit 1; }
as_user() { runuser -u "$SUDO_USER" -- "$@"; }

PYTHON=${1:-/usr/bin/python3.12}
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(as_user git -C "$HERE" rev-parse --show-toplevel)
WL=infra/07-workflow/n8n/workloads/hermes-blog-ingestion

as_user git -C "$REPO" fetch --quiet origin
COMMIT=$(as_user git -C "$REPO" rev-parse origin/main)
echo "commit: $COMMIT"

# Site values, read as data from .env (never sourced).
SITE=$(sed -n 's/^DEFAULT_URL=//p' "$REPO/.env" | tail -1 | tr -d "\"'")
[[ "$SITE" =~ ^[a-z0-9]([a-z0-9.-]*[a-z0-9])?$ ]] || { echo "DEFAULT_URL missing or invalid in $REPO/.env" >&2; exit 1; }

# Root-owned archive in a root-only directory, as install.py requires. The
# installer and units come from that archive, not the user-writable checkout.
TAR=/root/hermes-attester-$COMMIT.tar
as_user git -C "$REPO" archive --format=tar "$COMMIT" -- "$WL" > "$TAR"
chmod 0600 "$TAR"
STAGE=$(mktemp -d /root/hermes-attester-stage.XXXXXX)
trap 'rm -rf "$STAGE"' EXIT
tar -xf "$TAR" -C "$STAGE" "$WL/install.py" "$WL/deploy/hermes-attester.service" "$WL/deploy/hermes-attester.timer"

PREVIOUS=$(readlink /opt/hermes-attester/current || true)
RELEASE=/opt/hermes-attester/releases/$COMMIT
[[ -d "$RELEASE" ]] || RELEASE=$(python3 -I "$STAGE/$WL/install.py" --role attester --archive "$TAR" --python "$PYTHON")
echo "previous: ${PREVIOUS:-none}"
echo "release: $RELEASE"
ln -sfn "$RELEASE" /opt/hermes-attester/current

printf 'HERMES_GATEWAY_URL=https://blog-export.%s\nHERMES_INTERNAL_ZONE=%s\n' "$SITE" "$SITE" \
  > /etc/hermes-attester/environment.new
chown root:root /etc/hermes-attester/environment.new
chmod 0644 /etc/hermes-attester/environment.new
mv /etc/hermes-attester/environment.new /etc/hermes-attester/environment
echo "environment: $(tr '\n' ' ' < /etc/hermes-attester/environment)"

install -o root -g root -m 0644 "$STAGE/$WL/deploy/hermes-attester.service" "$STAGE/$WL/deploy/hermes-attester.timer" /etc/systemd/system/
systemctl daemon-reload

# One manual run first. On failure the timer is stopped so a broken release or
# environment never keeps running.
if systemctl start hermes-attester.service; then
  journalctl -u hermes-attester.service -n 3 --no-pager -o cat
  systemctl enable --now hermes-attester.timer
  systemctl list-timers hermes-attester.timer --no-pager
else
  journalctl -u hermes-attester.service -n 20 --no-pager -o cat
  systemctl disable --now hermes-attester.timer || true
  echo "manual run failed: timer stopped; previous release: ${PREVIOUS:-none}" >&2
  exit 1
fi
