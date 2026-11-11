"""Run-bound acquisition records; these are not producer signatures."""

import base64
import hashlib
import json
import os
import re
import secrets
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

from . import source_check, source_fetch
from .private_records import PrivateRecords

MAX_TEXT_BYTES = 256 * 1024
MAX_RUN_ITEMS = 100
MAX_ITEM_FETCH_ATTEMPTS = 3
# POL-0091: open-web fallback. Only primary failures Crawl4AI can change; a
# refusal (private address, oversized body) is never retried through it.
CRAWL4AI_URL = "http://127.0.0.1:11235/crawl"
CRAWL4AI_TIMEOUT = 60
CRAWL4AI_MAX_RESPONSE = 32 * 1024 * 1024
FALLBACK_REASONS = frozenset({"status", "redirects", "connect"})
_LOOPBACK_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


class SourceQuality(ValueError):
    """Every item whose claims its page does not back, as item_id/codes dicts."""

    def __init__(self, failures):
        super().__init__("source_quality")
        self.failures = failures


def _time(value):
    if not isinstance(value, str):
        raise ValueError("invalid_time")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("invalid_time") from None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("invalid_time")
    return parsed.astimezone(UTC)


def timestamp(value):
    """Gateway-compatible UTC time, truncated to milliseconds."""
    value = _time(value) if isinstance(value, str) else value.astimezone(UTC)
    return value.strftime("%Y-%m-%dT%H:%M:%S.") + f"{value.microsecond // 1000:03d}Z"


def _key(job, run, item):
    return hashlib.sha256("\0".join((job, run, item)).encode()).hexdigest()


def _index_name(job, run):
    return "run-" + hashlib.sha256((job + "\0" + run).encode()).hexdigest() + ".index"


def _index(store, job, run, scheduled):
    raw = store.read(_index_name(job, run))
    if raw is None:
        return {
            "schema_version": "hermes-source-index/1",
            "job_id": job,
            "run_id": run,
            "scheduled_at": timestamp(scheduled),
            "items": {},
        }
    index = _decode(raw)
    if (
        set(index) != {"schema_version", "job_id", "run_id", "scheduled_at", "items"}
        or index["schema_version"] != "hermes-source-index/1"
        or (index["job_id"], index["run_id"], index["scheduled_at"])
        != (job, run, timestamp(scheduled))
        or not isinstance(index["items"], dict)
        or len(index["items"]) > MAX_RUN_ITEMS
    ):
        raise ValueError("invalid_index")
    for item, entry in index["items"].items():
        if (
            not isinstance(item, str)
            or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", item) is None
            or not isinstance(entry, dict)
            or set(entry) != {"source_url", "attempts", "collection_call_id"}
            or not isinstance(entry["source_url"], str)
            or not 1 <= len(entry["source_url"]) <= source_fetch.MAX_URL
            or type(entry["attempts"]) is not int
            or not 1 <= entry["attempts"] <= MAX_ITEM_FETCH_ATTEMPTS
            or not isinstance(entry["collection_call_id"], str)
            or re.fullmatch(r"[a-f0-9]{32}", entry["collection_call_id"]) is None
        ):
            raise ValueError("invalid_index")
    return index


def _decode(raw):
    def unique(pairs):
        result = {}
        for name, value in pairs:
            if name in result:
                raise ValueError("duplicate_key")
            result[name] = value
        return result

    def invalid(_value):
        raise ValueError("invalid_constant")

    value = json.loads(raw, object_pairs_hook=unique, parse_constant=invalid)
    if not isinstance(value, dict):
        raise ValueError("invalid_record")
    return value


def _check(record, job, run, item, scheduled):
    fields = {
        "schema_version",
        "job_id",
        "run_id",
        "item_id",
        "scheduled_at",
        "source_url",
        "final_url",
        "status",
        "fetched_at",
        "body_sha256",
        "content_type",
        "body_b64",
        "receipt_id",
        "collection_call_id",
    }
    if (
        set(record) != fields
        or record.get("schema_version") != "hermes-source-receipt/1"
        or (record.get("job_id"), record.get("run_id"), record.get("item_id"))
        != (job, run, item)
        or record.get("scheduled_at") != timestamp(scheduled)
        or not isinstance(record.get("receipt_id"), str)
        or re.fullmatch(r"[a-f0-9]{32}", record["receipt_id"]) is None
        or not isinstance(record.get("collection_call_id"), str)
        or re.fullmatch(r"[a-f0-9]{32}", record["collection_call_id"]) is None
        or not isinstance(record.get("source_url"), str)
        or not 1 <= len(record["source_url"]) <= source_fetch.MAX_URL
        or not isinstance(record.get("final_url"), str)
        or not 1 <= len(record["final_url"]) <= source_fetch.MAX_URL
        or source_fetch._canonical(record["final_url"]) != record["final_url"]
        or not isinstance(record.get("content_type"), str)
        or len(record["content_type"]) > 4096
        or not isinstance(record.get("body_b64"), str)
        or type(record.get("status")) is not int
        or not 200 <= record["status"] < 300
    ):
        raise ValueError("invalid_record")
    body = base64.b64decode(record["body_b64"], validate=True)
    if (
        len(body) > source_fetch.MAX_BYTES
        or hashlib.sha256(body).hexdigest() != record.get("body_sha256")
        or _time(record["fetched_at"]) < _time(scheduled)
    ):
        raise ValueError("invalid_record")
    result = source_fetch.FetchResult(
        record["final_url"],
        record["status"],
        record["body_sha256"],
        record["fetched_at"],
        record["content_type"],
        body,
    )
    return result


def _crawl4ai_token():
    """Same order as the plugin's other settings: environment, then Hermes .env."""
    token = os.environ.get("CRAWL4AI_API_TOKEN")
    if token:
        return token.strip()
    home = Path(os.environ.get("HERMES_HOME", "~/.hermes")).expanduser()
    for line in (home / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("CRAWL4AI_API_TOKEN="):
            value = line.split("=", 1)[1].strip().strip('"')
            if value:
                return value
    raise FileNotFoundError("crawl4ai_token_missing")


def _crawl4ai_fetch(url, *, opener=None):
    """Render one page through the loopback Crawl4AI; raises when it cannot."""
    token = _crawl4ai_token()
    payload = {
        "urls": [url],
        "crawler_config": {
            "type": "CrawlerRunConfig",
            "params": {"cache_mode": "bypass", "page_timeout": 25000},
        },
    }
    request = urllib.request.Request(
        CRAWL4AI_URL,
        json.dumps(payload).encode(),
        {"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
    )
    response = (opener or _LOOPBACK_OPENER.open)(request, timeout=CRAWL4AI_TIMEOUT)
    raw = response.read(CRAWL4AI_MAX_RESPONSE + 1)
    if len(raw) > CRAWL4AI_MAX_RESPONSE:
        raise ValueError("crawl4ai_too_large")
    page = json.loads(raw)["results"][0]
    markdown = page.get("markdown")
    if isinstance(markdown, dict):
        markdown = markdown.get("raw_markdown")
    status = page.get("status_code")
    # The receipt names what was actually loaded; _canonical refuses non-https.
    loaded = page.get("redirected_url")
    if page.get("url") != url or not isinstance(loaded, str):
        raise ValueError("crawl4ai_unbound")
    final_url = source_fetch._canonical(loaded)
    if (
        page.get("success") is not True
        or type(status) is not int
        or not 200 <= status < 300
        or not isinstance(markdown, str)
        or not markdown.strip()
    ):
        raise ValueError("crawl4ai_refused")
    body = markdown.encode("utf-8")
    if len(body) > source_fetch.MAX_BYTES:
        raise ValueError("crawl4ai_too_large")
    return source_fetch.FetchResult(
        final_url=final_url,
        status=status,
        sha256=hashlib.sha256(body).hexdigest(),
        fetched_at=source_fetch._utc_millis(datetime.now(UTC)),
        content_type="text/plain; charset=utf-8; x-collector=crawl4ai",
        body=body,
    )


def _fetch_with_fallback(url, *, crawler=None):
    try:
        return source_fetch.fetch(url)
    except source_fetch.FetchFailure as error:
        if error.reason not in FALLBACK_REASONS:
            raise
        try:
            return (crawler or _crawl4ai_fetch)(url)
        except Exception:
            raise error from None


def collect(root, job, run, scheduled, item, url, *, fetcher=None):
    """Fetch exactly once per run/item; publish bytes before returning text."""
    if (
        not isinstance(item, str)
        or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", item) is None
        or not isinstance(url, str)
        or not 1 <= len(url) <= source_fetch.MAX_URL
    ):
        raise ValueError("invalid_source_request")
    source_fetch._canonical(url)
    fetcher = fetcher or _fetch_with_fallback
    name = _key(job, run, item) + ".json"
    store = PrivateRecords(root)
    try:
        with store.lock(_index_name(job, run)):
            index = _index(store, job, run, scheduled)
            entry = index["items"].get(item)
            if entry is not None and entry["source_url"] != url:
                raise ValueError("source_conflict")
            raw = store.read(name)
            if raw is not None:
                record = _decode(raw)
                result = _check(record, job, run, item, scheduled)
                if (
                    entry is None
                    or record.get("source_url") != url
                    or entry["collection_call_id"] != record["collection_call_id"]
                ):
                    raise ValueError("invalid_index")
            else:
                if entry is None and len(index["items"]) >= MAX_RUN_ITEMS:
                    raise ValueError("source_item_limit")
                if entry is not None and entry["attempts"] >= MAX_ITEM_FETCH_ATTEMPTS:
                    raise ValueError("source_attempt_limit")
                call_id = secrets.token_hex(16)
                entry = {
                    "source_url": url,
                    "attempts": 1 if entry is None else entry["attempts"] + 1,
                    "collection_call_id": call_id,
                }
                index = {**index, "items": {**index["items"], item: entry}}
                store.write(
                    _index_name(job, run),
                    json.dumps(index, sort_keys=True, ensure_ascii=False).encode(),
                )
                try:
                    result = fetcher(url)
                except source_fetch.FetchFailure as error:
                    if error.reason == "content_encoding":
                        raise ValueError("content_encoding") from None
                    raise
                record = {
                    "schema_version": "hermes-source-receipt/1",
                    "job_id": job,
                    "run_id": run,
                    "item_id": item,
                    "scheduled_at": timestamp(scheduled),
                    "source_url": url,
                    "final_url": result.final_url,
                    "status": result.status,
                    "fetched_at": result.fetched_at,
                    "body_sha256": result.sha256,
                    "content_type": result.content_type,
                    "body_b64": base64.b64encode(result.body).decode("ascii"),
                    "receipt_id": secrets.token_hex(16),
                    "collection_call_id": call_id,
                }
                _check(record, job, run, item, scheduled)
                store.write(
                    name,
                    json.dumps(record, sort_keys=True, ensure_ascii=False).encode(),
                )
            text = source_check.page_text(result)
            if len(text.encode("utf-8")) > MAX_TEXT_BYTES:
                raise ValueError("source_too_large")
            return {
                "ok": True,
                "receipt_id": record["receipt_id"],
                "item_id": item,
                "source_url": result.final_url,
                "fetched_at": result.fetched_at,
                "body_sha256": result.sha256,
                "collection_call_id": record["collection_call_id"],
                "normalized_text": text,
            }
    finally:
        store.close()


def resolve(root, job, run, scheduled, items, receipt_ids=None):
    """Pair each item with this run's own record by item_id; check stored bytes.

    ``receipt_ids`` is accepted for the tool contract but never decides pairing
    (plugin 0.4.5): one slipped receipt must not refuse the whole report. Rows
    carry the paired record's ``receipt_id`` in item order.
    """
    del receipt_ids
    if not isinstance(items, list) or not items:
        raise ValueError("source_receipts_required")
    store = PrivateRecords(root)
    rows, seen, failures = [], set(), []
    try:
        with store.lock(_index_name(job, run)):
            index = _index(store, job, run, scheduled)
            for item in items:
                if (
                    not isinstance(item, dict)
                    or not isinstance(item.get("item_id"), str)
                    or item["item_id"] in seen
                ):
                    raise ValueError("source_identity")
                item_id = item["item_id"]
                seen.add(item_id)
                raw = store.read(_key(job, run, item_id) + ".json")
                if raw is None:
                    # Keep going, so one call names every failing item.
                    failures.append({"item_id": item_id, "codes": ["source_missing"]})
                    continue
                record = _decode(raw)
                result = _check(record, job, run, item_id, scheduled)
                entry = index["items"].get(item_id)
                if (
                    entry is None
                    or entry["collection_call_id"] != record["collection_call_id"]
                    or entry["source_url"] != record["source_url"]
                ):
                    raise ValueError("source_mismatch")
                if item.get("source_url") != result.final_url:
                    failures.append(
                        {"item_id": item_id, "codes": ["source_url_mismatch"]}
                    )
                    continue
                text = source_check.page_text(result)
                if len(text.encode("utf-8")) > MAX_TEXT_BYTES:
                    raise ValueError("source_too_large")
                codes = source_check.check_item(item, text)
                if codes:
                    failures.append({"item_id": item_id, "codes": codes})
                    continue
                rows.append(
                    {
                        "item_id": item_id,
                        "source_url": result.final_url,
                        "body_sha256": result.sha256,
                        "fetched_at": result.fetched_at,
                        "collection_call_id": record["collection_call_id"],
                        "receipt_id": record["receipt_id"],
                        "text": text,
                    }
                )
        if failures:
            raise SourceQuality(failures)
        return rows
    finally:
        store.close()
