#!/usr/bin/env python3
"""Run one k6 attempt in a pre-approved, isolated Docker network."""

from __future__ import annotations

import datetime as dt
import hashlib
import ipaddress
import json
import os
import pathlib
import re
import stat
import subprocess
from typing import Any

EXIT_SCHEMA = "hyhome.quality-exit/v2"
SHA256 = re.compile(r"[0-9a-f]{64}")
NAME = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_.-]{0,127}")
IMAGE = re.compile(r"[a-z0-9./_-]+@sha256:[0-9a-f]{64}")
MAX_INSPECT_BYTES = 1024 * 1024


class ExecutorError(RuntimeError):
    """The isolated Docker execution boundary was not satisfied."""


def _timestamp() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _canonical(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode()


def _write_once(path: pathlib.Path, payload: bytes, mode: int = 0o640) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC
    try:
        descriptor = os.open(path, flags, mode)
    except FileExistsError:
        if path.is_symlink() or not path.is_file() or path.read_bytes() != payload:
            raise ExecutorError(f"immutable artifact conflict: {path.name}") from None
        return
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())


def _write_exit(
    attempt_dir: pathlib.Path,
    state: str,
    exit_code: int,
    started_at: str,
    error_class: str | None = None,
) -> None:
    record: dict[str, Any] = {
        "schema_version": EXIT_SCHEMA,
        "raw_points_required": True,
        "execution_state": state,
        "exit_code": exit_code,
        "started_at": started_at,
        "ended_at": _timestamp(),
    }
    if error_class is not None:
        record["error_class"] = error_class
    _write_once(attempt_dir / "exit.json", _canonical(record))


def _docker_environment() -> dict[str, str]:
    allowed = {"PATH", "HOME", "DOCKER_CONFIG", "LANG", "LC_ALL", "TZ"}
    return {key: value for key, value in os.environ.items() if key in allowed}


def _inspect(
    docker: str,
    context: str,
    kind: str,
    target: str,
) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            [docker, "--context", context, kind, "inspect", target],
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
            env=_docker_environment(),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ExecutorError(f"Docker {kind} inspect failed") from exc
    if completed.returncode != 0 or len(completed.stdout.encode()) > MAX_INSPECT_BYTES:
        raise ExecutorError(f"Docker {kind} inspect failed")
    try:
        records = json.loads(completed.stdout)
    except (TypeError, json.JSONDecodeError) as exc:
        raise ExecutorError(f"Docker {kind} inspect returned invalid JSON") from exc
    if not isinstance(records, list) or len(records) != 1:
        raise ExecutorError(f"Docker {kind} inspect returned unexpected records")
    record = records[0]
    if not isinstance(record, dict):
        raise ExecutorError(f"Docker {kind} inspect returned an invalid record")
    return record


def _network_contract(
    manifest: dict[str, Any],
    network: dict[str, Any],
    requested_name: str,
    peer_name: str,
    metrics_peer: str | None = None,
) -> tuple[str, str]:
    labels = network.get("Labels")
    containers = network.get("Containers")
    ipam = network.get("IPAM")
    configs = ipam.get("Config") if isinstance(ipam, dict) else None
    if (
        network.get("Name") != requested_name
        or network.get("Driver") != "bridge"
        or network.get("Scope") != "local"
        or network.get("Internal") is not True
        or network.get("Attachable") is not False
        or not isinstance(labels, dict)
        or labels.get("hyhome.quality.run_id") != manifest["run_id"]
        or labels.get("hyhome.quality.purpose") != "k6-wiremock"
        or not isinstance(containers, dict)
        or len(containers) != (2 if metrics_peer else 1)
        or not isinstance(configs, list)
    ):
        raise ExecutorError("network is not a dedicated internal quality network")
    subnets = {
        item.get("Subnet")
        for item in configs
        if isinstance(item, dict) and isinstance(item.get("Subnet"), str)
    }
    if subnets != set(manifest["target"]["allowed_networks"]):
        raise ExecutorError("network subnets differ from the approved manifest")
    endpoints = {
        item.get("Name"): (key, item)
        for key, item in containers.items()
        if isinstance(item, dict)
    }
    if metrics_peer and set(endpoints) != {peer_name, metrics_peer}:
        raise ExecutorError("network peers are not the approved target and ingress")
    peer_id, endpoint = endpoints.get(peer_name, next(iter(containers.items())))
    if (
        not isinstance(endpoint, dict)
        or endpoint.get("Name") != peer_name
        or not isinstance(peer_id, str)
    ):
        raise ExecutorError("network peer is not the approved WireMock container")
    peer_address = str(endpoint.get("IPv4Address", "")).split("/", 1)[0]
    try:
        address = ipaddress.ip_address(peer_address)
    except ValueError as exc:
        raise ExecutorError("WireMock endpoint has no valid private address") from exc
    networks = [
        ipaddress.ip_network(value, strict=True)
        for value in manifest["target"]["allowed_networks"]
    ]
    if not any(address in item for item in networks):
        raise ExecutorError("WireMock endpoint is outside the approved network")
    network_id = network.get("Id")
    if not isinstance(network_id, str) or not NAME.fullmatch(network_id):
        raise ExecutorError("network has no usable immutable identifier")
    return network_id, peer_id


def _metrics_peer_contract(
    manifest: dict[str, Any],
    peer: dict[str, Any],
    network_name: str,
    peer_name: str,
) -> None:
    """Admit only the per-run OTLP relay; it, not k6, holds the Alloy token."""
    config = peer.get("Config")
    host = peer.get("HostConfig")
    labels = config.get("Labels") if isinstance(config, dict) else None
    settings = peer.get("NetworkSettings")
    networks = settings.get("Networks") if isinstance(settings, dict) else None
    endpoint = networks.get(network_name) if isinstance(networks, dict) else None
    aliases = endpoint.get("Aliases") if isinstance(endpoint, dict) else None
    image = config.get("Image") if isinstance(config, dict) else None
    if (
        peer.get("Name") != f"/{peer_name}"
        or peer.get("State", {}).get("Running") is not True
        or not isinstance(labels, dict)
        or labels.get("hyhome.quality.run_id") != manifest["run_id"]
        or labels.get("hyhome.quality.role") != "metrics-ingress"
        or not isinstance(image, str)
        or not image.startswith("grafana/alloy@sha256:")
        or not IMAGE.fullmatch(image)
        or not isinstance(host, dict)
        or host.get("ReadonlyRootfs") is not True
        or host.get("Privileged") is not False
        or host.get("CapDrop") != ["ALL"]
        or host.get("CapAdd") not in ([], None)
        or host.get("PortBindings") not in ({}, None)
        or not isinstance(aliases, list)
        or "metrics-ingress" not in aliases
        or not isinstance(networks, dict)
        or len(networks) > 2
    ):
        raise ExecutorError("metrics ingress peer contract is invalid")


def _telemetry_arguments(manifest: dict[str, Any]) -> list[str]:
    """k6 OTLP settings come from the executor and the validated manifest only."""
    resource = ",".join(
        (
            f"project.id={manifest['project_id']}",
            f"deployment.environment.name={manifest['environment']}",
            f"service.instance.id={manifest['run_id']}-a{manifest['attempt']}",
        )
    )
    settings = {
        "K6_OTEL_EXPORTER_PROTOCOL": "http/protobuf",
        "K6_OTEL_HTTP_EXPORTER_ENDPOINT": "metrics-ingress:4318",
        "K6_OTEL_HTTP_EXPORTER_URL_PATH": "/v1/metrics",
        "K6_OTEL_HTTP_EXPORTER_INSECURE": "true",
        "K6_OTEL_SERVICE_NAME": "k6",
        "K6_OTEL_METRIC_PREFIX": "k6_",
        "K6_OTEL_EXPORT_INTERVAL": "5s",
        "OTEL_RESOURCE_ATTRIBUTES": resource,
    }
    arguments = []
    for key, value in settings.items():
        arguments.extend(("--env", f"{key}={value}"))
    return arguments


def _peer_contract(
    manifest: dict[str, Any],
    peer: dict[str, Any],
    network_name: str,
    peer_name: str,
    expected_id: str,
) -> None:
    config = peer.get("Config")
    state = peer.get("State")
    labels = config.get("Labels") if isinstance(config, dict) else None
    command = config.get("Cmd") if isinstance(config, dict) else None
    exposed = config.get("ExposedPorts") if isinstance(config, dict) else None
    host = peer.get("HostConfig")
    settings = peer.get("NetworkSettings")
    networks = settings.get("Networks") if isinstance(settings, dict) else None
    ports = settings.get("Ports") if isinstance(settings, dict) else None
    endpoint = networks.get(network_name) if isinstance(networks, dict) else None
    aliases = endpoint.get("Aliases") if isinstance(endpoint, dict) else None
    if (
        not isinstance(peer.get("Id"), str)
        or not peer["Id"].startswith(expected_id)
        or peer.get("Name") != f"/{peer_name}"
        or not isinstance(state, dict)
        or state.get("Running") is not True
        or not isinstance(labels, dict)
        or labels.get("hyhome.quality.run_id") != manifest["run_id"]
        or labels.get("hyhome.quality.role") != "wiremock"
        or labels.get("hyhome.quality.mock_mode") != manifest["mock_mode"]
        or not isinstance(command, list)
        or "--admin-api-require-https" not in command
        or (manifest["mock_mode"] == "load" and "--no-request-journal" not in command)
        or not isinstance(exposed, dict)
        or "8080/tcp" not in exposed
        or not set(exposed) <= {"8080/tcp", "8443/tcp"}
        or any(str(item).startswith("--https-port") for item in command)
        or not isinstance(host, dict)
        or host.get("PortBindings") not in ({}, None)
        or host.get("ExtraHosts") not in ([], None)
        or not isinstance(networks, dict)
        or set(networks) != {network_name}
        or not isinstance(aliases, list)
        or "wiremock" not in aliases
        or (ports is not None and not isinstance(ports, dict))
        or any(value not in (None, []) for value in (ports or {}).values())
    ):
        raise ExecutorError("WireMock peer isolation contract is invalid")


def _snapshot_scenario(
    manifest: dict[str, Any],
    scenario_root: pathlib.Path,
    attempt_dir: pathlib.Path,
) -> pathlib.Path:
    root = scenario_root.resolve(strict=True)
    source = (root / manifest["scenario_path"]).resolve(strict=True)
    try:
        source.relative_to(root)
    except ValueError as exc:
        raise ExecutorError("scenario escaped its approved root") from exc
    if source.is_symlink() or not source.is_file() or "," in str(source):
        raise ExecutorError("scenario is not a mount-safe regular file")
    payload = source.read_bytes()
    if hashlib.sha256(payload).hexdigest() != manifest["fixture_sha256"]:
        raise ExecutorError("scenario changed after manifest preparation")
    snapshot = attempt_dir / "scenario.js"
    _write_once(snapshot, payload, 0o440)
    snapshot.chmod(0o440)
    return snapshot


def _summary_wrapper(
    manifest: dict[str, Any], attempt_dir: pathlib.Path
) -> pathlib.Path:
    # Preserve the external scenario exports; infra owns thresholds and summary.
    thresholds = json.dumps(manifest["thresholds"], sort_keys=True, allow_nan=False)
    payload = (
        "import * as scenario from '/scripts/scenario.js';\n"
        "export * from '/scripts/scenario.js';\n"
        "export default scenario.default;\n"
        f"export const options = {{...scenario.options, thresholds: {thresholds}}};\n"
        "export function handleSummary(data) { return {\n"
        "  '/results/raw-summary.json': JSON.stringify(data)\n"
        "}; }\n"
    ).encode()
    wrapper = attempt_dir / "runner.js"
    _write_once(wrapper, payload, 0o440)
    wrapper.chmod(0o440)
    return wrapper


def _prepare_result_file(
    attempt_dir: pathlib.Path, name: str = "raw-summary.json"
) -> pathlib.Path:
    result = attempt_dir / name
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC
    try:
        descriptor = os.open(result, flags, 0o640)
    except FileExistsError as exc:
        raise ExecutorError("raw summary already exists") from exc
    os.close(descriptor)
    return result


def execute(
    manifest: dict[str, Any],
    scenario_root: pathlib.Path,
    attempt_dir: pathlib.Path,
    network_name: str,
    peer_name: str,
    docker_binary: str = "docker",
    docker_context: str = "default",
    guard_config: pathlib.Path | None = None,
    backend_network: str | None = None,
    backend_peer: str | None = None,
    metrics_peer: str | None = None,
) -> int:
    telemetry = manifest.get("telemetry", {"mode": "none"})["mode"]
    if (telemetry == "otlp") != bool(metrics_peer) or (
        metrics_peer
        and (
            not NAME.fullmatch(metrics_peer)
            or metrics_peer in {peer_name, backend_peer}
        )
    ):
        raise ExecutorError("metrics ingress must be given exactly for OTLP telemetry")
    if (
        not NAME.fullmatch(network_name)
        or not NAME.fullmatch(peer_name)
        or not NAME.fullmatch(docker_context)
        or manifest["environment"] != "test"
        or manifest["mock_mode"] not in {"function", "load"}
        or manifest["target"]["origin"] != "http://wiremock:8080"
        or not isinstance(manifest.get("tool_image"), str)
        or not IMAGE.fullmatch(manifest["tool_image"])
    ):
        raise ExecutorError("executor inputs are outside the synthetic v1 contract")
    if (attempt_dir / "exit.json").exists():
        raise ExecutorError("attempt already has exit metadata")
    info = attempt_dir.stat()
    uid, gid = os.geteuid(), os.getegid()
    if (
        not stat.S_ISDIR(info.st_mode)
        or info.st_uid != uid
        or info.st_gid != gid
        or not info.st_mode & stat.S_IWUSR
        or not info.st_mode & stat.S_IXUSR
        or "," in str(attempt_dir.resolve())
    ):
        raise ExecutorError("attempt directory is not writable by the fixed run user")
    started_at = _timestamp()
    try:
        snapshot = _snapshot_scenario(manifest, scenario_root, attempt_dir)
        network = _inspect(docker_binary, docker_context, "network", network_name)
        network_id, peer_id = _network_contract(
            manifest, network, network_name, peer_name, metrics_peer
        )
        if metrics_peer:
            _metrics_peer_contract(
                manifest,
                _inspect(docker_binary, docker_context, "container", metrics_peer),
                network_name,
                metrics_peer,
            )
        peer = _inspect(docker_binary, docker_context, "container", peer_name)
        if guard_config is None:
            _peer_contract(manifest, peer, network_name, peer_name, peer_id)
        else:
            from http_guard import validate

            if (
                manifest["mock_mode"] != "load"
                or not backend_network
                or not backend_peer
                or not NAME.fullmatch(backend_network)
                or not NAME.fullmatch(backend_peer)
                or backend_network == network_name
                or not isinstance(peer.get("Id"), str)
                or not peer["Id"].startswith(peer_id)
                or peer.get("Name") != f"/{peer_name}"
                or peer.get("State", {}).get("Running") is not True
            ):
                raise ExecutorError("HTTP guard peer identity is invalid")
            validate(
                manifest,
                peer,
                network_name,
                backend_network,
                backend_peer,
                guard_config,
                lambda kind, name: _inspect(docker_binary, docker_context, kind, name),
                _canonical,
            )
        wrapper = _summary_wrapper(manifest, attempt_dir)
        result = _prepare_result_file(attempt_dir)
        points = _prepare_result_file(attempt_dir, "raw-points.json")
    except (
        ExecutorError,
        OSError,
        TypeError,
        KeyError,
        AttributeError,
        ValueError,
    ) as exc:
        _write_exit(
            attempt_dir,
            "interrupted",
            125,
            started_at,
            "isolation_preflight_failed",
        )
        if isinstance(exc, ExecutorError):
            raise
        raise ExecutorError("isolation preflight failed") from exc

    budget = manifest["budget"]
    container_name = (
        f"hyhome-k6-{manifest['run_id'].replace('-', '')}-a{manifest['attempt']}"
    )
    scenario_mount = (
        f"type=bind,src={snapshot},dst=/scripts/scenario.js,"
        "readonly,bind-propagation=rprivate"
    )
    result_mount = (
        f"type=bind,src={result},dst=/results/raw-summary.json,"
        "bind-propagation=rprivate"
    )
    command = [
        docker_binary,
        "--context",
        docker_context,
        "run",
        "--rm",
        "--pull",
        "never",
        "--name",
        container_name,
        "--network",
        network_id,
        "--read-only",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "--pids-limit",
        "128",
        "--cpus",
        f"{budget['cpu_millis'] / 1000:.3f}",
        "--memory",
        f"{budget['memory_mib']}m",
        "--memory-swap",
        f"{budget['memory_mib']}m",
        "--user",
        f"{uid}:{gid}",
        "--tmpfs",
        "/tmp:rw,noexec,nosuid,nodev,size=64m",
        "--ulimit",
        "nofile=1024:1024",
        "--ulimit",
        "fsize=67108864:67108864",
        "--mount",
        f"type=bind,src={points},dst=/results/raw-points.json,bind-propagation=rprivate",
        "--mount",
        scenario_mount,
        "--mount",
        result_mount,
        "--mount",
        f"type=bind,src={wrapper},dst=/scripts/runner.js,readonly,bind-propagation=rprivate",
        "--env",
        "HYHOME_TARGET_ORIGIN=http://wiremock:8080",
        *(_telemetry_arguments(manifest) if metrics_peer else []),
        manifest["tool_image"],
        "run",
        "--no-color",
        "--out",
        "json=/results/raw-points.json",
        *(("--out", "opentelemetry") if metrics_peer else ()),
        "--summary-trend-stats",
        "avg,min,med,max,p(90),p(95),p(99),count",
        "--max-redirects",
        "0",
        "--system-tags",
        "method,status,error_code,expected_response,scenario",
        "--vus",
        str(budget["users"]),
        "--rps",
        str(budget["rate_per_second"]),
        "--duration",
        f"{budget['duration_seconds']}s",
        "--iterations",
        str(budget["max_iterations"]),
    ]
    for name in ("project_id", "environment", "run_id", "attempt"):
        command.extend(("--tag", f"{name}={manifest[name]}"))
    command.extend(("--tag", f"testid={manifest['run_id']}", "/scripts/runner.js"))
    if guard_config is None:
        _write_exit(
            attempt_dir, "interrupted", 125, started_at, "path_confinement_unavailable"
        )
        raise ExecutorError("approved HTTP path enforcement proxy is not configured")
    command[command.index("--name") : command.index("--name")] = [
        "--label",
        f"hyhome.quality.run_id={manifest['run_id']}",
        "--label",
        "hyhome.quality.role=k6-runner",
    ]
    try:
        completed = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=budget["duration_seconds"] + 30,
            env=_docker_environment(),
        )
    except subprocess.TimeoutExpired:
        _write_exit(attempt_dir, "interrupted", 124, started_at, "runner_timeout")
        owned = _inspect(docker_binary, docker_context, "container", container_name)
        labels = owned.get("Config", {}).get("Labels", {})
        if (
            labels.get("hyhome.quality.run_id") == manifest["run_id"]
            and labels.get("hyhome.quality.role") == "k6-runner"
            and owned.get("Config", {}).get("Image") == manifest["tool_image"]
        ):
            subprocess.run(
                [
                    docker_binary,
                    "--context",
                    docker_context,
                    "rm",
                    "--force",
                    owned["Id"],
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=10,
                check=False,
                env=_docker_environment(),
            )
        return 124
    except OSError:
        _write_exit(attempt_dir, "interrupted", 127, started_at, "runner_unavailable")
        return 127
    exit_code = completed.returncode
    _write_exit(
        attempt_dir,
        "completed" if exit_code >= 0 else "interrupted",
        exit_code if exit_code >= 0 else 128 - exit_code,
        started_at,
    )
    return exit_code if exit_code >= 0 else 128 - exit_code
