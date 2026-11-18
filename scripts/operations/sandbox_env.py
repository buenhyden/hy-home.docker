#!/usr/bin/env python3
"""Isolated Docker sandbox: doctor, selective plan, owned start and cleanup.

Runs only on the per-user rootless Docker daemon, never on the production
socket. `plan` resolves the requested services and their `depends_on`
closure, refuses an empty, wildcard or `all` selection and an oversized one,
and blocks any service that would reach the host: the Docker socket, a bind
outside the repository or the run directory, a real secret file, host
networking or privilege. `up` starts an allowed closure as project
`hyhome-sbx-<run>` with every network internal and records the run; `down`
and `cleanup` remove only projects this tool recorded.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE_DIRECTORY = ".workspace-sandbox"
PROJECT_PREFIX = "hyhome-sbx-"
MAX_SERVICES = 8
MAX_MEMORY_BYTES = 4 * 1024**3
PRODUCTION_SOCKETS = ("/var/run/docker.sock", "/run/docker.sock")
SELECTION = re.compile(r"^[a-z0-9][a-z0-9_.-]*$")
TOOLS = (
    "docker",
    "dockerd-rootless-setuptool.sh",
    "rootlesskit",
    "newuidmap",
    "newgidmap",
    "slirp4netns",
    "qemu-system-x86_64",
    "k3d",
    "bwrap",
)


class SandboxError(Exception):
    """A refused or failed sandbox operation."""


def state_dir() -> Path:
    path = ROOT / STATE_DIRECTORY
    path.mkdir(mode=0o700, exist_ok=True)
    return path


def rootless_socket() -> Path:
    runtime = os.environ.get("XDG_RUNTIME_DIR") or f"/run/user/{os.getuid()}"
    return Path(runtime) / "docker.sock"


def _run(command, timeout=120, **options) -> subprocess.CompletedProcess:
    return subprocess.run(
        command, capture_output=True, text=True, timeout=timeout, check=False, **options
    )


def doctor() -> dict:
    """Read-only facts about the host and the rootless sandbox daemon."""
    memory = {}
    for line in Path("/proc/meminfo").read_text().splitlines()[:3]:
        key, value = line.split(":")
        memory[key] = int(value.split()[0]) * 1024
    subuid = Path("/etc/subuid")
    user = os.environ.get("USER", "")
    socket = rootless_socket()
    server = None
    if socket.is_socket():
        result = _run(
            [
                "docker",
                "-H",
                f"unix://{socket}",
                "version",
                "--format",
                "{{.Server.Version}}",
            ],
            timeout=10,
        )
        server = result.stdout.strip() if result.returncode == 0 else None
    tools = {tool: shutil.which(tool) is not None for tool in TOOLS}
    return {
        "kernel": os.uname().release,
        "cpus": os.cpu_count(),
        "memory_bytes": memory.get("MemTotal"),
        "memory_available_bytes": memory.get("MemAvailable"),
        "disk_free_bytes": shutil.disk_usage(ROOT).free,
        "kvm_usable": os.access("/dev/kvm", os.R_OK | os.W_OK),
        "tools": tools,
        "subuid": subuid.exists()
        and any(
            line.startswith(f"{user}:") for line in subuid.read_text().splitlines()
        ),
        "production_socket_writable": any(
            os.access(path, os.W_OK) for path in PRODUCTION_SOCKETS
        ),
        "rootless_socket": str(socket),
        "rootless_server": server,
        "rootless_ready": server is not None,
        "rootless_installable": tools["dockerd-rootless-setuptool.sh"]
        and tools["newuidmap"]
        and tools["newgidmap"],
    }


def render(files: list[Path]) -> dict:
    """Render the compose model read-only, every profile included."""
    command = ["docker", "compose"]
    for file in files:
        command += ["-f", str(file)]
    command += ["--profile", "*", "config", "--format", "json"]
    result = _run(command, timeout=180, cwd=ROOT)
    if result.returncode != 0:
        raise SandboxError(f"compose render failed: {result.stderr.strip()[:200]}")
    return json.loads(result.stdout)


def closure(config: dict, requested: list[str]) -> list[str]:
    services = config.get("services", {})
    if not requested:
        raise SandboxError(
            "an empty selection would start every service; name services"
        )
    for name in requested:
        if name.lower() == "all" or not SELECTION.match(name):
            raise SandboxError(f"refused selection {name!r}: no wildcard or all")
        if name not in services:
            raise SandboxError(f"unknown service {name!r}")
    selected, pending = set(), list(requested)
    while pending:
        name = pending.pop()
        if name not in selected:
            selected.add(name)
            pending.extend(services[name].get("depends_on") or {})
    return sorted(selected)


def _inside(path: str, root: Path) -> bool:
    return Path(path).resolve().is_relative_to(root.resolve())


# Repository paths that hold secrets, state or history; never mounted.
PRIVATE_PARTS = ("secrets", ".git")


def _repository_safe(source: str) -> bool:
    if not _inside(source, ROOT):
        return False
    parts = Path(source).resolve().relative_to(ROOT.resolve()).parts
    return not any(
        part in PRIVATE_PARTS or part.startswith((".env", ".workspace-"))
        for part in parts
    )


def _host_namespace(service: dict) -> list[str]:
    found = []
    mode = service.get("network_mode")
    if mode and mode != "none" and not str(mode).startswith("service:"):
        found.append(f"uses network_mode {mode}")
    for key in ("pid", "ipc", "uts", "userns_mode", "cgroup"):
        if str(service.get(key, "")) == "host" or str(service.get(key, "")).startswith(
            "container:"
        ):
            found.append(f"shares the {key} namespace {service.get(key)}")
    if service.get("privileged"):
        found.append("runs privileged")
    reservations = (
        service.get("deploy", {}).get("resources", {}).get("reservations", {})
    )
    if service.get("devices") or reservations.get("devices") or service.get("gpus"):
        found.append("maps host devices or GPUs")
    if service.get("runtime"):
        found.append(f"uses the {service.get('runtime')} runtime")
    if service.get("cap_add"):
        found.append(f"adds capabilities {service.get('cap_add')}")
    if any("unconfined" in str(o) for o in service.get("security_opt") or []):
        found.append("disables a security profile")
    return found


def assess(config: dict, selected: list[str], run_dir: Path) -> dict[str, list[str]]:
    """Name every way a selected service would reach the host or exceed limits."""
    services, secrets = config["services"], config.get("secrets", {})
    volumes, networks = config.get("volumes", {}), config.get("networks", {})
    configs = config.get("configs", {})
    problems: dict[str, list[str]] = {}
    total = 0
    for name in selected:
        service, found = services[name], []
        for mount in service.get("volumes") or []:
            source = str(mount.get("source", ""))
            if "docker.sock" in source:
                found.append(f"mounts the Docker socket {source}")
            elif mount.get("type") == "bind" and not (
                (_repository_safe(source) and mount.get("read_only"))
                or _inside(source, run_dir)
            ):
                found.append(f"binds a host path outside the sandbox: {source}")
            elif mount.get("type") == "volume":
                declared = volumes.get(source, {}) or {}
                options = " ".join(
                    map(str, (declared.get("driver_opts") or {}).values())
                )
                if (
                    declared.get("external")
                    or declared.get("driver") not in (None, "local")
                    or "bind" in options
                    or "device" in (declared.get("driver_opts") or {})
                ):
                    found.append(f"uses a volume that reaches the host: {source}")
            elif mount.get("type") not in ("bind", "volume", "tmpfs"):
                found.append(f"uses a {mount.get('type')} mount")
        for secret in service.get("secrets") or []:
            source = secrets.get(secret.get("source", ""), {}).get("file", "")
            if not source or not _inside(source, run_dir):
                found.append(f"uses a real secret file {secret.get('source')}")
        for item in service.get("configs") or []:
            source = configs.get(item.get("source", ""), {}).get("file", "")
            if not source or not _inside(source, run_dir):
                found.append(
                    f"uses a config file outside the sandbox {item.get('source')}"
                )
        for env_file in service.get("env_file") or []:
            path = env_file.get("path") if isinstance(env_file, dict) else env_file
            if not _inside(str(path), run_dir):
                found.append(f"reads an env file outside the sandbox {path}")
        for network in service.get("networks") or {}:
            if (networks.get(network) or {}).get("external"):
                found.append(f"joins the external network {network}")
        found += _host_namespace(service)
        limits = service.get("deploy", {}).get("resources", {}).get("limits", {})
        memory = service.get("mem_limit") or limits.get("memory")
        if not memory:
            found.append("has no memory limit")
        else:
            total += int(memory)
        if found:
            problems[name] = found
    if len(selected) > MAX_SERVICES:
        problems["<selection>"] = [f"{len(selected)} services exceed {MAX_SERVICES}"]
    if total > MAX_MEMORY_BYTES:
        problems.setdefault("<selection>", []).append(
            f"{total} bytes of memory exceed {MAX_MEMORY_BYTES}"
        )
    return problems


def plan(files: list[Path], requested: list[str]) -> dict:
    config = render(files)
    selected = closure(config, requested)
    problems = assess(config, selected, state_dir() / "plan")
    return {
        "requested": sorted(requested),
        "services": selected,
        "problems": problems,
        "allowed": not problems,
    }


def _sandbox_host() -> str:
    socket = rootless_socket()
    if str(socket) in PRODUCTION_SOCKETS or not socket.is_socket():
        raise SandboxError(f"no rootless sandbox daemon at {socket}; run install")
    return f"unix://{socket}"


def _compose(host, project, files, *arguments, timeout=600):
    command = ["docker", "-H", host, "compose", "-p", project]
    for file in files:
        command += ["-f", str(file)]
    environment = {**os.environ, "DOCKER_HOST": host}
    return _run([*command, *arguments], timeout=timeout, cwd=ROOT, env=environment)


def up(files: list[Path], requested: list[str]) -> dict:
    host = _sandbox_host()
    run_id = uuid.uuid4().hex[:12]
    run_dir = state_dir() / run_id
    run_dir.mkdir(mode=0o700)
    config = render(files)
    selected = closure(config, requested)
    problems = assess(config, selected, run_dir)
    if problems:
        run_dir.rmdir()
        raise SandboxError(f"plan refused: {json.dumps(problems)}")
    networks = sorted(
        {
            network
            for name in selected
            for network in (config["services"][name].get("networks") or {})
        }
    )
    # Every network the closure uses is internal: no route out of the sandbox.
    override = run_dir / "override.json"
    override.write_text(
        json.dumps({"networks": {n: {"internal": True} for n in networks}})
    )
    record = {
        "run_id": run_id,
        "project": PROJECT_PREFIX + run_id,
        "host": host,
        "files": [str(f) for f in files],
        "services": selected,
    }
    (state_dir() / f"{run_id}.json").write_text(json.dumps(record, indent=2))
    started = _compose(
        host,
        record["project"],
        [*files, override],
        "--profile",
        "*",
        "up",
        "--detach",
        "--wait",
        "--no-build",
        *selected,
    )
    if started.returncode != 0:
        down(run_id)
        raise SandboxError(f"start failed and was cleaned up: {started.stderr[-300:]}")
    return record


def down(run_id: str) -> dict:
    """Remove one recorded project with its containers, networks and volumes."""
    path = state_dir() / f"{run_id}.json"
    if not path.exists():
        raise SandboxError(f"no recorded sandbox run {run_id}")
    record = json.loads(path.read_text())
    if not record["project"].startswith(PROJECT_PREFIX) or any(
        record["host"].endswith(socket) for socket in PRODUCTION_SOCKETS
    ):
        raise SandboxError("record does not name an owned sandbox project")
    files = [Path(f) for f in record["files"]]
    override = state_dir() / run_id / "override.json"
    if override.exists():
        files.append(override)
    result = _compose(
        record["host"],
        record["project"],
        files,
        "--profile",
        "*",
        "down",
        "--volumes",
        "--remove-orphans",
        "--timeout",
        "10",
    )
    if result.returncode != 0:
        raise SandboxError(f"cleanup failed: {result.stderr.strip()[-300:]}")
    shutil.rmtree(state_dir() / run_id, ignore_errors=True)
    path.unlink()
    return {"removed": record["project"]}


def cleanup() -> dict:
    """Remove recorded runs and report sandbox projects nobody recorded."""
    removed = [down(p.stem)["removed"] for p in sorted(state_dir().glob("*.json"))]
    unrecorded = []
    if rootless_socket().is_socket():
        listing = _run(
            [
                "docker",
                "-H",
                f"unix://{rootless_socket()}",
                "ps",
                "-a",
                "--format",
                '{{.Label "com.docker.compose.project"}}',
            ]
        )
        unrecorded = sorted(
            {p for p in listing.stdout.split() if p.startswith(PROJECT_PREFIX)}
        )
    return {"removed": removed, "unrecorded_projects": unrecorded}


def install(uninstall: bool = False) -> dict:
    """Install or remove the rootless daemon; refuses without uidmap."""
    if not doctor()["rootless_installable"]:
        raise SandboxError(
            "rootless Docker needs newuidmap and newgidmap (package uidmap)"
        )
    action = "uninstall" if uninstall else "install"
    result = _run(
        ["dockerd-rootless-setuptool.sh", action, "--skip-iptables"], timeout=300
    )
    if result.returncode != 0:
        raise SandboxError(f"setup tool failed: {result.stderr.strip()[-300:]}")
    return {"action": action, "rootless_ready": doctor()["rootless_ready"]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor")
    for name in ("plan", "up"):
        sub = commands.add_parser(name)
        sub.add_argument("services", nargs="*")
        sub.add_argument("-f", "--file", action="append", type=Path, default=[])
    commands.add_parser("down").add_argument("run_id")
    commands.add_parser("cleanup")
    commands.add_parser("install").add_argument("--uninstall", action="store_true")
    args = parser.parse_args(argv)
    files = [f.resolve() for f in getattr(args, "file", [])] or [
        ROOT / "docker-compose.yml"
    ]
    try:
        if args.command == "doctor":
            result = doctor()
        elif args.command == "plan":
            result = plan(files, args.services)
        elif args.command == "up":
            result = up(files, args.services)
        elif args.command == "down":
            result = down(args.run_id)
        elif args.command == "cleanup":
            result = cleanup()
        else:
            result = install(args.uninstall)
    except (SandboxError, subprocess.TimeoutExpired) as error:
        print(f"SANDBOX_REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result.get("allowed", True) else 3


if __name__ == "__main__":
    raise SystemExit(main())
