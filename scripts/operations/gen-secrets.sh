#!/usr/bin/env bash

# ==============================================================================
# gen-secrets.sh - hy-home.docker Secret Management Script
# ==============================================================================

set -euo pipefail
IFS=$'\n\t'
umask 077

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
EXAMPLE_FILE="${REPO_ROOT}/secrets/SENSITIVE_ENV_VARS.md.example"
TARGET_FILE="${REPO_ROOT}/secrets/SENSITIVE_ENV_VARS.md"
ENV_FILE="${REPO_ROOT}/.env"
IMPLEMENTATION_FILE="${REPO_ROOT}/scripts/operations/gen-secrets.sh"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

MODE="run"
declare -A ENV_VALUES=()
declare -A SECRET_VALUES=()
declare -a TEMP_PATHS=()

ROW_ID=""
ROW_AUTO=""
ROW_VALUE=""
ROW_ENV_VAR=""
ROW_FILE_PATH=""

usage() {
    cat <<'USAGE'
Usage: bash scripts/operations/gen-secrets.sh [--help|--check|--dry-run|--sync-metadata|--sync-metadata-check|--sync-metadata-prune|--sync-metadata-prune-check]

Generate local Docker secret files from repository secret registry metadata.

Modes:
  --help     Show this help without reading secret value sources.
  --check    Verify required tools and path layout without reading or writing
             secret values, .env, or secret files.
  --dry-run  Report planned actions from the example registry by ID/path only.
             Does not read .env, SENSITIVE_ENV_VARS.md, or secret files.

  --sync-metadata        Preserve private value cells and existing env assignments;
                         align public metadata and append missing public keys only.
  --sync-metadata-check  Same comparison without writes; exits 1 on drift.
  --sync-metadata-prune  Also remove private env assignments and registry rows
                         absent from their public metadata sources.
  --sync-metadata-prune-check
                         Same exact-set comparison without writes; exits 1 on drift.

No-argument mode preserves the existing operator workflow and may read/write
local secret registry and secret files. Do not use no-argument mode for audit
or verification.
USAGE
}

info() {
    printf '%b%s%b\n' "$BLUE" "$1" "$NC"
}

warn() {
    printf '%b%s%b\n' "$YELLOW" "$1" "$NC"
}

error() {
    printf '%bError:%b %s\n' "$RED" "$NC" "$1" >&2
}

die() {
    error "$1"
    exit 1
}

cleanup() {
    local path
    for path in "${TEMP_PATHS[@]}"; do
        if [[ -n "$path" && -e "$path" ]]; then
            rm -rf -- "$path"
        fi
    done
}
trap cleanup EXIT

parse_args() {
    if [[ "$#" -gt 1 ]]; then
        usage >&2
        exit 2
    fi

    case "${1-}" in
        "")
            MODE="run"
            ;;
        --help|-h)
            MODE="help"
            ;;
        --check)
            MODE="check"
            ;;
        --dry-run)
            MODE="dry-run"
            ;;
        --sync-metadata|--sync-metadata-check|--sync-metadata-prune|--sync-metadata-prune-check)
            MODE="${1#--}"
            ;;
        *)
            usage >&2
            exit 2
            ;;
    esac
}

trim() {
    local value="${1-}"
    value="${value#"${value%%[![:space:]]*}"}"
    value="${value%"${value##*[![:space:]]}"}"
    printf '%s' "$value"
}

strip_surrounding_quotes() {
    local value="$1"
    if [[ "${#value}" -ge 2 && "$value" == \"*\" && "$value" == *\" ]]; then
        value="${value:1:${#value}-2}"
    elif [[ "${#value}" -ge 2 && "$value" == \'*\' && "$value" == *\' ]]; then
        value="${value:1:${#value}-2}"
    fi
    printf '%s' "$value"
}

clean_cell() {
    local value
    value="$(trim "${1-}")"
    value="${value//\`/}"
    value="${value//\*/}"
    printf '%s' "$value"
}

clean_value_cell() {
    local value
    value="$(trim "${1-}")"
    value="${value//\`/}"
    printf '%s' "$value"
}

is_table_row() {
    [[ "${1-}" =~ ^[[:space:]]*\| ]]
}

is_header_or_separator() {
    local line="$1"
    [[ "$line" =~ \|[[:space:]]ID[[:space:]]\| ]] || [[ "$line" =~ \|[[:space:]]:--- ]]
}

parse_row() {
    local line="$1"
    local _lead id auto _kind value env_var file_path _date _purpose _tail
    ROW_ID=""
    ROW_AUTO=""
    ROW_VALUE=""
    ROW_ENV_VAR=""
    ROW_FILE_PATH=""

    IFS='|' read -r _lead id auto _kind value env_var file_path _date _purpose _tail <<< "$line"
    ROW_ID="$(clean_cell "$id")"
    ROW_AUTO="$(clean_cell "$auto")"
    ROW_VALUE="$(clean_value_cell "$value")"
    ROW_ENV_VAR="$(clean_cell "$env_var")"
    ROW_FILE_PATH="$(clean_cell "$file_path")"
}

is_placeholder_value() {
    local value="$1"
    [[ -z "$value" || "$value" == *"비어있음"* || "$value" == "(empty)" ]]
}

resolve_repo_path() {
    local rel_path="$1"
    if [[ -z "$rel_path" || "$rel_path" == "-" ]]; then
        printf '%s' ""
        return 0
    fi
    if [[ "$rel_path" == /* ]]; then
        die "absolute secret paths are not supported: ${rel_path}"
    fi
    printf '%s/%s' "$REPO_ROOT" "$rel_path"
}

make_temp_file() {
    local path
    path="$(mktemp)"
    chmod 600 "$path"
    TEMP_PATHS+=("$path")
    printf '%s' "$path"
}

check_required_tools() {
    local missing=0
    local tool
    for tool in git date mktemp rm cp mkdir chmod dirname mv tr head htpasswd; do
        if ! command -v "$tool" >/dev/null 2>&1; then
            error "Required tool '${tool}' not found."
            missing=1
        fi
    done
    return "$missing"
}

check_layout() {
    local failures=0

    check_required_tools || failures=1

    printf 'CHECK repo_root=%s\n' "$REPO_ROOT"

    if [[ -f "$EXAMPLE_FILE" ]]; then
        printf 'CHECK example_registry=present path=%s\n' "$EXAMPLE_FILE"
    else
        printf 'CHECK example_registry=missing path=%s\n' "$EXAMPLE_FILE"
        failures=1
    fi

    if [[ -e "$TARGET_FILE" ]]; then
        printf 'CHECK target_registry=present path=%s\n' "$TARGET_FILE"
    else
        printf 'CHECK target_registry=absent path=%s\n' "$TARGET_FILE"
    fi

    if [[ -e "$ENV_FILE" ]]; then
        printf 'CHECK env_file=present path=%s\n' "$ENV_FILE"
    else
        printf 'CHECK env_file=absent path=%s\n' "$ENV_FILE"
    fi

    if [[ -e "${REPO_ROOT}/scripts/gen-secrets.sh" ]]; then
        printf 'CHECK root_duplicate=present path=%s\n' "${REPO_ROOT}/scripts/gen-secrets.sh"
        failures=1
    else
        printf 'CHECK root_duplicate=absent path=%s\n' "${REPO_ROOT}/scripts/gen-secrets.sh"
    fi

    if [[ -f "$IMPLEMENTATION_FILE" ]]; then
        printf 'CHECK implementation=present path=%s\n' "$IMPLEMENTATION_FILE"
    else
        printf 'CHECK implementation=missing path=%s\n' "$IMPLEMENTATION_FILE"
        failures=1
    fi

    return "$failures"
}

load_env_values() {
    local line stripped key value
    [[ -f "$ENV_FILE" ]] || return 0

    while IFS= read -r line || [[ -n "$line" ]]; do
        stripped="$(trim "$line")"
        [[ -z "$stripped" || "$stripped" == \#* ]] && continue
        [[ "$stripped" == *=* ]] || continue

        key="$(trim "${stripped%%=*}")"
        value="$(trim "${stripped#*=}")"
        value="${value%%[[:space:]]#*}"
        value="$(trim "$value")"
        value="$(strip_surrounding_quotes "$value")"

        if [[ -n "$key" ]]; then
            ENV_VALUES["$key"]="$value"
        fi
    done < "$ENV_FILE"
}

get_env_val() {
    local var_name="${1-}"
    if [[ -z "$var_name" || "$var_name" == "-" ]]; then
        return 1
    fi
    if [[ -v "ENV_VALUES[$var_name]" && -n "${ENV_VALUES[$var_name]}" ]]; then
        printf '%s' "${ENV_VALUES[$var_name]}"
        return 0
    fi
    return 1
}

gen_password() {
    local password=""
    local chunk=""
    while [[ "${#password}" -lt 16 ]]; do
        chunk="$(LC_ALL=C tr -dc 'A-Za-z0-9' < /dev/urandom | head -c "$((16 - ${#password}))" || true)"
        password+="$chunk"
    done
    printf '%s' "$password"
}

read_secret_file() {
    local path="$1"
    local value
    [[ -s "$path" ]] || return 1
    value="$(<"$path")"
    printf '%s' "$value"
}

write_secret_file() {
    local path="$1"
    local value="$2"
    mkdir -p -- "$(dirname "$path")"
    printf '%s' "$value" > "$path"
    # Owner plus the owner's primary group (SECRETS_GID); containers that do not
    # run as the owner read secret files through group_add, never "other".
    chmod 640 "$path" 2>/dev/null || true
}

generate_htpasswd_hash() {
    local user_value="$1"
    local pass_value="$2"
    local hashed

    if ! htpasswd -ni "$user_value" >/dev/null 2>&1 <<< "probe"; then
        die "htpasswd stdin mode is unavailable; refusing to expose password via argv."
    fi

    hashed="$(printf '%s\n' "$pass_value" | htpasswd -ni "$user_value")"
    printf '%s' "$(trim "$hashed")"
}

ensure_target_registry() {
    if [[ ! -f "$TARGET_FILE" ]]; then
        [[ -f "$EXAMPLE_FILE" ]] || die "example registry not found: ${EXAMPLE_FILE}"
        warn "Initializing registry from example: ${TARGET_FILE}"
        cp -- "$EXAMPLE_FILE" "$TARGET_FILE"
        chmod 600 "$TARGET_FILE" 2>/dev/null || true
    fi
}

collect_secret_values() {
    local line full_path new_value env_value

    while IFS= read -r line || [[ -n "$line" ]]; do
        if ! is_table_row "$line" || is_header_or_separator "$line"; then
            continue
        fi

        parse_row "$line"
        [[ -n "$ROW_ID" ]] || continue
        [[ "$ROW_ID" == "INFRA-003" || "$ROW_ID" == "INFRA-004" || "$ROW_ID" == "INFRA-007" ]] && continue

        full_path="$(resolve_repo_path "$ROW_FILE_PATH")"
        new_value=""

        if [[ -n "$full_path" && -s "$full_path" ]]; then
            new_value="$(read_secret_file "$full_path")"
        elif is_placeholder_value "$ROW_VALUE"; then
            env_value="$(get_env_val "$ROW_ENV_VAR" || true)"
            if [[ -n "$env_value" ]]; then
                new_value="$env_value"
            elif [[ "$ROW_AUTO" == "O" ]]; then
                new_value="$(gen_password)"
            fi
        else
            new_value="$ROW_VALUE"
        fi

        if [[ -n "$new_value" ]]; then
            SECRET_VALUES["$ROW_ID"]="$new_value"
            if [[ -n "$full_path" && ( ! -f "$full_path" || ! -s "$full_path" ) ]]; then
                write_secret_file "$full_path" "$new_value"
            fi
        fi
    done < "$TARGET_FILE"
}

process_htpasswd() {
    local target_id="$1"
    local user_id="$2"
    local pass_id="$3"
    local target_file_path="$4"
    local user_value="${SECRET_VALUES[$user_id]-}"
    local pass_value="${SECRET_VALUES[$pass_id]-}"
    local full_path hashed existing

    if [[ -z "$user_value" || -z "$pass_value" ]]; then
        return 0
    fi

    full_path="${REPO_ROOT}/${target_file_path}"

    # bcrypt salts differ per run, so compare by verifying, not by string:
    # an existing entry that still matches the ID and password is kept.
    if [[ -f "$full_path" && -s "$full_path" ]] &&
        printf '%s\n' "$pass_value" | htpasswd -vi "$full_path" "$user_value" >/dev/null 2>&1; then
        existing="$(read_secret_file "$full_path")"
        SECRET_VALUES["$target_id"]="$existing"
        return 0
    fi

    hashed="$(generate_htpasswd_hash "$user_value" "$pass_value")"
    if [[ -f "$full_path" && -s "$full_path" ]]; then
        warn "Updating htpasswd hash for ${target_id} to match current source IDs."
    fi
    write_secret_file "$full_path" "$hashed"

    SECRET_VALUES["$target_id"]="$hashed"
}

render_row_with_value() {
    local line="$1"
    local value="$2"
    local lead id auto kind _old_value env_var file_path _old_date purpose tail

    IFS='|' read -r lead id auto kind _old_value env_var file_path _old_date purpose tail <<< "$line"
    # The date cell is public metadata; writing a value never changes it.
    printf '%s|%s|%s|%s| `%s` |%s|%s|%s|%s|%s\n' \
        "$lead" "$id" "$auto" "$kind" "$value" "$env_var" "$file_path" "$_old_date" "$purpose" "$tail"
}

rewrite_registry() {
    local final_temp line current_value value
    final_temp="$(make_temp_file)"

    while IFS= read -r line || [[ -n "$line" ]]; do
        if is_table_row "$line" && ! is_header_or_separator "$line"; then
            parse_row "$line"
            if [[ -n "$ROW_ID" && -v "SECRET_VALUES[$ROW_ID]" ]]; then
                value="${SECRET_VALUES[$ROW_ID]}"
                current_value="$ROW_VALUE"
                if [[ "$value" != "$current_value" ]] || is_placeholder_value "$current_value"; then
                    render_row_with_value "$line" "$value" >> "$final_temp"
                else
                    printf '%s\n' "$line" >> "$final_temp"
                fi
            else
                printf '%s\n' "$line" >> "$final_temp"
            fi
        else
            printf '%s\n' "$line" >> "$final_temp"
        fi
    done < "$TARGET_FILE"

    mv -- "$final_temp" "$TARGET_FILE"
}

run_generation() {
    printf '%b=== hy-home.docker Secret Management System ===%b\n' "$BLUE" "$NC"
    check_required_tools
    ensure_target_registry
    load_env_values

    info "Processing secrets..."
    collect_secret_values

    process_htpasswd "INFRA-003" "INFRA-001" "INFRA-002" "secrets/auth/traefik_basicauth_password.txt"
    process_htpasswd "INFRA-004" "OBS-003" "OBS-004" "secrets/auth/traefik_opensearch_basicauth_password.txt"
    process_htpasswd "INFRA-007" "OBS-012" "OBS-013" "secrets/auth/traefik_prometheus_api_htpasswd.txt"

    info "Updating Markdown registry..."
    rewrite_registry

    printf '%bProcessing complete!%b\n' "$GREEN" "$NC"
    printf 'Registry updated: %s\n' "$TARGET_FILE"
}

dry_run_action_for_row() {
    local full_path="$1"
    local action

    if [[ "$ROW_ID" == "INFRA-003" || "$ROW_ID" == "INFRA-004" || "$ROW_ID" == "INFRA-007" ]]; then
        printf '%s' "derive-htpasswd"
        return 0
    fi

    if [[ -n "$full_path" ]]; then
        if [[ -s "$full_path" ]]; then
            action="keep-existing-file"
        elif [[ -e "$full_path" ]]; then
            action="fill-empty-file"
        elif [[ "$ROW_AUTO" == "O" ]]; then
            action="create-generated-file"
        elif [[ -n "$ROW_ENV_VAR" && "$ROW_ENV_VAR" != "-" ]]; then
            action="create-from-env-if-set"
        else
            action="manual-file-required"
        fi
    elif [[ "$ROW_AUTO" == "O" ]]; then
        action="update-registry-generated-value"
    elif [[ -n "$ROW_ENV_VAR" && "$ROW_ENV_VAR" != "-" ]]; then
        action="update-registry-from-env-if-set"
    else
        action="manual-registry-required"
    fi

    printf '%s' "$action"
}

run_dry_run() {
    local line full_path action total=0

    # Metadata-only inspection does not require htpasswd or generation tools.
    [[ -f "$EXAMPLE_FILE" ]] || die "example registry not found: ${EXAMPLE_FILE}"

    printf 'DRY-RUN source=example-registry path=%s\n' "$EXAMPLE_FILE"
    printf 'DRY-RUN target_registry_path=%s\n' "$TARGET_FILE"
    printf 'DRY-RUN note=values-not-read-or-written\n'

    while IFS= read -r line || [[ -n "$line" ]]; do
        if ! is_table_row "$line" || is_header_or_separator "$line"; then
            continue
        fi

        parse_row "$line"
        [[ -n "$ROW_ID" ]] || continue
        full_path="$(resolve_repo_path "$ROW_FILE_PATH")"
        action="$(dry_run_action_for_row "$full_path")"
        total=$((total + 1))

        if [[ -n "$ROW_FILE_PATH" && "$ROW_FILE_PATH" != "-" ]]; then
            printf 'DRY-RUN id=%s action=%s path=%s\n' "$ROW_ID" "$action" "$ROW_FILE_PATH"
        else
            printf 'DRY-RUN id=%s action=%s path=-\n' "$ROW_ID" "$action"
        fi
    done < "$EXAMPLE_FILE"

    printf 'DRY-RUN summary rows=%d\n' "$total"
}


run_metadata_sync() {
    python3 - "$REPO_ROOT" "$MODE" <<'PY_METADATA'
import os
from pathlib import Path
import re
import stat
import sys
import tempfile

root = Path(sys.argv[1]).resolve()
mode = sys.argv[2]
check_only = mode.endswith("-check")
prune = mode.startswith("sync-metadata-prune")


def safe_path(relative):
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("unsafe metadata path")
    target = root / path
    for item in (target, *target.parents):
        if item == root:
            break
        if item.is_symlink():
            raise ValueError("symlink metadata path")
    if not target.resolve().is_relative_to(root):
        raise ValueError("metadata path escapes repository")
    return target


def clean(cell):
    return cell.strip().strip("*`").strip()


def rows(text, strict):
    result = {}
    for line in text.splitlines(keepends=True):
        if not line.lstrip().startswith("|"):
            continue
        cells = line.split("|")
        if strict and len(cells) != 10:
            raise ValueError("malformed registry row")
        identity = clean(cells[1]) if len(cells) > 1 else ""
        if identity == "ID" or re.fullmatch(r":?-{3,}:?", identity):
            continue
        if not re.fullmatch(r"[A-Z][A-Z0-9_-]*-[0-9]+", identity):
            if strict:
                raise ValueError("malformed registry identity")
            continue
        if len(cells) != 10:
            raise ValueError("malformed registry row")
        if identity in result:
            raise ValueError("duplicate registry identity")
        relative = clean(cells[6])
        if relative and relative != "-":
            path = safe_path(relative)
            if not path.is_relative_to(root / "secrets"):
                raise ValueError("secret metadata path outside secret directory")
        result[identity] = (line, cells)
    return result


def registry_plan(source, current, exact):
    """Render the private registry as the public one with private values.

    Every line except a row's value cell comes from the public registry, in
    its order, so the two files differ only in values. A private row the
    public registry lacks is kept at the end unless pruning.
    """
    public = rows(source, exact)
    private = rows(current, exact)
    if not current:
        return source
    output = source
    for identity, (line, cells) in public.items():
        if identity in private:
            merged = list(cells)
            merged[4] = private[identity][1][4]
            output = output.replace(line, "|".join(merged), 1)
    extra = [line for identity, (line, _) in private.items() if identity not in public]
    if extra and not exact:
        output += ("" if output.endswith("\n") else "\n") + "\n## Private-only rows\n\n"
        output += "| ID | Auto | Kind | Value | Env | Path | Date | Purpose |\n"
        output += "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
        output += "".join(extra)
    return output


def env_assignment_key(line, strict):
    body = line.rstrip("\r\n")
    stripped = body.strip()
    if not stripped or stripped.startswith("#"):
        return None
    if not strict:
        match = re.match(r"\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=", line)
        return match[1] if match else None
    match = re.fullmatch(r"\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)", body)
    if match is None:
        raise ValueError("unparseable environment line")
    value = match.group(2)
    if (len(value) - len(value.rstrip("\\"))) % 2:
        raise ValueError("continued environment assignment")
    candidate = value.lstrip()
    if candidate.startswith(('"', "'")):
        quote = candidate[0]
        escaped = False
        closing = None
        for index, character in enumerate(candidate[1:], 1):
            if quote == '"' and character == "\\" and not escaped:
                escaped = True
                continue
            if character == quote and not escaped:
                closing = index
                break
            escaped = False
        if closing is None:
            raise ValueError("multiline environment assignment")
        tail = candidate[closing + 1:].strip()
        if tail and not tail.startswith("#"):
            raise ValueError("ambiguous environment assignment")
    return match.group(1)


def env_keys(text, strict):
    result = {}
    for line in text.splitlines(keepends=True):
        key = env_assignment_key(line, strict)
        if key is None:
            continue
        if key in result:
            raise ValueError("duplicate environment key")
        result[key] = line
    return result


def env_plan(source, current, exact):
    public, private = env_keys(source, exact), env_keys(current, exact)
    if not current:
        return source
    if exact:
        output = "".join(
            line for line in current.splitlines(keepends=True)
            if (key := env_assignment_key(line, True)) is None or key in public
        )
    else:
        output = current
    additions = "".join(line for key, line in public.items() if key not in private)
    if additions:
        output += ("" if output.endswith("\n") or not output else "\n") + additions
    return output


def snapshot(path):
    safe_path(path.relative_to(root))
    if not path.exists():
        return None, None
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode):
        raise ValueError("metadata target must be regular")
    return path.read_bytes(), (info.st_dev, info.st_ino, info.st_mtime_ns, info.st_mode)


def replace(path, payload, mode):
    safe_path(path.relative_to(root))
    descriptor, name = tempfile.mkstemp(prefix=".metadata-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            os.fchmod(stream.fileno(), mode)
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def main():
    specifications = (("secrets/SENSITIVE_ENV_VARS.md.example", "secrets/SENSITIVE_ENV_VARS.md", registry_plan),
                      (".env.example", ".env", env_plan))
    plans = []
    for source_name, target_name, planner in specifications:
        source, target = safe_path(source_name), safe_path(target_name)
        before, identity = snapshot(target)
        public = source.read_bytes().decode("utf-8")
        current = (before or b"").decode("utf-8")
        after = planner(public, current, prune).encode("utf-8")
        current_mode = stat.S_IMODE(identity[3]) if identity else None
        if after != before or current_mode != 0o600:
            plans.append((target, before, identity, after))
    print("METADATA files_changed=" + str(len(plans)) + " values=preserved secret_files=untouched")
    if check_only:
        return int(bool(plans))
    for target, before, identity, _ in plans:
        if snapshot(target) != (before, identity):
            raise ValueError("metadata changed during planning")
    completed = []
    try:
        for target, before, identity, after in plans:
            if snapshot(target) != (before, identity):
                raise ValueError("metadata changed before replacement")
            replace(target, after, 0o600)
            completed.append((target, before, identity, after))
    except Exception:
        for target, before, identity, after in reversed(completed):
            # Never overwrite an operator edit made after this replacement.
            if target.read_bytes() == after:
                if before is None:
                    target.unlink()
                else:
                    replace(target, before, stat.S_IMODE(identity[3]))
        raise
    return 0


try:
    raise SystemExit(main())
except Exception:
    print("METADATA rejected: unsafe, ambiguous, changed or unreadable input; no values logged", file=sys.stderr)
    raise SystemExit(2)
PY_METADATA
}

main() {
    parse_args "$@"
    case "$MODE" in
        help)
            usage
            ;;
        check)
            check_layout
            ;;
        dry-run)
            run_dry_run
            ;;
        sync-metadata|sync-metadata-check|sync-metadata-prune|sync-metadata-prune-check)
            run_metadata_sync
            ;;
        run)
            run_generation
            ;;
        *)
            die "unsupported mode: ${MODE}"
            ;;
    esac
}

main "$@"
