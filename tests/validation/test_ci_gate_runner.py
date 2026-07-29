from __future__ import annotations

import dataclasses
import io
import json
import os
import pathlib
import shutil
import signal
import subprocess
import tempfile
import time
import unittest
from unittest import mock

from scripts.validation import ci_gate_contract as contract
from scripts.validation import ci_gate_runner as runner


REAL_SUBPROCESS_RUN = subprocess.run


def _leaf(
    gate_id: str,
    *,
    entrypoint: str = "scripts/validation/leaf.py",
    argv: tuple[str, ...] = (),
) -> contract.GateNode:
    return contract.GateNode(
        gate_id=gate_id,
        kind=contract.GateKind.LEAF,
        suite_key=gate_id.removeprefix("leaf."),
        entrypoint=pathlib.PurePosixPath(entrypoint),
        argv=argv,
        cwd=pathlib.PurePosixPath("."),
        allowed_env_keys=(),
        timeout_minutes=1,
        profiles=("local-harness",),
        opaque=True,
        children=(),
    )


def _setup(gate_id: str) -> contract.GateNode:
    return contract.GateNode(
        gate_id=gate_id,
        kind=contract.GateKind.SETUP,
        suite_key=None,
        entrypoint=pathlib.PurePosixPath("scripts/validation/setup.sh"),
        argv=(),
        cwd=pathlib.PurePosixPath("."),
        allowed_env_keys=(),
        timeout_minutes=1,
        profiles=("local-harness",),
        opaque=False,
        children=(),
    )


def _registry() -> contract.GateRegistry:
    nodes = (
        contract.GateNode(
            gate_id="local.test",
            kind=contract.GateKind.AGGREGATE,
            suite_key=None,
            entrypoint=None,
            argv=(),
            cwd=None,
            allowed_env_keys=(),
            timeout_minutes=None,
            profiles=("local-harness",),
            opaque=False,
            children=(
                "setup.repo-python-dependencies",
                "leaf.repo-contracts",
                "leaf.repo-contracts",
            ),
        ),
        _setup("setup.repo-python-dependencies"),
        _leaf("leaf.repo-contracts"),
    )
    return contract.GateRegistry(
        nodes=nodes,
        job_roots=(),
        profile_roots=(
            contract.ProfileRoot(
                "local-harness",
                ("local.test",),
                "local",
            ),
        ),
    )


def _invocation(
    gate_id: str,
    entrypoint: str,
    *,
    cwd: str = ".",
    allowed_env_keys: tuple[str, ...] = (),
) -> runner.GateInvocation:
    return runner.GateInvocation(
        gate_id=gate_id,
        entrypoint=pathlib.PurePosixPath(entrypoint),
        argv=(),
        cwd=pathlib.PurePosixPath(cwd),
        allowed_env_keys=allowed_env_keys,
        timeout_seconds=60,
    )


class CiGateRunnerContractTests(unittest.TestCase):
    def test_required_runner_interfaces_are_exact(self) -> None:
        self.assertEqual(
            (
                "gate_id",
                "entrypoint",
                "argv",
                "cwd",
                "allowed_env_keys",
                "timeout_seconds",
            ),
            tuple(
                field.name
                for field in dataclasses.fields(runner.GateInvocation)
            ),
        )

    def test_build_plan_preserves_order_and_deduplicates_gate_ids(self) -> None:
        plan = runner.build_execution_plan(
            _registry(),
            "local-harness",
            None,
            True,
        )
        self.assertEqual(
            (
                "setup.repo-python-dependencies",
                "leaf.repo-contracts",
            ),
            tuple(invocation.gate_id for invocation in plan),
        )

    def test_unknown_profile_and_gate_fail_closed(self) -> None:
        with self.assertRaises(contract.GateContractError) as profile_error:
            runner.build_execution_plan(
                _registry(),
                "unknown",
                None,
                True,
            )
        self.assertEqual("ci-gate-profile-unknown", profile_error.exception.code)
        with self.assertRaises(contract.GateContractError) as gate_error:
            runner.build_execution_plan(
                _registry(),
                "local-harness",
                "leaf.unknown",
                False,
            )
        self.assertEqual(
            "ci-gate-selection-unreachable",
            gate_error.exception.code,
        )

    def test_fake_executor_receives_each_leaf_once_in_order(self) -> None:
        seen: list[str] = []
        plan = runner.build_execution_plan(
            _registry(),
            "local-harness",
            None,
            True,
        )
        result = runner.execute_execution_plan(
            pathlib.Path.cwd(),
            plan,
            environ={"PATH": "/usr/bin", "GIT_DIR": "/tmp/hostile"},
            executor=lambda invocation: seen.append(invocation.gate_id) or 0,
        )
        self.assertEqual(0, result)
        self.assertEqual(
            ["setup.repo-python-dependencies", "leaf.repo-contracts"],
            seen,
        )

    def test_nonzero_fake_child_is_propagated_and_stops_plan(self) -> None:
        seen: list[str] = []

        def execute(invocation: runner.GateInvocation) -> int:
            seen.append(invocation.gate_id)
            return 17

        self.assertEqual(
            17,
            runner.execute_execution_plan(
                pathlib.Path.cwd(),
                (
                    _invocation("leaf.first", "first.py"),
                    _invocation("leaf.second", "second.py"),
                ),
                {"PATH": "/usr/bin"},
                executor=execute,
            ),
        )
        self.assertEqual(["leaf.first"], seen)

    def test_list_and_dry_run_are_deterministic_and_value_free(self) -> None:
        plan = runner.build_execution_plan(
            _registry(),
            "local-harness",
            None,
            True,
        )
        rendered = runner.render_execution_plan(plan)
        self.assertEqual(rendered, runner.render_execution_plan(plan))
        self.assertEqual(
            (
                "setup.repo-python-dependencies\tscripts/validation/setup.sh",
                "leaf.repo-contracts\tscripts/validation/leaf.py",
            ),
            rendered,
        )
        self.assertNotIn("hostile-secret-value", "\n".join(rendered))

    def test_cli_rejects_mutually_exclusive_gate_and_all(self) -> None:
        stderr = io.StringIO()
        with mock.patch("sys.stderr", stderr):
            result = runner.main(
                [
                    "--profile",
                    "local-harness",
                    "--gate",
                    "leaf.repo-contracts",
                    "--all",
                ]
            )
        self.assertEqual(2, result)
        self.assertIn("ci-gate-cli-arguments", stderr.getvalue())

    def test_cli_list_and_dry_run_use_strict_json_without_execution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            contract_path = root / ".github/workflow-contract.yml"
            contract_path.parent.mkdir()
            contract_path.write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "workflows": {},
                        "gate_nodes": [
                            {
                                "gate_id": "leaf.repo-contracts",
                                "kind": "leaf",
                                "suite_key": "repo-contracts",
                                "entrypoint": "scripts/validation/leaf.py",
                                "argv": [],
                                "cwd": ".",
                                "allowed_env_keys": [],
                                "timeout_minutes": 1,
                                "profiles": ["local-harness"],
                                "opaque": True,
                            }
                        ],
                        "job_roots": [],
                        "profile_roots": [
                            {
                                "profile": "local-harness",
                                "root_gate_ids": ["leaf.repo-contracts"],
                                "classification": "local",
                            }
                        ],
                        "actions": {},
                    },
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            with (
                mock.patch.dict(
                    os.environ,
                    {
                        "HYHOME_CI_GATE_ROOT": str(root),
                        "PATH": "/usr/bin",
                    },
                    clear=True,
                ),
                mock.patch.object(
                    runner,
                    "validate_gate_registry",
                    return_value=(),
                    create=True,
                ),
                mock.patch.object(
                    runner,
                    "execute_execution_plan",
                ) as execute,
                mock.patch("sys.stdout", new_callable=io.StringIO) as stdout,
            ):
                self.assertEqual(
                    0,
                    runner.main(["--profile", "local-harness", "--list"]),
                )
                self.assertEqual(
                    0,
                    runner.main(
                        [
                            "--profile",
                            "local-harness",
                            "--dry-run",
                            "--all",
                        ]
                    ),
                )
            execute.assert_not_called()
            self.assertEqual(
                2,
                stdout.getvalue().count(
                    "leaf.repo-contracts\tscripts/validation/leaf.py"
                ),
            )


class DescriptorExecutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir="/tmp")
        self.root = pathlib.Path(self.temporary.name).resolve()
        REAL_SUBPROCESS_RUN(
            ["git", "init", "-q"],
            cwd=self.root,
            check=True,
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def add_entrypoint(
        self,
        relative: str,
        text: str = "#!/usr/bin/env python3\nraise SystemExit(0)\n",
        *,
        mode: int = 0o755,
        tracked: bool = True,
    ) -> pathlib.Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        path.chmod(mode)
        if tracked:
            REAL_SUBPROCESS_RUN(
                ["git", "add", "--", relative],
                cwd=self.root,
                check=True,
            )
            if mode & 0o111:
                REAL_SUBPROCESS_RUN(
                    [
                        "git",
                        "update-index",
                        "--chmod=+x",
                        "--",
                        relative,
                    ],
                    cwd=self.root,
                    check=True,
                )
        return path

    def child_interceptor(self, captures: list[dict[str, object]]):
        def intercept(
            root_fd: int,
            item: runner._VerifiedInvocation,
            environment: dict[str, str],
        ) -> int:
            captures.append(
                {
                    "root_fd": root_fd,
                    "item": item,
                    "env": environment,
                    "shell": False,
                }
            )
            return 0

        return intercept

    def test_minimal_environment_clears_git_and_shares_one_home(self) -> None:
        self.add_entrypoint("scripts/validation/one.py")
        self.add_entrypoint("scripts/validation/two.py")
        captures: list[dict[str, object]] = []
        with mock.patch.object(
            runner,
            "_run_verified_child",
            side_effect=self.child_interceptor(captures),
        ):
            result = runner.execute_execution_plan(
                self.root,
                (
                    _invocation(
                        "leaf.one",
                        "scripts/validation/one.py",
                        allowed_env_keys=("EVENT_NAME",),
                    ),
                    _invocation("leaf.two", "scripts/validation/two.py"),
                ),
                {
                    "PATH": "/usr/bin",
                    "EVENT_NAME": "push",
                    "GIT_DIR": "/tmp/hostile",
                    "GIT_CONFIG": "hostile",
                    "PYTHONPATH": "/tmp/hostile",
                    "NODE_OPTIONS": "--require hostile",
                },
            )
        self.assertEqual(0, result)
        self.assertEqual(2, len(captures))
        environments = [capture["env"] for capture in captures]
        self.assertEqual(
            environments[0]["HOME"],  # type: ignore[index]
            environments[1]["HOME"],  # type: ignore[index]
        )
        for environment in environments:
            self.assertEqual("C.UTF-8", environment["LANG"])  # type: ignore[index]
            self.assertRegex(
                environment["HYHOME_CI_GATE_ROOT"],  # type: ignore[index]
                r"\A/proc/self/fd/[0-9]+\Z",
            )
            self.assertNotIn("GIT_DIR", environment)
            self.assertNotIn("GIT_CONFIG", environment)
            self.assertNotIn("NODE_OPTIONS", environment)
            self.assertNotEqual(
                "/tmp/hostile",
                environment["PYTHONPATH"],  # type: ignore[index]
            )
        self.assertFalse(pathlib.Path(environments[0]["HOME"]).exists())  # type: ignore[index]
        self.assertTrue(all(capture["shell"] is False for capture in captures))
        self.assertTrue(
            all(
                capture["item"].entrypoint_fd >= 0  # type: ignore[union-attr]
                for capture in captures
            )
        )
        self._assert_runner_rejects_immutable_and_dangerous_allowed_env_keys()

    def test_timeout_returns_124_and_home_is_cleaned(self) -> None:
        self.add_entrypoint("scripts/validation/timeout.py")
        homes: list[pathlib.Path] = []

        def intercept(
            _root_fd: int,
            _item: runner._VerifiedInvocation,
            environment: dict[str, str],
        ) -> int:
            homes.append(pathlib.Path(environment["HOME"]))
            return 124

        with mock.patch.object(
            runner,
            "_run_verified_child",
            side_effect=intercept,
        ):
            self.assertEqual(
                124,
                runner.execute_execution_plan(
                    self.root,
                    (_invocation("leaf.timeout", "scripts/validation/timeout.py"),),
                    {"PATH": "/usr/bin"},
                ),
            )
        self.assertEqual(1, len(homes))
        self.assertFalse(homes[0].exists())
        self._assert_timeout_terminates_child_and_grandchild_process_group()

    def test_executor_exception_always_cleans_home(self) -> None:
        created = self.root / "executor-home"

        def create_home(*_args: object, **_kwargs: object) -> str:
            created.mkdir()
            return str(created)

        with (
            mock.patch.object(runner.tempfile, "mkdtemp", side_effect=create_home),
            self.assertRaisesRegex(RuntimeError, "executor failed"),
        ):
            runner.execute_execution_plan(
                self.root,
                (_invocation("leaf.one", "unused.py"),),
                {"PATH": "/usr/bin"},
                executor=lambda _invocation: (_ for _ in ()).throw(
                    RuntimeError("executor failed")
                ),
            )
        self.assertFalse(created.exists())
        self._assert_home_cleanup_failure_is_value_free_and_not_silent()

    def test_symlink_untracked_mode_shebang_regular_and_cwd_fail_closed(
        self,
    ) -> None:
        valid = self.add_entrypoint("scripts/validation/valid.py")
        untracked = self.add_entrypoint(
            "scripts/validation/untracked.py",
            tracked=False,
        )
        wrong_mode = self.add_entrypoint(
            "scripts/validation/wrong-mode.py",
            mode=0o644,
        )
        unsupported = self.add_entrypoint(
            "scripts/validation/unsupported.py",
            "#!/bin/sh\nexit 0\n",
        )
        directory = self.root / "scripts/validation/not-regular.py"
        directory.mkdir()
        REAL_SUBPROCESS_RUN(
            ["git", "add", "--intent-to-add", "--", str(directory.relative_to(self.root))],
            cwd=self.root,
            check=False,
        )
        leaf_link = self.root / "scripts/validation/leaf-link.py"
        leaf_link.symlink_to(valid.name)
        parent_link = self.root / "linked"
        parent_link.symlink_to(self.root / "scripts", target_is_directory=True)
        cases = (
            (
                _invocation("leaf.symlink", "scripts/validation/leaf-link.py"),
                "ci-gate-entrypoint-symlink",
            ),
            (
                _invocation("leaf.parent", "linked/validation/valid.py"),
                "ci-gate-entrypoint-symlink",
            ),
            (
                _invocation("leaf.untracked", str(untracked.relative_to(self.root))),
                "ci-gate-entrypoint-untracked",
            ),
            (
                _invocation("leaf.mode", str(wrong_mode.relative_to(self.root))),
                "ci-gate-entrypoint-mode",
            ),
            (
                _invocation("leaf.shebang", str(unsupported.relative_to(self.root))),
                "ci-gate-entrypoint-shebang",
            ),
            (
                _invocation("leaf.regular", str(directory.relative_to(self.root))),
                "ci-gate-entrypoint-not-regular",
            ),
            (
                _invocation(
                    "leaf.cwd",
                    "scripts/validation/valid.py",
                    cwd="../outside",
                ),
                "ci-gate-cwd-invalid",
            ),
        )
        for invocation, expected_code in cases:
            with self.subTest(expected_code=expected_code):
                with self.assertRaises(contract.GateContractError) as caught:
                    runner.execute_execution_plan(
                        self.root,
                        (invocation,),
                        {"PATH": "/usr/bin"},
                    )
                self.assertEqual(expected_code, caught.exception.code)

    def test_path_replacement_after_open_executes_verified_descriptor(self) -> None:
        path = self.add_entrypoint(
            "scripts/validation/bound.py",
            "#!/usr/bin/env python3\n# original inode\nraise SystemExit(0)\n",
        )
        replacement = self.root / "replacement.py"
        replacement.write_text(
            "#!/usr/bin/env python3\n# replacement inode\nraise SystemExit(9)\n",
            encoding="utf-8",
        )
        replacement.chmod(0o755)
        observed: list[bytes] = []

        def intercept(
            _root_fd: int,
            item: runner._VerifiedInvocation,
            _environment: dict[str, str],
        ) -> int:
            os.replace(replacement, path)
            observed.append(os.pread(item.entrypoint_fd, 4096, 0))
            return 0

        with mock.patch.object(
            runner,
            "_run_verified_child",
            side_effect=intercept,
        ):
            self.assertEqual(
                0,
                runner.execute_execution_plan(
                    self.root,
                    (_invocation("leaf.bound", "scripts/validation/bound.py"),),
                    {"PATH": "/usr/bin"},
                ),
            )
        self.assertIn(b"original inode", observed[0])
        self.assertNotIn(b"replacement inode", observed[0])
        self._assert_descriptor_root_survives_path_replacement()

    def test_descriptor_mode_preserves_root_and_python_sibling_imports(
        self,
    ) -> None:
        self.add_entrypoint(
            "scripts/validation/sibling.py",
            "VALUE = 42\n",
            mode=0o644,
        )
        python_entrypoint = self.add_entrypoint(
            "scripts/validation/python-entry.py",
            (
                "#!/usr/bin/env python3\n"
                "import os\n"
                "import sibling\n"
                "from pathlib import Path\n"
                "root = Path(os.environ['HYHOME_CI_GATE_ROOT'])\n"
                "raise SystemExit(0 if sibling.VALUE == 42 and root.is_dir() else 7)\n"
            ),
        )
        bash_entrypoint = self.add_entrypoint(
            "scripts/validation/bash-entry.sh",
            (
                "#!/usr/bin/env bash\n"
                "set -euo pipefail\n"
                'test -d "$HYHOME_CI_GATE_ROOT"\n'
            ),
        )
        self.assertTrue(python_entrypoint.exists())
        self.assertTrue(bash_entrypoint.exists())
        self.assertEqual(
            0,
            runner.execute_execution_plan(
                self.root,
                (
                    _invocation(
                        "leaf.python",
                        "scripts/validation/python-entry.py",
                    ),
                    _invocation(
                        "leaf.bash",
                        "scripts/validation/bash-entry.sh",
                    ),
                ),
                {
                    "PATH": os.environ.get("PATH", os.defpath),
                    "PYTHONPATH": "/tmp/hostile",
                },
            ),
        )
        self._assert_python_startup_ignores_untracked_sitecustomize()

    def _assert_descriptor_root_survives_path_replacement(self) -> None:
        marker = self.root / "root-marker"
        marker.write_text("original", encoding="utf-8")
        self.add_entrypoint(
            "scripts/validation/root-bound.py",
            (
                "#!/usr/bin/env python3\n"
                "import os\n"
                "from pathlib import Path\n"
                "root = Path(os.environ['HYHOME_CI_GATE_ROOT'])\n"
                "raise SystemExit("
                "0 if (root / 'root-marker').read_text() == 'original' else 9"
                ")\n"
            ),
        )
        original_root = self.root.with_name(f"{self.root.name}-original")
        real_verify = runner._verify_invocation
        replaced = False

        def replace_after_verify(*args: object, **kwargs: object):
            nonlocal replaced
            verified = real_verify(*args, **kwargs)
            if not replaced:
                self.root.rename(original_root)
                self.root.mkdir()
                replaced = True
            return verified

        with mock.patch.object(
            runner,
            "_verify_invocation",
            side_effect=replace_after_verify,
        ):
            try:
                self.assertEqual(
                    0,
                    runner.execute_execution_plan(
                        self.root,
                        (
                            _invocation(
                                "leaf.root-bound",
                                "scripts/validation/root-bound.py",
                            ),
                        ),
                        {"PATH": os.environ.get("PATH", os.defpath)},
                    ),
                )
            finally:
                if replaced:
                    shutil.rmtree(self.root)
                    original_root.rename(self.root)

    def _assert_python_startup_ignores_untracked_sitecustomize(self) -> None:
        injected = self.root / "sitecustomize-ran"
        (self.root / "sitecustomize.py").write_text(
            (
                "from pathlib import Path\n"
                f"Path({str(injected)!r}).write_text('injected')\n"
            ),
            encoding="utf-8",
        )
        self.add_entrypoint(
            "scripts/validation/isolation.py",
            "#!/usr/bin/env python3\nraise SystemExit(0)\n",
        )
        self.assertEqual(
            0,
            runner.execute_execution_plan(
                self.root,
                (
                    _invocation(
                        "leaf.isolation",
                        "scripts/validation/isolation.py",
                    ),
                ),
                {"PATH": os.environ.get("PATH", os.defpath)},
            ),
        )
        self.assertFalse(injected.exists())

    def _assert_timeout_terminates_child_and_grandchild_process_group(
        self,
    ) -> None:
        prefix = self.root / "timeout-tree"
        child_source = (
            "import pathlib,signal,subprocess,sys,time\n"
            "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
            "grand=subprocess.Popen([sys.executable,'-c',"
            "'import signal,time; signal.signal(signal.SIGTERM, "
            "signal.SIG_IGN); time.sleep(60)'])\n"
            "pathlib.Path(sys.argv[1]+'.grandchild').write_text(str(grand.pid))\n"
            "time.sleep(60)\n"
        )
        entrypoint = (
            "#!/usr/bin/env python3\n"
            "import pathlib,subprocess,sys,time\n"
            f"source={child_source!r}\n"
            "child=subprocess.Popen([sys.executable,'-c',source,sys.argv[1]])\n"
            "pathlib.Path(sys.argv[1]+'.child').write_text(str(child.pid))\n"
            "while not pathlib.Path(sys.argv[1]+'.grandchild').exists():\n"
            "    time.sleep(0.01)\n"
            "time.sleep(60)\n"
        )
        self.add_entrypoint("scripts/validation/tree.py", entrypoint)
        invocation = dataclasses.replace(
            _invocation("leaf.tree", "scripts/validation/tree.py"),
            argv=(str(prefix),),
            timeout_seconds=1,
        )
        pid_paths = (
            pathlib.Path(f"{prefix}.child"),
            pathlib.Path(f"{prefix}.grandchild"),
        )
        pids: list[int] = []
        try:
            self.assertEqual(
                124,
                runner.execute_execution_plan(
                    self.root,
                    (invocation,),
                    {"PATH": os.environ.get("PATH", os.defpath)},
                ),
            )
            pids = [int(path.read_text()) for path in pid_paths]
            time.sleep(0.1)
            for pid in pids:
                with self.assertRaises(ProcessLookupError):
                    os.kill(pid, 0)
        finally:
            for pid in pids:
                try:
                    os.kill(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass

    def _assert_runner_rejects_immutable_and_dangerous_allowed_env_keys(
        self,
    ) -> None:
        dangerous = (
            "HOME",
            "PATH",
            "LANG",
            "LC_ALL",
            "TMPDIR",
            "PYTHONPATH",
            "PYTHONSTARTUP",
            "HYHOME_CI_GATE_ROOT",
            "BASH_ENV",
            "ENV",
            "NODE_OPTIONS",
            "CDPATH",
            "IFS",
            "SHELLOPTS",
            "GLOBIGNORE",
            "GIT_DIR",
            "GITHUB_TOKEN",
        )
        for key in dangerous:
            with self.subTest(key=key):
                with self.assertRaises(contract.GateContractError) as caught:
                    runner._child_environment(
                        self.root,
                        self.root / "home",
                        _invocation(
                            "leaf.env",
                            "scripts/validation/env.py",
                            allowed_env_keys=(key,),
                        ),
                        "python",
                        {"PATH": "/usr/bin", key: "hostile"},
                    )
                self.assertEqual("ci-gate-environment", caught.exception.code)

    def _assert_home_cleanup_failure_is_value_free_and_not_silent(self) -> None:
        home = self.root / "cleanup-home"

        def create_home(*_args: object, **_kwargs: object) -> str:
            home.mkdir()
            return str(home)

        try:
            with (
                mock.patch.object(
                    runner.tempfile,
                    "mkdtemp",
                    side_effect=create_home,
                ),
                mock.patch.object(
                    runner.shutil,
                    "rmtree",
                    side_effect=PermissionError("private cleanup path"),
                ),
                self.assertRaises(contract.GateContractError) as caught,
            ):
                runner.execute_execution_plan(
                    self.root,
                    (),
                    {"PATH": "/usr/bin"},
                    executor=lambda _invocation: 0,
                )
            self.assertEqual(
                "ci-gate-home-cleanup",
                caught.exception.code,
            )
            self.assertNotIn("private cleanup path", str(caught.exception))
        finally:
            if home.exists():
                shutil.rmtree(home)


if __name__ == "__main__":
    unittest.main()
