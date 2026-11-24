#!/usr/bin/env python3
"""Run dependent work units on shell or provider workers in separate worktrees.

A plan lists units with their command, or a Claude or Codex provider with a
model, prompt and USD cap, plus dependencies, owned paths and shared
resources. A provider unit starts only after the bound request brief allows
dispatch to every path it owns, and its final JSON (session, cost, error) is
kept in the report. A unit starts only when every dependency succeeded and it holds a
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
import hashlib
import json
import os
import posixpath
import re
import shutil
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
from scripts.lib.ops import dispatch_providers  # noqa: E402
from scripts.lib.ops.dispatch_process import (  # noqa: E402
    ProcessError as PlanError,
)
from scripts.lib.ops.dispatch_process import (  # noqa: E402
    _bootstrap,
    _budget,
    _disk_problem,
    _finish_environment,
    _git_view,
    _group_absent,
    _kill,
    _scope_absent,
    _spawn,
    _write_record,
)
from scripts.lib.ops.environment_admission import (  # noqa: E402
    AdmissionError,
    process_identity,
    process_status,
)

STORE_NAME = "dispatch.sqlite3"
CANCEL_NAME = "cancel"
DEFAULT_WORKERS = 2
DEFAULT_INTEGRATION_TIMEOUT = 600
# A unit id becomes a path component, so it must be a plain token.
UNIT_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}")
TICK = 0.05


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

    def release_run(self, run_id: str) -> None:
        """Free every lease a run still holds, for a dispatcher that died."""
        connection = self._connect()
        try:
            connection.execute(
                "UPDATE leases SET expires=0, holder=NULL WHERE holder LIKE ?",
                (run_id + ":%",),
            )
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


def _git(repo: Path, *args: str, data: bytes | None = None) -> bytes:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, input=data
    ).stdout


def _wt(gitdir: str, tree: Path, *args: str, data: bytes | None = None) -> bytes:
    """Git in a worktree through its recorded Git directory.

    A worker can delete or rewrite the worktree's `.git` file; without the
    explicit directory Git would walk up into the main repository.
    """
    return _git(tree, f"--git-dir={gitdir}", f"--work-tree={tree}", *args, data=data)


def _names(raw: bytes) -> list[str]:
    return [os.fsdecode(name) for name in raw.split(b"\0") if name]


def _remove_worktree(repo: Path, tree: Path) -> bool:
    subprocess.run(
        ["git", "-C", str(repo), "worktree", "remove", "--force", str(tree)],
        capture_output=True,
        check=False,
    )
    # Delete only a run's own worktree folder, never a path a plan could name.
    if tree.parent.name == "wt" and tree.parent.parent.parent.name == "runs":
        shutil.rmtree(tree, ignore_errors=True)
    return not tree.exists()


def _exited(process: subprocess.Popen) -> bool:
    """True once the leader exited, without reaping it.

    The leader stays a zombie until `wait`, so its process group id cannot be
    reused while the group is killed.
    """
    try:
        return (
            os.waitid(os.P_PID, process.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT)
            is not None
        )
    except ChildProcessError:
        return True


def _killpg(pid: int) -> None:
    try:
        os.killpg(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def _argv(value) -> bool:
    """A command Popen can start: a non-empty list of strings without NUL."""
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(part, str) and "\0" not in part for part in value)
    )


def _validate(plan: dict) -> dict[str, dict]:
    units = plan.get("units") or []
    ids = [u.get("id") for u in units]
    if not units or not all(ids) or len(set(ids)) != len(ids):
        raise PlanError("units need unique ids")
    for uid in ids:
        if not isinstance(uid, str) or not UNIT_ID.fullmatch(uid) or ".." in uid:
            raise PlanError(f"unit id {uid!r} is not a plain token")
    graph = {}
    for u in units:
        if "provider" in u:
            if "command" in u:
                raise PlanError(f"{u['id']} names both a command and a provider")
            try:
                dispatch_providers.validate(u["provider"])
            except dispatch_providers.ProviderError as error:
                raise PlanError(f"{u['id']}: {error}") from error
            if not all(
                isinstance(plan.get(key), str) and plan[key]
                for key in ("session", "request_revision")
            ):
                raise PlanError(
                    "a provider unit needs the plan's session and request_revision"
                )
        elif not _argv(u.get("command")):
            raise PlanError(f"{u['id']} needs a command list of strings")
        for dep in u.get("depends_on", []):
            if dep not in ids:
                raise PlanError(f"{u['id']} depends on unknown {dep}")
        for path in u.get("owned_paths", []):
            norm = posixpath.normpath(path)
            if posixpath.isabs(path) or norm == ".." or norm.startswith("../"):
                raise PlanError(f"{u['id']} owns a path outside the repository")
            if norm == ".":
                raise PlanError(f"{u['id']} must name paths, not the whole repository")
        graph[u["id"]] = set(u.get("depends_on", []))
    for unit in units:
        _budget(unit.get("resource_budget"), unit.get("timeout", 600))
    _budget(
        plan.get("integration_resource_budget"),
        plan.get("integration_timeout", DEFAULT_INTEGRATION_TIMEOUT),
    )
    if not all(_argv(check) for check in plan.get("integration_checks", [])):
        raise PlanError("integration checks must be command lists of strings")
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


def _brief_problem(repo: Path, plan: dict, owned: list[str]) -> str | None:
    """None when the bound brief allows dispatch to every owned path."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.lib.hooks.request_brief",
            "check",
            plan["session"],
            "dispatch",
            plan["request_revision"],
            str(plan.get("brief_revision", "")),
            *owned,
        ],
        cwd=repo,
        env=dict(os.environ, PYTHONPATH=str(ROOT)),
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if result.returncode == 0:
        return None
    return (result.stderr.strip().splitlines() or ["brief check failed"])[0][:200]


def _execution_admission(repo, *, recovery=False):
    from scripts.operations.lab import execution_admission

    return execution_admission(repo, recovery=recovery)


def cancel(state: Path) -> None:
    """Ask every run that started before now on this state directory to stop."""
    state.mkdir(mode=0o700, parents=True, exist_ok=True)
    (state / CANCEL_NAME).touch()


def run(repo: Path, state: Path, plan: dict) -> dict:
    units = _validate(plan)
    leases = Leases(state)
    admission = _execution_admission(repo)
    started_wall = time.time()
    run_id = time.strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:6]
    root = state / "runs" / run_id
    (root / "wt").mkdir(parents=True)
    (root / "dispatcher.pid").write_text(str(os.getpid()))
    _write_record(root / "dispatcher.json", process_identity())
    base = _git(repo, "rev-parse", plan.get("base", "HEAD")).decode().strip()
    lease_seconds = float(plan.get("lease_seconds", 0))
    workers = max(
        1, min(int(plan.get("max_workers", DEFAULT_WORKERS)), os.cpu_count() or 1)
    )
    start = time.monotonic()
    result = {uid: {"id": uid, "status": "pending"} for uid in units}
    done_order: list[str] = []
    patches: dict[str, bytes] = {}
    running: dict[str, dict] = {}
    cancelled = False

    def cancel_requested() -> bool:
        try:
            return (state / CANCEL_NAME).stat().st_mtime >= started_wall
        except FileNotFoundError:
            return False

    def clock() -> float:
        return round(time.monotonic() - start, 3)

    def finish(uid: str, status: str, reason: str = "") -> None:
        result[uid].update(status=status, reason=reason, finished=clock())
        job = running.pop(uid)
        if not _finish_environment(job, admission):
            result[uid].update(status="failed", reason="environment cleanup unverified")
            return
        leases.release(job["tokens"], job["holder"])
        shutil.rmtree(job["git_view"], ignore_errors=True)
        _remove_worktree(repo, job["worktree"])
        (root / f"{uid}.pgid").unlink(missing_ok=True)

    def collect(uid: str, job: dict) -> None:
        # Background children must not outlive the worker into the checks.
        _killpg(job["process"].pid)
        code = job["process"].wait()
        spec = units[uid].get("provider")
        if spec:
            output = (root / f"{uid}.log").read_text(errors="replace")
            result[uid]["provider"] = dispatch_providers.result(spec["name"], output)
        if code != 0:
            return finish(uid, "failed", f"exit {code}")
        if spec and result[uid]["provider"]["is_error"]:
            return finish(uid, "failed", "provider reported an error")
        gitdir, tree = job["gitdir"], job["worktree"]
        try:
            _wt(gitdir, tree, "add", "-A")
            changed = _wt(
                gitdir,
                tree,
                "diff",
                "--cached",
                "--no-renames",
                "--name-only",
                "-z",
                job["start"],
            )
        except subprocess.CalledProcessError:
            return finish(uid, "rejected", "worktree damaged")
        paths = _names(changed)
        outside = [p for p in paths if not any(_under(p, o) for o in job["owned"])]
        if outside:
            return finish(uid, "rejected", "outside ownership: " + ", ".join(outside))
        if not leases.valid(job["tokens"], job["holder"]):
            return finish(uid, "rejected", "stale lease")
        patch = _wt(
            gitdir, tree, "diff", "--cached", "--no-renames", "--binary", job["start"]
        )
        # Workers can reach the run folder, so the accepted patch is kept in
        # memory and the file is a record that is never read back.
        patches[uid] = patch
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
        command, profile = u.get("command"), None
        if "provider" in u:
            problem = _brief_problem(repo, plan, owned)
            if problem:
                leases.release(tokens, holder)
                result[u["id"]].update(status="failed", reason=problem)
                return
            command, profile = dispatch_providers.launch(u["provider"])
        tree = root / "wt" / u["id"]
        reservation = None
        spawn_attempted = False
        view = root / "git" / u["id"]
        try:
            budget = _budget(u.get("resource_budget"), timeout)
            reservation = admission.admit(services=(), budget=budget, kind="worker")
            _git(repo, "worktree", "add", "--detach", "-q", str(tree), base)
            gitdir = _git(tree, "rev-parse", "--absolute-git-dir").decode().strip()
            ancestors = _ancestors(units, u["id"])
            for prior in done_order:
                if prior in ancestors and patches[prior]:
                    _wt(gitdir, tree, "apply", "--index", "-", data=patches[prior])
            start_tree = _wt(gitdir, tree, "write-tree").decode().strip()
            _git_view(gitdir, tree, base, view, budget["disk_bytes"])
            env = dict(
                os.environ,
                HY_TASK=str(plan.get("task", "")),
                HY_BRIEF_REVISION=str(plan.get("brief_revision", "")),
                HY_WORK_UNIT=u["id"],
                HY_FENCE=json.dumps(tokens),
            )
            with open(root / f"{u['id']}.log", "wb") as log:
                spawn_attempted = True
                execution = _spawn(
                    command,
                    root=root,
                    name=u["id"],
                    cwd=tree,
                    env=env,
                    stdout=log,
                    admission=admission,
                    budget=budget,
                    kind="worker",
                    reservation=reservation,
                    git_view=view,
                    disk_paths=(tree, view, root / f"{u['id']}.log"),
                    provider=profile,
                )
        except (
            subprocess.CalledProcessError,
            OSError,
            AdmissionError,
            PlanError,
        ) as error:
            safe_cleanup = not spawn_attempted
            if not safe_cleanup and reservation is not None:
                safe_cleanup = not any(
                    row["token"] == reservation["token"] for row in admission.records()
                )
            if safe_cleanup:
                shutil.rmtree(view, ignore_errors=True)
                _remove_worktree(repo, tree)
                if reservation is not None and not spawn_attempted:
                    admission.release(reservation["token"], verify=lambda _: True)
                leases.release(tokens, holder)
            reason = (
                f"setup failed: {error.cmd[3:6]}"
                if isinstance(error, subprocess.CalledProcessError)
                else f"could not start: {error}"
            )
            result[u["id"]].update(status="failed", reason=reason)
            return
        running[u["id"]] = dict(
            **execution,
            git_view=view,
            tokens=tokens,
            holder=holder,
            worktree=tree,
            gitdir=gitdir,
            start=start_tree,
            owned=owned,
            deadline=time.monotonic() + timeout,
        )
        result[u["id"]].update(status="running", started=clock(), fence=tokens)

    try:
        while True:
            if not cancelled and cancel_requested():
                cancelled = True
                for uid, job in list(running.items()):
                    _kill(job["process"])
                    finish(uid, "cancelled", "cancel requested")
            for uid, job in list(running.items()):
                problem = _disk_problem(job["disk_paths"], job["disk_budget"])
                if problem:
                    _kill(job["process"])
                    finish(uid, "failed", problem)
                elif _exited(job["process"]):
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
        owned = [
            posixpath.normpath(p)
            for u in units.values()
            for p in u.get("owned_paths", [])
        ]
        integration = _integrate(
            repo,
            root,
            base,
            done_order,
            plan.get("integration_checks", []),
            patches,
            owned,
            float(plan.get("integration_timeout", DEFAULT_INTEGRATION_TIMEOUT)),
            cancel_requested,
            admission,
            plan.get("integration_resource_budget"),
        )
        cancelled = integration["status"] == "cancelled"
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


def _integrate(
    repo,
    root,
    base,
    order,
    checks,
    patches,
    owned,
    timeout,
    cancel_requested,
    admission,
    resource_budget,
) -> dict:
    """Apply every unit patch on the base and rerun the integration checks."""
    tree = root / "wt" / "integration"
    _git(repo, "worktree", "add", "--detach", "-q", str(tree), base)
    try:
        for uid in order:
            if not patches[uid]:
                continue
            try:
                _git(tree, "apply", "--index", "-", data=patches[uid])
            except subprocess.CalledProcessError:
                return {"status": "failed", "reason": f"{uid} patch does not apply"}
        names = _git(
            tree, "diff", "--cached", "--no-renames", "--name-only", "-z", base
        )
        outside = [p for p in _names(names) if not any(_under(p, o) for o in owned)]
        if outside:
            return {
                "status": "failed",
                "reason": "outside ownership: " + ", ".join(outside),
            }
        combined = _git(tree, "diff", "--cached", "--no-renames", "--binary", base)
        # The run folder is reachable by workers: replace any planted file and
        # give the operator a digest to compare before applying the patch.
        patch = root / "integrated.patch"
        patch.unlink(missing_ok=True)
        with open(patch, "xb") as handle:
            handle.write(combined)
        found = {"patch": str(patch), "sha256": hashlib.sha256(combined).hexdigest()}
        gitdir = _git(tree, "rev-parse", "--absolute-git-dir").decode().strip()
        for number, check in enumerate(checks):
            reservation = None
            spawn_attempted = False
            view = root / "git" / ("integration-" + str(number))
            try:
                budget = _budget(resource_budget, timeout)
                reservation = admission.admit(services=(), budget=budget, kind="worker")
                _git_view(gitdir, tree, base, view, budget["disk_bytes"])
                spawn_attempted = True
                execution = _spawn(
                    check,
                    root=root,
                    name="integration",
                    cwd=tree,
                    env=os.environ.copy(),
                    stdout=subprocess.DEVNULL,
                    admission=admission,
                    budget=budget,
                    kind="worker",
                    reservation=reservation,
                    git_view=view,
                    disk_paths=(tree, view, patch),
                )
                process = execution["process"]
            except (
                OSError,
                AdmissionError,
                PlanError,
                subprocess.CalledProcessError,
            ) as error:
                if not spawn_attempted:
                    shutil.rmtree(view, ignore_errors=True)
                    if reservation is not None:
                        admission.release(reservation["token"], verify=lambda _: True)
                return {
                    "status": "failed",
                    "reason": f"check {check} could not start: {error}",
                    **found,
                }
            deadline = time.monotonic() + timeout
            while not _exited(process):
                problem = _disk_problem(
                    execution["disk_paths"], execution["disk_budget"]
                )
                if problem or cancel_requested() or time.monotonic() > deadline:
                    _kill(process)
                    if _finish_environment(execution, admission):
                        shutil.rmtree(view, ignore_errors=True)
                    if cancel_requested():
                        return {"status": "cancelled", **found}
                    return {
                        "status": "failed",
                        "reason": problem or f"check {check} timeout",
                        **found,
                    }
                time.sleep(TICK)
            problem = _disk_problem(execution["disk_paths"], execution["disk_budget"])
            _killpg(process.pid)
            code = process.wait()
            if not _finish_environment(execution, admission):
                return {
                    "status": "failed",
                    "reason": "environment cleanup unverified",
                    **found,
                }
            shutil.rmtree(view, ignore_errors=True)
            if code != 0 or problem:
                return {
                    "status": "failed",
                    "reason": problem or f"check {check} exit {process.returncode}",
                    **found,
                }
        return {"status": "passed", "checks": len(checks), **found}
    finally:
        _remove_worktree(repo, tree)


def cleanup(repo: Path, state: Path) -> list[str]:
    """Recover recorded owned environments; retain unknown/reused identities."""
    removed = []
    admission = _execution_admission(repo, recovery=True)
    for root in sorted((state / "runs").glob("*")):
        try:
            owner = json.loads((root / "dispatcher.json").read_text())
            if process_status(owner) != "absent":
                continue
        except (OSError, ValueError):
            continue
        records = {r["token"]: r for r in admission.records()}
        recovered = True
        for path in root.glob("*.process.json"):
            try:
                saved = json.loads(path.read_text())
                record = records.get(saved["token"])
                identity = saved["identity"]
                if record is None:
                    if (
                        process_status(identity) == "absent"
                        and _group_absent(identity)
                        and _scope_absent(saved["scope"], saved["token"])
                    ):
                        path.unlink()
                        continue
                    recovered = False
                    continue
                metadata = record.get("metadata", {})
                if (
                    record is None
                    or record["workspace_id"] != admission.workspace_id
                    or record["daemon_id"] != admission.daemon_id
                    or record["kind"] != "worker"
                    or metadata.get("process_file") != str(path)
                    or metadata.get("scope") != saved["scope"]
                ):
                    recovered = False
                    continue
                if (
                    record.get("identity") is not None
                    and record["identity"] != identity
                ):
                    recovered = False
                    continue
                absent = _scope_absent(saved["scope"], saved["token"], stop=True)
                deadline = time.monotonic() + 2
                while (
                    process_status(identity) == "alive" and time.monotonic() < deadline
                ):
                    time.sleep(TICK)
                if not admission.release(
                    saved["token"],
                    verify=lambda _, absent=absent, identity=identity: (
                        absent
                        and process_status(identity) == "absent"
                        and _group_absent(identity)
                    ),
                ):
                    recovered = False
                    continue
                path.unlink()
            except (OSError, ValueError, KeyError, AdmissionError):
                recovered = False
        if not recovered or list(root.glob("*.process.json")):
            continue
        shutil.rmtree(root / "git", ignore_errors=True)
        for pgid in root.glob("*.pgid"):
            pgid.unlink()
        for tree in sorted((root / "wt").glob("*")):
            if _remove_worktree(repo, tree):
                removed.append(str(tree))
        Leases(state).release_run(root.name)
    _git(repo, "worktree", "prune")
    return removed


def main(argv: list[str] | None = None) -> int:
    values = sys.argv[1:] if argv is None else argv
    if len(values) == 4 and values[0] == "--bootstrap":
        return _bootstrap(values[1], int(values[2]), int(values[3]))
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
    except (PlanError, AdmissionError) as error:
        print(f"PLAN_REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "succeeded" else 1


if __name__ == "__main__":
    raise SystemExit(main())
