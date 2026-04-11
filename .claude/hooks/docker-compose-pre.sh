#!/usr/bin/env bash
# shellcheck disable=SC2154
# PreToolUse Hook — Docker Compose edit warning
# Notify Claude before editing docker-compose*.yml files

INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    inp = data.get('tool_input', {})
    print(inp.get('file_path') or inp.get('path', ''))
except:
    print('')
" 2>/dev/null)

[ -z "$FILE_PATH" ] && exit 0

# Check if file is docker-compose
case "$FILE_PATH" in
    *docker-compose*.yml|*docker-compose*.yaml)
        ;;
    *)
        exit 0
        ;;
esac

SHORT_PATH="${FILE_PATH/#$CLAUDE_PROJECT_DIR\/}"

python3 -c "
import json, sys
path = sys.argv[1]
msg = (
    '🐳 **Docker Compose file edit detected**\n\n'
    f'You are about to edit `${path}`.\n\n'
    '**After editing, verify:**\n'
    '- Run `bash scripts/validate-docker-compose.sh`\n'
    '- Check port conflicts, volume paths, and missing environment variables\n'
    '- Ensure the network name matches the existing configuration\n\n'
    '> The PostToolUse hook will run validation after the edit.'
)
print(json.dumps({'systemMessage': msg}))
" "$SHORT_PATH"

exit 0
