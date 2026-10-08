"""Create, verify and remove the per-run OTLP relay of one k6 attempt.

The relay is the only metrics peer k6 may reach. It joins exactly the run
network (alias `metrics-ingress`) and one internal egress network that reaches
HOME Alloy, holds the bearer token, and replaces every producer resource
attribute with the run identity it receives from this controller (SPEC-0214).
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import stat
import subprocess
import time
from collections.abc import Callable
from typing import Any

CONFIG = pathlib.Path(__file__).resolve().with_name("metrics-ingress.alloy")
CONFIG_TARGET = "/etc/alloy/relay.alloy"
TOKEN_TARGET = "/run/secrets/quality_otlp_token"
COMMAND = ["run", "--storage.path=/tmp/alloy", CONFIG_TARGET]
ALIAS = "metrics-ingress"
ROLE = "metrics-ingress"
IMAGE = re.compile(r"grafana/alloy@sha256:[0-9a-f]{64}")
NAME = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_.-]{0,127}")
MAX_TOKEN_BYTES = 4096
ENTRYPOINT = ["/bin/alloy"]
# The image's own environment; anything else beside the identity is refused.
IMAGE_ENV = {"PATH", "ALLOY_DEPLOY_MODE"}
TMPFS = {"/tmp": "rw,noexec,nosuid,nodev,size=64m"}
LIMITS = {
    "NanoCpus": 250_000_000,
    "Memory": 256 * 2**20,
    "MemorySwap": 256 * 2**20,
    "PidsLimit": 64,
}
# Alloy serves /-/ready on its loopback HTTP server; the image ships bash.
HEALTH = (
    "exec 3<>/dev/tcp/127.0.0.1/12345 && "
    'printf "GET /-/ready HTTP/1.0\\r\\n\\r\\n" >&3 && head -1 <&3 | grep -q " 200"'
)


class RelayError(ValueError):
    """The per-run relay could not be created, verified or removed safely."""


def relay_name(manifest: dict[str, Any]) -> str:
    return (
        f"hyhome-k6relay-{manifest['run_id'].replace('-', '')}-a{manifest['attempt']}"
    )


def environment(manifest: dict[str, Any]) -> dict[str, str]:
    """The only identity the relay stamps on forwarded metrics."""
    return {
        "HYHOME_QUALITY_PROJECT_ID": manifest["project_id"],
        "HYHOME_QUALITY_ENVIRONMENT": manifest["environment"],
        "HYHOME_QUALITY_INSTANCE": f"{manifest['run_id']}-a{manifest['attempt']}",
    }


def _labels(manifest: dict[str, Any]) -> dict[str, str]:
    return {
        "hyhome.quality.run_id": manifest["run_id"],
        "hyhome.quality.attempt": str(manifest["attempt"]),
        "hyhome.quality.role": ROLE,
    }


def _sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _token(path: pathlib.Path) -> pathlib.Path:
    """A regular, non-empty, single-line file that other users cannot read."""
    try:
        info = path.lstat()
    except OSError as exc:
        raise RelayError("relay token file is unavailable") from exc
    if (
        not path.is_absolute()
        or "," in str(path)
        or not stat.S_ISREG(info.st_mode)
        or info.st_mode & 0o007
        or not 0 < info.st_size <= MAX_TOKEN_BYTES
        or path.read_bytes().rstrip(b"\n").count(b"\n")
    ):
        raise RelayError("relay token file must be a private single-line file")
    return path


def _docker(
    docker: str, context: str, *arguments: str, timeout: int = 30
) -> subprocess.CompletedProcess[str]:
    from container_executor import _docker_environment

    return subprocess.run(
        [docker, "--context", context, *arguments],
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
        env=_docker_environment(),
    )


def start(
    manifest: dict[str, Any],
    docker: str,
    context: str,
    run_network: str,
    egress_network: str,
    image: str,
    token_file: pathlib.Path,
    ready_seconds: int = 60,
    sleep: Callable[[float], None] = time.sleep,
) -> str:
    """Create the relay, attach both networks, start it and wait until ready."""
    if (
        not IMAGE.fullmatch(image)
        or not all(
            NAME.fullmatch(item) for item in (context, run_network, egress_network)
        )
        or run_network == egress_network
        or "," in str(CONFIG)
    ):
        raise RelayError("relay inputs are outside the approved contract")
    token = _token(token_file)
    name = relay_name(manifest)
    command = ["create", "--pull", "never", "--name", name]
    for key, value in _labels(manifest).items():
        command += ["--label", f"{key}={value}"]
    for key, value in environment(manifest).items():
        command += ["--env", f"{key}={value}"]
    command += [
        "--user", f"{os.geteuid()}:{os.getegid()}",
        "--read-only",
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "--pids-limit", "64",
        "--cpus", "0.250",
        "--memory", "256m",
        "--memory-swap", "256m",
        "--tmpfs", f"/tmp:{TMPFS['/tmp']}",
        "--restart", "no",
        "--network", run_network,
        "--network-alias", ALIAS,
        "--mount", f"type=bind,src={CONFIG},dst={CONFIG_TARGET},readonly",
        "--mount", f"type=bind,src={token},dst={TOKEN_TARGET},readonly",
        "--health-cmd", f"bash -c '{HEALTH}'",
        "--health-interval", "2s",
        "--health-timeout", "2s",
        "--health-retries", "15",
        image,
        *COMMAND,
    ]  # fmt: skip
    try:
        if _docker(docker, context, *command).returncode != 0:
            raise RelayError("relay could not be created; run cleanup for this run")
        for step in (
            ("network", "connect", egress_network, name),
            ("start", name),
        ):
            if _docker(docker, context, *step).returncode != 0:
                raise RelayError("relay could not be attached or started")
        for _ in range(ready_seconds):
            state = _docker(
                docker, context, "inspect", "--format", "{{.State.Health.Status}}", name
            )
            if state.returncode == 0 and state.stdout.strip() == "healthy":
                return name
            sleep(1)
        raise RelayError("relay did not become ready")
    except BaseException:
        # Keep the original error (a cancel stays a cancel); a relay that
        # cannot be removed here is left to `cleanup --run-id`.
        try:
            stop(manifest, docker, context)
        except RelayError:
            pass
        raise


def stop(manifest: dict[str, Any], docker: str, context: str) -> bool:
    """Drain and remove this attempt's relay; never touch another container."""
    name = relay_name(manifest)
    found = _docker(
        docker, context, "inspect", "--format", "{{json .Config.Labels}}", name
    )
    if found.returncode != 0:
        return False
    labels = json.loads(found.stdout or "null")
    if not isinstance(labels, dict) or any(
        labels.get(key) != value for key, value in _labels(manifest).items()
    ):
        raise RelayError("container with the relay name belongs to another run")
    # SIGTERM lets Alloy flush its export queue before the container goes.
    _docker(docker, context, "stop", "--time", "10", name, timeout=30)
    if _docker(docker, context, "rm", "--force", name).returncode != 0:
        raise RelayError("relay could not be removed")
    return True


def cleanup(run_id: str, docker: str, context: str) -> list[str]:
    """Remove the relay and k6 runner containers left by one run, and no other."""
    listed = _docker(
        docker, context, "ps", "--all", "--quiet",
        "--filter", f"label=hyhome.quality.run_id={run_id}",
    )  # fmt: skip
    if listed.returncode != 0:
        raise RelayError("containers of the run could not be listed")
    removed = []
    for container in listed.stdout.split():
        record = _docker(docker, context, "inspect", container)
        if record.returncode != 0:
            continue
        (item,) = json.loads(record.stdout)
        labels = item.get("Config", {}).get("Labels") or {}
        if labels.get("hyhome.quality.run_id") != run_id or labels.get(
            "hyhome.quality.role"
        ) not in {ROLE, "k6-runner"}:
            continue
        if _docker(docker, context, "rm", "--force", item["Id"]).returncode == 0:
            removed.append(item["Name"].lstrip("/"))
    return removed


def contract(
    manifest: dict[str, Any],
    relay: dict[str, Any],
    run_network: str,
    egress_network: str,
    egress: dict[str, Any],
) -> None:
    """The executor admits the relay only if it is exactly what `start` builds."""
    config = relay.get("Config")
    host = relay.get("HostConfig")
    settings = relay.get("NetworkSettings")
    if not all(isinstance(item, dict) for item in (config, host, settings)):
        raise RelayError("metrics ingress peer contract is invalid")
    labels = config.get("Labels") or {}
    networks = settings.get("Networks")
    endpoint = networks.get(run_network) if isinstance(networks, dict) else None
    aliases = endpoint.get("Aliases") if isinstance(endpoint, dict) else None
    identity = [f"{key}={value}" for key, value in environment(manifest).items()]
    mounts = {
        item.get("Destination"): item
        for item in relay.get("Mounts") or []
        if isinstance(item, dict)
    }
    source = pathlib.Path(str(mounts.get(CONFIG_TARGET, {}).get("Source", "")))
    token = pathlib.Path(str(mounts.get(TOKEN_TARGET, {}).get("Source", "")))
    try:
        _token(token)
    except RelayError as exc:
        raise RelayError("metrics ingress peer contract is invalid") from exc
    env = config.get("Env") or []
    restart = host.get("RestartPolicy") or {}
    if (
        relay.get("Name") != f"/{relay_name(manifest)}"
        or relay.get("State", {}).get("Running") is not True
        or any(labels.get(key) != value for key, value in _labels(manifest).items())
        or not IMAGE.fullmatch(str(config.get("Image")))
        or config.get("Cmd") != COMMAND
        or config.get("Entrypoint") != ENTRYPOINT
        or config.get("User") != f"{os.geteuid()}:{os.getegid()}"
        or sorted(item for item in env if item.startswith("HYHOME_"))
        != sorted(identity)
        or any(
            item.split("=", 1)[0] not in IMAGE_ENV
            for item in env
            if not item.startswith("HYHOME_")
        )
        or any(host.get(key) != value for key, value in LIMITS.items())
        or restart.get("Name") not in ("no", "")
        or host.get("Tmpfs") != TMPFS
        or host.get("ReadonlyRootfs") is not True
        or host.get("Privileged") is not False
        or host.get("CapDrop") != ["ALL"]
        or host.get("CapAdd") not in ([], None)
        or host.get("PortBindings") not in ({}, None)
        or host.get("PublishAllPorts") is True
        or host.get("ExtraHosts") not in ([], None)
        or not any(
            str(item).startswith("no-new-privileges")
            for item in host.get("SecurityOpt") or []
        )
        or set(mounts) != {CONFIG_TARGET, TOKEN_TARGET}
        or any(
            item.get("Type") != "bind" or item.get("RW") is not False
            for item in mounts.values()
        )
        or not source.is_file()
        or source.is_symlink()
        or _sha256(source) != _sha256(CONFIG)
        or not isinstance(networks, dict)
        or set(networks) != {run_network, egress_network}
        or not isinstance(aliases, list)
        or ALIAS not in aliases
        or egress.get("Name") != egress_network
        or egress.get("Driver") != "bridge"
        or egress.get("Scope") != "local"
        or egress.get("Internal") is not True
    ):
        raise RelayError("metrics ingress peer contract is invalid")
