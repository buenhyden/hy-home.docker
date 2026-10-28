"""Offline generated-shell credential custody regressions."""

import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from .test_openbao_issuance import BASE, REV, WHEN, FakeAPI, M, custody_dir


class RequestCustodyTests(unittest.TestCase):
    """Execute the generated server shell with synthetic credentials and CLI stubs."""

    def setUp(self):
        self.fixture = tempfile.TemporaryDirectory()
        self.addCleanup(self.fixture.cleanup)
        self.root = Path(self.fixture.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.memory = self.root / "memory"
        self.memory.mkdir()
        self.capture = self.root / "capture.json"
        self.api = M.DockerAPI(
            "server",
            "volume",
            "agent",
            "fixture-issuer",
            "fixture-cleanup",
            request_script=(BASE / "scripts/renderer-request.sh").read_text(),
        )
        self.env = {
            **os.environ,
            "BAO_ADDR": "https://127.0.0.1:8200",
            "BAO_CACERT": "/openbao/tls/ca.pem",
            "BAO_TLS_SERVER_NAME": "openbao",
            "BAO_TOKEN": "poisoned-token",
            "VAULT_TOKEN": "poisoned-vault-token",
            "BAO_TOKEN_PATH": "/poisoned-token-file",
            "BAO_NAMESPACE": "poisoned-namespace",
            "BAO_SKIP_VERIFY": "true",
            "VAULT_SKIP_VERIFY": "true",
            "BAO_HEADERS": "poisoned-header",
            "HTTPS_PROXY": "https://proxy.invalid",
            "BAO_CLI_CONFIG": "/poisoned-config",
            "HOME": str(self.root / "poisoned-home"),
        }
        self.stub(
            "stat",
            '#!/bin/sh\nif [ "$1" = -f ]; then echo tmpfs; else exec /usr/bin/stat "$@"; fi\n',
        )
        self.bao()

    def stub(self, name, script):
        path = self.bin / name
        path.write_text(script)
        path.chmod(0o700)

    def bao(self, *, failure=False, pause=False):
        self.stub(
            "bao",
            f"#!{sys.executable}\n"
            + f"""import json,os,pathlib,sys,time
p=pathlib.Path(os.environ.get("BAO_TOKEN_PATH", "/absent"))
d=p.parent
info=p.stat() if p.exists() else None
pathlib.Path({str(self.capture)!r}).write_text(json.dumps({{
 "env":dict(os.environ), "argv":sys.argv, "token":p.read_text() if p.exists() else None,
 "mode":info.st_mode & 0o777 if info else None, "links":info.st_nlink if info else None,
 "directory_mode":d.stat().st_mode & 0o777, "stdin":sys.stdin.read(),
}}))
{"time.sleep(30)" if pause else ""}
print('{{}}')
sys.exit({2 if failure else 0})
""",
        )

    def script(self, *, issuer=True, payload=None):
        observed = []

        def command(argv, **kwargs):
            observed.append((argv, kwargs))
            return b"{}"

        with patch.object(self.api, "command", side_effect=command):
            self.api.request("write", M.PREFIX + "/secret-id", payload, issuer=issuer)
        argv, kwargs = observed[0]
        self.assertEqual(["docker", "exec", "-i", "server"], argv[:4])
        for token in ("fixture-issuer", "fixture-cleanup"):
            self.assertNotIn(token, " ".join(argv))
        script = argv[6].replace("/dev/shm", str(self.memory))
        script = script.replace("PATH=/bin:/usr/bin", f"PATH={self.bin}:/bin:/usr/bin")
        # The real CA is deliberately outside this offline fixture.
        script = script.replace('[ -r "$BAO_CACERT" ]', ":")
        return ["/bin/sh", "-c", script, *argv[7:]], kwargs["payload"]

    def execute(self, **kwargs):
        argv, body = self.script(**kwargs)
        done = subprocess.run(
            argv, input=body, env=self.env, capture_output=True, timeout=8, check=False
        )
        for token in (b"fixture-issuer", b"fixture-cleanup", b"poisoned-token"):
            self.assertNotIn(token, done.stdout + done.stderr)
        return done

    def test_private_file_replaces_raw_environment_and_preserves_json_stdin(self):
        for issuer in (True, False):
            with self.subTest(issuer=issuer):
                self.assertEqual(
                    0,
                    self.execute(issuer=issuer, payload={"key": "fixture"}).returncode,
                )
                captured = json.loads(self.capture.read_text())
                self.assertEqual(
                    "fixture-issuer" if issuer else "fixture-cleanup", captured["token"]
                )
                self.assertEqual(0o600, captured["mode"])
                self.assertEqual(1, captured["links"])
                self.assertEqual(0o700, captured["directory_mode"])
                self.assertEqual({"key": "fixture"}, json.loads(captured["stdin"]))
                self.assertEqual(
                    {
                        "PATH",
                        "HOME",
                        "BAO_ADDR",
                        "BAO_CACERT",
                        "BAO_TLS_SERVER_NAME",
                        "BAO_TOKEN_PATH",
                        "LC_CTYPE",
                    },
                    set(captured["env"]),
                )
                self.assertNotIn(
                    captured["token"],
                    json.dumps(captured["env"]) + str(captured["argv"]),
                )
                self.assertEqual(
                    str(Path(captured["env"]["BAO_TOKEN_PATH"]).parent),
                    captured["env"]["HOME"],
                )
                self.assertFalse(Path(captured["env"]["BAO_TOKEN_PATH"]).exists())
                self.assertEqual([], list(self.memory.iterdir()))

    def test_cli_failure_removes_private_credential(self):
        self.bao(failure=True)
        self.assertEqual(2, self.execute().returncode)
        self.assertTrue(self.capture.exists())
        self.assertEqual([], list(self.memory.iterdir()))

    def test_non_tmpfs_or_symlinked_base_refused_before_cli(self):
        self.stub(
            "stat",
            '#!/bin/sh\nif [ "$1" = -f ]; then echo ext4; else exec /usr/bin/stat "$@"; fi\n',
        )
        self.assertNotEqual(0, self.execute().returncode)
        self.assertFalse(self.capture.exists())
        self.memory.rmdir()
        self.memory.symlink_to(self.root, target_is_directory=True)
        self.assertNotEqual(0, self.execute().returncode)
        self.assertFalse(self.capture.exists())

    def test_signal_removes_credential_and_terminates_cli(self):
        self.bao(pause=True)
        argv, body = self.script()
        process = subprocess.Popen(
            argv,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.env,
        )
        try:
            process.stdin.write(body)
            process.stdin.close()
            for _ in range(100):
                if self.capture.exists() or process.poll() is not None:
                    break
                time.sleep(0.01)
            self.assertTrue(self.capture.exists())
            process.send_signal(signal.SIGTERM)
            self.assertNotEqual(0, process.wait(timeout=5))
            self.assertEqual([], list(self.memory.iterdir()))
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=5)
            process.stdout.close()
            process.stderr.close()

    def test_unsafe_tls_address_or_identity_refused_before_token_read(self):
        for key, value in (
            ("BAO_ADDR", "https://attacker.invalid:8200"),
            ("BAO_ADDR", "https://127.0.0.1:8200/redirect"),
            ("BAO_ADDR", "https://127.0.0.1:0"),
            ("BAO_ADDR", "https://127.0.0.1:65536"),
            ("BAO_CACERT", "/attacker/ca.pem"),
            ("BAO_TLS_SERVER_NAME", "attacker.invalid"),
        ):
            with self.subTest(key=key, value=value):
                original = self.env[key]
                self.env[key] = value
                self.assertNotEqual(0, self.execute().returncode)
                self.env[key] = original
                self.assertFalse(self.capture.exists())
                self.assertEqual([], list(self.memory.iterdir()))

    def test_private_directory_and_single_link_file_guards(self):
        for guard in (
            "directory-mode",
            "token-links",
            "token-mode",
            "private-filesystem",
            "private-device",
        ):
            with self.subTest(guard=guard):
                self.stub(
                    "stat",
                    "#!/bin/sh\n"
                    + f"""
case "$1:$2:$3" in
-f:-c:%T) case "$4" in */renderer-issuance.*) echo {"ext4" if guard == "private-filesystem" else "tmpfs"};; *) echo tmpfs;; esac;;
-c:%a:%u:*) echo {"755" if guard == "directory-mode" else "700"}:$(id -u);;
-c:%a:%h:%u:*) echo {"644" if guard == "token-mode" else "600"}:{2 if guard == "token-links" else 1}:$(id -u);;
-c:%d:*/renderer-issuance.*) echo {999 if guard == "private-device" else 1};;
-c:%d:*) echo 1;;
*) exec /usr/bin/stat "$@";;
esac
""",
                )
                self.assertNotEqual(0, self.execute().returncode)
                self.assertFalse(self.capture.exists())
                self.assertEqual([], list(self.memory.iterdir()))

    def test_internal_timeout_and_failed_post_request_cleanup_are_uncertain(self):
        self.bao(pause=True)
        argv, body = self.script()
        argv[4] = "1"
        done = subprocess.run(
            argv, input=body, env=self.env, capture_output=True, timeout=5, check=False
        )
        self.assertEqual(124, done.returncode)
        self.assertTrue(self.capture.exists())
        self.assertEqual([], list(self.memory.iterdir()))
        self.bao()
        self.stub("rmdir", "#!/bin/sh\nexit 1\n")
        self.assertEqual(125, self.execute().returncode)
        self.assertFalse(any(self.memory.glob("*/token")))
        for failure in (M.Blocked, InterruptedError):
            with (
                self.subTest(failure=failure),
                patch.object(self.api, "command", side_effect=failure),
            ):
                with self.assertRaises(M.Uncertain):
                    self.api.issue({"key": "fixture"})

    def test_ambiguous_request_retains_journal_without_cleanup_or_reissue(self):
        class UncertainAPI(FakeAPI):
            def accessors(inner):
                inner.calls.append("accessors")
                return []

            def issue(inner, metadata):
                inner.calls.append("issue")
                with patch.object(self.api, "command", side_effect=M.Blocked):
                    return self.api.issue(metadata)

        with (
            tempfile.TemporaryDirectory() as directory,
            M.Journal(directory) as journal,
        ):
            api = UncertainAPI()
            api.journal = journal
            with self.assertRaises(M.Blocked):
                M.run_issuance(
                    api,
                    journal,
                    revision=REV,
                    custody=custody_dir(self),
                    clock=lambda: WHEN,
                )
            self.assertEqual(["issue"], api.calls)
            self.assertIsNotNone(journal.load())
            with self.assertRaises(M.Blocked):
                M.run_issuance(api, journal, revision=REV, custody=custody_dir(self))
            self.assertEqual(["issue", "accessors"], api.calls)
            self.assertIsNotNone(journal.load())


if __name__ == "__main__":
    unittest.main()
