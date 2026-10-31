"""Synthetic Ed25519 producer keys and signatures for tests only."""

import base64
import json

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

DOMAIN = b"hermes-companion-evidence/1\x00"
JOBS = ["6eabd835f969", "25674fbc0bf3", "8d0925bc571d"]


def new_key():
    return Ed25519PrivateKey.generate()


def entry(private, key_id="synthetic-producer", **overrides):
    public = private.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )
    value = dict(
        key_id=key_id,
        algorithm="ed25519",
        public_key=base64.b64encode(public).decode(),
        jobs=JOBS,
        not_before="2026-01-01T00:00:00Z",
        not_after="2099-01-01T00:00:00Z",
    )
    value.update(overrides)
    return value


def write_store(path, *entries):
    path.write_text(
        json.dumps({"schema_version": "hermes-producer-keys/1", "keys": list(entries)})
    )


def sign(private, evidence, key_id="synthetic-producer"):
    return json.dumps(
        dict(
            schema_version="hermes-companion-signature/1",
            key_id=key_id,
            algorithm="ed25519",
            signature=base64.b64encode(private.sign(DOMAIN + evidence)).decode(),
        )
    ).encode()
