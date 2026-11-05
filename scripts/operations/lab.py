#!/usr/bin/env python3
"""Run one standalone LAB (`labs/<name>/docker-compose.yml`) under a lease (SPEC-0215).

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
  readiness LAB [--report PATH]
                              read-only promotion readiness report
                              (SPEC-0263); exit 0 only when every
                              criterion is PASS

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
import shutil
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
SECRETS_TREE = os.path.realpath(ROOT / "secrets")
LAB_SECRETS_TREE = os.path.realpath(ROOT / "secrets" / "labs")


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
    limits, users = {}, {}
    # Per-service identities, so a replacement can retire exactly its own
    # services' containers, ports and folders (readiness).
    by_service: dict[str, dict[str, set]] = {}
    for name, service in model.get("services", {}).items():
        replicas = int((service.get("deploy") or {}).get("replicas") or 1)
        own = by_service[name] = {"containers": set(), "ports": set(), "dirs": set()}
        if service.get("container_name"):
            own["containers"].add(service["container_name"])
        else:
            own["containers"] |= {
                f"{project}-{name}-{i}" for i in range(1, replicas + 1)
            }
        containers |= own["containers"]
        for port in service.get("ports", []) or []:
            if port.get("published"):
                own["ports"].add(
                    f"{port.get('host_ip', '0.0.0.0')}:{port['published']}"
                )
        ports |= own["ports"]
        build = service.get("build")
        if isinstance(build, dict) and isinstance(build.get("context"), str):
            own["dirs"].add(os.path.realpath(build["context"]))
        for mount in service.get("volumes", []) or []:
            if mount.get("type") == "bind":
                # realpath: a symlinked root must not hide an overlap.
                declared = mount["source"]
                path = os.path.realpath(declared)
                own["dirs"].add(path)
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
                    {
                        "declared": declared,
                        "real": path,
                        "read_only": read_only,
                        "service": name,
                        "target": mount.get("target"),
                    }
                )
            elif mount.get("type") == "volume":
                if not mount.get("read_only"):
                    written.add(mount.get("source"))
        # A KRaft cluster ID shared with HOME would let a LAB broker join or
        # confuse HOME metadata; every LAB needs its own.
        environment = service.get("environment") or {}
        if isinstance(environment, dict) and environment.get("CLUSTER_ID"):
            cluster_ids.add(str(environment["CLUSTER_ID"]))
        # Per-container limits as declared; the totals count replicas.
        limits[name] = {
            "cpus": float(service.get("cpus") or 0),
            "memory": float(int(service.get("mem_limit") or 0)),
        }
        cpus += limits[name]["cpus"] * replicas
        users[name] = service.get("user")
        memory += limits[name]["memory"] * replicas
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
    # Compose defaults: bridge for a network, local for a volume.
    drivers = {
        (item or {}).get("driver") or default
        for key, default in (("networks", "bridge"), ("volumes", "local"))
        for item in (model.get(key) or {}).values()
    }
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
        "services": limits,
        "users": users,
        "drivers": drivers,
        "by_service": by_service,
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
    # Writable binds only, before sensitive inputs are promoted to state.
    found["bound_state"] = set(found["state"])
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


def _path_conflict(
    path: str,
    owner: dict,
    other_path: str,
    other: dict,
    owner_name: str | None = None,
) -> bool:
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
    # restic backs up the repo's secrets/ through a read-only bind; it owns
    # none of the owner LAB's read-only copies under secrets/labs/<owner>/.
    # A writable bind of secrets/, a HOME secret, another LAB's copy, the
    # whole LAB tree or a writable LAB bind still clashes.
    if (
        owner_name
        and other_path == SECRETS_TREE
        and other_path in other["inputs"]
        and other_path not in other.get("bound_state", other["state"])
        and path.startswith(os.path.join(LAB_SECRETS_TREE, owner_name) + os.sep)
        and path in owner["inputs"]
        and path not in owner["state"]
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
        # The allowed Docker socket is shared with HOME by design; a path that
        # also arrives through any other source keeps its treatment.
        sources = lab.get("sources", [])
        shared_socket = {s["real"] for s in sources if _socket_exception(name, s)} - {
            s["real"] for s in sources if not _socket_exception(name, s)
        }
        for other_name, other in others:
            if other is lab:
                continue
            for key in ("containers", "networks", "cluster_ids"):
                for clash in sorted(lab[key] & other[key]):
                    problems.append(f"{name}: {key[:-1]} {clash} also in {other_name}")
            for port in sorted(lab["ports"]):
                if any(_port_clash(port, p) for p in other["ports"]):
                    problems.append(f"{name}: host port {port} also in {other_name}")
            for path in sorted(lab["paths"] - shared_socket):
                conflicts = [
                    p
                    for p in other["paths"]
                    if _path_conflict(path, lab, p, other, owner_name=name)
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
            # /var/run is a symlink to /run on most hosts.
            if _has_symlink_component(declared) and not _socket_exception(name, source):
                problems.append(f"{name}: read-only source contains a symlink")
            if not declared.exists():
                problems.append(f"{name}: read-only source target does not exist")
    return problems


def _within(path: str, root: str) -> bool:
    return path == root or path.startswith(root.rstrip(os.sep) + os.sep)


def _covers(root: str, path: str) -> bool:
    return _within(path, root)


def _socket_exception(name: str, source: dict) -> bool:
    """SPEC-0263 section 3: supabase `vector` alone may bind the Docker socket,
    read-only, for log collection. Decided on the declared path, since
    /var/run is a symlink to /run on most hosts."""
    return (
        name == "supabase"
        and source.get("service") == "vector"
        and source["declared"] == "/var/run/docker.sock"
        and source.get("target") == "/var/run/docker.sock"
        and source["read_only"] is True
    )


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
    secret_value = env.get("LAB_SECRET_DIR") or "../../secrets/labs"
    # Compose resolves a relative LAB_SECRET_DIR against the LAB folder
    # labs/<name>/; every LAB folder sits at that one depth (SPEC-0263).
    secret = os.path.realpath(ROOT / "labs" / "lab" / secret_value)
    # Decided from the resolved secrets tree too: a symlinked secrets/ must
    # not let a sibling of secrets/labs pass as outside the repo.
    secrets_root = os.path.realpath(ROOT / "secrets")
    if unsafe(secret) or (
        (_within(secret, repo) or _within(secret, secrets_root))
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

    def allowed(real: str, read_only: bool, name: str) -> bool:
        # Each LAB reads only its own copies, <LAB_SECRET_DIR>/<name>/.
        own = os.path.join(secret, name) if secret else None
        if _sensitive_input(real, None):
            # Secrets and sockets only from this LAB's secret copies.
            return bool(read_only and own and _within(real, own))
        if data and _within(real, data):
            return True
        if read_only and own and _within(real, own):
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
            if _socket_exception(name, source):
                continue
            if not allowed(source["real"], source["read_only"], name):
                problems.append(
                    f"{name}: source {source['real']} is outside the LAB allowlist"
                )
        for context in lab.get("build_inputs", []):
            if not allowed(context, True, name):
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
    """SPEC-0263 section 1: a LAB is the folder `labs/<name>/`."""
    if re.fullmatch(r"[a-z0-9-]+", name):
        if (ROOT / f"labs/{name}/docker-compose.yml").is_file():
            return f"labs/{name}/docker-compose.yml"
        if (ROOT / f"labs/{name}.yml").is_file():
            raise LabError(
                f"{name}: flat labs/{name}.yml is retired; "
                f"use labs/{name}/docker-compose.yml"
            )
    raise LabError(f"unknown LAB {name!r}")


MANIFEST_KINDS = frozenset({"add", "replace-same", "replace-substitute", "undecided"})
REPLACEMENT_KINDS = frozenset({"replace-same", "replace-substitute"})
INTEGRATION_KINDS = frozenset(
    {
        "gateway-route",
        "oidc-client",
        "database-role",
        "observability",
        "openbao",
        "network",
    }
)
TARGET_FOLDER = re.compile(r"^infra/\d\d-[a-z0-9-]+/.+/$")
SECRET_CATALOG = "infra/03-security/openbao/secret-catalog.json"
MIB_BYTES = 2**20


def _repo_path(value: object) -> pathlib.Path | None:
    """A manifest path: repo-relative, no `..`, and resolving inside ROOT."""
    if not isinstance(value, str) or not value or os.path.isabs(value):
        return None
    if ".." in pathlib.PurePosixPath(value).parts:
        return None
    path = ROOT / value
    root = os.path.realpath(ROOT)
    return path if _within(os.path.realpath(path), root) else None


def load_manifest(name: str) -> dict:
    import yaml

    path = ROOT / f"labs/{name}/promotion.yaml"
    if not path.is_file():
        raise LabError(f"{name}: no promotion manifest labs/{name}/promotion.yaml")
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise LabError(f"{name}: promotion manifest is not a mapping")
    return loaded


def catalog_ids() -> set[str]:
    try:
        catalog = json.loads((ROOT / SECRET_CATALOG).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise LabError(f"secret catalog {SECRET_CATALOG} is unreadable: {exc}") from exc
    try:
        return {entry["id"] for entry in catalog.get("entries", [])}
    except (AttributeError, KeyError, TypeError) as exc:
        raise LabError(f"secret catalog {SECRET_CATALOG} is malformed: {exc}") from exc


def manifest_problems(
    name: str, manifest: dict, lab: dict, catalog_ids: set[str]
) -> list[str]:
    """SPEC-0263 section 2: a manifest consistent with its rendered LAB."""
    problems = []
    kind = manifest.get("kind")
    if kind not in MANIFEST_KINDS:
        problems.append(f"{name}: unknown kind {kind!r}")
    target = manifest.get("target")
    if kind == "undecided" and "target" in manifest:
        problems.append(f"{name}: target is not allowed on kind undecided")
    elif kind in MANIFEST_KINDS - {"undecided"} and not isinstance(target, dict):
        problems.append(f"{name}: target is required for kind {kind}")
    if isinstance(target, dict):
        folder = target.get("folder")
        if (
            not isinstance(folder, str)
            or not TARGET_FOLDER.fullmatch(folder)
            or ".." in folder.split("/")
        ):
            problems.append(
                f"{name}: target folder {folder!r} is outside infra/<tier>/"
            )
    if kind in REPLACEMENT_KINDS and not manifest.get("replaces"):
        problems.append(f"{name}: kind {kind} needs a non-empty replaces")
    for item in manifest.get("integrations") or []:
        integration = item.get("kind") if isinstance(item, dict) else item
        if integration not in INTEGRATION_KINDS:
            problems.append(f"{name}: unknown integration kind {integration!r}")
    for item in manifest.get("secrets") or []:
        row = item.get("row") if isinstance(item, dict) else item
        if row not in catalog_ids:
            problems.append(f"{name}: secret row {row!r} has no catalog row")
    declared = (manifest.get("resources") or {}).get("services") or {}
    rendered = lab["services"]
    for service in sorted(set(declared) | set(rendered)):
        want, have = declared.get(service), rendered.get(service)
        if isinstance(want, dict) and (
            not want.get("cpus") or not want.get("memory_mib")
        ):
            problems.append(
                f"{name}: resources.services {service} has no cpus or memory"
            )
        if (
            not isinstance(want, dict)
            or have is None
            or float(want.get("cpus") or 0) != have["cpus"]
            or float(want.get("memory_mib") or 0) * 2**20 != have["memory"]
        ):
            problems.append(
                f"{name}: resources.services {service} disagrees with rendered limits"
            )
    documents = manifest.get("documents") or {}
    for key in ("guide", "runbook", "guide_target", "runbook_target"):
        path = documents.get(key)
        if path is None and key in {"guide", "runbook"}:
            problems.append(f"{name}: documents {key} is missing")
        elif path is not None and not (
            _repo_path(path) is not None and _repo_path(path).exists()
        ):
            problems.append(
                f"{name}: documents {key} {path} does not exist in the repo"
            )
    return problems


# SPEC-0263 section 5: the OS and Docker reserve kept off the promotion
# budget (owner decision C, 2026-11-05; policy 0107 holds the same table).
PROMOTION_RESERVE = {"cpus": 2.0, "memory_mib": 4096, "disk_percent": 10}
ALLOWED_DRIVERS = frozenset({"local", "bridge", "overlay"})
MAX_ID = 65534
NAME = re.compile(r"[a-z_][a-z0-9_.-]*", re.IGNORECASE)
INFO_SOURCE = "docker info --format '{{json .}}'"


@functools.cache
def profile_vocabulary() -> frozenset[str]:
    """POL-0078 profile names, through the reader the profile gates use."""
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from scripts.lib.document_governance.operations_catalog import (
        _conftest_profile_names,
    )

    return _conftest_profile_names(ROOT)


def measure_host(docker: str, data_root: str) -> dict:
    """Read-only HOME measurements, each `{"value": ..., "source": ...}`.
    A value that cannot be read is left out, so readiness reports NOT_RUN."""
    host = {}
    info = run([docker, "info", "--format", "{{json .}}"])
    try:
        data = json.loads(info.stdout) if info.returncode == 0 else {}
    except ValueError:  # unparsable output is unmeasured, not a crash
        data = {}
    data = data if isinstance(data, dict) else {}
    for key, name in (
        ("NCPU", "NCPU"),
        ("MemTotal", "MemTotal"),
        ("DockerRootDir", "DockerRootDir"),
        ("ServerVersion", "docker_version"),
        ("CgroupVersion", "cgroup_version"),
    ):
        if data.get(key) not in (None, ""):
            host[name] = {"value": data[key], "source": f"{INFO_SOURCE} .{key}"}
    compose = run([docker, "compose", "version", "--short"])
    if compose.returncode == 0 and compose.stdout.strip():
        host["compose_version"] = {
            "value": compose.stdout.strip(),
            "source": "docker compose version --short",
        }
    docker_data = (host.get("DockerRootDir") or {}).get("value")
    for name, path in (("disk_data", data_root), ("disk_docker", docker_data)):
        if not path:
            continue
        try:
            usage = shutil.disk_usage(path)
        except OSError:
            continue
        host[name] = {
            "value": {"path": path, "free": usage.free, "total": usage.total},
            "source": f"shutil.disk_usage({path})",
        }
    return host


def _compose_services(path: str) -> set[str] | None:
    """Service names a repository Compose file declares, or None if absent."""
    import yaml

    file = _repo_path(path)
    if file is None or not file.is_file():
        return None
    try:
        loaded = yaml.safe_load(file.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None
    return (
        set((loaded or {}).get("services") or {}) if isinstance(loaded, dict) else set()
    )


def _root_includes() -> set[str]:
    """Compose files the root docker-compose.yml includes."""
    import yaml

    try:
        loaded = yaml.safe_load((ROOT / "docker-compose.yml").read_text("utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return set()
    items = (loaded or {}).get("include") or [] if isinstance(loaded, dict) else []
    return {str(item.get("path") if isinstance(item, dict) else item) for item in items}


def _version(text: object) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"\d+", str(text))[:3])


def _user_valid(user: str) -> bool:
    """uid[:gid], each numeric in 0..65534 or a name the image resolves."""
    parts = user.split(":")
    return len(parts) <= 2 and all(
        (part.isdigit() and int(part) <= MAX_ID) or NAME.fullmatch(part)
        for part in parts
    )


def _criterion(values: dict, failed: list[str], unmeasured: list[str]) -> dict:
    result = "FAIL" if failed else "NOT_RUN" if unmeasured else "PASS"
    return {"result": result, "values": values, "problems": failed + unmeasured}


def readiness(
    name: str,
    manifest: dict,
    lab: dict,
    host: dict,
    running: list[dict],
    root: dict,
) -> dict:
    """SPEC-0263 section 5: a fail-closed promotion readiness report."""
    source = f"labs/{name}/promotion.yaml"
    kind = manifest.get("kind")
    target = manifest.get("target") or {}
    # Only a replacement kind retires anything. Each retired service must be
    # declared in an existing compose_path and rendered in root; a claim that
    # fails is a composition problem and retires nothing.
    replaces = manifest.get("replaces") if kind in REPLACEMENT_KINDS else None
    retired: set[str] = set()
    covering: list[str] = []  # compose files that declare the retired services
    replace_problems = []
    includes = _root_includes() if replaces else set()
    for item in replaces or []:
        item = item if isinstance(item, dict) else {}
        path = str(item.get("compose_path"))
        services = [str(s) for s in item.get("services") or [item.get("service")] if s]
        declared = _compose_services(path)
        missing = [
            s
            for s in services
            if s not in (declared or ()) or s not in root.get("by_service", {})
        ]
        if declared is None:
            replace_problems.append(f"replaces compose_path {path} does not exist")
        elif path not in includes:
            replace_problems.append(
                f"replaces compose_path {path} is not included by root"
            )
        elif not services or missing:
            replace_problems.append(
                f"replaces {path}: services {missing or services} are not "
                "declared there and rendered in root"
            )
        else:
            retired |= set(services)
            covering.append(path)
    by_service = root.get("by_service", {})
    kept_identity = {
        key: set().union(*(v[key] for s, v in by_service.items() if s not in retired))
        for key in ("containers", "ports", "dirs")
    }
    # A port or container name that a kept service also declares stays.
    retired_identity = {
        key: set().union(*(by_service[s][key] for s in retired)) - kept_identity[key]
        for key in ("containers", "ports", "dirs")
    }
    criteria = {}

    # Tier fit.
    failed: list[str] = []
    folder = target.get("folder")
    values = {
        "kind": {"value": kind, "source": source},
        "folder": {"value": folder, "source": source},
        # Spec section 5 "matches the service function" is an owner judgment;
        # it is shown, not measured, and does not block PASS (narrowing in
        # POL-0107 awaiting owner acceptance).
        "function_fit": {"value": "NOT_RUN", "source": "owner judgment, not measured"},
    }
    if kind not in MANIFEST_KINDS - {"undecided"}:
        failed.append(f"kind {kind!r} has no promotion target")
    if (
        not isinstance(folder, str)
        or not TARGET_FOLDER.fullmatch(folder)
        or ".." in folder.split("/")
    ):
        failed.append(f"target folder {folder!r} is outside infra/<tier>/")
    elif _repo_path(folder) is None:
        failed.append(f"target folder {folder} resolves outside the repository")
    else:
        tier = "/".join(folder.split("/")[:2])
        values["tier_exists"] = {"value": (ROOT / tier).is_dir(), "source": tier}
        if not (ROOT / tier).is_dir():
            failed.append(f"tier folder {tier} does not exist")
        exists = (ROOT / folder).exists()
        values["folder_exists"] = {"value": exists, "source": folder}

        # An existing folder is a declared replacement only when retired
        # services own it exclusively: it holds a verified retired Compose
        # file or a retired service's build context or bind source, and no
        # kept service's build context or bind source lies inside it. Derived
        # from the root render, not from the manifest.
        real = os.path.realpath(ROOT / folder)
        claimed = any(path.startswith(folder) for path in covering) or any(
            _within(item, real) for item in retired_identity["dirs"]
        )
        shared = {
            s
            for s, v in by_service.items()
            if s not in retired and any(_within(item, real) for item in v["dirs"])
        }
        # The filesystem too: every service a Compose file inside the folder
        # declares must be retired (dev-db/ still declares dev-pg).
        if exists and pathlib.Path(real).is_dir():
            # rglob does not follow a symlinked directory, so one hides files.
            linked = [
                p
                for p in pathlib.Path(real).rglob("*")
                if p.is_symlink() and p.is_dir()
            ]
            if linked:
                failed.append(f"target folder {folder} holds a symlinked directory")
            for found in pathlib.Path(real).rglob("*compose*.y*ml"):
                path = os.path.relpath(found, os.path.realpath(ROOT))
                declared = _compose_services(path)
                if declared is None:
                    failed.append(f"compose file {path} in the target cannot be read")
                    continue
                shared |= declared - retired
        shared = sorted(shared)
        if exists and (not claimed or shared):
            failed.append(
                f"target folder {folder} exists and is not a replacement"
                + (f"; kept services use it: {', '.join(shared)}" if shared else "")
            )
    unmeasured = []
    try:
        failed += manifest_problems(name, manifest, lab, catalog_ids())
    except LabError as exc:
        unmeasured.append(str(exc))
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise LabError(f"{name}: invalid manifest or catalog: {exc!r}", 2) from exc
    criteria["tier"] = _criterion(values, failed, unmeasured)

    # Service composition. The retired services' own containers and ports
    # are removed from root and running before collisions(); networks and
    # data paths stay, since retiring a service frees neither.
    failed, unmeasured = list(replace_problems), []
    kept_root = dict(root)
    for key in ("containers", "ports"):
        kept_root[key] = root[key] - retired_identity[key]
    kept_running = [
        c for c in running if c["name"] not in retired_identity["containers"]
    ]
    clashes = collisions({name: lab}, kept_root, kept_running)
    failed += clashes
    profile = target.get("profile")
    values = {
        "collisions": {
            "value": len(clashes),
            "source": "collisions() against the root render and docker inspect",
        },
        "retired_services": {"value": sorted(retired), "source": source},
        "profile": {"value": profile, "source": source},
        # Spec section 5 profile and consumer clashes are not measured.
        "profile_and_consumer_clashes": {"value": "NOT_RUN", "source": "not measured"},
    }
    unmeasured.append("profile and consumer clashes are not measured")
    try:
        if profile not in profile_vocabulary():
            failed.append(f"profile {profile!r} is not in the POL-0078 vocabulary")
    except Exception as exc:  # an unreadable policy cannot pass
        unmeasured.append(f"POL-0078 vocabulary unreadable: {exc}")
    for item in manifest.get("integrations") or []:
        owner = item.get("owner") if isinstance(item, dict) else None
        path = _repo_path(owner)
        if path is None or not path.exists():
            failed.append(f"integration owner {owner!r} does not exist")
    criteria["composition"] = _criterion(values, failed, unmeasured)

    # Linux.
    failed, unmeasured = [], []
    requirements = manifest.get("host") or {}
    cgroup = (host.get("cgroup_version") or {}).get("value")
    values = {
        "cgroup_version": {
            "value": cgroup,
            "source": (host.get("cgroup_version") or {}).get("source", INFO_SOURCE),
        }
    }
    # Spec section 5 groups and file modes are not measured.
    values["groups_and_file_modes"] = {"value": "NOT_RUN", "source": "not measured"}
    unmeasured.append("groups and file modes are not measured")
    features = [str(f) for f in requirements.get("kernel_features") or []]
    if lab["cpus"] or lab["memory"] or "cgroup2" in features:
        if cgroup is None:
            unmeasured.append("cgroup version was not measured")
        elif str(cgroup) != "2":
            failed.append(f"declared limits need cgroup v2, host has v{cgroup}")
    for service, user in sorted(lab.get("users", {}).items()):
        if user is None:
            continue
        values[f"user {service}"] = {
            "value": str(user),
            "source": f"rendered compose services.{service}.user"
            + ("" if str(user).replace(":", "").isdigit() else "; resolved in image"),
        }
        if not _user_valid(str(user)):
            failed.append(f"{service}: user {user!r} is not a valid uid[:gid]")
    unmeasured += [
        f"kernel feature {f} cannot be measured" for f in features if f != "cgroup2"
    ]
    criteria["linux"] = _criterion(values, failed, unmeasured)

    # Docker.
    failed, unmeasured = [], []
    values = {}
    for key, measured in (("docker", "docker_version"), ("compose", "compose_version")):
        found = host.get(measured)
        values[measured] = found or {"value": None, "source": INFO_SOURCE}
        if found is None:
            unmeasured.append(f"{key} version was not measured")
        elif key in requirements and _version(found["value"]) < _version(
            requirements[key]
        ):
            failed.append(f"{key} {found['value']} is older than {requirements[key]}")
    drivers = sorted(lab.get("drivers", set()))
    values["drivers"] = {"value": drivers, "source": "rendered compose"}
    failed += [
        f"driver {d} is not allowed" for d in drivers if d not in ALLOWED_DRIVERS
    ]
    data_root = host.get("DockerRootDir")
    values["DockerRootDir"] = data_root or {"value": None, "source": INFO_SOURCE}
    if data_root is None:
        unmeasured.append("Docker data root was not measured")
    elif not os.path.isabs(str(data_root["value"])):
        failed.append(f"Docker data root {data_root['value']} is not absolute")
    criteria["docker"] = _criterion(values, failed, unmeasured)

    # Server resources: limits in bytes, reported in MiB.
    failed, unmeasured = [], []
    counted = [
        c for c in running if c.get("running", True) and c["project"] != lab["project"]
    ]
    retiring = [c for c in counted if c["name"] in retired_identity["containers"]]
    kept = [c for c in counted if c not in retiring]
    unlimited = sorted(c["name"] for c in kept if not c["cpus"] or not c["memory"])
    unmeasured += [f"running container {c} declares no limit" for c in unlimited]
    # A candidate service without a limit cannot be summed either.
    unmeasured += [
        f"candidate service {s} declares no limit"
        for s, v in sorted(lab["services"].items())
        if not v["cpus"] or not v["memory"]
    ]
    ncpu, memtotal = host.get("NCPU"), host.get("MemTotal")
    inspect = "docker inspect HostConfig.NanoCpus/Memory of running containers"
    values = {
        "running_cpus": {"value": sum(c["cpus"] for c in counted), "source": inspect},
        "retired_cpus": {"value": sum(c["cpus"] for c in retiring), "source": inspect},
        "candidate_cpus": {"value": lab["cpus"], "source": "rendered compose"},
        "running_memory_mib": {
            "value": sum(c["memory"] for c in counted) / MIB_BYTES,
            "source": inspect,
        },
        "retired_memory_mib": {
            "value": sum(c["memory"] for c in retiring) / MIB_BYTES,
            "source": inspect,
        },
        "candidate_memory_mib": {
            "value": lab["memory"] / MIB_BYTES,
            "source": "rendered compose",
        },
        "unlimited_containers": {"value": unlimited, "source": inspect},
    }
    cpus = sum(c["cpus"] for c in kept) + lab["cpus"]
    memory = sum(c["memory"] for c in kept) + lab["memory"]
    values["cpus_needed"] = {"value": cpus, "source": "running - retired + candidate"}
    values["memory_needed_mib"] = {
        "value": memory / MIB_BYTES,
        "source": "running - retired + candidate",
    }
    if ncpu is None or memtotal is None:
        unmeasured.append("host CPU count or memory was not measured")
    else:
        values["NCPU"], values["MemTotal"] = ncpu, memtotal
        cpu_budget = float(ncpu["value"]) - PROMOTION_RESERVE["cpus"]
        memory_budget = (
            float(memtotal["value"]) - PROMOTION_RESERVE["memory_mib"] * MIB_BYTES
        )
        values["cpu_budget"] = {"value": cpu_budget, "source": "NCPU - reserve"}
        values["memory_budget_mib"] = {
            "value": memory_budget / MIB_BYTES,
            "source": "MemTotal - reserve",
        }
        if cpus > cpu_budget:
            failed.append(f"CPUs {cpus:g} exceed budget {cpu_budget:g}")
        if memory > memory_budget:
            failed.append(
                f"memory {memory / MIB_BYTES:.0f} MiB exceeds budget "
                f"{memory_budget / MIB_BYTES:.0f} MiB"
            )
    need = (manifest.get("resources") or {}).get("disk_gib") or {}
    for disk, key in (("disk_data", "data"), ("disk_docker", "images")):
        found = host.get(disk)
        if found is None or key not in need:
            unmeasured.append(f"{disk} free space or disk_gib.{key} is missing")
            continue
        usage = found["value"]
        values[disk] = found
        free = usage["free"] - usage["total"] * PROMOTION_RESERVE["disk_percent"] / 100
        values[f"{disk}_usable_gib"] = {
            "value": round(free / 2**30, 1),
            "source": found.get("source", "shutil.disk_usage"),
        }
        try:
            needed = float(need[key]) * 2**30
        except (TypeError, ValueError) as exc:
            raise LabError(f"{name}: disk_gib.{key} is not a number", 2) from exc
        if free < needed:
            failed.append(
                f"{disk}: {free / 2**30:.1f} GiB usable, disk_gib.{key} needs "
                f"{need[key]}"
            )
    # Over budget stays FAIL even with unlimited containers: the known lower
    # bound already exceeds the budget. NOT_RUN only when the measured sum fits.
    criteria["resources"] = _criterion(values, failed, unmeasured)

    results = {c["result"] for c in criteria.values()}
    overall = (
        "PASS" if results == {"PASS"} else "FAIL" if "FAIL" in results else "NOT_RUN"
    )
    return {"lab": name, "kind": kind, "result": overall, "criteria": criteria}


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
    ids = catalog_ids()
    manifests = []
    for name, lab in selected.items():
        try:
            manifests += manifest_problems(name, load_manifest(name), lab, ids)
        except LabError as exc:  # a missing manifest is a problem, not a crash
            manifests.append(str(exc))
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
        + stale_volumes(args.docker, selected)
        + manifests,
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


def cmd_readiness(args) -> int:
    """Read HOME state only: renders, docker info/inspect and disk usage."""
    candidate = footprint(render(args.docker, args.env_file, lab_file(args.lab)))
    root = root_footprint(
        render(args.docker, args.root_env_file, None),
        env_file=args.root_env_file,
        docker_root=docker_root(args.docker),
    )
    report = readiness(
        args.lab,
        load_manifest(args.lab),
        candidate,
        measure_host(args.docker, root["home_data_root"]),
        running_containers(args.docker),
        root,
    )
    text = json.dumps(report, indent=2) + "\n"
    if args.report:
        args.report.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if report["result"] == "PASS" else 3


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
    ready = commands.add_parser("readiness")
    ready.add_argument("lab")
    ready.add_argument("--report", type=pathlib.Path)
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
        if args.command == "readiness":
            return cmd_readiness(args)
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
