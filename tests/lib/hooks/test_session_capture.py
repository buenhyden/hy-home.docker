"""Session capture on temporary stores and synthetic transcripts only."""

from __future__ import annotations

import datetime as dt
import fcntl
import json
import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.lib.hooks import session_capture as capture


def line(uuid: str, text: str | None = None) -> str:
    if text is None:
        return json.dumps({"type": "assistant", "uuid": uuid}) + "\n"
    record = {
        "type": "user",
        "uuid": uuid,
        "promptId": f"p-{uuid}",
        "message": {"role": "user", "content": text},
    }
    return json.dumps(record) + "\n"


class CaptureTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        home = self.base / "home"
        patcher = mock.patch.dict(os.environ, {"HOME": str(home)})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.sessions = home / ".claude" / "projects" / "workspace"
        self.sessions.mkdir(parents=True)
        self.transcript = self.sessions / "s1.jsonl"
        self.transcript.write_text("")
        self.directory = self.base / ".workspace-capture"

    def prompt(self, text, session="s1", provider="claude", path=None):
        payload = {
            "session_id": session,
            "prompt": text,
            "transcript_path": str(path or self.transcript),
        }
        return capture.enqueue(
            "UserPromptSubmit", payload, provider, self.directory, "workspace"
        )

    def events(self, session="s1"):
        connection = capture.connect(self.directory)
        try:
            rows = connection.execute(
                "SELECT * FROM events WHERE session_id=? ORDER BY sequence", (session,)
            )
            return [dict(row) for row in rows]
        finally:
            connection.close()

    def session(self, provider="claude", session="s1"):
        return capture.reconcile(self.directory, provider, session)[0]

    def test_enqueue_is_private_idempotent_and_redacts_secrets(self):
        text = "deploy with token=abc123 and ghp_" + "a" * 36
        self.assertEqual(self.prompt(text), self.prompt(text))
        (event,) = self.events()
        self.assertNotIn("abc123", event["prompt"])
        self.assertNotIn("ghp_", event["prompt"])
        self.assertEqual(2, event["redactions"])
        self.assertEqual("hook", event["origin"])
        self.assertEqual(0o700, stat.S_IMODE(self.directory.stat().st_mode))
        store = self.directory / capture.STORE_NAME
        self.assertEqual(0o600, stat.S_IMODE(store.stat().st_mode))

    def test_reconcile_links_hook_prompts_and_recovers_missed_ones(self):
        self.prompt("first question")
        self.transcript.write_text(
            line("u1", "first question") + line("a1") + line("u2", "missed by hook")
        )
        result = self.session()
        self.assertEqual("complete", result["completeness"], result)
        events = self.events()
        self.assertEqual(["p-u1", "p-u2"], [e["source_ref"] for e in events])
        self.assertEqual(["hook", "transcript"], [e["origin"] for e in events])
        # A second pass finds nothing new and records no duplicate.
        self.session()
        self.assertEqual(2, len(self.events()))

    def test_partial_flush_and_late_transcript_stay_partial_until_seen(self):
        self.prompt("late prompt")
        self.transcript.write_text(line("u0", "earlier") + '{"type": "user", "uu')
        result = self.session()
        self.assertEqual("partial", result["completeness"])
        self.assertIn("not yet flushed", result["reason"])
        self.assertIn("hook prompts not yet in the transcript", result["reason"])
        self.transcript.write_text(line("u0", "earlier") + line("u1", "late prompt"))
        result = self.session()
        self.assertEqual("complete", result["completeness"], result)
        self.assertEqual(2, len(self.events()))

    def test_rewritten_transcript_is_rescanned_without_duplicates(self):
        self.transcript.write_text(line("u1", "one") + line("u2", "two"))
        self.prompt("one")
        self.session()
        replaced = self.sessions / "replacement.jsonl"
        replaced.write_text(line("u1", "one"))
        os.replace(replaced, self.transcript)
        result = self.session()
        self.assertEqual("complete", result["completeness"], result)
        self.assertEqual(["p-u1", "p-u2"], [e["source_ref"] for e in self.events()])

    def test_unreadable_lines_are_reported_not_hidden(self):
        self.prompt("ok")
        self.transcript.write_text(line("u1", "ok") + "not json\n")
        result = self.session()
        self.assertEqual("partial", result["completeness"])
        self.assertIn("1 unreadable lines", result["reason"])

    def test_codex_and_missing_paths_report_their_limits(self):
        capture.enqueue(
            "UserPromptSubmit",
            {"session_id": "c1", "prompt": "hi", "transcript_path": None},
            "codex",
            self.directory,
            "workspace",
        )
        self.assertEqual("unavailable", self.session("codex", "c1")["completeness"])
        rollout = self.base / "rollout.jsonl"
        rollout.write_text("{}\n")
        self.prompt("hi", session="c2", provider="codex", path=rollout)
        result = self.session("codex", "c2")
        self.assertEqual("partial", result["completeness"])
        self.assertIn("unsupported", result["reason"])

    def test_files_outside_the_provider_sessions_are_never_read(self):
        outside = self.base / "personal.jsonl"
        outside.write_text(line("u1", "private"))
        self.prompt("q", session="s9", path=outside)
        link = self.sessions / "linked.jsonl"
        link.symlink_to(outside)
        self.prompt("q", session="s8", path=link)
        for session in ("s9", "s8"):
            result = self.session(session=session)
            self.assertEqual("unavailable", result["completeness"], result)
        self.assertEqual(1, len(self.events("s9")))

    def age(self, days):
        old = dt.datetime.now(dt.UTC) - dt.timedelta(days=days)
        connection = capture.connect(self.directory)
        connection.execute(
            "UPDATE events SET occurred_at=?", (old.isoformat(timespec="seconds"),)
        )
        connection.close()

    def test_content_expires_at_30_days_and_metadata_at_90(self):
        self.prompt("old")
        self.age(capture.CONTENT_DAYS + 1)
        capture.reconcile(self.directory)
        (event,) = self.events()
        self.assertEqual(
            (None, None, "expired"),
            (event["prompt"], event["prompt_digest"], event["content_state"]),
        )
        self.age(capture.METADATA_DAYS + 1)
        self.assertEqual([], capture.reconcile(self.directory))
        self.assertEqual([], self.events())

    def test_redaction_runs_on_the_whole_text_before_the_byte_cap(self):
        cap = capture.MAX_CONTENT_BYTES
        secret = "ghp_" + "b" * 36
        text = "a" * (cap - 25) + " " + secret + " " + "t" * 100  # cut-first leaks
        self.prompt(text)
        (event,) = self.events()
        self.assertNotIn("bbbbbbbb", event["prompt"])
        self.assertLessEqual(len(event["prompt"].encode()), cap)
        self.assertEqual(
            ("truncated", 1), (event["content_state"], event["redactions"])
        )

    def test_the_content_fingerprint_is_not_a_digest_of_the_raw_text(self):
        text = "use token=hunter2 now"
        self.prompt(text)
        (event,) = self.events()
        self.assertNotEqual(capture.digest(text), event["prompt_digest"])
        self.assertEqual(capture.digest(event["prompt"]), event["prompt_digest"])

    def test_every_insert_takes_a_new_ingest_sequence(self):
        self.prompt("one")
        self.prompt("two", session="s2")
        capture.enqueue(
            "Stop", {"session_id": "s1", "turn_id": "t"}, "claude", self.directory, "w"
        )
        connection = capture.connect(self.directory)
        sequences = [
            row[0]
            for row in connection.execute("SELECT ingest_seq FROM events ORDER BY 1")
        ]
        connection.close()
        self.assertEqual([1, 2, 3], sequences)

    def test_the_visible_final_response_is_redacted_and_bounded(self):
        payload = {
            "session_id": "s1",
            "turn_id": "t1",
            "last_assistant_message": "done; key sk-" + "c" * 30 + " " + "x" * 40000,
        }
        capture.enqueue("Stop", payload, "claude", self.directory, "workspace")
        (event,) = self.events()
        self.assertNotIn("ccccccccc", event["response"])
        self.assertLessEqual(len(event["response"].encode()), capture.MAX_CONTENT_BYTES)
        self.assertEqual("truncated", event["content_state"])

    def test_a_store_from_before_the_contract_is_migrated_once(self):
        import sqlite3

        self.directory.mkdir()
        old = sqlite3.connect(self.directory / capture.STORE_NAME)
        old.execute(
            "CREATE TABLE events (event_id TEXT PRIMARY KEY, workspace_id TEXT NOT"
            " NULL, provider TEXT NOT NULL, provider_version TEXT, session_id TEXT"
            " NOT NULL, sequence INTEGER NOT NULL, event_kind TEXT NOT NULL, origin"
            " TEXT NOT NULL, source_ref TEXT, occurred_at TEXT NOT NULL, captured_at"
            " TEXT NOT NULL, transcript_path TEXT, transcript_offset INTEGER, prompt"
            " TEXT, prompt_digest TEXT, redactions INTEGER NOT NULL DEFAULT 0)"
        )
        long = "x" * (capture.MAX_CONTENT_BYTES + 10)
        for number, (prompt, when) in enumerate(
            ((long, "2026-11-20T00:00:01.500Z"), (None, "2026-11-20T00:00:00+00:00"))
        ):
            old.execute(
                "INSERT INTO events VALUES (?, 'w', 'claude', NULL, 's1', ?,"
                " 'UserPromptSubmit', 'hook', NULL, ?, ?, NULL, NULL, ?, ?, 0)",
                (f"e{number}", number, when, when.replace(".500Z", "+00:00"),
                 prompt, capture.digest(prompt or "")),
            )  # fmt: skip
        old.commit()
        old.close()
        events = {e["event_id"]: e for e in self.events()}
        self.assertEqual(
            (2, 1), (events["e0"]["ingest_seq"], events["e1"]["ingest_seq"])
        )
        self.assertEqual("truncated", events["e0"]["content_state"])
        self.assertEqual(capture.MAX_CONTENT_BYTES, len(events["e0"]["prompt"]))
        self.assertEqual("2026-11-20T00:00:01+00:00", events["e0"]["occurred_at"])
        self.assertIsNone(events["e1"]["prompt_digest"])
        self.prompt("after")
        self.assertEqual(3, max(e["ingest_seq"] for e in self.events()))

    def test_a_row_written_by_older_code_after_migration_is_adopted(self):
        self.prompt("new code")
        connection = capture.connect(self.directory)
        raw = "old code token=hunter2 " + "y" * (capture.MAX_CONTENT_BYTES + 5)
        connection.execute(  # another checkout still runs the code before P10
            "INSERT INTO events (event_id, workspace_id, provider, session_id,"
            " sequence, event_kind, origin, occurred_at, captured_at, prompt,"
            " prompt_digest) VALUES ('late', 'w', 'claude', 's1', 2,"
            " 'UserPromptSubmit', 'hook', '2026-11-24T00:00:00.250Z',"
            " '2026-11-24T00:00:00+00:00', ?, ?)",
            (raw, capture.digest(raw)),
        )
        connection.close()
        late = {e["event_id"]: e for e in self.events()}["late"]
        self.assertEqual(2, late["ingest_seq"])
        self.assertNotIn("hunter2", late["prompt"])
        self.assertEqual("truncated", late["content_state"])
        self.assertEqual(capture.digest(late["prompt"]), late["prompt_digest"])
        self.assertEqual("2026-11-24T00:00:00+00:00", late["occurred_at"])

    def test_a_full_store_keeps_metadata_and_names_the_gap(self):
        with mock.patch.object(capture, "STORE_QUOTA_BYTES", 0):
            self.prompt("no room")
        (event,) = self.events()
        self.assertEqual((None, "quota"), (event["prompt"], event["content_state"]))

    def test_hook_failure_is_recorded_and_never_raises(self):
        self.directory.mkdir()
        (self.directory / capture.STORE_NAME).mkdir()  # not a database file
        payload = json.dumps({"session_id": "s1", "prompt": "x"})
        with mock.patch.object(capture, "capture_dir", return_value=self.directory):
            capture.hook("UserPromptSubmit", payload, "claude")
        report = capture.status(self.directory)
        self.assertEqual(1, report["capture_failures"])
        self.assertIn("UserPromptSubmit", report["last_failure"])

    def test_only_prompts_the_user_typed_are_captured(self):
        notice = "<task-notification>task finished</task-notification>"
        self.assertIsNone(self.prompt(notice))
        self.assertIsNone(self.prompt("[Request interrupted by user for tool use]"))
        system = json.loads(line("u1", notice))
        system["origin"] = {"kind": "task-notification"}
        typed = json.loads(line("u2", "typed"))
        typed["origin"] = {"kind": "human"}
        summary = json.loads(line("u3", "continued session summary"))
        summary["isCompactSummary"] = True
        self.transcript.write_text(
            "".join(json.dumps(record) + "\n" for record in (system, typed, summary))
        )
        self.prompt("first")  # creates the session row
        self.session()
        prompts = [e["prompt"] for e in self.events()]
        self.assertEqual(["first", "typed"], prompts)

    def test_a_payload_without_a_session_is_ignored_not_counted(self):
        capture.enqueue("SessionStart", {}, "claude", self.directory, "workspace")
        self.assertEqual(0, capture.status(self.directory)["capture_failures"])

    def test_a_held_reconcile_lock_skips_instead_of_waiting(self):
        self.directory.mkdir()
        with open(self.directory / "reconcile.lock", "a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            self.assertIn("skipped", capture.reconcile(self.directory)[0])


class CaptureDirectoryTests(unittest.TestCase):
    def test_an_explicit_directory_keeps_tests_out_of_the_real_store(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with mock.patch.dict(os.environ, {"HY_HOME_CAPTURE_DIR": temporary}):
                self.assertEqual(Path(temporary), capture.capture_dir())
        with mock.patch.dict(os.environ, {"HY_HOME_CAPTURE_DIR": ""}):
            self.assertEqual(capture.CAPTURE_DIRECTORY, capture.capture_dir().name)


if __name__ == "__main__":
    unittest.main()
