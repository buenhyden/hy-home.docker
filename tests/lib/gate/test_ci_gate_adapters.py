from __future__ import annotations

import ast
import fcntl
import io
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import tomllib
import unittest
from collections.abc import Mapping
from unittest import mock

from scripts.lib.gate import ci_gate_adapters as adapters

ROOT = pathlib.Path(__file__).resolve().parents[3]
REAL_SUBPROCESS_RUN = subprocess.run
EXPECTED_SUBCOMMANDS = (
    "verify-metadata-base",
    "check-diff-hygiene",
    "check-shell-syntax",
    "run-unittest",
    "run-agent-output-eval",
    "run-npm",
    "check-git-flow",
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
        return subprocess.CompletedProcess(argv, 0, b"", b"")


class CiGateAdapterTests(unittest.TestCase):
    def test_retired_setup_commands_are_rejected_by_the_argv_contract(self) -> None:
        for argv in (
            ("install-python-requirements", "scripts/requirements.txt"),
            ("prepare-compose-env",),
        ):
            with self.subTest(argv=argv):
                with self.assertRaises(adapters.AdapterError) as caught:
                    adapters.validate_adapter_argv(argv)
                self.assertEqual("ci-gate-adapter-command", caught.exception.code)

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
        with mock.patch.object(
            adapters,
            "_run_child",
            side_effect=recorder,
            create=True,
        ):
            result = adapters.run_adapter(
                self.root,
                argv,
                environ or {"PATH": "/usr/bin"},
            )
        return result, recorder

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

    def test_check_shell_syntax_uses_nul_tracked_paths_and_one_bash_call(
        self,
    ) -> None:
        result, recorder = self.run_with_recorder(
            ("check-shell-syntax",),
            results=[
                subprocess.CompletedProcess(
                    ("git",),
                    0,
                    b"evals/a.sh\0scripts/b.sh\0.claude/hooks/c.sh\0",
                    b"",
                ),
                subprocess.CompletedProcess(("bash",), 0, b"", b""),
            ],
        )
        self.assertEqual(0, result)
        self.assertEqual(
            (
                "git",
                "ls-files",
                "-z",
                "--",
                "evals/**/*.sh",
                "scripts/**/*.sh",
                ".claude/hooks/*.sh",
            ),
            recorder.calls[0][0],
        )
        self.assertEqual(
            ("bash", "-n", "evals/a.sh", "scripts/b.sh", ".claude/hooks/c.sh"),
            recorder.calls[1][0],
        )

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
            "tests.lib.agent_governance.test_agent_governance_contract",
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

    def test_run_agent_output_eval_checks_markers_and_emits_output_once(
        self,
    ) -> None:
        recorder = ChildRecorder(
            [
                subprocess.CompletedProcess(
                    ("bash",),
                    0,
                    b"fixtures_check=pass\nregressions_check=pass\n",
                    b"",
                )
            ]
        )
        with (
            mock.patch.object(
                adapters,
                "_run_child",
                side_effect=recorder,
                create=True,
            ),
            mock.patch("sys.stdout", new_callable=io.StringIO) as stdout,
        ):
            result = adapters.run_adapter(
                self.root,
                ("run-agent-output-eval",),
                {"PATH": "/usr/bin"},
            )
        self.assertEqual(0, result)
        self.assertEqual(
            1,
            stdout.getvalue().count("fixtures_check=pass"),
        )
        self.assertEqual(
            1,
            stdout.getvalue().count("regressions_check=pass"),
        )
        self.assertEqual(
            (
                "bash",
                "evals/run-agent-output-eval-fixtures.sh",
                "--check-fixtures",
                "--check-regressions",
            ),
            recorder.calls[0][0],
        )

    def test_run_agent_output_eval_propagates_child_and_rejects_bad_output(
        self,
    ) -> None:
        invalid_outputs = (
            ("missing-fixtures", b"regressions_check=pass\n"),
            ("missing-regressions", b"fixtures_check=pass\n"),
            (
                "nul",
                b"fixtures_check=pass\nregressions_check=pass\n\0",
            ),
            (
                "oversize",
                b"fixtures_check=pass\nregressions_check=pass\n"
                + b"x" * (adapters._MAX_CAPTURE_BYTES + 1),
            ),
            (
                "invalid-utf8",
                b"fixtures_check=pass\nregressions_check=pass\n\xff",
            ),
        )
        expected_argv = (
            "bash",
            "evals/run-agent-output-eval-fixtures.sh",
            "--check-fixtures",
            "--check-regressions",
        )
        nonzero = ChildRecorder(
            [subprocess.CompletedProcess(("bash",), 23, b"", b"failure")]
        )
        with (
            mock.patch.object(adapters, "_run_child", side_effect=nonzero),
            mock.patch("sys.stdout", new_callable=io.StringIO) as stdout,
        ):
            self.assertEqual(
                23,
                adapters.run_adapter(
                    self.root,
                    ("run-agent-output-eval",),
                    {"PATH": "/usr/bin"},
                ),
            )
        self.assertEqual("", stdout.getvalue())
        self.assertEqual(expected_argv, nonzero.calls[0][0])

        for label, output in invalid_outputs:
            recorder = ChildRecorder(
                [subprocess.CompletedProcess(("bash",), 0, output, b"")]
            )
            with (
                self.subTest(case=label),
                mock.patch.object(adapters, "_run_child", side_effect=recorder),
                mock.patch("sys.stdout", new_callable=io.StringIO) as stdout,
                self.assertRaises(adapters.AdapterError) as caught,
            ):
                adapters.run_adapter(
                    self.root,
                    ("run-agent-output-eval",),
                    {"PATH": "/usr/bin"},
                )
            self.assertEqual(
                "ci-gate-adapter-eval-output",
                caught.exception.code,
            )
            self.assertEqual("", stdout.getvalue())
            self.assertEqual(expected_argv, recorder.calls[0][0])

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

    def test_check_git_flow_validates_without_shell_or_child_process(
        self,
    ) -> None:
        (self.root / ".cz.toml").write_bytes((ROOT / ".cz.toml").read_bytes())
        accepted = (
            ("feat(api v2)!: Remove legacy endpoint", "feat/135-typed-gates"),
            ("fix: Correct typed gate", "fix/135-typed-gates"),
            ("fix!: Patch production gate", "hotfix/135-patch-gate"),
            ("docs: Update guide", "docs/update-guide"),
            ("style: Format sources", "style/format-sources"),
            ("refactor: Simplify parser", "refactor/simplify-parser"),
            ("perf: Reduce parsing cost", "perf/reduce-cost"),
            ("test: Cover commit grammar", "test/commit-grammar"),
            ("build: Update build image", "build/update-image"),
            ("ci: Align workflow checks", "ci/align-checks"),
            ("chore: Maintain repository", "chore/maintenance"),
            ("revert: Restore prior behavior", "revert/restore-behavior"),
            ("release: Publish v1.2.3", "release/publish-v1.2.3"),
            ("deps: Update dependency pins", "deps/update-pins"),
            ("feat: Add automation", "codex/commit-contract"),
            ("deps: Update dependency pins", "dependabot/pip/requests-3"),
        )
        for title, branch in accepted:
            with self.subTest(title=title, branch=branch):
                result, recorder = self.run_with_recorder(
                    ("check-git-flow",),
                    environ={
                        "PATH": "/usr/bin",
                        "PR_TITLE": title,
                        "HEAD_REF": branch,
                    },
                )
                self.assertEqual(0, result)
                self.assertEqual([], recorder.calls)

        rejected = (
            ("feat: lower case subject", "feat/135-typed-gates"),
            ("feat: Subject ends with period.", "feat/135-typed-gates"),
            (f"feat: {'A' * 70}", "feat/135-typed-gates"),
            ("unknown: Add typed gate", "feat/135-typed-gates"),
            ("feat: Add typed gate", "feat/missingissue"),
            ("feat: Add typed gate", "unknown/topic"),
        )
        for title, branch in rejected:
            with self.subTest(title=title, branch=branch):
                with self.assertRaises(adapters.AdapterError) as caught:
                    adapters.run_adapter(
                        self.root,
                        ("check-git-flow",),
                        {"PATH": "/usr/bin", "PR_TITLE": title, "HEAD_REF": branch},
                    )
                self.assertEqual("ci-gate-adapter-git-flow", caught.exception.code)

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
                self.assertEqual("Breaking Changes", breaking.get("group"))
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

    def test_check_git_flow_fails_closed_for_invalid_commit_contract(self) -> None:
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
                        ("check-git-flow",),
                        {
                            "PATH": "/usr/bin",
                            "PR_TITLE": "feat: Add typed gate",
                            "HEAD_REF": "feat/135-typed-gates",
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


if __name__ == "__main__":
    unittest.main()
