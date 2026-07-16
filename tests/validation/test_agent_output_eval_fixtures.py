from __future__ import annotations

import importlib.util
import contextlib
import io
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts/validation/agent_output_eval.py"
RUNNER = ROOT / "scripts/validation/run-agent-output-eval-fixtures.sh"
CATALOG = ROOT / "docs/90.references/data/governance/agent-output-eval-fixtures.md"
CONTRACT = ROOT / "docs/00.agent-governance/contracts/agent-catalog.yaml"

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
    def run_runner(self, *arguments: str, input_text: str | None = None):
        return subprocess.run(
            [str(RUNNER), *arguments],
            cwd=ROOT,
            input=input_text,
            capture_output=True,
            text=True,
            check=False,
        )

    def catalog_fixture(self) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path]:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        catalog = root / CATALOG.relative_to(ROOT)
        contract = root / CONTRACT.relative_to(ROOT)
        catalog.parent.mkdir(parents=True, exist_ok=True)
        contract.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(CATALOG, catalog)
        shutil.copy2(CONTRACT, contract)
        return directory, root

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
        result = self.run_runner("--check-fixtures", "--check-regressions")

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("fixtures_expected=8", result.stdout)
        self.assertIn("regressions_expected=10", result.stdout)
        self.assertIn("fixtures_check=pass", result.stdout)
        self.assertIn("regressions_check=pass", result.stdout)

    def test_fixture_and_regression_checks_support_separate_and_combined_modes(
        self,
    ) -> None:
        fixtures = self.run_runner("--check-fixtures")
        regressions = self.run_runner("--check-regressions")
        combined = self.run_runner("--check-fixtures", "--check-regressions")

        self.assertEqual(0, fixtures.returncode, fixtures.stdout + fixtures.stderr)
        self.assertIn("fixtures_check=pass", fixtures.stdout)
        self.assertNotIn("regressions_check=", fixtures.stdout)
        self.assertEqual(
            0, regressions.returncode, regressions.stdout + regressions.stderr
        )
        self.assertNotIn("fixtures_check=", regressions.stdout)
        self.assertIn("regressions_check=pass", regressions.stdout)
        self.assertEqual(0, combined.returncode, combined.stdout + combined.stderr)
        self.assertIn("fixtures_check=pass", combined.stdout)
        self.assertIn("regressions_check=pass", combined.stdout)

    def test_runner_is_directly_executable_and_strict(self) -> None:
        self.assertTrue(os.access(RUNNER, os.X_OK))
        result = self.run_runner("--check-fixtures", "--check-regressions")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

        rejected = self.run_runner("--check-fixtures", "unexpected-value")
        self.assertEqual(2, rejected.returncode)
        self.assertEqual("FAIL: AOE-ARGUMENTS-INVALID\n", rejected.stderr)

        duplicate = self.run_runner("--check-fixtures", "--check-fixtures")
        self.assertEqual(2, duplicate.returncode)
        self.assertEqual("FAIL: AOE-ARGUMENTS-INVALID\n", duplicate.stderr)

    def test_catalog_sections_are_exact_and_section_bound(self) -> None:
        evaluator = load_eval_module()
        mutations = {
            "duplicate": lambda text: (
                text + "\n### AOE-DOC-001: Stage Reference Update\n"
            ),
            "swapped-label": lambda text: text.replace(
                "### AOE-DOC-001: Stage Reference Update",
                "### AOE-DOC-001: Provider Surface Parity",
            ),
            "moved-context": lambda text: text.replace(
                "`docs/99.templates/templates/common/reference.template.md`, ", ""
            ),
            "calibration": lambda text: text.replace(
                "`CAL-AOE-DOC-001`; pass threshold `0.50`",
                "`CAL-AOE-PROVIDER-001`; pass threshold `0.75`",
            ),
            "regression": lambda text: text.replace(
                "`AOE-REG-010=pass`", "`AOE-REG-999=pass`"
            ),
            "block-code": lambda text: text.replace(
                "`AOE-BLOCK-REFERENCE-AUTHORITY`",
                "`AOE-BLOCK-LIVE-STATE`",
            ),
            "unexpected-field": lambda text: text.replace(
                "| Surface | docs/90.references/** |",
                "| Surface | docs/90.references/** |\n| Unexpected Field | value |",
                1,
            ),
            "duplicate-field": lambda text: text.replace(
                "| Surface | docs/90.references/** |",
                "| Surface | docs/90.references/** |\n| Surface | docs/90.references/** |",
                1,
            ),
            "missing-field": lambda text: text.replace(
                "| Input Scenario | User asks to add or continue a source-backed research, audit, or data reference. |\n",
                "",
                1,
            ),
            "moved-field": lambda text: text.replace(
                "| Surface | docs/90.references/** |\n",
                "",
                1,
            ).replace(
                "| Calibration | `CAL-AOE-DOC-001`; pass threshold `0.50`. |",
                "| Calibration | `CAL-AOE-DOC-001`; pass threshold `0.50`. |\n| Surface | docs/90.references/** |",
                1,
            ),
            "swapped-fields": lambda text: text.replace(
                "| Surface | docs/90.references/** |\n| Input Scenario | User asks to add or continue a source-backed research, audit, or data reference. |",
                "| Input Scenario | User asks to add or continue a source-backed research, audit, or data reference. |\n| Surface | docs/90.references/** |",
                1,
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                holder, root = self.catalog_fixture()
                with holder:
                    path = root / CATALOG.relative_to(ROOT)
                    path.write_text(
                        mutate(path.read_text(encoding="utf-8")), encoding="utf-8"
                    )
                    self.assertEqual(1, evaluator.check_fixtures(root))

    def test_catalog_thresholds_are_bound_to_typed_contract(self) -> None:
        evaluator = load_eval_module()
        holder, root = self.catalog_fixture()
        with holder:
            contract = root / CONTRACT.relative_to(ROOT)
            contract.write_text(
                contract.read_text(encoding="utf-8").replace(
                    "    AOE-DOC-001: 0.50", "    AOE-DOC-001: 0.75"
                ),
                encoding="utf-8",
            )
            self.assertEqual(1, evaluator.check_fixtures(root))

    def test_catalog_narrative_fields_are_bound_to_typed_fixtures(self) -> None:
        evaluator = load_eval_module()
        mutations = (
            (
                "Input Scenario",
                "User asks to add or continue a source-backed research, audit, or data reference.",
            ),
            (
                "Expected Output",
                "Adds or updates a reference document with required sections, source links, related documents, index updates, and progress evidence.",
            ),
            (
                "Scoring Criteria",
                "Scope routing, source grounding, reference-template compliance, index synchronization, generated LLM Wiki freshness, validation evidence.",
            ),
            (
                "Block Conditions",
                "Active policy hidden inside reference docs; missing sources for external claims; secret/raw-log content; stale target paths.",
            ),
            (
                "Evidence",
                "`git diff --check`, LLM Wiki freshness, doc traceability when relevant, doc implementation alignment, repo contracts.",
            ),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                holder, root = self.catalog_fixture()
                with holder:
                    path = root / CATALOG.relative_to(ROOT)
                    path.write_text(
                        path.read_text(encoding="utf-8").replace(
                            f"| {field} | {value} |",
                            f"| {field} | altered canonical narrative |",
                            1,
                        ),
                        encoding="utf-8",
                    )
                    self.assertEqual(1, evaluator.check_fixtures(root))

    def test_cli_rejects_unsafe_or_sensitive_inputs_value_free(self) -> None:
        token_key = "to" + "ken"
        password_key = "pass" + "word"
        cases = (
            ("absolute-passwd", ["--output", "/etc/passwd"], None),
            ("absolute-hosts", ["--output", "/etc/hosts"], None),
            (
                "quoted-json-token",
                ["--stdin"],
                f'{{"{token_key}": "synthetic-value"}}',
            ),
            (
                "quoted-yaml-password",
                ["--stdin"],
                f'{password_key}: "synthetic-value"',
            ),
            (
                "quoted-json-aws-access-key",
                ["--stdin"],
                '{"AWS_ACCESS_KEY_ID": "synthetic-value"}',
            ),
            (
                "env-aws-secret-key",
                ["--stdin"],
                "AWS_SECRET_ACCESS_KEY='synthetic-value'",
            ),
            (
                "quoted-yaml-database-url",
                ["--stdin"],
                'DATABASE_URL: "synthetic-value"',
            ),
            (
                "quoted-env-oauth-client",
                ["--stdin"],
                "'OAUTH_CLIENT_ID'='synthetic-value'",
            ),
        )
        for label, source_args, input_text in cases:
            with self.subTest(label=label):
                result = self.run_runner(
                    "--fixture",
                    "AOE-DOC-001",
                    "--classification",
                    "synthetic-fixture",
                    *source_args,
                    input_text=input_text,
                )
                self.assertNotEqual(0, result.returncode)
                rendered = result.stdout + result.stderr
                self.assertNotIn("/etc/passwd", rendered)
                self.assertNotIn("/etc/hosts", rendered)
                self.assertNotIn("synthetic-value", rendered)
                self.assertNotIn("Traceback", rendered)

    def test_repo_input_reader_rejects_outside_symlink_fifo_and_prohibited_classes(
        self,
    ) -> None:
        evaluator = load_eval_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            allowed = root / "tests/fixtures/agent-output-eval"
            allowed.mkdir(parents=True)
            safe = allowed / "synthetic.md"
            safe.write_text("synthetic fixture", encoding="utf-8")
            subprocess.run(
                ["git", "add", "tests/fixtures/agent-output-eval/synthetic.md"],
                cwd=root,
                check=True,
            )
            self.assertEqual(
                "synthetic fixture",
                evaluator._read_synthetic_path(
                    root, pathlib.Path("tests/fixtures/agent-output-eval/synthetic.md")
                ),
            )

            outside = root / "outside.md"
            outside.write_text("outside-value", encoding="utf-8")
            (allowed / "linked.md").symlink_to(outside)
            os.mkfifo(allowed / "pipe.md")
            prohibited = allowed / "auth-token.log"
            prohibited.write_text("value", encoding="utf-8")
            (allowed / ".env.local").write_text("value", encoding="utf-8")
            for path in (
                pathlib.Path("outside.md"),
                pathlib.Path("tests/fixtures/agent-output-eval/linked.md"),
                pathlib.Path("tests/fixtures/agent-output-eval/pipe.md"),
                pathlib.Path("tests/fixtures/agent-output-eval/auth-token.log"),
                pathlib.Path("tests/fixtures/agent-output-eval/.env.local"),
                pathlib.Path("tests/fixtures/agent-output-eval/oauth-client.json"),
                pathlib.Path("tests/fixtures/agent-output-eval/.auth.yaml"),
                pathlib.Path("tests/fixtures/agent-output-eval/credentials.backup"),
                pathlib.Path("tests/fixtures/agent-output-eval/token-store.txt"),
                pathlib.Path("tests/fixtures/agent-output-eval/evaluation.log"),
                pathlib.Path("tests/fixtures/agent-output-eval/shell-history.txt"),
                pathlib.Path("tests/fixtures/agent-output-eval/.oauthrc"),
                pathlib.Path("tests/fixtures/agent-output-eval/.authrc"),
                pathlib.Path("tests/fixtures/agent-output-eval/.credentialstore"),
                pathlib.Path("tests/fixtures/agent-output-eval/.tokenfile"),
                pathlib.Path("tests/fixtures/agent-output-eval/.logdata"),
                pathlib.Path("tests/fixtures/agent-output-eval/.historybackup"),
            ):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    evaluator._read_synthetic_path(root, path)

    def test_repo_input_reader_requires_git_tracked_regular_input(self) -> None:
        evaluator = load_eval_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            allowed = root / "tests/fixtures/agent-output-eval"
            allowed.mkdir(parents=True)
            relative = pathlib.Path(
                "tests/fixtures/agent-output-eval/reviewed-synthetic.md"
            )
            candidate = root / relative
            candidate.write_text("reviewed synthetic fixture", encoding="utf-8")

            with self.assertRaises(ValueError):
                evaluator._read_synthetic_path(root, relative)

            subprocess.run(["git", "add", relative.as_posix()], cwd=root, check=True)
            self.assertEqual(
                "reviewed synthetic fixture",
                evaluator._read_synthetic_path(root, relative),
            )

    def test_composite_environment_credentials_are_rejected_in_bounded_formats(
        self,
    ) -> None:
        evaluator = load_eval_module()
        sensitive_cases = (
            '{"AWS_ACCESS_KEY_ID": "synthetic-value"}',
            "AWS-SECRET-ACCESS-KEY='synthetic-value'",
            'DATABASE_URL: "synthetic-value"',
            "'oauth_client_id' = 'synthetic-value'",
        )
        for payload in sensitive_cases:
            with self.subTest(payload=payload.split("synthetic", 1)[0]):
                self.assertTrue(evaluator._contains_sensitive_content(payload))

        self.assertFalse(
            evaluator._contains_sensitive_content(
                "NOT_AWS_ACCESS_KEY_ID documents a synthetic field name"
            )
        )

    def test_common_compound_credentials_are_boundary_aware_and_value_free(
        self,
    ) -> None:
        evaluator = load_eval_module()
        api_key_assignment = "_".join(("API", "KEY")) + '="fixture-value"'
        client_secret_assignment = "-".join(("client", "secret")) + ": 'fixture-value'"
        sensitive_cases = (
            api_key_assignment,
            client_secret_assignment,
            'ACCESS_TOKEN = "fixture-value"',
            "refresh_token='fixture-value'",
            'AZURE_CLIENT_SECRET: "fixture-value"',
            'POSTGRES_PASSWORD="fixture-value"',
            "Authorization: Bearer fixture-value",
            "Cookie: session_id=fixture-value",
            "Set-Cookie: session=fixture-value",
            'COOKIE="fixture-value"',
            'PROXY_AUTHORIZATION="fixture-value"',
            'SESSION_TOKEN="fixture-value"',
        )
        safe_cases = (
            "NOT_API_KEY documents a fixture field",
            "NOT_API_KEY_MATERIAL=fixture",
            "API_KEY_ROTATION_POLICY=quarterly",
            "CLIENT_SECRETARY=assigned",
            "ACCESS_TOKENIZATION=enabled",
            "REFRESH_TOKENIZER=enabled",
            "AZURE_CLIENT_SECRETARY=assigned",
            "PASSWORD_POLICY=strict",
            "authorization guidance is documented",
            "cookie handling and session behavior are documented",
        )
        for payload in sensitive_cases:
            with self.subTest(kind="sensitive", key=payload.split("=", 1)[0]):
                self.assertTrue(evaluator._contains_sensitive_content(payload))
        for payload in safe_cases:
            with self.subTest(kind="safe", text=payload):
                self.assertFalse(evaluator._contains_sensitive_content(payload))

        result = self.run_runner(
            "--fixture",
            "AOE-DOC-001",
            "--classification",
            "synthetic-fixture",
            "--stdin",
            input_text=api_key_assignment,
        )
        self.assertEqual(1, result.returncode)
        self.assertEqual("FAIL: AOE-INPUT-REJECTED\n", result.stderr)
        self.assertNotIn("fixture-value", result.stdout + result.stderr)

    def test_evidence_count_and_combined_byte_limits_are_exact(self) -> None:
        evaluator = load_eval_module()
        self.assertEqual(8, evaluator.MAX_EVIDENCE_FILES)
        self.assertEqual(1_048_576, evaluator.MAX_COMBINED_INPUT_BYTES)

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            allowed = root / "tests/fixtures/agent-output-eval"
            allowed.mkdir(parents=True)
            output = allowed / "output.md"
            output.write_text("o", encoding="utf-8")
            evidence = []
            for index in range(evaluator.MAX_EVIDENCE_FILES + 1):
                path = allowed / f"evidence-{index}.md"
                path.write_text("e", encoding="utf-8")
                evidence.append(path.relative_to(root))
            subprocess.run(
                ["git", "add", "tests/fixtures/agent-output-eval"], cwd=root, check=True
            )
            relative_output = output.relative_to(root)

            self.assertEqual(
                "o" + "\ne" * evaluator.MAX_EVIDENCE_FILES,
                evaluator._read_synthetic_inputs(
                    root,
                    relative_output,
                    evidence[: evaluator.MAX_EVIDENCE_FILES],
                ),
            )
            with self.assertRaises(ValueError):
                evaluator._read_synthetic_inputs(root, relative_output, evidence)
            with self.assertRaises(ValueError):
                evaluator._read_synthetic_inputs(
                    root,
                    relative_output,
                    (evidence[0], evidence[0]),
                )

            boundary_output = allowed / "boundary-output.md"
            boundary_evidence = allowed / "boundary-evidence.md"
            boundary_output.write_text(
                "a" * (evaluator.MAX_COMBINED_INPUT_BYTES - 3),
                encoding="utf-8",
            )
            boundary_evidence.write_text("é", encoding="utf-8")
            subprocess.run(
                [
                    "git",
                    "add",
                    boundary_output.relative_to(root).as_posix(),
                    boundary_evidence.relative_to(root).as_posix(),
                ],
                cwd=root,
                check=True,
            )
            combined = evaluator._read_synthetic_inputs(
                root,
                boundary_output.relative_to(root),
                (boundary_evidence.relative_to(root),),
            )
            self.assertEqual(
                evaluator.MAX_COMBINED_INPUT_BYTES,
                len(combined.encode("utf-8")),
            )

            boundary_evidence.write_text("éx", encoding="utf-8")
            subprocess.run(
                ["git", "add", boundary_evidence.relative_to(root).as_posix()],
                cwd=root,
                check=True,
            )
            with self.assertRaises(ValueError):
                evaluator._read_synthetic_inputs(
                    root,
                    boundary_output.relative_to(root),
                    (boundary_evidence.relative_to(root),),
                )

    def test_stdin_and_evidence_share_combined_utf8_byte_limit(self) -> None:
        evaluator = load_eval_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            allowed = root / "tests/fixtures/agent-output-eval"
            allowed.mkdir(parents=True)
            evidence = allowed / "stdin-evidence.md"
            evidence.write_text("é", encoding="utf-8")
            relative = evidence.relative_to(root)
            subprocess.run(["git", "add", relative.as_posix()], cwd=root, check=True)
            original_root = evaluator.ROOT
            evaluator.ROOT = root
            try:
                for extra, rejected in ((0, False), (1, True)):
                    stdin_text = "a" * (evaluator.MAX_COMBINED_INPUT_BYTES - 3 + extra)
                    stdout = io.StringIO()
                    stderr = io.StringIO()
                    with (
                        self.subTest(extra=extra),
                        contextlib.redirect_stdout(stdout),
                        contextlib.redirect_stderr(stderr),
                        mock.patch.object(sys, "stdin", io.StringIO(stdin_text)),
                    ):
                        result = evaluator.main(
                            [
                                "--fixture",
                                "AOE-DOC-001",
                                "--classification",
                                "synthetic-fixture",
                                "--stdin",
                                "--evidence",
                                relative.as_posix(),
                            ]
                        )
                    if rejected:
                        self.assertEqual(1, result)
                        self.assertEqual(
                            "FAIL: AOE-INPUT-REJECTED\n", stderr.getvalue()
                        )
                    else:
                        self.assertIn(
                            "Agent output eval fixture score", stdout.getvalue()
                        )
                        self.assertNotIn("AOE-INPUT-REJECTED", stderr.getvalue())
            finally:
                evaluator.ROOT = original_root

    def test_combined_input_masking_is_rejected_without_values(self) -> None:
        evaluator = load_eval_module()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            allowed = root / "tests/fixtures/agent-output-eval"
            allowed.mkdir(parents=True)
            first = allowed / "synthetic-output.md"
            second = allowed / "synthetic-evidence.md"
            first.write_text('Stage 00 contract evidence password: "', encoding="utf-8")
            second.write_text('combined-sensitive-value"', encoding="utf-8")
            subprocess.run(
                [
                    "git",
                    "add",
                    "tests/fixtures/agent-output-eval/synthetic-output.md",
                    "tests/fixtures/agent-output-eval/synthetic-evidence.md",
                ],
                cwd=root,
                check=True,
            )
            with self.assertRaises(ValueError) as context:
                evaluator._read_synthetic_inputs(
                    root,
                    pathlib.Path(
                        "tests/fixtures/agent-output-eval/synthetic-output.md"
                    ),
                    (
                        pathlib.Path(
                            "tests/fixtures/agent-output-eval/synthetic-evidence.md"
                        ),
                    ),
                )
            self.assertNotIn("combined-sensitive-value", str(context.exception))

    def test_cli_rejects_unknown_arguments_without_traceback(self) -> None:
        unknown_value = ("to" + "ken") + "=" + "synthetic-value"
        result = self.run_runner("--unknown", unknown_value)

        self.assertEqual(2, result.returncode)
        self.assertEqual("FAIL: AOE-ARGUMENTS-INVALID\n", result.stderr)
        self.assertNotIn("synthetic-value", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
