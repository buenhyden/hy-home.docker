from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
POST_TOOL = ROOT / "scripts/hooks/post-tool-validate.sh"
EVENT_HOOK = ROOT / "scripts/hooks/agent-event-hook.sh"


class AgentGovernanceCiRoutingTests(unittest.TestCase):
    @staticmethod
    def _write_executable(path: pathlib.Path, text: str) -> None:
        path.write_text(text, encoding="utf-8")
        path.chmod(0o755)

    def _hook_repo(self, directory: str) -> pathlib.Path:
        repo = pathlib.Path(directory)
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(
            ["git", "config", "user.email", "t@example.com"], cwd=repo, check=True
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"], cwd=repo, check=True
        )
        gate = repo / "scripts/validation/run-ci-gate.py"
        gate.parent.mkdir(parents=True)
        gate.write_text(
            "import pathlib, sys\n"
            "path = pathlib.Path('.gate-calls')\n"
            "before = path.read_text() if path.exists() else ''\n"
            "path.write_text(before + ' '.join(sys.argv[1:]) + '\\n')\n"
            "raise SystemExit(int(pathlib.Path('.gate-exit').read_text()) "
            "if pathlib.Path('.gate-exit').exists() else 0)\n",
            encoding="utf-8",
        )
        tracked = repo / "tracked.txt"
        tracked.write_text("before\n", encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-qm", "seed"], cwd=repo, check=True)
        return repo

    @staticmethod
    def _stop_environment(
        repo: pathlib.Path, provider: str, *, path: str | None = None
    ) -> dict[str, str]:
        environment = dict(os.environ)
        environment.pop("CODEX_PROJECT_DIR", None)
        environment.pop("CLAUDE_PROJECT_DIR", None)
        environment.pop("HY_HOME_HOOK_PROVIDER", None)
        environment.pop("AGENT_ALLOW_UNCOMMITTED_STOP", None)
        environment["PATH"] = path or environment["PATH"]
        if provider == "codex":
            environment["CODEX_PROJECT_DIR"] = str(repo)
            environment["HY_HOME_HOOK_PROVIDER"] = "codex"
        else:
            environment["CLAUDE_PROJECT_DIR"] = str(repo)
        return environment

    def _run_stop(
        self,
        repo: pathlib.Path,
        provider: str = "claude",
        *,
        payload: dict[str, object] | None = None,
        allow_uncommitted: bool = True,
        path: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        environment = self._stop_environment(repo, provider, path=path)
        if allow_uncommitted:
            environment["AGENT_ALLOW_UNCOMMITTED_STOP"] = "1"
        return subprocess.run(
            ["bash", str(EVENT_HOOK), "Stop"],
            cwd=repo,
            input=json.dumps(payload or {}),
            capture_output=True,
            text=True,
            env=environment,
            check=False,
        )

    def test_github_routing_uses_canonical_stage00_roots(self) -> None:
        paths = (
            ROOT / ".github/CODEOWNERS",
            ROOT / ".github/PULL_REQUEST_TEMPLATE.md",
            ROOT / ".github/labeler.yml",
        )
        text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        self.assertIn("docs/00.agent-governance/policies/", text)
        self.assertNotIn("docs/00.agent-governance/rules/", text)
        self.assertNotIn("." + "ge" + "mini", text.lower())

    def test_manifest_registers_provider_check_and_renderer(self) -> None:
        manifest = yaml.safe_load((ROOT / "scripts/manifest.yaml").read_text())
        serialized = str(manifest)
        self.assertIn("check-agent-governance-contract.py", serialized)
        self.assertIn("provider_surface_renderer.py", serialized)

    def test_repository_contract_does_not_require_removed_handoff(self) -> None:
        self.assertFalse((ROOT / "scripts/validation/check-repo-contracts.sh").exists())
        manifest = (ROOT / "scripts/manifest.yaml").read_text(encoding="utf-8")
        self.assertNotIn("check-repo-" + "contracts.sh", manifest)

    def test_post_tool_yaml_registry_uses_governance_parser_not_json_tool(self) -> None:
        text = (ROOT / "scripts/hooks/post-tool-validate.sh").read_text()
        self.assertNotIn(
            "python3 -m json.tool docs/00.agent-governance/providers/registry.yaml",
            text,
        )
        self.assertNotIn("run-ci-gate.py --profile changed", text)
        self.assertNotIn("check-agent-governance-contract.py", text)

    def test_stop_runs_changed_profile_once_for_every_git_visible_state(self) -> None:
        mutations = {
            "modified": lambda repo: (repo / "tracked.txt").write_text(
                "after\n", encoding="utf-8"
            ),
            "staged": lambda repo: (
                (repo / "tracked.txt").write_text("after\n", encoding="utf-8"),
                subprocess.run(["git", "add", "tracked.txt"], cwd=repo, check=True),
            ),
            "untracked": lambda repo: (repo / "new.txt").write_text(
                "new\n", encoding="utf-8"
            ),
            "deleted": lambda repo: (repo / "tracked.txt").unlink(),
        }
        for provider in ("claude", "codex"):
            for name, mutate in mutations.items():
                with (
                    self.subTest(provider=provider, state=name),
                    tempfile.TemporaryDirectory() as directory,
                ):
                    repo = self._hook_repo(directory)
                    mutate(repo)
                    result = self._run_stop(repo, provider)
                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertEqual(
                        ["--profile changed"],
                        (repo / ".gate-calls")
                        .read_text(encoding="utf-8")
                        .splitlines(),
                    )

    def test_stop_clean_tree_skips_changed_profile(self) -> None:
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider), tempfile.TemporaryDirectory() as name:
                repo = self._hook_repo(name)
                result = self._run_stop(repo, provider)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertFalse((repo / ".gate-calls").exists())

    def test_stop_retry_never_reruns_changed_profile_or_completes(self) -> None:
        for provider in ("claude", "codex"):
            for state_changed in (False, True):
                with (
                    self.subTest(provider=provider, state_changed=state_changed),
                    tempfile.TemporaryDirectory() as name,
                ):
                    repo = self._hook_repo(name)
                    (repo / "tracked.txt").write_text("after\n", encoding="utf-8")
                    (repo / ".gate-exit").write_text("9", encoding="utf-8")
                    first = self._run_stop(repo, provider)
                    self.assertEqual(0, first.returncode, first.stderr)
                    self.assertNotIn("Session ending", first.stdout)
                    self.assertEqual(
                        1, len((repo / ".gate-calls").read_text().splitlines())
                    )

                    if state_changed:
                        (repo / "tracked.txt").write_text(
                            "changed again\n", encoding="utf-8"
                        )
                    retry = self._run_stop(
                        repo, provider, payload={"stop_hook_active": True}
                    )
                    self.assertEqual(0, retry.returncode, retry.stderr)
                    self.assertNotIn("Session ending", retry.stdout)
                    self.assertIn("manual", retry.stdout.lower())
                    response = json.loads(retry.stdout.splitlines()[-1])
                    self.assertIs(response["continue"], False)
                    self.assertIn("stopReason", response)
                    self.assertEqual(
                        1, len((repo / ".gate-calls").read_text().splitlines())
                    )

    def test_logical_commit_blocked_retry_skips_changed_profile(self) -> None:
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider), tempfile.TemporaryDirectory() as name:
                repo = self._hook_repo(name)
                (repo / "tracked.txt").write_text("after\n", encoding="utf-8")
                first = self._run_stop(repo, provider, allow_uncommitted=False)
                self.assertEqual(0, first.returncode, first.stderr)
                self.assertIn("Uncommitted paths", first.stdout)
                self.assertEqual(1, len((repo / ".gate-calls").read_text().splitlines()))
                retry = self._run_stop(
                    repo,
                    provider,
                    payload={"stop_hook_active": True},
                    allow_uncommitted=False,
                )
                self.assertEqual(0, retry.returncode, retry.stderr)
                self.assertIn("manual", retry.stdout.lower())
                self.assertEqual(1, len((repo / ".gate-calls").read_text().splitlines()))

    def test_stop_git_status_failure_blocks_without_session_end(self) -> None:
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider), tempfile.TemporaryDirectory() as name:
                repo = self._hook_repo(name)
                fake_bin = repo / "fake-bin"
                fake_bin.mkdir()
                self._write_executable(
                    fake_bin / "git",
                    "#!/bin/sh\n"
                    "if [ \"$1\" = status ]; then exit 42; fi\n"
                    "exec /usr/bin/git \"$@\"\n",
                )
                result = self._run_stop(
                    repo,
                    provider,
                    path=f"{fake_bin}:/usr/bin:/bin",
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertNotIn("Session ending", result.stdout)
                self.assertIn("git status", result.stdout.lower())
                self.assertFalse((repo / ".gate-calls").exists())

    def test_stop_long_path_diagnostics_are_byte_bounded(self) -> None:
        cases = {
            "ascii": "/".join(["x" * 200] * 18),
            "multibyte": "/".join(["가" * 60] * 18),
        }
        for provider in ("claude", "codex"):
            for name, segments in cases.items():
                with (
                    self.subTest(provider=provider, path_kind=name),
                    tempfile.TemporaryDirectory() as directory,
                ):
                    repo = self._hook_repo(directory)
                    porcelain = "\n".join(
                        f"?? {segments}/file-{index:03d}.txt" for index in range(80)
                    )
                    self.assertGreater(len(porcelain.encode("utf-8")), 131072)
                    (repo / ".fake-status").write_text(
                        porcelain + "\n", encoding="utf-8"
                    )
                    fake_bin = repo / "fake-bin"
                    fake_bin.mkdir()
                    self._write_executable(
                        fake_bin / "git",
                        "#!/bin/sh\n"
                        "if [ \"$1\" = status ]; then exec /bin/cat .fake-status; fi\n"
                        "exec /usr/bin/git \"$@\"\n",
                    )
                    result = self._run_stop(
                        repo,
                        provider,
                        allow_uncommitted=False,
                        path=f"{fake_bin}:/usr/bin:/bin",
                    )
                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertNotIn("Session ending", result.stdout)
                    response = json.loads(result.stdout.splitlines()[-1])
                    self.assertEqual("block", response["decision"])
                    reason = response["reason"]
                    self.assertIn("Uncommitted paths", reason)
                    self.assertIn("[additional changed-path bytes omitted]", reason)
                    displayed_paths = reason.split("Uncommitted paths:\n", 1)[1]
                    self.assertLessEqual(len(displayed_paths.encode("utf-8")), 6000)
                    self.assertLess(len(reason.encode("utf-8")), 8000)
                    self.assertEqual(
                        1, len((repo / ".gate-calls").read_text().splitlines())
                    )

    def test_stop_malformed_git_status_blocks_as_parser_failure(self) -> None:
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider), tempfile.TemporaryDirectory() as name:
                repo = self._hook_repo(name)
                fake_bin = repo / "fake-bin"
                fake_bin.mkdir()
                self._write_executable(
                    fake_bin / "git",
                    "#!/bin/sh\n"
                    "if [ \"$1\" = status ]; then printf '%s\\n' malformed; exit 0; fi\n"
                    "exec /usr/bin/git \"$@\"\n",
                )
                result = self._run_stop(
                    repo,
                    provider,
                    allow_uncommitted=False,
                    path=f"{fake_bin}:/usr/bin:/bin",
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertNotIn("Session ending", result.stdout)
                self.assertIn("could not be parsed", result.stdout.lower())
                self.assertIn("manual", result.stdout.lower())
                self.assertEqual(
                    1, len((repo / ".gate-calls").read_text().splitlines())
                )

    def test_stop_timeout_blocks_and_reserves_diagnostic_budget(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            repo = self._hook_repo(name)
            (repo / "tracked.txt").write_text("after\n", encoding="utf-8")
            fake_bin = repo / "fake-bin"
            fake_bin.mkdir()
            self._write_executable(
                fake_bin / "timeout",
                "#!/bin/sh\nprintf '%s\\n' \"$@\" > .timeout-arguments\nexit 124\n",
            )
            result = self._run_stop(
                repo, path=f"{fake_bin}:/usr/bin:/bin"
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertNotIn("Session ending", result.stdout)
            self.assertIn("timed out", result.stdout.lower())
            self.assertIn("manual", result.stdout.lower())
            self.assertEqual(
                [
                    "--kill-after=5s",
                    "540s",
                    "python3",
                    "scripts/validation/run-ci-gate.py",
                    "--profile",
                    "changed",
                ],
                (repo / ".timeout-arguments").read_text().splitlines(),
            )
            self.assertFalse((repo / ".gate-calls").exists())

    def test_active_workflows_route_provider_validation(self) -> None:
        workflow_text = (ROOT / ".github/workflows/ci-quality.yml").read_text(
            encoding="utf-8"
        )
        self.assertEqual(1, workflow_text.count("run-ci-gate.py --profile changed"))
        self.assertEqual(1, workflow_text.count("run-ci-gate.py --profile full"))
        self.assertNotIn("--gate", workflow_text)

    def test_post_tool_rejects_unsafe_paths_before_any_write(self) -> None:
        cases = (
            "absolute",
            "traversal",
            "noncanonical",
            "symlink",
            "control",
            "hardlink",
        )
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                base = pathlib.Path(directory)
                root = base / "repo"
                root.mkdir()
                inside = root / "inside.md"
                outside = base / "outside.md"
                inside.write_text("inside trailing space   \n", encoding="utf-8")
                outside.write_text("outside trailing space   \n", encoding="utf-8")
                if case == "absolute":
                    supplied = str(inside)
                    observed = inside
                elif case == "traversal":
                    supplied = "../outside.md"
                    observed = outside
                elif case == "noncanonical":
                    supplied = "./inside.md"
                    observed = inside
                elif case == "symlink":
                    link = root / "linked.md"
                    link.symlink_to(outside)
                    supplied = "linked.md"
                    observed = outside
                elif case == "control":
                    supplied = "inside.md\n../outside.md"
                    observed = outside
                else:
                    os.link(outside, root / "hardlinked.md")
                    supplied = "hardlinked.md"
                    observed = outside
                before = observed.read_bytes()
                result = subprocess.run(
                    ["bash", str(POST_TOOL)],
                    cwd=ROOT,
                    input=json.dumps({"tool_input": {"file_path": supplied}}),
                    capture_output=True,
                    text=True,
                    env={
                        "PATH": "/usr/bin:/bin",
                        "CODEX_PROJECT_DIR": str(root),
                    },
                    check=False,
                )
                self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertEqual(before, observed.read_bytes())

    def test_post_tool_check_mode_is_non_mutating_and_runs_bounded_checks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            shell = repo / "scripts/example.sh"
            shell.parent.mkdir(parents=True)
            shell.write_text("#!/bin/sh\necho ok\n", encoding="utf-8")
            subprocess.run(["git", "add", "scripts/example.sh"], cwd=repo, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Test",
                    "-c",
                    "user.email=t@example.com",
                    "commit",
                    "-qm",
                    "seed",
                ],
                cwd=repo,
                check=True,
            )
            shell.write_text("#!/bin/sh\necho ok   \n", encoding="utf-8")
            before = shell.read_bytes()
            result = subprocess.run(
                ["bash", str(POST_TOOL), "--check"],
                cwd=repo,
                input=json.dumps({"tool_input": {"file_path": "scripts/example.sh"}}),
                capture_output=True,
                text=True,
                env={
                    "PATH": "/usr/bin:/bin",
                    "CODEX_PROJECT_DIR": str(repo),
                },
                check=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertEqual(before, shell.read_bytes())

    def test_post_tool_propagates_available_linter_failures(self) -> None:
        for suffix, tool in (("sh", "shellcheck"), ("yaml", "yamllint")):
            with (
                self.subTest(tool=tool),
                tempfile.TemporaryDirectory() as directory,
            ):
                repo = pathlib.Path(directory)
                subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
                relative = pathlib.Path("scripts/example." + suffix)
                target = repo / relative
                target.parent.mkdir(parents=True)
                target.write_text(
                    "#!/bin/sh\necho ok\n" if suffix == "sh" else "key: value\n",
                    encoding="utf-8",
                )
                subprocess.run(["git", "add", str(relative)], cwd=repo, check=True)
                fake_bin = repo / "fake-bin"
                fake_bin.mkdir()
                self._write_executable(fake_bin / tool, "#!/bin/sh\nexit 37\n")
                result = subprocess.run(
                    ["bash", str(POST_TOOL), "--check"],
                    cwd=repo,
                    input=json.dumps(
                        {"tool_input": {"file_path": relative.as_posix()}}
                    ),
                    capture_output=True,
                    text=True,
                    env={
                        "PATH": f"{fake_bin}:/usr/bin:/bin",
                        "CODEX_PROJECT_DIR": str(repo),
                    },
                    check=False,
                )
                self.assertEqual(37, result.returncode, result.stdout + result.stderr)

    def test_post_tool_checks_shell_files_outside_scripts(self) -> None:
        for relative in ("infra/example.sh", "tests/example.sh", "example.sh"):
            for check in ("shfmt", "shellcheck", "syntax"):
                with (
                    self.subTest(path=relative, check=check),
                    tempfile.TemporaryDirectory() as directory,
                ):
                    repo = pathlib.Path(directory)
                    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
                    target = repo / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(
                        "#!/bin/sh\nif then\n" if check == "syntax"
                        else "#!/bin/sh\necho ok\n",
                        encoding="utf-8",
                    )
                    before = target.read_bytes()
                    fake_bin = repo / "fake-bin"
                    fake_bin.mkdir()
                    for tool in ("shfmt", "shellcheck"):
                        self._write_executable(
                            fake_bin / tool,
                            "#!/bin/sh\nexit " + ("37" if tool == check else "0") + "\n",
                        )
                    result = subprocess.run(
                        ["bash", str(POST_TOOL), "--check"],
                        cwd=repo,
                        input=json.dumps({"tool_input": {"file_path": relative}}),
                        capture_output=True,
                        text=True,
                        env={
                            "PATH": f"{fake_bin}:/usr/bin:/bin",
                            "CODEX_PROJECT_DIR": str(repo),
                        },
                        check=False,
                    )
                    if check == "syntax":
                        self.assertNotEqual(0, result.returncode)
                        self.assertIn(relative, result.stderr)
                    else:
                        self.assertEqual(37, result.returncode, result.stderr)
                    self.assertEqual(before, target.read_bytes())

    def test_post_tool_checks_each_changed_shell_file_for_syntax(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            scripts = repo / "scripts"
            scripts.mkdir()
            (scripts / "first.sh").write_text(
                "#!/bin/sh\necho valid\n", encoding="utf-8"
            )
            (scripts / "second.sh").write_text(
                "#!/bin/sh\nif then\n", encoding="utf-8"
            )
            result = subprocess.run(
                ["bash", str(POST_TOOL), "--check"],
                cwd=repo,
                input=json.dumps(
                    {
                        "tool_input": {
                            "files": ["scripts/first.sh", "scripts/second.sh"]
                        }
                    }
                ),
                capture_output=True,
                text=True,
                env={
                    "PATH": "/usr/bin:/bin",
                    "CODEX_PROJECT_DIR": str(repo),
                },
                check=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("second.sh", result.stderr)


if __name__ == "__main__":
    unittest.main()
