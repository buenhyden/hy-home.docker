from __future__ import annotations

import json
import os
import pathlib
import re
import shutil
import shlex
import subprocess
import sys
import tempfile
import time
import unittest

import yaml

from scripts.lib.gate import ci_gate_contract as contract

ROOT = pathlib.Path(__file__).resolve().parents[2]
POST_TOOL = ROOT / "scripts/hooks/post-tool-validate.sh"
EVENT_HOOK = ROOT / "scripts/hooks/agent-event-hook.sh"
QA_CI_TOOLS = ROOT / "scripts/operations/use-qa-ci-tools.sh"
INFRA_STATIC = ROOT / ".agents/skills/infra-validate/scripts/static-checks.sh"


class AgentGovernanceCiRoutingTests(unittest.TestCase):
    def test_hadolint_docker_image_matches_hook_revision(self) -> None:
        document = yaml.safe_load(
            (ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
        )
        repositories = [
            repository
            for repository in document["repos"]
            if repository["repo"] == "https://github.com/hadolint/hadolint"
        ]
        self.assertEqual(1, len(repositories))
        repository = repositories[0]
        hooks = [
            hook for hook in repository["hooks"] if hook["id"] == "hadolint-docker"
        ]
        self.assertEqual(1, len(hooks))

        expected = "ghcr.io/hadolint/hadolint:{} hadolint".format(repository["rev"])
        self.assertEqual(expected, hooks[0].get("entry"))

    def test_public_hooks_admit_every_tracked_path_and_root_tool_owner(self) -> None:
        document = yaml.safe_load(
            (ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
        )
        hooks = {
            hook["id"]: hook
            for repository in document["repos"]
            if repository["repo"] == "local"
            for hook in repository["hooks"]
            if hook["id"] in {"public-validation-changed", "public-validation-full"}
        }
        self.assertEqual(
            {"public-validation-changed", "public-validation-full"}, set(hooks)
        )
        tracked = (
            subprocess.run(
                ["git", "ls-files", "-z"],
                cwd=ROOT,
                capture_output=True,
                check=True,
            )
            .stdout.decode("utf-8")
            .split("\0")
        )
        for hook_id, hook in hooks.items():
            selector = re.compile(hook["files"])
            omitted = [
                path for path in tracked if path and not selector.fullmatch(path)
            ]
            with self.subTest(hook=hook_id):
                self.assertEqual([], omitted)
                self.assertTrue(hook.get("always_run"))

        root_tool_paths = {
            ".cz.toml",
            ".editorconfig",
            ".gitattributes",
            ".gitignore",
            ".gitleaks.toml",
            ".gitmessage",
            ".gitmodules",
            ".graphifyignore",
            ".hadolint.yaml",
            ".markdownlint-cli2.yaml",
            ".prettierignore",
            ".rtk/",
            ".shellcheckrc",
            ".yamllint",
            "cliff.toml",
            "ruff.toml",
        }
        public = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        matching_rules = {
            prefix: rule.suites
            for rule in public.changed_rules
            for prefix in rule.prefixes
            if prefix in root_tool_paths
        }
        self.assertEqual(root_tool_paths, set(matching_rules))
        self.assertEqual({("repository-integrity",)}, set(matching_rules.values()))

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
        subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
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

    def test_github_routing_includes_hidden_canonical_home(self) -> None:
        paths = (
            ROOT / ".github/CODEOWNERS",
            ROOT / ".github/PULL_REQUEST_TEMPLATE.md",
            ROOT / ".github/labeler.yml",
        )
        text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        self.assertIn(".agents/", text)
        self.assertNotIn("docs/00.agent-governance/", text)
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
            "python3 -m json.tool .agents/governance/providers/registry.yaml",
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
                        (repo / ".gate-calls").read_text(encoding="utf-8").splitlines(),
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
                self.assertEqual(
                    1, len((repo / ".gate-calls").read_text().splitlines())
                )
                retry = self._run_stop(
                    repo,
                    provider,
                    payload={"stop_hook_active": True},
                    allow_uncommitted=False,
                )
                self.assertEqual(0, retry.returncode, retry.stderr)
                self.assertIn("manual", retry.stdout.lower())
                self.assertEqual(
                    1, len((repo / ".gate-calls").read_text().splitlines())
                )

    def test_stop_git_status_failure_blocks_without_session_end(self) -> None:
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider), tempfile.TemporaryDirectory() as name:
                repo = self._hook_repo(name)
                fake_bin = repo / "fake-bin"
                fake_bin.mkdir()
                self._write_executable(
                    fake_bin / "git",
                    "#!/bin/sh\n"
                    'if [ "$1" = status ]; then exit 42; fi\n'
                    'exec /usr/bin/git "$@"\n',
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
                        'if [ "$1" = status ]; then exec /bin/cat .fake-status; fi\n'
                        'exec /usr/bin/git "$@"\n',
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
                    'exec /usr/bin/git "$@"\n',
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
            result = self._run_stop(repo, path=f"{fake_bin}:/usr/bin:/bin")
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
                    supplied = str(outside)
                    observed = outside
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
                    ["bash", str(POST_TOOL), "--write"],
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

    def test_post_tool_default_and_check_mode_are_non_mutating(self) -> None:
        for flags in ([], ["--check"]):
            with self.subTest(flags=flags):
                self._assert_post_tool_is_non_mutating(flags)

    def test_agent_event_hook_requests_post_tool_writes_explicitly(self) -> None:
        text = (ROOT / "scripts/hooks/agent-event-hook.sh").read_text()
        self.assertIn("bash scripts/hooks/post-tool-validate.sh --write", text)

    def _assert_post_tool_is_non_mutating(self, flags: list[str]) -> None:
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
                ["bash", str(POST_TOOL), *flags],
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

    def test_post_tool_preserves_the_prepared_python_search_order(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = pathlib.Path(directory)
            repo = base / "repo"
            repo.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            helper = repo / "scripts" / "operations" / "use-qa-ci-tools.sh"
            helper.parent.mkdir(parents=True)
            helper_called = base / "helper-called"
            helper.write_text(
                QA_CI_TOOLS.read_text(encoding="utf-8")
                + f"\n: > {shlex.quote(str(helper_called))}\n",
                encoding="utf-8",
            )
            target = repo / "example.json"
            target.write_text("{}\n", encoding="utf-8")
            before = target.read_bytes()

            trace = base / "python-trace"
            prepared_bin = base / "prepared" / "bin"
            user_bin = base / "home" / ".local" / "bin"
            prepared_bin.mkdir(parents=True)
            user_bin.mkdir(parents=True)
            real_python = shlex.quote(str(pathlib.Path(sys.executable).resolve()))
            self._write_executable(
                prepared_bin / "python3",
                "#!/bin/sh\nprintf 'prepared\\n' >> \"$TOOL_TRACE\"\n"
                f'exec {real_python} "$@"\n',
            )
            self._write_executable(
                user_bin / "python3",
                "#!/bin/sh\nprintf 'user-global\\n' >> \"$TOOL_TRACE\"\n"
                f'exec {real_python} "$@"\n',
            )

            result = subprocess.run(
                ["bash", str(POST_TOOL), "--check"],
                cwd=repo,
                input=json.dumps({"tool_input": {"file_path": "example.json"}}),
                capture_output=True,
                text=True,
                env={
                    "PATH": f"{prepared_bin}:/usr/bin:/bin",
                    "HOME": str(base / "home"),
                    "TOOL_TRACE": str(trace),
                    "CODEX_PROJECT_DIR": str(repo),
                },
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(before, target.read_bytes())
            self.assertFalse(helper_called.exists())
            selections = trace.read_text(encoding="utf-8").splitlines()
            self.assertTrue(selections)
            self.assertEqual({"prepared"}, set(selections))

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
            for check in ("shellcheck", "syntax"):
                with (
                    self.subTest(path=relative, check=check),
                    tempfile.TemporaryDirectory() as directory,
                ):
                    repo = pathlib.Path(directory)
                    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
                    target = repo / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(
                        "#!/bin/sh\nif then\n"
                        if check == "syntax"
                        else "#!/bin/sh\necho ok\n",
                        encoding="utf-8",
                    )
                    before = target.read_bytes()
                    fake_bin = repo / "fake-bin"
                    fake_bin.mkdir()
                    # shfmt stays on PATH and always fails: the hook must not
                    # reach for an unregistered formatter, so only the tool
                    # named by `check` can decide this subcase.
                    self._write_executable(fake_bin / "shfmt", "#!/bin/sh\nexit 37\n")
                    self._write_executable(
                        fake_bin / "shellcheck",
                        "#!/bin/sh\nexit "
                        + ("37" if check == "shellcheck" else "0")
                        + "\n",
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
        """`bash -n` names the offending file, whatever the host has installed.

        The syntax case has to reach `bash -n` to prove anything, and ShellCheck
        rejects the same file first as a parse error on stdout. Whether that
        happens depended on the host: a runner with /usr/bin/shellcheck failed
        this case while a workstation whose shellcheck sits outside the
        restricted PATH passed it. The lint step is stubbed out so the reporter
        is always the one under test.
        """

        with tempfile.TemporaryDirectory() as directory:
            repo = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            scripts = repo / "scripts"
            scripts.mkdir()
            (scripts / "first.sh").write_text(
                "#!/bin/sh\necho valid\n", encoding="utf-8"
            )
            (scripts / "second.sh").write_text("#!/bin/sh\nif then\n", encoding="utf-8")
            fake_bin = repo / "fake-bin"
            fake_bin.mkdir()
            self._write_executable(fake_bin / "shellcheck", "#!/bin/sh\nexit 0\n")
            result = subprocess.run(
                ["bash", str(POST_TOOL), "--check"],
                cwd=repo,
                input=json.dumps(
                    {"tool_input": {"files": ["scripts/first.sh", "scripts/second.sh"]}}
                ),
                capture_output=True,
                text=True,
                env={
                    "PATH": f"{fake_bin}:/usr/bin:/bin",
                    "CODEX_PROJECT_DIR": str(repo),
                },
                check=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("second.sh", result.stderr)


class InfraAndStyleSkillHelperTests(unittest.TestCase):
    CHECKS = {
        "bash-runtime", "python-runtime", "yaml-parser", "git-discovery",
        "tracked-snapshot", "input-graph", "support-tools", "fixture-git",
        "yaml-lint", "shell-lint", "docker-cli", "compose-plugin",
        "compose-config-render", "compose-structure", "runtime-observation",
        "secret-values", "fixture-cleanup",
    }

    @staticmethod
    def _write_executable(path: pathlib.Path, body: str) -> None:
        path.write_text("#!/bin/sh\n" + body, encoding="utf-8")
        path.chmod(0o755)

    def _repo(self, base: pathlib.Path, compose: str = "services:\n  app:\n    image: busybox\n") -> tuple[pathlib.Path, pathlib.Path]:
        repo = base / "repo with spaces"
        script = repo / ".agents/skills/infra-validate/scripts/static-checks.sh"
        validator = repo / "scripts/validation/validate-docker-compose.sh"
        script.parent.mkdir(parents=True)
        validator.parent.mkdir(parents=True)
        script.write_bytes(INFRA_STATIC.read_bytes())
        validator.write_bytes((ROOT / "scripts/validation/validate-docker-compose.sh").read_bytes())
        (repo / "docker-compose.yml").write_text(compose, encoding="utf-8")
        (repo / ".env.example").write_text("APP_PORT=1234\n", encoding="utf-8")
        (repo / ".yamllint").write_text("extends: default\n", encoding="utf-8")
        (repo / ".shellcheckrc").write_text(
            "external-sources=true\nsource-path=SCRIPTDIR\n", encoding="utf-8"
        )
        policy = repo / "docs/05.operations/policies/0078-compose-profile-vocabulary.md"
        policy.parent.mkdir(parents=True)
        policy.write_text("| Named selection | Profiles |\n| --- | --- |\n| HOME | `core` |\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
        tools = base / "tools"
        tools.mkdir()
        for name in ("bash", "cp", "dirname", "git", "mkdir", "python3", "rm", "sed", "sleep", "sort", "tr", "wc"):
            target = shutil.which(name)
            if target:
                (tools / name).symlink_to(target)
        trace = tools / "docker.trace"
        environment_trace = tools / "docker.env"
        self._write_executable(
            tools / "docker",
            f'printf "%s\\n" "$*" >> {shlex.quote(str(trace))}\n'
            f'plugin={shlex.quote(str(tools / "plugin.exit"))}\n'
            f'failure={shlex.quote(str(tools / "docker.exit"))}\n'
            f'delay={shlex.quote(str(tools / "docker.sleep"))}\n'
            f'survived={shlex.quote(str(tools / "docker.survived"))}\n'
            f'printf "PWD=%s\\nHOME=%s\\nXDG=%s\\nDOCKER_CONFIG=%s\\nDOCKER_HOST=%s\\nTMPDIR=%s\\nPATH=%s\\nCOMPOSE=%s\\n" "$PWD" "$HOME" "$XDG_CONFIG_HOME" "$DOCKER_CONFIG" "$DOCKER_HOST" "$TMPDIR" "$PATH" "${{COMPOSE_PROJECT_NAME-}}" > {shlex.quote(str(environment_trace))}\n'
            'if [ -f "$delay" ]; then trap "" TERM; (trap "" TERM; /bin/sleep 10; : > "$survived") & wait; fi\n'
            'case "$*" in\n'
            '  "compose version") if [ -f "$plugin" ]; then read -r status < "$plugin"; exit "$status"; fi; exit 0 ;;\n'
            '  *"config --profiles"*) printf "core\\n" ;;\n'
            '  *"config --services"*) printf "app\\n" ;;\n'
            '  *"config --format json"*) printf "{\\\"services\\\":{}}\\n" ;;\n'
            'esac\nif [ -f "$failure" ]; then read -r status < "$failure"; exit "$status"; fi\nexit 0\n',
        )
        self._write_executable(
            tools / "yamllint",
            f'printf "%s\\n" "$@" > {shlex.quote(str(tools / "yaml.args"))}\n'
            f'failure={shlex.quote(str(tools / "yaml.exit"))}\n'
            'if [ -f "$failure" ]; then read -r status < "$failure"; exit "$status"; fi\nexit 0\n',
        )
        self._write_executable(
            tools / "shellcheck",
            f'printf "%s\\n" "$@" > {shlex.quote(str(tools / "shell.args"))}\n'
            f'failure={shlex.quote(str(tools / "shell.exit"))}\n'
            'if [ -f "$failure" ]; then read -r status < "$failure"; exit "$status"; fi\nexit 0\n',
        )
        return repo, tools

    @staticmethod
    def _run(repo: pathlib.Path, tools: pathlib.Path, *args: str, cwd: pathlib.Path | None = None, extra: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        env = {"PATH": str(tools), "LC_ALL": "C"}
        env.update(extra or {})
        return subprocess.run(["/bin/bash", str(repo / ".agents/skills/infra-validate/scripts/static-checks.sh"), *args], cwd=cwd or repo, text=True, capture_output=True, env=env, check=False)

    @staticmethod
    def _track(repo: pathlib.Path, relative: str, body: str, *, executable: bool = False) -> pathlib.Path:
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
        if executable:
            target.chmod(0o755)
        subprocess.run(["git", "add", relative], cwd=repo, check=True)
        return target

    def _assert_report(self, result: subprocess.CompletedProcess[str]) -> None:
        lines = result.stdout.splitlines()
        records = {line.split()[0] for line in lines if " category=" in line}
        self.assertTrue(self.CHECKS <= records, result.stdout)
        self.assertTrue(any(line.startswith("summary ") for line in lines))
        self.assertTrue(all(len(line.encode("utf-8")) <= 4096 for line in lines))
        self.assertTrue(all("child_exit=" in line for line in lines if " category=" in line))

    def test_static_checks_close_cli_and_ignore_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, tools = self._repo(pathlib.Path(directory))
            for cwd in (repo, repo / "scripts", repo / ".agents/skills/infra-validate"):
                result = self._run(repo, tools, cwd=cwd)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn("shell-lint NOT_APPLICABLE category=no-eligible-input", result.stdout)
                self.assertIn("runtime-observation NOT_RUN", result.stdout)
            self.assertEqual(0, self._run(repo, tools, "--help").returncode)
            bad = self._run(repo, tools, "--bad")
            self.assertEqual(2, bad.returncode)
            self.assertFalse((tools / "docker.trace").read_text().startswith("--bad"))

    def test_static_checks_aggregate_fail_over_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, tools = self._repo(pathlib.Path(directory))
            (tools / "yamllint").unlink()
            (tools / "docker.exit").write_text("37", encoding="utf-8")
            result = self._run(repo, tools)
            self.assertEqual(1, result.returncode, result.stdout)
            self.assertIn("yaml-lint BLOCKED category=missing-tool", result.stdout)
            self.assertIn("compose-config-render FAIL category=command-failed child_exit=37", result.stdout)
            self.assertRegex(result.stdout, r"summary .*FAIL=[1-9].*BLOCKED=[1-9]")

    def test_static_checks_block_git_and_plugin_failures(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, tools = self._repo(pathlib.Path(directory))
            real_git = (tools / "git").resolve()
            (tools / "git").unlink()
            self._write_executable(tools / "git", f'exit 41\n# {real_git}\n')
            result = self._run(repo, tools)
            self.assertEqual(2, result.returncode)
            self.assertIn("git-discovery BLOCKED category=command-failed child_exit=41", result.stdout)
            self.assertIn("support-tools PASS category=available", result.stdout)
            self.assertIn("docker-cli PASS category=available", result.stdout)
        with tempfile.TemporaryDirectory() as directory:
            repo, tools = self._repo(pathlib.Path(directory))
            (tools / "plugin.exit").write_text("42", encoding="utf-8")
            result = self._run(repo, tools)
            self.assertEqual(2, result.returncode)
            self.assertIn("compose-plugin BLOCKED category=plugin-unavailable child_exit=42", result.stdout)

    def test_static_checks_bound_git_failures_and_index_races(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, tools = self._repo(pathlib.Path(directory))
            (tools / "git").unlink()
            (tools / "git").write_text("#!/missing/interpreter\n", encoding="utf-8")
            (tools / "git").chmod(0o755)
            result = self._run(repo, tools)
            self.assertEqual(2, result.returncode)
            self.assertIn("git-discovery BLOCKED category=launch-error child_exit=127", result.stdout)
        for name, body, category in (
            (
                "invalid",
                'if [ "$1" = ls-files ]; then printf "\\377"; exit 0; fi\n',
                "invalid-output",
            ),
            (
                "oversize",
                'if [ "$1" = rev-parse ]; then while :; do printf "'
                + ("x" * 96)
                + '"; done; fi\n',
                "output-limit",
            ),
        ):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                repo, tools = self._repo(pathlib.Path(directory))
                script = repo / ".agents/skills/infra-validate/scripts/static-checks.sh"
                if name == "oversize":
                    script.write_text(
                        script.read_text(encoding="utf-8").replace(
                            "MAX_CAPTURE = 16 * 1024 * 1024", "MAX_CAPTURE = 64"
                        ),
                        encoding="utf-8",
                    )
                real_git = (tools / "git").resolve()
                (tools / "git").unlink()
                self._write_executable(
                    tools / "git",
                    body + f'exec {shlex.quote(str(real_git))} "$@"\n',
                )
                ambient = pathlib.Path(directory) / "ambient-tmp"
                ambient.mkdir()
                started = time.monotonic()
                result = self._run(
                    repo, tools, extra={"TMPDIR": str(ambient)}
                )
                elapsed = time.monotonic() - started
                self.assertEqual(2, result.returncode, result.stdout)
                self.assertIn(
                    f"git-discovery BLOCKED category={category}", result.stdout
                )
                if name == "oversize":
                    self.assertLess(elapsed, 3)
                    self.assertEqual([], list(ambient.iterdir()))
        with tempfile.TemporaryDirectory() as directory:
            base = pathlib.Path(directory)
            repo, tools = self._repo(base)
            real_git = (tools / "git").resolve()
            counter = tools / "ls-files.count"
            (tools / "git").unlink()
            self._write_executable(
                tools / "git",
                f'counter={shlex.quote(str(counter))}\n'
                'if [ "$1" = ls-files ]; then\n'
                '  count=0; [ ! -f "$counter" ] || read -r count < "$counter"\n'
                '  count=$((count + 1)); printf "%s\\n" "$count" > "$counter"\n'
                f'  {shlex.quote(str(real_git))} "$@"\n'
                '  [ "$count" -lt 2 ] || printf "drift\\000"\n'
                '  exit 0\n'
                'fi\n'
                f'exec {shlex.quote(str(real_git))} "$@"\n',
            )
            result = self._run(repo, tools)
            self.assertEqual(2, result.returncode, result.stdout)
            self.assertIn("input-graph BLOCKED category=unsafe-input-graph", result.stdout)
            self.assertFalse((tools / "docker.trace").exists())
        with tempfile.TemporaryDirectory() as directory:
            repo, tools = self._repo(pathlib.Path(directory))
            real_git = (tools / "git").resolve()
            (tools / "git").unlink()
            self._write_executable(
                tools / "git",
                'if [ "$1" = init ]; then exit 43; fi\n'
                f'exec {shlex.quote(str(real_git))} "$@"\n',
            )
            result = self._run(repo, tools)
            self.assertEqual(2, result.returncode, result.stdout)
            self.assertIn("fixture-git BLOCKED category=command-failed child_exit=43", result.stdout)
            self.assertFalse((tools / "docker.trace").exists())

    def test_static_checks_fail_closed_for_missing_prerequisites(self) -> None:
        cases = (
            ("python3", "python-runtime"),
            ("docker", "docker-cli"),
            ("yamllint", "yaml-lint"),
            ("cp", "support-tools"),
        )
        for executable, check in cases:
            with self.subTest(executable=executable), tempfile.TemporaryDirectory() as directory:
                repo, tools = self._repo(pathlib.Path(directory))
                (tools / executable).unlink()
                result = self._run(repo, tools)
                self.assertEqual(2, result.returncode, result.stdout)
                self.assertIn(f"{check} BLOCKED category=missing-tool", result.stdout)
                self._assert_report(result)
        with tempfile.TemporaryDirectory() as directory:
            repo, tools = self._repo(pathlib.Path(directory))
            (tools / "python3").unlink()
            self._write_executable(tools / "python3", "exit 1\n")
            result = self._run(repo, tools)
            self.assertEqual(2, result.returncode)
            self.assertIn("yaml-parser BLOCKED category=missing-tool", result.stdout)
            self._assert_report(result)

    def test_static_checks_lint_every_tracked_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, tools = self._repo(pathlib.Path(directory))
            self._track(repo, "infra/check.sh", "#!/bin/sh\necho ok\n", executable=True)
            self._track(repo, "infra/config.yml", "key: value\n")
            result = self._run(repo, tools)
            self.assertEqual(0, result.returncode, result.stdout)
            self.assertIn("shell-lint PASS category=validated child_exit=0", result.stdout)
            self.assertIn("yaml-lint PASS category=validated child_exit=0", result.stdout)
            self.assertEqual(
                ["--rcfile=.shellcheckrc", "--severity=warning", "infra/check.sh"],
                (tools / "shell.args").read_text(encoding="utf-8").splitlines(),
            )
            self.assertEqual(
                ["-c", ".yamllint", "-s", "infra/config.yml"],
                (tools / "yaml.args").read_text(encoding="utf-8").splitlines(),
            )
            (tools / "shell.exit").write_text("37", encoding="utf-8")
            (tools / "yaml.exit").write_text("38", encoding="utf-8")
            result = self._run(repo, tools)
            self.assertEqual(1, result.returncode, result.stdout)
            self.assertIn("shell-lint FAIL category=command-failed child_exit=37", result.stdout)
            self.assertIn("yaml-lint FAIL category=command-failed child_exit=38", result.stdout)
        with tempfile.TemporaryDirectory() as directory:
            repo, tools = self._repo(pathlib.Path(directory))
            self._track(repo, "infra/check.sh", "#!/bin/sh\necho ok\n", executable=True)
            (tools / "shellcheck").unlink()
            result = self._run(repo, tools)
            self.assertEqual(2, result.returncode, result.stdout)
            self.assertIn("shell-lint BLOCKED category=missing-tool child_exit=127", result.stdout)

    def test_static_checks_block_unsafe_graph_before_docker(self) -> None:
        cases = (
            ("services:\n  app:\n    image: busybox\n    volumes: ['/outside:/inside']\n", "external-absolute-path"),
            ("services:\n  app:\n    image: busybox\n    env_file: ${MISSING}\n", "unresolved-path-interpolation"),
            ("services:\n  app:\n    image: one\n  app:\n    image: two\n", "unsupported-input-graph"),
            ("services:\n  app:\n    build: []\n", "unsupported-input-graph"),
            ("services:\n  app:\n    image: busybox\n    label_file: ./labels\n", "unsupported-input-graph"),
            ("services:\n  app:\n    image: busybox\n    credential_spec: {file: ./cred}\n", "unsupported-input-graph"),
            ("services:\n  app:\n    image: busybox\n    develop: {watch: [{path: ./src, action: sync}]}\n", "unsupported-input-graph"),
            ("services: {app: {image: busybox}}\nconfigs: {bad: {unknown_file: ./x}}\n", "unsupported-input-graph"),
            ("unknown_top: {file: ./x}\nservices: {}\n", "unsupported-input-graph"),
            ("services: {app: {image: busybox, unknown_host: ./x}}\n", "unsupported-input-graph"),
            ("include: [{path: child.yml, project_directory: project, env_file: include.env}]\nservices: {}\n", "unsupported-input-graph"),
            ("services: {app: {image: busybox, extends: {file: base.yml, service: base}}}\n", "unsupported-input-graph"),
        )
        for compose, category in cases:
            with self.subTest(category=category), tempfile.TemporaryDirectory() as directory:
                repo, tools = self._repo(pathlib.Path(directory), compose)
                result = self._run(repo, tools)
                self.assertEqual(2, result.returncode, result.stdout)
                self.assertIn(f"input-graph BLOCKED category={category}", result.stdout)
                self.assertFalse((tools / "docker.trace").exists())

    def test_static_checks_continue_lint_after_graph_block(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, tools = self._repo(
                pathlib.Path(directory),
                "services:\n  app:\n    image: busybox\n    volumes: ['/outside:/x']\n",
            )
            self._track(repo, "infra/check.sh", "#!/bin/sh\necho ok\n", executable=True)
            self._track(repo, "infra/config.yml", "key: value\n")
            (tools / "shell.exit").write_text("37", encoding="utf-8")
            (tools / "yaml.exit").write_text("38", encoding="utf-8")
            result = self._run(repo, tools)
            self.assertEqual(1, result.returncode, result.stdout)
            self.assertIn("input-graph BLOCKED category=external-absolute-path", result.stdout)
            self.assertIn("shell-lint FAIL category=command-failed child_exit=37", result.stdout)
            self.assertIn("yaml-lint FAIL category=command-failed child_exit=38", result.stdout)
            self.assertFalse((tools / "docker.trace").exists())

    def test_static_checks_validate_the_reachable_compose_graph(self) -> None:
        compose = (
            "include: [child.yml]\n"
            "services:\n"
            "  app:\n"
            "    image: busybox\n"
            "    env_file: {path: app.env, required: true}\n"
            "    build:\n"
            "      context: build\n"
            "      dockerfile: Dockerfile\n"
            "      additional_contexts: {extra: extra}\n"
            "    volumes:\n"
            "      - ./config.txt:/config:ro\n"
            "      - {type: bind, source: ./bind, target: /bind}\n"
            "configs: {cfg: {file: ./config.txt}}\n"
            "secrets: {generated: {file: ./generated/secret.txt}}\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            repo, tools = self._repo(pathlib.Path(directory), compose)
            files = {
                "child.yml": "services: {child: {image: busybox}}\n",
                "app.env": "APP=fixture\n",
                "build/Dockerfile": "FROM scratch\n",
                "extra/keep": "fixture\n",
                "bind/keep": "fixture\n",
                "config.txt": "fixture\n",
            }
            for relative, body in files.items():
                self._track(repo, relative, body)
            result = self._run(repo, tools)
            self.assertEqual(0, result.returncode, result.stdout)
            self.assertIn("input-graph PASS category=verified", result.stdout)

    def test_static_checks_reject_symlink_and_sensitive_graph_inputs(self) -> None:
        cases = ("infra/.env.local", "infra/secrets/value.txt")
        for relative in cases:
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as directory:
                repo, tools = self._repo(
                    pathlib.Path(directory),
                    f"services:\n  app:\n    image: busybox\n    env_file: {relative}\n",
                )
                self._track(repo, relative, "DO_NOT_READ\n")
                result = self._run(repo, tools)
                self.assertEqual(2, result.returncode, result.stdout)
                self.assertFalse((tools / "docker.trace").exists())
        with tempfile.TemporaryDirectory() as directory:
            base = pathlib.Path(directory)
            repo, tools = self._repo(
                base,
                "services:\n  app:\n    image: busybox\n    volumes: ['./config/link:/x']\n",
            )
            outside = base / "outside"
            outside.write_text("DO_NOT_READ", encoding="utf-8")
            link = repo / "config/link"
            link.parent.mkdir()
            link.symlink_to(outside)
            subprocess.run(["git", "add", "config/link"], cwd=repo, check=True)
            result = self._run(repo, tools)
            self.assertEqual(2, result.returncode, result.stdout)
            self.assertIn("input-graph BLOCKED", result.stdout)
            self.assertFalse((tools / "docker.trace").exists())
        with tempfile.TemporaryDirectory() as directory:
            base = pathlib.Path(directory)
            repo, tools = self._repo(
                base,
                "services:\n  app:\n    image: busybox\n    volumes: ['./config:/x']\n",
            )
            self._track(repo, "config/data", "tracked\n")
            shutil.rmtree(repo / "config")
            outside_dir = base / "outside-dir"
            outside_dir.mkdir()
            (outside_dir / "data").write_text("DO_NOT_READ", encoding="utf-8")
            (repo / "config").symlink_to(outside_dir, target_is_directory=True)
            result = self._run(repo, tools)
            self.assertEqual(2, result.returncode, result.stdout)
            self.assertIn("input-graph BLOCKED", result.stdout)
            self.assertFalse((tools / "docker.trace").exists())

    def test_static_checks_reject_cycles_and_generated_collisions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, tools = self._repo(
                pathlib.Path(directory),
                "include: [child.yml]\nservices: {app: {image: busybox}}\n",
            )
            self._track(
                repo,
                "child.yml",
                "include: [docker-compose.yml]\nservices: {child: {image: busybox}}\n",
            )
            result = self._run(repo, tools)
            self.assertEqual(2, result.returncode, result.stdout)
            self.assertIn("input-graph BLOCKED category=unsupported-input-graph", result.stdout)
            self.assertFalse((tools / "docker.trace").exists())
        with tempfile.TemporaryDirectory() as directory:
            repo, tools = self._repo(
                pathlib.Path(directory),
                "services: {app: {image: busybox}}\n"
                "secrets: {bad: {file: ./.env.example}}\n",
            )
            result = self._run(repo, tools)
            self.assertEqual(2, result.returncode, result.stdout)
            self.assertIn("input-graph BLOCKED category=unsafe-input-graph", result.stdout)
            self.assertFalse((tools / "docker.trace").exists())

    def test_static_checks_timeout_kills_the_child_group(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo, tools = self._repo(pathlib.Path(directory))
            script = repo / ".agents/skills/infra-validate/scripts/static-checks.sh"
            script.write_text(
                script.read_text(encoding="utf-8")
                .replace("TIMEOUT_SECONDS = 59", "TIMEOUT_SECONDS = 0.1")
                .replace("KILL_GRACE_SECONDS = 1", "KILL_GRACE_SECONDS = 0.1"),
                encoding="utf-8",
            )
            (tools / "docker.sleep").touch()
            result = self._run(repo, tools)
            self.assertEqual(1, result.returncode, result.stdout)
            self.assertIn("compose-plugin FAIL category=timeout child_exit=124", result.stdout)
            self.assertFalse((tools / "docker.survived").exists())

    def test_static_checks_do_not_touch_real_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = pathlib.Path(directory)
            repo, tools = self._repo(base)
            sentinel = "SYNTHETIC_SECRET_MUST_NOT_LEAK"
            env_file = repo / ".env"
            env_file.write_text(sentinel, encoding="utf-8")
            (repo / ".gitignore").write_text(".env\nignored/\n", encoding="utf-8")
            ignored = repo / "ignored"
            ignored.mkdir()
            (ignored / "data").write_text(sentinel, encoding="utf-8")
            outside = base / "outside"
            outside.write_text(sentinel, encoding="utf-8")
            (ignored / "outside-link").symlink_to(outside)
            before = (
                env_file.read_bytes(),
                (ignored / "data").read_bytes(),
                outside.read_bytes(),
                env_file.stat(),
            )
            result = self._run(repo, tools)
            self.assertEqual(0, result.returncode, result.stdout)
            self.assertNotIn(sentinel, result.stdout + result.stderr)
            self.assertEqual(before[:3], (env_file.read_bytes(), (ignored / "data").read_bytes(), outside.read_bytes()))
            self.assertEqual(
                (before[3].st_ino, before[3].st_size, before[3].st_mtime_ns),
                (env_file.stat().st_ino, env_file.stat().st_size, env_file.stat().st_mtime_ns),
            )
            self.assertEqual([], list(repo.glob(".infra-static-*")))
            calls = (tools / "docker.trace").read_text().splitlines()
            self.assertTrue(calls)
            self.assertTrue(all(call.startswith("compose ") for call in calls))
            self.assertFalse(any("network" in call or "inspect" in call for call in calls))
            child_env = dict(
                line.split("=", 1)
                for line in (tools / "docker.env").read_text(encoding="utf-8").splitlines()
            )
            self.assertTrue(child_env["PWD"].startswith(str(repo / ".infra-static-")))
            self.assertEqual(child_env["PWD"] + "/.home", child_env["HOME"])
            self.assertEqual(child_env["PWD"] + "/.xdg", child_env["XDG"])
            self.assertEqual(child_env["PWD"] + "/.docker", child_env["DOCKER_CONFIG"])
            self.assertEqual(child_env["PWD"] + "/.tmp", child_env["TMPDIR"])
            self.assertEqual(child_env["PWD"] + "/.bin", child_env["PATH"])
            self.assertEqual("", child_env["COMPOSE"])
            self.assertEqual(
                "unix://" + child_env["PWD"] + "/.no-docker.sock",
                child_env["DOCKER_HOST"],
            )
            self._assert_report(result)


class QaCiToolEnvironmentTests(unittest.TestCase):
    @staticmethod
    def _write_executable(path: pathlib.Path) -> None:
        path.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        path.chmod(0o755)

    def test_repeated_bootstrap_preserves_existing_path_and_adds_each_dir_once(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = pathlib.Path(directory)
            prepared_bin = base / "prepared" / "bin"
            user_bin = base / "home" / ".local" / "bin"
            go_bin = base / "home" / "go" / "bin"
            extra_bin = base / "extra" / "bin"
            for path in (prepared_bin, user_bin, go_bin, extra_bin):
                path.mkdir(parents=True)
            self._write_executable(prepared_bin / "selected-tool")
            self._write_executable(user_bin / "selected-tool")
            self._write_executable(extra_bin / "extra-tool")

            original = [str(prepared_bin), "/usr/bin", "/bin"]
            command = (
                '. "$1"\n'
                'first="$PATH"\n'
                '. "$1"\n'
                'printf "FIRST=%s\\nSECOND=%s\\nSELECTED=%s\\nEXTRA=%s\\n" '
                '"$first" "$PATH" "$(command -v selected-tool)" '
                '"$(command -v extra-tool)"\n'
            )
            result = subprocess.run(
                ["/bin/bash", "-c", command, "bash", str(QA_CI_TOOLS)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                env={
                    "PATH": ":".join(original),
                    "HOME": str(base / "home"),
                    "QA_CI_NODE_BIN": "",
                    "QA_CI_EXTRA_PATHS": str(extra_bin),
                },
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            observed = dict(line.split("=", 1) for line in result.stdout.splitlines())
            self.assertEqual(observed["FIRST"], observed["SECOND"])
            entries = observed["SECOND"].split(":")
            self.assertEqual(original, entries[: len(original)])
            for path in (user_bin, go_bin, extra_bin):
                self.assertEqual(1, entries.count(str(path)))
            self.assertEqual(str(prepared_bin / "selected-tool"), observed["SELECTED"])
            self.assertEqual(str(extra_bin / "extra-tool"), observed["EXTRA"])

    def test_executed_bootstrap_still_reports_missing_tools(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            empty_path = pathlib.Path(directory) / "empty"
            empty_path.mkdir()
            result = subprocess.run(
                ["/bin/sh", str(QA_CI_TOOLS)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                env={
                    "PATH": str(empty_path),
                    "HOME": directory,
                    "QA_CI_NODE_BIN": "",
                },
                check=False,
            )

            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("python3=MISSING", result.stdout)
            self.assertIn("shellcheck=MISSING", result.stdout)


class PostToolFormattingOwnershipTests(unittest.TestCase):
    """The hook may format only in agreement with the registered owner.

    `.agents/governance/quality-standards.md` section 10 makes
    `.pre-commit-config.yaml` the sole place a formatting owner is named. These
    cases pin the three ways this hook previously disagreed with it.
    """

    @staticmethod
    def _write_executable(path: pathlib.Path, text: str) -> None:
        path.write_text(text, encoding="utf-8")
        path.chmod(0o755)

    @staticmethod
    def _repo(directory: str) -> pathlib.Path:
        repo = pathlib.Path(directory)
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        return repo

    def _run(
        self,
        repo: pathlib.Path,
        relative: str,
        *,
        path_prefix: str = "",
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(POST_TOOL), "--write"],
            cwd=repo,
            input=json.dumps({"tool_input": {"file_path": relative}}),
            capture_output=True,
            text=True,
            env={
                "PATH": f"{path_prefix}/usr/bin:/bin",
                "CODEX_PROJECT_DIR": str(repo),
            },
            check=False,
        )

    @staticmethod
    def _registered_shellcheck_severity() -> str:
        document = yaml.safe_load(
            (ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
        )
        for repository in document["repos"]:
            for hook in repository["hooks"]:
                if hook["id"] == "shellcheck":
                    for argument in hook.get("args", ()):
                        if argument.startswith("--severity="):
                            return argument
        raise AssertionError("no shellcheck severity is registered")

    def test_every_text_mutator_excludes_the_same_frozen_payloads(self) -> None:
        """Three mutators exclude these bytes; they must not drift apart.

        `.pre-commit-config.yaml` declares the boundary once as an anchor, and
        the PostToolUse hook reads that declaration. `markdownlint-cli2` runs
        with `fix: true` and cannot read a YAML anchor from another file, so it
        restates the boundary in its own ignore list. This compares the two by
        what they select rather than by how they spell it.
        """

        anchor = re.search(
            r"^\s*exclude:\s*&frozen_archive_payloads\s+'(?P<pattern>[^']+)'\s*$",
            (ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"),
            re.M,
        )
        self.assertIsNotNone(anchor, "the frozen payload anchor is missing")
        frozen = re.compile(anchor.group("pattern"))

        ignores = yaml.safe_load(
            (ROOT / ".markdownlint-cli2.yaml").read_text(encoding="utf-8")
        )["ignores"]

        def markdownlint_ignores(relative: str) -> bool:
            return any(
                relative.startswith(entry) if entry.endswith("/") else relative == entry
                for entry in ignores
            )

        tracked = subprocess.run(
            ["git", "ls-files", "-z", "docs/98.archive"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout.decode("utf-8")
        documents = [item for item in tracked.split("\0") if item.endswith(".md")]
        self.assertTrue(documents, "the archive holds no tracked Markdown")

        disagreements = [
            relative
            for relative in documents
            if bool(frozen.search(relative)) != markdownlint_ignores(relative)
        ]
        self.assertEqual([], disagreements)

    def test_pre_commit_registers_no_shell_formatting_owner(self) -> None:
        """A shell formatter absent from the owner does not govern the repository."""

        document = yaml.safe_load(
            (ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
        )
        registered = {
            hook["id"]
            for repository in document["repos"]
            for hook in repository["hooks"]
        }
        self.assertNotIn("shfmt", registered)

    def test_post_tool_does_not_run_an_unregistered_shell_formatter(self) -> None:
        """A shfmt on PATH that always fails must not reach the exit code."""

        with tempfile.TemporaryDirectory() as directory:
            repo = self._repo(directory)
            shell = repo / "example.sh"
            shell.write_text("#!/bin/sh\nif true; then\n    echo ok\nfi\n", "utf-8")
            before = shell.read_bytes()
            fake_bin = repo / "fake-bin"
            fake_bin.mkdir()
            self._write_executable(fake_bin / "shfmt", "#!/bin/sh\nexit 37\n")

            result = self._run(repo, "example.sh", path_prefix=f"{fake_bin}:")

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(before, shell.read_bytes())

    def test_post_tool_shellcheck_matches_the_registered_severity(self) -> None:
        """The hook passes the severity its registered owner declares."""

        with tempfile.TemporaryDirectory() as directory:
            repo = self._repo(directory)
            (repo / "example.sh").write_text("#!/bin/sh\necho ok\n", encoding="utf-8")
            fake_bin = repo / "fake-bin"
            fake_bin.mkdir()
            self._write_executable(
                fake_bin / "shellcheck",
                '#!/bin/sh\nprintf "%s\\n" "$@" > "$(dirname "$0")/argv"\nexit 0\n',
            )

            result = self._run(repo, "example.sh", path_prefix=f"{fake_bin}:")

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            recorded = (fake_bin / "argv").read_text(encoding="utf-8").split()
            self.assertIn(self._registered_shellcheck_severity(), recorded)

    def test_post_tool_mutator_honors_the_declared_frozen_boundary(self) -> None:
        """The boundary is read from the owner, not restated in this hook."""

        with tempfile.TemporaryDirectory() as directory:
            repo = self._repo(directory)
            (repo / ".pre-commit-config.yaml").write_text(
                "repos:\n"
                "  - repo: local\n"
                "    hooks:\n"
                "      - id: trailing-whitespace\n"
                "        exclude: &frozen_archive_payloads '^frozen/'\n",
                encoding="utf-8",
            )
            payload = "text with trailing space   \nno final newline"
            for relative in ("frozen/preserved.md", "active/normalized.md"):
                target = repo / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(payload, encoding="utf-8")

            frozen = repo / "frozen/preserved.md"
            active = repo / "active/normalized.md"
            before = frozen.read_bytes()

            self.assertEqual(0, self._run(repo, "frozen/preserved.md").returncode)
            self.assertEqual(0, self._run(repo, "active/normalized.md").returncode)

            self.assertEqual(before, frozen.read_bytes())
            self.assertEqual(
                "text with trailing space\nno final newline\n",
                active.read_text(encoding="utf-8"),
            )

    def test_post_tool_rejects_an_owner_without_the_frozen_anchor(self) -> None:
        """A registered owner that declares no boundary fails closed."""

        with tempfile.TemporaryDirectory() as directory:
            repo = self._repo(directory)
            (repo / ".pre-commit-config.yaml").write_text(
                "repos:\n  - repo: local\n    hooks:\n      - id: trailing-whitespace\n",
                encoding="utf-8",
            )
            target = repo / "active/document.md"
            target.parent.mkdir(parents=True)
            target.write_text("text   \n", encoding="utf-8")
            before = target.read_bytes()

            result = self._run(repo, "active/document.md")

            self.assertNotEqual(0, result.returncode)
            self.assertIn("frozen_archive_payloads", result.stderr)
            self.assertEqual(before, target.read_bytes())


if __name__ == "__main__":
    unittest.main()
