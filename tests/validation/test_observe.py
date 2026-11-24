"""The observe report reads temporary stores and a fake journal only."""

from __future__ import annotations

import datetime as dt
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.lib.hooks import session_capture as capture
from scripts.operations import observe
from scripts.operations import session_analysis as analysis
from scripts.operations import task_forecast as forecast

NOW = dt.datetime.now(dt.UTC).replace(microsecond=0)


def at(**delta) -> str:
    return (NOW + dt.timedelta(**delta)).isoformat()


def fake_journal(lines: dict[str, list[str]]):
    def journal(unit: str, scope: str, since: str, until: str) -> list[str]:
        return lines.get(unit, [])

    return journal


class ObserveTests(unittest.TestCase):
    def setUp(self) -> None:
        global NOW, SINCE, UNTIL
        NOW = dt.datetime.now(dt.UTC).replace(microsecond=0)
        SINCE, UNTIL = at(hours=-30), at(hours=1)
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name) / ".workspace-capture"
        connection = capture.connect(self.directory)
        for event, session, when in (
            ("e1", "s1", at(hours=-1)),
            ("e0", "s0", at(days=-40)),
        ):
            connection.execute(
                "INSERT INTO events (event_id, workspace_id, provider, session_id,"
                " sequence, event_kind, origin, occurred_at, captured_at)"
                " VALUES (?, 'w', 'codex', ?, 1, 'prompt', 'hook', ?, ?)",
                (event, session, when, when),
            )
        for session, reason in (
            ("s1", "3 unreadable lines; transcript format unsupported"),
            ("s0", "transcript format unsupported"),
        ):
            connection.execute(
                "INSERT INTO sessions (provider, session_id, completeness, reason)"
                " VALUES ('codex', ?, 'partial', ?)",
                (session, reason),
            )
        connection.close()
        runs = analysis.connect(self.directory)
        runs.execute(
            "INSERT INTO runs (analysis_key, trigger, started_at, finished_at,"
            " state, events, candidates) VALUES ('k1', 'scheduled', ?, ?,"
            " 'complete', 1, 0)",
            (at(hours=-2), at(hours=-2)),
        )
        runs.close()
        (self.directory / analysis.STATUS_NAME).write_text(
            json.dumps(
                {"trigger": "manual", "started_at": at(minutes=-30), "state": "failed"}
            )
        )
        for task, status in (("T1", "completed"), ("T2", "failed")):
            forecast.forecast(
                self.directory, task, "ci-run", 1, 2, 3, forecasted_at=at(hours=-4),
                assumptions="test", reference_class="test",
            )  # fmt: skip
            forecast.observe(
                self.directory, task, status, at(hours=-3), at(hours=-2, minutes=-55)
            )
        self.write_run("20261119T010000-abcdef", {
            "task": "SPEC-0212-TSK-0090", "status": "failed",
        })  # fmt: skip
        self.journal_lines = {
            "hyhome-backup.service": [
                "hyhome-backup.service: Failed with result 'exit-code'.",
                "journal body marker do-not-copy-this",
                "hyhome-backup.service: Failed with result 'exit-code'.",
                "Finished hyhome-backup.service - HOME backup.",
            ],
            f"{analysis.UNIT}.service": [
                f"Finished {analysis.UNIT}.service.",
            ],
        }
        self.journal = fake_journal(self.journal_lines)

    def write_run(self, name: str, content) -> Path:
        run = self.directory / "dispatch" / "runs" / name
        run.mkdir(parents=True)
        (run / "report.json").write_text(json.dumps(content))
        return run

    def report(self, since=None, until=None, journal=None) -> dict:
        return observe.report(
            self.directory, since or SINCE, until or UNTIL,
            journal=journal or self.journal,
        )  # fmt: skip

    def sources(self, result: dict) -> list[str]:
        return sorted(f["source"] for f in result["failures"])

    def test_each_source_is_counted_in_the_window_only(self) -> None:
        result = self.report()
        self.assertEqual(1, result["capture"]["events"])
        self.assertEqual(1, result["capture"]["incomplete_sessions"])
        self.assertEqual({"complete": 1}, result["analysis"]["runs"])
        self.assertEqual("failed", result["analysis"]["last_status"])
        self.assertEqual({"completed": 1, "failed": 1}, result["forecast"]["outcomes"])
        self.assertEqual({"failed": 1}, result["dispatch"]["runs"])
        backup = result["units"]["hyhome-backup.service"]
        self.assertEqual((2, 1), (backup["failed"], backup["succeeded"]))

    def test_every_failure_names_an_owner_and_a_next_step(self) -> None:
        result = self.report()
        self.assertEqual(
            ["analysis", "capture", "dispatch", "forecast", "unit"],
            self.sources(result),
        )
        for failure in result["failures"]:
            self.assertTrue(failure["owner"])
            self.assertTrue(failure["next"])
        (dispatch_failure,) = [
            f for f in result["failures"] if f["source"] == "dispatch"
        ]
        self.assertEqual("SPEC-0212-TSK-0090", dispatch_failure["owner"])
        (capture_failure,) = [f for f in result["failures"] if f["source"] == "capture"]
        self.assertEqual(
            "unreadable lines; transcript format unsupported", capture_failure["item"]
        )
        self.assertIn(
            "step 4",
            next(f for f in result["failures"] if f["source"] == "unit")["next"],
        )

    def test_no_log_or_worker_text_reaches_the_report(self) -> None:
        self.write_run("20261119T020000-123456", {
            "task": "forged owner text", "status": "rm -rf everything",
        })  # fmt: skip
        self.write_run("not-a-run-id", {"task": "x", "status": "failed"})
        text = json.dumps(self.report())
        for leaked in ("do-not-copy-this", "Failed with result", "forged owner text",
                       "rm -rf everything", "not-a-run-id"):  # fmt: skip
            self.assertNotIn(leaked, text)

    def test_unreadable_run_reports_do_not_stop_the_report(self) -> None:
        self.write_run("20261119T030000-000001", None)
        broken = self.directory / "dispatch" / "runs" / "20261119T030000-000002"
        broken.mkdir()
        (broken / "report.json").symlink_to(broken / "missing")
        failures = [f for f in self.report()["failures"] if f["source"] == "dispatch"]
        self.assertEqual(3, len(failures))

    def test_a_symlinked_store_is_reported_unavailable(self) -> None:
        store = self.directory / capture.STORE_NAME
        store.rename(self.directory / "real.sqlite3")
        store.symlink_to(self.directory / "real.sqlite3")
        result = self.report()
        items = [f["item"] for f in result["failures"] if f["source"] == "capture"]
        self.assertEqual(1, items.count("capture.sqlite3 unavailable"))

    def test_status_file_and_degraded_log_problems_are_failures(self) -> None:
        status = self.directory / analysis.STATUS_NAME
        status.unlink()
        status.symlink_to(self.directory / "elsewhere.json")
        (self.directory / "degraded.log").write_bytes(b"\xff\xfe not utf-8\n")
        items = [f["item"] for f in self.report()["failures"]]
        self.assertIn("analysis-status.json unavailable", items)
        self.assertIn("degraded.log unavailable", items)

    def test_a_forecast_reference_is_echoed_only_in_task_form(self) -> None:
        forecast.forecast(
            self.directory, "free text owner", "ci-run", 1, 2, 3,
            forecasted_at=at(hours=-4), assumptions="test", reference_class="test",
        )  # fmt: skip
        forecast.observe(
            self.directory, "free text owner", "failed", at(hours=-3), at(hours=-2)
        )
        self.assertNotIn("free text owner", json.dumps(self.report()))

    def test_the_report_states_its_window_and_cost(self) -> None:
        result = self.report()
        self.assertEqual((SINCE, UNTIL), (result["since"], result["until"]))
        self.assertIn("observed_at", result)
        self.assertGreaterEqual(result["cost_seconds"], 0)
        self.assertIn("queue", " ".join(result["unmeasured"]))

    def test_an_unreadable_journal_is_reported_not_hidden(self) -> None:
        def broken(unit, scope, since, until):
            raise OSError("journal unavailable")

        result = self.report(journal=broken)
        self.assertEqual(
            "unreadable", result["units"]["hyhome-backup.service"]["state"]
        )

    def test_a_restricted_journal_is_unreadable(self) -> None:
        hint = "Hint: You are currently not seeing messages from other users and the system."
        done = subprocess.CompletedProcess([], 0, "Finished x\n", hint)
        with mock.patch.object(observe.subprocess, "run", return_value=done):
            with self.assertRaises(OSError):
                observe.system_journal("hyhome-backup.service", "system", SINCE, UNTIL)

    def test_a_day_without_any_run_is_a_failure(self) -> None:
        result = self.report(journal=fake_journal({}))
        missing = [f["item"] for f in result["failures"] if f["source"] == "unit"]
        self.assertEqual(sorted(observe.WATCHED), sorted(missing))
        short = self.report(since=at(hours=-25), journal=fake_journal({}))
        self.assertEqual([], [f for f in short["failures"] if f["source"] == "unit"])

    def test_an_empty_store_reports_zero_without_failures(self) -> None:
        empty = self.directory.parent / "empty"
        result = observe.report(empty, at(minutes=-30), UNTIL, journal=fake_journal({}))
        self.assertEqual(0, result["capture"]["events"])
        self.assertEqual([], result["failures"])

    def test_the_retired_analysis_unit_name_still_counts_its_runs(self) -> None:
        journal = dict(self.journal_lines)
        journal[f"{analysis.UNIT}.service"] = []
        journal[f"{analysis.LEGACY_UNIT}.service"] = [
            f"Finished {analysis.LEGACY_UNIT}.service."
        ]
        result = self.report(journal=fake_journal(journal))
        unit = result["units"][f"{analysis.UNIT}.service"]
        self.assertEqual((0, 1), (unit["failed"], unit["succeeded"]))
        self.assertNotIn(
            f"{analysis.UNIT}.service",
            [f["item"] for f in result["failures"] if f["source"] == "unit"],
        )

    def test_a_run_refused_before_any_worker_started_is_blocked(self) -> None:
        self.write_run("20261119T040000-000003", {
            "task": "SPEC-0212-TSK-0110", "status": "failed",
            "units": [{"id": "a", "status": "failed", "reason": "brief scope"}],
        })  # fmt: skip
        result = self.report()
        self.assertEqual({"failed": 1, "blocked": 1}, result["dispatch"]["runs"])
        self.assertIn(
            "20261119T040000-000003 blocked",
            [f["item"] for f in result["failures"]],
        )

    def test_dispatch_units_time_and_cli_cost_are_linked(self) -> None:
        self.write_run("20261119T050000-000004", {
            "task": "SPEC-0212-TSK-0110", "status": "failed",
            "elapsed_seconds": 15.8, "unit_seconds": 11.2,
            "units": [
                {"id": "a", "status": "succeeded", "started": 4.4,
                 "provider": {"name": "claude", "cost_usd": 0.004,
                              "num_turns": 3, "is_error": False}},
                {"id": "b", "status": "failed", "reason": "could not start"},
                {"id": "c", "status": "succeeded", "started": 1.0,
                 "provider": {"name": "forged provider text", "cost_usd": "lots"}},
            ],
        })  # fmt: skip
        result = self.report()
        self.assertIn(
            "20261119T050000-000004 failed", [f["item"] for f in result["failures"]]
        )
        dispatch = result["dispatch"]
        self.assertEqual({"succeeded": 2, "blocked": 1}, dispatch["units"])
        self.assertEqual(
            (15.8, 11.2), (dispatch["elapsed_seconds"], dispatch["unit_seconds"])
        )
        self.assertEqual(
            {"n": 2, "median": 2.7, "max": 4.4}, dispatch["start_wait_seconds"]
        )
        self.assertEqual(
            {"claude": {"units": 1, "cli_estimate_usd": 0.004, "turns": 3,
                        "cost_unknown": 0},
             "unrecognised": {"units": 1, "cli_estimate_usd": 0.0, "turns": 0,
                              "cost_unknown": 1}},
            dispatch["providers"],
        )  # fmt: skip
        self.assertNotIn("forged provider text", json.dumps(dispatch))

    def test_the_candidate_chain_keeps_unobserved_effects_apart(self) -> None:
        store = analysis.connect(self.directory)
        for cid, decision, task, effect in (
            ("c1", "pending", None, None),
            ("c2", "rejected", None, None),
            ("c3", "accepted", None, None),
            ("c4", "accepted", "SPEC-0212-TSK-0111", None),
            ("c5", "accepted", "SPEC-0212-TSK-0111", "improved"),
        ):
            store.execute(
                "INSERT INTO candidates (candidate_id, rule, decision, task_ref,"
                " effect, source_event_ids) VALUES (?, 'r', ?, ?, ?, ?)",
                (cid, decision, task, effect, '["e1"]' if cid != "c1" else "[]"),
            )
        store.execute(
            "INSERT INTO promotions (candidate_id, review_digest, request, state,"
            " created_at) VALUES ('c5', 'd', '{}', 'promoted', ?)",
            (at(hours=-1),),
        )
        store.close()
        chain = self.report()["analysis"]["chain"]
        self.assertEqual(
            {"candidates": 5, "with_sources": 4, "pending": 1, "rejected": 1,
             "accepted": 3, "promoted": 1, "linked_to_task": 2,
             "effect": {"improved": 1}, "effect_unobserved": 1},
            chain,
        )  # fmt: skip

    def test_billed_cost_stays_unmeasured(self) -> None:
        unmeasured = " ".join(self.report()["unmeasured"])
        self.assertIn("billed", unmeasured)

    def test_a_reversed_window_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            self.report(since=UNTIL, until=SINCE)


if __name__ == "__main__":
    unittest.main()
