"""Airflow-only protected capture and bounded initial-upload context."""

from __future__ import annotations

import json
import os
import re
import time
from types import SimpleNamespace

from tests.validation._opsflow_airflow_native_guards import (
    RehearsalFailure,
    _bound_evidence_file,
    _directory_identity,
    failure_evidence,
    retained_failure_evidence,
    retained_metadata,
    safe_exception,
)
from tests.validation._opsflow_evidence_redaction import redact_text

REGISTRY_KEYS = frozenset("metadata valkey s3_key s3_secret fernet jwt ingest".split())

CELERY_IDLE = """import contextlib,json,sys
with contextlib.redirect_stdout(sys.stderr):
 from airflow.providers.celery.executors.celery_executor_utils import app
 ins=app.control.inspect(timeout=5)
 a=ins.active();r=ins.reserved()
print(json.dumps({'active':a,'reserved':r}))
"""


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise RehearsalFailure("duplicate JSON field rejected")
        value[key] = item
    return value


def _generated_secrets(owned):
    descriptor = os.open(
        owned.directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    )
    try:
        parent = _directory_identity(descriptor)
        named = owned.directory.stat(follow_symlinks=False)
        if (
            parent[:2] != list(owned.dir_identity)
            or [named.st_dev, named.st_ino] != parent[:2]
        ):
            raise RehearsalFailure("generated registry parent changed")
        path = owned.directory / "synthetic-secrets.json"
        expected = owned.files.get(path)
        body = _bound_evidence_file(descriptor, path.name, expected, metadata=True)
        value = json.loads(body, object_pairs_hook=_unique_object)
        if (
            not isinstance(value, dict)
            or set(value) != REGISTRY_KEYS
            or any(
                not isinstance(item, str) or not 4 <= len(item) <= 512
                for item in value.values()
            )
        ):
            raise RehearsalFailure("generated registry shape rejected")
        return tuple(value.values())
    finally:
        os.close(descriptor)


def capture_failure(owned, role, args, result, *, s3_log_capture=None):
    if "command_failure" in owned.receipt:
        return
    blank = SimpleNamespace(returncode=result.returncode, stdout="", stderr="")
    fact, _ = failure_evidence(role, args, blank)
    record = owned.receipt["command_failure"] = {**fact, "capture_complete": False}
    try:
        secrets = _generated_secrets(owned)
        redacted = SimpleNamespace(
            returncode=result.returncode,
            stdout=redact_text(result.stdout, secrets),
            stderr=redact_text(result.stderr, secrets),
        )
        fact, streams = failure_evidence(role, args, redacted)
        for name in ("stdout", "stderr"):
            fact[name] = {
                **fact[name],
                "raw_source_bytes": len(getattr(result, name).encode("utf-8")),
            }
        fact = {**fact, "redaction": "before-retention"}
        if s3_log_capture is not None:
            if s3_log_capture not in {"COMPLETE", "PARTIAL"}:
                raise RehearsalFailure("S3 capture state rejected")
            fact = {**fact, "s3_log_capture": s3_log_capture}
        record = owned.receipt["command_failure"] = {**fact, "capture_complete": False}
        for name, body in streams.items():
            owned.private("failure-" + name + ".txt", body)
        metadata = retained_metadata(
            owned.directory, owned.dir_identity, owned.files, fact
        )
        path = owned.private(
            "failure-metadata.json", json.dumps(metadata, sort_keys=True)
        )
        identity = record["metadata_identity"] = owned.files[path]
        retained_failure_evidence(owned.directory, identity)
        record["capture_complete"] = True
    except BaseException as error:
        record.update(
            capture_exception=safe_exception(error),
            directory_identity=owned.dir_identity,
            partial_file_identities={
                p.name: identity for p, identity in owned.files.items()
            },
        )
        raise


def capture_s3_upload_failure(owned, role, args, result):
    if "command_failure" in owned.receipt:
        return
    if role != "worker" or len(args) != 3 or tuple(args[:2]) != ("python", "-c"):
        raise RehearsalFailure("initial upload context scope rejected")
    previous, cancellation = owned.client.deadline, None
    owned.client.deadline = min(previous, time.monotonic() + 5)
    context, state = "S3 context unavailable", "PARTIAL"
    try:
        owned.remaining()
        record = owned.containers["s3"]
        if not re.fullmatch(r"[0-9a-f]{64}", record.cid):
            raise RehearsalFailure("S3 context exact identity rejected")
        owned.verify(record, full=False)
        owned.remaining()
        logs = owned.client.run_result("logs", "--tail", "100", record.cid)
        if type(logs.returncode) is int and logs.returncode == 0:
            context = logs.stdout + logs.stderr
            state = "COMPLETE"
        else:
            context = "S3 log command nonzero; client failure preserved"
    except BaseException as error:
        context = "S3 context partial: " + safe_exception(error)
        if not isinstance(error, Exception):
            cancellation = error
    finally:
        owned.client.deadline = previous
    combined = SimpleNamespace(
        returncode=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr + "\n=== exact-owned S3 bounded context ===\n" + context,
    )
    try:
        capture_failure(owned, role, args, combined, s3_log_capture=state)
    finally:
        if cancellation is not None:
            raise cancellation


def inspect_celery_idle(owned):
    args = ("python", "-c", CELERY_IDLE)
    result = owned.exec_result("worker", *args)
    try:
        if result.returncode:
            raise RehearsalFailure("Celery idle command failed")
        state = json.loads(result.stdout, object_pairs_hook=_unique_object)
        expected = "celery@" + owned.containers["worker"].name
        if not isinstance(state, dict) or set(state) != {"active", "reserved"}:
            raise RehearsalFailure("Celery idle state shape rejected")
        if any(
            not isinstance(state[key], dict)
            or set(state[key]) != {expected}
            or state[key][expected] != []
            for key in ("active", "reserved")
        ):
            raise RehearsalFailure("Celery writer not idle")
        return state
    except Exception:
        try:
            capture_failure(owned, "worker", args, result)
        except Exception:
            # capture_failure records its finite partial state; original failure wins.
            pass
        raise
