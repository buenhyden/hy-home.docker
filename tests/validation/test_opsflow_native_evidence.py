"""Docker-free guards for retained n8n native failure evidence."""

from __future__ import annotations

import base64
import json
import os
import stat
import subprocess
import tempfile
import unittest
import urllib.parse
from pathlib import Path
from unittest import mock

from tests.validation import _opsflow_native_evidence as evidence
from tests.validation import _opsflow_native_ownership as ownership
from tests.validation import test_opsflow_native_rehearsal as native_driver
from tests.validation._opsflow_native_evidence import (
    FAILURE_OUTPUT_LIMIT,
    FIXTURE_NAMES,
    PrivateFile,
    reconcile_failure_evidence,
    retain_failure_output,
    sanitized_failure_summary,
    verify_failure_evidence,
)
from tests.validation._opsflow_native_fixture import NativeFixture, RehearsalFailure
from tests.validation._opsflow_native_inputs import N8N_ID, N8N_REF


class NativeEvidenceGuardTests(unittest.TestCase):
    @staticmethod
    def _fixture_files(directory: Path):
        config = directory / "docker-config"
        config.mkdir(mode=0o700)
        files, values = {}, {}
        for index, name in enumerate(sorted(FIXTURE_NAMES)):
            value = f"SyntheticSecret-{index}-abcdefghijklmnopqrstuvwxyz:/+?="
            content = value + "\n" if name.endswith(".secret") else ""
            path = directory / name
            path.write_text(content)
            path.chmod(0o600)
            metadata = path.stat(follow_symlinks=False)
            files[path] = PrivateFile(
                path,
                metadata.st_dev,
                metadata.st_ino,
                metadata.st_uid,
                metadata.st_gid,
                0o600,
            )
            values[name] = value
        return files, values

    def test_head_tail_retention_keeps_utf8_terminal_failure(self):
        terminal = "Fatal: terminal-종료\n"
        text, metadata = evidence._bounded_text(
            "시" * FAILURE_OUTPUT_LIMIT + "\n" + terminal
        )
        self.assertLessEqual(len(text.encode("utf-8")), FAILURE_OUTPUT_LIMIT)
        self.assertTrue(text.endswith(terminal))
        self.assertNotIn("�", text)
        self.assertEqual("head_tail", metadata["retention"])
        self.assertTrue(metadata["truncated"])

    def test_private_identity_preserves_group_and_rejects_wrong_gid_or_mode(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "foreign-owned.dump"
            path.write_text("synthetic\n")
            path.chmod(0o640)
            metadata = path.stat(follow_symlinks=False)
            item = PrivateFile(
                path,
                metadata.st_dev,
                metadata.st_ino,
                metadata.st_uid,
                metadata.st_gid,
                0o640,
            )
            changed = item.with_uid(70)
            self.assertEqual(70, changed.uid)
            self.assertEqual(metadata.st_gid, changed.gid)
            self.assertEqual(0o640, changed.mode)
            summary, _ = evidence._read_file(path, 1024, item)
            self.assertEqual(metadata.st_gid, summary["gid"])
            with self.assertRaisesRegex(ValueError, "metadata rejected"):
                evidence._read_file(
                    path,
                    1024,
                    PrivateFile(
                        path,
                        metadata.st_dev,
                        metadata.st_ino,
                        metadata.st_uid,
                        metadata.st_gid + 1,
                        0o640,
                    ),
                )
            with self.assertRaisesRegex(ValueError, "metadata rejected"):
                evidence._read_file(
                    path,
                    1024,
                    PrivateFile(
                        path,
                        metadata.st_dev,
                        metadata.st_ino,
                        metadata.st_uid,
                        metadata.st_gid,
                        0o600,
                    ),
                )

    def test_foreign_container_files_keep_host_group_and_exact_private_mode(self):
        fixture = object.__new__(NativeFixture)
        fixture.host_uid = os.geteuid()
        fixture.host_gid = os.getegid()
        fixture.dumps = {}
        created, chowned = {}, []

        def private(name, _content, *, mode=0o600):
            created[name] = mode
            return Path("/owned") / name

        fixture.private = private
        fixture.chown_secret = lambda path, uid: chowned.append((path.name, uid))
        fixture.create_secrets()

        foreign = {
            "metadata-pg.secret": 70,
            "dev-pg.secret": 70,
            "valkey-server.secret": 999,
            "metadata.dump": 70,
            "dev-roles.sql": 70,
            "dev.dump": 70,
        }
        self.assertEqual(foreign, dict(chowned))
        self.assertEqual(
            set(foreign), {name for name, mode in created.items() if mode == 0o640}
        )
        self.assertTrue(
            all(mode == 0o600 for name, mode in created.items() if name not in foreign)
        )

    def test_chown_secret_changes_only_uid_and_verifies_group_and_mode(self):
        fixture = object.__new__(NativeFixture)
        fixture.host_gid = os.getegid()
        path = Path("/owned/metadata-pg.secret")
        fixture.files = {
            path: PrivateFile(path, 1, 2, os.geteuid(), fixture.host_gid, 0o640)
        }
        fixture.create = mock.Mock()
        fixture.start = mock.Mock()
        fixture.runtime_headroom = mock.Mock()
        fixture._verify_container = mock.Mock()
        fixture.remove = mock.Mock()
        fixture.containers = {"secret-prep": mock.Mock(cid="a" * 64)}
        fixture.client = mock.Mock()
        fixture.client.run_result.return_value = subprocess.CompletedProcess(
            [], 0, "0\n", ""
        )
        metadata = mock.Mock(
            st_uid=70,
            st_gid=fixture.host_gid,
            st_mode=stat.S_IFREG | 0o640,
        )

        with mock.patch.object(Path, "stat", return_value=metadata):
            fixture.chown_secret(path, 70)

        self.assertEqual(70, fixture.files[path].uid)
        self.assertEqual(fixture.host_gid, fixture.files[path].gid)
        self.assertEqual(0o640, fixture.files[path].mode)
        self.assertEqual(
            (f"70:{fixture.host_gid}", "/owned-secret"),
            fixture.create.call_args.kwargs["command"],
        )

    def test_readiness_capture_does_not_swallow_cancellation(self):
        client = mock.Mock()
        client.run_result.side_effect = KeyboardInterrupt()
        with (
            mock.patch.object(
                ownership, "inspect_container_identity", return_value={"State": {}}
            ),
            self.assertRaises(KeyboardInterrupt),
        ):
            ownership.main_readiness_failure_facts(
                client, mock.Mock(), "opsflow-native-" + "b" * 24
            )

    def test_exact_cid_absence_poll_handles_delay_persistence_and_cancellation(self):
        cid = "a" * 64
        missing = subprocess.CompletedProcess(
            [], 1, "\n", f"Error: No such object: {cid}\n"
        )
        present = subprocess.CompletedProcess([], 0, cid + "\n", "")
        delayed = mock.Mock()
        delayed.cleanup_deadline, delayed.deadline = None, 5.0
        delayed.run_result.side_effect = [present, missing]
        with (
            mock.patch.object(
                ownership.time,
                "monotonic",
                side_effect=[0.0, 0.0, 0.1, 0.2],
            ),
            mock.patch.object(ownership.time, "sleep"),
        ):
            observed = ownership.wait_container_absent(delayed, cid, 5.0)
        self.assertTrue(observed.absent)
        self.assertEqual(
            (1, 1, 0), (observed.present, observed.exact_absent, observed.unknown)
        )
        self.assertEqual(5.0, delayed.deadline)

        persistent = mock.Mock()
        persistent.cleanup_deadline, persistent.deadline = None, 5.0
        persistent.run_result.return_value = present
        with (
            mock.patch.object(
                ownership.time,
                "monotonic",
                side_effect=[0.0, 0.0, 5.0, 5.0],
            ),
            mock.patch.object(ownership.time, "sleep"),
        ):
            observed = ownership.wait_container_absent(persistent, cid, 5.0)
        self.assertFalse(observed.absent)
        self.assertEqual(
            (1, 0, 0), (observed.present, observed.exact_absent, observed.unknown)
        )
        self.assertEqual(5.0, persistent.deadline)

        cancelled = mock.Mock()
        cancelled.cleanup_deadline, cancelled.deadline = None, 5.0
        cancelled.run_result.side_effect = KeyboardInterrupt()
        with (
            mock.patch.object(ownership.time, "monotonic", side_effect=[0.0, 0.0]),
            self.assertRaises(KeyboardInterrupt),
        ):
            ownership.wait_container_absent(cancelled, cid, 5.0)
        self.assertEqual(5.0, cancelled.deadline)
        unknown_result = subprocess.CompletedProcess([], 1, "", "daemon unavailable\n")
        unknown_then_absent = mock.Mock()
        unknown_then_absent.cleanup_deadline, unknown_then_absent.deadline = None, 5.0
        unknown_then_absent.run_result.side_effect = [unknown_result, missing]
        with (
            mock.patch.object(
                ownership.time,
                "monotonic",
                side_effect=[0.0, 0.0, 0.1, 0.2],
            ),
            mock.patch.object(ownership.time, "sleep"),
        ):
            observed = ownership.wait_container_absent(unknown_then_absent, cid, 5.0)
        self.assertTrue(observed.absent)
        self.assertEqual(
            (0, 1, 1), (observed.present, observed.exact_absent, observed.unknown)
        )

        unknown = mock.Mock()
        unknown.cleanup_deadline, unknown.deadline = None, 5.0
        unknown.run_result.return_value = unknown_result
        with (
            mock.patch.object(
                ownership.time, "monotonic", side_effect=[0.0, 0.0, 5.0, 5.0]
            ),
            mock.patch.object(ownership.time, "sleep"),
        ):
            observed = ownership.wait_container_absent(unknown, cid, 5.0)
        self.assertFalse(observed.absent)
        self.assertEqual(
            (0, 0, 1), (observed.present, observed.exact_absent, observed.unknown)
        )

        for rejected in (
            subprocess.CompletedProcess(
                [], 1, "unexpected\n", f"Error: No such object: {cid}\n"
            ),
            subprocess.CompletedProcess(
                [], 1, "\N{NO-BREAK SPACE}", f"Error: No such object: {cid}\n"
            ),
            subprocess.CompletedProcess(
                [], 1, "\n", f"Error: No such object: {'b' * 64}\n"
            ),
        ):
            with self.subTest(rejected=rejected):
                with self.assertRaises(ValueError):
                    ownership.exact_container_absent(rejected, cid)

        timed_out = mock.Mock()
        timed_out.cleanup_deadline, timed_out.deadline = None, 5.0
        timed_out.run_result.side_effect = subprocess.TimeoutExpired(
            ["/usr/bin/docker", "info"], 0.02
        )
        with mock.patch.object(ownership.time, "monotonic", side_effect=[0.0, 0.0]):
            observed = ownership.wait_container_absent(timed_out, cid, 5.0)
        self.assertFalse(observed.absent)
        self.assertEqual(
            (0, 0, 1), (observed.present, observed.exact_absent, observed.unknown)
        )
        self.assertEqual(5.0, timed_out.deadline)

    def test_remove_releases_only_after_exact_absence_and_records_finite_facts(self):
        fixture = object.__new__(NativeFixture)
        record = ownership.Container(
            "d" * 64,
            "owned",
            "dev-pg",
            1,
            N8N_ID,
            N8N_REF,
            "70:70",
            ("dev",),
            (),
            (),
        )
        fixture.containers = {"dev-pg": record}
        fixture.pending_containers = {"dev-pg": mock.Mock()}
        fixture.receipt = {}
        fixture.client = mock.Mock()
        fixture.final_deadline = 5.0
        fixture.client.cleanup_deadline, fixture.client.deadline = None, 5.0
        fixture.client.run_result.side_effect = [
            subprocess.CompletedProcess([], 1, "", "withheld"),
            subprocess.CompletedProcess(
                [], 1, "", f"Error: No such object: {record.cid}\n"
            ),
        ]
        fixture._verify_owned = mock.Mock()
        with mock.patch.object(ownership.time, "monotonic", side_effect=[0.0, 0.0]):
            fixture.remove("dev-pg")
        self.assertEqual({}, fixture.containers)
        self.assertEqual({}, fixture.pending_containers)
        self.assertEqual(
            {"present": 0, "exact_absent": 1, "unknown": 0},
            fixture.receipt["container_removal_facts"]["dev-pg"],
        )

    def test_bounded_output_is_private_and_receipt_contains_only_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            directory.chmod(0o700)
            files, values = self._fixture_files(directory)
            receipt = {}
            secret = values["owner.secret"]
            encoded = base64.b64encode(secret.encode()).decode()
            quoted = urllib.parse.quote(secret, safe="")
            prefix = f'{secret}\nError: startup failed {quoted} https://fixture:{secret}@internal.invalid postgresql://fixture:unregistered-pass@internal/db {{"password":"unregistered-pass"}} Authorization=Bearer short-token-value token={encoded}\n'
            head = (FAILURE_OUTPUT_LIMIT - len("\n[... bounded head/tail ...]\n")) // 2
            boundary = head - len(prefix.encode()) - len(secret) // 2
            result = subprocess.CompletedProcess(
                [],
                7,
                prefix
                + "~" * boundary
                + secret
                + "~" * FAILURE_OUTPUT_LIMIT
                + "\nFatal: terminal-sentinel "
                + secret
                + "\n",
                "fatal exception\n",
            )
            retain_failure_output(directory, files, receipt, result)

            self.assertEqual(
                {path.name for path in files},
                FIXTURE_NAMES
                | {
                    "failure-stdout.txt",
                    "failure-stderr.txt",
                    "failure-metadata.json",
                },
            )
            for path in files:
                metadata = path.stat(follow_symlinks=False)
                self.assertTrue(stat.S_ISREG(metadata.st_mode))
                self.assertEqual(0o600, stat.S_IMODE(metadata.st_mode))
                self.assertEqual(1, metadata.st_nlink)
            self.assertLessEqual(
                (directory / "failure-stdout.txt").stat().st_size,
                FAILURE_OUTPUT_LIMIT,
            )
            stored = (directory / "failure-stdout.txt").read_text()
            for forbidden in (
                secret,
                secret[: len(secret) // 2],
                secret[len(secret) // 2 :],
                encoded,
                quoted,
                "short-token-value",
                "unregistered-pass",
            ):
                self.assertNotIn(forbidden, stored)
            self.assertNotIn("https://fixture:" + secret, stored)
            public = json.dumps(receipt, sort_keys=True)
            self.assertNotIn(values["owner.secret"], public)
            evidence = receipt["failure_evidence"]
            self.assertEqual(
                {
                    "schema_version",
                    "role",
                    "command_id",
                    "exit_code",
                    "streams",
                    "directory",
                    "docker_config",
                    "retained_files",
                    "metadata_file",
                },
                set(evidence),
            )
            self.assertTrue(evidence["streams"]["stdout"]["truncated"])
            self.assertEqual("head_tail", evidence["streams"]["stdout"]["retention"])
            self.assertEqual(
                len(result.stdout.encode()),
                evidence["streams"]["stdout"]["source_bytes"],
            )
            self.assertEqual(
                len(stored.encode()), evidence["streams"]["stdout"]["bytes"]
            )
            self.assertEqual(
                {
                    key: value
                    for key, value in evidence.items()
                    if key != "metadata_file"
                },
                json.loads((directory / "failure-metadata.json").read_text()),
            )
            self.assertEqual(
                FIXTURE_NAMES
                | {
                    "failure-stdout.txt",
                    "failure-stderr.txt",
                    "failure-metadata.json",
                },
                {item["name"] for item in evidence["retained_files"]}
                | {evidence["metadata_file"]["name"]},
            )
            self.assertEqual(18, len(verify_failure_evidence(directory, evidence)))
            summary = sanitized_failure_summary(directory, evidence)
            self.assertIn("Error: startup failed", summary)
            self.assertIn("fatal exception", summary)
            self.assertIn("Fatal: terminal-sentinel", summary)
            self.assertNotIn(values["owner.secret"], summary)
            self.assertNotIn(
                base64.b64encode(values["owner.secret"].encode()).decode(), summary
            )
            self.assertNotIn("https://fixture:" + values["owner.secret"], summary)
            self.assertNotIn("short-token-value", summary)
            (directory / "unexpected").write_text("blocked")
            with self.assertRaisesRegex(ValueError, "directory file set"):
                reconcile_failure_evidence(directory, evidence)
            self.assertTrue((directory / "failure-stdout.txt").exists())
            (directory / "unexpected").unlink()
            stdout = directory / "failure-stdout.txt"
            stdout.write_bytes(b"x" * stdout.stat().st_size)
            with self.assertRaisesRegex(ValueError, "identity changed"):
                verify_failure_evidence(directory, evidence)

    def test_registry_failure_prevents_both_stream_writes(self):
        for condition in ("missing", "empty"):
            with (
                self.subTest(condition=condition),
                tempfile.TemporaryDirectory() as temporary,
            ):
                directory = Path(temporary)
                files, _ = self._fixture_files(directory)
                target = directory / "owner.secret"
                if condition == "missing":
                    target.unlink()
                else:
                    target.write_text("")
                receipt = {}
                with self.assertRaises(ValueError):
                    retain_failure_output(
                        directory,
                        files,
                        receipt,
                        subprocess.CompletedProcess([], 1, "withheld", "withheld"),
                    )
                self.assertEqual({"status": "PENDING"}, receipt["failure_evidence"])
                self.assertFalse((directory / "failure-stdout.txt").exists())
                self.assertFalse((directory / "failure-stderr.txt").exists())

    def test_exact_reconciliation_removes_only_the_bound_attempt(self):
        parent = Path(tempfile.mkdtemp())
        directory = parent / "attempt"
        directory.mkdir(mode=0o700)
        files, _ = self._fixture_files(directory)
        receipt = {}
        retain_failure_output(
            directory,
            files,
            receipt,
            subprocess.CompletedProcess([], 1, "Error: bounded", ""),
        )
        reconcile_failure_evidence(directory, receipt["failure_evidence"])
        self.assertFalse(directory.exists())
        parent.rmdir()

    def test_diagnosis_rechecks_file_identity_after_manifest_verification(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            directory.chmod(0o700)
            files, _ = self._fixture_files(directory)
            receipt = {}
            retain_failure_output(
                directory,
                files,
                receipt,
                subprocess.CompletedProcess([], 1, "Error: bounded", ""),
            )
            real_verify = evidence.verify_failure_evidence

            def mutate_after_verify(*args):
                paths = real_verify(*args)
                secret = directory / "owner.secret"
                secret.write_bytes(b"z" * secret.stat().st_size)
                return paths

            with (
                mock.patch.object(
                    evidence,
                    "verify_failure_evidence",
                    side_effect=mutate_after_verify,
                ),
                self.assertRaisesRegex(ValueError, "changed before diagnosis"),
            ):
                sanitized_failure_summary(directory, receipt["failure_evidence"])

    def test_verification_rejects_named_path_replacement_after_fd_read(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            directory.chmod(0o700)
            files, _ = self._fixture_files(directory)
            receipt = {}
            retain_failure_output(
                directory,
                files,
                receipt,
                subprocess.CompletedProcess([], 1, "Error: bounded", ""),
            )
            target = directory / "owner.secret"
            target_inode = target.stat(follow_symlinks=False).st_ino
            real_read = evidence.os.read
            replaced = False

            def replace_after_read(descriptor, size):
                nonlocal replaced
                content = real_read(descriptor, size)
                if (
                    not content
                    and not replaced
                    and os.fstat(descriptor).st_ino == target_inode
                ):
                    target.unlink()
                    target.write_text("replacement must remain\n")
                    target.chmod(0o600)
                    replaced = True
                return content

            with (
                mock.patch.object(evidence.os, "read", side_effect=replace_after_read),
                self.assertRaisesRegex(ValueError, "metadata rejected"),
            ):
                verify_failure_evidence(directory, receipt["failure_evidence"])
            self.assertTrue(replaced)
            self.assertEqual("replacement must remain\n", target.read_text())

    def test_reconciliation_rejects_replacement_after_bound_fd_read(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            directory.chmod(0o700)
            files, _ = self._fixture_files(directory)
            receipt = {}
            retain_failure_output(
                directory,
                files,
                receipt,
                subprocess.CompletedProcess([], 1, "Error: bounded", ""),
            )
            target = directory / "dev-pg.secret"
            target_inode = target.stat(follow_symlinks=False).st_ino
            real_read = evidence.os.read
            real_verify = evidence.verify_failure_evidence
            armed = False

            def arm_after_verify(*args):
                nonlocal armed
                paths = real_verify(*args)
                armed = True
                return paths

            def replace_after_read(descriptor, size):
                nonlocal armed
                content = real_read(descriptor, size)
                if (
                    armed
                    and not content
                    and os.fstat(descriptor).st_ino == target_inode
                ):
                    target.unlink()
                    target.write_text("replacement must remain\n")
                    target.chmod(0o600)
                    armed = False
                return content

            with (
                mock.patch.object(
                    evidence,
                    "verify_failure_evidence",
                    side_effect=arm_after_verify,
                ),
                mock.patch.object(evidence.os, "read", side_effect=replace_after_read),
                self.assertRaisesRegex(ValueError, "changed before unlink"),
            ):
                reconcile_failure_evidence(directory, receipt["failure_evidence"])
            self.assertFalse(armed)
            self.assertEqual("replacement must remain\n", target.read_text())

    def test_exclusive_writer_rejects_preexisting_symlink(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            files, _ = self._fixture_files(directory)
            target = directory / "outside"
            target.write_text("unchanged")
            (directory / "failure-stdout.txt").symlink_to(target)
            receipt = {}
            with self.assertRaises(FileExistsError):
                retain_failure_output(
                    directory,
                    files,
                    receipt,
                    subprocess.CompletedProcess([], 1, "withheld", ""),
                )
            self.assertEqual("unchanged", target.read_text())
            self.assertEqual({"status": "PENDING"}, receipt["failure_evidence"])

    def test_cleanup_preserves_cancellation_after_receipt_and_unlock(self):
        def fixture() -> NativeFixture:
            item = object.__new__(NativeFixture)
            item.client = mock.Mock()
            item.client.run.return_value = ""
            item.containers, item.networks = {}, {}
            item.pending_containers, item.pending_networks = {}, {}
            item.swept_cids, item.swept_nids = set(), set()
            item.receipt = {"cleanup": "PENDING"}
            item.attempt = "opsflow-native-" + "c" * 24
            item.directory = Path("/tmp/owned-cancellation-attempt")
            item.dir_identity = None
            item.lock_fd = -1
            item._cleanup_host = mock.Mock()
            return item

        for cancellation in (KeyboardInterrupt, SystemExit):
            with self.subTest(cancellation=cancellation.__name__):
                begin = fixture()
                begin.client.begin_cleanup.side_effect = cancellation()
                with self.assertRaises(cancellation):
                    begin.cleanup()
                self.assertEqual("FAIL", begin.receipt["cleanup"])
                self.assertIn("cleanup_boundary", begin.receipt["cleanup_failures"])

        remove = fixture()
        remove.containers["main"] = mock.Mock(cid="a" * 64)
        remove.remove = mock.Mock(side_effect=KeyboardInterrupt())
        with self.assertRaises(KeyboardInterrupt):
            remove.cleanup()
        self.assertEqual("FAIL", remove.receipt["cleanup"])
        self.assertEqual(["a" * 64], remove.receipt["retained"]["container_ids"])

        unlock = fixture()
        unlock.lock_fd = 7
        with (
            mock.patch(
                "tests.validation._opsflow_native_evidence.fcntl.flock",
                side_effect=KeyboardInterrupt(),
            ),
            mock.patch("tests.validation._opsflow_native_evidence.os.close") as close,
            self.assertRaises(KeyboardInterrupt),
        ):
            unlock.cleanup()
        close.assert_called_once_with(7)
        self.assertEqual(-1, unlock.lock_fd)
        self.assertEqual("FAIL", unlock.receipt["cleanup"])
        self.assertIn("lock", unlock.receipt["cleanup_failures"])

    def test_cleanup_persistent_container_issues_one_removal_and_retains_identity(self):
        fixture = object.__new__(NativeFixture)
        record = ownership.Container(
            "d" * 64,
            "owned-main",
            "main",
            1,
            N8N_ID,
            N8N_REF,
            "1000:1000",
            ("ctl",),
            (),
            (),
        )
        fixture.client = mock.Mock()
        fixture.client.run.return_value = ""
        fixture.containers = {"main": record}
        fixture.networks = {}
        fixture.pending_containers, fixture.pending_networks = {}, {}
        fixture.swept_cids, fixture.swept_nids = set(), set()
        fixture.receipt = {"cleanup": "PENDING"}
        fixture.attempt = "opsflow-native-" + "b" * 24
        fixture.directory = Path("/tmp/owned-attempt-safe-name")
        fixture.dir_identity = (1, 2)
        fixture.lock_fd = -1
        fixture._cleanup_host = mock.Mock()
        fixture.remove = mock.Mock(
            side_effect=RehearsalFailure("owned container removal failed")
        )

        with self.assertRaises(RehearsalFailure):
            fixture.cleanup()

        fixture.remove.assert_called_once_with("main")
        self.assertIs(record, fixture.containers["main"])
        self.assertEqual([record.cid], fixture.receipt["retained"]["container_ids"])
        self.assertIn("container", fixture.receipt["cleanup_failures"])
        fixture._cleanup_host.assert_not_called()

    def test_cleanup_removes_known_containers_before_polling_pending(self):
        fixture = object.__new__(NativeFixture)
        record = ownership.Container(
            "d" * 64,
            "owned-main",
            "main",
            1,
            N8N_ID,
            N8N_REF,
            "1000:1000",
            ("ctl",),
            (),
            (),
        )
        late = ownership.Container(
            "e" * 64, "owned-prep", "secret-prep", 1, N8N_ID, N8N_REF, "0:0", (), (), ()
        )
        fixture.client = mock.Mock()
        fixture.client.run.return_value = ""
        fixture.containers = {"main": record}
        fixture.networks = {}
        fixture.pending_containers = {"main": mock.Mock(), "secret-prep": mock.Mock()}
        fixture.pending_networks = {}
        fixture.swept_cids, fixture.swept_nids = set(), set()
        fixture.receipt = {"cleanup": "PENDING"}
        fixture.attempt = "opsflow-native-" + "b" * 24
        fixture.directory = Path("/tmp/owned-attempt-safe-name")
        fixture.dir_identity = (1, 2)
        fixture.lock_fd = -1
        fixture._cleanup_host = mock.Mock()
        events = []

        def remove(role):
            events.append(("remove", role))
            fixture.containers.pop(role)
            fixture.pending_containers.pop(role, None)

        def adopt(role):
            events.append(("adopt", role))
            fixture.containers[role] = late

        fixture.remove = remove
        fixture._adopt_pending_container = adopt
        try:
            fixture.cleanup()
        except RehearsalFailure:
            pass
        self.assertEqual(
            [("remove", "main"), ("adopt", "secret-prep"), ("remove", "secret-prep")],
            events,
        )

    def test_registered_scenario_finalizes_once_and_preserves_original_error(self):
        case = native_driver.OpsflowN8nNativeRehearsal(
            "test_actual_queue_runner_capture_unknown_reconcile_and_restore"
        )
        case._finished = False
        case.fixture = mock.Mock()
        case.fixture.receipt = {"native": "NOT_RUN"}
        case.fixture.receipt_json.return_value = '{"cleanup":"FAIL"}'

        case.run_scenario = mock.Mock(side_effect=KeyboardInterrupt())
        case.fixture.cleanup.side_effect = SystemExit(9)
        with (
            mock.patch("builtins.print") as printed,
            self.assertRaises(KeyboardInterrupt),
        ):
            case.test_actual_queue_runner_capture_unknown_reconcile_and_restore()
        case.run_scenario.assert_called_once_with()
        case.fixture.cleanup.assert_called_once_with()
        printed.assert_called_once_with('OPSFLOW_N8N_NATIVE_RECEIPT {"cleanup":"FAIL"}')
        case.finish()
        case.tearDown()
        case.fixture.cleanup.assert_called_once_with()

        for failure in (KeyboardInterrupt(), SystemExit(4)):
            with self.subTest(failure=type(failure).__name__):
                other = native_driver.OpsflowN8nNativeRehearsal(
                    "test_actual_queue_runner_capture_unknown_reconcile_and_restore"
                )
                other._finished = False
                other.fixture = mock.Mock()
                other.fixture.receipt = {"native": "NOT_RUN"}
                other.fixture.receipt_json.return_value = "{}"
                other.run_scenario = mock.Mock()
                other.fixture.cleanup.side_effect = failure
                with (
                    mock.patch("builtins.print") as printed,
                    self.assertRaises(type(failure)),
                ):
                    other.test_actual_queue_runner_capture_unknown_reconcile_and_restore()
                printed.assert_called_once()

    def test_cleanup_retains_evidence_but_no_docker_identity(self):
        fixture = object.__new__(NativeFixture)
        fixture.client = mock.Mock()
        fixture.client.run.return_value = ""
        fixture.containers, fixture.networks = {}, {}
        fixture.pending_containers, fixture.pending_networks = {}, {}
        fixture.swept_cids, fixture.swept_nids = set(), set()
        fixture.receipt = {
            "cleanup": "PENDING",
            "failure_evidence": {"status": "retained"},
        }
        fixture.attempt = "opsflow-native-" + "b" * 24
        fixture.directory = Path("/tmp/owned-evidence-attempt")
        fixture.dir_identity = (1, 2)
        fixture.lock_fd = -1
        fixture._cleanup_host = mock.Mock()

        with self.assertRaises(RehearsalFailure):
            fixture.cleanup()
        self.assertEqual(
            ["failure_evidence_retained"], fixture.receipt["cleanup_failures"]
        )
        self.assertEqual([], fixture.receipt["retained"]["container_ids"])
        self.assertEqual([], fixture.receipt["retained"]["network_ids"])
        self.assertEqual(
            fixture.directory.name, fixture.receipt["retained"]["attempt_dir"]
        )
        fixture._cleanup_host.assert_not_called()


if __name__ == "__main__":
    unittest.main()
