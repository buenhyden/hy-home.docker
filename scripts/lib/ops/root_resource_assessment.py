"""Bounded public root-resource assessment for SPEC-0218 W10.

The helper accepts one explicitly selected JSON fact set. It never contacts
Docker, the network, environment files, logs, secrets, or the host runtime.
Its result is an assessment and cannot authorize a configuration mutation.
"""

from __future__ import annotations

import datetime as dt
import errno
import hashlib
import json
import math
import os
import re
import stat
from pathlib import Path
from typing import NoReturn

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry
from referencing.exceptions import NoSuchResource

from scripts.validation import compose_controls

ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = (
    ROOT / "infra/09-platform-ops/resource-optimization/measurement.schema.json"
)
MAX_INPUT_BYTES = 256 * 1024
MAX_DEPTH = 32
MAX_NODES = 8192
MAX_NUMBER = 10**15
PRIVATE_NAME_PARTS = (".env", "secret", "raw", "log")
PRIVATE_DIRECTORIES = frozenset(
    {
        ".aws",
        ".ssh",
        ".kube",
        ".docker",
        ".codex",
        "secrets",
        "secret",
        "logs",
        "log",
        "raw",
        "credentials",
        "auth",
    }
)
METRIC_UNITS = {
    "cpu_throttled_seconds": "seconds",
    "cpu_throttled_periods": "count",
    "rss_bytes": "bytes",
    "heap_bytes": "bytes",
    "work_mem_bytes": "bytes",
    "connections": "count",
    "tmpfs_bytes": "bytes",
    "shm_bytes": "bytes",
    "cache_bytes": "bytes",
    "off_heap_bytes": "bytes",
    "resource_overhead_bytes": "bytes",
    "worker_count": "count",
    "pid_peak": "count",
    "oom_events": "count",
    "exit_events": "count",
    "latency_p95_ms": "milliseconds",
    "throughput_per_second": "per_second",
    "recovery_seconds": "seconds",
    "gpu_memory_bytes": "bytes",
    "gpu_utilization_ratio": "ratio",
}
BUDGET_UNITS = {
    "cpu_limit_cores": "cores",
    "memory_limit_bytes": "bytes",
    "connection_limit": "count",
    "tmpfs_limit_bytes": "bytes",
    "shm_limit_bytes": "bytes",
    "worker_limit": "count",
    "pid_limit": "count",
    "latency_p95_budget_ms": "milliseconds",
    "throughput_floor_per_second": "per_second",
    "recovery_budget_seconds": "seconds",
    "gpu_memory_limit_bytes": "bytes",
}
COUNT_METRICS = {
    "cpu_throttled_periods",
    "connections",
    "worker_count",
    "pid_peak",
    "oom_events",
    "exit_events",
}
COUNT_BUDGETS = {"connection_limit", "worker_limit", "pid_limit"}


class PublicInputError(ValueError):
    """A value-free public input failure safe to print."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(f"ERROR {code}")


def _reject_duplicate(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise PublicInputError("DUPLICATE_FIELD")
        result[key] = value
    return result


def _reject_nonfinite(_: str) -> NoReturn:
    raise PublicInputError("NONFINITE_NUMBER")


def _safe_name(path: Path) -> None:
    name = path.name.lower()
    if path.suffix.lower() != ".json":
        raise PublicInputError("UNSAFE_INPUT_PATH")
    if name.startswith(".") or any(part in name for part in PRIVATE_NAME_PARTS):
        raise PublicInputError("PRIVATE_INPUT_PATH")
    if ".." in path.parts:
        raise PublicInputError("UNSAFE_INPUT_PATH")
    if any(
        part.lower() in PRIVATE_DIRECTORIES or part.lower().startswith(".env")
        for part in path.parts[:-1]
    ):
        raise PublicInputError("PRIVATE_INPUT_PATH")


def _identity(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
        info.st_nlink,
    )


def _open_parent(candidate: Path) -> int:
    """Anchor every component without traversing symlink directories."""
    absolute = Path(os.path.abspath(candidate))
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    descriptor = os.open(absolute.anchor, flags)
    try:
        for part in absolute.parts[1:-1]:
            next_descriptor = os.open(part, flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = next_descriptor
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def _bounded_value(document: object) -> None:
    pending = [(document, 0)]
    nodes = 0
    while pending:
        value, depth = pending.pop()
        nodes += 1
        if depth > MAX_DEPTH or nodes > MAX_NODES:
            raise PublicInputError("INPUT_TOO_COMPLEX")
        if type(value) is dict:
            if len(value) > MAX_NODES:
                raise PublicInputError("INPUT_TOO_COMPLEX")
            for key, item in value.items():
                if type(key) is not str or len(key) > 1024:
                    raise PublicInputError("INVALID_DOCUMENT")
                pending.append((item, depth + 1))
        elif type(value) is list:
            if len(value) > MAX_NODES:
                raise PublicInputError("INPUT_TOO_COMPLEX")
            pending.extend((item, depth + 1) for item in value)
        elif type(value) is str:
            if len(value) > 1024:
                raise PublicInputError("INPUT_TOO_COMPLEX")
        elif type(value) is float:
            if not math.isfinite(value):
                raise PublicInputError("NONFINITE_NUMBER")
            if abs(value) > MAX_NUMBER:
                raise PublicInputError("INVALID_DOCUMENT")
        elif type(value) is int:
            if abs(value) > MAX_NUMBER:
                raise PublicInputError("INVALID_DOCUMENT")
        elif value is not None and type(value) is not bool:
            raise PublicInputError("INVALID_DOCUMENT")


def _check_json_depth(text: str) -> None:
    depth = 0
    in_string = escaped = False
    for character in text:
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            in_string = True
        elif character in "[{":
            depth += 1
            if depth > MAX_DEPTH:
                raise PublicInputError("INPUT_TOO_COMPLEX")
        elif character in "]}":
            depth -= 1


def _parse_document(body: bytes) -> dict[str, object]:
    try:
        text = body.decode("utf-8")
        _check_json_depth(text)
        value = json.loads(
            text, object_pairs_hook=_reject_duplicate, parse_constant=_reject_nonfinite
        )
    except PublicInputError:
        raise
    except (UnicodeError, ValueError, RecursionError, OverflowError):
        raise PublicInputError("INVALID_JSON") from None
    _bounded_value(value)
    if type(value) is not dict:
        raise PublicInputError("INVALID_DOCUMENT")
    return value


def _read_body(candidate: Path, parent: int) -> bytes:
    descriptor = None
    try:
        metadata = os.stat(candidate.name, dir_fd=parent, follow_symlinks=False)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise PublicInputError("UNSAFE_INPUT_PATH")
        if metadata.st_size > MAX_INPUT_BYTES:
            raise PublicInputError("INPUT_TOO_LARGE")
        flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_NONBLOCK
        descriptor = os.open(candidate.name, flags, dir_fd=parent)
        current = os.fstat(descriptor)
        if not stat.S_ISREG(current.st_mode) or current.st_nlink != 1:
            raise PublicInputError("UNSAFE_INPUT_PATH")
        if _identity(current) != _identity(metadata):
            raise PublicInputError("INPUT_CHANGED")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = None
            body = stream.read(MAX_INPUT_BYTES + 1)
            if _identity(os.fstat(stream.fileno())) != _identity(current):
                raise PublicInputError("INPUT_CHANGED")
            after = os.stat(candidate.name, dir_fd=parent, follow_symlinks=False)
            if _identity(after) != _identity(current):
                raise PublicInputError("INPUT_CHANGED")
        if len(body) > MAX_INPUT_BYTES:
            raise PublicInputError("INPUT_TOO_LARGE")
        return body
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _read_document(
    path: str | os.PathLike[str],
) -> tuple[dict[str, object], str]:
    parent = None
    try:
        candidate = Path(path)
        _safe_name(candidate)
        _safe_name(Path(os.path.abspath(candidate)))
        parent = _open_parent(candidate)
        body = _read_body(candidate, parent)
    except PublicInputError:
        raise
    except OSError as error:
        code = (
            "UNSAFE_INPUT_PATH"
            if error.errno in {errno.ELOOP, errno.ENOTDIR}
            else "INPUT_UNAVAILABLE"
        )
        raise PublicInputError(code) from None
    except (ValueError, TypeError):
        raise PublicInputError("UNSAFE_INPUT_PATH") from None
    finally:
        if parent is not None:
            os.close(parent)
    return _parse_document(body), hashlib.sha256(body).hexdigest()


def load_document(path: str | os.PathLike[str]) -> dict[str, object]:
    """Load bounded public JSON without following any path symlink."""
    return _read_document(path)[0]


def _schema() -> dict[str, object]:
    try:
        value = _read_document(SCHEMA_PATH)[0]
        _require_local_references(value)
        Draft202012Validator.check_schema(value)
    except Exception:
        raise PublicInputError("INVALID_SCHEMA") from None
    return value


def _require_local_references(schema: dict[str, object]) -> None:
    pending = [schema]
    while pending:
        item = pending.pop()
        if isinstance(item, dict):
            for name, value in item.items():
                if name in {"$ref", "$dynamicRef"} and (
                    not isinstance(value, str) or not value.startswith("#/")
                ):
                    raise PublicInputError("INVALID_SCHEMA")
                pending.append(value)
        elif isinstance(item, list):
            pending.extend(item)


def _deny_external(uri: str):
    raise NoSuchResource(ref=uri)


def _validate(document: dict[str, object]) -> None:
    _bounded_value(document)
    if type(document) is not dict:
        raise PublicInputError("INVALID_DOCUMENT")
    try:
        validator = Draft202012Validator(
            _schema(),
            format_checker=FormatChecker(),
            registry=Registry(retrieve=_deny_external),
        )
        if next(validator.iter_errors(document), None) is not None:
            raise PublicInputError("INVALID_DOCUMENT")
    except PublicInputError:
        raise
    except Exception:
        raise PublicInputError("INVALID_SCHEMA") from None
    groups = (
        (document["metrics"], COUNT_METRICS, METRIC_UNITS),
        (document["budgets"], COUNT_BUDGETS, BUDGET_UNITS),
    )
    for facts, count_names, units in groups:
        for name, fact in facts.items():
            if fact["unit"] != units[name]:
                raise PublicInputError("INVALID_DOCUMENT")
            if fact["status"] != "known":
                continue
            value = fact["value"]
            if isinstance(value, bool) or not math.isfinite(value):
                raise PublicInputError("INVALID_DOCUMENT")
            if name in count_names and not float(value).is_integer():
                raise PublicInputError("INVALID_DOCUMENT")
    gpu_ratio = document["metrics"]["gpu_utilization_ratio"]
    if gpu_ratio["status"] == "known" and gpu_ratio["value"] > 1:
        raise PublicInputError("INVALID_DOCUMENT")
    service = document["controls"]["effective_service"]
    limits = service.get("deploy", {}).get("resources", {}).get("limits", {})
    for owner, names in (
        (service, ("cpus", "mem_limit")),
        (limits, ("cpus", "memory")),
    ):
        for name in names:
            if name in owner:
                number = re.match(r"^[0-9]+(?:\.[0-9]+)?", str(owner[name]))
                if number is None or float(number.group()) <= 0:
                    raise PublicInputError("INVALID_DOCUMENT")


def _known(fact: dict[str, object]) -> float | None:
    return float(fact["value"]) if fact["status"] == "known" else None


def _has_unknowns(document: dict[str, object]) -> bool:
    provenance = document["provenance"]
    if (
        provenance["status"] != "known"
        or provenance["collector_id"] is None
        or provenance["receipt_sha256"] is None
        or provenance["method"] == "unknown"
        or provenance["aggregation"] == "unknown"
    ):
        return True
    return any(
        fact["status"] == "unknown"
        for group in (document["metrics"], document["budgets"])
        for fact in group.values()
    )


def _identity_mismatch(document: dict[str, object]) -> bool:
    if document["controls"]["compose_file"] != document["source"]["compose_file"]:
        return True
    deployed = document["deployed"]
    if deployed["status"] != "observed" or deployed["platform"] is None:
        return True
    source = document["source"]
    return any(
        deployed[key] != source[key]
        for key in (
            "repository_sha",
            "compose_file_sha256",
            "effective_config_sha256",
            "image_digest",
            "image_config_sha256",
        )
    )


def _contradictory(document: dict[str, object], today: dt.date) -> bool:
    window = document["window"]
    try:
        started = dt.datetime.fromisoformat(window["started_at"].replace("Z", "+00:00"))
        ended = dt.datetime.fromisoformat(window["ended_at"].replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return True
    elapsed = (ended - started).total_seconds()
    if ended.astimezone(dt.UTC).date() > today:
        return True
    if elapsed <= 0 or abs(elapsed - window["duration_seconds"]) > 1:
        return True
    if (window["sample_count"] - 1) * window["cadence_seconds"] > elapsed:
        return True

    metrics = document["metrics"]
    budgets = document["budgets"]
    comparisons = (
        ("rss_bytes", "memory_limit_bytes"),
        ("connections", "connection_limit"),
        ("tmpfs_bytes", "tmpfs_limit_bytes"),
        ("shm_bytes", "shm_limit_bytes"),
        ("worker_count", "worker_limit"),
        ("pid_peak", "pid_limit"),
        ("latency_p95_ms", "latency_p95_budget_ms"),
        ("recovery_seconds", "recovery_budget_seconds"),
        ("gpu_memory_bytes", "gpu_memory_limit_bytes"),
    )
    for metric_name, budget_name in comparisons:
        metric = _known(metrics[metric_name])
        budget = _known(budgets[budget_name])
        if metric is not None and budget is not None and metric > budget:
            return True
    throughput = _known(metrics["throughput_per_second"])
    floor = _known(budgets["throughput_floor_per_second"])
    return throughput is not None and floor is not None and throughput < floor


def _controls(
    document: dict[str, object], today: dt.date
) -> tuple[dict[str, object], list[str]]:
    selected = document["controls"]
    service_name = document["target"]["service"]
    service = selected["effective_service"]
    roots = tuple(selected["secret_roots"])
    deviations = compose_controls.deviations(service, roots)
    models = {
        "root": (
            {"services": {service_name: service}},
            {service_name: selected["compose_file"]},
            roots,
        )
    }
    findings = compose_controls.check(selected["registry"], models, today)
    return deviations, findings


def _required_not_applicable(document: dict[str, object]) -> bool:
    required = (
        (
            "metrics",
            (
                "rss_bytes",
                "pid_peak",
                "oom_events",
                "exit_events",
                "cpu_throttled_seconds",
                "cpu_throttled_periods",
            ),
        ),
        ("budgets", ("cpu_limit_cores", "memory_limit_bytes", "pid_limit")),
    )
    return any(
        document[group][name]["status"] == "not_applicable"
        for group, names in required
        for name in names
    )


def evaluate(
    document: dict[str, object], *, today: dt.date | None = None
) -> dict[str, object]:
    """Return stable blocker codes and sanitized control results."""
    _validate(document)
    observation_date = today or dt.date.today()
    if type(observation_date) is not dt.date:
        raise PublicInputError("INVALID_DOCUMENT")
    control_deviations, control_findings = _controls(document, observation_date)
    blockers: list[str] = []
    synthetic = (
        document["evidence_kind"] == "synthetic"
        or document["provenance"]["method"] == "synthetic"
    )
    if synthetic:
        blockers.append("SYNTHETIC_EVIDENCE")
    if _has_unknowns(document):
        blockers.append("UNKNOWN_FACTS")
    if _required_not_applicable(document):
        blockers.append("REQUIRED_FACTS_NOT_APPLICABLE")
    if dt.date.fromisoformat(document["controls"]["as_of"]) > observation_date:
        blockers.append("FUTURE_CONTROL_DATE")
    proposal = document["proposal"]
    if document["window"]["phase"] == "idle" and (
        proposal["lower_memory_limit"] or proposal["lower_cpu_limit"]
    ):
        blockers.append("IDLE_ONLY_LOWERING")
    if _identity_mismatch(document):
        blockers.append("SOURCE_DEPLOYED_MISMATCH")
    if _contradictory(document, observation_date):
        blockers.append("CONTRADICTORY_FACTS")
    if not document["workload"]["representative"]:
        blockers.append("UNREPRESENTATIVE_WORKLOAD")
    if control_findings:
        blockers.append("CONTROL_FINDINGS")
    return {
        "schema_version": 1,
        "status": "BLOCKED" if blockers else "REVIEWABLE",
        "blockers": blockers,
        "control_deviations": control_deviations,
        "control_findings": control_findings,
        "evidence_scope": "SOURCE/UNIT/STATIC",
        "synthetic": synthetic,
        "runtime_acceptance": False,
        "mutation_authorized": False,
    }


def evaluate_file(path: str | os.PathLike[str]) -> dict[str, object]:
    """Load and evaluate one public fact file, binding its exact bytes."""
    document, digest = _read_document(path)
    return {**evaluate(document), "input_sha256": digest}
