"""Public selection and W48 synthetic decisions; no production or private I/O.

The injected projection remains test-only; P02 API compatibility is checked offline.
Structural validation supplies neither authorization nor native acceptance.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

MAX_BYTES = 131072
MAX_DEPTH = 12
MAX_NODES = 4096
PACKAGE = (
    Path(__file__).resolve().parents[3] / "infra/03-security/openbao/consumer-migration"
)


class MigrationError(ValueError):
    """Fixed public diagnostic; never include candidate or adapter payloads."""


@dataclass(frozen=True)
class CatalogBinding:
    """Hashes of public catalog/schema/API bytes, supplied by the caller."""

    revision: str
    schema_version: str
    catalog_sha256: str
    schema_sha256: str
    source_sha256: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class CatalogSelection:
    """Provisional P02-shaped public projection, never a second catalog."""

    id: str
    scope: str
    classification: str
    action: str
    disposition: str
    consumer_status: str
    consumers: tuple[str, ...]
    alias_of: str | None
    source_path: str | None
    destination_status: str
    mount: str | None
    kv_path: str | None
    field: str | None


@dataclass(frozen=True)
class FrozenAuthority:
    """Caller-owned synthetic boundary, separate from candidate bindings."""

    binding: CatalogBinding
    lookup: Callable[[str], CatalogSelection | None]


@dataclass(frozen=True, slots=True)
class SyntheticKvObservation:
    """Declared test metadata, not an authenticated probe or byte comparison."""

    data_state: str
    metadata_state: str
    kv_version: int | None


@dataclass(frozen=True, slots=True)
class SyntheticCopyDecision:
    """Hypothetical decision, never an approval, command or migration receipt."""

    status: str
    kv_version: int | None
    cas: int | None


def _validate_synthetic_observation(observation):
    if type(observation) is not SyntheticKvObservation:
        raise MigrationError("synthetic_observation_invalid")
    if (
        type(observation.data_state) is not str
        or observation.data_state not in {"not_found", "equal", "different", "unknown"}
        or type(observation.metadata_state) is not str
        or observation.metadata_state
        not in {
            "never_created",
            "present",
            "soft_deleted",
            "destroyed",
            "unknown",
            "forbidden",
            "mount_missing",
        }
        or (
            observation.kv_version is not None
            and (type(observation.kv_version) is not int or observation.kv_version <= 0)
        )
    ):
        raise MigrationError("synthetic_observation_invalid")


def decide_synthetic_copy(
    observation: SyntheticKvObservation, *, phase: str
) -> SyntheticCopyDecision:
    """Model declared states only; cannot read, compare, write, retry or approve."""
    if type(phase) is not str or phase not in {
        "pre_write",
        "ambiguous_write",
        "cas_race",
    }:
        raise MigrationError("synthetic_copy_phase_invalid")
    _validate_synthetic_observation(observation)
    if (
        phase == "pre_write"
        and observation.data_state == "not_found"
        and observation.metadata_state == "never_created"
        and observation.kv_version is None
    ):
        return SyntheticCopyDecision("WOULD_CREATE", None, 0)
    if observation.metadata_state == "present" and observation.kv_version is not None:
        if observation.data_state == "equal":
            status = "WOULD_NOOP" if phase == "pre_write" else "RECONCILED_EQUAL"
            return SyntheticCopyDecision(status, observation.kv_version, None)
        if observation.data_state == "different":
            return SyntheticCopyDecision("CONFLICT", observation.kv_version, None)
    return SyntheticCopyDecision("UNRESOLVED", None, None)


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise MigrationError("duplicate_json_key")
        result = {**result, key: value}
    return result


def _nonfinite(_):
    raise MigrationError("nonfinite_json")


def _bounded(document):
    pending = [(document, 0)]
    count = 0
    while pending:
        node, depth = pending.pop()
        count += 1
        if count > MAX_NODES or depth > MAX_DEPTH:
            raise MigrationError("public_input_bounds")
        if isinstance(node, dict):
            pending.extend((value, depth + 1) for value in node.values())
        elif isinstance(node, list):
            pending.extend((value, depth + 1) for value in node)


def parse_public_json(raw: bytes) -> dict:
    if not isinstance(raw, bytes) or len(raw) > MAX_BYTES:
        raise MigrationError("public_input_size")
    try:
        document = json.loads(raw, object_pairs_hook=_unique, parse_constant=_nonfinite)
    except (ValueError, UnicodeError, RecursionError) as error:
        if isinstance(error, MigrationError):
            raise error from None
        raise MigrationError("public_input_json") from None
    if not isinstance(document, dict):
        raise MigrationError("public_input_object")
    _bounded(document)
    return document


def _schema(kind):
    if kind not in {"wave", "receipt"}:
        raise MigrationError("public_contract_kind")
    try:
        schema = json.loads((PACKAGE / f"{kind}.schema.json").read_bytes())
        Draft202012Validator.check_schema(schema)
    except (OSError, ValueError, SchemaError):
        raise MigrationError("public_schema_invalid") from None
    return schema


def validate_public(kind: str, document: dict) -> None:
    """Check shape only; PASS never authorizes a pilot or a state transition."""
    _bounded(document)
    try:
        Draft202012Validator(_schema(kind)).validate(document)
    except (ValidationError, TypeError):
        raise MigrationError("public_contract_invalid") from None
    if kind == "receipt":
        identifiers = tuple(item["id"] for item in document["items"])
        if len(set(identifiers)) != len(identifiers):
            raise MigrationError("duplicate_receipt_id")


def _authority(authority):
    if (
        type(authority) is not FrozenAuthority
        or type(authority.binding) is not CatalogBinding
        or not callable(authority.lookup)
    ):
        raise MigrationError("invalid_authority")
    binding = authority.binding.as_dict()
    try:
        Draft202012Validator(_schema("wave")["$defs"]["catalog"]).validate(binding)
    except ValidationError:
        raise MigrationError("invalid_authority_binding") from None
    return binding


def _path(value, prefix):
    if not isinstance(value, str) or len(value) > 256 or not value.startswith(prefix):
        raise MigrationError("unsafe_catalog_path")
    if any(
        not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", part)
        or part in {"labs", ".", ".."}
        for part in value.split("/")
    ):
        raise MigrationError("unsafe_catalog_path")


def _eligible(row, identifier, consumer):
    if type(row) is not CatalogSelection or row.id != identifier:
        raise MigrationError("unknown_catalog_id")
    if row.alias_of is not None or identifier.startswith("LAB-") or row.scope != "root":
        raise MigrationError("ineligible_catalog_id")
    if (
        row.classification != "kv_static"
        or row.action != "IMPLEMENT"
        or row.disposition != "ACTIVE_KEEP"
        or row.consumer_status != "DECLARED"
        or row.destination_status != "APPROVED"
        or row.field != "value"
    ):
        raise MigrationError("catalog_copy_not_approved")
    if (
        type(row.consumers) is not tuple
        or any(not isinstance(item, str) for item in row.consumers)
        or consumer not in row.consumers
        or len(set(row.consumers)) != len(row.consumers)
    ):
        raise MigrationError("unresolved_catalog_consumer")
    _path(row.source_path, "secrets/")
    _path(row.kv_path, "hy-home/")
    if (
        not isinstance(row.mount, str)
        or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", row.mount)
        or row.mount in {"sys", "auth", "identity"}
    ):
        raise MigrationError("unsafe_catalog_mount")
    return row


def select_wave(
    document: dict, authority: FrozenAuthority
) -> tuple[CatalogSelection, ...]:
    """Select synthetic public projections; never open a source or contact Bao."""
    validate_public("wave", document)
    expected = _authority(authority)
    if document["catalog"] != expected:
        raise MigrationError("catalog_binding_mismatch")
    selected = ()
    destinations = frozenset()
    for identifier in document["secret_ids"]:
        try:
            row = authority.lookup(identifier)
        except Exception:
            raise MigrationError("catalog_adapter_failed") from None
        row = _eligible(row, identifier, document["consumer"])
        destination = (row.mount, row.kv_path)
        if destination in destinations:
            raise MigrationError("duplicate_destination")
        destinations = destinations | {destination}
        selected = (*selected, row)
    return selected
