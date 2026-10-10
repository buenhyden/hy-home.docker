"""Pure parsed-input semantics for Wiki preparation contracts."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from datetime import datetime


class PreparationError(ValueError):
    """A fixed, input-free contract error."""


ENFORCEMENT = frozenset(
    {"search", "point-query", "citation", "download", "cache", "old-generation"}
)
DISABLED = frozenset(
    "wiki-runtime workspace-create secret-issue blog-write wiki-schedule "
    "resource-provision".split()
)
SOURCE_REFS = {
    "buenhyden/blog-data": "dev",
    "buenhyden/Project-Template": "dev",
    "buenhyden/hy-home.docker": "main",
    "buenhyden/hy-home.k8s": "main",
}
TRANSITIONS = {
    "pending": frozenset({"running", "cancelled"}),
    "running": frozenset({"partial", "succeeded", "failed", "cancelled"}),
    "partial": frozenset({"running", "failed", "cancelled"}),
    "failed": frozenset({"pending"}),
    "succeeded": frozenset(),
    "cancelled": frozenset(),
}
MAX_JOB_ATTEMPTS, MAX_JOB_TIMEOUT_SECONDS, MAX_POLICY_LIST_ITEMS = 3, 300, 128
VERSION_FIELDS = {"parser", "chunker", "embedding"}


def _require(condition: bool, reason: str) -> None:
    if not condition:
        raise PreparationError(reason)


def _trusted_strings(value: object) -> frozenset[str]:
    _require(isinstance(value, list), "invalid trusted allowlist")
    _require(
        len(value) <= MAX_POLICY_LIST_ITEMS
        and all(isinstance(item, str) and item for item in value)
        and len(value) == len(set(value)),
        "invalid trusted allowlist",
    )
    return frozenset(value)


def _valid_versions(value) -> bool:
    return (
        isinstance(value, Mapping)
        and value.keys() == VERSION_FIELDS
        and all(
            isinstance(item, str) and item and "*" not in item
            for item in value.values()
        )
    )


def _safe_path(path: str) -> bool:
    return (
        isinstance(path, str)
        and bool(path)
        and not path.startswith("/")
        and not any(char in path for char in ("%", "\\", ":", "*", "?", "\x00"))
        and all(
            part and part not in {".", ".."} for part in path.rstrip("/").split("/")
        )
    )


def _source(source: Mapping, policy: Mapping) -> Mapping:
    sources = policy.get("sources")
    _require(isinstance(sources, Mapping), "invalid trusted source policy")
    allowed = sources.get(source["repository"])
    _require(isinstance(allowed, Mapping), "invalid trusted source policy")
    paths = _trusted_strings(allowed.get("paths"))
    _require(
        SOURCE_REFS.get(source["repository"]) == source["ref"]
        and source["ref"] in _trusted_strings(allowed.get("refs"))
        and source["revision"] in _trusted_strings(allowed.get("revisions")),
        "source ref outside knowledge allowlist",
    )
    _require(
        all(_safe_path(path) and path in paths for path in source["paths"]),
        "source path outside trusted allowlist",
    )
    return allowed


def _consumer_identity(doc: Mapping, policy: Mapping):
    project, reg = doc["project_id"], doc["registration"]
    scope = policy.get("resources", {})
    _require(
        doc["namespace"] == project == reg["project_id"] == doc["identity"]["audience"],
        "cross-project namespace",
    )
    _require(
        doc["identity"] == policy.get("identity")
        and doc["classification"] == policy.get("classification"),
        "identity or classification outside policy",
    )
    _require(
        scope.get("db_prefix") == project.replace("-", "_") + "_"
        and all(value.startswith(scope["db_prefix"]) for value in reg["db"].values()),
        "cross-project database namespace",
    )
    _require(
        reg["s3"]["bucket"] == project
        and reg["search"]["collection"] == project
        and reg["search"]["authorization_path"] == "/projects/" + project
        and reg["oidc"]["client_id"] == project
        and reg["telemetry"]["service.name"] == project
        and reg["valkey"]["acl_prefix"] == project,
        "cross-project resource namespace",
    )
    return project, reg, scope


def _consumer_resources(project, reg, scope, policy) -> None:
    exact = {
        "s3_bucket": reg["s3"]["bucket"],
        "search_collection": reg["search"]["collection"],
        "search_authorization_path": reg["search"]["authorization_path"],
        "oidc_client_id": reg["oidc"]["client_id"],
        "telemetry_service": reg["telemetry"]["service.name"],
        "valkey_prefix": reg["valkey"]["acl_prefix"],
    }
    _require(
        all(scope.get(key) == value for key, value in exact.items()),
        "resource outside trusted scope",
    )
    _require(
        scope.get("valkey_user_prefix") == project + "-"
        and reg["valkey"]["acl_user"].startswith(scope["valkey_user_prefix"])
        and scope.get("network_prefix") == project + "-"
        and all(
            name.startswith(scope["network_prefix"]) for name in reg["allowed_networks"]
        )
        and scope.get("s3_prefix") == project + "/"
        and reg["s3"]["prefix"].startswith(scope["s3_prefix"])
        and _safe_path(reg["s3"]["prefix"]),
        "cross-project consumer identity",
    )
    _require(
        set(reg["secret_refs"]) <= _trusted_strings(policy.get("secret_refs")),
        "secret reference outside policy",
    )


def _consumer_registration(reg, scope, policy) -> None:
    _require(
        {name: reg[name] for name in ("infra_ref", "template_ref", "project_ref")}
        == policy.get("registration_refs"),
        "registration ref outside trusted allowlist",
    )
    _require(
        reg["endpoints"] == policy.get("registration_endpoints")
        and reg["db"] == scope.get("db")
        and set(reg["allowed_networks"])
        <= _trusted_strings(policy.get("allowed_networks"))
        and reg["quota"] == policy.get("quota"),
        "registration resource outside trusted policy",
    )
    _require(
        reg["backup_restore"] == policy.get("registration_backup_restore"),
        "backup or restore owner outside trusted policy",
    )
    _require(
        reg["approval"]["state"] == "draft"
        and reg["verification"]["state"] == "not_run",
        "preparation cannot assert runtime approval",
    )


def _consumer_policy(doc, policy) -> None:
    _require(
        doc["retention_days"] <= policy.get("retention_days", 0)
        and doc["backup"] == policy.get("backup"),
        "retention or recovery outside trusted policy",
    )
    for key in ("permissions", "valkey_commands", "egress", "metric_labels"):
        _require(
            set(doc[key]) <= _trusted_strings(policy.get(key)),
            "capability outside trusted policy",
        )
    search, trusted_search = doc["qdrant_rbac"], policy.get("qdrant_rbac")
    _require(
        isinstance(trusted_search, Mapping)
        and search.keys() == trusted_search.keys()
        and search["collection"] == doc["project_id"] == trusted_search["collection"]
        and set(search["roles"]) == _trusted_strings(trusted_search.get("roles"))
        and doc["max_metric_series"] <= policy.get("max_metric_series", 0),
        "search or metric scope outside policy",
    )
    _require(
        set(doc["disabled_by_design"]) == DISABLED, "runtime actions must stay disabled"
    )
    for source in doc["sources"]:
        _source(source, policy)


def _consumer(doc: Mapping, policy: Mapping) -> None:
    project, reg, scope = _consumer_identity(doc, policy)
    _consumer_resources(project, reg, scope, policy)
    _consumer_registration(reg, scope, policy)
    _consumer_policy(doc, policy)


def _artifact_source(doc, payload, policy) -> None:
    _require(isinstance(payload, bytes), "synthetic bytes required")
    versions = _source(doc["source"], policy).get("versions")
    _require(
        isinstance(versions, list)
        and len(versions) <= MAX_POLICY_LIST_ITEMS
        and all(_valid_versions(value) for value in versions)
        and len({tuple(sorted(value.items())) for value in versions}) == len(versions)
        and doc["versions"] in versions,
        "version outside trusted allowlist",
    )
    _require(
        doc["path"] in doc["source"]["paths"], "artifact path outside source allowlist"
    )
    _require(
        doc["revision"]
        == doc["source"]["revision"]
        == doc["provenance"]["source_revision"],
        "revision mismatch",
    )
    digest = hashlib.sha256(payload).hexdigest()
    _require(
        digest
        == doc["sha256"]
        == doc["provenance"]["artifact_sha256"]
        == doc["idempotency_key"],
        "synthetic hash mismatch",
    )


def _artifact_authority(doc, policy) -> None:
    _require(doc["acl"]["project_id"] == doc["project_id"], "cross-project ACL")
    _require(
        set(doc["enforcement"]) == ENFORCEMENT, "incomplete revocation enforcement"
    )
    try:
        effective = datetime.fromisoformat(doc["effective_at"].replace("Z", "+00:00"))
        retrieved = datetime.fromisoformat(doc["retrieved_at"].replace("Z", "+00:00"))
        _require(
            effective.tzinfo is not None
            and retrieved.tzinfo is not None
            and effective <= retrieved,
            "invalid artifact time",
        )
    except ValueError:
        raise PreparationError("invalid artifact time") from None
    _require(
        set(doc["acl"]["readers"]) <= _trusted_strings(policy.get("acl_readers")),
        "reader outside trusted allowlist",
    )
    _require(
        all(
            reader.startswith(doc["project_id"] + "-")
            for reader in doc["acl"]["readers"]
        ),
        "cross-project reader",
    )


def _artifact_state(doc) -> None:
    events = doc["events"]
    _require(
        len({event["id"] for event in events}) == len(events),
        "duplicate revocation event",
    )
    _require(
        all(event["generation"] <= doc["generation"] for event in events),
        "future revocation generation",
    )
    sequences = [event["sequence"] for event in events]
    _require(sequences == sorted(set(sequences)), "revocation event order")
    _require(
        doc["evaluated_sequence"] >= max(sequences, default=0),
        "revocation not yet evaluated",
    )
    _require(
        all(
            max(sequences, default=0) <= watermark <= doc["evaluated_sequence"]
            for watermark in doc["surface_watermarks"].values()
        ),
        "invalid revocation surface",
    )
    expected = (
        "deleted"
        if any(event["kind"] == "delete" for event in events)
        else "revoked"
        if events
        else "allowed"
    )
    _require(
        doc["access_state"] == expected and doc["tombstone"] == (expected == "deleted"),
        "revocation or deletion bypass",
    )


def _artifact(doc: Mapping, payload, policy: Mapping) -> None:
    _artifact_source(doc, payload, policy)
    _artifact_authority(doc, policy)
    _artifact_state(doc)


def _job_authority(doc, policy) -> None:
    authority = policy.get("job", {})
    _require(
        doc["job_id"] == authority.get("job_id")
        and doc["dedup_key"] == authority.get("dedup_key")
        and doc["outbox"]["event_id"] == authority.get("event_id"),
        "job identity outside trusted policy",
    )
    limit, timeout = authority.get("max_attempts"), authority.get("timeout_seconds")
    _require(
        type(limit) is int
        and 1 <= limit <= MAX_JOB_ATTEMPTS
        and type(timeout) is int
        and 1 <= timeout <= MAX_JOB_TIMEOUT_SECONDS
        and doc["max_attempts"] == limit
        and doc["timeout_seconds"] == timeout,
        "job retry or timeout outside trusted policy",
    )


def _job_history(doc):
    state, attempts = "pending", 0
    for step in doc["transitions"]:
        _require(
            not (step["from"] == "failed" and step["to"] == "pending")
            or attempts < doc["max_attempts"],
            "retry budget exhausted",
        )
        _require(
            step["from"] == state and step["to"] in TRANSITIONS[state],
            "illegal job transition",
        )
        attempts += int(step["from"] == "pending" and step["to"] == "running")
        state = step["to"]
    _require(state == doc["state"], "job state does not match history")
    _require(
        doc["attempt"] == attempts and attempts <= doc["max_attempts"],
        "retry history or budget mismatch",
    )
    return state, attempts


def _job_delivery(doc, state, attempts) -> None:
    _require(
        (doc["backfill"] and doc["backfill_of"] not in {None, doc["job_id"]})
        or (not doc["backfill"] and doc["backfill_of"] is None),
        "invalid backfill provenance",
    )
    _require(doc["dedup_key"] == doc["outbox"]["dedup_key"], "outbox dedup mismatch")
    exhausted = state == "failed" and attempts == doc["max_attempts"]
    disposal = doc["dead_letter"]
    _require(
        disposal["disposition"] == ("quarantined" if exhausted else "none")
        and disposal["reason"] == ("retry-exhausted" if exhausted else None),
        "dead-letter disposition mismatch",
    )
    if doc["outbox"]["acknowledged"]:
        _require(
            state in {"succeeded", "cancelled"}, "premature outbox acknowledgement"
        )


def _job_publication(doc, state) -> None:
    if doc["published_generation"] is not None:
        _require(
            state == "succeeded"
            and all(v == "verified" for v in doc["stores"].values()),
            "unverified generation publication",
        )
        _require(
            doc["published_generation"] == doc["generation"],
            "generation pointer mismatch",
        )
        _require(
            doc["generation_watermark"]
            >= max(doc["deletion_watermark"], doc["generation"]),
            "deletion and generation must precede publication",
        )
    _require(
        doc["generation_watermark"] <= doc["outbox"]["sequence"]
        and doc["deletion_watermark"] <= doc["outbox"]["sequence"],
        "watermark beyond outbox",
    )


def _job(doc: Mapping, policy: Mapping) -> None:
    _job_authority(doc, policy)
    state, attempts = _job_history(doc)
    _job_delivery(doc, state, attempts)
    _job_publication(doc, state)


def _canonical_writes(writes: list) -> list:
    return sorted(
        writes,
        key=lambda write: (write["path"], write["candidate_id"], write["sha256"]),
    )


def _blog_authority(doc, payloads, policy):
    _require(isinstance(payloads, Mapping), "candidate synthetic bytes required")
    trusted = policy.get("blog", {})
    _require(isinstance(trusted, Mapping), "invalid trusted handoff policy")
    candidate_ids = _trusted_strings(trusted.get("candidate_ids"))
    allowed_paths = _trusted_strings(trusted.get("allowed_paths"))
    trusted_writes = trusted.get("write_set")
    _require(
        isinstance(trusted_writes, list)
        and len(trusted_writes) <= MAX_POLICY_LIST_ITEMS
        and all(isinstance(write, Mapping) for write in trusted_writes),
        "invalid trusted handoff policy",
    )
    _require(
        doc["repository"] == trusted.get("repository")
        and doc["base_sha"] == trusted.get("base_sha"),
        "handoff target outside trusted policy",
    )
    _require(
        set(doc["selected"]) == candidate_ids
        and set(doc["allowed_paths"]) <= allowed_paths
        and _canonical_writes(doc["write_set"]) == _canonical_writes(trusted_writes),
        "handoff selection outside trusted policy",
    )


def _blog_selection(doc):
    candidates = doc["candidates"]
    _require(
        all(
            _safe_path(item["path"]) and item["path"].startswith("Literature/")
            for item in candidates
        ),
        "candidate outside Literature scope",
    )
    ids = [candidate["id"] for candidate in candidates]
    _require(len(ids) == len(set(ids)), "duplicate candidate identity")
    selected = set(doc["selected"])
    _require(selected <= set(ids), "unknown selected candidate")
    approval = doc["approval"]
    _require(
        set(approval["selected"]) == selected
        and approval["base_sha"] == doc["base_sha"] == doc["receipt"]["base_sha"],
        "approval or base mismatch",
    )
    writes = doc["write_set"]
    paths = [write["path"] for write in writes]
    _require(len(paths) == len(set(paths)), "duplicate write path")
    _require(
        len(writes) == len(selected)
        and {write["candidate_id"] for write in writes} == selected,
        "write set must match selection",
    )
    return writes, {candidate["id"]: candidate for candidate in candidates}


def _blog_payloads(doc, payloads, writes, by_id) -> None:
    for write in writes:
        candidate = by_id[write["candidate_id"]]
        _require(
            _safe_path(write["path"])
            and write["path"].startswith("Literature/")
            and write["path"] in doc["allowed_paths"],
            "write path outside candidate allowlist",
        )
        _require(
            write["path"] == candidate["path"]
            and write["sha256"] == candidate["sha256"],
            "candidate write mismatch",
        )
        payload = payloads.get(write["candidate_id"])
        _require(
            isinstance(payload, bytes)
            and hashlib.sha256(payload).hexdigest() == write["sha256"],
            "candidate synthetic hash mismatch",
        )
    writes = _canonical_writes(writes)
    _require(
        doc["receipt"]["write_set_sha256"] == _digest(writes),
        "write-set receipt mismatch",
    )
    _require(
        doc["receipt"]["idempotency_key"]
        == _digest(
            {
                "project_id": doc["project_id"],
                "repository": doc["repository"],
                "base_sha": doc["base_sha"],
                "write_set": writes,
            }
        ),
        "handoff idempotency mismatch",
    )


def _digest(value) -> str:
    import json

    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def _blog(doc: Mapping, payloads, policy: Mapping) -> None:
    _blog_authority(doc, payloads, policy)
    writes, by_id = _blog_selection(doc)
    _blog_payloads(doc, payloads, writes, by_id)


def validate_semantics(kind: str, doc: Mapping, policy: Mapping, payload) -> None:
    if kind == "consumer-manifest":
        _consumer(doc, policy)
    elif kind == "source-artifact":
        _artifact(doc, payload, policy)
    elif kind == "job-outbox-handoff":
        _job(doc, policy)
    else:
        _blog(doc, payload, policy)
