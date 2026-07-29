from __future__ import annotations

import dataclasses
import io
import json
import os
import pathlib
import select
import shutil
import signal
import subprocess
import tempfile
import threading
import unittest
from unittest import mock

from scripts.validation import ci_gate_contract as contract
from scripts.validation import ci_gate_runner as runner


REAL_SUBPROCESS_RUN = subprocess.run
REAL_SHUTIL_RMTREE = shutil.rmtree


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
        self._assert_runner_finalizes_every_adapter_result()
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
        self._assert_registered_adapter_integrations()
        self._assert_python_startup_ignores_untracked_sitecustomize()

    def _assert_descriptor_root_survives_path_replacement(self) -> None:
        (self.root / ".env.example").write_text(
            "ORIGINAL_ROOT=1\n",
            encoding="utf-8",
        )
        REAL_SUBPROCESS_RUN(
            ["git", "add", "--", ".env.example"],
            cwd=self.root,
            check=True,
        )
        adapter_source = pathlib.Path(runner.__file__).with_name(
            "ci_gate_adapters.py"
        ).read_text(encoding="utf-8")
        self.add_entrypoint(
            "scripts/validation/ci_gate_adapters.py",
            adapter_source,
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
                            dataclasses.replace(
                                _invocation(
                                    "setup.compose-env",
                                    "scripts/validation/ci_gate_adapters.py",
                                ),
                                argv=("prepare-compose-env",),
                            ),
                        ),
                        {"PATH": os.environ.get("PATH", os.defpath)},
                    ),
                )
                self.assertEqual(
                    "ORIGINAL_ROOT=1\n",
                    (original_root / ".env").read_text(encoding="utf-8"),
                )
                self.assertFalse((self.root / ".env").exists())
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
        adapter_source = pathlib.Path(runner.__file__).with_name(
            "ci_gate_adapters.py"
        ).read_text(encoding="utf-8")
        self.add_entrypoint(
            "scripts/validation/ci_gate_adapters.py",
            adapter_source,
        )
        fake_bin = self.root / "fake-bin-isolation"
        fake_bin.mkdir()
        fake_uvx = fake_bin / "uvx"
        fake_uvx.write_text(
            self._fd_inventory_uvx_source(),
            encoding="utf-8",
        )
        fake_uvx.chmod(0o755)
        invocation = dataclasses.replace(
            _invocation(
                "leaf.zizmor",
                "scripts/validation/ci_gate_adapters.py",
            ),
            argv=("run-zizmor-sarif",),
        )
        self.assertEqual(
            0,
            runner.execute_execution_plan(
                self.root,
                (invocation,),
                {
                    "PATH": (
                        f"{fake_bin}:"
                        f"{os.environ.get('PATH', os.defpath)}"
                    )
                },
            ),
        )
        self.assertFalse(injected.exists())
        self.assertEqual(
            b'{"runs":[]}\n',
            (self.root / "results.sarif").read_bytes(),
        )
        (self.root / "results.sarif").unlink()

    def _assert_registered_adapter_integrations(self) -> None:
        adapter_source = pathlib.Path(runner.__file__).with_name(
            "ci_gate_adapters.py"
        ).read_text(encoding="utf-8")
        self.add_entrypoint(
            "scripts/validation/ci_gate_adapters.py",
            adapter_source,
        )
        (self.root / ".env.example").write_text(
            "SAFE_EXAMPLE=1\n",
            encoding="utf-8",
        )
        REAL_SUBPROCESS_RUN(
            ["git", "add", "--", ".env.example"],
            cwd=self.root,
            check=True,
        )
        fake_bin = self.root / "fake-bin"
        fake_bin.mkdir()
        fake_uvx = fake_bin / "uvx"
        fake_uvx.write_text(
            self._fd_inventory_uvx_source(),
            encoding="utf-8",
        )
        fake_uvx.chmod(0o755)
        plan = (
            dataclasses.replace(
                _invocation(
                    "setup.compose-env",
                    "scripts/validation/ci_gate_adapters.py",
                ),
                argv=("prepare-compose-env",),
            ),
            dataclasses.replace(
                _invocation(
                    "leaf.zizmor",
                    "scripts/validation/ci_gate_adapters.py",
                ),
                argv=("run-zizmor-sarif",),
            ),
        )
        self.assertEqual(
            0,
            runner.execute_execution_plan(
                self.root,
                plan,
                {
                    "PATH": (
                        f"{fake_bin}:"
                        f"{os.environ.get('PATH', os.defpath)}"
                    )
                },
            ),
        )
        self.assertEqual(
            b"SAFE_EXAMPLE=1\n",
            (self.root / ".env").read_bytes(),
        )
        self.assertEqual(
            b'{"runs":[]}\n',
            (self.root / "results.sarif").read_bytes(),
        )
        (self.root / ".env").unlink()
        (self.root / "results.sarif").unlink()

    def _fd_inventory_uvx_source(self) -> str:
        return (
            "#!/usr/bin/env python3\n"
            "import os, pathlib\n"
            "root=pathlib.Path(os.environ['HYHOME_CI_GATE_ROOT'])\n"
            "visible=[]\n"
            "for name in os.listdir('/proc/self/fd'):\n"
            "    number=int(name)\n"
            "    if number <= 2: continue\n"
            "    try: target=os.readlink('/proc/self/fd/'+name)\n"
            "    except OSError: continue\n"
            "    visible.append(target)\n"
            "valid=(len(visible)==1 and "
            "pathlib.Path(visible[0]).samefile(root) and "
            "os.getpgrp()==os.getpgid(os.getppid()))\n"
            "if not valid: raise SystemExit(9)\n"
            "print('{\"runs\":[]}')\n"
        )

    def _assert_timeout_terminates_child_and_grandchild_process_group(
        self,
    ) -> None:
        child_source = (
            "import os,pathlib,signal,subprocess,sys,time\n"
            "mode,ready,ack,release,trigger=sys.argv[1:]\n"
            "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
            "grand_source=\"import pathlib,signal,sys,time; \"\n"
            "grand_source+=\"signal.signal(signal.SIGTERM, signal.SIG_IGN); \"\n"
            "grand_source+=\"release=pathlib.Path(sys.argv[1]); \"\n"
            "grand_source+=\"\\nwhile not release.exists(): time.sleep(0.01)\"\n"
            "grand=subprocess.Popen([sys.executable,'-c',grand_source,release])\n"
            "with open(ready,'w',encoding='ascii') as stream:\n"
            "    stream.write(f'{os.getpid()} {grand.pid}\\n')\n"
            "    stream.flush()\n"
            "while not pathlib.Path(ack).exists(): time.sleep(0.01)\n"
            "if mode == 'safe-normal':\n"
            "    pathlib.Path(release).touch()\n"
            "    grand.wait()\n"
            "elif mode == 'overflow':\n"
            f"    os.write(1, b'x' * ({1024 * 1024 + 1}))\n"
            "    time.sleep(60)\n"
            "elif mode == 'read-error':\n"
            "    pathlib.Path(trigger).touch()\n"
            "    os.write(1, b'x')\n"
            "    time.sleep(60)\n"
            "else:\n"
            "    time.sleep(60)\n"
        )
        harness = (
            "#!/usr/bin/env python3\n"
            "import pathlib,subprocess,sys,time\n"
            "from scripts.validation import ci_gate_adapters as adapters\n"
            "mode,ready,ack,release,trigger=sys.argv[1:]\n"
            f"source={child_source!r}\n"
            "command=(sys.executable,'-c',source,mode,ready,ack,release,trigger)\n"
            "if mode in {'timeout','nonzero'}:\n"
            "    child=subprocess.Popen(command)\n"
            "    while not pathlib.Path(ack).exists(): time.sleep(0.01)\n"
            "    if mode == 'timeout': time.sleep(60)\n"
            "    raise SystemExit(17)\n"
            "if mode == 'read-error':\n"
            "    real_read=adapters.os.read\n"
            "    def controlled_read(descriptor, size):\n"
            "        if pathlib.Path(trigger).exists():\n"
            "            raise OSError('private read payload')\n"
            "        return real_read(descriptor, size)\n"
            "    adapters.os.read=controlled_read\n"
            "try:\n"
            "    result=adapters._run_child(\n"
            "        command,\n"
            "        root=pathlib.Path(adapters.os.environ['HYHOME_CI_GATE_ROOT']),\n"
            "        environ=adapters.os.environ,\n"
            "        capture_output=mode in {'overflow','read-error'},\n"
            "    )\n"
            "except adapters.AdapterError:\n"
            "    raise SystemExit(2)\n"
            "raise SystemExit(result.returncode)\n"
        )
        adapter_source = pathlib.Path(runner.__file__).with_name(
            "ci_gate_adapters.py"
        ).read_text(encoding="utf-8")
        self.add_entrypoint(
            "scripts/validation/ci_gate_adapters.py",
            adapter_source,
        )
        self.add_entrypoint("scripts/validation/tree-harness.py", harness)
        for mode, expected in (
            ("timeout", 124),
            ("overflow", 2),
            ("read-error", 2),
            ("nonzero", 17),
            ("safe-normal", 0),
        ):
            with self.subTest(lifecycle=mode):
                ready_path = self.root / f"{mode}.ready"
                ack_path = self.root / f"{mode}.ack"
                release_path = self.root / f"{mode}.release"
                trigger_path = self.root / f"{mode}.trigger"
                os.mkfifo(ready_path)
                ready_fd = os.open(
                    ready_path,
                    os.O_RDONLY | os.O_NONBLOCK,
                )
                result_read_fd, result_write_fd = os.pipe2(os.O_CLOEXEC)
                result: list[int | BaseException] = []
                pidfds: list[int] = []
                invocation = dataclasses.replace(
                    _invocation(
                        f"leaf.lifecycle-{mode}",
                        "scripts/validation/tree-harness.py",
                    ),
                    argv=(
                        mode,
                        str(ready_path),
                        str(ack_path),
                        str(release_path),
                        str(trigger_path),
                    ),
                    timeout_seconds=1 if mode == "timeout" else 10,
                )

                def execute() -> None:
                    try:
                        result.append(
                            runner.execute_execution_plan(
                                self.root,
                                (invocation,),
                                {
                                    "PATH": os.environ.get(
                                        "PATH",
                                        os.defpath,
                                    )
                                },
                            )
                        )
                    except BaseException as error:
                        result.append(error)
                    finally:
                        os.write(result_write_fd, b"done")
                        os.close(result_write_fd)

                worker = threading.Thread(target=execute)
                try:
                    worker.start()
                    ready_poll = select.poll()
                    ready_poll.register(ready_fd, select.POLLIN)
                    self.assertTrue(ready_poll.poll(5000))
                    pids = tuple(
                        int(value)
                        for value in os.read(ready_fd, 128)
                        .decode("ascii")
                        .split()
                    )
                    self.assertEqual(2, len(pids))
                    pidfds = [os.pidfd_open(pid) for pid in pids]
                    ack_path.touch()
                    result_poll = select.poll()
                    result_poll.register(result_read_fd, select.POLLIN)
                    self.assertTrue(result_poll.poll(15000))
                    os.read(result_read_fd, 16)
                    worker.join()
                    self.assertEqual([expected], result)
                    for pidfd in pidfds:
                        exit_poll = select.poll()
                        exit_poll.register(pidfd, select.POLLIN)
                        self.assertTrue(exit_poll.poll(1000))
                finally:
                    for pidfd in pidfds:
                        try:
                            signal.pidfd_send_signal(
                                pidfd,
                                signal.SIGKILL,
                            )
                        except OSError:
                            pass
                        os.close(pidfd)
                    os.close(ready_fd)
                    os.close(result_read_fd)

    def _assert_runner_finalizes_every_adapter_result(self) -> None:
        item = runner._VerifiedInvocation(
            _invocation("leaf.lifecycle", "scripts/validation/lifecycle.py"),
            entrypoint_fd=42,
            cwd_fd=43,
            interpreter="python",
        )
        for outcome, expected in ((0, 0), (17, 17), ("timeout", 124)):
            with self.subTest(outcome=outcome):
                process = mock.Mock(pid=43210)
                trace: list[object] = []

                def wait(timeout: float) -> int:
                    trace.append(("wait", timeout))
                    if outcome == "timeout" and not any(
                        entry in {
                            ("signal", signal.SIGTERM),
                            ("signal", signal.SIGKILL),
                        }
                        for entry in trace
                    ):
                        raise subprocess.TimeoutExpired(("adapter",), 60)
                    return 9 if outcome == "timeout" else int(outcome)

                process.wait.side_effect = wait
                process.poll.side_effect = AssertionError(
                    "poll before identity-safe finalization"
                )
                process.communicate.side_effect = AssertionError(
                    "communicate before identity-safe finalization"
                )
                readiness = (
                    [False, False, True]
                    if outcome == "timeout"
                    else [True]
                )

                def pidfd_ready(
                    descriptor: int,
                    timeout: float,
                ) -> bool:
                    trace.append(("ready", descriptor, timeout))
                    return readiness.pop(0)

                def signal_group(pgid: int, signum: int) -> None:
                    self.assertNotIn("wait", [entry[0] for entry in trace if isinstance(entry, tuple)])
                    trace.append(("signal", signum))

                def members(
                    pgid: int,
                    leader_pid: int,
                    **_kwargs: object,
                ) -> tuple[int, ...]:
                    self.assertEqual(43210, pgid)
                    self.assertEqual(43210, leader_pid)
                    self.assertNotIn("wait", [entry[0] for entry in trace if isinstance(entry, tuple)])
                    trace.append(("members", pgid))
                    return ()

                with (
                    mock.patch.object(
                        runner.subprocess,
                        "Popen",
                        return_value=process,
                    ) as popen,
                    mock.patch.object(
                        runner.os,
                        "pidfd_open",
                        side_effect=lambda pid: trace.append(
                            ("pidfd-open", pid)
                        )
                        or 91,
                    ) as pidfd_open,
                    mock.patch.object(
                        runner,
                        "_pidfd_ready",
                        side_effect=pidfd_ready,
                        create=True,
                    ),
                    mock.patch.object(
                        runner,
                        "_same_pgid_members",
                        side_effect=members,
                        create=True,
                    ),
                    mock.patch.object(
                        runner.os,
                        "killpg",
                        side_effect=signal_group,
                    ) as killpg,
                    mock.patch.object(
                        runner,
                        "_wait_for_process_group_absence",
                        return_value=True,
                        create=True,
                    ),
                    mock.patch.object(
                        runner.os,
                        "close",
                        side_effect=lambda descriptor: trace.append(
                            ("close", descriptor)
                        ),
                    ) as close,
                ):
                    self.assertEqual(
                        expected,
                        runner._run_verified_child(
                            41,
                            item,
                            {"PATH": "/usr/bin"},
                        ),
                    )
                self.assertTrue(popen.call_args.kwargs["start_new_session"])
                self.assertEqual(
                    (41, 42, 43),
                    popen.call_args.kwargs["pass_fds"],
                )
                pidfd_open.assert_called_once_with(43210)
                process.poll.assert_not_called()
                process.communicate.assert_not_called()
                process.wait.assert_called_once_with(
                    timeout=runner._TERMINATION_GRACE_SECONDS
                )
                self.assertEqual(
                    [signal.SIGTERM]
                    if outcome != "timeout"
                    else [signal.SIGTERM, signal.SIGKILL],
                    [call.args[1] for call in killpg.call_args_list],
                )
                close.assert_called_once_with(91)
                wait_index = next(
                    index
                    for index, entry in enumerate(trace)
                    if isinstance(entry, tuple) and entry[0] == "wait"
                )
                for index, entry in enumerate(trace):
                    if (
                        isinstance(entry, tuple)
                        and entry[0] in {"signal", "members"}
                    ):
                        self.assertLess(index, wait_index)

        for kill_error, wait_error, expected_code in (
            (
                ProcessLookupError(),
                None,
                "ci-gate-runner-pidfd-acquisition",
            ),
            (
                PermissionError("private signal payload"),
                None,
                "ci-gate-runner-cleanup",
            ),
            (
                PermissionError("private signal payload"),
                subprocess.TimeoutExpired(("adapter",), 0.25),
                "ci-gate-runner-cleanup",
            ),
        ):
            with self.subTest(
                acquisition_kill=type(kill_error).__name__,
                acquisition_wait=type(wait_error).__name__,
            ):
                process = mock.Mock(pid=43210)
                process.wait.return_value = 0
                if wait_error is not None:
                    process.wait.side_effect = wait_error
                with (
                    mock.patch.object(
                        runner.subprocess,
                        "Popen",
                        return_value=process,
                    ),
                    mock.patch.object(
                        runner.os,
                        "pidfd_open",
                        side_effect=OSError("private pidfd payload"),
                    ),
                    mock.patch.object(
                        runner.os,
                        "killpg",
                        side_effect=kill_error,
                    ) as killpg,
                    mock.patch.object(
                        runner,
                        "_finalize_process_group",
                        return_value=None,
                    ),
                    mock.patch.object(runner.os, "close") as close,
                    self.assertRaises(
                        contract.GateContractError
                    ) as caught,
                ):
                    runner._run_verified_child(
                        41,
                        item,
                        {"PATH": "/usr/bin"},
                    )
                self.assertEqual(expected_code, caught.exception.code)
                self.assertNotIn("private", str(caught.exception))
                killpg.assert_called_once_with(43210, signal.SIGKILL)
                process.wait.assert_called_once_with(
                    timeout=runner._TERMINATION_GRACE_SECONDS
                )
                close.assert_not_called()

        for pidfd_error, expected_code in (
            (
                RuntimeError("private pidfd runtime payload"),
                "ci-gate-runner-cleanup",
            ),
            (
                KeyboardInterrupt("private pidfd interrupt"),
                None,
            ),
            (
                SystemExit("private pidfd exit"),
                None,
            ),
            (
                GeneratorExit("private pidfd generator"),
                None,
            ),
        ):
            with self.subTest(pidfd_error=type(pidfd_error).__name__):
                process = mock.Mock(pid=43210)
                trace: list[tuple[str, object]] = []

                def acquisition_wait(*, timeout: float) -> int:
                    trace.append(("wait", timeout))
                    return 0

                process.wait.side_effect = acquisition_wait

                def acquisition_signal(_pgid: int, signum: int) -> None:
                    self.assertFalse(
                        any(event[0] == "wait" for event in trace)
                    )
                    trace.append(("signal", signum))

                with (
                    mock.patch.object(
                        runner.subprocess,
                        "Popen",
                        return_value=process,
                    ),
                    mock.patch.object(
                        runner.os,
                        "pidfd_open",
                        side_effect=pidfd_error,
                    ),
                    mock.patch.object(
                        runner.os,
                        "killpg",
                        side_effect=acquisition_signal,
                    ) as killpg,
                    mock.patch.object(runner.os, "close") as close,
                ):
                    if expected_code is not None:
                        with self.assertRaises(
                            contract.GateContractError
                        ) as caught:
                            runner._run_verified_child(
                                41,
                                item,
                                {"PATH": "/usr/bin"},
                            )
                        self.assertEqual(expected_code, caught.exception.code)
                        self.assertNotIn("private", str(caught.exception))
                    else:
                        try:
                            runner._run_verified_child(
                                41,
                                item,
                                {"PATH": "/usr/bin"},
                            )
                        except BaseException as caught:
                            self.assertIs(pidfd_error, caught)
                        else:
                            self.fail(
                                "pidfd control-flow interruption was not re-raised"
                            )
                killpg.assert_called_once_with(43210, signal.SIGKILL)
                process.wait.assert_called_once_with(
                    timeout=runner._TERMINATION_GRACE_SECONDS
                )
                close.assert_not_called()

        process = mock.Mock(pid=43210)
        process.wait.side_effect = KeyboardInterrupt(
            "private acquisition wait interrupt"
        )
        with (
            mock.patch.object(
                runner.subprocess,
                "Popen",
                return_value=process,
            ),
            mock.patch.object(
                runner.os,
                "pidfd_open",
                side_effect=OSError("private pidfd payload"),
            ),
            mock.patch.object(runner.os, "killpg") as killpg,
            mock.patch.object(runner.os, "close") as close,
        ):
            observed_acquisition_error: BaseException | None = None
            try:
                runner._run_verified_child(
                    41,
                    item,
                    {"PATH": "/usr/bin"},
                )
            except BaseException as error:
                observed_acquisition_error = error
            else:
                self.fail("interrupted acquisition wait did not fail closed")
        self.assertIsInstance(
            observed_acquisition_error,
            contract.GateContractError,
        )
        self.assertEqual(
            "ci-gate-runner-cleanup",
            getattr(observed_acquisition_error, "code", None),
        )
        self.assertNotIn("private", str(observed_acquisition_error))
        killpg.assert_called_once_with(43210, signal.SIGKILL)
        process.wait.assert_called_once_with(
            timeout=runner._TERMINATION_GRACE_SECONDS
        )
        close.assert_not_called()

        def exercise_later_case(
            *,
            name: str,
            readiness: list[bool | BaseException],
            term_error: BaseException | None = None,
            kill_error: BaseException | None = None,
            member_effects: list[tuple[int, ...] | BaseException] | None = None,
            wait_error: BaseException | None = None,
            close_error: BaseException | None = None,
            expected_result: int | None = None,
            expected_code: str | None = None,
            expected_interruption: BaseException | None = None,
            expect_wait: bool = True,
        ) -> None:
            process = mock.Mock(pid=43210)
            process.poll.side_effect = AssertionError("forbidden poll")
            process.communicate.side_effect = AssertionError(
                "forbidden communicate"
            )
            member_queue = list(member_effects or [()])
            trace: list[tuple[str, object]] = []

            def wait(*, timeout: float) -> int:
                self.assertFalse(
                    any(entry[0] == "wait" for entry in trace),
                    "the bounded wait may begin only once",
                )
                trace.append(("wait", timeout))
                if wait_error is not None:
                    raise wait_error
                return 0

            process.wait.side_effect = wait

            def ready(_descriptor: int, _timeout: float) -> bool:
                self.assertFalse(
                    any(entry[0] == "wait" for entry in trace),
                    "pidfd readiness is forbidden after reap begins",
                )
                trace.append(("ready", _descriptor))
                effect = readiness.pop(0)
                if isinstance(effect, BaseException):
                    raise effect
                return effect

            def signal_group(_pgid: int, signum: int) -> None:
                self.assertFalse(
                    any(entry[0] == "wait" for entry in trace),
                    "numeric process-group signaling is forbidden after reap begins",
                )
                trace.append(("signal", signum))
                if signum == signal.SIGTERM and term_error is not None:
                    raise term_error
                if signum == signal.SIGKILL and kill_error is not None:
                    raise kill_error

            def members(
                _pgid: int,
                _leader_pid: int,
                **_kwargs: object,
            ) -> tuple[int, ...]:
                self.assertFalse(
                    any(entry[0] == "wait" for entry in trace),
                    "proc scanning is forbidden after reap begins",
                )
                effect = member_queue.pop(0)
                if isinstance(effect, BaseException):
                    raise effect
                return effect

            def close(_descriptor: int) -> None:
                trace.append(("close", 91))
                if close_error is not None:
                    raise close_error

            with (
                self.subTest(later_case=name),
                mock.patch.object(
                    runner.subprocess,
                    "Popen",
                    return_value=process,
                ),
                mock.patch.object(runner.os, "pidfd_open", return_value=91),
                mock.patch.object(
                    runner,
                    "_pidfd_ready",
                    side_effect=ready,
                    create=True,
                ),
                mock.patch.object(
                    runner,
                    "_same_pgid_members",
                    side_effect=members,
                    create=True,
                ),
                mock.patch.object(
                    runner.os,
                    "killpg",
                    side_effect=signal_group,
                ),
                mock.patch.object(
                    runner,
                    "_wait_for_process_group_absence",
                    return_value=True,
                    create=True,
                ),
                mock.patch.object(runner.os, "close", side_effect=close),
            ):
                if expected_interruption is not None:
                    try:
                        runner._run_verified_child(
                            41,
                            item,
                            {"PATH": "/usr/bin"},
                        )
                    except BaseException as caught:
                        self.assertIs(expected_interruption, caught)
                    else:
                        self.fail("control-flow interruption was not re-raised")
                elif expected_code is None:
                    self.assertEqual(
                        expected_result,
                        runner._run_verified_child(
                            41,
                            item,
                            {"PATH": "/usr/bin"},
                        ),
                    )
                else:
                    observed_failure: BaseException | None = None
                    try:
                        runner._run_verified_child(
                            41,
                            item,
                            {"PATH": "/usr/bin"},
                        )
                    except BaseException as error:
                        observed_failure = error
                    else:
                        self.fail("runner failure did not fail closed")
                    self.assertIsInstance(
                        observed_failure,
                        contract.GateContractError,
                    )
                    self.assertEqual(
                        expected_code,
                        getattr(observed_failure, "code", None),
                    )
                    self.assertNotIn("private", str(observed_failure))
            if expect_wait:
                process.wait.assert_called_once_with(
                    timeout=runner._TERMINATION_GRACE_SECONDS
                )
            else:
                process.wait.assert_not_called()
            process.poll.assert_not_called()
            process.communicate.assert_not_called()
            self.assertEqual(("close", 91), trace[-1])

        exercise_later_case(
            name="term-esrch",
            readiness=[True],
            term_error=ProcessLookupError(),
            expected_result=0,
        )
        exercise_later_case(
            name="kill-esrch",
            readiness=[False, False, True],
            kill_error=ProcessLookupError(),
            expected_result=124,
        )
        exercise_later_case(
            name="later-readiness-skips-wait",
            readiness=[
                True,
                contract.GateContractError(
                    "ci-gate-runner-pidfd-readiness",
                    "pidfd",
                    "the adapter leader readiness could not be observed",
                ),
            ],
            term_error=PermissionError("private TERM payload"),
            expected_code="ci-gate-runner-cleanup",
            expect_wait=False,
        )
        exercise_later_case(
            name="kill-failure-still-readies-reaps-and-closes",
            readiness=[False, False, True],
            kill_error=PermissionError("private KILL payload"),
            expected_code="ci-gate-runner-cleanup",
        )
        exercise_later_case(
            name="ready-wait-timeout-still-closes",
            readiness=[True],
            wait_error=subprocess.TimeoutExpired(("adapter",), 0.25),
            expected_code="ci-gate-runner-cleanup",
        )
        exercise_later_case(
            name="pidfd-close-overrides-product",
            readiness=[True],
            close_error=OSError("private close payload"),
            expected_code="ci-gate-runner-cleanup",
        )
        exercise_later_case(
            name="scan-error-recovers-before-reap",
            readiness=[True, True],
            member_effects=[
                contract.GateContractError(
                    "ci-gate-runner-proc-scan",
                    "proc",
                    "the process-group membership scan failed",
                )
            ],
            expected_code="ci-gate-runner-proc-scan",
        )
        exercise_later_case(
            name="ordinary-readiness-error-normalizes-after-cleanup",
            readiness=[
                RuntimeError("private readiness runtime payload"),
                True,
            ],
            expected_code="ci-gate-runner-cleanup",
        )
        term_interrupt = KeyboardInterrupt("private TERM interrupt")
        exercise_later_case(
            name="term-control-flow-recovers-and-reraises",
            readiness=[True, True],
            term_error=term_interrupt,
            expected_interruption=term_interrupt,
        )
        scan_interrupt = GeneratorExit("private scan interrupt")
        exercise_later_case(
            name="scan-control-flow-recovers-and-reraises",
            readiness=[True, True],
            member_effects=[scan_interrupt],
            expected_interruption=scan_interrupt,
        )
        exercise_later_case(
            name="recovery-readiness-interruption-is-cleanup",
            readiness=[
                True,
                SystemExit("private recovery readiness exit"),
            ],
            term_error=PermissionError("private TERM payload"),
            expected_code="ci-gate-runner-cleanup",
            expect_wait=False,
        )
        exercise_later_case(
            name="recovery-wait-interruption-still-closes",
            readiness=[True, True],
            term_error=PermissionError("private TERM payload"),
            wait_error=KeyboardInterrupt("private recovery wait interrupt"),
            expected_code="ci-gate-runner-cleanup",
        )
        exercise_later_case(
            name="reap-interruption-does-not-reenter-numeric-cleanup",
            readiness=[True],
            wait_error=GeneratorExit("private reap interrupt"),
            expected_code="ci-gate-runner-cleanup",
        )
        exercise_later_case(
            name="post-reap-close-interruption-is-cleanup",
            readiness=[True],
            close_error=SystemExit("private pidfd close exit"),
            expected_code="ci-gate-runner-cleanup",
        )

        scanner = getattr(runner, "_same_pgid_members", None)
        self.assertTrue(
            callable(scanner),
            "strict bounded proc scanner must be implemented",
        )
        with tempfile.TemporaryDirectory(dir=self.root) as proc_temporary:
            proc_root = pathlib.Path(proc_temporary)

            def write_stat(pid: int, pgrp: int, payload: bytes | None = None) -> None:
                directory = proc_root / str(pid)
                directory.mkdir()
                (directory / "stat").write_bytes(
                    payload
                    if payload is not None
                    else (
                        f"{pid} (worker ({pid})) S 1 {pgrp} 1 0 0 0\n"
                    ).encode("ascii")
                )

            write_stat(43210, 43210)
            write_stat(123, 43210)
            write_stat(124, 99999)
            (proc_root / "125").mkdir()
            (proc_root / "net").write_text("metadata", encoding="ascii")
            self.assertEqual(
                (123,),
                scanner(43210, 43210, proc_root=proc_root),
            )

        for malformed_name, payload in (
            ("malformed", b"private malformed payload"),
            ("oversized", b"x" * (4096 + 1)),
        ):
            with (
                self.subTest(proc_case=malformed_name),
                tempfile.TemporaryDirectory(dir=self.root) as proc_temporary,
            ):
                proc_root = pathlib.Path(proc_temporary)
                numeric = proc_root / "126"
                numeric.mkdir()
                (numeric / "stat").write_bytes(payload)
                with self.assertRaises(
                    contract.GateContractError
                ) as caught:
                    scanner(43210, 43210, proc_root=proc_root)
                self.assertEqual(
                    "ci-gate-runner-proc-scan",
                    caught.exception.code,
                )
                self.assertNotIn("private", str(caught.exception))

        with tempfile.TemporaryDirectory(dir=self.root) as proc_temporary:
            proc_root = pathlib.Path(proc_temporary)
            target = proc_root / "target"
            target.mkdir()
            (target / "stat").write_bytes(
                b"127 (worker) S 1 43210 1 0\n"
            )
            (proc_root / "127").symlink_to(target, target_is_directory=True)
            with self.assertRaises(contract.GateContractError) as caught:
                scanner(43210, 43210, proc_root=proc_root)
            self.assertEqual(
                "ci-gate-runner-proc-scan",
                caught.exception.code,
            )

        with tempfile.TemporaryDirectory(dir=self.root) as proc_temporary:
            proc_root = pathlib.Path(proc_temporary)
            real_open = os.open
            numeric = proc_root / "128"
            numeric.mkdir()
            (numeric / "stat").write_bytes(
                b"128 (worker) S 1 43210 1 0\n"
            )

            def deny_stat(
                path: str | pathlib.Path,
                flags: int,
                mode: int = 0o777,
                *,
                dir_fd: int | None = None,
            ) -> int:
                if path == "stat":
                    raise PermissionError("private permission payload")
                return real_open(path, flags, mode, dir_fd=dir_fd)

            with (
                mock.patch.object(runner.os, "open", side_effect=deny_stat),
                self.assertRaises(contract.GateContractError) as caught,
            ):
                scanner(43210, 43210, proc_root=proc_root)
            self.assertEqual(
                "ci-gate-runner-proc-scan",
                caught.exception.code,
            )
            self.assertNotIn("private", str(caught.exception))

        with tempfile.TemporaryDirectory(dir=self.root) as proc_temporary:
            proc_root = pathlib.Path(proc_temporary)
            numeric = proc_root / "129"
            numeric.mkdir()
            (numeric / "stat").write_bytes(
                b"129 (worker) S 1 43210 1 0\n"
            )
            real_read = os.read

            def fail_stat_read(descriptor: int, size: int) -> bytes:
                target = os.readlink(f"/proc/self/fd/{descriptor}")
                if target.endswith("/129/stat"):
                    raise OSError("private read payload")
                return real_read(descriptor, size)

            with (
                mock.patch.object(runner.os, "read", side_effect=fail_stat_read),
                self.assertRaises(contract.GateContractError) as caught,
            ):
                scanner(43210, 43210, proc_root=proc_root)
            self.assertEqual(
                "ci-gate-runner-proc-scan",
                caught.exception.code,
            )
            self.assertNotIn("private", str(caught.exception))

        for close_interruption in (
            KeyboardInterrupt("private stat close interrupt"),
            SystemExit("private stat close exit"),
            GeneratorExit("private stat close generator"),
        ):
            with self.subTest(
                proc_descriptor_close=type(close_interruption).__name__
            ):
                close_attempts: list[int] = []

                def open_proc_entry(
                    path: str | pathlib.Path,
                    _flags: int,
                    _mode: int = 0o777,
                    *,
                    dir_fd: int | None = None,
                ) -> int:
                    self.assertIn(path, {"130", "stat"})
                    self.assertIn(dir_fd, {77, 201})
                    return 201 if path == "130" else 202

                def close_proc_entry(descriptor: int) -> None:
                    close_attempts.append(descriptor)
                    if descriptor == 202:
                        raise close_interruption

                with (
                    mock.patch.object(
                        runner.os,
                        "open",
                        side_effect=open_proc_entry,
                    ),
                    mock.patch.object(
                        runner,
                        "_read_proc_stat",
                        return_value=b"130 (worker) S 1 43210 1 0\n",
                    ),
                    mock.patch.object(
                        runner.os,
                        "close",
                        side_effect=close_proc_entry,
                    ),
                ):
                    observed_close_error: BaseException | None = None
                    try:
                        runner._read_proc_entry_pgid(77, "130", 130)
                    except BaseException as error:
                        observed_close_error = error
                    else:
                        self.fail("proc descriptor cleanup did not fail closed")
                self.assertIsInstance(
                    observed_close_error,
                    contract.GateContractError,
                )
                self.assertEqual(
                    "ci-gate-runner-cleanup",
                    getattr(observed_close_error, "code", None),
                )
                self.assertNotIn("private", str(observed_close_error))
                self.assertEqual([202, 201], close_attempts)

        with tempfile.TemporaryDirectory(dir=self.root) as proc_temporary:
            proc_root = pathlib.Path(proc_temporary)
            real_open = os.open
            real_close = os.close
            proc_descriptors: list[int] = []
            close_attempts: list[int] = []
            scan_interrupt = KeyboardInterrupt("private scandir interrupt")

            def open_proc_root(*args: object, **kwargs: object) -> int:
                descriptor = real_open(*args, **kwargs)  # type: ignore[arg-type]
                proc_descriptors.append(descriptor)
                return descriptor

            def close_proc_root(descriptor: int) -> None:
                close_attempts.append(descriptor)
                real_close(descriptor)

            try:
                with (
                    mock.patch.object(
                        runner.os,
                        "open",
                        side_effect=open_proc_root,
                    ),
                    mock.patch.object(
                        runner.os,
                        "scandir",
                        side_effect=scan_interrupt,
                    ),
                    mock.patch.object(
                        runner.os,
                        "close",
                        side_effect=close_proc_root,
                    ),
                ):
                    try:
                        scanner(43210, 43210, proc_root=proc_root)
                    except BaseException as caught:
                        self.assertIs(scan_interrupt, caught)
                    else:
                        self.fail("scandir interruption was not re-raised")
            finally:
                for descriptor in proc_descriptors:
                    try:
                        real_close(descriptor)
                    except OSError:
                        pass
            self.assertEqual(proc_descriptors, close_attempts)

        with tempfile.TemporaryDirectory(dir=self.root) as proc_temporary:
            proc_root = pathlib.Path(proc_temporary)
            real_close = os.close
            close_attempts: list[int] = []

            def interrupt_proc_root_close(descriptor: int) -> None:
                close_attempts.append(descriptor)
                real_close(descriptor)
                raise GeneratorExit("private proc root close interrupt")

            with (
                mock.patch.object(
                    runner.os,
                    "close",
                    side_effect=interrupt_proc_root_close,
                ),
            ):
                observed_close_error: BaseException | None = None
                try:
                    scanner(43210, 43210, proc_root=proc_root)
                except BaseException as error:
                    observed_close_error = error
                else:
                    self.fail("proc-root cleanup did not fail closed")
            self.assertIsInstance(
                observed_close_error,
                contract.GateContractError,
            )
            self.assertEqual(
                "ci-gate-runner-cleanup",
                getattr(observed_close_error, "code", None),
            )
            self.assertNotIn("private", str(observed_close_error))
            self.assertEqual(1, len(close_attempts))

        with tempfile.TemporaryDirectory(dir=self.root) as proc_temporary:
            proc_root = pathlib.Path(proc_temporary)

            class FakeEntry:
                def __init__(self, name: str) -> None:
                    self.name = name

            class FakeScandir:
                def __enter__(self):
                    return (
                        FakeEntry(str(pid))
                        for pid in range(
                            getattr(runner, "_MAX_PROC_PID_ENTRIES", 65536)
                            + 1
                        )
                    )

                def __exit__(self, *_args: object) -> None:
                    return None

            with (
                mock.patch.object(
                    runner.os,
                    "scandir",
                    return_value=FakeScandir(),
                ),
                self.assertRaises(contract.GateContractError) as caught,
            ):
                scanner(43210, 43210, proc_root=proc_root)
            self.assertEqual(
                "ci-gate-runner-proc-scan",
                caught.exception.code,
            )

        with tempfile.TemporaryDirectory(dir=self.root) as proc_temporary:
            target = pathlib.Path(proc_temporary)
            proc_link = self.root / "proc-link"
            proc_link.symlink_to(target, target_is_directory=True)
            try:
                with self.assertRaises(
                    contract.GateContractError
                ) as caught:
                    scanner(43210, 43210, proc_root=proc_link)
                self.assertEqual(
                    "ci-gate-runner-proc-scan",
                    caught.exception.code,
                )
            finally:
                proc_link.unlink()

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

        transient_attempts = 0

        def transient_rmtree(path: pathlib.Path) -> None:
            nonlocal transient_attempts
            transient_attempts += 1
            if transient_attempts < 2:
                raise PermissionError("private transient cleanup path")
            REAL_SHUTIL_RMTREE(path)

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
                    side_effect=transient_rmtree,
                ),
                mock.patch.object(runner.time, "sleep") as sleep,
            ):
                self.assertEqual(
                    0,
                    runner.execute_execution_plan(
                        self.root,
                        (),
                        {"PATH": "/usr/bin"},
                        executor=lambda _invocation: 0,
                    ),
                )
            self.assertEqual(2, transient_attempts)
            sleep.assert_called_once_with(0.05)

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
                ) as rmtree,
                mock.patch.object(runner.time, "sleep") as sleep,
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
            self.assertEqual(3, rmtree.call_count)
            self.assertEqual(
                [mock.call(0.05), mock.call(0.05)],
                sleep.call_args_list,
            )
        finally:
            if home.exists():
                shutil.rmtree(home)


if __name__ == "__main__":
    unittest.main()
