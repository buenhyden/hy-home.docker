"""Synthetic TLS files and fake Docker/timeout only; never contact a daemon."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "infra/03-security/openbao/scripts/check-tls-material.sh"
IMAGE = "hy-home/openbao:2.7.1-go1.27.3-net0.60.0-r1@sha256:a58fb1109971e506e9de1a360aec48ae07af7b6ccf409f8bac329e30e8fde8c8"
MARKER = "synthetic-private-material"
CID = "a" * 64

FAKE_TIMEOUT = r"""#!/usr/bin/env python3
import json, os, subprocess, sys
from pathlib import Path
args = sys.argv[1:]
if args[0].startswith("--kill-after="):
    args.pop(0)
limit = float(args.pop(0))
with open(os.environ["PROBE_LOG"], "a") as log:
    log.write(json.dumps(["timeout", limit, *args]) + "\n")
if args[:2] == ["docker", "run"]:
    if os.environ.get("PROBE_PRECREATE_TIMEOUT") == "1":
        sys.exit(124)
    result = subprocess.run(args, check=False)
    # Model elapsed seconds without real waits or a Docker daemon.
    if float(os.environ.get("PROBE_SECONDS", "0")) > limit:
        sys.exit(124)
    sys.exit(result.returncode)
os.execvp(args[0], args)
"""

FAKE_DOCKER = r"""#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
state = Path(os.environ["PROBE_STATE"])
with open(os.environ["PROBE_LOG"], "a") as log:
    log.write(json.dumps(["docker", *args]) + "\n")
print("synthetic-private-material", file=sys.stderr)
if args[0] == "run":
    cidfile = Path(args[args.index("--cidfile") + 1]) if "--cidfile" in args else None
    if cidfile and os.environ.get("PROBE_NO_CID") != "1":
        cidfile.write_text("a" * 64)
    state.write_text("present")
    sys.exit(int(os.environ.get("PROBE_EXIT", "0")))
if args[:2] == ["container", "ls"]:
    if os.environ.get("PROBE_LIST_FAIL") == "1":
        sys.exit(1)
    if state.exists():
        print(os.environ.get("PROBE_CID", "a" * 64))
    sys.exit(0)
if args[:2] == ["container", "rm"]:
    if os.environ.get("PROBE_REMOVE_FAIL") == "1":
        sys.exit(1)
    if os.environ.get("PROBE_STAYS") != "1":
        state.unlink(missing_ok=True)
    sys.exit(0)
sys.exit(99)
"""


class TLSMaterialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.fixture = Path(cls.temporary.name)
        cls.certificates = cls.fixture / "tls"
        cls.certificates.mkdir()
        cls.issue(cls.certificates, "DNS:openbao,IP:127.0.0.1")

    @staticmethod
    def issue(directory, san, days="1"):
        subprocess.run(
            [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-keyout",
                str(directory / "server-key.pem"),
                "-out",
                str(directory / "server.pem"),
                "-days",
                days,
                "-subj",
                "/CN=openbao",
                "-addext",
                "subjectAltName=" + san,
                "-addext",
                "extendedKeyUsage=serverAuth",
            ],
            capture_output=True,
            check=True,
        )
        shutil.copy2(directory / "server.pem", directory / "ca.pem")

    def setUp(self):
        self.temporary_run = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_run.cleanup)
        self.directory = Path(self.temporary_run.name)
        self.material = self.directory / "tls"
        shutil.copytree(self.certificates, self.material)
        self.tools = self.directory / "bin"
        self.tools.mkdir()
        for name, source in (("docker", FAKE_DOCKER), ("timeout", FAKE_TIMEOUT)):
            path = self.tools / name
            path.write_text(source)
            path.chmod(0o700)
        self.log = self.directory / "calls.jsonl"
        self.state = self.directory / "container"

    def run_probe(self, **environment):
        result = subprocess.run(
            ["sh", str(SCRIPT), str(self.material), IMAGE],
            env={
                **os.environ,
                "PATH": f"{self.tools}:{os.environ['PATH']}",
                "PROBE_LOG": str(self.log),
                "PROBE_STATE": str(self.state),
                **environment,
            },
            capture_output=True,
            check=False,
            timeout=10,
        )
        self.assertNotIn(MARKER.encode(), result.stdout + result.stderr)
        if self.log.exists():
            for call in self.calls():
                if "--cidfile" in call:
                    tracking = Path(call[call.index("--cidfile") + 1]).parent
                    self.addCleanup(shutil.rmtree, tracking, ignore_errors=True)
        return result

    def calls(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def test_probe_over_twenty_seconds_completes_within_sixty_and_cleans_owned_id(self):
        result = self.run_probe(PROBE_SECONDS="25")
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn(b"TLS_MATERIAL PASS", result.stdout)
        calls = self.calls()
        native = next(call for call in calls if call[:3] == ["timeout", 60, "docker"])
        self.assertEqual("run", native[3])
        for flag in (
            "--pull=never",
            "--network=none",
            "--user=100:1000",
            "--read-only",
            "--cap-drop=ALL",
            "--security-opt=no-new-privileges",
        ):
            self.assertIn(flag, native)
        self.assertEqual(3, sum("readonly" in arg for arg in native[2:]))
        self.assertIn(IMAGE, native)
        self.assertTrue(
            all(
                call[1] == 10
                for call in calls
                if call[:1] == ["timeout"] and call[2] == "openssl"
            )
        )
        self.assertIn(["docker", "container", "rm", "--force", CID], calls)
        owned_name = native[native.index("--name") + 1]
        listings = [call for call in calls if call[:3] == ["docker", "container", "ls"]]
        self.assertEqual(2, len(listings))
        for listing in listings:
            self.assertIn("name=^/" + owned_name + "$", listing)
            self.assertIn("label=hyhome.openbao.tls-probe=" + owned_name, listing)
        self.assertFalse(self.state.exists())
        tracking = Path(native[native.index("--cidfile") + 1]).parent
        self.assertFalse(tracking.exists())

    def test_timeout_and_docker_error_propagate_after_owned_cleanup(self):
        for environment in ({"PROBE_SECONDS": "61"}, {"PROBE_EXIT": "125"}):
            with self.subTest(environment=environment):
                result = self.run_probe(**environment)
                self.assertNotEqual(0, result.returncode)
                self.assertIn(b"FAIL check=native-user-read", result.stdout)
                self.assertIn(b"cleanup=pending-reconciliation", result.stdout)
                self.assertFalse(self.state.exists())

    def test_timeout_before_daemon_create_keeps_exact_identity_for_reconciliation(self):
        result = self.run_probe(PROBE_PRECREATE_TIMEOUT="1")
        self.assertNotEqual(0, result.returncode)
        self.assertIn(b"cleanup=pending-reconciliation", result.stdout)
        calls = self.calls()
        native = next(
            call for call in calls if call[:4] == ["timeout", 60, "docker", "run"]
        )
        tracking = Path(native[native.index("--cidfile") + 1]).parent
        name = native[native.index("--name") + 1]
        self.assertTrue(tracking.is_dir())
        self.assertEqual(
            [name, "hyhome.openbao.tls-probe=" + name],
            (tracking / "identity").read_text().splitlines(),
        )
        self.assertFalse(
            any(call[:3] == ["docker", "container", "rm"] for call in calls)
        )
        self.assertFalse(self.state.exists())

    def test_timeout_before_cid_write_recovers_only_owned_container(self):
        result = self.run_probe(PROBE_SECONDS="61", PROBE_NO_CID="1")
        self.assertNotEqual(0, result.returncode)
        self.assertIn(["docker", "container", "rm", "--force", CID], self.calls())
        self.assertFalse(self.state.exists())

    def test_cleanup_failure_and_ambiguous_ids_cannot_report_pass(self):
        for environment in (
            {"PROBE_REMOVE_FAIL": "1"},
            {"PROBE_LIST_FAIL": "1"},
            {"PROBE_STAYS": "1"},
            {"PROBE_CID": CID + "\n" + "b" * 64},
        ):
            with self.subTest(environment=environment):
                result = self.run_probe(**environment)
                self.assertNotEqual(0, result.returncode)
                self.assertIn(b"FAIL check=native-user-cleanup", result.stdout)
                self.assertNotIn(b"PASS", result.stdout)

    def test_material_missing_or_symlink_fails_before_docker(self):
        (self.material / "ca.pem").unlink()
        result = self.run_probe()
        self.assertIn(b"FAIL check=material-file", result.stdout)
        self.assertFalse(self.log.exists())
        (self.material / "ca.pem").symlink_to(self.certificates / "ca.pem")
        self.assertIn(b"FAIL check=material-file", self.run_probe().stdout)

    def test_bad_san_and_key_mismatch_remain_failures(self):
        self.issue(self.material, "DNS:wrong.invalid,IP:127.0.0.1")
        self.assertIn(b"FAIL check=chain-san", self.run_probe().stdout)
        shutil.copy2(self.certificates / "server.pem", self.material / "server.pem")
        shutil.copy2(self.certificates / "ca.pem", self.material / "ca.pem")
        self.assertIn(b"FAIL check=key-match", self.run_probe().stdout)

    def test_real_expired_certificate_and_missing_loopback_san_fail(self):
        subprocess.run(
            [
                "openssl",
                "x509",
                "-in",
                str(self.material / "server.pem"),
                "-signkey",
                str(self.material / "server-key.pem"),
                "-days",
                "-1",
                "-out",
                str(self.material / "expired.pem"),
            ],
            capture_output=True,
            check=True,
        )
        (self.material / "expired.pem").replace(self.material / "server.pem")
        self.assertIn(b"FAIL check=server-expiry", self.run_probe().stdout)
        self.issue(self.material, "DNS:openbao")
        self.assertIn(b"FAIL check=loopback-san", self.run_probe().stdout)

    def test_unreadable_host_material_stops_before_docker(self):
        path = self.material / "server-key.pem"
        path.chmod(0)
        self.addCleanup(path.chmod, 0o600)
        if os.access(path, os.R_OK):
            self.skipTest("current identity bypasses file read permissions")
        self.assertIn(b"FAIL check=material-file", self.run_probe().stdout)
        self.assertFalse(self.log.exists())

    def test_expiry_and_native_unreadable_fail_without_output(self):
        openssl = self.tools / "openssl"
        openssl.write_text("#!/bin/sh\necho synthetic-private-material >&2\nexit 1\n")
        openssl.chmod(0o700)
        self.assertIn(b"FAIL check=ca-expiry", self.run_probe().stdout)
        openssl.unlink()
        result = self.run_probe(PROBE_EXIT="1")
        self.assertIn(b"FAIL check=native-user-read", result.stdout)


if __name__ == "__main__":
    unittest.main()
