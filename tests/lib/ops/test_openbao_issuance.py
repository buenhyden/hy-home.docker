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
OLD = "synthetic-old-token"
NEW = "synthetic-new-token"


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
        # Live renderer tokens -> creation time; the stopped Agent's sink is OLD.
        self.tokens = {OLD: WHEN - 100}
        self.sink_token = OLD
        self.revoked = []

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
        if self.failure != "old-current":
            self.tokens[NEW] = WHEN + 2
            self.sink_token = NEW
        else:
            # Even a creation time that looks new cannot pass as the old token.
            self.tokens[OLD] = WHEN + 5
        return self.generation

    def stopped(self):
        return not self.running

    def stop(self):
        self.calls.append("stop")
        self.running = False

    def sink(self):
        return self.sink_token

    def lookup_self(self, token):
        if self.failure == "lookup-sealed":
            raise M.Uncertain()
        if token not in self.tokens:
            return None
        return {
            "policies": ["default", "renderer"],
            "path": "auth/approle/login",
            "meta": {"role_name": M.ROLE},
            "creation_time": self.tokens[token],
        }

    def revoke_self_allowed(self, token):
        return self.failure != "no-revoke-self"

    def revoke_self(self, token):
        self.calls.append("revoke")
        if self.failure == "revoke-lost":
            raise M.Uncertain()  # Request never reached the server.
        self.revoked.append(token)
        self.tokens.pop(token, None)
        if self.failure == "revoke-timeout":
            raise M.Uncertain()  # Revoked, but the reply was lost.

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


def anchor(directory):
    return json.loads((Path(directory) / "issuance.anchor").read_text())


def custody_dir(case):
    directory = tempfile.TemporaryDirectory()
    case.addCleanup(directory.cleanup)
    return M.Custody(directory.name, ("server", "volume", "1:2"))


class IssuanceRecoveryTests(unittest.TestCase):
    def run_case(self, api, journal, custody=None):
        api.journal = journal
        self.custody = custody or getattr(self, "custody", None) or custody_dir(self)
        return M.run_issuance(
            api,
            journal,
            revision=REV,
            custody=self.custody,
            clock=lambda: WHEN,
            nonce=lambda _: "1" * 32,
        )

    def test_success_requires_authentication_then_accessor_absence(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            M.Journal(directory) as journal,
        ):
            api = FakeAPI()
            self.assertEqual("authenticated", self.run_case(api, journal))
            self.assertEqual(
                ["issue", "deliver", "start", "ready", "revoke"], api.calls
            )
            self.assertIsNone(journal.load())
            self.assertEqual([OLD], api.revoked)
            self.assertIn(NEW, api.tokens)
            self.assertIsNone(self.custody.read())

    def test_new_issuance_binds_versioned_id_to_legacy_metadata_alias(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            M.Journal(directory) as journal,
        ):
            api = FakeAPI("kill")
            with self.assertRaises(SystemExit):
                self.run_case(api, journal)
            metadata = api.data["synthetic-accessor"]["metadata"]
            self.assertEqual(
                "1" * 32,
                metadata.get("issuance_id"),
                "new issuance must expose the version-bound identity",
            )
            self.assertEqual("3", metadata.get("issuance_schema"))
            self.assertEqual(metadata["issuance_id"], metadata["sec01_nonce"])
            self.assertEqual("issuing", journal.load().state)

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

    def test_start_failure_rolls_back_and_keeps_the_old_token(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            M.Journal(directory) as journal,
        ):
            api = FakeAPI("start")
            with self.assertRaises(M.Blocked):
                self.run_case(api, journal)
            self.assertIsNone(journal.load())
            self.assertEqual("rolled_back", anchor(directory)["state"])
            self.assertEqual(["issue", "deliver", "start", "stop"], api.calls)
            self.assertEqual(["synthetic-accessor"], api.destroyed)
            # The sink still held the old token: it is never revoked on rollback.
            self.assertEqual([], api.revoked)
            self.assertEqual(OLD, self.custody.read())

    def test_health_failure_revokes_only_the_new_token(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            M.Journal(directory) as journal,
        ):
            api = FakeAPI()
            api.functional = False
            with self.assertRaises(M.Blocked):
                self.run_case(api, journal)
            self.assertEqual([NEW], api.revoked)
            self.assertIn(OLD, api.tokens)
            self.assertEqual(OLD, self.custody.read())
            self.assertEqual("rolled_back", anchor(directory)["state"])
            # The next run takes the held old token as the one live generation.
            api.functional = True
            api.running = False
            self.assertEqual("authenticated", self.run_case(api, journal))
            self.assertEqual([NEW, OLD], api.revoked)
            self.assertIsNone(self.custody.read())
            self.assertEqual(2, api.calls.count("issue"))

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
                        "reconciled",
                        M.run_issuance(
                            api, journal, revision=REV, custody=custody_dir(self)
                        ),
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
 def sink(self):return None
with m.Journal(sys.argv[2]) as j:
 c=m.Custody(sys.argv[2],("s","v","j"))
 try:m.run_issuance(API(),j,revision="a"*40,custody=c,clock=lambda:1791615600,nonce=lambda _:"1"*32)
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
            "server",
            "volume",
            "agent",
            "synthetic-issuer",
            "synthetic-cleanup",
            request_script=":",
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
            "server",
            "volume",
            "agent",
            "synthetic-issuer",
            "synthetic-cleanup",
            request_script=":",
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

    def test_deliver_and_start_share_one_wrap_budget(self):
        api = M.DockerAPI(
            "server",
            "volume",
            "agent",
            "synthetic-issuer",
            "synthetic-cleanup",
            request_script=":",
        )
        clock = [1000.0]
        wrapped = {"wrap_info": {"token": "synthetic.wrapped"}}
        with (
            patch.object(M.time, "monotonic", side_effect=lambda: clock[0]),
            patch.object(api, "request", return_value=wrapped),
        ):
            api.deadline = 1240.0
            api.issue({})
            self.assertEqual(1045.0, api.wrap_deadline)

            def slow(argv, *, payload=None, seconds=20, empty_list_path=None):
                # Measured 11-19 s on 2026-10-27; above the old 20 s default.
                self.assertGreater(seconds, 20)
                self.assertLessEqual(seconds, 45)
                clock[0] += 21
                return b"2026-10-10T07:00:01Z"

            with patch.object(api, "command", side_effect=slow):
                api.deliver("synthetic-wrapped")
            # Start gets only what deliver left of the shared budget.
            with patch.object(api, "command") as call:
                call.return_value = b"2026-10-10T07:00:01Z"
                api.start()
                self.assertLessEqual(call.call_args_list[0].kwargs["seconds"], 24)
            # Too little wrap left after delivery: still issuing, so it raises.
            api.wrap_deadline = clock[0] + 30
            with patch.object(
                api,
                "command",
                side_effect=lambda *a, **k: clock.__setitem__(0, clock[0] + 25) or b"",
            ):
                with self.assertRaises(M.Blocked):
                    api.deliver("synthetic-wrapped")
            # Exhausted budget blocks before any container call.
            api.wrap_deadline = clock[0] + 3
            with patch.object(api, "command") as call:
                with self.assertRaises(M.Blocked):
                    api.deliver("synthetic-wrapped")
                call.assert_not_called()

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
                patch.object(M, "custody_directory", return_value=directory),
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
            "server",
            "volume",
            "agent",
            "synthetic-issuer",
            "synthetic-cleanup",
            request_script=":",
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
                "server",
                "volume",
                "agent",
                "synthetic-issuer",
                "synthetic-cleanup",
                request_script=":",
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
                M.run_issuance(api, journal, revision=REV, custody=custody_dir(self))
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
                    custody = custody_dir(self)
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
                                custody=custody,
                                clock=lambda: WHEN,
                                nonce=lambda _: "1" * 32,
                            )
                    self.assertIsNone(journal.load().agent_started_at)
                    self.assertEqual(
                        "reconciled",
                        M.run_issuance(api, journal, revision=REV, custody=custody),
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
            "server",
            "volume",
            "agent",
            "synthetic-issuer",
            "synthetic-cleanup",
            request_script=":",
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


def v2_record(state="delivered", started_at=None):
    return M.Record(
        "1" * 32,
        M.utc(WHEN),
        M.ROLE,
        REV,
        M.MANIFEST,
        state=state,
        agent_started_at=started_at,
        schema_version=2,
    )


class JournalV3Tests(IssuanceRecoveryTests.__base__):
    """Each v3 transition and its recovery, on a fake clock and fake bao."""

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.directory = directory.name
        self.journal = M.Journal(self.directory).__enter__()
        self.addCleanup(self.journal.__exit__)
        self.custody = custody_dir(self)

    def run_case(self, api):
        api.journal = self.journal
        return M.run_issuance(
            api,
            self.journal,
            revision=REV,
            custody=self.custody,
            clock=lambda: WHEN,
            nonce=lambda _: "1" * 32,
        )

    def test_current_v2_complete_anchor_reads_as_idle_and_moves_to_v3(self):
        # Shape of the HOME journal after the 2026-10-27 owner recovery.
        nonce = "f" * 32
        (Path(self.directory) / "issuance.anchor").write_text(
            json.dumps(
                {
                    "issuance_id": nonce,
                    "nonce": nonce,
                    "schema_version": 2,
                    "state": "complete",
                }
            )
        )
        (Path(self.directory) / "issuance.anchor").chmod(0o600)
        archived = Path(self.directory) / "issuance.json.recovered-20261027T172054"
        archived.write_text("{}")
        archived.chmod(0o600)
        self.assertIsNone(self.journal.load())
        api = FakeAPI()
        self.assertEqual("authenticated", self.run_case(api))
        self.assertEqual(3, anchor(self.directory)["schema_version"])
        self.assertEqual("complete", anchor(self.directory)["state"])
        self.assertTrue(archived.exists())

    def test_v2_delivered_stopped_and_consumed_self_reconciles(self):
        # 2026-10-27 second run: SecretID consumed, Agent stopped, journal delivered.
        self.journal.save(v2_record(started_at="2026-10-27T08:14:02Z"))
        api = FakeAPI()
        api.tokens[NEW] = WHEN + 7
        api.sink_token = NEW
        self.assertEqual("reconciled", self.run_case(api))
        self.assertEqual([NEW], api.revoked)
        self.assertIn(OLD, api.tokens)
        self.assertEqual(
            {"issuance_id": "1" * 32, "nonce": "1" * 32}
            | {"schema_version": 2, "state": "complete"},
            anchor(self.directory),
        )
        self.assertNotIn("issue", api.calls)

    def test_rollback_leaves_an_older_sink_token_alone(self):
        # v2 has no custody; the stopped sink still holds the pre-issuance token.
        self.journal.save(v2_record())
        api = FakeAPI()
        api.data["synthetic-accessor"] = {
            "metadata": v2_record().metadata(),
            "creation_time": M.utc(WHEN + 1),
        }
        self.assertEqual("reconciled", self.run_case(api))
        self.assertEqual(["synthetic-accessor"], api.destroyed)
        self.assertEqual([], api.revoked)
        self.assertIn(OLD, api.tokens)

    def test_v2_delivered_ready_keeps_legacy_completion(self):
        self.journal.save(v2_record(started_at=FakeAPI().generation))
        api = FakeAPI()
        api.running = True
        self.assertEqual("reconciled", self.run_case(api))
        self.assertEqual([], api.revoked)
        self.assertEqual("complete", anchor(self.directory)["state"])

    def test_v3_delivered_stopped_rolls_back_on_resume(self):
        api = FakeAPI()
        normal_ready = api.ready
        with patch.object(api, "ready", side_effect=SystemExit(137)):
            with self.assertRaises(SystemExit):
                self.run_case(api)
        self.assertEqual("delivered", self.journal.load().state)
        api.running = False  # Someone stopped the Agent, as on 2026-10-27.
        api.ready = normal_ready
        self.assertEqual("reconciled", self.run_case(api))
        self.assertEqual([NEW], api.revoked)
        self.assertEqual(OLD, self.custody.read())
        self.assertEqual("rolled_back", anchor(self.directory)["state"])

    def test_foreign_running_generation_is_never_rolled_back(self):
        self.journal.save(v2_record(started_at="2026-10-27T08:14:02Z"))
        api = FakeAPI()
        api.running = True
        api.generation = "2026-10-27T08:21:50Z"
        api.recovery_generation = lambda issued_at: api.generation
        with self.assertRaises(M.Blocked):
            self.run_case(api)
        self.assertNotIn("stop", api.calls)
        self.assertEqual([], api.revoked)

    def test_kill_in_prepared_closes_rolled_back_without_issue(self):
        api = FakeAPI()
        with patch.object(api, "sink", side_effect=SystemExit(137)):
            with self.assertRaises(SystemExit):
                self.run_case(api)
        self.assertEqual("prepared", self.journal.load().state)
        self.assertEqual("reconciled", self.run_case(api))
        self.assertEqual("rolled_back", anchor(self.directory)["state"])
        self.assertNotIn("issue", api.calls)

    def test_prepare_failures_block_before_any_secret_id(self):
        for case in ("multiple", "no-revoke-self", "lookup-sealed", "unsafe"):
            with self.subTest(case=case):
                self.setUp()
                api = FakeAPI(None if case in {"multiple", "unsafe"} else case)
                if case == "multiple":
                    self.custody.write("synthetic-other-token")
                    api.tokens["synthetic-other-token"] = WHEN - 50
                if case == "unsafe":
                    self.custody.write(OLD)
                    (Path(self.custody.directory) / self.custody.name).chmod(0o644)
                with self.assertRaises(M.Blocked):
                    self.run_case(api)
                self.assertNotIn("issue", api.calls)
                self.assertEqual([], api.revoked)
                self.assertEqual("rolled_back", anchor(self.directory)["state"])

    def test_no_live_old_generation_completes_without_revoke(self):
        for sink in (None, "synthetic-expired-token"):
            with self.subTest(sink=sink):
                self.setUp()
                api = FakeAPI()
                api.tokens.pop(OLD)
                api.sink_token = sink
                self.assertEqual("authenticated", self.run_case(api))
                self.assertEqual([], api.revoked)
                self.assertEqual("complete", anchor(self.directory)["state"])

    def test_old_equals_current_sink_rolls_back_without_revoking_old(self):
        api = FakeAPI("old-current")
        with self.assertRaises(M.Blocked):
            self.run_case(api)
        self.assertEqual([], api.revoked)
        self.assertIn(OLD, api.tokens)
        self.assertEqual(OLD, self.custody.read())
        self.assertEqual("rolled_back", anchor(self.directory)["state"])

    def test_kill_after_verified_resumes_revoke(self):
        api = FakeAPI()
        with patch.object(M, "revoke_old", side_effect=SystemExit(137)):
            with self.assertRaises(SystemExit):
                self.run_case(api)
        self.assertEqual("verified", self.journal.load().state)
        self.assertEqual("reconciled", self.run_case(api))
        self.assertEqual([OLD], api.revoked)
        self.assertIsNone(self.custody.read())
        self.assertEqual("complete", anchor(self.directory)["state"])

    def test_revoke_timeout_stays_revoking_then_reconciles(self):
        for failure, revokes in (("revoke-timeout", 1), ("revoke-lost", 2)):
            with self.subTest(failure=failure):
                self.setUp()
                api = FakeAPI(failure)
                with self.assertRaises(M.Uncertain):
                    self.run_case(api)
                self.assertEqual("revoking", self.journal.load().state)
                self.assertEqual(OLD, self.custody.read())
                api.failure = None
                self.assertEqual("reconciled", self.run_case(api))
                self.assertEqual(revokes, api.calls.count("revoke"))
                self.assertNotIn(OLD, api.tokens)
                self.assertIsNone(self.custody.read())
                self.assertEqual("complete", anchor(self.directory)["state"])

    def test_revoking_with_lost_or_changed_custody_blocks(self):
        for case in ("lost", "changed"):
            with self.subTest(case=case):
                self.setUp()
                api = FakeAPI("revoke-lost")
                with self.assertRaises(M.Uncertain):
                    self.run_case(api)
                api.failure = None
                if case == "lost":
                    self.custody.destroy()  # tmpfs gone after a reboot.
                else:
                    api.tokens[OLD] = WHEN - 1
                with self.assertRaises(M.Blocked):
                    self.run_case(api)
                self.assertEqual("revoking", self.journal.load().state)
                self.assertIn(OLD, api.tokens)

    def test_denied_before_revoke_intent_never_completes(self):
        api = FakeAPI()
        normal_finish = M.finish

        def deny_old_then_finish(*args):
            api.tokens.pop(OLD)  # 403 for a reason other than this revoke.
            return normal_finish(*args)

        with patch.object(M, "finish", side_effect=deny_old_then_finish):
            with self.assertRaises(M.Blocked):
                self.run_case(api)
        self.assertEqual("verified", self.journal.load().state)
        self.assertEqual(OLD, self.custody.read())
        self.assertNotIn("revoke", api.calls)

    def test_custody_is_bound_to_server_volume_and_journal(self):
        other = M.Custody(self.custody.directory, ("restore", "volume", "9:9"))
        self.custody.write(OLD)
        self.assertIsNone(other.read())
        other.destroy()
        self.assertEqual(OLD, self.custody.read())

    def test_stale_custody_pending_is_replaced_and_destroyed(self):
        pending = Path(self.custody.directory) / (self.custody.name + ".pending")
        pending.write_text(OLD)
        pending.chmod(0o600)
        self.assertEqual("authenticated", self.run_case(FakeAPI()))
        self.assertFalse(pending.exists())
        self.assertIsNone(self.custody.read())

    def test_rolling_back_resume_never_stops_a_foreign_generation(self):
        api = FakeAPI()
        api.functional = False
        api.revoke_self_allowed = lambda token: token == OLD
        with self.assertRaises(M.Blocked):
            self.run_case(api)
        self.assertEqual("rolling_back", self.journal.load().state)
        api.running = True
        api.generation = "2026-10-27T08:21:50Z"  # Owner's manual restart.
        api.recovery_generation = lambda issued_at: api.generation
        api.calls.clear()
        with self.assertRaises(M.Blocked):
            self.run_case(api)
        self.assertNotIn("stop", api.calls)

    def test_rolling_back_without_saved_generation_never_stops_a_running_agent(self):
        api = FakeAPI("start")  # start() raises before agent_started_at is saved.
        api.revoke_self_allowed = lambda token: False
        api.sink_token = None
        api.tokens.pop(OLD)
        self.journal.save(
            M.Record(
                "1" * 32,
                M.utc(WHEN),
                M.ROLE,
                REV,
                M.MANIFEST,
                state="rolling_back",
                schema_version=3,
            )
        )
        api.running = True  # Started by hand after the interrupted rollback.
        api.recovery_generation = lambda issued_at: api.generation
        with self.assertRaises(M.Blocked):
            self.run_case(api)
        self.assertNotIn("stop", api.calls)
        self.assertEqual("rolling_back", self.journal.load().state)

    def test_rollback_preflight_failure_keeps_rolling_back(self):
        api = FakeAPI()
        api.functional = False
        api.revoke_self_allowed = lambda token: token == OLD
        with self.assertRaises(M.Blocked):
            self.run_case(api)
        self.assertEqual("rolling_back", self.journal.load().state)
        self.assertIn(NEW, api.tokens)
        api.revoke_self_allowed = lambda token: True
        self.assertEqual("reconciled", self.run_case(api))
        self.assertEqual([NEW], api.revoked)
        self.assertEqual("rolled_back", anchor(self.directory)["state"])

    def test_v3_document_roundtrip_has_no_token_or_accessor(self):
        record = M.Record(
            "1" * 32,
            M.utc(WHEN),
            M.ROLE,
            REV,
            M.MANIFEST,
            state="revoking",
            agent_started_at="2026-10-10T07:00:01Z",
            schema_version=3,
            old_created=WHEN - 100,
        )
        self.journal.save(record)
        self.assertEqual(record, self.journal.load())
        text = (Path(self.directory) / "issuance.json").read_text()
        self.assertNotIn("token", text)
        self.assertNotIn("accessor", text)
        for bad in (
            {"old_created": WHEN + 1},
            {"old_created": True},
            {"schema_version": 2},
            {"state": "complete"},
        ):
            with self.subTest(bad=bad), self.assertRaises(M.Blocked):
                M.Record.from_document({**record.document(), **bad})
        with self.assertRaises(M.Blocked):
            M.Record.from_document({**record.document(), "secret": "x"})


class SelfTokenAdapterTests(unittest.TestCase):
    def api(self):
        return M.DockerAPI(
            "server",
            "volume",
            "agent",
            "synthetic-issuer",
            "synthetic-cleanup",
            request_script=":",
        )

    def test_only_self_token_403_is_denied(self):
        denied = subprocess.CompletedProcess(
            [], 2, b"", b"Error: Code: 403. Errors:\n* permission denied"
        )
        with patch.object(M.subprocess, "run", return_value=denied):
            with self.assertRaises(M.Denied):
                M.DockerAPI.command(["x"], denied=True)
            with self.assertRaises(M.Blocked) as caught:
                M.DockerAPI.command(["x"])
            self.assertNotIsInstance(caught.exception, M.Denied)
            api = self.api()
            self.assertIsNone(api.lookup_self("synthetic-old"))
            # A short-token 403 stays Uncertain, as before v3.
            with self.assertRaises(M.Uncertain):
                api.request("read", "auth/token/lookup-self")
        sealed = subprocess.CompletedProcess([], 2, b"", b"Code: 503.")
        with patch.object(M.subprocess, "run", return_value=sealed):
            with self.assertRaises(M.Uncertain):
                self.api().lookup_self("synthetic-old")

    def test_self_token_rides_stdin_and_revoke_self_is_silent(self):
        api = self.api()
        with patch.object(api, "command", return_value=b"") as call:
            self.assertEqual(
                {},
                api.request(
                    "write -force", "auth/token/revoke-self", token="synthetic-old"
                ),
            )
            self.assertNotIn("synthetic-old", " ".join(call.call_args.args[0]))
            self.assertTrue(
                call.call_args.kwargs["payload"].startswith(b"synthetic-old\n")
            )
            self.assertTrue(call.call_args.kwargs["denied"])
        allowed = {"data": {"auth/token/revoke-self": ["update"]}}
        for response, result in (
            (allowed, True),
            ({"data": {"auth/token/revoke-self": "update"}}, False),
            ({"data": {"auth/token/revoke-self": ["deny"]}}, False),
            ({}, False),
        ):
            with patch.object(api, "request", return_value=response):
                self.assertIs(result, api.revoke_self_allowed("synthetic-old"))

    def test_sink_read_is_read_only_offline_and_bounded(self):
        api = self.api()
        with patch.object(api, "command", return_value=b"synthetic.token") as call:
            self.assertEqual("synthetic.token", api.sink())
            argv = call.call_args.args[0]
            self.assertIn("--network=none", argv)
            self.assertIn("--read-only", argv)
            self.assertIn("--log-driver=none", argv)
            self.assertIn(
                "type=volume,source=volume,target=/openbao/agent,readonly", argv
            )
        with patch.object(api, "command", return_value=b""):
            self.assertIsNone(api.sink())
        for raw in (b"bad token", b"x" * 1025):
            with patch.object(api, "command", return_value=raw):
                with self.assertRaises(M.Blocked):
                    api.sink()

    def test_custody_directory_must_be_owner_tmpfs(self):
        with patch(
            "builtins.open",
            unittest.mock.mock_open(read_data="x /run/user/1 ext4 rw 0 0\n"),
        ):
            with self.assertRaises(M.Blocked):
                M.custody_directory()


if __name__ == "__main__":
    unittest.main()
