#!/usr/bin/env python3
"""Join what the agent tools and scheduled jobs left in one time window.

`report` reads, without writing, the capture, analysis and forecast stores,
the dispatch run reports and the journal of the scheduled units, and counts
what happened between `--since` and `--until` (default: the last 24 hours).
Every failure names its owner and the next step. Journal lines are only
counted; no log text, prompt or secret is copied into the report. The
report states its own run time as the observation cost, and what it cannot
measure. It is an on-demand view, never a gate and never an approval.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.lib.hooks import session_capture as capture  # noqa: E402

RUNBOOK = "RUN-0021"
# unit -> (journal scope, owner, next step)
WATCHED = {
    "hyhome-backup.service": (
        "system",
        f"{RUNBOOK} backup / @buenhyden",
        f"journalctl -u hyhome-backup.service; {RUNBOOK} step 1 and step 7",
    ),
    "hy-home-session-analysis.service": (
        "user",
        "ENVIRONMENT-CONSTRAINTS session analysis / @buenhyden",
        "journalctl --user -u hy-home-session-analysis.service; session_analysis.py status",
    ),
}
CAPTURE_OWNER = "ENVIRONMENT-CONSTRAINTS session capture / @buenhyden"
ANALYSIS_OWNER = WATCHED["hy-home-session-analysis.service"][1]
UNMEASURED = [
    "queue wait before each job starts",
    "context loading inside agents and reviewers",
    "token and money cost",
]


def _when(value: str) -> dt.datetime:
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError(f"time needs a UTC offset: {value}")
    return parsed


def _in(value: str | None, since: dt.datetime, until: dt.datetime) -> bool:
    try:
        return value is not None and since <= _when(value) < until
    except ValueError:
        return False


def _readonly(path: Path) -> sqlite3.Connection | None:
    if not path.is_file() or path.is_symlink():
        return None
    connection = sqlite3.connect(path.absolute().as_uri() + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def _rows(path: Path, query: str) -> list[sqlite3.Row]:
    connection = _readonly(path)
    if connection is None:
        return []
    try:
        return connection.execute(query).fetchall()
    finally:
        connection.close()


def system_journal(unit: str, scope: str, since: str, until: str) -> list[str]:
    stamp = "%Y-%m-%d %H:%M:%S UTC"
    command = ["journalctl", "--no-pager", "-o", "cat", "-u", unit]
    if scope == "user":
        command.insert(1, "--user")
    command += [
        "--since", _when(since).astimezone(dt.UTC).strftime(stamp),
        "--until", _when(until).astimezone(dt.UTC).strftime(stamp),
    ]  # fmt: skip
    done = subprocess.run(command, capture_output=True, text=True, check=False)
    if done.returncode != 0:
        raise OSError(f"journalctl exited {done.returncode}")
    return done.stdout.splitlines()


def report(directory: Path, since: str, until: str, journal=system_journal) -> dict:
    started = time.monotonic()
    low, high = _when(since), _when(until)
    failures = []

    def fail(source: str, item: str, count: int, owner: str, step: str) -> None:
        failures.append(
            {
                "source": source,
                "item": item,
                "count": count,
                "owner": owner,
                "next": step,
            }
        )

    events = _rows(directory / capture.STORE_NAME, "SELECT occurred_at FROM events")
    sessions = _rows(
        directory / capture.STORE_NAME, "SELECT completeness, reason FROM sessions"
    )
    incomplete = collections.Counter(
        row["reason"] or "unknown"
        for row in sessions
        if row["completeness"] != "complete"
    )
    degraded = directory / "degraded.log"
    degraded_lines = [
        line
        for line in (
            degraded.read_text(encoding="utf-8").splitlines()
            if degraded.is_file()
            else []
        )
        if _in(line[:25], low, high)
    ]
    result = {
        "since": since,
        "until": until,
        "capture": {
            "events": sum(_in(row["occurred_at"], low, high) for row in events),
            "incomplete_sessions": sum(incomplete.values()),
            "capture_failures": len(degraded_lines),
        },
    }
    for reason, count in sorted(incomplete.items()):
        fail(
            "capture",
            reason,
            count,
            CAPTURE_OWNER,
            "session_capture status; decide the capture-gap candidate",
        )
    if degraded_lines:
        fail(
            "capture",
            "degraded.log",
            len(degraded_lines),
            CAPTURE_OWNER,
            "read .workspace-capture/degraded.log",
        )

    runs = [
        row
        for row in _rows(
            directory / "analysis.sqlite3", "SELECT state, started_at FROM runs"
        )
        if _in(row["started_at"], low, high)
    ]
    run_states = collections.Counter(row["state"] for row in runs)
    pending = _rows(
        directory / "analysis.sqlite3",
        "SELECT COUNT(*) AS n FROM candidates WHERE decision = 'pending'",
    )
    result["analysis"] = {
        "runs": dict(run_states),
        "pending_candidates": pending[0]["n"] if pending else 0,
    }
    for state, count in sorted(run_states.items()):
        if state != "complete":
            fail(
                "analysis",
                f"run {state}",
                count,
                ANALYSIS_OWNER,
                "session_analysis.py status",
            )

    outcomes = [
        row
        for row in _rows(
            directory / "forecast.sqlite3",
            "SELECT task_ref, status, observed_at FROM outcomes",
        )
        if _in(row["observed_at"], low, high)
    ]
    result["forecast"] = {
        "outcomes": dict(collections.Counter(r["status"] for r in outcomes))
    }
    for row in outcomes:
        if row["status"] == "failed":
            fail(
                "forecast",
                f"task {row['task_ref']} failed",
                1,
                row["task_ref"],
                "the task's own record",
            )

    # Run reports sit in a folder workers can write; they are read as claims.
    dispatched = collections.Counter()
    for path in sorted((directory / "dispatch" / "runs").glob("*/report.json")):
        modified = dt.datetime.fromtimestamp(path.stat().st_mtime, dt.UTC)
        if not low <= modified < high:
            continue
        try:
            run = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            fail(
                "dispatch",
                path.parent.name,
                1,
                "TSK-0090 dispatcher",
                "unreadable run report",
            )
            continue
        status = str(run.get("status", "unknown"))
        dispatched[status] += 1
        if status not in ("succeeded", "cancelled"):
            fail(
                "dispatch",
                f"run {path.parent.name} {status}",
                1,
                str(run.get("task") or "TSK-0090 dispatcher"),
                "work_dispatch.py report in that run folder",
            )
    result["dispatch"] = {"runs": dict(dispatched)}

    units = {}
    for unit, (scope, owner, step) in WATCHED.items():
        try:
            lines = journal(unit, scope, since, until)
        except OSError:
            units[unit] = {"state": "unreadable"}
            fail(
                "unit",
                unit,
                1,
                owner,
                "the journal could not be read; check it by hand",
            )
            continue
        failed = sum("Failed with result" in line for line in lines)
        succeeded = sum(line.startswith("Finished ") for line in lines)
        units[unit] = {"state": "read", "failed": failed, "succeeded": succeeded}
        if failed:
            fail("unit", unit, failed, owner, step)
    result["units"] = units
    result["failures"] = failures
    result["unmeasured"] = UNMEASURED
    result["observed_at"] = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    result["cost_seconds"] = round(time.monotonic() - started, 3)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    show = commands.add_parser("report")
    now = dt.datetime.now(dt.UTC)
    show.add_argument(
        "--since", default=(now - dt.timedelta(days=1)).isoformat(timespec="seconds")
    )
    show.add_argument("--until", default=now.isoformat(timespec="seconds"))
    args = parser.parse_args(argv)
    try:
        result = report(capture.capture_dir(), args.since, args.until)
    except (ValueError, OSError, sqlite3.Error) as error:
        print(f"OBSERVE_REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
