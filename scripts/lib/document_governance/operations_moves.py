"""Pure, caller-reviewed Stage05 mapping checks; no move or approval authority.

Source admission uses caller-owned current Registry profiles. Numbered family
routes retain the original flat identity and use the registered domain paths.
This unit does not classify subjects from numbers or content.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from scripts.lib.document_governance.frontmatter import (
    FrontmatterError,
    frontmatter_record_from_text,
)
from scripts.lib.document_governance.taxonomy import (
    classify_path,
    validate_stable_identity,
)

_ROOT = ("docs", "05.operations")
_FAMILIES = {"guides": "guide", "policies": "policy", "runbooks": "runbook"}
_DOMAIN = re.compile(r"[0-9]{2}-[a-z0-9][a-z0-9-]*")


class MoveError(ValueError):
    """A refused public mapping, with a stable diagnostic code."""

    def __init__(self, code: str, path: str) -> None:
        self.code = code
        self.path = path
        super().__init__(f"{code}: {path}")


@dataclass(frozen=True)
class DocumentInput:
    """Already-read public document bytes represented as UTF-8 text."""

    path: str
    text: str


@dataclass(frozen=True)
class ReviewedMove:
    """Caller classification bound to exact source path and stable artifact ID.

    This records a proposed semantic decision, not an authenticated approval.
    """

    source: str
    artifact_id: str
    target: str
    domain: str
    lab: bool


@dataclass(frozen=True)
class MoveEntry:
    """Immutable proposal result; registration flags describe current profiles."""

    source: str
    artifact_id: str | None
    target: str | None
    domain: str | None
    state: str
    reason: str
    source_registered: bool = False
    target_registered: bool = False


@dataclass(frozen=True)
class MovePlan:
    """Results and populated folder obligations, not generated README content."""

    entries: tuple[MoveEntry, ...]
    required_readme_folders: tuple[str, ...]


def _path(raw: str) -> PurePosixPath:
    # PurePosixPath silently normalizes dot and empty segments; reject raw first.
    if (
        not isinstance(raw, str)
        or not raw
        or raw.startswith("/")
        or "\\" in raw
        or any(ord(char) < 32 or ord(char) == 127 for char in raw)
        or any(part in {"", ".", ".."} for part in raw.split("/"))
    ):
        raise MoveError("unsafe-path", str(raw))
    return PurePosixPath(raw)


def _operation_path(path: PurePosixPath) -> bool:
    return (
        path.parts[:2] == _ROOT
        and len(path.parts) >= 4
        and path.parts[2] in _FAMILIES
        and path.name != "README.md"
    )


def _source_identity(
    doc: DocumentInput,
    path: PurePosixPath,
    profiles: Mapping[str, Mapping[str, object]],
    domains: frozenset[str],
) -> tuple[str, str, bool]:
    if len(path.parts) not in {4, 5}:
        raise MoveError("source-contract", doc.path)
    if len(path.parts) == 5 and path.parts[3] not in domains:
        raise MoveError("unknown-domain", doc.path)
    flat = PurePosixPath(*path.parts[:3], path.name)
    role = _FAMILIES[path.parts[2]]
    if classify_path(flat, profiles) != role:
        raise MoveError("source-profile-invalid", doc.path)
    try:
        record = frontmatter_record_from_text(Path(doc.path), doc.text)
    except FrontmatterError as error:
        raise MoveError(error.code, doc.path) from error
    if not record.frontmatter_present:
        raise MoveError("frontmatter-missing", doc.path)
    if record.metadata.get("type") != profiles[role].get("type"):
        raise MoveError("type-path-mismatch", doc.path)
    findings = validate_stable_identity(
        flat, record.metadata, profiles, profile_id=role
    )
    if findings:
        raise MoveError(findings[0].code, doc.path)
    return (
        str(record.metadata["artifact_id"]),
        role,
        classify_path(path, profiles) == role,
    )


def _review_rows(
    rows: Sequence[ReviewedMove],
    source_keys: Mapping[str, str],
    domains: frozenset[str],
) -> dict[str, ReviewedMove]:
    result: dict[str, ReviewedMove] = {}
    for row in rows:
        source = _path(row.source)
        _path(row.target)
        if row.source.casefold() in {key.casefold() for key in result}:
            raise MoveError("review-source-collision", row.source)
        if row.source not in source_keys.values():
            raise MoveError("review-source-missing", row.source)
        if not _operation_path(source):
            raise MoveError("review-source-not-operation", row.source)
        if row.domain not in domains:
            raise MoveError("unknown-domain", row.source)
        if not isinstance(row.lab, bool) or row.lab != (row.domain == "15-labs"):
            raise MoveError("lab-domain-mismatch", row.source)
        result[row.source] = row
    return result


def _entry(
    doc: DocumentInput,
    path: PurePosixPath,
    row: ReviewedMove | None,
    identity: tuple[str, str, bool],
    profiles: Mapping[str, Mapping[str, object]],
) -> MoveEntry:
    artifact_id, role, registered = identity
    if row is None:
        return MoveEntry(
            doc.path,
            artifact_id,
            None,
            None,
            "REVIEW_REQUIRED",
            "semantic-decision-missing",
            registered,
        )
    if row.artifact_id != artifact_id:
        raise MoveError("review-id-mismatch", doc.path)
    expected = PurePosixPath(*path.parts[:3], row.domain, path.name)
    if row.target != str(expected):
        raise MoveError("target-contract", row.target)
    if len(path.parts) == 5 and path.parts[3] != row.domain:
        return MoveEntry(
            doc.path,
            artifact_id,
            row.target,
            row.domain,
            "REVIEW_REQUIRED",
            "existing-domain-conflict",
            registered,
            classify_path(expected, profiles) == role,
        )
    state = "ALREADY_ARRANGED" if path == expected else "MOVE"
    return MoveEntry(
        doc.path,
        artifact_id,
        row.target,
        row.domain,
        state,
        "caller-reviewed-proposal",
        registered,
        classify_path(expected, profiles) == role,
    )


def preflight_operations_moves(
    documents: Sequence[DocumentInput],
    reviewed_moves: Sequence[ReviewedMove],
    *,
    profiles: Mapping[str, Mapping[str, object]],
    domains: Sequence[str],
) -> MovePlan:
    """Refuse unsafe/conflicting maps; return immutable planning obligations.

    No filesystem discovery, I/O, subprocess, service or approval validation is
    performed. The caller freezes input hashes, owns the semantic decisions,
    checks content/links/anchors and obtains writer leases separately.
    """
    for domain in domains:
        if not isinstance(domain, str) or _DOMAIN.fullmatch(domain) is None:
            raise MoveError("invalid-domain", str(domain))
    allowed = frozenset(domains)
    source_keys: dict[str, str] = {}
    paths: dict[str, PurePosixPath] = {}
    for doc in documents:
        path = _path(doc.path)
        folded = doc.path.casefold()
        if folded in source_keys:
            raise MoveError("source-collision", doc.path)
        source_keys[folded] = doc.path
        paths[doc.path] = path
    rows = _review_rows(reviewed_moves, source_keys, allowed)
    identities: set[str] = set()
    targets: set[str] = set()
    folders: set[str] = set()
    entries: list[MoveEntry] = []
    for doc in documents:
        path = paths[doc.path]
        if not _operation_path(path):
            entries.append(
                MoveEntry(
                    doc.path, None, None, None, "OUT_OF_SCOPE", "not-operation-document"
                )
            )
            continue
        identity = _source_identity(doc, path, profiles, allowed)
        if identity[0] in identities:
            raise MoveError("artifact-id-collision", doc.path)
        identities.add(identity[0])
        entry = _entry(doc, path, rows.get(doc.path), identity, profiles)
        if entry.target is not None:
            folded = entry.target.casefold()
            if folded in targets or (
                folded in source_keys and source_keys[folded] != doc.path
            ):
                raise MoveError("target-collision", entry.target)
            targets.add(folded)
            if entry.state != "REVIEW_REQUIRED":
                target = PurePosixPath(entry.target)
                folders.update(
                    str(PurePosixPath(*target.parts[:length])) for length in (2, 3, 4)
                )
        entries.append(entry)
    return MovePlan(tuple(entries), tuple(sorted(folders)))
