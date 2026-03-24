#!/usr/bin/env bash
# SessionStart Hook — hy-home.docker 프로젝트 컨텍스트 로딩
# 세션 시작 시 프로젝트 상태를 Claude에게 주입

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Git 상태
GIT_BRANCH=$(git -C "$PROJECT_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
GIT_STATUS=$(git -C "$PROJECT_DIR" status --short 2>/dev/null | wc -l | tr -d ' ')
LAST_COMMIT=$(git -C "$PROJECT_DIR" log -1 --format="%h %s" 2>/dev/null || echo "unknown")

# 실행 중인 Docker 서비스
RUNNING_CONTAINERS=$(docker ps --format "{{.Names}}" 2>/dev/null | sort | tr '\n' ', ' | sed 's/,$//' || echo "docker 미실행")
CONTAINER_COUNT=$(docker ps -q 2>/dev/null | wc -l | tr -d ' ' || echo "0")

# infra 디렉토리 구조 요약
INFRA_DIRS=$(ls "$PROJECT_DIR/infra/" 2>/dev/null | tr '\n' ', ' | sed 's/,$//' || echo "없음")

python3 -c "
import json, sys

branch = sys.argv[1]
git_changes = sys.argv[2]
last_commit = sys.argv[3]
containers = sys.argv[4]
container_count = sys.argv[5]
infra_dirs = sys.argv[6]

msg = f'''🏠 **hy-home.docker 프로젝트 컨텍스트**

**Git 상태**
- 브랜치: \`{branch}\`
- 변경된 파일: {git_changes}개
- 최근 커밋: \`{last_commit}\`

**Docker 서비스**
- 실행 중: {container_count}개
- 서비스: {containers if containers else '없음'}

**인프라 레이어**
{infra_dirs}

**주요 규칙 (CLAUDE.md)**
- 배포 전 반드시 \`bash scripts/validate-docker-compose.sh\` 실행
'''

print(json.dumps({'systemMessage': msg.strip()}))
" "$GIT_BRANCH" "$GIT_STATUS" "$LAST_COMMIT" "$RUNNING_CONTAINERS" "$CONTAINER_COUNT" "$INFRA_DIRS"

exit 0
