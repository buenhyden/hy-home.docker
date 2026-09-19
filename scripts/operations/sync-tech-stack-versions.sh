#!/usr/bin/env bash
# Derive the tech-stack registry from tracked infrastructure Compose images.
#
# infra/tech-stack.versions.json is downstream of Git-tracked infrastructure
# Compose service image declarations, the sole authority for this projection.
# Existing component labels remain stable where possible, while repository,
# image, source-file and local/custom classifications are regenerated.
#
# Modes:
#   (default)    Apply tag updates in place (write mode).
#   --check      Report drift and exit 1 if the registry is out of sync; no write.
#   --dry-run    Print planned component/image changes only; no write.
#
# This is the public tech-stack drift gate. It reads checked-in defaults with a
# safe YAML loader; it does not render environment files or follow builds.
# Dockerfile FROM/ARG and inline builds remain upstream build sources owned by
# the Dockerfile/custom Renovate managers, outside this Compose-only projection.
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
import subprocess
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
COMPOSE_NAME = re.compile(r"(?:docker-)?compose[^/]*\.ya?ml\Z")
SOURCE_OF_TRUTH = (
    "Git-tracked infra/**/{compose,docker-compose}*.{yml,yaml} "
    "service image declarations"
)
LOCAL_REPOSITORY_PREFIXES = ("hy/", "hyhome/", "hy-home/")


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


def tracked_compose_files():
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--", "infra"],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ContractError("unable to enumerate tracked compose files") from exc
    paths = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        try:
            relative = raw.decode("utf-8")
        except UnicodeError as exc:
            raise ContractError("invalid tracked compose path") from exc
        path = pathlib.PurePosixPath(relative)
        if COMPOSE_NAME.fullmatch(path.name):
            paths.append(relative)
    return sorted(paths)


def discovered_repositories():
    discovered = {}
    for relative in tracked_compose_files():
        for image in declared_images(relative):
            repository = image_repository(image)
            discovered.setdefault(repository, {}).setdefault(relative, set()).add(image)
    return discovered


def read_registry(path):
    if path.is_symlink() or not path.is_file():
        raise ContractError("missing or invalid tech-stack version registry")
    raw = path.read_bytes().decode("utf-8")
    registry = json.loads(raw)
    if not isinstance(registry, dict):
        raise ContractError("invalid registry document")
    if registry.get("source_of_truth") != SOURCE_OF_TRUTH:
        raise ContractError(f"source_of_truth must equal {SOURCE_OF_TRUTH!r}")
    if registry.get("local_repository_prefixes") != list(LOCAL_REPOSITORY_PREFIXES):
        raise ContractError("invalid local_repository_prefixes")
    entries = registry.get("entries")
    if not isinstance(entries, list):
        raise ContractError("registry must define an entries list")
    components = set()
    repository_owners = {}
    for entry in entries:
        component = entry.get("component") if isinstance(entry, dict) else None
        if not isinstance(component, str) or not component or component in components:
            raise ContractError("invalid registry entry")
        components.add(component)
        for field in ("images", "compose_files"):
            values = entry.get(field)
            if not isinstance(values, list) or not all(
                isinstance(value, str) and value for value in values
            ):
                raise ContractError(f"invalid registry {field}")
        for image in entry["images"]:
            repository = image_repository(image)
            if (
                repository in repository_owners
                and repository_owners[repository] != component
            ):
                raise ContractError(
                    "duplicate repository ownership: "
                    f"{repository} ({repository_owners[repository]}, {component})"
                )
            repository_owners[repository] = component
    return raw, registry


def repository_classification(repository):
    return (
        "local-custom"
        if repository.startswith(LOCAL_REPOSITORY_PREFIXES)
        else "external"
    )


def expected_entries(registry, discovered):
    repository_owner = {}
    existing_by_component = {}
    component_order = []
    for entry in registry["entries"]:
        component = entry["component"]
        component_order.append(component)
        existing_by_component[component] = entry
        for image in entry["images"]:
            repository_owner[image_repository(image)] = component

    grouped = {}
    for repository in sorted(discovered):
        component = repository_owner.get(repository, f"Compose image: {repository}")
        grouped.setdefault(component, []).append(repository)

    ordered_components = [
        component for component in component_order if component in grouped
    ]
    ordered_components.extend(
        sorted(component for component in grouped if component not in component_order)
    )
    entries = []
    for component in ordered_components:
        repositories = sorted(grouped[component])
        existing = existing_by_component.get(component, {})
        entry = {"component": component}
        if isinstance(existing.get("tier"), str) and existing["tier"]:
            entry["tier"] = existing["tier"]
        elif component.startswith("Compose image: "):
            first_path = sorted(discovered[repositories[0]])[0]
            parts = pathlib.PurePosixPath(first_path).parts
            if len(parts) > 1:
                entry["tier"] = parts[1]
        classifications = {
            repository: repository_classification(repository)
            for repository in repositories
        }
        unique_classes = set(classifications.values())
        entry["classification"] = (
            next(iter(unique_classes)) if len(unique_classes) == 1 else "mixed"
        )
        entry["repository_classifications"] = classifications
        entry["images"] = sorted(
            {
                image
                for repository in repositories
                for images in discovered[repository].values()
                for image in images
            }
        )
        entry["compose_files"] = sorted(
            {
                relative
                for repository in repositories
                for relative in discovered[repository]
            }
        )
        entry["sources"] = [
            {
                "compose_file": relative,
                "images": sorted(images),
            }
            for repository in repositories
            for relative, images in sorted(discovered[repository].items())
        ]
        entries.append(entry)
    return entries


def expected_registry(registry, discovered):
    return {
        **registry,
        "source_of_truth": SOURCE_OF_TRUTH,
        "local_repository_prefixes": list(LOCAL_REPOSITORY_PREFIXES),
        "entries": expected_entries(registry, discovered),
    }


def source_projection(entries):
    projection = {}
    for entry in entries:
        component = entry["component"]
        sources = entry.get("sources")
        if isinstance(sources, list):
            for source in sources:
                if not isinstance(source, dict):
                    continue
                relative = source.get("compose_file")
                images = source.get("images")
                if not isinstance(relative, str) or not isinstance(images, list):
                    continue
                key = (component, relative)
                projection.setdefault(key, set()).update(
                    image for image in images if isinstance(image, str)
                )
            continue
        for relative in entry["compose_files"]:
            projection.setdefault((component, relative), set()).update(entry["images"])
    return projection


def projection_preview(registry, expected):
    current = source_projection(registry["entries"])
    target = source_projection(expected["entries"])
    lines = []
    for component, relative in sorted(set(current) | set(target)):
        old = sorted(current.get((component, relative), set()))
        new = sorted(target.get((component, relative), set()))
        if old == new:
            continue
        if not old:
            action = "add"
        elif not new:
            action = "remove"
        else:
            action = "change"
        lines.append(
            f"{action} {component} source={relative} "
            f"old={','.join(old) or '-'} new={','.join(new) or '-'}"
        )
    return lines


def render_registry(raw, registry):
    newline = "\r\n" if "\r\n" in raw else "\n"
    indent_match = re.search(r'(?:\r?\n)( +)"', raw)
    indent = len(indent_match[1]) if indent_match else 2
    rendered = json.dumps(registry, indent=indent, ensure_ascii=False) + "\n"
    return rendered.replace("\n", newline)


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
    discovered = discovered_repositories()
    expected = expected_registry(registry, discovered)
    if registry == expected:
        external = sum(
            repository_classification(repository) == "external"
            for repository in discovered
        )
        local = len(discovered) - external
        print(
            "tech-stack registry is in sync with tracked compose images. "
            f"repositories={len(discovered)} external={external} local_custom={local}"
        )
        return 0
    updated = render_registry(raw, expected)
    current_repositories = {
        image_repository(image)
        for entry in registry["entries"]
        for image in entry["images"]
    }
    target_repositories = set(discovered)
    for line in projection_preview(registry, expected):
        print(line)
    print(
        "projection drift: "
        f"add={len(target_repositories - current_repositories)} "
        f"remove={len(current_repositories - target_repositories)} "
        f"repositories={len(target_repositories)}"
    )
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
