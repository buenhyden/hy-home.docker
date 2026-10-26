#!/bin/sh
# Verify policies or evaluate the exact prepared versioned source corpus.
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
  *) echo "usage: $0 [verify|corpus|all]" >&2; exit 2 ;;
esac

check_manifest() {
  kind=$1
  expected=$2
  path=.conftest-source-inputs/$kind.paths0
  case "$expected" in
    ''|*[!0-9a-f]*) echo "ERROR: prepared Conftest context requires the host wrapper." >&2; exit 2 ;;
  esac
  if [ "${#expected}" -ne 64 ] || [ ! -f "$path" ] || [ -L "$path" ] || [ ! -s "$path" ]; then
    echo "ERROR: prepared Conftest context requires the host wrapper." >&2
    exit 2
  fi
  actual=$(sha256sum "$path")
  if [ "${actual%% *}" != "$expected" ]; then
    echo "ERROR: prepared Conftest manifest digest mismatch." >&2
    exit 2
  fi
}

if [ "$mode" != verify ]; then
  check_manifest compose "${HYHOME_CONFTEST_COMPOSE_SHA256-}"
  check_manifest dockerfile "${HYHOME_CONFTEST_DOCKERFILE_SHA256-}"
fi
if [ "$mode" != corpus ]; then
  conftest verify --policy "$policy"
fi
if [ "$mode" != verify ]; then
  xargs -0 conftest test --policy "$policy" --namespace compose -- <.conftest-source-inputs/compose.paths0
  xargs -0 conftest test --parser dockerfile --policy "$policy" --namespace dockerfile -- <.conftest-source-inputs/dockerfile.paths0
fi
