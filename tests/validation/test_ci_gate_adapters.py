from __future__ import annotations

import io
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from scripts.validation import ci_gate_adapters as adapters


REAL_SUBPROCESS_RUN = subprocess.run
EXPECTED_SUBCOMMANDS = (
    "verify-metadata-base",
    "publish-qa-recommendations",
    "check-diff-hygiene",
    "check-shell-syntax",
    "install-python-requirements",
    "run-unittest",
    "run-agent-output-eval",
    "run-npm",
    "check-git-flow",
    "prepare-compose-env",
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

    def test_publish_qa_recommendations_writes_one_bounded_summary(self) -> None:
        summary = self.root / "summary.md"
        summary.touch()
        result, recorder = self.run_with_recorder(
            ("publish-qa-recommendations",),
            environ={
                "PATH": "/usr/bin",
                "EVENT_NAME": "workflow_dispatch",
                "GITHUB_STEP_SUMMARY": str(summary),
            },
            results=[
                subprocess.CompletedProcess(("git",), 1, b"", b""),
                subprocess.CompletedProcess(
                    ("bash",),
                    0,
                    b"recommended=repo-contracts\n",
                    b"",
                ),
            ],
        )
        self.assertEqual(0, result)
        self.assertIn("## QA gate recommendations", summary.read_text())
        self.assertIn("recommended=repo-contracts", summary.read_text())
        self.assertEqual(
            (
                "bash",
                "scripts/validation/recommend-qa-gates.sh",
                "--files",
                ".github/workflows/ci-quality.yml",
            ),
            recorder.calls[-1][0],
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
                    b"scripts/a.sh\0.claude/hooks/b.sh\0",
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
                "scripts/**/*.sh",
                ".claude/hooks/*.sh",
            ),
            recorder.calls[0][0],
        )
        self.assertEqual(
            ("bash", "-n", "scripts/a.sh", ".claude/hooks/b.sh"),
            recorder.calls[1][0],
        )

    def test_install_python_requirements_has_two_exact_admitted_paths(
        self,
    ) -> None:
        for requirement in (
            "scripts/requirements.txt",
            "scripts/requirements-pre-commit.txt",
        ):
            with self.subTest(requirement=requirement):
                result, recorder = self.run_with_recorder(
                    ("install-python-requirements", requirement)
                )
                self.assertEqual(0, result)
                self.assertEqual(
                    ("python3", "-m", "pip", "install", "-r", requirement),
                    recorder.calls[0][0],
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
        self._assert_eval_invalid_utf8_is_normalized()

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
                "scripts/validation/run-agent-output-eval-fixtures.sh",
                "--check-fixtures",
                "--check-regressions",
            ),
            recorder.calls[0][0],
        )

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
                result, recorder = self.run_with_recorder(
                    ("run-npm", *command)
                )
                self.assertEqual(0, result)
                self.assertEqual(("npm", *command), recorder.calls[0][0])

    def test_check_git_flow_validates_without_shell_or_child_process(
        self,
    ) -> None:
        result, recorder = self.run_with_recorder(
            ("check-git-flow",),
            environ={
                "PATH": "/usr/bin",
                "PR_TITLE": "feat(ci): add typed gates",
                "HEAD_REF": "feat/135-typed-gates",
            },
        )
        self.assertEqual(0, result)
        self.assertEqual([], recorder.calls)
        with self.assertRaises(adapters.AdapterError) as caught:
            adapters.run_adapter(
                self.root,
                ("check-git-flow",),
                {
                    "PATH": "/usr/bin",
                    "PR_TITLE": "not conventional",
                    "HEAD_REF": "unknown",
                },
            )
        self.assertEqual("ci-gate-adapter-git-flow", caught.exception.code)

    def test_prepare_compose_env_is_exclusive_tracked_and_preserves_existing(
        self,
    ) -> None:
        REAL_SUBPROCESS_RUN(["git", "init", "-q"], cwd=self.root, check=True)
        source = self.root / ".env.example"
        source.write_bytes(b"SAFE_EXAMPLE=1\n")
        REAL_SUBPROCESS_RUN(
            ["git", "add", "--", ".env.example"],
            cwd=self.root,
            check=True,
        )
        self.assertEqual(
            0,
            adapters.run_adapter(
                self.root,
                ("prepare-compose-env",),
                {"PATH": "/usr/bin", "CI": "true"},
            ),
        )
        destination = self.root / ".env"
        self.assertEqual(source.read_bytes(), destination.read_bytes())
        destination.write_bytes(b"EXISTING_PRIVATE_BYTES\n")
        with self.assertRaises(adapters.AdapterError) as caught:
            adapters.run_adapter(
                self.root,
                ("prepare-compose-env",),
                {"PATH": "/usr/bin", "CI": "true"},
            )
        self.assertEqual(
            "ci-gate-adapter-compose-env-exists",
            caught.exception.code,
        )
        self.assertEqual(b"EXISTING_PRIVATE_BYTES\n", destination.read_bytes())
        self._assert_prepare_compose_env_rejects_non_blob_identical_sources()
        self._assert_prepare_compose_env_rejects_path_replacement_after_open()
        self._assert_compose_copy_normalizes_zero_short_write_and_cleans_partial()

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
                ("install-python-requirements", "../requirements.txt"),
                {"PATH": "/usr/bin"},
                "ci-gate-adapter-arguments",
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
        marker = self.root / "descriptor-root-marker"
        marker.write_text("bound", encoding="utf-8")
        root_fd = os.open(
            self.root,
            os.O_RDONLY | os.O_CLOEXEC | os.O_DIRECTORY,
        )
        try:
            descriptor_root = pathlib.Path(f"/proc/self/fd/{root_fd}")
            source = (
                "import os,pathlib\n"
                "root=pathlib.Path(os.environ['HYHOME_CI_GATE_ROOT'])\n"
                "raise SystemExit(0 if "
                "(root/'descriptor-root-marker').read_text()=='bound' "
                "and pathlib.Path.cwd()==root.resolve() else 9)\n"
            )
            result = adapters._run_child(
                (sys.executable, "-c", source),
                root=descriptor_root,
                environ={
                    "PATH": "/usr/bin",
                    "HYHOME_CI_GATE_ROOT": descriptor_root.as_posix(),
                },
                capture_output=True,
            )
        finally:
            os.close(root_fd)
        self.assertEqual(0, result.returncode)

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

    def _assert_eval_invalid_utf8_is_normalized(self) -> None:
        with mock.patch.object(
            adapters,
            "_run_child",
            return_value=subprocess.CompletedProcess(
                ("bash",),
                0,
                b"fixtures_check=pass\nregressions_check=pass\n\xff",
                b"",
            ),
        ):
            with self.assertRaises(adapters.AdapterError) as caught:
                adapters.run_adapter(
                    self.root,
                    ("run-agent-output-eval",),
                    {"PATH": "/usr/bin"},
                )
        self.assertEqual(
            "ci-gate-adapter-eval-output",
            caught.exception.code,
        )

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

    def _assert_prepare_compose_env_rejects_non_blob_identical_sources(
        self,
    ) -> None:
        for case in ("modified", "untracked", "symlink", "nonregular"):
            with self.subTest(case=case):
                case_root = self.root / case
                case_root.mkdir()
                REAL_SUBPROCESS_RUN(
                    ["git", "init", "-q"],
                    cwd=case_root,
                    check=True,
                )
                source = case_root / ".env.example"
                if case == "untracked":
                    source.write_bytes(b"UNTRACKED=1\n")
                elif case == "symlink":
                    target = case_root / "target"
                    target.write_bytes(b"TARGET=1\n")
                    source.symlink_to("target")
                elif case == "nonregular":
                    source.mkdir()
                else:
                    source.write_bytes(b"STAGED=1\n")
                    REAL_SUBPROCESS_RUN(
                        ["git", "add", "--", ".env.example"],
                        cwd=case_root,
                        check=True,
                    )
                    source.write_bytes(b"MODIFIED=1\n")
                with self.assertRaises(adapters.AdapterError) as caught:
                    adapters.run_adapter(
                        case_root,
                        ("prepare-compose-env",),
                        {"PATH": "/usr/bin", "CI": "true"},
                    )
                self.assertEqual(
                    "ci-gate-adapter-compose-source",
                    caught.exception.code,
                )
                self.assertFalse((case_root / ".env").exists())

    def _assert_prepare_compose_env_rejects_path_replacement_after_open(
        self,
    ) -> None:
        case_root = self.root / "replaced"
        case_root.mkdir()
        REAL_SUBPROCESS_RUN(["git", "init", "-q"], cwd=case_root, check=True)
        source = case_root / ".env.example"
        source.write_bytes(b"STAGED=1\n")
        REAL_SUBPROCESS_RUN(
            ["git", "add", "--", ".env.example"],
            cwd=case_root,
            check=True,
        )
        real_provenance = adapters._tracked_regular_source

        def replace_after_provenance(*args: object, **kwargs: object):
            result = real_provenance(*args, **kwargs)
            source.rename(case_root / ".env.original")
            source.write_bytes(b"REPLACED=1\n")
            return result

        with (
            mock.patch.object(
                adapters,
                "_tracked_regular_source",
                side_effect=replace_after_provenance,
            ),
            self.assertRaises(adapters.AdapterError) as caught,
        ):
            adapters.run_adapter(
                case_root,
                ("prepare-compose-env",),
                {"PATH": "/usr/bin", "CI": "true"},
            )
        self.assertEqual(
            "ci-gate-adapter-compose-source",
            caught.exception.code,
        )
        self.assertFalse((case_root / ".env").exists())

    def _assert_compose_copy_normalizes_zero_short_write_and_cleans_partial(
        self,
    ) -> None:
        case_root = self.root / "short-write"
        case_root.mkdir()
        REAL_SUBPROCESS_RUN(["git", "init", "-q"], cwd=case_root, check=True)
        source = case_root / ".env.example"
        source.write_bytes(b"STAGED=1\n")
        REAL_SUBPROCESS_RUN(
            ["git", "add", "--", ".env.example"],
            cwd=case_root,
            check=True,
        )
        real_write = os.write
        zero_writes = 0

        def zero_destination_write(
            descriptor: int,
            payload: bytes | memoryview,
        ) -> int:
            nonlocal zero_writes
            target = pathlib.Path(f"/proc/self/fd/{descriptor}")
            if target.resolve() == case_root / ".env":
                zero_writes += 1
                if zero_writes == 1:
                    return 0
                raise OSError("private short-write payload")
            return real_write(descriptor, payload)

        with (
            mock.patch.object(
                adapters.os,
                "write",
                side_effect=zero_destination_write,
            ),
            self.assertRaises(adapters.AdapterError) as caught,
        ):
            adapters.run_adapter(
                case_root,
                ("prepare-compose-env",),
                {"PATH": "/usr/bin", "CI": "true"},
            )
        self.assertEqual(
            "ci-gate-adapter-compose-output",
            caught.exception.code,
        )
        self.assertFalse((case_root / ".env").exists())


if __name__ == "__main__":
    unittest.main()
