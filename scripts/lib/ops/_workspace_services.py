"""Bounded, value-minimizing Compose declarations; never operational evidence."""

import hashlib
import posixpath
import re
import tempfile
from collections.abc import Mapping
from pathlib import Path, PurePosixPath

import yaml

from scripts.lib.document_governance.operations_catalog import (
    OperationsAuthorityError,
    _ComposeLoader,
    _overlay_annotation,
    _validate_overlay_base,
    read_bounded_regular,
)
from scripts.lib.ops.port_inventory import PortContractError, project
from scripts.lib.supply_chain.latest_version_gate import expected_from_root

NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,255}\Z")
COMPOSE = re.compile(r"(?:docker-compose|compose)[^/]*\.ya?ml\Z")
IMAGE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]*(?:@sha256:[a-f0-9]{64})?\Z")


class _InventoryLoader(_ComposeLoader):
    def construct_mapping(self, node, deep=False):
        keys = [
            key.value for key, _ in node.value if key.tag != "tag:yaml.org,2002:merge"
        ]
        if not all(isinstance(key, str) for key in keys):
            raise ValueError("invalid_yaml_key")
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate_yaml_key")
        return super().construct_mapping(node, deep=deep)


def _symbol(value):
    """Retain public identifiers, never interpolation defaults or URL credentials."""
    if not isinstance(value, str):
        return None
    if "$" in value or "://" in value or "@" in value or len(value) > 1024:
        return None
    return value if all(character.isprintable() for character in value) else None


def _reference(source, value):
    value = _symbol(value)
    if not value or value.startswith(("/", "~")) or "\\" in value:
        return None
    normalized = posixpath.normpath(posixpath.join(posixpath.dirname(source), value))
    return (
        normalized if normalized != ".." and not normalized.startswith("../") else None
    )


def _image(value):
    if (
        isinstance(value, str)
        and len(value) <= 1024
        and "://" not in value
        and IMAGE.fullmatch(value)
    ):
        return value
    return None


def _names(value):
    items = value.keys() if isinstance(value, Mapping) else value
    if not isinstance(items, (list, tuple, type({}.keys()))):
        return []
    return sorted(
        item for item in items if isinstance(item, str) and NAME.fullmatch(item)
    )


def _dependencies(service):
    value = service.get("depends_on", [])
    return [
        {
            "service": name,
            "condition": (
                value[name].get("condition", "service_started")
                if isinstance(value, Mapping) and isinstance(value[name], Mapping)
                else "service_started"
            ),
        }
        for name in _names(value)
        if not isinstance(value, Mapping)
        or not isinstance(value[name], Mapping)
        or value[name].get("condition", "service_started")
        in {"service_started", "service_healthy", "service_completed_successfully"}
    ]


def _mounts(service):
    rows = []
    values = service.get("volumes", [])
    for item in values if isinstance(values, list) else []:
        if isinstance(item, str):
            fields = item.split(":")
            source, target = (None, fields[0]) if len(fields) == 1 else fields[:2]
            kind = (
                "anonymous"
                if source is None
                else "bind"
                if "/" in source or "$" in source
                else "volume"
            )
        elif isinstance(item, Mapping):
            source, target, kind = (
                item.get("source"),
                item.get("target"),
                item.get("type"),
            )
        else:
            continue
        public_source = _symbol(source)
        if public_source and (
            public_source.startswith(("/", "~"))
            or ".." in PurePosixPath(public_source).parts
        ):
            public_source = None
        rows.append(
            {
                "type": kind
                if kind in {"bind", "volume", "tmpfs", "anonymous", "image"}
                else "unknown",
                "source": public_source,
                "target": _symbol(target),
            }
        )
    return rows


def _links(source, doc, gaps):
    relations = []
    if "x-hyhome-overlay" in doc:
        try:
            base = _overlay_annotation(PurePosixPath(source), doc).as_posix()
            target = _reference("", base)
            if target != base:
                raise ValueError("invalid_overlay_annotation")
            relations.append({"kind": "overlay", "source": source, "target": target})
        except (OperationsAuthorityError, ValueError):
            gaps.append({"source": source, "code": "invalid_overlay_annotation"})
    includes = doc.get("include", [])
    if not isinstance(includes, list):
        gaps.append({"source": source, "code": "invalid_include"})
        includes = []
    for item in includes:
        config = item if isinstance(item, Mapping) else {"path": item}
        paths = config.get("path", [])
        paths = [paths] if isinstance(paths, str) else paths
        if not isinstance(paths, list) or not paths:
            gaps.append({"source": source, "code": "invalid_include_path"})
            continue
        for value in paths:
            relation = {
                "kind": "include",
                "source": source,
                "target": _reference(source, value),
            }
            for key in ("project_directory", "env_file"):
                if key in config:
                    entries = (
                        config[key] if isinstance(config[key], list) else [config[key]]
                    )
                    relation[key] = [_reference(source, entry) for entry in entries]
                    if key == "project_directory" and None in relation[key]:
                        gaps.append(
                            {
                                "source": source,
                                "code": "unsafe_include_project_directory",
                            }
                        )
            relations.append(relation)
    services = doc.get("services", {})
    for name, service in services.items() if isinstance(services, Mapping) else []:
        if not isinstance(name, str) or not NAME.fullmatch(name):
            continue
        extends = service.get("extends") if isinstance(service, Mapping) else None
        if extends is None:
            continue
        if not isinstance(extends, Mapping) or not isinstance(
            extends.get("service"), str
        ):
            gaps.append({"source": source, "code": "invalid_extends"})
            continue
        relations.append(
            {
                "kind": "extends",
                "source": source,
                "service": name,
                "target": _reference(source, extends["file"])
                if "file" in extends
                else source,
                "target_service": extends["service"]
                if NAME.fullmatch(extends["service"])
                else None,
            }
        )
    return relations


def _load_sources(root, allowed, gaps):
    pending = sorted(
        path for path in allowed if COMPOSE.fullmatch(PurePosixPath(path).name)
    )
    documents, sources, relations, snapshots = {}, [], [], {}
    visited = set()
    while pending:
        source = pending.pop(0)
        if source in visited:
            continue
        visited.add(source)
        if source not in allowed:
            gaps.append({"source": source, "code": "source_not_allowlisted"})
            continue
        if not source.endswith((".yml", ".yaml")):
            gaps.append({"source": None, "code": "non_yaml_reference_refused"})
            continue
        try:
            raw = read_bounded_regular(root, PurePosixPath(source))
            doc = yaml.load(raw, Loader=_InventoryLoader) or {}
            if not isinstance(doc, Mapping) or not isinstance(
                doc.get("services", {}), Mapping
            ):
                raise ValueError("invalid_document")
        except (
            OSError,
            OperationsAuthorityError,
            ValueError,
            TypeError,
            yaml.YAMLError,
            UnicodeError,
            RecursionError,
        ) as error:
            code = (
                "duplicate_yaml_key"
                if isinstance(error, ValueError) and str(error) == "duplicate_yaml_key"
                else "source_unreadable_or_invalid"
            )
            gaps.append({"source": source, "code": code})
            continue
        documents[source] = doc
        snapshots[source] = raw
        sources.append(
            {
                "path": source,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "state": "parsed",
            }
        )
        links = _links(source, doc, gaps)
        relations.extend(links)
        pending.extend(link["target"] for link in links if link["target"])
        for link in links:
            if link["target"] is None:
                gaps.append(
                    {"source": source, "code": "unsafe_or_unresolved_reference"}
                )
    return documents, sources, relations, snapshots


def _root_expected(members, snapshots):
    # The existing authority must not reread a concurrently changed original
    # and follow newly introduced references outside the explicit allowlist.
    with tempfile.TemporaryDirectory(prefix="workspace-compose-") as directory:
        root = Path(directory)
        for source in members:
            target = root / source
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(snapshots[source])
        return expected_from_root(root)


def _closure(start, relations, kind="include"):
    pending, visited = [start], set()
    while pending:
        source = pending.pop()
        if source in visited:
            continue
        visited.add(source)
        pending.extend(
            link["target"]
            for link in relations
            if link["source"] == source and link["kind"] == kind and link["target"]
        )
    return visited


def _overlay_gaps(documents, relations, gaps):
    paths = frozenset(PurePosixPath(path) for path in documents)
    regular = frozenset(
        PurePosixPath(path)
        for path, doc in documents.items()
        if "x-hyhome-overlay" not in doc
    )
    included = frozenset(
        PurePosixPath(link["target"])
        for link in relations
        if link["kind"] == "include"
        and link["source"] == "docker-compose.yml"
        and link["target"]
    )
    for link in relations:
        if link["kind"] != "overlay":
            continue
        try:
            if link["target"] not in documents:
                raise ValueError("overlay_base_unresolved")
            _validate_overlay_base(
                PurePosixPath(link["source"]),
                PurePosixPath(link["target"]),
                tracked=paths,
                regular=regular,
                included=included,
                root_model=documents.get("docker-compose.yml", {}),
            )
        except (OperationsAuthorityError, ValueError):
            gaps.append({"source": link["source"], "code": "overlay_base_unresolved"})


def _service_rows(documents, members, gaps):
    rows = []
    for source, doc in sorted(documents.items()):
        services = doc.get("services", {})
        for name, service in services.items():
            if (
                not isinstance(name, str)
                or not NAME.fullmatch(name)
                or not isinstance(service, Mapping)
            ):
                gaps.append({"source": source, "code": "invalid_service"})
                continue
            try:
                endpoints = project(
                    {"services": {name: service}, "networks": doc.get("networks", {})}
                )["services"][0]
                endpoints = {
                    **endpoints,
                    "internal_dns": {
                        **endpoints["internal_dns"],
                        "endpoints": [
                            {
                                (
                                    "network_reference" if key == "network_key" else key
                                ): value
                                for key, value in endpoint.items()
                            }
                            for endpoint in endpoints["internal_dns"]["endpoints"]
                        ],
                    },
                }
            except (PortContractError, TypeError, ValueError, RecursionError):
                endpoints = None
                gaps.append(
                    {
                        "source": source,
                        "service": name,
                        "code": "endpoint_projection_unresolved",
                    }
                )
            secrets = service.get("secrets", [])
            secret_names = (
                [
                    item.get("source") if isinstance(item, Mapping) else item
                    for item in secrets
                ]
                if isinstance(secrets, list)
                else []
            )
            rows.append(
                {
                    "id": f"{source}::{name}",
                    "source": source,
                    "service": name,
                    "root_member": source in members,
                    "image": _image(service.get("image")),
                    "profiles": _names(service.get("profiles", [])),
                    "networks": _names(service.get("networks", [])),
                    "ports": endpoints,
                    "secrets": _names(secret_names),
                    "mounts": _mounts(service),
                    "depends_on": _dependencies(service),
                    "healthcheck_declared": isinstance(
                        service.get("healthcheck"), Mapping
                    ),
                    "consumers": [],
                    "caller_evidence": "unknown",
                    "data_flow_evidence": "unknown",
                    "product_registration": "unknown",
                    "runtime": "NOT_RUN",
                }
            )
    return rows


def inspect_services(root: Path, source_paths: list[str]) -> dict:
    """Read only explicitly allowed public paths; no env, secret or Docker IO.

    Candidate basenames are compose*.yml/yaml and docker-compose*.yml/yaml,
    including labs/<name>/docker-compose.yml. References can add arbitrary
    allowlisted YAML files.
    Every source+service is a declaration, never an independently deployed count.
    """
    gaps, allowed = [], set()
    for value in source_paths:
        if (
            not isinstance(value, str)
            or _reference("", value) != value
            or value in {".", ""}
        ):
            gaps.append({"source": None, "code": "invalid_public_source_path"})
        else:
            allowed.add(value)
    documents, sources, relations, snapshots = _load_sources(root, allowed, gaps)
    _overlay_gaps(documents, relations, gaps)
    members = (
        _closure("docker-compose.yml", relations)
        if "docker-compose.yml" in documents
        else set()
    )
    for link in relations:
        target = link["target"]
        if (
            link["kind"] == "include"
            and target
            and link["source"] in _closure(target, relations)
        ):
            gaps.append({"source": link["source"], "code": f"{link['kind']}_cycle"})
        if (
            link["kind"] == "extends"
            and target in documents
            and link["target_service"] not in documents[target].get("services", {})
        ):
            gaps.append({"source": link["source"], "code": "extends_service_missing"})
    edges = {
        (link["source"], link["service"]): (link["target"], link["target_service"])
        for link in relations
        if link["kind"] == "extends"
    }
    for start in edges:
        node, visited = start, set()
        while node in edges and node not in visited:
            visited.add(node)
            node = edges[node]
        if node in visited:
            gaps.append({"source": start[0], "code": "extends_cycle"})
    root_names = sorted(
        name
        for source in members
        if source in documents
        for name in documents[source].get("services", {})
        if isinstance(name, str)
    )
    if len(root_names) != len(set(root_names)):
        gaps.append({"source": "docker-compose.yml", "code": "duplicate_root_service"})
    if members and members <= set(documents):
        try:
            expected, evidence = _root_expected(members, snapshots)
            if (
                expected != root_names
                or {item["path"] for item in evidence["input_files"]} != members
            ):
                raise ValueError("root_membership_mismatch")
        except (ValueError, OSError, OperationsAuthorityError, yaml.YAMLError):
            gaps.append(
                {"source": "docker-compose.yml", "code": "root_authority_unresolved"}
            )
    elif members:
        gaps.append(
            {"source": "docker-compose.yml", "code": "root_authority_unresolved"}
        )
    rows = _service_rows(documents, members, gaps)
    targets = {
        link["target"]
        for link in relations
        if link["target"] and link["kind"] != "overlay"
    }
    overlays = {path for path, doc in documents.items() if "x-hyhome-overlay" in doc}
    entrypoints = sorted(
        (set(documents) - targets - overlays)
        | ({"docker-compose.yml"} & set(documents) - overlays)
    )
    projects = [_closure(entry, relations) for entry in entrypoints]
    for row in rows:
        scopes = [scope for scope in projects if row["source"] in scope]
        row["consumers"] = sorted(
            other["id"]
            for other in rows
            if any(other["source"] in scope for scope in scopes)
            and any(
                dependency["service"] == row["service"]
                for dependency in other["depends_on"]
            )
        )
    return {
        "services": rows,
        "sources": sorted(sources, key=lambda item: item["path"]),
        "root_services": sorted(set(root_names)),
        "entrypoints": entrypoints,
        "relations": relations,
        "render_cases": [],
        "gaps": gaps,
    }
