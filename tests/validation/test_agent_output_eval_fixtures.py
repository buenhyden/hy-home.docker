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
        self.assertEqual(8, evaluator.MAX_SENSITIVE_KEY_COMPONENTS)
        self.assertEqual(32, evaluator.MAX_SENSITIVE_KEY_COMPONENT_BYTES)
        self.assertEqual(4_096, evaluator.MAX_SENSITIVE_VALUE_BYTES)

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

    def test_provider_prefixed_credentials_and_auth_headers_use_bounded_key_grammar(
        self,
    ) -> None:
        evaluator = load_eval_module()
        sensitive_keys = (
            "GEMINI_API_KEY",
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GITHUB_TOKEN",
            "AWS_SESSION_TOKEN",
            "SERVICE_SECRET",
            "ID_TOKEN",
            "GOOGLE_APPLICATION_CREDENTIALS",
        )
        sensitive_headers = (
            "X-API-Key",
            "X-Auth-Token",
        )
        safe_assignments = (
            "GEMINI_API_KEY_ROTATION_POLICY=quarterly",
            "OPENAI_API_KEY_ROTATION_POLICY=quarterly",
            "GITHUB_TOKENIZER=enabled",
            "AWS_SESSION_TOKENIZER=enabled",
            "SERVICE_SECRETARY=assigned",
            "GOOGLE_APPLICATION_CREDENTIALS_ROTATION_POLICY=quarterly",
        )
        safe_prose = (
            "GEMINI_API_KEY is named in provider documentation",
            "Use X-API-Key only as a synthetic field label",
            "The local policy discusses GITHUB_TOKEN rotation",
        )

        for key in sensitive_keys:
            payload = f'{key}="fixture-value"'
            with self.subTest(kind="scorer-assignment", key=key):
                result = evaluator.score_text(
                    evaluator.FIXTURES["AOE-DOC-001"],
                    evaluator._pass_text(payload),
                )
                self.assertEqual("fail", result.result)
                self.assertIn("AOE-BLOCK-SENSITIVE-KV", result.block_codes)
            with self.subTest(kind="cli-assignment", key=key):
                cli = self.run_runner(
                    "--fixture",
                    "AOE-DOC-001",
                    "--classification",
                    "synthetic-fixture",
                    "--stdin",
                    input_text=payload,
                )
                self.assertEqual(1, cli.returncode)
                self.assertEqual("FAIL: AOE-INPUT-REJECTED\n", cli.stderr)
                self.assertNotIn("fixture-value", cli.stdout + cli.stderr)

        for header in sensitive_headers:
            payload = f"{header}: fixture-value"
            with self.subTest(kind="scorer-header", header=header):
                result = evaluator.score_text(
                    evaluator.FIXTURES["AOE-DOC-001"],
                    evaluator._pass_text(payload),
                )
                self.assertEqual("fail", result.result)
                self.assertIn("AOE-BLOCK-SENSITIVE-KV", result.block_codes)
            with self.subTest(kind="cli-header", header=header):
                cli = self.run_runner(
                    "--fixture",
                    "AOE-DOC-001",
                    "--classification",
                    "synthetic-fixture",
                    "--stdin",
                    input_text=payload,
                )
                self.assertEqual(1, cli.returncode)
                self.assertEqual("FAIL: AOE-INPUT-REJECTED\n", cli.stderr)
                self.assertNotIn("fixture-value", cli.stdout + cli.stderr)

        for payload in (*safe_assignments, *safe_prose):
            with self.subTest(kind="safe-scorer", payload=payload):
                result = evaluator.score_text(
                    evaluator.FIXTURES["AOE-DOC-001"],
                    evaluator._pass_text(payload),
                )
                self.assertNotIn("AOE-BLOCK-SENSITIVE-KV", result.block_codes)
            with self.subTest(kind="safe-cli", payload=payload):
                cli = self.run_runner(
                    "--fixture",
                    "AOE-DOC-001",
                    "--classification",
                    "synthetic-fixture",
                    "--stdin",
                    input_text=evaluator._pass_text(payload),
                )
                self.assertNotEqual("FAIL: AOE-INPUT-REJECTED\n", cli.stderr)
                self.assertIn("block_failures=0", cli.stdout)

    def test_typed_credential_candidates_cover_assignments_and_false_positives(
        self,
    ) -> None:
        evaluator = load_eval_module()
        sensitive = (
            "PASSWD:=fixture-value",
            "GITHUB_PAT+=fixture-value",
            "service.password?=fixture-value",
            "team__secret=fixture-value",
            "service---token=fixture-value",
            "worker.credentials=fixture-value",
            "OPENAI_API_KEY=fixture-value",
            "OPENAI_KEY=fixture-value",
            "ANTHROPIC_KEY=fixture-value",
            "GEMINI_KEY=fixture-value",
            "GITHUB_KEY=fixture-value",
            "AWS_KEY=fixture-value",
            "AZURE_KEY=fixture-value",
            "GOOGLE_KEY=fixture-value",
            "CLIENT_KEY=fixture-value",
            "OAUTH_KEY=fixture-value",
            "SERVICE_AUTH_KEY=fixture-value",
            "EDGE_ACCESS_KEY=fixture-value",
            "TLS_PRIVATE_KEY=fixture-value",
            "RELEASE_SIGNING_KEY=fixture-value",
            "BACKUP_ENCRYPTION_KEY=fixture-value",
            "GEMINI_PROVIDER_KEY=fixture-value",
            "AWS_ACCESS_KEY_ID=fixture-value",
            "DATABASE_URL=fixture-value",
            "OAUTH_CLIENT_ID=fixture-value",
            "GOOGLE_APPLICATION_CREDENTIALS=fixture-value",
            "X-API-Key: fixture-value",
            "X-Auth-Token: fixture-value",
        )
        safe = (
            "primary_key=fixture-value",
            "foreign_key=fixture-value",
            "cache_key=fixture-value",
            "public_key=fixture-value",
            "keyboard_key=fixture-value",
            "database_key=fixture-value",
            "OPENAI_API_KEY_ROTATION_POLICY=quarterly",
            "GITHUB_TOKENIZER=enabled",
            "TEAM_SECRETARY=assigned",
            "The API key policy is documented without an assignment.",
            "Primary key and foreign key are database concepts.",
        )

        for payload in sensitive:
            with self.subTest(
                kind="scorer-sensitive", key=payload.split("fixture", 1)[0]
            ):
                result = evaluator.score_text(
                    evaluator.FIXTURES["AOE-DOC-001"],
                    evaluator._pass_text(payload),
                )
                self.assertIn("AOE-BLOCK-SENSITIVE-KV", result.block_codes)
            with self.subTest(kind="cli-sensitive", key=payload.split("fixture", 1)[0]):
                cli = self.run_runner(
                    "--fixture",
                    "AOE-DOC-001",
                    "--classification",
                    "synthetic-fixture",
                    "--stdin",
                    input_text=payload,
                )
                self.assertEqual(1, cli.returncode)
                self.assertEqual("FAIL: AOE-INPUT-REJECTED\n", cli.stderr)
                self.assertNotIn("fixture-value", cli.stdout + cli.stderr)

        for payload in safe:
            with self.subTest(kind="scorer-safe", payload=payload):
                result = evaluator.score_text(
                    evaluator.FIXTURES["AOE-DOC-001"],
                    evaluator._pass_text(payload),
                )
                self.assertNotIn("AOE-BLOCK-SENSITIVE-KV", result.block_codes)
            with self.subTest(kind="cli-safe", payload=payload):
                cli = self.run_runner(
                    "--fixture",
                    "AOE-DOC-001",
                    "--classification",
                    "synthetic-fixture",
                    "--stdin",
                    input_text=evaluator._pass_text(payload),
                )
                self.assertNotEqual("FAIL: AOE-INPUT-REJECTED\n", cli.stderr)
                self.assertIn("block_failures=0", cli.stdout)

        for value_bytes in (4_096, 4_097):
            payload = 'OPENAI_API_KEY="' + ("x" * value_bytes) + '"'
            with self.subTest(value_bytes=value_bytes):
                self.assertTrue(evaluator._contains_sensitive_content(payload))
                result = evaluator.score_text(
                    evaluator.FIXTURES["AOE-DOC-001"],
                    evaluator._pass_text(payload),
                )
                self.assertIn("AOE-BLOCK-SENSITIVE-KV", result.block_codes)

    def test_credential_classifier_fails_closed_at_every_shape_boundary(self) -> None:
        evaluator = load_eval_module()
        operators = (":=", "+=", "?=", "=", ":")
        shape_boundaries = (
            ("service" + ("_" * 8) + "token", "fixture-value", True),
            ("service" + ("_" * 9) + "token", "fixture-value", False),
            ("service_a_b_c_d_e_f_token", "fixture-value", True),
            ("service_a_b_c_d_e_f_g_token", "fixture-value", False),
            (("a" * 32) + "_token", "fixture-value", True),
            (("a" * 33) + "_token", "fixture-value", False),
            ("STRIPE_KEY", "x" * 4_096, True),
            ("STRIPE_KEY", "x" * 4_097, False),
        )
        for key, value, expected_bounded in shape_boundaries:
            with self.subTest(kind="shape", key=key[:40], bounded=expected_bounded):
                _components, actual_bounded = evaluator._sensitive_candidate_shape(
                    key, value
                )
                self.assertEqual(expected_bounded, actual_bounded)

        sensitive_keys = (
            "service" + ("_" * 8) + "token",
            "service" + ("_" * 9) + "token",
            "service_a_b_c_d_e_f_token",
            "service_a_b_c_d_e_f_g_token",
            ("a" * 32) + "_token",
            ("a" * 33) + "_token",
            "STRIPE_KEY",
            "X-Authorization",
            "X-Cookie",
            "X-Set-Cookie",
            "SERVICE_AUTH",
            "SERVICE_2_TOKEN",
            "EDGE_COOKIE",
        )
        for key in sensitive_keys:
            for operator in operators:
                payload = f'{key}{operator}"fixture-value"'
                with self.subTest(key=key[:40], operator=operator):
                    self.assertTrue(evaluator._contains_sensitive_assignment(payload))
                    result = evaluator.score_text(
                        evaluator.FIXTURES["AOE-DOC-001"],
                        evaluator._pass_text(payload),
                    )
                    self.assertIn("AOE-BLOCK-SENSITIVE-KV", result.block_codes)

        for value_bytes in (4_096, 4_097):
            payload = 'STRIPE_KEY="' + ("x" * value_bytes) + '"'
            with self.subTest(value_bytes=value_bytes):
                self.assertTrue(evaluator._contains_sensitive_assignment(payload))

        cli_cases = (
            'service_________token="fixture-value"',
            'service_a_b_c_d_e_f_g_token="fixture-value"',
            f'{"a" * 33}_token="fixture-value"',
            'STRIPE_KEY="fixture-value"',
            'X-Authorization: "fixture-value"',
            'STRIPE_KEY="' + ("x" * 4_097) + '"',
        )
        for payload in cli_cases:
            with self.subTest(kind="value-free-cli", key=payload[:40]):
                cli = self.run_runner(
                    "--fixture",
                    "AOE-DOC-001",
                    "--classification",
                    "synthetic-fixture",
                    "--stdin",
                    input_text=payload,
                )
                self.assertEqual(1, cli.returncode)
                self.assertEqual("FAIL: AOE-INPUT-REJECTED\n", cli.stderr)
                self.assertNotIn("fixture-value", cli.stdout + cli.stderr)

        for key in (
            "primary_key",
            "foreign_key",
            "cache_key",
            "public_key",
            "keyboard_key",
            "database_key",
        ):
            with self.subTest(kind="reviewed-safe-namespace", key=key):
                self.assertFalse(
                    evaluator._contains_sensitive_assignment(f"{key}=fixture-value")
                )

    def test_credential_classifier_covers_numeric_and_camel_case_boundaries(
        self,
    ) -> None:
        evaluator = load_eval_module()
        sensitive = (
            "2FA_TOKEN=fixture-value",
            "1PASSWORD_SECRET=fixture-value",
            "SERVICE2_TOKEN=fixture-value",
            "apiKey=fixture-value",
            "clientSecret=fixture-value",
            "refreshToken=fixture-value",
            "accessToken=fixture-value",
            "unknownProviderApiKey=fixture-value",
            "xAuthToken=fixture-value",
            "xSessionCookie=fixture-value",
            "API_KEY_2=fixture-value",
            "apiKey2=fixture-value",
            "GITHUB_TOKEN_2=fixture-value",
        )
        safe = (
            "databaseKey=fixture-value",
            "cacheKey=fixture-value",
            "publicKey=fixture-value",
            "primaryKey=fixture-value",
            "foreignKey=fixture-value",
            "keyboardKey=fixture-value",
            "primary_key_2=fixture-value",
        )
        for payload in sensitive:
            with self.subTest(kind="sensitive", key=payload.split("=", 1)[0]):
                self.assertTrue(evaluator._contains_sensitive_assignment(payload))
        for payload in safe:
            with self.subTest(kind="safe", key=payload.split("=", 1)[0]):
                self.assertFalse(evaluator._contains_sensitive_assignment(payload))

    def test_credential_classifier_covers_version_environment_and_multiline_forms(
        self,
    ) -> None:
        evaluator = load_eval_module()
        sensitive = (
            "apiKeyV2=fixture-value",
            "API_KEY_V2=fixture-value",
            "GITHUB_TOKEN_V2=fixture-value",
            "X-Auth-Token-V2: fixture-value",
            "OPENAI_APIKEY=fixture-value",
            "clientSecretV2=fixture-value",
            "refreshTokenV3=fixture-value",
            "githubTokenProd=fixture-value",
            "OPENAI_API_KEY:\n  fixture-value",
            "Authorization:\n  Bearer fixture-value",
        )
        safe = (
            "primaryKeyV2=fixture-value",
            "database_key_prod=fixture-value",
            "API_KEY_ROTATION_POLICY_V2=quarterly",
            "Authorization:\nBearer is a documented scheme",
        )
        for payload in sensitive:
            with self.subTest(kind="scorer-sensitive", key=payload.splitlines()[0]):
                result = evaluator.score_text(
                    evaluator.FIXTURES["AOE-DOC-001"],
                    evaluator._pass_text("\n" + payload),
                )
                self.assertIn("AOE-BLOCK-SENSITIVE-KV", result.block_codes)
            with self.subTest(kind="cli-sensitive", key=payload.splitlines()[0]):
                cli = self.run_runner(
                    "--fixture",
                    "AOE-DOC-001",
                    "--classification",
                    "synthetic-fixture",
                    "--stdin",
                    input_text=payload,
                )
                self.assertEqual(1, cli.returncode)
                self.assertEqual("FAIL: AOE-INPUT-REJECTED\n", cli.stderr)
                self.assertNotIn("fixture-value", cli.stdout + cli.stderr)
        for payload in safe:
            with self.subTest(kind="safe", key=payload.splitlines()[0]):
                self.assertFalse(evaluator._contains_sensitive_assignment(payload))

        self.assertEqual(1, evaluator.MAX_SENSITIVE_LOOKAHEAD_LINES)
        self.assertEqual(8_192, evaluator.MAX_SENSITIVE_SCAN_LINES)
        self.assertEqual(1_048_576, evaluator.MAX_SENSITIVE_LINE_BYTES)
        self.assertFalse(
            evaluator._contains_sensitive_assignment(
                ("ordinary guidance\n" * evaluator.MAX_SENSITIVE_SCAN_LINES)
            )
        )
        self.assertTrue(
            evaluator._contains_sensitive_assignment(
                "ordinary guidance\n" * (evaluator.MAX_SENSITIVE_SCAN_LINES + 1)
            )
        )
        self.assertFalse(
            evaluator._contains_sensitive_assignment(
                "x" * evaluator.MAX_SENSITIVE_LINE_BYTES
            )
        )
        self.assertTrue(
            evaluator._contains_sensitive_assignment(
                "x" * (evaluator.MAX_SENSITIVE_LINE_BYTES + 1)
            )
        )
        self.assertTrue(
            evaluator._contains_sensitive_assignment(
                "OPENAI_API_KEY:\n\n  fixture-value"
            )
        )

    def test_credential_classifier_covers_fused_qualifiers_and_yaml_value_forms(
        self,
    ) -> None:
        evaluator = load_eval_module()
        sensitive = (
            "API_KEY_VERSION2=fixture-value",
            "API_KEY_VER2=fixture-value",
            "API_KEY_VERSION_2=fixture-value",
            "API_KEY_CI=fixture-value",
            "API_KEY_SANDBOX=fixture-value",
            "clientSecretCi=fixture-value",
            "refreshTokenSandbox=fixture-value",
            "SECRETKEY=fixture-value",
            "AWSSECRETACCESSKEY=fixture-value",
            "OPENAIAPIKEY=fixture-value",
            "openaiapikey=fixture-value",
            "API_KEY_FOO=fixture-value",
            "clientSecretBlue=fixture-value",
            "OPENAI_API_KEY_ROTATION_POLICY_BLUE=fixture-value",
            "OPENAIAPIKEYROTATIONPOLICYROTATIONPOLICY=fixture-value",
        )
        safe = (
            "PUBLICKEY=fixture-value",
            "PRIMARYKEY=fixture-value",
            "DATABASEKEY=fixture-value",
            "CACHEKEY=fixture-value",
            "FOREIGNKEY=fixture-value",
            "KEYBOARDKEY=fixture-value",
            "OPENAIAPIKEYROTATIONPOLICY=quarterly",
            "API_KEY_ROTATION_POLICY_CI=quarterly",
            "OPENAI_API_KEY_ROTATION_POLICY=quarterly",
        )
        multiline = (
            "OPENAI_API_KEY:\n- fixture-value",
            "OPENAI_API_KEY:\n  - fixture-value",
            "OPENAI_API_KEY:\n  |\n    fixture-value",
            "Authorization:\n  >-\n    Bearer fixture-value",
        )
        for payload in sensitive:
            with self.subTest(kind="sensitive", key=payload.split("=", 1)[0]):
                self.assertTrue(evaluator._contains_sensitive_assignment(payload))
        for payload in safe:
            with self.subTest(kind="safe", key=payload.split("=", 1)[0]):
                self.assertFalse(evaluator._contains_sensitive_assignment(payload))
        for payload in multiline:
            with self.subTest(kind="scorer", key=payload.splitlines()[0]):
                scored = evaluator.score_text(
                    evaluator.FIXTURES["AOE-DOC-001"],
                    evaluator._pass_text("\n" + payload),
                )
                self.assertIn("AOE-BLOCK-SENSITIVE-KV", scored.block_codes)
            with self.subTest(kind="cli", key=payload.splitlines()[0]):
                cli = self.run_runner(
                    "--fixture",
                    "AOE-DOC-001",
                    "--classification",
                    "synthetic-fixture",
                    "--stdin",
                    input_text=payload,
                )
                self.assertEqual(1, cli.returncode)
                self.assertEqual("FAIL: AOE-INPUT-REJECTED\n", cli.stderr)
                self.assertNotIn("fixture-value", cli.stdout + cli.stderr)

        exact_value = "v" * evaluator.MAX_SENSITIVE_VALUE_BYTES
        self.assertTrue(
            evaluator._contains_sensitive_assignment(
                f"OPENAI_API_KEY:\n  {exact_value}"
            )
        )
        self.assertTrue(
            evaluator._contains_sensitive_assignment(
                f"OPENAI_API_KEY:\n  {exact_value}x"
            )
        )

    def test_catalog_table_rejects_every_malformed_pipe_row(self) -> None:
        evaluator = load_eval_module()
        holder, root = self.catalog_fixture()
        with holder:
            catalog = root / CATALOG.relative_to(ROOT)
            catalog.write_text(
                catalog.read_text(encoding="utf-8").replace(
                    "| Surface | docs/90.references/** |",
                    "| Surface | docs/90.references/** |\n| MALFORMED HIDDEN ROW |",
                    1,
                ),
                encoding="utf-8",
            )
            self.assertEqual(1, evaluator.check_fixtures(root))

        sections, invalid = evaluator._catalog_sections(
            CATALOG.read_text(encoding="utf-8")
        )
        self.assertFalse(invalid)
        section = sections["AOE-DOC-001"][1]
        self.assertEqual(10, len(evaluator._table_fields(section)))
        self.assertEqual(
            {},
            evaluator._table_fields(
                section.replace(
                    "| Calibration |",
                    "| MALFORMED HIDDEN ROW |\n| Calibration |",
                    1,
                )
            ),
        )

    def test_credential_classifier_derives_fused_exact_keys_and_yaml_indicators(
        self,
    ) -> None:
        evaluator = load_eval_module()
        sensitive = (
            "AWSACCESSKEYID=fixture-value",
            "OAUTHCLIENTID=fixture-value",
            "GOOGLEAPPLICATIONCREDENTIALS=fixture-value",
            "DATABASEURL=fixture-value",
            "SESSIONCOOKIE=fixture-value",
            "PROXYAUTHORIZATION=fixture-value",
            "SESSIONTOKEN=fixture-value",
            "SETCOOKIE=fixture-value",
        )
        safe = (
            "DATABASEURLROTATIONPOLICY=quarterly",
            "SESSIONCOOKIEROTATIONPOLICY=quarterly",
            "PUBLICKEY=fixture-value",
        )
        yaml_continuations = (
            "OPENAI_API_KEY:\n|2",
            "OPENAI_API_KEY:\n|2-",
            "OPENAI_API_KEY:\n>+2",
            "OPENAI_API_KEY:\n|-2",
            "OPENAI_API_KEY:\n-",
            "OPENAI_API_KEY:\n  -",
        )
        for payload in sensitive:
            with self.subTest(kind="sensitive", key=payload.split("=", 1)[0]):
                self.assertTrue(evaluator._contains_sensitive_assignment(payload))
        for payload in safe:
            with self.subTest(kind="safe", key=payload.split("=", 1)[0]):
                self.assertFalse(evaluator._contains_sensitive_assignment(payload))
        for payload in yaml_continuations:
            with self.subTest(kind="yaml", marker=payload.splitlines()[1]):
                self.assertTrue(evaluator._contains_sensitive_assignment(payload))

        for payload in sensitive[:2]:
            with self.subTest(kind="scorer", key=payload.split("=", 1)[0]):
                scored = evaluator.score_text(
                    evaluator.FIXTURES["AOE-DOC-001"],
                    evaluator._pass_text("\n" + payload),
                )
                self.assertIn("AOE-BLOCK-SENSITIVE-KV", scored.block_codes)
            with self.subTest(kind="cli", key=payload.split("=", 1)[0]):
                cli = self.run_runner(
                    "--fixture",
                    "AOE-DOC-001",
                    "--classification",
                    "synthetic-fixture",
                    "--stdin",
                    input_text=payload,
                )
                self.assertEqual(1, cli.returncode)
                self.assertEqual("FAIL: AOE-INPUT-REJECTED\n", cli.stderr)
                self.assertNotIn("fixture-value", cli.stdout + cli.stderr)

        self.assertEqual(1, evaluator.MAX_SENSITIVE_LOOKAHEAD_LINES)
        self.assertTrue(
            evaluator._contains_sensitive_assignment("OPENAI_API_KEY:\n\nfixture")
        )

    def test_catalog_table_requires_one_exact_contiguous_state_machine(self) -> None:
        evaluator = load_eval_module()
        sections, invalid = evaluator._catalog_sections(
            CATALOG.read_text(encoding="utf-8")
        )
        self.assertFalse(invalid)
        section = sections["AOE-DOC-001"][1]
        self.assertEqual(10, len(evaluator._table_fields(section)))
        calibration_line = next(
            line for line in section.splitlines() if line.startswith("| Calibration |")
        )

        malformed_sections = (
            section.replace(
                "| --- | --- |",
                "| Field | Value |\n| --- | --- |",
                1,
            ),
            section.replace("| --- | --- |", "\n| --- | --- |", 1),
            section.replace(
                "| Input Scenario |",
                "| --- | --- |\n| Input Scenario |",
                1,
            ),
            section.replace(
                calibration_line, calibration_line + "\n\n| Extra | value |", 1
            ),
            section.replace(
                calibration_line,
                calibration_line + "\nordinary text\n| MALFORMED |",
                1,
            ),
            section.replace(calibration_line, calibration_line + "\n| --- | --- |", 1),
        )
        for index, malformed in enumerate(malformed_sections):
            with self.subTest(index=index):
                self.assertEqual({}, evaluator._table_fields(malformed))

    def test_credential_classifier_handles_prefixed_fused_and_explicit_yaml_keys(
        self,
    ) -> None:
        evaluator = load_eval_module()
        sensitive = (
            "PRODAWSACCESSKEYID=fixture-value",
            "MYOAUTHCLIENTID=fixture-value",
            "SERVICETOKEN=fixture-value",
            "DBPASSWORD=fixture-value",
            "FOOSECRET=fixture-value",
            "CLOUDCREDENTIAL=fixture-value",
            "MYTOKEN=fixture-value",
        )
        safe = (
            "TOKENIZER=fixture-value",
            "SECRETARY=fixture-value",
            "PUBLICKEY=fixture-value",
            "SERVICETOKENROTATIONPOLICY=quarterly",
            "service token policy guidance",
        )
        explicit_sensitive = (
            "? API_KEY\n: fixture-value",
            '? "API_KEY"\n: fixture-value',
        )
        explicit_safe = (
            "? PUBLIC_KEY\n: fixture-value",
            '? "STATUS"\n: fixture-value',
        )
        for payload in sensitive + explicit_sensitive:
            with self.subTest(kind="sensitive", payload=payload.splitlines()[0]):
                self.assertTrue(evaluator._contains_sensitive_assignment(payload))
        for payload in safe + explicit_safe:
            with self.subTest(kind="safe", payload=payload.splitlines()[0]):
                self.assertFalse(evaluator._contains_sensitive_assignment(payload))

        for payload in (sensitive[0], sensitive[2], explicit_sensitive[0]):
            with self.subTest(kind="scorer", payload=payload.splitlines()[0]):
                scored = evaluator.score_text(
                    evaluator.FIXTURES["AOE-DOC-001"],
                    evaluator._pass_text("\n" + payload),
                )
                self.assertIn("AOE-BLOCK-SENSITIVE-KV", scored.block_codes)
            with self.subTest(kind="cli", payload=payload.splitlines()[0]):
                cli = self.run_runner(
                    "--fixture",
                    "AOE-DOC-001",
                    "--classification",
                    "synthetic-fixture",
                    "--stdin",
                    input_text=payload,
                )
                self.assertEqual(1, cli.returncode)
                self.assertEqual("FAIL: AOE-INPUT-REJECTED\n", cli.stderr)
                self.assertNotIn("fixture-value", cli.stdout + cli.stderr)

    def test_credential_classifier_segments_sensitive_stems_before_qualifiers(
        self,
    ) -> None:
        evaluator = load_eval_module()
        sensitive = (
            "PRODAWSACCESSKEYIDBLUE=fixture-value",
            "MYOAUTHCLIENTIDCANARY=fixture-value",
            "SERVICETOKENBLUE=fixture-value",
            "SERVICETOKENPROD=fixture-value",
            "SERVICETOKENBACKUP=fixture-value",
            "serviceauth=fixture-value",
            "usercookie=fixture-value",
            "mysession=fixture-value",
        )
        safe = (
            "TOKENIZER=fixture-value",
            "SERVICETOKENIZER=fixture-value",
            "SECRETARY=fixture-value",
            "PASSWORDLESS=fixture-value",
            "AWSACCESSKEYIDENTIFIER=fixture-value",
            "PASSWORD_POLICY=minimum-length",
            "NOT_API_KEY_MATERIAL=true",
        )
        observed_sensitive = tuple(
            payload
            for payload in sensitive
            if not evaluator._contains_sensitive_assignment(payload)
        )
        observed_safe = tuple(
            payload
            for payload in safe
            if evaluator._contains_sensitive_assignment(payload)
        )

        scorer = evaluator.score_text(
            evaluator.FIXTURES["AOE-DOC-001"],
            evaluator._pass_text("\n" + sensitive[0]),
        )
        cli = self.run_runner(
            "--fixture",
            "AOE-DOC-001",
            "--classification",
            "synthetic-fixture",
            "--stdin",
            input_text=sensitive[1],
        )
        self.assertEqual(
            ((), (), True, 1, "FAIL: AOE-INPUT-REJECTED\n", False),
            (
                observed_sensitive,
                observed_safe,
                "AOE-BLOCK-SENSITIVE-KV" in scorer.block_codes,
                cli.returncode,
                cli.stderr,
                "fixture-value" in cli.stdout + cli.stderr,
            ),
        )

    def test_explicit_yaml_keys_support_comments_tags_and_multiline_forms(
        self,
    ) -> None:
        evaluator = load_eval_module()
        sensitive = (
            "? API_KEY # comment\n: fixture-value",
            '? "API_KEY" # comment\n: fixture-value',
            "? !!str API_KEY\n: fixture-value",
            "? !vault &credential API_KEY # comment\n: fixture-value",
            "? &credential !!str API_KEY\n: fixture-value",
            "?\n  API_KEY\n: fixture-value",
            "? # deferred key\n  OAUTH_CLIENT_ID # comment\n: fixture-value",
        )
        safe = (
            "? PUBLIC_KEY # comment\n: fixture-value",
            '? !!str "STATUS" # comment\n: fixture-value',
            '? !plain &metadata "STATUS" # comment\n: fixture-value',
            "?\n  PUBLIC_KEY\n: fixture-value",
        )
        observed_sensitive = tuple(
            payload
            for payload in sensitive
            if not evaluator._contains_sensitive_assignment(payload)
        )
        observed_safe = tuple(
            payload
            for payload in safe
            if evaluator._contains_sensitive_assignment(payload)
        )
        self.assertEqual(((), ()), (observed_sensitive, observed_safe))

    def test_catalog_table_rejects_competing_and_indented_pipe_rows(self) -> None:
        evaluator = load_eval_module()
        sections, invalid = evaluator._catalog_sections(
            CATALOG.read_text(encoding="utf-8")
        )
        self.assertFalse(invalid)
        section = sections["AOE-DOC-001"][1]
        calibration_line = next(
            line for line in section.splitlines() if line.startswith("| Calibration |")
        )
        surface_line = next(
            line for line in section.splitlines() if line.startswith("| Surface |")
        )
        malformed_sections = (
            "| Other | Table |\n| --- | --- |\n" + section,
            section.replace("| Field | Value |", " | Field | Value |", 1),
            section.replace(surface_line, "  " + surface_line, 1),
            section.replace(
                calibration_line,
                calibration_line + "\n\n  | Extra | value |",
                1,
            ),
        )
        self.assertEqual(10, len(evaluator._table_fields(section)))
        for index, malformed in enumerate(malformed_sections):
            with self.subTest(index=index):
                self.assertEqual({}, evaluator._table_fields(malformed))

    def test_catalog_table_rejects_blockquoted_competing_pipe_rows(self) -> None:
        evaluator = load_eval_module()
        sections, invalid = evaluator._catalog_sections(
            CATALOG.read_text(encoding="utf-8")
        )
        self.assertFalse(invalid)
        section = sections["AOE-DOC-001"][1]
        calibration_line = next(
            line for line in section.splitlines() if line.startswith("| Calibration |")
        )
        malformed_sections = (
            "> | Competing | row |\n" + section,
            "> > | Competing | row |\n" + section,
            ">> | Competing | row |\n" + section,
            section.replace(
                calibration_line,
                calibration_line + "\n\n> | Competing | row |",
                1,
            ),
            section.replace(
                calibration_line,
                calibration_line + "\n\n  >   | Competing | row |",
                1,
            ),
        )
        observed = tuple(
            index
            for index, malformed in enumerate(malformed_sections)
            if evaluator._table_fields(malformed) != {}
        )
        self.assertEqual((), observed)

    def test_fixture_catalog_reads_and_parsers_are_preallocation_bounded(self) -> None:
        evaluator = load_eval_module()
        self.assertEqual(64 * 1_024, evaluator.MAX_FIXTURE_CATALOG_BYTES)
        self.assertEqual(64 * 1_024, evaluator.MAX_TYPED_CATALOG_BYTES)
        self.assertEqual(1_024, evaluator.MAX_CATALOG_LINES)
        self.assertEqual(8_192, evaluator.MAX_CATALOG_LINE_BYTES)
        self.assertEqual(8, evaluator.MAX_CATALOG_SECTIONS)
        self.assertEqual(10, evaluator.MAX_CATALOG_FIELDS_PER_SECTION)
        self.assertEqual(8, evaluator.MAX_TYPED_THRESHOLDS)

        source = MODULE.read_text(encoding="utf-8")
        fixture_parser = source.split("def _typed_fixture_thresholds", 1)[1].split(
            "class _SafeArgumentParser", 1
        )[0]
        self.assertNotIn("read_text(", fixture_parser)
        self.assertNotIn("list(re.finditer", fixture_parser)
        self.assertNotIn(".splitlines()", fixture_parser)

        catalog_text = CATALOG.read_text(encoding="utf-8")
        sections, invalid = evaluator._catalog_sections(catalog_text)
        self.assertFalse(invalid)
        self.assertEqual(evaluator.MAX_CATALOG_SECTIONS, len(sections))
        duplicate_sections, duplicate_invalid = evaluator._catalog_sections(
            catalog_text + "\n### AOE-DOC-001: Duplicate\n"
        )
        self.assertTrue(duplicate_invalid)
        self.assertLessEqual(len(duplicate_sections), evaluator.MAX_CATALOG_SECTIONS)
        first_section = sections["AOE-DOC-001"][1]
        exact_fields = evaluator._table_fields(first_section)
        self.assertEqual(evaluator.MAX_CATALOG_FIELDS_PER_SECTION, len(exact_fields))
        self.assertEqual(
            {},
            evaluator._table_fields(
                first_section.replace(
                    "| Calibration |",
                    "| Unexpected | bounded |\n| Calibration |",
                    1,
                )
            ),
        )

        holder, root = self.catalog_fixture()
        with holder:
            catalog = root / CATALOG.relative_to(ROOT)
            contract_path = root / CONTRACT.relative_to(ROOT)
            catalog_bytes = catalog.stat().st_size
            contract_bytes = contract_path.stat().st_size
            with (
                mock.patch.object(
                    evaluator, "MAX_FIXTURE_CATALOG_BYTES", catalog_bytes
                ),
                mock.patch.object(evaluator, "MAX_TYPED_CATALOG_BYTES", contract_bytes),
            ):
                self.assertEqual(0, evaluator.check_fixtures(root))
                catalog.write_bytes(catalog.read_bytes() + b"x")
                self.assertEqual(1, evaluator.check_fixtures(root))

        holder, root = self.catalog_fixture()
        with holder:
            catalog = root / CATALOG.relative_to(ROOT)
            exact_lines = catalog.read_bytes().count(b"\n")
            expected_thresholds = {
                fixture.fixture_id: fixture.pass_threshold
                for fixture in evaluator.FIXTURES.values()
            }
            with (
                mock.patch.object(evaluator, "MAX_CATALOG_LINES", exact_lines),
                mock.patch.object(
                    evaluator,
                    "_typed_fixture_thresholds",
                    return_value=expected_thresholds,
                ),
            ):
                self.assertEqual(0, evaluator.check_fixtures(root))
                catalog.write_bytes(catalog.read_bytes() + b"\n")
                self.assertEqual(1, evaluator.check_fixtures(root))

        holder, root = self.catalog_fixture()
        with holder:
            exact_thresholds = evaluator._typed_fixture_thresholds(root)
            self.assertEqual(evaluator.MAX_TYPED_THRESHOLDS, len(exact_thresholds))
            contract_path = root / CONTRACT.relative_to(ROOT)
            contract_path.write_text(
                contract_path.read_text(encoding="utf-8").replace(
                    "    AOE-ROUTING-001: 0.50",
                    "    AOE-ROUTING-001: 0.50\n    AOE-EXTRA-001: 0.50",
                    1,
                ),
                encoding="utf-8",
            )
            self.assertEqual({}, evaluator._typed_fixture_thresholds(root))

        holder, root = self.catalog_fixture()
        with holder, tempfile.TemporaryDirectory() as external_directory:
            catalog = root / CATALOG.relative_to(ROOT)
            external = pathlib.Path(external_directory) / "catalog.md"
            shutil.copy2(catalog, external)
            catalog.unlink()
            catalog.symlink_to(external)
            self.assertEqual(1, evaluator.check_fixtures(root))

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
