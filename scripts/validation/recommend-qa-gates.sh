#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

usage() {
  cat <<'EOF'
Usage: bash scripts/validation/recommend-qa-gates.sh [--help]
       bash scripts/validation/recommend-qa-gates.sh [--working|--staged]
       bash scripts/validation/recommend-qa-gates.sh --base <git-ref>
       bash scripts/validation/recommend-qa-gates.sh --files <path> [path...]

Print advisory QA gate recommendations for changed paths. This script does not
run the gates and does not mutate repository, runtime, remote, or secret state.

Modes:
  --working  Use unstaged changed paths.
  --staged   Use staged changed paths.
  --base     Use paths changed between <git-ref>...HEAD.
  --files    Use the explicit path list that follows.

Default mode combines unstaged and staged changed paths.
EOF
}

MODE="auto"
BASE_REF=""
declare -a EXPLICIT_PATHS=()

while [[ "$#" -gt 0 ]]; do
  case "$1" in
  --help | -h)
    usage
    exit 0
    ;;
  --working)
    MODE="working"
    shift
    ;;
  --staged)
    MODE="staged"
    shift
    ;;
  --base)
    if [[ "$#" -lt 2 ]]; then
      usage >&2
      exit 2
    fi
    MODE="base"
    BASE_REF="$2"
    shift 2
    ;;
  --files)
    MODE="files"
    shift
    if [[ "$#" -eq 0 ]]; then
      usage >&2
      exit 2
    fi
    EXPLICIT_PATHS=("$@")
    break
    ;;
  *)
    usage >&2
    exit 2
    ;;
  esac
done

collect_paths() {
  case "$MODE" in
  auto)
    {
      git diff --name-only --diff-filter=AM
      git diff --cached --name-only --diff-filter=AM
    } | sort -u
    ;;
  working)
    git diff --name-only --diff-filter=AM
    ;;
  staged)
    git diff --cached --name-only --diff-filter=AM
    ;;
  base)
    git diff --name-only --diff-filter=AM "${BASE_REF}...HEAD"
    ;;
  files)
    printf '%s\n' "${EXPLICIT_PATHS[@]}"
    ;;
  *)
    return 2
    ;;
  esac
}

declare -a PATHS=()
while IFS= read -r path; do
  [[ -z "$path" ]] && continue
  path="${path#./}"
  PATHS+=("$path")
done < <(collect_paths | sort -u)

declare -a GATES=()
declare -A GATE_REASONS=()
declare -a REMOTE_NOTES=()
declare -A REMOTE_NOTE_SEEN=()

add_gate() {
  local command="$1"
  local reason="$2"

  if [[ -n "${GATE_REASONS[$command]+set}" ]]; then
    if [[ "; ${GATE_REASONS[$command]};" != *"; $reason;"* ]]; then
      GATE_REASONS[$command]="${GATE_REASONS[$command]}; $reason"
    fi
  else
    GATES+=("$command")
    GATE_REASONS[$command]="$reason"
  fi
}

add_remote_note() {
  local note="$1"
  if [[ -z "${REMOTE_NOTE_SEEN[$note]+set}" ]]; then
    REMOTE_NOTES+=("$note")
    REMOTE_NOTE_SEEN[$note]=1
  fi
}

add_lifecycle_gates() {
  add_gate "python3 -m unittest discover -s tests/validation -p 'test_document_corpus_lifecycle.py' -v" "document corpus lifecycle behavior changed"
  add_gate "python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-contract" "document corpus lifecycle machine and human contracts changed"
  add_gate "python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-promoted" "promoted lifecycle manifests must remain valid"
  add_gate "bash scripts/validation/generate-security-automation-readiness.sh --check" "lifecycle workflow and validation inventory may affect security readiness evidence"
  add_gate "bash scripts/validation/generate-audit-implementation-matrix.sh --check" "lifecycle workflow and validation inventory may affect audit implementation evidence"
  add_gate "bash scripts/knowledge/generate-llm-wiki-index.sh --check" "lifecycle documentation and generated data require navigation freshness"
  add_gate "bash scripts/knowledge/generate-llm-wiki-coverage.sh --check" "lifecycle documentation and generated data require coverage freshness"
}

recommend_for_path() {
  local path="$1"

  add_gate "git diff --check" "all changed files should pass whitespace hygiene"

  case "$path" in
  AGENTS.md | CLAUDE.md | GEMINI.md | .agents/* | .agents/** | .claude/* | .claude/** | .codex/* | .codex/**)
    add_gate "bash scripts/operations/sync-provider-surfaces.sh --check" "provider and root agent surfaces changed"
    add_gate "bash scripts/validation/validate-harness.sh" "agent harness surfaces changed"
    add_gate "bash scripts/validation/check-repo-contracts.sh" "provider and harness contracts changed"
    ;;
  esac

  case "$path" in
  .github/workflows/* | .github/workflows/** | .github/PULL_REQUEST_TEMPLATE.md | .github/SECURITY.md)
    add_gate "bash scripts/validation/check-repo-contracts.sh" "GitHub workflow or governance surface changed"
    add_remote_note "Verify GitHub-required checks, branch protection, and SARIF/upload behavior in GitHub after workflow-governance changes."
    ;;
  esac

  case "$path" in
  docs/* | docs/** | README.md)
    add_gate "bash scripts/knowledge/generate-llm-wiki-index.sh --check" "documentation navigation may need index freshness"
    add_gate "bash scripts/validation/check-doc-traceability.sh" "documentation links or execution/operations routing may have changed"
    add_gate "bash scripts/validation/check-doc-implementation-alignment.sh" "active docs must match tracked implementation surfaces"
    add_gate "bash scripts/validation/check-repo-contracts.sh" "documentation contracts changed"
    ;;
  esac

  case "$path" in
  docs/99.templates/* | docs/99.templates/**)
    add_gate "bash scripts/validation/check-template-security-baseline.sh" "template or template-support contracts changed"
    ;;
  esac

  case "$path" in
  docker-compose.yml | docker-compose.*.yml | infra/* | infra/**)
    add_gate "bash scripts/validation/validate-docker-compose.sh" "Compose or infrastructure surface changed"
    add_gate "bash scripts/hardening/check-all-hardening.sh" "infrastructure hardening surface changed"
    add_gate "bash scripts/validation/check-template-security-baseline.sh" "Compose security/template baseline may be affected"
    add_gate "bash scripts/validation/check-quickwin-baseline.sh" "QuickWin baseline controls may be affected"
    add_gate "bash scripts/operations/sync-tech-stack-versions.sh --check" "image/version registry may need drift validation"
    add_gate "bash scripts/validation/check-doc-implementation-alignment.sh" "infra changes can stale active docs"
    add_gate "bash scripts/validation/check-repo-contracts.sh" "infrastructure contracts changed"
    ;;
  esac

  case "$path" in
  scripts/* | scripts/** | .claude/hooks/* | .claude/hooks/**)
    add_gate "bash -n scripts/**/*.sh .claude/hooks/*.sh" "shell script or hook surface changed"
    add_gate "bash scripts/validation/run-local-qa-gates.sh --harness" "script or harness-adjacent surface changed"
    add_gate "bash scripts/validation/check-repo-contracts.sh" "script inventory or references may have changed"
    ;;
  esac

  case "$path" in
  scripts/validation/check-storybook-contract.sh | projects/storybook/* | projects/storybook/**)
    add_gate "bash scripts/validation/check-storybook-contract.sh" "Storybook/frontend quality contract changed"
    add_gate "npm run lint --prefix projects/storybook/nextjs" "frontend source changed"
    add_gate "npm run typecheck --prefix projects/storybook/nextjs" "frontend source changed"
    add_gate "npm run build --prefix projects/storybook/nextjs" "frontend source changed"
    add_gate "npm run build-storybook --prefix projects/storybook/nextjs" "Storybook surface changed"
    add_remote_note "GitHub frontend-quality and storybook-coverage jobs remain CI responsibilities after frontend changes."
    ;;
  esac

  case "$path" in
  secrets/* | secrets/** | .env.example)
    add_gate "bash scripts/operations/gen-secrets.sh --check" "secret metadata or example environment surface changed"
    add_gate "bash scripts/validation/check-repo-contracts.sh" "secret and environment documentation contracts changed"
    add_remote_note "Do not print or commit secret values; only metadata, IDs, paths, and readiness evidence are valid."
    ;;
  esac

  case "$path" in
  .pre-commit-config.yaml | \
    .github/workflows/* | .github/workflows/** | \
    scripts/validation/check-document-corpus-lifecycle.py | \
    tests/validation/test_document_corpus_lifecycle.py | \
    docs/98.archive/* | docs/98.archive/** | \
    docs/99.templates/support/document-corpus-migration-contract.yaml | \
    docs/99.templates/support/corpus-migration-contract.md | \
    docs/99.templates/support/archive-retention-contract.md | \
    docs/99.templates/templates/common/archive.template.md | \
    docs/90.references/data/governance/document-corpus-lifecycle/* | \
    docs/90.references/data/governance/document-corpus-lifecycle/**)
    add_lifecycle_gates
    ;;
  esac
}

for path in "${PATHS[@]}"; do
  recommend_for_path "$path"
done

echo "QA gate recommendation"
echo "mode=$MODE"
if [[ -n "$BASE_REF" ]]; then
  echo "base_ref=$BASE_REF"
fi
echo "changed_paths_total=${#PATHS[@]}"

if [[ "${#PATHS[@]}" -eq 0 ]]; then
  echo "No changed paths detected; no path-specific QA gates recommended."
  exit 0
fi

echo
echo "Changed paths:"
for path in "${PATHS[@]}"; do
  printf -- '- %s\n' "$path"
done

echo
echo "Recommended local gates:"
for command in "${GATES[@]}"; do
  printf -- '- %s\n' "$command"
  printf '  reason: %s\n' "${GATE_REASONS[$command]}"
done

if [[ "${#REMOTE_NOTES[@]}" -gt 0 ]]; then
  echo
  echo "Remote/manual responsibilities:"
  for note in "${REMOTE_NOTES[@]}"; do
    printf -- '- %s\n' "$note"
  done
fi
