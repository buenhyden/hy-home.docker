#!/usr/bin/env bash
# Sync the curated tech-stack registry to Docker Compose image tags/digests.
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
# This is the public tech-stack drift gate. It reads service image declarations
# with a safe YAML loader; it does not render environment files or follow builds.
# Dockerfile FROM/ARG and inline builds need a separate registry source contract.
set -euo pipefail

if (( $# > 1 )); then
  echo "Usage: $0 [--check | --dry-run]" >&2
  exit 2
fi

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

_verified_repository_root() {
  local entrypoint direct_root candidate direct_identity candidate_identity
  entrypoint="$(readlink -f -- "${BASH_SOURCE[0]}" 2>/dev/null || true)"
  if [[ -z "$entrypoint" || ! -f "$entrypoint" ]] \
    || ! direct_root="$(cd "$(dirname "$entrypoint")/../.." && pwd -P)"; then
    printf '%s\n' "FAIL: invalid HYHOME_CI_GATE_ROOT" >&2
    return 2
  fi
  if [[ -z "${HYHOME_CI_GATE_ROOT+x}" ]]; then
    printf '%s\n' "$direct_root"
    return 0
  fi
  candidate="$HYHOME_CI_GATE_ROOT"
  if [[ ! "$candidate" =~ ^/proc/self/fd/(0|[1-9][0-9]*)$ ]]; then
    printf '%s\n' "FAIL: invalid HYHOME_CI_GATE_ROOT" >&2
    return 2
  fi
  direct_identity="$(stat -Lc '%d:%i' -- "$direct_root" 2>/dev/null || true)"
  candidate_identity="$(stat -Lc '%d:%i' -- "$candidate" 2>/dev/null || true)"
  if [[ -z "$direct_identity" || "$candidate_identity" != "$direct_identity" || ! -d "$candidate" ]]; then
    printf '%s\n' "FAIL: invalid HYHOME_CI_GATE_ROOT" >&2
    return 2
  fi
  printf '%s\n' "$candidate"
}

REPO_ROOT="$(_verified_repository_root)"
cd "$REPO_ROOT"

SYNC_MODE="$MODE" python3 - <<'PY'
from __future__ import annotations

import json
import os
import pathlib
import re
import stat
import sys
import tempfile

import yaml


class ContractError(ValueError):
    pass


class ComposeLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        # Reject duplicate authored keys, but allow an explicit key to override
        # an inherited YAML merge (the normal Compose anchor convention).
        keys = set()
        for key_node, _ in node.value:
            if key_node.tag == "tag:yaml.org,2002:merge":
                continue
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str) or key in keys:
                raise ContractError("duplicate or non-string compose mapping key")
            keys.add(key)
        return super().construct_mapping(node, deep=deep)


def override_value(loader, node):
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    return loader.construct_mapping(node)


ComposeLoader.add_constructor("!override", override_value)
ComposeLoader.add_constructor("!reset", lambda loader, node: None)
DEFAULT = re.compile(r"\$\{[A-Za-z_][A-Za-z0-9_]*(?::-|-)([^{}]+)\}")
IMAGE = re.compile(
    r"(?P<repo>[a-z0-9][a-z0-9._/-]*(?::[0-9]+/[a-z0-9._/-]+)?)"
    r"(?::(?P<tag>[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}))?"
    r"(?:@sha256:(?P<digest>[a-fA-F0-9]{64}))?"
)
JSON_STRING = re.compile(r'"(?:[^"\\]|\\.)*"')


def image_repository(image):
    match = IMAGE.fullmatch(image) if isinstance(image, str) else None
    if not match or not (match["tag"] or match["digest"]):
        raise ContractError("invalid or unpinned image declaration")
    return match["repo"]


def declared_images(relative):
    if not isinstance(relative, str):
        raise ContractError("invalid compose path")
    path = pathlib.Path(relative)
    if path.is_absolute() or ".." in path.parts or path.is_symlink():
        raise ContractError("invalid compose path")
    if not path.is_file() or not path.resolve().is_relative_to(pathlib.Path.cwd()):
        raise ContractError("missing or invalid compose file")
    try:
        document = yaml.load(path.read_text(encoding="utf-8"), Loader=ComposeLoader)
        services = document.get("services") if isinstance(document, dict) else None
        if not isinstance(services, dict):
            raise ContractError("invalid compose services mapping")
        images = set()
        for service in services.values():
            if service is None:  # !reset removes a service/field.
                continue
            if not isinstance(service, dict):
                raise ContractError("invalid compose service mapping")
            image = service.get("image")
            if image is None:
                continue  # Build-only services have no runtime image declaration.
            if not isinstance(image, str):
                raise ContractError("invalid compose image scalar")
            # Resolve only checked-in defaults, never process environment values.
            image = DEFAULT.sub(lambda match: match[1], image)
            image_repository(image)
            images.add(image)
        return images
    except (OSError, UnicodeError, yaml.YAMLError, ValueError, RecursionError) as exc:
        raise ContractError(f"invalid compose declaration: {relative}") from exc


def read_registry(path):
    if path.is_symlink() or not path.is_file():
        raise ContractError("missing or invalid tech-stack version registry")
    raw = path.read_bytes().decode("utf-8")
    registry = json.loads(raw)
    entries = registry.get("entries") if isinstance(registry, dict) else None
    if not isinstance(entries, list) or not entries:
        raise ContractError("registry must define a non-empty entries list")
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("component"), str):
            raise ContractError("invalid registry entry")
        for field in ("images", "compose_files"):
            values = entry.get(field)
            if not isinstance(values, list) or not values or not all(
                isinstance(value, str) and value for value in values
            ):
                raise ContractError(f"invalid registry {field}")
    return raw, registry


def plan_changes(entries):
    planned = []
    for entry in entries:
        discovered = set()
        for relative in entry["compose_files"]:
            discovered.update(declared_images(relative))
        by_repository = {}
        for image in discovered:
            by_repository.setdefault(image_repository(image), set()).add(image)
        for image in entry["images"]:
            repository = image_repository(image)
            candidates = by_repository.get(repository, set())
            if not candidates:
                raise ContractError(
                    f"{entry['component']}: registry image repo not declared in compose: {repository}"
                )
            if len(candidates) != 1:
                raise ContractError(
                    f"{entry['component']}: ambiguous compose declarations for {repository}"
                )
            candidate = next(iter(candidates))
            if candidate != image:
                planned.append((entry["component"], image, candidate))
    return planned


def updated_registry(raw, registry, planned):
    replacements = {}
    for _, old, new in planned:
        if old in replacements and replacements[old] != new:
            raise ContractError("ambiguous registry replacement")
        replacements[old] = new
    # JSON token substitution preserves whitespace and untouched escapes. The
    # semantic comparison below forbids changes outside the curated image lists.
    updated = JSON_STRING.sub(
        lambda match: json.dumps(replacements[json.loads(match[0])])
        if json.loads(match[0]) in replacements else match[0], raw
    )
    expected = {
        **registry,
        "entries": [
            {**entry, "images": [replacements.get(image, image) for image in entry["images"]]}
            for entry in registry["entries"]
        ],
    }
    if json.loads(updated) != expected:
        raise ContractError("replacement would change non-image registry metadata")
    return updated


def atomic_write(path, raw, updated):
    temporary = None
    original = path.stat()
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=path.parent,
            prefix=f".{path.name}.", delete=False,
        ) as stream:
            temporary = pathlib.Path(stream.name)
            os.fchmod(stream.fileno(), stat.S_IMODE(original.st_mode))
            stream.write(updated)
            stream.flush()
            os.fsync(stream.fileno())
        current = path.stat()
        if path.is_symlink() or (
            current.st_dev, current.st_ino, current.st_size, current.st_mtime_ns
        ) != (
            original.st_dev, original.st_ino, original.st_size, original.st_mtime_ns
        ) or path.read_bytes().decode("utf-8") != raw:
            raise ContractError("registry changed during synchronization")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    mode = os.environ["SYNC_MODE"]
    path = pathlib.Path("infra/tech-stack.versions.json")
    raw, registry = read_registry(path)
    planned = plan_changes(registry["entries"])
    updated = updated_registry(raw, registry, planned)
    if not planned:
        print("tech-stack registry is in sync with declared compose images. changes=0")
        return 0
    for component, old, new in planned:
        print(f"{component}: {old} -> {new}")
    print(f"changes={len(planned)}")
    if mode == "check":
        print("FAIL: tech-stack registry is out of sync; run scripts/operations/sync-tech-stack-versions.sh", file=sys.stderr)
        return 1
    if mode == "write":
        atomic_write(path, raw, updated)
        print(f"wrote {path}")
    return 0


try:
    sys.exit(main())
except ContractError as exc:
    print(f"FAIL: {exc}", file=sys.stderr)
    sys.exit(1)
except (OSError, UnicodeError, json.JSONDecodeError):
    print("FAIL: unable to read or atomically update tech-stack registry", file=sys.stderr)
    sys.exit(1)
PY
