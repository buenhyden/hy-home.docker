#!/usr/bin/env bash
# Sourced by the disposable E2E scripts. Builds the Blog-data Gateway image
# from one exact commit with the Dockerfile's own build-context allowlist, so a
# template or registry the Dockerfile COPYs is never missing from the checkout.
# Needs gh access to the private Blog-data repository.
# Usage: build_gateway_image <blog-data-commit> <scratch-dir> <image-tag>
build_gateway_image() {
  local commit=$1 dir=$2 tag=$3 ignore paths
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
