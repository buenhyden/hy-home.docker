#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

usage() {
  cat <<'EOF'
Usage: bash scripts/validation/run-local-qa-gates.sh [--help|--list|--script-backed|--all-profiles|--harness]

Run the repository QA gates that are safe and meaningful in a local shell.

Modes:
  --script-backed  Default. Run local script-backed gates that correspond to
                   CI quality jobs or CI drift checks.
  --all-profiles   Run the same gates, but validate Docker Compose with the
                   governed all-profile set unless HYHOME_COMPOSE_PROFILES is
                   already set.
  --harness        Run only the harness-change-scoped subset of script-backed
                   gates (diff hygiene, shell syntax, doc traceability and
                   implementation alignment, Docker Compose, hardening,
                   template/security baseline, repository contracts). Use this
                   as a fast gate when changing harness surfaces such as
                   governance docs, scripts, templates, or the PR template.
  --list           Print local and remote-only QA/CI responsibilities.

Remote-only gates such as SARIF upload, protected-branch enforcement, and
GitHub-hosted required-check status are intentionally listed, not executed.
EOF
}

ALL_COMPOSE_PROFILES="${HYHOME_ALL_COMPOSE_PROFILES:-core data obs workflow ai tooling messaging security communication service storage admin iac registry sast sync testing graph mng ksql nginx}"
MODE="script-backed"

case "${1:-}" in
"")
  ;;
--script-backed)
  MODE="script-backed"
  ;;
--all-profiles)
  MODE="all-profiles"
  ;;
--harness)
  MODE="harness"
  ;;
--list)
  MODE="list"
  ;;
--help | -h)
  usage
  exit 0
  ;;
*)
  usage >&2
  exit 2
  ;;
esac

if [[ "$#" -gt 1 ]]; then
  usage >&2
  exit 2
fi

list_gates() {
  cat <<'EOF'
Local script-backed gates:
- git diff --check
- bash -n for scripts/**/*.sh and .claude/hooks/*.sh
- scripts/validation/recommend-qa-gates.sh (advisory; recommends gates, does not execute them)
- scripts/operations/sync-provider-surfaces.sh
- scripts/operations/sync-tech-stack-versions.sh --check
- scripts/validation/check-doc-traceability.sh
- scripts/validation/check-doc-implementation-alignment.sh
- scripts/validation/validate-docker-compose.sh
- scripts/hardening/check-all-hardening.sh
- scripts/validation/check-template-security-baseline.sh
- scripts/validation/check-quickwin-baseline.sh
- scripts/knowledge/generate-llm-wiki-index.sh --check
- scripts/validation/check-repo-contracts.sh

CI/local-tooling gates:
- pre-commit job: run in GitHub Actions; locally use pre-commit when installed.
- frontend-quality and storybook-coverage: run in GitHub Actions after npm ci.

Remote-only gates:
- zizmor SARIF upload with GitHub security permissions.
- PR required-check status, branch protection, CODEOWNERS review, and merge readiness.
- stale/greetings/pr-labeler/generate-changelog workflows are GitHub automation,
  not local script-backed quality gates.
EOF
}

run_step() {
  local label="$1"
  shift
  printf '\n==> %s\n' "$label"
  "$@"
}

run_bash_syntax() {
  local bash_files=()
  shopt -s nullglob globstar
  bash_files=(scripts/**/*.sh .claude/hooks/*.sh)
  shopt -u nullglob globstar

  if [[ "${#bash_files[@]}" -eq 0 ]]; then
    echo "No shell scripts found for syntax validation."
    return 0
  fi

  bash -n "${bash_files[@]}"
}

run_script_backed_gates() {
  if [[ -f scripts/operations/use-qa-ci-tools.sh ]]; then
    # shellcheck source=../operations/use-qa-ci-tools.sh
    source scripts/operations/use-qa-ci-tools.sh >/dev/null 2>&1 || true
  fi

  run_step "Diff whitespace hygiene" git diff --check
  run_step "Shell syntax" run_bash_syntax
  run_step "Provider surface drift" bash scripts/operations/sync-provider-surfaces.sh
  run_step "Tech-stack version drift" bash scripts/operations/sync-tech-stack-versions.sh --check
  run_step "Documentation traceability" bash scripts/validation/check-doc-traceability.sh
  run_step "Documentation implementation alignment" bash scripts/validation/check-doc-implementation-alignment.sh
  run_step "Docker Compose validation" bash scripts/validation/validate-docker-compose.sh
  run_step "Infrastructure hardening" bash scripts/hardening/check-all-hardening.sh
  run_step "Template/security baseline" bash scripts/validation/check-template-security-baseline.sh
  run_step "QuickWin baseline" bash scripts/validation/check-quickwin-baseline.sh
  run_step "LLM Wiki freshness" bash scripts/knowledge/generate-llm-wiki-index.sh --check
  run_step "Repository contracts" bash scripts/validation/check-repo-contracts.sh
}

run_harness_gates() {
  run_step "Diff whitespace hygiene" git diff --check
  run_step "Shell syntax" run_bash_syntax
  run_step "Documentation traceability" bash scripts/validation/check-doc-traceability.sh
  run_step "Documentation implementation alignment" bash scripts/validation/check-doc-implementation-alignment.sh
  run_step "Docker Compose validation" bash scripts/validation/validate-docker-compose.sh
  run_step "Infrastructure hardening" bash scripts/hardening/check-all-hardening.sh
  run_step "Template/security baseline" bash scripts/validation/check-template-security-baseline.sh
  run_step "Repository contracts" bash scripts/validation/check-repo-contracts.sh
}

case "$MODE" in
list)
  list_gates
  ;;
script-backed)
  run_script_backed_gates
  ;;
all-profiles)
  export HYHOME_COMPOSE_PROFILES="${HYHOME_COMPOSE_PROFILES:-$ALL_COMPOSE_PROFILES}"
  run_script_backed_gates
  ;;
harness)
  run_harness_gates
  ;;
*)
  usage >&2
  exit 2
  ;;
esac
