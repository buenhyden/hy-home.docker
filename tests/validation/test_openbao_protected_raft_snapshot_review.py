"""Adversarial review regressions for protected Raft snapshot custody."""

from __future__ import annotations

import contextlib
import errno
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.validation import test_openbao_protected_raft_snapshot as T

S = T.S


class NativeArchiveTests(unittest.TestCase):
    def validate(self, body):
        with tempfile.TemporaryFile() as stream:
            stream.write(body)
            stream.flush()
            return S.validate_archive(stream.fileno())

    def test_archive_validator_is_loaded_from_exact_reviewed_bytes(self):
        archive = S.load_archive()
        source = T.SOURCE.with_name("protected-snapshot-archive.py")
        self.assertEqual(
            hashlib.sha256(source.read_bytes()).hexdigest(), S.ARCHIVE_SHA256
        )
        self.assertTrue(callable(archive.validate_archive))
        custody = S.load_custody()
        custody_source = T.SOURCE.with_name("protected-snapshot-custody.py")
        self.assertEqual(
            hashlib.sha256(custody_source.read_bytes()).hexdigest(), S.CUSTODY_SHA256
        )
        self.assertTrue(callable(custody.ArtifactDirectory))

    def test_native_snapshot_meta_is_typed_bounded_and_matches_state_size(self):
        result = self.validate(T.raft_archive())
        self.assertEqual(result["state_size"], len(b"barrier-encrypted-state"))
        self.assertEqual(result["metadata"]["Version"], 1)

        base = T.native_meta()
        duplicate = (json.dumps(base)[:-1] + ',"Size":23}').encode()
        nonfinite = json.dumps(T.native_meta(Term=float("nan"))).encode()
        cases = (
            T.raft_archive(meta=T.native_meta(Size=22)),
            T.raft_archive(meta=T.native_meta(Index=True)),
            T.raft_archive(meta=T.native_meta(Version=2)),
            T.raft_archive(meta=T.native_meta(Configuration={})),
            T.raft_archive(
                meta=T.native_meta(
                    Configuration={
                        "Servers": [
                            {"Suffrage": 0, "ID": "same", "Address": "one:8201"},
                            {"Suffrage": 0, "ID": "same", "Address": "two:8201"},
                        ]
                    }
                )
            ),
            T.raft_archive(meta_raw=duplicate),
            T.raft_archive(meta_raw=nonfinite),
            T.raft_archive(meta=T.native_meta(ID="x" * 9000)),
        )
        for body in cases:
            with self.subTest(prefix=body[:12]), self.assertRaises(S.Blocked):
                self.validate(body)


class ReservationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.root.chmod(0o700)

    def test_attempt_lock_and_partials_precede_http_while_finals_are_absent(self):
        expected = {
            ".raft.snap.attempt",
            ".raft.snap.partial",
            ".raft.snap.receipt.json.partial",
        }

        class Probe(T.FakeAPI):
            def lookup(probe):
                self.assertEqual({path.name for path in self.root.iterdir()}, expected)
                return super().lookup()

        with S.ArtifactDirectory(self.root) as artifacts:
            S.save_snapshot(
                Probe(), artifacts, "raft.snap", T.TOKEN, T.CLUSTER, "2.6.2"
            )

    def test_any_suffix_collision_blocks_before_http(self):
        collision = self.root / ".raft.snap.receipt.json.partial"
        collision.write_bytes(b"foreign")
        collision.chmod(0o600)
        api = T.FakeAPI()
        with (
            S.ArtifactDirectory(self.root) as artifacts,
            self.assertRaises((S.Blocked, FileExistsError)),
        ):
            S.save_snapshot(api, artifacts, "raft.snap", T.TOKEN, T.CLUSTER, "2.6.2")
        self.assertEqual(api.calls, [])
        self.assertEqual(collision.read_bytes(), b"foreign")

    def test_receipt_namespace_artifact_name_is_rejected(self):
        with S.ArtifactDirectory(self.root) as artifacts, self.assertRaises(S.Blocked):
            artifacts.reserve_attempt("raft.receipt.json")
        self.assertEqual(list(self.root.iterdir()), [])

    def test_output_path_replacement_blocks_before_http(self):
        api = T.FakeAPI()
        artifacts = S.ArtifactDirectory(self.root)
        artifacts.reserve_attempt("raft.snap")
        moved = self.root.with_name(self.root.name + "-moved")
        self.root.rename(moved)
        self.root.mkdir(mode=0o700)
        self.addCleanup(lambda: moved.exists() and moved.rename(self.root / "held"))
        with self.assertRaises(S.Blocked):
            S.save_snapshot(
                api,
                artifacts,
                "raft.snap",
                T.TOKEN,
                T.CLUSTER,
                "2.6.2",
                attempt=artifacts.attempt,
            )
        self.assertEqual(api.calls, [])
        artifacts.close()

    def test_verified_source_directory_cannot_be_output_alias(self):
        token = self.root.parent / (self.root.name + "-token")
        token.write_text(T.TOKEN)
        token.chmod(0o600)
        self.addCleanup(token.unlink)
        with token.open("rb") as stream, S.ArtifactDirectory(self.root) as artifacts:
            identity = artifacts.identity
            with self.assertRaises(S.Blocked):
                S.check_role_aliases(
                    artifacts, stream.fileno(), (99, 99), (88, 88), identity
                )

    def test_parent_and_archive_must_share_current_source_directory(self):
        parent = S.load_parent()
        archive = S.load_archive()
        custody = S.load_custody()
        self.assertEqual(
            S.shared_source_identity(parent, archive, custody), parent.source_identity
        )
        archive.source_identity = (
            parent.source_identity[0],
            parent.source_identity[1] + 1,
        )
        with self.assertRaises(S.Blocked):
            S.shared_source_identity(parent, archive, custody)

    def test_main_rejects_loader_directory_swap_before_private_input(self):
        parent = S.load_parent()
        archive = S.load_archive()
        custody = S.load_custody()
        archive.source_identity = (
            parent.source_identity[0],
            parent.source_identity[1] + 1,
        )
        with (
            mock.patch.object(S, "load_parent", return_value=parent),
            mock.patch.object(S, "load_archive", return_value=archive),
            mock.patch.object(S, "load_custody", return_value=custody),
            mock.patch.object(parent, "hidden_input") as hidden,
            mock.patch("sys.stderr"),
        ):
            self.assertEqual(S.main([]), 1)
        hidden.assert_not_called()


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.root.chmod(0o700)

    def test_snapshot_publication_failure_keeps_the_only_complete_name(self):
        with S.ArtifactDirectory(self.root) as artifacts:
            original = artifacts.recheck

            def fail_after_publish():
                original()
                final = self.root / "raft.snap"
                if final.exists() and final.stat().st_size:
                    raise OSError()

            with mock.patch.object(
                artifacts, "recheck", side_effect=fail_after_publish
            ):
                with self.assertRaises(S.Indeterminate):
                    S.save_snapshot(
                        T.FakeAPI(),
                        artifacts,
                        "raft.snap",
                        T.TOKEN,
                        T.CLUSTER,
                        "2.6.2",
                    )
        self.assertEqual((self.root / "raft.snap").read_bytes(), T.raft_archive())

    def test_snapshot_publication_never_overwrites_concurrent_winner(self):
        winner = b"foreign-snapshot-winner"
        winner_inode = []

        with S.ArtifactDirectory(self.root) as artifacts:
            original_rename = artifacts.rename_noreplace

            def win_before_rename(directory, source, target):
                if target == "raft.snap":
                    descriptor = os.open(
                        target,
                        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                        0o600,
                        dir_fd=directory,
                    )
                    os.write(descriptor, winner)
                    winner_inode.append(os.fstat(descriptor).st_ino)
                    os.close(descriptor)
                return original_rename(directory, source, target)

            with mock.patch.object(
                artifacts, "rename_noreplace", side_effect=win_before_rename
            ):
                with self.assertRaises(S.Indeterminate):
                    S.save_snapshot(
                        T.FakeAPI(),
                        artifacts,
                        "raft.snap",
                        T.TOKEN,
                        T.CLUSTER,
                        "2.6.2",
                    )
        final = self.root / "raft.snap"
        self.assertEqual(final.read_bytes(), winner)
        self.assertEqual(final.stat().st_ino, winner_inode[0])
        self.assertFalse((self.root / "raft.snap.receipt.json").exists())

    def test_receipt_publication_never_overwrites_concurrent_winner(self):
        winner = b"foreign-receipt-winner"
        winner_inode = []

        with S.ArtifactDirectory(self.root) as artifacts:
            original_rename = artifacts.rename_noreplace

            def win_before_rename(directory, source, target):
                if target == "raft.snap.receipt.json":
                    descriptor = os.open(
                        target,
                        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                        0o600,
                        dir_fd=directory,
                    )
                    os.write(descriptor, winner)
                    winner_inode.append(os.fstat(descriptor).st_ino)
                    os.close(descriptor)
                return original_rename(directory, source, target)

            with mock.patch.object(
                artifacts, "rename_noreplace", side_effect=win_before_rename
            ):
                with self.assertRaises(S.Indeterminate):
                    S.save_snapshot(
                        T.FakeAPI(),
                        artifacts,
                        "raft.snap",
                        T.TOKEN,
                        T.CLUSTER,
                        "2.6.2",
                    )
        final = self.root / "raft.snap.receipt.json"
        self.assertEqual(final.read_bytes(), winner)
        self.assertEqual(final.stat().st_ino, winner_inode[0])
        self.assertTrue((self.root / "raft.snap").stat().st_size)

    def test_final_replacement_after_atomic_move_is_indeterminate_and_preserved(self):
        foreign = b"foreign-after-snapshot-move"

        with S.ArtifactDirectory(self.root) as artifacts:
            original_rename = artifacts.rename_noreplace

            def replace_after_rename(directory, source, target):
                result = original_rename(directory, source, target)
                if target == "raft.snap":
                    os.unlink(target, dir_fd=directory)
                    descriptor = os.open(
                        target,
                        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                        0o600,
                        dir_fd=directory,
                    )
                    os.write(descriptor, foreign)
                    os.close(descriptor)
                return result

            with mock.patch.object(
                artifacts, "rename_noreplace", side_effect=replace_after_rename
            ):
                with self.assertRaises(S.Indeterminate):
                    S.save_snapshot(
                        T.FakeAPI(),
                        artifacts,
                        "raft.snap",
                        T.TOKEN,
                        T.CLUSTER,
                        "2.6.2",
                    )
        self.assertEqual((self.root / "raft.snap").read_bytes(), foreign)
        self.assertFalse((self.root / "raft.snap.receipt.json").exists())

    def test_renameat2_unavailable_fails_closed_with_partial_retained(self):
        with S.ArtifactDirectory(self.root) as artifacts:
            unavailable = OSError(errno.ENOSYS, "synthetic unavailable")
            with mock.patch.object(
                artifacts, "rename_noreplace", side_effect=unavailable
            ):
                with self.assertRaises(S.Indeterminate):
                    S.save_snapshot(
                        T.FakeAPI(),
                        artifacts,
                        "raft.snap",
                        T.TOKEN,
                        T.CLUSTER,
                        "2.6.2",
                    )
        self.assertTrue((self.root / ".raft.snap.partial").stat().st_size)
        self.assertFalse((self.root / "raft.snap").exists())

    def test_same_size_change_during_publish_is_indeterminate_and_retained(self):
        with S.ArtifactDirectory(self.root) as artifacts:
            original_rename = artifacts.rename_noreplace

            def rename_then_mutate(directory, source, target):
                result = original_rename(directory, source, target)
                if target == "raft.snap":
                    descriptor = os.open(target, os.O_RDWR, dir_fd=directory)
                    first = os.pread(descriptor, 1, 0)
                    os.pwrite(descriptor, b"0" if first != b"0" else b"1", 0)
                    os.close(descriptor)
                return result

            with mock.patch.object(
                artifacts, "rename_noreplace", side_effect=rename_then_mutate
            ):
                with self.assertRaises(S.Indeterminate):
                    S.save_snapshot(
                        T.FakeAPI(),
                        artifacts,
                        "raft.snap",
                        T.TOKEN,
                        T.CLUSTER,
                        "2.6.2",
                    )
        self.assertTrue((self.root / "raft.snap").exists())
        self.assertFalse((self.root / "raft.snap.receipt.json").exists())

    def test_receipt_postpublication_failure_keeps_receipt_and_snapshot(self):
        with S.ArtifactDirectory(self.root) as artifacts:
            original = artifacts.recheck

            def fail_after_receipt():
                original()
                receipt = self.root / "raft.snap.receipt.json"
                if receipt.exists() and receipt.stat().st_size:
                    raise OSError()

            with mock.patch.object(
                artifacts, "recheck", side_effect=fail_after_receipt
            ):
                with self.assertRaises(S.Indeterminate):
                    S.save_snapshot(
                        T.FakeAPI(),
                        artifacts,
                        "raft.snap",
                        T.TOKEN,
                        T.CLUSTER,
                        "2.6.2",
                    )
        self.assertTrue((self.root / "raft.snap").stat().st_size)
        self.assertTrue((self.root / "raft.snap.receipt.json").stat().st_size)

    def test_snapshot_change_during_receipt_publication_is_indeterminate(self):
        with S.ArtifactDirectory(self.root) as artifacts:
            original_rename = artifacts.rename_noreplace

            def rename_then_mutate(directory, source, target):
                result = original_rename(directory, source, target)
                if target == "raft.snap.receipt.json":
                    descriptor = os.open("raft.snap", os.O_RDWR, dir_fd=directory)
                    first = os.pread(descriptor, 1, 0)
                    os.pwrite(descriptor, b"0" if first != b"0" else b"1", 0)
                    os.close(descriptor)
                return result

            with mock.patch.object(
                artifacts, "rename_noreplace", side_effect=rename_then_mutate
            ):
                with self.assertRaises(S.Indeterminate):
                    S.save_snapshot(
                        T.FakeAPI(),
                        artifacts,
                        "raft.snap",
                        T.TOKEN,
                        T.CLUSTER,
                        "2.6.2",
                    )
        self.assertTrue((self.root / "raft.snap").stat().st_size)
        self.assertTrue((self.root / "raft.snap.receipt.json").stat().st_size)


class EffectBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / "output"
        self.output.mkdir(mode=0o700)
        self.ca = self.root / "ca.pem"
        self.ca.write_text("public placeholder")
        self.ca.chmod(0o644)
        self.token = self.root / "token"
        self.token.write_text(T.TOKEN)
        self.token.chmod(0o600)
        self.parent = S.load_parent()

    def invoke_main(self, *patches):
        stderr = T.io.StringIO()
        with self.token.open("rb") as token_stream, contextlib.ExitStack() as stack:
            stack.enter_context(
                mock.patch.object(S, "load_parent", return_value=self.parent)
            )
            stack.enter_context(
                mock.patch.object(self.parent, "ca_context", return_value=object())
            )
            stack.enter_context(mock.patch("sys.stderr", stderr))
            for patch in patches:
                stack.enter_context(patch)
            status = S.main(
                [
                    "--ca",
                    str(self.ca),
                    "--ca-sha256",
                    "0" * 64,
                    "--output-directory",
                    str(self.output),
                    "--artifact-name",
                    "raft.snap",
                    "--expected-cluster-id",
                    T.CLUSTER,
                    "--expected-version",
                    "2.6.2",
                    "--connect-ip",
                    "127.0.0.1",
                    "--token-fd",
                    str(token_stream.fileno()),
                ]
            )
        return status, stderr.getvalue()

    def test_real_renew_shape_has_no_period_and_second_lookup_needs_margin(self):
        S.check_renewal(T.renewal(), T.TOKEN)

        class Expiring(T.FakeAPI):
            def lookup(self):
                self.calls.append(("GET", "auth/token/lookup-self"))
                if (
                    len(
                        [call for call in self.calls if call[1].endswith("lookup-self")]
                    )
                    == 2
                ):
                    return T.lookup(ttl=S.REQUEST_SECONDS + S.TTL_MARGIN)
                return T.lookup()

        api = Expiring()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.chmod(0o700)
            with S.ArtifactDirectory(root) as artifacts, self.assertRaises(S.Blocked):
                S.save_snapshot(
                    api, artifacts, "raft.snap", T.TOKEN, T.CLUSTER, "2.6.2"
                )
        self.assertNotIn(("GET", "sys/storage/raft/snapshot"), api.calls)

    def test_connection_close_after_renew_is_indeterminate(self):
        parent = S.load_parent()
        body = json.dumps(T.renewal()).encode()

        class Response:
            status = 200
            fp = None

            def getheaders(self):
                return [("Content-Length", str(len(body)))]

            def read(self, _size):
                value, body_holder[0] = body_holder[0], b""
                return value

        class Connection:
            def request(self, *_args, **_options):
                pass

            def getresponse(self):
                return Response()

            def abort(self):
                pass

            def close(self):
                raise OSError()

        body_holder = [body]
        parent.PinnedConnection = lambda *_args, **_options: Connection()
        api = S.SnapshotAPI(parent, T.TOKEN, object(), "127.0.0.1", timeout=1)
        with self.assertRaises(S.Indeterminate):
            api.renew()

    def test_interrupt_after_renew_started_is_indeterminate(self):
        class Interrupted(T.FakeAPI):
            def renew(self):
                self.calls.append(("POST", "auth/token/renew-self"))
                raise KeyboardInterrupt()

        api = Interrupted()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.chmod(0o700)
            with (
                S.ArtifactDirectory(root) as artifacts,
                self.assertRaises(S.Indeterminate),
            ):
                S.save_snapshot(
                    api, artifacts, "raft.snap", T.TOKEN, T.CLUSTER, "2.6.2"
                )

    def test_post_save_binding_failures_are_indeterminate(self):
        artifacts = mock.Mock()
        artifacts.recheck_attempt.side_effect = S.Blocked()
        with self.assertRaises(S.Indeterminate):
            S.verify_completion(artifacts, None, None)
        artifacts.recheck_attempt.side_effect = None
        with (
            mock.patch.object(S.os, "fstat", side_effect=OSError),
            self.assertRaises(S.Indeterminate),
        ):
            S.verify_completion(artifacts, 9, ((0,), (0,), (0,)))

    def test_main_interrupt_after_save_during_final_verification_is_indeterminate(self):
        status, stderr = self.invoke_main(
            mock.patch.object(S, "save_snapshot", return_value={}),
            mock.patch.object(S, "verify_completion", side_effect=KeyboardInterrupt),
        )
        self.assertEqual(status, 2)
        self.assertIn("INDETERMINATE", stderr)

    def test_main_interrupt_after_save_during_close_is_indeterminate(self):
        custody = S.load_custody()
        status, stderr = self.invoke_main(
            mock.patch.object(S, "load_custody", return_value=custody),
            mock.patch.object(S, "save_snapshot", return_value={}),
            mock.patch.object(S, "verify_completion", return_value=None),
            mock.patch.object(
                custody.ArtifactDirectory, "__exit__", side_effect=KeyboardInterrupt
            ),
        )
        self.assertEqual(status, 2)
        self.assertIn("INDETERMINATE", stderr)

    def test_main_interrupt_after_save_during_success_output_is_indeterminate(self):
        printing = mock.Mock(side_effect=[KeyboardInterrupt(), None])
        status, _stderr = self.invoke_main(
            mock.patch.object(S, "save_snapshot", return_value={}),
            mock.patch.object(S, "verify_completion", return_value=None),
            mock.patch("builtins.print", printing),
        )
        self.assertEqual(status, 2)
        self.assertEqual(printing.call_count, 2)


if __name__ == "__main__":
    unittest.main()
