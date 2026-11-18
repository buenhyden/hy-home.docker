#!/usr/bin/env python3
"""Daily deterministic analysis of captured sessions into reviewable candidates.

Each run reads the capture store read-only over the window since the last
completed run, groups repeated prompts, capture gaps and capture failures,
and records candidates with their source events. A lease with a fencing
token stops a duplicate run, an analysis key makes a repeated window a no-op,
and a missed day is caught up by the next run. Candidates are proposals:
accepting one records a decision and changes no policy, memory or check.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import signal
import socket
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.lib.hooks import session_capture as capture  # noqa: E402

POLICY_EDITION = "1"
STORE_NAME = "analysis.sqlite3"
STATUS_NAME = "analysis-status.json"
LEASE_SECONDS = 900
ATTEMPTS = 2
RETRY_SECONDS = 5
REPEAT_MIN = 3
MAX_SOURCES = 50
UNIT = "hy-home-session-analysis"
ON_CALENDAR = "*-*-* 03:00:00 Asia/Seoul"
EXIT_BUSY = 75
SCHEMA = (
    "CREATE TABLE IF NOT EXISTS lease (singleton INTEGER PRIMARY KEY"
    " CHECK (singleton = 1), token INTEGER NOT NULL, owner TEXT, expires_at TEXT)",
    "CREATE TABLE IF NOT EXISTS runs (analysis_key TEXT PRIMARY KEY, token INTEGER,"
    " trigger TEXT, window_start TEXT, window_end TEXT, started_at TEXT,"
    " finished_at TEXT, state TEXT NOT NULL, reason TEXT, events INTEGER,"
    " candidates INTEGER)",
    "CREATE TABLE IF NOT EXISTS candidates (candidate_id TEXT PRIMARY KEY,"
    " analysis_key TEXT, rule TEXT, pattern TEXT, hypothesis TEXT,"
    " proposed_change TEXT, expected_benefit TEXT, risk TEXT, test_plan TEXT,"
    " frequency INTEGER, conditions TEXT, source_event_ids TEXT,"
    " decision TEXT NOT NULL DEFAULT 'pending', decided_by TEXT, decided_at TEXT)",
)


class Busy(Exception):
    """Another run holds an unexpired lease."""


class Fenced(Exception):
    """The lease moved to another run before this one could commit."""


def now() -> dt.datetime:
    return dt.datetime.now(dt.UTC)


def stamp(value: dt.datetime) -> str:
    return value.isoformat(timespec="seconds")


def digest(*parts: object) -> str:
    return hashlib.sha256("\0".join(map(str, parts)).encode()).hexdigest()


def connect(directory: Path) -> sqlite3.Connection:
    capture.connect(directory).close()  # the same private directory checks
    path = directory / STORE_NAME
    if path.is_symlink():
        raise OSError("analysis store is a symbolic link")
    connection = sqlite3.connect(path, timeout=1.0, isolation_level=None)
    os.chmod(path, 0o600)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA busy_timeout = 1000")
    connection.execute("PRAGMA journal_mode = DELETE")
    for statement in SCHEMA:
        connection.execute(statement)
    return connection


def acquire(connection: sqlite3.Connection, owner: str) -> int:
    connection.execute("BEGIN IMMEDIATE")
    try:
        row = connection.execute("SELECT * FROM lease").fetchone()
        if row and row["owner"] and row["expires_at"] > stamp(now()):
            raise Busy(f"lease held by {row['owner']} until {row['expires_at']}")
        token = (row["token"] if row else 0) + 1
        expires = stamp(now() + dt.timedelta(seconds=LEASE_SECONDS))
        connection.execute(
            "INSERT INTO lease VALUES (1, ?, ?, ?) ON CONFLICT(singleton) DO UPDATE"
            " SET token=excluded.token, owner=excluded.owner,"
            " expires_at=excluded.expires_at",
            (token, owner, expires),
        )
        connection.execute("COMMIT")
        return token
    except BaseException:
        connection.execute("ROLLBACK")
        raise


def release(connection: sqlite3.Connection, token: int) -> None:
    connection.execute(
        "UPDATE lease SET owner=NULL, expires_at=NULL WHERE token=?", (token,)
    )


def read_capture(directory: Path, start: str | None) -> tuple[list[dict], list[dict]]:
    """Events after the window start and the sessions they belong to."""
    path = directory / capture.STORE_NAME
    if not path.is_file():
        return [], []
    source = sqlite3.connect(path.absolute().as_uri() + "?mode=ro", uri=True)
    source.row_factory = sqlite3.Row
    try:
        events = [
            dict(row)
            for row in source.execute(
                "SELECT event_id, provider, session_id, event_kind, captured_at,"
                " prompt FROM events WHERE captured_at > ? ORDER BY captured_at",
                (start or "",),
            )
        ]
        sessions = [dict(row) for row in source.execute("SELECT * FROM sessions")]
    finally:
        source.close()
    return events, sessions


def failures(directory: Path, start: str | None, end: str) -> list[str]:
    log = directory / "degraded.log"
    if not log.exists():
        return []
    lines = log.read_text(encoding="utf-8").splitlines()
    return [line for line in lines if (start or "") < line[:25] <= end]


def _candidate(rule, key, members, conditions, **text) -> dict:
    return {
        "rule": rule,
        "key": key,
        "pattern": key[:160],
        "events": members,
        "conditions": conditions,
        **text,
    }


def aggregate(
    events: list[dict], sessions: list[dict], failed: list[str]
) -> list[dict]:
    """Deterministic rules; every candidate names the events behind it."""
    found = []
    groups: dict[str, list[dict]] = {}
    for event in events:
        if event["event_kind"] == "UserPromptSubmit" and event["prompt"]:
            text = re.sub(r"\s+", " ", event["prompt"].casefold()).strip()
            if len(text) >= 8:
                groups.setdefault(text[:500], []).append(event)
    for text, members in sorted(groups.items()):
        if len(members) >= REPEAT_MIN:
            found.append(
                _candidate(
                    "repeated-prompt",
                    text,
                    members,
                    f"{len({m['session_id'] for m in members})} sessions",
                    hypothesis="The same instruction is typed repeatedly; this is a"
                    " hypothesis, not a confirmed cause.",
                    proposed_change="Review whether a skill, a reusable prompt or a"
                    " reviewed memory record would replace the repetition.",
                    expected_benefit="Fewer repeated instructions per session.",
                    risk="Repetition may be intentional; a shortcut may hide"
                    " per-request differences.",
                    test_plan="Compare the repetition count over the next two windows"
                    " after any adopted change.",
                )
            )
    latest = {(e["provider"], e["session_id"]): e for e in events}
    gaps: dict[str, list[dict]] = {}
    for session in sessions:
        key = (session["provider"], session["session_id"])
        if session["completeness"] != "complete" and key in latest:
            reason = session["reason"] or (
                "unknown" if session["last_reconciled"] else "not yet reconciled"
            )
            reason = reason.split(";")[0]
            reason = re.sub(r"^\d+ ", "", reason.strip())
            gaps.setdefault(f"{session['provider']}: {reason}", []).append(latest[key])
    for reason, members in sorted(gaps.items()):
        found.append(
            _candidate(
                "capture-gap",
                reason,
                members,
                f"{len(members)} sessions",
                hypothesis="Capture of these sessions is incomplete for the stated reason.",
                proposed_change="Check the provider's capture path for this reason.",
                expected_benefit="More sessions reach complete capture.",
                risk="Some reasons are provider limits that cannot be removed.",
                test_plan="Reconcile again and compare the completeness counts.",
            )
        )
    counts: dict[str, int] = {}
    for line in failed:
        reason = line[26:].strip() or "unknown"
        counts[reason] = counts.get(reason, 0) + 1
    for reason, count in sorted(counts.items()):
        found.append(
            _candidate(
                "capture-failure",
                reason,
                [],
                f"{count} failures",
                hypothesis="The capture hook failed for this reason.",
                proposed_change="Diagnose the failure in the capture module.",
                expected_benefit="No silent capture loss.",
                risk="A fix must not slow or change the hook result.",
                test_plan="Reproduce the failure in a capture test.",
            )
        )
    return found


def record(connection, analysis_key: str, found: list[dict]) -> None:
    for item in found:
        candidate_id = digest(item["rule"], item["key"])
        sources = [event["event_id"] for event in item["events"]][:MAX_SOURCES]
        frequency = len(item["events"]) or int(item["conditions"].split()[0])
        existing = connection.execute(
            "SELECT decision, frequency FROM candidates WHERE candidate_id=?",
            (candidate_id,),
        ).fetchone()
        if existing is None:
            connection.execute(
                "INSERT INTO candidates (candidate_id, analysis_key, rule, pattern,"
                " hypothesis, proposed_change, expected_benefit, risk, test_plan,"
                " frequency, conditions, source_event_ids)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    candidate_id,
                    analysis_key,
                    item["rule"],
                    item["pattern"],
                    item["hypothesis"],
                    item["proposed_change"],
                    item["expected_benefit"],
                    item["risk"],
                    item["test_plan"],
                    frequency,
                    item["conditions"],
                    json.dumps(sources),
                ),
            )
        elif existing["decision"] == "pending":
            # A decided candidate keeps its decision; a pending one accumulates.
            connection.execute(
                "UPDATE candidates SET analysis_key=?, frequency=?, conditions=?,"
                " source_event_ids=? WHERE candidate_id=?",
                (
                    analysis_key,
                    existing["frequency"] + frequency,
                    item["conditions"],
                    json.dumps(sources),
                    candidate_id,
                ),
            )


def write_status(directory: Path, status: dict) -> None:
    path = directory / STATUS_NAME
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(status, indent=2), encoding="utf-8")
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)


def _cancel(signum, frame):
    raise KeyboardInterrupt


def run(directory: Path, trigger: str) -> dict:
    connection = connect(directory)
    started = now()
    status = {"trigger": trigger, "started_at": stamp(started)}
    try:
        token = acquire(connection, f"{socket.gethostname()}:{os.getpid()}")
    except Busy as error:
        connection.close()
        status.update(state="skipped", reason=f"duplicate run: {error}")
        write_status(directory, status)
        return status
    previous = signal.signal(signal.SIGTERM, _cancel)
    analysis_key = None
    try:
        last = connection.execute(
            "SELECT max(window_end) FROM runs WHERE state='complete'"
        ).fetchone()[0]
        for attempt in range(1, ATTEMPTS + 1):
            try:
                events, sessions = read_capture(directory, last)
                break
            except sqlite3.OperationalError:
                if attempt == ATTEMPTS:
                    raise
                time.sleep(RETRY_SECONDS)
        end = max((e["captured_at"] for e in events), default=last or stamp(started))
        analysis_key = digest(directory.parent, last, end, POLICY_EDITION)
        status.update(window_start=last, window_end=end)
        if not events:
            release(connection, token)
            status.update(state="complete", reason="no new captured events")
            return status
        found = aggregate(events, sessions, failures(directory, last, end))
        connection.execute("BEGIN IMMEDIATE")
        current = connection.execute("SELECT token FROM lease").fetchone()[0]
        if current != token:
            raise Fenced(f"lease token {current} replaced {token}")
        record(connection, analysis_key, found)
        connection.execute(
            "INSERT OR REPLACE INTO runs VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (
                analysis_key,
                token,
                trigger,
                last,
                end,
                stamp(started),
                stamp(now()),
                "complete",
                None,
                len(events),
                len(found),
            ),
        )
        release(connection, token)
        connection.execute("COMMIT")
        status.update(state="complete", events=len(events), candidates=len(found))
        return status
    except KeyboardInterrupt:
        status.update(state="cancelled", reason="cancelled by signal")
        raise
    except Fenced as error:
        status.update(state="fenced", reason=str(error))
        raise
    except Exception as error:
        status.update(state="failed", reason=f"{type(error).__name__}: {error}")
        raise
    finally:
        signal.signal(signal.SIGTERM, previous)
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        if status.get("state") in ("cancelled", "failed"):
            release(connection, token)
        connection.close()
        status["finished_at"] = stamp(now())
        write_status(directory, status)


def candidates(directory: Path, everything: bool) -> list[dict]:
    connection = connect(directory)
    try:
        where = "" if everything else " WHERE decision='pending'"
        rows = connection.execute(
            "SELECT * FROM candidates" + where + " ORDER BY frequency DESC, rule"
        )
        return [
            {**dict(row), "source_event_ids": json.loads(row["source_event_ids"])}
            for row in rows
        ]
    finally:
        connection.close()


def decide(directory: Path, candidate_id: str, decision: str, owner: str) -> dict:
    """Record a review decision; it adopts nothing by itself."""
    connection = connect(directory)
    try:
        changed = connection.execute(
            "UPDATE candidates SET decision=?, decided_by=?, decided_at=?"
            " WHERE candidate_id=? AND decision='pending'",
            (decision, owner, stamp(now()), candidate_id),
        ).rowcount
    finally:
        connection.close()
    if not changed:
        raise LookupError("no pending candidate with that ID")
    return {"candidate_id": candidate_id, "decision": decision}


def install_timer(unit_dir: Path, on_calendar: str = ON_CALENDAR) -> dict:
    """Write the user service and timer and enable the timer."""
    unit_dir.mkdir(parents=True, exist_ok=True)
    service = (
        "[Unit]\nDescription=hy-home session analysis\n\n[Service]\nType=oneshot\n"
        f"WorkingDirectory={ROOT}\n"
        f"ExecStart=/usr/bin/python3 {ROOT}/scripts/operations/session_analysis.py"
        " run --trigger scheduled\nTimeoutStartSec=600\nNice=10\n"
    )
    timer = (
        "[Unit]\nDescription=Daily hy-home session analysis\n\n[Timer]\n"
        f"OnCalendar={on_calendar}\nPersistent=true\nAccuracySec=1min\n\n"
        "[Install]\nWantedBy=timers.target\n"
    )
    (unit_dir / f"{UNIT}.service").write_text(service, encoding="utf-8")
    (unit_dir / f"{UNIT}.timer").write_text(timer, encoding="utf-8")
    for command in (("daemon-reload",), ("enable", "--now", f"{UNIT}.timer")):
        subprocess.run(["systemctl", "--user", *command], check=True, timeout=30)
    return {"timer": f"{UNIT}.timer", "on_calendar": on_calendar}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    runner = commands.add_parser("run")
    runner.add_argument("--trigger", choices=("manual", "scheduled"), default="manual")
    commands.add_parser("status")
    listing = commands.add_parser("candidates")
    listing.add_argument("--all", action="store_true")
    deciding = commands.add_parser("decide")
    deciding.add_argument("candidate_id")
    deciding.add_argument("decision", choices=("accepted", "rejected"))
    deciding.add_argument("--owner", required=True)
    commands.add_parser("install-timer")
    args = parser.parse_args(argv)
    directory = capture.capture_dir()
    try:
        if args.command == "run":
            result = run(directory, args.trigger)
        elif args.command == "status":
            path = directory / STATUS_NAME
            result = (
                json.loads(path.read_text())
                if path.exists()
                else {"state": "never-run"}
            )
        elif args.command == "candidates":
            result = candidates(directory, args.all)
        elif args.command == "decide":
            result = decide(directory, args.candidate_id, args.decision, args.owner)
        else:
            result = install_timer(Path.home() / ".config" / "systemd" / "user")
    except (Fenced, KeyboardInterrupt) as error:
        print(f"SESSION_ANALYSIS_STOPPED: {type(error).__name__}", file=sys.stderr)
        return 1
    except LookupError as error:
        print(f"SESSION_ANALYSIS_NOT_FOUND: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if isinstance(result, dict) and result.get("state") == "skipped":
        return EXIT_BUSY
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
