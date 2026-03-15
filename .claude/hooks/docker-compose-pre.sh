#!/usr/bin/env bash
# PreToolUse Hook — Docker Compose 편집 전 경고
# docker-compose*.yml 파일을 수정하기 전에 Claude에게 주의사항 안내

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

# docker-compose 파일인지 확인
case "$FILE_PATH" in
    *docker-compose*.yml|*docker-compose*.yaml)
        ;;
    *)
        exit 0
        ;;
esac

SHORT_PATH="${FILE_PATH/#$CLAUDE_PROJECT_DIR\//}"

python3 -c "
import json, sys
path = sys.argv[1]
msg = (
    '🐳 **Docker Compose 파일 수정 감지**\n\n'
    f'\`{path}\` 파일을 수정하려 합니다.\n\n'
    '**수정 후 반드시 확인하세요:**\n'
    '- \`bash scripts/validate-docker-compose.sh\` 실행\n'
    '- 포트 충돌, 볼륨 경로, 환경변수 누락 여부 확인\n'
    '- 네트워크 이름이 기존 구성과 일치하는지 확인\n\n'
    '> PostToolUse hook이 수정 후 자동으로 검증을 실행합니다.'
)
print(json.dumps({'systemMessage': msg}))
" "$SHORT_PATH"

exit 0
