#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

# Local-only supply-chain rehearsal. Raw artifacts live in one private /tmp
# tree; only redacted summaries and a committed accepted-verdict pair may be
# handed off under the task-owned ignored output directory.

BASE_DIR="$(git rev-parse --show-toplevel)"
SERVICE_DIR="$BASE_DIR/examples/sample-web-service"
CHECKER="$BASE_DIR/scripts/validation/check-supply-chain-policy.py"
GRYPE_DB_SEED_HELPER="$BASE_DIR/scripts/validation/grype_db_seed.py"
TOOL_REGISTRY="$BASE_DIR/infra/supply-chain.tool-images.json"
POLICY="$BASE_DIR/infra/supply-chain.sample-service-policy.json"
COSIGN_OFFLINE_SIGNING_CONFIG="$BASE_DIR/infra/supply-chain.cosign-offline-signing-config.json"
TASK_DOC="$BASE_DIR/docs/04.execution/tasks/2026-07-19-security-supply-chain-remediation.md"
OUTPUT_RELATIVE="_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain"
OUTPUT_DIR="$BASE_DIR/$OUTPUT_RELATIVE"
GRYPE_DB_SEED_RELATIVE="_workspace/repo-support/task-2026-07-23-security-supply-chain-runtime-closure/grype-db-seed"
SOURCE_REVISION="$(git -C "$BASE_DIR" rev-parse HEAD)"
MODE="${1:-}"

readonly EXIT_USAGE=2 EXIT_POLICY=10 EXIT_BUILD=20 EXIT_SBOM=30
readonly EXIT_VULNERABILITY=40 EXIT_PROVENANCE=50 EXIT_SIGNATURE=60 EXIT_SCORECARD=70
readonly BUILD_MATERIAL_REF="alpine:3.21@sha256:48b0309ca019d89d40f670aa1bc06e426dc0931948452e8491e3d65087abc07d"
readonly BUILD_MATERIAL_REPO_DIGEST="alpine@sha256:48b0309ca019d89d40f670aa1bc06e426dc0931948452e8491e3d65087abc07d"
readonly BUILD_MATERIAL_CONFIG_ID="sha256:48b0309ca019d89d40f670aa1bc06e426dc0931948452e8491e3d65087abc07d"
readonly RUNTIME_MATERIAL_REF="nginxinc/nginx-unprivileged:1.31.3-alpine3.24-slim@sha256:90d82b3358df5758b3c57d20f2565082ce6f744906e7dc09afd0096c1b8eb2b5"
readonly RUNTIME_MATERIAL_REPO_DIGEST="nginxinc/nginx-unprivileged@sha256:90d82b3358df5758b3c57d20f2565082ce6f744906e7dc09afd0096c1b8eb2b5"
readonly RUNTIME_MATERIAL_CONFIG_ID="sha256:90d82b3358df5758b3c57d20f2565082ce6f744906e7dc09afd0096c1b8eb2b5"

declare -A IMAGE_CONFIG_DIGEST=() OCI_ARCHIVE_SHA256=()
runtime_dir=""
artifact_root=""
grype_db_dir=""
grype_db_status=""
grype_db_identity=""
grype_db_seed_source=""
private_key_dir=""
tool_tmp_dir=""
run_verdict_dir=""
build_context_snapshot=""
build_context_archive=""
BUILD_CONTEXT_SHA256=""
output_identity=""

usage() {
  cat <<'EOF'
Usage: bash scripts/security/verify-sample-service-supply-chain.sh --fixture-only|--preflight|--advisory|--scorecard-advisory

`--fixture-only` is deterministic and Docker-independent. `--preflight`
checks the local daemon, default Buildx driver, and exact local image IDs.
`--advisory` never pulls images or downloads a vulnerability database.
EOF
}

fail() {
  printf 'supply_chain_verification=fail class=%s reason=%s\n' "$1" "$2" >&2
  exit "$1"
}

tool_field() {
  python3 - "$TOOL_REGISTRY" "$1" "$2" <<'PY'
import json
import pathlib
import sys

registry = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
for tool in registry["tools"]:
    if tool["name"] == sys.argv[2]:
        if sys.argv[3] == "ref":
            print(f'{tool["image"]}@{tool["digest"]}')
        elif sys.argv[3] == "digest":
            print(tool["digest"])
        elif sys.argv[3] == "repo_digest":
            print(tool["repo_digest"])
        elif sys.argv[3] == "config_id":
            print(tool["config_id"])
        else:
            raise SystemExit(2)
        raise SystemExit(0)
raise SystemExit(1)
PY
}

tool_ref() {
  tool_field "$1" ref
}

tool_digest() {
  tool_field "$1" digest
}

tool_repo_digest() {
  tool_field "$1" repo_digest
}

tool_config_id() {
  tool_field "$1" config_id
}

load_tool_registry() {
  python3 "$CHECKER" --check >/dev/null || fail "$EXIT_POLICY" "tool-registry-or-fixture-policy-invalid"
  local tool
  for tool in syft grype cosign scorecard; do
    tool_ref "$tool" >/dev/null || fail "$EXIT_POLICY" "tool-reference-missing"
  done
}

validate_policy_and_exceptions() {
  [[ -f "$POLICY" && -f "$COSIGN_OFFLINE_SIGNING_CONFIG" && -f "$COSIGN_OFFLINE_TRUSTED_ROOT" && -f "$TASK_DOC" ]] || fail "$EXIT_POLICY" "policy-task-or-cosign-config-boundary-missing"
  python3 "$CHECKER" --check >/dev/null || fail "$EXIT_POLICY" "policy-or-exception-invalid"
}

prepare_transient_directory() {
  [[ -z "$runtime_dir" ]] || fail "$EXIT_POLICY" "runtime-directory-already-prepared"
  runtime_dir="$(mktemp -d /tmp/hyhome-supply-chain.XXXXXX)" || fail "$EXIT_POLICY" "runtime-directory-create-failed"
  chmod 700 "$runtime_dir"
  artifact_root="$runtime_dir/artifacts"
  grype_db_dir="$runtime_dir/grype-db-cache"
  grype_db_status="$runtime_dir/grype-db-status.txt"
  grype_db_identity="$runtime_dir/grype-db-identity.json"
  private_key_dir="$runtime_dir/keys"
  tool_tmp_dir="$runtime_dir/tool-tmp"
  run_verdict_dir="$runtime_dir/verdicts"
  build_context_snapshot="$runtime_dir/build-context.json"
  build_context_archive="$runtime_dir/build-context.tar"
  mkdir -m 700 "$artifact_root" "$grype_db_dir" "$private_key_dir" "$tool_tmp_dir" "$run_verdict_dir"
  mkdir -m 700 "$tool_tmp_dir/.cache"
  mkdir -m 700 "$artifact_root/baseline" "$artifact_root/candidate"
}

cleanup_transient_state() {
  if [[ -n "$runtime_dir" && "$runtime_dir" == /tmp/hyhome-supply-chain.* ]]; then
    rm -rf -- "$runtime_dir"
  fi
  runtime_dir=""
  artifact_root=""
  grype_db_dir=""
  grype_db_seed_source=""
  private_key_dir=""
  tool_tmp_dir=""
  run_verdict_dir=""
  build_context_snapshot=""
  build_context_archive=""
}

prepare_secure_output() {
  [[ "$OUTPUT_DIR" == "$BASE_DIR/$OUTPUT_RELATIVE" ]] || fail "$EXIT_POLICY" "task-output-path-invalid"
  output_identity="$(python3 "$CHECKER" --prepare-secure-output "$BASE_DIR" "$OUTPUT_RELATIVE")" || fail "$EXIT_POLICY" "secure-output-invalid"
  [[ "$output_identity" =~ ^[0-9]+:[0-9]+$ ]] || fail "$EXIT_POLICY" "secure-output-identity-invalid"
}

invalidate_consumer_verdicts() {
  [[ "$OUTPUT_DIR" == "$BASE_DIR/$OUTPUT_RELATIVE" ]] || fail "$EXIT_POLICY" "task-output-path-invalid"
  [[ -n "$output_identity" ]] || prepare_secure_output
  python3 "$CHECKER" --invalidate-secure-handoffs "$BASE_DIR" "$OUTPUT_RELATIVE" "$output_identity" || fail "$EXIT_POLICY" "stale-handoff-invalidation-failed"
}

capture_build_context_snapshot() {
  local snapshot_revision
  [[ -n "$build_context_snapshot" && -n "$build_context_archive" ]] || fail "$EXIT_POLICY" "build-context-snapshot-path-missing"
  BUILD_CONTEXT_SHA256="$(python3 "$CHECKER" --capture-build-context "$BASE_DIR" "examples/sample-web-service" "$build_context_snapshot" "$build_context_archive")" || fail "$EXIT_POLICY" "build-context-not-clean"
  [[ "$BUILD_CONTEXT_SHA256" =~ ^sha256:[0-9a-f]{64}$ ]] || fail "$EXIT_POLICY" "build-context-digest-invalid"
  snapshot_revision="$(python3 - "$build_context_snapshot" <<'PY'
import json
import pathlib
import sys

print(json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))["source_revision"])
PY
)" || fail "$EXIT_POLICY" "build-context-source-revision-invalid"
  [[ "$snapshot_revision" == "$SOURCE_REVISION" ]] || fail "$EXIT_POLICY" "build-context-source-revision-mismatch"
}

assert_build_context_unchanged() {
  [[ -n "$build_context_snapshot" && -f "$build_context_snapshot" && -n "$build_context_archive" && -f "$build_context_archive" ]] || fail "$EXIT_PROVENANCE" "build-context-snapshot-missing"
  python3 "$CHECKER" --verify-build-context "$BASE_DIR" "examples/sample-web-service" "$build_context_snapshot" "$build_context_archive" >/dev/null || fail "$EXIT_PROVENANCE" "build-context-changed"
}

role_artifact_dir() {
  local role="$1"
  if [[ -n "$artifact_root" ]]; then
    printf '%s\n' "$artifact_root/$role"
  else
    printf '%s\n' "$OUTPUT_DIR/$role"
  fi
}

assert_local_image_identity() {
  local reference="$1" expected_repo_digest="$2" expected_config_id="$3" inspection repo_digests actual_config_id
  inspection="$(docker image inspect --format '{{json .RepoDigests}}|{{.Id}}' "$reference" 2>/dev/null)" || fail "$EXIT_POLICY" "pinned-image-missing"
  repo_digests="${inspection%%|*}"
  actual_config_id="${inspection#*|}"
  python3 - "$repo_digests" "$expected_repo_digest" <<'PY' || fail "$EXIT_POLICY" "pinned-image-manifest-mismatch"
import json
import sys

try:
    repo_digests = json.loads(sys.argv[1])
except json.JSONDecodeError:
    raise SystemExit(1)
raise SystemExit(0 if isinstance(repo_digests, list) and sys.argv[2] in repo_digests else 1)
PY
  [[ "$actual_config_id" == "$expected_config_id" ]] || fail "$EXIT_POLICY" "pinned-image-config-id-mismatch"
}

assert_local_image_identities() {
  local tool reference repo_digest config_id
  for tool in syft grype cosign scorecard; do
    reference="$(tool_ref "$tool")" || fail "$EXIT_POLICY" "tool-reference-missing"
    repo_digest="$(tool_repo_digest "$tool")" || fail "$EXIT_POLICY" "tool-repo-digest-missing"
    config_id="$(tool_config_id "$tool")" || fail "$EXIT_POLICY" "tool-config-id-missing"
    assert_local_image_identity "$reference" "$repo_digest" "$config_id"
  done
  assert_local_image_identity "$BUILD_MATERIAL_REF" "$BUILD_MATERIAL_REPO_DIGEST" "$BUILD_MATERIAL_CONFIG_ID"
  assert_local_image_identity "$RUNTIME_MATERIAL_REF" "$RUNTIME_MATERIAL_REPO_DIGEST" "$RUNTIME_MATERIAL_CONFIG_ID"
}

assert_default_buildx_offline_capable() {
  local inspection
  docker buildx version >/dev/null 2>&1 || fail "$EXIT_POLICY" "docker-buildx-unavailable-advisory-blocked"
  inspection="$(docker buildx inspect default 2>/dev/null)" || fail "$EXIT_POLICY" "default-buildx-builder-unavailable"
  grep -Eq '^Name:[[:space:]]+default$' <<<"$inspection" || fail "$EXIT_POLICY" "default-buildx-name-invalid"
  grep -Eq '^Driver:[[:space:]]+docker$' <<<"$inspection" || fail "$EXIT_POLICY" "default-buildx-driver-invalid"
  grep -Eq '^Status:[[:space:]]+running$' <<<"$inspection" || fail "$EXIT_POLICY" "default-buildx-status-invalid"
}

ensure_advisory_prerequisites() {
  command -v docker >/dev/null || fail "$EXIT_POLICY" "docker-unavailable-advisory-blocked"
  docker info >/dev/null 2>&1 || fail "$EXIT_POLICY" "docker-daemon-unavailable-advisory-blocked"
  assert_default_buildx_offline_capable
}

assert_grype_db_seed_available() {
  local resolved prefix
  [[ -x "$GRYPE_DB_SEED_HELPER" ]] || fail "$EXIT_POLICY" "grype-db-seed-helper-unavailable-advisory-blocked"
  resolved="$("$GRYPE_DB_SEED_HELPER" --resolve-current "$BASE_DIR" "$GRYPE_DB_SEED_RELATIVE" 2>/dev/null)" || fail "$EXIT_POLICY" "grype-db-seed-unavailable-advisory-blocked"
  prefix="$BASE_DIR/$GRYPE_DB_SEED_RELATIVE/generations/"
  [[ "$resolved" == "$prefix"*"/cache" ]] || fail "$EXIT_POLICY" "grype-db-seed-path-invalid-advisory-blocked"
  [[ -d "$resolved" && ! -L "$resolved" ]] || fail "$EXIT_POLICY" "grype-db-seed-unavailable-advisory-blocked"
  [[ -d "$resolved/6" && ! -L "$resolved/6" ]] || fail "$EXIT_POLICY" "grype-db-seed-schema-invalid-advisory-blocked"
  grype_db_seed_source="$resolved"
}

seed_private_grype_db_cache() {
  local resolved
  [[ -n "$grype_db_seed_source" ]] || assert_grype_db_seed_available
  resolved="$("$GRYPE_DB_SEED_HELPER" --resolve-current "$BASE_DIR" "$GRYPE_DB_SEED_RELATIVE" 2>/dev/null)" || fail "$EXIT_POLICY" "grype-db-seed-revalidation-failed"
  [[ "$resolved" == "$grype_db_seed_source" ]] || fail "$EXIT_POLICY" "grype-db-seed-generation-changed"
  docker run --pull=never --rm --network none --user 0:0 --env "TARGET_UID=$(id -u)" --env "TARGET_GID=$(id -g)" --mount "type=bind,source=$grype_db_seed_source,target=/seed,readonly" --mount "type=bind,source=$grype_db_dir,target=/cache" "$BUILD_MATERIAL_REF" sh -ceu 'cp -a /seed/. /cache/; chown -R "$TARGET_UID:$TARGET_GID" /cache; find /cache -type d -exec chmod 700 {} +; find /cache -type f -exec chmod 600 {} +' || fail "$EXIT_POLICY" "grype-db-private-seed-failed"
}

remove_legacy_runtime_artifacts() {
  local current_identity name path
  current_identity="$(python3 "$CHECKER" --prepare-secure-output "$BASE_DIR" "$OUTPUT_RELATIVE")" || fail "$EXIT_POLICY" "secure-output-revalidation-failed"
  [[ "$current_identity" == "$output_identity" ]] || fail "$EXIT_POLICY" "secure-output-identity-mismatch"
  for name in baseline candidate grype-db-cache grype-db-status.txt grype-db-identity.json; do
    path="$OUTPUT_DIR/$name"
    [[ ! -L "$path" ]] || fail "$EXIT_POLICY" "legacy-runtime-artifact-symlink"
  done
  docker run --pull=never --rm --network none --user 0:0 --mount "type=bind,source=$OUTPUT_DIR,target=/handoff" "$BUILD_MATERIAL_REF" sh -ceu '
    for path in /handoff/baseline /handoff/candidate /handoff/grype-db-cache /handoff/grype-db-status.txt /handoff/grype-db-identity.json; do
      [ ! -L "$path" ] || exit 73
    done
    rm -rf -- /handoff/baseline /handoff/candidate /handoff/grype-db-cache
    rm -f -- /handoff/grype-db-status.txt /handoff/grype-db-identity.json
  ' || fail "$EXIT_POLICY" "legacy-runtime-artifact-cleanup-failed"
}

build_role_image() {
  local role="$1" role_dir label
  role_dir="$(role_artifact_dir "$role")"
  label="org.hyhome.delivery.rehearsal.role=${role}"
  [[ -f "$build_context_archive" && ! -L "$build_context_archive" ]] || fail "$EXIT_BUILD" "build-context-archive-missing"
  [[ "$(stat -c '%a:%u' "$build_context_archive")" == "600:$(id -u)" ]] || fail "$EXIT_BUILD" "build-context-archive-private-mode-invalid"
  mkdir -p "$role_dir"
  chmod 700 "$role_dir"
  docker buildx build --builder default --network=none --pull=false --output "type=oci,dest=$role_dir/image.oci.tar" --label "$label" --file Dockerfile - <"$build_context_archive" || fail "$EXIT_BUILD" "role-image-build-failed"
  chmod 600 "$role_dir/image.oci.tar"
}

export_oci_archive() {
  local role_dir
  role_dir="$(role_artifact_dir "$1")"
  [[ -s "$role_dir/image.oci.tar" && ! -L "$role_dir/image.oci.tar" ]] || fail "$EXIT_BUILD" "oci-archive-missing"
}

derive_subject_tuple() {
  local role="$1" role_dir
  role_dir="$(role_artifact_dir "$role")"
  IMAGE_CONFIG_DIGEST["$role"]="$(python3 "$CHECKER" --oci-archive-config-digest "$role_dir/image.oci.tar")" || fail "$EXIT_BUILD" "oci-archive-config-binding-invalid"
  [[ "${IMAGE_CONFIG_DIGEST[$role]}" =~ ^sha256:[0-9a-f]{64}$ ]] || fail "$EXIT_BUILD" "image-config-digest-invalid"
  OCI_ARCHIVE_SHA256["$role"]="sha256:$(sha256sum "$role_dir/image.oci.tar" | awk '{print $1}')"
  [[ "${OCI_ARCHIVE_SHA256[$role]}" =~ ^sha256:[0-9a-f]{64}$ ]] || fail "$EXIT_POLICY" "oci-archive-digest-invalid"
}

load_role_image_object() {
  local role="$1" role_dir observed tag label
  role_dir="$(role_artifact_dir "$role")"
  [[ -s "$role_dir/image.oci.tar" && ! -L "$role_dir/image.oci.tar" ]] || fail "$EXIT_BUILD" "oci-archive-missing"
  label="org.hyhome.delivery.rehearsal.role=${role}"
  tag="hyhome-local/sample-web-service:${SOURCE_REVISION}-${role}"
  docker buildx build --builder default --network=none --pull=false --load --tag "$tag" --label "$label" --file Dockerfile - <"$build_context_archive" >/dev/null || fail "$EXIT_BUILD" "role-image-load-failed"
  observed="$(docker image inspect --format '{{.Id}}' "$tag")" || fail "$EXIT_BUILD" "role-image-load-identity-missing"
  [[ -n "$observed" && "$observed" != *$'\n'* && "$observed" == "${IMAGE_CONFIG_DIGEST[$role]}" ]] || fail "$EXIT_BUILD" "role-image-load-identity-mismatch"
}

validate_live_sbom() {
  local role="$1" role_dir
  role_dir="$(role_artifact_dir "$role")"
  python3 - "$CHECKER" "$role_dir/sbom.cdx.json" "$role" "$SOURCE_REVISION" "${IMAGE_CONFIG_DIGEST[$role]}" "${OCI_ARCHIVE_SHA256[$role]}" <<'PY'
import importlib.util
import json
import pathlib
import sys

spec = importlib.util.spec_from_file_location("supply_chain_policy", sys.argv[1])
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
subject = {"role": sys.argv[3], "source_revision": sys.argv[4], "image_config_digest": sys.argv[5], "oci_archive_sha256": sys.argv[6]}
errors = module.validate_sbom_subject(json.loads(pathlib.Path(sys.argv[2]).read_text()), subject)
raise SystemExit(1 if errors else 0)
PY
}

bind_sbom_subject() {
  local role="$1" role_dir
  role_dir="$(role_artifact_dir "$role")"
  python3 - "$role_dir/sbom.cdx.json" "$role" "${IMAGE_CONFIG_DIGEST[$role]}" "${OCI_ARCHIVE_SHA256[$role]}" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
document = json.loads(path.read_text(encoding="utf-8"))
metadata = document.setdefault("metadata", {})
component = metadata.setdefault("component", {})
component["name"] = "examples/sample-web-service"
component["type"] = "container"
properties = [row for row in component.get("properties", []) if isinstance(row, dict) and row.get("name") not in {"org.hyhome.delivery.image_config_digest", "org.hyhome.delivery.oci_archive_sha256", "org.hyhome.delivery.rehearsal.role"}]
properties.extend([
    {"name": "org.hyhome.delivery.image_config_digest", "value": sys.argv[3]},
    {"name": "org.hyhome.delivery.oci_archive_sha256", "value": sys.argv[4]},
    {"name": "org.hyhome.delivery.rehearsal.role", "value": sys.argv[2]},
])
component["properties"] = properties
path.write_text(json.dumps(document, sort_keys=True) + "\n", encoding="utf-8")
path.chmod(0o600)
PY
}

write_redacted_grype_input() {
  local role="$1" role_dir
  role_dir="$(role_artifact_dir "$role")"
  python3 - "$role_dir/grype.raw.json" "$role_dir/grype.redacted.json" "${IMAGE_CONFIG_DIGEST[$role]}" <<'PY'
import json
import pathlib
import sys

raw = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
matches = []
for row in raw.get("matches", []):
    artifact = row.get("artifact") or {}
    vulnerability = row.get("vulnerability") or {}
    matches.append({"artifact": {"name": artifact.get("name", "")}, "vulnerability": {"id": vulnerability.get("id", ""), "severity": vulnerability.get("severity", "")}})
payload = {"matches": matches, "schema_version": 1, "subject_digest": sys.argv[3]}
path = pathlib.Path(sys.argv[2])
path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
path.chmod(0o600)
PY
}

evaluate_live_grype() {
  local role="$1" role_dir
  role_dir="$(role_artifact_dir "$role")"
  python3 - "$CHECKER" "$role_dir/grype.redacted.json" "$POLICY" "$BASE_DIR/infra/supply-chain.vulnerability-exceptions.json" "$role" "$SOURCE_REVISION" "${IMAGE_CONFIG_DIGEST[$role]}" "${OCI_ARCHIVE_SHA256[$role]}" "$role_dir/vulnerability-verdict.json" <<'PY'
import importlib.util
import json
import pathlib
import sys

spec = importlib.util.spec_from_file_location("supply_chain_policy", sys.argv[1])
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
fixture = json.loads(pathlib.Path(sys.argv[2]).read_text())
policy = json.loads(pathlib.Path(sys.argv[3]).read_text())
exceptions = json.loads(pathlib.Path(sys.argv[4]).read_text())
subject = {"role": sys.argv[5], "source_revision": sys.argv[6], "image_config_digest": sys.argv[7], "oci_archive_sha256": sys.argv[8]}
result = module.evaluate_grype_fixture(fixture, policy, exceptions, subject)
summary = {"exception_id": result["exception_id"], "policy_id": policy["policy_id"], "reason": result["reason"], "redaction_status": "passed", "role": subject["role"], "verdict": result["verdict"]}
path = pathlib.Path(sys.argv[9])
path.write_text(json.dumps(summary, sort_keys=True) + "\n", encoding="utf-8")
path.chmod(0o600)
raise SystemExit(0 if result["verdict"] == "accepted" else 1)
PY
}

generate_cyclonedx_and_grype_verdict() {
  local role="$1" role_dir
  role_dir="$(role_artifact_dir "$role")"
  docker run --pull=never --rm --network none --user "$(id -u):$(id -g)" --env HOME=/tmp --env XDG_CACHE_HOME=/tmp/.cache --env SYFT_CHECK_FOR_APP_UPDATE=false --mount "type=bind,source=$tool_tmp_dir,target=/tmp" --mount "type=bind,source=$role_dir,target=/workspace,readonly" "$(tool_ref syft)" "oci-archive:/workspace/image.oci.tar" -o cyclonedx-json >"$role_dir/sbom.cdx.json" || fail "$EXIT_SBOM" "sbom-generation-failed"
  chmod 600 "$role_dir/sbom.cdx.json"
  bind_sbom_subject "$role" || fail "$EXIT_SBOM" "sbom-subject-binding-failed"
  validate_live_sbom "$role" || fail "$EXIT_SBOM" "sbom-subject-mismatch"
  docker run --pull=never --rm --network none --user "$(id -u):$(id -g)" --env HOME=/tmp --env XDG_CACHE_HOME=/tmp/.cache --env GRYPE_CHECK_FOR_APP_UPDATE=false --env GRYPE_DB_CACHE_DIR=/grype-db-cache --mount "type=bind,source=$tool_tmp_dir,target=/tmp" --mount "type=bind,source=$grype_db_dir,target=/grype-db-cache,readonly" --mount "type=bind,source=$role_dir,target=/workspace,readonly" "$(tool_ref grype)" "sbom:/workspace/sbom.cdx.json" -o json >"$role_dir/grype.raw.json" || fail "$EXIT_VULNERABILITY" "grype-advisory-db-or-scan-unavailable"
  chmod 600 "$role_dir/grype.raw.json"
  write_redacted_grype_input "$role" || fail "$EXIT_VULNERABILITY" "grype-redaction-failed"
  evaluate_live_grype "$role"
}

require_consumer_safe_vulnerability_verdict() {
  local role_dir
  role_dir="$(role_artifact_dir "$1")"
  python3 - "$role_dir/vulnerability-verdict.json" <<'PY'
import json
import pathlib
import sys

try:
    payload = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError):
    raise SystemExit(1)
if not isinstance(payload, dict) or payload.get("verdict") != "accepted" or "exception_id" not in payload or payload["exception_id"] is not None:
    raise SystemExit(1)
PY
}

record_grype_db_identity() {
  docker run --pull=never --rm --network none --user "$(id -u):$(id -g)" --env HOME=/tmp --env XDG_CACHE_HOME=/tmp/.cache --env GRYPE_CHECK_FOR_APP_UPDATE=false --env GRYPE_DB_CACHE_DIR=/grype-db-cache --mount "type=bind,source=$tool_tmp_dir,target=/tmp" --mount "type=bind,source=$grype_db_dir,target=/grype-db-cache,readonly" "$(tool_ref grype)" db status >"$grype_db_status" || fail "$EXIT_POLICY" "grype-db-identity-unavailable"
  chmod 600 "$grype_db_status"
  python3 - "$grype_db_status" "$grype_db_identity" <<'PY'
import json
import pathlib
import re
import sys

status = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
fields = dict(re.findall(r"^(Schema|Built|Status):\s+(.+)$", status, flags=re.MULTILINE))
checksum = re.search(r"checksum=sha256%3A([0-9a-f]{64})", status)
payload = {"built": fields.get("Built"), "database_package_sha256": checksum.group(1) if checksum else None, "schema": fields.get("Schema"), "schema_version": 1, "status": fields.get("Status")}
if not all(payload[key] for key in ("built", "database_package_sha256", "schema", "status")):
    raise SystemExit("grype-db-identity-incomplete")
path = pathlib.Path(sys.argv[2])
path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
path.chmod(0o600)
PY
}

write_minimized_advisory_summary() {
  local role="$1" role_dir target
  role_dir="$(role_artifact_dir "$role")"
  target="$runtime_dir/advisory-summary.$role.json"
  python3 - "$role_dir/grype.redacted.json" "$role_dir/vulnerability-verdict.json" "$grype_db_identity" "$target" "$role" "$SOURCE_REVISION" "$BUILD_CONTEXT_SHA256" "${IMAGE_CONFIG_DIGEST[$role]}" "${OCI_ARCHIVE_SHA256[$role]}" <<'PY'
import collections
import json
import pathlib
import sys

redacted = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
verdict = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
database = json.loads(pathlib.Path(sys.argv[3]).read_text(encoding="utf-8"))
counts = collections.Counter(str(row.get("vulnerability", {}).get("severity", "unknown")).lower() for row in redacted.get("matches", []))
payload = {
    "build_context_sha256": sys.argv[7],
    "database": database,
    "exception_id": verdict.get("exception_id"),
    "image_config_digest": sys.argv[8],
    "oci_archive_sha256": sys.argv[9],
    "policy_id": verdict.get("policy_id"),
    "reason": verdict.get("reason"),
    "redaction_status": "passed",
    "role": sys.argv[5],
    "schema_version": 1,
    "source_revision": sys.argv[6],
    "verdict": verdict.get("verdict"),
    "vulnerability_counts": dict(sorted(counts.items())),
}
path = pathlib.Path(sys.argv[4])
path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
path.chmod(0o600)
PY
}

publish_role_advisory_summary() {
  local role="$1" source="$runtime_dir/advisory-summary.$1.json"
  write_minimized_advisory_summary "$role" || fail "$EXIT_VULNERABILITY" "advisory-summary-redaction-failed"
  python3 "$CHECKER" --publish-minimized-handoff "$BASE_DIR" "$OUTPUT_RELATIVE" "$output_identity" "advisory-summary.$role.json" "$source" || fail "$EXIT_VULNERABILITY" "advisory-summary-publication-failed"
}

generate_slsa_provenance() {
  local role="$1" role_dir
  role_dir="$(role_artifact_dir "$role")"
  python3 - "$role_dir/provenance.intoto.json" "$role" "$SOURCE_REVISION" "${OCI_ARCHIVE_SHA256[$role]}" "$BUILD_CONTEXT_SHA256" <<'PY'
import json
import pathlib
import sys

payload = {
    "_type": "https://in-toto.io/Statement/v1",
    "predicateType": "https://slsa.dev/provenance/v1",
    "subject": [{"name": "examples/sample-web-service", "digest": {"sha256": sys.argv[4].removeprefix("sha256:")}}],
    "predicate": {"buildDefinition": {"externalParameters": {"build_context_sha256": sys.argv[5], "role": sys.argv[2], "source_revision": sys.argv[3]}, "resolvedDependencies": [{"uri": "git+local://examples/sample-web-service", "digest": {"sha256": sys.argv[5].removeprefix("sha256:")}}]}, "runDetails": {"builder": {"id": "hyhome.local.supply-chain-wrapper"}}},
}
path = pathlib.Path(sys.argv[1])
path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
path.chmod(0o600)
PY
  python3 - "$CHECKER" "$role_dir/provenance.intoto.json" "$role" "$SOURCE_REVISION" "${IMAGE_CONFIG_DIGEST[$role]}" "${OCI_ARCHIVE_SHA256[$role]}" "$BUILD_CONTEXT_SHA256" <<'PY' || fail "$EXIT_PROVENANCE" "provenance-subject-mismatch"
import importlib.util
import json
import pathlib
import sys

spec = importlib.util.spec_from_file_location("supply_chain_policy", sys.argv[1])
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
subject = {"role": sys.argv[3], "source_revision": sys.argv[4], "image_config_digest": sys.argv[5], "oci_archive_sha256": sys.argv[6], "build_context_sha256": sys.argv[7]}
raise SystemExit(1 if module.validate_provenance_subject(json.loads(pathlib.Path(sys.argv[2]).read_text()), subject) else 0)
PY
}

sign_and_verify_archive() {
  local role="$1" other_role="candidate" role_dir other_dir cosign
  [[ "$role" == "baseline" ]] || other_role="baseline"
  role_dir="$(role_artifact_dir "$role")"
  other_dir="$(role_artifact_dir "$other_role")"
  cosign="$(tool_ref cosign)"
  if [[ ! -f "$private_key_dir/cosign.key" ]]; then
    docker run --pull=never --rm --network none --user "$(id -u):$(id -g)" --env HOME=/tmp --env XDG_CACHE_HOME=/tmp/.cache --env COSIGN_PASSWORD= --mount "type=bind,source=$tool_tmp_dir,target=/tmp" --mount "type=bind,source=$private_key_dir,target=/keys" "$cosign" generate-key-pair --output-key-prefix /keys/cosign || fail "$EXIT_SIGNATURE" "ephemeral-key-generation-failed"
  fi
  [[ -f "$COSIGN_OFFLINE_SIGNING_CONFIG" ]] || fail "$EXIT_SIGNATURE" "cosign-offline-signing-config-missing"
  docker run --pull=never --rm --network none --user "$(id -u):$(id -g)" --env HOME=/tmp --env XDG_CACHE_HOME=/tmp/.cache --env COSIGN_PASSWORD= --mount "type=bind,source=$tool_tmp_dir,target=/tmp" --mount "type=bind,source=$private_key_dir,target=/keys,readonly" --mount "type=bind,source=$role_dir,target=/workspace" --mount "type=bind,source=$COSIGN_OFFLINE_SIGNING_CONFIG,target=/policy/cosign-offline-signing-config.json,readonly" "$cosign" sign-blob --signing-config /policy/cosign-offline-signing-config.json --new-bundle-format=false --key /keys/cosign.key --bundle /workspace/cosign.bundle.json /workspace/image.oci.tar || fail "$EXIT_SIGNATURE" "archive-signing-failed"
  python3 - "$role_dir/cosign.bundle.json" "$role_dir/cosign.signature" <<'PY' || fail "$EXIT_SIGNATURE" "archive-signature-extraction-failed"
import base64
import json
import pathlib
import sys

bundle = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
signature = bundle.get("messageSignature", {}).get("signature")
if not isinstance(signature, str) or not signature:
    raise SystemExit("bundle messageSignature.signature missing")
try:
    base64.b64decode(signature, validate=True)
except Exception as exc:
    raise SystemExit(f"bundle signature is not base64: {exc}") from exc
path = pathlib.Path(sys.argv[2])
path.write_text(signature + "\n", encoding="utf-8")
path.chmod(0o600)
PY
  docker run --pull=never --rm --network none --user "$(id -u):$(id -g)" --env HOME=/tmp --env XDG_CACHE_HOME=/tmp/.cache --mount "type=bind,source=$tool_tmp_dir,target=/tmp" --mount "type=bind,source=$private_key_dir,target=/keys,readonly" --mount "type=bind,source=$role_dir,target=/workspace,readonly" "$cosign" verify-blob --insecure-ignore-tlog=true --key /keys/cosign.pub --signature /workspace/cosign.signature /workspace/image.oci.tar || fail "$EXIT_SIGNATURE" "archive-signature-verification-failed"
  cp "$role_dir/image.oci.tar" "$role_dir/tampered.oci.tar"
  chmod 600 "$role_dir/tampered.oci.tar"
  printf 'tamper' >>"$role_dir/tampered.oci.tar"
  if docker run --pull=never --rm --network none --user "$(id -u):$(id -g)" --env HOME=/tmp --env XDG_CACHE_HOME=/tmp/.cache --mount "type=bind,source=$tool_tmp_dir,target=/tmp" --mount "type=bind,source=$private_key_dir,target=/keys,readonly" --mount "type=bind,source=$role_dir,target=/workspace,readonly" "$cosign" verify-blob --insecure-ignore-tlog=true --key /keys/cosign.pub --signature /workspace/cosign.signature /workspace/tampered.oci.tar; then
    fail "$EXIT_SIGNATURE" "tampered-archive-accepted"
  fi
  if docker run --pull=never --rm --network none --user "$(id -u):$(id -g)" --env HOME=/tmp --env XDG_CACHE_HOME=/tmp/.cache --mount "type=bind,source=$tool_tmp_dir,target=/tmp" --mount "type=bind,source=$private_key_dir,target=/keys,readonly" --mount "type=bind,source=$role_dir,target=/workspace,readonly" --mount "type=bind,source=$other_dir,target=/other,readonly" "$cosign" verify-blob --insecure-ignore-tlog=true --key /keys/cosign.pub --signature /workspace/cosign.signature /other/image.oci.tar; then
    fail "$EXIT_SIGNATURE" "wrong-subject-archive-accepted"
  fi
}

write_verification_verdict() {
  local role="$1"
  [[ -n "$run_verdict_dir" && -d "$run_verdict_dir" ]] || fail "$EXIT_POLICY" "run-verdict-directory-invalid"
  python3 - "$run_verdict_dir/verification-verdict.$role.json" "$role" "$SOURCE_REVISION" "${IMAGE_CONFIG_DIGEST[$role]}" "${OCI_ARCHIVE_SHA256[$role]}" "$BUILD_CONTEXT_SHA256" <<'PY'
import datetime as dt
import json
import pathlib
import sys

payload = {"build_context_sha256": sys.argv[6], "exception_id": None, "image_config_digest": sys.argv[4], "oci_archive_sha256": sys.argv[5], "policy_id": "sample-service-local-v1", "producer_spec": "spec:126-security-supply-chain-remediation", "redaction_status": "passed", "role": sys.argv[2], "schema_version": 1, "source_revision": sys.argv[3], "verified_at": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"), "verdict": "accepted"}
path = pathlib.Path(sys.argv[1])
path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
path.chmod(0o600)
PY
}

publish_verification_verdicts() {
  [[ -n "$run_verdict_dir" && -d "$run_verdict_dir" ]] || fail "$EXIT_POLICY" "run-verdict-directory-invalid"
  python3 "$CHECKER" --publish-verdict-pair "$BASE_DIR" "$OUTPUT_RELATIVE" "$output_identity" "$run_verdict_dir/verification-verdict.baseline.json" "$run_verdict_dir/verification-verdict.candidate.json" "$SOURCE_REVISION" "$BUILD_CONTEXT_SHA256" || fail "$EXIT_POLICY" "verdict-pair-publication-failed"
}

run_preflight() {
  [[ -d "$SERVICE_DIR" && -f "$SERVICE_DIR/Dockerfile" && -f "$SERVICE_DIR/.dockerignore" ]] || fail "$EXIT_POLICY" "sample-service-material-missing"
  grep -Fqx "FROM $BUILD_MATERIAL_REF AS build" "$SERVICE_DIR/Dockerfile" || fail "$EXIT_POLICY" "build-material-pin-missing"
  grep -Fqx "FROM $RUNTIME_MATERIAL_REF AS runtime" "$SERVICE_DIR/Dockerfile" || fail "$EXIT_POLICY" "runtime-material-pin-missing"
  load_tool_registry
  validate_policy_and_exceptions
}

run_advisory() {
  prepare_secure_output
  invalidate_consumer_verdicts
  run_preflight
  prepare_transient_directory
  capture_build_context_snapshot
  assert_grype_db_seed_available
  ensure_advisory_prerequisites
  assert_local_image_identities
  seed_private_grype_db_cache
  remove_legacy_runtime_artifacts
  record_grype_db_identity
  build_role_image baseline
  assert_build_context_unchanged
  build_role_image candidate
  assert_build_context_unchanged
  export_oci_archive baseline
  export_oci_archive candidate
  derive_subject_tuple baseline
  derive_subject_tuple candidate
  if [[ "${IMAGE_CONFIG_DIGEST[baseline]}" == "${IMAGE_CONFIG_DIGEST[candidate]}" || "${OCI_ARCHIVE_SHA256[baseline]}" == "${OCI_ARCHIVE_SHA256[candidate]}" ]]; then
    fail "$EXIT_BUILD" "baseline-candidate-subjects-not-distinct"
  fi
  if ! generate_cyclonedx_and_grype_verdict baseline; then
    publish_role_advisory_summary baseline
    fail "$EXIT_VULNERABILITY" "grype-policy-rejected"
  fi
  publish_role_advisory_summary baseline
  require_consumer_safe_vulnerability_verdict baseline || fail "$EXIT_VULNERABILITY" "grype-exception-requires-manual-review"
  if ! generate_cyclonedx_and_grype_verdict candidate; then
    publish_role_advisory_summary candidate
    fail "$EXIT_VULNERABILITY" "grype-policy-rejected"
  fi
  publish_role_advisory_summary candidate
  require_consumer_safe_vulnerability_verdict candidate || fail "$EXIT_VULNERABILITY" "grype-exception-requires-manual-review"
  load_role_image_object baseline
  load_role_image_object candidate
  assert_build_context_unchanged
  generate_slsa_provenance baseline
  generate_slsa_provenance candidate
  sign_and_verify_archive baseline
  sign_and_verify_archive candidate
  assert_build_context_unchanged
  write_verification_verdict baseline
  write_verification_verdict candidate
  publish_verification_verdicts
  printf 'supply_chain_verification=pass roles=baseline,candidate redaction=passed\n'
}

run_scorecard_advisory() {
  run_preflight
  if ! grep -Fqx 'Scorecard network approval: confirmed' "$TASK_DOC"; then
    printf 'scorecard_advisory=skipped reason=task-read-only-network-approval-not-confirmed\n'
    return 0
  fi
  command -v docker >/dev/null || fail "$EXIT_SCORECARD" "docker-unavailable"
  docker info >/dev/null 2>&1 || fail "$EXIT_SCORECARD" "docker-daemon-unavailable"
  assert_local_image_identity "$(tool_ref scorecard)" "$(tool_repo_digest scorecard)" "$(tool_config_id scorecard)"
  docker run --pull=never --rm "$(tool_ref scorecard)" --repo "github.com/buenhyden/hy-home.docker" >/dev/null || fail "$EXIT_SCORECARD" "scorecard-observation-failed"
  printf 'scorecard_advisory=observed mode=read-only-advisory\n'
}

trap cleanup_transient_state EXIT

if [[ "${HYHOME_SUPPLY_CHAIN_LIBRARY_ONLY:-0}" == "1" ]]; then
  if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    exit 0
  fi
  return 0
fi

case "$MODE" in
--preflight)
  run_preflight
  ensure_advisory_prerequisites
  assert_local_image_identities
  printf 'supply_chain_preflight=pass\n'
  ;;
--fixture-only)
  run_preflight
  python3 "$CHECKER" --check
  printf 'supply_chain_fixture_policy=pass network=independent\n'
  ;;
--advisory)
  run_advisory
  ;;
--scorecard-advisory)
  run_scorecard_advisory
  ;;
*)
  usage >&2
  exit "$EXIT_USAGE"
  ;;
esac
