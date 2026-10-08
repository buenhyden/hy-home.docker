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
import json
import os
import pathlib
import re
import signal
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
LAB_PROJECT_PREFIX = "hy-home-lab-"
LEASE = re.compile(r"^([1-9][0-9]*)([mh])$")


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
    return subprocess.run(
        command, cwd=ROOT, text=True, capture_output=True, check=False, **kwargs
    )


def render(docker: str, env_file: pathlib.Path, compose_file: str | None) -> dict:
    command = [docker, "compose", "--env-file", str(env_file)]
    if compose_file:
        command += ["-f", compose_file]
    result = run([*command, "--profile", "*", "config", "--format", "json"])
    if result.returncode != 0:
        raise LabError(
            f"render failed for {compose_file or 'root'}: {result.stderr.strip()}", 1
        )
    return json.loads(result.stdout)


def footprint(model: dict) -> dict:
    """Names, ports, writable state paths and declared limits of one model."""
    project = model.get("name", "")
    containers, ports, paths, state, written = set(), set(), set(), set(), set()
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
            if mount.get("read_only"):
                continue
            if mount.get("type") == "bind":
                # realpath: a symlinked root must not hide an overlap.
                path = os.path.realpath(mount["source"])
                paths.add(path)
                state.add(path)
            elif mount.get("type") == "volume":
                written.add(mount.get("source"))
        cpus += float(service.get("cpus") or 0) * replicas
        memory += int(service.get("mem_limit") or 0) * replicas
    for key, volume in (model.get("volumes") or {}).items():
        device = (volume.get("driver_opts") or {}).get("device")
        if device:
            path = os.path.realpath(device)
            paths.add(path)
            # Read-only inputs (a scenario source) are never cleanup targets.
            if key in written:
                state.add(path)
    networks = {net.get("name") for net in (model.get("networks") or {}).values()}
    return {
        "project": project,
        "containers": containers,
        "ports": ports,
        "paths": paths,
        "state": state,
        "networks": networks - {None},
        "cpus": cpus,
        "memory": memory,
    }


def _nested(a: str, b: str) -> bool:
    return a == b or a.startswith(b + os.sep) or b.startswith(a + os.sep)


def _port_clash(a: str, b: str) -> bool:
    host_a, port_a = a.rsplit(":", 1)
    host_b, port_b = b.rsplit(":", 1)
    wildcard = {"0.0.0.0", "::", ""}
    return port_a == port_b and bool(host_a == host_b or {host_a, host_b} & wildcard)


def collisions(selected: dict[str, dict], root: dict, running: list[dict]) -> list[str]:
    """Every name, port or state path a selected LAB would share."""
    problems: list[str] = []
    others = [("root", root)] + [(f"lab {n}", f) for n, f in selected.items()]
    for name, lab in selected.items():
        for other_name, other in others:
            if other is lab:
                continue
            for key in ("containers", "networks"):
                for clash in sorted(lab[key] & other[key]):
                    problems.append(f"{name}: {key[:-1]} {clash} also in {other_name}")
            for port in sorted(lab["ports"]):
                if any(_port_clash(port, p) for p in other["ports"]):
                    problems.append(f"{name}: host port {port} also in {other_name}")
            for path in sorted(lab["paths"]):
                if any(_nested(path, p) for p in other["paths"]):
                    problems.append(f"{name}: data path {path} overlaps {other_name}")
        for container in running:
            if container["project"] == lab["project"]:
                continue
            if container["name"] in lab["containers"]:
                problems.append(f"{name}: container {container['name']} already runs")
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
    kept = [c for c in running if c["project"] not in projects]
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
    listed = run([docker, "ps", "-q"])
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
            }
        )
    return containers


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


def check(args, env) -> tuple[dict, dict[str, dict]]:
    selected = {
        name: footprint(render(args.docker, args.env_file, lab_file(name)))
        for name in args.labs
    }
    root = footprint(render(args.docker, args.root_env_file, None))
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
            c["name"] for c in running if not c["cpus"] or not c["memory"]
        ),
        "problems": collisions(selected, root, running)
        + budget(selected, running, env),
    }
    return report, selected


def compose_command(args, name: str, project: str) -> list[str]:
    return [
        args.docker, "compose", "-p", project, "--env-file", str(args.env_file),
        "-f", lab_file(name), "--profile", "*",
    ]  # fmt: skip


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
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
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
    # A job LAB may finish before it reports healthy, so `run` does not wait.
    result = run([*command, "--wait"] if wait else command)
    entry["state"] = "running" if result.returncode == 0 else "failed"
    write_entry(target, entry)
    print(json.dumps({k: entry[k] for k in ("lab", "state", "expires_at")}))
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
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
        run([docker, "stop", "--time", str(grace), jobs[0]], timeout=grace + 30)
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
    code = cmd_up(args, env, wait=False)
    if code != 0:
        return code
    target = ledger_dir(env) / f"{args.lab}.json"
    entry = json.loads(target.read_text(encoding="utf-8"))
    outcome, code = "failed", 1
    try:
        outcome, code = supervise(
            args.docker, entry["project"], deadline_seconds, args.grace
        )
    finally:
        stopped = stop(args, env, args.lab)
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
        projects = {c["project"] for c in running_containers(args.docker)}
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
