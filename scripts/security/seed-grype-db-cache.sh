#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

# The networked seed step is deliberately separate from the offline advisory.
# It accepts no artifact/source input and publishes only a private immutable DB
# generation plus one minimized atomic identity pointer.

BASE_DIR="$(git rev-parse --show-toplevel)"
HELPER="$BASE_DIR/scripts/validation/grype_db_seed.py"
CHECKER="$BASE_DIR/scripts/validation/check-supply-chain-policy.py"
TOOL_REGISTRY="$BASE_DIR/infra/supply-chain.tool-images.json"
TASK_DOC="$BASE_DIR/docs/04.execution/tasks/2026-07-23-security-supply-chain-runtime-closure.md"
OUTPUT_RELATIVE="_workspace/repo-support/task-2026-07-23-security-supply-chain-runtime-closure/grype-db-seed"
MODE="${1:-}"

readonly EXIT_USAGE=2 EXIT_POLICY=10 EXIT_NETWORK=20 EXIT_PUBLICATION=30
readonly GRYPE_REF="anchore/grype:v0.116.0@sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821"
readonly GRYPE_REPO_DIGEST="anchore/grype@sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821"
readonly GRYPE_CONFIG_ID="sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821"

runtime_dir=""
tool_tmp_dir=""
raw_log=""
output_identity=""
stage_identity=""
stage_path=""
published=0

usage() {
  printf '%s\n' 'Usage: bash scripts/security/seed-grype-db-cache.sh --preflight|--seed'
}

fail() {
  printf 'grype_db_seed=fail class=%s reason=%s\n' "$1" "$2" >&2
  exit "$1"
}

cleanup() {
  if [[ "$published" != 1 && -n "$output_identity" && -n "$stage_identity" && -n "$stage_path" ]]; then
    python3 "$HELPER" --discard-stage "$BASE_DIR" "$OUTPUT_RELATIVE" "$output_identity" "$stage_identity" "$stage_path" >/dev/null 2>&1 || true
  fi
  if [[ -n "$runtime_dir" && "$runtime_dir" == /tmp/hyhome-grype-db-seed.* ]]; then
    rm -rf -- "$runtime_dir"
  fi
  runtime_dir=""
  tool_tmp_dir=""
  raw_log=""
}

trap cleanup EXIT

assert_grype_registry_identity() {
  python3 - "$TOOL_REGISTRY" "$GRYPE_REF" "$GRYPE_REPO_DIGEST" "$GRYPE_CONFIG_ID" <<'PY'
import json
import pathlib
import sys

registry = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
rows = [row for row in registry.get("tools", []) if row.get("name") == "grype"]
if len(rows) != 1:
    raise SystemExit(1)
row = rows[0]
actual = (f'{row.get("image")}@{row.get("digest")}', row.get("repo_digest"), row.get("config_id"))
raise SystemExit(0 if actual == tuple(sys.argv[2:]) else 1)
PY
}

assert_local_grype_identity() {
  local inspection repo_digests actual_config_id
  inspection="$(docker image inspect --format '{{json .RepoDigests}}|{{.Id}}' "$GRYPE_REF" 2>/dev/null)" || fail "$EXIT_POLICY" "pinned-grype-image-missing"
  repo_digests="${inspection%%|*}"
  actual_config_id="${inspection#*|}"
  python3 - "$repo_digests" "$GRYPE_REPO_DIGEST" <<'PY' || fail "$EXIT_POLICY" "pinned-grype-manifest-mismatch"
import json
import sys

try:
    values = json.loads(sys.argv[1])
except json.JSONDecodeError:
    raise SystemExit(1)
raise SystemExit(0 if isinstance(values, list) and sys.argv[2] in values else 1)
PY
  [[ "$actual_config_id" == "$GRYPE_CONFIG_ID" ]] || fail "$EXIT_POLICY" "pinned-grype-config-mismatch"
}

run_preflight() {
  [[ -f "$HELPER" && -f "$CHECKER" && -f "$TOOL_REGISTRY" && -f "$TASK_DOC" ]] || fail "$EXIT_POLICY" "seed-contract-surface-missing"
  grep -Fqx 'Grype DB network approval: confirmed' "$TASK_DOC" || fail "$EXIT_POLICY" "seed-network-approval-missing"
  python3 "$CHECKER" --check >/dev/null || fail "$EXIT_POLICY" "supply-chain-policy-invalid"
  assert_grype_registry_identity || fail "$EXIT_POLICY" "pinned-grype-registry-identity-invalid"
  command -v docker >/dev/null || fail "$EXIT_POLICY" "docker-unavailable"
  docker info >/dev/null 2>&1 || fail "$EXIT_POLICY" "docker-daemon-unavailable"
  assert_local_grype_identity
}

prepare_private_runtime() {
  runtime_dir="$(mktemp -d /tmp/hyhome-grype-db-seed.XXXXXX)" || fail "$EXIT_POLICY" "seed-runtime-create-failed"
  chmod 700 "$runtime_dir"
  tool_tmp_dir="$runtime_dir/tool-tmp"
  raw_log="$runtime_dir/grype-db-update.raw.log"
  mkdir -m 700 "$tool_tmp_dir" "$tool_tmp_dir/.cache"
  : >"$raw_log"
  chmod 600 "$raw_log"
  mapfile -t stage_fields < <(python3 "$HELPER" --prepare-stage "$BASE_DIR" "$OUTPUT_RELATIVE") || fail "$EXIT_PUBLICATION" "seed-stage-prepare-failed"
  [[ "${#stage_fields[@]}" == 3 ]] || fail "$EXIT_PUBLICATION" "seed-stage-output-invalid"
  output_identity="${stage_fields[0]}"
  stage_identity="${stage_fields[1]}"
  stage_path="${stage_fields[2]}"
  [[ "$output_identity" =~ ^[0-9]+:[0-9]+$ && "$stage_identity" =~ ^[0-9]+:[0-9]+$ ]] || fail "$EXIT_PUBLICATION" "seed-stage-identity-invalid"
  [[ "$stage_path" == "$BASE_DIR/$OUTPUT_RELATIVE/".stage.* ]] || fail "$EXIT_PUBLICATION" "seed-stage-path-invalid"
}

run_seed() {
  local seeded_at identity_json
  run_preflight
  prepare_private_runtime
  docker run --pull=never --rm --network bridge --user "$(id -u):$(id -g)" --env HOME=/tmp --env XDG_CACHE_HOME=/tmp/.cache --env GRYPE_CHECK_FOR_APP_UPDATE=false --env GRYPE_DB_AUTO_UPDATE=false --env GRYPE_DB_CACHE_DIR=/grype-db-cache --mount "type=bind,source=$tool_tmp_dir,target=/tmp" --mount "type=bind,source=$stage_path/cache,target=/grype-db-cache" "$GRYPE_REF" db update >"$raw_log" 2>&1 || fail "$EXIT_NETWORK" "grype-db-update-failed"
  docker run --pull=never --rm --network none --user "$(id -u):$(id -g)" --env HOME=/tmp --env XDG_CACHE_HOME=/tmp/.cache --env GRYPE_CHECK_FOR_APP_UPDATE=false --env GRYPE_DB_AUTO_UPDATE=false --env GRYPE_DB_CACHE_DIR=/grype-db-cache --mount "type=bind,source=$tool_tmp_dir,target=/tmp" --mount "type=bind,source=$stage_path/cache,target=/grype-db-cache,readonly" "$GRYPE_REF" db status >"$stage_path/db-status.txt" 2>>"$raw_log" || fail "$EXIT_NETWORK" "grype-db-status-failed"
  chmod 600 "$stage_path/db-status.txt"
  seeded_at="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  identity_json="$(python3 "$HELPER" --finalize-stage "$BASE_DIR" "$OUTPUT_RELATIVE" "$output_identity" "$stage_identity" "$stage_path" "$stage_path/db-status.txt" "$seeded_at")" || fail "$EXIT_PUBLICATION" "seed-generation-publication-failed"
  published=1
  python3 - "$identity_json" <<'PY'
import json
import sys

payload = json.loads(sys.argv[1])
print(
    "grype_db_seed=pass"
    f" schema={payload['database']['schema']}"
    f" built={payload['database']['built']}"
    f" package_sha256={payload['database']['package_sha256']}"
    f" cache_tree_sha256={payload['cache']['tree_sha256']}"
)
PY
}

case "$MODE" in
--preflight)
  run_preflight
  printf 'grype_db_seed_preflight=pass network=not-used\n'
  ;;
--seed)
  run_seed
  ;;
*)
  usage >&2
  exit "$EXIT_USAGE"
  ;;
esac
