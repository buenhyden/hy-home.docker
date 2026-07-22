#!/usr/bin/env bash
set -Eeuo pipefail

# Local-only supply-chain rehearsal. Runtime artifacts are ignored; no image,
# attestation, signature, or report is published outside this worktree.

BASE_DIR="$(git rev-parse --show-toplevel)"
SERVICE_DIR="$BASE_DIR/examples/sample-web-service"
CHECKER="$BASE_DIR/scripts/validation/check-supply-chain-policy.py"
TOOL_REGISTRY="$BASE_DIR/infra/supply-chain.tool-images.json"
POLICY="$BASE_DIR/infra/supply-chain.sample-service-policy.json"
TASK_DOC="$BASE_DIR/docs/04.execution/tasks/2026-07-19-security-supply-chain-remediation.md"
OUTPUT_DIR="$BASE_DIR/_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain"
SOURCE_REVISION="$(git -C "$BASE_DIR" rev-parse HEAD)"
MODE="${1:-}"

readonly EXIT_USAGE=2 EXIT_POLICY=10 EXIT_BUILD=20 EXIT_SBOM=30
readonly EXIT_VULNERABILITY=40 EXIT_PROVENANCE=50 EXIT_SIGNATURE=60 EXIT_SCORECARD=70

declare -A IMAGE_CONFIG_DIGEST=() OCI_ARCHIVE_SHA256=()
private_key_dir=""
grype_db_dir=""
run_verdict_dir=""

usage() {
  cat <<'EOF'
Usage: bash scripts/security/verify-sample-service-supply-chain.sh --fixture-only|--preflight|--advisory|--scorecard-advisory

`--fixture-only` is deterministic and network-independent. `--advisory` never
pulls missing tool images or downloads a vulnerability database; unavailable
prerequisites are reported as blocked.
EOF
}

fail() {
  printf 'supply_chain_verification=fail class=%s reason=%s\n' "$1" "$2" >&2
  exit "$1"
}

tool_ref() {
  python3 - "$TOOL_REGISTRY" "$1" <<'PY'
import json
import pathlib
import sys

registry = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
for tool in registry["tools"]:
    if tool["name"] == sys.argv[2]:
        print(f'{tool["image"]}@{tool["digest"]}')
        raise SystemExit(0)
raise SystemExit(1)
PY
}

load_tool_registry() {
  python3 "$CHECKER" --check >/dev/null || fail "$EXIT_POLICY" "tool-registry-or-fixture-policy-invalid"
  local tool
  for tool in syft grype cosign scorecard; do
    tool_ref "$tool" >/dev/null || fail "$EXIT_POLICY" "tool-reference-missing"
  done
}

validate_policy_and_exceptions() {
  [[ -f "$POLICY" && -f "$TASK_DOC" ]] || fail "$EXIT_POLICY" "policy-or-task-boundary-missing"
  python3 "$CHECKER" --check >/dev/null || fail "$EXIT_POLICY" "policy-or-exception-invalid"
}

prepare_transient_directory() {
  mkdir -p "$OUTPUT_DIR"
  [[ -d "$OUTPUT_DIR" && "$OUTPUT_DIR" == "$BASE_DIR/_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain" ]] || fail "$EXIT_POLICY" "task-output-path-invalid"
  grype_db_dir="$OUTPUT_DIR/grype-db-cache"
  mkdir -p "$grype_db_dir"
  run_verdict_dir="$(mktemp -d "$OUTPUT_DIR/.verification-verdicts.XXXXXX")"
  private_key_dir="$(mktemp -d /tmp/hyhome-supply-chain.XXXXXX)"
  chmod 700 "$private_key_dir"
}

invalidate_consumer_verdicts() {
  mkdir -p "$OUTPUT_DIR"
  [[ -d "$OUTPUT_DIR" && "$OUTPUT_DIR" == "$BASE_DIR/_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain" ]] || fail "$EXIT_POLICY" "task-output-path-invalid"
  rm -f -- "$OUTPUT_DIR/verification-verdict.baseline.json" "$OUTPUT_DIR/verification-verdict.candidate.json"
}

build_role_image() {
  local role="$1"
  local label="org.hyhome.delivery.rehearsal.role=${role}"
  local role_dir="$OUTPUT_DIR/$role"
  mkdir -p "$role_dir"
  docker buildx build --output "type=oci,dest=$role_dir/image.oci.tar" --label "$label" --file "$SERVICE_DIR/Dockerfile" "$SERVICE_DIR" || fail "$EXIT_BUILD" "role-image-build-failed"
}

export_oci_archive() {
  local role="$1"
  local role_dir="$OUTPUT_DIR/$role"
  local archive="$role_dir/image.oci.tar"
  [[ -s "$archive" ]] || fail "$EXIT_BUILD" "oci-archive-missing"
}

derive_subject_tuple() {
  local role="$1"
  IMAGE_CONFIG_DIGEST["$role"]="$(python3 "$CHECKER" --oci-archive-config-digest "$OUTPUT_DIR/$role/image.oci.tar")" || fail "$EXIT_BUILD" "oci-archive-config-binding-invalid"
  [[ "${IMAGE_CONFIG_DIGEST[$role]}" =~ ^sha256:[0-9a-f]{64}$ ]] || fail "$EXIT_BUILD" "image-config-digest-invalid"
  OCI_ARCHIVE_SHA256["$role"]="sha256:$(sha256sum "$OUTPUT_DIR/$role/image.oci.tar" | awk '{print $1}')"
  [[ "${OCI_ARCHIVE_SHA256[$role]}" =~ ^sha256:[0-9a-f]{64}$ ]] || fail "$EXIT_POLICY" "oci-archive-digest-invalid"
}

validate_live_sbom() {
  local role="$1"
  python3 - "$CHECKER" "$OUTPUT_DIR/$role/sbom.cdx.json" "$role" "$SOURCE_REVISION" "${IMAGE_CONFIG_DIGEST[$role]}" "${OCI_ARCHIVE_SHA256[$role]}" <<'PY'
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
  local role="$1"
  python3 - "$OUTPUT_DIR/$role/sbom.cdx.json" "$role" "${IMAGE_CONFIG_DIGEST[$role]}" "${OCI_ARCHIVE_SHA256[$role]}" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
document = json.loads(path.read_text(encoding="utf-8"))
metadata = document.setdefault("metadata", {})
component = metadata.setdefault("component", {})
component["name"] = "examples/sample-web-service"
component["type"] = "container"
properties = [
    row
    for row in component.get("properties", [])
    if isinstance(row, dict)
    and row.get("name")
    not in {
        "org.hyhome.delivery.image_config_digest",
        "org.hyhome.delivery.oci_archive_sha256",
        "org.hyhome.delivery.rehearsal.role",
    }
]
properties.extend(
    [
        {"name": "org.hyhome.delivery.image_config_digest", "value": sys.argv[3]},
        {"name": "org.hyhome.delivery.oci_archive_sha256", "value": sys.argv[4]},
        {"name": "org.hyhome.delivery.rehearsal.role", "value": sys.argv[2]},
    ]
)
component["properties"] = properties
path.write_text(json.dumps(document, sort_keys=True) + "\n", encoding="utf-8")
PY
}

write_redacted_grype_input() {
  local role="$1"
  python3 - "$OUTPUT_DIR/$role/grype.raw.json" "$OUTPUT_DIR/$role/grype.redacted.json" "${IMAGE_CONFIG_DIGEST[$role]}" <<'PY'
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
pathlib.Path(sys.argv[2]).write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
PY
}

evaluate_live_grype() {
  local role="$1"
  python3 - "$CHECKER" "$OUTPUT_DIR/$role/grype.redacted.json" "$POLICY" "$BASE_DIR/infra/supply-chain.vulnerability-exceptions.json" "$role" "$SOURCE_REVISION" "${IMAGE_CONFIG_DIGEST[$role]}" "${OCI_ARCHIVE_SHA256[$role]}" "$OUTPUT_DIR/$role/vulnerability-verdict.json" <<'PY'
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
summary = {"exception_id": result["exception_id"], "policy_id": policy["policy_id"], "redaction_status": "passed", "role": subject["role"], "verdict": result["verdict"]}
pathlib.Path(sys.argv[9]).write_text(json.dumps(summary, sort_keys=True) + "\n", encoding="utf-8")
raise SystemExit(0 if result["verdict"] == "accepted" else 1)
PY
}

generate_cyclonedx_and_grype_verdict() {
  local role="$1" role_dir="$OUTPUT_DIR/$1"
  docker run --rm --network none --env SYFT_CHECK_FOR_APP_UPDATE=false --mount "type=bind,source=$role_dir,target=/workspace,readonly" "$(tool_ref syft)" "oci-archive:/workspace/image.oci.tar" -o cyclonedx-json >"$role_dir/sbom.cdx.json" || fail "$EXIT_SBOM" "sbom-generation-failed"
  bind_sbom_subject "$role" || fail "$EXIT_SBOM" "sbom-subject-binding-failed"
  validate_live_sbom "$role" || fail "$EXIT_SBOM" "sbom-subject-mismatch"
  docker run --rm --network none --env GRYPE_CHECK_FOR_APP_UPDATE=false --env GRYPE_DB_CACHE_DIR=/grype-db-cache --mount "type=bind,source=$grype_db_dir,target=/grype-db-cache,readonly" --mount "type=bind,source=$role_dir,target=/workspace" "$(tool_ref grype)" "sbom:/workspace/sbom.cdx.json" -o json >"$role_dir/grype.raw.json" || fail "$EXIT_VULNERABILITY" "grype-advisory-db-or-scan-unavailable"
  write_redacted_grype_input "$role" || fail "$EXIT_VULNERABILITY" "grype-redaction-failed"
  evaluate_live_grype "$role" || fail "$EXIT_VULNERABILITY" "grype-policy-rejected"
}

require_consumer_safe_vulnerability_verdict() {
  local role="$1"
  python3 - "$OUTPUT_DIR/$role/vulnerability-verdict.json" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
try:
    payload = json.loads(path.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError):
    raise SystemExit(1)

if not isinstance(payload, dict):
    raise SystemExit(1)
if payload.get("verdict") != "accepted" or "exception_id" not in payload:
    raise SystemExit(1)
if payload["exception_id"] is not None:
    raise SystemExit(1)
PY
}

generate_slsa_provenance() {
  local role="$1" dockerfile_digest
  dockerfile_digest="$(sha256sum "$SERVICE_DIR/Dockerfile" | awk '{print $1}')"
  python3 - "$OUTPUT_DIR/$role/provenance.intoto.json" "$role" "$SOURCE_REVISION" "${OCI_ARCHIVE_SHA256[$role]}" "$dockerfile_digest" <<'PY'
import json
import pathlib
import sys

payload = {
    "_type": "https://in-toto.io/Statement/v1",
    "predicateType": "https://slsa.dev/provenance/v1",
    "subject": [{"name": "examples/sample-web-service", "digest": {"sha256": sys.argv[4].removeprefix("sha256:")}}],
    "predicate": {"buildDefinition": {"externalParameters": {"role": sys.argv[2], "source_revision": sys.argv[3]}, "resolvedDependencies": [{"uri": "git+local://examples/sample-web-service/Dockerfile", "digest": {"sha256": sys.argv[5]}}]}, "runDetails": {"builder": {"id": "hyhome.local.supply-chain-wrapper"}}},
}
pathlib.Path(sys.argv[1]).write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
PY
  python3 - "$CHECKER" "$OUTPUT_DIR/$role/provenance.intoto.json" "$role" "$SOURCE_REVISION" "${IMAGE_CONFIG_DIGEST[$role]}" "${OCI_ARCHIVE_SHA256[$role]}" <<'PY' || fail "$EXIT_PROVENANCE" "provenance-subject-mismatch"
import importlib.util
import json
import pathlib
import sys

spec = importlib.util.spec_from_file_location("supply_chain_policy", sys.argv[1])
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
subject = {"role": sys.argv[3], "source_revision": sys.argv[4], "image_config_digest": sys.argv[5], "oci_archive_sha256": sys.argv[6]}
raise SystemExit(1 if module.validate_provenance_subject(json.loads(pathlib.Path(sys.argv[2]).read_text()), subject) else 0)
PY
}

sign_and_verify_archive() {
  local role="$1" other_role="candidate"
  [[ "$role" == "baseline" ]] || other_role="baseline"
  local cosign
  cosign="$(tool_ref cosign)"
  if [[ ! -f "$private_key_dir/cosign.key" ]]; then
    docker run --rm --network none --env COSIGN_PASSWORD= --mount "type=bind,source=$private_key_dir,target=/keys" "$cosign" generate-key-pair --output-key-prefix /keys/cosign || fail "$EXIT_SIGNATURE" "ephemeral-key-generation-failed"
  fi
  docker run --rm --network none --env COSIGN_PASSWORD= --mount "type=bind,source=$private_key_dir,target=/keys,readonly" --mount "type=bind,source=$OUTPUT_DIR/$role,target=/workspace" "$cosign" sign-blob --tlog-upload=false --key /keys/cosign.key --bundle /workspace/cosign.bundle.json /workspace/image.oci.tar || fail "$EXIT_SIGNATURE" "archive-signing-failed"
  docker run --rm --network none --mount "type=bind,source=$private_key_dir,target=/keys,readonly" --mount "type=bind,source=$OUTPUT_DIR/$role,target=/workspace,readonly" "$cosign" verify-blob --key /keys/cosign.pub --bundle /workspace/cosign.bundle.json /workspace/image.oci.tar || fail "$EXIT_SIGNATURE" "archive-signature-verification-failed"
  cp "$OUTPUT_DIR/$role/image.oci.tar" "$OUTPUT_DIR/$role/tampered.oci.tar"
  printf 'tamper' >>"$OUTPUT_DIR/$role/tampered.oci.tar"
  if docker run --rm --network none --mount "type=bind,source=$private_key_dir,target=/keys,readonly" --mount "type=bind,source=$OUTPUT_DIR/$role,target=/workspace,readonly" "$cosign" verify-blob --key /keys/cosign.pub --bundle /workspace/cosign.bundle.json /workspace/tampered.oci.tar; then
    fail "$EXIT_SIGNATURE" "tampered-archive-accepted"
  fi
  if docker run --rm --network none --mount "type=bind,source=$private_key_dir,target=/keys,readonly" --mount "type=bind,source=$OUTPUT_DIR/$role,target=/workspace,readonly" --mount "type=bind,source=$OUTPUT_DIR/$other_role,target=/other,readonly" "$cosign" verify-blob --key /keys/cosign.pub --bundle /workspace/cosign.bundle.json /other/image.oci.tar; then
    fail "$EXIT_SIGNATURE" "wrong-subject-archive-accepted"
  fi
}

write_verification_verdict() {
  local role="$1"
  [[ -n "$run_verdict_dir" && -d "$run_verdict_dir" ]] || fail "$EXIT_POLICY" "run-verdict-directory-invalid"
  python3 - "$run_verdict_dir/verification-verdict.$role.json" "$role" "$SOURCE_REVISION" "${IMAGE_CONFIG_DIGEST[$role]}" "${OCI_ARCHIVE_SHA256[$role]}" <<'PY'
import datetime as dt
import json
import pathlib
import sys

payload = {"exception_id": None, "image_config_digest": sys.argv[4], "oci_archive_sha256": sys.argv[5], "policy_id": "sample-service-local-v1", "producer_spec": "spec:126-security-supply-chain-remediation", "redaction_status": "passed", "role": sys.argv[2], "schema_version": 1, "source_revision": sys.argv[3], "verified_at": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"), "verdict": "accepted"}
pathlib.Path(sys.argv[1]).write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
PY
}

publish_verification_verdicts() {
  [[ -n "$run_verdict_dir" && -d "$run_verdict_dir" ]] || fail "$EXIT_POLICY" "run-verdict-directory-invalid"
  local role
  for role in baseline candidate; do
    [[ -f "$run_verdict_dir/verification-verdict.$role.json" ]] || fail "$EXIT_POLICY" "run-verdict-missing"
  done
  for role in baseline candidate; do
    mv -f -- "$run_verdict_dir/verification-verdict.$role.json" "$OUTPUT_DIR/verification-verdict.$role.json"
  done
  rmdir -- "$run_verdict_dir"
  run_verdict_dir=""
}

delete_ephemeral_private_key() {
  if [[ -n "$private_key_dir" && "$private_key_dir" == /tmp/hyhome-supply-chain.* && -d "$private_key_dir" ]]; then
    rm -rf -- "$private_key_dir"
  fi
  private_key_dir=""
}

delete_run_verdict_directory() {
  if [[ -n "$run_verdict_dir" && "$run_verdict_dir" == "$OUTPUT_DIR/.verification-verdicts."* && -d "$run_verdict_dir" ]]; then
    rm -rf -- "$run_verdict_dir"
  fi
  run_verdict_dir=""
}

cleanup_transient_state() {
  delete_ephemeral_private_key
  delete_run_verdict_directory
}

run_preflight() {
  [[ -d "$SERVICE_DIR" && -f "$SERVICE_DIR/Dockerfile" ]] || fail "$EXIT_POLICY" "sample-service-material-missing"
  grep -Fqx 'FROM alpine:3.21@sha256:48b0309ca019d89d40f670aa1bc06e426dc0931948452e8491e3d65087abc07d AS build' "$SERVICE_DIR/Dockerfile" || fail "$EXIT_POLICY" "build-material-pin-missing"
  grep -Fqx 'FROM nginxinc/nginx-unprivileged:1.27.3-alpine@sha256:9e7238f579a54582263a960d1b0094b4a3ecce641342eda3f8e2ff82b1703d2b AS runtime' "$SERVICE_DIR/Dockerfile" || fail "$EXIT_POLICY" "runtime-material-pin-missing"
  load_tool_registry
  validate_policy_and_exceptions
}

ensure_advisory_prerequisites() {
  command -v docker >/dev/null || fail "$EXIT_POLICY" "docker-unavailable-advisory-blocked"
  docker buildx version >/dev/null 2>&1 || fail "$EXIT_POLICY" "docker-buildx-unavailable-advisory-blocked"
  local tool
  for tool in syft grype cosign; do
    docker image inspect "$(tool_ref "$tool")" >/dev/null 2>&1 || fail "$EXIT_POLICY" "pinned-tool-image-unavailable-advisory-blocked"
  done
  [[ -n "$grype_db_dir" && -d "$grype_db_dir" ]] || fail "$EXIT_POLICY" "grype-db-cache-path-invalid"
  docker run --rm --network none --env GRYPE_CHECK_FOR_APP_UPDATE=false --env GRYPE_DB_CACHE_DIR=/grype-db-cache --mount "type=bind,source=$grype_db_dir,target=/grype-db-cache,readonly" "$(tool_ref grype)" db status >/dev/null 2>&1 || fail "$EXIT_POLICY" "grype-db-unavailable-advisory-blocked"
}

record_grype_db_identity() {
  docker run --rm --network none --env GRYPE_CHECK_FOR_APP_UPDATE=false --env GRYPE_DB_CACHE_DIR=/grype-db-cache --mount "type=bind,source=$grype_db_dir,target=/grype-db-cache,readonly" "$(tool_ref grype)" db status >"$OUTPUT_DIR/grype-db-status.txt" || fail "$EXIT_POLICY" "grype-db-identity-unavailable"
  python3 - "$OUTPUT_DIR/grype-db-status.txt" "$OUTPUT_DIR/grype-db-identity.json" <<'PY'
import json
import pathlib
import re
import sys

status = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
fields = dict(re.findall(r"^(Schema|Built|Status):\s+(.+)$", status, flags=re.MULTILINE))
checksum = re.search(r"checksum=sha256%3A([0-9a-f]{64})", status)
payload = {
    "built": fields.get("Built"),
    "database_package_sha256": checksum.group(1) if checksum else None,
    "schema": fields.get("Schema"),
    "schema_version": 1,
    "status": fields.get("Status"),
}
if not all(payload[key] for key in ("built", "database_package_sha256", "schema", "status")):
    raise SystemExit("grype-db-identity-incomplete")
pathlib.Path(sys.argv[2]).write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
PY
}

run_advisory() {
  invalidate_consumer_verdicts
  run_preflight
  prepare_transient_directory
  ensure_advisory_prerequisites
  record_grype_db_identity
  build_role_image baseline
  build_role_image candidate
  export_oci_archive baseline
  export_oci_archive candidate
  derive_subject_tuple baseline
  derive_subject_tuple candidate
  if [[ "${IMAGE_CONFIG_DIGEST[baseline]}" == "${IMAGE_CONFIG_DIGEST[candidate]}" || "${OCI_ARCHIVE_SHA256[baseline]}" == "${OCI_ARCHIVE_SHA256[candidate]}" ]]; then
    fail "$EXIT_BUILD" "baseline-candidate-subjects-not-distinct"
  fi
  generate_cyclonedx_and_grype_verdict baseline
  require_consumer_safe_vulnerability_verdict baseline || fail "$EXIT_VULNERABILITY" "grype-exception-requires-manual-review"
  generate_cyclonedx_and_grype_verdict candidate
  require_consumer_safe_vulnerability_verdict candidate || fail "$EXIT_VULNERABILITY" "grype-exception-requires-manual-review"
  generate_slsa_provenance baseline
  generate_slsa_provenance candidate
  sign_and_verify_archive baseline
  sign_and_verify_archive candidate
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
  docker image inspect "$(tool_ref scorecard)" >/dev/null 2>&1 || fail "$EXIT_SCORECARD" "pinned-scorecard-image-unavailable"
  docker run --rm "$(tool_ref scorecard)" --repo "github.com/buenhyden/hy-home.docker" >/dev/null || fail "$EXIT_SCORECARD" "scorecard-observation-failed"
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
