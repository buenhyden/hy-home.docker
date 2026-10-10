"""Pure synthetic Wiki preparation validation with fixed, input-free errors."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource

from scripts.lib.ops.wiki_preparation_semantics import (
    PreparationError,
    _require,
    _valid_versions,
    validate_semantics,
)

KINDS = frozenset(
    {"consumer-manifest", "source-artifact", "job-outbox-handoff", "blog-data-handoff"}
)


def _deny_external(uri: str):
    raise NoSuchResource(ref=uri)


def _hash(document: object) -> str:
    payload = json.dumps(
        document, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _schema(kind: str, document: Mapping, schemas: Mapping) -> None:
    _require(kind in KINDS and kind in schemas, "unknown preparation contract")
    try:
        resources = [
            (uri, Resource.from_contents(value))
            for uri, value in schemas.items()
            if uri.startswith("urn:")
        ]
        registry = Registry(retrieve=_deny_external).with_resources(resources)
        schema = schemas[kind]
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(
            schema, registry=registry, format_checker=FormatChecker()
        )
        _require(not any(validator.iter_errors(document)), "schema violation")
    except PreparationError:
        raise
    except Exception:
        raise PreparationError("unavailable or invalid schema reference") from None


SET_LISTS = frozenset(
    {
        "sources",
        "paths",
        "selected",
        "candidates",
        "allowed_paths",
        "write_set",
        "permissions",
        "valkey_commands",
        "roles",
        "egress",
        "metric_labels",
        "disabled_by_design",
        "readers",
        "enforcement",
        "secret_refs",
        "allowed_networks",
    }
)


def _canonical(value, key=""):
    if isinstance(value, Mapping):
        return {
            name: _canonical(item, name)
            for name, item in value.items()
            if name != "receipt"
        }
    if isinstance(value, list):
        items = [_canonical(item) for item in value]
        return (
            sorted(items, key=lambda item: json.dumps(item, sort_keys=True))
            if key in SET_LISTS
            else items
        )
    return value


STATE_FIELDS = {
    "source-artifact": frozenset(
        "generation events access_state evaluated_sequence surface_watermarks "
        "tombstone idempotency_key revision sha256 retrieved_at effective_at "
        "versions".split()
    ),
    "job-outbox-handoff": frozenset(
        "state transitions attempt dead_letter generation published_generation "
        "stores deletion_watermark generation_watermark".split()
    ),
}


def _admission(kind: str, doc: Mapping) -> Mapping:
    admission = {
        name: value
        for name, value in doc.items()
        if name not in STATE_FIELDS.get(kind, ())
    }
    if kind == "source-artifact":
        admission["source"] = {
            name: doc["source"][name] for name in ("repository", "ref", "paths")
        }
        admission["provenance"] = {"synthetic": doc["provenance"]["synthetic"]}
    elif kind == "job-outbox-handoff":
        admission["outbox"] = {
            name: doc["outbox"][name] for name in ("event_id", "dedup_key")
        }
    return admission


def _make_state_record(kind, doc, admission_hash, request_hash) -> dict:
    source = kind == "source-artifact"
    revision = {"generation": doc["generation"]}
    revision.update(
        {"evaluated_sequence": doc["evaluated_sequence"]}
        if source
        else {
            "transition_count": len(doc["transitions"]),
            "outbox_sequence": doc["outbox"]["sequence"],
            "attempt": doc["attempt"],
            "deletion_watermark": doc["deletion_watermark"],
            "generation_watermark": doc["generation_watermark"],
        }
    )
    return {
        "admission_sha256": admission_hash,
        "request_sha256": request_hash,
        "revision": revision,
        "state": doc["access_state" if source else "state"],
        "history": _canonical(doc["events" if source else "transitions"]),
        "artifact": {
            "source_revision": doc["revision"],
            "content_sha256": doc["sha256"],
            "versions": _canonical(doc["versions"]),
        }
        if source
        else None,
        "surface_watermarks": _canonical(doc["surface_watermarks"]) if source else None,
    }


def _same_int_frontier(old, new) -> bool:
    return (
        isinstance(old, Mapping)
        and old.keys() == new.keys()
        and all(type(value) is int for value in old.values())
    )


def _check_source_state(current, previous, revision, prior_revision) -> None:
    watermarks, old = current["surface_watermarks"], previous["surface_watermarks"]
    artifact = previous["artifact"]
    _require(
        isinstance(artifact, Mapping)
        and set(artifact) == {"source_revision", "content_sha256", "versions"}
        and all(
            isinstance(artifact[name], str)
            for name in ("source_revision", "content_sha256")
        )
        and _valid_versions(artifact["versions"])
        and (
            revision["generation"] > prior_revision["generation"]
            or current["artifact"] == artifact
        )
        and _same_int_frontier(old, watermarks)
        and all(watermarks[name] >= value for name, value in old.items()),
        "source watermark rollback",
    )
    allowed_states = {
        "allowed": {"allowed", "revoked", "deleted"},
        "revoked": {"revoked", "deleted"},
        "deleted": {"deleted"},
    }.get(previous["state"])
    _require(
        allowed_states is not None and current["state"] in allowed_states,
        "restricted source cannot be restored",
    )


def _check_prior_state(kind: str, current: Mapping, previous) -> None:
    _require(
        isinstance(previous, Mapping)
        and set(previous) == set(current)
        and _same_int_frontier(previous.get("revision"), current["revision"])
        and isinstance(previous.get("state"), str)
        and isinstance(previous.get("history"), list)
        and (
            kind == "source-artifact"
            or previous.get("artifact") is previous.get("surface_watermarks") is None
        ),
        "invalid prior state",
    )
    _require(
        previous["admission_sha256"] == current["admission_sha256"],
        "admission state conflict",
    )
    revision, prior_revision = current["revision"], previous["revision"]
    _require(
        all(revision[name] >= value for name, value in prior_revision.items())
        and current["history"][: len(previous["history"])] == previous["history"],
        "state rollback",
    )
    if kind == "source-artifact":
        _check_source_state(current, previous, revision, prior_revision)
    elif previous["state"] in {"succeeded", "cancelled"}:
        _require(
            revision == prior_revision and current["state"] == previous["state"],
            "terminal job cannot reopen",
        )
    _require(
        revision != prior_revision
        or current["request_sha256"] == previous["request_sha256"],
        "state revision conflict",
    )


def _validate_inputs(kind, doc, schemas, policy, prior_receipts, prior_states) -> None:
    _require(
        isinstance(doc, Mapping) and isinstance(schemas, Mapping),
        "parsed mappings required",
    )
    _require(
        isinstance(policy, Mapping) and isinstance(prior_receipts, Mapping),
        "trusted policy and prior receipts required",
    )
    if kind in {"source-artifact", "job-outbox-handoff"}:
        _require(isinstance(prior_states, Mapping), "prior states required")
    _require(
        isinstance(policy.get("project_id"), str)
        and bool(policy["project_id"])
        and doc.get("project_id") == policy["project_id"],
        "trusted project context mismatch",
    )
    _schema(kind, doc, schemas)


def _receipt_identity(kind, doc, request_hash):
    raw_key = (
        doc["receipt"]["idempotency_key"]
        if kind == "blog-data-handoff"
        else doc["idempotency_key"]
        if kind == "source-artifact"
        else doc["dedup_key"]
        if kind == "job-outbox-handoff"
        else request_hash
    )
    scope = {
        "project_id": doc["project_id"],
        "contract": kind,
        "raw_idempotency_key": raw_key,
    }
    admission_scope = scope
    if kind == "source-artifact":
        admission_scope = {
            "project_id": doc["project_id"],
            "contract": kind,
            "repository": doc["source"]["repository"],
            "ref": doc["source"]["ref"],
            "path": doc["path"],
        }
    admission_key = _hash({**admission_scope, "receipt": "admission"})
    admission_hash = _hash(
        {"kind": kind, "admission": _canonical(_admission(kind, doc))}
    )
    if kind == "source-artifact":
        scope["state_revision"] = {
            "generation": doc["generation"],
            "evaluated_sequence": doc["evaluated_sequence"],
        }
    elif kind == "job-outbox-handoff":
        scope["state_revision"] = {
            "generation": doc["generation"],
            "transition_count": len(doc["transitions"]),
            "outbox_sequence": doc["outbox"]["sequence"],
        }
    else:
        admission_key, admission_hash = _hash(scope), request_hash
    return raw_key, _hash(scope), admission_key, admission_hash


def _check_receipts(
    kind,
    doc,
    request_hash,
    state_key,
    admission_key,
    admission_hash,
    prior_receipts,
    prior_states,
):
    state_record = None
    if kind in {"source-artifact", "job-outbox-handoff"}:
        state_record = _make_state_record(kind, doc, admission_hash, request_hash)
        _require(
            (admission_key in prior_receipts) == (admission_key in prior_states),
            "incomplete prior state",
        )
        if admission_key in prior_states:
            _check_prior_state(kind, state_record, prior_states[admission_key])
    _require(
        admission_key not in prior_receipts
        or prior_receipts[admission_key] == admission_hash,
        "admission receipt conflict",
    )
    _require(
        state_key not in prior_receipts or prior_receipts[state_key] == request_hash,
        "idempotency conflict",
    )
    return state_record


def validate_preparation(
    kind: str,
    document: Mapping,
    schemas: Mapping,
    *,
    policy=None,
    synthetic_bytes=None,
    prior_receipts=None,
    prior_states=None,
) -> dict:
    _validate_inputs(kind, document, schemas, policy, prior_receipts, prior_states)
    try:
        validate_semantics(kind, document, policy, synthetic_bytes)
        request_hash = _hash({"kind": kind, "document": _canonical(document)})
        raw_key, state_key, admission_key, admission_hash = _receipt_identity(
            kind, document, request_hash
        )
        state_record = _check_receipts(
            kind,
            document,
            request_hash,
            state_key,
            admission_key,
            admission_hash,
            prior_receipts,
            prior_states,
        )
    except PreparationError:
        raise
    except (KeyError, TypeError, ValueError, AttributeError):
        raise PreparationError("invalid caller policy or synthetic input") from None
    return {
        "contract": kind,
        "schema_version": 1,
        "synthetic_contract_valid": True,
        "deployed": False,
        "external_facts_verified": False,
        "runtime": "NOT_RUN",
        "idempotency_key": state_key,
        "raw_idempotency_key": raw_key,
        "request_sha256": request_hash,
        "admission_idempotency_key": admission_key,
        "admission_sha256": admission_hash,
        "receipt_entries": {admission_key: admission_hash, state_key: request_hash},
        "state_record": state_record,
    }
