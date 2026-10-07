#!/usr/bin/env python3
"""Prepare, finalize, normalize, and import one immutable k6 attempt."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import ipaddress
import json
import math
import os
import pathlib
import re
import stat
import sys
import urllib.parse
import uuid
from typing import Any

MANIFEST_SCHEMA = "hyhome.quality-run/v2"
# v1 stays readable and means telemetry mode "none" (compatible change).
MANIFEST_SCHEMAS = ("hyhome.quality-run/v1", MANIFEST_SCHEMA)
TELEMETRY_MODES = ("none", "otlp")
EXIT_SCHEMA = "hyhome.quality-exit/v2"
FINAL_SCHEMA = "hyhome.quality-final/v1"
IMPORT_SCHEMA = "hyhome.quality-import/v1"
MAX_JSON_BYTES = 1024 * 1024
MAX_SCENARIO_BYTES = 16 * 1024 * 1024
SLUG = re.compile(r"[a-z0-9][a-z0-9-]{0,62}")
SHA256 = re.compile(r"[0-9a-f]{64}")
IMAGE = re.compile(r"[a-z0-9./_-]+@sha256:[0-9a-f]{64}")
REVISION = re.compile(r"[0-9a-f]{40}")
MANAGEMENT_PATHS = (
    "/__admin",
    "/admin",
    "/manage",
    "/management",
    "/metrics",
    "/debug",
)
PRIVATE_SUPERNETS = (
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("fc00::/7"),
)


class ContractError(ValueError):
    """A bounded quality-run contract was violated."""


def _canonical(value: object) -> bytes:
    try:
        return (
            json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n"
        ).encode()
    except (TypeError, ValueError) as exc:
        raise ContractError("value is not canonical JSON") from exc


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        info = path.lstat()
    except FileNotFoundError as exc:
        raise ContractError(f"missing artifact: {path.name}") from exc
    if not stat.S_ISREG(info.st_mode) or path.is_symlink():
        raise ContractError(f"artifact must be a regular file: {path.name}")
    if info.st_size > MAX_JSON_BYTES:
        raise ContractError(f"artifact is too large: {path.name}")
    try:
        value = json.loads(
            path.read_bytes(),
            object_pairs_hook=_pairs,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ContractError(f"non-finite JSON number: {value}")
            ),
        )
    except ContractError:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"invalid JSON artifact: {path.name}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"JSON artifact must be an object: {path.name}")
    _reject_nonfinite(value)
    return value


def _reject_nonfinite(value: object) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ContractError("non-finite JSON number")
    if isinstance(value, dict):
        for child in value.values():
            _reject_nonfinite(child)
    elif isinstance(value, list):
        for child in value:
            _reject_nonfinite(child)


def _exact_keys(value: dict[str, Any], expected: set[str], name: str) -> None:
    missing = expected - value.keys()
    extra = value.keys() - expected
    if missing or extra:
        raise ContractError(
            f"{name} keys mismatch; missing={sorted(missing)}, extra={sorted(extra)}"
        )


def _bounded_int(value: object, name: str, low: int, high: int) -> int:
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or not low <= value <= high
    ):
        raise ContractError(f"{name} must be an integer in {low}..{high}")
    return value


def _validate_origin(origin: object) -> str:
    if not isinstance(origin, str) or len(origin) > 255:
        raise ContractError("target origin must be a bounded string")
    parsed = urllib.parse.urlsplit(origin)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or parsed.path not in {"", "/"}
    ):
        raise ContractError("target origin must contain only scheme, host, and port")
    host = parsed.hostname
    try:
        address = ipaddress.ip_address(host)
    except ValueError as exc:
        if host == "localhost" or ("." in host and not host.endswith(".internal")):
            raise ContractError("public target origins are prohibited") from exc
    else:
        if (
            address.is_unspecified
            or address.is_loopback
            or address.is_link_local
            or address.is_multicast
            or not any(address in network for network in PRIVATE_SUPERNETS)
        ):
            raise ContractError("public target origins are prohibited")
    return origin.rstrip("/")


def validate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "schema_version",
        "run_id",
        "attempt",
        "project_id",
        "environment",
        "generator",
        "source_revision",
        "tool_image",
        "fixture_sha256",
        "scenario_path",
        "mock_mode",
        "target",
        "redirects",
        "budget",
        "thresholds",
    }
    if manifest.get("schema_version") == MANIFEST_SCHEMA:
        expected.add("telemetry")
    _exact_keys(manifest, expected, "manifest")
    if manifest["schema_version"] not in MANIFEST_SCHEMAS:
        raise ContractError(f"schema_version must be one of {MANIFEST_SCHEMAS}")
    telemetry = manifest.get("telemetry", {"mode": "none"})
    if not isinstance(telemetry, dict):
        raise ContractError("telemetry must be an object")
    # The executor owns the endpoint, credential and resource attributes.
    _exact_keys(telemetry, {"mode"}, "telemetry")
    if telemetry["mode"] not in TELEMETRY_MODES:
        raise ContractError("telemetry mode is not allowed")
    try:
        run_id = str(uuid.UUID(str(manifest["run_id"])))
    except (ValueError, AttributeError) as exc:
        raise ContractError("run_id must be a canonical UUID") from exc
    if manifest["run_id"] != run_id:
        raise ContractError("run_id must be a canonical UUID")
    _bounded_int(manifest["attempt"], "attempt", 1, 999)
    if not isinstance(manifest["project_id"], str) or not SLUG.fullmatch(
        manifest["project_id"]
    ):
        raise ContractError("project_id must be a lowercase slug")
    if manifest["environment"] not in {"development", "test", "staging"}:
        raise ContractError("environment is not allowed")
    if manifest["generator"] != "k6":
        raise ContractError("generator must be k6")
    if not isinstance(manifest["source_revision"], str) or not REVISION.fullmatch(
        manifest["source_revision"]
    ):
        raise ContractError("source_revision must be a full lowercase Git SHA")
    if not isinstance(manifest["tool_image"], str) or not IMAGE.fullmatch(
        manifest["tool_image"]
    ):
        raise ContractError("tool_image must use an immutable sha256 digest")
    if not isinstance(manifest["fixture_sha256"], str) or not SHA256.fullmatch(
        manifest["fixture_sha256"]
    ):
        raise ContractError("fixture_sha256 must be lowercase sha256")
    scenario = pathlib.PurePosixPath(str(manifest["scenario_path"]))
    if (
        scenario.is_absolute()
        or ".." in scenario.parts
        or scenario.suffix != ".js"
        or len(scenario.parts) == 0
    ):
        raise ContractError("scenario_path must be a relative JavaScript path")
    if manifest["mock_mode"] not in {"none", "function", "load"}:
        raise ContractError("mock_mode is not allowed")

    target = manifest["target"]
    if not isinstance(target, dict):
        raise ContractError("target must be an object")
    _exact_keys(
        target,
        {"origin", "allowed_origins", "allowed_networks", "paths"},
        "target",
    )
    origin = _validate_origin(target["origin"])
    origins = target["allowed_origins"]
    if not isinstance(origins, list) or not origins or len(origins) > 8:
        raise ContractError("allowed_origins must contain 1..8 origins")
    normalized_origins = [_validate_origin(item) for item in origins]
    if normalized_origins != [origin]:
        raise ContractError("v1 allowed_origins must contain only the target origin")
    networks = target["allowed_networks"]
    if not isinstance(networks, list) or not networks or len(networks) > 8:
        raise ContractError("allowed_networks must contain 1..8 private CIDRs")
    parsed_networks = []
    for item in networks:
        try:
            network = ipaddress.ip_network(item, strict=True)
        except (TypeError, ValueError) as exc:
            raise ContractError("allowed_networks contains invalid CIDR") from exc
        if network.is_global:
            raise ContractError("allowed_networks must be private")
        if not any(
            network.subnet_of(private) for private in PRIVATE_SUPERNETS
        ) or network.prefixlen < (24 if network.version == 4 else 64):
            raise ContractError("allowed_networks must be bounded private CIDRs")
        parsed_networks.append(network)
    try:
        target_address = ipaddress.ip_address(
            urllib.parse.urlsplit(origin).hostname or ""
        )
    except ValueError:
        pass
    else:
        if not any(target_address in network for network in parsed_networks):
            raise ContractError("target IP is outside allowed_networks")
    paths = target["paths"]
    if not isinstance(paths, list) or not paths or len(paths) > 64:
        raise ContractError("target paths must contain 1..64 paths")
    for request_path in paths:
        if (
            not isinstance(request_path, str)
            or not request_path.startswith("/")
            or "?" in request_path
            or "#" in request_path
            or len(request_path) > 512
            or "%" in request_path
            or "\\" in request_path
            or "//" in request_path
            or any(part in {".", ".."} for part in request_path.split("/"))
            or any(
                character.isspace() or ord(character) < 32 or ord(character) == 127
                for character in request_path
            )
        ):
            raise ContractError("target path is invalid")
        lowered = request_path.lower().rstrip("/")
        if any(
            lowered == item or lowered.startswith(f"{item}/")
            for item in MANAGEMENT_PATHS
        ):
            raise ContractError("management paths are prohibited")

    redirects = manifest["redirects"]
    if not isinstance(redirects, dict):
        raise ContractError("redirects must be an object")
    _exact_keys(redirects, {"policy", "max_redirects"}, "redirects")
    if redirects != {"policy": "deny", "max_redirects": 0}:
        raise ContractError("v1 redirect policy must deny all redirects")

    budget = manifest["budget"]
    if not isinstance(budget, dict):
        raise ContractError("budget must be an object")
    limits = {
        "users": (1, 500),
        "rate_per_second": (1, 10_000),
        "duration_seconds": (1, 3600),
        "max_iterations": (1, 10_000_000),
        "cpu_millis": (100, 8000),
        "memory_mib": (64, 16_384),
    }
    _exact_keys(budget, set(limits), "budget")
    for name, (low, high) in limits.items():
        _bounded_int(budget[name], name, low, high)
    thresholds = manifest["thresholds"]
    if not isinstance(thresholds, dict) or not thresholds or len(thresholds) > 64:
        raise ContractError("thresholds must contain 1..64 metrics")
    for metric, expressions in thresholds.items():
        if not isinstance(metric, str) or not re.fullmatch(
            r"[A-Za-z0-9_:{}.-]{1,128}", metric
        ):
            raise ContractError("threshold metric name is invalid")
        if (
            not isinstance(expressions, list)
            or not expressions
            or len(expressions) > 16
            or any(
                not isinstance(item, str) or not 1 <= len(item) <= 128
                for item in expressions
            )
        ):
            raise ContractError("threshold expressions are invalid")
    return manifest


def _sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_once(path: pathlib.Path, value: object) -> None:
    payload = _canonical(value)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC
    try:
        descriptor = os.open(path, flags, 0o640)
    except FileExistsError as already_exists:
        try:
            info = path.lstat()
            if not stat.S_ISREG(info.st_mode) or path.is_symlink():
                raise ContractError(
                    f"existing artifact is not a regular file: {path.name}"
                )
            existing = path.read_bytes()
        except OSError as exc:
            raise ContractError(
                f"cannot verify existing artifact: {path.name}"
            ) from exc
        if existing != payload:
            raise ContractError(
                f"immutable artifact conflict: {path.name}"
            ) from already_exists
        return
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())


def prepare(
    manifest_path: pathlib.Path, scenario_root: pathlib.Path, attempt_dir: pathlib.Path
) -> dict[str, Any]:
    manifest = validate_manifest(_load_json(manifest_path))
    root = scenario_root.resolve(strict=True)
    candidate = root / manifest["scenario_path"]
    if candidate.is_symlink():
        raise ContractError("scenario must not be a symlink")
    scenario = candidate.resolve(strict=True)
    try:
        scenario.relative_to(root)
    except ValueError as exc:
        raise ContractError("scenario_path escapes scenario root") from exc
    if (
        scenario.is_symlink()
        or not scenario.is_file()
        or scenario.stat().st_size > MAX_SCENARIO_BYTES
    ):
        raise ContractError("scenario must be a bounded regular file")
    if _sha256(scenario) != manifest["fixture_sha256"]:
        raise ContractError("fixture_sha256 does not match scenario bytes")
    try:
        attempt_dir.mkdir(mode=0o750)
    except FileExistsError as exc:
        raise ContractError("attempt directory already exists") from exc
    except OSError as exc:
        raise ContractError("attempt directory cannot be created") from exc
    _write_once(attempt_dir / "manifest.json", manifest)
    return manifest


def _timestamp() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_timestamp(value: object) -> dt.datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ContractError("timestamp must be RFC3339 UTC")
    try:
        parsed = dt.datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ContractError("timestamp must be RFC3339 UTC") from exc
    if parsed.tzinfo != dt.UTC:
        raise ContractError("timestamp must be RFC3339 UTC")
    return parsed


def finalize(attempt_dir: pathlib.Path) -> dict[str, Any]:
    from result_inspection import inspect_exit, inspect_raw_points, inspect_summary

    manifest = validate_manifest(_load_json(attempt_dir / "manifest.json"))
    _summary, samples, thresholds_ok, issues = inspect_summary(attempt_dir, manifest)
    exit_record, exit_issues = inspect_exit(attempt_dir)
    issues.extend(exit_issues)
    raw_required = bool(exit_record and exit_record.get("raw_points_required"))
    raw_issues: list[str] = []
    if raw_required or (attempt_dir / "raw-points.json").exists():
        _, raw_issues = inspect_raw_points(attempt_dir, manifest)
        issues.extend(raw_issues)
    execution_state = (
        exit_record["execution_state"] if exit_record is not None else "interrupted"
    )
    evidence_state = (
        "complete"
        if not issues and execution_state == "completed" and samples > 0
        else "incomplete"
    )
    import_allowed = (
        not raw_issues and "summary contains prohibited tags or strings" not in issues
    )
    exit_code = exit_record["exit_code"] if exit_record is not None else None
    if evidence_state == "incomplete":
        verdict = "incomplete"
    elif not thresholds_ok:
        verdict = "failed_threshold"
    elif exit_code != 0:
        verdict = "failed_execution"
    else:
        verdict = "passed"
    artifact_names = ["manifest.json", "scenario.js", "raw-summary.json", "exit.json"]
    if raw_required or (attempt_dir / "raw-points.json").exists():
        artifact_names.append("raw-points.json")
    artifacts = []
    for name in artifact_names:
        path = attempt_dir / name
        if path.is_file() and not path.is_symlink():
            artifacts.append(
                {
                    "name": name,
                    "sha256": _sha256(path),
                    "bytes": path.stat().st_size,
                }
            )
    checksums = {
        "schema_version": "hyhome.quality-checksums/v1",
        "artifacts": artifacts,
    }
    final: dict[str, Any] = {
        "schema_version": FINAL_SCHEMA,
        "run_id": manifest["run_id"],
        "attempt": manifest["attempt"],
        "project_id": manifest["project_id"],
        "execution_state": execution_state,
        "verdict": verdict,
        "evidence_state": evidence_state,
        "exit_code": exit_code,
        "started_at": exit_record.get("started_at") if exit_record else None,
        "ended_at": exit_record.get("ended_at") if exit_record else None,
        "samples": samples,
        "issues": sorted(set(issues)),
        "import_allowed": import_allowed,
    }
    checksums_path = attempt_dir / "checksums.json"
    _write_once(checksums_path, checksums)
    final["checksums_sha256"] = _sha256(checksums_path)
    final_path = attempt_dir / "final.json"
    _write_once(final_path, final)
    for path in [
        *(attempt_dir / artifact["name"] for artifact in artifacts),
        checksums_path,
        final_path,
    ]:
        path.chmod(0o440)
    return final


def prepare_import(
    attempt_dir: pathlib.Path,
    output_path: pathlib.Path,
    object_receipt_path: pathlib.Path | None = None,
    object_contract_path: pathlib.Path | None = None,
    approved_endpoints: tuple[str, ...] = (),
) -> dict[str, Any]:
    from result_inspection import inspect_summary

    manifest = validate_manifest(_load_json(attempt_dir / "manifest.json"))
    final = _load_json(attempt_dir / "final.json")
    final_keys = {
        "schema_version",
        "run_id",
        "attempt",
        "project_id",
        "execution_state",
        "verdict",
        "evidence_state",
        "exit_code",
        "started_at",
        "ended_at",
        "samples",
        "issues",
        "checksums_sha256",
        "import_allowed",
    }
    _exact_keys(final, final_keys, "final")
    if (
        final["schema_version"] != FINAL_SCHEMA
        or final["run_id"] != manifest["run_id"]
        or final["attempt"] != manifest["attempt"]
        or final["project_id"] != manifest["project_id"]
        or final["execution_state"] not in {"completed", "interrupted"}
        or final["verdict"]
        not in {"passed", "failed_threshold", "failed_execution", "incomplete"}
        or final["evidence_state"] not in {"complete", "incomplete"}
        or not isinstance(final["import_allowed"], bool)
        or not isinstance(final["checksums_sha256"], str)
        or not SHA256.fullmatch(final["checksums_sha256"])
        or final["checksums_sha256"] != _sha256(attempt_dir / "checksums.json")
    ):
        raise ContractError("final identity or states are invalid")
    if not final["import_allowed"]:
        raise ContractError("finalized evidence is quarantined and not importable")
    checksums = _load_json(attempt_dir / "checksums.json")
    artifacts = checksums.get("artifacts")
    if not isinstance(artifacts, list):
        raise ContractError("checksum artifact list is invalid")
    for artifact in artifacts:
        if not isinstance(artifact, dict) or set(artifact) != {
            "name",
            "sha256",
            "bytes",
        }:
            raise ContractError("checksum artifact entry is invalid")
        path = attempt_dir / str(artifact["name"])
        if (
            path.parent != attempt_dir
            or not path.is_file()
            or path.is_symlink()
            or path.stat().st_mode & 0o222
            or _sha256(path) != artifact["sha256"]
            or path.stat().st_size != artifact["bytes"]
        ):
            raise ContractError(f"checksum mismatch: {artifact.get('name', 'unknown')}")
    bound_artifacts = [dict(artifact, object_ref=None) for artifact in artifacts]
    if object_receipt_path is not None:
        from object_store import validate_object_binding, validate_receipt

        if object_contract_path is None:
            raise ContractError(
                "object references require an independently approved storage contract"
            )
        object_contract = _load_json(object_contract_path)
        try:
            receipt = validate_receipt(_load_json(object_receipt_path))
            if receipt["contract"] != object_contract:
                raise ContractError(
                    "object receipt differs from approved storage contract"
                )
            for item in receipt["artifacts"]:
                validate_object_binding(
                    item["object_ref"],
                    receipt["identity"],
                    item,
                    object_contract,
                    approved_endpoints,
                )
        except ValueError as exc:
            raise ContractError("object receipt is invalid") from exc
        identity = {
            name: manifest[name] for name in ("project_id", "run_id", "attempt")
        }
        if receipt["identity"] != identity or receipt["final_sha256"] != _sha256(
            attempt_dir / "final.json"
        ):
            raise ContractError("object receipt identity or final checksum mismatch")
        uploaded = {item["name"]: item for item in receipt["artifacts"]}
        if set(uploaded) != {item["name"] for item in artifacts}:
            raise ContractError("object receipt artifact set mismatch")
        for artifact in artifacts:
            if any(
                uploaded[artifact["name"]][key] != artifact[key]
                for key in ("name", "sha256", "bytes")
            ):
                raise ContractError("object receipt artifact checksum mismatch")
        bound_artifacts = [
            dict(artifact, object_ref=uploaded[artifact["name"]]["object_ref"])
            for artifact in artifacts
        ]
    summary, _, _, _ = inspect_summary(attempt_dir, manifest)
    metrics = []
    if isinstance(summary, dict) and isinstance(summary.get("metrics"), dict):
        for name, metric in sorted(summary["metrics"].items()):
            if isinstance(metric, dict):
                metrics.append(
                    {
                        "name": name,
                        "type": metric.get("type"),
                        "contains": metric.get("contains"),
                        "values": metric.get("values", {}),
                        "thresholds": metric.get("thresholds", {}),
                    }
                )
    payload: dict[str, Any] = {
        "schema_version": IMPORT_SCHEMA,
        "identity": {
            "run_id": manifest["run_id"],
            "attempt": manifest["attempt"],
            "project_id": manifest["project_id"],
        },
        "manifest_sha256": _sha256(attempt_dir / "manifest.json"),
        "final_sha256": _sha256(attempt_dir / "final.json"),
        "execution_state": final.get("execution_state"),
        "reported_verdict": final.get("verdict"),
        "evidence_state": final.get("evidence_state"),
        "ingestion_state": "pending",
        "started_at": final.get("started_at"),
        "ended_at": final.get("ended_at"),
        "samples": final.get("samples"),
        "metrics": metrics,
        "artifacts": bound_artifacts,
    }
    payload["payload_sha256"] = hashlib.sha256(_canonical(payload)).hexdigest()
    _write_once(output_path, payload)
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare_command = subparsers.add_parser("prepare")
    prepare_command.add_argument("--manifest", required=True, type=pathlib.Path)
    prepare_command.add_argument("--scenario-root", required=True, type=pathlib.Path)
    prepare_command.add_argument("--attempt-dir", required=True, type=pathlib.Path)
    runner = subparsers.add_parser("run")
    runner.add_argument("--manifest", required=True, type=pathlib.Path)
    runner.add_argument("--scenario-root", required=True, type=pathlib.Path)
    runner.add_argument("--attempt-dir", required=True, type=pathlib.Path)
    runner.add_argument("--docker-context", required=True)
    runner.add_argument("--network", required=True)
    runner.add_argument("--wiremock-container", required=True)
    runner.add_argument("--docker-binary", default="docker")
    runner.add_argument("--guard-config", type=pathlib.Path)
    runner.add_argument("--backend-network")
    runner.add_argument("--backend-container")
    runner.add_argument("--metrics-ingress-container")
    runner.add_argument("--metrics-egress-network")
    guard = subparsers.add_parser("prepare-guard")
    guard.add_argument("--manifest", required=True, type=pathlib.Path)
    guard.add_argument("--output", required=True, type=pathlib.Path)
    finalizer = subparsers.add_parser("finalize")
    finalizer.add_argument("--attempt-dir", required=True, type=pathlib.Path)
    importer = subparsers.add_parser("prepare-import")
    importer.add_argument("--attempt-dir", required=True, type=pathlib.Path)
    importer.add_argument("--output", required=True, type=pathlib.Path)
    importer.add_argument("--object-receipt", type=pathlib.Path)
    database_importer = subparsers.add_parser("import-db")
    database_importer.add_argument("--envelope", required=True, type=pathlib.Path)
    database_importer.add_argument("--receipt", required=True, type=pathlib.Path)
    database_importer.add_argument("--psql-binary", default="psql")
    for operation in (importer, database_importer):
        operation.add_argument("--object-contract", type=pathlib.Path)
        operation.add_argument(
            "--approved-object-endpoint", action="append", default=[]
        )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "prepare":
            prepare(args.manifest, args.scenario_root, args.attempt_dir)
        elif args.command == "prepare-guard":
            from http_guard import configuration

            manifest = validate_manifest(_load_json(args.manifest))
            _write_once(args.output, configuration(manifest))
        elif args.command == "run":
            from container_executor import ExecutorError, execute

            manifest = prepare(args.manifest, args.scenario_root, args.attempt_dir)
            try:
                return execute(
                    manifest,
                    args.scenario_root,
                    args.attempt_dir,
                    args.network,
                    args.wiremock_container,
                    args.docker_binary,
                    args.docker_context,
                    args.guard_config,
                    args.backend_network,
                    args.backend_container,
                    args.metrics_ingress_container,
                    args.metrics_egress_network,
                )
            except ExecutorError as exc:
                raise ContractError(str(exc)) from exc
        elif args.command == "finalize":
            finalize(args.attempt_dir)
        elif args.command == "prepare-import":
            prepare_import(
                args.attempt_dir,
                args.output,
                args.object_receipt,
                args.object_contract,
                tuple(args.approved_object_endpoint),
            )
        else:
            from result_import import ImportContractError, import_db

            try:
                _, exit_code = import_db(
                    args.envelope,
                    args.receipt,
                    args.psql_binary,
                    args.object_contract,
                    tuple(args.approved_object_endpoint),
                )
            except ImportContractError as exc:
                raise ContractError(str(exc)) from exc
            return exit_code
    except ContractError as exc:
        print(f"quality-run: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
