"""Producer authentication shared by every dispatch gate.

Companion Evidence v1 bytes are trusted only with a detached Ed25519 signature
by a key in the tracked producer key store that is active, unrevoked and scoped
to the job. Only then is the structural check in evidence.py consulted. The
signing key belongs to a restricted producer account, so the same-account LLM
tools and exporter cannot forge evidence. The tracked store ships empty, which
keeps all Hermes jobs blocked until a real key is admitted by review.
"""

import base64
import binascii
import hashlib
import json
import os
import re
import stat
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from . import evidence as companion
from . import policy
from .files import InputError, safe_read

TRUST_STORE = Path(__file__).resolve().parent / "producer-keys.json"
STORE_SCHEMA = "hermes-producer-keys/1"
SIGNATURE_SCHEMA = "hermes-companion-signature/1"
DOMAIN = b"hermes-companion-evidence/1\x00"
_KEY_ID = re.compile(r"[a-z0-9][a-z0-9._-]{0,63}\Z")
_FIELDS = {"key_id", "algorithm", "public_key", "jobs", "not_before", "not_after"}


class TrustError(ValueError):
    """Value-free rejection code."""


@dataclass(frozen=True)
class Authorization:
    times: companion.RunTimes
    evidence_sha256: str
    key_id: str


def _require(condition, code):
    if not condition:
        raise TrustError(code)


def _object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, "duplicate_key")
        result[key] = value
    return result


def _json(raw):
    try:
        return json.loads(raw, object_pairs_hook=_object)
    except TrustError:
        raise
    except (ValueError, UnicodeError, RecursionError):
        raise TrustError("invalid_json") from None


def _b64(value, size):
    try:
        raw = base64.b64decode(value, validate=True)
    except (binascii.Error, TypeError, ValueError):
        raise TrustError("invalid_base64") from None
    _require(len(raw) == size, "invalid_base64")
    return raw


def _epoch(value):
    _require(isinstance(value, str), "store_invalid")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise TrustError("store_invalid") from None
    _require(parsed.tzinfo is not None, "store_invalid")
    return parsed.timestamp()


def _protected(path):
    """Fail unless no non-root account can alter path or any ancestor.

    Each component must be a root-owned non-symlink without group or other
    write permission that the (non-root) running account cannot write, so
    neither the Publisher account nor the Hermes producer account can
    substitute it.
    """
    uid = os.getuid()
    for item in (path, *path.parents):
        info = os.lstat(item)
        _require(
            uid != 0
            and not stat.S_ISLNK(info.st_mode)
            and info.st_uid == 0
            and not stat.S_IMODE(info.st_mode) & 0o022
            and not os.access(item, os.W_OK, follow_symlinks=False),
            "store_unprotected",
        )


def _runtime_paths():
    """Interpreter, import path, every loaded module file and the key store."""
    paths = {TRUST_STORE, Path(sys.executable).resolve(), Path(sys.prefix)}
    paths.update(Path(__file__).resolve().parent.glob("*.py"))
    paths.update(Path(entry).resolve() for entry in sys.path if entry)
    for module in list(sys.modules.values()):
        name = getattr(module, "__file__", None)
        if isinstance(name, str):
            paths.add(Path(name).resolve())
    return sorted(
        path for path in paths if os.path.lexists(path) or path == TRUST_STORE
    )


def _runtime_protected():
    """The interpreter, verifier code, crypto library and key store are fixed.

    Requires `python3 -I` (no user site, PYTHONPATH or cwd imports). The
    signature modules are imported first, so every file that has run or will
    verify a signature, each import path directory, the interpreter and the
    key store pass _protected.
    """
    _require(sys.flags.isolated, "interpreter_unisolated")
    try:
        import cryptography.exceptions  # noqa: F401
        from cryptography.hazmat.primitives.asymmetric import ed25519  # noqa: F401
    except ImportError:
        raise TrustError("crypto_unavailable") from None
    for path in _runtime_paths():
        try:
            _protected(path)
        except OSError:
            raise TrustError("store_unavailable") from None


def _public_key(key_id, job_id, now):
    _runtime_protected()
    try:
        raw = safe_read(TRUST_STORE.parent, TRUST_STORE.name, limit=65536)
    except InputError:
        raise TrustError("store_unavailable") from None
    store = _json(raw)
    _require(
        isinstance(store, dict)
        and set(store) == {"schema_version", "keys"}
        and store["schema_version"] == STORE_SCHEMA
        and isinstance(store["keys"], list),
        "store_invalid",
    )
    matches, publics, ids = [], set(), set()
    for entry in store["keys"]:
        # Validate every entry, not only the selected one.
        _require(
            isinstance(entry, dict)
            and set(entry) in (_FIELDS, _FIELDS | {"revoked_at"})
            and isinstance(entry["key_id"], str)
            and _KEY_ID.fullmatch(entry["key_id"]) is not None
            and entry["algorithm"] == "ed25519"
            and isinstance(entry["jobs"], list)
            and all(isinstance(job, str) for job in entry["jobs"])
            and _epoch(entry["not_before"]) < _epoch(entry["not_after"])
            and ("revoked_at" not in entry or _epoch(entry["revoked_at"]) > 0),
            "store_invalid",
        )
        public = _b64(entry["public_key"], 32)
        # One key, one entry: revoking a key_id must revoke the key itself.
        _require(public not in publics and entry["key_id"] not in ids, "store_invalid")
        publics.add(public)
        ids.add(entry["key_id"])
        if entry["key_id"] == key_id:
            matches.append((entry, public))
    _require(len(matches) == 1, "untrusted_key")
    entry, public = matches[0]
    _require(job_id in entry["jobs"], "key_scope")
    # Revocation (any revoked_at) is retroactive; expiry is checked at use, so
    # undelivered records must drain before not_after.
    _require("revoked_at" not in entry, "key_revoked")
    _require(
        _epoch(entry["not_before"]) <= now < _epoch(entry["not_after"]), "key_expired"
    )
    return public


def verify_signature(job_id, evidence, signature, *, now=None):
    """Return the signing key id, or raise TrustError."""
    _require(
        isinstance(signature, bytes) and 0 < len(signature) <= 4096,
        "signature_missing",
    )
    envelope = _json(signature)
    _require(
        isinstance(envelope, dict)
        and set(envelope) == {"schema_version", "key_id", "algorithm", "signature"}
        and envelope["schema_version"] == SIGNATURE_SCHEMA
        and envelope["algorithm"] == "ed25519"
        and isinstance(envelope["key_id"], str),
        "signature_invalid",
    )
    public = _public_key(
        envelope["key_id"], job_id, time.time() if now is None else now
    )
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import (
            Ed25519PublicKey,
        )
    except ImportError:
        raise TrustError("crypto_unavailable") from None
    try:
        Ed25519PublicKey.from_public_bytes(public).verify(
            _b64(envelope["signature"], 64), DOMAIN + evidence
        )
    except (InvalidSignature, ValueError):
        raise TrustError("signature_invalid") from None
    return envelope["key_id"]


def authorize(box, key, *, now=None):
    """The single trust decision every dispatch gate consumes.

    Returns None only for a job that requires no evidence and has none bound.
    Otherwise returns an Authorization or raises TrustError or OutboxError.
    """
    evidence = box.get_unverified_evidence(key)
    if evidence is None:
        _require(not policy.evidence_required(key[0]), "evidence_missing")
        return None
    key_id = verify_signature(
        key[0], evidence, box.get_evidence_signature(key), now=now
    )
    try:
        times = companion.verify(*key, box.get(key)["candidate"], evidence)
    except companion.EvidenceError as error:
        raise TrustError(str(error)) from None
    return Authorization(times, hashlib.sha256(evidence).hexdigest(), key_id)
