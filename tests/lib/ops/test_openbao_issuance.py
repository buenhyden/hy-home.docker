"""Offline regression tests; never authenticate against HOME OpenBao."""

import importlib.util
import json
import os
import signal
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "infra/03-security/openbao"


class IssuancePolicyTests(unittest.TestCase):
    def test_operator_cannot_issue_renderer_secret_id_directly(self):
        policy = (BASE / "config/policies/operator.hcl").read_text()
        self.assertNotIn('path "auth/approle/role/hy-home-renderer/secret-id"', policy)
        self.assertIn('path "auth/token/create/renderer-issuer"', policy)
        self.assertIn('path "auth/token/create/renderer-cleanup"', policy)


SPEC = importlib.util.spec_from_file_location(
    "renderer_issuance", BASE / "scripts/renderer-issuance.py"
)
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)
REV = "a" * 40
WHEN = 1791615600


class FakeAPI:
    def __init__(self, failure=None):
        self.data = {}
        self.destroyed = []
        self.failure = failure
        self.calls = []
        self.generation = "2026-10-10T07:00:01Z"
        self.functional = True
        self.running = False
        self.journal = None

    def issue(self, metadata):
        assert self.journal.load().state == "issuing"
        self.calls.append("issue")
        self.data["synthetic-accessor"] = {
            "metadata": metadata,
            "creation_time": M.utc(WHEN + 1),
        }
        if self.failure == "issue":
            raise M.Blocked()
        if self.failure == "kill":
            raise SystemExit(137)
        return "synthetic-wrapped-token"

    def deliver(self, wrapped):
        self.calls.append("deliver")
        if self.failure in {"deliver", "term"}:
            raise InterruptedError()

    def start(self):
        self.calls.append("start")
        if self.failure == "start":
            raise M.Blocked()
        self.running = True
        self.data.clear()  # One-use SecretID consumed by synthetic current process.
        return self.generation

    def stopped(self):
        return not self.running

    def recovery_generation(self, issued_at):
        return self.generation if self.running else None

    def ready(self, generation):
        self.calls.append("ready")
        return self.functional and generation == self.generation

    def accessors(self):
        if self.failure == "sealed":
            raise M.Blocked()
        return list(self.data)

    def lookup(self, accessor):
        if self.failure == "denied":
            raise M.Blocked()
        return self.data[accessor]

    def destroy(self, accessor):
        self.destroyed.append(accessor)
        if self.failure != "destroy-unconfirmed":
            self.data.pop(accessor)


class JournalTests(unittest.TestCase):
    def test_private_atomic_roundtrip_contains_no_credentials_or_accessor(self):
        with tempfile.TemporaryDirectory() as directory:
            with M.Journal(directory) as journal:
                record = M.Record("1" * 32, M.utc(WHEN), M.ROLE, REV, M.MANIFEST)
                journal.save(record)
                self.assertEqual(record, journal.load())
                path = Path(directory) / "issuance.json"
                self.assertEqual(0o600, path.stat().st_mode & 0o777)
                self.assertNotIn("token", path.read_text())
                self.assertNotIn("accessor", path.read_text())
                self.assertFalse((Path(directory) / "issuance.pending").exists())
                journal.clear()
                self.assertIsNone(journal.load())

    def test_symlink_hardlink_world_readable_and_partial_fail_closed(self):
        for case in ("symlink", "hardlink", "public", "partial", "invalid", "extra"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / "issuance.json"
                if case == "symlink":
                    target.symlink_to("outside")
                elif case == "partial":
                    (Path(directory) / "issuance.json.pending").write_text("{")
                else:
                    target.write_text("{}" if case != "extra" else '{"secret":"bad"}')
                    target.chmod(0o600 if case != "public" else 0o644)
                    if case == "hardlink":
                        os.link(target, Path(directory) / "copy")
                with (
                    M.Journal(directory) as journal,
                    self.assertRaises((M.Blocked, OSError)),
                ):
                    journal.load()

    def test_concurrent_operator_fails_before_issuance(self):
        with tempfile.TemporaryDirectory() as directory, M.Journal(directory):
            with self.assertRaises(M.Blocked):
                with M.Journal(directory):
                    self.fail("second operator acquired journal")

    def test_public_or_symlink_directory_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "public"
            path.mkdir(mode=0o755)
            with self.assertRaises(M.Blocked):
                M.Journal(path)
            link = Path(directory) / "link"
            link.symlink_to(directory)
            with self.assertRaises(M.Blocked):
                M.Journal(link)


class IssuanceRecoveryTests(unittest.TestCase):
    def run_case(self, api, journal):
        api.journal = journal
        return M.run_issuance(
            api, journal, revision=REV, clock=lambda: WHEN, nonce=lambda _: "1" * 32
        )

    def test_success_requires_authentication_then_accessor_absence(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            M.Journal(directory) as journal,
        ):
            api = FakeAPI()
            self.assertEqual("authenticated", self.run_case(api, journal))
            self.assertEqual(["issue", "deliver", "start", "ready"], api.calls)
            self.assertIsNone(journal.load())

    def test_failure_after_creation_delivery_and_sigterm_revokes_exact_id(self):
        for failure in ("issue", "deliver", "term"):
            with (
                self.subTest(failure=failure),
                tempfile.TemporaryDirectory() as directory,
            ):
                with M.Journal(directory) as journal:
                    api = FakeAPI(failure)
                    with self.assertRaises(M.Blocked):
                        self.run_case(api, journal)
                    self.assertEqual(["synthetic-accessor"], api.destroyed)
                    self.assertIsNone(journal.load())

    def test_delivery_without_new_process_generation_retains_journal(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            M.Journal(directory) as journal,
        ):
            api = FakeAPI("start")
            with self.assertRaises(M.Blocked):
                self.run_case(api, journal)
            self.assertEqual("delivered", journal.load().state)
            self.assertIsNone(journal.load().agent_started_at)
            self.assertEqual("reconciled", self.run_case(api, journal))
            self.assertEqual(["issue", "deliver", "start"], api.calls)
            self.assertEqual(["synthetic-accessor"], api.destroyed)

    def test_health_failure_retains_until_matching_generation_is_ready(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            M.Journal(directory) as journal,
        ):
            api = FakeAPI()
            api.functional = False
            with self.assertRaises(M.Blocked):
                self.run_case(api, journal)
            self.assertEqual("delivered", journal.load().state)
            api.functional = True
            self.assertEqual("reconciled", self.run_case(api, journal))
            self.assertEqual(1, api.calls.count("issue"))

    def test_sigkill_then_restart_cleans_before_any_new_issue(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            M.Journal(directory) as journal,
        ):
            api = FakeAPI("kill")
            with self.assertRaises(SystemExit):
                self.run_case(api, journal)
            self.assertEqual("issuing", journal.load().state)
            api.failure = None
            self.assertEqual("reconciled", self.run_case(api, journal))
            self.assertEqual(1, api.calls.count("issue"))
            self.assertEqual(["synthetic-accessor"], api.destroyed)

    def test_unknown_nonce_time_role_duplicate_and_access_denial_block(self):
        for case in (
            "nonce",
            "time",
            "role",
            "duplicate",
            "none",
            "sealed",
            "denied",
            "malformed",
            "destroy-unconfirmed",
        ):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                with M.Journal(directory) as journal:
                    record = M.Record("1" * 32, M.utc(WHEN), M.ROLE, REV, M.MANIFEST)
                    journal.save(record)
                    api = FakeAPI(case)
                    api.data["one"] = {
                        "metadata": record.metadata(),
                        "creation_time": M.utc(WHEN + 1),
                    }
                    if case == "nonce":
                        api.data["one"]["metadata"]["sec01_nonce"] = "2" * 32
                    elif case == "role":
                        api.data["one"]["metadata"]["sec01_role"] = "other-role"
                    elif case == "time":
                        api.data["one"]["creation_time"] = M.utc(WHEN + 61)
                    elif case == "duplicate":
                        api.data["two"] = dict(api.data["one"])
                    elif case == "none":
                        api.data.clear()
                    elif case == "malformed":
                        api.data["one"] = {"metadata": None}
                    with self.assertRaises(M.Blocked):
                        self.run_case(api, journal)
                    self.assertIsNotNone(journal.load())
                    self.assertNotIn("issue", api.calls)
                    if case != "destroy-unconfirmed":
                        self.assertEqual([], api.destroyed)

    def test_other_nonce_accessor_is_never_destroyed(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            M.Journal(directory) as journal,
        ):
            record = M.Record("1" * 32, M.utc(WHEN), M.ROLE, REV, M.MANIFEST)
            journal.save(record)
            api = FakeAPI()
            api.data["ours"] = {
                "metadata": record.metadata(),
                "creation_time": M.utc(WHEN + 1),
            }
            api.data["other"] = {
                "metadata": {"sec01_nonce": "2" * 32},
                "creation_time": M.utc(WHEN + 1),
            }
            self.assertEqual("reconciled", self.run_case(api, journal))
            self.assertEqual(["ours"], api.destroyed)
            self.assertIn("other", api.data)


class TransportTests(unittest.TestCase):
    def test_tokens_metadata_and_accessors_never_appear_in_argv(self):
        api = M.DockerAPI(
            "server", "volume", "agent", "synthetic-issuer", "synthetic-cleanup"
        )
        responses = [
            json.dumps({"wrap_info": {"token": "synthetic-wrap"}}).encode(),
            b"",
            b"{}",
        ]
        observed = []

        def command(argv, **kwargs):
            observed.append((argv, kwargs.get("payload")))
            return responses.pop(0)

        with patch.object(api, "command", side_effect=command):
            api.issue({"nonce": "synthetic-nonce"})
            api.destroy("synthetic-accessor")
            api.lookup("synthetic-accessor")
        for argv, body in observed:
            for sensitive in (
                "synthetic-issuer",
                "synthetic-cleanup",
                "synthetic-accessor",
                "synthetic-nonce",
            ):
                self.assertNotIn(sensitive, " ".join(argv))
            self.assertIsInstance(body, bytes)

    def test_transport_failure_never_includes_original_stderr(self):
        response = subprocess.CompletedProcess(
            [], 2, b"", b"synthetic-sensitive-server-error"
        )
        with patch.object(M.subprocess, "run", return_value=response):
            with self.assertRaises(M.Blocked) as caught:
                M.DockerAPI.command(["docker"])
            self.assertEqual("", str(caught.exception))

    def test_empty_list_not_confused_with_permission_failure(self):
        responses = [
            subprocess.CompletedProcess(
                [], 2, b"", ("No value found at " + M.PREFIX + "/secret-id\n").encode()
            ),
            subprocess.CompletedProcess(
                [], 2, b"", b"Error making API request: permission denied"
            ),
        ]
        with patch.object(M.subprocess, "run", side_effect=responses):
            value = M.DockerAPI.command(
                ["docker"], empty_list_path=M.PREFIX + "/secret-id"
            )
            self.assertEqual([], json.loads(value)["data"]["keys"])
            with self.assertRaises(M.Blocked):
                M.DockerAPI.command(["docker"], empty_list_path=M.PREFIX + "/secret-id")

    def test_native_json_empty_list_sentinel_is_not_permission_success(self):
        for stderr in (b"", b"permission denied"):
            response = subprocess.CompletedProcess([], 2, b"{}\n", stderr)
            with patch.object(M.subprocess, "run", return_value=response):
                if stderr:
                    with self.assertRaises(M.Blocked):
                        M.DockerAPI.command(
                            ["docker"], empty_list_path=M.PREFIX + "/secret-id"
                        )
                else:
                    value = M.DockerAPI.command(
                        ["docker"], empty_list_path=M.PREFIX + "/secret-id"
                    )
                    self.assertEqual([], json.loads(value)["data"]["keys"])
        for raw in (b"null", b"[]", b'{"errors":[]}', b'{"unexpected":true}'):
            response = subprocess.CompletedProcess([], 2, raw, b"")
            with patch.object(M.subprocess, "run", return_value=response):
                with self.assertRaises(M.Blocked):
                    M.DockerAPI.command(
                        ["docker"], empty_list_path=M.PREFIX + "/secret-id"
                    )

    def test_native_cli_accessor_array_validated_without_api_envelope(self):
        api = M.DockerAPI("server", "volume", "agent", "issuer", "cleanup")
        with patch.object(api, "request", return_value=["synthetic-accessor"]):
            self.assertEqual(["synthetic-accessor"], api.accessors())
        for response in (
            ["same", "same"],
            ["../escape"],
            [3],
            {"unexpected": []},
            None,
        ):
            with patch.object(api, "request", return_value=response):
                with self.assertRaises(M.Blocked):
                    api.accessors()

    def test_exact_cleanup_policy_and_short_roles(self):
        policy = (BASE / "config/policies/renderer-cleanup.hcl").read_text()
        self.assertNotIn("*", policy)
        resource = policy.split("# Self-identity")[0]
        self.assertNotIn('"read"', resource)
        self.assertNotIn('"create"', policy)
        self.assertNotIn("secret/data", policy)
        self.assertEqual(3, policy.count('path "' + M.PREFIX))
        for name in ("renderer-issuer", "renderer-cleanup"):
            role = json.loads(
                (BASE / "config" / (name + "-token-role.json")).read_text()
            )
            self.assertEqual([name], role["allowed_policies"])
            self.assertFalse(role["renewable"])
            self.assertTrue(role["token_no_default_policy"])
            self.assertEqual("5m", role["token_explicit_max_ttl"])


class ProcessInterruptionTests(unittest.TestCase):
    def test_actual_sigkill_preserves_durable_journal_and_restart_reconciles(self):
        child = """import importlib.util,sys,time
from pathlib import Path
s=importlib.util.spec_from_file_location("child_issuance",sys.argv[1])
m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
with m.Journal(sys.argv[2]) as j:
 j.save(m.Record("1"*32,m.utc(1791615600),m.ROLE,"a"*40,m.MANIFEST))
 Path(sys.argv[2],"synthetic-ready").touch()
 time.sleep(30)
"""
        with tempfile.TemporaryDirectory() as directory:
            process = subprocess.Popen(
                [
                    sys.executable,
                    "-c",
                    child,
                    str(BASE / "scripts/renderer-issuance.py"),
                    directory,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            try:
                import time

                for _ in range(100):
                    if (Path(directory) / "synthetic-ready").exists():
                        break
                    if process.poll() is not None:
                        self.fail("synthetic child failed before durable write")
                    time.sleep(0.01)
                self.assertTrue((Path(directory) / "synthetic-ready").exists())
                process.send_signal(signal.SIGKILL)
                self.assertEqual(-signal.SIGKILL, process.wait(timeout=5))
                with M.Journal(directory) as journal:
                    record = journal.load()
                    self.assertEqual("issuing", record.state)
                    api = FakeAPI()
                    api.data["one"] = {
                        "metadata": record.metadata(),
                        "creation_time": M.utc(WHEN + 1),
                    }
                    self.assertEqual(
                        "reconciled", M.run_issuance(api, journal, revision=REV)
                    )
                    self.assertNotIn("issue", api.calls)
                    self.assertIsNone(journal.load())
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait(timeout=5)

    def test_actual_sigterm_runs_matching_id_cleanup(self):
        child = """import importlib.util,sys,signal
s=importlib.util.spec_from_file_location("child_issuance",sys.argv[1])
m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
def interrupted(*_): raise InterruptedError()
signal.signal(signal.SIGTERM,interrupted)
class API:
 data={}
 def issue(self,metadata):
  self.data["synthetic-accessor"]={"metadata":metadata,"creation_time":m.utc(1791615601)}
  signal.raise_signal(signal.SIGTERM)
 def accessors(self):return list(self.data)
 def lookup(self,a):return self.data[a]
 def destroy(self,a):self.data.pop(a)
with m.Journal(sys.argv[2]) as j:
 try:m.run_issuance(API(),j,revision="a"*40,clock=lambda:1791615600,nonce=lambda _:"1"*32)
 except m.Blocked:sys.exit(0 if j.load() is None else 2)
 sys.exit(3)
"""
        with tempfile.TemporaryDirectory() as directory:
            done = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    child,
                    str(BASE / "scripts/renderer-issuance.py"),
                    directory,
                ],
                capture_output=True,
                timeout=10,
                check=False,
            )
            self.assertEqual(0, done.returncode)
            self.assertEqual(b"", done.stdout)
            self.assertEqual(b"", done.stderr)


class DockerBindingTests(unittest.TestCase):
    def test_pinned_platform_and_independent_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            agent = Path(directory) / "agent"
            agent.mkdir()
            journal = Path(directory) / "journal"
            journal.mkdir(mode=0o700)
            responses = [
                M.MANIFEST.encode(),
                (M.MANIFEST + " true").encode(),
                (M.MANIFEST + " volume exact-volume").encode(),
                b'{"entrypoint":["/bin/sh","/openbao/scripts/start-agent.sh"],"cmd":null}',
                str(agent).encode(),
            ]
            with patch.object(M.DockerAPI, "command", side_effect=responses):
                M.validate_binding("server", "exact-volume", "agent", journal)
            for index in range(5):
                invalid = list(responses)
                invalid[index] = b"unverified"
                with (
                    self.subTest(index=index),
                    patch.object(M.DockerAPI, "command", side_effect=invalid),
                ):
                    with self.assertRaises(M.Blocked):
                        M.validate_binding("server", "exact-volume", "agent", journal)
            nested = agent / "nested"
            nested.mkdir()
            with patch.object(M.DockerAPI, "command", side_effect=responses):
                with self.assertRaises(M.Blocked):
                    M.validate_binding("server", "exact-volume", "agent", nested)

    def test_adapter_accessor_and_wrapping_response_validation(self):
        api = M.DockerAPI(
            "server", "volume", "agent", "synthetic-issuer", "synthetic-cleanup"
        )
        for response in ({}, {"wrap_info": {"token": "space forbidden"}}):
            with patch.object(api, "request", return_value=response):
                with self.assertRaises(M.Blocked):
                    api.issue({})
        for keys in (None, ["duplicate", "duplicate"], ["bad/value"], [2]):
            with patch.object(api, "request", return_value={"data": {"keys": keys}}):
                with self.assertRaises(M.Blocked):
                    api.accessors()
        with patch.object(api, "request", return_value={"data": {"keys": ["valid"]}}):
            self.assertEqual(["valid"], api.accessors())
        with patch.object(api, "command", return_value=b"malformed-json"):
            with self.assertRaises(M.Blocked):
                api.request("list", M.PREFIX + "/secret-id")

    def test_delivery_hardening_and_generation_health(self):
        api = M.DockerAPI(
            "server", "volume", "agent", "synthetic-issuer", "synthetic-cleanup"
        )
        with patch.object(api, "command", return_value=b"") as call:
            api.deliver("synthetic-wrapped")
            argv = call.call_args.args[0]
            self.assertIn("--network=none", argv)
            self.assertIn("--read-only", argv)
            self.assertIn("--cap-drop=ALL", argv)
            self.assertNotIn("synthetic-wrapped", " ".join(argv))
        with patch.object(api, "command", side_effect=[b"", b"2026-10-10T07:00:01Z"]):
            self.assertEqual("2026-10-10T07:00:01Z", api.start())
        with patch.object(api, "command", side_effect=[b"", b"2026-10-10T07:00:01Z"]):
            self.assertTrue(api.ready("2026-10-10T07:00:01Z"))
        with patch.object(api, "command", side_effect=[b"", b"different-generation"]):
            self.assertFalse(api.ready("2026-10-10T07:00:01Z"))
        with (
            patch.object(api, "command", side_effect=M.Blocked),
            patch.object(M.time, "sleep"),
        ):
            self.assertFalse(api.ready("2026-10-10T07:00:01Z"))

    def test_main_rejects_invalid_public_arguments_before_docker(self):
        valid = ["server", "volume", M.IMAGE, "agent", "/tmp/journal", REV]
        cases = [
            [],
            ["bad/name", *valid[1:]],
            [*valid[:2], "openbao/openbao:latest", *valid[3:]],
            [*valid[:4], "relative", REV],
            [*valid[:5], "bad"],
        ]
        for args in cases:
            with self.subTest(args=args), patch.object(M.DockerAPI, "command") as call:
                with self.assertRaises(M.Blocked):
                    M.main(args)
                call.assert_not_called()

    def test_main_reads_separate_tokens_only_from_stdin(self):
        import io

        with tempfile.TemporaryDirectory() as directory:
            args = ["server", "volume", M.IMAGE, "agent", directory, REV]
            with (
                patch.object(
                    M.sys, "stdin", io.StringIO("synthetic-issuer\nsynthetic-cleanup\n")
                ),
                patch.object(M, "validate_binding"),
                patch.object(M, "validate_receipt"),
                patch.object(M.DockerAPI, "validate_tokens"),
                patch.object(M.DockerAPI, "command", return_value=b"false"),
                patch.object(M, "run_issuance", return_value="authenticated") as run,
            ):
                self.assertEqual(0, M.main(args))
                api = run.call_args.args[0]
                self.assertEqual("synthetic-issuer", api.issuer)
                self.assertEqual("synthetic-cleanup", api.cleanup)
            with (
                patch.object(M, "validate_receipt"),
                patch.object(M.sys, "stdin", io.StringIO("\n\n")),
            ):
                with self.assertRaises(M.Blocked):
                    M.main(args)


class EffectiveTokenTests(unittest.TestCase):
    @staticmethod
    def data(policy):
        return {
            "data": {
                "policies": [policy],
                "identity_policies": [],
                "renewable": False,
                "ttl": 299,
                "explicit_max_ttl": 300,
                "type": "service",
                "path": "auth/token/create/" + policy,
            }
        }

    def test_exact_short_nonrenewable_roles(self):
        api = M.DockerAPI(
            "server", "volume", "agent", "synthetic-issuer", "synthetic-cleanup"
        )
        with patch.object(
            api,
            "request",
            side_effect=[self.data("renderer-issuer"), self.data("renderer-cleanup")],
        ):
            api.validate_tokens()

    def test_admin_default_renewable_expired_excess_ttl_or_wrong_role_rejected(self):
        mutations = (
            ("policies", ["root"]),
            ("policies", ["renderer-issuer", "default"]),
            ("identity_policies", ["admin"]),
            ("renewable", True),
            ("ttl", 0),
            ("ttl", 301),
            ("ttl", True),
            ("explicit_max_ttl", 301),
            ("type", "batch"),
            ("path", "auth/token/create/other"),
        )
        for key, value in mutations:
            response = self.data("renderer-issuer")
            response["data"][key] = value
            api = M.DockerAPI(
                "server", "volume", "agent", "synthetic-issuer", "synthetic-cleanup"
            )
            with (
                self.subTest(key=key, value=value),
                patch.object(api, "request", return_value=response),
            ):
                with self.assertRaises(M.Blocked):
                    api.validate_tokens()


class LostJournalTests(unittest.TestCase):
    def test_lost_active_journal_prevents_new_issuance(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            M.Journal(directory) as journal,
        ):
            journal.save(M.Record("1" * 32, M.utc(WHEN), M.ROLE, REV, M.MANIFEST))
            (Path(directory) / "issuance.json").unlink()
            api = FakeAPI()
            with self.assertRaises(M.Blocked):
                M.run_issuance(api, journal, revision=REV)
            self.assertNotIn("issue", api.calls)

    def test_lost_anchor_or_duplicated_field_prevents_new_issuance(self):
        for case in ("lost", "duplicate"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                with M.Journal(directory) as journal:
                    journal.save(
                        M.Record("1" * 32, M.utc(WHEN), M.ROLE, REV, M.MANIFEST)
                    )
                    anchor = Path(directory) / "issuance.anchor"
                    if case == "lost":
                        anchor.unlink()
                    else:
                        anchor.write_text(
                            '{"nonce":"'
                            + "1" * 32
                            + '","state":"active","state":"complete"}'
                        )
                    with self.assertRaises(M.Blocked):
                        journal.load()


class BoundaryRecoveryTests(unittest.TestCase):
    def test_kill_after_delivery_before_start_or_after_start_before_journal(self):
        for boundary in ("before-start", "after-start"):
            with (
                self.subTest(boundary=boundary),
                tempfile.TemporaryDirectory() as directory,
            ):
                with M.Journal(directory) as journal:
                    api = FakeAPI()
                    api.journal = journal
                    normal_start = api.start

                    def interrupted_start(boundary=boundary, normal_start=normal_start):
                        if boundary == "after-start":
                            normal_start()
                        raise SystemExit(137)

                    with patch.object(api, "start", side_effect=interrupted_start):
                        with self.assertRaises(SystemExit):
                            M.run_issuance(
                                api,
                                journal,
                                revision=REV,
                                clock=lambda: WHEN,
                                nonce=lambda _: "1" * 32,
                            )
                    self.assertIsNone(journal.load().agent_started_at)
                    self.assertEqual(
                        "reconciled", M.run_issuance(api, journal, revision=REV)
                    )
                    self.assertEqual(1, api.calls.count("issue"))
                    self.assertIsNone(journal.load())
                    if boundary == "before-start":
                        self.assertEqual(["synthetic-accessor"], api.destroyed)

    def test_interrupted_clear_finishes_using_matching_completion_witness(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            M.Journal(directory) as journal,
        ):
            record = M.Record("1" * 32, M.utc(WHEN), M.ROLE, REV, M.MANIFEST)
            journal.save(record)
            journal._write_json(
                "issuance.anchor", {"nonce": record.nonce, "state": "complete"}
            )
            self.assertIsNone(journal.load())
            self.assertFalse((Path(directory) / "issuance.json").exists())

    def test_recovery_rejects_old_or_unparseable_running_generation(self):
        api = M.DockerAPI(
            "server", "volume", "agent", "synthetic-issuer", "synthetic-cleanup"
        )
        for generation in (M.utc(WHEN - 1), "not-a-time"):
            with (
                patch.object(api, "stopped", return_value=False),
                patch.object(api, "_started_at", return_value=generation),
            ):
                with self.assertRaises(M.Blocked):
                    api.recovery_generation(M.utc(WHEN))
        with patch.object(api, "stopped", return_value=True):
            self.assertIsNone(api.recovery_generation(M.utc(WHEN)))

    def test_symlink_wrapper_or_helper_and_writable_helper_never_execute(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            wrapper = root / "issue.sh"
            helper = root / "renderer-issuance.py"
            marker = root / "executed"
            helper.write_text(
                "from pathlib import Path\nPath(" + repr(str(marker)) + ").touch()\n"
            )
            wrapper.symlink_to(BASE / "scripts/issue-renderer-secret-id.sh")
            args = ["server", "volume", M.IMAGE, "agent", str(root), REV]
            done = subprocess.run(
                ["sh", str(wrapper), *args],
                input=b"synthetic-issuer\nsynthetic-cleanup\n",
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(0, done.returncode)
            self.assertFalse(marker.exists())
            wrapper.unlink()
            wrapper.write_text(
                (BASE / "scripts/issue-renderer-secret-id.sh").read_text()
            )
            wrapper.chmod(0o600)
            helper.chmod(0o666)
            done = subprocess.run(
                ["sh", str(wrapper), *args],
                input=b"synthetic-issuer\nsynthetic-cleanup\n",
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(0, done.returncode)
            self.assertFalse(marker.exists())
            helper.unlink()
            helper.symlink_to(BASE / "scripts/renderer-issuance.py")
            done = subprocess.run(
                ["sh", str(wrapper), *args],
                input=b"synthetic-issuer\nsynthetic-cleanup\n",
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(0, done.returncode)
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
