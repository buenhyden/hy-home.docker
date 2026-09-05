#!/usr/bin/env bash

set -o pipefail

SOURCE_IMAGE='postgres:17.6-alpine@sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94'
TARGET_IMAGE='postgres:18.4-alpine@sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15'
DUMP_CLIENT_IMAGE='postgres:18.4-alpine@sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15'
SOURCE_IMAGE_REPO_DIGEST='postgres@sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94'
TARGET_IMAGE_REPO_DIGEST='postgres@sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15'
DUMP_CLIENT_IMAGE_REPO_DIGEST='postgres@sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15'
SOURCE_IMAGE_TARGET_DESCRIPTOR_DIGEST='sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94'
TARGET_IMAGE_TARGET_DESCRIPTOR_DIGEST='sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15'
DUMP_CLIENT_IMAGE_TARGET_DESCRIPTOR_DIGEST='sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15'
SOURCE_IMAGE_CONFIG_ID='sha256:d741b376874687de90374fd34f55c6b2760e8f7bd7e4ae5cd47f50757fc08cf8'
TARGET_IMAGE_CONFIG_ID='sha256:bd1890816ae0b8ad4644f05728570d4be774e1f1490d7232f5084b52ea335183'
DUMP_CLIENT_IMAGE_CONFIG_ID='sha256:bd1890816ae0b8ad4644f05728570d4be774e1f1490d7232f5084b52ea335183'
PROJECT_PREFIX='hyhome-ior-20260719'
TOTAL_TIMEOUT=420
CLEANUP_RESERVE_SECONDS=60
CLEANUP_COMMAND_CAP_SECONDS=8
TIMEOUT_NEGATIVE_TOTAL_SECONDS=20
TIMEOUT_NEGATIVE_CLEANUP_RESERVE_SECONDS=8

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
FIXTURE_DIR="${ROOT_DIR}/tests/fixtures/postgres-logical-upgrade"
COMPOSE_FILE="${FIXTURE_DIR}/docker-compose.yml"
SEED_SQL="${FIXTURE_DIR}/sql/001_schema_and_seed.sql"
ORACLE_SQL="${FIXTURE_DIR}/sql/010_integrity_oracle.sql"
PARTIAL_SQL="${FIXTURE_DIR}/sql/020_negative_partial_state.sql"
IMAGE_IDENTITY_CHECKER="${ROOT_DIR}/scripts/validation/check-supply-chain-policy.py"
HANDOFF_DIR="${ROOT_DIR}/_workspace/repo-support/task-2026-07-19-infrastructure-operations-readiness-remediation/postgres"
HANDOFF_PATH="${HANDOFF_DIR}/recovery-verdict.json"

SCRIPT_IS_SOURCED=false
TEST_SOURCE_BOUNDARY=false
if [ "${BASH_SOURCE[0]}" != "$0" ]; then
  SCRIPT_IS_SOURCED=true
  if [ "${IOR_SOURCE_ONLY:-}" = 1 ] && \
     [ "${IOR_TEST_SOURCE_ONLY:-}" = postgres-logical-upgrade-rehearsal-tests ]; then
    TEST_SOURCE_BOUNDARY=true
  fi
fi

RUN_MODE='normal'
NEGATIVE_CASE=''
RUN_ID="$$"
EVIDENCE_DIR="/tmp/hyhome-ior-evidence.${RUN_ID}"
if [ "$TEST_SOURCE_BOUNDARY" = true ]; then
  RUN_ID="${IOR_RUN_ID:-$$}"
  EVIDENCE_DIR="${IOR_EVIDENCE_DIR:-/tmp/hyhome-ior-evidence.${RUN_ID}}"
fi
SOURCE_PROJECT="${PROJECT_PREFIX}-${RUN_ID}-source"
TARGET_PROJECT="${PROJECT_PREFIX}-${RUN_ID}-target"
CANDIDATE_PATH="${EVIDENCE_DIR}/recovery-verdict.candidate.json"
DUMP_PATH="${EVIDENCE_DIR}/rehearsal.dump"
SOURCE_ORACLE_PATH="${EVIDENCE_DIR}/source-oracle.json"
TARGET_ORACLE_PATH="${EVIDENCE_DIR}/target-oracle.json"
RENDERED_TOPOLOGY_PATH="${EVIDENCE_DIR}/compose-rendered.source.json"
TARGET_RENDERED_TOPOLOGY_PATH="${EVIDENCE_DIR}/compose-rendered.target.json"
RUNTIME_LOG="${EVIDENCE_DIR}/runtime.log"
CLIENT_LABEL_OWNER='com.hyhome.ior.owner'
CLIENT_LABEL_RUN='com.hyhome.ior.run'

IOR_POSTGRES_PASSWORD=''
FIXTURE_SHA256=''
DUMP_SHA256=''
DUMP_BYTES=0
BACKUP_SECONDS=0
RESTORE_SECONDS=0
SOURCE_OWNED=false
TARGET_OWNED=false
PUBLISH_ALLOWED=false
CANDIDATE_WRITTEN=false
CANDIDATE_JSON=''
CLEANUP_COMPLETE=false
SIGNAL_RECEIVED=false
RUN_START_SECONDS=0
RUN_DEADLINE=0
OPERATION_DEADLINE=0
ACTIVE_TOTAL_TIMEOUT=$TOTAL_TIMEOUT
ACTIVE_CLEANUP_RESERVE=$CLEANUP_RESERVE_SECONDS
DUMP_CLIENT_ID=''
DUMP_CLIENT_MAY_EXIST=false
EVIDENCE_OWNED=false
EVIDENCE_DEVICE_INODE=''
EVIDENCE_OWNER_UID=''
EVIDENCE_REMOVED=false

print_failure() {
  printf 'status=failed failure_class=%s reason=%s\n' "$1" "$2"
}

reject_direct_test_controls() {
  local variable

  [ "$SCRIPT_IS_SOURCED" = false ] || return 0
  for variable in \
    IOR_RUN_ID \
    IOR_EVIDENCE_DIR \
    IOR_PROJECT_PREFIX \
    IOR_TEST_MODE \
    IOR_TEST_TOTAL_TIMEOUT \
    IOR_TEST_CLEANUP_RESERVE \
    IOR_SOURCE_ONLY \
    IOR_TEST_SOURCE_ONLY; do
    if [[ -v "$variable" ]]; then
      return 10
    fi
  done
}

remaining_until() {
  local deadline="$1"
  local remaining=$((deadline - SECONDS))

  if [ "$remaining" -lt 1 ]; then
    return 124
  fi
  printf '%s\n' "$remaining"
}

run_bounded() {
  local remaining

  remaining="$(remaining_until "$OPERATION_DEADLINE")" || return 124
  timeout --signal=KILL "${remaining}s" "$@"
}

run_cleanup_bounded() {
  local remaining
  local cap

  remaining="$(remaining_until "$RUN_DEADLINE")" || return 124
  cap=$remaining
  if [ "$cap" -gt "$CLEANUP_COMMAND_CAP_SECONDS" ]; then
    cap=$CLEANUP_COMMAND_CAP_SECONDS
  fi
  timeout --signal=KILL "${cap}s" "$@"
}

parse_args() {
  if [ "$#" -eq 0 ]; then
    return 0
  fi

  case "$1" in
    --check-config-only)
      [ "$#" -eq 1 ] || return 2
      RUN_MODE='check'
      ;;
    --negative-case)
      [ "$#" -eq 2 ] || return 2
      case "$2" in
        checksum-mismatch|partial-state|bad-target-major|timeout)
          NEGATIVE_CASE="$2"
          RUN_MODE='negative'
          ;;
        *) return 2 ;;
      esac
      ;;
    *) return 2 ;;
  esac
}

prepare_default_handoff_dir() {
  python3 - "$ROOT_DIR" "$HANDOFF_DIR" <<'PY'
import os
from pathlib import Path
import stat
import sys

root = Path(sys.argv[1])
handoff = Path(sys.argv[2])
anchor = root / "_workspace" / "repo-support"
expected = anchor / "task-2026-07-19-infrastructure-operations-readiness-remediation" / "postgres"
if handoff != expected:
    raise SystemExit(1)
if anchor.resolve(strict=True) != anchor or not stat.S_ISDIR(anchor.lstat().st_mode):
    raise SystemExit(1)

flags = os.O_RDONLY | os.O_DIRECTORY
if hasattr(os, "O_NOFOLLOW"):
    flags |= os.O_NOFOLLOW
fd = os.open(anchor, flags)
try:
    for component in (
        "task-2026-07-19-infrastructure-operations-readiness-remediation",
        "postgres",
    ):
        try:
            os.mkdir(component, 0o700, dir_fd=fd)
        except FileExistsError:
            pass
        next_fd = os.open(component, flags, dir_fd=fd)
        info = os.fstat(next_fd)
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid():
            os.close(next_fd)
            raise SystemExit(1)
        if stat.S_IMODE(info.st_mode) & 0o022:
            os.close(next_fd)
            raise SystemExit(1)
        os.close(fd)
        fd = next_fd
finally:
    os.close(fd)
PY
}

validate_handoff_parent() {
  python3 - "$HANDOFF_DIR" "$HANDOFF_PATH" <<'PY'
import os
from pathlib import Path
import stat
import sys

parent = Path(sys.argv[1])
target = Path(sys.argv[2])
try:
    parent_info = parent.lstat()
except OSError:
    raise SystemExit(1)
if target.parent != parent:
    raise SystemExit(1)
if not stat.S_ISDIR(parent_info.st_mode) or stat.S_ISLNK(parent_info.st_mode):
    raise SystemExit(1)
if parent.resolve(strict=True) != parent.absolute():
    raise SystemExit(1)
if parent_info.st_uid != os.getuid() or stat.S_IMODE(parent_info.st_mode) & 0o022:
    raise SystemExit(1)
PY
}

invalidate_canonical_handoff() {
  validate_handoff_parent || return 1
  python3 - "$HANDOFF_PATH" <<'PY'
import os
from pathlib import Path
import stat
import sys

target = Path(sys.argv[1])
try:
    info = target.lstat()
except FileNotFoundError:
    raise SystemExit(0)
except OSError:
    raise SystemExit(1)
if not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode):
    raise SystemExit(1)
if info.st_uid != os.getuid():
    raise SystemExit(1)
try:
    target.unlink()
except OSError:
    raise SystemExit(1)
try:
    target.lstat()
except FileNotFoundError:
    raise SystemExit(0)
raise SystemExit(1)
PY
}

create_owned_evidence_dir() {
  local identity

  [ "$EVIDENCE_DIR" = "/tmp/hyhome-ior-evidence.${RUN_ID}" ] || return 10
  if [ -e "$EVIDENCE_DIR" ] || [ -L "$EVIDENCE_DIR" ]; then
    return 10
  fi
  umask 077
  mkdir -m 700 -- "$EVIDENCE_DIR" || return 10
  identity="$(python3 - "$EVIDENCE_DIR" <<'PY'
import os
from pathlib import Path
import stat
import sys

path = Path(sys.argv[1])
info = path.lstat()
if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
    raise SystemExit(1)
if path.resolve(strict=True) != path.absolute():
    raise SystemExit(1)
if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o700:
    raise SystemExit(1)
print(f"{info.st_uid}:{info.st_dev}:{info.st_ino}")
PY
  )" || return 10
  EVIDENCE_OWNER_UID="${identity%%:*}"
  EVIDENCE_DEVICE_INODE="${identity#*:}"
  EVIDENCE_OWNED=true
  EVIDENCE_REMOVED=false
}

verify_evidence_ownership() {
  [ "$EVIDENCE_OWNED" = true ] || return 1
  [ "$EVIDENCE_REMOVED" = false ] || return 1
  python3 - "$EVIDENCE_DIR" "$EVIDENCE_OWNER_UID" "$EVIDENCE_DEVICE_INODE" <<'PY'
from pathlib import Path
import stat
import sys

path = Path(sys.argv[1])
expected_uid = int(sys.argv[2])
expected_identity = sys.argv[3]
try:
    info = path.lstat()
except OSError:
    raise SystemExit(1)
if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
    raise SystemExit(1)
if path.resolve(strict=True) != path.absolute():
    raise SystemExit(1)
if info.st_uid != expected_uid or stat.S_IMODE(info.st_mode) != 0o700:
    raise SystemExit(1)
if f"{info.st_dev}:{info.st_ino}" != expected_identity:
    raise SystemExit(1)
PY
}

create_owned_evidence_file() {
  local path="$1"

  verify_evidence_ownership || return 1
  case "$path" in
    "$EVIDENCE_DIR"/*) ;;
    *) return 1 ;;
  esac
  python3 - "$path" <<'PY'
import os
from pathlib import Path
import sys

path = Path(sys.argv[1])
flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
if hasattr(os, "O_NOFOLLOW"):
    flags |= os.O_NOFOLLOW
fd = os.open(path, flags, 0o600)
os.close(fd)
PY
}

remove_owned_evidence_file() {
  local path="$1"

  verify_evidence_ownership || return 1
  case "$path" in
    "$EVIDENCE_DIR"/*) ;;
    *) return 1 ;;
  esac
  python3 - "$path" "$EVIDENCE_OWNER_UID" <<'PY'
import os
from pathlib import Path
import stat
import sys

path = Path(sys.argv[1])
expected_uid = int(sys.argv[2])
try:
    info = path.lstat()
except FileNotFoundError:
    raise SystemExit(0)
except OSError:
    raise SystemExit(1)
if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
    raise SystemExit(1)
if info.st_uid != expected_uid:
    raise SystemExit(1)
try:
    path.unlink()
except OSError:
    raise SystemExit(1)
PY
}

cleanup_owned_evidence_dir() {
  local failed=0
  local path

  if [ "$EVIDENCE_OWNED" != true ]; then
    return 0
  fi
  if [ "$EVIDENCE_REMOVED" = true ]; then
    return 0
  fi
  verify_evidence_ownership || return 60
  for path in \
    "$DUMP_PATH" \
    "$SOURCE_ORACLE_PATH" \
    "$TARGET_ORACLE_PATH" \
    "$RENDERED_TOPOLOGY_PATH" \
    "$TARGET_RENDERED_TOPOLOGY_PATH" \
    "$CANDIDATE_PATH" \
    "$RUNTIME_LOG"; do
    if ! remove_owned_evidence_file "$path"; then
      failed=1
    fi
  done
  [ "$failed" -eq 0 ] || return 60
  verify_evidence_ownership || return 60
  python3 - "$EVIDENCE_DIR" "$EVIDENCE_OWNER_UID" "$EVIDENCE_DEVICE_INODE" <<'PY'
from pathlib import Path
import stat
import sys

path = Path(sys.argv[1])
expected_uid = int(sys.argv[2])
expected_identity = sys.argv[3]
info = path.lstat()
if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
    raise SystemExit(1)
if info.st_uid != expected_uid or f"{info.st_dev}:{info.st_ino}" != expected_identity:
    raise SystemExit(1)
path.rmdir()
PY
  [ ! -e "$EVIDENCE_DIR" ] && [ ! -L "$EVIDENCE_DIR" ] || return 60
  EVIDENCE_REMOVED=true
}

initialize_deadline_budget() {
  ACTIVE_TOTAL_TIMEOUT=$TOTAL_TIMEOUT
  ACTIVE_CLEANUP_RESERVE=$CLEANUP_RESERVE_SECONDS
  if [ "$NEGATIVE_CASE" = timeout ]; then
    ACTIVE_TOTAL_TIMEOUT=$TIMEOUT_NEGATIVE_TOTAL_SECONDS
    ACTIVE_CLEANUP_RESERVE=$TIMEOUT_NEGATIVE_CLEANUP_RESERVE_SECONDS
  fi
  if [ "$TEST_SOURCE_BOUNDARY" = true ]; then
    ACTIVE_TOTAL_TIMEOUT="${IOR_TEST_TOTAL_TIMEOUT:-$ACTIVE_TOTAL_TIMEOUT}"
    ACTIVE_CLEANUP_RESERVE="${IOR_TEST_CLEANUP_RESERVE:-$ACTIVE_CLEANUP_RESERVE}"
  fi
  [[ "$ACTIVE_TOTAL_TIMEOUT" =~ ^[0-9]+$ ]] || return 10
  [[ "$ACTIVE_CLEANUP_RESERVE" =~ ^[0-9]+$ ]] || return 10
  [ "$ACTIVE_TOTAL_TIMEOUT" -gt "$ACTIVE_CLEANUP_RESERVE" ] || return 10
  [ "$ACTIVE_CLEANUP_RESERVE" -ge 1 ] || return 10
  RUN_START_SECONDS=$SECONDS
  RUN_DEADLINE=$((RUN_START_SECONDS + ACTIVE_TOTAL_TIMEOUT))
  OPERATION_DEADLINE=$((RUN_DEADLINE - ACTIVE_CLEANUP_RESERVE))
}

initialize_runtime_state() {
  initialize_deadline_budget || return 10
  RENDERED_TOPOLOGY_PATH="${EVIDENCE_DIR}/compose-rendered.source.json"
  TARGET_RENDERED_TOPOLOGY_PATH="${EVIDENCE_DIR}/compose-rendered.target.json"
  create_owned_evidence_dir || return 10
  create_owned_evidence_file "$RUNTIME_LOG" || return 10
  IOR_POSTGRES_PASSWORD="$(od -An -N24 -tx1 /dev/urandom | tr -d ' \n')"
  [ "${#IOR_POSTGRES_PASSWORD}" -eq 48 ] || return 10
  export IOR_POSTGRES_PASSWORD
}

validate_rendered_topology_file() {
  local rendered_path="$1"
  local expected_project="$2"

  python3 - "$rendered_path" "$SOURCE_IMAGE" "$TARGET_IMAGE" "$expected_project" <<'PY'
import json
import os
import re
import sys

path, expected_source, expected_target, expected_project = sys.argv[1:]
expected_password = os.environ.get("IOR_POSTGRES_PASSWORD")

def reject(reason: str) -> None:
    print(reason)
    raise SystemExit(1)

try:
    with open(path, encoding="utf-8") as handle:
        document = json.load(handle)
except (OSError, ValueError):
    reject("compose-render-invalid-json")

if not isinstance(document, dict) or set(document) != {"name", "services", "networks"}:
    reject("unsafe-topology-extra")
if document.get("name") != expected_project:
    reject("unsafe-project-name")
services = document.get("services")
if not isinstance(services, dict) or set(services) != {"source", "target"}:
    reject("compose-service-set-invalid")
networks = document.get("networks")
if not isinstance(networks, dict) or set(networks) != {"default"}:
    reject("unsafe-network")
default_network = networks["default"]
if not isinstance(default_network, dict):
    reject("unsafe-network")
if default_network.get("external") not in (None, False):
    reject("unsafe-network")
if set(default_network) - {"name", "ipam", "external"}:
    reject("unsafe-network")
if default_network.get("name") != f"{expected_project}_default":
    reject("unsafe-network")
if default_network.get("ipam") not in (None, {}):
    reject("unsafe-network")
if not isinstance(expected_password, str) or not expected_password:
    reject("unsafe-environment")

images = {name: services[name].get("image") for name in services}
source_match = re.match(r"^postgres:(\d+)\.", images["source"] or "")
target_match = re.match(r"^postgres:(\d+)\.", images["target"] or "")
if source_match is None or int(source_match.group(1)) != 17:
    reject("bad-source-major")
if target_match is None or int(target_match.group(1)) != 18:
    reject("bad-target-major")
if images["source"] != expected_source:
    reject("source-image-drift")
if images["target"] != expected_target:
    reject("target-image-drift")

allowed_keys = {
    "command",
    "entrypoint",
    "environment",
    "healthcheck",
    "image",
    "networks",
    "pull_policy",
    "volumes",
}
for name, expected_target_path in {
    "source": "/var/lib/postgresql/data",
    "target": "/var/lib/postgresql",
}.items():
    service = services[name]
    if not isinstance(service, dict):
        reject("unsafe-service-option")
    if set(service) - allowed_keys:
        reject("unsafe-service-option")
    if service.get("command") not in (None, []):
        reject("unsafe-service-option")
    if service.get("entrypoint") not in (None, []):
        reject("unsafe-service-option")
    if service.get("networks") != {"default": None}:
        reject("unsafe-network")
    environment = service.get("environment")
    if not isinstance(environment, dict) or set(environment) != {
        "POSTGRES_DB",
        "POSTGRES_PASSWORD",
        "POSTGRES_USER",
    }:
        reject("unsafe-environment")
    if environment.get("POSTGRES_DB") != "rehearsal" or environment.get("POSTGRES_USER") != "rehearsal":
        reject("unsafe-environment")
    if environment.get("POSTGRES_PASSWORD") != expected_password:
        reject("unsafe-environment")
    healthcheck = service.get("healthcheck")
    if healthcheck != {
        "test": ["CMD-SHELL", "pg_isready -U rehearsal -d rehearsal"],
        "timeout": "2s",
        "interval": "2s",
        "retries": 30,
    }:
        reject("unsafe-healthcheck")
    volumes = service.get("volumes")
    if not isinstance(volumes, list) or len(volumes) != 1:
        reject("unsafe-volume")
    volume = volumes[0]
    if not isinstance(volume, dict):
        reject("unsafe-volume")
    if volume.get("type") != "volume" or volume.get("target") != expected_target_path:
        reject("unsafe-volume")
    if volume.get("source") not in (None, "") or volume.get("read_only") not in (None, False):
        reject("unsafe-volume")
    if set(volume) - {"type", "target", "volume", "source", "read_only"}:
        reject("unsafe-volume")
    if service.get("pull_policy") != "never":
        reject("unsafe-pull-policy")
PY
}

mutate_rendered_bad_target_major() {
  local rendered_path="$1"

  verify_evidence_ownership || return 1
  python3 - "$rendered_path" <<'PY'
import json
from pathlib import Path
import sys

path = Path(sys.argv[1])
document = json.loads(path.read_text(encoding="utf-8"))
document["services"]["target"]["image"] = (
    "postgres:19.0-alpine@sha256:"
    "9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15"
)
path.write_text(json.dumps(document, sort_keys=True), encoding="utf-8")
PY
}

render_and_validate_project_topology() {
  local project="$1"
  local rendered_path="$2"
  local mutate_bad_major="$3"
  local reason

  verify_evidence_ownership || {
    print_failure preflight evidence-ownership-lost
    return 10
  }
  if ! (set -o noclobber; run_bounded docker compose -p "$project" -f "$COMPOSE_FILE" \
    config --format json >"$rendered_path"); then
    print_failure preflight compose-render-failed
    return 10
  fi
  if [ "$mutate_bad_major" = true ]; then
    mutate_rendered_bad_target_major "$rendered_path" || {
      print_failure preflight compose-render-mutation-failed
      return 10
    }
  fi
  verify_evidence_ownership || {
    print_failure preflight evidence-ownership-lost
    return 10
  }
  reason="$(validate_rendered_topology_file "$rendered_path" "$project")" || {
    print_failure preflight "${reason:-compose-topology-invalid}"
    return 10
  }
}

render_and_validate_topology() {
  render_and_validate_project_topology \
    "$SOURCE_PROJECT" "$RENDERED_TOPOLOGY_PATH" false || return $?
  if [ "$NEGATIVE_CASE" = bad-target-major ]; then
    render_and_validate_project_topology \
      "$TARGET_PROJECT" "$TARGET_RENDERED_TOPOLOGY_PATH" true || return $?
  else
    render_and_validate_project_topology \
      "$TARGET_PROJECT" "$TARGET_RENDERED_TOPOLOGY_PATH" false || return $?
  fi
}

query_project_resource_state() {
  local project="$1"
  local phase="$2"
  local output
  local failed=0
  local present=0
  local runner=run_bounded

  [ "$phase" = cleanup ] && runner=run_cleanup_bounded
  output="$("$runner" docker ps -aq --filter "label=com.docker.compose.project=${project}")" || failed=1
  [ -z "$output" ] || present=1
  output="$("$runner" docker network ls -q --filter "label=com.docker.compose.project=${project}")" || failed=1
  [ -z "$output" ] || present=1
  output="$("$runner" docker volume ls -q --filter "label=com.docker.compose.project=${project}")" || failed=1
  [ -z "$output" ] || present=1
  [ "$failed" -eq 0 ] || return 2
  [ "$present" -eq 0 ] || return 0
  return 1
}

cleanup_log_path() {
  if [ "$EVIDENCE_OWNED" = true ] && \
     [ "$EVIDENCE_REMOVED" = false ] && \
     verify_evidence_ownership; then
    printf '%s\n' "$RUNTIME_LOG"
  else
    printf '/dev/null\n'
  fi
}

query_labeled_client_state() {
  local phase="$1"
  local output
  local runner=run_bounded

  [ "$phase" = cleanup ] && runner=run_cleanup_bounded
  output="$("$runner" docker ps -aq \
    --filter "label=${CLIENT_LABEL_OWNER}=${PROJECT_PREFIX}" \
    --filter "label=${CLIENT_LABEL_RUN}=${RUN_ID}")" || return 2
  [ -n "$output" ] || return 1
  printf '%s\n' "$output"
}

assert_no_project_collisions() {
  local project
  local state

  for project in "$SOURCE_PROJECT" "$TARGET_PROJECT"; do
    query_project_resource_state "$project" operation >/dev/null
    state=$?
    case "$state" in
      0)
        print_failure preflight project-collision
        return 10
        ;;
      1) ;;
      *)
        print_failure preflight docker-query-failed
        return 10
        ;;
    esac
  done
  query_labeled_client_state operation >/dev/null
  state=$?
  case "$state" in
    0)
      print_failure preflight project-collision
      return 10
      ;;
    1) ;;
    *)
      print_failure preflight docker-query-failed
      return 10
      ;;
  esac
}

observe_local_image_config_digest() {
  local image="$1"
  local archive config_digest status=0

  archive="$(mktemp "${EVIDENCE_DIR}/image-config.XXXXXX")" || return 10
  chmod 600 "$archive" || status=10
  if [ "$status" -eq 0 ]; then
    run_bounded docker image save --output "$archive" "$image" \
      >/dev/null 2>&1 || status=10
  fi
  if [ "$status" -eq 0 ]; then
    config_digest="$(
      run_bounded python3 "$IMAGE_IDENTITY_CHECKER" \
        --docker-save-config-digest "$archive"
    )" || status=10
  fi
  rm -f -- "$archive" || status=10
  [ "$status" -eq 0 ] || return "$status"
  printf '%s\n' "$config_digest"
}

assert_exact_local_image_identity() {
  local role="$1"
  local image="$2"
  local expected_repo_digest="$3"
  local expected_target_digest="$4"
  local expected_config_id="$5"
  local observed
  local actual_config_id

  observed="$(run_bounded docker image inspect --format '{{json .}}' "$image" 2>/dev/null)" || {
    print_failure preflight "${role}-image-not-local"
    return 10
  }
  [ -n "$observed" ] && [[ "$observed" != *$'\n'* ]] || {
    print_failure preflight "${role}-image-manifest-drift"
    return 10
  }
  python3 - "$observed" "$expected_repo_digest" \
    "$expected_target_digest" "$expected_config_id" <<'PY' || {
import json
import re
import sys

try:
    document = json.loads(sys.argv[1])
except (json.JSONDecodeError, TypeError):
    raise SystemExit(1)
repo_digests = document.get("RepoDigests") if isinstance(document, dict) else None
target_id = document.get("Id") if isinstance(document, dict) else None
descriptor = document.get("Descriptor") if isinstance(document, dict) else None
expected_repo, expected_target, expected_config = sys.argv[2:]
media_types = {
    "application/vnd.docker.distribution.manifest.list.v2+json",
    "application/vnd.docker.distribution.manifest.v2+json",
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.oci.image.manifest.v1+json",
}
raise SystemExit(0 if (
    isinstance(repo_digests, list)
    and expected_repo in repo_digests
    and re.fullmatch(r"sha256:[0-9a-f]{64}", expected_target)
    and re.fullmatch(r"sha256:[0-9a-f]{64}", expected_config)
    and expected_target != expected_config
    and isinstance(descriptor, dict)
    and descriptor.get("digest") == expected_target
    and descriptor.get("mediaType") in media_types
    and target_id in (expected_target, expected_config)
) else 1)
PY
    print_failure preflight "${role}-image-manifest-drift"
    return 10
  }
  actual_config_id="$(observe_local_image_config_digest "$image")" || {
    print_failure preflight "${role}-image-config-observation-failed"
    return 10
  }
  [ "$actual_config_id" = "$expected_config_id" ] || {
    print_failure preflight "${role}-image-config-id-drift"
    return 10
  }
}

assert_exact_local_image_identities() {
  assert_exact_local_image_identity \
    source "$SOURCE_IMAGE" "$SOURCE_IMAGE_REPO_DIGEST" \
    "$SOURCE_IMAGE_TARGET_DESCRIPTOR_DIGEST" "$SOURCE_IMAGE_CONFIG_ID" || return $?
  assert_exact_local_image_identity \
    target "$TARGET_IMAGE" "$TARGET_IMAGE_REPO_DIGEST" \
    "$TARGET_IMAGE_TARGET_DESCRIPTOR_DIGEST" "$TARGET_IMAGE_CONFIG_ID" || return $?
  assert_exact_local_image_identity \
    dump-client "$DUMP_CLIENT_IMAGE" \
    "$DUMP_CLIENT_IMAGE_REPO_DIGEST" \
    "$DUMP_CLIENT_IMAGE_TARGET_DESCRIPTOR_DIGEST" \
    "$DUMP_CLIENT_IMAGE_CONFIG_ID" || return $?
}

assert_safe_images_paths_and_project() {
  local required
  local command_name

  [ "$SOURCE_IMAGE" = 'postgres:17.6-alpine@sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94' ] || {
    print_failure preflight source-image-drift
    return 10
  }
  [ "$TARGET_IMAGE" = 'postgres:18.4-alpine@sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15' ] || {
    print_failure preflight target-image-drift
    return 10
  }
  [ "$DUMP_CLIENT_IMAGE" = 'postgres:18.4-alpine@sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15' ] || {
    print_failure preflight dump-client-image-drift
    return 10
  }
  [ "$SOURCE_IMAGE_REPO_DIGEST" = 'postgres@sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94' ] || {
    print_failure preflight source-image-repo-digest-drift
    return 10
  }
  [ "$TARGET_IMAGE_REPO_DIGEST" = 'postgres@sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15' ] || {
    print_failure preflight target-image-repo-digest-drift
    return 10
  }
  [ "$DUMP_CLIENT_IMAGE_REPO_DIGEST" = 'postgres@sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15' ] || {
    print_failure preflight dump-client-image-repo-digest-drift
    return 10
  }
  [ "$SOURCE_IMAGE_TARGET_DESCRIPTOR_DIGEST" = 'sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94' ] || {
    print_failure preflight source-image-target-descriptor-drift
    return 10
  }
  [ "$TARGET_IMAGE_TARGET_DESCRIPTOR_DIGEST" = 'sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15' ] || {
    print_failure preflight target-image-target-descriptor-drift
    return 10
  }
  [ "$DUMP_CLIENT_IMAGE_TARGET_DESCRIPTOR_DIGEST" = 'sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15' ] || {
    print_failure preflight dump-client-image-target-descriptor-drift
    return 10
  }
  [ "$SOURCE_IMAGE_CONFIG_ID" = 'sha256:d741b376874687de90374fd34f55c6b2760e8f7bd7e4ae5cd47f50757fc08cf8' ] || {
    print_failure preflight source-image-config-id-drift
    return 10
  }
  [ "$TARGET_IMAGE_CONFIG_ID" = 'sha256:bd1890816ae0b8ad4644f05728570d4be774e1f1490d7232f5084b52ea335183' ] || {
    print_failure preflight target-image-config-id-drift
    return 10
  }
  [ "$DUMP_CLIENT_IMAGE_CONFIG_ID" = 'sha256:bd1890816ae0b8ad4644f05728570d4be774e1f1490d7232f5084b52ea335183' ] || {
    print_failure preflight dump-client-image-config-id-drift
    return 10
  }
  [ "${IOR_PROJECT_PREFIX:-$PROJECT_PREFIX}" = "$PROJECT_PREFIX" ] || {
    print_failure preflight unsafe-project-prefix
    return 10
  }
  [[ "$RUN_ID" =~ ^[0-9]+$ ]] || {
    print_failure preflight unsafe-run-id
    return 10
  }
  [ "$EVIDENCE_DIR" = "/tmp/hyhome-ior-evidence.${RUN_ID}" ] || {
    print_failure preflight unsafe-evidence-path
    return 10
  }
  [ "$FIXTURE_DIR" = "${ROOT_DIR}/tests/fixtures/postgres-logical-upgrade" ] || {
    print_failure preflight unsafe-fixture-path
    return 10
  }
  for required in "$COMPOSE_FILE" "$SEED_SQL" "$ORACLE_SQL" "$PARTIAL_SQL" \
    "$IMAGE_IDENTITY_CHECKER"; do
    [ -f "$required" ] || {
      print_failure preflight fixture-missing
      return 10
    }
  done
  for command_name in docker sha256sum python3 timeout; do
    command -v "$command_name" >/dev/null 2>&1 || {
      print_failure preflight "command-missing-${command_name}"
      return 10
    }
  done
  assert_exact_local_image_identities || return $?
  if ! run_bounded docker compose version >>"$RUNTIME_LOG" 2>&1; then
    print_failure preflight docker-compose-unavailable
    return 10
  fi
  render_and_validate_topology || return $?
  assert_no_project_collisions || return $?
}

service_has_terminal_state() {
  local project="$1"
  local service="$2"
  local status
  local output

  for status in exited dead; do
    output="$(run_bounded docker compose -p "$project" -f "$COMPOSE_FILE" ps -q --status "$status" "$service" 2>>"$RUNTIME_LOG")" || return 2
    if [ -n "$output" ]; then
      return 0
    fi
  done
  return 1
}

read_database_identity() {
  local project="$1"
  local service="$2"
  local port="$3"

  [ "$port" = 1 ] || [ "$port" = 5432 ] || return 1
  # shellcheck disable=SC2016 # Expansion is intentionally in-container only.
  run_bounded docker compose -p "$project" -f "$COMPOSE_FILE" exec -T "$service" \
    sh -ec 'export PGPASSWORD="$POSTGRES_PASSWORD" PGCONNECT_TIMEOUT=1; exec psql "$@"' sh \
    -AtX -v ON_ERROR_STOP=1 -U rehearsal -d rehearsal \
    -h 127.0.0.1 -p "$port" \
    -c "SELECT pg_postmaster_start_time()" 2>>"$RUNTIME_LOG"
}

service_is_running_and_healthy() {
  local project="$1"
  local service="$2"
  local container_id
  local health

  container_id="$(run_bounded docker compose -p "$project" -f "$COMPOSE_FILE" \
    ps -q --status running "$service" 2>>"$RUNTIME_LOG")" || return 1
  [[ "$container_id" =~ ^[0-9a-f]{12,64}$ ]] || return 1
  health="$(run_bounded docker inspect \
    --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}missing{{end}}' \
    "$container_id" 2>>"$RUNTIME_LOG")" || return 1
  [ "$health" = healthy ]
}

database_readiness_stable() {
  local project="$1"
  local service="$2"
  local port="$3"
  local first_identity
  local second_identity

  # pg_isready can accept during the image's temporary initialization server.
  # Require two authenticated SQL identities across an interval, then confirm
  # that the same container remains running and healthy.
  first_identity="$(read_database_identity "$project" "$service" "$port")" || return 1
  [ -n "$first_identity" ] || return 1
  [[ "$first_identity" != *$'\n'* ]] || return 1
  run_bounded sleep 2 || return 1
  second_identity="$(read_database_identity "$project" "$service" "$port")" || return 1
  [ "$first_identity" = "$second_identity" ] || return 1
  service_is_running_and_healthy "$project" "$service"
}

start_source_and_wait() {
  local terminal_state

  verify_evidence_ownership || return 20
  SOURCE_OWNED=true
  if ! run_bounded docker compose -p "$SOURCE_PROJECT" -f "$COMPOSE_FILE" up -d --pull never --no-build --no-deps source >>"$RUNTIME_LOG" 2>&1; then
    print_failure readiness source-start-failed
    return 20
  fi
  while :; do
    if [ "$NEGATIVE_CASE" = timeout ]; then
      if database_readiness_stable "$SOURCE_PROJECT" source 1; then
        print_failure readiness timeout-probe-unexpectedly-ready
        return 20
      fi
    elif database_readiness_stable "$SOURCE_PROJECT" source 5432; then
      return 0
    fi
    if [ "$SECONDS" -ge "$OPERATION_DEADLINE" ]; then
      if [ "$NEGATIVE_CASE" = timeout ]; then
        print_failure readiness timeout
      else
        print_failure readiness source-timeout
      fi
      return 20
    fi
    service_has_terminal_state "$SOURCE_PROJECT" source
    terminal_state=$?
    case "$terminal_state" in
      0)
        print_failure readiness source-exited
        return 20
        ;;
      1) ;;
      *)
        print_failure readiness source-state-query-failed
        return 20
        ;;
    esac
    if ! run_bounded sleep 1; then
      if [ "$NEGATIVE_CASE" = timeout ]; then
        print_failure readiness timeout
      else
        print_failure readiness source-timeout
      fi
      return 20
    fi
  done
}

apply_seed_sql() {
  verify_evidence_ownership || return 40
  # shellcheck disable=SC2016 # Expansion is intentionally in-container only.
  if ! run_bounded docker compose -p "$SOURCE_PROJECT" -f "$COMPOSE_FILE" exec -T source \
    sh -ec 'export PGPASSWORD="$POSTGRES_PASSWORD"; exec psql "$@"' sh \
    -X -v ON_ERROR_STOP=1 -U rehearsal -d rehearsal \
    <"$SEED_SQL" >>"$RUNTIME_LOG" 2>&1; then
    print_failure restore seed-apply-failed
    return 40
  fi
}

capture_source_oracle() {
  verify_evidence_ownership || return 50
  # shellcheck disable=SC2016 # Expansion is intentionally in-container only.
  if ! (set -o noclobber; run_bounded docker compose -p "$SOURCE_PROJECT" -f "$COMPOSE_FILE" exec -T source \
    sh -ec 'export PGPASSWORD="$POSTGRES_PASSWORD"; exec psql "$@"' sh \
    -AtX -v ON_ERROR_STOP=1 -U rehearsal -d rehearsal \
    <"$ORACLE_SQL" >"$SOURCE_ORACLE_PATH" 2>>"$RUNTIME_LOG"); then
    print_failure integrity source-oracle-failed
    return 50
  fi
}

remove_owned_dump_client() {
  local failed=0
  local cleanup_log

  cleanup_log="$(cleanup_log_path)"

  if [ -n "$DUMP_CLIENT_ID" ]; then
    run_cleanup_bounded docker rm -f -v "$DUMP_CLIENT_ID" >>"$cleanup_log" 2>&1 || failed=1
  fi
  [ "$failed" -eq 0 ] || return 60
  DUMP_CLIENT_ID=''
  DUMP_CLIENT_MAY_EXIST=false
}

cleanup_labeled_dump_clients() {
  local client_id
  local client_ids
  local state
  local failed=0
  local cleanup_log

  [ "$DUMP_CLIENT_MAY_EXIST" = true ] || return 0
  cleanup_log="$(cleanup_log_path)"
  client_ids="$(query_labeled_client_state cleanup)"
  state=$?
  case "$state" in
    0)
      for client_id in $client_ids; do
        run_cleanup_bounded docker rm -f -v "$client_id" >>"$cleanup_log" 2>&1 || failed=1
      done
      ;;
    1) ;;
    *) failed=1 ;;
  esac
  query_labeled_client_state cleanup >/dev/null
  state=$?
  case "$state" in
    0) failed=1 ;;
    1) ;;
    *) failed=1 ;;
  esac
  [ "$failed" -eq 0 ] || return 60
  DUMP_CLIENT_ID=''
  DUMP_CLIENT_MAY_EXIST=false
}

create_owned_dump_client() {
  local status

  verify_evidence_ownership || return 1
  DUMP_CLIENT_MAY_EXIST=true
  export PGPASSWORD="$IOR_POSTGRES_PASSWORD"
  DUMP_CLIENT_ID="$(run_bounded docker create \
    --pull=never \
    --network "${SOURCE_PROJECT}_default" \
    --label "${CLIENT_LABEL_OWNER}=${PROJECT_PREFIX}" \
    --label "${CLIENT_LABEL_RUN}=${RUN_ID}" \
    -e PGPASSWORD \
    "$DUMP_CLIENT_IMAGE" \
    sh -ec 'exec pg_dump -Fc --no-owner --no-acl -h source -U rehearsal -d rehearsal -f /tmp/rehearsal.dump' \
    2>>"$RUNTIME_LOG")"
  status=$?
  unset PGPASSWORD
  [ "$status" -eq 0 ] || return "$status"
  [[ "$DUMP_CLIENT_ID" =~ ^[0-9a-f]{12,64}$ ]] || return 1
}

dump_custom_format_with_pg18_client() {
  local started=$SECONDS
  local wait_result
  local wait_status

  verify_evidence_ownership || return 30
  if ! create_owned_dump_client; then
    cleanup_labeled_dump_clients || true
    print_failure backup dump-client-create-failed
    return 30
  fi
  if ! run_bounded docker start "$DUMP_CLIENT_ID" >>"$RUNTIME_LOG" 2>&1; then
    remove_owned_dump_client || true
    print_failure backup dump-client-start-failed
    return 30
  fi
  wait_result="$(run_bounded docker wait "$DUMP_CLIENT_ID" 2>>"$RUNTIME_LOG")"
  wait_status=$?
  if [ "$wait_status" -ne 0 ]; then
    remove_owned_dump_client || true
    if [ "$wait_status" -eq 124 ]; then
      print_failure backup dump-client-timeout
    else
      print_failure backup dump-client-wait-failed
    fi
    return 30
  fi
  if [ "$wait_result" != 0 ]; then
    remove_owned_dump_client || true
    print_failure backup dump-client-nonzero
    return 30
  fi
  if ! run_bounded docker cp "${DUMP_CLIENT_ID}:/tmp/rehearsal.dump" "$DUMP_PATH" >>"$RUNTIME_LOG" 2>&1; then
    remove_owned_dump_client || true
    print_failure backup dump-copy-failed
    return 30
  fi
  if ! remove_owned_dump_client; then
    print_failure cleanup dump-client-cleanup-failed
    return 60
  fi
  verify_evidence_ownership || return 30
  BACKUP_SECONDS=$((SECONDS - started))
  [ -s "$DUMP_PATH" ] || {
    print_failure backup dump-empty
    return 30
  }
  DUMP_SHA256="$(sha256sum "$DUMP_PATH" | awk '{print $1}')"
  DUMP_BYTES="$(wc -c <"$DUMP_PATH" | tr -d ' ')"
}

start_target_and_wait() {
  local terminal_state

  verify_evidence_ownership || return 20
  TARGET_OWNED=true
  if ! run_bounded docker compose -p "$TARGET_PROJECT" -f "$COMPOSE_FILE" up -d --pull never --no-build --no-deps target >>"$RUNTIME_LOG" 2>&1; then
    print_failure readiness target-start-failed
    return 20
  fi
  while :; do
    if database_readiness_stable "$TARGET_PROJECT" target 5432; then
      return 0
    fi
    if [ "$SECONDS" -ge "$OPERATION_DEADLINE" ]; then
      print_failure readiness target-timeout
      return 20
    fi
    service_has_terminal_state "$TARGET_PROJECT" target
    terminal_state=$?
    case "$terminal_state" in
      0)
        print_failure readiness target-exited
        return 20
        ;;
      1) ;;
      *)
        print_failure readiness target-state-query-failed
        return 20
        ;;
    esac
    if ! run_bounded sleep 1; then
      print_failure readiness target-timeout
      return 20
    fi
  done
}

restore_without_owner_or_acl() {
  local started=$SECONDS

  verify_evidence_ownership || return 40
  # Restore contract: pg_restore --clean --if-exists --no-owner --no-acl
  # shellcheck disable=SC2016 # Expansion is intentionally in-container only.
  if ! run_bounded docker compose -p "$TARGET_PROJECT" -f "$COMPOSE_FILE" exec -T target \
    sh -ec 'export PGPASSWORD="$POSTGRES_PASSWORD"; exec pg_restore "$@"' sh \
    --clean --if-exists --no-owner --no-acl \
    -U rehearsal -d rehearsal <"$DUMP_PATH" >>"$RUNTIME_LOG" 2>&1; then
    print_failure restore restore-failed
    return 40
  fi
  RESTORE_SECONDS=$((SECONDS - started))
}

capture_target_oracle() {
  verify_evidence_ownership || return 50
  # shellcheck disable=SC2016 # Expansion is intentionally in-container only.
  if ! (set -o noclobber; run_bounded docker compose -p "$TARGET_PROJECT" -f "$COMPOSE_FILE" exec -T target \
    sh -ec 'export PGPASSWORD="$POSTGRES_PASSWORD"; exec psql "$@"' sh \
    -AtX -v ON_ERROR_STOP=1 -U rehearsal -d rehearsal \
    <"$ORACLE_SQL" >"$TARGET_ORACLE_PATH" 2>>"$RUNTIME_LOG"); then
    print_failure integrity target-oracle-failed
    return 50
  fi
}

compare_oracles() {
  verify_evidence_ownership || return 50
  if ! python3 - "$SOURCE_ORACLE_PATH" "$TARGET_ORACLE_PATH" 2>>"$RUNTIME_LOG" <<'PY'
import json
import sys

expected = {
    "schema_version",
    "server_version_num",
    "table_count",
    "account_count",
    "order_count",
    "balance_sum",
    "order_amount_sum",
    "account_digest",
    "order_digest",
    "foreign_key_orphan_count",
    "constraint_count",
}
with open(sys.argv[1], encoding="utf-8") as source_file:
    source = json.load(source_file)
with open(sys.argv[2], encoding="utf-8") as target_file:
    target = json.load(target_file)
if set(source) != expected or set(target) != expected:
    raise SystemExit(1)
if source["server_version_num"] != 170006 or target["server_version_num"] != 180004:
    raise SystemExit(1)
for key in expected - {"server_version_num"}:
    if source[key] != target[key]:
        raise SystemExit(1)
if source["schema_version"] != 1:
    raise SystemExit(1)
if source["table_count"] != 3 or source["account_count"] != 3:
    raise SystemExit(1)
if source["order_count"] != 4 or source["foreign_key_orphan_count"] != 0:
    raise SystemExit(1)
if source["constraint_count"] != 8:
    raise SystemExit(1)
PY
  then
    print_failure integrity oracle-mismatch
    return 50
  fi
}

run_partial_state_sql() {
  verify_evidence_ownership || return 1
  # shellcheck disable=SC2016 # Expansion is intentionally in-container only.
  run_bounded docker compose -p "$TARGET_PROJECT" -f "$COMPOSE_FILE" exec -T target \
    sh -ec 'export PGPASSWORD="$POSTGRES_PASSWORD"; exec psql "$@"' sh \
    -X -v ON_ERROR_STOP=1 -U rehearsal -d rehearsal \
    <"$PARTIAL_SQL" >>"$RUNTIME_LOG" 2>&1
}

partial_state_marker_exists() {
  local marker

  verify_evidence_ownership || return 1
  # shellcheck disable=SC2016 # Expansion is intentionally in-container only.
  marker="$(run_bounded docker compose -p "$TARGET_PROJECT" -f "$COMPOSE_FILE" exec -T target \
    sh -ec 'export PGPASSWORD="$POSTGRES_PASSWORD"; exec psql "$@"' sh \
    -AtX -v ON_ERROR_STOP=1 -U rehearsal -d rehearsal \
    -c "SELECT to_regclass('public.rehearsal_partial_state_marker') IS NOT NULL" \
    2>>"$RUNTIME_LOG")" || return 1
  [ "$marker" = t ]
}

run_selected_negative_case() {
  local current_sha256

  case "$NEGATIVE_CASE" in
    '') return 0 ;;
    checksum-mismatch)
      verify_evidence_ownership || return 50
      printf 'corruption-probe' >>"$DUMP_PATH"
      verify_evidence_ownership || return 50
      current_sha256="$(sha256sum "$DUMP_PATH" | awk '{print $1}')"
      if [ "$current_sha256" != "$DUMP_SHA256" ]; then
        print_failure integrity checksum-mismatch
        return 50
      fi
      print_failure integrity checksum-negative-not-detected
      return 50
      ;;
    partial-state)
      if run_partial_state_sql; then
        print_failure integrity partial-state-error-not-raised
        return 50
      fi
      if partial_state_marker_exists; then
        print_failure integrity partial-state-detected
        return 50
      fi
      print_failure integrity partial-state-marker-missing
      return 50
      ;;
    timeout)
      print_failure readiness timeout-not-detected
      return 20
      ;;
    bad-target-major)
      print_failure preflight bad-target-major-not-detected
      return 10
      ;;
    *)
      print_failure preflight unsupported-negative-case
      return 10
      ;;
  esac
}

build_recovery_verdict_json() {
  python3 - "$SOURCE_IMAGE" "$TARGET_IMAGE" \
    "$FIXTURE_SHA256" "$DUMP_SHA256" "$BACKUP_SECONDS" "$RESTORE_SECONDS" <<'PY'
import json
import sys

source, target, fixture, dump, backup, restore = sys.argv[1:]
payload = {
    "schema_version": 1,
    "producer_spec": "spec:125-infrastructure-operations-readiness-remediation",
    "scope": "synthetic-local",
    "source_image": source,
    "target_image": target,
    "fixture_sha256": f"sha256:{fixture}",
    "dump_sha256": f"sha256:{dump}",
    "integrity_status": "passed",
    "backup_seconds": int(backup),
    "restore_seconds": int(restore),
    "cleanup_status": "passed",
    "redaction_status": "passed",
}
print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
PY
}

write_recovery_verdict() {
  CANDIDATE_JSON="$(build_recovery_verdict_json)" || return 50
  CANDIDATE_WRITTEN=true
  PUBLISH_ALLOWED=true
}

project_resources_absent() {
  local project="$1"
  local state

  query_project_resource_state "$project" cleanup >/dev/null
  state=$?
  [ "$state" -eq 1 ]
}

cleanup_one_owned_project() {
  local project="$1"
  local owned_variable="$2"
  local owned="${!owned_variable}"
  local failed=0
  local cleanup_log

  [ "$owned" = true ] || return 0
  cleanup_log="$(cleanup_log_path)"
  run_cleanup_bounded docker compose -p "$project" -f "$COMPOSE_FILE" down --volumes --remove-orphans \
    >>"$cleanup_log" 2>&1 || failed=1
  project_resources_absent "$project" || failed=1
  [ "$failed" -eq 0 ] || return 60
  printf -v "$owned_variable" '%s' false
}

publish_canonical_after_cleanup() {
  [ "$PUBLISH_ALLOWED" = true ] || return 50
  [ "$CANDIDATE_WRITTEN" = true ] || return 50
  [ -n "$CANDIDATE_JSON" ] || return 50
  [ "$CLEANUP_COMPLETE" = true ] || return 50
  [ "$EVIDENCE_REMOVED" = true ] || return 50
  [ "$SOURCE_OWNED" = false ] || return 50
  [ "$TARGET_OWNED" = false ] || return 50
  [ "$DUMP_CLIENT_MAY_EXIST" = false ] || return 50
  [ "$NEGATIVE_CASE" = '' ] || return 50
  [ "$SIGNAL_RECEIVED" = false ] || return 50
  validate_handoff_parent || return 50
  python3 - "$HANDOFF_DIR" "$HANDOFF_PATH" "$RUN_ID" "$CANDIDATE_JSON" <<'PY'
import json
import os
from pathlib import Path
import stat
import sys

parent = Path(sys.argv[1])
target = Path(sys.argv[2])
run_id = sys.argv[3]
payload = json.loads(sys.argv[4])
expected = {
    "schema_version",
    "producer_spec",
    "scope",
    "source_image",
    "target_image",
    "fixture_sha256",
    "dump_sha256",
    "integrity_status",
    "backup_seconds",
    "restore_seconds",
    "cleanup_status",
    "redaction_status",
}
if set(payload) != expected or payload.get("cleanup_status") != "passed":
    raise SystemExit(1)
try:
    target.lstat()
except FileNotFoundError:
    pass
else:
    raise SystemExit(1)

temporary = parent / f".recovery-verdict.{run_id}.{os.getpid()}.tmp"
flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
if hasattr(os, "O_NOFOLLOW"):
    flags |= os.O_NOFOLLOW
fd = os.open(temporary, flags, 0o600)
try:
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, sort_keys=True, separators=(",", ":"))
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    try:
        info = target.lstat()
    except FileNotFoundError:
        pass
    else:
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            raise OSError("unsafe canonical target")
        raise OSError("canonical target appeared during publication")
    os.replace(temporary, target)
    directory_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
except BaseException:
    try:
        info = temporary.lstat()
        if stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid():
            temporary.unlink()
    except FileNotFoundError:
        pass
    raise
PY
}

cleanup_owned_projects_and_tmp() {
  local failed=0

  if [ "$CLEANUP_COMPLETE" = true ]; then
    return 0
  fi
  invalidate_canonical_handoff || failed=1
  cleanup_labeled_dump_clients || failed=1
  cleanup_one_owned_project "$TARGET_PROJECT" TARGET_OWNED || failed=1
  cleanup_one_owned_project "$SOURCE_PROJECT" SOURCE_OWNED || failed=1
  cleanup_owned_evidence_dir || failed=1
  invalidate_canonical_handoff || failed=1
  if [ "$failed" -ne 0 ]; then
    PUBLISH_ALLOWED=false
    print_failure cleanup owned-cleanup-failed
    return 60
  fi
  CLEANUP_COMPLETE=true
  printf 'cleanup_status=passed\n'
}

on_signal() {
  SIGNAL_RECEIVED=true
  PUBLISH_ALLOWED=false
  invalidate_canonical_handoff || true
  exit 20
}

on_exit() {
  local status=$?

  trap - EXIT
  if [ "$CLEANUP_COMPLETE" != true ]; then
    if ! cleanup_owned_projects_and_tmp; then
      status=60
    fi
  fi
  if [ "$status" -ne 0 ]; then
    if ! invalidate_canonical_handoff; then
      status=60
    fi
  fi
  exit "$status"
}

compute_fixture_sha256() {
  FIXTURE_SHA256="$({
    cd "$FIXTURE_DIR" || exit 1
    find docker-compose.yml sql topology -type f -print0 \
      | sort -z \
      | xargs -0 sha256sum
  } | sha256sum | awk '{print $1}')"
  [[ "$FIXTURE_SHA256" =~ ^[0-9a-f]{64}$ ]]
}

main() {
  local status

  set -o nounset
  trap on_exit EXIT
  trap 'on_signal' TERM
  trap 'on_signal' INT
  trap 'on_signal' HUP

  prepare_default_handoff_dir || {
    print_failure preflight unsafe-canonical-parent
    return 10
  }
  invalidate_canonical_handoff || {
    print_failure preflight unsafe-canonical-path
    return 10
  }
  if ! reject_direct_test_controls; then
    print_failure preflight test-control-forbidden
    return 10
  fi
  if ! parse_args "$@"; then
    print_failure usage invalid-arguments
    return 2
  fi
  if [ "$EVIDENCE_DIR" != "/tmp/hyhome-ior-evidence.${RUN_ID}" ]; then
    print_failure preflight unsafe-evidence-path
    return 10
  fi
  initialize_runtime_state || {
    print_failure preflight runtime-state-init-failed
    return 10
  }
  assert_safe_images_paths_and_project || return $?
  compute_fixture_sha256 || {
    print_failure preflight fixture-checksum-failed
    return 10
  }

  if [ "$RUN_MODE" = check ]; then
    cleanup_owned_projects_and_tmp || return $?
    printf 'status=check-passed\n'
    printf 'source_image=%s\n' "$SOURCE_IMAGE"
    printf 'target_image=%s\n' "$TARGET_IMAGE"
    printf 'fixture_sha256=sha256:%s\n' "$FIXTURE_SHA256"
    printf 'project_prefix=%s\n' "$PROJECT_PREFIX"
    printf 'total_timeout_seconds=%s\n' "$ACTIVE_TOTAL_TIMEOUT"
    printf 'cleanup_reserve_seconds=%s\n' "$ACTIVE_CLEANUP_RESERVE"
    printf 'operation_budget_seconds=%s\n' "$((ACTIVE_TOTAL_TIMEOUT - ACTIVE_CLEANUP_RESERVE))"
    printf 'evidence_path_class=/tmp/hyhome-ior-evidence.<decimal-pid>\n'
    printf 'evidence_ownership=exclusive-uid-mode-device-inode\n'
    printf 'cleanup=always-within-total-deadline\n'
    return 0
  fi

  start_source_and_wait || return $?
  apply_seed_sql || return $?
  capture_source_oracle || return $?
  dump_custom_format_with_pg18_client || return $?
  start_target_and_wait || return $?
  restore_without_owner_or_acl || return $?
  capture_target_oracle || return $?
  compare_oracles || return $?
  run_selected_negative_case || return $?
  write_recovery_verdict || return $?
  cleanup_owned_projects_and_tmp || return $?
  publish_canonical_after_cleanup || {
    print_failure cleanup canonical-publication-failed
    return 60
  }

  status=0
  printf 'status=passed integrity_status=passed\n'
  printf 'source_project=%s\n' "$SOURCE_PROJECT"
  printf 'target_project=%s\n' "$TARGET_PROJECT"
  printf 'fixture_sha256=sha256:%s\n' "$FIXTURE_SHA256"
  printf 'dump_sha256=sha256:%s\n' "$DUMP_SHA256"
  printf 'dump_bytes=%s\n' "$DUMP_BYTES"
  printf 'backup_seconds=%s\n' "$BACKUP_SECONDS"
  printf 'restore_seconds=%s\n' "$RESTORE_SECONDS"
  printf 'recovery_verdict=%s\n' "$HANDOFF_PATH"
  return "$status"
}

if [ "$SCRIPT_IS_SOURCED" = false ]; then
  main "$@"
elif [ "$TEST_SOURCE_BOUNDARY" != true ]; then
  print_failure usage test-source-boundary-required >&2
  return 2
fi
