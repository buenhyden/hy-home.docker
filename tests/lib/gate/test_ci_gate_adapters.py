from __future__ import annotations

import ast
import fcntl
import io
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import tomllib
import unittest
from collections.abc import Mapping
from datetime import UTC, datetime
from unittest import mock

from scripts.lib.gate import ci_gate_adapters as adapters

ROOT = pathlib.Path(__file__).resolve().parents[3]
REAL_SUBPROCESS_RUN = subprocess.run
EXPECTED_SUBCOMMANDS = (
    "verify-metadata-base",
    "check-diff-hygiene",
    "check-shell-syntax",
    "run-unittest",
    "run-npm",
    "run-approved-npm-audit",
    "check-commit-range",
    "install-playwright",
    "run-zizmor-sarif",
)


class ChildRecorder:
    def __init__(
        self,
        results: list[subprocess.CompletedProcess[bytes]] | None = None,
    ) -> None:
        self.calls: list[tuple[tuple[str, ...], dict[str, object]]] = []
        self.results = list(results or [])

    def __call__(
        self,
        argv: tuple[str, ...],
        **kwargs: object,
    ) -> subprocess.CompletedProcess[bytes]:
        self.calls.append((argv, kwargs))
        if self.results:
            return self.results.pop(0)
        stderr = b"Ran 1 test in 0.001s\n\nOK\n" if "unittest" in argv else b""
        return subprocess.CompletedProcess(argv, 0, b"", stderr)


class CiGateAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temporary.name).resolve()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_with_recorder(
        self,
        argv: tuple[str, ...],
        *,
        environ: dict[str, str] | None = None,
        results: list[subprocess.CompletedProcess[bytes]] | None = None,
    ) -> tuple[int, ChildRecorder]:
        recorder = ChildRecorder(results)
        with (
            mock.patch.object(
                adapters,
                "_run_child",
                side_effect=recorder,
                create=True,
            ),
            mock.patch.object(sys, "stdout", io.StringIO()),
            mock.patch.object(sys, "stderr", io.StringIO()),
        ):
            result = adapters.run_adapter(
                self.root,
                argv,
                environ or {"PATH": "/usr/bin"},
            )
        return result, recorder

    def git(self, *arguments: str) -> str:
        result = REAL_SUBPROCESS_RUN(
            ("git", *arguments),
            cwd=self.root,
            env={**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null"},
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def synthetic_merge_with_whitespace(self) -> tuple[str, str]:
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Diagnostic")
        self.git("config", "user.email", "diagnostic@example.invalid")
        self.git("commit", "--allow-empty", "-qm", "chore: Establish common base")
        self.git("switch", "-q", "-c", "feature")
        (self.root / "candidate.txt").write_text("trailing whitespace \n")
        self.git("add", "candidate.txt")
        self.git("commit", "-qm", "fix(ci): Preserve candidate range")
        head = self.git("rev-parse", "HEAD")
        self.git("switch", "-q", "main")
        self.git("commit", "--allow-empty", "-qm", "chore: Advance target")
        base = self.git("rev-parse", "HEAD")
        self.git("merge", "--no-ff", "feature", "-qm", f"Merge {head} into {base}")
        return base, head

    def test_closed_subcommand_catalog_is_exact(self) -> None:
        self.assertEqual(EXPECTED_SUBCOMMANDS, adapters.SUBCOMMANDS)
        self.assertFalse(
            pathlib.Path("scripts/validation/recommend-qa-gates.sh").exists()
        )

    def test_verify_metadata_base_uses_two_literal_git_vectors(self) -> None:
        result, recorder = self.run_with_recorder(
            ("verify-metadata-base",),
            environ={
                "PATH": "/usr/bin",
                "TEMPLATE_GATE_BASE": "0123456789abcdef0123456789abcdef01234567",
            },
        )
        self.assertEqual(0, result)
        self.assertEqual(
            [
                (
                    "git",
                    "cat-file",
                    "-e",
                    "0123456789abcdef0123456789abcdef01234567^{commit}",
                ),
                (
                    "git",
                    "merge-base",
                    "HEAD",
                    "0123456789abcdef0123456789abcdef01234567",
                ),
            ],
            [call[0] for call in recorder.calls],
        )

    def test_check_diff_hygiene_uses_literal_git_diff(self) -> None:
        result, recorder = self.run_with_recorder(("check-diff-hygiene",))
        self.assertEqual(0, result)
        self.assertEqual(
            [("git", "diff", "--check")],
            [call[0] for call in recorder.calls],
        )
        self._assert_descriptor_root_is_passed_to_adapter_children()

    def test_pr_diff_hygiene_checks_the_authenticated_candidate_range(self) -> None:
        base = "1" * 40
        head = "2" * 40
        merge = "3" * 40
        common = "4" * 40
        result, recorder = self.run_with_recorder(
            ("check-diff-hygiene",),
            environ={"PATH": "/usr/bin", "PR_BASE_SHA": base, "PR_HEAD_SHA": head},
            results=[
                subprocess.CompletedProcess(
                    (), 0, f"{merge} {base} {head}\n".encode(), b""
                ),
                subprocess.CompletedProcess((), 0, f"{common}\n".encode(), b""),
                subprocess.CompletedProcess((), 0, b"1\n", b""),
                subprocess.CompletedProcess((), 0, b"", b""),
            ],
        )
        self.assertEqual(0, result)
        self.assertEqual(
            [
                ("git", "rev-list", "--parents", "--max-count=1", "HEAD"),
                ("git", "merge-base", base, head),
                ("git", "rev-list", "--count", f"{base}..{head}"),
                ("git", "diff", "--check", f"{common}..{head}"),
            ],
            [call[0] for call in recorder.calls],
        )

    def test_pr_range_rejects_wrong_merge_parents_and_empty_history(self) -> None:
        base = "1" * 40
        head = "2" * 40
        merge = "3" * 40
        common = "4" * 40
        cases = (
            (
                "swapped-parents",
                [
                    subprocess.CompletedProcess(
                        (), 0, f"{merge} {head} {base}\n".encode(), b""
                    )
                ],
            ),
            (
                "third-parent",
                [
                    subprocess.CompletedProcess(
                        (), 0, f"{merge} {base} {head} {'5' * 40}\n".encode(), b""
                    )
                ],
            ),
            (
                "empty-range",
                [
                    subprocess.CompletedProcess(
                        (), 0, f"{merge} {base} {head}\n".encode(), b""
                    ),
                    subprocess.CompletedProcess((), 0, f"{common}\n".encode(), b""),
                    subprocess.CompletedProcess((), 0, b"0\n", b""),
                ],
            ),
        )
        for label, results in cases:
            with (
                self.subTest(label=label),
                mock.patch.object(
                    adapters,
                    "_run_child",
                    side_effect=ChildRecorder(results),
                ),
                self.assertRaises(adapters.AdapterError) as caught,
            ):
                adapters.run_adapter(
                    self.root,
                    ("check-diff-hygiene",),
                    {
                        "PATH": "/usr/bin",
                        "PR_BASE_SHA": base,
                        "PR_HEAD_SHA": head,
                    },
                )
            self.assertEqual(
                "ci-gate-adapter-pull-request-range", caught.exception.code
            )

    def test_check_shell_syntax_checks_each_nul_tracked_path_once(
        self,
    ) -> None:
        result, recorder = self.run_with_recorder(
            ("check-shell-syntax",),
            results=[
                subprocess.CompletedProcess(
                    ("git",),
                    0,
                    b"scripts/b.sh\0.claude/hooks/c.sh\0",
                    b"",
                ),
                subprocess.CompletedProcess(("bash",), 0, b"", b""),
                subprocess.CompletedProcess(("bash",), 0, b"", b""),
            ],
        )
        self.assertEqual(0, result)
        self.assertEqual(
            [
                (
                    "git",
                    "ls-files",
                    "-z",
                    "--",
                    "scripts/**/*.sh",
                    ".claude/hooks/*.sh",
                ),
                ("bash", "-n", "scripts/b.sh"),
                ("bash", "-n", ".claude/hooks/c.sh"),
            ],
            [call[0] for call in recorder.calls],
        )

    def test_check_shell_syntax_preserves_empty_and_inventory_failure(self) -> None:
        for label, inventory, expected in (
            ("empty", subprocess.CompletedProcess(("git",), 0, b"", b""), 0),
            ("git-failure", subprocess.CompletedProcess(("git",), 9, b"", b""), 9),
        ):
            with self.subTest(label=label):
                result, recorder = self.run_with_recorder(
                    ("check-shell-syntax",), results=[inventory]
                )
                self.assertEqual(expected, result)
                self.assertEqual(1, len(recorder.calls))

    def test_check_shell_syntax_fails_on_a_later_real_bash_input(self) -> None:
        scripts = self.root / "scripts"
        scripts.mkdir()
        (scripts / "valid.sh").write_text("touch syntax-ran\n", encoding="utf-8")
        (scripts / "invalid.sh").write_text("if true; then\n", encoding="utf-8")

        def tracked_then_real_bash(
            argv: tuple[str, ...], **_kwargs: object
        ) -> subprocess.CompletedProcess[bytes]:
            if argv[0] == "git":
                return subprocess.CompletedProcess(
                    argv,
                    0,
                    b"scripts/valid.sh\0scripts/invalid.sh\0",
                    b"",
                )
            return REAL_SUBPROCESS_RUN(
                argv,
                cwd=self.root,
                env={"PATH": "/usr/bin", "LANG": "C"},
                capture_output=True,
            )

        with mock.patch.object(
            adapters, "_run_child", side_effect=tracked_then_real_bash
        ):
            result = adapters.run_adapter(
                self.root,
                ("check-shell-syntax",),
                {"PATH": "/usr/bin", "LANG": "C"},
            )
        self.assertNotEqual(0, result)
        self.assertFalse((self.root / "syntax-ran").exists())

    def test_check_shell_syntax_stops_after_the_first_failure(self) -> None:
        result, recorder = self.run_with_recorder(
            ("check-shell-syntax",),
            results=[
                subprocess.CompletedProcess(
                    ("git",),
                    0,
                    b"scripts/a.sh\0scripts/b.sh\0scripts/c.sh\0",
                    b"",
                ),
                subprocess.CompletedProcess(("bash",), 0, b"", b""),
                subprocess.CompletedProcess(("bash",), 7, b"", b"invalid"),
            ],
        )
        self.assertEqual(7, result)
        self.assertEqual(
            [
                (
                    "git",
                    "ls-files",
                    "-z",
                    "--",
                    "scripts/**/*.sh",
                    ".claude/hooks/*.sh",
                ),
                ("bash", "-n", "scripts/a.sh"),
                ("bash", "-n", "scripts/b.sh"),
            ],
            [call[0] for call in recorder.calls],
        )

    def test_run_unittest_is_admitted_only_in_the_local_context(self) -> None:
        argv = ("run-unittest", "tests.validation.test_one", "-v")
        self.assertTrue(adapters.admits_adapter_invocation(argv, "local"))
        for context in ("pull_request", "push", "push_initial", "workflow_dispatch"):
            with self.subTest(context=context):
                self.assertFalse(adapters.admits_adapter_invocation(argv, context))

    def test_run_unittest_rejects_zero_tests_and_missing_execution_summary(self):
        for output in (b"Ran 0 tests in 0.000s\n\nOK\n", b"", b"OK\n"):
            with self.subTest(output=output):
                with self.assertRaises(adapters.AdapterError) as caught:
                    self.run_with_recorder(
                        ("run-unittest", "tests.validation.test_one", "-v"),
                        results=[subprocess.CompletedProcess((), 0, b"", output)],
                    )
                self.assertEqual("ci-gate-adapter-test-count", caught.exception.code)
        code, _ = self.run_with_recorder(
            ("run-unittest", "tests.validation.test_one", "-v"),
            results=[subprocess.CompletedProcess((), 2, b"", b"load failure")],
        )
        self.assertEqual(2, code)

    def test_required_unittest_gate_rejects_skipped_tests(self):
        with self.assertRaises(adapters.AdapterError) as caught:
            self.run_with_recorder(
                ("run-unittest", "tests.validation.test_one", "-v"),
                results=[
                    subprocess.CompletedProcess(
                        (), 0, b"", b"Ran 2 tests in 0.001s\n\nOK (skipped=1)\n"
                    )
                ],
            )
        self.assertEqual("ci-gate-adapter-tests-skipped", caught.exception.code)

    def test_run_unittest_reads_real_child_summary_and_emits_it_once(self) -> None:
        package = self.root / "tests/lib"
        package.mkdir(parents=True)
        (self.root / "tests/__init__.py").write_text("")
        (package / "__init__.py").write_text("")
        (package / "test_gate_fixture.py").write_text(
            "import unittest\nclass Fixture(unittest.TestCase):\n"
            "    def test_pass(self): self.assertTrue(True)\n"
        )
        output, errors = io.StringIO(), io.StringIO()
        with (
            mock.patch.object(sys, "stdout", output),
            mock.patch.object(sys, "stderr", errors),
        ):
            result = adapters.run_adapter(
                self.root,
                ("run-unittest", "tests.lib.test_gate_fixture", "-v"),
                {"PATH": "/usr/bin"},
            )
        self.assertEqual(0, result)
        self.assertEqual(1, errors.getvalue().count("Ran 1 test in"))
        self.assertIn("\nOK\n", errors.getvalue())

    def test_optional_runtime_skip_grammar_is_closed(self) -> None:
        module = "tests.lib.test_fixture"
        scope = module + ".Runtime"
        valid = ("run-unittest", module, "--optional-runtime-skips", scope, "-v")
        adapters.validate_adapter_argv(valid)
        for tail in (
            ("--optional-runtime-skips",),
            ("--optional-runtime-skips", module),
            ("--optional-runtime-skips", scope + ".test_one"),
            ("--optional-runtime-skips", "tests.lib.test_other.Runtime"),
            ("--optional-runtime-skips", scope, scope),
            ("--optional-runtime-skips", scope, "--optional-runtime-skips", scope),
        ):
            with self.subTest(tail=tail), self.assertRaises(adapters.AdapterError):
                adapters.validate_adapter_argv(("run-unittest", module, *tail, "-v"))

    def test_optional_runtime_skip_real_child_and_required_skip_failure(self) -> None:
        package = self.root / "tests/lib"
        package.mkdir(parents=True)
        (self.root / "tests/__init__.py").write_text("")
        (package / "__init__.py").write_text("")
        fixture = package / "test_fixture.py"
        source = (
            "import unittest\nclass Required(unittest.TestCase):\n"
            "    def test_pass(self): self.assertTrue(True)\n"
            "@unittest.skip('explicit opt-in required')\n"
            "class Runtime(unittest.TestCase):\n"
            "    def test_optional(self): pass\n"
        )
        argv = (
            "run-unittest",
            "tests.lib.test_fixture",
            "--optional-runtime-skips",
            "tests.lib.test_fixture.Runtime",
            "-v",
        )
        fixture.write_text(source)
        output, errors = io.StringIO(), io.StringIO()
        with (
            mock.patch.object(sys, "stdout", output),
            mock.patch.object(sys, "stderr", errors),
        ):
            self.assertEqual(
                0, adapters.run_adapter(self.root, argv, {"PATH": "/usr/bin"})
            )
        self.assertEqual(1, errors.getvalue().count("Ran 2 tests in"))
        fixture.write_text(
            source.replace(
                "    def test_pass",
                "    @unittest.skip('required missing')\n    def test_pass",
            )
        )
        with (
            mock.patch.object(sys, "stdout", io.StringIO()),
            mock.patch.object(sys, "stderr", io.StringIO()),
        ):
            with self.assertRaises(adapters.AdapterError) as caught:
                adapters.run_adapter(self.root, argv, {"PATH": "/usr/bin"})
        self.assertEqual("ci-gate-adapter-tests-skipped", caught.exception.code)

    def test_optional_runtime_skip_receipts_must_match_exact_scopes(self) -> None:
        module = "tests.lib.test_fixture"
        scope = module + ".Runtime"
        argv = ("run-unittest", module, "--optional-runtime-skips", scope, "-v")
        receipt = (
            b"test_one (tests.lib.test_fixture.Runtime.test_one) ... skipped 'opt-in'\n"
        )
        summary = b"Ran 2 tests in 0.001s\n\nOK (skipped=1)\n"
        code, recorder = self.run_with_recorder(
            argv, results=[subprocess.CompletedProcess((), 0, b"", receipt + summary)]
        )
        self.assertEqual(0, code)
        self.assertEqual(
            ("python3", "-m", "unittest", module, "-v"), recorder.calls[0][0]
        )
        passed = b"test_one (tests.lib.test_fixture.Runtime.test_one) ... ok\nRan 1 test in 0.001s\n\nOK\n"
        code, _ = self.run_with_recorder(
            argv, results=[subprocess.CompletedProcess((), 0, b"", passed)]
        )
        self.assertEqual(0, code)  # Allowing a skip never requires one.
        for output in (
            summary,
            receipt + receipt + summary,
            receipt + summary.replace(b"skipped=1", b"skipped=2"),
            receipt.replace(b".Runtime.", b".RuntimeExtra.") + summary,
            b"Ran 1 test in 0.001s\n\nOK\n",
        ):
            with self.subTest(output=output), self.assertRaises(adapters.AdapterError):
                self.run_with_recorder(
                    argv, results=[subprocess.CompletedProcess((), 0, b"", output)]
                )
        code, _ = self.run_with_recorder(
            argv, results=[subprocess.CompletedProcess((), 3, b"", summary)]
        )
        self.assertEqual(3, code)

    def test_run_unittest_requires_modules_then_literal_verbose_flag(
        self,
    ) -> None:
        result, recorder = self.run_with_recorder(
            (
                "run-unittest",
                "tests.validation.test_one",
                "tests.validation.test_two.case",
                "-v",
            )
        )
        self.assertEqual(0, result)
        self.assertEqual(
            (
                "python3",
                "-m",
                "unittest",
                "tests.validation.test_one",
                "tests.validation.test_two.case",
                "-v",
            ),
            recorder.calls[0][0],
        )
        self._assert_run_child_bounds_stdout_and_stderr_before_returning()
        self._assert_run_child_normalizes_spawn_error_without_payload()

    def test_run_unittest_accepts_exact_test_surfaces(self) -> None:
        modules = (
            "tests.validation.test_one",
            "tests.lib.hooks.test_tool_payload",
            "tests.lib.document_governance.test_metadata_validator",
            "tests.lib.gate.test_ci_gate_adapters",
            "tests.lib.gate.test_ci_gate_contract",
            "tests.lib.gate.test_github_workflow_contract",
            "tests.lib.ops.test_postgres_logical_upgrade_rehearsal",
            "tests.lib.supply_chain.test_grype_db_seed",
        )
        for module in modules:
            with self.subTest(module=module):
                result, recorder = self.run_with_recorder(
                    ("run-unittest", module, "-v")
                )
                self.assertEqual(0, result)
                self.assertEqual(
                    ("python3", "-m", "unittest", module, "-v"),
                    recorder.calls[0][0],
                )

    def test_run_unittest_rejects_outside_empty_or_invalid_module_segments(
        self,
    ) -> None:
        for module in (
            "tests.other.test_escape",
            "tests.lib",
            "tests.lib..test_escape",
            "tests.lib.gate.test-ci_gate_adapters",
            "tests.lib.123bad",
            "tests.lib.gate.9module",
            "tests.validation.0case",
        ):
            with self.subTest(module=module):
                with self.assertRaises(adapters.AdapterError) as caught:
                    adapters.run_adapter(
                        self.root,
                        ("run-unittest", module, "-v"),
                        {"PATH": "/usr/bin"},
                    )
                self.assertEqual("ci-gate-adapter-arguments", caught.exception.code)

    def test_run_npm_accepts_only_three_closed_grammar_shapes(self) -> None:
        commands = (
            (
                "audit",
                "--audit-level=high",
                "--prefix",
                "projects/storybook/nextjs",
            ),
            ("ci", "--prefix", "projects/storybook/nextjs"),
            (
                "run",
                "build-storybook",
                "--prefix",
                "projects/storybook/nextjs",
            ),
        )
        for command in commands:
            with self.subTest(command=command):
                result, recorder = self.run_with_recorder(("run-npm", *command))
                self.assertEqual(0, result)
                self.assertEqual(("npm", *command), recorder.calls[0][0])

    def test_check_commit_range_delegates_to_commitizen_with_bounded_base(
        self,
    ) -> None:
        (self.root / ".cz.toml").write_bytes((ROOT / ".cz.toml").read_bytes())
        base = "1" * 40
        head = "2" * 40
        merge = "3" * 40
        common = "4" * 40
        result, recorder = self.run_with_recorder(
            ("check-commit-range",),
            environ={"PATH": "/usr/bin", "PR_BASE_SHA": base, "PR_HEAD_SHA": head},
            results=[
                subprocess.CompletedProcess(
                    (), 0, f"{merge} {base} {head}\n".encode(), b""
                ),
                subprocess.CompletedProcess((), 0, f"{common}\n".encode(), b""),
                subprocess.CompletedProcess((), 0, b"1\n", b""),
                subprocess.CompletedProcess((), 0, b"", b""),
            ],
        )
        self.assertEqual(0, result)
        self.assertEqual(
            [
                ("git", "rev-list", "--parents", "--max-count=1", "HEAD"),
                ("git", "merge-base", base, head),
                ("git", "rev-list", "--count", f"{base}..{head}"),
                (
                    "cz",
                    "check",
                    "--rev-range",
                    f"{base}..{head}",
                    "--message-length-limit",
                    "75",
                ),
            ],
            [call[0] for call in recorder.calls],
        )
        for key in ("PR_BASE_SHA", "PR_HEAD_SHA"):
            for invalid in ("", "0" * 40, "main", "a" * 39):
                environment = {
                    "PATH": "/usr/bin",
                    "PR_BASE_SHA": base,
                    "PR_HEAD_SHA": head,
                    key: invalid,
                }
                with (
                    self.subTest(key=key, revision=invalid),
                    self.assertRaises(adapters.AdapterError) as caught,
                ):
                    adapters.run_adapter(
                        self.root, ("check-commit-range",), environment
                    )
                self.assertEqual(
                    "ci-gate-adapter-pull-request-range", caught.exception.code
                )
        with self.assertRaises(adapters.AdapterError) as identical:
            adapters.run_adapter(
                self.root,
                ("check-commit-range",),
                {"PATH": "/usr/bin", "PR_BASE_SHA": base, "PR_HEAD_SHA": base},
            )
        self.assertEqual("ci-gate-adapter-pull-request-range", identical.exception.code)

    def test_synthetic_merge_checks_head_commits_and_committed_whitespace(
        self,
    ) -> None:
        (self.root / ".cz.toml").write_bytes((ROOT / ".cz.toml").read_bytes())
        base, head = self.synthetic_merge_with_whitespace()
        environment = {
            "PATH": os.defpath,
            "PR_BASE_SHA": base,
            "PR_HEAD_SHA": head,
        }
        self.assertNotEqual(
            0,
            adapters.run_adapter(self.root, ("check-diff-hygiene",), environment),
        )
        actual_child = adapters._run_child
        commitizen_calls: list[tuple[str, ...]] = []

        def execute(argv: tuple[str, ...], **kwargs: object):
            if argv[:2] == ("cz", "check"):
                commitizen_calls.append(argv)
                return subprocess.CompletedProcess(argv, 0, b"", b"")
            return actual_child(argv, **kwargs)  # type: ignore[arg-type]

        with mock.patch.object(adapters, "_run_child", side_effect=execute):
            self.assertEqual(
                0,
                adapters.run_adapter(self.root, ("check-commit-range",), environment),
            )
        self.assertEqual(1, len(commitizen_calls))
        self.assertEqual(f"{base}..{head}", commitizen_calls[0][3])

    def test_commit_contract_translations_cover_every_canonical_type(self) -> None:
        commitizen = tomllib.loads((ROOT / ".cz.toml").read_text(encoding="utf-8"))[
            "tool"
        ]["commitizen"]
        customize = commitizen["customize"]
        expected_types = {
            "build",
            "chore",
            "ci",
            "deps",
            "docs",
            "feat",
            "fix",
            "perf",
            "refactor",
            "release",
            "revert",
            "style",
            "test",
        }
        self.assertEqual(expected_types, set(customize["change_type_map"]))
        choices = next(
            question["choices"]
            for question in customize["questions"]
            if question["name"] == "change_type"
        )
        self.assertEqual(expected_types, {choice["value"] for choice in choices})
        bump_pattern = re.compile(customize["bump_pattern"])

        def increment_for(message: str) -> str | None:
            increments = (None, "PATCH", "MINOR", "MAJOR")
            increment = None
            for line in message.splitlines():
                matched = bump_pattern.search(line)
                if matched is None:
                    continue
                candidate = next(
                    (
                        value
                        for key, value in customize["bump_map"].items()
                        if re.match(key, matched.group(1))
                    ),
                    None,
                )
                if increments.index(candidate) > increments.index(increment):
                    increment = candidate
            return increment

        bump_cases = (
            ("feat: Add endpoint", "MINOR"),
            ("fix(api): Correct endpoint", "PATCH"),
            ("fix(api!): Correct endpoint", "PATCH"),
            ("feat(api!v2): Add endpoint", "MINOR"),
            ("perf: Improve endpoint", "PATCH"),
            ("refactor: Simplify endpoint", "PATCH"),
            ("feat!: Remove endpoint", "MAJOR"),
            ("fix(api)!: Remove endpoint", "MAJOR"),
            ("chore!: Remove compatibility", "MAJOR"),
            (
                "\n\n".join(
                    (
                        "feat: Replace endpoint",
                        "BREAKING CHANGE: Clients must use the replacement",
                    )
                ),
                "MAJOR",
            ),
            (
                "\n\n".join(
                    (
                        "feat: Replace endpoint",
                        "BREAKING-CHANGE: Clients must use the replacement",
                    )
                ),
                "MAJOR",
            ),
            ("docs: Update endpoint guide", None),
        )
        for message, expected in bump_cases:
            with self.subTest(message=message):
                self.assertEqual(expected, increment_for(message))
        for change_type in expected_types:
            for header in (
                f"{change_type}!: Remove compatibility",
                f"{change_type}(api)!: Remove compatibility",
                f"{change_type}(api!)!: Remove compatibility",
            ):
                with self.subTest(breaking_header=header):
                    self.assertEqual("MAJOR", increment_for(header))

        cliff_config = tomllib.loads((ROOT / "cliff.toml").read_text(encoding="utf-8"))
        cliff = cliff_config["git"]
        changelog = cliff_config["changelog"]
        self.assertTrue(cliff["protect_breaking_commits"])
        self.assertIn("commit.breaking", changelog["body"])

        def first_parser(message: str, footer: str = "") -> dict[str, object] | None:
            for parser in cliff["commit_parsers"]:
                if "footer" in parser and re.search(parser["footer"], footer):
                    return parser
                if "message" in parser and re.search(parser["message"], message):
                    return parser
            return None

        for change_type in sorted(expected_types - {"release"}):
            with self.subTest(change_type=change_type):
                parser = first_parser(f"{change_type}: Subject")
                self.assertIsNotNone(parser)
                self.assertFalse(parser.get("skip", False))
        for message in ("release: Publish v1.2.3", "chore(release): Publish v1.2.3"):
            with self.subTest(message=message):
                parser = first_parser(message)
                self.assertIsNotNone(parser)
                self.assertTrue(parser.get("skip", False))
        for footer in (
            "BREAKING CHANGE: The legacy endpoint was removed",
            "BREAKING-CHANGE: The legacy endpoint was removed",
        ):
            with self.subTest(footer=footer):
                breaking = first_parser("feat: Remove legacy endpoint", footer)
                self.assertEqual("Changed", breaking.get("group"))
        nonbreaking = first_parser(
            "feat: Keep legacy endpoint",
            "BREAKING-CHANGED: This is an ordinary custom footer",
        )
        self.assertEqual("Added", nonbreaking.get("group"))

        def hook_pattern(name: str) -> re.Pattern[str]:
            source = (ROOT / ".agents/governance/hooks" / name).read_text(
                encoding="utf-8"
            )
            encoded = re.search(r"^pattern: (\".*\")$", source, re.MULTILINE)
            self.assertIsNotNone(encoded)
            return re.compile(ast.literal_eval(encoded.group(1)))

        commit_warning = hook_pattern("hookify.warn-conventional-commit.md")
        branch_warning = hook_pattern("hookify.warn-branch-naming.md")
        for change_type in expected_types:
            with self.subTest(hook="commit", change_type=change_type):
                self.assertIsNone(
                    commit_warning.search(f'git commit -m "{change_type}: Subject"')
                )
            with self.subTest(hook="branch", change_type=change_type):
                self.assertIsNone(
                    branch_warning.search(f"git switch -c {change_type}/topic")
                )
        self.assertIsNotNone(commit_warning.search('git commit -m "unknown: Subject"'))
        self.assertIsNotNone(branch_warning.search("git switch -c unknown/topic"))

    def test_check_commit_range_fails_closed_for_invalid_commit_contract(self) -> None:
        config = self.root / ".cz.toml"
        target = self.root / "target.toml"
        cases = ("missing", "malformed", "symlink")
        for case in cases:
            with self.subTest(case=case):
                config.unlink(missing_ok=True)
                target.unlink(missing_ok=True)
                if case == "malformed":
                    config.write_text("not valid toml =", encoding="utf-8")
                elif case == "symlink":
                    target.write_bytes((ROOT / ".cz.toml").read_bytes())
                    config.symlink_to(target.name)
                with self.assertRaises(adapters.AdapterError) as caught:
                    adapters.run_adapter(
                        self.root,
                        ("check-commit-range",),
                        {
                            "PATH": "/usr/bin",
                            "PR_BASE_SHA": "0123456789abcdef0123456789abcdef01234567",
                        },
                    )
                self.assertEqual("ci-gate-adapter-git-flow", caught.exception.code)

    def test_authored_commit_examples_match_the_canonical_schema(self) -> None:
        config = tomllib.loads((ROOT / ".cz.toml").read_text(encoding="utf-8"))
        commitizen = config["tool"]["commitizen"]
        pattern = re.compile(commitizen["customize"]["schema_pattern"])
        limit = commitizen["message_length_limit"]
        messages = (
            "feat(api v2)!: Remove legacy endpoint",
            "fix: Correct typed gate\n\nExplain why the gate needed correction",
            "\n\n".join(
                (
                    "feat: Replace legacy endpoint",
                    "BREAKING CHANGE: Clients must use the typed endpoint",
                )
            ),
            "\n\n".join(
                (
                    "feat: Replace legacy endpoint",
                    "BREAKING-CHANGE: Clients must use the typed endpoint",
                )
            ),
            "\n\n".join(
                (
                    "fix: Correct typed gate",
                    "Explain why the gate needed correction",
                    "Refs: #135",
                )
            ),
        )
        for message in messages:
            with self.subTest(message=message):
                self.assertLessEqual(len(message.partition("\n")[0]), limit)
                self.assertIsNotNone(pattern.fullmatch(message))

        type_pattern = "|".join(commitizen["customize"]["change_type_map"])
        example_pattern = re.compile(
            rf"(?P<message>(?:{type_pattern})(?:\([^()\r\n]+\))?!?: [^\"`\r\n]+)"
        )
        paths = (
            ROOT / ".gitmessage",
            ROOT / ".agents/governance/git-workflow.md",
            ROOT / ".agents/prompts/commit-message.md",
            ROOT / ".agents/governance/hooks/hookify.warn-conventional-commit.md",
        )
        for path in paths:
            examples = tuple(
                match.group("message").strip()
                for match in example_pattern.finditer(path.read_text(encoding="utf-8"))
            )
            self.assertTrue(examples, path)
            for message in examples:
                with self.subTest(path=path, message=message):
                    self.assertLessEqual(len(message.splitlines()[0]), limit)
                    self.assertIsNotNone(pattern.fullmatch(message))

    def test_install_playwright_uses_the_fixed_child_vector(self) -> None:
        result, recorder = self.run_with_recorder(("install-playwright",))
        self.assertEqual(0, result)
        self.assertEqual(
            (
                "npx",
                "--prefix",
                "projects/storybook/nextjs",
                "playwright",
                "install",
                "chromium",
                "--with-deps",
            ),
            recorder.calls[0][0],
        )

    def test_run_zizmor_sarif_uses_nofollow_descriptor_and_rejects_symlink(
        self,
    ) -> None:
        recorder = ChildRecorder()

        def write_sarif(
            argv: tuple[str, ...],
            **kwargs: object,
        ) -> subprocess.CompletedProcess[bytes]:
            recorder.calls.append((argv, kwargs))
            descriptor = kwargs["stdout"]
            os.write(descriptor, b'{"runs":[]}\n')  # type: ignore[arg-type]
            return subprocess.CompletedProcess(argv, 0, b"", b"")

        with mock.patch.object(
            adapters,
            "_run_child",
            side_effect=write_sarif,
            create=True,
        ):
            self.assertEqual(
                0,
                adapters.run_adapter(
                    self.root,
                    ("run-zizmor-sarif",),
                    {"PATH": "/usr/bin"},
                ),
            )
        self.assertEqual(b'{"runs":[]}\n', (self.root / "results.sarif").read_bytes())
        self.assertEqual(
            (
                "uvx",
                "--from",
                "zizmor==1.28.0",
                "zizmor",
                ".",
                "--format",
                "sarif",
                ".",
            ),
            recorder.calls[0][0],
        )
        (self.root / "results.sarif").unlink()
        (self.root / "target").write_text("private", encoding="utf-8")
        (self.root / "results.sarif").symlink_to("target")
        with self.assertRaises(adapters.AdapterError) as caught:
            adapters.run_adapter(
                self.root,
                ("run-zizmor-sarif",),
                {"PATH": "/usr/bin"},
            )
        self.assertEqual(
            "ci-gate-adapter-sarif-output",
            caught.exception.code,
        )
        (self.root / "results.sarif").unlink()
        self._assert_sarif_partial_is_removed_after_exception_and_retry_succeeds()
        cleanup_events: list[tuple[str, int | str]] = []

        def fail_sarif_close(descriptor: int) -> None:
            cleanup_events.append(("close", descriptor))
            raise OSError(f"private descriptor {descriptor}")

        def fail_sarif_unlink(
            path: str,
            *,
            dir_fd: int,
        ) -> None:
            self.assertEqual(800, dir_fd)
            cleanup_events.append(("unlink", path))
            raise OSError("private SARIF path")

        with (
            mock.patch.object(
                adapters,
                "_owned_root_descriptor",
                return_value=800,
            ),
            mock.patch.object(adapters.os, "open", return_value=801),
            mock.patch.object(
                adapters,
                "_run_child",
                side_effect=adapters.AdapterError(
                    "ci-gate-adapter-child-exec",
                    "the child process is unavailable",
                ),
            ),
            mock.patch.object(adapters.os, "close", side_effect=fail_sarif_close),
            mock.patch.object(adapters.os, "unlink", side_effect=fail_sarif_unlink),
            self.assertRaises(adapters.AdapterError) as cleanup_error,
        ):
            adapters._run_zizmor_sarif(
                pathlib.Path("/proc/self/fd/800"),
                {"PATH": "/usr/bin"},
            )
        self.assertEqual(
            "ci-gate-adapter-sarif-cleanup",
            cleanup_error.exception.code,
        )
        self.assertNotIn("private", str(cleanup_error.exception))
        self.assertEqual(
            [("close", 801), ("unlink", "results.sarif")],
            cleanup_events,
        )
        cleanup_events = []

        def close_successful_sarif(descriptor: int) -> None:
            cleanup_events.append(("close", descriptor))
            raise OSError("private successful SARIF close")

        def unlink_successful_sarif(
            path: str,
            *,
            dir_fd: int,
        ) -> None:
            self.assertEqual(810, dir_fd)
            cleanup_events.append(("unlink", path))

        with (
            mock.patch.object(
                adapters,
                "_owned_root_descriptor",
                return_value=810,
            ),
            mock.patch.object(adapters.os, "open", return_value=811),
            mock.patch.object(
                adapters,
                "_run_child",
                return_value=subprocess.CompletedProcess(
                    ("uvx",),
                    0,
                    b"",
                    b"",
                ),
            ),
            mock.patch.object(
                adapters.os,
                "close",
                side_effect=close_successful_sarif,
            ),
            mock.patch.object(
                adapters.os,
                "unlink",
                side_effect=unlink_successful_sarif,
            ),
            self.assertRaises(adapters.AdapterError) as cleanup_error,
        ):
            adapters._run_zizmor_sarif(
                pathlib.Path("/proc/self/fd/810"),
                {"PATH": "/usr/bin"},
            )
        self.assertEqual(
            "ci-gate-adapter-sarif-cleanup",
            cleanup_error.exception.code,
        )
        self.assertEqual(
            [("close", 811), ("unlink", "results.sarif")],
            cleanup_events,
        )
        with (
            mock.patch.object(
                adapters,
                "_adopt_root",
                return_value=(pathlib.Path("/proc/self/fd/812"), 812),
            ),
            mock.patch.object(
                adapters,
                "_dispatch_adapter",
                side_effect=adapters.AdapterError(
                    "ci-gate-adapter-sarif-cleanup",
                    "the SARIF output could not be cleaned up",
                ),
            ),
            mock.patch.object(
                adapters.os,
                "close",
                side_effect=OSError("private root close payload"),
            ),
            self.assertRaises(adapters.AdapterError) as priority_error,
        ):
            adapters.run_adapter(
                self.root,
                ("run-zizmor-sarif",),
                {"PATH": "/usr/bin"},
            )
        self.assertEqual(
            "ci-gate-adapter-sarif-cleanup",
            priority_error.exception.code,
        )

    def test_rejects_unknown_metacharacter_paths_npm_verbs_and_secret_env(
        self,
    ) -> None:
        cases = (
            (("unknown",), {"PATH": "/usr/bin"}, "ci-gate-adapter-command"),
            (
                ("bash;curl",),
                {"PATH": "/usr/bin"},
                "ci-gate-adapter-command",
            ),
            (
                (
                    "run-npm",
                    "publish",
                    "--prefix",
                    "projects/storybook/nextjs",
                ),
                {"PATH": "/usr/bin"},
                "ci-gate-adapter-arguments",
            ),
            (
                ("check-diff-hygiene",),
                {"PATH": "/usr/bin", "GITHUB_TOKEN": "not-inspected"},
                "ci-gate-adapter-environment",
            ),
        )
        for argv, environ, expected_code in cases:
            with self.subTest(argv=argv):
                with self.assertRaises(adapters.AdapterError) as caught:
                    adapters.run_adapter(self.root, argv, environ)
                self.assertEqual(expected_code, caught.exception.code)

    def _assert_run_child_bounds_stdout_and_stderr_before_returning(self) -> None:
        for stream in ("stdout", "stderr"):
            with self.subTest(stream=stream):
                descriptor = "1" if stream == "stdout" else "2"
                marker = self.root / f"{stream}-overflow-child-survived"
                source = (
                    "import os,pathlib,time\n"
                    f"os.write({descriptor}, b'x' * "
                    f"({adapters._MAX_CAPTURE_BYTES + 1}))\n"
                    "time.sleep(2)\n"
                    f"pathlib.Path({str(marker)!r}).write_text('survived')\n"
                )
                with self.assertRaises(adapters.AdapterError) as caught:
                    adapters._run_child(
                        (sys.executable, "-c", source),
                        root=self.root,
                        environ={"PATH": "/usr/bin"},
                        capture_output=True,
                    )
                self.assertEqual(
                    "ci-gate-adapter-output",
                    caught.exception.code,
                )
                self.assertFalse(marker.exists())

    def _assert_descriptor_root_is_passed_to_adapter_children(self) -> None:
        root_fd = os.open(
            self.root,
            os.O_RDONLY | os.O_CLOEXEC | os.O_DIRECTORY,
        )
        adopted: list[int] = []

        def inspect_child(
            argv: tuple[str, ...],
            **kwargs: object,
        ) -> subprocess.CompletedProcess[bytes]:
            child_root = pathlib.Path(kwargs["root"])  # type: ignore[arg-type]
            match = adapters._PROC_FD_ROOT.fullmatch(child_root.as_posix())
            self.assertIsNotNone(match)
            adopted_fd = int(match.group(1))  # type: ignore[union-attr]
            adopted.append(adopted_fd)
            self.assertNotEqual(root_fd, adopted_fd)
            self.assertTrue(os.path.isdir(child_root))
            self.assertFalse(os.get_inheritable(adopted_fd))
            self.assertTrue(fcntl.fcntl(adopted_fd, fcntl.F_GETFD) & fcntl.FD_CLOEXEC)
            self.assertEqual((adopted_fd,), adapters._root_pass_fds(child_root))
            self.assertEqual(
                child_root.as_posix(),
                kwargs["environ"]["HYHOME_CI_GATE_ROOT"],  # type: ignore[index]
            )
            with self.assertRaises(OSError):
                os.fstat(root_fd)
            return subprocess.CompletedProcess(argv, 0, b"", b"")

        try:
            descriptor_root = pathlib.Path(f"/proc/self/fd/{root_fd}")
            with mock.patch.object(
                adapters,
                "_run_child",
                side_effect=inspect_child,
            ):
                result = adapters.run_adapter(
                    descriptor_root,
                    ("check-diff-hygiene",),
                    {
                        "PATH": "/usr/bin",
                        "HYHOME_CI_GATE_ROOT": descriptor_root.as_posix(),
                    },
                )
        finally:
            try:
                os.close(root_fd)
            except OSError:
                pass
        self.assertEqual(0, result)
        self.assertEqual(1, len(adopted))
        with self.assertRaises(OSError):
            os.fstat(adopted[0])

        error_root_fd = os.open(
            self.root,
            os.O_RDONLY | os.O_CLOEXEC | os.O_DIRECTORY,
        )
        failed_adopted: list[int] = []

        def fail_child(
            _argv: tuple[str, ...],
            **kwargs: object,
        ) -> subprocess.CompletedProcess[bytes]:
            match = adapters._PROC_FD_ROOT.fullmatch(
                pathlib.Path(kwargs["root"]).as_posix()  # type: ignore[arg-type]
            )
            self.assertIsNotNone(match)
            failed_adopted.append(int(match.group(1)))  # type: ignore[union-attr]
            raise adapters.AdapterError(
                "ci-gate-adapter-child-exec",
                "the child process is unavailable",
            )

        with (
            mock.patch.object(adapters, "_run_child", side_effect=fail_child),
            self.assertRaises(adapters.AdapterError),
        ):
            adapters.run_adapter(
                pathlib.Path(f"/proc/self/fd/{error_root_fd}"),
                ("check-diff-hygiene",),
                {
                    "PATH": "/usr/bin",
                    "HYHOME_CI_GATE_ROOT": f"/proc/self/fd/{error_root_fd}",
                },
            )
        with self.assertRaises(OSError):
            os.fstat(error_root_fd)
        with self.assertRaises(OSError):
            os.fstat(failed_adopted[0])

        real_fcntl = fcntl.fcntl
        real_close = os.close
        for inherited_error, owned_error in (
            (OSError("private inherited descriptor"), None),
            (KeyboardInterrupt("private inherited interrupt"), None),
            (
                SystemExit("private inherited exit"),
                OSError("private owned descriptor"),
            ),
            (
                GeneratorExit("private inherited generator"),
                KeyboardInterrupt("private owned interrupt"),
            ),
        ):
            with self.subTest(
                inherited_error=type(inherited_error).__name__,
                owned_error=(
                    None if owned_error is None else type(owned_error).__name__
                ),
            ):
                inherited_fd = os.open(
                    self.root,
                    os.O_RDONLY | os.O_CLOEXEC | os.O_DIRECTORY,
                )
                adopted_after_failure: list[int] = []
                close_order: list[int] = []

                def capture_duplicate(
                    descriptor: int,
                    command: int,
                    argument: int = 0,
                ) -> int:
                    duplicated = real_fcntl(descriptor, command, argument)
                    adopted_after_failure.append(duplicated)
                    return duplicated

                def fail_inherited_close(descriptor: int) -> None:
                    close_order.append(descriptor)
                    real_close(descriptor)
                    if descriptor == inherited_fd:
                        raise inherited_error
                    if owned_error is not None:
                        raise owned_error

                observed_root_cleanup: BaseException | None = None
                try:
                    with (
                        mock.patch.object(
                            adapters.fcntl,
                            "fcntl",
                            side_effect=capture_duplicate,
                        ),
                        mock.patch.object(
                            adapters.os,
                            "close",
                            side_effect=fail_inherited_close,
                        ),
                    ):
                        try:
                            adapters.run_adapter(
                                pathlib.Path(f"/proc/self/fd/{inherited_fd}"),
                                ("check-diff-hygiene",),
                                {"PATH": "/usr/bin"},
                            )
                        except BaseException as error:
                            observed_root_cleanup = error
                        else:
                            self.fail("adopted-root cleanup did not fail closed")
                finally:
                    for descriptor in (
                        inherited_fd,
                        *adopted_after_failure,
                    ):
                        try:
                            real_close(descriptor)
                        except OSError:
                            pass
                self.assertEqual(
                    "ci-gate-adapter-root-cleanup",
                    getattr(observed_root_cleanup, "code", None),
                )
                self.assertIsInstance(
                    observed_root_cleanup,
                    adapters.AdapterError,
                )
                self.assertNotIn("private", str(observed_root_cleanup))
                self.assertEqual(
                    [inherited_fd, adopted_after_failure[0]],
                    close_order,
                )
                self.assertEqual(
                    1,
                    close_order.count(adopted_after_failure[0]),
                )

        observed_cleanup_error: BaseException | None = None
        with (
            mock.patch.object(
                adapters,
                "_adopt_root",
                return_value=(pathlib.Path("/proc/self/fd/902"), 902),
            ),
            mock.patch.object(
                adapters,
                "_dispatch_adapter",
                side_effect=adapters.AdapterError(
                    "ci-gate-adapter-child-exec",
                    "the child process is unavailable",
                ),
            ),
            mock.patch.object(
                adapters.os,
                "close",
                side_effect=OSError("private owned descriptor"),
            ) as close,
            self.assertRaises(adapters.AdapterError) as root_cleanup,
        ):
            adapters.run_adapter(
                self.root,
                ("check-diff-hygiene",),
                {"PATH": "/usr/bin"},
            )
        self.assertEqual(
            "ci-gate-adapter-root-cleanup",
            root_cleanup.exception.code,
        )
        self.assertNotIn("private", str(root_cleanup.exception))
        close.assert_called_once_with(902)

        class ExplodingEnvironment(Mapping[str, str]):
            def __getitem__(self, key: str) -> str:
                raise KeyError(key)

            def __iter__(self):
                raise RuntimeError("private environment payload")

            def __len__(self) -> int:
                return 1

        with (
            mock.patch.object(
                adapters,
                "_adopt_root",
                return_value=(pathlib.Path("/proc/self/fd/903"), 903),
            ),
            mock.patch.object(adapters.os, "close") as close,
            self.assertRaises(adapters.AdapterError) as operation_error,
        ):
            adapters.run_adapter(
                self.root,
                ("check-diff-hygiene",),
                ExplodingEnvironment(),
            )
        self.assertEqual(
            "ci-gate-adapter-operation",
            operation_error.exception.code,
        )
        self.assertNotIn("private", str(operation_error.exception))
        close.assert_called_once_with(903)

        typed_error = adapters.AdapterError(
            "ci-gate-adapter-command",
            "the adapter subcommand is not admitted",
        )
        for dispatch_error, expected_code in (
            (typed_error, "ci-gate-adapter-command"),
            (
                RuntimeError("private dispatch payload"),
                "ci-gate-adapter-operation",
            ),
            (OSError("private dispatch payload"), "ci-gate-adapter-operation"),
        ):
            with (
                self.subTest(dispatch_error=type(dispatch_error).__name__),
                mock.patch.object(
                    adapters,
                    "_adopt_root",
                    return_value=(pathlib.Path("/proc/self/fd/904"), 904),
                ),
                mock.patch.object(
                    adapters,
                    "_dispatch_adapter",
                    side_effect=dispatch_error,
                ),
                mock.patch.object(adapters.os, "close") as close,
                self.assertRaises(adapters.AdapterError) as caught,
            ):
                adapters.run_adapter(
                    self.root,
                    ("check-diff-hygiene",),
                    {"PATH": "/usr/bin"},
                )
            self.assertEqual(expected_code, caught.exception.code)
            self.assertNotIn("private", str(caught.exception))
            if dispatch_error is typed_error:
                self.assertIs(typed_error, caught.exception)
            close.assert_called_once_with(904)

        for interruption in (
            KeyboardInterrupt("private dispatch interrupt"),
            SystemExit("private dispatch exit"),
            GeneratorExit("private dispatch generator"),
        ):
            with (
                self.subTest(interruption=type(interruption).__name__),
                mock.patch.object(
                    adapters,
                    "_adopt_root",
                    return_value=(pathlib.Path("/proc/self/fd/905"), 905),
                ),
                mock.patch.object(
                    adapters,
                    "_dispatch_adapter",
                    side_effect=interruption,
                ),
                mock.patch.object(adapters.os, "close") as close,
            ):
                try:
                    adapters.run_adapter(
                        self.root,
                        ("check-diff-hygiene",),
                        {"PATH": "/usr/bin"},
                    )
                except BaseException as caught:
                    self.assertIs(interruption, caught)
                else:
                    self.fail("control-flow interruption was not re-raised")
            close.assert_called_once_with(905)

        with (
            mock.patch.object(
                adapters,
                "_adopt_root",
                return_value=(pathlib.Path("/proc/self/fd/906"), 906),
            ),
            mock.patch.object(
                adapters,
                "_dispatch_adapter",
                side_effect=KeyboardInterrupt("private product interrupt"),
            ),
            mock.patch.object(
                adapters.os,
                "close",
                side_effect=SystemExit("private cleanup interrupt"),
            ) as close,
        ):
            try:
                adapters.run_adapter(
                    self.root,
                    ("check-diff-hygiene",),
                    {"PATH": "/usr/bin"},
                )
            except BaseException as error:
                observed_cleanup_error = error
            else:
                self.fail("interrupted root cleanup did not fail closed")
        self.assertEqual(
            "ci-gate-adapter-root-cleanup",
            getattr(observed_cleanup_error, "code", None),
        )
        self.assertIsInstance(observed_cleanup_error, adapters.AdapterError)
        self.assertNotIn("private", str(observed_cleanup_error))
        close.assert_called_once_with(906)

        inventory_root, inventory_fd = adapters._adopt_root(self.root)
        inventory_source = (
            "import os\n"
            "visible=[]\n"
            "for name in os.listdir('/proc/self/fd'):\n"
            "    number=int(name)\n"
            "    if number <= 2: continue\n"
            "    try: target=os.readlink('/proc/self/fd/'+name)\n"
            "    except OSError: continue\n"
            "    visible.append((number,target))\n"
            "print(os.getsid(0), os.getpgrp(), repr(visible))\n"
        )
        try:
            inventory = adapters._run_child(
                (sys.executable, "-c", inventory_source),
                root=inventory_root,
                environ={
                    "PATH": "/usr/bin",
                    "HYHOME_CI_GATE_ROOT": inventory_root.as_posix(),
                },
                capture_output=True,
            )
        finally:
            os.close(inventory_fd)
        session, group, visible = inventory.stdout.decode("ascii").split(
            " ",
            2,
        )
        self.assertEqual(os.getsid(0), int(session))
        self.assertEqual(os.getpgrp(), int(group))
        self.assertEqual(
            [(inventory_fd, str(self.root))],
            ast.literal_eval(visible),
        )

    def _assert_run_child_normalizes_spawn_error_without_payload(self) -> None:
        with (
            mock.patch.object(
                adapters.subprocess,
                "Popen",
                side_effect=OSError("private executable path"),
            ),
            self.assertRaises(adapters.AdapterError) as caught,
        ):
            adapters._run_child(
                ("missing-program",),
                root=self.root,
                environ={"PATH": "/usr/bin"},
                capture_output=True,
            )
        self.assertEqual("ci-gate-adapter-child-exec", caught.exception.code)
        self.assertNotIn("private executable path", str(caught.exception))

    def _assert_sarif_partial_is_removed_after_exception_and_retry_succeeds(
        self,
    ) -> None:
        attempts = 0

        def fail_then_write(
            argv: tuple[str, ...],
            **kwargs: object,
        ) -> subprocess.CompletedProcess[bytes]:
            nonlocal attempts
            attempts += 1
            descriptor = kwargs["stdout"]
            os.write(descriptor, b'{"partial":true}')  # type: ignore[arg-type]
            if attempts == 1:
                raise adapters.AdapterError(
                    "ci-gate-adapter-child-exec",
                    "the child process is unavailable",
                )
            return subprocess.CompletedProcess(argv, 0, b"", b"")

        with mock.patch.object(
            adapters,
            "_run_child",
            side_effect=fail_then_write,
        ):
            with self.assertRaises(adapters.AdapterError):
                adapters.run_adapter(
                    self.root,
                    ("run-zizmor-sarif",),
                    {"PATH": "/usr/bin"},
                )
            self.assertFalse((self.root / "results.sarif").exists())
            self.assertEqual(
                0,
                adapters.run_adapter(
                    self.root,
                    ("run-zizmor-sarif",),
                    {"PATH": "/usr/bin"},
                ),
            )
        self.assertEqual(
            b'{"partial":true}',
            (self.root / "results.sarif").read_bytes(),
        )


class ApprovedNpmAuditTests(unittest.TestCase):
    chain = (
        "eslint-config-next@16.4.0",
        "@next/eslint-plugin-next@16.4.0",
        "fast-glob@3.3.1",
        "micromatch@4.0.8",
        "braces@3.0.3",
    )

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temporary.name)
        self.policy = dict(
            id="GHSA-vfj7-8cjw-p6xm",
            owner="@buenhyden",
            approved_at="2026-10-01T00:00:00Z",
            expires_at="2026-10-10T15:00:00Z",
            project="projects/storybook/nextjs",
            dependency_chain=self.chain,
            advisory_url="https://api.github.com/advisories/GHSA-vfj7-8cjw-p6xm",
        )
        packages = {}
        self.nodes = {}
        for index, item in enumerate(self.chain):
            name, version = item.rsplit("@", 1)
            via = (
                [self.chain[index + 1].rsplit("@", 1)[0]]
                if index < 4
                else [
                    dict(
                        url="https://github.com/advisories/GHSA-vfj7-8cjw-p6xm",
                        name="braces",
                        dependency="braces",
                        severity="high",
                        range="<=3.0.3",
                    )
                ]
            )
            path = "node_modules/" + name
            packages[path] = dict(
                version=version,
                dev=True,
                dependencies={self.chain[index + 1].rsplit("@", 1)[0]: "*"}
                if index < 4
                else {},
            )
            self.nodes[name] = dict(
                name=name,
                severity="high",
                via=via,
                nodes=[path],
                range="*",
                effects=[],
                fixAvailable=False,
            )
        target = self.root / self.policy["project"]
        target.mkdir(parents=True)
        self.lock = dict(lockfileVersion=3, packages=packages)
        (target / "package-lock.json").write_text(json.dumps(self.lock))
        self.advisory = dict(
            ghsa_id=self.policy["id"],
            cve_id="CVE-2026-93687",
            withdrawn_at=None,
            vulnerabilities=[
                dict(
                    package=dict(ecosystem="npm", name="braces"),
                    vulnerable_version_range="<= 3.0.3",
                    first_patched_version=None,
                )
            ],
        )

    def tearDown(self):
        self.temporary.cleanup()

    def audit(self, nodes=None, returncode=1):
        return subprocess.CompletedProcess(
            [],
            returncode,
            json.dumps(
                dict(
                    auditReportVersion=2,
                    vulnerabilities=self.nodes if nodes is None else nodes,
                    metadata=dict(
                        vulnerabilities=dict(
                            info=0,
                            low=0,
                            moderate=0,
                            high=5 if nodes is None else len(nodes),
                            critical=0,
                            total=5 if nodes is None else len(nodes),
                        )
                    ),
                )
            ).encode(),
            b"",
        )

    def run_audit(self, full=None, production=None):
        recorder = ChildRecorder(
            [full or self.audit(), production or self.audit({}, 0)]
        )
        with (
            mock.patch.object(adapters, "_run_child", side_effect=recorder),
            mock.patch.object(
                adapters,
                "_load_audit_acceptance",
                return_value=self.policy,
                create=True,
            ),
            mock.patch.object(
                adapters,
                "_fetch_audit_advisory",
                return_value=self.advisory,
                create=True,
            ),
            mock.patch.object(
                adapters,
                "_audit_now",
                return_value=datetime(2026, 10, 4, tzinfo=UTC),
                create=True,
            ),
            mock.patch.object(sys, "stdout", io.StringIO()) as output,
        ):
            result = adapters.run_adapter(
                self.root, ("run-approved-npm-audit",), {"PATH": "/usr/bin"}
            )
        return result, recorder, output.getvalue()

    def test_exact_dev_chain_is_accepted_with_raw_failure_visible(self):
        result, recorder, output = self.run_audit()
        self.assertEqual(0, result)
        self.assertEqual(2, len(recorder.calls))
        self.assertIn("--omit=dev", recorder.calls[1][0])
        self.assertIn("raw npm audit: FAIL", output)
        self.assertIn("ACCEPTED_RISK", output)

    def test_production_finding_rejects(self):
        with self.assertRaises(adapters.AdapterError):
            self.run_audit(production=self.audit())

    def test_unknown_advisory_and_dependency_reject(self):
        for mutation in ("url", "dependency"):
            nodes = json.loads(json.dumps(self.nodes))
            if mutation == "url":
                nodes["braces"]["via"][0]["url"] = (
                    "https://github.com/advisories/GHSA-unknown"
                )
            else:
                nodes["other"] = nodes.pop("braces")
            with (
                self.subTest(mutation=mutation),
                self.assertRaises(adapters.AdapterError),
            ):
                self.run_audit(full=self.audit(nodes))

    def test_malformed_and_tool_exit_reject(self):
        for code, payload in (
            (1, b"{}"),
            (2, b"{}"),
            (1, b"not-json"),
            (0, b'{"auditReportVersion":2,"vulnerabilities":{},"vulnerabilities":{}}'),
        ):
            with (
                self.subTest(code=code, payload=payload),
                self.assertRaises(adapters.AdapterError),
            ):
                self.run_audit(full=subprocess.CompletedProcess([], code, payload, b""))

    def test_lock_version_or_dev_scope_drift_reject(self):
        target = self.root / self.policy["project"] / "package-lock.json"
        for field, value in (("version", "3.0.4"), ("dev", False)):
            lock = json.loads(json.dumps(self.lock))
            lock["packages"]["node_modules/braces"][field] = value
            target.write_text(json.dumps(lock))
            with self.subTest(field=field), self.assertRaises(adapters.AdapterError):
                self.run_audit()

    def test_expired_and_patch_available_reject(self):
        self.policy["expires_at"] = "2026-10-04T00:00:00Z"
        with self.assertRaises(adapters.AdapterError):
            self.run_audit()
        self.policy["expires_at"] = "2026-10-10T15:00:00Z"
        self.policy["approved_at"] = "2026-10-05T00:00:00Z"
        with self.assertRaises(adapters.AdapterError):
            self.run_audit()
        self.policy["approved_at"] = "2026-10-01T00:00:00Z"
        self.advisory["vulnerabilities"][0]["first_patched_version"] = "3.0.4"
        with self.assertRaises(adapters.AdapterError):
            self.run_audit()

    def test_advisory_unknown_range_or_withdrawal_reject(self):
        for field, value in (("withdrawn_at", "2026-10-04"), ("ghsa_id", "GHSA-other")):
            saved = self.advisory[field]
            self.advisory[field] = value
            with self.subTest(field=field), self.assertRaises(adapters.AdapterError):
                self.run_audit()
            self.advisory[field] = saved
        self.advisory["vulnerabilities"][0]["vulnerable_version_range"] = "*"
        with self.assertRaises(adapters.AdapterError):
            self.run_audit()

    def test_advisory_transport_failure_is_closed(self):
        with (
            mock.patch.object(
                adapters, "_load_audit_acceptance", return_value=self.policy
            ),
            mock.patch.object(
                adapters, "_audit_now", return_value=datetime(2026, 10, 4, tzinfo=UTC)
            ),
            mock.patch.object(adapters.urllib.request, "build_opener") as opener,
        ):
            opener.return_value.open.side_effect = OSError("synthetic network failure")
            with self.assertRaises(adapters.AdapterError):
                adapters.run_adapter(
                    self.root, ("run-approved-npm-audit",), {"PATH": "/usr/bin"}
                )

    def test_closed_new_grammar_and_context(self):
        adapters.validate_adapter_argv(("run-approved-npm-audit",))
        with self.assertRaises(adapters.AdapterError):
            adapters.validate_adapter_argv(("run-approved-npm-audit", "--ignore"))
        self.assertNotIn("local", adapters.ADAPTER_CONTEXTS["run-approved-npm-audit"])

    def test_audit_metadata_mismatch_and_zero_audit(self):
        broken = self.audit()
        doc = json.loads(broken.stdout)
        doc["metadata"]["vulnerabilities"]["high"] = 4
        broken.stdout = json.dumps(doc).encode()
        with self.assertRaises(adapters.AdapterError):
            self.run_audit(full=broken)
        self.assertEqual(0, self.run_audit(full=self.audit({}, 0))[0])

    def test_missing_patch_status_and_cycle_reject(self):
        saved = self.advisory["vulnerabilities"][0].pop("first_patched_version")
        with self.assertRaises(adapters.AdapterError):
            self.run_audit()
        self.advisory["vulnerabilities"][0]["first_patched_version"] = saved
        nodes = json.loads(json.dumps(self.nodes))
        nodes["micromatch"]["via"] = ["fast-glob"]
        with self.assertRaises(adapters.AdapterError):
            self.run_audit(full=self.audit(nodes))

    def test_known_next_downgrade_is_not_a_braces_patch(self):
        for node in self.nodes.values():
            node["fixAvailable"] = {
                "name": "eslint-config-next",
                "version": "14.2.35",
                "isSemVerMajor": True,
            }
        self.assertEqual(0, self.run_audit()[0])
        self.nodes["braces"]["fixAvailable"]["version"] = "14.2.36"
        with self.assertRaises(adapters.AdapterError):
            self.run_audit()

    def test_unknown_stderr_and_malformed_fix_types_reject(self):
        full = self.audit()
        full.stderr = b"synthetic unknown diagnostic"
        with self.assertRaises(adapters.AdapterError):
            self.run_audit(full=full)
        for value in (
            0,
            None,
            True,
            {"name": "eslint-config-next", "version": "14.2.35", "isSemVerMajor": 1},
        ):
            self.nodes["braces"]["fixAvailable"] = value
            with self.subTest(value=value), self.assertRaises(adapters.AdapterError):
                self.run_audit()

    def test_missing_withdrawal_and_nonfinite_json_reject(self):
        self.advisory.pop("withdrawn_at")
        with self.assertRaises(adapters.AdapterError):
            self.run_audit()
        for payload in (b'{"unexpected":NaN}', b'{"unexpected":Infinity}'):
            with (
                self.subTest(payload=payload),
                self.assertRaises(adapters.AdapterError),
            ):
                adapters._audit_json(payload)


if __name__ == "__main__":
    unittest.main()
