#!/bin/bash
set -euo pipefail
umask 077

SCRIPT_NAME="$(basename "$0")"

usage() {
  cat <<'EOF'
Bootstrap file-based Docker secrets referenced by root docker-compose.yml.

Usage:
  scripts/bootstrap-secrets.sh [options]

Options:
  --env-file <path>        Env file to read non-secret sync values from (default: .env, fallback: .env.example)
  --compose-file <path>    Compose file to parse secrets from (default: docker-compose.yml)
  --dry-run                Print what would change without writing files
  --force                  Overwrite existing secret files
  --strict                 Fail if any placeholder (CHANGE_ME_*) remains
  --only <secret_name>     Generate only one secret (dependencies may still be generated)
  --list                   List discovered secrets and file paths, then exit
  --validate-compose        Run 'docker compose config -q' after generation
  -h, --help               Show this help

Notes:
  - Secrets are written under secrets/**/*.txt with restrictive permissions (0600).
  - By default, secret values are never printed.
  - Exception: Traefik BasicAuth passwords are printed once (stderr) on first generation.
EOF
}

die() {
  echo "ERROR: $*" >&2
  exit 1
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "Missing required command: $1"
}

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
[[ -n "$REPO_ROOT" ]] || die "This script must be run inside a git repository."
cd "$REPO_ROOT"

ENV_FILE=""
COMPOSE_FILE="docker-compose.yml"
DRY_RUN=false
FORCE=false
STRICT=false
ONLY_SECRET=""
LIST_ONLY=false
VALIDATE_COMPOSE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env-file)
      [[ $# -ge 2 ]] || die "--env-file requires a value"
      ENV_FILE="$2"
      shift 2
      ;;
    --compose-file)
      [[ $# -ge 2 ]] || die "--compose-file requires a value"
      COMPOSE_FILE="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --force)
      FORCE=true
      shift
      ;;
    --strict)
      STRICT=true
      shift
      ;;
    --only)
      [[ $# -ge 2 ]] || die "--only requires a secret name"
      ONLY_SECRET="$2"
      shift 2
      ;;
    --list)
      LIST_ONLY=true
      shift
      ;;
    --validate-compose)
      VALIDATE_COMPOSE=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "Unknown argument: $1"
      ;;
  esac
done

if [[ -z "$ENV_FILE" ]]; then
  if [[ -f ".env" ]]; then
    ENV_FILE=".env"
  else
    ENV_FILE=".env.example"
  fi
fi

[[ -f "$COMPOSE_FILE" ]] || die "Compose file not found: $COMPOSE_FILE"
[[ -f "$ENV_FILE" ]] || die "Env file not found: $ENV_FILE"

need_cmd openssl
need_cmd python3

env_get() {
  local file="$1"
  local key="$2"
  local val=""

  # Minimal .env parser:
  # - ignores blank lines and comments
  # - supports optional leading "export "
  # - supports quoted values "..." or '...'
  # - does NOT execute code (no source)
  val="$(
    python3 - "$file" "$key" <<'PY'
import re
import sys

path = sys.argv[1]
key = sys.argv[2]

pattern = re.compile(r'^\s*(?:export\s+)?' + re.escape(key) + r'\s*=\s*(.*)\s*$')

def strip_quotes(s: str) -> str:
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        return s[1:-1]
    return s

with open(path, "r", encoding="utf-8", errors="replace") as f:
    for raw in f:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = pattern.match(line)
        if not m:
            continue
        v = m.group(1).strip()
        # Remove inline comments only when it is obviously a comment (space + #)
        v = re.sub(r"\s+#.*$", "", v).strip()
        v = strip_quotes(v)
        print(v)
        sys.exit(0)
sys.exit(0)
PY
  )"

  printf '%s' "$val"
}

parse_secrets() {
  awk '
    BEGIN { in_secrets=0; current="" }
    /^secrets:[[:space:]]*$/ { in_secrets=1; next }
    /^include:[[:space:]]*$/ { in_secrets=0; current=""; next }
    in_secrets && /^[[:space:]]{2}#/ { next }
    in_secrets && /^[[:space:]]{2}[A-Za-z0-9_.-]+:[[:space:]]*$/ {
      current=$1
      sub(":", "", current)
      next
    }
    in_secrets && current != "" && /^[[:space:]]{4}file:[[:space:]]*/ {
      line=$0
      sub("^[[:space:]]{4}file:[[:space:]]*", "", line)
      sub("[[:space:]]+#.*$", "", line)
      gsub(/^["'\''"]|["'\''"]$/, "", line)
      print current "\t" line
      current=""
      next
    }
  ' "$COMPOSE_FILE"
}

resolve_secret_path() {
  local compose_path="$1"
  local resolved=""

  if [[ "$compose_path" == /* ]]; then
    resolved="$compose_path"
  else
    resolved="$REPO_ROOT/${compose_path#./}"
  fi

  case "$resolved" in
    "$REPO_ROOT"/secrets/*) ;;
    *)
      die "Refusing to write outside repo secrets/: $compose_path -> $resolved"
      ;;
  esac

  printf '%s' "$resolved"
}

write_secret_atomic() {
  local path="$1"
  local content="$2"

  mkdir -p "$(dirname "$path")"

  if [[ -f "$path" && "$FORCE" != "true" ]]; then
    echo "unchanged: ${path#$REPO_ROOT/}"
    return 0
  fi

  if [[ "$DRY_RUN" == "true" ]]; then
    if [[ -f "$path" ]]; then
      echo "would_overwrite: ${path#$REPO_ROOT/}"
    else
      echo "would_create: ${path#$REPO_ROOT/}"
    fi
    return 0
  fi

  local tmp
  tmp="$(mktemp)"
  chmod 600 "$tmp"
  printf '%s' "$content" > "$tmp"
  mv -f "$tmp" "$path"
  chmod 600 "$path"

  if [[ -f "$path" ]]; then
    echo "written: ${path#$REPO_ROOT/}"
  fi
}

b64url_encode() {
  # Reads stdin, writes base64url without padding/newlines.
  openssl base64 -A | tr '+/' '-_' | tr -d '='
}

jwt_hs256() {
  local secret="$1"
  local payload_json="$2"

  local header_json='{"alg":"HS256","typ":"JWT"}'
  local header_b64 payload_b64 signing_input sig_b64
  header_b64="$(printf '%s' "$header_json" | b64url_encode)"
  payload_b64="$(printf '%s' "$payload_json" | b64url_encode)"
  signing_input="${header_b64}.${payload_b64}"
  sig_b64="$(
    printf '%s' "$signing_input" \
      | openssl dgst -binary -sha256 -hmac "$secret" \
      | b64url_encode
  )"
  printf '%s' "${signing_input}.${sig_b64}"
}

gen_hex_32() { openssl rand -hex 32; }
gen_hex_16() { openssl rand -hex 16; }

gen_airflow_fernet_key() {
  python3 -c 'import base64,os; print(base64.urlsafe_b64encode(os.urandom(32)).decode())'
}

gen_oauth2_cookie_secret() {
  python3 -c 'import base64,os; print(base64.b64encode(os.urandom(32)).decode())'
}

gen_supabase_secret_key_base() {
  python3 -c 'import secrets; print(secrets.token_urlsafe(64))'
}

manual_placeholder_for() {
  local secret="$1"
  case "$secret" in
    slack_webhook) printf '%s' 'CHANGE_ME_SLACK_WEBHOOK_URL' ;;
    smtp_username) printf '%s' 'CHANGE_ME_SMTP_USERNAME' ;;
    smtp_password) printf '%s' 'CHANGE_ME_SMTP_PASSWORD' ;;
    supabase_openai_api_key) printf '%s' 'CHANGE_ME_OPENAI_API_KEY' ;;
    *) return 1 ;;
  esac
}

gen_traefik_htpasswd_line() {
  local password="$1"
  need_cmd htpasswd
  htpasswd -nbB admin "$password" | tr -d '\n'
}

should_process_secret() {
  local name="$1"
  if [[ -n "$ONLY_SECRET" ]]; then
    [[ "$name" == "$ONLY_SECRET" ]] && return 0
    return 1
  fi
  return 0
}

echo "Parsing secrets from: $COMPOSE_FILE"
mapfile -t SECRET_PAIRS < <(parse_secrets)

if [[ "${#SECRET_PAIRS[@]}" -eq 0 ]]; then
  die "No secrets with file: paths found in $COMPOSE_FILE (expected root secrets: file-based)"
fi

if [[ "$LIST_ONLY" == "true" ]]; then
  printf '%s\n' "${SECRET_PAIRS[@]}"
  exit 0
fi

declare -A secret_to_file=()
for pair in "${SECRET_PAIRS[@]}"; do
  name="${pair%%$'\t'*}"
  file="${pair#*$'\t'}"
  secret_to_file["$name"]="$file"
done

MANUAL_SECRET_NAMES=(slack_webhook smtp_username smtp_password supabase_openai_api_key)

ensure_secret_generated() {
  local secret_name="$1"

  local file_rel="${secret_to_file[$secret_name]:-}"
  [[ -n "$file_rel" ]] || die "Secret not found in compose secrets: $secret_name"
  local file_path
  file_path="$(resolve_secret_path "$file_rel")"

  if ! should_process_secret "$secret_name"; then
    return 0
  fi

  local value=""

  if value="$(manual_placeholder_for "$secret_name")"; then
    write_secret_atomic "$file_path" "$value"
    return 0
  fi

  case "$secret_name" in
    minio_root_username)
      write_secret_atomic "$file_path" "minio_root"
      ;;
    minio_app_username)
      local env_val
      env_val="$(env_get "$ENV_FILE" "MINIO_APP_USERNAME")"
      if [[ -z "$env_val" ]]; then
        env_val="minio_user"
      fi
      write_secret_atomic "$file_path" "$env_val"
      ;;
    traefik_basicauth_password|traefik_opensearch_basicauth_password)
      local existing=false
      [[ -f "$file_path" ]] && existing=true
      local pw hashline
      pw="$(gen_hex_16)"
      hashline="$(gen_traefik_htpasswd_line "$pw")"
      write_secret_atomic "$file_path" "$hashline"
      if [[ "$DRY_RUN" != "true" && "$existing" != "true" ]]; then
        echo "INFO: Traefik BasicAuth created (one-time password output) -> $secret_name: admin / $pw" >&2
      fi
      ;;
    airflow_fernet_key)
      write_secret_atomic "$file_path" "$(gen_airflow_fernet_key)"
      ;;
    oauth2_proxy_cookie_secret)
      write_secret_atomic "$file_path" "$(gen_oauth2_cookie_secret)"
      ;;
    supabase_secret_key_base)
      write_secret_atomic "$file_path" "$(gen_supabase_secret_key_base)"
      ;;
    n8n_encryption_key)
      write_secret_atomic "$file_path" "$(gen_hex_16)"
      ;;
    supabase_jwt_secret)
      write_secret_atomic "$file_path" "$(gen_hex_32)"
      ;;
    supabase_anon_key|supabase_service_key)
      local jwt_secret_path jwt_secret
      jwt_secret_path="$(resolve_secret_path "${secret_to_file[supabase_jwt_secret]}")"
      if [[ ! -f "$jwt_secret_path" || "$FORCE" == "true" ]]; then
        # Ensure dependency exists before deriving.
        local prev_only="$ONLY_SECRET"
        ONLY_SECRET="supabase_jwt_secret"
        ensure_secret_generated "supabase_jwt_secret"
        ONLY_SECRET="$prev_only"
      fi
      jwt_secret="$(tr -d '\n' < "$jwt_secret_path")"
      [[ -n "$jwt_secret" ]] || die "supabase_jwt_secret is empty; cannot derive JWT keys"

      local now exp role payload jwt
      now="$(date +%s)"
      exp="$((now + 315360000))" # 10 years
      if [[ "$secret_name" == "supabase_anon_key" ]]; then
        role="anon"
      else
        role="service_role"
      fi
      payload="$(printf '{"role":"%s","aud":"authenticated","iat":%s,"exp":%s}' "$role" "$now" "$exp")"
      jwt="$(jwt_hs256 "$jwt_secret" "$payload")"
      write_secret_atomic "$file_path" "$jwt"
      ;;
    *)
      write_secret_atomic "$file_path" "$(gen_hex_32)"
      ;;
  esac
}

for secret_name in "${!secret_to_file[@]}"; do
  ensure_secret_generated "$secret_name"
done

if [[ "$STRICT" != "true" ]]; then
  manual_remaining=()
  for secret_name in "${MANUAL_SECRET_NAMES[@]}"; do
    file_rel="${secret_to_file[$secret_name]:-}"
    [[ -n "$file_rel" ]] || continue
    file_path="$(resolve_secret_path "$file_rel")"

    if [[ "$DRY_RUN" == "true" ]]; then
      manual_remaining+=("$secret_name (${file_path#$REPO_ROOT/})")
      continue
    fi

    if [[ ! -f "$file_path" ]]; then
      manual_remaining+=("$secret_name (${file_path#$REPO_ROOT/})")
      continue
    fi

    if head -c 128 "$file_path" | grep -q '^CHANGE_ME_'; then
      manual_remaining+=("$secret_name (${file_path#$REPO_ROOT/})")
    fi
  done

  if [[ "${#manual_remaining[@]}" -gt 0 ]]; then
    echo "WARNING: Manual secrets still require real values (placeholders remain):" >&2
    for item in "${manual_remaining[@]}"; do
      echo "  - $item" >&2
    done
    echo "TIP: After updating, run: bash \"$0\" --strict" >&2
  fi
fi

if [[ "$STRICT" == "true" ]]; then
  failed=false
  for secret_name in "${!secret_to_file[@]}"; do
    file_path="$(resolve_secret_path "${secret_to_file[$secret_name]}")"
    [[ -f "$file_path" ]] || continue
    if head -c 128 "$file_path" | grep -q '^CHANGE_ME_'; then
      echo "STRICT: placeholder remains -> $secret_name (${file_path#$REPO_ROOT/})" >&2
      failed=true
    fi
  done
  if [[ "$failed" == "true" ]]; then
    exit 1
  fi
fi

if [[ "$VALIDATE_COMPOSE" == "true" ]]; then
  need_cmd docker
  echo "Validating compose config: docker compose --env-file $ENV_FILE -f $COMPOSE_FILE config -q"
  docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" config -q
fi

echo "Done."
