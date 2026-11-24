"""Boundary consumers for the existing dispatcher's gated shell profile."""

import fcntl
import json
import os
import signal
import socket
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from scripts.lib.ops import dispatch_process as execution
from scripts.lib.ops.environment_admission import Admission


class EgressBoundaryTests(unittest.TestCase):
    def test_an_egress_limited_provider_runs_inside_pasta_with_private_ranges_cut(self):
        with tempfile.TemporaryDirectory() as folder:
            command, _ = execution._bounded_command(
                ["codex", "exec"], "a" * 32,
                {"cpus": 0.3, "memory_bytes": 2**30, "disk_bytes": 2**30,
                 "runtime_seconds": 60},
                cwd=folder, env={},
                provider={"binds": [], "env": {}, "share_net": True,
                          "egress": "public", "dns": "8.8.8.8"},
            )  # fmt: skip
        pasta = command.index("/usr/bin/pasta")
        for flag in ("--config-net", "--no-map-gw", "-4"):
            self.assertIn(flag, command[pasta:])
        for option in ("-T", "-U", "-t", "-u"):
            self.assertEqual("none", command[command.index(option, pasta) + 1])
        self.assertEqual("198.18.0.1", command[command.index("-g", pasta) + 1])
        script = command[command.index("-c", pasta) + 1]
        for net in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16",
                    "100.64.0.0/10", "169.254.0.0/16"):  # fmt: skip
            self.assertIn(net, script)
        self.assertIn("unreachable", script)
        self.assertEqual("8.8.8.8", command[command.index("-c", pasta) + 3])
        bwrap = command.index("/usr/bin/bwrap")
        self.assertLess(pasta, bwrap)
        self.assertIn("--share-net", command[bwrap:])
        data = command.index("--ro-bind-data", bwrap)
        self.assertEqual(["3", "/etc/resolv.conf"], command[data + 1 : data + 3])

    def test_an_invalid_resolver_is_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                execution._bounded_command(
                    ["codex"], "a" * 32,
                    {"cpus": 0.3, "memory_bytes": 2**30, "disk_bytes": 2**30,
                     "runtime_seconds": 60},
                    cwd=folder, env={},
                    provider={"binds": [], "env": {}, "share_net": True,
                              "egress": "public", "dns": "8.8.8.8; id"},
                )  # fmt: skip


class DispatchProcessTests(unittest.TestCase):
    def test_controller_does_not_forward_unselected_environment_secrets(self):
        found = execution._controller_environment(
            {
                "HOME": "/example",
                "HY_TASK": "TSK-test",
                "HY_FENCE": "{}",
                "AWS_SECRET_ACCESS_KEY": "synthetic-test-value",
                "API_TOKEN": "dummy",
                "PYTHONPATH": "/unexpected",
                "PATH": "/unexpected",
            }
        )
        self.assertEqual(
            {
                "HOME": "/example",
                "HY_TASK": "TSK-test",
                "HY_FENCE": "{}",
                "PATH": "/usr/bin:/bin",
                "LC_ALL": "C.UTF-8",
                "XDG_RUNTIME_DIR": f"/run/user/{os.getuid()}",
                "DBUS_SESSION_BUS_ADDRESS": f"unix:path=/run/user/{os.getuid()}/bus",
            },
            found,
        )

    def test_invalid_or_unbounded_profiles_are_refused(self):
        for value in (
            {"cpus": float("nan")},
            {"cpus": float("inf")},
            {"memory_bytes": 0},
            {"disk_bytes": -1},
            {"runtime_seconds": 601},
            {"unrecognized": 1},
            {"cpus": True},
        ):
            with self.subTest(value=value):
                with self.assertRaises(execution.ProcessError):
                    execution._budget(value, 10)
        with self.assertRaises(execution.ProcessError):
            execution._budget({"runtime_seconds": 2}, 3)

    def test_foreign_scope_name_is_never_queried_or_stopped(self):
        with mock.patch.object(execution.subprocess, "run") as run:
            self.assertFalse(execution._scope_absent("other.scope", "token", stop=True))
        run.assert_not_called()

    def test_scope_owner_mismatch_prevents_stop(self):
        status = subprocess.CompletedProcess(
            [],
            0,
            stdout=("LoadState=loaded\nActiveState=active\nDescription=someone-else\n"),
        )
        with mock.patch.object(execution.subprocess, "run", return_value=status) as run:
            self.assertFalse(
                execution._scope_absent(
                    "hy-home-worker-token.scope", "token", stop=True
                )
            )
        self.assertEqual(1, run.call_count)
        self.assertIn("show", run.call_args.args[0])

    def test_unknown_manager_state_is_not_absence(self):
        status = subprocess.CompletedProcess([], 1, stdout="")
        with mock.patch.object(execution.subprocess, "run", return_value=status):
            self.assertFalse(
                execution._scope_absent(
                    "hy-home-worker-token.scope", "token", stop=True
                )
            )

    def test_missing_owned_scope_is_verified_absent(self):
        status = subprocess.CompletedProcess([], 0, stdout="LoadState=not-found\n")
        with mock.patch.object(execution.subprocess, "run", return_value=status) as run:
            self.assertTrue(
                execution._scope_absent(
                    "hy-home-worker-token.scope", "token", stop=True
                )
            )
        self.assertEqual(1, run.call_count)

    def test_owned_scope_stops_before_successful_absence_result(self):
        active = (
            "LoadState=loaded\nActiveState=active\nDescription=hy-home-worker:token\n"
        )
        inactive = active.replace("ActiveState=active", "ActiveState=inactive")
        results = [
            subprocess.CompletedProcess([], 0, stdout=active),
            subprocess.CompletedProcess([], 0),
            subprocess.CompletedProcess([], 0, stdout=inactive),
        ]
        with mock.patch.object(execution.subprocess, "run", side_effect=results) as run:
            self.assertTrue(
                execution._scope_absent(
                    "hy-home-worker-token.scope", "token", stop=True
                )
            )
        self.assertEqual("stop", run.call_args_list[1].args[0][2])


class DiskBoundaryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.owned = self.root / "owned"
        self.owned.mkdir()

    def test_usage_counts_owned_files_without_following_external_symlinks(self):
        outside = self.root / "outside"
        outside.write_bytes(b"x" * 10000)
        (self.owned / "link").symlink_to(outside)
        (self.owned / "small").write_bytes(b"x")
        self.assertIsNone(execution._disk_problem((self.owned,), 1024))
        (self.owned / "large").write_bytes(b"x" * 2000)
        self.assertEqual(
            "disk budget exceeded", execution._disk_problem((self.owned,), 1024)
        )

    def test_unknown_usage_and_unsupported_objects_fail_closed(self):
        self.assertEqual(
            "owned disk usage unavailable",
            execution._disk_problem((self.root / "missing",), 1024),
        )
        os.mkfifo(self.owned / "pipe")
        self.assertEqual(
            "unsupported owned disk object",
            execution._disk_problem((self.owned,), 1024),
        )

    def test_host_headroom_failure_is_not_free_space(self):
        space = mock.Mock(f_bavail=0, f_frsize=4096, f_blocks=1000)
        with mock.patch.object(execution.os, "fstatvfs", return_value=space):
            self.assertEqual(
                "host disk headroom below10percent",
                execution._disk_problem((self.owned,), 1024),
            )


class SpawnFailureTests(unittest.TestCase):
    def test_popen_failure_releases_only_an_absent_owned_worker_reservation(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        budget = {
            "cpus": 1,
            "memory_bytes": 1024**2,
            "disk_bytes": 1024**2,
            "runtime_seconds": 60,
        }
        admission = Admission(
            root / "admission",
            namespace="host",
            workspace_id="repo",
            inventory=["one"],
            limits={
                "cpus": 2,
                "memory_bytes": 2 * 1024**2,
                "disk_bytes": 2 * 1024**2,
                "runtime_seconds": 120,
            },
        )
        reservation = admission.admit(kind="worker", budget=budget)
        process_file = root / "unit.process.json"
        scope = "hy-home-worker-" + reservation["token"] + ".scope"
        with (
            mock.patch.object(
                execution,
                "_bounded_command",
                return_value=(["/usr/bin/true"], scope),
            ),
            mock.patch.object(
                execution.subprocess, "Popen", side_effect=OSError("spawn refused")
            ),
            mock.patch.object(execution, "_scope_absent", return_value=True) as absent,
        ):
            with self.assertRaisesRegex(OSError, "spawn refused"):
                execution._spawn(
                    ["/usr/bin/true"],
                    root=root,
                    name="unit",
                    cwd=root,
                    env={},
                    stdout=subprocess.DEVNULL,
                    admission=admission,
                    budget=budget,
                    kind="worker",
                    reservation=reservation,
                )
        absent.assert_called_once_with(scope, reservation["token"], stop=True)
        self.assertEqual([], admission.records())
        self.assertFalse(process_file.exists())

    def test_intent_write_failure_releases_only_an_absent_owned_reservation(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        budget = {
            "cpus": 1,
            "memory_bytes": 1024**2,
            "disk_bytes": 1024**2,
            "runtime_seconds": 60,
        }
        admission = Admission(
            root / "admission",
            namespace="host",
            workspace_id="repo",
            inventory=["one"],
            limits={
                "cpus": 2,
                "memory_bytes": 2 * 1024**2,
                "disk_bytes": 2 * 1024**2,
                "runtime_seconds": 120,
            },
        )
        reservation = admission.admit(kind="worker", budget=budget)
        scope = "hy-home-worker-" + reservation["token"] + ".scope"
        with (
            mock.patch.object(
                execution,
                "_bounded_command",
                return_value=(["/usr/bin/true"], scope),
            ),
            mock.patch.object(
                execution, "_write_record", side_effect=OSError("disk full")
            ),
            mock.patch.object(execution, "_scope_absent", return_value=True) as absent,
            mock.patch.object(execution.subprocess, "Popen") as spawn,
        ):
            with self.assertRaisesRegex(OSError, "disk full"):
                execution._spawn(
                    ["/usr/bin/true"],
                    root=root,
                    name="unit",
                    cwd=root,
                    env={},
                    stdout=subprocess.DEVNULL,
                    admission=admission,
                    budget=budget,
                    kind="worker",
                    reservation=reservation,
                )
        absent.assert_called_once_with(scope, reservation["token"], stop=True)
        spawn.assert_not_called()
        self.assertEqual([], admission.records())


class RegisteredDockerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.store = Admission(
            self.root / "admission",
            namespace="host",
            workspace_id="repo",
            inventory=["one", "two"],
            limits={
                "cpus": 8,
                "memory_bytes": 8 * 1024**3,
                "disk_bytes": 8 * 1024**3,
                "runtime_seconds": 600,
            },
        )
        self.claim = self.store.admit(
            kind="lab",
            project="hy-home-lab-case",
            budget={
                "cpus": 2,
                "memory_bytes": 1024**3,
                "disk_bytes": 1024**3,
                "runtime_seconds": 60,
            },
        )
        self.directory = execution.prepare_registered_docker(
            self.store, self.claim["token"]
        )
        self.record = self.store.records()[0]
        self.argv = [
            "/usr/bin/docker",
            "--host",
            "unix:///var/run/docker.sock",
            "compose",
            "--project-name",
            "hy-home-lab-case",
            "up",
            "-d",
            "case",
        ]

    def test_only_local_generated_lifecycle_commands_enter_trusted_lane(self):
        for command in (
            ["sh", "-c", "true"],
            ["/usr/bin/docker", "run", "alpine"],
            [*self.argv[:4], "exec", "case", "sh"],
            [*self.argv[:4], "run", "case"],
            ["/usr/bin/docker", "--host", "tcp://example:2375", *self.argv[3:]],
        ):
            with self.subTest(command=command):
                with self.assertRaises(execution.ProcessError):
                    execution.run_registered_docker(
                        command,
                        cwd=self.root,
                        timeout=10,
                        admission=self.store,
                        token=self.claim["token"],
                    )
        self.assertEqual(
            "prepared",
            json.loads((self.directory / "operation.json").read_text())["state"],
        )

    def test_prepared_operation_is_absent_but_lost_journal_is_unknown(self):
        self.assertTrue(execution.verify_registered_docker_absent(self.record))
        (self.directory / "operation.json").unlink()
        self.assertFalse(execution.verify_registered_docker_absent(self.record))

    def test_unstarted_intent_cleanup_requires_proven_absent_owned_scope(self):
        token = "d" * 32
        execution._write_record(
            self.directory / "operation.json",
            {
                "claim_token": self.claim["token"],
                "operation_token": token,
                "state": "intent",
            },
        )
        with (
            mock.patch.object(execution, "process_status", return_value="absent"),
            mock.patch.object(execution, "_scope_absent", return_value=False) as scope,
        ):
            self.assertFalse(execution.cleanup_unstarted_registered_docker(self.record))
            scope.assert_called_once_with("hy-home-worker-" + token + ".scope", token)
        self.assertTrue((self.directory / "operation.json").exists())
        with (
            mock.patch.object(execution, "process_status", return_value="absent"),
            mock.patch.object(execution, "_scope_absent", return_value=True),
        ):
            self.assertTrue(execution.cleanup_unstarted_registered_docker(self.record))
        self.assertFalse(self.directory.exists())

    def test_concurrent_operation_cannot_overwrite_the_current_journal(self):
        original = (self.directory / "operation.json").read_bytes()
        with open(self.directory / "operation.lock", "rb") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            with self.assertRaisesRegex(execution.ProcessError, "already active"):
                execution.run_registered_docker(
                    self.argv,
                    cwd=self.root,
                    timeout=10,
                    admission=self.store,
                    token=self.claim["token"],
                )
        self.assertEqual(original, (self.directory / "operation.json").read_bytes())

    def test_existing_claim_recovery_operation_never_rewrites_the_database(self):
        def scope(command, token, budget):
            return ["/usr/bin/true"], "hy-home-worker-" + token + ".scope"

        with (
            mock.patch.object(execution, "_scope_command", side_effect=scope),
            mock.patch.object(execution, "_scope_absent", return_value=True),
            mock.patch.object(
                self.store, "update", side_effect=AssertionError("recovery write")
            ),
            mock.patch.object(
                self.store, "admit", side_effect=AssertionError("recovery admit")
            ),
        ):
            result = execution.run_registered_docker(
                self.argv,
                cwd=self.root,
                timeout=10,
                admission=self.store,
                token=self.claim["token"],
            )
            self.assertEqual(0, result.returncode)
            self.assertTrue(execution.verify_registered_docker_absent(self.record))
            self.assertEqual(
                1,
                len(self.store.records()),
                "controller must not release container claim",
            )
            self.assertTrue(
                self.store.release(self.claim["token"], verify=lambda _: True)
            )
            self.assertTrue(execution.cleanup_registered_docker(self.record))
        self.assertFalse(self.directory.exists())

    def test_lab_receives_a_bounded_structured_controller_failure(self):
        from scripts.operations import lab

        def scope(command, token, budget):
            return [
                "/usr/bin/python3",
                "-c",
                "import sys;sys.stderr.write('SYNTHETIC_OUTPUT_SENTINEL'*1000);sys.exit(7)",
            ], "hy-home-worker-" + token + ".scope"

        with (
            mock.patch.object(execution, "_scope_command", side_effect=scope),
            mock.patch.object(execution, "_scope_absent", return_value=True),
        ):
            result = lab.run(
                [
                    "/usr/bin/docker",
                    "compose",
                    "--project-name",
                    "hy-home-lab-case",
                    "up",
                    "-d",
                    "case",
                ],
                timeout=10,
                admission=self.store,
                token=self.claim["token"],
            )
        self.assertEqual(7, result.returncode)
        self.assertTrue(
            result.stderr.strip(), "LAB failure lost the controller diagnostic"
        )
        self.assertIn("up", result.stderr)
        self.assertIn("7", result.stderr)
        self.assertLessEqual(len(result.stderr.encode()), 128)
        self.assertNotIn("SYNTHETIC_OUTPUT_SENTINEL", result.stderr)
        self.assertEqual("", result.stdout)

    def test_wrong_compose_project_cannot_reach_the_registered_spawn(self):
        command = list(self.argv)
        command[5] = "hy-home-lab-foreign"
        before = (self.directory / "operation.json").read_bytes()
        with mock.patch.object(
            execution,
            "_spawn",
            side_effect=AssertionError("foreign project reached spawn"),
        ):
            with self.assertRaisesRegex(execution.ProcessError, "project"):
                execution.run_registered_docker(
                    command,
                    cwd=self.root,
                    timeout=10,
                    admission=self.store,
                    token=self.claim["token"],
                )
        self.assertEqual(before, (self.directory / "operation.json").read_bytes())

    def test_repeated_preparation_does_not_recreate_lost_operation_proof(self):
        (self.directory / "operation.json").unlink()
        with self.assertRaises(execution.ProcessError):
            execution.prepare_registered_docker(self.store, self.claim["token"])
        self.assertFalse((self.directory / "operation.json").exists())

    def test_timed_out_controller_is_reaped_without_releasing_container_claim(self):
        def scope(command, token, budget):
            return ["/usr/bin/sleep", "30"], "hy-home-worker-" + token + ".scope"

        with (
            mock.patch.object(execution, "_scope_command", side_effect=scope),
            mock.patch.object(execution, "_scope_absent", return_value=True),
        ):
            result = execution.run_registered_docker(
                self.argv,
                cwd=self.root,
                timeout=0.1,
                admission=self.store,
                token=self.claim["token"],
            )
            self.assertEqual(124, result.returncode)
            self.assertTrue(execution.verify_registered_docker_absent(self.record))
            self.assertEqual(1, len(self.store.records()))

    def test_cancelled_controller_is_reaped_before_cancellation_propagates(self):
        original_spawn = execution._spawn

        def spawn(*args, **kwargs):
            job = original_spawn(*args, **kwargs)
            wait = job["process"].wait
            calls = [False]

            def interrupt_once(*a, **kw):
                if not calls[0]:
                    calls[0] = True
                    raise KeyboardInterrupt
                return wait(*a, **kw)

            job["process"].wait = interrupt_once
            return job

        def scope(command, token, budget):
            return ["/usr/bin/sleep", "30"], "hy-home-worker-" + token + ".scope"

        with (
            mock.patch.object(execution, "_scope_command", side_effect=scope),
            mock.patch.object(execution, "_scope_absent", return_value=True),
            mock.patch.object(execution, "_spawn", side_effect=spawn),
        ):
            with self.assertRaises(KeyboardInterrupt):
                execution.run_registered_docker(
                    self.argv,
                    cwd=self.root,
                    timeout=10,
                    admission=self.store,
                    token=self.claim["token"],
                )
            self.assertTrue(execution.verify_registered_docker_absent(self.record))
            self.assertEqual(1, len(self.store.records()))

    def test_foreign_claim_and_unknown_operation_are_not_cleaned(self):
        foreign = {**self.record, "token": "different-token"}
        self.assertFalse(execution.verify_registered_docker_absent(foreign, stop=True))
        self.assertFalse(execution.cleanup_registered_docker(foreign))
        (self.directory / "unowned-file").write_text("preserve")
        self.assertFalse(execution.cleanup_registered_docker(self.record))
        self.assertTrue((self.directory / "unowned-file").exists())


class BootstrapTests(unittest.TestCase):
    def case(self, command=None):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / "process.json"
        path.write_text(json.dumps({"token": "case", "scope": None, "state": "intent"}))
        control_r, control_w = os.pipe()
        ack_r, ack_w = os.pipe()
        self.addCleanup(os.close, ack_r)
        if command is not None:
            os.write(control_w, json.dumps(command).encode() + b"\n")
        os.close(control_w)
        return path, control_r, ack_w

    def test_closed_release_gate_executes_no_command(self):
        path, control, ack = self.case()
        with mock.patch.object(execution.subprocess, "Popen") as spawn:
            self.assertEqual(125, execution._bootstrap(path, control, ack))
        spawn.assert_not_called()
        self.assertEqual("ready", json.loads(path.read_text())["state"])

    def test_invalid_release_command_is_refused(self):
        path, control, ack = self.case([])
        with mock.patch.object(execution.subprocess, "Popen") as spawn:
            self.assertEqual(125, execution._bootstrap(path, control, ack))
        spawn.assert_not_called()

    def test_parent_death_stops_owned_scope_and_group(self):
        path, control, ack = self.case(["true"])
        child = mock.Mock()
        child.poll.return_value = None
        with (
            mock.patch.object(execution.subprocess, "Popen", return_value=child),
            mock.patch.object(execution, "_scope_absent", return_value=True) as stop,
            mock.patch.object(
                execution.os, "killpg", side_effect=SystemExit("owned stop")
            ) as kill,
        ):
            with self.assertRaisesRegex(SystemExit, "owned stop"):
                execution._bootstrap(path, control, ack)
        stop.assert_called_once_with(None, "case", stop=True)
        kill.assert_called_once_with(os.getpgrp(), signal.SIGKILL)

    def test_success_preserves_command_status_and_removes_background_children(self):
        path, control, ack = self.case(["true"])
        child = mock.Mock(returncode=7)
        child.poll.return_value = 7
        descriptor = os.open("/dev/null", os.O_RDONLY)
        candidate = mock.Mock(name="candidate")
        candidate.name = "1234567"
        with (
            mock.patch.object(execution.subprocess, "Popen", return_value=child),
            mock.patch.object(execution.Path, "iterdir", return_value=[candidate]),
            mock.patch.object(execution.os, "pidfd_open", return_value=descriptor),
            mock.patch.object(execution.os, "getpgid", return_value=os.getpgrp()),
            mock.patch.object(execution.signal, "pidfd_send_signal") as kill,
        ):
            self.assertEqual(7, execution._bootstrap(path, control, ack))
        kill.assert_called_once_with(descriptor, signal.SIGKILL)


@unittest.skipUnless(
    os.environ.get("HYHOME_INTEGRATION") == "1",
    "requires approved host user-manager/bwrap observation",
)
class NativeShellBoundaryTests(unittest.TestCase):
    def test_actual_selected_shell_boundary_and_owned_cleanup(self):
        from scripts.operations import lab

        temporary = tempfile.TemporaryDirectory(prefix="p07-shell-boundary-")
        verified = {"closed": True}

        def cleanup_fixture():
            if verified["closed"]:
                temporary.cleanup()
            else:
                temporary._finalizer.detach()  # Preserve an unknown live mount for owned recovery.

        self.addCleanup(cleanup_fixture)
        case = Path(temporary.name)
        tree = case / "worktree"
        tree.mkdir()
        outside = case / "outside"
        outside.mkdir()
        (outside / "protected").write_text("synthetic-only")
        listener = socket.socket(socket.AF_UNIX)
        self.addCleanup(listener.close)
        listener.bind(str(outside / "dummy-docker.sock"))
        listener.listen(1)
        network = socket.socket()
        self.addCleanup(network.close)
        network.bind(("127.0.0.1", 0))
        network.listen(1)
        (tree / "normal").write_text("public-input")
        git_environment = {
            "PATH": "/usr/bin:/bin",
            "HOME": "/nonexistent",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null",
        }

        def git(*args, input=None):
            return subprocess.run(
                ["git", "-C", str(tree), *args],
                env=git_environment,
                input=input,
                capture_output=True,
                check=True,
            ).stdout

        git("init", "-q")
        git(
            "-c",
            "user.name=test",
            "-c",
            "user.email=test@example.invalid",
            "add",
            "normal",
        )
        git(
            "-c",
            "user.name=test",
            "-c",
            "user.email=test@example.invalid",
            "commit",
            "-qm",
            "fixture",
        )
        gitdir = git("rev-parse", "--absolute-git-dir").decode().strip()
        base = git("rev-parse", "HEAD").decode().strip()
        budget = execution._budget(None, 20)
        projection = execution._git_view(
            gitdir, tree, base, case / "git-view", budget["disk_bytes"]
        )
        source = (
            "import json,os,pathlib,socket,subprocess,time\n"
            "p=pathlib.Path\nresult={'read':p('normal').read_text()=='public-input'}\n"
            "p('allowed').write_text('owned-write')\n"
            "result['git']=subprocess.run(['git','status','--porcelain'],capture_output=True,text=True,check=True).stdout\n"
            "result['secret_environment_absent']='SYNTHETIC_SECRET_TOKEN' not in os.environ\n"
            "targets="
            + repr([str(outside / "protected"), str(outside / "dummy-docker.sock")])
            + "\n"
            "for name,mode in [('outside_read','r'),('outside_write','w')]:\n"
            " try:\n  open(targets[0],mode).close();result[name]=False\n"
            " except OSError:result[name]=True\n"
            "try:\n s=socket.socket(socket.AF_UNIX);s.connect(targets[1]);result['socket']=False\n"
            "except OSError:result['socket']=True\n"
            "try:\n s=socket.socket();s.settimeout(.2);s.connect(('127.0.0.1',"
            + str(network.getsockname()[1])
            + "));result['network']=False\n"
            "except OSError:result['network']=True\n"
            "p('result.json').write_text(json.dumps(result));p('ready').touch()\n"
            "end=time.monotonic()+8\n"
            "while not p('release').exists() and time.monotonic()<end:time.sleep(.02)\n"
        )
        # Real host admission and current complete inventory, without starting a product service.
        store = lab.execution_admission(Path(__file__).resolve().parents[3])
        verified["closed"] = False
        with open(case / "output.log", "wb") as output:
            job = execution._spawn(
                ["/usr/bin/python3", "-c", source],
                root=case,
                name="probe",
                cwd=tree,
                env={**os.environ, "SYNTHETIC_SECRET_TOKEN": "dummy"},
                stdout=output,
                admission=store,
                budget=budget,
                kind="worker",
                git_view=projection,
                disk_paths=(tree, projection, case / "output.log"),
            )
        try:
            deadline = time.monotonic() + 8
            while not (tree / "ready").exists():
                self.assertLess(time.monotonic(), deadline)
                self.assertIsNone(
                    job["process"].poll(), (case / "output.log").read_text()
                )
                time.sleep(0.02)
            result = json.loads((tree / "result.json").read_text())
            self.assertEqual("owned-write", (tree / "allowed").read_text())
            self.assertIn("allowed", result.pop("git"))
            self.assertTrue(all(result.values()), result)
            self.assertEqual("synthetic-only", (outside / "protected").read_text())
            observed = subprocess.run(
                [
                    "/usr/bin/systemctl",
                    "--user",
                    "show",
                    job["scope"],
                    "--property=MemoryMax,TasksMax,CPUQuotaPerSecUSec,RuntimeMaxUSec,ControlGroup",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            properties = dict(
                line.split("=", 1) for line in observed.stdout.splitlines()
            )
            self.assertEqual(str(budget["memory_bytes"]), properties["MemoryMax"])
            self.assertEqual("256", properties["TasksMax"])
            self.assertEqual("1s", properties["CPUQuotaPerSecUSec"])
            self.assertEqual("20s", properties["RuntimeMaxUSec"])
            self.assertTrue(properties["ControlGroup"])
            (tree / "release").touch()
            self.assertEqual(0, job["process"].wait(timeout=5))
        finally:
            if job["process"].returncode is None:
                execution._kill(job["process"])
            verified["closed"] = execution._finish_environment(job, store)
            self.assertTrue(verified["closed"])
        self.assertFalse(
            any(row["token"] == job["environment_token"] for row in store.records())
        )


if __name__ == "__main__":
    unittest.main()
