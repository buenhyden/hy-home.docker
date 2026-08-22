"""Bounded parsing and supersession validation for Stage 02 documents."""

from __future__ import annotations

import dataclasses
import os
import pathlib
import re
import stat
from collections.abc import Iterable, Mapping

from scripts.lib.document_governance.frontmatter import (
    FrontmatterError,
    frontmatter_record_from_text,
)
from scripts.lib.document_governance.registry import DocumentRegistry, load_registry
from scripts.lib.document_governance.taxonomy import architecture_identity


MAX_ARCHITECTURE_BYTES = 512 * 1024
MAX_ARCHITECTURE_DOCUMENTS = 256
_DESCRIPTION_PATH = re.compile(r"(?P<number>[0-9]{4})-[a-z0-9][a-z0-9-]*\.md")
_DECISION_PATH = re.compile(r"(?P<number>[0-9]{4})-[a-z0-9][a-z0-9-]*\.md")
_DESCRIPTION_ID = re.compile(r"AD-[0-9]{4}")
_DECISION_ID = re.compile(r"ADR-[0-9]{4}")
_REQUIREMENT_ID = re.compile(r"REQ-[0-9]{4}")
_EXPECTED_PROFILE_CONTRACTS = {
    "architecture-description": (
        "docs/02.architecture/descriptions/{number:4}-{slug}.md",
        "AD-{number:4}",
        "living",
    ),
    "adr": (
        "docs/02.architecture/decisions/{number:4}-{slug}.md",
        "ADR-{number:4}",
        "adr",
    ),
}


class ArchitectureDocumentError(ValueError):
    """Raised when the Stage 02 corpus cannot be loaded safely."""


@dataclasses.dataclass(frozen=True)
class ArchitectureDocument:
    """One canonical, deeply immutable Stage 02 document record."""

    path: pathlib.PurePosixPath
    artifact_id: str
    artifact_type: str
    status: str
    parent_ids: tuple[str, ...]
    supersedes: tuple[str, ...]
    superseded_by: str | None


@dataclasses.dataclass(frozen=True, order=True)
class ArchitectureFinding:
    """One deterministic supersession-graph finding."""

    code: str
    path: str
    message: str


def _require_directory(path: pathlib.Path, label: str) -> None:
    try:
        metadata = path.lstat()
    except OSError as error:
        raise ArchitectureDocumentError(f"cannot stat {label}: {error}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ArchitectureDocumentError(
            f"{label} must be a regular non-symlink directory"
        )


def _file_snapshot(metadata: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _read_regular_utf8(path: pathlib.Path) -> str:
    try:
        metadata = path.lstat()
    except OSError as error:
        raise ArchitectureDocumentError(
            f"cannot stat architecture document: {error}"
        ) from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise ArchitectureDocumentError(
            "architecture document must be a regular non-symlink file"
        )
    if metadata.st_size > MAX_ARCHITECTURE_BYTES:
        raise ArchitectureDocumentError("architecture document exceeds the byte limit")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
        try:
            opened = os.fstat(descriptor)
            if not stat.S_ISREG(opened.st_mode):
                raise ArchitectureDocumentError(
                    "architecture document changed to a non-regular file"
                )
            if _file_snapshot(opened) != _file_snapshot(metadata):
                raise ArchitectureDocumentError(
                    "architecture document changed while opening"
                )
            if opened.st_size > MAX_ARCHITECTURE_BYTES:
                raise ArchitectureDocumentError(
                    "architecture document exceeds the byte limit"
                )
            chunks: list[bytes] = []
            length = 0
            while True:
                chunk = os.read(
                    descriptor,
                    min(64 * 1024, MAX_ARCHITECTURE_BYTES + 1 - length),
                )
                if not chunk:
                    break
                chunks.append(chunk)
                length += len(chunk)
                if length > MAX_ARCHITECTURE_BYTES:
                    raise ArchitectureDocumentError(
                        "architecture document exceeds the byte limit"
                    )
            verified = os.fstat(descriptor)
            if (
                _file_snapshot(verified) != _file_snapshot(opened)
                or length != opened.st_size
            ):
                raise ArchitectureDocumentError(
                    "architecture document changed while reading"
                )
        finally:
            os.close(descriptor)
    except ArchitectureDocumentError:
        raise
    except OSError as error:
        raise ArchitectureDocumentError(
            f"cannot read architecture document: {error}"
        ) from error
    try:
        return b"".join(chunks).decode("utf-8")
    except UnicodeDecodeError as error:
        raise ArchitectureDocumentError(
            "architecture document is not valid UTF-8"
        ) from error


def _validate_registry_contract(registry: DocumentRegistry) -> None:
    for profile_id, expected in _EXPECTED_PROFILE_CONTRACTS.items():
        profile = registry.profiles.get(profile_id)
        if not isinstance(profile, Mapping):
            raise ArchitectureDocumentError(
                f"Stage 99 profile is missing: {profile_id}"
            )
        path_pattern, artifact_pattern, lifecycle_id = expected
        if (
            profile.get("path_pattern") != path_pattern
            or profile.get("artifact_id_pattern") != artifact_pattern
            or profile.get("identity_relation") != "direct"
            or profile.get("lifecycle_id") != lifecycle_id
        ):
            raise ArchitectureDocumentError(
                f"Stage 99 architecture profile is not canonical: {profile_id}"
            )
        if lifecycle_id not in registry.lifecycles:
            raise ArchitectureDocumentError(
                f"Stage 99 lifecycle is missing: {lifecycle_id}"
            )


def _string_tuple(value: object, field: str) -> tuple[str, ...]:
    if not isinstance(value, tuple) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise ArchitectureDocumentError(
            f"architecture frontmatter {field} must be a string list"
        )
    if len(value) != len(set(value)):
        raise ArchitectureDocumentError(
            f"architecture frontmatter {field} contains duplicates"
        )
    return value


def _canonical_parent(parent: str, artifact_type: str) -> bool:
    if artifact_type == "architecture-description":
        return _REQUIREMENT_ID.fullmatch(parent) is not None
    return (
        _REQUIREMENT_ID.fullmatch(parent) is not None
        or _DESCRIPTION_ID.fullmatch(parent) is not None
    )


def parse_architecture_document(
    path: pathlib.Path,
    *,
    registry: DocumentRegistry | None = None,
) -> ArchitectureDocument:
    """Parse one registered prefixless Architecture Description or ADR."""

    path = pathlib.Path(path)
    directory = path.parent.name
    if directory == "descriptions":
        artifact_type = "architecture-description"
        path_pattern = _DESCRIPTION_PATH
    elif directory == "decisions":
        artifact_type = "adr"
        path_pattern = _DECISION_PATH
    else:
        raise ArchitectureDocumentError(
            "architecture document parent must be descriptions or decisions"
        )
    match = path_pattern.fullmatch(path.name)
    if match is None:
        raise ArchitectureDocumentError("architecture document path is not prefixless")
    text = _read_regular_utf8(path)
    try:
        record = frontmatter_record_from_text(path, text)
    except FrontmatterError as error:
        raise ArchitectureDocumentError(str(error)) from error
    if record.metadata.get("profile_id") != artifact_type:
        raise ArchitectureDocumentError(
            f"architecture document has the wrong profile_id: {artifact_type}"
        )
    if record.metadata.get("artifact_type") != artifact_type:
        raise ArchitectureDocumentError(
            f"architecture document has the wrong artifact_type: {artifact_type}"
        )
    relative_path = pathlib.PurePosixPath(
        "docs/02.architecture", directory, path.name
    )
    owned_identity = architecture_identity(relative_path)
    if owned_identity is None or owned_identity[0] != artifact_type:
        raise ArchitectureDocumentError("architecture document path has no registered identity")
    expected_artifact_id = owned_identity[1]
    artifact_id = record.metadata.get("artifact_id")
    if artifact_id != expected_artifact_id:
        raise ArchitectureDocumentError(
            f"path requires uppercase {expected_artifact_id}, found {artifact_id!r}"
        )
    active_registry = load_registry() if registry is None else registry
    _validate_registry_contract(active_registry)
    lifecycle_id = _EXPECTED_PROFILE_CONTRACTS[artifact_type][2]
    status = record.metadata.get("status")
    if not isinstance(status, str) or status not in active_registry.lifecycles[lifecycle_id]:
        raise ArchitectureDocumentError(
            f"architecture document status is outside lifecycle: {status!r}"
        )
    parent_ids = _string_tuple(record.metadata.get("parent_ids"), "parent_ids")
    if any(not _canonical_parent(parent, artifact_type) for parent in parent_ids):
        raise ArchitectureDocumentError(
            "architecture parent_ids must use uppercase canonical stable IDs"
        )
    supersedes_value = record.metadata.get("supersedes", ())
    supersedes = _string_tuple(supersedes_value, "supersedes")
    superseded_by = record.metadata.get("superseded_by")
    if superseded_by is not None and not isinstance(superseded_by, str):
        raise ArchitectureDocumentError("superseded_by must be a stable ID or null")
    identity_pattern = _DESCRIPTION_ID if artifact_type == "architecture-description" else _DECISION_ID
    if any(identity_pattern.fullmatch(item) is None for item in supersedes):
        raise ArchitectureDocumentError(
            "supersedes must use same-type uppercase stable IDs"
        )
    if superseded_by is not None and identity_pattern.fullmatch(superseded_by) is None:
        raise ArchitectureDocumentError(
            "superseded_by must use a same-type uppercase stable ID"
        )
    return ArchitectureDocument(
        relative_path,
        artifact_id,
        artifact_type,
        status,
        parent_ids,
        supersedes,
        superseded_by,
    )


def load_architecture_documents(
    stage_root: pathlib.Path,
    *,
    registry: DocumentRegistry | None = None,
) -> tuple[ArchitectureDocument, ...]:
    """Load only the bounded, registered Stage 02 regular-file corpus."""

    stage_root = pathlib.Path(stage_root)
    _require_directory(stage_root, "Stage 02")
    forbidden = stage_root / "requirements"
    if forbidden.exists() or forbidden.is_symlink():
        raise ArchitectureDocumentError(
            "docs/02.architecture/requirements is forbidden"
        )
    allowed_root_entries = {"README.md", "descriptions", "decisions"}
    actual_root_entries = {entry.name for entry in stage_root.iterdir()}
    unexpected = sorted(actual_root_entries - allowed_root_entries)
    missing = sorted(allowed_root_entries - actual_root_entries)
    if unexpected or missing:
        detail = ", ".join(unexpected or missing)
        raise ArchitectureDocumentError(f"unregistered Stage 02 entry: {detail}")
    _read_regular_utf8(stage_root / "README.md")
    active_registry = load_registry() if registry is None else registry
    _validate_registry_contract(active_registry)
    paths: list[pathlib.Path] = []
    for directory in ("descriptions", "decisions"):
        child_root = stage_root / directory
        _require_directory(child_root, f"Stage 02 {directory}")
        has_index = False
        for entry in sorted(child_root.iterdir(), key=lambda item: item.name):
            if entry.name == "README.md":
                _read_regular_utf8(entry)
                has_index = True
                continue
            pattern = _DESCRIPTION_PATH if directory == "descriptions" else _DECISION_PATH
            if pattern.fullmatch(entry.name) is None:
                raise ArchitectureDocumentError(
                    f"unregistered Stage 02 entry: {directory}/{entry.name}"
                )
            paths.append(entry)
            if len(paths) > MAX_ARCHITECTURE_DOCUMENTS:
                raise ArchitectureDocumentError(
                    "Stage 02 exceeds the architecture document limit"
                )
        if not has_index:
            raise ArchitectureDocumentError(f"Stage 02 {directory} index is missing")
    documents = tuple(
        parse_architecture_document(path, registry=active_registry) for path in paths
    )
    identities = tuple(document.artifact_id for document in documents)
    if len(identities) != len(set(identities)):
        duplicate = next(
            identity for identity in identities if identities.count(identity) > 1
        )
        raise ArchitectureDocumentError(
            f"duplicate architecture identity: {duplicate}"
        )
    return documents


def _cycle_nodes(edges: Mapping[str, tuple[str, ...]]) -> frozenset[str]:
    visited: set[str] = set()
    active: list[str] = []
    active_set: set[str] = set()
    cyclic: set[str] = set()

    def visit(identity: str) -> None:
        if identity in visited:
            return
        if identity in active_set:
            start = active.index(identity)
            cyclic.update(active[start:])
            return
        active.append(identity)
        active_set.add(identity)
        for target in edges.get(identity, ()):
            if target in edges:
                visit(target)
        active.pop()
        active_set.remove(identity)
        visited.add(identity)

    for identity in sorted(edges):
        visit(identity)
    return frozenset(cyclic)


def validate_supersession_graph(
    documents: Iterable[ArchitectureDocument],
) -> tuple[ArchitectureFinding, ...]:
    """Validate reciprocal, acyclic, in-place Stage 02 supersession."""

    corpus = tuple(documents)
    by_id: dict[str, ArchitectureDocument] = {}
    findings: set[ArchitectureFinding] = set()
    for document in corpus:
        if document.artifact_id in by_id:
            findings.add(
                ArchitectureFinding(
                    "architecture-identity-duplicate",
                    document.path.as_posix(),
                    f"duplicate stable identity: {document.artifact_id}",
                )
            )
        else:
            by_id[document.artifact_id] = document
        if document.artifact_type == "adr" and document.status == "superseded":
            if document.path.parts[:3] != (
                "docs",
                "02.architecture",
                "decisions",
            ):
                findings.add(
                    ArchitectureFinding(
                        "superseded-adr-archived",
                        document.path.as_posix(),
                        "superseded ADRs must remain in the Stage 02 decision log",
                    )
                )
        if document.status == "superseded" and document.superseded_by is None:
            findings.add(
                ArchitectureFinding(
                    "supersession-successor-missing",
                    document.path.as_posix(),
                    "a superseded document must declare superseded_by",
                )
            )
        if document.status != "superseded" and document.superseded_by is not None:
            findings.add(
                ArchitectureFinding(
                    "supersession-status-mismatch",
                    document.path.as_posix(),
                    "superseded_by requires status: superseded",
                )
            )

    edges = {document.artifact_id: document.supersedes for document in corpus}
    for document in corpus:
        if document.supersedes and document.status not in {"active", "superseded"}:
            findings.add(
                ArchitectureFinding(
                    "supersession-successor-not-effective",
                    document.path.as_posix(),
                    "a superseding document must be active or itself superseded",
                )
            )
        for predecessor_id in document.supersedes:
            predecessor = by_id.get(predecessor_id)
            if predecessor is None:
                findings.add(
                    ArchitectureFinding(
                        "supersession-dangling",
                        document.path.as_posix(),
                        f"supersedes target does not exist: {predecessor_id}",
                    )
                )
                continue
            if predecessor.artifact_type != document.artifact_type:
                findings.add(
                    ArchitectureFinding(
                        "supersession-type-mismatch",
                        document.path.as_posix(),
                        f"supersession crosses document types: {predecessor_id}",
                    )
                )
            if predecessor.status != "superseded":
                findings.add(
                    ArchitectureFinding(
                        "supersession-predecessor-not-superseded",
                        predecessor.path.as_posix(),
                        f"superseded predecessor is not superseded: {predecessor_id}",
                    )
                )
            if predecessor.superseded_by != document.artifact_id:
                findings.add(
                    ArchitectureFinding(
                        "supersession-asymmetric",
                        document.path.as_posix(),
                        f"{predecessor_id} does not reciprocate {document.artifact_id}",
                    )
                )
        if document.superseded_by is None:
            continue
        successor = by_id.get(document.superseded_by)
        if successor is None:
            findings.add(
                ArchitectureFinding(
                    "supersession-dangling",
                    document.path.as_posix(),
                    f"superseded_by target does not exist: {document.superseded_by}",
                )
            )
        elif document.artifact_id not in successor.supersedes:
            findings.add(
                ArchitectureFinding(
                    "supersession-asymmetric",
                    document.path.as_posix(),
                    f"{document.superseded_by} does not supersede {document.artifact_id}",
                )
            )
    for identity in sorted(_cycle_nodes(edges)):
        document = by_id.get(identity)
        findings.add(
            ArchitectureFinding(
                "supersession-cycle",
                document.path.as_posix() if document is not None else identity,
                f"supersession cycle includes {identity}",
            )
        )
    return tuple(sorted(findings))
