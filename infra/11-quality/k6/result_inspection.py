"""Inspect k6 summary and exit artifacts without exporting unsafe strings."""

from __future__ import annotations

import pathlib
import re
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
    if set(record) not in (required, required | {"error_class"}):
        return None, ["exit metadata keys are invalid"]
    if (
        record["schema_version"] != contract.EXIT_SCHEMA
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
