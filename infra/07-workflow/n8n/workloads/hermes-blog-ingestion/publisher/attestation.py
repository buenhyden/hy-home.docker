"""Blog-data attestation/2: the Gateway-verified signature over a report.

The signed bytes bind the stored request (its SHA-256 is recomputed here, never
trusted), the items whose source was fetched and quoted, and the evidence hash.
The signature uses a separate key from the Hermes companion signature.
"""

import base64
import hashlib
import json
import os
import re
import stat
from pathlib import Path

from .delivery import FailureKind, TransportFailure
from .files import InputError, open_directory

PREFIX = b"blog-data-attestation/2\x00"
DESTINATION = "blog-data-attestation"
_IDENTITY = ("producer", "job_id", "run_id", "fire_id", "source_sha256")
_ITEM_KEYS = {"item_id", "fetched_at", "final_url"}
_FETCHED_AT = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d{3})?Z")
_SHA256 = re.compile(r"[0-9a-f]{64}")
_URL_FORBIDDEN = re.compile(r"[\s\x00-\x1f\x7f]")


class AttestationError(ValueError):
    pass


def _canonical(value):
    # Blog-data contract.mjs canonical(): sorted keys, no spaces, raw UTF-8.
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()


def _check(verified_items, evidence_sha256):
    """Shape the Gateway also enforces; the Gateway stays the authority."""
    ok = (
        isinstance(evidence_sha256, str)
        and _SHA256.fullmatch(evidence_sha256)
        and isinstance(verified_items, list)
        and len(verified_items) <= 100
    )
    previous = None
    for item in verified_items if ok else ():
        ok = (
            isinstance(item, dict)
            and set(item) == _ITEM_KEYS
            and all(isinstance(item[k], str) for k in _ITEM_KEYS)
            and item["item_id"] != ""
            and (previous is None or previous < item["item_id"])
            and _FETCHED_AT.fullmatch(item["fetched_at"])
            and item["final_url"].startswith("https://")
            and len(item["final_url"]) <= 2048
            and "@" not in item["final_url"].split("/")[2]
            and not _URL_FORBIDDEN.search(item["final_url"])
        )
        if not ok:
            break
        previous = item["item_id"]
    if not ok:
        raise AttestationError("verified_items")


def message(request_bytes, verified_items, evidence_sha256):
    """Bytes the Gateway verifies: prefix + identity, content and verified items.

    request_bytes are the canonical bytes GET /v1/ingestions/{id}/request
    returns; their SHA-256 is content_sha256 and is recomputed, not trusted.
    """
    _check(verified_items, evidence_sha256)
    try:
        request = json.loads(request_bytes)
        if not isinstance(request, dict) or not all(
            isinstance(request.get(name), str)
            for name in ("producer", "job_id", "source_sha256")
        ):
            raise ValueError
    except (ValueError, UnicodeError):
        raise AttestationError("request_invalid") from None
    content = {k: v for k, v in request.items() if k != "idempotency_key"}
    if _canonical(content) != request_bytes:
        raise AttestationError("fingerprint")
    signed = {name: request.get(name) for name in _IDENTITY}
    signed["content_sha256"] = hashlib.sha256(request_bytes).hexdigest()
    signed["verified_items"] = verified_items
    signed["evidence_sha256"] = evidence_sha256
    return PREFIX + _canonical(signed)


def load_signing_key(path):
    """Load an Ed25519 key readable only by its owner or the attester's group.

    Every ancestor is pinned without following symlinks, and the directory
    holding the key must not be writable by anyone but its owner, so another
    account can neither read nor swap the key.
    """
    path = Path(path)
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK
    try:
        with open_directory(path.parent) as directory:
            parent = os.fstat(directory)
            descriptor = os.open(path.name, flags, dir_fd=directory)
    except (OSError, InputError):
        raise AttestationError("key_unavailable") from None
    try:
        info = os.fstat(descriptor)
        mode = stat.S_IMODE(info.st_mode)
        if (
            parent.st_uid not in (0, os.getuid())
            or stat.S_IMODE(parent.st_mode) & 0o022
            or not stat.S_ISREG(info.st_mode)
            or info.st_nlink != 1
            or info.st_uid not in (0, os.getuid())
            # Owner read/write and group read at most; nothing for others.
            or mode & ~0o640
            # A group may read it only if that group is the attester's own.
            or (mode & 0o040 and info.st_gid != os.getegid())
            or info.st_size > 4096
        ):
            raise AttestationError("key_permissions")
        raw = os.read(descriptor, 4097)
    finally:
        os.close(descriptor)
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import (
            Ed25519PrivateKey,
        )

        key = serialization.load_pem_private_key(raw, password=None)
    except (ImportError, ValueError, TypeError):
        raise AttestationError("key_invalid") from None
    if not isinstance(key, Ed25519PrivateKey):
        raise AttestationError("key_invalid")
    return key


def request_body(key_id, key, signed, verified_items, evidence_sha256):
    _check(verified_items, evidence_sha256)
    return json.dumps(
        {
            "schema_version": "2.0",
            "key_id": key_id,
            "algorithm": "ed25519",
            "signature": base64.b64encode(key.sign(signed)).decode("ascii"),
            "verified_items": verified_items,
            "evidence_sha256": evidence_sha256,
        },
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()


def outcome(result):
    """attested (201 new, 200 resent), rejected (operator), or retry."""
    if isinstance(result, TransportFailure):
        # Credentials and certificates need an operator, not the timer.
        stop = (FailureKind.AUTH, FailureKind.TLS)
        return "rejected" if result.kind in stop else "retry"
    if result.status in (200, 201):
        return "attested"
    if result.status == 429 or result.status >= 500:
        return "retry"
    return "rejected"
