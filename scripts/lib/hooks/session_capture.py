"""Session capture: visible prompts and event metadata for this workspace only.

Hooks call `enqueue`, which writes one redacted event and returns; it never
blocks the hook or changes its output. Selected content (the visible prompt and
the visible final response) is redacted whole, then cut to a UTF-8 byte cap and
checked again before it is stored; it expires 30 days after the event and the
metadata 90 days after it. Each insert takes a never-reused ingest sequence,
the cursor the analysis reads. `reconcile` runs detached afterwards:
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
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CAPTURE_DIRECTORY = ".workspace-capture"
STORE_NAME = "capture.sqlite3"
CONTENT_DAYS = 30
METADATA_DAYS = 90
MAX_CONTENT_BYTES = 16 * 1024
TOOL_RESULT_BYTES = 4 * 1024
STORE_QUOTA_BYTES = 256 * 1024 * 1024
SCHEMA_VERSION = 4
HEAD_BYTES = 4096
EVENTS = (
    "UserPromptSubmit",
    "Stop",
    "PreCompact",
    "SessionStart",
    "PostToolUseFailure",
    "PostToolUse",
)
TOOL_FAILURE = "PostToolUseFailure"
EXIT_CODE = re.compile(r"(?:Exit code:?|exited with code)\s*(-?\d+)")
SCHEMA = (
    "CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY,"
    " workspace_id TEXT NOT NULL, provider TEXT NOT NULL, provider_version TEXT,"
    " session_id TEXT NOT NULL, sequence INTEGER NOT NULL, event_kind TEXT NOT NULL,"
    " origin TEXT NOT NULL, source_ref TEXT, occurred_at TEXT NOT NULL,"
    " captured_at TEXT NOT NULL, transcript_path TEXT, transcript_offset INTEGER,"
    " prompt TEXT, prompt_digest TEXT, redactions INTEGER NOT NULL DEFAULT 0,"
    " ingest_seq INTEGER, response TEXT, content_state TEXT, tool_name TEXT,"
    " tool_result TEXT, event_marker TEXT)",
    # Rows up to this ingest sequence have a verified, text-free event ID.
    "CREATE TABLE IF NOT EXISTS capture_meta (key TEXT PRIMARY KEY,"
    " value INTEGER NOT NULL)",
    "INSERT OR IGNORE INTO capture_meta VALUES ('verified_through', 0)",
    # An event ID that was derived from captured text, mapped to its new ID
    # until the analysis store has rewritten its references.
    "CREATE TABLE IF NOT EXISTS rekeyed (old_id TEXT PRIMARY KEY,"
    " new_id TEXT NOT NULL)",
    # The ingest sequence lives apart from the rows, so a deleted row never
    # frees its number for a later insert.
    "CREATE TABLE IF NOT EXISTS ingest (singleton INTEGER PRIMARY KEY"
    " CHECK (singleton = 1), seq INTEGER NOT NULL)",
    "INSERT OR IGNORE INTO ingest VALUES (1, 0)",
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
SYSTEM_PREFIXES = (
    "<task-notification>",
    "<local-command-stdout>",
    "<system-reminder>",
    "[Request interrupted by user",
)
ASSIGNMENT = re.compile(
    r"(?i)\b(password|passwd|secret|token|api[_-]?key)(\s*[:=]\s*)(?!\[REDACTED\](?:\s|$))(\S+)"
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


def _cut(text: str, cap: int) -> str:
    return text.encode()[:cap].decode(errors="ignore")


def bounded(text: str, cap: int = MAX_CONTENT_BYTES) -> tuple[str, int, bool]:
    """Redact the whole text, cut it to the byte cap, then redact again."""
    text, count = redact(text)
    truncated = len(text.encode()) > cap
    if truncated:
        text, again = redact(_cut(text, cap))
        text, count = _cut(text, cap), count + again
    return text, count, truncated


def event_time(value: object) -> str:
    """A normalized UTC stamp; an unreadable time is fixed at first observation."""
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return now()
    if parsed.tzinfo is None:
        return now()
    return parsed.astimezone(dt.UTC).isoformat(timespec="seconds")


def _content(directory: Path, text: str | None, cap: int = MAX_CONTENT_BYTES) -> tuple:
    """(stored text, its fingerprint, redaction count, content state)."""
    if text is None:
        return None, None, 0, None
    try:
        size = (directory / STORE_NAME).stat().st_size
    except OSError:
        size = 0  # not created yet
    if size >= STORE_QUOTA_BYTES:
        return None, None, 0, "quota"  # metadata only; never a raw spill
    stored, redactions, truncated = bounded(text, cap)
    # The fingerprint covers the stored, redacted text and expires with it.
    return stored, digest(stored), redactions, "truncated" if truncated else "stored"


def capture_dir(cwd: Path | None = None) -> Path:
    """The private directory beside the shared memory store of this clone.

    `HY_HOME_CAPTURE_DIR` names another directory, so a test that drives the
    real hooks never writes into the operator's store.
    """
    override = os.environ.get("HY_HOME_CAPTURE_DIR")
    if override:
        return Path(override)
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
    if connection.execute("PRAGMA user_version").fetchone()[0] < SCHEMA_VERSION:
        _migrate(connection)
    for statement in SCHEMA:
        connection.execute(statement)
    if connection.execute(
        "SELECT 1 FROM events WHERE ingest_seq IS NULL OR ingest_seq >"
        " (SELECT value FROM capture_meta WHERE key='verified_through') LIMIT 1"
    ).fetchone():
        # A checkout still on older code can share this store: adopt its rows,
        # so the cursor reads them once and no ID derives from captured text.
        connection.execute("BEGIN IMMEDIATE")
        try:
            _adopt(connection)
            _verify_ids(connection)
            connection.execute("COMMIT")
        except BaseException:
            connection.execute("ROLLBACK")
            raise
    return connection


def _migrate(connection: sqlite3.Connection) -> None:
    """Bring a version 0 store to the current contract once, in one transaction."""
    connection.execute("BEGIN IMMEDIATE")
    try:
        if connection.execute("PRAGMA user_version").fetchone()[0] >= SCHEMA_VERSION:
            connection.execute("COMMIT")
            return
        for statement in SCHEMA:
            connection.execute(statement)
        columns = {row[1] for row in connection.execute("PRAGMA table_info(events)")}
        for column in (
            "ingest_seq INTEGER",
            "response TEXT",
            "content_state TEXT",
            "tool_name TEXT",
            "tool_result TEXT",
            "event_marker TEXT",
        ):
            if column.split()[0] not in columns:
                connection.execute(f"ALTER TABLE events ADD COLUMN {column}")
        _adopt(connection)
        connection.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS events_ingest ON events (ingest_seq)"
        )
        connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
        connection.execute("COMMIT")
    except BaseException:
        connection.execute("ROLLBACK")
        raise


def _adopt(connection: sqlite3.Connection) -> None:
    """Give rows written without the contract a sequence, bounded text and time.

    Older code cut a prompt before redacting it, kept a digest of the raw text
    and stored the transcript's own time format; redact and cut the text again,
    replace that digest and normalize the time.
    """
    rows = connection.execute(
        "SELECT rowid, prompt, occurred_at FROM events WHERE ingest_seq IS NULL"
        " ORDER BY captured_at, rowid"
    ).fetchall()
    for rowid, prompt, occurred in rows:
        stored, redactions, truncated = bounded(prompt) if prompt else (None, 0, 0)
        connection.execute(
            "UPDATE events SET ingest_seq=?, occurred_at=?, prompt=?,"
            " prompt_digest=?, redactions=redactions+?, content_state=?"
            " WHERE rowid=?",
            (
                _next_ingest(connection),
                event_time(occurred),
                stored,
                digest(stored) if stored else None,
                redactions,
                ("truncated" if truncated else "stored") if stored else None,
                rowid,
            ),
        )


def event_key(provider: str, session: str, event: str, marker: object) -> str:
    return digest("\0".join(map(str, ("event", provider, session, event, marker))))


def _rekey_id(provider: str, session: str, sequence: int) -> str:
    return digest(f"event-v3\0{provider}\0{session}\0{sequence}")


def _verify_ids(connection: sqlite3.Connection) -> None:
    """Rekey hook prompt rows past the watermark whose ID came from their text.

    Current code derives an ID from the stored marker only; earlier code also
    hashed the prompt. Any row that matches neither the marker key nor the
    rekey key gets the rekey key, and the old ID is mapped until the
    analysis store has rewritten its references.
    """
    mark = connection.execute(
        "SELECT value FROM capture_meta WHERE key='verified_through'"
    ).fetchone()[0]
    rows = connection.execute(
        "SELECT event_id, provider, session_id, event_kind, ingest_seq, event_marker"
        " FROM events WHERE ingest_seq > ? AND origin='hook'"
        " AND event_kind='UserPromptSubmit'",
        (mark,),
    ).fetchall()
    for old, provider, session, kind, sequence, marker in rows:
        new = _rekey_id(provider, session, sequence)
        if old == new or (
            marker is not None and old == event_key(provider, session, kind, marker)
        ):
            continue
        connection.execute("UPDATE events SET event_id=? WHERE event_id=?", (new, old))
        connection.execute("INSERT OR REPLACE INTO rekeyed VALUES (?, ?)", (old, new))
    connection.execute(
        "UPDATE capture_meta SET value=(SELECT coalesce(max(ingest_seq), 0)"
        " FROM events) WHERE key='verified_through'"
    )


def rekeys(directory: Path) -> dict[str, str]:
    """Old to new event IDs the analysis store has not yet applied."""
    path = directory / STORE_NAME
    if not path.is_file():
        return {}
    source = sqlite3.connect(path.absolute().as_uri() + "?mode=ro", uri=True)
    try:
        return dict(source.execute("SELECT old_id, new_id FROM rekeyed"))
    except sqlite3.OperationalError:
        return {}  # a store before the map
    finally:
        source.close()


def forget_rekeys(directory: Path, old_ids: list[str]) -> None:
    """Drop applied entries, so no text-derived ID outlives its rewrite."""
    if not old_ids:
        return
    connection = connect(directory)
    try:
        connection.executemany(
            "DELETE FROM rekeyed WHERE old_id=?", [(old,) for old in old_ids]
        )
    finally:
        connection.close()


def _tool_failure(event: str, payload: dict, provider: str) -> str | None:
    """The failure text of a tool call, or None when nothing failed."""
    if event == TOOL_FAILURE:
        if payload.get("is_interrupt"):
            return None  # a cancellation, not a failure
        error = payload.get("error")
        return error if isinstance(error, str) and error else None
    if provider != "codex" or payload.get("tool_name") != "Bash":
        return None  # Claude reports failures through PostToolUseFailure
    response = payload.get("tool_response")
    if isinstance(response, dict):
        code = response.get("exit_code", response.get("exitCode"))
        text = response.get("output") or response.get("stderr") or ""
        if type(code) is int and code != 0:
            return str(text) or f"exit code {code}"
        return None
    if isinstance(response, str):
        found = EXIT_CODE.search(response)
        return response if found and int(found.group(1)) != 0 else None
    return None


def directory_of(connection: sqlite3.Connection) -> Path:
    return Path(connection.execute("PRAGMA database_list").fetchone()[2]).parent


def _next_ingest(connection) -> int:
    return connection.execute(
        "UPDATE ingest SET seq = seq + 1 RETURNING seq"
    ).fetchone()[0]


def _prune(connection) -> None:
    now_ = dt.datetime.now(dt.UTC)
    content = (now_ - dt.timedelta(days=CONTENT_DAYS)).isoformat(timespec="seconds")
    metadata = (now_ - dt.timedelta(days=METADATA_DAYS)).isoformat(timespec="seconds")
    connection.execute("DELETE FROM events WHERE occurred_at < ?", (metadata,))
    connection.execute(
        "UPDATE events SET prompt=NULL, response=NULL, tool_result=NULL,"
        " prompt_digest=NULL, content_state='expired' WHERE occurred_at < ? AND"
        " (prompt IS NOT NULL OR response IS NOT NULL OR tool_result IS NOT NULL"
        " OR prompt_digest IS NOT NULL)",
        (content,),
    )
    connection.execute(
        "DELETE FROM sessions WHERE NOT EXISTS (SELECT 1 FROM events e"
        " WHERE e.provider=sessions.provider AND e.session_id=sessions.session_id)"
    )


def prune(directory: Path) -> None:
    """Expire content at 30 days and records at 90; the daily analysis calls it."""
    connection = connect(directory)
    try:
        connection.execute("BEGIN IMMEDIATE")
        try:
            _prune(connection)
            connection.execute("COMMIT")
        except BaseException:
            connection.execute("ROLLBACK")
            raise
    finally:
        connection.close()


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
    text = tool = None
    if event in (TOOL_FAILURE, "PostToolUse"):
        text = _tool_failure(event, payload, provider)
        if text is None:
            return None
        event, tool = TOOL_FAILURE, str(payload.get("tool_name") or "unknown")[:80]
    elif event == "UserPromptSubmit":
        text = str(payload.get("prompt") or "")
    elif event == "Stop":
        message = payload.get("last_assistant_message")
        text = message if isinstance(message, str) and message else None
    cap = TOOL_RESULT_BYTES if tool else MAX_CONTENT_BYTES
    stored, prompt_digest, redactions, content_state = _content(directory, text, cap)
    prompt = stored if event == "UserPromptSubmit" else None
    response = stored if event == "Stop" else None
    tool_result = stored if tool else None
    # A retried hook repeats the same turn, tool call, source or transcript
    # size; the ID never includes captured text.
    marker = (
        payload.get("turn_id")
        or payload.get("tool_use_id")
        or payload.get("source")
        or offset
    )
    if marker is None:
        marker = uuid.uuid4().hex  # nothing stable to retry on
    event_id = event_key(provider, session, event, marker)
    connection = connect(directory)
    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute(
            "INSERT OR IGNORE INTO events (event_id, workspace_id, provider,"
            " provider_version, session_id, sequence, event_kind, origin, source_ref,"
            " occurred_at, captured_at, transcript_path, transcript_offset, prompt,"
            " prompt_digest, redactions, response, content_state, ingest_seq,"
            " tool_name, tool_result, event_marker)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
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
                response,
                content_state,
                _next_ingest(connection),
                tool,
                tool_result,
                str(marker),
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
    prompt, prompt_digest, redactions, state = _content(directory_of(connection), text)
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
    return connection.execute(
        "INSERT OR IGNORE INTO events (event_id, workspace_id, provider, session_id,"
        " sequence, event_kind, origin, source_ref, occurred_at, captured_at,"
        " transcript_path, prompt, prompt_digest, redactions, content_state,"
        " ingest_seq)"
        " SELECT ?, workspace_id, ?, ?, ?, 'UserPromptSubmit', 'transcript', ?, ?,"
        " ?, ?, ?, ?, ?, ?, ? FROM events WHERE provider=? AND session_id=? LIMIT 1",
        (
            digest(f"{provider}\0{session}\0transcript\0{source_ref}"),
            provider,
            session,
            _next_sequence(connection, provider, session),
            source_ref,
            event_time(line.get("timestamp")),
            now(),
            transcript,
            prompt,
            prompt_digest,
            redactions,
            state,
            _next_ingest(connection),
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
            _prune(connection)
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
        "content_days": CONTENT_DAYS,
        "metadata_days": METADATA_DAYS,
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
        stored = enqueue(event, payload, provider, directory, str(directory.parent))
    except Exception as error:
        _degraded(directory, f"{provider} {event} {type(error).__name__}")
        return
    if stored is None:
        return  # nothing of this workspace's sessions was captured
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
