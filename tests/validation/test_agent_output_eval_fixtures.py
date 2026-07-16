from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts/validation/agent_output_eval.py"
RUNNER = ROOT / "scripts/validation/run-agent-output-eval-fixtures.sh"

EXPECTED_FIXTURE_IDS = (
    "AOE-ADAPTER-001",
    "AOE-CLOSURE-001",
    "AOE-DOC-001",
    "AOE-HOOK-001",
    "AOE-INFRA-001",
    "AOE-PROVIDER-001",
    "AOE-ROLE-001",
    "AOE-ROUTING-001",
)


def load_eval_module():
    spec = importlib.util.spec_from_file_location("agent_output_eval", MODULE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load eval module: {MODULE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AgentOutputEvalFixtureTests(unittest.TestCase):
    def test_fixture_catalog_has_exact_eight_ids_and_calibration(self) -> None:
        evaluator = load_eval_module()

        self.assertEqual(EXPECTED_FIXTURE_IDS, tuple(sorted(evaluator.FIXTURES)))
        for fixture in evaluator.FIXTURES.values():
            self.assertGreater(fixture.pass_threshold, 0)
            self.assertLessEqual(fixture.pass_threshold, 1)
            self.assertRegex(fixture.calibration_id, r"^CAL-AOE-[A-Z]+-[0-9]{3}$")
            self.assertTrue(fixture.required_context)
            self.assertTrue(fixture.criteria)

    def test_regression_catalog_has_exact_ten_positive_negative_cases(self) -> None:
        evaluator = load_eval_module()

        regressions = evaluator.REGRESSION_CASES
        self.assertEqual(10, len(regressions))
        self.assertEqual(10, len({case.case_id for case in regressions}))
        self.assertEqual(
            {"pass", "fail"}, {case.expected_result for case in regressions}
        )
        self.assertTrue(
            {
                "routing",
                "retired-role",
                "boundary-escalation",
                "hook-denial",
                "bounded-retry",
                "completion-evidence",
                "adapter-rendering",
                "model-fallback",
                "calibration",
            }.issubset({case.category for case in regressions})
        )

    def test_regressions_are_deterministic_and_failure_output_is_value_free(
        self,
    ) -> None:
        evaluator = load_eval_module()

        first = evaluator.run_regressions()
        second = evaluator.run_regressions()
        self.assertEqual(first, second)
        self.assertEqual(10, len(first))
        self.assertTrue(all(result.matched_expectation for result in first))
        rendered = evaluator.render_regression_results(first)
        self.assertNotRegex(rendered, r"sk-[A-Za-z0-9_-]+")
        self.assertNotIn("PRIVATE KEY", rendered)
        self.assertNotIn("raw payload", rendered.lower())

    def test_catalog_check_emits_both_required_ci_markers(self) -> None:
        result = subprocess.run(
            ["bash", str(RUNNER), "--check-fixtures"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("fixtures_expected=8", result.stdout)
        self.assertIn("regressions_expected=10", result.stdout)
        self.assertIn("fixtures_check=pass", result.stdout)
        self.assertIn("regressions_check=pass", result.stdout)

    def test_cli_rejects_unknown_arguments_without_traceback(self) -> None:
        result = subprocess.run(
            ["bash", str(RUNNER), "--unknown"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(2, result.returncode)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
