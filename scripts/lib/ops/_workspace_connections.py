"""Public, source-declared connection inventory orchestration and validation."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path, PurePosixPath
from typing import Any

from scripts.lib.document_governance.operations_catalog import (
    OperationsAuthorityError,
    read_bounded_regular,
)
from scripts.lib.ops._workspace_connection_sources import (
    ALLOWED_KINDS,
    ConnectionSourceError,
    DuplicateSourceKey,
    candidate_kind,
    extract_source,
    public_source_path,
)

SHA256 = re.compile(r"^[0-9a-f]{64}$")
SAFE_NAME = re.compile(r"^[A-Za-z0-9_.:@/-]+$")
PROVIDER_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,255}$")
ROW_KEYS = {
    "id",
    "source",
    "caller_roles",
    "provider",
    "port_contract",
    "auth_kind",
    "secret_refs",
    "disposition",
    "reason",
    "owner",
    "registration",
}
PORT_LOCATIONS = {
    "listener",
    "service_dns",
    "host_publication",
    "gateway_backend",
}
PORT_STATES = {"declared", "absent", "unpublished", "disabled", "unknown"}
AUTH_KINDS = {
    "none",
    "unknown",
    "named-user-secret-reference",
    "credential-reference",
}
DISPOSITIONS = {"adopted", "deferred", "unnecessary"}
EVIDENCE_LEVELS = {
    "source-declared",
    "provisioned-source",
    "fixture",
    "sdk-only",
    "inactive-workflow-source",
}
GAP_CODES = {
    "duplicate-key",
    "source-invalid",
    "endpoint-unresolved",
    "endpoint-port-invalid",
    "credential-bearing-endpoint-refused",
    "endpoint-query-refused",
}
SOURCE_RESULTS = {"extracted", "no-matching-connection", "partial", "gap"}


class ConnectionInventoryError(ValueError):
    """A safe connection census boundary error."""


def _safe_path(root: Path, relative: str) -> Path:
    if not public_source_path(relative):
        raise ConnectionInventoryError(
            "connection source is outside the public boundary"
        )
    candidate = root.joinpath(*PurePosixPath(relative).parts)
    current = root
    for part in PurePosixPath(relative).parts:
        current = current / part
        if current.is_symlink():
            raise ConnectionInventoryError("connection source is a symbolic link")
    return candidate


def _source_result(parsed: bool, gap_count: int, rows: list[dict[str, Any]]) -> str:
    if not parsed:
        return "gap"
    if rows and gap_count:
        return "partial"
    if rows:
        return "extracted"
    if gap_count:
        return "gap"
    return "no-matching-connection"


def _coverage(
    connections: list[dict[str, Any]], sources: list[dict[str, Any]]
) -> dict[str, int]:
    return {
        "candidate_sources": len(sources),
        "parsed_sources": sum(source["result"] != "gap" for source in sources),
        "extracted_sources": sum(
            source["result"] in {"extracted", "partial"} for source in sources
        ),
        "unhandled_sources": sum(
            source["result"] in {"gap", "partial"} for source in sources
        ),
        "connection_rows": len(connections),
    }


def inspect_connections(
    root: Path,
    files: list[dict[str, Any]],
    services: list[dict[str, Any]],
) -> dict[str, Any]:
    """Extract safe connection facts from bounded, public source files."""
    connections: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []
    gaps: list[dict[str, str]] = []
    for file_row in sorted(files, key=lambda item: str(item.get("path", ""))):
        source = file_row.get("path")
        kind = candidate_kind(source) if isinstance(source, str) else None
        if kind is None or file_row.get("state") != "HASHED":
            continue
        expected_sha = file_row.get("sha256")
        if not isinstance(expected_sha, str) or not SHA256.fullmatch(expected_sha):
            raise ConnectionInventoryError(
                "connection source has no valid public digest"
            )
        _safe_path(root, source)
        try:
            raw = read_bounded_regular(
                root,
                PurePosixPath(source),
                max_bytes=16 * 1024 * 1024,
            )
        except OperationsAuthorityError as exc:
            raise ConnectionInventoryError(
                "connection source could not be read safely"
            ) from exc
        if hashlib.sha256(raw).hexdigest() != expected_sha:
            raise ConnectionInventoryError("connection source changed during scan")

        parsed = True
        source_gaps: list[dict[str, str]] = []
        source_ref = {"path": source, "sha256": expected_sha}
        try:
            source_rows = extract_source(kind, raw, source_ref, services, source_gaps)
        except DuplicateSourceKey:
            parsed = False
            source_rows = []
            source_gaps = [{"source": source, "code": "duplicate-key"}]
        except ConnectionSourceError:
            parsed = False
            source_rows = []
            source_gaps = [{"source": source, "code": "source-invalid"}]
        connections.extend(source_rows)
        gaps.extend(source_gaps)
        sources.append(
            {
                "path": source,
                "sha256": expected_sha,
                "kind": kind,
                "result": _source_result(parsed, len(source_gaps), source_rows),
            }
        )

    gaps = [
        {"source": source, "code": code}
        for source, code in sorted(
            {(gap["source"], gap["code"]) for gap in gaps},
        )
    ]
    result = {
        "connections": sorted(connections, key=lambda row: row["id"]),
        "connection_sources": sources,
        "connection_gaps": gaps,
    }
    result["connection_coverage"] = _coverage(
        result["connections"], result["connection_sources"]
    )
    validate_connections(result, public_files=files)
    return result


def _validate_text(value: Any, field: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or not SAFE_NAME.fullmatch(value)
        or "://" in value
    ):
        raise ConnectionInventoryError(f"invalid connection {field}")
    return value


def _validate_row(row: Any, source_keys: set[tuple[str, str]]) -> None:
    if not isinstance(row, dict) or set(row) != ROW_KEYS:
        raise ConnectionInventoryError("connection row schema is not closed")
    _validate_text(row["id"], "id")
    provenance = row["source"]
    if not isinstance(provenance, dict) or set(provenance) != {"path", "sha256"}:
        raise ConnectionInventoryError("connection provenance schema is not closed")
    source = _validate_text(provenance["path"], "source")
    digest = provenance["sha256"]
    if not isinstance(digest, str) or not SHA256.fullmatch(digest):
        raise ConnectionInventoryError("invalid connection source digest")
    if (source, digest) not in source_keys:
        raise ConnectionInventoryError("connection provenance is not authoritative")
    callers = row["caller_roles"]
    if (
        not isinstance(callers, list)
        or not callers
        or len(callers) != len(set(callers))
    ):
        raise ConnectionInventoryError("invalid connection caller roles")
    for caller in callers:
        if not isinstance(caller, str) or not PROVIDER_NAME.fullmatch(caller):
            raise ConnectionInventoryError("invalid connection caller")
    provider = row["provider"]
    if provider is not None:
        if not isinstance(provider, str) or not PROVIDER_NAME.fullmatch(provider):
            raise ConnectionInventoryError("invalid connection provider")
    ports = row["port_contract"]
    if not isinstance(ports, dict) or set(ports) != PORT_LOCATIONS:
        raise ConnectionInventoryError("connection ports schema is not closed")
    for location, value in ports.items():
        if not isinstance(value, dict) or set(value) != {"state", "port"}:
            raise ConnectionInventoryError(f"invalid {location} port contract")
        if value["state"] not in PORT_STATES:
            raise ConnectionInventoryError(f"invalid {location} port state")
        port = value["port"]
        if port is not None and (
            not isinstance(port, int)
            or isinstance(port, bool)
            or not 1 <= port <= 65535
        ):
            raise ConnectionInventoryError(f"invalid {location} port")
    if row["auth_kind"] not in AUTH_KINDS:
        raise ConnectionInventoryError("invalid connection auth kind")
    refs = row["secret_refs"]
    if not isinstance(refs, list) or len(refs) != len(set(refs)):
        raise ConnectionInventoryError("invalid connection secret references")
    for ref in refs:
        _validate_text(ref, "secret reference")
        if "/" in ref or "\\" in ref:
            raise ConnectionInventoryError("secret reference must be a public name")
    if row["disposition"] not in DISPOSITIONS:
        raise ConnectionInventoryError("invalid connection disposition")
    _validate_text(row["reason"], "reason")
    _validate_text(row["owner"], "owner")
    registration = row["registration"]
    if (
        not isinstance(registration, dict)
        or set(registration) != {"level", "actual_state"}
        or registration["level"] not in EVIDENCE_LEVELS
        or registration["actual_state"] != "UNKNOWN"
    ):
        raise ConnectionInventoryError("invalid connection registration evidence")


def _authoritative_sources(
    public_files: list[dict[str, Any]],
) -> set[tuple[str, str]]:
    authoritative: set[tuple[str, str]] = set()
    for row in public_files:
        if not isinstance(row, dict):
            continue
        path = row.get("path")
        digest = row.get("sha256")
        if (
            row.get("state") == "HASHED"
            and isinstance(path, str)
            and candidate_kind(path) is not None
            and public_source_path(path)
            and isinstance(digest, str)
            and SHA256.fullmatch(digest)
        ):
            authoritative.add((path, digest))
    return authoritative


def _validate_sources(
    document: dict[str, Any], public_files: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    sources: dict[str, dict[str, Any]] = {}
    source_keys: set[tuple[str, str]] = set()
    for row in document["connection_sources"]:
        if not isinstance(row, dict) or set(row) != {
            "path",
            "sha256",
            "kind",
            "result",
        }:
            raise ConnectionInventoryError("connection source schema is not closed")
        path = _validate_text(row["path"], "source path")
        digest = row["sha256"]
        if (
            not public_source_path(path)
            or not isinstance(digest, str)
            or not SHA256.fullmatch(digest)
            or row["kind"] not in ALLOWED_KINDS
            or row["kind"] != candidate_kind(path)
            or row["result"] not in SOURCE_RESULTS
            or path in sources
            or (path, digest) in source_keys
        ):
            raise ConnectionInventoryError("invalid connection source provenance")
        sources[path] = row
        source_keys.add((path, digest))
    if source_keys != _authoritative_sources(public_files):
        raise ConnectionInventoryError("connection source census is incomplete")
    return sources


def _validate_gaps_and_results(
    document: dict[str, Any], sources: dict[str, dict[str, Any]]
) -> None:
    row_sources = {row["source"]["path"] for row in document["connections"]}
    gap_pairs: set[tuple[str, str]] = set()
    gap_sources: set[str] = set()
    for gap in document["connection_gaps"]:
        if not isinstance(gap, dict) or set(gap) != {"source", "code"}:
            raise ConnectionInventoryError("connection gap schema is not closed")
        source = _validate_text(gap["source"], "gap source")
        code = gap["code"]
        if (
            source not in sources
            or code not in GAP_CODES
            or (source, code) in gap_pairs
        ):
            raise ConnectionInventoryError("invalid connection gap provenance")
        gap_pairs.add((source, code))
        gap_sources.add(source)
    for path, source in sources.items():
        has_rows = path in row_sources
        has_gaps = path in gap_sources
        expected = (
            "partial"
            if has_rows and has_gaps
            else "extracted"
            if has_rows
            else "gap"
            if has_gaps
            else "no-matching-connection"
        )
        if source["result"] != expected:
            raise ConnectionInventoryError("connection source result is inconsistent")


def validate_connections(
    document: dict[str, Any],
    *,
    public_files: list[dict[str, Any]],
) -> bool:
    """Validate the closed connection inventory and bind it to public file rows."""
    required = {
        "connections",
        "connection_sources",
        "connection_gaps",
        "connection_coverage",
    }
    if not isinstance(document, dict) or set(document) != required:
        raise ConnectionInventoryError("connection inventory schema is not closed")
    if not all(
        isinstance(document[key], list)
        for key in ("connections", "connection_sources", "connection_gaps")
    ):
        raise ConnectionInventoryError("connection inventory collections must be lists")
    if not isinstance(public_files, list):
        raise ConnectionInventoryError("public file census must be a list")
    sources = _validate_sources(document, public_files)
    source_keys = {(path, row["sha256"]) for path, row in sources.items()}
    seen_ids: set[str] = set()
    for row in document["connections"]:
        _validate_row(row, source_keys)
        if row["id"] in seen_ids:
            raise ConnectionInventoryError("duplicate connection id")
        seen_ids.add(row["id"])
    _validate_gaps_and_results(document, sources)
    if document["connection_coverage"] != _coverage(
        document["connections"], document["connection_sources"]
    ):
        raise ConnectionInventoryError("connection coverage does not match inventory")
    return True
