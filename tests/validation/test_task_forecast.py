"""Task forecasts run on temporary capture stores only."""

from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from scripts.operations import task_forecast as forecast

START = "2026-11-18T10:00:00+00:00"


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
            **extra,
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

    def test_an_empty_score_has_no_coverage_or_bound(self) -> None:
        p50 = forecast.score(self.directory)["quantiles"]["p50"]
        self.assertEqual(
            (0, None, None), (p50["n"], p50["coverage"], p50["coverage_95"])
        )


if __name__ == "__main__":
    unittest.main()
