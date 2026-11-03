"""Read-only Stage 98 loaders that current, non-archive checks still use.

No function here validates Stage 98; SPEC-0248 lists every caller and the
replacement each needs before the archive bodies are removed.
"""

from __future__ import annotations

import dataclasses
import functools
import os
import pathlib
import re
import stat
from collections.abc import Callable
from typing import Any

import yaml

from scripts.lib.document_governance.frontmatter import safe_load_unique
from scripts.lib.document_governance.git_provenance import (
    recovery_commit_is_valid,
    verify_recovery_blobs_batch,
)
from scripts.lib.document_governance.registry import (
    ARCHIVE_MODEL_ADOPTED,
    PRESERVED_DISPOSITIONS,
    DocumentRegistry,
    archive_disposition_model,
    artifact_identifier_regex,
    classify_path,
    load_registry,
    path_matches_pattern,
    preserved_origin_path,
)

MAX_DOCUMENT_BYTES = 1_048_576
MAX_ARCHIVE_ENTRIES = 512
MAX_ARCHIVE_BYTES = 32 * 1024 * 1024
_MIGRATION_FIELDS = frozenset(
    {
        "schema_version",
        "migration_id",
        "baseline_commit",
        "approval",
        "consumer_policy",
        "final_compaction",
        "planned_creations",
        "rows",
    }
)


def recover_legacy_parent_identities(root: pathlib.Path) -> set[str]:
    """Recover pre-taxonomy Spec/Plan/Task parents from the frozen ledger."""

    ledger = root / "docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md"
    try:
        text = ledger.read_text(encoding="utf-8")
        fenced = (
            text.split("## Archive Ledger", 1)[1]
            .split("```yaml", 1)[1]
            .split("```", 1)[0]
        )
        document = safe_load_unique(fenced)
    except (OSError, UnicodeError, IndexError, yaml.YAMLError):
        return set()
    records = document.get("records") if isinstance(document, dict) else None
    if not isinstance(records, list):
        return set()
    identities: set[str] = set()
    for row in records:
        if not isinstance(row, dict):
            return set()
        legacy = row.get("legacy_path")
        artifact_id = row.get("artifact_id")
        if not isinstance(legacy, str) or not isinstance(artifact_id, str):
            continue
        spec_match = re.fullmatch(
            r"docs/(?:98\.archive/03\.specs/|03\.specs/)(\d{3})-([^/]+)/spec\.md",
            legacy,
        )
        if artifact_id.startswith("spec-") and spec_match:
            identities.add(f"spec:{spec_match.group(1)}-{spec_match.group(2)}")
        execution_match = re.fullmatch(
            r"docs/04\.execution/(plans|tasks)/([^/]+)\.md", legacy
        )
        if execution_match:
            role = "plan" if execution_match.group(1) == "plans" else "task"
            identities.add(f"{role}:{execution_match.group(2)}")
    return identities


def _safe_path(value: object) -> pathlib.PurePosixPath | None:
    if not isinstance(value, str) or not value or value.startswith("-"):
        return None
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or not path.parts:
        return None
    if any(
        part in {"", ".", ".."}
        or part.startswith("-")
        or "\\" in part
        or any(ord(character) < 32 or ord(character) == 127 for character in part)
        for part in path.parts
    ):
        return None
    return path


def _directory_flags() -> int:
    return (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )


def _path_identity(metadata: os.stat_result) -> tuple[int, int]:
    """Return what a symlink swap cannot forge.

    The stat-then-open check exists to prove the descriptor refers to the
    object that was stat'd. Only device and inode carry that. Link count and
    timestamps move whenever anything else writes into the directory, which on
    a shared parent such as /tmp happens continuously and proves nothing; an
    attacker who swaps a directory can match a timestamp with utimensat but
    cannot match an inode. Content that must not move while a load runs is
    guarded separately by the fuller snapshot below.
    """

    return (metadata.st_dev, metadata.st_ino)


def _snapshot(metadata: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _open_directory_at(
    parent: int, name: str, label: str
) -> tuple[int, tuple[int, ...]]:
    descriptor: int | None = None
    try:
        before = os.stat(name, dir_fd=parent, follow_symlinks=False)
        if stat.S_ISLNK(before.st_mode) or not stat.S_ISDIR(before.st_mode):
            raise ValueError(f"{label} must be a non-symlink directory")
        descriptor = os.open(name, _directory_flags(), dir_fd=parent)
        opened = os.fstat(descriptor)
    except OSError as error:
        if descriptor is not None:
            os.close(descriptor)
        raise ValueError(f"cannot open {label}: {error}") from error
    assert descriptor is not None
    if _path_identity(opened) != _path_identity(before):
        os.close(descriptor)
        raise ValueError(f"{label} changed while opening")
    return descriptor, _snapshot(opened)


def _open_directory_path(
    path: pathlib.Path, label: str
) -> tuple[int, int, str, tuple[int, ...]]:
    absolute = pathlib.Path(os.path.abspath(path))
    if not absolute.is_absolute() or len(absolute.parts) < 2:
        raise ValueError(f"{label} must be an absolute contained path")
    parent = os.open(os.path.sep, _directory_flags())
    try:
        for part in absolute.parts[1:-1]:
            if part in {"", ".", ".."}:
                raise ValueError(f"{label} contains an unsafe component")
            child, _ = _open_directory_at(parent, part, f"{label} parent")
            os.close(parent)
            parent = child
        name = absolute.parts[-1]
        descriptor, snapshot = _open_directory_at(parent, name, label)
        return parent, descriptor, name, snapshot
    except BaseException:
        os.close(parent)
        raise


def _verify_directory(
    parent: int,
    name: str,
    descriptor: int,
    snapshot: tuple[int, ...],
    label: str,
) -> None:
    try:
        linked = os.stat(name, dir_fd=parent, follow_symlinks=False)
        opened = os.fstat(descriptor)
    except OSError as error:
        raise ValueError(f"{label} changed while loading: {error}") from error
    if (
        stat.S_ISLNK(linked.st_mode)
        or _snapshot(linked) != snapshot
        or _snapshot(opened) != snapshot
    ):
        raise ValueError(f"{label} changed while loading")


def _bounded_entries(
    descriptor: int,
    *,
    label: str,
    limit: int,
) -> tuple[tuple[str, os.stat_result], ...]:
    entries: list[tuple[str, os.stat_result]] = []
    try:
        with os.scandir(descriptor) as iterator:
            for entry in iterator:
                if len(entries) >= limit:
                    raise ValueError(f"{label} entry limit exceeded")
                entries.append((entry.name, entry.stat(follow_symlinks=False)))
    except OSError as error:
        raise ValueError(f"cannot enumerate {label}: {error}") from error
    return tuple(sorted(entries, key=lambda item: item[0]))


def _read_regular_at(
    parent: int,
    name: str,
    label: str,
    *,
    expected: os.stat_result | None = None,
) -> bytes:
    try:
        before = expected or os.stat(name, dir_fd=parent, follow_symlinks=False)
    except OSError as error:
        raise ValueError(f"cannot stat {label}: {error}") from error
    if stat.S_ISLNK(before.st_mode) or not stat.S_ISREG(before.st_mode):
        raise ValueError(f"document is not a bounded regular file: {label}")
    if before.st_size > MAX_DOCUMENT_BYTES:
        raise ValueError(f"document exceeds the byte limit: {label}")
    try:
        descriptor = os.open(
            name,
            os.O_RDONLY
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | os.O_NONBLOCK,
            dir_fd=parent,
        )
    except OSError as error:
        raise ValueError(f"cannot open {label}: {error}") from error
    try:
        opened = os.fstat(descriptor)
        if _snapshot(opened) != _snapshot(before):
            raise ValueError(f"document changed while opening: {label}")
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            chunk = os.read(descriptor, min(65_536, remaining))
            if not chunk:
                raise ValueError(f"document ended before its snapshotted size: {label}")
            chunks.append(chunk)
            remaining -= len(chunk)
        if os.read(descriptor, 1):
            raise ValueError(f"document grew during its bounded read: {label}")
        after = os.fstat(descriptor)
        linked = os.stat(name, dir_fd=parent, follow_symlinks=False)
        if _snapshot(after) != _snapshot(before) or _snapshot(linked) != _snapshot(
            before
        ):
            raise ValueError(f"document changed during its bounded read: {label}")
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def _read_regular(path: pathlib.Path) -> bytes:
    parent, descriptor, name, snapshot = _open_directory_path(
        path.parent, f"{path} parent"
    )
    try:
        entries = dict(
            _bounded_entries(
                descriptor, label=f"{path} parent", limit=MAX_ARCHIVE_ENTRIES
            )
        )
        if path.name not in entries:
            raise ValueError(f"document is missing: {path}")
        raw = _read_regular_at(
            descriptor, path.name, str(path), expected=entries[path.name]
        )
        _verify_directory(parent, name, descriptor, snapshot, f"{path} parent")
        return raw
    finally:
        os.close(descriptor)
        os.close(parent)


def _decode_document(path: pathlib.Path) -> str:
    try:
        return _read_regular(path).decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"document is not UTF-8: {path}") from error


def _frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise ValueError("frontmatter is required")
    marker = text.find("\n---\n", 4)
    if marker < 0:
        raise ValueError("frontmatter is unterminated")
    try:
        loaded = _load_archive_yaml(text[4:marker])
    except (yaml.YAMLError, ValueError) as error:
        raise ValueError("frontmatter YAML is invalid or has duplicate keys") from error
    if not isinstance(loaded, dict) or any(not isinstance(key, str) for key in loaded):
        raise ValueError("frontmatter must be a string-key mapping")
    return loaded, text[marker + 5 :]


def _load_archive_yaml(source: str) -> object:
    """Load strict Archive YAML without aliases or merge-key indirection."""

    root = yaml.compose(source, Loader=yaml.SafeLoader)
    seen: set[int] = set()

    def visit(node: yaml.nodes.Node | None) -> None:
        if node is None:
            return
        identity = id(node)
        if identity in seen:
            raise ValueError("Archive YAML aliases are not supported")
        seen.add(identity)
        if isinstance(node, yaml.nodes.MappingNode):
            for key, value in node.value:
                if key.tag == "tag:yaml.org,2002:merge":
                    raise ValueError("Archive YAML merge keys are not supported")
                visit(key)
                visit(value)
        elif isinstance(node, yaml.nodes.SequenceNode):
            for value in node.value:
                visit(value)

    visit(root)
    return safe_load_unique(source)


def _section(body: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        body,
    )
    if match is None:
        raise ValueError(f"missing tombstone section: {heading}")
    return match.group(1).strip()


def _code_value(value: str) -> str:
    match = re.fullmatch(r"`([^`]+)`", value.strip())
    if match is None:
        raise ValueError("tombstone value must be one code span")
    return match.group(1)


_ARCHIVE_PREFIX = "docs/98.archive/"
# The catalog is its own record so the Stage 98 README can stay a router
# (SPEC-0179 Archive 3.0.0); its header and rows are unchanged by the move.
_CATALOG_RECORD = "docs/98.archive/retention-catalog.md"
_CATALOG_SEPARATOR = re.compile(r"(?:\|:?-{3,}:?){4}\|")
# A catalog unit is a directory the Registry registers as one whole package: a
# Spec package or an Incident bundle. Every other preserved file is its own unit.
_CATALOG_UNIT_PROFILES = ("spec", "incident")
_NO_DURABLE_CONTRACT = "no durable contract"
_NO_CORRECTIVE_ACTION = re.compile(r"no corrective action:\s*\S")
_CODE_SPAN = re.compile(r"`([^`]+)`")


@dataclasses.dataclass(frozen=True, order=True)
class RetentionCatalogRow:
    """One Retention Envelope, as the four cells of its catalog row."""

    record: str
    disposition: str
    names: str
    source: str


@functools.lru_cache(maxsize=1)
def _catalog_registry() -> DocumentRegistry:
    # Unit shapes, identifier shapes, and owner classification are the
    # repository Registry's code-time contract, not a value a checked root
    # supplies, so a fixture root that carries only the switch still reads them.
    return load_registry()


@functools.lru_cache(maxsize=1)
def _catalog_contract() -> tuple[
    tuple[str, ...], re.Pattern[str], re.Pattern[str], re.Pattern[str]
]:
    """Read unit path patterns and identifier patterns from the Registry once."""

    registry = _catalog_registry()
    units = tuple(
        str(registry.profiles[profile]["path_pattern"])
        for profile in _CATALOG_UNIT_PROFILES
    )
    identifiers = artifact_identifier_regex(
        tuple(
            pattern
            for profile in registry.profiles.values()
            if isinstance(pattern := profile.get("artifact_id_pattern"), str)
        )
    )
    incident = artifact_identifier_regex(
        (str(registry.profiles["incident"]["artifact_id_pattern"]),)
    )
    # An Incident and its Postmortem are the record, never its corrective owner.
    incident_records = artifact_identifier_regex(
        tuple(
            str(registry.profiles[profile]["artifact_id_pattern"])
            for profile in ("incident", "postmortem")
        )
    )
    return units, identifiers, incident, incident_records


def _is_unit_directory(origin: str) -> bool:
    units, _, _, _ = _catalog_contract()
    return any(
        path_matches_pattern(f"{origin}/{pathlib.PurePosixPath(unit).name}", unit)
        for unit in units
    )


def retention_unit(record: str) -> str:
    """Return the catalog unit of an archive-relative path: its package or itself."""

    disposition, _, rest = record.partition("/")
    parts = rest.split("/")
    for depth in range(1, len(parts)):
        directory = "/".join(parts[:depth])
        if _is_unit_directory(f"docs/{directory}"):
            return f"{disposition}/{directory}/"
    return record


def _names_owner_path(
    root: pathlib.Path,
    names: str,
    owner_exists: Callable[[pathlib.PurePosixPath], bool] | None = None,
    registry: DocumentRegistry | None = None,
) -> bool:
    """Whether `names` cites a current document a Registry profile classifies."""

    for span in _CODE_SPAN.findall(names):
        path = _safe_path(span)
        if path is None or path.as_posix().startswith(_ARCHIVE_PREFIX):
            continue
        if (
            classify_path(
                path, registry if registry is not None else _catalog_registry()
            )
            is None
        ):
            continue
        try:
            if owner_exists is None:
                _read_regular(root / path)
            elif not owner_exists(path):
                continue
        except (OSError, ValueError):
            continue
        return True
    return False


def _names_are_valid(
    root: pathlib.Path,
    disposition: str,
    names: str,
    owner_exists: Callable[[pathlib.PurePosixPath], bool] | None = None,
    registry: DocumentRegistry | None = None,
) -> bool:
    """Whether `Names` holds what its class must name, with no invented identifier."""

    _, identifiers, incident, incident_records = _catalog_contract()
    if not names.strip():
        return False
    if disposition == "retired":
        return True
    if disposition == "superseded":
        return identifiers.search(names) is not None
    if disposition == "completed":
        return (
            names.strip() == _NO_DURABLE_CONTRACT
            or identifiers.search(names) is not None
            or _names_owner_path(root, names, owner_exists, registry)
        )
    match = incident.search(names)
    if match is None:
        return False
    owner = incident_records.sub(" ", names)
    return (
        identifiers.search(owner) is not None
        or _names_owner_path(root, owner, owner_exists, registry)
        or _NO_CORRECTIVE_ACTION.search(owner) is not None
    )


def _catalog_cells(line: str) -> tuple[str, ...]:
    return tuple(cell.strip() for cell in line.strip().strip("|").split("|"))


def _catalog_rows(
    text: str,
) -> tuple[RetentionCatalogRow, ...]:
    contract = _catalog_registry().common["archive_retention"]
    header = tuple(contract["capture_columns"])
    section = re.search(
        rf"(?ms)^## {re.escape(contract['capture_section'])}[ \t]*\n(.*?)(?=^## |\Z)",
        text,
    )
    if section is None:
        return ()
    lines = [
        line.strip()
        for line in section.group(1).splitlines()
        if line.strip().startswith("|")
    ]
    if (
        len(lines) < 2
        or _catalog_cells(lines[0]) != header
        or _CATALOG_SEPARATOR.fullmatch(re.sub(r"\s", "", lines[1])) is None
    ):
        return ()
    return tuple(
        RetentionCatalogRow(*cells)
        for line in lines[2:]
        if len(cells := _catalog_cells(line)) == len(header)
    )


def _code_span(value: str) -> str | None:
    match = re.fullmatch(r"`([^`]+)`", value)
    return match.group(1) if match is not None else None


def _catalog_index_text(root: pathlib.Path) -> str | None:
    try:
        return _decode_document(root / _CATALOG_RECORD)
    except ValueError:
        return None


def _catalog_members(
    path: pathlib.Path, is_package: bool
) -> dict[str, tuple[str, bytes]] | None:
    """Snapshot a retention unit without following links or reading special files."""

    parent, descriptor, name, snapshot = _open_directory_path(
        path.parent, "retention unit parent"
    )
    members: dict[str, tuple[str, bytes]] = {}
    entry_count = byte_count = 0

    def visit(
        directory: int, prefix: str, names: tuple[str, ...] | None = None
    ) -> None:
        nonlocal entry_count, byte_count
        entries = (
            tuple(
                (item, os.stat(item, dir_fd=directory, follow_symlinks=False))
                for item in names
            )
            if names is not None
            else _bounded_entries(
                directory, label="retention unit", limit=MAX_ARCHIVE_ENTRIES
            )
        )
        for filename, metadata in entries:
            entry_count += 1
            if entry_count > MAX_ARCHIVE_ENTRIES:
                raise ValueError("retention unit entry limit exceeded")
            relative = f"{prefix}{filename}" if is_package else ""
            if stat.S_ISDIR(metadata.st_mode) and is_package:
                child, before = _open_directory_at(
                    directory, filename, "retention member"
                )
                try:
                    visit(child, f"{relative}/")
                    _verify_directory(
                        directory, filename, child, before, "retention member"
                    )
                finally:
                    os.close(child)
            else:
                raw = _read_regular_at(
                    directory, filename, "retention member", expected=metadata
                )
                byte_count += len(raw)
                if byte_count > MAX_ARCHIVE_BYTES:
                    raise ValueError("retention unit byte limit exceeded")
                mode = "100755" if metadata.st_mode & stat.S_IXUSR else "100644"
                members[relative] = (mode, raw)

    try:
        try:
            os.stat(path.name, dir_fd=descriptor, follow_symlinks=False)
        except FileNotFoundError:
            return None
        if is_package:
            child, before = _open_directory_at(descriptor, path.name, "retention unit")
            try:
                visit(child, "")
                _verify_directory(
                    descriptor, path.name, child, before, "retention unit"
                )
            finally:
                os.close(child)
        else:
            visit(descriptor, "", (path.name,))
        _verify_directory(parent, name, descriptor, snapshot, "retention unit parent")
        return members
    finally:
        os.close(descriptor)
        os.close(parent)


def preserved_member_paths(
    archive_root: pathlib.Path, disposition: str
) -> tuple[str, ...]:
    """Enumerate one preserved subtree through the bounded no-follow reader."""

    if disposition not in PRESERVED_DISPOSITIONS:
        raise ValueError("unregistered preservation disposition")
    try:
        members = _catalog_members(archive_root / disposition, True) or {}
    except (OSError, ValueError) as error:
        raise ValueError("preserved subtree is unsafe") from error
    return tuple(f"{disposition}/{member}" for member in sorted(members))


def retention_catalog_records(root: pathlib.Path) -> frozenset[str]:
    """Return the archive-relative units the Retention Catalog has a row for."""

    text = _catalog_index_text(pathlib.Path(root))
    rows = _catalog_rows(text) if text is not None else ()
    return frozenset(
        record for row in rows if (record := _code_span(row.record)) is not None
    )


def retention_catalog_retirements(
    root: pathlib.Path,
) -> frozenset[pathlib.PurePosixPath]:
    """Return the origin path of each `retired/` file a catalog row covers."""

    root = pathlib.Path(root)
    records = retention_catalog_records(root)
    archive = root / _ARCHIVE_PREFIX
    origins: set[pathlib.PurePosixPath] = set()
    for relative in preserved_member_paths(archive, "retired"):
        if retention_unit(relative) not in records:
            continue
        origin = preserved_origin_path(f"{_ARCHIVE_PREFIX}{relative}")
        if origin is not None:
            origins.add(pathlib.PurePosixPath(origin))
    return frozenset(origins)


def sealed_tombstone(
    path: pathlib.Path,
) -> tuple[dict[str, Any], pathlib.PurePosixPath, str] | None:
    """Return a Tombstone's metadata, retired path and recovery commit, or None.

    This is the minimal contract a Tombstone must meet before it grants a
    current exemption: `type: archive/tombstone`, `status: sealed`, a safe
    `Retired Path`, and a `Recovery Commit` that is one exact commit OID.
    Anything else grants nothing and raises nothing.
    """

    if path.is_symlink() or not path.is_file():
        return None
    try:
        metadata, body = _frontmatter(path.read_text(encoding="utf-8"))
        retired = _safe_path(_code_value(_section(body, "Retired Path")))
        commit = _code_value(_section(body, "Recovery Commit"))
    except (OSError, UnicodeError, ValueError):
        return None
    if (
        metadata.get("type") != "archive/tombstone"
        or metadata.get("status") != "sealed"
        or retired is None
        or not recovery_commit_is_valid(commit)
    ):
        return None
    return metadata, retired, commit


def recorded_retired_paths(root: pathlib.Path) -> frozenset[pathlib.PurePosixPath]:
    """Return the origin paths Stage 98 records as approved retirements.

    A sealed Tombstone (see `sealed_tombstone`) records a withdrawal only when
    its retired path is a regular blob at its recovery commit; once the archive
    disposition model is adopted a Retention Catalog row for a `retired/` unit
    records one too. This is a reader, not a validator: a record that fails
    its contract or its blob proof grants no exemption and raises nothing.
    """

    root = pathlib.Path(root)
    candidates = [
        (retired, commit)
        for path in sorted((root / _ARCHIVE_PREFIX / "tombstones").glob("*/*.md"))
        if (record := sealed_tombstone(path)) is not None
        for _, retired, commit in (record,)
    ]
    recorded: set[pathlib.PurePosixPath] = set()
    try:
        proofs = verify_recovery_blobs_batch(candidates, repo_root=root)
    except (OSError, ValueError):
        proofs = ()
    recorded.update(proof.path for proof in proofs if proof.is_regular_blob)
    if archive_disposition_model(root) == ARCHIVE_MODEL_ADOPTED:
        try:
            recorded |= retention_catalog_retirements(root)
        except (OSError, ValueError):
            pass
    return frozenset(recorded)
