# fmt: off
import importlib.util
import io
import itertools
import json
import os
import stat
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "infra/03-security/openbao/scripts/protected-semantic-restore.py"
EXECUTION_SOURCE = ROOT / "infra/03-security/openbao/scripts/protected-semantic-execution.py"
def load_source():
    spec = importlib.util.spec_from_file_location("protected_semantic_restore", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
def load_execution():
    spec = importlib.util.spec_from_file_location("protected_semantic_execution_test", EXECUTION_SOURCE)
    module = importlib.util.module_from_spec(spec)
    __import__("sys").modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
class FakeResponse:
    def __init__(self, status, document, *, headers=()):
        self.status = status
        self.headers = list(headers)
        self.raw = json.dumps(document).encode()

    def getheaders(self):
        return self.headers

    def read(self, maximum):
        return self.raw[:maximum]
class FakeConnection:
    responses = None
    calls = None

    def __init__(self, *_args, **_kwargs):
        pass

    def request(self, method, path, body=None, headers=None):
        self.calls.append((method, path, body, dict(headers or {})))

    def getresponse(self):
        return self.responses.pop(0)

    def abort(self):
        pass

    def close(self):
        pass
class Parent:
    PinnedConnection = FakeConnection

    @staticmethod
    def parse_response(raw):
        return json.loads(raw)

    class Blocked(Exception):
        pass
def kv(value, version=4, *, destroyed=False, deletion_time=""):
    return {
        "data": {
            "data": {"admin_password": value, "unrelated": "discard-me"},
            "metadata": {
                "version": version,
                "destroyed": destroyed,
                "deletion_time": deletion_time,
            },
        }
    }
class CanaryTests(unittest.TestCase):
    def setUp(self):
        self.subject = load_source()
        FakeConnection.responses = []
        FakeConnection.calls = []

    def test_reads_only_two_fixed_routes_and_retains_value_and_version(self):
        FakeConnection.responses = [
            FakeResponse(200, kv("keycloak-sentinel", 7)),
            FakeResponse(200, kv("grafana-sentinel", 9)),
        ]
        reader = self.subject.LiveCanaries(Parent, "token", object(), "192.0.2.4")
        self.assertEqual(
            reader.read_all(),
            (("keycloak-sentinel", 7), ("grafana-sentinel", 9)),
        )
        self.assertEqual(
            [(method, path) for method, path, _body, _headers in FakeConnection.calls],
            [
                ("GET", "/v1/secret/data/hy-home/02-auth/keycloak"),
                ("GET", "/v1/secret/data/hy-home/06-observability/grafana"),
            ],
        )
        self.assertTrue(all(call[2] is None for call in FakeConnection.calls))

    def test_rejects_redirect_non_200_and_invalid_kv_shapes(self):
        bad = [
            FakeResponse(302, kv("x"), headers=(("Location", "https://other"),)),
            FakeResponse(403, {}),
            FakeResponse(200, kv("x", True)),
            FakeResponse(200, kv("x", 0)),
            FakeResponse(200, kv("x", destroyed=True)),
            FakeResponse(200, kv("x", deletion_time="2026-10-14T00:00:00Z")),
            FakeResponse(200, kv("", 1)),
            FakeResponse(200, {"data": {"data": {}, "metadata": {"version": 1}}}),
        ]
        for response in bad:
            with self.subTest(status=response.status, body=response.raw):
                FakeConnection.responses = [response]
                with self.assertRaises(self.subject.Blocked):
                    self.subject.LiveCanaries(Parent, "token", object(), "192.0.2.4").read_all()

    def test_third_route_and_writes_are_not_exposed(self):
        self.assertEqual(
            self.subject.CANARIES,
            (
                ("secret/data/hy-home/02-auth/keycloak", "admin_password"),
                ("secret/data/hy-home/06-observability/grafana", "admin_password"),
            ),
        )
        self.assertFalse(hasattr(self.subject.LiveCanaries, "request"))


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.subject = load_source()
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        self.snapshot = self.root / "raft.snap"
        self.receipt = self.root / "raft.snap.receipt.json"
        self.lease = self.root / "quiescence.json"
        for path, raw in (
            (self.snapshot, b"snapshot"),
            (self.receipt, b"{}"),
            (
                self.lease,
                json.dumps(
                    {
                        "schema_version": 1,
                        "lease_id": "a" * 32,
                        "started_at_utc": "2026-10-14T00:00:00+00:00",
                        "expires_at_utc": "2999-10-14T00:00:00+00:00",
                        "released_at_utc": None,
                        "snapshot_sha256": "b" * 64,
                    }
                ).encode(),
            ),
        ):
            path.write_bytes(raw)
            path.chmod(0o600)

    def tearDown(self):
        self.directory.cleanup()

    def test_no_effect_until_both_gets_and_post_read_rechecks_pass(self):
        admission = mock.Mock()
        reader = mock.Mock()
        effects = mock.Mock()
        reference = (("one", 1), ("two", 2))
        reader.read_all.return_value = reference
        self.subject.orchestrate(admission, reader, effects)
        self.assertEqual(
            admission.method_calls,
            [mock.call.pre_read(), mock.call.post_read()],
        )
        effects.perform.assert_called_once_with(reference)

    def test_read_or_recheck_failure_has_zero_effects(self):
        for failure in ("pre", "read", "post"):
            admission = mock.Mock()
            reader = mock.Mock()
            effects = mock.Mock()
            if failure == "pre":
                admission.pre_read.side_effect = self.subject.Blocked()
            elif failure == "read":
                reader.read_all.side_effect = self.subject.Blocked()
            else:
                reader.read_all.return_value = (("one", 1), ("two", 2))
                admission.post_read.side_effect = self.subject.Blocked()
            with self.subTest(failure=failure), self.assertRaises(self.subject.Blocked):
                self.subject.orchestrate(admission, reader, effects)
            effects.perform.assert_not_called()

    def test_lease_change_expiry_or_release_blocks(self):
        descriptor = os.open(self.lease, os.O_RDONLY)
        self.addCleanup(os.close, descriptor)
        digest = __import__("hashlib").sha256(self.lease.read_bytes()).hexdigest()
        lease = self.subject.QuiescenceLease(descriptor, "a" * 32, "b" * 64, digest)
        lease.recheck("2026-10-14T00:00:01+00:00", now=2000000000)
        with self.assertRaises(self.subject.Blocked):
            lease.recheck("2026-10-14T00:00:01+00:00", now=0)
        with self.assertRaises(self.subject.Blocked):
            lease.recheck("2026-10-13T23:59:59+00:00", now=2000000000)
        changed = json.loads(self.lease.read_text())
        changed["released_at_utc"] = "2026-10-14T00:01:00+00:00"
        self.lease.write_text(json.dumps(changed))
        with self.assertRaises(self.subject.Blocked):
            lease.recheck("2026-10-14T00:00:01+00:00", now=2000000000)

    def test_lease_fd_must_match_protected_digest(self):
        descriptor = os.open(self.lease, os.O_RDONLY)
        self.addCleanup(os.close, descriptor)
        with self.assertRaises(self.subject.Blocked):
            self.subject.QuiescenceLease(descriptor, "a" * 32, "b" * 64, "c" * 64)


class CommandAndSecretTests(unittest.TestCase):
    def setUp(self):
        self.subject = load_source()

    def test_container_profiles_are_frozen(self):
        self.assertEqual(
            self.subject.SERVER_LIMITS,
            (
                "--memory",
                "512m",
                "--memory-swap",
                "512m",
                "--cpus",
                "1",
                "--pids-limit",
                "512",
            ),
        )
        self.assertEqual(
            self.subject.SMALL_LIMITS,
            (
                "--memory",
                "32m",
                "--memory-swap",
                "32m",
                "--cpus",
                "0.25",
                "--pids-limit",
                "16",
            ),
        )
        base = self.subject.container_security(self.subject.SERVER_LIMITS)
        self.assertIn("--cap-drop", base)
        self.assertIn("no-new-privileges", base)
        self.assertIn("--read-only", base)

    def test_secret_sentinels_never_enter_public_receipt(self):
        reference = (("keycloak-sentinel", 3), ("grafana-sentinel", 5))
        receipt = self.subject.success_receipt(reference, "lease-id", "c" * 64, 12, 4)
        rendered = json.dumps(receipt)
        self.assertNotIn("sentinel", rendered)
        self.assertEqual(receipt["canaries_equal"], True)


class UtilityTests(unittest.TestCase):
    def setUp(self):
        self.subject = load_source()
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)

    def tearDown(self):
        self.directory.cleanup()

    def private(self, name, raw):
        path = self.root / name
        path.write_bytes(raw)
        path.chmod(0o600)
        return path

    def test_json_digest_and_held_file_guards(self):
        self.assertEqual(self.subject._unique([("a", 1)]), {"a": 1})
        with self.assertRaises(self.subject.Blocked):
            self.subject._unique([("a", 1), ("a", 2)])
        self.assertEqual(self.subject._json(b'{"a":[1]}'), {"a": [1]})
        for raw in (b"", b'{"a":1,"a":2}', b"[]" * 40000):
            with self.subTest(raw=raw[:20]), self.assertRaises(self.subject.Blocked):
                self.subject._json(raw)
        path = self.private("public.json", b'{"ok":true}')
        digest = __import__("hashlib").sha256(path.read_bytes()).hexdigest()
        descriptor, info = self.subject._open_held(path, digest, private=True)
        try:
            self.assertEqual(self.subject._digest_fd(descriptor, info.st_size), digest)
        finally:
            os.close(descriptor)
        with self.assertRaises(self.subject.Blocked):
            self.subject._open_held(path, "0" * 64, private=True)
        path.chmod(0o644)
        with self.assertRaises(self.subject.Blocked):
            self.subject._open_held(path, digest, private=True)

    def test_directory_and_reviewed_dependency_loaders(self):
        descriptor = self.subject._open_directory(self.root)
        os.close(descriptor)
        with self.assertRaises(self.subject.Blocked):
            self.subject._open_directory(Path("relative"))
        parent, archive, execution = self.subject.load_dependencies()
        self.assertEqual(parent.HOST, "openbao.hy.home.arpa")
        self.assertTrue(callable(archive.validate_archive))
        self.assertTrue(callable(execution.HeldBytes.open))

    def test_contract_accepts_only_exact_owned_inputs(self):
        candidate = "hy-home/openbao:2.7.1-go1.27.3-net0.60.0-r1@sha256:" + "a" * 64
        value = {
            "schema_version": 1,
            "attempt": self.subject.ATTEMPT,
            "target": str(self.subject.TARGET),
            "parent": {"dev": 2064, "ino": 115612004, "uid": 1000, "gid": 1000},
            "snapshot": {
                "sha256": "b" * 64,
                "receipt_sha256": "c" * 64,
                "dev": 1,
                "ino": 2,
                "size": 3,
                "cluster_id": self.subject.CLUSTER,
                "version": self.subject.OLD_VERSION,
                "raft_index": 4,
                "raft_term": 5,
            },
            "quiescence": {"lease_id": "d" * 32, "lease_sha256": "e" * 64},
            "candidate": {
                "reference": candidate,
                "image_id": "sha256:" + "f" * 64,
                "version": self.subject.OWNED_VERSION,
            },
            "renderer": {
                "helper": "/trusted/issue-renderer-secret-id.sh",
                "bundle": "/trusted/bundle",
                "revision": "1" * 40,
                "helper_receipt_sha256": "2" * 64,
                "bundle_receipt_sha256": "3" * 64,
            },
            "security_receipt_sha256": "4" * 64,
        }
        raw = json.dumps(value).encode()
        path = self.private("contract.json", raw)
        digest = __import__("hashlib").sha256(raw).hexdigest()
        execution = load_execution()
        contract, held = self.subject._contract(path, digest, execution)
        self.addCleanup(held.close)
        self.assertEqual(contract, value)
        for key, replacement in (
            ("target", "/wrong"),
            ("attempt", "wrong"),
            ("schema_version", 2),
        ):
            bad = {**value, key: replacement}
            raw = json.dumps(bad).encode()
            path.write_bytes(raw)
            with self.assertRaises(self.subject.Blocked):
                self.subject._contract(path, __import__("hashlib").sha256(raw).hexdigest(), execution)

    def test_secret_fd_and_hidden_input_modes(self):
        class SecretParent:
            @staticmethod
            def read_secret_fd(fd):
                return os.pread(fd, 100, 0).decode()

            @staticmethod
            def hidden_input(label):
                return label

            class Blocked(Exception):
                pass

        fds = []
        for number in range(4):
            path = self.private(str(number), f"secret-{number}".encode())
            fds.append(os.open(path, os.O_RDONLY))
        self.addCleanup(lambda: [os.close(fd) for fd in fds])
        options = SimpleNamespace(home_read_fd=fds[0], root_fd=fds[1], share_1_fd=fds[2], share_2_fd=fds[3])
        self.assertEqual(
            self.subject._secrets(SecretParent, options),
            ("secret-0", "secret-1", ("secret-2", "secret-3")),
        )
        hidden = SimpleNamespace(home_read_fd=None, root_fd=None, share_1_fd=None, share_2_fd=None)
        self.assertEqual(self.subject._secrets(SecretParent, hidden)[0], "HOME operator token")
        hidden.root_fd = fds[1]
        with self.assertRaises(self.subject.Blocked):
            self.subject._secrets(SecretParent, hidden)


class RuntimeUnitTests(unittest.TestCase):
    def setUp(self):
        self.subject = load_source()

    @staticmethod
    def result(stdout=b"", stderr=b"", returncode=0):
        return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)

    def effect(self):
        effect = self.subject.RecoveryEffects.__new__(self.subject.RecoveryEffects)
        effect.execution = load_execution()
        effect.held_artifacts = []
        effect.contract = {
            "candidate": {"reference": "candidate", "image_id": "candidate-id"},
            "snapshot": {"sha256": "a" * 64, "raft_index": 8, "raft_term": 2},
            "quiescence": {"lease_id": "b" * 32},
            "renderer": {
                "helper": "/trusted/helper",
                "bundle": "/trusted/bundle",
                "revision": "c" * 40,
                "helper_receipt_sha256": "d" * 64,
                "bundle_receipt_sha256": "e" * 64,
            },
        }
        effect.root_token = "root-secret"
        effect.shares = ("share-one", "share-two")
        effect.contract_digest = "f" * 64
        effect.ledger = None
        effect.reclaim_paths = effect.agent_id = None
        return effect

    def test_server_watcher_and_status_commands_are_bounded(self):
        effect = self.effect()
        runtime = mock.Mock()
        runtime.containers = []
        runtime.docker.return_value = self.result(stdout=b"true false")
        runtime.remember.side_effect = ["a" * 64, "b" * 64]
        effect.runtime = runtime
        effect.runner = SimpleNamespace(engine=SimpleNamespace(probe=None))
        with tempfile.TemporaryDirectory() as directory:
            effect._server("old", "image", Path(directory), "none")
        effect._watcher()
        effect._watcher_ok()
        create_calls = [c for c in runtime.docker.call_args_list if c.args[0] == "create"]
        self.assertEqual((len(create_calls), all("--label" in call.args for call in create_calls)), (2, True))
        server = create_calls[0].args
        self.assertIn("--memory-swap", server)
        self.assertIn("--network=none", create_calls[1].args)
        self.assertNotIn("--network-alias", server)
        # The image's own entrypoint writes BAO_LOCAL_CONFIG and adds -config;
        # neither image has /bin/bao, and the read-only root needs a config tmpfs.
        self.assertNotIn("--entrypoint", server)
        self.assertEqual(server[-2:], ("image", "server"))
        self.assertIn(
            "/openbao/config:rw,noexec,nosuid,nodev,size=1m,mode=0700,uid=100,gid=1000",
            server,
        )

    def test_wait_status_unseal_status_and_canaries(self):
        effect = self.effect()
        effect.runtime = mock.Mock()
        effect.runtime.exec.side_effect = [
            self.result(returncode=2, stdout=b"bad"),
            self.result(returncode=2, stdout=b'{"initialized":true,"sealed":true}'),
        ]
        self.assertTrue(effect._wait_status("server", True, True)["sealed"])
        # An unsealed node answers login and reads only once it is the active node.
        effect.runtime.exec.side_effect = [
            self.result(stdout=b'{"initialized":true,"sealed":false,"is_self":false}'),
            self.result(stdout=b'{"initialized":true,"sealed":false,"is_self":true}'),
        ]
        effect.runtime.exec.reset_mock()
        self.assertTrue(effect._wait_status("server", True, False)["is_self"])
        self.assertEqual(effect.runtime.exec.call_count, 2)
        effect._json_exec = mock.Mock(
            side_effect=[
                (
                    self.result(),
                    {
                        "sealed": False,
                        "cluster_id": self.subject.CLUSTER,
                        "version": self.subject.OLD_VERSION,
                        "storage_type": "raft",
                    },
                ),
                (self.result(), kv("one", 1)),
                (self.result(), kv("two", 2)),
                (self.result(), {}),
            ]
        )
        effect._status("server", self.subject.OLD_VERSION)
        self.assertEqual(effect._canaries("server"), (("one", 1), ("two", 2)))
        effect._unseal("server", "share-secret")
        self.assertNotIn("share-secret", repr(effect._json_exec.call_args.args))
        self.assertEqual(effect._json_exec.call_args.kwargs["input"], b"share-secret")
        # operator unseal refuses non-terminal stdin; the API path reads key=- from stdin.
        self.assertEqual(
            effect._json_exec.call_args.args[1:], ("write", "-format=json", "sys/unseal", "key=-")
        )

    def test_init_restore_rejects_foreign_then_uses_original_shares(self):
        effect = self.effect()
        effect.runtime = mock.Mock()
        effect.runtime.exec.return_value = self.result(returncode=2, stderr=b"* invalid key: failed to decrypt keys from storage")
        effect._wait_status = mock.Mock()
        init = {"root_token": "synthetic-root", "unseal_keys_b64": ["x", "y", "z"]}
        below = {"sealed": True, "progress": 1}
        effect._json_exec = mock.Mock(side_effect=[(self.result(), init), (self.result(), below)])
        effect._unseal = mock.Mock()
        effect._status = mock.Mock()
        order = mock.Mock()
        order.attach_mock(effect._unseal, "unseal")
        order.attach_mock(effect.runtime.login, "login")
        order.attach_mock(effect.runtime.restore, "restore")
        order.attach_mock(effect._wait_status, "wait")
        effect._init_restore("old", Path("/tmp"))
        # A new server is sealed: its own shares open it before the throwaway login
        # and the restore, then the original shares open the restored keyring. Each
        # login waits for an unsealed active node.
        self.assertEqual(
            [(c[0], *c.args) for c in order.mock_calls],
            [("wait", "old", False, True), ("unseal", "old", "x"), ("unseal", "old", "y"), ("wait", "old", True, False), ("login", "old", "synthetic-root"), ("restore", "old"), ("wait", "old", True, True)]
            + [("unseal", "old", share) for share in effect.shares]
            + [("wait", "old", True, False), ("login", "old", effect.root_token)],
        )
        # One foreign share is accepted below the threshold; the second must fail to combine.
        self.assertEqual(effect._json_exec.call_args_list[1].kwargs["input"], b"x")
        self.assertEqual(effect.runtime.exec.call_args_list[0].kwargs["input"], b"y")

    def test_init_restore_stops_when_foreign_shares_unseal_or_skip_progress(self):
        init = {"root_token": "synthetic-root", "unseal_keys_b64": ["x", "y", "z"]}
        for first, second_rc in (({"sealed": True, "progress": 1}, 0), ({"sealed": False, "progress": 0}, 2), ({"sealed": True, "progress": 1}, 1)):
            effect = self.effect()
            effect.runtime = mock.Mock()
            effect.runtime.exec.return_value = self.result(returncode=second_rc)
            effect._wait_status = mock.Mock()
            effect._json_exec = mock.Mock(side_effect=[(self.result(), init), (self.result(), first)])
            effect._unseal = mock.Mock()
            with self.assertRaises(self.subject.Indeterminate):
                effect._init_restore("old", Path("/tmp"))
            used = {c.args[1] for c in effect._unseal.call_args_list}
            self.assertFalse(used & set(effect.shares))

    def test_token_creation_and_agent_output_comparison(self):
        effect = self.effect()
        effect.runtime = mock.Mock()
        effect.runtime.containers = []
        effect.runtime.volumes = []
        effect.runtime.networks = ["n" * 64]
        effect.runtime.docker.return_value = self.result(stdout=b"0 false")
        effect.runtime.remember.side_effect = ["p" * 64, "agent-volume", "q" * 64, "r" * 64]
        effect.runtime.exec.side_effect = [
            # The templates write the exact value; HOME's canary ended in a newline.
            self.result(stdout=b"alpha\n"),
            self.result(stdout=b"1\n"),
            self.result(stdout=b"beta"),
            self.result(stdout=b"2\n"),
            self.result(stdout=b""),
            self.result(stdout=b""),
        ]
        effect.runner = mock.Mock()
        effect.runner.run.return_value = self.result()
        effect._json_exec = mock.Mock(
            side_effect=[
                (self.result(), {"data": {"role_id": "role"}}),
            ]
        )
        effect._create_tokens = mock.Mock(return_value=("issuer", "cleanup"))
        effect._fresh = mock.Mock(side_effect=self.fresh_stopped)
        old_umask = os.umask(0o077)
        try:
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                bundle = root / "bundle"
                (bundle / "config").mkdir(parents=True, mode=0o700)
                effect.materialized_bundle = bundle
                effect.materialized_helper = root / "helper"
                effect._agent("server", root, (("alpha\n", 1), ("beta", 2)))
                # RUN-0085 runs the restore under umask 077; root with only CHOWN
                # must still traverse every input directory as "other".
                modes = {name: stat.S_IMODE((root / name).stat().st_mode) for name in ("agent", "out", "bundle", "bundle/config")}
        finally:
            os.umask(old_umask)
        self.assertEqual(set(modes.values()), {0o755})
        self.assertEqual(effect._json_exec.call_count, 1)
        prep = effect.runtime.docker.call_args_list[0].args
        self.assertNotIn("DAC_READ_SEARCH", prep)
        # The stopped Agent's UID 100 files, rendered values included, are destroyed
        # where they were written, by UID 100 with no capability, on a fresh runner.
        fresh = [c.args for c in effect._fresh.call_args_list]
        revokes = [c for c in fresh if "auth/token/revoke" in c]
        self.assertEqual(len(revokes), 2)
        stop = fresh.index(("stop", "--time", "10", "q" * 64))
        self.assertEqual(fresh[stop + 1][:2], ("inspect", "--type=container"))
        reclaim = fresh[stop + 2]
        self.assertEqual(reclaim[:4], ("run", "--rm", "--name", self.subject.ATTEMPT + "-agent-reclaim"))
        self.assertIn(("--user", "100:1000"), list(itertools.pairwise(reclaim)))
        self.assertNotIn("--cap-add", reclaim)
        self.assertEqual("find /agent /out /bundle -mindepth 1 -delete; chmod 0755 /agent /out /bundle", reclaim[-1])
        self.assertLess(fresh.index(revokes[-1]), stop)
        self.assertEqual((effect.runner.run.call_args.args[0][0], "issuer" in repr(effect.runner.run.call_args.args[0]), "/bundle" in repr(effect.runtime.docker.call_args_list[0])), (str(effect.materialized_helper), False, True))

    def agent_effect(self):
        effect = self.effect()
        effect.runtime = mock.Mock()
        effect.runtime.networks = ["n" * 64]
        effect.runtime.docker.return_value = self.result(stdout=b"0 false")
        effect.runtime.remember.side_effect = ["p" * 64, "agent-volume", "q" * 64]
        effect.runner = mock.Mock()
        effect._json_exec = mock.Mock(return_value=(self.result(), {"data": {"role_id": "role"}}))
        effect._create_tokens = mock.Mock(return_value=("issuer", "cleanup"))
        effect._fresh = mock.Mock(side_effect=self.fresh_stopped)
        return effect

    def fresh_stopped(self, *args, **_kwargs):
        return self.result(stdout=b"false\n" if args[0] == "inspect" else b"")

    def run_agent(self, effect):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "bundle").mkdir()
            effect.materialized_bundle = root / "bundle"
            effect.materialized_helper = root / "helper"
            with self.assertRaises(self.subject.Indeterminate):
                effect._agent("server", root, (("alpha", 1), ("beta", 2)))
        return [c.args for c in effect._fresh.call_args_list]

    def test_helper_failure_or_deadline_still_revokes_and_reclaims(self):
        # A spent deadline or a dead watcher fails every shared-runner command, so
        # revoke and reclaim run on their own runner.
        for failure in (self.result(returncode=1), self.subject.Indeterminate()):
            effect = self.agent_effect()
            effect.runner.run.side_effect = [failure]
            fresh = self.run_agent(effect)
            with self.subTest(failure=failure):
                self.assertEqual(sum("auth/token/revoke" in c for c in fresh), 2)
                self.assertEqual(fresh[-1][:4], ("run", "--rm", "--name", self.subject.ATTEMPT + "-agent-reclaim"))

    def test_failure_before_tokens_reclaims_without_revoking(self):
        effect = self.agent_effect()
        effect.runtime.remember.side_effect = ["p" * 64, self.subject.Indeterminate()]
        fresh = self.run_agent(effect)
        self.assertFalse(any("auth/token/revoke" in c for c in fresh))
        self.assertFalse(any(c[0] == "stop" for c in fresh))
        self.assertEqual(fresh[-1][:2], ("run", "--rm"))
        effect._create_tokens.assert_not_called()

    def test_running_agent_or_failed_reclaim_is_indeterminate_and_kept(self):
        # A stop that leaves the Agent running would let it re-render after the delete.
        effect = self.agent_effect()
        effect.runner.run.side_effect = [self.result(returncode=1)]
        effect._fresh.side_effect = lambda *a, **k: self.result(stdout=b"true\n" if a[0] == "inspect" else b"")
        fresh = self.run_agent(effect)
        self.assertFalse(any(c[:2] == ("run", "--rm") for c in fresh))
        self.assertIsNotNone(effect.reclaim_paths)
        effect = self.agent_effect()
        effect.runner.run.side_effect = [self.result(returncode=1)]
        effect._fresh.side_effect = lambda *a, **k: (_ for _ in ()).throw(self.subject.Indeterminate()) if a[0] == "run" else self.fresh_stopped(*a)
        self.run_agent(effect)
        self.assertIsNotNone(effect.reclaim_paths)

    def test_removed_agent_still_reclaims_and_daemon_error_does_not(self):
        effect = self.agent_effect()
        effect.agent_id, effect.reclaim_paths = "q" * 64, (Path("/a"), Path("/o"), Path("/b"))
        effect._fresh.side_effect = lambda *a, **k: self.result(returncode=1, stderr=b"Error: No such container: x") if a[0] in ("stop", "inspect") else self.result()
        effect._reclaim()
        self.assertEqual(effect._fresh.call_args.args[:2], ("run", "--rm"))
        self.assertIsNone(effect.reclaim_paths)
        effect.reclaim_paths = (Path("/a"), Path("/o"), Path("/b"))
        effect._fresh.side_effect = lambda *a, **k: self.result(returncode=1, stderr=b"Cannot connect to the Docker daemon") if a[0] == "inspect" else self.result()
        with self.assertRaises(self.subject.Indeterminate):
            effect._reclaim()
        self.assertIsNotNone(effect.reclaim_paths)

    def test_fresh_runner_ignores_the_spent_shared_deadline(self):
        effect = self.effect()
        effect.runner = effect.execution.CommandRunner(time.monotonic() - 1, self.subject.Indeterminate)
        runner = mock.Mock()
        runner.run.return_value = self.result()
        with mock.patch.object(effect.execution, "BoundedRunner", return_value=runner) as made:
            effect._fresh("version")
        self.assertGreater(made.call_args.args[0], time.monotonic())
        self.assertIsNone(made.call_args.kwargs.get("probe"))
        self.assertEqual(runner.run.call_args.args[0], ["docker", "version"])
        runner.run.side_effect = effect.execution.ProcessError()
        with mock.patch.object(effect.execution, "BoundedRunner", return_value=runner), self.assertRaises(self.subject.Indeterminate):
            effect._fresh("version")

    def test_partial_token_issue_revokes_every_issued_token(self):
        effect = self.effect()
        effect.runtime = mock.Mock()
        effect._fresh = mock.Mock(return_value=self.result(stdout=b""))
        effect._json_exec = mock.Mock(side_effect=[(self.result(), {"auth": {"client_token": "issued"}}), self.subject.Indeterminate()])
        with self.assertRaises(self.subject.Indeterminate):
            effect._create_tokens("server")
        revoke = effect._fresh.call_args
        self.assertIn("auth/token/revoke", revoke.args)
        self.assertIn(b'"issued"', revoke.kwargs["input"])
        # The issuer helper requires explicit_max_ttl 300, which an empty body
        # through the role leaves at 0; send the RUN-0085 W5 request exactly.
        created = effect._json_exec.call_args_list[0]
        self.assertEqual(created.args[1:], ("write", "-format=json", "auth/token/create/renderer-issuer", "-"))
        self.assertEqual(
            json.loads(created.kwargs["input"]),
            {"policies": "renderer-issuer", "ttl": "5m", "explicit_max_ttl": "5m", "renewable": False, "no_default_policy": True},
        )

    def test_revoke_success_has_no_body_and_failure_is_indeterminate(self):
        # auth/token/revoke answers 204 with no body, so success is the exit status.
        effect = self.effect()
        effect._fresh = mock.Mock(return_value=self.result(stdout=b""))
        effect._revoke_tokens("server", ("one", "two"))
        self.assertEqual(effect._fresh.call_count, 2)
        self.assertEqual(effect._fresh.call_args_list[0].args, ("exec", "-i", "server", "bao", "write", "auth/token/revoke", "-"))
        self.assertNotIn("one", repr(effect._fresh.call_args_list[0].args))
        self.assertIn(b'"one"', effect._fresh.call_args_list[0].kwargs["input"])
        effect._fresh.side_effect = [self.result(stdout=b""), self.subject.Indeterminate()]
        with self.assertRaises(self.subject.Indeterminate):
            effect._revoke_tokens("server", ("one", "two"))

    def test_tls_material_keeps_ca_key_outside_mounted_directory(self):
        effect = self.effect()
        effect.runner = effect.execution.CommandRunner(time.monotonic() + 30, self.subject.Indeterminate)
        old_umask = os.umask(0o077)
        self.addCleanup(os.umask, old_umask)
        with tempfile.TemporaryDirectory(dir="/tmp") as directory:
            root = Path(directory)
            effect._tls(root)
            # RUN-0085 sets umask 077; the UID 100 server reads tls/ through its group.
            self.assertEqual(stat.S_IMODE((root / "tls").stat().st_mode), 0o750)
            self.assertTrue((root / "tls/ca.pem").is_file())
            self.assertTrue((root / "issuer/ca-key.pem").is_file())
            self.assertFalse((root / "tls/ca-key.pem").exists())

    def test_perform_orders_old_removal_before_candidate_and_accepts_after_cleanup(self):
        effect = self.effect()
        reference = (("alpha", 1), ("beta", 2))
        effect.runtime = mock.Mock()
        effect.runtime.containers = ["a" * 64]
        effect.runtime.networks = []
        effect.runtime.docker.side_effect = [self.result(), self.result(), self.result()]
        effect.runtime.remember.return_value = "n" * 64
        effect.runtime.exec.return_value = self.result(stderr=b"Code: 403", returncode=2)
        effect._tmp = mock.Mock(return_value=Path("/tmp/owned-runtime"))
        for name in (
            "_materialize_artifacts",
            "_copy_snapshot",
            "_tls",
            "_prepare_target",
            "_watcher",
            "_watcher_ok",
            "_init_restore",
            "_status",
            "_agent",
            "_wait_status",
        ):
            setattr(effect, name, mock.Mock())
        effect._server = mock.Mock(side_effect=["a" * 64, "b" * 64])
        effect._canaries = mock.Mock(return_value=reference)
        effect._unseal = mock.Mock()
        ledger = mock.Mock()
        with (
            mock.patch.object(self.subject, "AttemptLedger", return_value=ledger),
            mock.patch.object(self.subject.shutil, "rmtree"),
        ):
            receipt = effect.perform(reference)
        self.assertTrue(receipt["canaries_equal"])
        self.assertEqual(effect._wait_status.call_args_list[-1].args, ("b" * 64, True, False))
        execs = [c.args[1:] for c in effect.runtime.exec.call_args_list]
        self.assertLess(execs.index(("bao", "lease", "revoke", "-prefix", "auth/approle/login")), execs.index(("bao", "token", "revoke", "-self")))
        calls = effect.runtime.docker.call_args_list
        self.assertEqual(calls[0].args[:3], ("stop", "--time", "10"))
        effect.runtime.cleanup.assert_called_once()
        self.assertEqual(ledger.write.call_args_list[-1].args[0], "accepted")

    def test_failure_reclaims_after_cleanup_and_reports_residue(self):
        effect, ledger = self.effect(), mock.Mock()
        effect.runtime = mock.Mock()
        effect._tmp = mock.Mock(return_value=Path("/tmp/owned-runtime"))
        effect._materialize_artifacts = effect._copy_snapshot = effect._tls = mock.Mock()
        order = mock.Mock()

        def agent_started():
            effect.reclaim_paths = (Path("/a"), Path("/o"), Path("/b"))
            raise RuntimeError()

        effect._prepare_target = mock.Mock(side_effect=agent_started)
        effect._fresh = mock.Mock(return_value=self.result())
        order.attach_mock(effect.runtime.cleanup, "cleanup")
        order.attach_mock(effect._fresh, "fresh")
        stderr = io.StringIO()
        with (
            mock.patch.object(self.subject, "AttemptLedger", return_value=ledger),
            mock.patch.object(self.subject.shutil, "rmtree", side_effect=OSError()),
            mock.patch("sys.stderr", stderr),
            self.assertRaises(self.subject.Indeterminate),
        ):
            effect.perform((("a", 1), ("b", 2)))
        names = [c[0] for c in order.mock_calls]
        self.assertEqual(names[0], "cleanup")
        self.assertEqual(order.mock_calls[1].args[:2], ("run", "--rm"))
        self.assertIn("RESIDUE: /dev/shm attempt directory retained", stderr.getvalue())

    def test_every_post_ledger_exception_is_indeterminate_and_retained(self):
        for failure in (RuntimeError(), KeyboardInterrupt()):
            effect, ledger = self.effect(), mock.Mock()
            effect.runtime = mock.Mock()
            effect._tmp = mock.Mock(return_value=Path("/tmp/owned-runtime"))
            effect._materialize_artifacts = effect._copy_snapshot = effect._tls = mock.Mock()
            effect._prepare_target = mock.Mock(side_effect=failure)
            with mock.patch.object(self.subject, "AttemptLedger", return_value=ledger), mock.patch.object(self.subject.shutil, "rmtree"):
                with self.subTest(failure=type(failure).__name__), self.assertRaises(self.subject.Indeterminate):
                    effect.perform((("a", 1), ("b", 2)))
            self.assertEqual(ledger.write.call_args_list[-1].args[0], "indeterminate")
            effect.runtime.cleanup.assert_called_once()


class IntegrationBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.subject = load_source()
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)

    def tearDown(self):
        self.directory.cleanup()

    @staticmethod
    def digest(raw):
        return __import__("hashlib").sha256(raw).hexdigest()

    def test_admission_revalidates_archive_receipt_and_absent_target(self):
        snapshot = self.root / "raft.snap"
        snapshot.write_bytes(b"snapshot-bytes")
        snapshot.chmod(0o600)
        snapshot_fd = os.open(snapshot, os.O_RDONLY)
        self.addCleanup(os.close, snapshot_fd)
        info = os.fstat(snapshot_fd)
        expected = {"sha256": self.digest(b"snapshot-bytes"), "size": info.st_size, "dev": info.st_dev, "ino": info.st_ino, "raft_index": 17, "raft_term": 3}
        receipt = self.root / "receipt.json"
        receipt.write_text(json.dumps({**expected, "cluster_id": self.subject.CLUSTER, "version": self.subject.OLD_VERSION, "http_status": 200, "saved_at_utc": "2026-10-14T00:00:01+00:00"}))
        receipt.chmod(0o600)
        receipt_fd = os.open(receipt, os.O_RDONLY)
        self.addCleanup(os.close, receipt_fd)
        execution = load_execution()
        receipt_held = execution.HeldBytes.open(receipt, self.digest(receipt.read_bytes()), private=True)
        contract_file = self.root / "contract"
        contract_file.write_bytes(b"{}")
        contract_file.chmod(0o600)
        contract_held = execution.HeldBytes.open(contract_file, self.digest(b"{}"))
        self.addCleanup(receipt_held.close)
        self.addCleanup(contract_held.close)
        archive = SimpleNamespace(ArchiveBlocked=RuntimeError, validate_archive=lambda _fd: {"sha256": expected["sha256"], "size": expected["size"], "metadata": {"Index": 17, "Term": 3}})
        lease = mock.Mock()
        target = self.root / "new-target"
        parent = self.root.stat()
        with mock.patch.object(self.subject, "TARGET", target), mock.patch.object(self.subject, "PARENT_IDENTITY", (parent.st_dev, parent.st_ino, parent.st_uid, parent.st_gid)):
            admission = self.subject.Admission({"snapshot": expected}, contract_held, snapshot_fd, info, receipt_held, archive, lease)
            admission.pre_read()
            admission.post_read()
            target.mkdir()
            with self.assertRaises(self.subject.Blocked):
                admission.post_read()
        self.assertEqual(lease.recheck.call_count, 3)

    def test_ledger_is_exclusive_private_and_durable(self):
        target = self.root / "target"
        parent = self.root.stat()
        identity = (parent.st_dev, parent.st_ino, parent.st_uid, parent.st_gid)
        with mock.patch.object(self.subject, "TARGET", target), mock.patch.object(self.subject, "PARENT_IDENTITY", identity):
            ledger = self.subject.AttemptLedger("a" * 64)
            ledger.write("accepted", "a" * 64, canaries_equal=True)
            ledger.close()
            path = self.root / self.subject.LEDGER
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(json.loads(path.read_text())["state"], "accepted")
            with self.assertRaises(FileExistsError):
                self.subject.AttemptLedger("a" * 64)

    def test_preflight_verifies_exact_images_receipts_and_bundle(self):
        bundle = self.root / "bundle"
        names = {"scripts/start-agent.sh", "scripts/health-agent.sh", "config/agent.hcl", "config/templates/keycloak_admin_password.ctmpl", "config/templates/grafana_admin_password.ctmpl", "config/templates/keycloak_admin_password_version.ctmpl", "config/templates/grafana_admin_password_version.ctmpl"}
        digests = {}
        for name in names:
            path = bundle / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(name.encode())
            path.chmod(0o644)
            digests[name] = self.digest(name.encode())
        revision = "c" * 40
        bundle_receipt = json.dumps({"source_revision": revision, "sha256": digests}, separators=(",", ":")).encode()
        (bundle / "source-receipt.json").write_bytes(bundle_receipt)
        (bundle / "source-receipt.json").chmod(0o644)
        helper_dir = self.root / "helper"
        helper_dir.mkdir()
        helper_source = ROOT / "infra/03-security/openbao/scripts"
        helper_files = {name: (helper_source / name).read_bytes() for name in ("issue-renderer-secret-id.sh", "renderer-issuance.py", "renderer-request.sh")}
        for name, raw in helper_files.items():
            (helper_dir / name).write_bytes(raw)
            (helper_dir / name).chmod(0o500 if name == "issue-renderer-secret-id.sh" else 0o400)
        helper_receipt = json.dumps({"source_revision": revision, "sha256": {name: self.digest(raw) for name, raw in helper_files.items()}}, separators=(",", ":")).encode()
        (helper_dir / "source-receipt.json").write_bytes(helper_receipt)
        (helper_dir / "source-receipt.json").chmod(0o644)
        effect = self.subject.RecoveryEffects.__new__(self.subject.RecoveryEffects)
        effect.execution = load_execution()
        effect.held_artifacts = []
        self.addCleanup(lambda: [held.close() for held in effect.held_artifacts])
        candidate_ref, candidate_id = "candidate-ref", "sha256:" + "f" * 64
        effect.contract = {
            "candidate": {"reference": candidate_ref, "image_id": candidate_id},
            "renderer": {
                "helper": str(helper_dir / "issue.sh"),
                "bundle": str(bundle),
                "revision": revision,
                "helper_receipt_sha256": self.digest(helper_receipt),
                "bundle_receipt_sha256": self.digest(bundle_receipt),
            },
        }
        effect.runtime = mock.Mock()

        def docker(*args, **_kwargs):
            if args[:2] == ("image", "inspect"):
                identity = self.subject.OLD_IMAGE if args[-1] == self.subject.OLD_IMAGE else candidate_id
                # With the containerd store, --platform names the platform manifest
                # of a multi-arch upstream tag, not the local image ID.
                if any(arg.startswith("--platform") for arg in args):
                    return SimpleNamespace(stdout=("sha256:" + "9" * 64 + "\n").encode(), returncode=0)
                return SimpleNamespace(stdout=(identity + " linux/amd64\n").encode(), returncode=0)
            return SimpleNamespace(stdout=b"", returncode=1)

        effect.runtime.docker.side_effect = docker
        effect.runner = mock.Mock()
        trusted_group = mock.patch.object(self.subject.os, "getegid", return_value=1000)
        trusted_group.start()
        self.addCleanup(trusted_group.stop)
        for mounted in (b"tmpfs rw,nosuid,noexec\n", b"ext4 rw\n", b"tmpfs\n"):
            effect.runner.run.return_value = SimpleNamespace(stdout=mounted, returncode=0)
            with self.subTest(mounted=mounted), self.assertRaises(self.subject.Blocked):
                effect.preflight()
        effect.runtime.docker.reset_mock()
        effect.runner.run.return_value = SimpleNamespace(stdout=b"tmpfs rw,nosuid,nodev,inode64\n", returncode=0)
        effect.preflight()
        self.assertEqual(effect.runtime.docker.call_count, 10)
        with mock.patch.object(self.subject.os, "getegid", return_value=1001), self.assertRaises(self.subject.Blocked):
            effect.preflight()
        inspected = {c.args[-1] for c in effect.runtime.docker.call_args_list if "inspect" in c.args}
        for suffix in ("-chown", "-agent-chown", "-agent-reclaim", "-net"):
            self.assertIn(self.subject.ATTEMPT + suffix, inspected)
        def taken(*args, **_kwargs):
            if args[:2] == ("network", "inspect"):
                return SimpleNamespace(stdout=b"[]", returncode=0)
            return docker(*args)
        effect.runtime.docker.side_effect = taken
        with self.assertRaises(self.subject.Blocked):
            effect.preflight()
        effect.runtime.docker.side_effect = docker
        for wrong in (" linux/arm64", " linux/amd64 extra"):
            def other(*args, wrong=wrong, **_kwargs):
                if args[:2] == ("image", "inspect"):
                    return SimpleNamespace(stdout=(self.subject.OLD_IMAGE + wrong + "\n").encode(), returncode=0)
                return docker(*args)
            effect.runtime.docker.side_effect = other
            with self.subTest(wrong=wrong), self.assertRaises(self.subject.Blocked):
                effect.preflight()
        effect.runtime.docker.side_effect = docker
        stage = self.root / "stage"
        stage.mkdir()
        effect._materialize_artifacts(stage)
        self.assertEqual(effect.materialized_helper.read_bytes(), helper_files["issue-renderer-secret-id.sh"])
        self.assertNotEqual(effect.materialized_helper, Path(effect.contract["renderer"]["helper"]))
        copied_receipt = stage / "trusted/helper/source-receipt.json"
        self.assertEqual(copied_receipt.read_bytes(), helper_receipt)
        self.assertEqual(copied_receipt.stat().st_mode & 0o777, 0o400)
        copied_issuance = stage / "trusted/helper/renderer-issuance.py"
        spec = importlib.util.spec_from_file_location("materialized_renderer_issuance", copied_issuance)
        module = importlib.util.module_from_spec(spec)
        __import__("sys").modules[spec.name] = module
        spec.loader.exec_module(module)
        self.assertEqual(module.validate_receipt(revision), helper_files["renderer-request.sh"].decode())

    def test_snapshot_copy_reuses_held_fd_and_keeps_read_only_file(self):
        raw = b"same-held-snapshot"
        source = self.root / "source.snap"
        source.write_bytes(raw)
        source.chmod(0o600)
        descriptor = os.open(source, os.O_RDONLY)
        self.addCleanup(os.close, descriptor)
        effect = self.subject.RecoveryEffects.__new__(self.subject.RecoveryEffects)
        effect.admission = SimpleNamespace(snapshot_fd=descriptor, snapshot_info=os.fstat(descriptor))
        effect.contract = {"snapshot": {"sha256": self.digest(raw)}}
        destination = self.root / "copy"
        destination.mkdir()
        effect._copy_snapshot(destination)
        copied = destination / "raft.snap"
        self.assertEqual(copied.read_bytes(), raw)
        # Group 1000 can read it inside the server container; nothing can write it.
        self.assertEqual(copied.stat().st_mode & 0o777, 0o440)

    def test_main_reports_accepted_blocked_and_indeterminate(self):
        args = []
        for name, value in (
            ("contract", "c"),
            ("contract-sha256", "d"),
            ("snapshot", "s"),
            ("snapshot-receipt", "r"),
            ("security-receipt", "q"),
            ("ca", "a"),
            ("ca-sha256", "b"),
            ("connect-ip", "192.0.2.1"),
            ("quiescence-fd", "9"),
        ):
            args.extend(("--" + name, value))
        contract = {
            "snapshot": {"sha256": "a" * 64, "receipt_sha256": "b" * 64},
            "quiescence": {"lease_id": "c" * 32, "lease_sha256": "e" * 64},
            "security_receipt_sha256": "d" * 64,
        }
        parent = SimpleNamespace(
            ca_context=mock.Mock(return_value=object()),
            check_operator=mock.Mock(),
            API=mock.Mock(return_value=SimpleNamespace(request=mock.Mock(return_value={}))),
            Blocked=RuntimeError,
        )
        receipt_held, contract_held = mock.Mock(), mock.Mock()
        custody_error = type("CustodyError", (Exception,), {})
        execution = SimpleNamespace(HeldBytes=SimpleNamespace(open=mock.Mock(return_value=receipt_held)), CustodyError=custody_error)

        def opened(*_args, **_kwargs):
            descriptor = os.open("/dev/null", os.O_RDONLY)
            return descriptor, os.fstat(descriptor)

        with (
            mock.patch.object(self.subject, "load_dependencies", return_value=(parent, object(), execution)),
            mock.patch.object(self.subject, "_contract", return_value=(contract, contract_held)),
            mock.patch.object(self.subject, "_open_held", side_effect=opened),
            mock.patch.object(self.subject, "QuiescenceLease"),
            mock.patch.object(
                self.subject,
                "_secrets",
                return_value=("home", "root", ("s1", "s2")),
            ),
            mock.patch.object(self.subject, "Admission"),
            mock.patch.object(self.subject, "RecoveryEffects"),
            mock.patch.object(self.subject, "LiveCanaries"),
            mock.patch.object(self.subject, "orchestrate") as run,
            mock.patch("builtins.print") as printed,
        ):
            self.assertEqual(self.subject.main(args), 0)
            printed.assert_called_with("RESTORE_ACCEPTED", flush=True)
            run.side_effect = self.subject.Indeterminate()
            self.assertEqual(self.subject.main(args), 2)
        with (
            mock.patch.object(
                self.subject,
                "load_dependencies",
                side_effect=self.subject.Blocked(),
            ),
            mock.patch("builtins.print"),
        ):
            self.assertEqual(self.subject.main(args), 1)


if __name__ == "__main__":
    unittest.main()
