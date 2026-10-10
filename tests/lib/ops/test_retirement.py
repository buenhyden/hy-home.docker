"""Exact retirement regressions use only synthetic temporary files."""

import json
import os
import subprocess
import tempfile
import unittest
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

from scripts.lib.ops import retire_materials as retirement

NOW = datetime(2026, 10, 10, 10, tzinfo=UTC)


class RetirementTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "secrets/db/legacy-app/unused.txt"
        self.path.parent.mkdir(parents=True)
        self.path.write_text("synthetic")
        self.row = self.receipt(self.path)

    def receipt(self, path):
        relative = path.relative_to(self.root)
        return {
            "id": "TEST-001",
            "path": relative.as_posix(),
            "scope": "root",
            "kind": "legacy-secret",
            "identity": retirement.identity(path),
            "parents": retirement.parent_identities(self.root, relative),
            "decision": "delete",
            "reviewed_at": NOW.isoformat(),
            "owner": "synthetic-operator",
            "evidence_ref": "task/cleanup",
            "checked": dict.fromkeys(retirement.CHECKS, True),
            "evidence": dict.fromkeys(retirement.CHECKS, "task/cleanup"),
            "consumers": [],
            "recovery_required": False,
            "maintenance": {
                "writers_stopped": True,
                "evidence_ref": "task/cleanup",
                "owner": "synthetic-operator",
                "reviewed_at": NOW.isoformat(),
            },
        }

    def assert_blocked(self, row):
        self.assertFalse(retirement.inspect_plan(self.root, [row], NOW)[0]["eligible"])
        with self.assertRaises(ValueError):
            retirement.apply_plan(self.root, [row], NOW)
        self.assertTrue(self.path.exists())

    def test_actual_delete_and_idempotent_retry(self):
        untouched = deepcopy(self.row)
        self.assertTrue(
            retirement.inspect_plan(self.root, [self.row], NOW)[0]["eligible"]
        )
        self.assertEqual(
            retirement.apply_plan(self.root, [self.row], NOW)[0]["result"], "deleted"
        )
        self.assertFalse(self.path.exists())
        self.assertEqual(
            retirement.apply_plan(self.root, [self.row], NOW)[0]["result"],
            "already-absent",
        )
        self.assertEqual(self.row, untouched)

    def test_retry_after_empty_parent_rmdir(self):
        retirement.apply_plan(self.root, [self.row], NOW)
        self.path.parent.rmdir()
        self.assertEqual(
            retirement.apply_plan(self.root, [self.row], NOW)[0]["result"],
            "already-absent",
        )

    def test_unknown_evidence_blocks_every_axis(self):
        for axis in retirement.CHECKS:
            for field, value in [("checked", False), ("evidence", "")]:
                with self.subTest(axis=axis, field=field):
                    row = deepcopy(self.row)
                    row[field][axis] = value
                    self.assert_blocked(row)

    def test_missing_or_malformed_receipt_fields_block(self):
        changes = [
            ("decision", "keep"),
            ("consumers", ["cold-start"]),
            ("consumers", None),
            ("recovery_required", True),
            ("checked", []),
            ("evidence", None),
            ("owner", ""),
            ("evidence_ref", ""),
            ("maintenance", None),
            ("maintenance", {"writers_stopped": False, "evidence_ref": "task/cleanup"}),
            ("maintenance", {"writers_stopped": True, "evidence_ref": ""}),
            ("parents", []),
        ]
        for field, value in changes:
            with self.subTest(field=field, value=value):
                row = {**self.row, field: value}
                self.assert_blocked(row)

    def test_backup_only_consumer_remains(self):
        self.assert_blocked({**self.row, "consumers": ["encrypted-snapshot-restore"]})

    def test_review_time_bounds(self):
        for stamp in [
            "",
            None,
            "broken",
            "2026-10-10T10:00:00",
            "2026-10-10T08:59:59+00:00",
            "2026-10-10T10:00:01+00:00",
        ]:
            with self.subTest(stamp=stamp):
                self.assert_blocked({**self.row, "reviewed_at": stamp})
        row = {**self.row, "reviewed_at": "2026-10-10T09:00:00Z"}
        self.assertTrue(retirement.inspect_plan(self.root, [row], NOW)[0]["eligible"])
        stale = {**self.row["maintenance"], "reviewed_at": "2026-10-01T00:00:00Z"}
        self.assert_blocked({**self.row, "maintenance": stale})

    def test_protected_and_invalid_paths(self):
        names = [
            "../outside",
            "/etc/passwd",
            "secrets//a",
            "secrets/./a",
            "secrets/a/../b",
            "secrets/a\\b",
            "secrets/a\nb",
            "secrets",
            "other/a",
            "secrets/labs/a",
            "secrets/backup/password.txt",
            "secrets/security/openbao/password.txt",
            "secrets/certs/a.txt",
            "docs/98.archive/history.md",
            "docs/.backup-old/a",
            "docs/.retired-other/a",
            "infra/.git/a",
            "infra/history/a",
            "infra/audit/a",
            retirement.CANONICAL_SMTP,
            "infra/common-optimizations.yml",
            "infra/common-optimizations.exceptions.json",
            "secrets/a/fernet.txt",
            "secrets/a/encryption.txt",
            "secrets/a/key.pem",
            "secrets/a/identity.txt",
            "infra/audit.jsonl",
            "docs/history.md",
            "infra/opaque.pem",
            "secrets/auth/oauth2-proxy/oauth2_proxy_cookie_secret.txt",
        ]
        for name in names:
            with self.subTest(name=name), self.assertRaises(ValueError):
                retirement.inspect_plan(self.root, [{**self.row, "path": name}], NOW)
        for changes in [{"scope": "lab"}, {"kind": "volume"}, {"id": "COMM-002"}]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                retirement.inspect_plan(self.root, [{**self.row, **changes}], NOW)

    def test_protected_crypto_ids_cannot_be_relabelled(self):
        for identifier in [
            "IAM-005",
            "SUPA-010",
            "AUTO-003",
            "AUTO-005",
            "AUTO-014",
            "AUTO-020",
            "AI-005",
            "CACHE-024",
            "SEC-003",
            "BKP-001",
            "LAB-015",
        ]:
            with self.subTest(identifier=identifier), self.assertRaises(ValueError):
                retirement.inspect_plan(
                    self.root, [{**self.row, "id": identifier}], NOW
                )

    def test_input_validation_and_duplicate_targets(self):
        for rows in [[self.row, self.row], [None], {}, [self.row] * 4097]:
            with self.subTest(kind=type(rows).__name__), self.assertRaises(ValueError):
                retirement.inspect_plan(self.root, rows, NOW)
        with self.assertRaises(ValueError):
            retirement.inspect_plan(self.root, [self.row], NOW.replace(tzinfo=None))
        with self.assertRaises(ValueError):
            retirement.parent_identities(self.root, Path("../outside"))
        with self.assertRaises(ValueError):
            retirement.parent_identities(self.root, Path("/outside"))

    def test_changed_identity_and_shared_inode(self):
        self.path.write_text("changed-size")
        self.assert_blocked(self.row)
        self.row = self.receipt(self.path)
        os.link(self.path, self.root / "shared.txt")
        row = self.receipt(self.path)
        self.assert_blocked(row)

    def test_parent_ctime_drift_and_parent_replacement(self):
        walk = retirement._walk

        def changed(*args, **kwargs):
            fd, parents = walk(*args, **kwargs)
            parents[-1]["identity"]["ctime_ns"] += 1
            return fd, parents

        with patch.object(retirement, "_walk", side_effect=changed):
            self.assert_blocked(self.row)
        self.row = self.receipt(self.path)
        moved = self.path.parent.with_name("original")
        self.path.parent.rename(moved)
        self.path.parent.mkdir()
        self.path.write_text("synthetic")
        self.assert_blocked(self.row)

    def test_symlink_target_parent_root_and_ancestor_refused(self):
        cases = ["target", "parent", "root", "ancestor"]
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                real = Path(tmp) / "real"
                target = real / "secrets/a/file.txt"
                target.parent.mkdir(parents=True)
                target.write_text("synthetic")
                row = {**self.row, "path": "secrets/a/file.txt"}
                if case == "target":
                    target.unlink()
                    target.symlink_to(self.path)
                    root = real
                elif case == "parent":
                    target.unlink()
                    target.parent.rmdir()
                    target.parent.symlink_to(self.path.parent, target_is_directory=True)
                    root = real
                elif case == "root":
                    root = Path(tmp) / "alias"
                    root.symlink_to(real, target_is_directory=True)
                else:
                    alias = Path(tmp) / "alias"
                    alias.symlink_to(real.parent, target_is_directory=True)
                    root = alias / "real"
                with self.assertRaises((ValueError, OSError)):
                    retirement.inspect_plan(root, [row], NOW)

    def test_nonregular_nodes_rejected_without_opening(self):
        self.path.unlink()
        os.mkfifo(self.path)
        with self.assertRaises(ValueError):
            retirement.inspect_plan(self.root, [self.row], NOW)
        self.path.unlink()
        self.path.mkdir()
        with self.assertRaises(ValueError):
            retirement.inspect_plan(self.root, [self.row], NOW)

    def test_invalid_root_spelling_refused(self):
        for root in ["relative", str(self.root) + "/..", str(self.root) + "//child"]:
            with self.subTest(root=root), self.assertRaises(ValueError):
                retirement.inspect_plan(root, [self.row], NOW)

    def test_whole_batch_preflight_and_same_parent_success(self):
        second = self.path.with_name("second.txt")
        second.write_text("synthetic")
        rows = [self.receipt(self.path), self.receipt(second)]
        bad = {**rows[1], "consumers": ["cold-start"]}
        with self.assertRaises(ValueError):
            retirement.apply_plan(self.root, [rows[0], bad], NOW)
        self.assertTrue(self.path.exists())
        self.assertTrue(second.exists())
        self.assertEqual(
            [item["result"] for item in retirement.apply_plan(self.root, rows, NOW)],
            ["deleted", "deleted"],
        )

    def test_tracking_refusal_and_git_failure_closed(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(
            ["git", "-C", str(self.root), "add", "--", self.row["path"]], check=True
        )
        self.row = self.receipt(self.path)
        self.assert_blocked(self.row)
        with patch.object(retirement.subprocess, "run") as command:
            command.return_value.returncode = 128
            with self.assertRaises(ValueError):
                retirement.inspect_plan(self.root, [self.row], NOW)

    def test_drift_between_full_preflight_and_handles_blocks_everything(self):
        original = retirement.inspect_plan

        def drift(*args, **kwargs):
            result = original(*args, **kwargs)
            self.path.write_text("changed after preflight")
            return result

        with (
            patch.object(retirement, "inspect_plan", side_effect=drift),
            self.assertRaises(ValueError),
        ):
            retirement.apply_plan(self.root, [self.row], NOW)
        self.assertTrue(self.path.exists())

    def test_parent_change_after_preflight_blocks_everything(self):
        original = retirement.inspect_plan

        def drift(*args, **kwargs):
            result = original(*args, **kwargs)
            self.row["parents"][-1]["identity"]["ctime_ns"] += 1
            return result

        with (
            patch.object(retirement, "inspect_plan", side_effect=drift),
            self.assertRaises(ValueError),
        ):
            retirement.apply_plan(self.root, [self.row], NOW)
        self.assertTrue(self.path.exists())

    def test_target_drift_immediately_before_unlink(self):
        original = retirement._unlink_regular

        def drift(root, row, handle, updates):
            self.path.write_text("changed during apply")
            return original(root, row, handle, updates)

        with patch.object(retirement, "_unlink_regular", side_effect=drift):
            with self.assertRaises(retirement.PartialFailure) as caught:
                retirement.apply_plan(self.root, [self.row], NOW)
        self.assertEqual(caught.exception.results[0]["result"], "failed")
        self.assertTrue(self.path.exists())

    def test_parent_drift_immediately_before_unlink(self):
        original = retirement._unlink_regular

        def drift(root, row, handle, updates):
            self.path.with_name("concurrent.txt").write_text("synthetic")
            return original(root, row, handle, updates)

        with patch.object(retirement, "_unlink_regular", side_effect=drift):
            with self.assertRaises(retirement.PartialFailure):
                retirement.apply_plan(self.root, [self.row], NOW)
        self.assertTrue(self.path.exists())

    def test_partial_failure_reports_deleted_failed_and_unattempted(self):
        paths = [
            self.path,
            self.path.with_name("second.txt"),
            self.path.with_name("third.txt"),
        ]
        for path in paths[1:]:
            path.write_text("synthetic")
        rows = [self.receipt(path) for path in paths]
        unlink = os.unlink

        def fail_second(name, *, dir_fd=None):
            if name == "second.txt":
                raise OSError("synthetic sensitive error")
            return unlink(name, dir_fd=dir_fd)

        with patch.object(retirement.os, "unlink", side_effect=fail_second):
            with self.assertRaises(retirement.PartialFailure) as caught:
                retirement.apply_plan(self.root, rows, NOW)
        self.assertEqual(
            [item["result"] for item in caught.exception.results],
            ["deleted", "failed", "not-attempted"],
        )
        self.assertFalse(paths[0].exists())
        self.assertTrue(paths[1].exists())
        self.assertTrue(paths[2].exists())

    def test_fsync_failure_preserves_actual_unlink_status(self):
        with patch.object(
            retirement.os, "fsync", side_effect=OSError("synthetic sensitive error")
        ):
            with self.assertRaises(retirement.PartialFailure) as caught:
                retirement.apply_plan(self.root, [self.row], NOW)
        self.assertEqual(
            caught.exception.results[0]["result"], "deleted-durability-unknown"
        )
        self.assertFalse(self.path.exists())

    def test_postunlink_link_change_reports_unconfirmed_deletion(self):
        unlink = os.unlink

        def relink(name, *, dir_fd=None):
            os.link(name, "unexpected-link.txt", src_dir_fd=dir_fd, dst_dir_fd=dir_fd)
            return unlink(name, dir_fd=dir_fd)

        with patch.object(retirement.os, "unlink", side_effect=relink):
            with self.assertRaises(retirement.PartialFailure) as caught:
                retirement.apply_plan(self.root, [self.row], NOW)
        self.assertEqual(
            caught.exception.results[0]["result"], "deleted-identity-unconfirmed"
        )
        self.assertFalse(self.path.exists())

    def test_absent_target_reappearing_after_preflight_blocks_batch(self):
        self.path.unlink()
        original = retirement.inspect_plan

        def recreate(*args, **kwargs):
            result = original(*args, **kwargs)
            self.path.write_text("new active material")
            return result

        with patch.object(retirement, "inspect_plan", side_effect=recreate):
            with self.assertRaises(ValueError):
                retirement.apply_plan(self.root, [self.row], NOW)
        self.assertTrue(self.path.exists())

    def test_replacement_during_unlink_is_never_success(self):
        unlink = os.unlink

        def replace(name, *, dir_fd=None):
            result = unlink(name, dir_fd=dir_fd)
            self.path.write_text("new active material")
            return result

        with patch.object(retirement.os, "unlink", side_effect=replace):
            with self.assertRaises(retirement.PartialFailure) as caught:
                retirement.apply_plan(self.root, [self.row], NOW)
        self.assertEqual(
            caught.exception.results[0]["result"], "deleted-identity-unconfirmed"
        )
        self.assertTrue(self.path.exists())

    def test_shared_lock_rejects_concurrent_acquisition(self):
        with retirement.retirement_lock(self.root):
            with self.assertRaises(OSError):
                with retirement.retirement_lock(self.root):
                    pass

    def test_lock_file_permissions_and_symlink_refused(self):
        info = self.root.stat()
        digest = retirement.hashlib.sha256(
            f"{info.st_dev}:{info.st_ino}".encode("ascii")
        ).hexdigest()
        directory = Path("/tmp") / f"cln01-retirement-{os.getuid()}-{digest}"
        with retirement.retirement_lock(self.root):
            pass
        lock = directory / "lock"
        lock.chmod(0o644)
        try:
            with self.assertRaises(ValueError):
                with retirement.retirement_lock(self.root):
                    pass
        finally:
            lock.chmod(0o600)
        lock.unlink()
        lock.symlink_to(self.path)
        try:
            with self.assertRaises(OSError):
                with retirement.retirement_lock(self.root):
                    pass
        finally:
            lock.unlink()

    def test_lock_directory_permissions_refused(self):
        info = self.root.stat()
        digest = retirement.hashlib.sha256(
            f"{info.st_dev}:{info.st_ino}".encode("ascii")
        ).hexdigest()
        directory = Path("/tmp") / f"cln01-retirement-{os.getuid()}-{digest}"
        directory.mkdir(mode=0o700, exist_ok=True)
        directory.chmod(0o755)
        try:
            with self.assertRaises(ValueError):
                with retirement.retirement_lock(self.root):
                    pass
        finally:
            directory.chmod(0o700)

    def test_unicode_format_and_control_path_characters_rejected(self):
        for marker in ["\u202e", "\u2066", "\u200b", "\x7f", "\ud800"]:
            row = {**self.row, "path": "secrets/db/legacy-app/" + marker + "unused.txt"}
            with self.subTest(codepoint=ord(marker)), self.assertRaises(ValueError):
                retirement.inspect_plan(self.root, [row], NOW)

    def test_review_root_double_slash_alias_rejected(self):
        alias = "/" + str(self.root)
        with self.assertRaises(ValueError):
            retirement.inspect_plan(alias, [self.row], NOW)

    def test_review_internal_manifest_double_slash_alias_rejected(self):
        inside = self.manifest(self.root)
        with self.assertRaises(ValueError):
            retirement.load_manifest(self.root, Path("/" + str(inside)))

    def test_review_opened_root_identity_prevents_manifest_ancestor_alias(self):
        info = self.root.stat()
        with self.assertRaises(ValueError):
            retirement._exact_root(
                self.root, forbidden_identity=(info.st_dev, info.st_ino)
            )

    def test_review_shared_lock_uses_opened_inode_despite_alias_label(self):
        exact = retirement._exact_root

        def alias_root(root, *args, **kwargs):
            _, fd = exact(self.root, *args, **kwargs)
            return Path("/tmp/synthetic-alias-label"), fd

        with retirement.retirement_lock(self.root):
            with patch.object(retirement, "_exact_root", side_effect=alias_root):
                with self.assertRaises(OSError):
                    with retirement.retirement_lock(Path("/tmp/synthetic-alias-label")):
                        pass

    def test_smtp_duplicate_route_owned_by_smtp01_is_held(self):
        for change in [
            {"id": "COMM-003"},
            {"path": "secrets/communication/supabase/supabase_smtp_password.txt"},
            {
                "path": "secrets/communication/supabase/supabase_smtp_password.txt",
                "id": "TEST-001",
            },
        ]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                retirement.inspect_plan(self.root, [{**self.row, **change}], NOW)

    def test_review_retained_pg020_path_and_identifier_are_hard_protected(self):
        for change in [
            {"id": "PG-020"},
            {"path": "secrets/db/legacy-app/service_password.txt"},
            {"path": "secrets/db/legacy-app/service_password.txt", "id": "TEST-001"},
        ]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                retirement.inspect_plan(self.root, [{**self.row, **change}], NOW)

    def test_review_missing_and_malformed_material_identifier_refused(self):
        for identifier in [None, "", [], {}, "TEST 001", "test-001", "../TEST-001"]:
            with self.subTest(identifier=identifier), self.assertRaises(ValueError):
                retirement.inspect_plan(
                    self.root, [{**self.row, "id": identifier}], NOW
                )

    def test_review_maintenance_owner_and_timestamp_required(self):
        for maintenance in [
            {"writers_stopped": True, "evidence_ref": "task/cleanup"},
            {**self.row["maintenance"], "owner": "", "reviewed_at": NOW.isoformat()},
            {
                "writers_stopped": True,
                "evidence_ref": "task/cleanup",
                "owner": "operator",
            },
            {
                **self.row["maintenance"],
                "owner": "operator",
                "reviewed_at": "2026-10-10T08:59:59Z",
            },
            {
                **self.row["maintenance"],
                "owner": "operator",
                "reviewed_at": "2026-10-10T10:00:01Z",
            },
        ]:
            with self.subTest(maintenance=maintenance):
                self.assert_blocked({**self.row, "maintenance": maintenance})

    def test_review_tracking_refuses_caller_git_index_and_directory_overrides(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(
            ["git", "-C", str(self.root), "add", "--", self.row["path"]], check=True
        )
        self.row = self.receipt(self.path)
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp)
            subprocess.run(["git", "init", "-q", str(fake)], check=True)
            overrides = [
                {"GIT_INDEX_FILE": str(fake / "empty-index")},
                {"GIT_DIR": str(fake / ".git"), "GIT_WORK_TREE": str(fake)},
            ]
            for override in overrides:
                with (
                    self.subTest(override=tuple(override)),
                    patch.dict(os.environ, override),
                ):
                    self.assert_blocked(self.row)

    def test_review_nested_repository_root_is_refused(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        nested = self.root / "nested"
        target = nested / self.row["path"]
        target.parent.mkdir(parents=True)
        target.write_text("synthetic")
        with self.assertRaises(ValueError):
            retirement.inspect_plan(nested, [self.row], NOW)

    def manifest(self, parent, changes=None):
        parent.chmod(0o700)
        path = parent / "receipt.json"
        doc = {"entries": [self.row], **(changes or {})}
        path.write_text(json.dumps(doc))
        path.chmod(0o600)
        return path

    def test_private_manifest_and_maintenance_injection(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            row = {
                key: value for key, value in self.row.items() if key != "maintenance"
            }
            path = self.manifest(
                parent, {"entries": [row], "maintenance": self.row["maintenance"]}
            )
            doc = retirement.load_manifest(self.root, path)
            self.assertEqual(doc["entries"][0]["maintenance"], self.row["maintenance"])
            self.assertNotIn("maintenance", row)

    def test_manifest_protection_and_invalid_shape(self):
        inside = self.manifest(self.root)
        with self.assertRaises(ValueError):
            retirement.load_manifest(self.root, inside)
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            path = self.manifest(parent)
            parent.chmod(0o755)
            with self.assertRaises(ValueError):
                retirement.load_manifest(self.root, path)
            parent.chmod(0o700)
            path.chmod(0o644)
            with self.assertRaises(ValueError):
                retirement.load_manifest(self.root, path)
            path.chmod(0o600)
            os.link(path, parent / "hardlink.json")
            with self.assertRaises(ValueError):
                retirement.load_manifest(self.root, path)
            (parent / "hardlink.json").unlink()
            for document in [
                [],
                {"entries": {}},
                {"entries": [None]},
                {"entries": "sensitive"},
            ]:
                path.write_text(json.dumps(document))
                with (
                    self.subTest(document_type=type(document).__name__),
                    self.assertRaises(ValueError),
                ):
                    retirement.load_manifest(self.root, path)
            path.write_text("x" * (retirement.MAX_MANIFEST + 1))
            with self.assertRaises(ValueError):
                retirement.load_manifest(self.root, path)
            path.unlink()
            path.symlink_to(inside)
            with self.assertRaises(OSError):
                retirement.load_manifest(self.root, path)

    def test_manifest_owner_and_snapshot_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.manifest(Path(tmp))
            with patch.object(retirement.os, "getuid", return_value=os.getuid() + 1):
                with self.assertRaises(ValueError):
                    retirement.load_manifest(self.root, path)
            read = os.read

            def mutate(fd, length):
                raw = read(fd, length)
                path.write_text("changed")
                return raw

            with patch.object(retirement.os, "read", side_effect=mutate):
                with self.assertRaises(ValueError):
                    retirement.load_manifest(self.root, path)


if __name__ == "__main__":
    unittest.main()
