"""Queue attester: verify each queued report's items against their sources.

Only items whose quotes were found on the fetched page are signed; the signed
body is stored before it is sent, so a lost response resends identical bytes.
Logs and counts never carry item text, URLs or credentials.
"""

import base64
import hashlib
import http.client
import json
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path
from urllib.parse import urlsplit

from . import attestation, source_fetch
from .candidates import JOBS
from .delivery import FailureKind, TransportFailure
from .outbox import valid_gateway_report_id
from .private_records import PrivateRecords, RecordError
from .source_check import check_item, page_text
from .source_fetch import FetchFailure, fetch

VERIFIER = "hy-home-attester/1"
MAX_ITEMS = 100
MAX_QUEUE_PAGES = 10
MAX_QUEUE_REPORTS = 100
MAX_RESPONSE = 4 * 1024 * 1024
_TIME = "%Y-%m-%dT%H:%M:%SZ"


class GatewayError(ValueError):
    pass


def _https_opener(host, port, path, headers):
    connection = http.client.HTTPSConnection(
        host, port, timeout=30, context=source_fetch.tls_context()
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
        pages = 0
        while True:
            if pages >= MAX_QUEUE_PAGES:
                raise GatewayError("queue_page_limit")
            pages += 1
            status, body = self._get(
                f"/v1/attestation-queue?limit={MAX_ITEMS}&after={after}"
            )
            if status != 200:
                raise GatewayError("queue_status")
            try:
                data = _strict_json(body)
                if (
                    not isinstance(data, dict)
                    or set(data) != {"items", "next_after"}
                    or not isinstance(data["items"], list)
                    or len(data["items"]) > MAX_ITEMS
                    or any(
                        not isinstance(entry, dict)
                        or not valid_gateway_report_id(entry.get("report_id"))
                        for entry in data["items"]
                    )
                ):
                    raise ValueError("queue_shape")
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


def _strict_json(raw):
    def unique(pairs):
        value = {}
        for name, item in pairs:
            if name in value:
                raise ValueError("duplicate_key")
            value[name] = item
        return value

    def invalid(_value):
        raise ValueError("invalid_constant")

    return json.loads(raw, object_pairs_hook=unique, parse_constant=invalid)


def _valid_evidence(value, report_id, verified_items, request_items):
    if (
        not isinstance(value, dict)
        or set(value) != {"verifier", "report_id", "items"}
        or value["verifier"] != VERIFIER
        or value["report_id"] != report_id
        or not isinstance(value["items"], list)
        or len(value["items"]) > MAX_ITEMS
        or not isinstance(request_items, list)
        or len(request_items) != len(value["items"])
    ):
        return False
    expected = []
    names = {
        "item_id",
        "url",
        "final_url",
        "status",
        "response_sha256",
        "fetched_at",
        "result",
        "codes",
    }
    for item, requested in zip(value["items"], request_items, strict=True):
        if (
            not isinstance(item, dict)
            or not isinstance(requested, dict)
            or set(item) != names
            or not isinstance(item["item_id"], str)
            or item["item_id"] != requested.get("item_id")
            or item["result"] not in ("verified", "unverified")
            or not isinstance(item["codes"], list)
            or any(not isinstance(code, str) for code in item["codes"])
            or (
                item["result"] == "verified"
                and (
                    item["codes"]
                    or type(item["status"]) is not int
                    or not 200 <= item["status"] < 300
                    or not isinstance(item["response_sha256"], str)
                    or re.fullmatch(r"[a-f0-9]{64}", item["response_sha256"]) is None
                )
            )
            or (item["result"] == "unverified" and not item["codes"])
        ):
            return False
        if item["result"] == "verified":
            expected.append(
                {
                    "item_id": item["item_id"],
                    "final_url": item["final_url"],
                    "fetched_at": item["fetched_at"],
                }
            )
    return sorted(expected, key=lambda item: item["item_id"]) == verified_items


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
    states = PrivateRecords(state_dir)
    evidences = PrivateRecords(evidence_dir)
    counts = dict(attested=0, held_items=0, skipped=0, retry=0, rejected=0)
    errors = {}
    halt = []
    active_reports = 0
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

    def save(report_id, state):
        states.write(report_id + ".json", json.dumps(state, sort_keys=True).encode())

    def deliver(report_id, state, raw=None):
        # The queue ID, on-disk state, evidence and signature must describe the
        # same request before any network replay, including legacy snapshots.
        try:
            if state.get("report_id") != report_id or state.get("status") != "signed":
                raise ValueError
            raw = reader.request(report_id) if raw is None else raw
            if raw is None:
                raise ValueError
            evidence = evidences.read(report_id + ".json")
            body = base64.b64decode(state["body"], validate=True)
            envelope = _strict_json(body)
            evidence_object = (
                _strict_json(evidence) if isinstance(evidence, bytes) else None
            )
            request_object = _strict_json(raw)
            if (
                not isinstance(envelope, dict)
                or set(envelope)
                != {
                    "schema_version",
                    "key_id",
                    "algorithm",
                    "signature",
                    "verified_items",
                    "evidence_sha256",
                }
                or envelope.get("key_id") != key_id
                or envelope.get("schema_version") != "2.0"
                or envelope.get("algorithm") != "ed25519"
                or not isinstance(evidence, bytes)
                or hashlib.sha256(evidence).hexdigest()
                != envelope.get("evidence_sha256")
                or not isinstance(request_object, dict)
                or not _valid_evidence(
                    evidence_object,
                    report_id,
                    envelope.get("verified_items"),
                    request_object.get("items"),
                )
                or state.get("request_sha256") != hashlib.sha256(raw).hexdigest()
            ):
                raise ValueError
            message = attestation.message(
                raw, envelope["verified_items"], envelope["evidence_sha256"]
            )
            key.public_key().verify(
                base64.b64decode(envelope["signature"], validate=True), message
            )
        except Exception:
            counts["rejected"] += 1
            return
        try:
            result = send(report_id, body)
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
            save(report_id, state)
            counts["attested"] += 1
        elif verdict == "rejected":
            state["status"] = "rejected"
            save(report_id, state)
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
        for position, raw in enumerate(items if isinstance(items, list) else []):
            if not isinstance(raw, dict):
                continue
            item_id, url = raw.get("item_id"), raw.get("source_url")
            if not isinstance(item_id, str) or not item_id or item_id in seen:
                entries.append(_entry(None, None, "unverified", ["item_id"]))
                continue
            seen.add(item_id)
            url = url if isinstance(url, str) else None
            if position >= MAX_ITEMS:
                entries.append(_entry(item_id, url, "unverified", ["limit"]))
                continue
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
        nonlocal active_reports
        raw_state = states.read(report_id + ".json")
        state = _strict_json(raw_state) if raw_state is not None else {}
        if not isinstance(state, dict) or (
            "report_id" in state and state["report_id"] != report_id
        ):
            raise RecordError("state_identity")
        if set(state) - {
            "first_attempt_at",
            "report_id",
            "status",
            "body",
            "request_sha256",
        }:
            raise RecordError("state_shape")
        status = state.get("status")
        if status in ("attested", "rejected", "skipped"):
            counts["skipped"] += 1
            return
        if active_reports >= MAX_QUEUE_REPORTS:
            counts["retry"] += 1
            halt.append(True)
            return
        active_reports += 1
        if "body" in state:  # signed: only ever resend the stored bytes
            deliver(report_id, state)
            return
        raw = reader.request(report_id)
        if raw is None:
            save(report_id, {"status": "skipped"})
            counts["skipped"] += 1
            return
        state.setdefault("first_attempt_at", now().strftime(_TIME))
        save(report_id, state)
        try:
            request = _strict_json(raw)
            if not isinstance(request, dict):
                raise attestation.AttestationError("request_invalid")
            # Reject ambiguous/noncanonical stored requests before source I/O.
            attestation.message(raw, [], "0" * 64)
            items = request.get("items")
            if (
                not isinstance(items, list)
                or not 1 <= len(items) <= MAX_ITEMS
                or any(
                    not isinstance(item, dict)
                    or not isinstance(item.get("item_id"), str)
                    or not item["item_id"]
                    for item in items
                )
                or len({item["item_id"] for item in items}) != len(items)
            ):
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
            save(report_id, state)
            counts["rejected"] += 1
            return
        if evidences.read(report_id + ".json") is not None:
            raise RecordError("orphan_evidence")
        evidences.write(report_id + ".json", evidence)
        state.update(
            report_id=report_id,
            status="signed",
            body=base64.b64encode(body).decode("ascii"),
            request_sha256=hashlib.sha256(raw).hexdigest(),
        )
        save(report_id, state)
        counts["held_items"] += held
        deliver(report_id, state, raw)

    seen_reports = set()
    try:
        for report_id in reader.queue():
            if halt:
                break
            try:
                if not valid_gateway_report_id(report_id):
                    raise GatewayError("report_id")
                if report_id in seen_reports:
                    counts["rejected"] += 1
                    errors["duplicate_report"] = errors.get("duplicate_report", 0) + 1
                    continue
                seen_reports.add(report_id)
                with states.lock(report_id):
                    process(report_id)
            except Exception as error:  # one bad report must not stop the run
                counts["rejected"] += 1
                errors[type(error).__name__] = errors.get(type(error).__name__, 0) + 1
    except GatewayError:
        counts["rejected"] += 1
        errors["GatewayError"] = errors.get("GatewayError", 0) + 1
    finally:
        states.close()
        evidences.close()
    return counts | ({"errors": errors} if errors else {})
