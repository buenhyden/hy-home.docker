"""Pure Blog-data v1 adapter pinned to its published contract revision.

The caller supplies authoritative per-run timestamps. This module does not
discover them or perform network I/O, and is not wired into the live CLI.
"""

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlsplit

from .candidates import JOBS
from .delivery import BoundRequest, Outcome, OutcomeKind, Receipt
from .http_transport import HttpResponse

REVISION = "blog-data@a6d0957ad380f179f73bdd2a60ff23792d53f7ae"
DESTINATION = "n8n_hermes_ingestion"
_KINDS = {
    "strategy-news": ("news", "news"),
    "devops-brief": ("devops", "devops"),
    "solo-dev-ideas": ("business_ideas", "business_idea"),
}
_IDENTITY = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_REPORT_ID = re.compile(r"[a-f0-9-]{36}\Z")


def _timestamp(value):
    if not isinstance(value, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?(?:Z|[+-]\d{2}:\d{2})", value
    ):
        raise ValueError("invalid_timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("invalid_timestamp") from None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("invalid_timestamp")
    return value


def _identity(value):
    if not isinstance(value, str) or not _IDENTITY.fullmatch(value):
        raise ValueError("invalid_identity")
    return value


def _object(pairs):
    data = {}
    for key, value in pairs:
        if key in data:
            raise ValueError("invalid_json")
        data[key] = value
    return data


def _decode(raw):
    if not isinstance(raw, bytes):
        raise ValueError("invalid_bytes")
    try:
        return raw.decode("utf-8", errors="strict")
    except UnicodeError:
        raise ValueError("invalid_text") from None


def _source_url(value):
    if not isinstance(value, str) or not value or len(value) > 2048:
        raise ValueError("invalid_url")
    if any(c.isspace() or unicodedata.category(c) == "Cc" for c in value):
        raise ValueError("invalid_url")
    try:
        parsed = urlsplit(value)
        if (
            parsed.scheme not in ("http", "https")
            or not parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
            or "\\" in value
        ):
            raise ValueError("invalid_url")
        _ = parsed.port
        parsed.hostname.encode("idna")
    except (UnicodeError, ValueError):
        raise ValueError("invalid_url") from None
    return value


def _items(data, snapshot, item_kind):
    items = data.get("items")
    ideas = snapshot.get("ideas", ())
    if not isinstance(items, list) or not 1 <= len(items) <= 100:
        raise ValueError("invalid_items")
    if item_kind == "business_idea" and len(ideas) != len(items):
        raise ValueError("invalid_ideas")
    if item_kind != "business_idea" and ideas:
        raise ValueError("invalid_ideas")
    result = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError("invalid_item")
        title = item.get("title")
        if not isinstance(title, str) or not 1 <= len(title) <= 300:
            raise ValueError("invalid_title")
        body = {"candidate": item}
        if item_kind == "business_idea":
            ref, raw = ideas[index]
            if ref != item.get("source_ref") or hashlib.sha256(
                raw
            ).hexdigest() != item.get("source_sha256"):
                raise ValueError("invalid_idea")
            body["source_text"] = _decode(raw)
        text = json.dumps(
            body,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        if len(text) > 32768:
            raise ValueError("item_too_large")
        entry = dict(
            item_id=f"item-{index + 1}", kind=item_kind, title=title, body=text
        )
        if item.get("source_url") is not None:
            entry["source_url"] = _source_url(item["source_url"])
        result.append(entry)
    return result


@dataclass(frozen=True)
class GatewayAdapter:
    scheduled_at: str
    generated_at: str
    collected_at: str
    idempotent_writes = True

    def __post_init__(self):
        for value in (self.scheduled_at, self.generated_at, self.collected_at):
            _timestamp(value)

    def prepare(self, snapshot):
        try:
            job, run = _identity(snapshot["job_id"]), _identity(snapshot["run_id"])
            if job not in JOBS:
                raise ValueError("invalid_job")
            if (
                hashlib.sha256(snapshot["candidate"]).hexdigest()
                != snapshot["candidate_sha256"]
            ):
                raise ValueError("candidate_mismatch")
            data = json.loads(
                _decode(snapshot["candidate"]),
                object_pairs_hook=_object,
                parse_constant=lambda _: (_ for _ in ()).throw(
                    ValueError("invalid_json")
                ),
            )
            if data["job_id"] != job or data["run_id"] != run:
                raise ValueError("identity_mismatch")
            if data["generated_at"] != self.generated_at:
                raise ValueError("timestamp_mismatch")
            report_kind, item_kind = _KINDS[data["report_kind"]]
            raw = snapshot["source"]
            source = _decode(raw)
            digest = hashlib.sha256(raw).hexdigest()
            if digest != snapshot["source_sha256"] or not 1 <= len(source) <= 524288:
                raise ValueError("invalid_source")
            source_ref = snapshot["source_ref"]
            if not isinstance(source_ref, str) or not 1 <= len(source_ref) <= 1024:
                raise ValueError("invalid_ref")
            if data["source_ref"] != source_ref or data["source_sha256"] != digest:
                raise ValueError("source_mismatch")
            key = hashlib.sha256((job + ":" + run).encode()).hexdigest()
            report = dict(
                schema_version="1.0",
                producer="hermes",
                job_id=job,
                run_id=run,
                report_kind=report_kind,
                scheduled_at=self.scheduled_at,
                generated_at=self.generated_at,
                collected_at=self.collected_at,
                source_ref=source_ref,
                source_text=source,
                source_sha256=digest,
                idempotency_key=key,
                items=_items(data, snapshot, item_kind),
            )
            body = json.dumps(
                report,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8")
            if len(body) > 1024 * 1024:
                raise ValueError("request_too_large")
            return BoundRequest(REVISION, DESTINATION, body)
        except (KeyError, TypeError, UnicodeError, ValueError, RecursionError):
            raise ValueError("invalid_snapshot") from None

    def interpret(self, response, request):
        if not isinstance(response, HttpResponse):
            return Outcome(OutcomeKind.UNKNOWN)
        if response.status == 409:
            return Outcome(OutcomeKind.CONFLICT)
        if response.status in (400, 401, 403, 404, 413, 415, 422):
            return Outcome(OutcomeKind.REJECTED)
        if response.status not in (200, 201):
            return Outcome(OutcomeKind.UNKNOWN)
        try:
            if (
                response.content_type is None
                or response.content_type.split(";", 1)[0].strip().lower()
                != "application/json"
            ):
                raise ValueError
            data = json.loads(_decode(response.body), object_pairs_hook=_object)
            sent = json.loads(_decode(request.body), object_pairs_hook=_object)
            if (
                set(data)
                != {
                    "id",
                    "persisted",
                    "duplicate",
                    "status",
                    "candidate_count",
                    "status_url",
                }
                or not isinstance(data["id"], str)
                or not _REPORT_ID.fullmatch(data["id"])
                or data["persisted"] is not True
                or data["status"] != "received"
                or type(data["duplicate"]) is not bool
                or data["duplicate"] != (response.status == 200)
                or type(data["candidate_count"]) is not int
                or data["candidate_count"] != len(sent["items"])
                or data["status_url"] != "/v1/ingestions/" + data["id"]
                or hashlib.sha256(request.body).hexdigest() != request.body_sha256
                or sent["source_sha256"] != request.source_sha256
                or (sent["job_id"], sent["run_id"]) != request.key
                or request.contract_revision != REVISION
                or request.destination != DESTINATION
            ):
                raise ValueError
            return Outcome(
                OutcomeKind.DURABLE,
                # Gateway returns its ID; the hashes are local request bindings.
                Receipt(
                    request.key,
                    request.source_sha256,
                    request.body_sha256,
                    True,
                    data["id"],
                ),
            )
        except (KeyError, ValueError, TypeError, RecursionError):
            return Outcome(OutcomeKind.UNKNOWN)
