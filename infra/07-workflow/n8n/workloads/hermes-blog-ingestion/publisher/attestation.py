"""Blog-data attestation for a report this Publisher already delivered.

Runs as its own account. It never trusts Publisher state: the request bytes are
rebuilt from producer-signed evidence exactly as dispatch builds them, and the
Gateway verifies the signature against the report it stored, so anything n8n or
an account in between changed fails there with 422. The signature is a separate
contract from the Hermes companion signature and uses a separate key.
"""

import base64
import hashlib
import json
import os
import stat
from pathlib import Path

from . import evidence as companion
from . import trust
from .delivery import FailureKind, TransportFailure
from .files import InputError, open_directory
from .gateway_adapter import GatewayAdapter

PREFIX = b"blog-data-attestation/1\x00"
DESTINATION = "blog-data-attestation"
_IDENTITY = ("producer", "job_id", "run_id", "fire_id", "source_sha256")


class AttestationError(ValueError):
    pass


def _canonical(value):
    # Blog-data contract.mjs canonical(): sorted keys, no spaces, raw UTF-8.
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()


def message(body):
    """Bytes the Gateway verifies: prefix + identity and receive fingerprint."""
    try:
        request = json.loads(body)
        if not isinstance(request, dict) or not all(
            isinstance(request.get(name), str)
            for name in ("producer", "job_id", "source_sha256")
        ):
            raise ValueError
        content = {k: v for k, v in request.items() if k != "idempotency_key"}
        identity = {name: request.get(name) for name in _IDENTITY}
        identity["content_sha256"] = hashlib.sha256(_canonical(content)).hexdigest()
        return PREFIX + _canonical(identity)
    except (ValueError, UnicodeError):
        raise AttestationError("request_invalid") from None


def verified_request(snapshot, evidence, signature, *, now=None):
    """Return (dispatch body, evidence SHA-256) only for producer-signed evidence.

    The checks trust.authorize applies before dispatch, on bytes read fresh
    from the producer rather than from the Publisher's outbox.
    """
    trust.verify_signature(snapshot.job_id, evidence, signature, now=now)
    try:
        times = companion.verify(
            snapshot.job_id, snapshot.run_id, snapshot.candidate, evidence
        )
    except companion.EvidenceError as error:
        raise trust.TrustError(str(error)) from None
    generated = json.loads(snapshot.candidate)["generated_at"]
    adapter = GatewayAdapter(times.scheduled_at, generated, times.collected_at)
    # The outbox row shape dispatch hands the adapter.
    row = dict(
        job_id=snapshot.job_id,
        run_id=snapshot.run_id,
        candidate=snapshot.candidate,
        candidate_sha256=hashlib.sha256(snapshot.candidate).hexdigest(),
        source_ref=snapshot.source_ref,
        source=snapshot.source,
        source_sha256=hashlib.sha256(snapshot.source).hexdigest(),
        ideas=snapshot.ideas,
    )
    return adapter.prepare(row).body, hashlib.sha256(evidence).hexdigest()


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


def request_body(key_id, key, signed):
    return json.dumps(
        {
            "schema_version": "1.0",
            "key_id": key_id,
            "algorithm": "ed25519",
            "signature": base64.b64encode(key.sign(signed)).decode("ascii"),
        },
        separators=(",", ":"),
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
