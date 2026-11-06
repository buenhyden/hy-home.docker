#!/usr/bin/env bash
# Install the research-report plugin of merged origin/main into this user's
# Hermes, then restart hermes-gateway.service: cron runs inside it and keeps the
# plugin it loaded at start.
# Run as the Hermes user, without sudo:  bash deploy/update-hermes-plugin.sh
# Rollback is a separately approved operation: stop the service, preserve the
# current plugin directory, reconstruct a 0700 directory containing exactly the
# printed source-only backup files (do not overlay it), run doctor, then restart.
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$HERE" rev-parse --show-toplevel)
SRC=infra/07-workflow/n8n/workloads/hermes-blog-ingestion/hermes-plugin
PLUGIN=$HOME/.hermes/plugins/research-report
PLUGIN_PARENT=$HOME/.hermes/plugins
UID_NOW=$(id -u)

safe_directory() {
  local path=$1 owner mode
  [[ -d "$path" && ! -L "$path" ]] || return 1
  read -r owner mode < <(stat -c '%u %a' -- "$path")
  [[ "$owner" == "$UID_NOW" ]] && (( (8#$mode & 8#022) == 0 ))
}
# Name the refused path with its octal mode, owner and link count.
refuse() {
  local reason=$1 path=$2 facts
  facts=$(stat -c '0%a, uid %u, links %h' -- "$path" 2>/dev/null) || facts=missing
  echo "$reason: $path (mode $facts)" >&2
  exit 1
}
safe_file() {
  local path=$1 owner mode links
  [[ -f "$path" && ! -L "$path" ]] || return 1
  read -r owner mode links < <(stat -c '%u %a %h' -- "$path")
  [[ "$owner" == "$UID_NOW" && "$links" == 1 ]] && (( (8#$mode & 8#022) == 0 ))
}

for path in "$HOME" "$HOME/.hermes" "$PLUGIN_PARENT"; do
  safe_directory "$path" || refuse "unsafe plugin ancestor" "$path"
done

git -C "$REPO" fetch --quiet origin
COMMIT=$(git -C "$REPO" rev-parse --verify 'origin/main^{commit}')
FILES=(__init__.py plugin.yaml tools.py webhook_transport.py)
SHARED=(gateway_receipt.py private_records.py source_check.py source_collection.py source_fetch.py)
EXPECTED=$(printf '%s\n' "${FILES[@]}" | LC_ALL=C sort)
ACTUAL=$(git -C "$REPO" ls-tree --name-only "$COMMIT:$SRC")
[[ "$ACTUAL" == "$EXPECTED" ]] || { echo "unexpected plugin source files" >&2; exit 1; }

# Prepare and verify every file before changing the installed plugin.  The
# shared files are the exact canonical publisher bytes at the same commit.
STAGE=$(mktemp -d "$PLUGIN_PARENT/.research-report-stage.XXXXXXXX")
trap 'rm -rf -- "$STAGE"' EXIT
stage_file() {
  local source=$1 target=$2 entry blob actual
  entry=$(git -C "$REPO" ls-tree "$COMMIT" -- "$source")
  [[ "$entry" =~ ^100644[[:space:]]blob[[:space:]]([0-9a-f]{40})[[:space:]] ]] || {
    echo "bundle file missing or not a regular tracked file" >&2; exit 1;
  }
  blob=${BASH_REMATCH[1]}
  git -C "$REPO" show "$COMMIT:$source" > "$STAGE/$target"
  actual=$(git -C "$REPO" hash-object "$STAGE/$target")
  [[ "$actual" == "$blob" ]] || { echo "bundle digest mismatch" >&2; exit 1; }
}
for f in "${FILES[@]}"; do stage_file "$SRC/$f" "$f"; done
for f in "${SHARED[@]}"; do stage_file "${SRC%/hermes-plugin}/publisher/$f" "$f"; done

[[ ! -L "$PLUGIN" ]] || { echo "plugin directory is a symlink" >&2; exit 1; }
[[ -d "$PLUGIN" ]] || mkdir -m 0700 "$PLUGIN"
safe_directory "$PLUGIN" || refuse "unsafe plugin directory" "$PLUGIN"
shopt -s nullglob dotglob
for path in "$PLUGIN"/*; do
  name=${path##*/}
  [[ ! -L "$path" ]] || { echo "plugin contains a symlink" >&2; exit 1; }
  if [[ "$name" == __pycache__ && -d "$path" ]]; then
    safe_directory "$path" || refuse "unsafe plugin bytecode directory" "$path"
    for cached in "$path"/*; do
      safe_file "$cached" || refuse "unsafe plugin bytecode file" "$cached"
    done
    continue
  fi
  case " ${FILES[*]} ${SHARED[*]} " in
    *" $name "*) safe_file "$path" || refuse "unsafe installed plugin file" "$path" ;;
    *) echo "unexpected installed plugin file" >&2; exit 1 ;;
  esac
done
shopt -u nullglob dotglob
BACKUP=$HOME/.hermes/plugins/.research-report-backup-$(date -u +%Y%m%dT%H%M%SZ)
mkdir -m 0700 "$BACKUP"
# Preserve only reviewed source files. Bytecode and arbitrary extras must never
# enter a rollback release, even if the current cache happened to be safe.
for f in "${FILES[@]}" "${SHARED[@]}"; do
  if [[ -e "$PLUGIN/$f" ]]; then
    safe_file "$PLUGIN/$f" || refuse "unsafe backup source" "$PLUGIN/$f"
    install -m 0600 -- "$PLUGIN/$f" "$BACKUP/$f"
  fi
done
for f in "${FILES[@]}" "${SHARED[@]}"; do
  temporary=$(mktemp "$PLUGIN/.new-$f.XXXXXXXX")
  cat "$STAGE/$f" > "$temporary"
  chmod 0600 "$temporary"
  safe_file "$temporary" || refuse "unsafe staged plugin file" "$temporary"
  mv -T "$temporary" "$PLUGIN/$f"
done
rm -rf "$PLUGIN/__pycache__"
for f in "${FILES[@]}" "${SHARED[@]}"; do
  safe_file "$PLUGIN/$f" || refuse "unsafe installed plugin file" "$PLUGIN/$f"
  if [[ "$(sha256sum < "$STAGE/$f")" != "$(sha256sum < "$PLUGIN/$f")" ]]; then
    echo "$f DIFF" >&2
    exit 1
  fi
  echo "$f MATCH"
done
echo "backup: $BACKUP"
hermes plugins doctor research-report | tail -3
systemctl --user restart hermes-gateway.service
systemctl --user show hermes-gateway.service -p ActiveState -p ActiveEnterTimestamp
