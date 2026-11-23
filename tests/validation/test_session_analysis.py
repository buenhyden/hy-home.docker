"""Session analysis runs on temporary capture stores only."""

from __future__ import annotations

import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.lib.hooks import session_capture as capture
from scripts.operations import session_analysis as analysis


class AnalysisTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name) / ".workspace-capture"

    def prompt(self, text: str, session: str, when: str | None = None) -> None:
        capture.enqueue(
            "UserPromptSubmit",
            {"session_id": session, "prompt": text, "turn_id": f"{session}-{when}"},
            "claude",
            self.directory,
            "workspace",
        )
        if when:
            connection = capture.connect(self.directory)
            connection.execute(
                "UPDATE events SET captured_at=? WHERE event_id=(SELECT event_id"
                " FROM events ORDER BY rowid DESC LIMIT 1)",
                (when,),
            )
            connection.close()

    def repeated(self, sessions=("s1", "s2", "s3"), when=None) -> None:
        for session in sessions:
            self.prompt("please rerun the gate checks", session, when)

    def run_once(self) -> dict:
        return analysis.run(self.directory, "manual")

    def repeats(self, everything=False) -> list[dict]:
        found = analysis.candidates(self.directory, everything)
        return [c for c in found if c["rule"] == "repeated-prompt"]

    def status(self) -> dict:
        return json.loads((self.directory / analysis.STATUS_NAME).read_text())

    def test_a_run_links_candidates_to_events_and_repeats_as_a_no_op(self):
        self.repeated()
        result = self.run_once()
        self.assertEqual("complete", result["state"], result)
        (found,) = self.repeats()
        self.assertEqual(3, found["frequency"])
        self.assertEqual(3, len(found["source_event_ids"]))
        self.assertEqual("pending", found["decision"])
        again = self.run_once()
        self.assertEqual("no new captured events", again["reason"])
        self.assertEqual(3, self.repeats()[0]["frequency"])

    def test_a_held_lease_skips_a_duplicate_run(self):
        connection = analysis.connect(self.directory)
        analysis.acquire(connection, "other:1")
        connection.close()
        self.repeated()
        self.assertEqual("skipped", self.run_once()["state"])
        self.assertEqual([], analysis.candidates(self.directory, True))

    def test_a_replaced_lease_fences_the_commit(self):
        self.repeated()
        original = analysis.aggregate

        def steal(*args):
            other = analysis.connect(self.directory)
            other.execute("UPDATE lease SET token = token + 1")
            other.close()
            return original(*args)

        with mock.patch.object(analysis, "aggregate", steal):
            with self.assertRaises(analysis.Fenced):
                self.run_once()
        self.assertEqual([], analysis.candidates(self.directory, True))
        self.assertEqual("fenced", self.status()["state"])

    def test_cancellation_and_failure_release_the_lease_and_report(self):
        self.repeated()
        for error, state in (
            (KeyboardInterrupt, "cancelled"),
            (RuntimeError, "failed"),
        ):
            with self.subTest(state=state):
                with mock.patch.object(analysis, "aggregate", side_effect=error):
                    with self.assertRaises(error):
                        self.run_once()
                self.assertEqual(state, self.status()["state"])
        self.assertEqual("complete", self.run_once()["state"])

    def test_a_missed_window_is_caught_up_once(self):
        for day, session in zip((15, 16, 17), ("s1", "s2", "s3"), strict=True):
            when = dt.datetime(2026, 11, day, tzinfo=dt.UTC)
            self.repeated((session,), when.isoformat(timespec="seconds"))
        result = self.run_once()
        self.assertEqual(3, result["events"])
        self.repeated(("s4",))
        later = self.run_once()
        self.assertEqual(1, later["events"])
        self.assertEqual(result["window_end"], later["window_start"])

    def test_a_decided_candidate_keeps_its_decision(self):
        self.repeated()
        self.run_once()
        (found,) = self.repeats()
        analysis.decide(self.directory, found["candidate_id"], "rejected", "owner")
        self.repeated(("s4", "s5", "s6"))
        self.run_once()
        (kept,) = self.repeats(everything=True)
        self.assertEqual(("rejected", 3), (kept["decision"], kept["frequency"]))
        with self.assertRaises(LookupError):
            analysis.decide(self.directory, found["candidate_id"], "accepted", "owner")

    def test_capture_gaps_and_failures_become_candidates(self):
        self.prompt("one prompt only", "gap")
        capture.reconcile(self.directory)  # no transcript path: unavailable
        stamp = analysis.stamp(analysis.now() + dt.timedelta(seconds=-1))
        (self.directory / "degraded.log").write_text(f"{stamp} claude Stop OSError\n")
        self.run_once()
        rules = {c["rule"]: c for c in analysis.candidates(self.directory, False)}
        self.assertIn("claude: no transcript path", rules["capture-gap"]["pattern"])
        self.assertEqual(1, rules["capture-failure"]["frequency"])

    def test_an_unreconciled_session_is_named_as_such(self):
        self.prompt("waiting for reconcile", "fresh")
        self.run_once()
        gaps = [
            c
            for c in analysis.candidates(self.directory, False)
            if c["rule"] == "capture-gap"
        ]
        self.assertEqual(["claude: not yet reconciled"], [c["pattern"] for c in gaps])

    def memory_store(self):
        from scripts.lib.ops.memory_capacity import MemoryCapacity
        from scripts.operations import agent_memory as memory

        path = self.directory.parent / ".workspace-memory" / "memory.sqlite3"
        MemoryCapacity(path).reconcile()
        connection = memory.connect(path)
        self.addCleanup(connection.close)

        def writer(request):
            return memory.put(
                connection,
                expected_revision=0,
                workspace_id="test",
                tier="long-term",
                kind="experience",
                review_state="candidate",
                **request,
            )

        return memory, connection, writer

    def accepted(self) -> dict:
        self.repeated()
        self.run_once()
        (found,) = self.repeats()
        analysis.decide(self.directory, found["candidate_id"], "accepted", "owner")
        (intent,) = self.outbox()
        return intent

    def outbox(self) -> list[dict]:
        connection = analysis.connect(self.directory)
        try:
            return [
                {**dict(r), **json.loads(r["request"])}
                for r in connection.execute("SELECT * FROM promotions")
            ]
        finally:
            connection.close()

    def interrupted(self, writer) -> None:
        with mock.patch.object(analysis, "_receipt", side_effect=OSError):
            with self.assertRaises(OSError):
                analysis.promote(self.directory, writer)
        self.assertEqual("pending", self.outbox()[0]["state"])

    def test_an_accepted_candidate_promotes_once_without_session_text(self):
        memory, connection, writer = self.memory_store()
        intent = self.accepted()
        self.assertEqual("pending", intent["state"])
        result = analysis.promote(self.directory, writer)
        self.assertEqual([intent["candidate_id"]], result["promoted"])
        record = memory.get(connection, intent["memory_id"])
        self.assertEqual("candidate", record["provenance"]["review_state"])
        self.assertNotIn("please rerun", record["body"])
        (events,) = [r for r in record["source_refs"] if r["kind"] == "session-events"]
        self.assertEqual(3, len(events["event_ids"]))
        self.assertIn("content_expires_at", events)
        self.assertEqual([], memory.current_records(connection, None, False))
        self.assertEqual([], analysis.promote(self.directory, writer)["promoted"])
        self.assertEqual(1, len(memory.history(connection, intent["memory_id"], 10)))

    def test_a_retry_after_an_interrupted_receipt_writes_once(self):
        memory, connection, writer = self.memory_store()
        intent = self.accepted()
        self.interrupted(writer)
        self.assertEqual(1, len(analysis.promote(self.directory, writer)["promoted"]))
        self.assertEqual(1, len(memory.history(connection, intent["memory_id"], 10)))

    def test_a_retry_does_not_revive_a_record_erased_before_its_receipt(self):
        memory, connection, writer = self.memory_store()
        intent = self.accepted()
        self.interrupted(writer)
        memory.erase(connection, [intent["memory_id"]])
        analysis.promote(self.directory, writer)
        self.assertIsNone(memory.get(connection, intent["memory_id"]))
        self.assertEqual("promoted", self.outbox()[0]["state"])

    def test_a_refused_memory_write_stays_pending_with_its_reason(self):
        self.accepted()
        refused = mock.Mock(
            returncode=4, stdout="", stderr="MEMORY_CAPACITY_EXCEEDED: store limit\n"
        )
        with mock.patch.object(analysis.subprocess, "run", return_value=refused) as cli:
            result = analysis.promote(self.directory)
        arguments = cli.call_args.args[0]
        self.assertEqual(
            ["put", "session-analysis-"], [arguments[2], arguments[3][:17]]
        )
        self.assertIn("candidate", arguments)
        self.assertNotIn("please rerun", cli.call_args.kwargs["input"])
        (intent,) = self.outbox()
        self.assertEqual(1, len(result["pending"]))
        self.assertEqual(("pending", 1), (intent["state"], intent["attempts"]))
        self.assertIn("MEMORY_CAPACITY_EXCEEDED", intent["last_error"])

    def test_a_changed_review_or_a_rejection_is_not_promoted(self):
        _, _, writer = self.memory_store()
        intent = self.accepted()
        store = analysis.connect(self.directory)
        store.execute("UPDATE candidates SET proposed_change='edited'")
        store.close()
        result = analysis.promote(self.directory, writer)
        self.assertEqual(
            ([], [intent["candidate_id"]]), (result["promoted"], result["stale"])
        )
        self.assertEqual("stale", self.outbox()[0]["state"])
        self.prompt("one gap prompt", "gap")
        capture.reconcile(self.directory)
        self.run_once()
        gap = next(
            c
            for c in analysis.candidates(self.directory, False)
            if c["rule"] == "capture-gap"
        )
        analysis.decide(self.directory, gap["candidate_id"], "rejected", "owner")
        self.assertEqual(1, len(self.outbox()))

    def test_install_writes_a_persistent_daily_timer(self):
        units = self.directory.parent / "units"
        with mock.patch.object(analysis.subprocess, "run") as systemctl:
            result = analysis.install_timer(units)
        timer = (units / f"{analysis.UNIT}.timer").read_text()
        service = (units / f"{analysis.UNIT}.service").read_text()
        self.assertIn("OnCalendar=*-*-* 03:00:00 Asia/Seoul", timer)
        self.assertIn("Persistent=true", timer)
        self.assertIn("run --trigger scheduled", service)
        self.assertNotIn("Restart=", service)
        self.assertEqual("hy-home-session-analysis.timer", result["timer"])
        self.assertEqual(2, systemctl.call_count)


if __name__ == "__main__":
    unittest.main()
