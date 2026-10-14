"""Public synthetic selection and separately controller-admitted W48 copy API.

FrozenAuthority and the public CLI stay offline. The private executor requires
concrete out-of-band controller admission; no record authenticates itself.
"""

from __future__ import annotations

import json
import os
import re
import time
from collections.abc import Callable
from contextlib import ExitStack
from dataclasses import asdict, dataclass
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from scripts.lib.ops._openbao_copy_io import (
    MAX_BYTES,
    MigrationError,
    ProtectedInput,
    hold_input,
    token_text,
    validate_input,
    verified_context,
)
from scripts.lib.ops._openbao_copy_transport import (
    CopyBudget,
    CopyTransport,
    validate_endpoint,
)

MAX_DEPTH = 12
MAX_NODES = 4096
PACKAGE = (
    Path(__file__).resolve().parents[3] / "infra/03-security/openbao/consumer-migration"
)


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


@dataclass(frozen=True, slots=True)
class CopyPlan:
    """Concrete runtime inputs, not an approval or a public wave/receipt schema."""

    consumer: str
    selections: tuple[CatalogSelection, ...]
    sources: tuple[ProtectedInput, ...]
    origin: str
    connect_ip: str
    copy_token: ProtectedInput
    metadata_token: ProtectedInput
    ca: ProtectedInput
    ca_sha256: str
    budget: CopyBudget


@dataclass(frozen=True, slots=True)
class CopyItem:
    """Observed version and POST provenance remain separate value-free fields."""

    id: str
    status: str
    kv_version: int | None
    write_attempted: bool = False
    accepted_version: int | None = None


@dataclass(frozen=True, slots=True)
class CopyReport:
    """Fixed value-free runtime result; no hashes derived from private values."""

    status: str
    items: tuple[CopyItem, ...]
    diagnostic: str | None


def _validate_copy_plan(plan):
    if (
        type(plan) is not CopyPlan
        or not isinstance(plan.consumer, str)
        or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", plan.consumer)
        or type(plan.selections) is not tuple
        or not 1 <= len(plan.selections) <= 32
        or type(plan.sources) is not tuple
        or len(plan.sources) != len(plan.selections)
        or not isinstance(plan.ca_sha256, str)
        or not re.fullmatch(r"[0-9a-f]{64}", plan.ca_sha256)
    ):
        raise MigrationError("copy_plan_invalid")
    validate_endpoint(plan.origin, plan.connect_ip, plan.budget)
    validate_input(plan.copy_token)
    validate_input(plan.metadata_token)
    validate_input(plan.ca, ca=True)
    if plan.copy_token == plan.metadata_token:
        raise MigrationError("copy_token_scope_not_separated")
    ids, destinations, sources = frozenset(), frozenset(), frozenset()
    for row, reference in zip(plan.selections, plan.sources, strict=True):
        if type(row) is not CatalogSelection or not re.fullmatch(
            r"[A-Z][A-Z0-9]{1,15}-[0-9]{3}", row.id
        ):
            raise MigrationError("copy_selection_invalid")
        _eligible(row, row.id, plan.consumer)
        validate_input(reference)
        destination, source = (
            (row.mount, row.kv_path),
            (reference.root, reference.relative),
        )
        if (
            row.source_path != reference.relative
            or row.id in ids
            or destination in destinations
            or source in sources
        ):
            raise MigrationError("copy_selection_invalid")
        ids, destinations, sources = (
            ids | {row.id},
            destinations | {destination},
            sources | {source},
        )

    # A root/path spelling is not a role boundary: compare absolute bindings.
    references = (*plan.sources, plan.copy_token, plan.metadata_token, plan.ca)
    paths = tuple(reference.root + "/" + reference.relative for reference in references)
    if len(frozenset(paths)) != len(paths):
        raise MigrationError("copy_input_role_alias")


def _check_role_inodes(inputs):
    identities = tuple(
        (info.st_dev, info.st_ino)
        for info in (os.fstat(held.descriptor) for held in inputs)
    )
    if len(frozenset(identities)) != len(identities):
        raise MigrationError("copy_input_role_alias")


def _active(metadata):
    if (
        not isinstance(metadata, dict)
        or metadata.get("deletion_time") != ""
        or metadata.get("destroyed") is not False
    ):
        raise MigrationError("copy_version_unverifiable")


def _data(document):
    try:
        envelope = document["data"]
        metadata, fields = envelope["metadata"], envelope["data"]
        _active(metadata)
        version = metadata["version"]
        if (
            type(version) is not int
            or version <= 0
            or type(fields) is not dict
            or set(fields) != {"value"}
            or type(fields["value"]) is not str
        ):
            raise ValueError
        return fields["value"].encode("utf-8"), version
    except (KeyError, TypeError, ValueError, UnicodeError):
        raise MigrationError("copy_version_unverifiable") from None


def _metadata(document):
    try:
        data = document["data"]
        version = data["current_version"]
        versions = data["versions"]
        if type(version) is not int or version <= 0 or type(versions) is not dict:
            raise ValueError
        _active(versions[str(version)])
        return version
    except (KeyError, TypeError, ValueError):
        raise MigrationError("copy_version_unverifiable") from None


def _mount_config(document):
    data = document.get("data")
    if (
        not isinstance(data, dict)
        or type(data.get("max_versions")) is not int
        or data["max_versions"] < 0
        or type(data.get("cas_required")) is not bool
        or not isinstance(data.get("delete_version_after"), str)
    ):
        raise MigrationError("copy_mount_unverifiable")


def _readback(transport, path, meta_path, copy_token, metadata_token, source):
    status, before = transport.request("GET", meta_path, metadata_token)
    if status != 200:
        raise MigrationError("copy_readback_unverifiable")
    version = _metadata(before)
    status, document = transport.request("GET", path, copy_token)
    if status != 200:
        raise MigrationError("copy_readback_unverifiable")
    data, actual = _data(document)
    status, after = transport.request("GET", meta_path, metadata_token)
    if status != 200 or version != actual or _metadata(after) != version:
        raise MigrationError("copy_readback_unverifiable")
    return ("RECONCILED_EQUAL" if data == source else "CONFLICT"), version


def _copy_one(row, held, transport, copy_token, metadata_token, check_inputs):
    path, meta_path = (
        f"/v1/{row.mount}/data/{row.kv_path}",
        f"/v1/{row.mount}/metadata/{row.kv_path}",
    )
    status, document = transport.request("GET", path, copy_token)
    if status == 200:
        data, version = _data(document)
        status, metadata = transport.request("GET", meta_path, metadata_token)
        if status != 200 or _metadata(metadata) != version:
            raise MigrationError("copy_version_unverifiable")
        return CopyItem(row.id, "NOOP" if data == held.data else "CONFLICT", version)
    if status != 404 or document != {"errors": []}:
        raise MigrationError("copy_absence_unverifiable")
    status, config = transport.request("GET", f"/v1/{row.mount}/config", metadata_token)
    if status != 200:
        raise MigrationError("copy_mount_unverifiable")
    _mount_config(config)
    status, metadata = transport.request("GET", meta_path, metadata_token)
    if status != 404 or metadata != {"errors": []}:
        raise MigrationError("copy_absence_unverifiable")
    check_inputs()
    accepted_version = None
    try:
        status, response = transport.request(
            "POST",
            path,
            copy_token,
            {"options": {"cas": 0}, "data": {"value": held.data.decode("utf-8")}},
        )
        if status == 200:
            entry = response.get("data")
            _active(entry)
            if entry.get("version") == 1 and type(entry.get("version")) is int:
                accepted_version = 1
        outcome, version = _readback(
            transport, path, meta_path, copy_token, metadata_token, held.data
        )
        if accepted_version == version and outcome == "RECONCILED_EQUAL":
            outcome = "CREATED"
        return CopyItem(row.id, outcome, version, True, accepted_version)
    except Exception:
        # A lost POST is never retried; reconcile once within the original budget.
        try:
            outcome, version = _readback(
                transport, path, meta_path, copy_token, metadata_token, held.data
            )
            return CopyItem(row.id, outcome, version, True, accepted_version)
        except Exception:
            return CopyItem(row.id, "UNRESOLVED", None, True, accepted_version)


def _run_copy(plan, stack):
    deadline = time.monotonic() + plan.budget.total
    held_sources = tuple(hold_input(reference, stack) for reference in plan.sources)
    copy_token = hold_input(plan.copy_token, stack)
    metadata_token = hold_input(plan.metadata_token, stack)
    ca = hold_input(plan.ca, stack, ca=True)
    all_inputs = (*held_sources, copy_token, metadata_token, ca)
    _check_role_inodes(all_inputs)
    # UTF-8 JSON strings preserve bytes round-trip; refuse binary conversion.
    try:
        if any(
            source.data.decode("utf-8").encode("utf-8") != source.data
            for source in held_sources
        ):
            raise UnicodeError
    except UnicodeError:
        raise MigrationError("copy_source_encoding_unsupported") from None
    copy_text, metadata_text = token_text(copy_token), token_text(metadata_token)
    if copy_text == metadata_text:
        raise MigrationError("copy_token_scope_not_separated")
    context = verified_context(ca, plan.ca_sha256)

    def check_inputs():
        for held in all_inputs:
            held.check()

    paths = tuple(
        path
        for row in plan.selections
        for path in (
            f"/v1/{row.mount}/data/{row.kv_path}",
            f"/v1/{row.mount}/metadata/{row.kv_path}",
            f"/v1/{row.mount}/config",
        )
    )
    transport = CopyTransport(
        plan.origin,
        plan.connect_ip,
        plan.budget,
        context,
        paths,
        deadline,
        check_inputs,
    )
    items = ()
    for row, held in zip(plan.selections, held_sources, strict=True):
        try:
            check_inputs()
            item = _copy_one(
                row, held, transport, copy_text, metadata_text, check_inputs
            )
            try:
                check_inputs()
            except Exception:
                item = CopyItem(
                    row.id,
                    "UNRESOLVED",
                    item.kv_version,
                    item.write_attempted,
                    item.accepted_version,
                )
        except Exception:
            item = CopyItem(row.id, "UNRESOLVED", None)
        items = (*items, item)
        if item.status not in {"CREATED", "NOOP", "RECONCILED_EQUAL"}:
            partial = any(
                item.write_attempted or item.status in {"CREATED", "RECONCILED_EQUAL"}
                for item in items
            )
            return CopyReport(
                "PARTIAL" if partial else "BLOCKED", items, "copy_wave_stopped"
            )
    return CopyReport("COMPLETE", items, None)


def _cleanup_failure(report):
    partial = report.status == "PARTIAL" or any(
        item.write_attempted for item in report.items
    )
    return CopyReport(
        "PARTIAL" if partial else "BLOCKED", report.items, "copy_cleanup_failed"
    )


def execute_copy(
    plan: CopyPlan, *, authorize: Callable[[CopyPlan], bool]
) -> CopyReport:
    """Run only after trusted controller admission; records cannot authorize this.

    The controller must resolve the current trusted user/native permission origin,
    bind the complete P02 source/catalog and accepted P01 identity/short TTL/ACL/
    mount/CA/consumer/recovery facts to this exact plan, then return literal True.
    No public schema, FrozenAuthority, JSON or boolean field is an authenticator.
    """
    report = None
    try:
        _validate_copy_plan(plan)
        if not callable(authorize):
            raise MigrationError("copy_not_authorized")
        try:
            admitted = authorize(plan)
        except Exception:
            raise MigrationError("copy_not_authorized") from None
        if admitted is not True:
            raise MigrationError("copy_not_authorized")
        with ExitStack() as stack:
            report = _run_copy(plan, stack)
            return report
    except MigrationError as error:
        if report is not None:
            return _cleanup_failure(report)
        return CopyReport("BLOCKED", (), str(error))
    except Exception:
        if report is not None:
            return _cleanup_failure(report)
        return CopyReport("BLOCKED", (), "copy_executor_failed")
