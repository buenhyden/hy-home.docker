"""Bounded immutable public manifest contracts; no import-time external I/O."""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime
from types import MappingProxyType
from typing import Any, Protocol

MAX_BYTES = 1024 * 1024
MAX_RECORDS = 5000
MAX_DEPTH = 32
FORBIDDEN_SEGMENTS = frozenset(
    ("secret", "secrets", "password", "passwords", "credentials", "tokens")
)
SOURCES = MappingProxyType(
    {
        "hy-home.docker": ("buenhyden/hy-home.docker", "main"),
        "hy-home.k8s": ("buenhyden/hy-home.k8s", "main"),
        "Project-Template": ("buenhyden/Project-Template", "dev"),
        "blog-data": ("buenhyden/blog-data", "dev"),
    }
)
_FIELDS = frozenset(
    ("schema_version", "source", "repository", "ref", "captured_at", "records")
)
_ROW_FIELDS = frozenset(("path", "revision", "content_sha256", "title"))
_TIMESTAMP = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|[+-][0-9]{2}:[0-9]{2})"
)


class ContractError(ValueError):
    """Fixed public failure code, never an input payload."""


@dataclass(frozen=True)
class Manifest:
    source: str
    repository: str
    ref: str
    captured_at: datetime
    records: tuple[Mapping[str, str], ...]


class Store(Protocol):
    def read_input(self, key: str) -> bytes: ...

    def put_verified(self, key: str, body: bytes) -> None:
        """Upload/reuse exact bytes and read them back before returning."""
        ...


class Publisher(Protocol):
    def publish(
        self, manifest: Manifest, identifier: str, digest: str, artifact: str
    ) -> str: ...


def _raw(raw: bytes) -> None:
    if not isinstance(raw, bytes) or not 1 <= len(raw) <= MAX_BYTES:
        raise ContractError("input_size")


def _source(source: str) -> None:
    if not isinstance(source, str) or source not in SOURCES:
        raise ContractError("source_not_allowed")


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ContractError("duplicate_json_key")
    return result


def _constant(_: str) -> None:
    raise ContractError("nonfinite_json")


def _depth(text: str) -> None:
    depth, quoted, escaped = 0, False, False
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in "[{":
            depth += 1
            if depth > MAX_DEPTH:
                raise ContractError("json_depth")
        elif char in "]}":
            depth -= 1


def _finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ContractError("nonfinite_json")
    if isinstance(value, dict):
        for child in value.values():
            _finite(child)
    elif isinstance(value, list):
        for child in value:
            _finite(child)


def _decode(raw: bytes) -> Any:
    try:
        text = raw.decode("utf-8")
        _depth(text)
        value = json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError):
        raise ContractError("invalid_json") from None
    _finite(value)
    return value


def _control(text: str) -> bool:
    return any(ord(char) < 32 or 127 <= ord(char) <= 159 for char in text)


def _captured(value: Any) -> datetime:
    if not isinstance(value, str) or not _TIMESTAMP.fullmatch(value):
        raise ContractError("captured_at")
    try:
        captured = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return captured.astimezone(UTC)
    except (ValueError, OverflowError):
        raise ContractError("captured_at") from None


def _row(value: Any) -> Mapping[str, str]:
    if not isinstance(value, dict) or set(value) != _ROW_FIELDS:
        raise ContractError("record_fields")
    if any(not isinstance(item, str) for item in value.values()):
        raise ContractError("record_type")
    path = value["path"]
    parts = path.split("/")
    if (
        not 1 <= len(path) <= 512
        or path.startswith("/")
        or "\\" in path
        or _control(path)
        or any(
            part in ("", ".", "..")
            or part.startswith(".")
            or part.lower() in FORBIDDEN_SEGMENTS
            for part in parts
        )
    ):
        raise ContractError("record_path")
    if not re.fullmatch(r"[0-9a-f]{40}", value["revision"]):
        raise ContractError("revision")
    if not re.fullmatch(r"[0-9a-f]{64}", value["content_sha256"]):
        raise ContractError("content_hash")
    if not 1 <= len(value["title"]) <= 256 or _control(value["title"]):
        raise ContractError("title")
    return MappingProxyType(dict(value))


def parse_manifest(raw: bytes) -> Manifest:
    _raw(raw)
    value = _decode(raw)
    if not isinstance(value, dict) or set(value) != _FIELDS:
        raise ContractError("manifest_fields")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ContractError("schema_version")
    _source(value["source"])
    if (value["repository"], value["ref"]) != SOURCES[value["source"]]:
        raise ContractError("source_ref_mismatch")
    captured = _captured(value["captured_at"])
    rows = value["records"]
    if not isinstance(rows, list) or not 1 <= len(rows) <= MAX_RECORDS:
        raise ContractError("record_count")
    records = tuple(_row(row) for row in rows)
    if len({row["path"] for row in records}) != len(records):
        raise ContractError("duplicate_path")
    return Manifest(
        value["source"],
        value["repository"],
        value["ref"],
        captured,
        tuple(sorted(records, key=lambda row: row["path"])),
    )


def run_id(source: str, raw: bytes) -> str:
    _source(source)
    _raw(raw)
    digest = hashlib.sha256(raw).hexdigest()
    return hashlib.sha256(f"{source}:{digest}".encode()).hexdigest()


def object_key(source: str, business_date: str) -> str:
    _source(source)
    if not isinstance(business_date, str):
        raise ContractError("business_date")
    try:
        parsed = date.fromisoformat(business_date)
    except ValueError:
        raise ContractError("business_date") from None
    if parsed.isoformat() != business_date:
        raise ContractError("business_date")
    return f"manifest-input/{source}/{business_date}.json"


def _external(operation, code: str):
    try:
        return operation()
    except Exception:
        raise ContractError(code) from None


def ingest(
    store: Store, db: Publisher, source: str, business_date: str
) -> dict[str, str | int]:
    key = object_key(source, business_date)
    raw = _external(lambda: store.read_input(key), "input_read_failed")
    manifest = parse_manifest(raw)
    if (
        manifest.source != source
        or manifest.captured_at.date().isoformat() != business_date
    ):
        raise ContractError("partition_mismatch")
    identifier = run_id(source, raw)
    digest = hashlib.sha256(raw).hexdigest()
    artifact = f"manifest-validated/{source}/{identifier}.json"
    _external(lambda: store.put_verified(artifact, raw), "artifact_verification_failed")
    status = _external(
        lambda: db.publish(manifest, identifier, digest, artifact), "publication_failed"
    )
    if not isinstance(status, str) or status not in (
        "published",
        "historical",
        "replayed",
    ):
        raise ContractError("publication_status")
    return {"run_id": identifier, "status": status, "records": len(manifest.records)}
