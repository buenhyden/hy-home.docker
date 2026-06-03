#!/usr/bin/env bash
# Sync the curated tech-stack version registry to declared Docker Compose image tags.
#
# infra/tech-stack.versions.json is, by its own declaration, downstream of the
# Docker Compose image declarations ("source_of_truth": "Docker Compose image
# declarations"). When an image tag changes in a listed compose file (for
# example via a Dependabot bump), this script re-points the matching curated
# registry image to the compose-declared tag, preserving file formatting and the
# curated image set.
#
# Modes:
#   (default)    Apply tag updates in place (write mode).
#   --check      Report drift and exit 1 if the registry is out of sync; no write.
#   --dry-run    Print planned component/image changes only; no write.
#
# The image-extraction rules mirror the "Tech-stack version drift" gate in
# scripts/validation/check-repo-contracts.sh so a synced registry passes that gate.
set -euo pipefail

MODE="write"
case "${1:-}" in
--check) MODE="check" ;;
--dry-run) MODE="dry-run" ;;
"") MODE="write" ;;
*)
  echo "Usage: $0 [--check | --dry-run]" >&2
  exit 2
  ;;
esac

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

SYNC_MODE="$MODE" python3 - <<'PY'
from __future__ import annotations

import os
import pathlib
import re
import sys

mode = os.environ.get("SYNC_MODE", "write")
registry_path = pathlib.Path("infra/tech-stack.versions.json")

if not registry_path.is_file():
    print(f"FAIL: missing tech-stack version registry: {registry_path}", file=sys.stderr)
    sys.exit(1)

raw = registry_path.read_text()

import json

try:
    registry = json.loads(raw)
except Exception as exc:  # noqa: BLE001
    print(f"FAIL: invalid JSON in {registry_path}: {exc}", file=sys.stderr)
    sys.exit(1)

entries = registry.get("entries")
if not isinstance(entries, list) or not entries:
    print(f"FAIL: {registry_path} must define a non-empty entries list", file=sys.stderr)
    sys.exit(1)

image_line_re = re.compile(r"(?m)^\s*image:\s*['\"]?([^'\"\s#]+)")
default_image_re = re.compile(r"\$\{[^}:]+:-([^}]+)\}")


def declared_images(path: pathlib.Path) -> set[str]:
    text = path.read_text(errors="ignore")
    images: set[str] = set()
    for match in image_line_re.finditer(text):
        raw_image = match.group(1)
        images.add(raw_image)
        default_match = default_image_re.search(raw_image)
        if default_match:
            images.add(default_match.group(1))
    return images


def split_repo_tag(image: str) -> tuple[str, str] | None:
    # Split on the last colon that is not part of a registry host:port segment.
    last_segment = image.rsplit("/", 1)[-1]
    if ":" not in last_segment:
        return None
    repo, tag = image.rsplit(":", 1)
    return repo, tag


planned: list[tuple[str, str, str]] = []  # (component, old_image, new_image)
warnings: list[str] = []

for entry in entries:
    component = entry.get("component", "<unknown>")
    images = entry.get("images")
    compose_files = entry.get("compose_files")
    if not isinstance(images, list) or not isinstance(compose_files, list):
        continue

    discovered: set[str] = set()
    for compose_file in compose_files:
        compose_path = pathlib.Path(compose_file)
        if compose_path.is_file():
            discovered.update(declared_images(compose_path))

    repo_to_tags: dict[str, set[str]] = {}
    for image in discovered:
        parsed = split_repo_tag(image)
        if parsed:
            repo_to_tags.setdefault(parsed[0], set()).add(parsed[1])

    for image in images:
        parsed = split_repo_tag(image)
        if not parsed:
            continue
        repo, tag = parsed
        candidate_tags = repo_to_tags.get(repo)
        if not candidate_tags:
            warnings.append(f"{component}: registry image repo not declared in compose: {image}")
            continue
        if tag in candidate_tags:
            continue
        if len(candidate_tags) > 1:
            warnings.append(
                f"{component}: ambiguous compose tags for {repo}: {sorted(candidate_tags)}; left unchanged"
            )
            continue
        new_tag = next(iter(candidate_tags))
        planned.append((component, image, f"{repo}:{new_tag}"))

for warning in warnings:
    print(f"WARN: {warning}", file=sys.stderr)

if not planned:
    print("tech-stack registry is in sync with declared compose image tags. changes=0")
    sys.exit(0)

for component, old_image, new_image in planned:
    print(f"{component}: {old_image} -> {new_image}")
print(f"changes={len(planned)}")

if mode == "check":
    print("FAIL: tech-stack registry is out of sync; run scripts/operations/sync-tech-stack-versions.sh", file=sys.stderr)
    sys.exit(1)

if mode == "dry-run":
    sys.exit(0)

# write mode: literal, formatting-preserving substitution of each curated image.
updated = raw
for _component, old_image, new_image in planned:
    needle = f'"{old_image}"'
    replacement = f'"{new_image}"'
    if updated.count(needle) != 1:
        print(
            f"FAIL: expected exactly one occurrence of {needle} for safe replacement", file=sys.stderr
        )
        sys.exit(1)
    updated = updated.replace(needle, replacement)

# Re-validate the result parses as JSON before writing.
try:
    json.loads(updated)
except Exception as exc:  # noqa: BLE001
    print(f"FAIL: post-sync JSON is invalid: {exc}", file=sys.stderr)
    sys.exit(1)

registry_path.write_text(updated)
print(f"wrote {registry_path}")
PY
