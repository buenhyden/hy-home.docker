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
