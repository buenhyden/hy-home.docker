from __future__ import annotations

import collections
import os
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
TASK10_BASELINE = "f259c139fb7da166609029cdd3657de87e639f6b"


def archive_api():
    try:
        from scripts.lib.document_governance import archive
    except ImportError as exc:
        raise AssertionError("Task 10 archive authority is missing") from exc
    return archive


class ArchiveMinimizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.archive = archive_api()

    def test_archive_has_only_registered_minimal_roots(self) -> None:
        inventory = self.archive.load_archive(ROOT / "docs/98.archive")
        self.assertEqual(("README.md", "migrations", "tombstones"), inventory.root_entries)
        self.assertEqual(3, len(inventory.migrations))
        self.assertEqual(38, len(inventory.tombstones))
        self.assertTrue(all(item.is_minimal for item in inventory.tombstones))
        self.assertFalse((ROOT / "docs/98.archive/changes").exists())

    def test_all_184_preservation_decisions_are_unique_and_reviewed(self) -> None:
        decisions = self.archive.load_task10_preservation_decisions(ROOT)
        self.assertEqual(184, len(decisions))
        self.assertEqual(
            {"git-only": 146, "minimal-tombstone": 38},
            dict(collections.Counter(item.disposition for item in decisions)),
        )
        self.assertEqual(184, len({item.stable_path for item in decisions}))
        self.assertTrue(all(item.reviewer_decision == "approved" for item in decisions))
        self.assertTrue(all(item.recovery.commit for item in decisions))

    def test_only_the_exact_14_reviewed_baseline_paths_may_lack_metadata(self) -> None:
        from scripts.lib.document_governance import git_provenance

        approved = tuple(sorted(self.archive.APPROVED_BASELINE_RECOVERY_PATHS))
        self.assertEqual(14, len(approved))
        unlisted = pathlib.PurePosixPath(
            "docs/98.archive/changes/chg-0002-01-gateway-standardization/task.md"
        )
        metadata = git_provenance.ArchivedMetadata(
            unlisted,
            "232effd9a5e00907bdbe30efc6665023fb2d07f4",
            unlisted,
        )
        with mock.patch.object(
            self.archive,
            "read_archived_metadata_batch",
            return_value=(metadata,),
        ):
            resolved = self.archive._legacy_change_recoveries(
                ROOT,
                (*approved, unlisted),
            )
        self.assertEqual(TASK10_BASELINE, resolved[approved[0]].commit)
        self.assertEqual(metadata.archived_commit, resolved[unlisted].commit)

        with mock.patch.object(
            self.archive,
            "read_archived_metadata_batch",
            return_value=(),
        ):
            with self.assertRaisesRegex(ValueError, "unapproved missing"):
                self.archive._legacy_change_recoveries(ROOT, (*approved, unlisted))

        swapped = git_provenance.ArchivedMetadata(
            approved[0], TASK10_BASELINE, approved[0]
        )
        with mock.patch.object(
            self.archive,
            "read_archived_metadata_batch",
            return_value=(swapped,),
        ):
            with self.assertRaisesRegex(ValueError, "unapproved missing"):
                self.archive._legacy_change_recoveries(ROOT, (*approved, unlisted))

    def test_task10_recovery_references_all_resolve_to_regular_blobs(self) -> None:
        rows = self.archive.load_task10_recovery_references(ROOT)
        self.assertEqual(272, len(rows))
        self.assertEqual(14, sum(item.commit == TASK10_BASELINE for item in rows))
        self.assertEqual((), self.archive.validate_recovery_rows(rows, ROOT))

    def test_recovery_validator_rejects_unsafe_values_and_non_blobs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Archive Test"], cwd=root, check=True)
            (root / "body.md").write_text("body\n", encoding="utf-8")
            (root / "tree").mkdir()
            (root / "tree/item.md").write_text("item\n", encoding="utf-8")
            try:
                (root / "link.md").symlink_to("body.md")
            except OSError:
                self.skipTest("symlink creation is unavailable")
            subprocess.run(["git", "add", "body.md", "tree/item.md", "link.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
            commit = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True
            ).stdout.strip()
            RecoveryReference = self.archive.RecoveryReference
            rows = (
                RecoveryReference(commit, pathlib.PurePosixPath("missing.md")),
                RecoveryReference(commit, pathlib.PurePosixPath("link.md")),
                RecoveryReference(commit, pathlib.PurePosixPath("tree")),
                RecoveryReference("f" * 40, pathlib.PurePosixPath("body.md")),
                RecoveryReference("-" + commit[1:], pathlib.PurePosixPath("body.md")),
                RecoveryReference(commit, pathlib.PurePosixPath("-body.md")),
                RecoveryReference(commit, pathlib.PurePosixPath("bad\x00path")),
            )
            codes = {item.code for item in self.archive.validate_recovery_rows(rows, root)}
            self.assertIn("recovery-object-missing", codes)
            self.assertIn("recovery-object-not-regular-blob", codes)
            self.assertIn("recovery-commit-invalid", codes)
            self.assertIn("recovery-path-invalid", codes)

    def test_recovery_batch_rejects_a_tree_entry_with_a_missing_blob(self) -> None:
        from scripts.lib.document_governance import git_provenance

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Archive Test"], cwd=root, check=True)
            (root / "body.md").write_text("body\n", encoding="utf-8")
            subprocess.run(["git", "add", "body.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
            commit = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            blob = subprocess.run(
                ["git", "rev-parse", "HEAD:body.md"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            (root / ".git/objects" / blob[:2] / blob[2:]).unlink()

            proof = git_provenance.verify_recovery_blobs_batch(
                ((pathlib.PurePosixPath("body.md"), commit),),
                repo_root=root,
            )[0]
            self.assertFalse(proof.exists)
            self.assertFalse(proof.is_regular_blob)
            findings = self.archive.validate_recovery_rows(
                (
                    self.archive.RecoveryReference(
                        commit,
                        pathlib.PurePosixPath("body.md"),
                    ),
                ),
                root,
            )
            self.assertEqual(
                (
                    self.archive.ArchiveFinding(
                        "recovery-object-missing",
                        "body.md",
                    ),
                ),
                findings,
            )

    def test_invalid_recovery_identity_is_rejected_before_git(self) -> None:
        from scripts.lib.document_governance import git_provenance

        invalid = (
            ("f" * 39, pathlib.PurePosixPath("docs/body.md")),
            ("f" * 40, pathlib.PurePosixPath("-body.md")),
            ("f" * 40, pathlib.PurePosixPath("docs/bad\x00body.md")),
            ("f" * 40, pathlib.PurePosixPath("../outside.md")),
        )
        with mock.patch.object(git_provenance, "_run_git") as run_git:
            for commit, path in invalid:
                with self.subTest(commit=commit, path=path):
                    proof = git_provenance.verify_recovery_blob(path, commit, repo_root=ROOT)
                    self.assertFalse(proof.exists)
                    self.assertFalse(proof.is_regular_blob)
            run_git.assert_not_called()

    def test_recovery_row_shape_rejects_null_line_sha_and_unknown_fields(self) -> None:
        valid = {
            "status": "completed",
            "recovery_commit": TASK10_BASELINE,
            "original_path": "docs/retired.md",
        }
        self.assertEqual(
            self.archive.RecoveryReference(TASK10_BASELINE, pathlib.PurePosixPath("docs/retired.md")),
            self.archive.parse_recovery_row(valid),
        )
        for mutation in (
            {**valid, "recovery_commit": None},
            {**valid, "recovery_commit": TASK10_BASELINE + ":42"},
            {**valid, "snapshot_count": 184},
            {**valid, "unexpected": True},
        ):
            with self.subTest(mutation=mutation):
                with self.assertRaises(ValueError):
                    self.archive.parse_recovery_row(mutation)

    def test_archive_yaml_rejects_duplicate_keys_and_unknown_task10_fields(self) -> None:
        for duplicate in ("archived_commit", "archived_from"):
            source = f"---\n{duplicate}: first\n{duplicate}: second\n---\nbody\n"
            with self.subTest(duplicate=duplicate):
                with self.assertRaisesRegex(ValueError, "duplicate keys"):
                    self.archive._frontmatter(source)
        with self.assertRaises(ValueError):
            self.archive._frontmatter("---\nfirst: &value x\nsecond: *value\n---\nbody\n")

        tombstone = next((ROOT / "docs/98.archive/tombstones").rglob("*.md"))
        tombstone_text = tombstone.read_text(encoding="utf-8").replace(
            "status: completed\n",
            "status: completed\nunexpected: true\n",
            1,
        )
        with self.assertRaisesRegex(ValueError, "minimal contract"):
            self.archive._parse_tombstone_text(
                tombstone_text,
                pathlib.PurePosixPath("docs/98.archive/tombstones/03.specs/0001-sample.md"),
                "0001-sample.md",
            )

        original = (
            ROOT / "docs/98.archive/migrations/0003-workspace-governance-simplification.md"
        ).read_text(encoding="utf-8")
        mutations = (
            original.replace("\nrows:\n", "\nrows: []\nrows:\n", 1),
            original.replace(
                "row_id: mig-0003-r0566,",
                "row_id: duplicate, row_id: mig-0003-r0566,",
                1,
            ),
            original.replace(
                "row_id: mig-0003-r0566,",
                "row_id: mig-0003-r0566, unexpected: true,",
                1,
            ),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                target = root / "docs/98.archive/migrations"
                target.mkdir(parents=True)
                (target / "0003-workspace-governance-simplification.md").write_text(
                    mutation,
                    encoding="utf-8",
                )
                with self.assertRaises(ValueError):
                    self.archive.task10_rows(root)

    def test_task10_rows_reject_same_shape_semantic_mutations(self) -> None:
        original = (
            ROOT / "docs/98.archive/migrations/0003-workspace-governance-simplification.md"
        ).read_text(encoding="utf-8")
        mutations = (
            original.replace("action: rename, owner_task: 10", "action: invented, owner_task: 10", 1),
            original.replace("row_id: mig-0003-r0600,", "row_id: mig-0003-r0601,", 1),
            original.replace(
                "source_path: docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md",
                "source_path: ../outside.md",
                1,
            ),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                target = root / "docs/98.archive/migrations"
                target.mkdir(parents=True)
                (target / "0003-workspace-governance-simplification.md").write_text(
                    mutation,
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(ValueError, "frozen digest"):
                    self.archive.task10_rows(root)

    def test_archive_reads_reject_ancestor_symlink_special_file_and_swap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            actual = root / "actual"
            actual.mkdir()
            body = actual / "body.md"
            body.write_text("body\n", encoding="utf-8")
            alias = root / "alias"
            try:
                alias.symlink_to(actual, target_is_directory=True)
            except OSError:
                self.skipTest("symlink creation is unavailable")
            with self.assertRaises(ValueError):
                self.archive._read_regular(alias / "body.md")

            fifo = actual / "pipe.md"
            os.mkfifo(fifo)
            with self.assertRaisesRegex(ValueError, "regular file"):
                self.archive._read_regular(fifo)

            parent = os.open(actual, self.archive._directory_flags())
            try:
                expected = os.stat("body.md", dir_fd=parent, follow_symlinks=False)
                replacement = actual / "replacement.md"
                replacement.write_text("changed\n", encoding="utf-8")
                os.replace(replacement, body)
                with self.assertRaisesRegex(ValueError, "changed while opening"):
                    self.archive._read_regular_at(
                        parent,
                        "body.md",
                        "body.md",
                        expected=expected,
                    )
            finally:
                os.close(parent)

    def test_archive_enumeration_and_aggregate_byte_limits_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive_root = pathlib.Path(directory) / "docs/98.archive"
            (archive_root / "migrations").mkdir(parents=True)
            (archive_root / "tombstones").mkdir()
            (archive_root / "README.md").write_text("README\n", encoding="utf-8")
            (archive_root / "extra.md").write_text("extra\n", encoding="utf-8")
            with mock.patch.object(self.archive, "MAX_ROOT_ENTRIES", 3):
                with self.assertRaisesRegex(ValueError, "entry limit"):
                    self.archive.load_archive(archive_root)

        with tempfile.TemporaryDirectory() as directory:
            archive_root = pathlib.Path(directory) / "docs/98.archive"
            (archive_root / "migrations").mkdir(parents=True)
            partition = archive_root / "tombstones/00.agent-governance"
            partition.mkdir(parents=True)
            (archive_root / "README.md").write_text("README\n", encoding="utf-8")
            source = next((ROOT / "docs/98.archive/tombstones").rglob("*.md"))
            (partition / "0001-sample.md").write_text(
                source.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            with mock.patch.object(self.archive, "MAX_ARCHIVE_BYTES", 1):
                with self.assertRaisesRegex(ValueError, "aggregate byte limit"):
                    self.archive.load_archive(archive_root)

    def test_frozen_migration_is_byte_identical_at_prefixless_path(self) -> None:
        path = ROOT / "docs/98.archive/migrations/0003-workspace-governance-simplification.md"
        self.assertEqual(
            "271f21c50cf4ab765422ee552de244a4340c160e53149231eb6be45f03476ab9",
            self.archive.sha256_file(path),
        )
        self.assertFalse((ROOT / "docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md").exists())


if __name__ == "__main__":
    unittest.main()
