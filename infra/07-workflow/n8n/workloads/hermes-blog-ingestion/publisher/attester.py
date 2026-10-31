"""Queue attester: verify each queued report's items against their sources.

Only items whose quotes were found on the fetched page are signed; the signed
body is stored before it is sent, so a lost response resends identical bytes.
Logs and counts never carry item text, URLs or credentials.
"""

import base64
import hashlib
import http.client
import json
import os
import ssl
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path
from urllib.parse import urlsplit

from . import attestation
from .candidates import JOBS
from .delivery import FailureKind, TransportFailure
from .outbox import valid_gateway_report_id
from .source_check import check_item, page_text
from .source_fetch import FetchFailure, fetch

VERIFIER = "hy-home-attester/1"
MAX_ITEMS = 100
MAX_RESPONSE = 4 * 1024 * 1024
_TIME = "%Y-%m-%dT%H:%M:%SZ"


class GatewayError(ValueError):
    pass


def _https_opener(host, port, path, headers):
    connection = http.client.HTTPSConnection(
        host, port, timeout=30, context=ssl.create_default_context()
    )
    try:
        connection.request("GET", path, headers=headers)
        response = connection.getresponse()
        body = response.read(MAX_RESPONSE + 1)
        return response.status, body
    except http.client.HTTPException:
        raise GatewayError("http_protocol") from None
    finally:
        connection.close()


class GatewayReader:
    def __init__(self, base_url, auth_header, *, opener=None):
        parts = urlsplit(base_url)
        if (
            parts.scheme != "https"
            or not parts.hostname
            or parts.username
            or parts.path not in ("", "/")
            or parts.query
        ):
            raise GatewayError("gateway_url")
        self._host = parts.hostname
        self._port = parts.port or 443
        name, value = auth_header
        # Held in memory only; http.client rejects control characters in it.
        self._headers = {name: value, "Accept": "application/json"}
        self._open = opener or _https_opener

    def _get(self, path):
        status, body = self._open(self._host, self._port, path, self._headers)
        if len(body) > MAX_RESPONSE:
            raise GatewayError("response_too_large")
        return status, body

    def queue(self):
        after = 0
        while True:
            status, body = self._get(
                f"/v1/attestation-queue?limit={MAX_ITEMS}&after={after}"
            )
            if status != 200:
                raise GatewayError("queue_status")
            try:
                data = json.loads(body)
                ids = [entry["report_id"] for entry in data["items"]]
                following = data["next_after"]
            except (ValueError, KeyError, TypeError):
                raise GatewayError("queue_shape") from None
            yield from ids
            if following is None:
                return
            # A cursor that does not advance would loop forever.
            if type(following) is not int or following <= after:
                raise GatewayError("queue_cursor")
            after = following

    def request(self, report_id):
        if not valid_gateway_report_id(report_id):
            raise GatewayError("report_id")
        status, body = self._get(f"/v1/ingestions/{report_id}/request")
        if status == 200:
            return body
        if status == 409 and b"REPORT_QUARANTINED" in body:
            return None
        raise GatewayError("request_status")


def _private_dir(path):
    if not path.is_dir():
        path.mkdir(mode=0o700, parents=True, exist_ok=True)
        path.chmod(0o700)


def _write(path, data):
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=".tmp-")
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    except BaseException:
        os.unlink(temporary)
        raise


def _load(path):
    try:
        return json.loads(path.read_bytes())
    except FileNotFoundError:
        return {}


def _save(path, state):
    _write(path, json.dumps(state, sort_keys=True).encode())


def _entry(item_id, url, result, codes, fetched=None):
    return {
        "item_id": item_id,
        "url": url,
        "final_url": fetched.final_url if fetched else None,
        "status": fetched.status if fetched else None,
        "response_sha256": fetched.sha256 if fetched else None,
        "fetched_at": fetched.fetched_at if fetched else None,
        "result": result,
        "codes": codes,
    }


def run(
    reader,
    send,
    *,
    key_id,
    key,
    state_dir,
    evidence_dir,
    fetcher=fetch,
    now=None,
    retry=timedelta(hours=6),
):
    now = now or (lambda: datetime.now(UTC))
    state_dir, evidence_dir = Path(state_dir), Path(evidence_dir)
    _private_dir(state_dir)
    _private_dir(evidence_dir)
    counts = dict(attested=0, held_items=0, skipped=0, retry=0, rejected=0)
    errors = {}
    halt = []
    cache = {}  # url -> FetchResult | FetchFailure, one fetch per URL per run

    def fetch_once(url):
        if url not in cache:
            try:
                cache[url] = fetcher(url)
            except FetchFailure as failure:
                cache[url] = failure
            except UnicodeError:  # e.g. a lone surrogate in the URL: never fetchable
                cache[url] = FetchFailure("url")
        return cache[url]

    def deliver(path, state):
        try:
            result = send(state["report_id"], base64.b64decode(state["body"]))
        except TransportFailure as failure:
            result = failure
        verdict = attestation.outcome(result)
        # A credential, certificate or body-cap (413) problem says nothing about the content:
        # keep the signed body for the next run and stop sending in this one.
        if verdict == "rejected" and (
            (
                isinstance(result, TransportFailure)
                and result.kind in (FailureKind.AUTH, FailureKind.TLS)
            )
            or getattr(result, "status", None) in (401, 403, 413)
        ):
            counts["rejected"] += 1
            halt.append(True)
        elif verdict == "attested":
            state["status"] = "attested"
            _save(path, state)
            counts["attested"] += 1
        elif verdict == "rejected":
            state["status"] = "rejected"
            _save(path, state)
            counts["rejected"] += 1
        else:
            counts["retry"] += 1

    def check_items(request):
        """Return (verified, evidence entries, pending flag)."""
        items = request.get("items")
        if request.get("job_id") not in JOBS:
            items = (
                [i for i in items if isinstance(i, dict)]
                if isinstance(items, list)
                else []
            )
            return (
                [],
                [
                    _entry(i.get("item_id"), None, "unverified", ["job_unapproved"])
                    for i in items
                ],
                False,
            )
        verified, entries, pending, seen = [], [], False, set()
        for raw in items if isinstance(items, list) else []:
            if not isinstance(raw, dict):
                continue
            item_id, url = raw.get("item_id"), raw.get("source_url")
            if not isinstance(item_id, str) or not item_id or item_id in seen:
                entries.append(_entry(None, None, "unverified", ["item_id"]))
                continue
            seen.add(item_id)
            url = url if isinstance(url, str) else None
            early = [
                c
                for c in check_item(raw, "")
                if c in ("field_missing", "quotes_missing")
            ]
            if early:
                entries.append(_entry(item_id, url, "unverified", early))
                continue
            found = fetch_once(url)
            if isinstance(found, FetchFailure):
                if found.transient:
                    pending = True
                    entries.append(_entry(item_id, url, "pending", [found.reason]))
                else:
                    entries.append(_entry(item_id, url, "unverified", [found.reason]))
                continue
            codes = check_item(raw, page_text(found))
            entries.append(
                _entry(
                    item_id, url, "unverified" if codes else "verified", codes, found
                )
            )
            if not codes:
                verified.append(
                    {
                        "item_id": item_id,
                        "fetched_at": found.fetched_at,
                        "final_url": found.final_url,
                    }
                )
        return verified, entries, pending

    def process(report_id):
        path = state_dir / f"{report_id}.json"
        state = _load(path)
        status = state.get("status")
        if status in ("attested", "rejected", "skipped"):
            counts["skipped"] += 1
            return
        if "body" in state:  # signed: only ever resend the stored bytes
            deliver(path, state)
            return
        raw = reader.request(report_id)
        if raw is None:
            _save(path, {"status": "skipped"})
            counts["skipped"] += 1
            return
        state.setdefault("first_attempt_at", now().strftime(_TIME))
        _save(path, state)
        try:
            request = json.loads(raw)
            if not isinstance(request, dict):
                raise attestation.AttestationError("request_invalid")
            verified, entries, pending = check_items(request)
            if pending:
                started = datetime.strptime(state["first_attempt_at"], _TIME).replace(
                    tzinfo=UTC
                )
                if now() - started < retry:
                    counts["retry"] += 1
                    return
                for entry in entries:
                    if entry["result"] == "pending":
                        entry["result"] = "unverified"
            verified.sort(key=lambda i: i["item_id"])
            for extra in verified[MAX_ITEMS:]:
                for entry in entries:
                    if entry["item_id"] == extra["item_id"]:
                        entry.update(result="unverified", codes=["limit"])
            verified = verified[:MAX_ITEMS]
            held = sum(1 for e in entries if e["result"] != "verified")
            evidence = attestation._canonical(
                {"verifier": VERIFIER, "report_id": report_id, "items": entries}
            )
            digest = hashlib.sha256(evidence).hexdigest()
            signed = attestation.message(raw, verified, digest)
            body = attestation.request_body(key_id, key, signed, verified, digest)
        except (attestation.AttestationError, json.JSONDecodeError):
            state["status"] = "rejected"
            _save(path, state)
            counts["rejected"] += 1
            return
        _write(evidence_dir / f"{report_id}.json", evidence)
        state.update(
            report_id=report_id,
            status="signed",
            body=base64.b64encode(body).decode("ascii"),
        )
        _save(path, state)
        counts["held_items"] += held
        deliver(path, state)

    for report_id in reader.queue():
        if halt:
            break
        try:
            if not valid_gateway_report_id(report_id):
                raise GatewayError("report_id")
            process(report_id)
        except Exception as error:  # one bad report must not stop the run
            counts["rejected"] += 1
            errors[type(error).__name__] = errors.get(type(error).__name__, 0) + 1
    return counts | ({"errors": errors} if errors else {})
