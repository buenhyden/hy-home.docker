"""The observe report reads temporary stores and a fake journal only."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.lib.hooks import session_capture as capture
from scripts.operations import observe
from scripts.operations import session_analysis as analysis
from scripts.operations import task_forecast as forecast

SINCE = "2026-11-18T00:00:00+00:00"
UNTIL = "2026-11-19T00:00:00+00:00"


def fake_journal(lines: dict[str, list[str]]):
    def journal(unit: str, scope: str, since: str, until: str) -> list[str]:
        return lines.get(unit, [])

    return journal


class ObserveTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name) / ".workspace-capture"
        connection = capture.connect(self.directory)
        connection.execute(
            "INSERT INTO events (event_id, workspace_id, provider, session_id,"
            " sequence, event_kind, origin, occurred_at, captured_at)"
            " VALUES ('e1', 'w', 'claude', 's1', 1, 'prompt', 'hook',"
            " '2026-11-18T10:00:00+00:00', '2026-11-18T10:00:01+00:00')"
        )
        connection.execute(
            "INSERT INTO sessions (provider, session_id, completeness, reason)"
            " VALUES ('codex', 's2', 'incomplete', 'transcript format unsupported')"
        )
        connection.close()
        runs = analysis.connect(self.directory)
        runs.execute(
            "INSERT INTO runs (analysis_key, trigger, started_at, finished_at,"
            " state, events, candidates) VALUES ('k1', 'scheduled',"
            " '2026-11-18T18:00:00+00:00', '2026-11-18T18:00:01+00:00',"
            " 'failed', 0, 0)"
        )
        runs.close()
        for task, status in (("T1", "completed"), ("T2", "failed")):
            forecast.forecast(
                self.directory, task, "ci-run", 1, 2, 3,
                forecasted_at="2026-11-18T08:00:00+00:00",
            )  # fmt: skip
            forecast.observe(
                self.directory, task, status,
                "2026-11-18T09:00:00+00:00", "2026-11-18T09:05:00+00:00",
            )  # fmt: skip
        run = self.directory / "dispatch" / "runs" / "r1"
        run.mkdir(parents=True)
        (run / "report.json").write_text(
            json.dumps(
                {
                    "run_id": "r1",
                    "task": "SPEC-0212-TSK-0090",
                    "status": "failed",
                    "elapsed_seconds": 3.0,
                    "units": [{"id": "a", "status": "failed"}],
                }
            )
        )
        self.journal = fake_journal(
            {
                "hyhome-backup.service": [
                    "hyhome-backup.service: Failed with result 'exit-code'.",
                    "RESTIC_PASSWORD=do-not-copy-this",
                    "hyhome-backup.service: Failed with result 'exit-code'.",
                    "Finished hyhome-backup.service - HOME backup.",
                ],
                "hy-home-session-analysis.service": [
                    "Finished hy-home-session-analysis.service.",
                ],
            }
        )

    def report(self) -> dict:
        return observe.report(self.directory, SINCE, UNTIL, journal=self.journal)

    def test_each_source_is_counted_in_the_window(self) -> None:
        result = self.report()
        self.assertEqual(1, result["capture"]["events"])
        self.assertEqual(1, result["capture"]["incomplete_sessions"])
        self.assertEqual({"failed": 1}, result["analysis"]["runs"])
        self.assertEqual({"completed": 1, "failed": 1}, result["forecast"]["outcomes"])
        self.assertEqual({"failed": 1}, result["dispatch"]["runs"])
        backup = result["units"]["hyhome-backup.service"]
        self.assertEqual((2, 1), (backup["failed"], backup["succeeded"]))

    def test_every_failure_names_an_owner_and_a_next_step(self) -> None:
        failures = self.report()["failures"]
        sources = sorted(f["source"] for f in failures)
        self.assertEqual(
            ["analysis", "capture", "dispatch", "forecast", "unit"], sources
        )
        for failure in failures:
            self.assertTrue(failure["owner"])
            self.assertTrue(failure["next"])
        (dispatch_failure,) = [f for f in failures if f["source"] == "dispatch"]
        self.assertEqual("SPEC-0212-TSK-0090", dispatch_failure["owner"])

    def test_no_log_text_reaches_the_report(self) -> None:
        text = json.dumps(self.report())
        self.assertNotIn("do-not-copy-this", text)
        self.assertNotIn("Failed with result", text)

    def test_the_report_states_its_window_and_cost(self) -> None:
        result = self.report()
        self.assertEqual((SINCE, UNTIL), (result["since"], result["until"]))
        self.assertIn("observed_at", result)
        self.assertGreaterEqual(result["cost_seconds"], 0)
        self.assertIn("queue", " ".join(result["unmeasured"]))

    def test_an_unreadable_journal_is_reported_not_hidden(self) -> None:
        def broken(unit, scope, since, until):
            raise OSError("journal unavailable")

        result = observe.report(self.directory, SINCE, UNTIL, journal=broken)
        backup = result["units"]["hyhome-backup.service"]
        self.assertEqual("unreadable", backup["state"])
        self.assertIn(
            "hyhome-backup.service",
            [f["item"] for f in result["failures"] if f["source"] == "unit"],
        )

    def test_an_empty_store_reports_zero_without_failures(self) -> None:
        empty = self.directory.parent / "empty"
        result = observe.report(empty, SINCE, UNTIL, journal=fake_journal({}))
        self.assertEqual(0, result["capture"]["events"])
        self.assertEqual([], result["failures"])


if __name__ == "__main__":
    unittest.main()
