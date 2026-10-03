"""Inspect k6 summary and exit artifacts without exporting unsafe strings."""

from __future__ import annotations

import json
import math
import os
import pathlib
import re
import stat
from typing import Any

import quality_run as contract


def _contains_sensitive_summary(value: object) -> bool:
    prohibited_keys = {"url", "ip", "authorization", "cookie", "set-cookie"}
    prohibited_text = re.compile(
        r"https?://|authorization|cookie|bearer\s|x-api-key|[?&][^=]{1,64}=",
        re.IGNORECASE,
    )
    if isinstance(value, str):
        return bool(prohibited_text.search(value))
    if isinstance(value, dict):
        return any(
            str(key).lower() in prohibited_keys
            or prohibited_text.search(str(key))
            or _contains_sensitive_summary(child)
            for key, child in value.items()
        )
    if isinstance(value, list):
        return any(_contains_sensitive_summary(child) for child in value)
    return False


def inspect_summary(
    attempt_dir: pathlib.Path, manifest: dict[str, Any]
) -> tuple[dict[str, Any] | None, int, bool, list[str]]:
    issues: list[str] = []
    try:
        summary = contract._load_json(attempt_dir / "raw-summary.json")
    except contract.ContractError as exc:
        return None, 0, False, [str(exc)]
    if _contains_sensitive_summary(summary):
        return None, 0, False, ["summary contains prohibited tags or strings"]
    metrics = summary.get("metrics")
    if not isinstance(metrics, dict):
        return summary, 0, False, ["summary metrics are missing"]
    try:
        samples = metrics["iterations"]["values"]["count"]
    except (KeyError, TypeError):
        samples = 0
    if (
        isinstance(samples, bool)
        or not isinstance(samples, (int, float))
        or not contract.math.isfinite(samples)
        or samples <= 0
        or int(samples) != samples
    ):
        issues.append("summary has no valid samples")
        sample_count = 0
    else:
        sample_count = int(samples)
    thresholds_ok = True
    for metric_name, expressions in manifest["thresholds"].items():
        metric = metrics.get(metric_name)
        observed = metric.get("thresholds") if isinstance(metric, dict) else None
        for expression in expressions:
            result = observed.get(expression) if isinstance(observed, dict) else None
            if not isinstance(result, dict) or not isinstance(result.get("ok"), bool):
                issues.append(f"threshold result missing: {metric_name}")
                thresholds_ok = False
            elif not result["ok"]:
                thresholds_ok = False
    return summary, sample_count, thresholds_ok, issues


def inspect_raw_points(
    attempt_dir: pathlib.Path, manifest: dict[str, Any]
) -> tuple[int, list[str]]:
    """Validate bounded native NDJSON without rewriting timestamp precision."""
    allowed_tags = {
        "project_id",
        "environment",
        "run_id",
        "attempt",
        "testid",
        "method",
        "status",
        "error_code",
        "expected_response",
        "scenario",
    }
    metrics: set[str] = set()
    trends: set[str] = set()
    count = 0
    trend_points = 0
    try:
        descriptor = os.open(
            attempt_dir / "raw-points.json", os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC
        )
        with os.fdopen(descriptor, "rb") as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_size > 67108864:
                raise ValueError("raw point file size or type invalid")
            consumed = 0
            while line := stream.readline(65537):
                consumed += len(line)
                if consumed > 67108864:
                    raise ValueError("raw point stream exceeds byte quota")
                if len(line) > 65536 or not line.endswith(b"\n"):
                    raise ValueError("raw point line truncated or oversized")
                record = json.loads(
                    line,
                    object_pairs_hook=contract._pairs,
                    parse_constant=contract._reject_nonfinite,
                )
                if (
                    not isinstance(record, dict)
                    or set(record) != {"type", "metric", "data"}
                    or _contains_sensitive_summary(record)
                ):
                    raise ValueError("raw point record contains unsafe metadata")
                name, data = record["metric"], record["data"]
                if (
                    not isinstance(name, str)
                    or not name
                    or len(name) > 256
                    or not isinstance(data, dict)
                ):
                    raise ValueError("raw point metric descriptor invalid")
                if record["type"] == "Metric":
                    if (
                        data.get("name") != name
                        or data.get("type") not in {"counter", "gauge", "rate", "trend"}
                        or data.get("contains") not in {"default", "time", "data"}
                    ):
                        raise ValueError("raw metric type invalid")
                    metrics.add(name)
                    if data["type"] == "trend":
                        trends.add(name)
                elif record["type"] == "Point":
                    if name not in metrics or set(data) != {"time", "value", "tags"}:
                        raise ValueError(
                            "raw point missing descriptor or unexpected fields"
                        )
                    contract._parse_timestamp(data["time"])
                    value = data["value"]
                    if (
                        isinstance(value, bool)
                        or not isinstance(value, (int, float))
                        or not math.isfinite(value)
                    ):
                        raise ValueError("raw point value nonfinite")
                    tags = data["tags"]
                    if not isinstance(tags, dict) or set(tags) - allowed_tags:
                        raise ValueError("raw point tags unapproved")
                    for key, tag in tags.items():
                        if not isinstance(tag, str) or not re.fullmatch(
                            r"[A-Za-z0-9_.:-]{0,128}", tag
                        ):
                            raise ValueError("raw point tag unsafe")
                        if key in {
                            "project_id",
                            "environment",
                            "run_id",
                            "attempt",
                        } and tag != str(manifest[key]):
                            raise ValueError("raw point identity mismatch")
                    if (
                        any(
                            tags.get(key) != str(manifest[key])
                            for key in (
                                "project_id",
                                "environment",
                                "run_id",
                                "attempt",
                            )
                        )
                        or tags.get("testid") != manifest["run_id"]
                    ):
                        raise ValueError("raw point identity missing")
                    count += 1
                    trend_points += name in trends
                else:
                    raise ValueError("raw point record type invalid")
            after = os.fstat(stream.fileno())
            if (
                info.st_dev,
                info.st_ino,
                info.st_size,
                info.st_mtime_ns,
                info.st_ctime_ns,
            ) != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
                after.st_ctime_ns,
            ):
                raise ValueError("raw point stream changed during inspection")
        if not count or not trend_points:
            raise ValueError("raw point distribution empty")
    except (
        OSError,
        ValueError,
        TypeError,
        KeyError,
        OverflowError,
        RecursionError,
        contract.ContractError,
    ) as exc:
        return 0, ["raw points invalid: " + type(exc).__name__]
    return count, []


def inspect_exit(
    attempt_dir: pathlib.Path,
) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        record = contract._load_json(attempt_dir / "exit.json")
    except contract.ContractError as exc:
        return None, [str(exc)]
    required = {
        "schema_version",
        "execution_state",
        "exit_code",
        "started_at",
        "ended_at",
    }
    if record.get("schema_version") == contract.EXIT_SCHEMA:
        required.add("raw_points_required")
        if record.get("raw_points_required") is not True:
            return None, ["native raw point requirement invalid"]
    if set(record) not in (required, required | {"error_class"}):
        return None, ["exit metadata keys are invalid"]
    if (
        record["schema_version"] not in {contract.EXIT_SCHEMA, "hyhome.quality-exit/v1"}
        or record["execution_state"] not in {"completed", "interrupted"}
        or isinstance(record["exit_code"], bool)
        or not isinstance(record["exit_code"], int)
    ):
        return None, ["exit metadata values are invalid"]
    try:
        started = contract._parse_timestamp(record["started_at"])
        ended = contract._parse_timestamp(record["ended_at"])
    except contract.ContractError as exc:
        return None, [str(exc)]
    if ended < started:
        return None, ["exit end time precedes start time"]
    return record, []
