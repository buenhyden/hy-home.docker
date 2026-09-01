from __future__ import annotations

import ast
import collections
import copy
import os
import pathlib
import re
import subprocess
import tempfile
import unittest
from unittest import mock

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[3]
TASK10_BASELINE = "f259c139fb7da166609029cdd3657de87e639f6b"


def archive_api():
    try:
        from scripts.lib.document_governance import archive
    except ImportError as exc:
        raise AssertionError("Task 10 archive authority is missing") from exc
    return archive


class MigrationStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.archive = archive_api()
        self.commit = "494065806794980080b081439298d7b534d10803"
        self.row = {
            "row_id": "mig-0003-r0001", "source_path": "docs/99.templates/support/README.md",
            "target_path": None, "artifact_id": None, "action": "delete",
            "owner_task": 13, "source_kind": "tracked", "source_owner_task": None,
            "active_consumers": [], "recovery_commit": None, "status": "planned",
        }
        self.approved = {
            "schema_version": 2, "migration_id": "mig-0003", "rows": [self.row],
            "baseline_commit": self.commit, "approval": {"status": "approved"},
            "consumer_policy": {}, "final_compaction": {}, "planned_creations": [],
        }

    def read(self, document):
        raw = ("```yaml\n" + yaml.safe_dump(document) + "```\n").encode()
        with mock.patch.object(self.archive, "_read_regular", return_value=raw), mock.patch.object(
            self.archive, "_approved_migration_document", return_value=copy.deepcopy(self.approved),
            create=True,
        ):
            return self.archive._migration_document(ROOT)

    def compact(self):
        row = {key: self.row[key] for key in (
            "source_path", "target_path", "artifact_id", "action", "recovery_commit"
        )}
        row["recovery_commit"] = self.commit
        additions = [
            {"source_path": path, "target_path": None, "artifact_id": None,
             "action": "delete", "recovery_commit": self.commit}
            for path in self.archive.ONE_TIME_VERIFIER_PATHS
        ]
        additions.extend(
            {"source_path": f"docs/03.specs/{slug}/spec.md", "target_path": None,
             "artifact_id": f"SPEC-{slug[:4]}", "action": "delete", "recovery_commit": self.commit}
            for slug in ("0090-workspace-audit-2026-05", "0091-workspace-doc-consistency-2026-05",
                         "0092-workspace-consistency-2026-05b")
        )
        return {"schema_version": 3, "migration_id": "mig-0003", "rows": [row, *additions]}

    def test_live_reader_accepts_native_approved_completed_and_compact_states(self):
        self.assertEqual(self.approved, self.read(self.approved))
        completed = copy.deepcopy(self.approved)
        completed["rows"][0].update(status="completed", recovery_commit=self.commit)
        self.assertEqual(completed, self.read(completed))
        self.assertEqual(self.compact(), self.read(self.compact()))

    def test_compact_projection_normalizes_only_five_approved_singular_targets(self):
        approved = self.archive._approved_migration_document(ROOT)
        projected = self.archive._compact_mapping_selection(approved)
        retained = [row for row in approved["rows"] if row["row_id"] not in {"mig-0003-r0842", "mig-0003-r0848", "mig-0003-r0852"}]
        # Derived from the frozen ledger this test already read. The digest
        # tripwire proves that ledger is byte-identical, so a literal count
        # here would only restate what the digest already guarantees.
        self.assertEqual(len(retained), len(projected))
        changed = [row["row_id"] for row, result in zip(retained, projected, strict=True)
                   if row["target_path"] != result["target_path"]]
        self.assertEqual([f"mig-0003-r{n:04d}" for n in (233, 239, 242, 245, 248)], changed)
        expected_targets = {
            "mig-0003-r0233": "docs/03.specs/0123-agentic-engineering-audit-remediation/tasks/tsk-0001-research-pack-extension.md",
            "mig-0003-r0239": "docs/03.specs/0134-agent-governance-canonical-convergence/tasks/tsk-0001-canonical-convergence.md",
            "mig-0003-r0242": "docs/03.specs/0135-target-surface-delta-convergence/tasks/tsk-0001-delta-convergence.md",
            "mig-0003-r0245": "docs/03.specs/0136-sdlc-taxonomy-convergence/tasks/tsk-0001-taxonomy-convergence.md",
            "mig-0003-r0248": "docs/03.specs/0152-deleted-reference-leaf-disposition/tasks/tsk-0001-reference-disposition.md",
        }
        for row, result in zip(retained, projected, strict=True):
            expected = {
                key: row[key]
                for key in ("source_path", "target_path", "artifact_id", "action")
            }
            if row["row_id"] in expected_targets:
                expected["target_path"] = expected_targets[row["row_id"]]
            self.assertEqual(result, expected)

    def test_compact_projection_has_real_recovery_and_no_retained_owner_deletion(self):
        approved = self.archive._approved_migration_document(ROOT)
        rows = self.archive._compact_mapping_selection(approved)
        sources = [row["source_path"] for row in rows]
        recoveries = {}
        for commit in (approved["baseline_commit"], "71f89ba1430245c89d10c36a084fc2fae9cfe98b", self.commit):
            for offset in range(0, len(sources), 512):
                batch = sources[offset:offset + 512]
                proofs = self.archive.verify_recovery_blobs_batch(
                    [(path, commit) for path in batch], repo_root=ROOT,
                )
                for path, proof in zip(batch, proofs, strict=True):
                    if proof.is_regular_blob:
                        recoveries.setdefault(path, commit)
        self.assertEqual(set(sources), set(recoveries))
        rows = [{**row, "recovery_commit": recoveries[row["source_path"]]} for row in rows]
        appended = self.compact()["rows"][1:]
        expected_rows = len(rows) + len(appended)
        rows.extend(appended)
        self.assertEqual(expected_rows, len(rows))
        compact = {"schema_version": 3, "migration_id": "mig-0003", "rows": rows}
        raw = ("```yaml\n" + yaml.safe_dump(compact) + "```\n").encode()
        with mock.patch.object(self.archive, "_read_regular", return_value=raw):
            self.assertEqual(compact, self.archive._migration_document(ROOT))
        unexecuted = [
            row
            for row in approved["rows"]
            if row["row_id"] in {"mig-0003-r0848", "mig-0003-r0852"}
        ]
        for row in unexecuted:
            self.assertTrue((ROOT / row["source_path"]).is_file())
            self.assertNotIn(row["source_path"], sources)
        for mutation in (rows[:-1], rows + [rows[0]], [rows[1], rows[0], *rows[2:]]):
            raw = ("```yaml\n" + yaml.safe_dump({**compact, "rows": mutation}) + "```\n").encode()
            with self.subTest(rows=len(mutation)), mock.patch.object(self.archive, "_read_regular", return_value=raw), self.assertRaises(ValueError):
                self.archive._migration_document(ROOT)

    def test_live_reader_rejects_multiple_or_unterminated_ledger_fences(self):
        valid = "```yaml\n" + yaml.safe_dump(self.approved) + "```\n"
        for candidate in (valid + valid, valid.removesuffix("```\n")):
            with self.subTest(terminated=candidate.endswith("```\n")), mock.patch.object(
                self.archive, "_read_regular", return_value=candidate.encode(),
            ), mock.patch.object(
                self.archive, "_approved_migration_document", return_value=self.approved,
            ), self.assertRaisesRegex(ValueError, "fenced"):
                self.archive._migration_document(ROOT)

    def test_compact_live_reader_rejects_missing_extra_duplicate_unsafe_and_wrong_recovery(self):
        cases = []
        for key in self.approved:
            if key not in self.compact():
                candidate = self.compact()
                candidate[key] = self.approved[key]
                cases.append(candidate)
        for key in self.row:
            if key not in self.compact()["rows"][0]:
                candidate = self.compact()
                candidate["rows"][0][key] = self.row[key]
                cases.append(candidate)
        for key, value in (("source_path", "../outside"), ("source_path", "docs/unknown.md"),
                           ("target_path", "../outside"), ("recovery_commit", None),
                           ("recovery_commit", "HEAD"), ("recovery_commit", "0" * 40),
                           ("action", "unknown"), ("artifact_id", "unexpected")):
            candidate = self.compact()
            candidate["rows"][0][key] = value
            cases.append(candidate)
        candidate = self.compact()
        candidate["rows"] = []
        cases.append(candidate)
        candidate = self.compact()
        candidate["rows"] *= 2
        cases.append(candidate)
        candidate = self.compact()
        candidate["rows"].pop()
        cases.append(candidate)
        candidate = self.compact()
        candidate["rows"][-1]["source_path"] = "scripts/unapproved.py"
        cases.append(candidate)
        candidate = self.compact()
        candidate["rows"][-1]["recovery_commit"] = "889d3868ecd0913cddac79a718584a54a8453525"
        cases.append(candidate)
        for index, candidate in enumerate(cases):
            with self.subTest(case=index), self.assertRaises(ValueError):
                self.read(candidate)

    def test_execution_changes_are_limited_to_completed_status_and_proved_recovery(self):
        for key, value in (("status", "unknown"), ("status", "completed"),
                           ("recovery_commit", self.commit), ("owner_task", 1),
                           ("active_consumers", ["docs/unapproved.md"])):
            candidate = copy.deepcopy(self.approved)
            candidate["rows"][0][key] = value
            with self.subTest(field=key), self.assertRaises(ValueError):
                self.read(candidate)
        candidate = copy.deepcopy(self.approved)
        candidate["approval"] = {"status": "draft"}
        with self.assertRaises(ValueError):
            self.read(candidate)

    def test_native_compact_rows_reach_remaining_archive_consumers(self):

        approved = self.archive._approved_migration_document(ROOT)
        compact = {"schema_version": 3, "migration_id": "mig-0003", "rows": [
            {**{key: row[key] for key in ("source_path", "target_path", "artifact_id", "action")},
             "recovery_commit": self.commit}
            for row in approved["rows"]
        ]}
        first = self.archive.TASK10_FIRST_ROW
        last = self.archive.TASK10_LAST_ROW
        expected = [
            row
            for row in approved["rows"]
            if first <= row["row_id"] <= last
        ]
        with mock.patch.object(self.archive, "_migration_document", return_value=compact):
            self.assertEqual(len(expected), len(self.archive.task10_rows(ROOT)))


class ArchiveMinimizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.archive = archive_api()

    def test_no_census_literal_pins_archive_content(self) -> None:
        """A count that describes repository content is computed from it.

        Authoring one tombstone during SPEC-0157's design broke eleven
        hand-maintained counts, one of them encoded in a test's name. Each had
        to be found and advanced by hand, and finding them was the expensive
        part.
        """

        sources = (
            pathlib.Path("scripts/lib/document_governance/archive.py"),
            pathlib.Path("tests/lib/document_governance/test_archive.py"),
            *(
                path.relative_to(ROOT)
                for path in sorted(
                    (ROOT / "tests/validation/lifecycle").glob("*.py")
                )
            ),
        )
        offenders = []
        for source in sources:
            text = (ROOT / source).read_text(encoding="utf-8")
            for pattern in (
                r"tombstones\s*=\s*\d+",
                r"recovery_rows\s*=\s*\d+",
                r"decisions\s*=\s*\d+",
                r"TASK10_RECOVERY_REFERENCE_COUNT\s*=\s*\d+",
                r"assertEqual\(\s*\d+\s*,\s*len\(inventory\.tombstones\)\)",
                r"(?:load_task10_recovery_references\(ROOT\)"
                r"|item\.recovery for item in inventory\.tombstones)"
                r"[\s\S]{0,240}?assertEqual\(\s*\d+\s*,\s*len\(rows\)\)",
            ):
                offenders.extend(
                    f"{source}:{match}" for match in re.findall(pattern, text)
                )
        self.assertEqual([], offenders)

    def test_no_current_repository_spec_package_cardinality_pin(self) -> None:
        """The current repository surface is derived from its spec directories."""

        source = ROOT / "tests/lib/document_governance/test_spec_packages.py"
        tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        offenders = []
        for method in ast.walk(tree):
            if not isinstance(method, ast.FunctionDef) or not method.name.startswith(
                "test_current_repository_"
            ):
                continue
            for call in ast.walk(method):
                if not (
                    isinstance(call, ast.Call)
                    and isinstance(call.func, ast.Attribute)
                    and call.func.attr == "assertEqual"
                    and len(call.args) >= 2
                ):
                    continue
                for literal, candidate in (call.args[:2], call.args[1::-1]):
                    if not (
                        isinstance(literal, ast.Constant)
                        and isinstance(literal.value, int)
                        and isinstance(candidate, ast.Call)
                        and isinstance(candidate.func, ast.Name)
                        and candidate.func.id == "len"
                        and len(candidate.args) == 1
                        and isinstance(candidate.args[0], ast.Name)
                        and candidate.args[0].id == "packages"
                    ):
                        continue
                    offenders.append(f"{method.name}:{literal.value}")
        self.assertEqual([], offenders)

    def test_archive_has_only_registered_minimal_roots(self) -> None:
        inventory = self.archive.load_archive(ROOT / "docs/98.archive")
        self.assertEqual(("README.md", "migrations", "tombstones"), inventory.root_entries)
        self.assertEqual(3, len(inventory.migrations))
        tombstone_files = [
            path
            for path in (ROOT / "docs/98.archive/tombstones").rglob("*.md")
            if path.name.upper() != "README.MD"
        ]
        self.assertEqual(len(tombstone_files), len(inventory.tombstones))
        self.assertTrue(all(item.is_minimal for item in inventory.tombstones))
        self.assertFalse((ROOT / "docs/98.archive/changes").exists())

    def test_every_preservation_decision_is_unique_and_reviewed(self) -> None:
        """Stated as relations, so authoring a tombstone does not edit this test.

        The three counts this replaced (189 decisions, 146 git-only with 43
        minimal-tombstone, 189 distinct paths) all moved together whenever a
        tombstone was written, and each had to be found and advanced by hand.
        What the test is actually for is that every decision names a distinct
        path, that a minimal-tombstone decision exists for exactly the
        tombstones the archive holds, and that every decision is approved and
        recoverable. None of that needs a literal.
        """

        decisions = self.archive.load_task10_preservation_decisions(ROOT)
        inventory = self.archive.load_archive(ROOT / "docs/98.archive")
        self.assertEqual(len(decisions), len({item.stable_path for item in decisions}))
        dispositions = collections.Counter(item.disposition for item in decisions)
        self.assertEqual({"git-only", "minimal-tombstone"}, set(dispositions))
        self.assertEqual(len(inventory.tombstones), dispositions["minimal-tombstone"])
        self.assertEqual(len(decisions), sum(dispositions.values()))
        self.assertTrue(all(item.reviewer_decision == "approved" for item in decisions))
        self.assertTrue(all(item.recovery.commit for item in decisions))

    def test_only_the_reviewed_baseline_paths_may_lack_metadata(self) -> None:
        from scripts.lib.document_governance import git_provenance

        approved = tuple(sorted(self.archive.APPROVED_BASELINE_RECOVERY_PATHS))
        self.assertTrue(approved)
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
        self.assertEqual(len(rows), len(set(rows)))
        original_paths = {row.original_path for row in rows}
        retired_paths_on_disk = set()
        for tombstone_file in (ROOT / "docs/98.archive/tombstones").rglob("*.md"):
            if tombstone_file.name.upper() == "README.MD":
                continue
            match = re.search(
                r"(?ms)^## Retired Path\s*$\n\s*`([^`]+)`",
                tombstone_file.read_text(encoding="utf-8"),
            )
            self.assertIsNotNone(match, tombstone_file)
            retired_paths_on_disk.add(pathlib.PurePosixPath(match.group(1)))
        self.assertTrue(retired_paths_on_disk.issubset(original_paths))
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
        """Repaired 2026-08-29; it had stopped testing anything.

        Two independent breakages had accumulated. The ledger was projected to
        the compact schema-3 form, so three of the four mutation strings —
        `owner_task`, `row_id` — no longer occur in the file and `str.replace`
        returned it unchanged; the test was feeding the ORIGINAL bytes and
        asserting they were rejected. And the fixture root held only the ledger
        with no git repository, so `git cat-file --batch-check` failed before the
        digest comparison was ever reached, which is the `ValueError` the
        assertion was actually catching. Together those meant the test would have
        passed on a clean file and failed on nothing. The mutations below are
        expressed against the schema-3 row shape, and the root is a shared clone
        so the recovery commits resolve and the digest check is what answers.
        """

        approved = self.archive._approved_migration_document(ROOT)
        ledger_relative = (
            "docs/98.archive/migrations/0003-workspace-governance-simplification.md"
        )
        original = (ROOT / ledger_relative).read_text(encoding="utf-8")
        row = (
            "- source_path: docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md\n"
            "  target_path: docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md\n"
            "  artifact_id: mig-0001\n"
            "  action: rename\n"
        )
        self.assertEqual(1, original.count(row))
        # Each mutation is paired with the guard it must trip. Asserting one
        # shared message would have hidden which defence actually answered, and
        # two of these are caught by a structural rule BEFORE the digest, which
        # is a stronger rejection rather than a weaker one.
        mutations = (
            # same shape, different executed semantics: a rename becomes a delete
            (
                original.replace(row, row.replace("action: rename", "action: delete"), 1),
                "action and target disagree",
            ),
            # same shape, different destination: only the digest can see this
            (
                original.replace(row, row.replace("0001-sdlc", "0009-sdlc"), 1),
                "frozen digest",
            ),
            # same shape, source escapes the repository
            (
                original.replace(
                    "source_path: docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md",
                    "source_path: ../outside.md",
                    1,
                ),
                "path is invalid",
            ),
        )
        for index, (mutation, expected) in enumerate(mutations):
            with self.subTest(index=index):
                self.assertNotEqual(original, mutation, "mutation must change the file")
            with self.subTest(index=index), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                subprocess.run(
                    ("git", "clone", "--shared", "--no-checkout", "--quiet", str(ROOT), str(root)),
                    check=True,
                )
                target = root / "docs/98.archive/migrations"
                target.mkdir(parents=True)
                (target / "0003-workspace-governance-simplification.md").write_text(
                    mutation,
                    encoding="utf-8",
                )
                with mock.patch.object(
                    self.archive, "_approved_migration_document", return_value=approved,
                ), self.assertRaisesRegex(ValueError, expected):
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

    def test_every_frozen_migration_is_byte_identical(self) -> None:
        """0001 and 0002 had no integrity control until 2026-09-02.

        Only 0003 was digest-tripwired. The action-count maps in
        `lifecycle/promoted.py` were the sole thing standing between 0001 and a
        silent edit, and a count cannot see a changed path or commit. All three
        retained ledgers are frozen evidence, so all three are pinned here.
        """

        for name, digest in (
            (
                "0001-sdlc-taxonomy-convergence.md",
                "08275f2a4a9f4ac60114af382d9da1de90425e2b28510f327425a10d3a7b4729",
            ),
            (
                "0002-operations-catalog-convergence.md",
                "060c455eb0a2ed78aef419834ea99dd84f911668739d14ed3c7bbcd3e188ac12",
            ),
        ):
            with self.subTest(migration=name):
                self.assertEqual(
                    digest,
                    self.archive.sha256_file(
                        ROOT / "docs/98.archive/migrations" / name
                    ),
                )

    def test_frozen_migration_is_byte_identical_at_prefixless_path(self) -> None:
        # Repinned 2026-09-02. The artifact-identity convergence moved this
        # ledger's own frontmatter to the `type`/`artifact_id` envelope
        # (`MIG-0003`). The fenced evidence block is byte-identical to its
        # predecessor and `archive._migration_document` still reverifies it
        # against the approved Git blob; only frontmatter moved.
        path = ROOT / "docs/98.archive/migrations/0003-workspace-governance-simplification.md"
        self.assertEqual(
            "33be9ffe500b1edc8af6c0a76feaa4466a97dc9aff29669124a339bf5550ffdb",
            self.archive.sha256_file(path),
        )
        self.assertFalse((ROOT / "docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md").exists())


if __name__ == "__main__":
    unittest.main()
