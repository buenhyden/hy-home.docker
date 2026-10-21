"""W3a input producers, checked by the restore program's own validators."""

import datetime
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import types
import unittest
import uuid
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "infra/03-security/openbao/scripts/protected-restore-inputs.py"
SPEC = importlib.util.spec_from_file_location("protected_restore_inputs", SOURCE)
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


def load_roles():
    path = ROOT / "infra/03-security/openbao/scripts/protected-renderer-roles.py"
    spec = importlib.util.spec_from_file_location("_rehearsal_renderer_roles", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


# Restored Raft data is written as UID 100 and stays for the owner to remove.
REHEARSAL_PARENT = os.environ.get("HYHOME_OPENBAO_REHEARSAL_PARENT") or None

UTC = datetime.UTC
SNAPSHOT = b"synthetic snapshot bytes"


class LeaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.directory = Path(self.tmp.name) / "lease"
        self.directory.mkdir(mode=0o700)
        self.receipt = Path(self.tmp.name) / "receipt.json"
        self.start = datetime.datetime(2026, 10, 14, 12, 0, tzinfo=UTC)

    def tearDown(self):
        self.tmp.cleanup()

    def write_receipt(self, saved):
        self.receipt.write_text(
            json.dumps({"sha256": "b" * 64, "saved_at_utc": saved.isoformat()})
        )

    def test_bound_lease_passes_the_restore_lease_check(self):
        lease_id = M.lease_start(self.directory, self.start)
        saved = self.start + datetime.timedelta(minutes=2)
        self.write_receipt(saved)
        now = saved + datetime.timedelta(minutes=1)
        bound_id, digest = M.lease_bind(self.directory, self.receipt, 60, now)
        self.assertEqual(bound_id, lease_id)
        path = self.directory / M.LEASE
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        restore = M.load_restore()
        descriptor = os.open(path, os.O_RDONLY)
        self.addCleanup(os.close, descriptor)
        lease = restore.QuiescenceLease(descriptor, lease_id, "b" * 64, digest)
        lease.recheck(saved.isoformat(), now=now.timestamp() + 60)
        with self.assertRaises(restore.Blocked):
            lease.recheck(saved.isoformat(), now=now.timestamp() + 3601)

    def test_snapshot_saved_before_writers_stopped_is_refused(self):
        M.lease_start(self.directory, self.start)
        self.write_receipt(self.start - datetime.timedelta(seconds=1))
        with self.assertRaises(M.Blocked):
            M.lease_bind(self.directory, self.receipt, 60, self.start)
        self.assertFalse((self.directory / M.LEASE).exists())

    def test_bind_in_the_same_second_as_the_save_is_accepted(self):
        M.lease_start(self.directory)
        self.write_receipt(datetime.datetime.now(UTC))
        M.lease_bind(self.directory, self.receipt, 60)

    def test_save_long_after_writers_stopped_is_refused(self):
        M.lease_start(self.directory, self.start)
        saved = self.start + M.MAX_START_TO_SAVE + datetime.timedelta(seconds=1)
        self.write_receipt(saved)
        with self.assertRaises(M.Blocked):
            M.lease_bind(self.directory, self.receipt, 60, saved)

    def test_lease_length_and_overwrite_are_refused(self):
        M.lease_start(self.directory, self.start)
        self.write_receipt(self.start)
        for minutes in (0, M.MAX_LEASE_MINUTES + 1):
            with self.subTest(minutes=minutes), self.assertRaises(M.Blocked):
                M.lease_bind(self.directory, self.receipt, minutes, self.start)
        with self.assertRaises(FileExistsError):
            M.lease_start(self.directory, self.start)

    def test_shared_directory_is_refused(self):
        self.directory.chmod(0o750)
        with self.assertRaises(M.Blocked):
            M.lease_start(self.directory)


class BundleAndReceiptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.parent = Path(self.tmp.name) / "tools"
        self.parent.mkdir(mode=0o700)
        self.revision = self.git("rev-parse", "HEAD")

    def tearDown(self):
        self.tmp.cleanup()

    @staticmethod
    def git(*arguments):
        return subprocess.run(
            ["git", "-C", str(ROOT), *arguments],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    def repository(self):
        # A linked worktree keeps .git as a file; use the common checkout.
        return Path(self.git("rev-parse", "--git-common-dir")).resolve().parent

    def test_bundle_matches_the_revision_and_the_restore_receipt_shape(self):
        target = self.parent / "bundle"
        digest = M.bundle(self.repository(), self.revision, target)
        receipt_path = target / "source-receipt.json"
        self.assertEqual(hashlib.sha256(receipt_path.read_bytes()).hexdigest(), digest)
        receipt = json.loads(receipt_path.read_text())
        self.assertEqual(receipt["source_revision"], self.revision)
        self.assertEqual(set(receipt["sha256"]), set(M.BUNDLE))
        for name, value in receipt["sha256"].items():
            raw = (target / name).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), value)
            self.assertEqual((target / name).stat().st_mode & 0o777, 0o400)
        with self.assertRaises(M.Blocked):
            M.bundle(self.repository(), self.revision, target)

    def test_bundle_refuses_a_short_revision_or_a_tree(self):
        tree = self.git("rev-parse", "HEAD^{tree}")
        for revision in (self.revision[:12], tree):
            with self.subTest(revision=revision), self.assertRaises(M.Blocked):
                M.bundle(self.repository(), revision, self.parent / "other")
        self.assertFalse((self.parent / "other").exists())

    def test_candidate_comes_from_compose_at_the_revision(self):
        reference = M.candidate_reference(self.repository(), self.revision)
        compose = self.git("show", self.revision + ":" + M.COMPOSE)
        self.assertIn("image: " + reference, compose)
        self.assertTrue(reference.startswith("hy-home/openbao:"))

    def test_security_receipt_freezes_both_openbao_rows_at_the_revision(self):
        output = self.parent / "security.json"
        digest = M.security_receipt(self.repository(), self.revision, output)
        value = json.loads(output.read_text())
        self.assertEqual(value["source_revision"], self.revision)
        ledger_raw = subprocess.run(
            ["git", "-C", str(ROOT), "show", self.revision + ":" + M.LEDGER],
            capture_output=True,
            check=True,
        ).stdout
        self.assertEqual(
            [row["service"] for row in value["rows"]], ["openbao", "openbao-agent"]
        )
        self.assertEqual(value["ledger_sha256"], hashlib.sha256(ledger_raw).hexdigest())
        self.assertEqual(hashlib.sha256(output.read_bytes()).hexdigest(), digest)


class ImageTests(unittest.TestCase):
    def run_with(self, returncode, stdout):
        done = subprocess.CompletedProcess([], returncode, stdout.encode(), b"")
        with mock.patch.object(M.subprocess, "run", return_value=done) as run:
            return M.image_id("ref"), run

    def test_local_id_on_linux_amd64_is_returned_with_a_fixed_path(self):
        value, run = self.run_with(0, "sha256:" + "a" * 64 + " linux/amd64\n")
        self.assertEqual(value, "sha256:" + "a" * 64)
        self.assertNotIn("--platform=linux/amd64", run.call_args.args[0])
        self.assertEqual(run.call_args.kwargs["env"], {"PATH": "/usr/bin:/bin"})

    def test_other_platform_or_failed_docker_is_refused(self):
        for code, out in (
            (0, "sha256:" + "a" * 64 + " linux/arm64"),
            (1, "sha256:" + "a" * 64 + " linux/amd64"),
            (0, ""),
        ):
            with self.subTest(code=code, out=out), self.assertRaises(M.Blocked):
                self.run_with(code, out)


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.root = root
        self.snapshot = root / "raft-pre-upgrade.snap"
        self.snapshot.write_bytes(SNAPSHOT)
        self.snapshot.chmod(0o600)
        info = self.snapshot.stat()
        self.digest = hashlib.sha256(SNAPSHOT).hexdigest()
        self.receipt = root / "raft-pre-upgrade.snap.receipt.json"
        self.receipt.write_text(
            json.dumps(
                {
                    "sha256": self.digest,
                    "size": len(SNAPSHOT),
                    "dev": info.st_dev,
                    "ino": info.st_ino,
                    "cluster_id": "51fbfa38-a715-7dca-629f-3f07233749f4",
                    "version": "2.6.2",
                    "http_status": 200,
                    "saved_at_utc": "2026-10-14T12:01:00+00:00",
                }
            )
        )
        self.lease = root / "lease.json"
        self.lease.write_text(
            json.dumps({"lease_id": "c" * 32, "snapshot_sha256": self.digest})
        )
        for name in ("helper", "bundle"):
            (root / name).mkdir()
            (root / name / "source-receipt.json").write_text(
                json.dumps({"source_revision": "d" * 40, "sha256": {}})
            )
        self.security = root / "security.json"
        self.security.write_text("{}")

    def tearDown(self):
        self.tmp.cleanup()

    def restore(self, digest=None):
        restore = M.load_restore()
        parent, _archive, execution = restore.load_dependencies()
        archive = types.SimpleNamespace(
            ArchiveBlocked=ValueError,
            validate_archive=lambda _fd: {
                "sha256": digest or self.digest,
                "size": len(SNAPSHOT),
                "metadata": {"Index": 42, "Term": 3},
            },
        )
        restore.load_dependencies = mock.Mock(return_value=(parent, archive, execution))
        return restore

    def options(self):
        return types.SimpleNamespace(
            output=str(self.root / "contract.json"),
            snapshot=str(self.snapshot),
            snapshot_receipt=str(self.receipt),
            lease=str(self.lease),
            helper_directory=str(self.root / "helper"),
            bundle=str(self.root / "bundle"),
            revision="d" * 40,
            security_receipt=str(self.security),
            repository="unused",
        )

    @staticmethod
    def inspect(_reference):
        return "sha256:" + "f" * 64

    @staticmethod
    def reference(_repository, _revision):
        return "hy-home/openbao:2.7.1-go1.27.3-net0.60.0-r1@sha256:" + "e" * 64

    def make(self, options=None, digest=None, reference=None):
        return M.contract(
            options or self.options(),
            self.restore(digest),
            inspect=self.inspect,
            reference=reference or self.reference,
        )

    def test_contract_passes_the_restore_schema_and_binds_every_input(self):
        digest = self.make()
        output = self.root / "contract.json"
        self.assertEqual(hashlib.sha256(output.read_bytes()).hexdigest(), digest)
        value = json.loads(output.read_text())
        self.assertEqual(value["snapshot"]["raft_index"], 42)
        self.assertEqual(value["snapshot"]["sha256"], self.digest)
        self.assertEqual(
            value["quiescence"]["lease_sha256"],
            hashlib.sha256(self.lease.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            value["renderer"]["helper"],
            str(self.root / "helper/issue-renderer-secret-id.sh"),
        )

    def test_snapshot_not_matching_its_receipt_writes_nothing(self):
        with self.assertRaises(M.Blocked):
            self.make(digest="0" * 64)
        self.assertFalse((self.root / "contract.json").exists())

    def test_wrong_candidate_fails_the_self_check_and_leaves_no_file(self):
        with self.assertRaises(M.Blocked):
            self.make(reference=lambda *_: "openbao/openbao:old")
        self.assertFalse((self.root / "contract.json").exists())

    def test_receipt_from_another_revision_is_refused(self):
        (self.root / "bundle/source-receipt.json").write_text(
            json.dumps({"source_revision": "a" * 40, "sha256": {}})
        )
        with self.assertRaises(M.Blocked):
            self.make()
        self.assertFalse((self.root / "contract.json").exists())


@unittest.skipUnless(
    os.environ.get("HYHOME_OPENBAO_REHEARSAL") == "1",
    "opt-in native rehearsal: real snapshot, producers and restore validators",
)
class NativeRehearsalTests(unittest.TestCase):
    """Producer CLI end to end, then the restore client on owned synthetic state.

    The read-only test stops before RecoveryEffects.perform and only stats the
    fixed target's parent. The perform test replaces HOME's attempt, target,
    parent and cluster constants in this process only.
    """

    OLD_IMAGE = (
        "sha256:11fd73a2102cda9c55d5d881a8c3210303146a7ec1e8ac76f526e175c6d24641"
    )

    def produce(self, *arguments):
        output = io.StringIO()
        with mock.patch("sys.stdout", output), mock.patch("sys.stderr"):
            code = M.main(list(arguments))
        self.assertEqual(code, 0, "producer step failed: " + arguments[0])
        return output.getvalue().split()

    def private(self, name):
        path = self.work / name
        path.mkdir(mode=0o700)
        return path

    def home(self):
        from tests.validation import _openbao_rehearsal_fixture as native

        fixture = native.OwnedFixture(
            image=self.OLD_IMAGE,
            version="2.6.2",
            image_reference="openbao/openbao:2.6.2",
        )
        self.addCleanup(fixture.cleanup)
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.work = Path(tmp.name)
        fixture.prepare()
        _name, client = fixture.server("w4")
        shares = client.initialize()
        return native, fixture, client, shares

    def inputs(self, client, cluster, restore):
        """W3 snapshot and every W3a input up to, not including, the contract."""
        inputs, snapshots, tools = (
            self.private(name) for name in ("inputs", "snapshots", "tools")
        )
        self.produce("lease-start", "--directory", str(inputs))
        status, raw = client.api("GET", "sys/storage/raft/snapshot", binary=True)
        self.assertEqual(status, 200)
        snapshot = snapshots / "raft-pre-upgrade.snap"
        M.write_new(snapshot, raw)
        info = snapshot.stat()
        receipt = snapshots / "raft-pre-upgrade.snap.receipt.json"
        M.write_new(
            receipt,
            M.canonical(
                {
                    "sha256": hashlib.sha256(raw).hexdigest(),
                    "size": len(raw),
                    "dev": info.st_dev,
                    "ino": info.st_ino,
                    "cluster_id": cluster,
                    "version": restore.OLD_VERSION,
                    "http_status": 200,
                    "saved_at_utc": datetime.datetime.now(UTC).isoformat(),
                }
            ),
        )
        _bound, lease_id, lease_sha = self.produce(
            "lease-bind",
            "--directory",
            str(inputs),
            "--snapshot-receipt",
            str(receipt),
            "--minutes",
            "30",
        )
        repository = (
            Path(BundleAndReceiptTests.git("rev-parse", "--git-common-dir"))
            .resolve()
            .parent
        )
        revision = BundleAndReceiptTests.git("rev-parse", "HEAD")
        installer = (
            ROOT / "infra/03-security/openbao/scripts/install-renderer-issuer.sh"
        )
        helper = tools / revision
        subprocess.run(
            ["/bin/sh", str(installer), str(repository), revision, str(helper)],
            check=True,
            timeout=60,
        )
        self.produce(
            "bundle",
            "--repository",
            str(repository),
            "--revision",
            revision,
            "--target",
            str(inputs / "bundle"),
        )
        security = inputs / "security-receipt.json"
        self.produce(
            "security-receipt",
            "--repository",
            str(repository),
            "--revision",
            revision,
            "--output",
            str(security),
        )
        return types.SimpleNamespace(
            output=str(inputs / "restore-contract.json"),
            snapshot=str(snapshot),
            snapshot_receipt=str(receipt),
            lease=str(inputs / M.LEASE),
            helper_directory=str(helper),
            bundle=str(inputs / "bundle"),
            revision=revision,
            security_receipt=str(security),
            repository=str(repository),
            lease_id=lease_id,
            lease_sha256=lease_sha,
        )

    def admit(self, restore, options, digest):
        """The restore client's own admission, exactly as main() builds it."""
        _parent, archive, execution = restore.load_dependencies()
        contract, contract_held = restore._contract(options.output, digest, execution)
        self.addCleanup(contract_held.close)
        self.assertEqual(contract["quiescence"]["lease_sha256"], options.lease_sha256)
        snapshot_fd, snapshot_info = restore._open_held(
            options.snapshot,
            contract["snapshot"]["sha256"],
            maximum=32 << 20,
            private=True,
        )
        self.addCleanup(os.close, snapshot_fd)
        receipt_held = execution.HeldBytes.open(
            options.snapshot_receipt,
            contract["snapshot"]["receipt_sha256"],
            private=True,
        )
        self.addCleanup(receipt_held.close)
        lease_fd = os.open(options.lease, os.O_RDONLY)
        self.addCleanup(os.close, lease_fd)
        lease = restore.QuiescenceLease(
            lease_fd,
            options.lease_id,
            contract["snapshot"]["sha256"],
            options.lease_sha256,
        )
        return (
            execution,
            contract,
            restore.Admission(
                contract,
                contract_held,
                snapshot_fd,
                snapshot_info,
                receipt_held,
                archive,
                lease,
            ),
        )

    def test_inputs_pass_every_read_only_restore_check(self):
        _native, _fixture, client, _shares = self.home()
        restore = M.load_restore()
        options = self.inputs(client, restore.CLUSTER, restore)
        arguments = ["contract"]
        for name in (
            "output",
            "snapshot",
            "snapshot-receipt",
            "lease",
            "helper-directory",
            "bundle",
            "revision",
            "security-receipt",
            "repository",
        ):
            arguments += ["--" + name, getattr(options, name.replace("-", "_"))]
        _written, digest = self.produce(*arguments)
        execution, contract, admission = self.admit(restore, options, digest)
        admission.pre_read()
        effects = restore.RecoveryEffects(
            None, contract, admission, ("a", "b", ("c", "d")), digest, execution
        )
        self.addCleanup(lambda: [held.close() for held in effects.held_artifacts])
        effects.preflight()

    def test_full_perform_restores_upgrades_and_renders(self):
        """Old-image restore, candidate upgrade, Agent render, accepted ledger."""
        native, fixture, client, shares = self.home()
        cluster = client.api("GET", "sys/seal-status")[1]["cluster_id"]
        reference = self.seed(native, fixture, client, cluster)
        restore = M.load_restore()
        attempt = "p01-rehearsal-" + uuid.uuid4().hex[:12]
        # Docker writes the restored Raft data as UID 100; the owner removes it.
        parent = Path(tempfile.mkdtemp(prefix=attempt + "-", dir=REHEARSAL_PARENT))
        parent.chmod(0o700)
        for name, value in (
            ("ATTEMPT", attempt),
            ("LEDGER", "." + attempt + ".attempt.json"),
            ("TARGET", parent / attempt),
            ("CLUSTER", cluster),
        ):
            patcher = mock.patch.object(restore, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        options = self.inputs(client, cluster, restore)
        digest = M.contract(options, restore=restore)
        # _contract pins HOME's parent literally; the target's real parent
        # replaces it only after the contract is admitted.
        info = parent.stat()
        with mock.patch.object(
            restore,
            "PARENT_IDENTITY",
            (info.st_dev, info.st_ino, info.st_uid, info.st_gid),
        ):
            execution, contract, admission = self.admit(restore, options, digest)
            home_token = client.api("POST", "auth/token/create", {"ttl": "30m"})[1][
                "auth"
            ]["client_token"]
            effects = restore.RecoveryEffects(
                None,
                contract,
                admission,
                (home_token, client.token, tuple(shares[:2])),
                digest,
                execution,
            )
            self.addCleanup(lambda: [held.close() for held in effects.held_artifacts])
            base = restore.load_dependencies()[0]
            # HOME's gateway name and port are the only replaced transport facts.
            gateway = types.SimpleNamespace(**vars(base))
            gateway.PinnedConnection = lambda _host, _port, **kwargs: (
                base.PinnedConnection("openbao", native.PORT, **kwargs)
            )
            ca = fixture.tls / "ca.pem"
            reader = restore.LiveCanaries(
                gateway,
                home_token,
                base.ca_context(str(ca), hashlib.sha256(ca.read_bytes()).hexdigest()),
                client.target,
            )
            self.assertEqual(reader.read_all(), reference)
            # RUN-0085 runs W3a under umask 077; every container must still read
            # the directories the client creates.
            previous = os.umask(0o077)
            try:
                receipt = restore.orchestrate(admission, reader, effects)
            finally:
                os.umask(previous)
        self.assertEqual(
            receipt,
            {
                "canaries_equal": True,
                "lease_id": options.lease_id,
                "snapshot_sha256": contract["snapshot"]["sha256"],
                "raft_index": contract["snapshot"]["raft_index"],
                "raft_term": contract["snapshot"]["raft_term"],
            },
        )
        ledger = json.loads((parent / ("." + attempt + ".attempt.json")).read_text())
        self.assertEqual(ledger["state"], "accepted")
        for kind in (["ps", "-aq"], ["volume", "ls", "-q"], ["network", "ls", "-q"]):
            leftovers = subprocess.run(
                ["docker", *kind, "--filter", "label=hy-home.attempt=" + attempt],
                capture_output=True,
                check=True,
            ).stdout
            self.assertEqual(leftovers, b"", kind[0])
        # The rendered values, the Agent token and the keys lived only here.
        self.assertEqual(list(Path("/dev/shm").glob(attempt + "-*")), [])

    def seed(self, native, fixture, client, cluster):
        """HOME's canaries and renderer roles, applied by the reviewed W1c tool."""

        def ok(method, path, payload=None):
            status, body = client.api(method, path, payload)
            self.assertIn(status, (200, 204), "synthetic setup request failed")
            return body

        ok("POST", "sys/mounts/secret", {"type": "kv", "options": {"version": "2"}})
        # A new KV v2 mount answers 400 until its metadata upgrade finishes.
        for _ in range(40):
            if client.api("GET", "secret/config")[0] == 200:
                break
            time.sleep(0.25)
        values = {}
        for route, writes in (("02-auth/keycloak", 2), ("06-observability/grafana", 1)):
            for _ in range(writes):
                value = uuid.uuid4().hex
                version = ok(
                    "POST",
                    "secret/data/hy-home/" + route,
                    {"data": {"admin_password": value}},
                )["data"]["version"]
            values[route] = (value, version)
        ok("POST", "sys/auth/approle", {"type": "approle"})
        ok(
            "POST",
            "auth/approle/role/hy-home-renderer",
            {"token_policies": ["renderer"]},
        )
        roles = load_roles()
        w1 = self.private("w1")
        for name, value in (
            ("root.token", client.token),
            (
                "state.json",
                json.dumps({"state": "DELIVERED", "operator_healthy": True}),
            ),
        ):
            M.write_new(w1 / name, value.encode())
        operation = self.private("roles")
        ca = fixture.tls / "ca.pem"
        root_fd = os.open(w1 / "root.token", os.O_RDONLY)
        self.addCleanup(os.close, root_fd)
        original = roles.BASE.PinnedConnection
        output = io.StringIO()
        with (
            mock.patch.object(roles.BASE, "HOST", "openbao"),
            mock.patch.object(
                roles.BASE,
                "PinnedConnection",
                lambda host, _port, **kwargs: original(host, native.PORT, **kwargs),
            ),
            mock.patch("sys.stdout", output),
        ):
            code = roles.main(
                [
                    "apply",
                    "--ca",
                    str(ca),
                    "--ca-sha256",
                    hashlib.sha256(ca.read_bytes()).hexdigest(),
                    "--connect-ip",
                    client.target,
                    "--expected-cluster-id",
                    cluster,
                    "--custody-directory",
                    str(operation),
                    "--w1-custody-directory",
                    str(w1),
                    "--root-fd",
                    str(root_fd),
                ]
            )
        self.assertEqual((code, output.getvalue()), (0, "RENDERER_ROLES_APPLIED\n"))
        return (values["02-auth/keycloak"], values["06-observability/grafana"])


if __name__ == "__main__":
    unittest.main()
