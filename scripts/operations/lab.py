#!/usr/bin/env python3
"""Run one standalone LAB (`labs/<name>.yml`) under a lease (SPEC-0215).

Commands:
  check LAB [LAB...]          refuse collisions, HOME data overlap, budget or
                              concurrency excess; print a JSON report
  up LAB --purpose --lease    check, record a ledger entry, start the project
  run LAB --purpose --lease --deadline [--grace]
                              start a job LAB, wait for its `hy-home.lab.job`
                              container, stop it at the deadline or on
                              SIGTERM, then stop the project
  down LAB                    stop only that project; never removes volumes
  reap                        stop every LAB whose lease has expired
  status                      print ledger entries and whether each runs

The ledger lives in `${LAB_DATA_DIR}/.ledger/<lab>.json` and names the exact
containers, networks and data paths an operator may later remove by hand.
Declared CPU and memory limits are ceilings, not measured usage.

Exit codes: 0 success, 1 Docker or Compose failure, 2 invalid input,
3 refused by a check.
"""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import json
import os
import pathlib
import re
import signal
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
LAB_PROJECT_PREFIX = "hy-home-lab-"
LEASE = re.compile(r"^([1-9][0-9]*)([mh])$")
SHARED_PUBLIC_INPUTS = frozenset(
    {
        os.path.realpath(ROOT / "infra/common-optimizations.yml"),
        # The tracked PostgreSQL provisioning entry point: HOME provision jobs
        # and the dbt/superset LAB provisioners mount the same file read-only.
        os.path.realpath(
            ROOT / "infra/04-data/mng-db/pg/provision/run-feature-provision.sh"
        ),
    }
)


# Compose build keys a LAB may use; see footprint.
BUILD_KEYS = frozenset(
    {"context", "dockerfile", "args", "target", "labels", "tags", "additional_contexts"}
)
# Tracked source trees HOME tools may read whole; see _path_conflict.
SOURCE_TREES = frozenset(os.path.realpath(ROOT / name) for name in ("infra", "labs"))


class LabError(Exception):
    def __init__(self, message: str, code: int = 2) -> None:
        super().__init__(message)
        self.code = code


def read_env(path: pathlib.Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^([A-Z][A-Z0-9_]*)=(.*)$", line.strip())
            if match:
                values[match[1]] = match[2].strip().strip('"').strip("'")
    return values | {k: v for k, v in os.environ.items() if k.startswith("LAB_")}


def run(command: list[str], **kwargs) -> subprocess.CompletedProcess:
    # No stdin: a Compose prompt (such as recreating a changed volume) must
    # fail the command instead of waiting forever.
    kwargs.setdefault("stdin", subprocess.DEVNULL)
    return subprocess.run(
        command, cwd=ROOT, text=True, capture_output=True, check=False, **kwargs
    )


def render(docker: str, env_file: pathlib.Path, compose_file: str | None) -> dict:
    command = [docker, "compose", "--env-file", str(env_file)]
    if compose_file:
        command += ["-f", compose_file]
    # --no-env-resolution keeps services[*].env_file (merged through extends
    # and include) instead of inlining it, so a LAB env_file can be refused.
    result = run(
        [
            *command,
            "--profile",
            "*",
            "config",
            "--no-env-resolution",
            "--format",
            "json",
        ]
    )
    if result.returncode != 0:
        raise LabError(
            f"render failed for {compose_file or 'root'}: {result.stderr.strip()}", 1
        )
    return json.loads(result.stdout)


def footprint(model: dict) -> dict:
    """Names, ports, writable state paths and declared limits of one model."""
    project = model.get("name", "")
    containers, ports, paths, state, inputs, written = (
        set(),
        set(),
        set(),
        set(),
        set(),
        set(),
    )
    sensitive_inputs, public_inputs = set(), set()
    sources = []
    cluster_ids = set()
    cpus = memory = 0.0
    for name, service in model.get("services", {}).items():
        replicas = int((service.get("deploy") or {}).get("replicas") or 1)
        if service.get("container_name"):
            containers.add(service["container_name"])
        else:
            containers |= {f"{project}-{name}-{i}" for i in range(1, replicas + 1)}
        for port in service.get("ports", []) or []:
            if port.get("published"):
                ports.add(f"{port.get('host_ip', '0.0.0.0')}:{port['published']}")
        for mount in service.get("volumes", []) or []:
            if mount.get("type") == "bind":
                # realpath: a symlinked root must not hide an overlap.
                declared = mount["source"]
                path = os.path.realpath(declared)
                read_only = bool(mount.get("read_only"))
                paths.add(path)
                if read_only:
                    inputs.add(path)
                    if _sensitive_input(path, mount.get("target")):
                        sensitive_inputs.add(path)
                    elif _public_file(path):
                        public_inputs.add(path)
                else:
                    state.add(path)
                sources.append(
                    {"declared": declared, "real": path, "read_only": read_only}
                )
            elif mount.get("type") == "volume":
                if not mount.get("read_only"):
                    written.add(mount.get("source"))
        # A KRaft cluster ID shared with HOME would let a LAB broker join or
        # confuse HOME metadata; every LAB needs its own.
        environment = service.get("environment") or {}
        if isinstance(environment, dict) and environment.get("CLUSTER_ID"):
            cluster_ids.add(str(environment["CLUSTER_ID"]))
        cpus += float(service.get("cpus") or 0) * replicas
        memory += int(service.get("mem_limit") or 0) * replicas
    devices = {}
    for key, volume in (model.get("volumes") or {}).items():
        device = (volume.get("driver_opts") or {}).get("device")
        if device:
            devices[volume.get("name") or f"{project}_{key}"] = device
            path = os.path.realpath(device)
            paths.add(path)
            # Read-only inputs (a scenario source) are never cleanup targets.
            if key in written:
                state.add(path)
                read_only = False
            else:
                inputs.add(path)
                read_only = True
                if _sensitive_input(path, None):
                    sensitive_inputs.add(path)
                elif _public_file(path):
                    public_inputs.add(path)
            sources.append({"declared": device, "real": path, "read_only": read_only})
    # Compose secret files are mounted without a bind entry; each is a
    # sensitive input of the model that declares it.
    for secret in (model.get("secrets") or {}).values():
        source = (secret or {}).get("file")
        if isinstance(source, str) and source:
            path = os.path.realpath(source)
            paths.add(path)
            inputs.add(path)
            sensitive_inputs.add(path)
            sources.append({"declared": source, "real": path, "read_only": True})
    # Compose config files reach the container like secrets, without a bind.
    for config in (model.get("configs") or {}).values():
        source = (config or {}).get("file")
        if isinstance(source, str) and source:
            path = os.path.realpath(source)
            paths.add(path)
            inputs.add(path)
            if _sensitive_input(path, None):
                sensitive_inputs.add(path)
            sources.append({"declared": source, "real": path, "read_only": True})
    # A build context is sent whole to the builder: it must meet the
    # read-only source rules. Build secrets and SSH forwarding are refused.
    build_inputs, build_forbidden = [], []
    for name, service in model.get("services", {}).items():
        if service.get("env_file"):
            build_forbidden.append(f"{name}: env_file")
        build = service.get("build")
        if not isinstance(build, dict):
            continue
        contexts = [
            build.get("context"),
            *(build.get("additional_contexts") or {}).values(),
        ]
        build_inputs += [
            os.path.realpath(item)
            for item in contexts
            if isinstance(item, str) and item
        ]
        # Allowlist of build keys: anything else (ssh, secrets, cache_to,
        # cache_from, network, entitlements, privileged, dockerfile_inline,
        # future keys) is refused.
        for key in sorted(set(build) - BUILD_KEYS):
            build_forbidden.append(f"{name}: build {key}")
        # The Dockerfile resolves against its context and must stay inside it.
        context = build.get("context")
        dockerfile = build.get("dockerfile")
        if isinstance(dockerfile, str) and dockerfile:
            base = os.path.realpath(context) if isinstance(context, str) else ""
            resolved = os.path.realpath(os.path.join(base, dockerfile))
            if not base or not _within(resolved, base):
                build_forbidden.append(f"{name}: build dockerfile outside the context")
    networks = {net.get("name") for net in (model.get("networks") or {}).values()}
    return {
        "build_inputs": build_inputs,
        "build_forbidden": build_forbidden,
        "project": project,
        "containers": containers,
        "ports": ports,
        "paths": paths,
        "state": state,
        "inputs": inputs,
        "sensitive_inputs": sensitive_inputs,
        "public_inputs": public_inputs,
        "sources": sources,
        "networks": networks - {None},
        "cluster_ids": cluster_ids,
        "volume_devices": devices,
        "cpus": cpus,
        "memory": memory,
    }


def _public_file(path: str) -> bool:
    """A regular file both sides may mount read-only: an allowlisted shared
    input, or any git-tracked, non-sensitive file in the repository."""
    if not pathlib.Path(path).is_file():
        return False
    if path in SHARED_PUBLIC_INPUTS:
        return True
    repo = os.path.realpath(ROOT)
    return (
        path.startswith(repo + os.sep)
        and not _sensitive_input(path, None)
        and _tracked_only(path)
    )


def _sensitive_input(source: str, target: object) -> bool:
    target_path = os.path.normpath(target) if isinstance(target, str) else ""
    source_path = pathlib.Path(source)
    lexical_secret = "secrets" in source_path.parts or (
        source_path.name == ".env"
        or (
            source_path.name.startswith(".env.")
            and not source_path.name.endswith(".example")
        )
    )
    protected_target = target_path == "/var/run/docker.sock" or (
        target_path == "/run/secrets" or target_path.startswith("/run/secrets/")
    )
    source_is_socket = source == "/var/run/docker.sock" or source_path.suffix == ".sock"
    return lexical_secret or protected_target or source_is_socket


def root_footprint(
    model: dict,
    env_file: pathlib.Path | str | None = None,
    docker_root: str | None = None,
) -> dict:
    """Root footprint bound to Compose's rendered DEFAULT_DATA_DIR marker.

    HOME's read-only / observers own no path, so every HOME asset no bind
    covers is recorded here: secret files, the root env file and Docker's
    data root are HOME state, and the first two are sensitive.
    """
    marker = model.get("x-hyhome-data-root")
    if not isinstance(marker, str) or not os.path.isabs(marker):
        raise LabError("root x-hyhome-data-root must be an absolute path")
    found = footprint(model)
    home_data_root = os.path.realpath(marker)
    found["home_data_root"] = home_data_root
    found["paths"].add(home_data_root)
    found["state"].add(home_data_root)
    for path in set(found["sensitive_inputs"]):
        found["state"].add(path)
    if env_file is not None:
        path = os.path.realpath(env_file)
        found["paths"].add(path)
        found["state"].add(path)
        found["sensitive_inputs"].add(path)
    found["docker_root"] = os.path.realpath(docker_root) if docker_root else None
    if docker_root:
        path = os.path.realpath(docker_root)
        found["paths"].add(path)
        found["state"].add(path)
    return found


@functools.cache
def _tracked_only(path: str) -> bool:
    """True when path is a tracked file, or a directory with tracked files
    and no untracked or ignored ones (which may hold local secrets)."""
    relative = os.path.relpath(path, os.path.realpath(ROOT))
    # Literal pathspecs: a name such as cfg[1] must not glob-match cfg1.
    tracked = run(["git", "--literal-pathspecs", "ls-files", "-z", "--", relative])
    others = run(  # untracked, including ignored
        ["git", "--literal-pathspecs", "ls-files", "-z", "--others", "--", relative]
    )
    # Local edits to a tracked file are not public (opensearch.yml is
    # tracked but meant to be edited locally).
    clean = run(
        ["git", "--literal-pathspecs", "diff", "--quiet", "HEAD", "--", relative]
    )
    return (
        tracked.returncode == 0
        and others.returncode == 0
        and clean.returncode == 0
        and bool(tracked.stdout)
        and not others.stdout
    )


def _nested(a: str, b: str) -> bool:
    try:
        return os.path.commonpath((a, b)) in {a, b}
    except ValueError:
        return False


def _port_clash(a: str, b: str) -> bool:
    host_a, port_a = a.rsplit(":", 1)
    host_b, port_b = b.rsplit(":", 1)
    wildcard = {"0.0.0.0", "::", ""}
    return port_a == port_b and bool(host_a == host_b or {host_a, host_b} & wildcard)


def _path_conflict(path: str, owner: dict, other_path: str, other: dict) -> bool:
    if not _nested(path, other_path):
        return False
    # A read-only bind of the host root (cadvisor, node-exporter) contains
    # every path but owns none; without this every LAB overlaps root. A LAB
    # binding / itself still meets root's own data paths.
    if (
        other_path == "/"
        and other_path in other["inputs"]
        and "/" not in other["state"]
    ):
        return False
    # A read-only, non-sensitive bind of a tracked source tree (conftest reads
    # infra/ and labs/) owns no LAB config inside it. Only a read-only,
    # non-sensitive LAB path strictly inside the tree qualifies (owner
    # decision 2026-11-05); writable, secret or whole-tree binds still clash.
    if (
        other_path in SOURCE_TREES
        and path.startswith(other_path + os.sep)
        and other_path in other["inputs"]
        and other_path not in other["state"]
        and other_path not in other["sensitive_inputs"]
        and path in owner["inputs"]
        and path not in owner["state"]
        and path not in owner["sensitive_inputs"]
        and _tracked_only(path)
    ):
        return False
    shared_public_input = (
        path == other_path
        and path in owner["inputs"]
        and other_path in other["inputs"]
        and path in owner["public_inputs"]
        and other_path in other["public_inputs"]
        and path not in owner["state"]
        and other_path not in other["state"]
        and path not in owner["sensitive_inputs"]
        and other_path not in other["sensitive_inputs"]
    )
    return not shared_public_input


def collisions(selected: dict[str, dict], root: dict, running: list[dict]) -> list[str]:
    """Every name, port or state path a selected LAB would share."""
    problems: list[str] = []
    others = [("root", root)] + [(f"lab {n}", f) for n, f in selected.items()]
    for name, lab in selected.items():
        for other_name, other in others:
            if other is lab:
                continue
            for key in ("containers", "networks", "cluster_ids"):
                for clash in sorted(lab[key] & other[key]):
                    problems.append(f"{name}: {key[:-1]} {clash} also in {other_name}")
            for port in sorted(lab["ports"]):
                if any(_port_clash(port, p) for p in other["ports"]):
                    problems.append(f"{name}: host port {port} also in {other_name}")
            for path in sorted(lab["paths"]):
                conflicts = [
                    p for p in other["paths"] if _path_conflict(path, lab, p, other)
                ]
                if conflicts:
                    if (
                        path in lab["sensitive_inputs"]
                        and path in conflicts
                        and path in other["sensitive_inputs"]
                    ):
                        problems.append(
                            f"{name}: sensitive read-only path {path} also in "
                            f"{other_name}"
                        )
                    else:
                        problems.append(
                            f"{name}: data path {path} overlaps {other_name}"
                        )
        for container in running:
            if container["project"] == lab["project"]:
                continue
            if container["name"] in lab["containers"]:
                problems.append(f"{name}: container {container['name']} already exists")
            if container.get("running", True):
                for port in sorted(lab["ports"]):
                    if any(_port_clash(port, p) for p in container["ports"]):
                        problems.append(
                            f"{name}: host port {port} held by {container['name']}"
                        )
    return problems


def budget(
    selected: dict[str, dict], running: list[dict], env: dict[str, str]
) -> list[str]:
    try:
        cpu_budget = float(env["LAB_HOST_BUDGET_CPUS"])
        memory_budget = float(env["LAB_HOST_BUDGET_MEMORY_MIB"]) * 2**20
        max_labs = int(env.get("LAB_MAX_CONCURRENT") or 1)
    except (KeyError, ValueError) as exc:
        raise LabError(f"set a numeric LAB host budget: {exc}") from exc
    projects = {lab["project"] for lab in selected.values()}
    kept = [
        c for c in running if c["project"] not in projects and c.get("running", True)
    ]
    cpus = sum(c["cpus"] for c in kept) + sum(x["cpus"] for x in selected.values())
    memory = sum(c["memory"] for c in kept) + sum(
        x["memory"] for x in selected.values()
    )
    labs = {c["project"] for c in kept if c["project"].startswith(LAB_PROJECT_PREFIX)}
    problems = []
    if cpus > cpu_budget:
        problems.append(f"declared CPUs {cpus:g} exceed budget {cpu_budget:g}")
    if memory > memory_budget:
        problems.append(
            f"declared memory {memory / 2**20:.0f} MiB exceeds budget "
            f"{memory_budget / 2**20:.0f} MiB"
        )
    if len(labs | projects) > max_labs:
        problems.append(f"{len(labs | projects)} LABs would run; limit is {max_labs}")
    return problems


def running_containers(docker: str) -> list[dict]:
    listed = run([docker, "ps", "--all", "--quiet"])
    if listed.returncode != 0:
        raise LabError(f"docker ps failed: {listed.stderr.strip()}", 1)
    ids = listed.stdout.split()
    if not ids:
        return []
    inspected = run([docker, "inspect", *ids])
    if inspected.returncode != 0:
        raise LabError(f"docker inspect failed: {inspected.stderr.strip()}", 1)
    containers = []
    for item in json.loads(inspected.stdout):
        host = item.get("HostConfig") or {}
        labels = (item.get("Config") or {}).get("Labels") or {}
        ports = {
            f"{binding.get('HostIp') or '0.0.0.0'}:{binding['HostPort']}"
            for bindings in (host.get("PortBindings") or {}).values()
            for binding in bindings or []
            if binding.get("HostPort")
        }
        containers.append(
            {
                "name": item["Name"].lstrip("/"),
                "project": labels.get("com.docker.compose.project", ""),
                "ports": ports,
                "cpus": (host.get("NanoCpus") or 0) / 1e9,
                "memory": host.get("Memory") or 0,
                "running": (item.get("State") or {}).get("Running") is True,
            }
        )
    return containers


def _has_symlink_component(path: pathlib.Path) -> bool:
    return any(candidate.is_symlink() for candidate in (path, *path.parents))


def path_integrity_problems(selected: dict[str, dict]) -> list[str]:
    """Refuse missing or symlinked immutable inputs without touching state."""
    problems = []
    for name, lab in selected.items():
        for source in lab["sources"]:
            if not source["read_only"]:
                continue
            declared = pathlib.Path(source["declared"])
            if not declared.is_absolute():
                problems.append(f"{name}: read-only source must be absolute")
                continue
            if not os.path.lexists(declared):
                problems.append(f"{name}: read-only source does not exist")
                continue
            if _has_symlink_component(declared):
                problems.append(f"{name}: read-only source contains a symlink")
            if not declared.exists():
                problems.append(f"{name}: read-only source target does not exist")
    return problems


def _within(path: str, root: str) -> bool:
    return path == root or path.startswith(root.rstrip(os.sep) + os.sep)


def _covers(root: str, path: str) -> bool:
    return _within(path, root)


def source_allowlist_problems(
    selected: dict[str, dict], env: dict[str, str], root: dict | None = None
) -> list[str]:
    """Owner decisions 2026-11-05: a LAB may only use its own data, read-only
    LAB secret copies, read-only operator LAB_* inputs, writable
    LAB_*_RESULT_DIR outputs and read-only, non-sensitive, clean git-tracked
    repo paths. No root may cover the repo, its secrets, HOME data, Docker's
    root or the user home, and operator roots may not lie inside the repo.
    Overlap with HOME is checked separately."""
    repo = os.path.realpath(ROOT)
    root = root or {}
    protected = {
        repo,
        os.path.realpath(ROOT / "secrets"),
        os.path.realpath(pathlib.Path.home()),
        *(
            item
            for item in (root.get("home_data_root"), root.get("docker_root"))
            if item
        ),
    }
    problems = []

    def unsafe(path: str) -> bool:
        return any(_covers(path, item) for item in protected)

    data_value = env.get("LAB_DATA_DIR")
    data = os.path.realpath(data_value) if data_value else None
    if data and (unsafe(data) or _within(data, repo)):
        problems.append(f"LAB_DATA_DIR {data} covers or sits in a protected path")
        data = None
    secret_value = env.get("LAB_SECRET_DIR") or "../secrets/labs"
    # Compose resolves a relative LAB_SECRET_DIR against labs/.
    secret = os.path.realpath(ROOT / "labs" / secret_value)
    if unsafe(secret) or (
        _within(secret, repo)
        and not _within(secret, os.path.realpath(ROOT / "secrets" / "labs"))
    ):
        # Inside the repo only secrets/labs holds LAB copies; elsewhere would
        # admit HOME secret subdirectories or .git.
        problems.append(f"LAB_SECRET_DIR {secret} is not a LAB secret location")
        secret = None

    def operator_roots(results: bool) -> set[str]:
        found = set()
        for key, value in env.items():
            if (
                not key.startswith("LAB_")
                or key in {"LAB_DATA_DIR", "LAB_SECRET_DIR"}
                or not os.path.isabs(value)
                or key.endswith("_RESULT_DIR") is not results
            ):
                continue
            path = os.path.realpath(value)
            # An unsafe or sensitive root (the Docker socket) admits nothing.
            if unsafe(path) or _within(path, repo) or _sensitive_input(path, None):
                continue
            found.add(path)
        return found

    operator, results = operator_roots(False), operator_roots(True)

    def allowed(real: str, read_only: bool) -> bool:
        if _sensitive_input(real, None):
            # Secrets and sockets only from the LAB secret copies.
            return bool(read_only and secret and _within(real, secret))
        if data and _within(real, data):
            return True
        if read_only and secret and _within(real, secret):
            return True
        if read_only and any(_within(real, item) for item in operator | results):
            return True
        if any(_within(real, item) for item in results):
            return True
        return (
            read_only
            and _within(real, repo)
            and real != repo
            and not _sensitive_input(real, None)
            and _tracked_only(real)
        )

    for name, lab in selected.items():
        for source in lab["sources"]:
            if not allowed(source["real"], source["read_only"]):
                problems.append(
                    f"{name}: source {source['real']} is outside the LAB allowlist"
                )
        for context in lab.get("build_inputs", []):
            if not allowed(context, True):
                problems.append(
                    f"{name}: build context {context} is outside the LAB allowlist"
                )
        problems += [
            f"{name}: {item} is refused" for item in lab.get("build_forbidden", [])
        ]
    return problems


def include_problems(name: str, path: pathlib.Path | str) -> list[str]:
    """A top-level include may carry its own env_file, which the rendered
    model resolves and drops, so a LAB file may not include anything."""
    try:
        import yaml
    except ImportError as exc:  # fail closed without a parser
        raise LabError("PyYAML is required to check LAB includes") from exc
    loaded = yaml.safe_load(pathlib.Path(path).read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        return [f"{name}: LAB file is not a Compose mapping"]
    return [f"{name}: include is refused in a LAB"] if "include" in loaded else []


def data_root_problems(env: dict[str, str], root: dict) -> list[str]:
    data = env.get("LAB_DATA_DIR")
    if not data or not os.path.isabs(data):
        raise LabError("LAB_DATA_DIR must be an absolute path")
    lab_data_root = os.path.realpath(data)
    if _nested(lab_data_root, root["home_data_root"]):
        return ["LAB_DATA_DIR overlaps the rendered DEFAULT_DATA_DIR"]
    return []


def lab_file(name: str) -> str:
    if (
        not re.fullmatch(r"[a-z0-9-]+", name)
        or not (ROOT / f"labs/{name}.yml").is_file()
    ):
        raise LabError(f"unknown LAB {name!r}")
    return f"labs/{name}.yml"


def ledger_dir(env: dict[str, str]) -> pathlib.Path:
    data = env.get("LAB_DATA_DIR")
    if not data or not os.path.isabs(data):
        raise LabError("LAB_DATA_DIR must be an absolute path")
    return pathlib.Path(data) / ".ledger"


def stale_volumes(docker: str, selected: dict[str, dict]) -> list[str]:
    """A kept volume record that points at another data root.

    `down` keeps volumes, so after `LAB_DATA_DIR` changes Compose would ask
    whether to recreate the record; the operator removes it on purpose.
    """
    problems = []
    for name, lab in selected.items():
        for volume, device in sorted(lab.get("volume_devices", {}).items()):
            found = run(
                [docker, "volume", "inspect", "--format", "{{json .Options}}", volume]
            )
            if found.returncode != 0:
                continue
            options = json.loads(found.stdout or "{}") or {}
            if options.get("device") not in (None, device):
                problems.append(
                    f"{name}: volume {volume} points at {options['device']}, not "
                    f"{device}; remove the record with `docker volume rm {volume}` "
                    "(bind data stays on disk)"
                )
    return problems


def docker_root(docker: str) -> str:
    result = run([docker, "info", "--format", "{{.DockerRootDir}}"])
    root = result.stdout.strip()
    if result.returncode != 0 or not os.path.isabs(root):
        raise LabError("Docker data root unavailable; refusing without it")
    return root


def check(args, env) -> tuple[dict, dict[str, dict]]:
    selected = {
        name: footprint(render(args.docker, args.env_file, lab_file(name)))
        for name in args.labs
    }
    root = root_footprint(
        render(args.docker, args.root_env_file, None),
        env_file=args.root_env_file,
        docker_root=docker_root(args.docker),
    )
    running = running_containers(args.docker)
    report = {
        "labs": {
            name: {
                "project": lab["project"],
                "declared_cpus": lab["cpus"],
                "declared_memory_mib": round(lab["memory"] / 2**20),
            }
            for name, lab in selected.items()
        },
        # Unlimited containers cannot be summed; they are listed, not counted.
        "running_without_limits": sorted(
            c["name"]
            for c in running
            if c["running"] and (not c["cpus"] or not c["memory"])
        ),
        "problems": data_root_problems(env, root)
        + path_integrity_problems(selected)
        + source_allowlist_problems(selected, env, root)
        + [
            item
            for name in selected
            for item in include_problems(name, ROOT / lab_file(name))
        ]
        + collisions(selected, root, running)
        + budget(selected, running, env)
        + stale_volumes(args.docker, selected),
    }
    return report, selected


def compose_command(args, name: str, project: str) -> list[str]:
    return [
        args.docker, "compose", "-p", project, "--env-file", str(args.env_file),
        "-f", lab_file(name), "--profile", "*",
    ]  # fmt: skip


def wait_ready(docker: str, project: str, timeout: int) -> str | None:
    """None once every container is healthy, running without a health check,
    or a one-shot job (restart `no`) that exited 0; otherwise the first
    reason it is not. A one-shot job that still runs is not ready yet.

    `compose up --wait` treats an init job that exits 0 as a failure, so the
    LAB controller judges readiness itself.
    """
    deadline = time.monotonic() + timeout
    while True:
        listed = run(
            [docker, "ps", "--all", "--quiet",
             "--filter", f"label=com.docker.compose.project={project}"]
        )  # fmt: skip
        ids = listed.stdout.split()
        inspected = run([docker, "inspect", *ids]) if ids else None
        records = json.loads(inspected.stdout) if inspected and inspected.stdout else []
        pending = []
        for record in records:
            state = record.get("State") or {}
            name = str(record.get("Name", "")).lstrip("/")
            health = (state.get("Health") or {}).get("Status")
            restart = ((record.get("HostConfig") or {}).get("RestartPolicy") or {}).get(
                "Name"
            )
            if state.get("Status") == "exited":
                if state.get("ExitCode") != 0:
                    return f"{name} exited {state.get('ExitCode')}"
            elif health == "unhealthy":
                return f"{name} is unhealthy"
            elif (
                state.get("Status") != "running"
                or health == "starting"
                or restart == "no"
            ):
                pending.append(name)
        if records and not pending:
            return None
        if time.monotonic() >= deadline:
            return "not ready: " + (", ".join(sorted(pending)[:5]) or "no containers")
        time.sleep(2)


def write_entry(path: pathlib.Path, entry: dict) -> None:
    path.write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")


def cmd_up(args, env, *, wait: bool = True) -> int:
    match = LEASE.fullmatch(args.lease)
    if not match or not args.purpose.strip():
        raise LabError("give --purpose and a --lease such as 30m or 4h")
    minutes = int(match[1]) * (60 if match[2] == "h" else 1)
    if minutes > int(env.get("LAB_MAX_LEASE_MINUTES") or 1440):
        raise LabError("lease exceeds LAB_MAX_LEASE_MINUTES")
    ledger = ledger_dir(env)
    args.labs = [args.lab]
    report, selected = check(args, env)
    if report["problems"]:
        print(json.dumps(report, indent=2))
        return 3
    lab = selected[args.lab]
    data_root = pathlib.Path(os.path.realpath(ledger.parent))
    for path in lab["state"]:
        if pathlib.Path(path).is_relative_to(data_root):
            state_dir = pathlib.Path(path)
            if not state_dir.exists():
                state_dir.mkdir(parents=True)
                # Group-writable whatever the umask: LAB processes run as their
                # image user with the operator's group (SECRETS_GID).
                state_dir.chmod(0o770)
    now = dt.datetime.now(dt.UTC)
    entry = {
        "lab": args.lab,
        "project": lab["project"],
        "compose_file": lab_file(args.lab),
        "purpose": args.purpose.strip(),
        "started_at": now.isoformat(),
        "expires_at": (now + dt.timedelta(minutes=minutes)).isoformat(),
        "state": "starting",
        "cleanup": {
            "containers": sorted(lab["containers"]),
            "networks": sorted(lab["networks"]),
            "paths": sorted(lab["state"]),
        },
    }
    ledger.mkdir(parents=True, exist_ok=True)
    target = ledger / f"{args.lab}.json"
    write_entry(target, entry)
    command = [*compose_command(args, args.lab, lab["project"]), "up", "-d"]
    result = run(command)
    reason = result.stderr.strip() if result.returncode != 0 else None
    # A job LAB may finish before it reports healthy, so `run` does not wait.
    if reason is None and wait:
        timeout = int(env.get("LAB_READY_TIMEOUT_SECONDS") or 600)
        reason = wait_ready(args.docker, lab["project"], timeout)
    entry["state"] = "running" if reason is None else "failed"
    write_entry(target, entry)
    print(json.dumps({k: entry[k] for k in ("lab", "state", "expires_at")}))
    if reason is not None:
        print(reason, file=sys.stderr)
        return 1
    return 0


def stop(args, env, name: str) -> int:
    target = ledger_dir(env) / f"{name}.json"
    if not target.is_file():
        raise LabError(f"no ledger entry for {name}; it was not started by lab.py")
    entry = json.loads(target.read_text(encoding="utf-8"))
    if not str(entry.get("project", "")).startswith(LAB_PROJECT_PREFIX):
        raise LabError(f"ledger for {name} names a non-LAB project")
    # By project label only (no render, so lost inputs cannot block a stop),
    # and no -v: data and volumes stay for review.
    command = [args.docker, "compose", "-p", entry["project"], "down"]
    command += ["--timeout", "30"]
    result = run(command)
    entry["state"] = "stopped" if result.returncode == 0 else "stop-failed"
    entry["stopped_at"] = dt.datetime.now(dt.UTC).isoformat()
    write_entry(target, entry)
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        return 1
    return 0


def _cancel(signum, frame) -> None:
    raise KeyboardInterrupt


def supervise(docker: str, project: str, deadline: int, grace: int) -> tuple[str, int]:
    """Wait for the project's one job container; stop it at the deadline.

    A deadline or SIGTERM/SIGINT stops the job with SIGTERM and `grace`
    seconds, so a tool such as Locust can flush its result files, before the
    caller removes the project. Returns the outcome and the controller code:
    the job's own exit code, 124 for the deadline or 130 for a cancel.
    """
    listed = run(
        [docker, "ps", "--all", "--quiet",
         "--filter", f"label=com.docker.compose.project={project}",
         "--filter", "label=hy-home.lab.job=true"]
    )  # fmt: skip
    jobs = listed.stdout.split()
    if listed.returncode != 0 or len(jobs) != 1:
        raise LabError(f"{project} has no single job container", 1)
    previous = signal.signal(signal.SIGTERM, _cancel)
    try:
        try:
            waited = run([docker, "wait", jobs[0]], timeout=deadline)
            if waited.returncode != 0 or not waited.stdout.strip().isdigit():
                raise LabError("docker wait failed", 1)
            code = int(waited.stdout)
            return ("completed" if code == 0 else "failed"), code
        except subprocess.TimeoutExpired:
            outcome, code = "deadline_exceeded", 124
        except KeyboardInterrupt:
            outcome, code = "cancelled", 130
        try:
            run([docker, "stop", "--time", str(grace), jobs[0]], timeout=grace + 30)
        except subprocess.TimeoutExpired:
            pass  # the caller's `down` still removes the project
        return outcome, code
    finally:
        signal.signal(signal.SIGTERM, previous)


def cmd_run(args, env) -> int:
    """Start a job LAB, bound it by a deadline inside its lease, then stop it."""
    lease, deadline = LEASE.fullmatch(args.lease), LEASE.fullmatch(args.deadline)
    if not lease or not deadline:
        raise LabError("give --lease and --deadline such as 30m")
    seconds = {"m": 60, "h": 3600}
    deadline_seconds = int(deadline[1]) * seconds[deadline[2]]
    if deadline_seconds > int(lease[1]) * seconds[lease[2]] or args.grace < 1:
        raise LabError("the deadline must fit inside the lease")
    target = ledger_dir(env) / f"{args.lab}.json"
    before = target.stat().st_mtime_ns if target.exists() else None
    outcome, code = "failed", 1
    # Installed before anything starts, so a SIGTERM during `up` still stops
    # the project below instead of leaving it unsupervised.
    previous = signal.signal(signal.SIGTERM, _cancel)
    try:
        code = cmd_up(args, env, wait=False)
        if code == 0:
            entry = json.loads(target.read_text(encoding="utf-8"))
            outcome, code = supervise(
                args.docker, entry["project"], deadline_seconds, args.grace
            )
        else:
            outcome = "start_failed"
    except KeyboardInterrupt:
        outcome, code = "cancelled", 130
    finally:
        signal.signal(signal.SIGTERM, previous)
        # Stop only a project this call recorded; a refused start writes none.
        started = target.exists() and target.stat().st_mtime_ns != before
        stopped = stop(args, env, args.lab) if started else 0
        if started:
            entry = json.loads(target.read_text(encoding="utf-8"))
            entry.update(
                outcome=outcome, job_exit_code=code, deadline_seconds=deadline_seconds
            )
            write_entry(target, entry)
            print(
                json.dumps(
                    {k: entry[k] for k in ("lab", "state", "outcome", "job_exit_code")}
                )
            )
    return code or stopped


def entries(env) -> list[dict]:
    directory = ledger_dir(env)
    if not directory.is_dir():
        return []
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(directory.glob("*.json"))
    ]


def cmd_reap(args, env) -> int:
    now = dt.datetime.now(dt.UTC)
    code = 0
    for entry in entries(env):
        expired = dt.datetime.fromisoformat(entry["expires_at"]) <= now
        if expired and entry["state"] in {
            "starting",
            "running",
            "failed",
            "stop-failed",
        }:
            code = max(code, stop(args, env, entry["lab"]))
    return code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--docker", default="docker")
    parser.add_argument("--env-file", type=pathlib.Path, default=ROOT / "labs/.env")
    parser.add_argument("--root-env-file", type=pathlib.Path, default=ROOT / ".env")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check").add_argument("labs", nargs="+")
    up = commands.add_parser("up")
    up.add_argument("lab")
    up.add_argument("--purpose", required=True)
    up.add_argument("--lease", required=True)
    job = commands.add_parser("run")
    job.add_argument("lab")
    job.add_argument("--purpose", required=True)
    job.add_argument("--lease", required=True)
    job.add_argument("--deadline", required=True)
    job.add_argument("--grace", type=int, default=30)
    commands.add_parser("down").add_argument("lab")
    commands.add_parser("reap")
    commands.add_parser("status")
    args = parser.parse_args(argv)
    env = read_env(args.env_file)
    try:
        if args.command == "check":
            report, _ = check(args, env)
            print(json.dumps(report, indent=2))
            return 3 if report["problems"] else 0
        if args.command == "up":
            return cmd_up(args, env)
        if args.command == "run":
            return cmd_run(args, env)
        if args.command == "down":
            return stop(args, env, args.lab)
        if args.command == "reap":
            return cmd_reap(args, env)
        projects = {
            c["project"] for c in running_containers(args.docker) if c["running"]
        }
        for entry in entries(env):
            entry["project_running"] = entry["project"] in projects
            print(json.dumps(entry))
        return 0
    except LabError as exc:
        print(f"lab.py: {exc}", file=sys.stderr)
        return exc.code
    except (KeyError, TypeError, ValueError) as exc:
        # Bad env values or a hand-edited ledger are invalid input, not a crash.
        print(f"lab.py: invalid input: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
