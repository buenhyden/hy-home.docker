#!/usr/bin/env bash
# Deterministic, offline contract checks for the cache-only E2E image resolver.
set -euo pipefail
test_dir=$(cd "$(dirname "$0")" && pwd)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
mkdir "$work/bin"
cat >"$work/bin/docker" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
[[ $* == "image inspect --format {{.Id}} {{.Os}}/{{.Architecture}} hy-home/blog-ingestion:"* ]] || exit 88
case ${FAKE_IMAGE:-present} in
  present)
    case $(uname -m) in
      x86_64) platform=linux/amd64 ;;
      aarch64|arm64) platform=linux/arm64 ;;
      *) exit 1 ;;
    esac
    printf '%s\n' "sha256:$(printf 'a%.0s' {1..64}) $platform" ;;
  missing) exit 1 ;;
  malformed) printf '%s\n' 'sha256:bad linux/amd64' ;;
esac
SH
chmod 0755 "$work/bin/docker"
export PATH="$work/bin:$PATH"
source "$test_dir/gateway-image.sh"
commit=0123456789abcdef0123456789abcdef01234567
image=$(gateway_cached_image "$commit")
[[ "$image" == "sha256:$(printf 'a%.0s' {1..64})" ]]
if FAKE_IMAGE=missing gateway_cached_image "$commit"; then exit 1; fi
if FAKE_IMAGE=malformed gateway_cached_image "$commit"; then exit 1; fi
if gateway_cached_image invalid; then exit 1; fi
cat >"$work/bin/git" <<'SH'
#!/usr/bin/env bash
if [[ $# == 4 && $1 == -C && $3 == rev-parse && $4 == --show-toplevel ]]; then
  exec /usr/bin/git "$@"
fi
printf '%s\n' forbidden >"$TRACE_FILE"
exit 99
SH
chmod 0755 "$work/bin/git"
export TRACE_FILE="$work/git-trace"
if build_gateway_image invalid "$work/build" synthetic >/dev/null 2>&1; then
  printf '%s\n' 'build unexpectedly accepted an invalid source identifier' >&2
  exit 1
fi
if [[ -e $TRACE_FILE ]]; then
  printf '%s\n' 'invalid build identifier invoked git' >&2
  exit 1
fi
if FAKE_IMAGE=missing bash "$test_dir/e2e-upgrade.sh" --cache-only >/dev/null 2>&1; then
  printf '%s\n' 'cache-only unexpectedly accepted missing image' >&2
  exit 1
fi
if [[ -e $TRACE_FILE ]]; then
  printf '%s\n' 'cache-only invoked an unexpected git command' >&2
  exit 1
fi
if FAKE_IMAGE=missing bash "$test_dir/e2e-ingress.sh" --cache-only >/dev/null 2>&1; then
  printf '%s\n' 'cache-only ingress unexpectedly accepted missing image' >&2
  exit 1
fi
if [[ -e $TRACE_FILE ]]; then
  printf '%s\n' 'cache-only ingress invoked an unexpected git command' >&2
  exit 1
fi
printf '%s\n' 'PASS: cached image is pinned; missing, malformed and invalid references are rejected'
