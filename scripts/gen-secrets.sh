#!/bin/bash

# ==============================================================================
# hy-home.docker Secret Generation Script (Full Automation & Templating)
# ==============================================================================
# 1. SENSITIVE_ENV_VARS.md가 없으면 .example에서 복사하여 초기화합니다.
# 2. 레지스트리를 파싱하여 secrets 파일을 자동 생성하고 레지스트리를 갱신합니다.
# 3. 모든 값은 백틱(``)으로 감싸서 Markdown 형식을 유지합니다.
# ==============================================================================

SET_FORCE=false
REGISTRY_FILE="secrets/SENSITIVE_ENV_VARS.md"
EXAMPLE_FILE="secrets/SENSITIVE_ENV_VARS.md.example"
GENERATED_COUNT=0
SKIPPED_COUNT=0
SYNCED_COUNT=0
BACKUP_COUNT=0
CURRENT_DATE=$(date +%Y-%m-%d)

# 도움말 출력
usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  --force    기존 파일 내용이 있더라도 강제로 다시 생성 (Backup .bak 파일 생성)"
    echo "  --help     도움말 출력"
    exit 0
}

# 인수 처리
for arg in "$@"; do
    case $arg in
        --force) SET_FORCE=true ;;
        --help) usage ;;
    esac
done

# 필요한 도구 확인
if ! command -v openssl >/dev/null 2>&1; then
    echo "❌ Error: openssl이 설치되어 있지 않습니다."
    exit 1
fi

# 0. 레지스트리 파일 초기화 확인
if [ ! -f "$REGISTRY_FILE" ]; then
    if [ -f "$EXAMPLE_FILE" ]; then
        echo "📝 Initializing $REGISTRY_FILE from $EXAMPLE_FILE..."
        cp "$EXAMPLE_FILE" "$REGISTRY_FILE"
    else
        echo "❌ Error: Registry 파일($REGISTRY_FILE)과 템플릿($EXAMPLE_FILE)이 모두 없습니다."
        exit 1
    fi
fi

# 랜덤 비밀번호 생성 함수 (16자리, 대소문자+숫자)
generate_password() {
    openssl rand -base64 32 | tr -dc 'A-Za-z0-9' | head -c 16
}

# htpasswd 생성 함수 (Apache MD5 기반)
generate_htpasswd() {
    local username=$1
    local password=$2
    if openssl passwd -apr1 "test" >/dev/null 2>&1; then
        echo "${username}:$(openssl passwd -apr1 "${password}")"
    else
        echo "❌ Error: htpasswd 생성을 위한 openssl passwd -apr1 명령어가 지원되지 않습니다." >&2
        return 1
    fi
}

# 레지스트리 항목(값 및 날짜) 업데이트 함수
update_registry_entry() {
    local target_path=$1
    local new_value=$2
    local new_date=$3

    # 값을 백틱(``)으로 감싸서 기록 (이미 감싸져 있지 않은 경우에 대비)
    case $new_value in
        \`*\`) formatted_value=" $new_value " ;;
        *) formatted_value=" \`$new_value\` " ;;
    esac

    awk -v p="$target_path" -v v="$formatted_value" -v d=" $new_date " -F'|' '
        BEGIN { OFS="|" }
        {
            # 필드 6에서 백틱과 공백을 제거하고 비교
            raw_path = $6;
            gsub(/`/, "", raw_path);
            gsub(/ /, "", raw_path);

            if (raw_path == p) {
                # 값 업데이트
                $4 = v;
                # 날짜 업데이트
                $7 = d;
            }
            print $0;
        }
    ' "$REGISTRY_FILE" > "${REGISTRY_FILE}.tmp" && mv "${REGISTRY_FILE}.tmp" "$REGISTRY_FILE"
}

echo "----------------------------------------------------------------"
echo "🔐 hy-home.docker Secret Generation Start"
echo "Today: ${CURRENT_DATE}"
echo "----------------------------------------------------------------"

LAST_ID="admin"

# 파례(|) 구분 테이블 행만 추출하여 처리
grep "|" "$REGISTRY_FILE" | grep -v "자동화(Auto)" | grep -v ":---" | while IFS='|' read -r empty auto type value env_var path date purpose rest; do
    # 필드 양 끝 공백 및 백틱(`) 제거
    auto=$(echo "$auto" | sed 's/^[[:space:]`]*//;s/[[:space:]`]*$//;s/`//g')
    type=$(echo "$type" | sed 's/^[[:space:]`]*//;s/[[:space:]]*$//;s/`//g')
    value=$(echo "$value" | sed 's/^[[:space:]`]*//;s/[[:space:]`]*$//;s/`//g')
    path=$(echo "$path" | sed 's/^[[:space:]`]*//;s/[[:space:]`]*$//;s/`//g')
    purpose=$(echo "$purpose" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

    # ID 행인 경우 기억해둠
    if [[ "$type" == "ID" || "$type" == "User" || "$type" == "Account" ]]; then
        if [[ "$value" != "(N/A)" ]]; then
            LAST_ID="$value"
        fi
    fi

    # 파일 경로가 없거나 '-'이면 처리 대상 아님
    if [ -z "$path" ] || [[ "$path" == "-" ]]; then
        continue
    fi

    # 1. 기존 파일이 있고 생성하지 않는 경우, 레지스트리 값 동기화 확인
    if [ -s "$path" ] && [ "$SET_FORCE" = false ]; then
        if [[ "$value" == "(비어있음)" || -z "$value" || "$value" == "-" ]]; then
            FILE_CONTENT=$(cat "$path")
            SYNC_VAL=""
            if [[ "$path" == *"_password"* ]] && [[ "$FILE_CONTENT" == *":"* ]]; then
                SYNC_VAL=$(echo "$FILE_CONTENT" | cut -c 1-20)...
            else
                SYNC_VAL="$FILE_CONTENT"
            fi

            update_registry_entry "$path" "$SYNC_VAL" "$CURRENT_DATE"
            echo "🔄  Synced (Formatting): $path"
            SYNCED_COUNT=$((SYNCED_COUNT + 1))
        else
            echo "⏩  Skipping (Registry filled): $path"
        fi
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        continue
    fi

    # 2. 자동화 비대상(X) 또는 SKIP 태그 확인
    if [[ "$auto" == "X" ]] || [[ "$purpose" == *"[SKIP]"* ]]; then
        # SKIP 대상도 날짜가 비어있으면 오늘 날짜로 채워줌
        current_date_val=$(echo "$date" | xargs)
        if [ -z "$current_date_val" ] || [[ "$current_date_val" == "-" ]]; then
             update_registry_entry "$path" "$value" "$CURRENT_DATE"
        fi
        echo "⏩  Skipping (X/[SKIP]): $path"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        continue
    fi

    # 3. 시크릿 생성 및 업데이트
    mkdir -p "$(dirname "$path")"
    if [ -s "$path" ] && [ "$SET_FORCE" = true ]; then
        cp "$path" "${path}.bak"
        BACKUP_COUNT=$((BACKUP_COUNT + 1))
    fi

    RAW_PASS=$(generate_password)
    NEW_CONTENT=""
    REGISTRY_VALUE=""

    if [[ "$path" == *"traefik_basicauth"* ]] || [[ "$path" == *"traefik_opensearch_basicauth"* ]]; then
        NEW_CONTENT=$(generate_htpasswd "$LAST_ID" "$RAW_PASS")
        REGISTRY_VALUE=$(echo "$NEW_CONTENT" | cut -c 1-20)...
        echo "🔑 Created htpasswd for $LAST_ID -> $path"
    else
        NEW_CONTENT="$RAW_PASS"
        REGISTRY_VALUE="$RAW_PASS"
        echo "🎲 Created Password -> $path"
    fi

    # 파일 저장 및 레지스트리 갱신
    echo -n "$NEW_CONTENT" > "$path"
    update_registry_entry "$path" "$REGISTRY_VALUE" "$CURRENT_DATE"
    GENERATED_COUNT=$((GENERATED_COUNT + 1))

    # 서브쉘 카운트 유지
    echo "$GENERATED_COUNT" > /tmp/gen_count
    echo "$SKIPPED_COUNT" > /tmp/skip_count
    echo "$SYNCED_COUNT" > /tmp/sync_count
    echo "$BACKUP_COUNT" > /tmp/bak_count
done

# 카운트 복구
if [ -f /tmp/gen_count ]; then
    GENERATED_COUNT=$(cat /tmp/gen_count)
    SKIPPED_COUNT=$(cat /tmp/skip_count)
    SYNCED_COUNT=$(cat /tmp/sync_count)
    BACKUP_COUNT=$(cat /tmp/bak_count)
    rm /tmp/gen_count /tmp/skip_count /tmp/sync_count /tmp/bak_count
fi

echo "----------------------------------------------------------------"
echo "✅ 작업 완료!"
echo "✨ 생성됨: ${GENERATED_COUNT} 개"
echo "🔄  동기화됨: ${SYNCED_COUNT} 개"
echo "📦 백업됨: ${BACKUP_COUNT} 개"
echo "⏭️  건너뜀: ${SKIPPED_COUNT} 개"
echo "----------------------------------------------------------------"
