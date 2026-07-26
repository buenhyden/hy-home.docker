#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "compose-core-readiness: not inside a Git worktree" >&2
  exit 10
}

# shellcheck source=scripts/validation/compose-core-readiness.lib.sh
source "${BASE_DIR}/scripts/validation/compose-core-readiness.lib.sh"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/validation/run-compose-core-readiness.sh --preflight
  bash scripts/validation/run-compose-core-readiness.sh --scenario startup-readiness
  bash scripts/validation/run-compose-core-readiness.sh --scenario vault-restart-recovery
  bash scripts/validation/run-compose-core-readiness.sh --scenario negative-timeout
  bash scripts/validation/run-compose-core-readiness.sh --cleanup-only --project-name hyhome-crr-20260719-12345-abcd1234

Exit classes: 0=pass, 2=usage, 10=preflight/scope, 20=startup,
30=readiness, 40=recovery, 50=cleanup ambiguity.
EOF
}

# shellcheck disable=SC2329 # Invoked by the EXIT/signal trap.
cleanup_runtime_material() {
  local runtime_dir="${CRR_RUNTIME_DIR-}"
  [ -n "$runtime_dir" ] || return 0
  if [ -L "$runtime_dir" ]; then
    crr_error "refusing to remove symbolic-link runtime path"
    return "$CRR_EXIT_CLEANUP"
  fi
  case "${runtime_dir#/tmp/}" in
  hyhome-crr-20260719-[0-9]*-[a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9])
    [ "$(realpath -m -- "$runtime_dir")" = "$runtime_dir" ] || {
      crr_error "refusing to remove runtime path with redirected ancestors"
      return "$CRR_EXIT_CLEANUP"
    }
    rm -rf -- "$runtime_dir"
    ;;
  *)
    crr_error "refusing to remove non-owned runtime path"
    return "$CRR_EXIT_CLEANUP"
    ;;
  esac
}

# shellcheck disable=SC2329 # Invoked by the EXIT/signal trap.
has_owned_cleanup_marker() {
  local runtime_dir="${CRR_RUNTIME_DIR-}" runtime_project
  [ -n "$runtime_dir" ] || return 1
  case "$runtime_dir" in
  /tmp/*) runtime_project="${runtime_dir#/tmp/}" ;;
  *) return 1 ;;
  esac
  is_owned_project_name "$runtime_project" || return 1
  [ "${CRR_PROJECT_NAME-}" = "$runtime_project" ] || return 1
  [ "$(realpath -m -- "$runtime_dir")" = "$runtime_dir" ] || return 1
  [ ! -L "$runtime_dir" ] || return 1
  [ -f "${runtime_dir}/cleanup-required" ]
}

# shellcheck disable=SC2329 # Invoked by the EXIT/signal trap.
on_exit() {
  local status="$?"
  local cleanup_status=0
  trap - EXIT HUP INT TERM

  if [ "${CRR_CLEANUP_DONE:-false}" != "true" ] &&
    { [ "${CRR_CLEANUP_REQUIRED:-false}" = "true" ] || has_owned_cleanup_marker; }; then
    cleanup_owned_project "${CRR_PROJECT_NAME-}" || cleanup_status=$?
  fi
  cleanup_runtime_material || cleanup_status=$?

  if [ "$cleanup_status" -ne 0 ]; then
    status="$CRR_EXIT_CLEANUP"
  fi
  exit "$status"
}

execute_runtime_scenario() {
  assert_docker_compose
  prepare_synthetic_secrets
  render_core_model
  assert_docker_daemon
  assert_local_image_identities
  assert_target_capacity

  : >"${CRR_RUNTIME_DIR}/cleanup-required"
  start_vault
  initialize_unseal_and_configure_synthetic_vault
  prepare_vault_agent_output_volume
  start_remaining_services
  collect_service_states
  probe_all_service_endpoints || return "$CRR_EXIT_READINESS"

  case "$CRR_MODE" in
  startup-readiness) ;;
  vault-restart-recovery)
    recover_vault_after_restart
    collect_service_states
    probe_all_service_endpoints || {
      crr_error "endpoint recovery verification failed"
      return "$CRR_EXIT_RECOVERY"
    }
    ;;
  negative-timeout)
    if probe_service_endpoint "http://127.0.0.1:1/readiness" 1; then
      crr_error "negative timeout target unexpectedly responded"
      return "$CRR_EXIT_READINESS"
    fi
    jq -S '. + {"negative-timeout": "timed_out"}' \
      "$CRR_ENDPOINTS_JSON" >"${CRR_ENDPOINTS_JSON}.next" ||
      return "$CRR_EXIT_READINESS"
    mv "${CRR_ENDPOINTS_JSON}.next" "$CRR_ENDPOINTS_JSON" ||
      return "$CRR_EXIT_READINESS"
    ;;
  *) return "$CRR_EXIT_USAGE" ;;
  esac
}

main() {
  local parse_status scenario_verdict started_at started_at_iso elapsed
  local execution_status status overall_status cleanup_label

  set +e
  parse_args "$@"
  parse_status=$?
  set -e
  if [ "$parse_status" -ne 0 ]; then
    usage >&2
    return "$parse_status"
  fi

  assert_linked_worktree
  if [ "$CRR_MODE" = "cleanup-only" ]; then
    CRR_PROJECT_NAME="$CRR_REQUESTED_PROJECT"
    CRR_RUNTIME_DIR="/tmp/${CRR_PROJECT_NAME}"
  else
    allocate_runtime_identity
  fi
  CRR_CLEANUP_REQUIRED="false"
  CRR_CLEANUP_DONE="false"

  prepare_owned_paths
  trap on_exit EXIT HUP INT TERM

  if [ "$CRR_MODE" = "cleanup-only" ]; then
    assert_docker_compose
    assert_docker_daemon
    cleanup_owned_project "$CRR_PROJECT_NAME"
    printf 'cleanup_status=passed project_name=%s\n' "$CRR_PROJECT_NAME"
    return 0
  fi

  if [ "$CRR_MODE" = "preflight" ]; then
    assert_docker_compose
    prepare_synthetic_secrets
    render_core_model
    assert_docker_daemon
    assert_local_image_identities
    printf '%s\n' \
      "preflight_status=passed" \
      "project_name=${CRR_PROJECT_NAME}" \
      "target_class=${CRR_TARGET_CLASS}" \
      "target_capacity_min=4cpu,4gib-memory,8gib-storage" \
      "resource_limits=keycloak:1.00cpu/768m,oauth2-proxy:0.50cpu/256m,traefik:0.50cpu/256m,vault:0.50cpu/256m,vault-agent:0.25cpu/128m" \
      "services=keycloak,oauth2-proxy,traefik,vault,vault-agent" \
      "ports=18000,18443,18082,18083,18200" \
      "startup_timeout_seconds=${CRR_STARTUP_TIMEOUT_SECONDS:-180}" \
      "recovery_timeout_seconds=${CRR_RECOVERY_TIMEOUT_SECONDS:-120}" \
      "readiness_handoff=${CRR_VERDICT_PATH}" \
      "scenario_evidence_pattern=${CRR_EVIDENCE_DIR}/readiness-verdict.<scenario>.json" \
      "cleanup_command=bash scripts/validation/run-compose-core-readiness.sh --cleanup-only --project-name ${CRR_PROJECT_NAME}"
    return 0
  fi

  scenario_verdict="${CRR_EVIDENCE_DIR}/readiness-verdict.${CRR_MODE}.json"
  execution_status=0
  if [ "$CRR_MODE" != "negative-timeout" ] &&
    ! rm -f -- "$CRR_VERDICT_PATH"; then
    crr_error "canonical readiness handoff invalidation failed"
    execution_status="$CRR_EXIT_READINESS"
  fi

  printf '{}\n' >"$CRR_SERVICES_JSON"
  printf '{}\n' >"$CRR_ENDPOINTS_JSON"
  started_at="$(date +%s)"
  started_at_iso="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

  if [ "$execution_status" -eq 0 ]; then
    set +e
    (set -e; execute_runtime_scenario)
    execution_status=$?
    set -e
  fi
  if [ -f "${CRR_RUNTIME_DIR}/cleanup-required" ]; then
    CRR_CLEANUP_REQUIRED="true"
  fi

  overall_status="failed"
  if [ "$execution_status" -eq 0 ]; then
    if [ "$CRR_MODE" = "negative-timeout" ]; then
      overall_status="timed_out"
    else
      overall_status="$(
        classify_readiness_status "$CRR_SERVICES_JSON" true
      )" || {
        crr_error "readiness status classification failed"
        overall_status="failed"
      }
      if [ "$overall_status" != "ready" ]; then
        case "$CRR_MODE" in
        vault-restart-recovery) execution_status="$CRR_EXIT_RECOVERY" ;;
        *) execution_status="$CRR_EXIT_READINESS" ;;
        esac
      fi
    fi
  fi
  elapsed="$(( $(date +%s) - started_at ))"

  set +e
  finish_scenario "$CRR_MODE" "$overall_status" "$scenario_verdict" \
    "$CRR_PROJECT_NAME" "$elapsed" "$CRR_SERVICES_JSON" "$CRR_ENDPOINTS_JSON" \
    "$started_at_iso" "" "$execution_status" "$CRR_CLEANUP_REQUIRED"
  status=$?
  set -e

  if [ "$status" -eq 0 ] && [ "$overall_status" = "ready" ]; then
    publish_canonical_readiness_handoff "$scenario_verdict" "$CRR_VERDICT_PATH" ||
      status="$CRR_EXIT_READINESS"
  fi

  cleanup_label="passed"
  [ "$status" -eq "$CRR_EXIT_CLEANUP" ] && cleanup_label="failed"
  printf 'scenario=%s overall_status=%s cleanup_status=%s exit_class=%s evidence_path=%s readiness_handoff=%s\n' \
    "$CRR_MODE" "$overall_status" "$cleanup_label" "$status" \
    "$scenario_verdict" "$CRR_VERDICT_PATH"
  return "$status"
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  main "$@"
fi
