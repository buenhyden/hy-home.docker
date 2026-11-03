"""Tests for the fixed, offline P03 Hermes regression gate."""

from __future__ import annotations

import importlib.util
import io
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts/validation/check-p03-hermes.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "check_p03_hermes_under_test",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load P03 Hermes gate: {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def passing_test() -> unittest.FunctionTestCase:
    return unittest.FunctionTestCase(lambda: None)


def skipped_test() -> unittest.FunctionTestCase:
    return unittest.FunctionTestCase(unittest.skip("synthetic skip")(lambda: None))


def failing_test() -> unittest.FunctionTestCase:
    def fail() -> None:
        raise AssertionError("synthetic failure")

    return unittest.FunctionTestCase(fail)


class _RecordingLoader:
    def __init__(self, suites: tuple[unittest.TestSuite, ...]) -> None:
        self._suites = iter(suites)
        self.calls: list[tuple[str, str, str]] = []

    def discover(self, start_dir: str, pattern: str, top_level_dir: str):
        self.calls.append((start_dir, pattern, top_level_dir))
        return next(self._suites)


class P03HermesGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()

    def test_loads_only_the_two_fixed_regression_files(self) -> None:
        suites = (
            unittest.TestSuite([passing_test()]),
            unittest.TestSuite([passing_test()]),
        )
        loader = _RecordingLoader(suites)

        suite = self.module.load_suite(loader=loader)

        start = str(self.module.HERMES_TESTS)
        self.assertEqual(2, suite.countTestCases())
        self.assertEqual(
            [
                (start, "test_research_report_plugin.py", start),
                (start, "test_webhook_transport.py", start),
            ],
            loader.calls,
        )

    def test_rejects_zero_discovered_tests(self) -> None:
        loader = _RecordingLoader((unittest.TestSuite(), unittest.TestSuite()))
        stream = io.StringIO()

        self.assertEqual(1, self.module.run(loader=loader, stream=stream))
        self.assertIn("no tests discovered", stream.getvalue())

    def test_rejects_skip_only_result(self) -> None:
        loader = _RecordingLoader(
            (
                unittest.TestSuite([skipped_test()]),
                unittest.TestSuite([skipped_test()]),
            )
        )
        stream = io.StringIO()

        self.assertEqual(1, self.module.run(loader=loader, stream=stream))
        self.assertIn("all discovered tests skipped", stream.getvalue())

    def test_propagates_test_failures(self) -> None:
        loader = _RecordingLoader(
            (
                unittest.TestSuite([passing_test()]),
                unittest.TestSuite([failing_test()]),
            )
        )

        self.assertEqual(1, self.module.run(loader=loader, stream=io.StringIO()))

    def test_rejects_arguments_without_running_tests(self) -> None:
        self.assertEqual(2, self.module.main(["unexpected"]))


if __name__ == "__main__":
    unittest.main()
