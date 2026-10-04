#!/usr/bin/env python3
"""Import one finalized quality envelope through the perf_db SQL contract."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import os
import pathlib
import re
import stat
import subprocess
import uuid
from typing import Any

IMPORT_SCHEMA = "hyhome.quality-import/v1"
RECEIPT_SCHEMA = "hyhome.quality-import-receipt/v1"
MAX_JSON_BYTES = 1024 * 1024
SHA256 = re.compile(r"[0-9a-f]{64}")
SLUG = re.compile(r"[a-z0-9][a-z0-9-]{0,62}")


class ImportContractError(ValueError):
    """An import envelope or immutable receipt violated its contract."""


def _canonical(value: object) -> bytes:
    try:
        return (
            json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n"
        ).encode()
    except (TypeError, ValueError) as exc:
        raise ImportContractError("value is not canonical JSON") from exc


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, child in pairs:
        if key in value:
            raise ImportContractError(f"duplicate JSON key: {key}")
        value[key] = child
    return value


def _reject_nonfinite(value: object) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ImportContractError("non-finite JSON number")
    if isinstance(value, dict):
        for child in value.values():
            _reject_nonfinite(child)
    elif isinstance(value, list):
        for child in value:
            _reject_nonfinite(child)


def _load_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        info = path.lstat()
    except FileNotFoundError as exc:
        raise ImportContractError(f"missing import artifact: {path.name}") from exc
    if (
        not stat.S_ISREG(info.st_mode)
        or path.is_symlink()
        or info.st_size > MAX_JSON_BYTES
    ):
        raise ImportContractError("import artifact must be a bounded regular file")
    try:
        value = json.loads(path.read_bytes(), object_pairs_hook=_pairs)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ImportContractError("import artifact is invalid JSON") from exc
    if not isinstance(value, dict):
        raise ImportContractError("import artifact must be an object")
    _reject_nonfinite(value)
    return value


def _exact(value: dict[str, Any], keys: set[str], name: str) -> None:
    if set(value) != keys:
        raise ImportContractError(f"{name} keys are invalid")


def _utc_timestamp(value: object) -> dt.datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ImportContractError("import timestamp must be RFC3339 UTC")
    try:
        parsed = dt.datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ImportContractError("import timestamp must be RFC3339 UTC") from exc
    if parsed.tzinfo != dt.UTC:
        raise ImportContractError("import timestamp must be RFC3339 UTC")
    return parsed


def _validate(
    envelope: dict[str, Any],
    object_contract: dict[str, Any] | None = None,
    approved_endpoints: tuple[str, ...] = (),
) -> None:
    _exact(
        envelope,
        {
            "schema_version",
            "identity",
            "manifest_sha256",
            "final_sha256",
            "payload_sha256",
            "execution_state",
            "reported_verdict",
            "evidence_state",
            "ingestion_state",
            "started_at",
            "ended_at",
            "samples",
            "metrics",
            "artifacts",
        },
        "import envelope",
    )
    identity = envelope["identity"]
    if not isinstance(identity, dict):
        raise ImportContractError("import identity must be an object")
    _exact(identity, {"run_id", "attempt", "project_id"}, "import identity")
    try:
        run_id = str(uuid.UUID(str(identity["run_id"])))
    except (ValueError, AttributeError) as exc:
        raise ImportContractError("import run_id must be a UUID") from exc
    if identity["run_id"] != run_id:
        raise ImportContractError("import run_id must be canonical")
    if (
        isinstance(identity["attempt"], bool)
        or not isinstance(identity["attempt"], int)
        or not 1 <= identity["attempt"] <= 999
        or not isinstance(identity["project_id"], str)
        or not SLUG.fullmatch(identity["project_id"])
    ):
        raise ImportContractError("import identity values are invalid")
    for name in ("manifest_sha256", "final_sha256", "payload_sha256"):
        if not isinstance(envelope[name], str) or not SHA256.fullmatch(envelope[name]):
            raise ImportContractError(f"import {name} is invalid")
    if (
        envelope["schema_version"] != IMPORT_SCHEMA
        or envelope["execution_state"] not in {"completed", "interrupted"}
        or envelope["reported_verdict"]
        not in {"passed", "failed_threshold", "failed_execution", "incomplete"}
        or envelope["evidence_state"] not in {"complete", "incomplete"}
        or envelope["ingestion_state"] != "pending"
    ):
        raise ImportContractError("import states are invalid")
    if envelope["execution_state"] == "interrupted" and (
        envelope["evidence_state"] != "incomplete"
        or envelope["reported_verdict"] != "incomplete"
    ):
        raise ImportContractError("interrupted import state is inconsistent")
    if (
        envelope["reported_verdict"] in {"passed", "failed_threshold"}
        and envelope["evidence_state"] != "complete"
    ) or (
        envelope["reported_verdict"] == "incomplete"
        and envelope["evidence_state"] != "incomplete"
    ):
        raise ImportContractError("import verdict and evidence are inconsistent")
    started_at = envelope["started_at"]
    ended_at = envelope["ended_at"]
    if started_at is None or ended_at is None:
        if envelope["execution_state"] != "interrupted" or not (
            started_at is None and ended_at is None
        ):
            raise ImportContractError("import timestamps are incomplete")
    elif _utc_timestamp(ended_at) < _utc_timestamp(started_at):
        raise ImportContractError("import end time precedes start time")
    if (
        isinstance(envelope["samples"], bool)
        or not isinstance(envelope["samples"], int)
        or envelope["samples"] < 0
        or not isinstance(envelope["metrics"], list)
        or not isinstance(envelope["artifacts"], list)
    ):
        raise ImportContractError("import result values are invalid")
    for metric in envelope["metrics"]:
        if not isinstance(metric, dict):
            raise ImportContractError("import metric must be an object")
        _exact(
            metric,
            {"name", "type", "contains", "values", "thresholds"},
            "import metric",
        )
        if (
            not isinstance(metric["name"], str)
            or not isinstance(metric["values"], dict)
            or not isinstance(metric["thresholds"], dict)
        ):
            raise ImportContractError("import metric values are invalid")
    for artifact in envelope["artifacts"]:
        if not isinstance(artifact, dict):
            raise ImportContractError("import artifact must be an object")
        _exact(
            artifact,
            {"name", "sha256", "bytes", "object_ref"},
            "import artifact",
        )
        if (
            not isinstance(artifact["name"], str)
            or not isinstance(artifact["sha256"], str)
            or not SHA256.fullmatch(artifact["sha256"])
            or isinstance(artifact["bytes"], bool)
            or not isinstance(artifact["bytes"], int)
            or artifact["bytes"] < 0
        ):
            raise ImportContractError("import artifact values are invalid")
        if artifact["object_ref"] is not None:
            from object_store import validate_object_binding

            try:
                validate_object_binding(
                    artifact["object_ref"],
                    identity,
                    artifact,
                    object_contract,
                    approved_endpoints,
                )
            except ValueError as exc:
                raise ImportContractError("import object reference is invalid") from exc
    unhashed = dict(envelope)
    del unhashed["payload_sha256"]
    if hashlib.sha256(_canonical(unhashed)).hexdigest() != envelope["payload_sha256"]:
        raise ImportContractError("import payload_sha256 mismatch")


def _write_once(path: pathlib.Path, value: object) -> None:
    payload = _canonical(value)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC
    try:
        descriptor = os.open(path, flags, 0o640)
    except FileExistsError:
        if path.is_symlink() or not path.is_file() or path.read_bytes() != payload:
            raise ImportContractError("immutable import receipt conflict") from None
        return
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())


def import_db(
    envelope_path: pathlib.Path,
    receipt_path: pathlib.Path,
    psql_binary: str = "psql",
    object_contract_path: pathlib.Path | None = None,
    approved_endpoints: tuple[str, ...] = (),
) -> tuple[dict[str, Any], int]:
    envelope = _load_json(envelope_path)
    object_contract = (
        _load_json(object_contract_path) if object_contract_path is not None else None
    )
    _validate(envelope, object_contract, approved_endpoints)
    encoded = _canonical(envelope).hex()
    unsigned = dict(envelope)
    del unsigned["payload_sha256"]
    unsigned_encoded = _canonical(unsigned).hex()
    statement = (
        "SELECT quality.import_payload("
        f"convert_from(decode('{encoded}','hex'),'UTF8')::jsonb,"
        f"decode('{unsigned_encoded}','hex'));\n"
    )
    try:
        allowed_environment = {
            "PATH",
            "LANG",
            "LC_ALL",
            "TZ",
            "PGHOST",
            "PGPORT",
            "PGDATABASE",
            "PGUSER",
            "PGPASSFILE",
            "PGSSLMODE",
            "PGSSLROOTCERT",
        }
        completed = subprocess.run(
            [
                psql_binary,
                "--no-psqlrc",
                "--set=ON_ERROR_STOP=1",
                "--tuples-only",
                "--no-align",
                "--quiet",
            ],
            input=statement,
            text=True,
            capture_output=True,
            check=False,
            env={
                **{
                    key: value
                    for key, value in os.environ.items()
                    if key in allowed_environment
                },
                "PGCONNECT_TIMEOUT": "10",
            },
            timeout=30,
        )
        database_result = completed.stdout.strip()
        imported = completed.returncode == 0 and database_result in {
            "inserted",
            "exact_replay",
        }
        exit_code = (
            completed.returncode if completed.returncode else (0 if imported else 2)
        )
        error_class = None if imported else "database_import_failed"
    except subprocess.TimeoutExpired:
        database_result, imported, exit_code = None, False, 124
        error_class = "database_import_timeout"
    except OSError:
        database_result, imported, exit_code = None, False, 127
        error_class = "database_client_unavailable"
    receipt = {
        "schema_version": RECEIPT_SCHEMA,
        "payload_sha256": envelope["payload_sha256"],
        "ingestion_state": "imported" if imported else "failed",
        "database_result": database_result if imported else None,
        "attempted_at": dt.datetime.now(dt.UTC)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "error_class": error_class,
    }
    _write_once(receipt_path, receipt)
    return receipt, exit_code
