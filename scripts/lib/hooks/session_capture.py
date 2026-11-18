"""Session capture: visible prompts and event metadata for this workspace only.

Hooks call `enqueue`, which writes one redacted event and returns; it never
blocks the hook or changes its output. `reconcile` runs detached afterwards:
it reads a Claude transcript from its cursor to recover prompts the hooks
missed and records how complete each session's capture is. Captured records
are evidence, never instructions, approvals or memory.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CAPTURE_DIRECTORY = ".workspace-capture"
STORE_NAME = "capture.sqlite3"
RETENTION_DAYS = 90
MAX_PROMPT_BYTES = 64 * 1024
HEAD_BYTES = 4096
EVENTS = ("UserPromptSubmit", "Stop", "PreCompact", "SessionStart")
SCHEMA = (
    "CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY,"
    " workspace_id TEXT NOT NULL, provider TEXT NOT NULL, provider_version TEXT,"
    " session_id TEXT NOT NULL, sequence INTEGER NOT NULL, event_kind TEXT NOT NULL,"
    " origin TEXT NOT NULL, source_ref TEXT, occurred_at TEXT NOT NULL,"
    " captured_at TEXT NOT NULL, transcript_path TEXT, transcript_offset INTEGER,"
    " prompt TEXT, prompt_digest TEXT, redactions INTEGER NOT NULL DEFAULT 0)",
    "CREATE TABLE IF NOT EXISTS sessions (provider TEXT NOT NULL,"
    " session_id TEXT NOT NULL, transcript_path TEXT, inode INTEGER,"
    " offset INTEGER NOT NULL DEFAULT 0, head_digest TEXT,"
    " completeness TEXT NOT NULL, reason TEXT, unsupported INTEGER NOT NULL DEFAULT 0,"
    " recovered INTEGER NOT NULL DEFAULT 0, last_reconciled TEXT,"
    " PRIMARY KEY (provider, session_id))",
)
# Secret shapes are removed before anything is written; the count is kept.
SECRETS = (
    re.compile(
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
        re.S,
    ),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
)
# Lines a provider injects as user turns that the user did not type.
SYSTEM_PREFIXES = ("<task-notification>", "<local-command-stdout>", "<system-reminder>")
ASSIGNMENT = re.compile(
    r"(?i)\b(password|passwd|secret|token|api[_-]?key)(\s*[:=]\s*)(\S+)"
)


def now() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()


def redact(text: str) -> tuple[str, int]:
    count = 0
    for pattern in SECRETS:
        text, found = pattern.subn("[REDACTED]", text)
        count += found
    text, found = ASSIGNMENT.subn(r"\1\2[REDACTED]", text)
    return text, count + found


def _bounded(text: str) -> tuple[str, int]:
    return redact(text.encode()[:MAX_PROMPT_BYTES].decode(errors="ignore"))


def capture_dir(cwd: Path | None = None) -> Path:
    """The private directory beside the shared memory store of this clone."""
    from scripts.operations.agent_memory import store_path

    return store_path(cwd).parent.parent / CAPTURE_DIRECTORY


def connect(directory: Path) -> sqlite3.Connection:
    if directory.is_symlink():
        raise OSError("capture directory is a symbolic link")
    directory.mkdir(mode=0o700, exist_ok=True)
    os.chmod(directory, 0o700)
    path = directory / STORE_NAME
    if path.is_symlink():
        raise OSError("capture store is a symbolic link")
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
        os.close(os.open(path, flags, 0o600))
    except FileExistsError:
        pass
    connection = sqlite3.connect(path, timeout=1.0, isolation_level=None)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA busy_timeout = 1000")
    connection.execute("PRAGMA journal_mode = DELETE")
    for statement in SCHEMA:
        connection.execute(statement)
    return connection


def _degraded(directory: Path, reason: str) -> None:
    """Make a failed capture visible without ever failing the hook."""
    try:
        directory.mkdir(mode=0o700, exist_ok=True)
        with open(directory / "degraded.log", "a", encoding="utf-8") as stream:
            stream.write(f"{now()} {reason}\n")
    except OSError:
        pass


def _next_sequence(connection, provider: str, session: str) -> int:
    return connection.execute(
        "SELECT coalesce(max(sequence), 0) + 1 FROM events"
        " WHERE provider=? AND session_id=?",
        (provider, session),
    ).fetchone()[0]


def enqueue(
    event: str, payload: dict, provider: str, directory: Path, workspace_id: str
) -> str | None:
    """Store one event durably and return its ID; duplicates are ignored."""
    if event not in EVENTS:
        return None
    session = str(payload.get("session_id") or "")
    if not session:
        return None  # every provider event carries one; this caller is not a provider
    if event == "UserPromptSubmit" and str(
        payload.get("prompt") or ""
    ).lstrip().startswith(SYSTEM_PREFIXES):
        return None  # a provider notification, not a prompt the user typed
    transcript = payload.get("transcript_path")
    transcript = transcript if isinstance(transcript, str) and transcript else None
    offset = None
    if transcript:
        try:
            offset = os.stat(transcript).st_size
        except OSError:
            offset = None
    prompt = prompt_digest = None
    redactions = 0
    if event == "UserPromptSubmit":
        raw = str(payload.get("prompt") or "")
        prompt_digest = digest(raw)
        prompt, redactions = _bounded(raw)
    # A retried hook repeats the same turn, source or transcript size.
    marker = payload.get("turn_id") or payload.get("source") or offset
    event_id = digest(
        "\0".join(map(str, (provider, session, event, marker, prompt_digest)))
    )
    connection = connect(directory)
    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute(
            "INSERT OR IGNORE INTO events (event_id, workspace_id, provider,"
            " provider_version, session_id, sequence, event_kind, origin, source_ref,"
            " occurred_at, captured_at, transcript_path, transcript_offset, prompt,"
            " prompt_digest, redactions) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                event_id,
                workspace_id,
                provider,
                payload.get("model") or payload.get("version"),
                session,
                _next_sequence(connection, provider, session),
                event,
                "hook",
                payload.get("turn_id"),
                now(),
                now(),
                transcript,
                offset,
                prompt,
                prompt_digest,
                redactions,
            ),
        )
        connection.execute(
            "INSERT OR IGNORE INTO sessions (provider, session_id, transcript_path,"
            " completeness) VALUES (?,?,?,?)",
            (provider, session, transcript, "partial" if transcript else "unavailable"),
        )
        if transcript:
            connection.execute(
                "UPDATE sessions SET transcript_path=? WHERE provider=?"
                " AND session_id=? AND transcript_path IS NULL",
                (transcript, provider, session),
            )
        connection.execute("COMMIT")
    finally:
        connection.close()
    return event_id


def _claude_prompt(line: dict) -> tuple[str, str] | None:
    """Return the visible prompt text and its stable ID, or None."""
    if line.get("type") != "user" or line.get("isMeta") or line.get("isCompactSummary"):
        return None
    origin = line.get("origin")
    if isinstance(origin, dict) and origin.get("kind") != "human":
        return None
    message = line.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    if isinstance(content, list):
        parts = [part for part in content if isinstance(part, dict)]
        if any(part.get("type") == "tool_result" for part in parts):
            return None
        content = "".join(
            part.get("text", "") for part in parts if part.get("type") == "text"
        )
    if not isinstance(content, str) or not content:
        return None
    if content.lstrip().startswith(SYSTEM_PREFIXES):
        return None
    return content, str(line.get("promptId") or line.get("uuid") or "")


def _allowed_transcript(path: Path, provider: str) -> bool:
    """Read only this provider's own session files, never other personal files."""
    root = {"claude": Path.home() / ".claude" / "projects"}.get(provider)
    try:
        return (
            root is not None
            and not path.is_symlink()
            and path.is_file()
            and path.suffix == ".jsonl"
            and path.stat().st_uid == os.getuid()
            and path.resolve().is_relative_to(root.resolve())
        )
    except OSError:
        return False


def _recover(connection, provider, session, transcript, line, text, source_ref):
    """Link a transcript prompt to its hook event, or record it as recovered."""
    prompt_digest = digest(text)
    if connection.execute(
        "SELECT 1 FROM events WHERE provider=? AND session_id=? AND source_ref=?",
        (provider, session, source_ref),
    ).fetchone():
        return 0
    matched = connection.execute(
        "SELECT event_id FROM events WHERE provider=? AND session_id=?"
        " AND event_kind='UserPromptSubmit' AND prompt_digest=?"
        " AND source_ref IS NULL ORDER BY sequence LIMIT 1",
        (provider, session, prompt_digest),
    ).fetchone()
    if matched:
        connection.execute(
            "UPDATE events SET source_ref=? WHERE event_id=?", (source_ref, matched[0])
        )
        return 0
    prompt, redactions = _bounded(text)
    return connection.execute(
        "INSERT OR IGNORE INTO events (event_id, workspace_id, provider, session_id,"
        " sequence, event_kind, origin, source_ref, occurred_at, captured_at,"
        " transcript_path, prompt, prompt_digest, redactions)"
        " SELECT ?, workspace_id, ?, ?, ?, 'UserPromptSubmit', 'transcript', ?, ?,"
        " ?, ?, ?, ?, ? FROM events WHERE provider=? AND session_id=? LIMIT 1",
        (
            digest(f"{provider}\0{session}\0transcript\0{source_ref}"),
            provider,
            session,
            _next_sequence(connection, provider, session),
            source_ref,
            str(line.get("timestamp") or now()),
            now(),
            transcript,
            prompt,
            prompt_digest,
            redactions,
            provider,
            session,
        ),
    ).rowcount


def reconcile_session(connection, provider: str, session: str) -> dict:
    row = connection.execute(
        "SELECT * FROM sessions WHERE provider=? AND session_id=?", (provider, session)
    ).fetchone()

    def finish(completeness, reason, **fields):
        connection.execute(
            "UPDATE sessions SET completeness=?, reason=?, last_reconciled=?"
            + "".join(f", {key}=?" for key in fields)
            + " WHERE provider=? AND session_id=?",
            (completeness, reason, now(), *fields.values(), provider, session),
        )
        return {
            "provider": provider,
            "session_id": session,
            "completeness": completeness,
            "reason": reason,
        }

    transcript = row["transcript_path"]
    if not transcript:
        return finish("unavailable", "no transcript path from the provider")
    if provider != "claude":
        # Codex 0.169 rollouts mix injected context into user messages, so the
        # visible prompt cannot be told apart; only hook events are captured.
        return finish("partial", "transcript format unsupported; hook events only")
    path = Path(transcript)
    if not _allowed_transcript(path, provider):
        return finish(
            "unavailable", "transcript missing or outside the provider's sessions"
        )
    stat = path.stat()
    with open(path, "rb") as stream:
        head = digest(stream.read(HEAD_BYTES).decode("utf-8", "replace"))
        offset = row["offset"] or 0
        rewritten = (
            row["inode"] not in (None, stat.st_ino)
            or stat.st_size < offset
            or (row["head_digest"] not in (None, head) and offset >= HEAD_BYTES)
        )
        if rewritten:
            offset = 0  # rescan; already captured prompts are skipped by ID
        stream.seek(offset)
        data = stream.read()
    end = data.rfind(b"\n") + 1
    pending = len(data) - end  # a partly flushed last line waits for later
    unsupported, recovered = row["unsupported"], row["recovered"]
    for raw in data[:end].splitlines():
        try:
            line = json.loads(raw)
        except ValueError:
            unsupported += 1
            continue
        found = _claude_prompt(line) if isinstance(line, dict) else None
        if found is not None:
            recovered += _recover(
                connection, provider, session, transcript, line, *found
            )
    unmatched = connection.execute(
        "SELECT count(*) FROM events WHERE provider=? AND session_id=?"
        " AND event_kind='UserPromptSubmit' AND source_ref IS NULL",
        (provider, session),
    ).fetchone()[0]
    reasons = [
        text
        for flag, text in (
            (unsupported, f"{unsupported} unreadable lines"),
            (pending, "last line not yet flushed"),
            (unmatched, f"{unmatched} hook prompts not yet in the transcript"),
        )
        if flag
    ]
    return finish(
        "partial" if reasons else "complete",
        "; ".join(reasons) or None,
        inode=stat.st_ino,
        offset=offset + end,
        head_digest=head,
        unsupported=unsupported,
        recovered=recovered,
    )


def reconcile(
    directory: Path, provider: str | None = None, session: str | None = None
) -> list[dict]:
    """Rescan sessions under an exclusive lock and prune expired records."""
    directory.mkdir(mode=0o700, exist_ok=True)
    with open(directory / "reconcile.lock", "a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return [{"skipped": "another reconcile holds the lock"}]
        connection = connect(directory)
        try:
            connection.execute("BEGIN IMMEDIATE")
            cutoff = dt.datetime.now(dt.UTC) - dt.timedelta(days=RETENTION_DAYS)
            connection.execute(
                "DELETE FROM events WHERE captured_at < ?",
                (cutoff.isoformat(timespec="seconds"),),
            )
            connection.execute(
                "DELETE FROM sessions WHERE NOT EXISTS (SELECT 1 FROM events e"
                " WHERE e.provider=sessions.provider"
                " AND e.session_id=sessions.session_id)"
            )
            where = " WHERE provider=? AND session_id=?" if session else ""
            selected = connection.execute(
                "SELECT provider, session_id FROM sessions" + where,
                (provider, session) if session else (),
            ).fetchall()
            results = [reconcile_session(connection, p, s) for p, s in selected]
            connection.execute("COMMIT")
            return results
        except BaseException:
            if connection.in_transaction:
                connection.execute("ROLLBACK")
            raise
        finally:
            connection.close()


def status(directory: Path) -> dict:
    path = directory / STORE_NAME
    log = directory / "degraded.log"
    failures = log.read_text(encoding="utf-8").splitlines() if log.exists() else []
    result = {
        "sessions": [],
        "events": 0,
        "capture_failures": len(failures),
        "last_failure": failures[-1] if failures else None,
        "retention_days": RETENTION_DAYS,
    }
    if not path.exists():
        return result
    if path.is_symlink() or not path.is_file():
        return {**result, "store_error": "capture store is not a regular file"}
    try:
        connection = sqlite3.connect(path.absolute().as_uri() + "?mode=ro", uri=True)
    except sqlite3.Error as error:
        return {**result, "store_error": type(error).__name__}
    connection.row_factory = sqlite3.Row
    try:
        result["sessions"] = [
            dict(row)
            for row in connection.execute(
                "SELECT s.provider, s.session_id, s.completeness, s.reason,"
                " s.recovered, s.last_reconciled, count(e.event_id) AS events"
                " FROM sessions s LEFT JOIN events e USING (provider, session_id)"
                " GROUP BY s.provider, s.session_id"
                " ORDER BY s.last_reconciled DESC"
            )
        ]
        result["events"] = connection.execute("SELECT count(*) FROM events").fetchone()[
            0
        ]
    finally:
        connection.close()
    return result


def hook(event: str, raw: str, provider: str) -> None:
    """Hook entry: enqueue, then start a detached reconcile when useful."""
    try:
        directory = capture_dir()
    except Exception:
        return
    try:
        payload = json.loads(raw) if raw.strip() else {}
        payload = payload if isinstance(payload, dict) else {}
        enqueue(event, payload, provider, directory, str(directory.parent))
    except Exception as error:
        _degraded(directory, f"{provider} {event} {type(error).__name__}")
        return
    if event == "Stop" or (
        event == "SessionStart" and payload.get("source") in ("resume", "compact")
    ):
        try:
            subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "scripts.lib.hooks.session_capture",
                    "reconcile",
                    "--provider",
                    provider,
                    "--session",
                    str(payload.get("session_id")),
                ],
                cwd=ROOT,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
        except OSError as error:
            _degraded(directory, f"{provider} reconcile start {type(error).__name__}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("hook").add_argument("event")
    run = commands.add_parser("reconcile")
    run.add_argument("--provider")
    run.add_argument("--session")
    commands.add_parser("status")
    args = parser.parse_args(argv)
    if args.command == "hook":
        provider = os.environ.get("HY_HOME_HOOK_PROVIDER", "claude")
        hook(args.event, sys.stdin.read(), provider)
        return 0
    directory = capture_dir()
    if args.command == "reconcile":
        result = reconcile(directory, args.provider, args.session)
    else:
        result = status(directory)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
