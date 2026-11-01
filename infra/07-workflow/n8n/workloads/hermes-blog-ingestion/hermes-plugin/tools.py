from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import time
import urllib.request
from pathlib import Path
from typing import Any

HERMES_HOME = Path.home() / ".hermes"
OUTBOX_DIR = HERMES_HOME / "data" / "research-report-outbox"
WEBHOOK_URL_DEFAULT = "https://n8n.local/webhook/hermes-blog-ingestion"
SECRET_FILE = HERMES_HOME / "secrets" / "research-webhook.secret"
# The Gateway binds the webhook token to this producer; the model does not choose it.
PRODUCER = "hermes"
# Hermes' plugin context, bound by register(); it reports the cron run in progress.
_CTX = None

_ALLOWED_JOBS = {
    "6eabd835f969": "news",
    "25674fbc0bf3": "devops",
    "8d0925bc571d": "business_ideas",
}
_IDENTITY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
_HTTP_TIMEOUT = 15
SOURCE_QUOTE_MAX = 500
SCHEMA_VERSION = "1.0"


def _load_url() -> str:
    env_url = os.environ.get("RESEARCH_WEBHOOK_URL")
    if env_url:
        return env_url
    env_file = HERMES_HOME / ".env"
    if env_file.is_file():
        for line in env_file.read_text().splitlines():
            if line.startswith("RESEARCH_WEBHOOK_URL="):
                return line.split("=", 1)[1].strip().strip('"')
    return WEBHOOK_URL_DEFAULT


def _load_secret() -> str:
    env_secret = os.environ.get("RESEARCH_WEBHOOK_SECRET")
    if env_secret:
        return env_secret
    if SECRET_FILE.is_file():
        return SECRET_FILE.read_text().strip()
    return ""


def _identity(value: Any) -> bool:
    return isinstance(value, str) and bool(_IDENTITY_RE.fullmatch(value))


def _validate(payload: dict[str, Any]) -> str | None:
    if payload.get("schema_version") != SCHEMA_VERSION:
        return "invalid_schema_version"
    if not _identity(payload.get("producer")):
        return "invalid_producer"
    if not _identity(payload.get("job_id")):
        return "invalid_job_id"
    if payload.get("job_id") not in _ALLOWED_JOBS:
        return "job_not_allowed"
    if not (payload.get("run_id") is not None or payload.get("fire_id") is not None):
        return "missing_run_or_fire_id"
    if payload.get("run_id") is not None and not _identity(payload.get("run_id")):
        return "invalid_run_id"
    if payload.get("fire_id") is not None and not _identity(payload.get("fire_id")):
        return "invalid_fire_id"
    if payload.get("report_kind") != _ALLOWED_JOBS[payload["job_id"]]:
        return "report_kind_mismatch"
    source_text = payload.get("source_text")
    if not isinstance(source_text, str) or not source_text:
        return "invalid_source_text"
    source_sha = payload.get("source_sha256")
    if not _SHA256_RE.fullmatch(source_sha or ""):
        return "invalid_source_sha256"
    if hashlib.sha256(source_text.encode("utf-8")).hexdigest() != source_sha:
        return "source_sha_mismatch"
    if not _identity(payload.get("idempotency_key")):
        return "invalid_idempotency_key"
    items = payload.get("items")
    if not isinstance(items, list) or not (1 <= len(items) <= 100):
        return "invalid_items"
    for item in items:
        if not isinstance(item, dict):
            return "invalid_item"
        for field in ("item_id", "kind", "title", "body"):
            if field not in item:
                return f"missing_{field}"
        if not _identity(item.get("item_id")):
            return "invalid_item_id"
        if item.get("kind") not in (
            "news",
            "devops",
            "business_idea",
            "infrastructure",
        ):
            return "invalid_item_kind"
        if not (1 <= len(item.get("title", "")) <= 300):
            return "invalid_title"
        if not (1 <= len(item.get("body", "")) <= 32768):
            return "invalid_body"
        if "source_url" in item and item["source_url"] is not None:
            if (
                not isinstance(item["source_url"], str)
                or len(item["source_url"]) > 2048
            ):
                return "invalid_source_url"
        if "source_quotes" in item:
            quotes = item["source_quotes"]
            if not isinstance(quotes, list) or not (1 <= len(quotes) <= 3):
                return "invalid_source_quotes"
            for quote in quotes:
                if (
                    not isinstance(quote, str)
                    or not quote.strip()
                    or len(quote) > SOURCE_QUOTE_MAX
                ):
                    return "invalid_source_quote"
    for field in ("scheduled_at", "generated_at", "collected_at"):
        value = payload.get(field)
        if not isinstance(value, str) or not value:
            return f"missing_{field}"
    source_ref = payload.get("source_ref")
    if not isinstance(source_ref, str) or not (1 <= len(source_ref) <= 1024):
        return "invalid_source_ref"
    if "companion_evidence" in payload:
        return "companion_evidence_not_allowed_in_gateway_request"
    return None


def _allowed_url(url: str) -> bool:
    from urllib.parse import urlsplit

    parsed = urlsplit(url)
    if parsed.scheme == "https":
        return True
    if parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost"}:
        return True
    return False


def handle_submit_report(args: dict[str, Any], **kwargs) -> str:
    """Hermes tool entry point: the registry accepts only a str result."""
    return json.dumps(_submit(args), ensure_ascii=False)


def _submit(args: dict[str, Any]) -> dict[str, Any]:
    payload = args.get("payload") if isinstance(args, dict) else None
    if not isinstance(payload, dict):
        payload = args if isinstance(args, dict) else {}
    run = _CTX.current_cron_execution() if _CTX is not None else None
    if run is None:
        return {"ok": False, "error": "not_a_cron_run"}
    if run.job_id not in _ALLOWED_JOBS:
        return {"ok": False, "error": "job_not_allowed"}
    # Identity comes from the scheduler and the token, not from the model.
    payload = {
        **payload,
        "producer": PRODUCER,
        "job_id": run.job_id,
        "report_kind": _ALLOWED_JOBS[run.job_id],
        "run_id": run.execution_id,
        "idempotency_key": f"{run.job_id}-{run.execution_id}",
    }

    error = _validate(payload)
    if error:
        return {"ok": False, "error": error}

    idem = payload["idempotency_key"]
    gateway_payload = {k: v for k, v in payload.items() if k != "companion_evidence"}
    payload_bytes = json.dumps(
        gateway_payload, ensure_ascii=False, sort_keys=True
    ).encode("utf-8")
    payload_sha = hashlib.sha256(payload_bytes).hexdigest()

    OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(OUTBOX_DIR, 0o700)
    except OSError:
        pass
    key = f"{payload['job_id']}:{idem}"
    record_path = OUTBOX_DIR / f"{key}.json"

    existing = None
    if record_path.is_file():
        try:
            existing = json.loads(record_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            corrupt = record_path.with_suffix(f".corrupt.{int(time.time())}.json")
            try:
                record_path.rename(corrupt)
            except OSError:
                pass
            existing = None

    if existing is not None:
        if existing.get("payload_sha256") != payload_sha:
            return {"ok": False, "error": "idempotency_conflict"}
        if existing.get("status") == "persisted":
            return {
                "ok": True,
                "status": "already_persisted",
                "receipt": existing.get("response"),
            }
        stored_b64 = existing.get("payload_b64")
        if stored_b64:
            try:
                payload_bytes = base64.b64decode(stored_b64)
            except Exception:
                pass

    record = {
        "key": key,
        "job_id": payload["job_id"],
        "idempotency_key": idem,
        "payload_sha256": payload_sha,
        "payload_b64": base64.b64encode(payload_bytes).decode("ascii"),
        "status": "pending",
        "submitted_at": time.time(),
        "attempts": 0,
        "last_error": None,
        "url": None,
    }
    tmp = record_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
    tmp.replace(record_path)
    try:
        os.chmod(record_path, 0o600)
    except OSError:
        pass

    url = _load_url()
    if not _allowed_url(url):
        record["status"] = "failed"
        record["last_error"] = "disallowed_url"
        record_path.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
        return {"ok": False, "error": "disallowed_url"}

    secret = _load_secret()
    headers = {
        "Content-Type": "application/json",
        "X-Hermes-Ingest-Token": secret,
    }
    record["url"] = url

    attempts = 0
    last_error = None
    response_obj = None
    status_code = None
    persisted = False
    retryable_statuses = {429, 500, 502, 503, 504}
    non_retryable = {401, 403, 409, 422}
    for attempt in range(1, 4):
        attempts = attempt
        try:

            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, *a, **kw):
                    return None

            req = urllib.request.Request(
                url, data=payload_bytes, headers=headers, method="POST"
            )
            opener = urllib.request.build_opener(NoRedirect)
            with opener.open(req, timeout=_HTTP_TIMEOUT) as resp:
                status_code = resp.getcode()
                raw = resp.read()
                try:
                    response_obj = json.loads(raw.decode("utf-8"))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    response_obj = None
                if (
                    status_code in (200, 201)
                    and isinstance(response_obj, dict)
                    and response_obj.get("persisted") is True
                ):
                    persisted = True
                    break
                last_error = f"http_{status_code}_not_persisted"
                if (
                    status_code in non_retryable
                    or status_code not in retryable_statuses
                ):
                    break
        except urllib.request.HTTPError as exc:
            status_code = exc.code
            last_error = f"http_{exc.code}"
            if exc.code in non_retryable or exc.code not in retryable_statuses:
                break
        except Exception:
            last_error = "network_or_timeout"
        if not persisted:
            time.sleep(min(2 * attempt, 5))

    record["attempts"] = attempts
    record["last_error"] = last_error
    record["status"] = "persisted" if persisted else "failed"
    record["status_code"] = status_code
    record["response"] = response_obj
    record_path.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
    try:
        os.chmod(record_path, 0o600)
    except OSError:
        pass

    if not persisted:
        return {
            "ok": False,
            "error": "delivery_failed",
            "status_code": status_code,
            "error_type": last_error,
            "idempotency_key": idem,
        }
    return {
        "ok": True,
        "status": "persisted",
        "status_code": status_code,
        "response": response_obj,
        "idempotency_key": idem,
    }


SUBMIT_RESEARCH_REPORT_SCHEMA = {
    "name": "submit_research_report",
    "description": "Submit a structured research report to the configured n8n webhook.",
    "parameters": {
        "type": "object",
        "properties": {"payload": {"type": "object"}},
        "required": ["payload"],
    },
}
