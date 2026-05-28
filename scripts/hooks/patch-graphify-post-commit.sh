#!/usr/bin/env bash
# Re-applies the graphify-out filter to .git/hooks/post-commit.
#
# Run this after `graphify hook install` overwrites the post-commit hook.
# Without the filter, committing graphify-out/ triggers another rebuild,
# which produces new graphify-out/ changes, creating an infinite loop.
#
# Usage: bash scripts/hooks/patch-graphify-post-commit.sh

set -euo pipefail

HOOK=".git/hooks/post-commit"
MARKER="grep -v '^graphify-out/'"
FILTER_LINE="CHANGED=\$(printf '%s\\n' \"\$CHANGED\" | grep -v '^graphify-out/')"
ANCHOR='CHANGED=\$(git diff --name-only HEAD~1 HEAD'

if [ ! -f "$HOOK" ]; then
  echo "ERROR: $HOOK not found. Run 'graphify hook install' first." >&2
  exit 1
fi

if grep -q "$MARKER" "$HOOK"; then
  echo "Patch already applied — no changes made."
  exit 0
fi

if ! grep -q "$ANCHOR" "$HOOK"; then
  echo "ERROR: expected anchor line not found in $HOOK. Hook format may have changed." >&2
  exit 1
fi

# Insert filter line immediately after the CHANGED= assignment
sed -i "/$ANCHOR/a $FILTER_LINE" "$HOOK"

echo "Patch applied: graphify-out/ is now filtered from post-commit rebuild trigger."
