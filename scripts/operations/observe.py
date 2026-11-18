#!/usr/bin/env python3
"""Join what the agent tools and scheduled jobs left in one time window.

`report` reads, without writing, the capture, analysis and forecast stores,
the dispatch run reports and the journal of the scheduled units, and counts
what happened between `--since` and `--until` (default: the last 24 hours).
Every failure names its owner and the next step. Journal lines are only
counted, and fields that workers can write are echoed only in a fixed shape, so no log text, prompt
or secret is copied into the report. A store that cannot be read, a journal
that hides lines, and a daily unit with no run in a window of a day or more
are failures, not zeros; a day here is 29 hours, for the timer delay and run time. The report states its own run time as the
observation cost, and what it cannot measure. It is an on-demand view,
never a gate and never an approval.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.lib.hooks import session_capture as capture  # noqa: E402
from scripts.operations.agent_memory import MemoryStoreError  # noqa: E402

RUNBOOK = "RUN-0021"
# unit -> (journal scope, owner, next step); each runs at least once a day.
WATCHED = {
    "hyhome-backup.service": (
        "system",
        f"{RUNBOOK} backup / @buenhyden",
        f"journalctl -u hyhome-backup.service; {RUNBOOK} step 4 and step 7",
    ),
    "hy-home-session-analysis.service": (
        "user",
        "ENVIRONMENT-CONSTRAINTS session analysis / @buenhyden",
        "journalctl --user -u hy-home-session-analysis.service;"
        " session_analysis.py status",
    ),
}
CAPTURE_OWNER = "ENVIRONMENT-CONSTRAINTS session capture / @buenhyden"
ANALYSIS_OWNER = WATCHED["hy-home-session-analysis.service"][1]
DISPATCH_OWNER = "TSK-0090 dispatcher"
TASK_REF = re.compile(r"SPEC-\d{4}-TSK-\d{4}")
RUN_ID = re.compile(r"\d{8}T\d{6}-[0-9a-f]{6}")
RUN_STATES = ("succeeded", "failed", "cancelled")
FAILED_ANALYSIS = ("failed", "cancelled", "fenced")
RESTRICTED = "not seeing messages from other users"
# A daily unit may start up to 30 minutes late and run up to 4 hours, so two
# finished runs can lie further apart than one day.
MISSED_RUN_WINDOW = dt.timedelta(hours=29)
UNMEASURED = [
    "queue wait before each job starts",
    "context loading inside agents and reviewers",
    "token and money cost",
    "analysis runs before the last one that ended other than complete",
]


class StoreUnavailable(Exception):
    """A store that exists but cannot be read as one."""


def _when(value: str) -> dt.datetime:
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError(f"time needs a UTC offset: {value}")
    return parsed


def _in(value, since: dt.datetime, until: dt.datetime) -> bool:
    try:
        return isinstance(value, str) and since <= _when(value) < until
    except ValueError:
        return False


def _rows(path: Path, query: str) -> list[sqlite3.Row]:
    """Rows from a store opened read-only; [] when it does not exist."""
    if not path.exists() and not path.is_symlink():
        return []
    if path.is_symlink() or not path.is_file():
        raise StoreUnavailable(path.name)
    try:
        connection = sqlite3.connect(path.absolute().as_uri() + "?mode=ro", uri=True)
        connection.row_factory = sqlite3.Row
        try:
            return connection.execute(query).fetchall()
        finally:
            connection.close()
    except sqlite3.Error as error:
        raise StoreUnavailable(path.name) from error


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
    if RESTRICTED in done.stderr:
        raise OSError("journal hides other users' and system lines")
    return done.stdout.splitlines()


def _reason(text: str | None) -> str:
    """A capture reason without the counts it embeds, so one cause is one row."""
    return re.sub(r"\b\d+ ", "", text or "unknown").strip()


def report(directory: Path, since: str, until: str, journal=system_journal) -> dict:
    started = time.monotonic()
    low, high = _when(since), _when(until)
    if low >= high:
        raise ValueError("--since must be earlier than --until")
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

    unavailable: set[str] = set()

    def rows(source: str, owner: str, name: str, query: str) -> list[sqlite3.Row]:
        try:
            return _rows(directory / name, query)
        except StoreUnavailable:
            if name not in unavailable:
                unavailable.add(name)
                fail(
                    source, f"{name} unavailable", 1, owner, f"check {directory / name}"
                )
            return []

    # Capture: events and the incomplete sessions active inside the window.
    events = rows(
        "capture", CAPTURE_OWNER, capture.STORE_NAME,
        "SELECT session_id, occurred_at FROM events",
    )  # fmt: skip
    active = {row["session_id"] for row in events if _in(row["occurred_at"], low, high)}
    sessions = rows(
        "capture", CAPTURE_OWNER, capture.STORE_NAME,
        "SELECT session_id, completeness, reason FROM sessions",
    )  # fmt: skip
    incomplete = collections.Counter(
        _reason(row["reason"])
        for row in sessions
        if row["completeness"] != "complete" and row["session_id"] in active
    )
    degraded = directory / "degraded.log"
    try:
        lines = (
            degraded.read_text(encoding="utf-8").splitlines()
            if degraded.is_file()
            else []
        )
    except (OSError, UnicodeDecodeError):
        lines = []
        fail("capture", "degraded.log unavailable", 1, CAPTURE_OWNER,
             f"check {degraded}")  # fmt: skip
    degraded_count = sum(_in(line[:25], low, high) for line in lines)
    result = {
        "since": since,
        "until": until,
        "capture": {
            "events": sum(_in(row["occurred_at"], low, high) for row in events),
            "incomplete_sessions": sum(incomplete.values()),
            "capture_failures": degraded_count,
        },
    }
    for reason, count in sorted(incomplete.items()):
        fail(
            "capture", reason, count, CAPTURE_OWNER,
            "session_capture status; decide the capture-gap candidate",
        )  # fmt: skip
    if degraded_count:
        fail(
            "capture", "degraded.log", degraded_count, CAPTURE_OWNER,
            "read .workspace-capture/degraded.log",
        )  # fmt: skip

    # Analysis: the runs table holds complete runs only; the status file holds
    # the last run whatever its end.
    runs = rows(
        "analysis", ANALYSIS_OWNER, "analysis.sqlite3",
        "SELECT state, started_at FROM runs",
    )  # fmt: skip
    run_states = collections.Counter(
        row["state"] for row in runs if _in(row["started_at"], low, high)
    )
    pending = rows(
        "analysis", ANALYSIS_OWNER, "analysis.sqlite3",
        "SELECT COUNT(*) AS n FROM candidates WHERE decision = 'pending'",
    )  # fmt: skip
    status_path = directory / "analysis-status.json"
    last = None
    if status_path.is_symlink() or (status_path.exists() and not status_path.is_file()):
        fail("analysis", "analysis-status.json unavailable", 1, ANALYSIS_OWNER,
             f"check {status_path}")  # fmt: skip
    elif status_path.is_file():
        try:
            status = json.loads(status_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            status = None
            fail("analysis", "analysis-status.json unreadable", 1, ANALYSIS_OWNER,
                 "session_analysis.py status")  # fmt: skip
        if isinstance(status, dict) and _in(status.get("started_at"), low, high):
            state = status.get("state")
            last = (
                state
                if state in (*FAILED_ANALYSIS, "complete", "skipped")
                else "unknown"
            )
            if last in FAILED_ANALYSIS or last == "unknown":
                fail("analysis", f"last run {last}", 1, ANALYSIS_OWNER,
                     "session_analysis.py status")  # fmt: skip
    result["analysis"] = {
        "runs": dict(run_states),
        "last_status": last,
        "pending_candidates": pending[0]["n"] if pending else 0,
    }

    # Forecast outcomes recorded inside the window.
    outcomes = [
        row
        for row in rows(
            "forecast",
            "TSK-0089 forecast",
            "forecast.sqlite3",
            "SELECT task_ref, status, observed_at FROM outcomes",
        )
        if _in(row["observed_at"], low, high)
    ]
    result["forecast"] = {
        "outcomes": dict(collections.Counter(r["status"] for r in outcomes))
    }
    for row in outcomes:
        if row["status"] == "failed":
            # Any worktree can record a forecast, so the reference is a claim.
            ref = row["task_ref"]
            known = isinstance(ref, str) and TASK_REF.fullmatch(ref)
            fail("forecast", f"task {ref if known else 'with an unrecognised reference'} failed",
                 1, ref if known else "TSK-0089 forecast", "the task's own record")  # fmt: skip

    # Dispatch reports sit in a folder workers can write: read them as claims
    # and echo only values that match a fixed shape.
    dispatched = collections.Counter()
    for path in sorted((directory / "dispatch" / "runs").glob("*/report.json")):
        name = (
            path.parent.name
            if RUN_ID.fullmatch(path.parent.name)
            else "unrecognised run folder"
        )
        try:
            modified = dt.datetime.fromtimestamp(path.stat().st_mtime, dt.UTC)
            if not low <= modified < high:
                continue
            run = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(run, dict):
                raise ValueError("not an object")
        except (OSError, ValueError):
            fail("dispatch", f"{name} unreadable", 1, DISPATCH_OWNER,
                 "inspect that run folder")  # fmt: skip
            continue
        status = run.get("status") if run.get("status") in RUN_STATES else "unknown"
        task = run.get("task")
        owner = (
            task
            if isinstance(task, str) and TASK_REF.fullmatch(task)
            else DISPATCH_OWNER
        )
        dispatched[status] += 1
        if status not in ("succeeded", "cancelled"):
            fail("dispatch", f"{name} {status}", 1, owner,
                 "work_dispatch.py report in that run folder")  # fmt: skip
    result["dispatch"] = {"runs": dict(dispatched)}

    # Scheduled units: count, never copy, journal lines.
    daily = high - low >= MISSED_RUN_WINDOW
    units = {}
    for unit, (scope, owner, step) in WATCHED.items():
        try:
            lines = journal(unit, scope, since, until)
        except OSError:
            units[unit] = {"state": "unreadable"}
            fail("unit", unit, 1, owner,
                 "the journal could not be read in full; check it with access to it")  # fmt: skip
            continue
        failed = sum("Failed with result" in line for line in lines)
        succeeded = sum(line.startswith("Finished ") for line in lines)
        units[unit] = {"state": "read", "failed": failed, "succeeded": succeeded}
        if failed:
            fail("unit", unit, failed, owner, step)
        elif daily and not succeeded:
            fail("unit", unit, 1, owner,
                 "no finished or failed run in the window; check the timer and"
                 f" systemctl status {unit}")  # fmt: skip
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
    except (ValueError, OSError, sqlite3.Error, MemoryStoreError) as error:
        print(f"OBSERVE_REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
