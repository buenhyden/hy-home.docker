from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any

from . import schemas

HERMES_HOME = Path.home() / ".hermes"
OUTBOX = HERMES_HOME / "data" / "research-report-outbox.json"
WEBHOOK_URL = (
    os.environ.get("RESEARCH_WEBHOOK_URL")
    or "https://n8n.local/webhook/hermes-blog-ingestion"
)
SECRET_FILE = HERMES_HOME / "secrets" / "research-webhook.secret"


def _load_url() -> str:
    env_url = os.environ.get("RESEARCH_WEBHOOK_URL")
    if env_url:
        return env_url
    env_file = HERMES_HOME / ".env"
    if env_file.is_file():
        for line in env_file.read_text().splitlines():
            if line.startswith("RESEARCH_WEBHOOK_URL="):
                return line.split("=", 1)[1].strip().strip('"')
    return WEBHOOK_URL


def _load_secret() -> str:
    env_secret = os.environ.get("RESEARCH_WEBHOOK_SECRET")
    if env_secret:
        return env_secret
    if SECRET_FILE.is_file():
        return SECRET_FILE.read_text().strip()
    return ""


def _hash_bytes(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def handle_submit_report(args: dict[str, Any], **kwargs) -> dict[str, Any]:
    payload = args.get("payload") if isinstance(args, dict) else None
    if not isinstance(payload, dict):
        payload = args if isinstance(args, dict) else {}
    job_id = payload.get("job_id")
    if job_id not in schemas.ALLOWED_JOBS:
        return {"ok": False, "error": "job_not_allowed", "job_id": job_id}

    for field in schemas.REPORT_SCHEMA["required"]:
        if field not in payload:
            return {"ok": False, "error": "missing_field", "field": field}

    expected_kind = schemas.ALLOWED_REPORT_KINDS.get(job_id)
    if payload.get("report_kind") != expected_kind:
        return {"ok": False, "error": "report_kind_mismatch", "expected": expected_kind}

    items = payload.get("items")
    if not isinstance(items, list) or not items:
        return {"ok": False, "error": "invalid_items"}

    companion = payload.get("companion_evidence")
    if companion is not None and not isinstance(companion, dict):
        return {"ok": False, "error": "invalid_companion_evidence"}

    outbox: dict[str, Any] = {}
    if OUTBOX.is_file():
        try:
            outbox = json.loads(OUTBOX.read_text())
        except Exception:
            outbox = {}

    idem = payload.get("idempotency_key")
    key = f"{job_id}:{idem}"
    existing = outbox.get(key)
    if existing and existing.get("status") in ("delivered", "persisted"):
        return {
            "ok": True,
            "status": "already_delivered",
            "receipt": existing.get("response"),
        }

    url = _load_url()
    secret = _load_secret()
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if secret:
        headers["Authorization"] = f"Bearer {secret}"

    attempts = 0
    last_error = None
    response_obj = None
    status_code = None
    persisted = False
    for attempt in range(1, 3):
        attempts = attempt
        try:
            req = urllib.request.Request(url, data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=15) as resp:
                status_code = resp.getcode()
                raw = resp.read()
                try:
                    response_obj = json.loads(raw.decode("utf-8"))
                except Exception:
                    response_obj = {"raw": raw.decode("utf-8", "replace")}
                if (
                    status_code in (200, 201)
                    and isinstance(response_obj, dict)
                    and response_obj.get("persisted") is True
                ):
                    persisted = True
                    break
                last_error = f"http_{status_code}_not_persisted"
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {exc}"
        time.sleep(1)

    record = {
        "submitted_at": int(time.time()),
        "attempts": attempts,
        "last_error": last_error,
        "status": "delivered" if persisted else "failed",
        "url": url,
        "payload_sha256": hashlib.sha256(body).hexdigest(),
        "response": response_obj,
        "status_code": status_code,
    }
    outbox[key] = record
    OUTBOX.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUTBOX.with_suffix(".tmp")
    tmp.write_text(json.dumps(outbox, ensure_ascii=False, indent=2))
    tmp.replace(OUTBOX)

    if not persisted:
        return {
            "ok": False,
            "error": "delivery_failed",
            "status_code": status_code,
            "error_detail": last_error,
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
        "properties": {
            "payload": {
                "type": "object",
                "description": "The structured research report payload.",
            }
        },
        "required": ["payload"],
    },
}
