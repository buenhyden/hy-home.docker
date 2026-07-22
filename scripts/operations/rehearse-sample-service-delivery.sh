#!/usr/bin/env bash
# Local-only sample service promotion/rollback rehearsal for Spec 127.

set -uo pipefail

DRE_TOTAL_TIMEOUT_SECONDS=180
DRE_CLEANUP_RESERVE_SECONDS=30
DRE_BASELINE_PORT=18080
DRE_CANARY_PORT=18081
DRE_OWNER_LABEL="task:2026-07-19-deployment-release-engineering-remediation"
DRE_SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
DRE_ROOT="$(cd -- "$DRE_SCRIPT_DIR/../.." && pwd -P)"
DRE_COMPOSE_PATH="$DRE_ROOT/examples/sample-web-service/docker-compose.yml"
DRE_OVERRIDE_PATH="$DRE_ROOT/tests/fixtures/sample-service-delivery/compose.delivery.override.yml"
DRE_FIXTURE_BASELINE_PATH="$DRE_ROOT/tests/fixtures/sample-service-delivery/spec126-verdict.baseline.accepted.json"
DRE_FIXTURE_CANDIDATE_PATH="$DRE_ROOT/tests/fixtures/sample-service-delivery/spec126-verdict.candidate.accepted.json"
DRE_REAL_BASELINE_PATH="$DRE_ROOT/_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.baseline.json"
DRE_REAL_CANDIDATE_PATH="$DRE_ROOT/_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.candidate.json"
DRE_READINESS_PATH="$DRE_ROOT/_workspace/repo-support/task-2026-07-19-compose-runtime-readiness-remediation/compose/readiness-verdict.json"
DRE_RECOVERY_PATH="$DRE_ROOT/_workspace/repo-support/task-2026-07-19-infrastructure-operations-readiness-remediation/postgres/recovery-verdict.json"
DRE_RECORD_PATH_DEFAULT="$DRE_ROOT/_workspace/repo-support/task-2026-07-19-deployment-release-engineering-remediation/delivery/rehearsal-record.json"

declare -Ag VERDICT_ROLE=()
declare -Ag VERDICT_SOURCE_REVISION=()
declare -Ag VERDICT_IMAGE_CONFIG_DIGEST=()
declare -Ag VERDICT_OCI_ARCHIVE_SHA256=()

dre_fail() {
  local class="$1"
  local code="$2"
  printf 'class=%s code=%s\n' "$class" "$code" >&2
  return "$class"
}

dre_python_json() {
  command python3 - "$@"
}

parse_subcommand() {
  SUBCOMMAND="${1:-}"
  case "$SUBCOMMAND" in
    preflight|rehearse|cleanup) ;;
    *) return 2 ;;
  esac
}

load_and_validate_verdict() {
  local expected_role="${1:-}"
  local verdict_path="${2:-}"
  local parsed

  [[ "$expected_role" == "baseline" || "$expected_role" == "candidate" ]] || {
    dre_fail 10 verdict-role-invalid
    return
  }
  [[ -f "$verdict_path" && ! -L "$verdict_path" ]] || {
    dre_fail 10 verdict-file-missing
    return
  }

  if ! parsed="$(dre_python_json "$expected_role" "$verdict_path" <<'PY'
import json
import re
import sys
from pathlib import Path

expected_role, raw_path = sys.argv[1:]
def unique_object(pairs):
    result = {}
    for key, item in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = item
    return result
expected_keys = {
    "schema_version", "producer_spec", "role", "source_revision",
    "image_config_digest", "oci_archive_sha256", "policy_id", "verdict",
    "exception_id", "verified_at", "redaction_status",
}
try:
    raw = Path(raw_path).read_text(encoding="utf-8")
    value = json.loads(raw, object_pairs_hook=unique_object)
except (OSError, UnicodeError, ValueError):
    raise SystemExit(1)
if not isinstance(value, dict) or set(value) != expected_keys:
    raise SystemExit(1)
if type(value["schema_version"]) is not int or value["schema_version"] != 1:
    raise SystemExit(1)
if value["producer_spec"] != "spec:126-security-supply-chain-remediation":
    raise SystemExit(1)
if value["role"] != expected_role:
    raise SystemExit(1)
if not isinstance(value["source_revision"], str) or not re.fullmatch(r"[0-9a-f]{40}", value["source_revision"]):
    raise SystemExit(1)
digest = r"sha256:[0-9a-f]{64}"
if not isinstance(value["image_config_digest"], str) or not re.fullmatch(digest, value["image_config_digest"]):
    raise SystemExit(1)
if not isinstance(value["oci_archive_sha256"], str) or not re.fullmatch(digest, value["oci_archive_sha256"]):
    raise SystemExit(1)
if value["policy_id"] != "sample-service-local-v1":
    raise SystemExit(1)
if value["verdict"] != "accepted" or value["exception_id"] is not None:
    raise SystemExit(1)
if value["redaction_status"] != "passed":
    raise SystemExit(1)
if not isinstance(value["verified_at"], str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value["verified_at"]):
    raise SystemExit(1)
print("\t".join((value["role"], value["source_revision"], value["image_config_digest"], value["oci_archive_sha256"])))
PY
)"; then
    dre_fail 10 verdict-invalid
    return
  fi

  IFS=$'\t' read -r VERDICT_ROLE["$expected_role"] \
    VERDICT_SOURCE_REVISION["$expected_role"] \
    VERDICT_IMAGE_CONFIG_DIGEST["$expected_role"] \
    VERDICT_OCI_ARCHIVE_SHA256["$expected_role"] <<<"$parsed"
}

assert_distinct_subjects_and_same_revision() {
  [[ "${VERDICT_ROLE[baseline]:-}" == baseline ]] || {
    dre_fail 10 baseline-verdict-unavailable
    return
  }
  [[ "${VERDICT_ROLE[candidate]:-}" == candidate ]] || {
    dre_fail 10 candidate-verdict-unavailable
    return
  }
  [[ "${VERDICT_SOURCE_REVISION[baseline]:-}" == "${VERDICT_SOURCE_REVISION[candidate]:-}" ]] || {
    dre_fail 10 source-revision-mismatch
    return
  }
  [[ "${VERDICT_IMAGE_CONFIG_DIGEST[baseline]:-}" != "${VERDICT_IMAGE_CONFIG_DIGEST[candidate]:-}" ]] || {
    dre_fail 10 image-config-digest-not-distinct
    return
  }
  [[ "${VERDICT_OCI_ARCHIVE_SHA256[baseline]:-}" != "${VERDICT_OCI_ARCHIVE_SHA256[candidate]:-}" ]] || {
    dre_fail 10 oci-archive-digest-not-distinct
    return
  }
  SOURCE_REVISION="${VERDICT_SOURCE_REVISION[baseline]:-}"
}

validate_local_image_object() {
  local role="${1:-}"
  local digest="${2:-}"
  local observed
  [[ "$role" == baseline || "$role" == candidate ]] || {
    dre_fail 10 local-image-role-invalid
    return
  }
  [[ "$digest" == "${VERDICT_IMAGE_CONFIG_DIGEST[$role]:-}" ]] || {
    dre_fail 10 local-image-input-mismatch
    return
  }
  if ! observed="$(dre_operation_bounded 8 docker image inspect --format '{{.Id}}' "$digest")"; then
    dre_fail 10 local-image-object-missing
    return
  fi
  [[ -n "$observed" && "$observed" != *$'\n'* && "$observed" == "$digest" ]] || {
    dre_fail 10 local-image-object-ambiguous
    return
  }
}

validate_local_image_objects() {
  validate_local_image_object baseline "${VERDICT_IMAGE_CONFIG_DIGEST[baseline]:-}" || return
  validate_local_image_object candidate "${VERDICT_IMAGE_CONFIG_DIGEST[candidate]:-}"
}

assert_ports_and_owned_project_names() {
  [[ "$DRE_BASELINE_PORT" == 18080 && "$DRE_CANARY_PORT" == 18081 ]] || {
    dre_fail 10 ports-invalid
    return
  }
  [[ "$DRE_BASELINE_PORT" != "$DRE_CANARY_PORT" ]] || {
    dre_fail 10 ports-collide
    return
  }
  assert_owned_project_names
}

start_baseline() {
  BASELINE_START_ATTEMPTED=true
  if ! DRE_ROLE=baseline DRE_TASK_ID="$TASK_ID" DRE_HOST_PORT="$DRE_BASELINE_PORT" \
    DRE_IMAGE_CONFIG_DIGEST="${VERDICT_IMAGE_CONFIG_DIGEST[baseline]}" \
    dre_compose "$BASELINE_PROJECT" up -d --pull never --no-build --remove-orphans; then
    dre_fail 20 baseline-start-failed
    return
  fi
  BASELINE_STARTED=true
}

wait_container_and_http_health() {
  local project="$1"
  local port="$2"
  local deadline="$3"
  local failure_class="${4:-30}"
  local boundary="${5:-operation}"
  local bounded=dre_operation_bounded
  local container_query=dre_owned_container_id
  local container_id state marker http_code

  if [[ "$boundary" == cleanup ]]; then
    bounded=dre_cleanup_bounded
    container_query=dre_owned_container_id_cleanup
  fi

  while (( SECONDS < deadline )); do
    if ! container_id="$("$container_query" "$project")"; then
      dre_fail "$failure_class" health-container-query-failed
      return
    fi
    if [[ -n "$container_id" ]]; then
      state="$("$bounded" 8 docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$container_id" 2>/dev/null || true)"
      http_code="$("$bounded" 8 curl --silent --show-error --output /dev/null --write-out '%{http_code}' "http://127.0.0.1:${port}/" 2>/dev/null || true)"
      marker="$("$bounded" 8 curl --silent --show-error --fail "http://127.0.0.1:${port}/" 2>/dev/null | command grep -Fq '<h1>sample-web-service</h1>' && printf present || printf absent)"
      if health_observation_is_accepted "$state" "$http_code" "$marker" &&
        [[ "$project" != "${CANARY_PROJECT:-}" || "${CANARY_HEALTH_FORCED_TIMEOUT:-false}" != true ]]; then
        return 0
      fi
    fi
    "$bounded" 3 sleep 2 || true
  done
  dre_fail "$failure_class" health-deadline-exceeded
}

start_canary() {
  CANARY_START_ATTEMPTED=true
  if ! DRE_ROLE=canary DRE_TASK_ID="$TASK_ID" DRE_HOST_PORT="$DRE_CANARY_PORT" \
    DRE_IMAGE_CONFIG_DIGEST="${VERDICT_IMAGE_CONFIG_DIGEST[candidate]}" \
    dre_compose "$CANARY_PROJECT" up -d --pull never --no-build --remove-orphans; then
    dre_fail 30 canary-start-failed
    return
  fi
  CANARY_STARTED=true
}

record_promotion_decision() {
  [[ "${PROMOTION_GATES_COMPLETE:-false}" == true ]] || {
    dre_fail 40 promotion-gates-incomplete
    return
  }
  PROMOTION_DECISION=promoted
  ROLLBACK_DECISION=not_required
  POST_ROLLBACK_HEALTH=not_applicable
}

inject_canary_timeout_when_requested() {
  CANARY_HEALTH_FORCED_TIMEOUT=false
  if [[ "${FAILURE_MODE:-none}" == canary-health-timeout ]]; then
    CANARY_HEALTH_FORCED_TIMEOUT=true
  fi
}

rollback_to_baseline_digest() {
  PROMOTION_DECISION=not_promoted
  if ! dre_cleanup_one_project "$CANARY_PROJECT"; then
    ROLLBACK_DECISION=failed
    dre_fail 50 canary-stop-failed
    return
  fi
  CANARY_STARTED=false
  ROLLBACK_DECISION=rolled_back_to_baseline
}

verify_baseline_previous_digest() {
  local container_id observed_digest
  container_id="$(dre_owned_container_id_cleanup "$BASELINE_PROJECT")" || return 50
  [[ -n "$container_id" ]] || {
    dre_fail 50 baseline-container-missing
    return
  }
  observed_digest="$(dre_cleanup_bounded 8 docker inspect --format '{{.Image}}' "$container_id")" || {
    dre_fail 50 baseline-digest-query-failed
    return
  }
  [[ "$observed_digest" == "${VERDICT_IMAGE_CONFIG_DIGEST[baseline]:-}" ]] || {
    dre_fail 50 baseline-digest-mismatch
    return
  }
}

verify_post_rollback_health() {
  verify_baseline_previous_digest || return
  wait_container_and_http_health "$BASELINE_PROJECT" "$DRE_BASELINE_PORT" "$DRE_RUN_DEADLINE" 50 cleanup || return
  POST_ROLLBACK_HEALTH=passed
}

write_rehearsal_record() {
  CANDIDATE_JSON="$(build_rehearsal_record_json)" || return
  publish_rehearsal_record
}

cleanup_owned_projects() {
  local failed=0
  assert_owned_project_names || return
  dre_cleanup_one_project "$CANARY_PROJECT" || failed=1
  dre_cleanup_one_project "$BASELINE_PROJECT" || failed=1
  if (( failed != 0 )); then
    CLEANUP_COMPLETE=false
    dre_fail 60 owned-cleanup-failed
    return
  fi
  CLEANUP_COMPLETE=true
  BASELINE_STARTED=false
  CANARY_STARTED=false
}

assert_owned_project_names() {
  local pattern='^hyhome-dre-20260719-[0-9]+-(baseline|canary)$'
  [[ "${BASELINE_PROJECT:-}" =~ $pattern && "${BASELINE_PROJECT}" == *-baseline ]] || {
    dre_fail 10 baseline-project-not-owned
    return
  }
  [[ "${CANARY_PROJECT:-}" =~ $pattern && "${CANARY_PROJECT}" == *-canary ]] || {
    dre_fail 10 canary-project-not-owned
    return
  }
  [[ "${BASELINE_PROJECT%-baseline}" == "${CANARY_PROJECT%-canary}" ]] || {
    dre_fail 10 project-pair-mismatch
    return
  }
}

health_observation_is_accepted() {
  [[ "${1:-}" == healthy && "${2:-}" == 200 && "${3:-}" == present ]]
}

validate_compose_contract() {
  local compose_path="${1:-}"
  local override_path="${2:-}"
  [[ -f "$compose_path" && -f "$override_path" ]] || {
    dre_fail 10 compose-contract-file-missing
    return
  }
  dre_python_json "$compose_path" "$override_path" <<'PY' || {
import re
import sys
from pathlib import Path

try:
    compose = Path(sys.argv[1]).read_text(encoding="utf-8")
    override = Path(sys.argv[2]).read_text(encoding="utf-8")
except (OSError, UnicodeError):
    raise SystemExit(1)
if re.search(r"(?m)^name\s*:", compose) or re.search(r"(?m)^\s+container_name\s*:", compose):
    raise SystemExit(1)
required = (
    "127.0.0.1:${DRE_HOST_PORT:?loopback host port required}:8080",
    "org.hyhome.delivery.owner: task:2026-07-19-deployment-release-engineering-remediation",
    "org.hyhome.delivery.task-id: ${DRE_TASK_ID:?delivery task id required}",
    "org.hyhome.delivery.role: ${DRE_ROLE:?delivery role required}",
    "image: ${DRE_IMAGE_CONFIG_DIGEST:?immutable local image config digest required}",
    "pull_policy: never",
)
if any(item not in override for item in required):
    raise SystemExit(1)
for label in (
    "org.hyhome.delivery.owner:",
    "org.hyhome.delivery.task-id:",
    "org.hyhome.delivery.role:",
):
    if override.count(label) != 2:
        raise SystemExit(1)
if override.count("build: !reset null") != 1 or override.count("127.0.0.1:${DRE_HOST_PORT") != 1:
    raise SystemExit(1)
PY
    dre_fail 10 compose-contract-invalid
    return
  }
}

validate_readiness_verdict() {
  local path="${1:-}"
  [[ -f "$path" && ! -L "$path" ]] || {
    dre_fail 10 readiness-verdict-missing
    return
  }
  dre_python_json "$path" <<'PY' || {
import json
import re
import sys
from pathlib import Path

keys = {
    "approval_ref", "cleanup_status", "completed_at", "elapsed_seconds",
    "endpoint_verdicts", "observed_state", "overall_status", "producer_spec",
    "producer_task", "project_name", "recovery_status", "redaction_status",
    "scenario", "schema_version", "services", "started_at", "target_class",
    "teardown_status",
}
def unique_object(pairs):
    result = {}
    for key, item in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = item
    return result
endpoints = {"keycloak-ready", "oauth2-proxy-ping", "traefik-ping", "vault-agent-sentinel", "vault-health"}
services = {"keycloak", "oauth2-proxy", "traefik", "vault", "vault-agent"}
try:
    value = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"), object_pairs_hook=unique_object)
except (OSError, UnicodeError, ValueError):
    raise SystemExit(1)
if not isinstance(value, dict) or set(value) != keys:
    raise SystemExit(1)
if type(value["schema_version"]) is not int or value["schema_version"] != 2:
    raise SystemExit(1)
exact = {
    "producer_spec": "spec:124-compose-runtime-readiness-remediation",
    "producer_task": "task:2026-07-19-compose-runtime-readiness-remediation",
    "scenario": "vault-restart-recovery",
    "target_class": "local-linked-worktree-docker-engine",
    "observed_state": "ready", "overall_status": "ready",
    "recovery_status": "passed", "teardown_status": "passed",
    "cleanup_status": "passed", "redaction_status": "passed",
}
if any(value.get(key) != expected for key, expected in exact.items()):
    raise SystemExit(1)
if value["approval_ref"] != "task:2026-07-19-compose-runtime-readiness-remediation#approval-2026-07-19":
    raise SystemExit(1)
if not isinstance(value["project_name"], str) or not re.fullmatch(r"hyhome-crr-[a-z0-9-]+", value["project_name"]):
    raise SystemExit(1)
if type(value["elapsed_seconds"]) is not int or value["elapsed_seconds"] < 0:
    raise SystemExit(1)
if set(value["endpoint_verdicts"]) != endpoints or any(v != "passed" for v in value["endpoint_verdicts"].values()):
    raise SystemExit(1)
if set(value["services"]) != services:
    raise SystemExit(1)
if any(not isinstance(v, dict) or v != {"container": "healthy"} for v in value["services"].values()):
    raise SystemExit(1)
timestamp = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
if any(not isinstance(value[k], str) or not re.fullmatch(timestamp, value[k]) for k in ("started_at", "completed_at")):
    raise SystemExit(1)
PY
    dre_fail 10 readiness-verdict-invalid
    return
  }
}

validate_recovery_boundary() {
  local path="${1:-}"
  [[ -f "$path" && ! -L "$path" ]] || {
    dre_fail 10 recovery-boundary-missing
    return
  }
  dre_python_json "$path" <<'PY' || {
import json
import re
import sys
from pathlib import Path

keys = {
    "backup_seconds", "cleanup_status", "dump_sha256", "fixture_sha256",
    "integrity_status", "producer_spec", "redaction_status", "restore_seconds",
    "schema_version", "scope", "source_image", "target_image",
}
def unique_object(pairs):
    result = {}
    for key, item in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = item
    return result
try:
    value = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"), object_pairs_hook=unique_object)
except (OSError, UnicodeError, ValueError):
    raise SystemExit(1)
if not isinstance(value, dict) or set(value) != keys:
    raise SystemExit(1)
exact = {
    "schema_version": 1,
    "producer_spec": "spec:125-infrastructure-operations-readiness-remediation",
    "scope": "synthetic-local", "integrity_status": "passed",
    "cleanup_status": "passed", "redaction_status": "passed",
}
if any(type(value[k]) is not type(expected) or value[k] != expected for k, expected in exact.items()):
    raise SystemExit(1)
digest = r"sha256:[0-9a-f]{64}"
if any(not isinstance(value[k], str) or not re.fullmatch(digest, value[k]) for k in ("fixture_sha256", "dump_sha256")):
    raise SystemExit(1)
image = r"[a-z0-9./_-]+:[A-Za-z0-9._-]+@sha256:[0-9a-f]{64}"
if any(not isinstance(value[k], str) or not re.fullmatch(image, value[k]) for k in ("source_image", "target_image")):
    raise SystemExit(1)
if any(type(value[k]) is not int or value[k] < 0 for k in ("backup_seconds", "restore_seconds")):
    raise SystemExit(1)
PY
    dre_fail 10 recovery-boundary-invalid
    return
  }
}

build_rehearsal_record_json() {
  dre_python_json \
    "${SOURCE_REVISION:-}" \
    "${BASELINE_VERDICT_PATH:-}" \
    "${CANDIDATE_VERDICT_PATH:-}" \
    "${READINESS_VERDICT_PATH:-$DRE_READINESS_PATH}" \
    "${BASELINE_PROJECT:-}" \
    "${CANARY_PROJECT:-}" \
    "${PROMOTION_DECISION:-not_run}" \
    "${ROLLBACK_DECISION:-not_run}" \
    "${POST_ROLLBACK_HEALTH:-not_run}" \
    "${RECOVERY_VERDICT_PATH:-$DRE_RECOVERY_PATH}" \
    "${CLEANUP_COMPLETE:-false}" <<'PY'
import json
import sys

(revision, baseline_ref, candidate_ref, readiness_ref,
 baseline_project, canary_project, promotion, rollback, post_health,
 recovery_ref, cleanup) = sys.argv[1:]
rehearsal_id = f"local-rehearsal-20260719-{revision[:12]}"
value = {
    "schema_version": 1,
    "producer_spec": "spec:127-deployment-release-engineering-remediation",
    "release_rehearsal_id": rehearsal_id,
    "source_revision": revision,
    "baseline_verdict_ref": baseline_ref.rsplit("/", 1)[-1],
    "candidate_verdict_ref": candidate_ref.rsplit("/", 1)[-1],
    "readiness_verdict_ref": readiness_ref.rsplit("/", 1)[-1],
    "baseline_project": baseline_project,
    "canary_project": canary_project,
    "promotion_decision": promotion,
    "rollback_decision": rollback,
    "post_rollback_health": post_health,
    "data_impact": "none",
    "recovery_boundary_ref": recovery_ref.rsplit("/", 1)[-1],
    "cleanup_status": "passed" if cleanup == "true" else "failed",
    "remote_non_goals_confirmed": True,
}
print(json.dumps(value, sort_keys=True, separators=(",", ":")))
PY
}

prepare_canonical_record_path() {
  dre_python_json "$DRE_ROOT" "$DRE_RECORD_PATH_DEFAULT" <<'PY' || {
import os
from pathlib import Path
import stat
import sys

root = Path(sys.argv[1])
target = Path(sys.argv[2])
anchor = root / "_workspace" / "repo-support"
expected = anchor / "task-2026-07-19-deployment-release-engineering-remediation" / "delivery" / "rehearsal-record.json"
if target != expected:
    raise SystemExit(1)
try:
    anchor_info = anchor.lstat()
except OSError:
    raise SystemExit(1)
if not stat.S_ISDIR(anchor_info.st_mode) or stat.S_ISLNK(anchor_info.st_mode):
    raise SystemExit(1)
if anchor.resolve(strict=True) != anchor.absolute() or anchor_info.st_uid != os.getuid():
    raise SystemExit(1)
if stat.S_IMODE(anchor_info.st_mode) & 0o022:
    raise SystemExit(1)

flags = os.O_RDONLY | os.O_DIRECTORY
if hasattr(os, "O_NOFOLLOW"):
    flags |= os.O_NOFOLLOW
fd = os.open(anchor, flags)
try:
    for component in (
        "task-2026-07-19-deployment-release-engineering-remediation",
        "delivery",
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

try:
    info = target.lstat()
except FileNotFoundError:
    pass
else:
    if not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode) or info.st_uid != os.getuid():
        raise SystemExit(1)
    target.unlink()
PY
    dre_fail 10 canonical-record-path-unsafe
    return
  }
}

publish_rehearsal_record() {
  [[ "${CLEANUP_COMPLETE:-false}" == true ]] || {
    dre_fail 40 cleanup-incomplete
    return
  }
  local record_path="${REHEARSAL_RECORD_PATH:-$DRE_RECORD_PATH_DEFAULT}"
  local record_dir
  if ! dre_python_json "${CANDIDATE_JSON:-}" <<'PY'
import json
import re
import sys

keys = {
    "schema_version", "producer_spec", "release_rehearsal_id",
    "source_revision", "baseline_verdict_ref", "candidate_verdict_ref",
    "readiness_verdict_ref", "baseline_project", "canary_project",
    "promotion_decision", "rollback_decision", "post_rollback_health",
    "data_impact", "recovery_boundary_ref", "cleanup_status",
    "remote_non_goals_confirmed",
}
def unique_object(pairs):
    result = {}
    for key, item in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = item
    return result
try:
    value = json.loads(sys.argv[1], object_pairs_hook=unique_object)
except (UnicodeError, ValueError):
    raise SystemExit(1)
if not isinstance(value, dict) or set(value) != keys:
    raise SystemExit(1)
if type(value["schema_version"]) is not int or value["schema_version"] != 1:
    raise SystemExit(1)
if value["producer_spec"] != "spec:127-deployment-release-engineering-remediation":
    raise SystemExit(1)
if not isinstance(value["source_revision"], str) or not re.fullmatch(r"[0-9a-f]{40}", value["source_revision"]):
    raise SystemExit(1)
if value["release_rehearsal_id"] != f"local-rehearsal-20260719-{value['source_revision'][:12]}":
    raise SystemExit(1)
if value["baseline_verdict_ref"] != "verification-verdict.baseline.json":
    raise SystemExit(1)
if value["candidate_verdict_ref"] != "verification-verdict.candidate.json":
    raise SystemExit(1)
if value["readiness_verdict_ref"] != "readiness-verdict.json":
    raise SystemExit(1)
if value["recovery_boundary_ref"] != "recovery-verdict.json":
    raise SystemExit(1)
project = r"hyhome-dre-20260719-[0-9]+"
if not re.fullmatch(project + r"-baseline", value["baseline_project"]):
    raise SystemExit(1)
if not re.fullmatch(project + r"-canary", value["canary_project"]):
    raise SystemExit(1)
if value["baseline_project"][:-9] != value["canary_project"][:-7]:
    raise SystemExit(1)
allowed_decisions = {
    ("promoted", "not_required", "not_applicable"),
    ("not_promoted", "rolled_back_to_baseline", "passed"),
}
if (value["promotion_decision"], value["rollback_decision"], value["post_rollback_health"]) not in allowed_decisions:
    raise SystemExit(1)
if value["data_impact"] != "none" or value["cleanup_status"] != "passed":
    raise SystemExit(1)
if value["remote_non_goals_confirmed"] is not True:
    raise SystemExit(1)
PY
  then
    dre_fail 40 record-schema-invalid
    return
  fi
  record_dir="$(dirname -- "$record_path")"
  dre_python_json "$record_dir" "$record_path" "${CANDIDATE_JSON:-}" <<'PY' || {
import json
import os
from pathlib import Path
import stat
import sys

parent = Path(sys.argv[1])
target = Path(sys.argv[2])
payload = json.loads(sys.argv[3])
if target.parent != parent or target.name != "rehearsal-record.json":
    raise SystemExit(1)
try:
    parent_info = parent.lstat()
except OSError:
    raise SystemExit(1)
if not stat.S_ISDIR(parent_info.st_mode) or stat.S_ISLNK(parent_info.st_mode):
    raise SystemExit(1)
if parent.resolve(strict=True) != parent.absolute() or parent_info.st_uid != os.getuid():
    raise SystemExit(1)
if stat.S_IMODE(parent_info.st_mode) & 0o022:
    raise SystemExit(1)
if not hasattr(os, "O_NOFOLLOW"):
    raise SystemExit(1)
flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
parent_fd = os.open(parent, flags)
try:
    opened_parent = os.fstat(parent_fd)
    if (opened_parent.st_dev, opened_parent.st_ino) != (parent_info.st_dev, parent_info.st_ino):
        raise OSError("record parent identity changed")
    if not stat.S_ISDIR(opened_parent.st_mode) or opened_parent.st_uid != os.getuid():
        raise OSError("record parent ownership changed")
    if stat.S_IMODE(opened_parent.st_mode) & 0o022:
        raise OSError("record parent mode changed")

    target_name = target.name
    temporary_name = f".rehearsal-record.{os.getpid()}.tmp"
    try:
        os.stat(target_name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        pass
    else:
        raise OSError("record target exists")

    write_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    fd = os.open(temporary_name, write_flags, 0o600, dir_fd=parent_fd)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        temporary_info = os.stat(
            temporary_name, dir_fd=parent_fd, follow_symlinks=False
        )
        if not stat.S_ISREG(temporary_info.st_mode) or temporary_info.st_uid != os.getuid():
            raise OSError("temporary record identity drift")
        if stat.S_IMODE(temporary_info.st_mode) != 0o600:
            raise OSError("temporary record mode drift")
        try:
            os.stat(target_name, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise OSError("record target appeared")
        current_parent = os.stat(parent, follow_symlinks=False)
        if (current_parent.st_dev, current_parent.st_ino) != (
            opened_parent.st_dev,
            opened_parent.st_ino,
        ):
            raise OSError("record parent path changed")
        os.replace(
            temporary_name,
            target_name,
            src_dir_fd=parent_fd,
            dst_dir_fd=parent_fd,
        )
        os.fsync(parent_fd)
    except BaseException:
        try:
            info = os.stat(temporary_name, dir_fd=parent_fd, follow_symlinks=False)
            if stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid():
                os.unlink(temporary_name, dir_fd=parent_fd)
        except FileNotFoundError:
            pass
        raise
    target_info = os.stat(target_name, dir_fd=parent_fd, follow_symlinks=False)
    if not stat.S_ISREG(target_info.st_mode) or target_info.st_uid != os.getuid():
        raise OSError("record target identity drift")
    if stat.S_IMODE(target_info.st_mode) != 0o600:
        raise OSError("record target mode drift")
finally:
    os.close(parent_fd)
PY
    dre_fail 40 record-publication-failed
    return
  }
}

dre_operation_bounded() {
  local requested="$1"
  shift
  local remaining limit
  remaining=$(( ${DRE_OPERATION_DEADLINE:-$((SECONDS + DRE_TOTAL_TIMEOUT_SECONDS - DRE_CLEANUP_RESERVE_SECONDS))} - SECONDS ))
  (( remaining > 0 )) || return 124
  limit="$requested"
  (( limit <= remaining )) || limit="$remaining"
  command timeout --foreground --signal=KILL "${limit}s" "$@"
}

dre_cleanup_bounded() {
  local requested="$1"
  shift
  local remaining limit
  remaining=$(( ${DRE_RUN_DEADLINE:-$((SECONDS + DRE_TOTAL_TIMEOUT_SECONDS))} - SECONDS ))
  (( remaining > 0 )) || return 124
  limit="$requested"
  (( limit <= remaining )) || limit="$remaining"
  command timeout --foreground --signal=KILL "${limit}s" "$@"
}

dre_timeout() {
  dre_operation_bounded "$@"
}

dre_compose() {
  local project="$1"
  shift
  assert_owned_project_names || return
  [[ "$project" == "$BASELINE_PROJECT" || "$project" == "$CANARY_PROJECT" ]] || {
    dre_fail 10 compose-project-not-owned
    return
  }
  dre_timeout 30 docker compose --project-name "$project" \
    --file "$DRE_COMPOSE_PATH" --file "$DRE_OVERRIDE_PATH" "$@"
}

dre_owned_container_id() {
  dre_query_owned_container_id "$1" dre_operation_bounded 30
}

dre_owned_container_id_cleanup() {
  dre_query_owned_container_id "$1" dre_cleanup_bounded 50
}

dre_query_owned_container_id() {
  local project="$1"
  local bounded="$2"
  local failure_class="$3"
  local output all_output role
  [[ "$project" == "${BASELINE_PROJECT:-}" || "$project" == "${CANARY_PROJECT:-}" ]] || {
    dre_fail 10 container-query-project-not-owned
    return
  }
  role=baseline
  [[ "$project" == *-canary ]] && role=canary
  all_output="$("$bounded" 8 docker ps --all --quiet \
    --filter "label=com.docker.compose.project=$project")" || {
    dre_fail "$failure_class" container-query-failed
    return
  }
  output="$("$bounded" 8 docker ps --all --quiet \
    --filter "label=org.hyhome.delivery.owner=$DRE_OWNER_LABEL" \
    --filter "label=org.hyhome.delivery.task-id=$TASK_ID" \
    --filter "label=org.hyhome.delivery.role=$role" \
    --filter "label=com.docker.compose.project=$project")" || {
    dre_fail "$failure_class" container-query-failed
    return
  }
  [[ "$all_output" == "$output" ]] || {
    dre_fail "$failure_class" container-query-ownership-ambiguous
    return
  }
  if [[ -n "$output" && "$output" == *$'\n'* ]]; then
    dre_fail "$failure_class" container-query-ambiguous
    return
  fi
  printf '%s' "$output"
}

dre_cleanup_one_project() {
  local project="$1"
  local all_containers owned_containers all_networks owned_networks volumes role
  role=baseline
  [[ "$project" == *-canary ]] && role=canary

  all_containers="$(dre_cleanup_bounded 8 docker ps --all --quiet \
    --filter "label=com.docker.compose.project=$project")" || {
    dre_fail 60 cleanup-container-query-failed
    return
  }
  owned_containers="$(dre_cleanup_bounded 8 docker ps --all --quiet \
    --filter "label=com.docker.compose.project=$project" \
    --filter "label=org.hyhome.delivery.owner=$DRE_OWNER_LABEL" \
    --filter "label=org.hyhome.delivery.task-id=$TASK_ID" \
    --filter "label=org.hyhome.delivery.role=$role")" || {
    dre_fail 60 cleanup-owned-container-query-failed
    return
  }
  all_networks="$(dre_cleanup_bounded 8 docker network ls --quiet \
    --filter "label=com.docker.compose.project=$project")" || {
    dre_fail 60 cleanup-network-query-failed
    return
  }
  owned_networks="$(dre_cleanup_bounded 8 docker network ls --quiet \
    --filter "label=com.docker.compose.project=$project" \
    --filter "label=org.hyhome.delivery.owner=$DRE_OWNER_LABEL" \
    --filter "label=org.hyhome.delivery.task-id=$TASK_ID" \
    --filter "label=org.hyhome.delivery.role=$role")" || {
    dre_fail 60 cleanup-owned-network-query-failed
    return
  }
  volumes="$(dre_cleanup_bounded 8 docker volume ls --quiet \
    --filter "label=com.docker.compose.project=$project")" || {
    dre_fail 60 cleanup-volume-query-failed
    return
  }
  [[ "$all_containers" == "$owned_containers" && "$all_networks" == "$owned_networks" && -z "$volumes" ]] || {
    dre_fail 60 cleanup-ownership-ambiguous
    return
  }
  [[ "$owned_containers" != *$'\n'* && "$owned_networks" != *$'\n'* ]] || {
    dre_fail 60 cleanup-resource-cardinality-invalid
    return
  }
  if [[ -z "$owned_containers" && -z "$owned_networks" ]]; then
    return 0
  fi
  if [[ -n "$owned_containers" ]]; then
    dre_cleanup_bounded 8 docker rm --force "$owned_containers" || {
      dre_fail 60 cleanup-container-remove-failed
      return
    }
  fi
  if [[ -n "$owned_networks" ]]; then
    dre_cleanup_bounded 8 docker network rm "$owned_networks" || {
      dre_fail 60 cleanup-network-remove-failed
      return
    }
  fi
}

dre_discover_owned_project_pair() {
  local container_lines network_lines lines line project role
  BASELINE_PROJECT=""
  CANARY_PROJECT=""
  container_lines="$(dre_cleanup_bounded 8 docker ps --all \
    --filter "label=org.hyhome.delivery.owner=$DRE_OWNER_LABEL" \
    --filter "label=org.hyhome.delivery.task-id=$TASK_ID" \
    --format '{{.Label "com.docker.compose.project"}}|{{.Label "org.hyhome.delivery.role"}}')" || {
    dre_fail 60 cleanup-discovery-container-query-failed
    return
  }
  network_lines="$(dre_cleanup_bounded 8 docker network ls \
    --filter "label=org.hyhome.delivery.owner=$DRE_OWNER_LABEL" \
    --filter "label=org.hyhome.delivery.task-id=$TASK_ID" \
    --format '{{.Label "com.docker.compose.project"}}|{{.Label "org.hyhome.delivery.role"}}')" || {
    dre_fail 60 cleanup-discovery-network-query-failed
    return
  }
  lines="$container_lines"
  if [[ -n "$network_lines" ]]; then
    lines+=$'\n'
    lines+="$network_lines"
  fi
  while IFS= read -r line; do
    [[ -n "$line" ]] || continue
    project="${line%%|*}"
    role="${line#*|}"
    case "$role" in
      baseline)
        [[ -z "$BASELINE_PROJECT" || "$BASELINE_PROJECT" == "$project" ]] || {
          dre_fail 60 cleanup-discovery-baseline-ambiguous
          return
        }
        BASELINE_PROJECT="$project"
        ;;
      canary)
        [[ -z "$CANARY_PROJECT" || "$CANARY_PROJECT" == "$project" ]] || {
          dre_fail 60 cleanup-discovery-canary-ambiguous
          return
        }
        CANARY_PROJECT="$project"
        ;;
      *)
        dre_fail 60 cleanup-discovery-role-invalid
        return
        ;;
    esac
  done <<<"$lines"

  if [[ -z "$BASELINE_PROJECT" && -z "$CANARY_PROJECT" ]]; then
    return 1
  fi
  [[ -n "$BASELINE_PROJECT" && -n "$CANARY_PROJECT" ]] || {
    dre_fail 60 cleanup-discovery-pair-incomplete
    return
  }
  assert_owned_project_names || {
    dre_fail 60 cleanup-discovery-pair-invalid
    return
  }
}

dre_reject_direct_test_controls() {
  local name
  while IFS= read -r name; do
    case "$name" in
      DRE_TEST_*|DRE_SOURCE_TEST_BOUNDARY|REHEARSAL_RECORD_PATH)
        dre_fail 10 direct-test-control-rejected
        return
        ;;
    esac
  done < <(compgen -e)
}

dre_resolve_cli_path() {
  local raw="$1"
  [[ "$raw" != /* && "$raw" != *..* ]] || return 1
  local resolved
  resolved="$(command realpath -m -- "$DRE_ROOT/$raw")" || return 1
  [[ "$resolved" == "$DRE_ROOT/"* ]] || return 1
  printf '%s' "$resolved"
}

dre_parse_options() {
  TASK_ID=""
  BASELINE_VERDICT_PATH=""
  CANDIDATE_VERDICT_PATH=""
  FAILURE_MODE=none
  case "$SUBCOMMAND" in
    preflight)
      [[ "$#" -eq 7 && "$2" == --task-id && "$4" == --baseline-verdict && "$6" == --candidate-verdict ]] || return 2
      TASK_ID="$3"
      BASELINE_VERDICT_PATH="$(dre_resolve_cli_path "$5")" || return 2
      CANDIDATE_VERDICT_PATH="$(dre_resolve_cli_path "$7")" || return 2
      [[ "$BASELINE_VERDICT_PATH" == "$DRE_FIXTURE_BASELINE_PATH" && "$CANDIDATE_VERDICT_PATH" == "$DRE_FIXTURE_CANDIDATE_PATH" ]] || return 2
      ;;
    rehearse)
      [[ "$#" -eq 9 && "$2" == --task-id && "$4" == --baseline-verdict && "$6" == --candidate-verdict && "$8" == --failure-mode ]] || return 2
      TASK_ID="$3"
      BASELINE_VERDICT_PATH="$(dre_resolve_cli_path "$5")" || return 2
      CANDIDATE_VERDICT_PATH="$(dre_resolve_cli_path "$7")" || return 2
      FAILURE_MODE="$9"
      [[ "$BASELINE_VERDICT_PATH" == "$DRE_REAL_BASELINE_PATH" && "$CANDIDATE_VERDICT_PATH" == "$DRE_REAL_CANDIDATE_PATH" ]] || return 2
      [[ "$FAILURE_MODE" == none || "$FAILURE_MODE" == canary-health-timeout ]] || return 2
      ;;
    cleanup)
      [[ "$#" -eq 3 && "$2" == --task-id ]] || return 2
      TASK_ID="$3"
      ;;
  esac
  [[ "$TASK_ID" =~ ^[a-z0-9-]+$ ]] || return 2
}

dre_prepare_identity() {
  BASELINE_PROJECT="hyhome-dre-20260719-$$-baseline"
  CANARY_PROJECT="hyhome-dre-20260719-$$-canary"
  assert_ports_and_owned_project_names
}

assert_loopback_ports_available() {
  dre_python_json "$DRE_BASELINE_PORT" "$DRE_CANARY_PORT" <<'PY' || {
from pathlib import Path
import sys

required = {int(raw_port) for raw_port in sys.argv[1:]}
listening = set()
for table in (Path("/proc/net/tcp"), Path("/proc/net/tcp6")):
    try:
        rows = table.read_text(encoding="ascii").splitlines()[1:]
    except OSError:
        raise SystemExit(1)
    for row in rows:
        fields = row.split()
        if len(fields) < 4 or fields[3] != "0A":
            continue
        try:
            listening.add(int(fields[1].rsplit(":", 1)[1], 16))
        except (IndexError, ValueError):
            raise SystemExit(1)
if required & listening:
    raise SystemExit(1)
PY
    dre_fail 10 loopback-port-unavailable
    return
  }
}

dre_preflight() {
  load_and_validate_verdict baseline "$BASELINE_VERDICT_PATH" || return
  load_and_validate_verdict candidate "$CANDIDATE_VERDICT_PATH" || return
  assert_distinct_subjects_and_same_revision || return
  validate_readiness_verdict "$DRE_READINESS_PATH" || return
  validate_recovery_boundary "$DRE_RECOVERY_PATH" || return
  validate_compose_contract "$DRE_COMPOSE_PATH" "$DRE_OVERRIDE_PATH" || return
  dre_prepare_identity || return
  assert_loopback_ports_available || return
  printf 'status=passed evidence=fixture-contract-only source_revision=%s readiness=passed recovery_boundary=passed compose=passed ports=18080,18081\n' "$SOURCE_REVISION"
}

dre_cleanup_preserving_status() {
  local status="$1"
  if ! cleanup_owned_projects; then
    return 60
  fi
  return "$status"
}

dre_on_signal() {
  exit 60
}

dre_on_exit() {
  local status=$?
  trap - EXIT INT TERM HUP
  if [[ "${DRE_RUNTIME_ACTIVE:-false}" == true && "${CLEANUP_COMPLETE:-false}" != true ]] && \
    [[ "${BASELINE_START_ATTEMPTED:-false}" == true || "${CANARY_START_ATTEMPTED:-false}" == true || \
       "${BASELINE_STARTED:-false}" == true || "${CANARY_STARTED:-false}" == true ]]; then
    cleanup_owned_projects || status=60
  fi
  exit "$status"
}

dre_rehearse() {
  local status
  load_and_validate_verdict baseline "$BASELINE_VERDICT_PATH" || return
  load_and_validate_verdict candidate "$CANDIDATE_VERDICT_PATH" || return
  assert_distinct_subjects_and_same_revision || return
  validate_readiness_verdict "$DRE_READINESS_PATH" || return
  validate_recovery_boundary "$DRE_RECOVERY_PATH" || return
  validate_compose_contract "$DRE_COMPOSE_PATH" "$DRE_OVERRIDE_PATH" || return
  dre_prepare_identity || return
  assert_loopback_ports_available || return
  prepare_canonical_record_path || return

  DRE_RUN_DEADLINE=$(( SECONDS + DRE_TOTAL_TIMEOUT_SECONDS ))
  DRE_OPERATION_DEADLINE=$(( DRE_RUN_DEADLINE - DRE_CLEANUP_RESERVE_SECONDS ))
  validate_local_image_objects || return
  CLEANUP_COMPLETE=false
  DRE_RUNTIME_ACTIVE=true
  BASELINE_START_ATTEMPTED=false
  BASELINE_STARTED=false
  CANARY_START_ATTEMPTED=false
  CANARY_STARTED=false
  PROMOTION_GATES_COMPLETE=false
  PROMOTION_DECISION=not_run
  ROLLBACK_DECISION=not_run
  POST_ROLLBACK_HEALTH=not_run
  trap dre_on_exit EXIT
  trap dre_on_signal INT TERM HUP

  start_baseline
  status=$?
  if (( status != 0 )); then
    dre_cleanup_preserving_status "$status"
    return
  fi
  wait_container_and_http_health "$BASELINE_PROJECT" "$DRE_BASELINE_PORT" "$DRE_OPERATION_DEADLINE" 20
  status=$?
  if (( status != 0 )); then
    dre_cleanup_preserving_status "$status"
    return
  fi
  start_canary
  status=$?
  if (( status != 0 )); then
    if ! rollback_to_baseline_digest || ! verify_post_rollback_health; then
      dre_cleanup_preserving_status 50
      return
    fi
    dre_cleanup_preserving_status "$status"
    return
  fi
  inject_canary_timeout_when_requested
  status=$?
  if (( status == 0 )); then
    wait_container_and_http_health "$CANARY_PROJECT" "$DRE_CANARY_PORT" "$DRE_OPERATION_DEADLINE" 30
    status=$?
  fi
  if (( status != 0 )); then
    if ! rollback_to_baseline_digest || ! verify_post_rollback_health; then
      dre_cleanup_preserving_status 50
      return
    fi
    if ! cleanup_owned_projects; then
      return 60
    fi
    write_rehearsal_record || return 40
    return 30
  fi
  PROMOTION_GATES_COMPLETE=true
  record_promotion_decision || return
  cleanup_owned_projects || return 60
  write_rehearsal_record || return 40
  DRE_RUNTIME_ACTIVE=false
  return 0
}

dre_cleanup_command() {
  local status
  DRE_RUN_DEADLINE=$(( SECONDS + DRE_TOTAL_TIMEOUT_SECONDS ))
  DRE_OPERATION_DEADLINE=$(( DRE_RUN_DEADLINE - DRE_CLEANUP_RESERVE_SECONDS ))
  CLEANUP_COMPLETE=false
  dre_discover_owned_project_pair
  status=$?
  if (( status != 0 )); then
    if (( status == 1 )); then
      dre_fail 60 cleanup-discovery-pair-absent
      return
    fi
    return 60
  fi
  cleanup_owned_projects
}

main() {
  dre_reject_direct_test_controls || return
  parse_subcommand "${1:-}" || {
    dre_fail 2 usage
    return
  }
  dre_parse_options "$@" || {
    dre_fail 2 usage
    return
  }
  case "$SUBCOMMAND" in
    preflight) dre_preflight ;;
    rehearse) dre_rehearse ;;
    cleanup) dre_cleanup_command ;;
  esac
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
elif [[ "${DRE_SOURCE_TEST_BOUNDARY:-}" != 1 ]]; then
  dre_fail 10 source-boundary-rejected
  return 10
fi
