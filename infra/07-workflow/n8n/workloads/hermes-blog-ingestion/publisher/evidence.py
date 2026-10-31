"""Hermes Companion Evidence v1: structural binding check, not authentication.

A pass proves only that the bytes are internally consistent with the staged
candidate. It does not prove which process wrote them; the dispatch gates in
policy, Outbox and transport stay closed until a producer trust anchor is
separately admitted (see the workload README contract section).
"""

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlsplit

SCHEMA = "hermes-companion-evidence/1"
_HEX64 = re.compile(r"[0-9a-f]{64}\Z")
_TS = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?(?:Z|[+-]\d{2}:\d{2})\Z"
)
# Hermes may emit microseconds in generated_at; the adapter truncates them.
_GENERATED = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})\Z"
)
_TOP = {
    "schema_version",
    "producer",
    "job_id",
    "run_id",
    "candidate_sha256",
    "scheduled_at",
    "items",
}
_ITEM = {
    "index",
    "source_url",
    "fetched_url",
    "fetched_at",
    "http_status",
    "body_sha256",
    "cache",
    "tool_call_id",
    "status",
}


class EvidenceError(ValueError):
    """Value-free rejection code."""


@dataclass(frozen=True)
class RunTimes:
    scheduled_at: str
    collected_at: str


def _require(condition, code):
    if not condition:
        raise EvidenceError(code)


def _object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, "duplicate_key")
        result[key] = value
    return result


def _reject_constant(_value):
    raise EvidenceError("invalid_json")


def _time(value, pattern=None):
    pattern = pattern or _TS
    _require(isinstance(value, str) and pattern.fullmatch(value), "timestamp")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise EvidenceError("timestamp") from None


def _cache(value):
    if not isinstance(value, dict) or set(value) != {"hit", "key_sha256"}:
        return False
    if value["hit"] is False:
        return value["key_sha256"] is None
    return (
        value["hit"] is True
        and isinstance(value["key_sha256"], str)
        and _HEX64.fullmatch(value["key_sha256"]) is not None
    )


def _https(value):
    try:
        parts = urlsplit(value)
        parts.port  # noqa: B018 - raises ValueError for an invalid port
        return (
            len(value) <= 2048
            and parts.scheme == "https"
            and bool(parts.hostname)
            and parts.username is None
            and parts.password is None
            and not any(ord(c) <= 32 or ord(c) >= 127 for c in value)
        )
    except (TypeError, ValueError, AttributeError):
        return False


def verify(job_id, run_id, candidate, evidence):
    """Return run times derived only from bound direct-fetch records.

    collected_at is the latest item fetched_at; nothing is estimated. Every
    candidate item needs exactly one record, so an item without a source URL
    cannot be verified and blocks the whole run. A cache hit keeps the original
    direct-fetch time, never the cache materialization time.
    """
    try:
        data = json.loads(
            evidence, object_pairs_hook=_object, parse_constant=_reject_constant
        )
        report = json.loads(candidate)
        items = report["items"]
        generated = _time(report["generated_at"], _GENERATED)
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError) as error:
        if isinstance(error, EvidenceError):
            raise
        raise EvidenceError("invalid_json") from None
    _require(isinstance(data, dict) and set(data) == _TOP, "fields")
    _require(data["schema_version"] == SCHEMA, "schema_version")
    producer = data["producer"]
    _require(
        isinstance(producer, dict)
        and set(producer) == {"name", "version"}
        and all(isinstance(v, str) and 0 < len(v) <= 128 for v in producer.values()),
        "producer",
    )
    _require(data["job_id"] == job_id and data["run_id"] == run_id, "identity")
    _require(
        data["candidate_sha256"] == hashlib.sha256(candidate).hexdigest(),
        "candidate_digest",
    )
    scheduled = _time(data["scheduled_at"])
    _require(scheduled <= generated, "scheduled_after_generation")
    records = data["items"]
    _require(
        isinstance(items, list)
        and isinstance(records, list)
        and len(records) == len(items) > 0,
        "coverage",
    )
    latest = None
    for index, (item, record) in enumerate(zip(items, records, strict=True)):
        _require(isinstance(record, dict) and set(record) == _ITEM, "fields")
        _require(type(record["index"]) is int and record["index"] == index, "order")
        _require(
            isinstance(item, dict)
            and isinstance(item.get("source_url"), str)
            and record["source_url"] == item["source_url"],
            "source_url",
        )
        _require(_https(record["fetched_url"]), "fetched_url")
        _require(
            type(record["http_status"]) is int and 200 <= record["http_status"] < 300,
            "http_status",
        )
        _require(
            isinstance(record["body_sha256"], str)
            and _HEX64.fullmatch(record["body_sha256"]) is not None,
            "body_digest",
        )
        _require(_cache(record["cache"]), "cache")
        _require(
            isinstance(record["tool_call_id"], str)
            and 0 < len(record["tool_call_id"]) <= 128,
            "tool_call_id",
        )
        # Partial, failed or cancelled acquisitions never verify a run.
        _require(record["status"] == "complete", "status")
        fetched = _time(record["fetched_at"])
        _require(fetched <= generated, "fetched_after_generation")
        _require(record["cache"]["hit"] or fetched >= scheduled, "fetched_before_run")
        if latest is None or fetched > latest[0]:
            latest = (fetched, record["fetched_at"])
    return RunTimes(data["scheduled_at"], latest[1])
