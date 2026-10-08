#!/bin/sh
# Verify the policies, scan the tracked corpus, or preserve the combined default.
set -eu
script_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
cd "$script_dir/../../.."
policy=infra/11-quality/conftest/policy
mode=${1-all}
[ "$#" -le 1 ] || {
  echo "usage: $0 [verify|corpus|all]" >&2
  exit 2
}
case "$mode" in
  verify|corpus|all) ;;
  *)
    echo "usage: $0 [verify|corpus|all]" >&2
    exit 2
    ;;
esac
if [ "$mode" != corpus ]; then
  conftest verify --policy "$policy"
fi
if [ "$mode" != verify ]; then
  { find infra -name 'docker-compose*.yml' -type f; find labs -maxdepth 1 -name '*.yml' -type f; } | sort | xargs conftest test --policy "$policy" --namespace compose
  find infra -name 'Dockerfile*' -type f | sort | xargs conftest test --parser dockerfile --policy "$policy" --namespace dockerfile
fi
