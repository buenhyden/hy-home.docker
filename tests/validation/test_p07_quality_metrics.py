"""Synthetic safety and self-observation contracts for the P07 fixture."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

import yaml

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples/operations/quality-metrics"
SPEC = importlib.util.spec_from_file_location(
    "p07_quality_acceptance", FIXTURE / "acceptance.py"
)
assert SPEC and SPEC.loader
acceptance = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(acceptance)


class AlloySelfObservationContract(unittest.TestCase):
    def test_fixture_prometheus_scrapes_exact_internal_alloy_target(self):
        config = yaml.safe_load(acceptance.prometheus_config())
        self.assertEqual("1s", config["global"]["scrape_interval"])
        job = config["scrape_configs"][0]
        self.assertEqual("alloy", job["job_name"])
        self.assertEqual(["alloy:12345"], job["static_configs"][0]["targets"])
        self.assertEqual(
            {"alloy", "manage-postgres", "mng-valkey-exporter"},
            {x["job_name"] for x in config["scrape_configs"]},
        )

    def test_changed_dashboard_queries_are_extracted_and_semantically_checked(self):
        queries = acceptance.dashboard_panel_queries()
        self.assertEqual(11, len(queries))
        self.assertTrue(all(expr for _, expr in queries))

        def query(expr):
            if "vector(0) == 1" in expr:
                return []
            return [{"value": [1, "1"]}]

        self.assertEqual(11, acceptance.validate_dashboard_queries(query, queries))
        with self.assertRaises(AssertionError):
            acceptance.validate_dashboard_queries(lambda _: [], queries)
        with self.assertRaises(AssertionError):
            acceptance.validate_dashboard_queries(
                lambda _: [{"value": [1, "NaN"]}], queries
            )

    def test_fixture_keeps_admin_ports_private_and_resource_bounds(self):
        config = yaml.safe_load((FIXTURE / "docker-compose.yml").read_text())
        self.assertTrue(config["networks"]["metrics"]["internal"])
        for service in config["services"].values():
            self.assertNotIn("ports", service)
            self.assertTrue(service["read_only"])
            self.assertIn("mem_limit", service)
            self.assertIn("cpus", service)
        self.assertEqual(["metrics"], config["services"]["alloy"]["networks"])
        command = config["services"]["alloy"]["command"]
        self.assertIn("--server.http.listen-addr=0.0.0.0:12345", command)
        self.assertIn("--disable-reporting=true", command)

    def test_alloy_observation_requires_each_metric_and_never_exports_label_values(
        self,
    ):
        def query(expression):
            return [
                {
                    "metric": {"job": "alloy", "component_id": "sensitive-label"},
                    "value": [1, "0"],
                }
            ]

        observed = acceptance.alloy_observation(query)
        self.assertEqual(set(acceptance.ALLOY_METRICS), set(observed))
        self.assertNotIn("sensitive-label", repr(observed))
        self.assertIn("component_id", observed[acceptance.ALLOY_METRICS[0]])
        with self.assertRaises(AssertionError):
            acceptance.alloy_observation(lambda _: [])
        with self.assertRaises(AssertionError):
            acceptance.alloy_observation(
                lambda _: [{"metric": {"job": "alloy"}, "value": [1, "NaN"]}]
            )

    def test_failed_or_timed_out_command_does_not_echo_arguments_or_stderr(self):
        canary = "synthetic" + "-secret-canary"
        failed = subprocess.CompletedProcess(["docker", canary], 1, "", canary)
        for outcome in (
            failed,
            subprocess.TimeoutExpired(["docker", canary], 60, stderr=canary),
            OSError(canary),
        ):
            with self.subTest(outcome=type(outcome).__name__):
                with mock.patch.object(
                    acceptance.subprocess,
                    "run",
                    side_effect=[outcome]
                    if isinstance(outcome, BaseException)
                    else None,
                    return_value=outcome,
                ):
                    with self.assertRaises(RuntimeError) as caught:
                        acceptance.command(["docker", canary], input=canary)
                    self.assertNotIn(canary, str(caught.exception))
                    self.assertIsNone(caught.exception.__cause__)

    def test_invalid_cli_does_not_echo_unrecognized_arguments(self):
        canary = "synthetic" + "-secret-canary"
        result = subprocess.run(
            [
                sys.executable,
                str(FIXTURE / "acceptance.py"),
                "--alloy-image",
                "a",
                "--prom-image",
                "b",
                "--probe-image",
                "c",
                "--unknown",
                canary,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(2, result.returncode)
        self.assertNotIn(canary, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
