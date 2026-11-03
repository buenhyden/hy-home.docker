#!/usr/bin/env bash
# Sourced by the disposable E2E scripts. Builds the Blog-data Gateway image
# from one exact commit with the Dockerfile's own build-context allowlist, so a
# template or registry the Dockerfile COPYs is never missing from the checkout.
# Needs gh access to the private Blog-data repository.
# Usage: build_gateway_image <blog-data-commit> <scratch-dir> <image-tag>

# Resolve a local image to its immutable image ID without pulling, building or
# retagging it. The tag is only a lookup hint; no provenance claim follows from
# a locally available image. The chosen ID is what callers execute.
cached_image_id() {
  local reference=$1 output image platform extra host_arch
  if ! output=$(docker image inspect --format '{{.Id}} {{.Os}}/{{.Architecture}}' "$reference"); then
    printf 'cached image unavailable: %s\n' "$reference" >&2
    return 1
  fi
  read -r image platform extra <<<"$output"
  case $(uname -m) in
    x86_64) host_arch=amd64 ;;
    aarch64|arm64) host_arch=arm64 ;;
    *) printf 'unsupported host architecture\n' >&2; return 1 ;;
  esac
  if [[ ! $image =~ ^sha256:[a-f0-9]{64}$ || $platform != "linux/$host_arch" || -n ${extra:-} ]]; then
    printf 'invalid cached image identity or platform: %s\n' "$reference" >&2
    return 1
  fi
  printf 'INFO cache %s %s %s; source binding not verified by cache lookup\n' "$reference" "$image" "$platform" >&2
  printf '%s\n' "$image"
}

gateway_cached_image() {
  local commit=$1
  if [[ ! $commit =~ ^[a-f0-9]{40}$ ]]; then
    printf 'invalid gateway source identifier\n' >&2
    return 1
  fi
  cached_image_id "hy-home/blog-ingestion:$commit"
}

# A failed create can leave a daemon-side resource behind. Only remove a
# resource bearing this exact attempt's label, never a name alone.
cleanup_owned() {
  local type=$1 name=$2 owner=$3 label format
  case $type in
    container) format='{{index .Config.Labels "hyhome.hermes-e2e"}}' ;;
    network|volume) format='{{index .Labels "hyhome.hermes-e2e"}}' ;;
    *) return 1 ;;
  esac
  label=$(docker "$type" inspect --format "$format" "$name" 2>/dev/null) || return 0
  [[ $label == "$owner" ]] || return 0
  case $type in
    container) docker container rm -f "$name" >/dev/null 2>&1 || true ;;
    network) docker network rm "$name" >/dev/null 2>&1 || true ;;
    volume) docker volume rm "$name" >/dev/null 2>&1 || true ;;
  esac
}

build_gateway_image() {
  local commit=$1 dir=$2 tag=$3 ignore paths
  if [[ ! $commit =~ ^[a-f0-9]{40}$ ]]; then
    printf 'invalid gateway source identifier\n' >&2
    return 1
  fi
  git init -q "$dir"
  git -C "$dir" remote add origin "https://github.com/buenhyden/blog-data.git"
  git -C "$dir" -c "credential.helper=!gh auth git-credential" \
    fetch -q --depth 1 --filter=blob:none origin "$commit"
  git -C "$dir" sparse-checkout set --no-cone /.github/docker/
  git -C "$dir" -c "credential.helper=!gh auth git-credential" checkout -q FETCH_HEAD
  [ "$(git -C "$dir" rev-parse HEAD)" = "$commit" ] || return 1
  ignore=$dir/.github/docker/ingestion.Dockerfile.dockerignore
  # "!path/**" and "!file" re-include lines become sparse patterns.
  mapfile -t paths < <(sed -n 's#^!\(.*\)$#/\1#p' "$ignore" | sed 's#/\*\*$#/#')
  [ "${#paths[@]}" -gt 0 ] || return 1
  git -C "$dir" sparse-checkout set --no-cone "${paths[@]}"
  git -C "$dir" -c "credential.helper=!gh auth git-credential" checkout -q FETCH_HEAD
  docker build -q -f "$dir/.github/docker/ingestion.Dockerfile" -t "$tag" "$dir" >/dev/null
}
