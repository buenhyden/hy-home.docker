"""Harness for tests/e2e-ingress.sh: the real attester against throwaway Traefik.

Test only. The throwaway Traefik serves a self-signed certificate, so the
reader's opener and the sender here skip verification; production code
(`GatewayReader`, `HttpTransport`) keeps the system CA store and has no switch.
Usage: e2e_attest_harness.py <config.json> run|resend|forge ...
"""

import base64
import hashlib
import http.client
import json
import socket
import ssl
import sys
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)
from publisher import attestation, attester
from publisher.source_fetch import FetchFailure, FetchResult


def NOW():  # the Gateway refuses a fetched_at ahead of its own clock
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


HOST = "blog-export.hy.home.arpa"
cfg = json.load(open(sys.argv[1]))
work = Path(cfg["work"])
auth = ("Authorization", "Bearer " + cfg["attest_token"])
context = ssl.create_default_context()
context.minimum_version = ssl.TLSVersion.TLSv1_2
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


def _call(method, path, headers, body=None):
    raw = socket.create_connection((cfg["lan_ip"], cfg["port"]), 30)
    connection = http.client.HTTPSConnection(HOST, cfg["port"], context=context)
    connection.sock = context.wrap_socket(raw, server_hostname=HOST)
    try:
        connection.request(method, path, body=body, headers=headers)
        response = connection.getresponse()
        return response.status, response.read()
    finally:
        connection.close()


def opener(host, port, path, headers):
    return _call("GET", path, headers)


def send(report_id, body):
    status, answer = _call(
        "POST",
        f"/v1/ingestions/{report_id}/attestations",
        {auth[0]: auth[1], "Content-Type": "application/json"},
        body,
    )
    with open(work / "sends.log", "a") as log:
        log.write(f"{report_id} {status} {answer[:200]!r}\n")
    return SimpleNamespace(status=status)


def page(url, text):
    body = f"<html><body><p>{text}</p></body></html>".encode()
    return FetchResult(
        url, 200, hashlib.sha256(body).hexdigest(),
        NOW(), "text/html; charset=utf-8", body,
    )  # fmt: skip


def fetcher(url):
    # Fixed pages, no network: A supports its item, B contradicts its item.
    pages = json.load(open(cfg["pages"]))
    if url not in pages:
        raise FetchFailure("not_found")
    return page(url, pages[url])


reader = attester.GatewayReader(f"https://{HOST}:{cfg['port']}", auth, opener=opener)
command = sys.argv[2]
if command == "run":
    key = attestation.load_signing_key(cfg["key"])
    print(json.dumps(attester.run(
        reader, send, key_id="attest-e2e", key=key,
        state_dir=work / "state", evidence_dir=work / "evidence", fetcher=fetcher,
    ), sort_keys=True))  # fmt: skip
elif command == "resend":  # the stored signed body, byte for byte
    state = json.load(open(work / "state" / f"{sys.argv[3]}.json"))
    print(send(sys.argv[3], base64.b64decode(state["body"])).status)
elif command == "forge":  # forge <report_id> forged|tampered <out>
    report_id, kind, out = sys.argv[3:]
    request = reader.request(report_id)
    item = [{"item_id": "x-1", "fetched_at": NOW(),
             "final_url": "https://example.org/page"}]  # fmt: skip
    digest = hashlib.sha256(b"x").hexdigest()
    if kind == "forged":
        key = Ed25519PrivateKey.generate()  # not in export.attestation_keys
        signed = attestation.message(request, item, digest)
        body = attestation.request_body("attest-e2e", key, signed, item, digest)
    else:  # valid key, but the signature covers no verified items
        key = attestation.load_signing_key(cfg["key"])
        signed = attestation.message(request, [], digest)
        body = attestation.request_body("attest-e2e", key, signed, item, digest)
    Path(out).write_bytes(body)
