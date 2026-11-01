#!/usr/bin/env bash
# Install the research-report plugin of merged origin/main into this user's
# Hermes, then restart hermes-gateway.service: cron runs inside it and keeps the
# plugin it loaded at start.
# Run as the Hermes user, without sudo:  bash deploy/update-hermes-plugin.sh
# Rollback: copy the printed backup back over the plugin directory and restart
# hermes-gateway.service.
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$HERE" rev-parse --show-toplevel)
SRC=infra/07-workflow/n8n/workloads/hermes-blog-ingestion/hermes-plugin
PLUGIN=$HOME/.hermes/plugins/research-report

git -C "$REPO" fetch --quiet origin
mapfile -t FILES < <(git -C "$REPO" ls-tree --name-only "origin/main:$SRC")
[[ ${#FILES[@]} -gt 0 ]] || { echo "origin/main has no $SRC" >&2; exit 1; }

mkdir -p "$PLUGIN"
BACKUP=$HOME/.hermes/plugins/.research-report-backup-$(date -u +%Y%m%dT%H%M%SZ)
cp -a "$PLUGIN" "$BACKUP"
for f in "${FILES[@]}"; do
  git -C "$REPO" show "origin/main:$SRC/$f" > "$PLUGIN/$f.new"
  mv "$PLUGIN/$f.new" "$PLUGIN/$f"
done
rm -rf "$PLUGIN/__pycache__"
for f in "${FILES[@]}"; do
  if [[ "$(git -C "$REPO" show "origin/main:$SRC/$f" | sha256sum)" != "$(sha256sum < "$PLUGIN/$f")" ]]; then
    echo "$f DIFF" >&2
    exit 1
  fi
  echo "$f MATCH"
done
echo "backup: $BACKUP"
hermes plugins doctor research-report | tail -3
systemctl --user restart hermes-gateway.service
systemctl --user show hermes-gateway.service -p ActiveState -p ActiveEnterTimestamp
