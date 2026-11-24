#!/usr/bin/env python3
"""Daily deterministic analysis of captured sessions into reviewable candidates.

Each run expires captured content and old candidates, then reads at most
MAX_EVENTS captured events after the last committed ingest sequence and the
failure log after its byte offset. It groups repeated prompts, corrections
after a response, capture gaps and capture failures into candidates whose
source events accumulate, and commits them with the new cursor in one
transaction. A lease with a fencing token stops a duplicate run, a lost cursor
only redelivers events already counted, and the unread backlog is reported. Candidates are proposals: an
accepted decision and its promotion intent are recorded together, and the
outbox writes one unreviewed `candidate` memory record per decision through the
memory CLI with a stable request key. Raw captured text is never copied, and
no policy, skill or check changes.
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
from scripts.operations import work_dispatch  # noqa: E402

POLICY_EDITION = "1"
STORE_NAME = "analysis.sqlite3"
STATUS_NAME = "analysis-status.json"
LEASE_SECONDS = 900
ATTEMPTS = 2
RETRY_SECONDS = 5
REPEAT_MIN = 3
MAX_EVENTS = 5000
CANDIDATE_DAYS = 90
CLOSED_CANDIDATE_DAYS = 30
LEGACY_UNIT = "hy-home-session-analysis"
CORRECTION_CUES = (
    "no,", "no.", "wrong", "that's not", "that is not", "not what i",
    "아니", "틀렸", "잘못",
)  # fmt: skip
ON_CALENDAR = "*-*-* 03:00:00 Asia/Seoul"
EXIT_BUSY = 75
SCHEMA = (
    "CREATE TABLE IF NOT EXISTS lease (singleton INTEGER PRIMARY KEY"
    " CHECK (singleton = 1), token INTEGER NOT NULL, owner TEXT, expires_at TEXT)",
    "CREATE TABLE IF NOT EXISTS runs (analysis_key TEXT PRIMARY KEY, token INTEGER,"
    " trigger TEXT, window_start TEXT, window_end TEXT, started_at TEXT,"
    " finished_at TEXT, state TEXT NOT NULL, reason TEXT, events INTEGER,"
    " candidates INTEGER, cursor_start INTEGER, cursor_end INTEGER,"
    " log_offset INTEGER, log_head TEXT, backlog INTEGER)",
    "CREATE TABLE IF NOT EXISTS candidates (candidate_id TEXT PRIMARY KEY,"
    " analysis_key TEXT, rule TEXT, pattern TEXT, hypothesis TEXT,"
    " proposed_change TEXT, expected_benefit TEXT, risk TEXT, test_plan TEXT,"
    " frequency INTEGER, conditions TEXT, source_event_ids TEXT,"
    " decision TEXT NOT NULL DEFAULT 'pending', decided_by TEXT, decided_at TEXT,"
    " created_at TEXT, pattern_expires_at TEXT, task_ref TEXT, check_ref TEXT,"
    " effect TEXT, effect_sample INTEGER, effect_at TEXT)",
    # The promotion outbox: one intent per accepted, reviewed candidate.
    "CREATE TABLE IF NOT EXISTS promotions (candidate_id TEXT PRIMARY KEY,"
    " review_digest TEXT NOT NULL, request TEXT NOT NULL,"
    " state TEXT NOT NULL DEFAULT 'pending', memory_revision INTEGER,"
    " attempts INTEGER NOT NULL DEFAULT 0, last_error TEXT,"
    " created_at TEXT NOT NULL, settled_at TEXT)",
)
# The reviewed fields a promotion is bound to; `pattern` holds captured text.
REVIEWED = (
    "rule",
    "hypothesis",
    "proposed_change",
    "expected_benefit",
    "risk",
    "test_plan",
    "frequency",
    "conditions",
    "source_event_ids",
    "decision",
    "decided_by",
    "decided_at",
)
MEMORY_CLI = ROOT / "scripts/operations/agent_memory.py"


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
    _migrate(connection)
    return connection


ADDED = {
    "runs": ("cursor_start INTEGER", "cursor_end INTEGER", "log_offset INTEGER",
             "log_head TEXT", "backlog INTEGER"),
    "candidates": ("created_at TEXT", "pattern_expires_at TEXT", "task_ref TEXT",
                   "check_ref TEXT", "effect TEXT", "effect_sample INTEGER",
                   "effect_at TEXT"),
}  # fmt: skip


def _migrate(connection: sqlite3.Connection) -> None:
    """Add the cursor and expiry columns to a store written before them."""
    for table, columns in ADDED.items():
        present = {row[1] for row in connection.execute(f"PRAGMA table_info({table})")}
        for column in columns:
            if column.split()[0] not in present:
                connection.execute(f"ALTER TABLE {table} ADD COLUMN {column}")
    # Earlier candidates start their lives at their run; their captured pattern
    # expires 30 days after that run's window.
    connection.execute(
        "UPDATE candidates SET created_at=coalesce((SELECT started_at FROM runs r"
        " WHERE r.analysis_key=candidates.analysis_key), ?) WHERE created_at IS NULL",
        (stamp(now()),),
    )
    connection.execute(
        "UPDATE candidates SET pattern_expires_at=strftime('%Y-%m-%dT%H:%M:%S+00:00',"
        " coalesce((SELECT window_end FROM runs r WHERE"
        " r.analysis_key=candidates.analysis_key), created_at), ?)"
        " WHERE pattern_expires_at IS NULL AND rule='repeated-prompt'"
        " AND pattern IS NOT NULL",
        (f"+{capture.CONTENT_DAYS} days",),
    )


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


def _cursor(connection, directory: Path) -> tuple[int, int, str | None]:
    """The last committed event sequence and failure-log offset."""
    row = connection.execute(
        "SELECT cursor_end, log_offset, log_head, window_end FROM runs"
        " WHERE state='complete' ORDER BY cursor_end IS NULL, cursor_end DESC,"
        " window_end DESC LIMIT 1"
    ).fetchone()
    if row is None:
        return 0, 0, None
    if row["cursor_end"] is not None:
        return row["cursor_end"], row["log_offset"] or 0, row["log_head"]
    # A run before the sequence cursor: events up to its window end were read.
    source = _capture(directory)
    try:
        legacy = source.execute(
            "SELECT coalesce(max(ingest_seq), 0) FROM events WHERE captured_at <= ?",
            (row["window_end"],),
        ).fetchone()[0]
    finally:
        source.close()
    return legacy, 0, None


def _capture(directory: Path) -> sqlite3.Connection:
    path = directory / capture.STORE_NAME
    source = sqlite3.connect(path.absolute().as_uri() + "?mode=ro", uri=True)
    source.row_factory = sqlite3.Row
    return source


def read_capture(directory: Path, cursor: int, limit: int) -> dict:
    """New events after the cursor, bounded, plus the context the rules need."""
    empty = {
        "events": [],
        "sessions": [],
        "history": [],
        "stops": [],
        "tools": [],
        "backlog": 0,
    }
    if not (directory / capture.STORE_NAME).is_file():
        return empty
    source = _capture(directory)
    try:
        source.execute("BEGIN")  # one snapshot for every read below
        events = [
            dict(row)
            for row in source.execute(
                "SELECT event_id, provider, session_id, sequence, event_kind,"
                " occurred_at, prompt, ingest_seq FROM events WHERE ingest_seq > ?"
                " ORDER BY ingest_seq LIMIT ?",
                (cursor, limit),
            )
        ]
        end = events[-1]["ingest_seq"] if events else cursor
        backlog = source.execute(
            "SELECT count(*) FROM events WHERE ingest_seq > ?", (end,)
        ).fetchone()[0]
        # Prompts with content up to the new cursor, so a repetition split
        # across runs or days is still seen.
        history = [
            dict(row)
            for row in source.execute(
                "SELECT event_id, provider, session_id, sequence, occurred_at, prompt"
                " FROM events WHERE event_kind='UserPromptSubmit'"
                " AND prompt IS NOT NULL AND ingest_seq <= ? ORDER BY ingest_seq",
                (end,),
            )
        ]
        stops = [
            dict(row)
            for row in source.execute(
                "SELECT event_id, provider, session_id, sequence FROM events"
                " WHERE event_kind='Stop' AND response IS NOT NULL AND ingest_seq <= ?",
                (end,),
            )
        ]
        tools = [
            dict(row)
            for row in source.execute(
                "SELECT event_id, tool_name, tool_result, occurred_at FROM events"
                " WHERE event_kind=? AND tool_result IS NOT NULL AND ingest_seq <= ?",
                (capture.TOOL_FAILURE, end),
            )
        ]
        sessions = [dict(row) for row in source.execute("SELECT * FROM sessions")]
    finally:
        source.close()
    return {
        "events": events,
        "sessions": sessions,
        "history": history,
        "stops": stops,
        "tools": tools,
        "backlog": backlog,
        "end": end,
    }


def failures(directory: Path, offset: int, head: str | None) -> tuple:
    """Complete failure-log lines after the offset; a rotated log restarts."""
    log = directory / "degraded.log"
    try:
        data = log.read_bytes()
    except OSError:
        return [], 0, None
    first = data[: data.find(b"\n") + 1]
    current = digest(first) if first else None
    if len(data) < offset or (head is not None and current != head):
        offset = 0
    end = data.rfind(b"\n") + 1
    if end <= offset:
        return [], offset, current
    lines = data[offset:end].decode("utf-8", "replace").splitlines()
    return [line for line in lines if line.strip()], end, current


def _candidate(rule, key, members, conditions, **text) -> dict:
    return {
        "rule": rule,
        "key": key,
        "pattern": key[:160],
        "events": members,
        "conditions": conditions,
        "frequency": None,  # the accumulated source events count
        "additive": False,
        "content": False,
        **text,
    }


def _normal(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def aggregate(batch: dict, failed: list[str]) -> list[dict]:
    """Deterministic rules; every candidate names the events behind it."""
    events, sessions = batch["events"], batch["sessions"]
    found = []
    fresh = {
        _normal(e["prompt"])[:500]
        for e in events
        if e["event_kind"] == "UserPromptSubmit" and e["prompt"]
    }
    groups: dict[str, list[dict]] = {}
    for event in batch["history"]:
        text = _normal(event["prompt"])[:500]
        if len(text) >= 8 and text in fresh:
            groups.setdefault(text, []).append(event)
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
                    content=True,
                )
            )
    corrections = [
        e for e in batch["history"] if _normal(e["prompt"]).startswith(CORRECTION_CUES)
    ]
    if any(e["event_id"] in {n["event_id"] for n in events} for e in corrections):
        replies = []
        for prompt in corrections:
            before = [
                s
                for s in batch["stops"]
                if (s["provider"], s["session_id"])
                == (prompt["provider"], prompt["session_id"])
                and s["sequence"] < prompt["sequence"]
            ]
            if before:
                replies.append(max(before, key=lambda s: s["sequence"]))
        if len(corrections) >= REPEAT_MIN:
            item = _candidate(
                "correction",
                "corrections after a visible response",
                corrections + replies,
                f"{len(corrections)} corrections,"
                f" {len({c['session_id'] for c in corrections})} sessions",
                hypothesis="Responses were corrected right after they were shown;"
                " this is a hypothesis, not a confirmed cause.",
                proposed_change="Read the corrected responses and decide whether a"
                " skill, a check or a reviewed memory record would prevent them.",
                expected_benefit="Fewer corrections per session.",
                risk="A cue word can open a prompt that is no correction.",
                test_plan="Compare the correction count over the next two windows"
                " after any adopted change.",
            )
            item["frequency"] = len(corrections)
            found.append(item)
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
    fresh_ids = {e["event_id"] for e in events}
    failing: dict[str, list[dict]] = {}
    for event in batch["tools"]:
        lines = [x for x in event["tool_result"].splitlines() if x.strip()]
        head = re.sub(r"\d+", "#", _normal(lines[0] if lines else ""))[:120]
        failing.setdefault(f"{event['tool_name']}: {head}", []).append(event)
    for key, members in sorted(failing.items()):
        touched = any(m["event_id"] in fresh_ids for m in members)
        if touched and len(members) >= REPEAT_MIN:
            found.append(
                _candidate(
                    "tool-failure",
                    key,
                    members,
                    f"{len(members)} failures",
                    hypothesis="The same tool call fails the same way repeatedly;"
                    " this is a hypothesis, not a confirmed cause.",
                    proposed_change="Read the failure text and decide whether a skill,"
                    " a check or a reviewed memory record would prevent it.",
                    expected_benefit="Fewer repeated tool failures.",
                    risk="The first line may group different causes.",
                    test_plan="Compare the failure count over the next two windows"
                    " after any adopted change.",
                    content=True,
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
                frequency=count,
                additive=True,
            )
        )
    return found


def _expiry(members: list[dict]) -> str | None:
    times = [m["occurred_at"] for m in members if m.get("occurred_at")]
    if not times:
        return None
    newest = dt.datetime.fromisoformat(max(times))
    return stamp(newest + dt.timedelta(days=capture.CONTENT_DAYS))


def record(connection, analysis_key: str, found: list[dict]) -> None:
    """Insert or accumulate candidates; source events form a union, never a swap."""
    for item in found:
        candidate_id = digest(item["rule"], item["key"])
        new = [event["event_id"] for event in item["events"]]
        expires = _expiry(item["events"]) if item["content"] else None
        existing = connection.execute(
            "SELECT * FROM candidates WHERE candidate_id=?", (candidate_id,)
        ).fetchone()
        if existing is None:
            sources = list(dict.fromkeys(new))
            frequency = item["frequency"] or len(sources)
            connection.execute(
                "INSERT INTO candidates (candidate_id, analysis_key, rule, pattern,"
                " hypothesis, proposed_change, expected_benefit, risk, test_plan,"
                " frequency, conditions, source_event_ids, created_at,"
                " pattern_expires_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
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
                    stamp(now()),
                    expires,
                ),
            )
        elif existing["decision"] == "pending":
            # A decided candidate keeps its reviewed revision; a pending one
            # accumulates, and a redelivered event is counted once.
            sources = list(
                dict.fromkeys(json.loads(existing["source_event_ids"]) + new)
            )
            if item["additive"]:
                frequency = existing["frequency"] + item["frequency"]
            elif item["frequency"] is not None:
                frequency = max(existing["frequency"], item["frequency"])
            else:
                frequency = len(sources)
            later = max(
                filter(None, (existing["pattern_expires_at"], expires)), default=None
            )
            connection.execute(
                "UPDATE candidates SET analysis_key=?, frequency=?, conditions=?,"
                " source_event_ids=?, pattern=?, pattern_expires_at=?"
                " WHERE candidate_id=?",
                (
                    analysis_key,
                    frequency,
                    item["conditions"],
                    json.dumps(sources),
                    item["pattern"],
                    later,
                    candidate_id,
                ),
            )


def _rekey(connection, mapping: dict[str, str]) -> None:
    """Rewrite references to event IDs the capture store replaced."""
    if not mapping:
        return
    for row in connection.execute("SELECT * FROM candidates").fetchall():
        events = json.loads(row["source_event_ids"])
        moved = [mapping.get(event, event) for event in events]
        if moved == events:
            continue
        before = review_digest(row)
        connection.execute(
            "UPDATE candidates SET source_event_ids=? WHERE candidate_id=?",
            (json.dumps(moved), row["candidate_id"]),
        )
        after = review_digest(
            connection.execute(
                "SELECT * FROM candidates WHERE candidate_id=?", (row["candidate_id"],)
            ).fetchone()
        )
        for promotion in connection.execute(
            "SELECT candidate_id, request FROM promotions WHERE candidate_id=?"
            " AND review_digest=?",
            (row["candidate_id"], before),
        ).fetchall():
            # Only the ID changed, so the reviewed revision stays the same.
            request = json.loads(promotion["request"])
            for reference in request["source_refs"]:
                if reference.get("kind") == "session-events":
                    reference["event_ids"] = [
                        mapping.get(event, event) for event in reference["event_ids"]
                    ]
            connection.execute(
                "UPDATE promotions SET request=?, review_digest=? WHERE candidate_id=?",
                (json.dumps(request, sort_keys=True), after, promotion["candidate_id"]),
            )


def expire(connection) -> None:
    """Captured text leaves with its content; candidates leave at 90/30 days."""
    current = now()
    connection.execute(
        "UPDATE candidates SET pattern=NULL WHERE pattern_expires_at < ?",
        (stamp(current),),
    )
    # A candidate linked to a Task waits for its effect up to the 90-day
    # metadata lifetime; any other decided one leaves after 30 days.
    connection.execute(
        "DELETE FROM candidates WHERE (decision='pending' AND created_at < ?)"
        " OR (decision!='pending' AND decided_at < ? AND candidate_id NOT IN"
        " (SELECT candidate_id FROM promotions WHERE state='pending')"
        " AND (task_ref IS NULL OR effect IS NOT NULL OR decided_at < ?))",
        (
            stamp(current - dt.timedelta(days=CANDIDATE_DAYS)),
            stamp(current - dt.timedelta(days=CLOSED_CANDIDATE_DAYS)),
            stamp(current - dt.timedelta(days=CANDIDATE_DAYS)),
        ),
    )
    connection.execute(
        "DELETE FROM promotions WHERE candidate_id NOT IN"
        " (SELECT candidate_id FROM candidates)"
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
        capture.prune(directory)  # the daily content and record expiry
        work_dispatch.expire_runs(directory / "dispatch")  # D10 worker text
        moved = capture.rekeys(directory)
        cursor, offset, head = _cursor(connection, directory)
        for attempt in range(1, ATTEMPTS + 1):
            try:
                batch = read_capture(directory, cursor, MAX_EVENTS)
                break
            except sqlite3.OperationalError:
                if attempt == ATTEMPTS:
                    raise
                time.sleep(RETRY_SECONDS)
        end = batch.get("end", cursor)
        failed, log_offset, log_head = failures(directory, offset, head)
        analysis_key = digest(directory.parent, cursor, end, log_offset, POLICY_EDITION)
        events = batch["events"]
        status.update(cursor_start=cursor, cursor_end=end, backlog=batch["backlog"])
        found = aggregate(batch, failed) if events or failed else []
        connection.execute("BEGIN IMMEDIATE")
        current = connection.execute("SELECT token FROM lease").fetchone()[0]
        if current != token:
            raise Fenced(f"lease token {current} replaced {token}")
        expire(connection)
        _rekey(connection, moved)
        if events or failed:
            record(connection, analysis_key, found)
            connection.execute(
                "INSERT OR REPLACE INTO runs (analysis_key, token, trigger,"
                " started_at, finished_at, state, events, candidates, cursor_start,"
                " cursor_end, log_offset, log_head, backlog)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    analysis_key,
                    token,
                    trigger,
                    stamp(started),
                    stamp(now()),
                    "complete",
                    len(events),
                    len(found),
                    cursor,
                    end,
                    log_offset,
                    log_head,
                    batch["backlog"],
                ),
            )
            status.update(events=len(events), candidates=len(found))
        else:
            status.update(reason="no new captured events")
        release(connection, token)
        connection.execute("COMMIT")
        capture.forget_rekeys(directory, list(moved))
        status.update(state="complete")
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
        found = [
            {**dict(row), "source_event_ids": json.loads(row["source_event_ids"])}
            for row in rows
        ]
    finally:
        connection.close()
    present = set()
    if (directory / capture.STORE_NAME).is_file():
        source = _capture(directory)
        try:
            present = {row[0] for row in source.execute("SELECT event_id FROM events")}
        finally:
            source.close()
    for item in found:
        # Provenance whose record has expired stays named but is counted apart.
        item["source_expired"] = sum(
            1 for event in item["source_event_ids"] if event not in present
        )
    return found


def review_digest(row) -> str:
    return digest(*(row[field] for field in REVIEWED))


def _content_expiry(directory: Path, event_ids: list[str], decided_at: str) -> str:
    """When the newest source event's captured content leaves its 30 days."""
    path = directory / capture.STORE_NAME
    newest = None
    if event_ids and path.is_file():
        source = sqlite3.connect(path.absolute().as_uri() + "?mode=ro", uri=True)
        try:
            marks = ",".join("?" * len(event_ids))
            newest = source.execute(
                f"SELECT max(occurred_at) FROM events WHERE event_id IN ({marks})",
                event_ids,
            ).fetchone()[0]
        finally:
            source.close()
    if newest is None:  # already pruned: the content has expired
        return decided_at
    expiry = dt.datetime.fromisoformat(newest) + dt.timedelta(days=capture.CONTENT_DAYS)
    return stamp(expiry.astimezone(dt.UTC))


def _intent(directory: Path, row) -> dict:
    """The whole memory request, fixed at decision time so a retry is identical."""
    reviewed = review_digest(row)
    events = json.loads(row["source_event_ids"])
    references = [
        {
            "kind": "session-analysis-candidate",
            "candidate_id": row["candidate_id"],
            "review_digest": reviewed,
        }
    ]
    if events:
        references.append(
            {
                "kind": "session-events",
                "event_ids": events,
                "content_expires_at": _content_expiry(
                    directory, events, row["decided_at"]
                ),
            }
        )
    body = (
        f"Session analysis candidate ({row['rule']}) accepted by"
        f" {row['decided_by']} at {row['decided_at']}.\n"
        f"Hypothesis: {row['hypothesis']}\n"
        f"Proposed change: {row['proposed_change']}\n"
        f"Expected benefit: {row['expected_benefit']}\n"
        f"Risk: {row['risk']}\n"
        f"Test plan: {row['test_plan']}\n"
        f"Frequency: {row['frequency']} ({row['conditions']})\n"
    )
    return {
        "memory_id": "session-analysis-" + row["candidate_id"][:40],
        "request_key": f"promotion:{row['candidate_id'][:40]}:{reviewed[:16]}",
        "owner": "session-analysis",
        "body": body,
        "source_refs": references,
    }


def decide(directory: Path, candidate_id: str, decision: str, owner: str) -> dict:
    """Record a review decision; an acceptance also records its promotion intent."""
    connection = connect(directory)
    try:
        connection.execute("BEGIN IMMEDIATE")
        try:
            changed = connection.execute(
                "UPDATE candidates SET decision=?, decided_by=?, decided_at=?"
                " WHERE candidate_id=? AND decision='pending'",
                (decision, owner, stamp(now()), candidate_id),
            ).rowcount
            if changed and decision == "accepted":
                row = connection.execute(
                    "SELECT * FROM candidates WHERE candidate_id=?", (candidate_id,)
                ).fetchone()
                connection.execute(
                    "INSERT INTO promotions (candidate_id, review_digest, request,"
                    " created_at) VALUES (?,?,?,?)",
                    (
                        candidate_id,
                        review_digest(row),
                        json.dumps(_intent(directory, row), sort_keys=True),
                        stamp(now()),
                    ),
                )
            connection.execute("COMMIT")
        except BaseException:
            connection.execute("ROLLBACK")
            raise
    finally:
        connection.close()
    if not changed:
        raise LookupError("no pending candidate with that ID")
    return {"candidate_id": candidate_id, "decision": decision}


TASK_REF = re.compile(r"SPEC-\d{4}-TSK-\d{4}")
EFFECTS = ("improved", "unchanged", "worsened")


def _follow_up(directory: Path, candidate_id: str, query: str, values: tuple) -> None:
    connection = connect(directory)
    try:
        changed = connection.execute(query, (*values, candidate_id)).rowcount
    finally:
        connection.close()
    if not changed:
        raise LookupError("no accepted candidate with that ID at this step")


def link(directory: Path, candidate_id: str, task_ref: str, check: str) -> dict:
    """Tie an accepted candidate to the Task that changes it and its check row."""
    if not TASK_REF.fullmatch(task_ref or "") or not check or len(check) > 200:
        raise ValueError("link needs SPEC-####-TSK-#### and a check row name")
    _follow_up(
        directory, candidate_id,
        "UPDATE candidates SET task_ref=?, check_ref=? WHERE candidate_id=?"
        " AND decision='accepted' AND effect IS NULL",
        (task_ref, check),
    )  # fmt: skip
    return {"candidate_id": candidate_id, "task_ref": task_ref, "check_ref": check}


def effect(directory: Path, candidate_id: str, result: str, sample: int) -> dict:
    """Record the observed effect of a linked change against a compared sample."""
    if result not in EFFECTS or type(sample) is not int or sample < 1:
        raise ValueError(
            "effect needs improved, unchanged or worsened and a sample of 1+"
        )
    _follow_up(
        directory, candidate_id,
        "UPDATE candidates SET effect=?, effect_sample=?, effect_at=?"
        " WHERE candidate_id=? AND task_ref IS NOT NULL",
        (result, sample, stamp(now())),
    )  # fmt: skip
    return {"candidate_id": candidate_id, "effect": result, "sample": sample}


class PromotionError(Exception):
    """The memory CLI refused or failed a promotion write."""


def _cli_writer(request: dict) -> int:
    """Write through the sanctioned memory CLI; nothing waits under a lock here."""
    arguments = [
        sys.executable,
        str(MEMORY_CLI),
        "put",
        request["memory_id"],
        "--expected-revision",
        "0",
        "--tier",
        "long-term",
        "--kind",
        "experience",
        "--review-state",
        "candidate",
        "--owner",
        request["owner"],
        "--request-key",
        request["request_key"],
    ]
    for reference in request["source_refs"]:
        arguments += ["--source-ref", json.dumps(reference, sort_keys=True)]
    result = subprocess.run(
        arguments,
        input=request["body"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if result.returncode:
        reason = (result.stderr.strip().splitlines() or ["no message"])[0]
        raise PromotionError(f"exit {result.returncode}: {reason[:200]}")
    return int(json.loads(result.stdout)["revision"])


def _receipt(connection, candidate_id: str, revision: int) -> None:
    connection.execute(
        "UPDATE promotions SET state='promoted', memory_revision=?, settled_at=?"
        " WHERE candidate_id=? AND state='pending'",
        (revision, stamp(now()), candidate_id),
    )


def promote(directory: Path, writer=None, include_earlier: bool = False) -> dict:
    """Drain pending promotion intents; a retry reuses the same request key.

    `include_earlier` first records an intent for each candidate accepted
    before the outbox existed, on the owner's request.
    """
    writer = writer or _cli_writer
    result = {"promoted": [], "stale": [], "pending": []}
    connection = connect(directory)
    try:
        if include_earlier:
            connection.execute("BEGIN IMMEDIATE")
            try:
                for row in connection.execute(
                    "SELECT * FROM candidates WHERE decision='accepted' AND"
                    " candidate_id NOT IN (SELECT candidate_id FROM promotions)"
                ).fetchall():
                    connection.execute(
                        "INSERT INTO promotions (candidate_id, review_digest, request,"
                        " created_at) VALUES (?,?,?,?)",
                        (
                            row["candidate_id"],
                            review_digest(row),
                            json.dumps(_intent(directory, row), sort_keys=True),
                            stamp(now()),
                        ),
                    )
                connection.execute("COMMIT")
            except BaseException:
                connection.execute("ROLLBACK")
                raise
        intents = connection.execute(
            "SELECT p.candidate_id, p.review_digest, p.request, c.* FROM promotions p"
            " JOIN candidates c USING (candidate_id) WHERE p.state='pending'"
            " ORDER BY p.created_at"
        ).fetchall()
        for intent in intents:
            candidate_id = intent["candidate_id"]
            if review_digest(intent) != intent["review_digest"]:
                # The reviewed revision changed; the old promotion never runs.
                connection.execute(
                    "UPDATE promotions SET state='stale', settled_at=?"
                    " WHERE candidate_id=? AND state='pending'",
                    (stamp(now()), candidate_id),
                )
                result["stale"].append(candidate_id)
                continue
            try:
                revision = writer(json.loads(intent["request"]))
            except (PromotionError, subprocess.TimeoutExpired, OSError) as error:
                connection.execute(
                    "UPDATE promotions SET attempts=attempts+1, last_error=?"
                    " WHERE candidate_id=?",
                    (str(error)[:200], candidate_id),
                )
                result["pending"].append(candidate_id)
                continue
            _receipt(connection, candidate_id, revision)
            result["promoted"].append(candidate_id)
    finally:
        connection.close()
    return result


class SchedulerError(Exception):
    """The timer cannot be bound to this checkout."""


def workspace_key(root: Path = ROOT) -> str:
    return digest(root.resolve())[:12]


def unit_name(root: Path = ROOT) -> str:
    """One unit per clone, so two checkouts never share or overwrite a timer."""
    return f"{LEGACY_UNIT}-{workspace_key(root)}"


UNIT = unit_name()


def primary_checkout(root: Path = ROOT) -> bool:
    """A linked worktree disappears with its dispatcher; it never owns a timer."""

    def git(*args):
        return subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--path-format=absolute", *args],
            capture_output=True, text=True, check=True, timeout=30,
        ).stdout.strip()  # fmt: skip

    return git("--git-dir") == git("--git-common-dir")


def _retire_legacy(unit_dir: Path) -> list[str]:
    """Move this checkout's fixed-name unit; another checkout's stays untouched."""
    service = unit_dir / f"{LEGACY_UNIT}.service"
    try:
        text = service.read_text(encoding="utf-8")
    except OSError:
        return []
    if f"WorkingDirectory={ROOT}\n" not in text:
        return []
    subprocess.run(
        ["systemctl", "--user", "disable", "--now", f"{LEGACY_UNIT}.timer"],
        check=False, timeout=30,
    )  # fmt: skip
    removed = []
    for suffix in (".service", ".timer"):
        path = unit_dir / f"{LEGACY_UNIT}{suffix}"
        if path.exists():
            path.unlink()
            removed.append(path.name)
    return removed


def install_timer(
    unit_dir: Path, directory: Path, on_calendar: str = ON_CALENDAR
) -> dict:
    """Write and enable this checkout's user service and timer, bound to its store."""
    if not primary_checkout():
        raise SchedulerError(f"{ROOT} is a linked worktree; install from the primary")
    unit_dir.mkdir(parents=True, exist_ok=True)
    retired = _retire_legacy(unit_dir)
    service = (
        f"[Unit]\nDescription=hy-home session analysis for {ROOT}\n\n"
        "[Service]\nType=oneshot\n"
        f"WorkingDirectory={ROOT}\n"
        f"Environment=HY_HOME_CAPTURE_DIR={directory}\n"
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
    return {
        "timer": f"{UNIT}.timer",
        "on_calendar": on_calendar,
        "store": str(directory),
        "retired": retired,
    }


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
    linking = commands.add_parser("link")
    linking.add_argument("candidate_id")
    linking.add_argument("--task", required=True)
    linking.add_argument("--check", required=True)
    observing = commands.add_parser("effect")
    observing.add_argument("candidate_id")
    observing.add_argument("result", choices=EFFECTS)
    observing.add_argument("--sample", type=int, required=True)
    promoting = commands.add_parser("promote")
    promoting.add_argument(
        "--include-earlier",
        action="store_true",
        help="also promote candidates accepted before the outbox existed",
    )
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
            if args.decision == "accepted":
                result["promotion"] = promote(directory)
        elif args.command == "link":
            result = link(directory, args.candidate_id, args.task, args.check)
        elif args.command == "effect":
            result = effect(directory, args.candidate_id, args.result, args.sample)
        elif args.command == "promote":
            result = {
                "promotion": promote(directory, include_earlier=args.include_earlier)
            }
        else:
            result = install_timer(
                Path.home() / ".config" / "systemd" / "user", directory
            )
    except (Fenced, KeyboardInterrupt) as error:
        print(f"SESSION_ANALYSIS_STOPPED: {type(error).__name__}", file=sys.stderr)
        return 1
    except LookupError as error:
        print(f"SESSION_ANALYSIS_NOT_FOUND: {error}", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"SESSION_ANALYSIS_REFUSED: {error}", file=sys.stderr)
        return 2
    except SchedulerError as error:
        print(f"SESSION_ANALYSIS_SCHEDULER: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if isinstance(result, dict) and result.get("state") == "skipped":
        return EXIT_BUSY
    if isinstance(result, dict) and result.get("promotion", {}).get("pending"):
        print("SESSION_ANALYSIS_PROMOTION_PENDING: retry with promote", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
