"""Task forecasts run on temporary capture stores only."""

from __future__ import annotations

import math
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.operations import task_forecast as forecast

START = "2026-11-18T10:00:00+00:00"
REQUIRED = {"assumptions": "one runner, no waits", "reference_class": "ci runs"}


class ForecastTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name) / ".workspace-capture"

    def predict(self, task="T1", quantiles=(10, 20, 30), **extra) -> int:
        return forecast.forecast(
            self.directory,
            task,
            "ci-run",
            *quantiles,
            forecasted_at=extra.pop("at", "2026-11-18T09:00:00+00:00"),
            **{**REQUIRED, **extra},
        )

    def test_inverted_negative_or_unknown_inputs_are_refused(self) -> None:
        for quantiles, extra in (
            ((20, 10, 30), {}),
            ((-1, 10, 30), {}),
            ((10, 20, 30), {"unit": "hours"}),
            ((10, 20, 30), {"time_basis": "wall"}),
        ):
            with self.subTest(quantiles=quantiles, extra=extra):
                with self.assertRaises(forecast.ForecastError):
                    self.predict(quantiles=quantiles, **extra)

    def test_non_finite_values_are_refused(self) -> None:
        for quantiles in ((1, 2, math.inf), (math.nan, 2, 3)):
            with self.subTest(quantiles=quantiles):
                with self.assertRaises(forecast.ForecastError):
                    self.predict(quantiles=quantiles)
        self.predict(time_basis="active")
        with self.assertRaises(forecast.ForecastError):
            forecast.observe(
                self.directory,
                "T1",
                "completed",
                START,
                "2026-11-18T10:05:00+00:00",
                active_minutes=math.nan,
            )
        self.assertEqual(0, forecast.score(self.directory)["completed"])

    def test_insert_or_replace_cannot_rewrite_a_row(self) -> None:
        self.predict()
        forecast.observe(
            self.directory, "T1", "failed", START, "2026-11-18T10:05:00+00:00"
        )
        connection = forecast.connect(self.directory)
        for statement in (
            "INSERT OR REPLACE INTO forecasts SELECT * FROM forecasts",
            "REPLACE INTO outcomes SELECT task_ref, 'completed', started_at,"
            " finished_at, active_minutes, runner_wait_minutes,"
            " user_wait_minutes, observed_at FROM outcomes",
        ):
            with self.subTest(statement=statement):
                with self.assertRaises(sqlite3.DatabaseError):
                    connection.execute(statement)
        connection.close()
        self.assertEqual(1, forecast.score(self.directory)["failed"])

    def test_a_future_end_or_active_time_over_elapsed_is_refused(self) -> None:
        self.predict(time_basis="active")
        for finished, active in (
            ("2999-01-01T00:00:00+00:00", 5),
            ("2026-11-18T10:10:00+00:00", 11),
        ):
            with self.subTest(finished=finished, active=active):
                with self.assertRaises(forecast.ForecastError):
                    forecast.observe(
                        self.directory,
                        "T1",
                        "completed",
                        START,
                        finished,
                        active_minutes=active,
                    )

    def test_calibration_is_claimed_per_type_only(self) -> None:
        for task, task_type in (("T1", "ci-run"), ("T2", "build")):
            forecast.forecast(
                self.directory,
                task,
                task_type,
                1,
                2,
                3,
                forecasted_at="2026-11-18T09:00:00+00:00",
                **REQUIRED,
            )
            forecast.observe(
                self.directory, task, "completed", START, "2026-11-18T10:02:00+00:00"
            )
        with mock.patch.object(forecast, "MIN_CALIBRATION_SAMPLE", 2):
            pooled = forecast.score(self.directory)
            one = forecast.score(self.directory, "ci-run")
        self.assertEqual(2, pooled["completed"])
        self.assertNotEqual("empirical", pooled["calibration"])
        self.assertEqual(1, one["completed"])
        self.assertEqual("insufficient sample", one["calibration"])
        with mock.patch.object(forecast, "MIN_CALIBRATION_SAMPLE", 1):
            typed = forecast.score(self.directory, "ci-run")
        self.assertEqual("empirical", typed["calibration"])

    def test_the_cli_refuses_with_exit_2_instead_of_a_traceback(self) -> None:
        self.directory.mkdir(parents=True)
        with mock.patch.dict(os.environ, {"HY_HOME_CAPTURE_DIR": str(self.directory)}):
            refused = forecast.main(
                [
                    "observe",
                    "missing",
                    "--status",
                    "completed",
                    "--started-at",
                    START,
                    "--finished-at",
                    START,
                ]
            )
            (self.directory / forecast.STORE_NAME).unlink()
            (self.directory / forecast.STORE_NAME).symlink_to(self.directory / "x")
            broken = forecast.main(["score"])
        self.assertEqual((2, 2), (refused, broken))

    def test_a_changed_estimate_is_a_new_revision_and_rows_are_immutable(
        self,
    ) -> None:
        self.assertEqual(1, self.predict())
        self.assertEqual(2, self.predict(quantiles=(15, 25, 40)))
        connection = forecast.connect(self.directory)
        for statement in (
            "UPDATE forecasts SET p80 = 99",
            "DELETE FROM forecasts",
        ):
            with self.subTest(statement=statement):
                with self.assertRaises(sqlite3.DatabaseError):
                    connection.execute(statement)
        connection.close()

    def test_an_outcome_needs_a_forecast_made_before_the_start(self) -> None:
        with self.assertRaises(forecast.ForecastError):
            forecast.observe(self.directory, "T1", "completed", START, START)
        self.predict(at="2026-11-18T11:00:00+00:00")
        with self.assertRaises(forecast.ForecastError):
            forecast.observe(
                self.directory, "T1", "completed", START, "2026-11-18T10:20:00+00:00"
            )

    def test_an_outcome_is_recorded_once_and_closes_the_forecast(self) -> None:
        self.predict()
        with self.assertRaises(forecast.ForecastError):
            forecast.observe(
                self.directory, "T1", "completed", START, "2026-11-18T09:59:00+00:00"
            )
        forecast.observe(
            self.directory, "T1", "completed", START, "2026-11-18T10:25:00+00:00"
        )
        for call in (
            lambda: forecast.observe(
                self.directory, "T1", "cancelled", START, "2026-11-18T10:30:00+00:00"
            ),
            lambda: self.predict(at="2026-11-18T12:00:00+00:00"),
        ):
            with self.assertRaises(forecast.ForecastError):
                call()

    def test_active_basis_scores_the_active_minutes(self) -> None:
        self.predict(time_basis="active")
        with self.assertRaises(forecast.ForecastError):
            forecast.observe(
                self.directory, "T1", "completed", START, "2026-11-18T11:00:00+00:00"
            )
        record = forecast.observe(
            self.directory,
            "T1",
            "completed",
            START,
            "2026-11-18T11:00:00+00:00",
            active_minutes=18,
            user_wait_minutes=42,
        )
        self.assertEqual(18, record["actual_minutes"])

    def test_score_reports_coverage_pinball_and_censoring_per_quantile(
        self,
    ) -> None:
        for task, minutes in (("T1", 5), ("T2", 25), ("T3", 50)):
            self.predict(task)
            end = f"2026-11-18T{10 + minutes // 60:02d}:{minutes % 60:02d}:00+00:00"
            forecast.observe(self.directory, task, "completed", START, end)
        self.predict("T4")
        forecast.observe(
            self.directory, "T4", "cancelled", START, "2026-11-18T10:03:00+00:00"
        )
        self.predict("T5")
        forecast.observe(
            self.directory, "T5", "failed", START, "2026-11-18T10:40:00+00:00"
        )
        result = forecast.score(self.directory)
        self.assertEqual(3, result["completed"])
        self.assertEqual(1, result["cancelled"])
        self.assertEqual(1, result["failed"])
        self.assertEqual("insufficient sample", result["calibration"])
        p50 = result["quantiles"]["p50"]
        self.assertEqual(3, p50["n"])
        self.assertAlmostEqual(1 / 3, p50["coverage"])
        # 95% Wilson interval for 1 of 3
        low, high = p50["coverage_95"]
        self.assertAlmostEqual(0.0615, low, places=4)
        self.assertAlmostEqual(0.7923, high, places=4)
        # pinball at p=0.5 for actuals 5, 25, 50 against q=20
        self.assertAlmostEqual((7.5 + 2.5 + 15) / 3, p50["pinball"])

    def finish(self, task, minutes, status="completed", **extra):
        end = f"2026-11-18T{10 + minutes // 60:02d}:{minutes % 60:02d}:00+00:00"
        return forecast.observe(self.directory, task, status, START, end, **extra)

    def test_a_score_never_mixes_time_bases(self) -> None:
        self.predict("T1")
        self.finish("T1", 15)
        self.predict("T2", time_basis="active")
        self.finish("T2", 40, active_minutes=15)
        with mock.patch.object(forecast, "MIN_CALIBRATION_SAMPLE", 1):
            mixed = forecast.score(self.directory, "ci-run")
            elapsed = forecast.score(self.directory, "ci-run", "elapsed")
        self.assertEqual("mixed time bases; score one basis", mixed["calibration"])
        self.assertEqual(
            [("ci-run", "active", 1), ("ci-run", "elapsed", 1)],
            [
                (g["task_type"], g["time_basis"], g["completed"])
                for g in mixed["groups"]
            ],
        )
        self.assertEqual(
            ("empirical", 1), (elapsed["calibration"], elapsed["completed"])
        )

    def test_the_comparable_sample_is_counted_from_earlier_completed_tasks(self):
        self.predict("T1")
        self.finish("T1", 30)  # done at 10:30
        for task, at, extra in (
            ("T2", "2026-11-18T11:00:00+00:00", {}),
            ("T3", "2026-11-18T11:00:00+00:00", {"time_basis": "active"}),
            ("T4", "2026-11-18T10:10:00+00:00", {}),
        ):
            self.predict(task, at=at, sample_size=10, **extra)
        connection = forecast.connect(self.directory)
        prior = dict(
            connection.execute("SELECT task_ref, comparable_prior FROM forecasts")
        )
        connection.close()
        self.assertEqual({"T1": 0, "T2": 1, "T3": 0, "T4": 0}, prior)

    def test_an_outcome_names_its_forecast_and_blocked_or_open_is_not_scored(self):
        self.predict("T1")
        self.predict("T1", quantiles=(12, 22, 32), at="2026-11-18T09:30:00+00:00")
        self.assertEqual(2, self.finish("T1", 20)["revision"])
        connection = forecast.connect(self.directory)
        linked = connection.execute(
            "SELECT forecast_revision FROM outcomes WHERE task_ref='T1'"
        ).fetchone()[0]
        connection.close()
        self.assertEqual(2, linked)
        self.predict("T2")
        self.finish("T2", 90, status="blocked")
        self.predict("T3")
        result = forecast.score(self.directory, "ci-run", "elapsed")
        self.assertEqual(
            (1, 1, 1), (result["completed"], result["blocked"], result["open"])
        )

    def test_a_forecast_without_assumptions_or_reference_class_is_refused(self):
        for missing in ("assumptions", "reference_class"):
            with self.subTest(missing=missing):
                with self.assertRaises(forecast.ForecastError):
                    self.predict(**{missing: " "})
        with self.assertRaises(forecast.ForecastError):
            self.predict(sample_size=True)

    def test_an_empty_score_has_no_coverage_or_bound(self) -> None:
        p50 = forecast.score(self.directory)["quantiles"]["p50"]
        self.assertEqual(
            (0, None, None), (p50["n"], p50["coverage"], p50["coverage_95"])
        )


if __name__ == "__main__":
    unittest.main()
