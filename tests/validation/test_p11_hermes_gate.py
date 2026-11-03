"""Tests for the complete, offline P11 Hermes regression gate."""

from __future__ import annotations

import importlib.util
import io
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts/validation/check-p11-hermes.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "check_p11_hermes_under_test",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load P11 Hermes gate: {MODULE_PATH}")
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


def successful_e2e_runner(*_args, **_kwargs) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout=(
            "PASS: cached image is pinned; missing, malformed and invalid "
            "references are rejected\n"
        ),
        stderr="",
    )


class _RecordingLoader:
    def __init__(self, suite: unittest.TestSuite) -> None:
        self._suite = suite
        self.calls: list[tuple[str, str, str]] = []

    def discover(self, start_dir: str, pattern: str, top_level_dir: str):
        self.calls.append((start_dir, pattern, top_level_dir))
        return self._suite


class P11HermesGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()

    def test_loads_the_complete_offline_regression_directory_once(self) -> None:
        loader = _RecordingLoader(unittest.TestSuite([passing_test()]))

        suite = self.module.load_suite(loader=loader)

        start = str(self.module.HERMES_TESTS)
        self.assertEqual(1, suite.countTestCases())
        self.assertEqual([(start, "test_*.py", start)], loader.calls)

    def test_rejects_zero_discovered_tests(self) -> None:
        stream = io.StringIO()

        self.assertEqual(
            1,
            self.module.run(
                loader=_RecordingLoader(unittest.TestSuite()),
                stream=stream,
                contract_runner=successful_e2e_runner,
            ),
        )
        self.assertIn("no tests discovered", stream.getvalue())

    def test_rejects_skip_only_result(self) -> None:
        stream = io.StringIO()

        self.assertEqual(
            1,
            self.module.run(
                loader=_RecordingLoader(unittest.TestSuite([skipped_test()])),
                stream=stream,
                contract_runner=successful_e2e_runner,
            ),
        )
        self.assertIn("all discovered tests skipped", stream.getvalue())

    def test_propagates_test_failures(self) -> None:
        suite = unittest.TestSuite([passing_test(), failing_test()])

        self.assertEqual(
            1,
            self.module.run(
                loader=_RecordingLoader(suite),
                stream=io.StringIO(),
                contract_runner=successful_e2e_runner,
            ),
        )

    def test_accepts_a_nonempty_successful_suite(self) -> None:
        suite = unittest.TestSuite([passing_test(), skipped_test()])

        self.assertEqual(
            0,
            self.module.run(
                loader=_RecordingLoader(suite),
                stream=io.StringIO(),
                contract_runner=successful_e2e_runner,
            ),
        )

    def test_runs_the_cache_only_e2e_contract_with_a_bounded_environment(self) -> None:
        runner = Mock(side_effect=successful_e2e_runner)

        self.assertEqual(
            0,
            self.module.run_e2e_contract(
                runner=runner,
                stream=io.StringIO(),
            ),
        )
        runner.assert_called_once_with(
            ["/bin/bash", str(self.module.HERMES_E2E_CONTRACT)],
            cwd=self.module.ROOT,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=self.module.E2E_TIMEOUT_SECONDS,
            env=self.module.E2E_ENVIRONMENT,
            check=False,
        )

    def test_rejects_a_failed_cache_only_e2e_contract(self) -> None:
        failed = subprocess.CompletedProcess(
            args=[], returncode=7, stdout="", stderr="synthetic failure"
        )

        self.assertEqual(
            1,
            self.module.run_e2e_contract(
                runner=Mock(return_value=failed),
                stream=io.StringIO(),
            ),
        )

    def test_rejects_a_cache_only_e2e_timeout(self) -> None:
        timeout = subprocess.TimeoutExpired(cmd=["/bin/bash"], timeout=1)

        self.assertEqual(
            1,
            self.module.run_e2e_contract(
                runner=Mock(side_effect=timeout),
                stream=io.StringIO(),
            ),
        )

    def test_rejects_zero_or_unrecognised_e2e_contract_results(self) -> None:
        for output in ("", "PASS: unrelated contract\n"):
            with self.subTest(output=output):
                result = subprocess.CompletedProcess(
                    args=[], returncode=0, stdout=output, stderr=""
                )
                self.assertEqual(
                    1,
                    self.module.run_e2e_contract(
                        runner=Mock(return_value=result),
                        stream=io.StringIO(),
                    ),
                )

    def test_complete_gate_propagates_the_e2e_contract_result(self) -> None:
        e2e_failure = subprocess.CompletedProcess(
            args=[], returncode=1, stdout="", stderr=""
        )
        suite = unittest.TestSuite([passing_test()])

        self.assertEqual(
            1,
            self.module.run(
                loader=_RecordingLoader(suite),
                stream=io.StringIO(),
                contract_runner=Mock(return_value=e2e_failure),
            ),
        )

    def test_rejects_arguments_without_running_tests(self) -> None:
        self.assertEqual(2, self.module.main(["unexpected"]))

    def test_reads_exact_pins_from_the_workload_lock(self) -> None:
        pins = self.module.locked_requirements()

        self.assertIn("cryptography", pins)
        self.assertTrue(all(version[0].isdigit() for version in pins.values()))

    def test_locked_versions_must_all_match_to_run_in_process(self) -> None:
        pins = {"cryptography": "46.0.7", "cffi": "2.1.1"}
        installed = {"cryptography": "46.0.7", "cffi": "2.1.1"}

        self.assertTrue(
            self.module.locked_requirements_present(pins, version=installed.__getitem__)
        )
        installed["cffi"] = "2.0.0"
        self.assertFalse(
            self.module.locked_requirements_present(pins, version=installed.__getitem__)
        )

        def missing(_name: str) -> str:
            raise self.module.importlib.metadata.PackageNotFoundError

        self.assertFalse(self.module.locked_requirements_present(pins, version=missing))

    def test_workload_environment_installs_only_the_hashed_lock_then_reruns(
        self,
    ) -> None:
        calls: list[tuple[list[str], dict]] = []
        controller_sites: list[str] = []

        def runner(argv, **kwargs):
            calls.append((list(argv), kwargs))
            if len(calls) == 3:  # the child: the .pth must already exist
                venv = pathlib.Path(argv[0]).parents[1]
                (pth,) = venv.glob("lib/python*/site-packages/*.pth")
                controller_sites.extend(pth.read_text().split())
            return subprocess.CompletedProcess(argv, 0, "", "")

        self.assertEqual(
            0,
            self.module.run_in_workload_environment(
                runner=runner, stream=io.StringIO()
            ),
        )
        (create, _), (install, _), (child, child_kwargs) = calls
        self.assertEqual([sys.executable, "-m", "venv"], create[:3])
        venv_python = str(pathlib.Path(create[3]) / "bin/python")
        self.assertEqual(venv_python, install[0])
        self.assertIn("--require-hashes", install)
        self.assertIn("--no-deps", install)
        self.assertIn("--only-binary=:all:", install)
        self.assertEqual(str(self.module.HERMES_LOCK), install[-1])
        self.assertEqual([venv_python, str(MODULE_PATH)], child)
        self.assertEqual("1", child_kwargs["env"][self.module.CHILD_MARKER])
        # The controller's packages stay importable after the locked ones.
        self.assertEqual(self.module.controller_site_paths(), controller_sites)

    def test_rerun_keeps_the_runner_descriptor_root_open(self) -> None:
        descriptor = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY)
        try:
            with patch.dict(
                self.module.os.environ,
                {"HYHOME_CI_GATE_ROOT": f"/proc/self/fd/{descriptor}"},
            ):
                self.assertEqual(
                    (descriptor,), self.module.inherited_root_descriptors()
                )
        finally:
            os.close(descriptor)
        with patch.dict(self.module.os.environ, {"HYHOME_CI_GATE_ROOT": str(ROOT)}):
            self.assertEqual((), self.module.inherited_root_descriptors())

    def test_failed_workload_install_stops_before_running_tests(self) -> None:
        calls: list[list[str]] = []

        def runner(argv, **_kwargs):
            calls.append(list(argv))
            code = 1 if "install" in argv else 0
            return subprocess.CompletedProcess(argv, code, "", "")

        stream = io.StringIO()
        self.assertEqual(
            1, self.module.run_in_workload_environment(runner=runner, stream=stream)
        )
        self.assertEqual(2, len(calls))
        self.assertIn("install failed", stream.getvalue())

    def test_child_without_the_locked_versions_fails_closed(self) -> None:
        with (
            patch.dict(self.module.os.environ, {self.module.CHILD_MARKER: "1"}),
            patch.object(
                self.module, "locked_requirements_present", return_value=False
            ),
            patch.object(self.module, "run_in_workload_environment") as bootstrap,
        ):
            self.assertEqual(1, self.module.main([]))
        bootstrap.assert_not_called()

    def test_rejects_a_missing_test_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(
                self.module.HermesGateError,
                "unavailable",
            ):
                self.module.load_suite(root=pathlib.Path(directory))

    def test_rejects_a_symlinked_test_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            test_directory = (
                root / "infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests"
            )
            target = root / "external-tests"
            target.mkdir()
            test_directory.parent.mkdir(parents=True)
            test_directory.symlink_to(target, target_is_directory=True)

            with self.assertRaisesRegex(
                self.module.HermesGateError,
                "not canonical",
            ):
                self.module.load_suite(root=root)


if __name__ == "__main__":
    unittest.main()
