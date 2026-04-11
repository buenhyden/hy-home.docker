#!/usr/bin/env bash
# shellcheck disable=SC2154
# SessionStart Hook — hy-home.docker project context loading
# Inject project status into Claude at session start

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Git status
GIT_BRANCH=$(git -C "$PROJECT_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
GIT_STATUS=$(git -C "$PROJECT_DIR" status --short 2>/dev/null | wc -l | tr -d ' ')
LAST_COMMIT=$(git -C "$PROJECT_DIR" log -1 --format="%h %s" 2>/dev/null || echo "unknown")

# Running Docker services
RUNNING_CONTAINERS=$(docker ps --format "{{.Names}}" 2>/dev/null | sort | tr '\n' ', ' | sed 's/,$//' || echo "docker not running")
CONTAINER_COUNT=$(docker ps -q 2>/dev/null | wc -l | tr -d ' ' || echo "0")

# Infra directory summary
INFRA_DIRS=$(ls "$PROJECT_DIR/infra/" 2>/dev/null | tr '\n' ', ' | sed 's/,$//' || echo "none")

python3 -c "
import json, sys

branch = sys.argv[1]
git_changes = sys.argv[2]
last_commit = sys.argv[3]
containers = sys.argv[4]
container_count = sys.argv[5]
infra_dirs = sys.argv[6]

msg = f'''🏠 **hy-home.docker project context**

**Git status**
- Branch: `${branch}`
- Changed files: `${git_changes}`
- Last commit: `${last_commit}`

**Docker services**
- Running: {container_count}
- Services: {containers if containers else 'none'}

**Infra layer**
{infra_dirs}

**Key rules (CLAUDE.md)**
- Run `bash scripts/validate-docker-compose.sh` before deploy
'''

print(json.dumps({'systemMessage': msg.strip()}))
" "$GIT_BRANCH" "$GIT_STATUS" "$LAST_COMMIT" "$RUNNING_CONTAINERS" "$CONTAINER_COUNT" "$INFRA_DIRS"

exit 0
