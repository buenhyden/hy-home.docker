# fmt: off
import hashlib
import importlib.util
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "infra/03-security/openbao/scripts/protected-semantic-execution.py"


def load_source():
    spec = importlib.util.spec_from_file_location("protected_semantic_execution", SOURCE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class HeldBytesTests(unittest.TestCase):
    def setUp(self):
        self.subject = load_source()
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)

    def tearDown(self):
        self.directory.cleanup()

    def held(self, raw=b"reviewed"):
        path = self.root / "input"
        path.write_bytes(raw)
        path.chmod(0o600)
        digest = hashlib.sha256(raw).hexdigest()
        return path, self.subject.HeldBytes.open(path, digest, maximum=1024, private=True)

    def test_captures_once_and_rejects_same_inode_mutation(self):
        path, held = self.held()
        self.addCleanup(held.close)
        self.assertEqual(held.raw, b"reviewed")
        descriptor = os.open(path, os.O_WRONLY)
        os.pwrite(descriptor, b"MUTATED!", 0)
        os.close(descriptor)
        self.assertEqual(held.raw, b"reviewed")
        with self.assertRaises(self.subject.CustodyError):
            held.revalidate()

    def test_replacement_never_changes_captured_bytes_or_materialized_copy(self):
        path, held = self.held()
        self.addCleanup(held.close)
        replacement = self.root / "replacement"
        replacement.write_bytes(b"evil-byte")
        replacement.chmod(0o600)
        replacement.replace(path)
        with self.assertRaises(self.subject.CustodyError):
            held.revalidate()
        destination = self.root / "private"
        destination.mkdir(mode=0o700)
        output = held.materialize(destination, "helper", 0o500)
        self.assertEqual(output.read_bytes(), b"reviewed")
        self.assertEqual(output.stat().st_mode & 0o777, 0o500)

    def test_rejects_invalid_utf8_digest_mode_link_and_unsafe_relative_path(self):
        path = self.root / "input"
        path.write_bytes(b"\xff")
        path.chmod(0o600)
        held = self.subject.HeldBytes.open(path, hashlib.sha256(b"\xff").hexdigest(), maximum=2, private=True)
        self.addCleanup(held.close)
        with self.assertRaises(self.subject.CustodyError):
            held.json()
        with self.assertRaises(self.subject.CustodyError):
            held.materialize(self.root, "../escape", 0o400)
        with self.assertRaises(self.subject.CustodyError):
            self.subject.HeldBytes.open(path, "x", maximum=2, private=True)

    def test_strict_json_and_file_shape_fail_closed(self):
        for raw in (b"", b'{"x":1,"x":2}', b'[[[[[[[[[[[[[[[[[[0]]]]]]]]]]]]]]]]]]'):
            with self.subTest(raw=raw), self.assertRaises(self.subject.CustodyError):
                self.subject.strict_json(raw)
        path = self.root / "public"
        path.write_bytes(b"x")
        path.chmod(0o666)
        with self.assertRaises(self.subject.CustodyError):
            self.subject.HeldBytes.open(path, hashlib.sha256(b"x").hexdigest())
        path.chmod(0o600)
        held = self.subject.HeldBytes.open(path, hashlib.sha256(b"x").hexdigest(), private=True)
        held.close()
        with self.assertRaises(self.subject.CustodyError):
            held.revalidate()


class BoundedRunnerTests(unittest.TestCase):
    def setUp(self):
        self.subject = load_source()

    def test_captures_small_output_and_uses_public_environment(self):
        runner = self.subject.BoundedRunner(time.monotonic() + 5)
        result = runner.run([sys.executable, "-c", "import os;print(os.environ.get('PATH'));print('err',file=__import__('sys').stderr)"])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), b"/usr/bin:/bin")
        self.assertEqual(result.stderr.strip(), b"err")

    def test_kills_and_reaps_stdout_or_stderr_over_cap(self):
        runner = self.subject.BoundedRunner(time.monotonic() + 5, output_limit=1024)
        for stream in ("stdout", "stderr"):
            code = f"import sys;getattr(sys,{stream!r}).write('x'*100000);getattr(sys,{stream!r}).flush()"
            with self.subTest(stream=stream), self.assertRaises(self.subject.ProcessError):
                runner.run([sys.executable, "-c", code])
            self.assertIsNotNone(runner.last_pid)
            with self.assertRaises(ChildProcessError):
                os.waitpid(runner.last_pid, os.WNOHANG)

    def test_probe_exit_interrupts_blocked_command_and_reaps(self):
        calls = 0
        def probe():
            nonlocal calls
            calls += 1
            if calls > 1:
                raise self.subject.ProcessError()
        runner = self.subject.BoundedRunner(time.monotonic() + 5, probe=probe)
        started = time.monotonic()
        with self.assertRaises(self.subject.ProcessError):
            runner.run([sys.executable, "-c", "import time;time.sleep(30)"])
        self.assertLess(time.monotonic() - started, 2)
        with self.assertRaises(ChildProcessError):
            os.waitpid(runner.last_pid, os.WNOHANG)

    def test_deadline_kills_and_allow_failure_is_bounded(self):
        runner = self.subject.BoundedRunner(time.monotonic() + 0.2)
        with self.assertRaises(self.subject.ProcessError):
            runner.run([sys.executable, "-c", "import time;time.sleep(30)"])
        allowed = self.subject.BoundedRunner(time.monotonic() + 5).run([sys.executable, "-c", "raise SystemExit(7)"], allow_failure=True)
        self.assertEqual(allowed.returncode, 7)

    def test_rejects_bad_argv_input_and_unaccepted_exit(self):
        runner = self.subject.BoundedRunner(time.monotonic() + 5, input_limit=2)
        for argv, data in (([], None), ([""], None), ([sys.executable], b"too-long")):
            with self.subTest(argv=argv), self.assertRaises(self.subject.ProcessError):
                runner.run(argv, input=data)
        with self.assertRaises(self.subject.ProcessError):
            runner.run([sys.executable, "-c", "raise SystemExit(9)"])


class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.subject = load_source()

    def test_cleanup_has_independent_deadline_and_attempts_every_exact_id(self):
        calls = []
        results = iter([self.subject.Result(1, b"", b""), self.subject.Result(0, b"", b""), self.subject.Result(0, b"", b"")])
        runner = mock.Mock()
        runner.run.side_effect = lambda argv, **_kw: (calls.append(argv), next(results))[1]
        with mock.patch.object(self.subject, "BoundedRunner", return_value=runner):
            failed = self.subject.cleanup_exact(["container-id"], ["volume-id"], ["network-id"], seconds=10)
        self.assertTrue(failed)
        self.assertEqual(calls, [["docker", "rm", "--force", "container-id"], ["docker", "volume", "rm", "volume-id"], ["docker", "network", "rm", "network-id"]])

    def test_runtime_records_created_ids_and_keeps_secret_on_stdin(self):
        runner = mock.Mock(engine=SimpleNamespace(probe=None))
        runner.run.side_effect = [self.subject.Result(0, b"", b""), self.subject.Result(0, b"100 1000 600 1 regular file\n", b""), self.subject.Result(0, b"", b"")]
        runtime = self.subject.ContainerRuntime(runner, "attempt")
        identity = runtime.remember("container", self.subject.Result(0, ("a" * 64 + "\n").encode(), b""))
        runtime.login(identity, "root-sentinel")
        runtime.restore(identity)
        login, restore = runner.run.call_args_list[0], runner.run.call_args_list[2]
        self.assertNotIn("root-sentinel", repr(login.args[0]))
        self.assertEqual(login.kwargs["input"], b"root-sentinel\n")
        self.assertEqual(restore.args[0][-2:], ["-force", "/restore/raft.snap"])
        # Without a TTY, login reads "-" from stdin; the image ships busybox stat in /bin;
        # restore runs as the server user, since root without capabilities cannot read.
        self.assertEqual(login.args[0][-3:], ["login", "-no-print", "-"])
        self.assertIn("/bin/stat", runner.run.call_args_list[1].args[0])
        self.assertNotIn("--user", restore.args[0])
        self.assertEqual(runtime.containers, [identity])

    def test_runtime_rejects_unknown_ids_bad_token_file_and_dead_watcher(self):
        runner = mock.Mock(engine=SimpleNamespace(probe=None))
        runtime = self.subject.ContainerRuntime(runner, "attempt")
        with self.assertRaises(self.subject.ProcessError):
            runtime.remember("container", self.subject.Result(0, b"name\n", b""))
        runner.run.return_value = self.subject.Result(0, b"bad\n", b"")
        with self.assertRaises(self.subject.ProcessError):
            runtime.login("a" * 64, "token")
        runtime.watcher = "b" * 64
        with mock.patch.object(self.subject, "BoundedRunner") as bounded:
            bounded.return_value.run.return_value = self.subject.Result(0, b"false false\n", b"")
            with self.assertRaises(self.subject.ProcessError):
                runtime.watcher_probe()


if __name__ == "__main__":
    unittest.main()
