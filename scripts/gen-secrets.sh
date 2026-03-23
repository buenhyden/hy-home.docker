#!/bin/bash

# ==============================================================================
# gen-secrets.sh - hy-home.docker Secret Management Script
# ==============================================================================

set -e

# Configuration
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
EXAMPLE_FILE="${REPO_ROOT}/secrets/SENSITIVE_ENV_VARS.md.example"
TARGET_FILE="${REPO_ROOT}/secrets/SENSITIVE_ENV_VARS.md"
ENV_FILE="${REPO_ROOT}/.env"
CURRENT_DATE=$(date +%Y-%m-%d)

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=== hy-home.docker Secret Management System ===${NC}"

# Check for required tools
for tool in htpasswd openssl tr head awk grep sed; do
    if ! command -v $tool &> /dev/null; then
        echo -e "${RED}Error: Required tool '$tool' not found.${NC}"
        exit 1
    fi
done

# Initialize target file if not exists
if [ ! -f "$TARGET_FILE" ]; then
    echo -e "${YELLOW}Initializing ${TARGET_FILE} from example...${NC}"
    cp "$EXAMPLE_FILE" "$TARGET_FILE"
fi

# Load .env variables into a temporary file
TEMP_ENV=$(mktemp)
if [ -f "$ENV_FILE" ]; then
    # Clean up .env: remove comments, empty lines, and trim spaces
    grep -v '^[[:space:]]*#' "$ENV_FILE" | grep -v '^[[:space:]]*$' | sed 's/[[:space:]]*=[[:space:]]*/=/' > "$TEMP_ENV" || true
fi

# Store values in a temporary directory
VAL_DIR=$(mktemp -d)
trap 'rm -rf "$VAL_DIR" "$TEMP_ENV"' EXIT

get_env_val() {
    local var_name=$1
    [ -z "$var_name" ] || [ "$var_name" == "-" ] && return 1
    # Find the variable and extract value, removing quotes and tailing comments
    local val=$(grep "^[[:space:]]*${var_name}=" "$TEMP_ENV" | head -n 1 | cut -d'=' -f2- | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//" -e 's/[[:space:]]*#.*$//')
    if [ -n "$val" ]; then
        echo -n "$val"
        return 0
    fi
    return 1
}

gen_password() {
    LC_ALL=C tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 16
}

echo -e "${BLUE}Processing secrets...${NC}"

# First pass: Collect metadata and generate/sync values
while IFS= read -r line; do
    if [[ "$line" =~ ^[[:space:]]*"|" ]]; then
        # Skip header and separator rows specifically
        if [[ "$line" =~ "| ID |" ]] || [[ "$line" =~ "| :---" ]]; then
            echo "$line" >> /dev/null # just to keep IFS consistent if needed
            continue
        fi

        # Extract columns
        ID=$(echo "$line" | cut -d'|' -f2 | xargs | tr -d '*')
        AUTO=$(echo "$line" | cut -d'|' -f3 | xargs | tr -d '`')
        VALUE_RAW=$(echo "$line" | cut -d'|' -f5 | xargs)
        VALUE=$(echo "$VALUE_RAW" | tr -d '`')
        ENV_VAR=$(echo "$line" | cut -d'|' -f6 | xargs | tr -d '`')
        FILE_PATH=$(echo "$line" | cut -d'|' -f7 | xargs | tr -d '`')

        [ -z "$ID" ] && continue
        # htpasswd entries are handled separately because they depend on other values
        [[ "$ID" == "INFRA-003" || "$ID" == "INFRA-004" ]] && continue

        NEW_VALUE=""
        FULL_PATH=""
        if [ -n "$FILE_PATH" ] && [ "$FILE_PATH" != "-" ]; then
            FULL_PATH="${REPO_ROOT}/${FILE_PATH}"
        fi

        # 1. NEW LOGIC: Always check VAL_DIR if we already processed it (should not happen in pass 1 but good for safety)
        # 2. Check if file exists and has content - prioritize THIS over generation
        if [ -n "$FULL_PATH" ] && [ -s "$FULL_PATH" ]; then
            NEW_VALUE=$(cat "$FULL_PATH")
        # Match placeholder if value starts with '(' and contains '비어있음'
        elif [[ -z "$VALUE" ]] || [[ "$VALUE" == *"비어있음"* ]] || [[ "$VALUE" == "(empty)" ]]; then
            # Priority 1: .env check
            ENV_VAL=$(get_env_val "$ENV_VAR" || echo "")
            if [ -n "$ENV_VAL" ]; then
                NEW_VALUE="$ENV_VAL"
            elif [ "$AUTO" == "O" ]; then
                NEW_VALUE=$(gen_password)
            fi
        else
            # Keep existing value in the Markdown
            NEW_VALUE="$VALUE"
        fi

        if [ -n "$NEW_VALUE" ]; then
            echo -n "$NEW_VALUE" > "$VAL_DIR/$ID"
            if [ -n "$FULL_PATH" ]; then
                if [ ! -f "$FULL_PATH" ] || [ ! -s "$FULL_PATH" ]; then
                    mkdir -p "$(dirname "$FULL_PATH")"
                    echo -n "$NEW_VALUE" > "$FULL_PATH"
                fi
            fi
        fi
    fi
done < "$TARGET_FILE"

# Second pass: Handle special dependencies (htpasswd)
# CRITICAL: Always regenerate hash if source values (ID/PW) are available in VAL_DIR
process_htpasswd() {
    local target_id=$1
    local user_id=$2
    local pass_id=$3
    local target_file_path=$4

    local user_val=$(cat "$VAL_DIR/$user_id" 2>/dev/null || echo "")
    local pass_val=$(cat "$VAL_DIR/$pass_id" 2>/dev/null || echo "")

    if [ -n "$user_val" ] && [ -n "$pass_val" ]; then
        local full_path="${REPO_ROOT}/${target_file_path}"
        local hashed=$(htpasswd -nb "$user_val" "$pass_val" | xargs)
        
        # If the file already exists, we MUST check if it matches our new hash
        if [ -f "$full_path" ] && [ -s "$full_path" ]; then
            local existing=$(cat "$full_path")
            # If they differ, we overwrite both the file and the registry to maintain consistency
            if [ "$hashed" != "$existing" ]; then
                echo -e "${YELLOW}Updating htpasswd hash for $target_id to match current ID/PW...${NC}"
                echo -n "$hashed" > "$full_path"
            fi
        else
            mkdir -p "$(dirname "$full_path")"
            echo -n "$hashed" > "$full_path"
        fi
        
        echo -n "$hashed" > "$VAL_DIR/$target_id"
    fi
}

process_htpasswd "INFRA-003" "INFRA-001" "INFRA-002" "secrets/auth/traefik_basicauth_password.txt"
process_htpasswd "INFRA-004" "OBS-003" "OBS-004" "secrets/auth/traefik_opensearch_basicauth_password.txt"

# Third pass: Update the Markdown target file
echo -e "${BLUE}Updating Markdown registry...${NC}"
FINAL_TEMP=$(mktemp)

while IFS= read -r line; do
    if [[ "$line" =~ ^[[:space:]]*"|" ]]; then
        if [[ "$line" =~ "| ID |" ]] || [[ "$line" =~ "| :---" ]]; then
            echo "$line" >> "$FINAL_TEMP"
            continue
        fi

        ID=$(echo "$line" | cut -d'|' -f2 | xargs | tr -d '*')

        # Check if we have a value for this ID
        if [ -n "$ID" ] && [ -f "$VAL_DIR/$ID" ]; then
            VAL=$(cat "$VAL_DIR/$ID")
            
            # Extract current value from the line to see if it changed
            CURRENT_VAL=$(echo "$line" | cut -d'|' -f5 | xargs | tr -d '`')
            
            # If value changed OR it was a placeholder OR if it's a derived hash that might have changed
            # we update row and date.
            if [[ "$VAL" != "$CURRENT_VAL" ]] || [[ "$CURRENT_VAL" == *"비어있음"* ]]; then
                echo "$line" | awk -F'|' -v v="$VAL" -v d="$CURRENT_DATE" 'BEGIN {OFS="|"} {
                    if (length(v) > 0) { $5 = " `"v"` "; }
                    else { $5 = " (비어있음) "; }
                    $8 = " "d" ";
                    print $0;
                }' >> "$FINAL_TEMP"
            else
                # Value matches existing non-placeholder, keep row as is (don't update date)
                echo "$line" >> "$FINAL_TEMP"
            fi
        else
            echo "$line" >> "$FINAL_TEMP"
        fi
    else
        if [[ "$line" =~ "마지막 업데이트:" ]]; then
            echo "*마지막 업데이트: ${CURRENT_DATE}* (스크립트 자동 갱신 완료)" >> "$FINAL_TEMP"
        else
            echo "$line" >> "$FINAL_TEMP"
        fi
    fi
done < "$TARGET_FILE"

mv "$FINAL_TEMP" "$TARGET_FILE"

echo -e "${GREEN}Processing complete!${NC}"
echo -e "Registry updated: ${TARGET_FILE}"
