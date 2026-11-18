#!/usr/bin/env python3
"""Run dependent work units on shell workers in separate Git worktrees.

A plan lists units with their command, dependencies, owned paths and shared
resources. A unit starts only when every dependency succeeded and it holds a
lease on each owned path and shared resource; each lease carries a fencing
generation, so a result whose lease expired or was taken over is refused. A
worktree separates files, not processes: it is not a sandbox. A result that
changes a path outside the unit's ownership is refused. A failure blocks only
its downstream units. Cancelling kills each running worker's process group
and starts nothing more. When every unit succeeded, the integrator applies
the patches on the base commit and runs the integration checks again; a
worker's own success is never the integrated result.
"""

from __future__ import annotations

import argparse
import graphlib
import json
import os
import posixpath
import signal
import sqlite3
import subprocess
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.lib.hooks import session_capture as capture  # noqa: E402

STORE_NAME = "dispatch.sqlite3"
CANCEL_NAME = "cancel"
DEFAULT_WORKERS = 2
TICK = 0.05


class PlanError(ValueError):
    """A plan the dispatcher refuses to run."""


def _under(path: str, owner: str) -> bool:
    owner = owner.rstrip("/")
    return path == owner or path.startswith(owner + "/")


def _conflicts(a: str, b: str) -> bool:
    if a.startswith("path:") and b.startswith("path:"):
        return _under(a[5:].rstrip("/"), b[5:]) or _under(b[5:].rstrip("/"), a[5:])
    return a == b


class Leases:
    """Resource leases with a generation per resource that fences old holders."""

    def __init__(self, directory: Path) -> None:
        directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.path = directory / STORE_NAME

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=5.0, isolation_level=None)
        os.chmod(self.path, 0o600)
        connection.execute(
            "CREATE TABLE IF NOT EXISTS leases (resource TEXT PRIMARY KEY,"
            " generation INTEGER NOT NULL, holder TEXT, expires REAL NOT NULL)"
        )
        return connection

    def acquire(self, resources, holder: str, ttl: float) -> dict | None:
        """All resources at once with new generations, or None if any is held."""
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            now = time.time()
            held = connection.execute(
                "SELECT resource FROM leases WHERE expires > ? AND holder != ?",
                (now, holder),
            ).fetchall()
            if any(_conflicts(r, h) for r in resources for (h,) in held):
                connection.execute("ROLLBACK")
                return None
            tokens = {}
            for resource in resources:
                row = connection.execute(
                    "SELECT generation FROM leases WHERE resource=?", (resource,)
                ).fetchone()
                tokens[resource] = (row[0] if row else 0) + 1
                connection.execute(
                    "INSERT OR REPLACE INTO leases VALUES (?,?,?,?)",
                    (resource, tokens[resource], holder, now + ttl),
                )
            connection.execute("COMMIT")
            return tokens
        finally:
            connection.close()

    def valid(self, tokens: dict, holder: str) -> bool:
        """True only while every lease is unexpired at the same generation."""
        connection = self._connect()
        try:
            now = time.time()
            for resource, generation in tokens.items():
                row = connection.execute(
                    "SELECT generation, holder, expires FROM leases WHERE resource=?",
                    (resource,),
                ).fetchone()
                if row is None or row[0] != generation or row[1] != holder:
                    return False
                if row[2] <= now:
                    return False
            return True
        finally:
            connection.close()

    def release(self, tokens: dict, holder: str) -> None:
        connection = self._connect()
        try:
            for resource, generation in tokens.items():
                connection.execute(
                    "UPDATE leases SET expires=0, holder=NULL"
                    " WHERE resource=? AND generation=? AND holder=?",
                    (resource, generation, holder),
                )
        finally:
            connection.close()


def _git(repo: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True
    ).stdout


def _validate(plan: dict) -> dict[str, dict]:
    units = plan.get("units") or []
    ids = [u.get("id") for u in units]
    if not units or not all(ids) or len(set(ids)) != len(ids):
        raise PlanError("units need unique ids")
    graph = {}
    for u in units:
        if not u.get("command") or not isinstance(u["command"], list):
            raise PlanError(f"{u['id']} needs a command list")
        for dep in u.get("depends_on", []):
            if dep not in ids:
                raise PlanError(f"{u['id']} depends on unknown {dep}")
        for path in u.get("owned_paths", []):
            norm = posixpath.normpath(path)
            if posixpath.isabs(path) or norm == ".." or norm.startswith("../"):
                raise PlanError(f"{u['id']} owns a path outside the repository")
        graph[u["id"]] = set(u.get("depends_on", []))
    try:
        tuple(graphlib.TopologicalSorter(graph).static_order())
    except graphlib.CycleError as error:
        raise PlanError(f"dependency cycle: {error.args[1]}") from error
    return {u["id"]: u for u in units}


def _ancestors(units: dict, uid: str) -> set[str]:
    seen, stack = set(), list(units[uid].get("depends_on", []))
    while stack:
        dep = stack.pop()
        if dep not in seen:
            seen.add(dep)
            stack.extend(units[dep].get("depends_on", []))
    return seen


def _kill(process: subprocess.Popen) -> None:
    """Stop the worker's whole process group, then reap the worker."""
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(process.pid, sig)
        except ProcessLookupError:
            break
        time.sleep(0.5)
    process.wait()


def cancel(state: Path) -> None:
    """Ask every run using this state directory to stop."""
    state.mkdir(mode=0o700, parents=True, exist_ok=True)
    (state / CANCEL_NAME).touch()


def run(repo: Path, state: Path, plan: dict) -> dict:
    units = _validate(plan)
    leases = Leases(state)
    (state / CANCEL_NAME).unlink(missing_ok=True)
    run_id = time.strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:6]
    root = state / "runs" / run_id
    (root / "wt").mkdir(parents=True)
    (root / "dispatcher.pid").write_text(str(os.getpid()))
    base = _git(repo, "rev-parse", plan.get("base", "HEAD")).decode().strip()
    lease_seconds = float(plan.get("lease_seconds", 0))
    # ponytail: a flat worker ceiling capped by CPUs; memory-aware quota when workers get heavy
    workers = max(
        1, min(int(plan.get("max_workers", DEFAULT_WORKERS)), os.cpu_count() or 1)
    )
    start = time.monotonic()
    result = {uid: {"id": uid, "status": "pending"} for uid in units}
    done_order: list[str] = []
    running: dict[str, dict] = {}
    cancelled = False

    def clock() -> float:
        return round(time.monotonic() - start, 3)

    def finish(uid: str, status: str, reason: str = "") -> None:
        result[uid].update(status=status, reason=reason, finished=clock())
        job = running.pop(uid)
        leases.release(job["tokens"], job["holder"])
        _git(repo, "worktree", "remove", "--force", str(job["worktree"]))
        (root / f"{uid}.pgid").unlink(missing_ok=True)

    def collect(uid: str, job: dict) -> None:
        code = job["process"].returncode
        if code != 0:
            return finish(uid, "failed", f"exit {code}")
        tree = job["worktree"]
        _git(tree, "add", "-A")
        changed = _git(tree, "diff", "--cached", "--name-only", "-z", job["start"])
        paths = [p for p in changed.decode().split("\0") if p]
        outside = [p for p in paths if not any(_under(p, o) for o in job["owned"])]
        if outside:
            return finish(uid, "rejected", "outside ownership: " + ", ".join(outside))
        if not leases.valid(job["tokens"], job["holder"]):
            return finish(uid, "rejected", "stale lease")
        patch = _git(tree, "diff", "--cached", "--binary", job["start"])
        (root / f"{uid}.patch").write_bytes(patch)
        result[uid]["changed"] = paths
        done_order.append(uid)
        finish(uid, "succeeded")

    def launch(u: dict) -> None:
        holder = f"{run_id}:{u['id']}"
        owned = [posixpath.normpath(p) for p in u.get("owned_paths", [])]
        resources = ["path:" + p for p in owned] + list(u.get("shared_resources", []))
        timeout = float(u.get("timeout", 600))
        tokens = leases.acquire(resources, holder, lease_seconds or timeout + 60)
        if tokens is None:
            return
        tree = root / "wt" / u["id"]
        _git(repo, "worktree", "add", "--detach", "-q", str(tree), base)
        ancestors = _ancestors(units, u["id"])
        for prior in done_order:
            if prior in ancestors:
                _git(tree, "apply", "--index", str(root / f"{prior}.patch"))
        start_tree = _git(tree, "write-tree").decode().strip()
        env = dict(
            os.environ,
            HY_TASK=str(plan.get("task", "")),
            HY_BRIEF_REVISION=str(plan.get("brief_revision", "")),
            HY_WORK_UNIT=u["id"],
            HY_FENCE=json.dumps(tokens),
        )
        with open(root / f"{u['id']}.log", "wb") as log:
            process = subprocess.Popen(
                u["command"],
                cwd=tree,
                env=env,
                stdout=log,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
            )
        (root / f"{u['id']}.pgid").write_text(str(process.pid))
        running[u["id"]] = dict(
            process=process,
            tokens=tokens,
            holder=holder,
            worktree=tree,
            start=start_tree,
            owned=owned,
            deadline=time.monotonic() + timeout,
        )
        result[u["id"]].update(status="running", started=clock(), fence=tokens)

    try:
        while True:
            if not cancelled and (state / CANCEL_NAME).exists():
                cancelled = True
                for uid, job in list(running.items()):
                    _kill(job["process"])
                    finish(uid, "cancelled", "cancel requested")
            for uid, job in list(running.items()):
                if job["process"].poll() is not None:
                    collect(uid, job)
                elif time.monotonic() > job["deadline"]:
                    _kill(job["process"])
                    finish(uid, "failed", "timeout")
            for uid, u in units.items():
                entry = result[uid]
                if entry["status"] != "pending":
                    continue
                deps = [result[d]["status"] for d in u.get("depends_on", [])]
                if cancelled or any(
                    s not in ("pending", "running", "succeeded") for s in deps
                ):
                    entry.update(
                        status="blocked",
                        reason="cancel requested" if cancelled else "upstream failed",
                    )
                elif all(s == "succeeded" for s in deps) and len(running) < workers:
                    launch(u)
            if not running and all(r["status"] != "pending" for r in result.values()):
                break
            time.sleep(TICK)
    finally:
        for uid, job in list(running.items()):
            _kill(job["process"])
            finish(uid, "cancelled", "dispatcher stopped")
        _git(repo, "worktree", "prune")

    integration = {"status": "not run"}
    if not cancelled and all(r["status"] == "succeeded" for r in result.values()):
        integration = _integrate(
            repo, root, base, done_order, plan.get("integration_checks", [])
        )
    status = (
        "cancelled"
        if cancelled
        else "succeeded"
        if integration["status"] == "passed"
        else "failed"
    )
    report = {
        "run_id": run_id,
        "task": plan.get("task"),
        "brief_revision": plan.get("brief_revision"),
        "base": base,
        "max_workers": workers,
        "status": status,
        "elapsed_seconds": clock(),
        "unit_seconds": round(
            sum(r.get("finished", 0) - r.get("started", 0) for r in result.values()),
            3,
        ),
        "units": list(result.values()),
        "integration": integration,
    }
    (root / "report.json").write_text(json.dumps(report, indent=2))
    return report


def _integrate(repo, root, base, order, checks) -> dict:
    """Apply every unit patch on the base and rerun the integration checks."""
    tree = root / "wt" / "integration"
    _git(repo, "worktree", "add", "--detach", "-q", str(tree), base)
    try:
        for uid in order:
            try:
                _git(tree, "apply", "--index", str(root / f"{uid}.patch"))
            except subprocess.CalledProcessError:
                return {"status": "failed", "reason": f"{uid} patch does not apply"}
        patch = root / "integrated.patch"
        patch.write_bytes(_git(tree, "diff", "--cached", "--binary", base))
        for check in checks:
            done = subprocess.run(
                check,
                cwd=tree,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                check=False,
            )
            if done.returncode != 0:
                return {
                    "status": "failed",
                    "reason": f"check {check} exit {done.returncode}",
                    "patch": str(patch),
                }
        return {"status": "passed", "patch": str(patch), "checks": len(checks)}
    finally:
        _git(repo, "worktree", "remove", "--force", str(tree))


def cleanup(repo: Path, state: Path) -> list[str]:
    """Stop workers and remove worktrees left by a dispatcher that died."""
    removed = []
    for root in sorted((state / "runs").glob("*")):
        try:
            os.kill(int((root / "dispatcher.pid").read_text()), 0)
            continue
        except (ProcessLookupError, FileNotFoundError, ValueError):
            pass
        for pgid in root.glob("*.pgid"):
            try:
                os.killpg(int(pgid.read_text()), signal.SIGKILL)
            except (ProcessLookupError, ValueError):
                pass
            pgid.unlink()
        for tree in sorted((root / "wt").glob("*")):
            subprocess.run(
                ["git", "-C", str(repo), "worktree", "remove", "--force", str(tree)],
                capture_output=True,
                check=False,
            )
            removed.append(str(tree))
    _git(repo, "worktree", "prune")
    return removed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--state-dir", type=Path)
    parser.add_argument("--repo", type=Path, default=ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("run").add_argument("plan", type=Path)
    commands.add_parser("cancel")
    commands.add_parser("cleanup")
    args = parser.parse_args(argv)
    state = args.state_dir or capture.capture_dir() / "dispatch"
    if args.command == "cancel":
        cancel(state)
        return 0
    if args.command == "cleanup":
        print(json.dumps(cleanup(args.repo, state), indent=2))
        return 0
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: cancel(state))
    try:
        report = run(args.repo, state, json.loads(args.plan.read_text()))
    except PlanError as error:
        print(f"PLAN_REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "succeeded" else 1


if __name__ == "__main__":
    raise SystemExit(main())
