"""Synthetic TLS checks; real Docker delay cases require an explicit opt-in."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest import mock

from tests.validation import _openbao_tls_delay_native as native
from tests.validation._openbao_tls_delay_native import (
    READ_SCRIPT,
    _native_docker_wrapper,
    _native_run_argv,
    _native_validate_run,
)

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


@unittest.skipUnless(
    os.environ.get("HYHOME_OPENBAO_TLS_DELAY_NATIVE") == "1",
    "requires explicit HYHOME_OPENBAO_TLS_DELAY_NATIVE=1",
)
class TLSMaterialNativeDelayTests(native.NativeHarness):
    issue = staticmethod(TLSMaterialTests.issue)
    test_source = Path(__file__)

    @classmethod
    def setUpClass(cls):
        if os.environ.get("HYHOME_OPENBAO_TLS_DELAY_NATIVE") != "1":
            raise unittest.SkipTest(
                "requires explicit HYHOME_OPENBAO_TLS_DELAY_NATIVE=1"
            )
        if os.getgid() != 1000:
            raise RuntimeError(
                "default Docker context and synthetic fixture GID 1000 are required"
            )
        if shutil.which("docker") != "/usr/bin/docker":
            raise RuntimeError("PATH must resolve docker to verified /usr/bin/docker")
        cls.docker = "/usr/bin/docker"
        setup_root = Path(tempfile.mkdtemp(prefix="hyhome-b3-preflight-"))
        cls.docker_config = setup_root / "docker-config"
        cls.docker_config.mkdir(mode=0o700)
        context = native._native_call(
            cls.docker, ["context", "show"], config_dir=cls.docker_config
        )
        if context.returncode or context.stdout.strip() != b"default":
            raise RuntimeError("default Docker context is required")
        result = native._native_call(
            cls.docker, ["image", "inspect", IMAGE], config_dir=cls.docker_config
        )
        if result.returncode:
            raise RuntimeError(
                "exact approved cached image is unavailable; no pull allowed"
            )
        image = json.loads(result.stdout)[0]
        if image["Config"].get("Volumes") is not None:
            raise RuntimeError("image-declared volumes are not admitted")
        cls.image_id = image["Id"]

    def _fixture(self, delay):
        root = Path(tempfile.mkdtemp(prefix="hyhome-b3-native-"))
        material = root / "tls"
        material.mkdir(mode=0o750)
        material.chmod(0o750)
        (root / "docker-config").mkdir(mode=0o700)
        self.issue(material, "DNS:openbao,IP:127.0.0.1")
        for name in ("ca.pem", "server.pem", "server-key.pem"):
            (material / name).chmod(0o640 if name == "server-key.pem" else 0o644)
        tools = root / "bin"
        tools.mkdir(mode=0o700)
        config = {
            "docker": self.docker,
            "image_id": self.image_id,
            "material": str(material),
            "delay": delay,
            "intent": str(root / "intent.json"),
            "cleanup_log": str(root / "cleanup.jsonl"),
            "docker_config": str(root / "docker-config"),
            "registration": str(root / "registration.json"),
            "dispatch_result": str(root / "dispatch-result.json"),
            "deadline": native.time.monotonic() + 190,
        }
        Path(config["cleanup_log"]).touch(mode=0o600)
        native._native_write(root / "config.json", config)
        wrapper = tools / "docker"
        wrapper.write_text(
            f"#!{native.sys.executable}\nimport runpy, sys\nrunpy.run_path({str(Path(native.__file__).resolve())!r})['_native_docker_wrapper'](sys.argv[1:], {str(root / 'config.json')!r})\n"
        )
        wrapper.chmod(0o700)
        return root, config

    def test_native_twenty_five_second_probe(self):
        self._run_delay(25)

    def test_native_sixty_one_second_timeout(self):
        self._run_delay(61)

    def test_native_real_command_error(self):
        self._run_delay("error")

    def test_native_verified_container_kill(self):
        self._run_delay("kill")

    def test_native_controlled_late_dispatch(self):
        self._run_delay("late")


class TLSNativeGuardTests(unittest.TestCase):
    def test_exact_native_argv_rejects_duplicate_or_changed_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            material = Path(directory)
            for name in ("ca.pem", "server.pem", "server-key.pem"):
                path = material / name
                path.write_text("synthetic fixture")
                path.chmod(0o640 if name == "server-key.pem" else 0o644)
            tracking = Path("/tmp") / ("openbao-tls." + uuid.uuid4().hex[:10])
            tracking.mkdir(mode=0o700)
            self.addCleanup(shutil.rmtree, tracking)
            identity = tracking / "identity"
            identity.write_text(
                f"{tracking.name}\nhyhome.openbao.tls-probe={tracking.name}\n"
            )
            identity.chmod(0o600)
            argv = _native_run_argv(material, tracking)
            self.assertEqual(
                tracking, _native_validate_run(argv, material, os.getuid())
            )
            for changed in (
                [*argv, "--privileged"],
                [*argv[:1], "--network=host", *argv[1:]],
                ["other-image" if value == IMAGE else value for value in argv],
                [
                    value.replace("hyhome.openbao.tls-probe=", "wrong=")
                    for value in argv
                ],
                ["wrong-name" if value == tracking.name else value for value in argv],
                [value.replace("dst=/tls/ca.pem", "dst=/outside") for value in argv],
                [*argv[:-1], "id"],
            ):
                with (
                    self.subTest(changed=changed),
                    mock.patch.dict(os.environ, {"DOCKER_HOST": ""}),
                    mock.patch(
                        native.__name__ + "._native_read",
                        return_value={"delay": 25, "material": str(material)},
                    ),
                    mock.patch("os.execve") as execute,
                    self.assertRaises(ValueError),
                ):
                    _native_docker_wrapper(changed, Path("/unused"))
                execute.assert_not_called()
            identity.chmod(0o644)
            with self.assertRaises(ValueError):
                _native_validate_run(argv, material, os.getuid())

    def test_default_native_guard_precedes_certificates_and_subprocesses(self):
        with (
            mock.patch.dict(os.environ, {"HYHOME_OPENBAO_TLS_DELAY_NATIVE": ""}),
            mock.patch.object(TLSMaterialTests, "issue") as issue,
            mock.patch("subprocess.run") as run,
            self.assertRaises(unittest.SkipTest),
        ):
            TLSMaterialNativeDelayTests.setUpClass()
        issue.assert_not_called()
        run.assert_not_called()


class TLSNativeDispatchGuardTests(unittest.TestCase):
    def test_payloads_are_closed_and_late_release_requires_every_witness(self):
        from tests.validation import _openbao_tls_delay_native as native

        self.assertEqual("sleep 2; exit 17", native._native_payload("error"))
        self.assertEqual("sleep 120; " + READ_SCRIPT, native._native_payload("kill"))
        self.assertEqual("sleep 30; " + READ_SCRIPT, native._native_payload("late"))
        with self.assertRaises(ValueError):
            native._native_payload("unapproved")
        native._native_release_allowed(
            1, b"cleanup=pending-reconciliation", True, 0, b""
        )
        for values in (
            (0, b"cleanup=pending-reconciliation", True, 0, b""),
            (1, b"FAIL", True, 0, b""),
            (1, b"cleanup=pending-reconciliation", False, 0, b""),
            (1, b"cleanup=pending-reconciliation", True, 1, b""),
            (1, b"cleanup=pending-reconciliation", True, 0, b"a" * 64),
        ):
            with self.subTest(values=values), self.assertRaises(ValueError):
                native._native_release_allowed(*values)

    def test_dispatch_control_requires_one_exact_release_and_eof(self):
        from tests.validation import _openbao_tls_delay_native as native

        for payload in (b"", b"release\nrelease\n", b"other\n"):
            read_fd, write_fd = os.pipe()
            os.write(write_fd, payload)
            os.close(write_fd)
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                native._native_control(read_fd)
        read_fd, write_fd = os.pipe()
        os.write(write_fd, b"release\n")
        os.close(write_fd)
        native._native_control(read_fd)

    def _dispatch_fixture(self):
        temporary = tempfile.TemporaryDirectory(prefix="hyhome-b3-native-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        material = root / "tls"
        material.mkdir(mode=0o750)
        material.chmod(0o750)
        # Synthetic guards run on any host GID; Native setup still requires 1000.
        gid_patch = mock.patch.object(native, "FIXTURE_GID", material.stat().st_gid)
        gid_patch.start()
        self.addCleanup(gid_patch.stop)
        (root / "docker-config").mkdir(mode=0o700)
        for name in ("ca.pem", "server.pem", "server-key.pem"):
            path = material / name
            path.write_text("synthetic fixture")
            path.chmod(0o640 if name == "server-key.pem" else 0o644)
        tracking = Path("/tmp") / ("openbao-tls." + uuid.uuid4().hex[:10])
        tracking.mkdir(mode=0o700)
        self.addCleanup(shutil.rmtree, tracking)
        identity = tracking / "identity"
        identity.write_text(
            f"{tracking.name}\nhyhome.openbao.tls-probe={tracking.name}\n"
        )
        identity.chmod(0o600)
        config = {
            "delay": "late",
            "material": str(material),
            "deadline": native.time.monotonic() + 190,
            "docker": "/usr/bin/docker",
            "intent": str(root / "intent.json"),
            "cleanup_log": str(root / "cleanup.jsonl"),
            "registration": str(root / "registration.json"),
            "dispatch_result": str(root / "dispatch-result.json"),
            "docker_config": str(root / "docker-config"),
        }
        native._native_write(root / "config.json", config)
        native._native_write(
            Path(config["intent"]), {"name": tracking.name, "tracking": str(tracking)}
        )
        native._native_write(
            Path(config["registration"]),
            {
                "config": str(root / "config.json"),
                "tracking": str(tracking),
                "argv": _native_run_argv(material, tracking),
            },
        )
        return root, config

    def test_registered_dispatch_is_one_shot_and_rejects_symlink(self):
        root, config = self._dispatch_fixture()
        with (
            mock.patch.object(native.os, "getpid", return_value=123),
            mock.patch.object(native.os, "getpgrp", return_value=123),
            mock.patch.object(native.os, "getsid", return_value=123),
            mock.patch.object(native, "_native_control"),
            mock.patch.dict(os.environ, {"DOCKER_HOST": ""}),
            mock.patch.object(
                native,
                "_native_call",
                return_value=subprocess.CompletedProcess(
                    [], 0, ("a" * 64 + "\n").encode(), b""
                ),
            ) as call,
        ):
            native._native_dispatch(root / "config.json", 99)
            with self.assertRaises(FileExistsError):
                native._native_dispatch(root / "config.json", 99)
            self.assertEqual(1, call.call_count)
            self.assertIn("--detach", call.call_args.args[1])
        registration = Path(config["registration"])
        saved = root / "saved.json"
        registration.rename(saved)
        registration.symlink_to(saved)
        with self.assertRaises(ValueError):
            native._native_read(registration)

    def test_dispatch_registration_cannot_substitute_source_intent(self):
        root, config = self._dispatch_fixture()
        native._native_write(
            Path(config["intent"]), {"name": "different", "tracking": "/tmp/different"}
        )
        with (
            mock.patch.object(native.os, "getpid", return_value=123),
            mock.patch.object(native.os, "getpgrp", return_value=123),
            mock.patch.object(native.os, "getsid", return_value=123),
            mock.patch.object(native, "_native_control"),
            mock.patch.dict(os.environ, {"DOCKER_HOST": ""}),
            mock.patch.object(
                native,
                "_native_call",
                return_value=subprocess.CompletedProcess(
                    [], 0, ("a" * 64 + "\n").encode(), b""
                ),
            ) as call,
            self.assertRaises(ValueError),
        ):
            native._native_dispatch(root / "config.json", 99)
        call.assert_not_called()

    def test_fixed_docker_rejects_config_alternate_and_path_shadow(self):
        root, config = self._dispatch_fixture()
        config["docker"] = str(Path(native.sys.executable).resolve())
        with self.assertRaises(ValueError):
            native._native_private_config(root / "config.json", config)
        with (
            mock.patch.dict(
                os.environ, {"HYHOME_OPENBAO_TLS_DELAY_NATIVE": "1", "DOCKER_HOST": ""}
            ),
            mock.patch.object(native.os, "getgid", return_value=1000),
            mock.patch.object(shutil, "which", return_value=config["docker"]),
            mock.patch.object(
                native,
                "_native_call",
                return_value=subprocess.CompletedProcess([], 1, b"", b""),
            ) as call,
            self.assertRaises(RuntimeError),
        ):
            TLSMaterialNativeDelayTests.setUpClass()
        call.assert_not_called()

    def test_source_cid_rejects_malformed_symlink_mode_and_mismatch(self):
        _root, config = self._dispatch_fixture()
        intent = native._native_read(Path(config["intent"]))
        tracking = Path(intent["tracking"])
        self.assertIsNone(native._native_cid(tracking))
        cidfile = tracking / "cid"
        for value in ("x" * 64, "a" * 66, "a" * 64 + " "):
            cidfile.write_text(value)
            cidfile.chmod(0o600)
            with self.subTest(value=value), self.assertRaises(ValueError):
                native._native_cid(tracking)
        cidfile.write_text("a" * 64)
        cidfile.chmod(0o600)
        self.assertEqual("a" * 64, native._native_cid(tracking))
        with (
            mock.patch.object(native.os, "getuid", return_value=os.getuid() + 1),
            self.assertRaises(ValueError),
        ):
            native._native_cid(tracking)
        cidfile.chmod(0o644)
        with self.assertRaises(ValueError):
            native._native_cid(tracking)
        cidfile.chmod(0o600)
        with self.assertRaises(ValueError):
            native._native_cid(tracking, "b" * 64)
        saved = tracking / "saved"
        cidfile.rename(saved)
        cidfile.symlink_to(saved)
        with self.assertRaises(ValueError):
            native._native_cid(tracking)

    def test_observer_waits_for_empty_cid_before_inspect_or_kill(self):
        _root, config = self._dispatch_fixture()
        config["delay"] = "kill"
        tracking = Path(native._native_read(Path(config["intent"]))["tracking"])
        cidfile = tracking / "cid"
        cidfile.touch(mode=0o600)
        with self.assertRaises(ValueError):
            native._native_cid(tracking, "a" * 64)
        cid = "a" * 64
        harness, witness, stop = native.NativeHarness(), {"started": 0}, mock.Mock()
        stop.is_set.return_value = False
        container = {"Id": cid, "State": {"Running": True}}

        def deliver(_timeout):
            call.assert_not_called()
            self.assertNotIn("container", witness)
            cidfile.write_text(cid)

        def docker(_config, argv):
            self.assertEqual(cid, cidfile.read_text())
            self.assertTrue(argv[1] != "kill" or events.called)
            return subprocess.CompletedProcess(
                argv, 0, json.dumps([container]).encode(), b""
            )

        stop.wait.side_effect = deliver
        with (
            mock.patch.object(native, "_native_container_identity"),
            mock.patch.object(
                harness, "_events", return_value=["early proof"]
            ) as events,
            mock.patch.object(harness, "_call", side_effect=docker) as call,
        ):
            harness._observe(config, stop, witness)
        self.assertNotIn("error", witness)
        self.assertEqual(container, witness["container"])
        self.assertEqual(0, witness["kill_exit"])
        stop.wait.assert_called_once_with(0.1)
        self.assertEqual(
            [
                mock.call(config, ["container", "inspect", cid]),
                mock.call(config, ["container", "kill", "--signal", "KILL", cid]),
            ],
            call.call_args_list,
        )

    def test_early_events_survive_later_history_loss_and_reject_incomplete_proof(self):
        _root, config = self._dispatch_fixture()
        intent = native._native_read(Path(config["intent"]))
        cid, name = "a" * 64, intent["name"]
        attributes = dict.fromkeys(("name", "hyhome.openbao.tls-probe"), name)
        actor = {"ID": cid, "Attributes": attributes}
        rows = [
            {"Action": action, "timeNano": index * 10**9, "Actor": actor}
            for index, action in enumerate(("create", "start", "die", "destroy"))
        ]
        receipt = {"witness": {"events": rows[:2]}}
        Path(config["cleanup_log"]).write_text("")
        output = subprocess.CompletedProcess(
            [], 0, "\n".join(map(json.dumps, rows[2:])).encode(), b""
        )
        harness = TLSMaterialNativeDelayTests()
        with mock.patch.object(harness, "_call", return_value=output):
            harness._delay_events(config, intent, 0, 4, cid, receipt)
            self.assertEqual(rows, receipt["events"])
            self.assertEqual(1, receipt["native_seconds"])
            wrong = [{**row, "Actor": {**actor, "ID": "b" * 64}} for row in rows[2:]]
            for required, subset in (
                ((), rows[2:]),
                (("create", "start"), rows[2:]),
                (("die", "destroy"), rows[-1:]),
                (("die", "destroy"), wrong),
            ):
                output.stdout = "\n".join(map(json.dumps, subset)).encode()
                with self.subTest(required=required, subset=subset):
                    with self.assertRaises(AssertionError):
                        harness._events(config, intent, 0, 4, cid, required)

    def test_observer_cid_mismatch_fails_before_witness_or_kill(self):
        _root, config = self._dispatch_fixture()
        config["delay"] = "kill"
        tracking = Path(native._native_read(Path(config["intent"]))["tracking"])
        cidfile = tracking / "cid"
        cidfile.write_text("a" * 64)
        cidfile.chmod(0o600)
        harness = native.NativeHarness()
        witness = {}
        container = {"Id": "b" * 64, "State": {"Running": True}}
        with (
            mock.patch.object(native, "_native_container_identity"),
            mock.patch.object(
                harness,
                "_call",
                return_value=subprocess.CompletedProcess(
                    [], 0, json.dumps([container]).encode(), b""
                ),
            ) as call,
        ):
            harness._observe(config, native.threading.Event(), witness)
        self.assertNotIn("container", witness)
        self.assertIn("error", witness)
        self.assertEqual(1, call.call_count)

    def test_tls_directories_keep_mode_under_restrictive_umask(self):
        previous = os.umask(0o077)
        try:
            root, config = self._dispatch_fixture()
            native._native_private_config(root / "config.json", config)
            harness = TLSMaterialNativeDelayTests()
            harness.docker, harness.image_id = "/usr/bin/docker", "synthetic-image"

            def issue(directory, san):
                for name in ("ca.pem", "server.pem", "server-key.pem"):
                    (directory / name).write_text("synthetic fixture")

            harness.issue = issue
            fixture, native_config = harness._fixture(25)
            self.addCleanup(shutil.rmtree, fixture)
            native._native_private_config(fixture / "config.json", native_config)
        finally:
            os.umask(previous)

    def test_client_environment_is_private_and_scrubs_every_override(self):
        root, _config = self._dispatch_fixture()
        directory = root / "docker-config"
        inherited = {
            "DOCKER_HOST": "tcp://private.invalid",
            "DOCKER_CONTEXT": "private",
            "DOCKER_CERT_PATH": "/private",
            "DOCKER_TLS_VERIFY": "1",
            "DOCKER_TLS": "1",
            "DOCKER_AUTH_CONFIG": "synthetic-auth",
            "DOCKER_CUSTOM_HEADERS": "synthetic",
            "DOCKER_API_VERSION": "bad",
        }
        with mock.patch.dict(os.environ, inherited):
            environment = native._native_environment(directory)
            self.assertEqual(
                {"DOCKER_CONFIG": str(directory)},
                {
                    key: value
                    for key, value in environment.items()
                    if key.startswith("DOCKER_")
                },
            )
            self.assertEqual("tcp://private.invalid", os.environ["DOCKER_HOST"])
        with mock.patch.object(native.subprocess, "run") as execute:
            native._native_call("/usr/bin/docker", ["version"], config_dir=directory)
        self.assertEqual(
            ["/usr/bin/docker", "--context", "default", "version"],
            execute.call_args.args[0],
        )
        self.assertEqual(
            str(directory), execute.call_args.kwargs["env"]["DOCKER_CONFIG"]
        )
        (directory / "config.json").write_text("{}")
        with self.assertRaises(ValueError):
            native._native_environment(directory)

    def test_unreleased_helper_is_reaped_and_cannot_dispatch(self):
        root, config = self._dispatch_fixture()
        helper = native.OwnedDispatch(root)
        result = helper.finish(cancel=True)
        self.assertTrue(result["reaped"] and result["group_gone"])
        self.assertTrue(result["control_closed"] and result["future_dispatch_disabled"])
        self.assertFalse(Path(config["dispatch_result"]).exists())
        with self.assertRaises(ValueError):
            helper.release()


if __name__ == "__main__":
    unittest.main()
