#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: bash scripts/knowledge/generate-llm-wiki-coverage.sh [--check|--stdout]

Generate the repo-local LLM Wiki coverage snapshot through the canonical Python
generator. A sealed Gate 9 manifest is accepted only with --stdout.

Options:
  --check   Fail when the generated coverage snapshot is stale.
  --stdout  Write the rendered Markdown to stdout without modifying the repository.
  -h, --help
             Show this help.
EOF
}

mode="--write"
if (( $# > 1 )); then
  usage >&2
  exit 2
fi
case "${1:-}" in
  "") ;;
  --check) mode="--check" ;;
  --stdout) mode="--stdout" ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac

exec python3 scripts/knowledge/generate-llm-wiki.py --artifact coverage "$mode"
