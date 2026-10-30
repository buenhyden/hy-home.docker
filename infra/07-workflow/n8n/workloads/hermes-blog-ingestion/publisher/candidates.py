"""Lossless export snapshots using the digest-bound SPEC0247 validator."""

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

from .files import BATCH_LIMIT, InputError, safe_read

JOBS = ("6eabd835f969", "25674fbc0bf3", "8d0925bc571d")
EXPORT_NAME = re.compile(r"[0-9a-f]{32}\.json\Z")
REVIEWED_SHA256 = "8c988c715286edd53d2f7e5931cb349e6a5bed49be8ec2f8e7be98f2810c7297"


@dataclass(frozen=True)
class Snapshot:
    job_id: str
    run_id: str
    candidate: bytes
    source_ref: str
    source: bytes
    ideas: tuple[tuple[str, bytes], ...] = ()


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def load_validator(path, expected_sha256):
    """Execute only the exact reviewed dependency, never its CLI or shell."""
    if expected_sha256 != REVIEWED_SHA256:
        raise InputError("validator_digest")
    path = Path(path)
    try:
        raw = safe_read(path.parent, path.name)
        if sha256(raw) != expected_sha256:
            raise InputError("validator_digest")
        module = ModuleType("hermes_reviewed_candidate_validator")
        exec(compile(raw, "<reviewed-hermes-validator>", "exec"), module.__dict__)
        return module.validate
    except (OSError, SyntaxError, AttributeError):
        raise InputError("validator_unavailable") from None


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError("invalid_json")
        result[key] = value
    return result


def _reject_constant(_value):
    raise InputError("invalid_json")


def load_candidate(
    exports, job_id, name, source_root, item_root, validator, *, batch_limit=BATCH_LIMIT
):
    """Validate structure before opening approved report/idea references."""
    if job_id not in JOBS:
        raise InputError("job_blocked")
    if not isinstance(name, str) or not EXPORT_NAME.fullmatch(name):
        raise InputError("export_name")
    raw = safe_read(exports, f"{job_id}/{name}")
    try:
        data = json.loads(
            raw, object_pairs_hook=_unique_object, parse_constant=_reject_constant
        )
        if validator(data):
            raise InputError("job_blocked")
    except (ValueError, TypeError, KeyError, RecursionError, UnicodeError):
        raise InputError("candidate_invalid") from None
    if data["job_id"] != job_id or data["run_id"] != name[:-5]:
        raise InputError("identity_mismatch")
    remaining = batch_limit - len(raw)

    def read_checked(root, ref, claimed):
        nonlocal remaining
        if remaining <= 0:
            raise InputError("batch_limit")
        value = safe_read(root, ref)
        remaining -= len(value)
        if remaining < 0:
            raise InputError("batch_limit")
        if sha256(value) != claimed:
            raise InputError("source_digest")
        return value

    source = read_checked(source_root, data["source_ref"], data["source_sha256"])
    ideas = tuple(
        (
            item["source_ref"],
            read_checked(item_root, item["source_ref"], item["source_sha256"]),
        )
        for item in data["items"]
        if data["report_kind"] == "solo-dev-ideas"
    )
    return Snapshot(job_id, data["run_id"], raw, data["source_ref"], source, ideas)
