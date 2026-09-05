#!/usr/bin/env bash

# Library for check-compose-core-readiness.sh. Sourcing this file must not mutate
# Docker state or create files.

# shellcheck disable=SC2034 # Constants and parse results are consumed by the wrapper.

CRR_EXIT_USAGE=2
CRR_EXIT_PREFLIGHT=10
CRR_EXIT_STARTUP=20
CRR_EXIT_READINESS=30
CRR_EXIT_RECOVERY=40
CRR_EXIT_CLEANUP=50

CRR_PROJECT_PREFIX="hyhome-crr-20260719-"
CRR_OWNER_LABEL="task-2026-07-19-compose-runtime-readiness-remediation"
CRR_PRODUCER_SPEC="spec:124-compose-runtime-readiness-remediation"
CRR_PRODUCER_TASK="task:2026-07-19-compose-runtime-readiness-remediation"
CRR_APPROVAL_REF="task:2026-07-19-compose-runtime-readiness-remediation#approval-2026-07-19"
CRR_TARGET_CLASS="local-linked-worktree-docker-engine"
CRR_EXPECTED_SERVICES=(keycloak oauth2-proxy traefik vault vault-agent)
CRR_EXPECTED_PORTS=(18000 18443 18082 18083 18200)
CRR_EXPECTED_IMAGE_IDENTITIES=(
  "quay.io/keycloak/keycloak@sha256:0aae0de7fca85525f727d3354df17896092de8bb26ae4c12d89c77e5df8cbce4|quay.io/keycloak/keycloak@sha256:0aae0de7fca85525f727d3354df17896092de8bb26ae4c12d89c77e5df8cbce4|sha256:0aae0de7fca85525f727d3354df17896092de8bb26ae4c12d89c77e5df8cbce4|sha256:1361d6e492058a69d979ab735cfc19e73e5f1e0a707e8fa5cfb610c00bc3cff2"
  "quay.io/oauth2-proxy/oauth2-proxy@sha256:10a1165743a192e1940b4708fb9647027185ce11a681a1c5519b442ff7f1f561|quay.io/oauth2-proxy/oauth2-proxy@sha256:10a1165743a192e1940b4708fb9647027185ce11a681a1c5519b442ff7f1f561|sha256:10a1165743a192e1940b4708fb9647027185ce11a681a1c5519b442ff7f1f561|sha256:cf3a5d50849b1799260d6aca62367c333b33472f208cbbdaab243a831b1a622f"
  "traefik@sha256:21a3d83696379bac6434bb32e1dde0aff0e84ef2abd053ed3db87d3f45e749b2|traefik@sha256:21a3d83696379bac6434bb32e1dde0aff0e84ef2abd053ed3db87d3f45e749b2|sha256:21a3d83696379bac6434bb32e1dde0aff0e84ef2abd053ed3db87d3f45e749b2|sha256:7982c57cc89de38c6ca9e3f17caa0569890d2043f6f5271c78ad75a2cff50f32"
  "hashicorp/vault@sha256:a296a888b118615dc01d5f1a6846e6d4a7277946caaed5b447008fff5fe06b54|hashicorp/vault@sha256:a296a888b118615dc01d5f1a6846e6d4a7277946caaed5b447008fff5fe06b54|sha256:a296a888b118615dc01d5f1a6846e6d4a7277946caaed5b447008fff5fe06b54|sha256:1747a4ab1e1bea8938269b23827165c5d80eecbdb5c115fd58e6380569537c84"
)

crr_error() {
  printf 'compose-core-readiness: %s\n' "$*" >&2
}

crr_fail() {
  local code="$1"
  shift
  crr_error "$*"
  return "$code"
}

is_owned_project_name() {
  [[ "${1-}" =~ ^hyhome-crr-20260719-[0-9]+-[a-z0-9]{8}$ ]]
}

allocate_runtime_identity() {
  local attempt candidate project_suffix runtime_dir
  runtime_dir=""
  for attempt in 1 2 3 4 5; do
    candidate="$(mktemp -d "/tmp/${CRR_PROJECT_PREFIX}$$-XXXXXXXX")" ||
      break
    project_suffix="${candidate##*-}"
    project_suffix="${project_suffix,,}"
    runtime_dir="/tmp/${CRR_PROJECT_PREFIX}$$-${project_suffix}"
    if mkdir -m 700 -- "$runtime_dir" 2>/dev/null; then
      rmdir -- "$candidate"
      break
    fi
    rmdir -- "$candidate"
    runtime_dir=""
  done
  [ -n "$runtime_dir" ] || {
    crr_fail "$CRR_EXIT_PREFLIGHT" "collision-resistant runtime allocation failed"
    return
  }
  CRR_RUNTIME_DIR="$runtime_dir"
  CRR_PROJECT_NAME="${runtime_dir#/tmp/}"
  if ! is_owned_project_name "$CRR_PROJECT_NAME"; then
    rm -rf -- "$runtime_dir"
    crr_fail "$CRR_EXIT_PREFLIGHT" "allocated project identity is outside ownership"
    return
  fi
  export CRR_RUNTIME_DIR CRR_PROJECT_NAME
}

parse_args() {
  CRR_MODE=""
  CRR_REQUESTED_PROJECT=""

  case "${1-}" in
  --preflight)
    [ "$#" -eq 1 ] || return "$CRR_EXIT_USAGE"
    CRR_MODE="preflight"
    ;;
  --scenario)
    [ "$#" -eq 2 ] || return "$CRR_EXIT_USAGE"
    case "$2" in
    startup-readiness | vault-restart-recovery | negative-timeout)
      CRR_MODE="$2"
      ;;
    *)
      return "$CRR_EXIT_USAGE"
      ;;
    esac
    ;;
  --cleanup-only)
    [ "$#" -eq 3 ] && [ "$2" = "--project-name" ] ||
      return "$CRR_EXIT_USAGE"
    is_owned_project_name "$3" ||
      return "$CRR_EXIT_PREFLIGHT"
    CRR_MODE="cleanup-only"
    CRR_REQUESTED_PROJECT="$3"
    ;;
  *)
    return "$CRR_EXIT_USAGE"
    ;;
  esac
}

assert_linked_worktree() {
  local root git_dir
  root="$(git rev-parse --show-toplevel 2>/dev/null)" ||
    crr_fail "$CRR_EXIT_PREFLIGHT" "not inside a Git worktree"
  git_dir="$(git rev-parse --git-dir 2>/dev/null)" ||
    crr_fail "$CRR_EXIT_PREFLIGHT" "cannot resolve Git metadata"
  git_dir="$(cd "$git_dir" && pwd -P)"

  case "$git_dir" in
  */.git/worktrees/*) ;;
  *)
    crr_fail "$CRR_EXIT_PREFLIGHT" \
      "runtime rehearsal requires a linked worktree"
    return
    ;;
  esac

  CRR_ROOT="$root"
}

assert_docker_compose() {
  command -v docker >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_PREFLIGHT" "docker CLI is unavailable"
  docker compose version >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_PREFLIGHT" "Docker Compose v2 is unavailable"
  command -v jq >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_PREFLIGHT" "jq is unavailable"
  command -v python3 >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_PREFLIGHT" "python3 is unavailable"
  command -v curl >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_PREFLIGHT" "curl is unavailable"
  command -v openssl >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_PREFLIGHT" "openssl is unavailable"
  command -v realpath >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_PREFLIGHT" "realpath is unavailable"
  command -v timeout >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_PREFLIGHT" "timeout is unavailable"
}

assert_docker_daemon() {
  docker info >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_PREFLIGHT" "Docker daemon is unavailable"
}

observe_docker_image_config_digest() {
  local image_ref="$1"
  local archive config_digest status=0
  archive="$(mktemp "${CRR_RUNTIME_DIR}/image-config.XXXXXX.tar")" ||
    return "$CRR_EXIT_PREFLIGHT"
  chmod 600 "$archive" || status="$CRR_EXIT_PREFLIGHT"
  if [ "$status" -eq 0 ]; then
    timeout --signal=KILL 60s docker image save \
      --output "$archive" "$image_ref" >/dev/null 2>&1 ||
      status="$CRR_EXIT_PREFLIGHT"
  fi
  if [ "$status" -eq 0 ]; then
    config_digest="$(
      python3 "${CRR_ROOT}/scripts/validation/check-supply-chain-policy.py" \
        --docker-save-config-digest "$archive"
    )" || status="$CRR_EXIT_PREFLIGHT"
  fi
  rm -f -- "$archive" || status="$CRR_EXIT_PREFLIGHT"
  [ "$status" -eq 0 ] || return "$status"
  printf '%s\n' "$config_digest"
}

assert_local_image_identity() {
  local image_ref="$1"
  local expected_repo_digest="$2"
  local expected_target_digest="$3"
  local expected_config_id="$4"
  local observed actual_config_id
  if ! observed="$(
    docker image inspect --format '{{json .}}' \
      "$image_ref" 2>/dev/null
  )"; then
    crr_fail "$CRR_EXIT_PREFLIGHT" \
      "local image identity is unavailable for ${image_ref}"
    return
  fi
  if ! python3 - "$observed" "$expected_repo_digest" \
    "$expected_target_digest" "$expected_config_id" <<'PY'
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
if (
    not isinstance(repo_digests, list)
    or expected_repo not in repo_digests
    or not re.fullmatch(r"sha256:[0-9a-f]{64}", expected_target)
    or not re.fullmatch(r"sha256:[0-9a-f]{64}", expected_config)
    or expected_target == expected_config
    or not isinstance(descriptor, dict)
    or descriptor.get("digest") != expected_target
    or descriptor.get("mediaType") not in media_types
    or target_id not in (expected_target, expected_config)
):
    raise SystemExit(1)
PY
  then
    crr_fail "$CRR_EXIT_PREFLIGHT" \
      "local repository manifest or target descriptor mismatch for ${image_ref}"
    return
  fi
  actual_config_id="$(observe_docker_image_config_digest "$image_ref")" || {
    crr_fail "$CRR_EXIT_PREFLIGHT" \
      "local image configuration body is unavailable for ${image_ref}"
    return
  }
  if [ "$actual_config_id" != "$expected_config_id" ]; then
    crr_fail "$CRR_EXIT_PREFLIGHT" \
      "local image configuration ID mismatch for ${image_ref}"
    return
  fi
}

assert_local_image_identities() {
  local identity image_ref expected_repo_digest expected_target_digest
  local expected_config_id
  for identity in "${CRR_EXPECTED_IMAGE_IDENTITIES[@]}"; do
    IFS='|' read -r image_ref expected_repo_digest expected_target_digest \
      expected_config_id <<<"$identity"
    assert_local_image_identity \
      "$image_ref" "$expected_repo_digest" "$expected_target_digest" \
      "$expected_config_id" || return
  done
}

assert_target_capacity() {
  local capacity cpu_count memory_bytes docker_root available_kib
  if ! capacity="$(docker info --format '{{.NCPU}} {{.MemTotal}} {{.DockerRootDir}}' 2>/dev/null)"; then
    crr_fail "$CRR_EXIT_PREFLIGHT" "target capacity cannot be observed"
    return
  fi
  read -r cpu_count memory_bytes docker_root <<<"$capacity"
  if ! [[ "$cpu_count" =~ ^[0-9]+$ ]] ||
    ! [[ "$memory_bytes" =~ ^[0-9]+$ ]] ||
    [ -z "$docker_root" ]; then
    crr_fail "$CRR_EXIT_PREFLIGHT" "target capacity response is invalid"
    return
  fi
  if ! available_kib="$(df -Pk -- "$docker_root" 2>/dev/null | awk 'NR == 2 {print $4}')" ||
    ! [[ "$available_kib" =~ ^[0-9]+$ ]]; then
    crr_fail "$CRR_EXIT_PREFLIGHT" "target capacity storage cannot be observed"
    return
  fi
  if [ "$cpu_count" -lt 4 ] ||
    [ "$memory_bytes" -lt 4294967296 ] ||
    [ "$available_kib" -lt 8388608 ]; then
    crr_fail "$CRR_EXIT_PREFLIGHT" \
      "target capacity is below 4 CPUs, 4 GiB memory, or 8 GiB storage"
    return
  fi
}

assert_owned_path_boundary() {
  local path="$1"
  local boundary="$2"
  local label="$3"
  local cursor resolved_path resolved_boundary

  case "$path" in
  "$boundary" | "$boundary"/*) ;;
  *)
    crr_fail "$CRR_EXIT_PREFLIGHT" "${label} path is outside its owned boundary"
    return
    ;;
  esac

  cursor="$path"
  while :; do
    if [ -L "$cursor" ]; then
      crr_fail "$CRR_EXIT_PREFLIGHT" "${label} path contains a symbolic link"
      return
    fi
    [ "$cursor" = "$boundary" ] && break
    cursor="$(dirname "$cursor")"
  done

  resolved_path="$(realpath -m -- "$path")" ||
    return "$CRR_EXIT_PREFLIGHT"
  resolved_boundary="$(realpath -m -- "$boundary")" ||
    return "$CRR_EXIT_PREFLIGHT"
  case "$resolved_path" in
  "$resolved_boundary" | "$resolved_boundary"/*) ;;
  *)
    crr_fail "$CRR_EXIT_PREFLIGHT" "${label} path resolves outside its owned boundary"
    return
    ;;
  esac
}

prepare_owned_paths() {
  : "${CRR_ROOT:?CRR_ROOT is required}"
  : "${CRR_PROJECT_NAME:?CRR_PROJECT_NAME is required}"
  is_owned_project_name "$CRR_PROJECT_NAME" ||
    crr_fail "$CRR_EXIT_PREFLIGHT" "project identity is outside the owned prefix"

  CRR_TASK_ROOT="${CRR_ROOT}/_workspace/repo-support/task-2026-07-19-compose-runtime-readiness-remediation"
  CRR_EVIDENCE_DIR="${CRR_TASK_ROOT}/compose"
  local expected_runtime_dir="/tmp/${CRR_PROJECT_NAME}"
  CRR_RUNTIME_DIR="${CRR_RUNTIME_DIR:-$expected_runtime_dir}"
  [ "$CRR_RUNTIME_DIR" = "$expected_runtime_dir" ] || {
    crr_fail "$CRR_EXIT_PREFLIGHT" "runtime identity and path disagree"
    return
  }
  CRR_SECRET_DIR="${CRR_RUNTIME_DIR}/secrets"
  CRR_CONFIG_DIR="${CRR_RUNTIME_DIR}/config"
  CRR_RENDERED_MODEL="${CRR_RUNTIME_DIR}/rendered-core-model.json"
  CRR_RAW_MODEL="${CRR_RUNTIME_DIR}/rendered-root-model.json"
  CRR_SERVICES_JSON="${CRR_RUNTIME_DIR}/services.json"
  CRR_ENDPOINTS_JSON="${CRR_RUNTIME_DIR}/endpoints.json"
  CRR_VERDICT_PATH="${CRR_EVIDENCE_DIR}/readiness-verdict.json"
  CRR_NETWORK_NAME="${CRR_PROJECT_NAME}_crr_net"

  assert_owned_path_boundary "$CRR_TASK_ROOT" "$CRR_ROOT" "task" || return
  assert_owned_path_boundary "$CRR_EVIDENCE_DIR" "$CRR_TASK_ROOT" "evidence" || return
  assert_owned_path_boundary "$CRR_RUNTIME_DIR" /tmp "runtime" || return
  assert_owned_path_boundary "$CRR_SECRET_DIR" "$CRR_RUNTIME_DIR" "secret" || return
  assert_owned_path_boundary "$CRR_CONFIG_DIR" "$CRR_RUNTIME_DIR" "config" || return

  umask 077
  mkdir -p "$CRR_EVIDENCE_DIR" "$CRR_SECRET_DIR" "$CRR_CONFIG_DIR"
  assert_owned_path_boundary "$CRR_EVIDENCE_DIR" "$CRR_TASK_ROOT" "evidence" || return
  assert_owned_path_boundary "$CRR_SECRET_DIR" "$CRR_RUNTIME_DIR" "secret" || return
  assert_owned_path_boundary "$CRR_CONFIG_DIR" "$CRR_RUNTIME_DIR" "config" || return
  chmod 700 "$CRR_RUNTIME_DIR" "$CRR_SECRET_DIR" "$CRR_CONFIG_DIR"
  export CRR_SECRET_DIR CRR_CONFIG_DIR CRR_NETWORK_NAME
}

prepare_synthetic_secrets() {
  : "${CRR_SECRET_DIR:?CRR_SECRET_DIR is required}"
  : "${CRR_CONFIG_DIR:?CRR_CONFIG_DIR is required}"

  umask 077
  rm -f -- \
    "${CRR_SECRET_DIR}/keycloak_admin_password" \
    "${CRR_SECRET_DIR}/oauth2_proxy_client_secret" \
    "${CRR_SECRET_DIR}/oauth2_proxy_cookie_secret" \
    "${CRR_SECRET_DIR}/vault_agent_role_id" \
    "${CRR_SECRET_DIR}/vault_agent_secret_id" \
    "${CRR_SECRET_DIR}/vault_unseal_key" \
    "${CRR_SECRET_DIR}/vault_root_token"
  rm -f -- \
    "${CRR_CONFIG_DIR}/vault-readiness.hcl" \
    "${CRR_CONFIG_DIR}/vault-agent-readiness.hcl" \
    "${CRR_CONFIG_DIR}/traefik-readiness.yml"
  openssl rand -hex 24 >"${CRR_SECRET_DIR}/keycloak_admin_password"
  openssl rand -hex 24 >"${CRR_SECRET_DIR}/oauth2_proxy_client_secret"
  openssl rand -hex 16 | tr -d '\n' >"${CRR_SECRET_DIR}/oauth2_proxy_cookie_secret"

  cat >"${CRR_CONFIG_DIR}/vault-readiness.hcl" <<'EOF'
disable_mlock = true
ui = false
api_addr = "http://vault:8200"

storage "file" {
  path = "/vault/file"
}

listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = true
}
EOF

  cat >"${CRR_CONFIG_DIR}/traefik-readiness.yml" <<'EOF'
http:
  routers:
    crr-oauth2:
      entryPoints:
        - web
      rule: "Path(`/ping`)"
      service: crr-oauth2
  services:
    crr-oauth2:
      loadBalancer:
        servers:
          - url: http://oauth2-proxy:4180
EOF

  cat >"${CRR_CONFIG_DIR}/vault-agent-readiness.hcl" <<'EOF'
pid_file = "/tmp/vault-agent.pid"

vault {
  address = "http://vault:8200"
}

auto_auth {
  method "approle" {
    mount_path = "auth/approle"
    config = {
      role_id_file_path = "/run/secrets/vault_agent_role_id"
      secret_id_file_path = "/run/secrets/vault_agent_secret_id"
      remove_secret_id_file_after_reading = false
    }
  }
}

template {
  contents = "{{ with secret \"secret/data/readiness\" }}{{ .Data.data.sentinel }}{{ end }}\n"
  destination = "/vault/out/readiness.sentinel"
  perms = "0644"
}
EOF

  : >"${CRR_SECRET_DIR}/vault_agent_role_id"
  : >"${CRR_SECRET_DIR}/vault_agent_secret_id"
  : >"${CRR_SECRET_DIR}/vault_unseal_key"
  : >"${CRR_SECRET_DIR}/vault_root_token"
  set_container_material_permissions
}

set_container_material_permissions() {
  chmod 0444 \
    "${CRR_SECRET_DIR}/keycloak_admin_password" \
    "${CRR_SECRET_DIR}/oauth2_proxy_client_secret" \
    "${CRR_SECRET_DIR}/oauth2_proxy_cookie_secret" \
    "${CRR_SECRET_DIR}/vault_agent_role_id" \
    "${CRR_SECRET_DIR}/vault_agent_secret_id" \
    "${CRR_SECRET_DIR}/vault_unseal_key" \
    "${CRR_SECRET_DIR}/vault_root_token"
  chmod 0644 \
    "${CRR_CONFIG_DIR}/vault-readiness.hcl" \
    "${CRR_CONFIG_DIR}/vault-agent-readiness.hcl" \
    "${CRR_CONFIG_DIR}/traefik-readiness.yml"
}

unseal_vault_from_mounted_secret() {
  # shellcheck disable=SC2016 # Expansion is intentionally in-container only.
  crr_compose exec -T vault sh -ec '
    unseal_key="$(cat /run/secrets/crr-vault-unseal-key)"
    [ -n "$unseal_key" ]
    exec vault operator unseal "$unseal_key"
  ' >/dev/null 2>&1
}

vault_exec_with_mounted_root_token() {
  # shellcheck disable=SC2016 # Expansion is intentionally in-container only.
  crr_compose exec -T vault sh -ec '
    VAULT_TOKEN="$(cat /run/secrets/crr-vault-root-token)"
    [ -n "$VAULT_TOKEN" ]
    export VAULT_TOKEN
    exec vault "$@"
  ' sh "$@"
}

crr_compose() {
  : "${CRR_ROOT:?CRR_ROOT is required}"
  : "${CRR_PROJECT_NAME:?CRR_PROJECT_NAME is required}"
  docker compose \
    --env-file "${CRR_ROOT}/tests/fixtures/compose-core-readiness/env.runtime.example" \
    -f "${CRR_ROOT}/docker-compose.yml" \
    -f "${CRR_ROOT}/tests/fixtures/compose-core-readiness/compose.core-runtime.override.yml" \
    --project-name "$CRR_PROJECT_NAME" \
    --profile core \
    "$@"
}

assert_exact_service_set() {
  local model="$1"
  python3 - "$model" <<'PY'
import json
import sys
from pathlib import Path

expected = {"keycloak", "oauth2-proxy", "traefik", "vault", "vault-agent"}
try:
    document = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError):
    print("compose-core-readiness: exact service set cannot be parsed", file=sys.stderr)
    raise SystemExit(10)
actual = set(document.get("services", {}))
if actual != expected:
    print("compose-core-readiness: exact service set mismatch", file=sys.stderr)
    raise SystemExit(10)
PY
}

assert_isolated_paths_ports_networks() {
  local model="$1"
  local root="${CRR_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
  local runtime_dir="${CRR_RUNTIME_DIR-}"
  python3 - "$model" "$root" "$runtime_dir" <<'PY'
import json
import os
import sys
from pathlib import Path

expected_services = {"keycloak", "oauth2-proxy", "traefik", "vault", "vault-agent"}
expected_ports = {"18000", "18443", "18082", "18083", "18200"}
expected_limits = {
    "keycloak": (1.0, 805306368),
    "oauth2-proxy": (0.5, 268435456),
    "traefik": (0.5, 268435456),
    "vault": (0.5, 268435456),
    "vault-agent": (0.25, 134217728),
}
expected_images = {
    "keycloak": "quay.io/keycloak/keycloak@sha256:0aae0de7fca85525f727d3354df17896092de8bb26ae4c12d89c77e5df8cbce4",
    "oauth2-proxy": "quay.io/oauth2-proxy/oauth2-proxy@sha256:10a1165743a192e1940b4708fb9647027185ce11a681a1c5519b442ff7f1f561",
    "traefik": "traefik@sha256:21a3d83696379bac6434bb32e1dde0aff0e84ef2abd053ed3db87d3f45e749b2",
    "vault": "hashicorp/vault@sha256:a296a888b118615dc01d5f1a6846e6d4a7277946caaed5b447008fff5fe06b54",
    "vault-agent": "hashicorp/vault@sha256:a296a888b118615dc01d5f1a6846e6d4a7277946caaed5b447008fff5fe06b54",
}
root = sys.argv[2]
runtime_dir = sys.argv[3]
try:
    document = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError):
    print("compose-core-readiness: isolated model cannot be parsed", file=sys.stderr)
    raise SystemExit(10)

services = document.get("services", {})
errors = []
if set(services) != expected_services:
    errors.append("service set")

ports = set()
for name, service in services.items():
    if service.get("image") != expected_images.get(name):
        errors.append(f"image identity:{name}")
    if service.get("build") is not None:
        errors.append(f"runtime build:{name}")
    if service.get("container_name") not in (None, ""):
        errors.append(f"fixed container name:{name}")
    if set((service.get("networks") or {}).keys()) != {"crr_net"}:
        errors.append(f"network scope:{name}")
    expected_cpu, expected_memory = expected_limits.get(name, (None, None))
    try:
        actual_cpu = float(service.get("cpus"))
        actual_memory = int(service.get("mem_limit"))
    except (TypeError, ValueError):
        errors.append(f"resource limit:{name}")
    else:
        if actual_cpu != expected_cpu or actual_memory != expected_memory:
            errors.append(f"resource limit:{name}")
    for port in service.get("ports") or []:
        published = str(port.get("published", ""))
        ports.add(published)
        if port.get("host_ip") != "127.0.0.1":
            errors.append(f"host binding:{name}")
    for volume in service.get("volumes") or []:
        source = str(volume.get("source", ""))
        if volume.get("type") == "bind":
            if root and source.startswith(root + "/"):
                errors.append(f"repository bind:{name}")
            target = str(volume.get("target", ""))
            if source.endswith("/docker.sock") or target.endswith("/docker.sock"):
                errors.append(f"raw docker socket:{name}")
                continue
            if not runtime_dir:
                errors.append(f"runtime bind without identity:{name}")
                continue
            try:
                resolved_source = os.path.realpath(source)
                resolved_runtime = os.path.realpath(runtime_dir)
                if os.path.commonpath([resolved_source, resolved_runtime]) != resolved_runtime:
                    errors.append(f"bind source:{name}")
            except ValueError:
                errors.append(f"bind source:{name}")
            if volume.get("read_only") is not True:
                errors.append(f"writable bind:{name}")

if ports != expected_ports:
    errors.append("published port set")
networks = document.get("networks") or {}
if set(networks) != {"crr_net"} or networks.get("crr_net", {}).get("external") is True:
    errors.append("external/shared network")

serialized = json.dumps(document, sort_keys=True)
for forbidden in ("mng-pg", "mng-valkey", "k3d-hyhome"):
    if forbidden in serialized:
        errors.append(f"forbidden reference:{forbidden}")

if errors:
    print("compose-core-readiness: isolated model rejected", file=sys.stderr)
    raise SystemExit(10)
PY
}

render_core_model() {
  crr_compose config --format json >"$CRR_RAW_MODEL" ||
    crr_fail "$CRR_EXIT_PREFLIGHT" "Compose model rendering failed"
  assert_exact_service_set "$CRR_RAW_MODEL" || return "$CRR_EXIT_PREFLIGHT"

  jq -S '{name, services, networks, volumes, secrets}' \
    "$CRR_RAW_MODEL" >"$CRR_RENDERED_MODEL" ||
    crr_fail "$CRR_EXIT_PREFLIGHT" "rendered model normalization failed"
  assert_exact_service_set "$CRR_RENDERED_MODEL" || return "$CRR_EXIT_PREFLIGHT"
  assert_isolated_paths_ports_networks "$CRR_RENDERED_MODEL" ||
    return "$CRR_EXIT_PREFLIGHT"
}

assert_redacted_file() {
  local candidate="$1"
  local secret_dir="${CRR_SECRET_DIR-}"
  [ -n "$secret_dir" ] && [ -d "$secret_dir" ] || return 0
  python3 - "$candidate" "$secret_dir" <<'PY'
import sys
from pathlib import Path

candidate = Path(sys.argv[1]).read_bytes()
for secret_path in Path(sys.argv[2]).iterdir():
    if not secret_path.is_file():
        continue
    secret = secret_path.read_bytes().strip()
    if secret and secret in candidate:
        raise SystemExit(1)
PY
}

write_readiness_verdict() {
  local output="$1"
  local project_name="$2"
  local scenario="$3"
  local overall_status="$4"
  local elapsed_seconds="$5"
  local cleanup_status="$6"
  local redaction_status="$7"
  local services_json="$8"
  local endpoints_json="$9"
  local started_at="${10}"
  local completed_at="${11}"
  local output_dir temporary recovery_status

  is_owned_project_name "$project_name" ||
    crr_fail "$CRR_EXIT_PREFLIGHT" "verdict project name is not owned"
  case "$scenario" in
  startup-readiness | vault-restart-recovery | negative-timeout) ;;
  *) return 1 ;;
  esac
  case "$overall_status" in ready | timed_out | failed | degraded) ;; *) return 1 ;; esac
  [[ "$elapsed_seconds" =~ ^[0-9]+$ ]] || return 1
  [ "$cleanup_status" = "passed" ] || [ "$cleanup_status" = "failed" ] || return 1
  [ "$redaction_status" = "passed" ] || [ "$redaction_status" = "failed" ] || return 1
  [[ "$started_at" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$ ]] || return 1
  [[ "$completed_at" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$ ]] || return 1

  recovery_status="not_applicable"
  if [ "$scenario" = "vault-restart-recovery" ]; then
    recovery_status="failed"
    [ "$overall_status" = "ready" ] && recovery_status="passed"
  fi

  output_dir="$(dirname "$output")"
  mkdir -p "$output_dir"
  temporary="$(mktemp "${output_dir}/.readiness-verdict.XXXXXX")"
  if ! jq -S -n \
    --arg producer_spec "$CRR_PRODUCER_SPEC" \
    --arg producer_task "$CRR_PRODUCER_TASK" \
    --arg approval_ref "$CRR_APPROVAL_REF" \
    --arg scenario "$scenario" \
    --arg target_class "$CRR_TARGET_CLASS" \
    --arg project_name "$project_name" \
    --arg started_at "$started_at" \
    --arg completed_at "$completed_at" \
    --arg overall_status "$overall_status" \
    --arg recovery_status "$recovery_status" \
    --argjson elapsed_seconds "$elapsed_seconds" \
    --arg cleanup_status "$cleanup_status" \
    --arg redaction_status "$redaction_status" \
    --slurpfile services "$services_json" \
    --slurpfile endpoint_verdicts "$endpoints_json" \
    '{
      schema_version: 2,
      producer_spec: $producer_spec,
      producer_task: $producer_task,
      approval_ref: $approval_ref,
      scenario: $scenario,
      target_class: $target_class,
      project_name: $project_name,
      started_at: $started_at,
      completed_at: $completed_at,
      services: $services[0],
      endpoint_verdicts: $endpoint_verdicts[0],
      observed_state: $overall_status,
      recovery_status: $recovery_status,
      teardown_status: $cleanup_status,
      overall_status: $overall_status,
      elapsed_seconds: $elapsed_seconds,
      cleanup_status: $cleanup_status,
      redaction_status: $redaction_status
    }' >"$temporary"; then
    rm -f "$temporary"
    return 1
  fi

  if ! assert_redacted_file "$temporary"; then
    rm -f "$temporary"
    crr_error "secret material rejected from readiness verdict"
    return 1
  fi
  mv "$temporary" "$output"
}

publish_canonical_readiness_handoff() {
  local scenario_verdict="$1"
  local canonical_verdict="$2"
  local temporary
  case "$scenario_verdict" in
  "${CRR_EVIDENCE_DIR}"/readiness-verdict.startup-readiness.json | \
    "${CRR_EVIDENCE_DIR}"/readiness-verdict.vault-restart-recovery.json) ;;
  *)
    crr_fail "$CRR_EXIT_READINESS" "scenario verdict is not eligible for readiness handoff"
    return
    ;;
  esac
  [ "$canonical_verdict" = "${CRR_EVIDENCE_DIR}/readiness-verdict.json" ] || {
    crr_fail "$CRR_EXIT_READINESS" "canonical readiness handoff path is invalid"
    return
  }
  temporary="$(mktemp "${CRR_EVIDENCE_DIR}/.readiness-handoff.XXXXXX")" ||
    return "$CRR_EXIT_READINESS"
  if ! jq -S . "$scenario_verdict" >"$temporary" ||
    ! assert_redacted_file "$temporary"; then
    rm -f "$temporary"
    crr_fail "$CRR_EXIT_READINESS" "canonical readiness handoff publication failed"
    return
  fi
  mv "$temporary" "$canonical_verdict"
}

list_owned_resource_ids() {
  local kind="$1"
  local project_name="$2"
  if [ "$kind" = "container" ]; then
    docker container ls -aq \
      --filter "label=com.docker.compose.project=${project_name}"
  else
    docker "$kind" ls -q \
      --filter "label=com.docker.compose.project=${project_name}"
  fi
}

assert_owned_resource_labels() {
  local project_name="$1"
  local kind id ids owner
  for kind in container network volume; do
    if ! ids="$(list_owned_resource_ids "$kind" "$project_name" 2>/dev/null)"; then
      crr_error "cleanup resource enumeration failed for ${kind}"
      return "$CRR_EXIT_CLEANUP"
    fi
    while IFS= read -r id; do
      [ -n "$id" ] || continue
      if [ "$kind" = "container" ]; then
        if ! owner="$(docker container inspect \
          --format '{{ index .Config.Labels "org.hyhome.readiness-owner" }}' \
          "$id" 2>/dev/null)"; then
          crr_error "cleanup ownership inspection failed for ${kind}"
          return "$CRR_EXIT_CLEANUP"
        fi
      elif ! owner="$(docker "$kind" inspect \
        --format '{{ index .Labels "org.hyhome.readiness-owner" }}' \
        "$id" 2>/dev/null)"; then
        crr_error "cleanup ownership inspection failed for ${kind}"
        return "$CRR_EXIT_CLEANUP"
      fi
      if [ "$owner" != "$CRR_OWNER_LABEL" ]; then
        crr_error "cleanup ownership label mismatch for ${kind}"
        return "$CRR_EXIT_CLEANUP"
      fi
    done <<<"$ids"
  done
}

cleanup_owned_project() {
  local project_name="${1:-${CRR_PROJECT_NAME-}}"
  is_owned_project_name "$project_name" ||
    crr_fail "$CRR_EXIT_CLEANUP" "cleanup project name is not owned"
  if [ "${CRR_CLEANUP_DONE:-false}" = "true" ]; then
    return 0
  fi

  if ! assert_owned_resource_labels "$project_name"; then
    return "$CRR_EXIT_CLEANUP"
  fi
  CRR_PROJECT_NAME="$project_name"
  if ! crr_compose down --volumes --remove-orphans --timeout 15 >/dev/null 2>&1; then
    crr_error "owned Compose teardown failed"
    return "$CRR_EXIT_CLEANUP"
  fi

  local kind ids
  for kind in container network volume; do
    if ! ids="$(list_owned_resource_ids "$kind" "$project_name" 2>/dev/null)"; then
      crr_error "post-teardown resource enumeration failed for ${kind}"
      return "$CRR_EXIT_CLEANUP"
    fi
    if [ -n "$ids" ]; then
      crr_fail "$CRR_EXIT_CLEANUP" "owned ${kind} remains after teardown"
      return
    fi
  done
  CRR_CLEANUP_DONE="true"
}

start_vault() {
  crr_compose up -d --pull never --no-build vault >/dev/null ||
    crr_fail "$CRR_EXIT_STARTUP" "Vault startup failed"
  wait_container_health vault "${CRR_STARTUP_TIMEOUT_SECONDS:-180}" ||
    crr_fail "$CRR_EXIT_STARTUP" "Vault initialization health timed out"
}

initialize_unseal_and_configure_synthetic_vault() {
  local init_json
  init_json="${CRR_SECRET_DIR}/vault-init.json"
  crr_compose exec -T vault vault operator init \
    -key-shares=1 -key-threshold=1 -format=json >"$init_json" 2>/dev/null ||
    crr_fail "$CRR_EXIT_STARTUP" "synthetic Vault initialization failed"
  chmod 600 "$init_json"

  chmod 0600 \
    "${CRR_SECRET_DIR}/vault_unseal_key" \
    "${CRR_SECRET_DIR}/vault_root_token"
  jq -er '.unseal_keys_b64[0]' "$init_json" \
    >"${CRR_SECRET_DIR}/vault_unseal_key" ||
    crr_fail "$CRR_EXIT_STARTUP" "synthetic Vault unseal material is incomplete"
  jq -er '.root_token' "$init_json" \
    >"${CRR_SECRET_DIR}/vault_root_token" ||
    crr_fail "$CRR_EXIT_STARTUP" "synthetic Vault root-token material is incomplete"
  set_container_material_permissions
  rm -f "$init_json"

  unseal_vault_from_mounted_secret ||
    crr_fail "$CRR_EXIT_STARTUP" "synthetic Vault unseal failed"

  vault_exec_with_mounted_root_token auth enable approle >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_STARTUP" "synthetic AppRole enable failed"
  vault_exec_with_mounted_root_token \
    secrets enable -path=secret kv-v2 >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_STARTUP" "synthetic KV enable failed"
  printf '%s\n' \
    'path "secret/data/readiness" { capabilities = ["read"] }' |
    vault_exec_with_mounted_root_token \
      policy write readiness - >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_STARTUP" "synthetic Vault policy failed"
  vault_exec_with_mounted_root_token \
    write auth/approle/role/readiness \
    token_policies=readiness token_ttl=10m token_max_ttl=30m >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_STARTUP" "synthetic AppRole configuration failed"
  vault_exec_with_mounted_root_token \
    kv put secret/readiness sentinel=ready >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_STARTUP" "synthetic readiness sentinel failed"
  chmod 0600 \
    "${CRR_SECRET_DIR}/vault_agent_role_id" \
    "${CRR_SECRET_DIR}/vault_agent_secret_id"
  vault_exec_with_mounted_root_token \
    read -field=role_id auth/approle/role/readiness/role-id \
    >"${CRR_SECRET_DIR}/vault_agent_role_id" 2>/dev/null ||
    crr_fail "$CRR_EXIT_STARTUP" "synthetic AppRole role ID failed"
  vault_exec_with_mounted_root_token \
    write -field=secret_id -f auth/approle/role/readiness/secret-id \
    >"${CRR_SECRET_DIR}/vault_agent_secret_id" 2>/dev/null ||
    crr_fail "$CRR_EXIT_STARTUP" "synthetic AppRole secret ID failed"
  set_container_material_permissions
}

prepare_vault_agent_output_volume() {
  crr_compose run --rm --no-deps --pull never --user 0:0 --cap-add CHOWN \
    --entrypoint sh vault-agent -ec \
    'chmod 0750 /vault/out && chown vault:vault /vault/out' \
    >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_STARTUP" \
      "Vault Agent output volume preparation failed"
}

start_remaining_services() {
  crr_compose up -d --pull never --no-build --wait \
    --wait-timeout "${CRR_STARTUP_TIMEOUT_SECONDS:-180}" \
    keycloak oauth2-proxy traefik vault-agent >/dev/null ||
    crr_fail "$CRR_EXIT_STARTUP" "remaining service startup failed"
}

wait_container_health() {
  local service="$1"
  local timeout_seconds="$2"
  local started now container_id state
  started="$(date +%s)"
  while :; do
    container_id="$(crr_compose ps -q "$service" 2>/dev/null || true)"
    if [ -n "$container_id" ]; then
      state="$(docker container inspect --format \
        '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' \
        "$container_id" 2>/dev/null || true)"
      [ "$state" = "healthy" ] && return 0
      [ "$state" = "exited" ] && return 1
    fi
    now="$(date +%s)"
    [ $((now - started)) -lt "$timeout_seconds" ] || return 1
    sleep 2
  done
}

probe_service_endpoint() {
  local endpoint="$1"
  local timeout_seconds="${2:-10}"
  curl --fail --silent --show-error \
    --max-time "$timeout_seconds" "$endpoint" >/dev/null 2>&1
}

collect_service_states() {
  local temporary service container_id state
  temporary="$(mktemp "${CRR_RUNTIME_DIR}/service-states.XXXXXX")"
  printf '{}\n' >"$temporary"
  for service in "${CRR_EXPECTED_SERVICES[@]}"; do
    container_id="$(crr_compose ps -q "$service" 2>/dev/null || true)"
    state="unknown"
    if [ -n "$container_id" ]; then
      state="$(docker container inspect --format \
        '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' \
        "$container_id" 2>/dev/null || true)"
    fi
    jq -S --arg service "$service" --arg state "$state" \
      '. + {($service): {container: $state}}' "$temporary" \
      >"${temporary}.next"
    mv "${temporary}.next" "$temporary"
  done
  mv "$temporary" "$CRR_SERVICES_JSON"
}

probe_all_service_endpoints() {
  local failed=0
  local keycloak_status="passed"
  local oauth_status="passed"
  local traefik_status="passed"
  local vault_status="passed"
  local agent_status="passed"

  probe_service_endpoint "http://127.0.0.1:18083/health/ready" || {
    keycloak_status="failed"
    failed=1
  }
  probe_service_endpoint "http://127.0.0.1:18000/ping" || {
    oauth_status="failed"
    failed=1
  }
  probe_service_endpoint "http://127.0.0.1:18082/ping" || {
    traefik_status="failed"
    failed=1
  }
  probe_service_endpoint \
    "http://127.0.0.1:18200/v1/sys/health?standbyok=true" || {
    vault_status="failed"
    failed=1
  }
  crr_compose exec -T vault-agent \
    test -s /vault/out/readiness.sentinel >/dev/null 2>&1 || {
    agent_status="failed"
    failed=1
  }
  jq -S -n \
    --arg keycloak "$keycloak_status" \
    --arg oauth "$oauth_status" \
    --arg traefik "$traefik_status" \
    --arg vault "$vault_status" \
    --arg agent "$agent_status" \
    '{
      "keycloak-ready": $keycloak,
      "oauth2-proxy-ping": $oauth,
      "traefik-ping": $traefik,
      "vault-health": $vault,
      "vault-agent-sentinel": $agent
    }' >"$CRR_ENDPOINTS_JSON"
  [ "$failed" -eq 0 ]
}

classify_readiness_status() {
  local services_json="$1"
  local endpoints_passed="$2"
  local containers_healthy="false"
  if jq -e 'all(.[]; .container == "healthy")' "$services_json" >/dev/null; then
    containers_healthy="true"
  fi
  if [ "$containers_healthy" != "true" ]; then
    printf 'failed\n'
  elif [ "$endpoints_passed" = "true" ]; then
    printf 'ready\n'
  else
    printf 'degraded\n'
  fi
}

recover_vault_after_restart() {
  crr_compose stop vault-agent >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_RECOVERY" "Vault Agent stop for recovery failed"
  crr_compose run --rm --no-deps --entrypoint sh vault-agent -ec \
    'rm -f /vault/out/readiness.sentinel' >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_RECOVERY" \
      "fresh Vault Agent sentinel removal failed"
  crr_compose stop vault >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_RECOVERY" "Vault stop for recovery failed"
  crr_compose start vault >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_RECOVERY" "Vault restart failed"
  wait_container_health vault "${CRR_RECOVERY_TIMEOUT_SECONDS:-120}" ||
    crr_fail "$CRR_EXIT_RECOVERY" "Vault sealed health timed out"
  unseal_vault_from_mounted_secret ||
    crr_fail "$CRR_EXIT_RECOVERY" "Vault recovery unseal failed"
  crr_compose start vault-agent >/dev/null 2>&1 ||
    crr_fail "$CRR_EXIT_RECOVERY" "Vault Agent restart failed"
  wait_container_health vault-agent "${CRR_RECOVERY_TIMEOUT_SECONDS:-120}" ||
    crr_fail "$CRR_EXIT_RECOVERY" \
      "fresh Vault Agent sentinel recovery timed out"
}

finish_scenario() {
  local scenario="$1"
  local overall_status="$2"
  local verdict="$3"
  local project_name="$4"
  local elapsed_seconds="$5"
  local services_json="$6"
  local endpoints_json="$7"
  local started_at="$8"
  local completed_at="${9-}"
  local execution_status="${10:-0}"
  local cleanup_required="${11:-true}"
  local cleanup_status="passed"

  if [ "$cleanup_required" = "true" ] &&
    ! cleanup_owned_project "$project_name"; then
    cleanup_status="failed"
  fi
  completed_at="${completed_at:-$(date -u +%Y-%m-%dT%H:%M:%SZ)}"
  if [ "$cleanup_status" = "failed" ]; then
    overall_status="failed"
  fi
  write_readiness_verdict "$verdict" "$project_name" "$scenario" \
    "$overall_status" "$elapsed_seconds" "$cleanup_status" passed \
    "$services_json" "$endpoints_json" "$started_at" "$completed_at" ||
    return "$CRR_EXIT_READINESS"

  [ "$cleanup_status" = "passed" ] || return "$CRR_EXIT_CLEANUP"
  [ "$execution_status" -eq 0 ] || return "$execution_status"
  if [ "$scenario" = "negative-timeout" ] && [ "$overall_status" = "timed_out" ]; then
    return "$CRR_EXIT_READINESS"
  fi
  [ "$overall_status" = "ready" ] || return "$CRR_EXIT_READINESS"
}
