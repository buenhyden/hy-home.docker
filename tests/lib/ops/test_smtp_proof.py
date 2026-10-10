"""Fail-closed SMTP retirement proof boundary regressions."""

import json
import os
import stat
import subprocess
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

import yaml

from scripts.lib.ops import smtp_contract as module
from scripts.lib.ops.smtp_contract import (
    CANONICAL,
    CANONICAL_PATH,
    OLD,
    ContractError,
    metadata_retired,
    root_identity,
    source_hashes,
    verify_proof,
)

NOW = datetime(2026, 10, 10, 10, 0, tzinfo=UTC)
ROOT = Path(__file__).parents[3]
MOUNT_CASES = (
    ({"Type": "bind", "Source": "OLD", "Destination": "/x", "RW": False}, True),
    (
        {"Type": "bind", "Source": "PARENT", "Destination": "/x", "RW": False},
        True,
    ),
    (
        {
            "Type": "bind",
            "Source": "SECRETS",
            "Destination": "/src/host/secrets",
            "RW": False,
        },
        True,
    ),
    ({"Type": "volume", "Source": "OLD", "Destination": "/x", "RW": False}, False),
    (
        {"Type": "bind", "Source": "/unrelated", "Destination": "/x", "RW": False},
        False,
    ),
)


class SMTPProofTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.base = Path(directory.name)
        self.root = self.base / "root"
        include = self.root / "infra/auth.yml"
        include.parent.mkdir(parents=True)
        (self.root / "docker-compose.yml").write_text(
            yaml.safe_dump(
                {
                    "include": ["infra/auth.yml"],
                    "secrets": {CANONICAL: {"file": CANONICAL_PATH}},
                }
            )
        )
        include.write_text(
            yaml.safe_dump(
                {
                    "services": {
                        "auth": {"secrets": [{"source": CANONICAL, "target": OLD}]}
                    }
                }
            )
        )
        self.proof_parent = self.base / "operator-proof"
        self.proof_parent.mkdir(mode=0o700)
        self.proof = self.proof_parent / "smtp01.json"
        self.receipt = self._receipt()
        self._write(self.receipt)
        runner = patch.object(module, "_run", side_effect=self._run)
        clock = patch.object(module, "_now", return_value=NOW, create=True)
        runner.start()
        clock.start()
        self.addCleanup(runner.stop)
        self.addCleanup(clock.stop)

    def _receipt(self):
        return {
            "host": module.socket.gethostname(),
            "git_sha": "synthetic-sha",
            "source_sha256": source_hashes(self.root),
            "old_mount_consumers": [],
            "job_backup_external_verified": True,
            "canonical_restore_mapping_verified": True,
            "consumer_creation_quiesced": True,
            "source_private_mutation_quiesced": True,
            "root_identity": root_identity(self.root),
            "operation": "retire-supabase-smtp",
            "target": "COMM-003",
            "observation_id": "SMTP01:synthetic-observation-1",
            "approval_record": "TASK:synthetic-approval-1",
            "observed_at": "2026-10-10T09:58:00Z",
            "expires_at": "2026-10-10T10:05:00Z",
        }

    def _run(self, arguments, root=None):
        if arguments[0] == "git":
            return b"synthetic-sha\n"
        if arguments[:3] == ["docker", "ps", "-aq"]:
            return b""
        raise AssertionError("unexpected synthetic command")

    def _write(self, receipt, path=None):
        path = path or self.proof
        path.write_text(json.dumps(receipt))
        path.chmod(0o600)
        return path

    def _reject(self, path=None):
        with self.assertRaises(ContractError):
            verify_proof(self.root, path or self.proof)

    def test_fresh_external_owner_only_receipt_is_accepted(self):
        verify_proof(self.root, self.proof)

    def test_proof_path_rejects_links_modes_location_and_unsafe_parent(self):
        for case in (
            "symlink",
            "hardlink",
            "mode",
            "in_root",
            "dotdot_in_root",
            "parent_mode",
        ):
            with self.subTest(case=case):
                self._write(self.receipt)
                path = self.proof
                if case == "symlink":
                    target = self._write(self.receipt, self.proof_parent / "target")
                    path.unlink()
                    path.symlink_to(target)
                elif case == "hardlink":
                    target = self._write(self.receipt, self.proof_parent / "target")
                    path.unlink()
                    os.link(target, path)
                elif case == "mode":
                    path.chmod(0o644)
                elif case in ("in_root", "dotdot_in_root"):
                    parent = self.root / "proof"
                    parent.mkdir(mode=0o700, exist_ok=True)
                    path = self._write(self.receipt, parent / "smtp01.json")
                    if case == "dotdot_in_root":
                        path = Path("/tmp/../tmp") / path.relative_to("/tmp")
                else:
                    self.proof_parent.chmod(0o755)
                self._reject(path)
                self.proof_parent.chmod(0o700)
                for child in self.proof_parent.iterdir():
                    child.unlink()

    def test_wrong_owner_and_oversize_receipts_are_rejected(self):
        real_fstat = module.os.fstat

        def wrong_owner(fd):
            info = real_fstat(fd)
            if stat.S_ISREG(info.st_mode):
                values = list(info)
                values[4] = info.st_uid + 1
                return os.stat_result(values)
            return info

        with patch.object(module.os, "fstat", side_effect=wrong_owner):
            self._reject()
        self.proof.write_text(json.dumps(self.receipt) + " " * 70_000)
        self.proof.chmod(0o600)
        self._reject()

    def test_exact_schema_rejects_missing_extra_duplicate_and_invalid_ids(self):
        missing = dict(self.receipt)
        missing.pop("approval_record")
        extra = dict(self.receipt, unexpected="synthetic")
        for receipt in (missing, extra):
            with self.subTest(receipt=set(receipt)):
                self._write(receipt)
                self._reject()
        duplicate = json.dumps(self.receipt)[:-1] + ',"target":"COMM-003"}'
        self.proof.write_text(duplicate)
        self.proof.chmod(0o600)
        self._reject()
        for field, value in (
            ("operation", "other-operation"),
            ("target", "COMM-002"),
            ("observation_id", "bad value"),
            ("approval_record", "*"),
            ("approval_record", True),
        ):
            with self.subTest(field=field, value=value):
                self._write(dict(self.receipt, **{field: value}))
                self._reject()

    def test_every_authority_field_is_bound(self):
        for field in self.receipt:
            with self.subTest(field=field):
                self._write(dict(self.receipt, **{field: None}))
                self._reject()

    def test_timestamp_freshness_is_bounded_and_unambiguous(self):
        cases = (
            {"observed_at": "2026-10-10T09:54:59Z"},
            {"observed_at": "2026-10-10T10:00:31Z"},
            {"expires_at": "2026-10-10T10:00:00Z"},
            {"expires_at": "2026-10-10T10:04:59Z"},
            {"expires_at": "2026-10-10T10:14:01Z"},
            {"observed_at": "2026-10-10T09:58:00+00:00"},
            {"expires_at": "2026-10-10 10:05:00Z"},
            {"observed_at": True},
        )
        for change in cases:
            with self.subTest(change=change):
                self._write(dict(self.receipt, **change))
                self._reject()

    def test_receipt_identity_change_during_read_is_rejected(self):
        real_read = module.os.read
        changed = False

        def mutate_after_read(fd, size):
            nonlocal changed
            data = real_read(fd, size)
            if data and not changed:
                changed = True
                with self.proof.open("ab") as stream:
                    stream.write(b" ")
            return data

        with patch.object(module.os, "read", side_effect=mutate_after_read):
            self._reject()

    def test_dirty_tracked_worktree_or_index_is_rejected(self):
        for dirty in ("worktree", "index"):
            with self.subTest(dirty=dirty):

                def command(arguments, root=None, dirty=dirty):
                    if arguments[:3] == ["git", "rev-parse", "HEAD"]:
                        return b"synthetic-sha\n"
                    if arguments[:3] == ["git", "diff", "--quiet"]:
                        if dirty == "worktree":
                            raise subprocess.CalledProcessError(1, arguments)
                        return b""
                    if arguments[:3] == ["git", "diff", "--cached"]:
                        if dirty == "index":
                            raise subprocess.CalledProcessError(1, arguments)
                        return b""
                    if arguments[:3] == ["docker", "ps", "-aq"]:
                        return b""
                    raise AssertionError("unexpected synthetic command")

                with patch.object(module, "_run", side_effect=command):
                    self._reject()

    def test_every_old_path_ancestor_bind_blocks_retirement(self):
        for mount, rejected in MOUNT_CASES:
            with self.subTest(mount=mount):
                mounted = dict(mount)
                mounted["Source"] = {
                    "OLD": str(self.root / module.OLD_PATH),
                    "PARENT": str((self.root / module.OLD_PATH).parent),
                    "SECRETS": str(self.root / "secrets"),
                }.get(mount["Source"], mount["Source"])

                def command(arguments, root=None, mounted=mounted):
                    if arguments[:3] == ["git", "rev-parse", "HEAD"]:
                        return b"synthetic-sha\n"
                    if arguments[0] == "git":
                        return b""
                    if arguments[:3] == ["docker", "ps", "-aq"]:
                        return b"synthetic-container"
                    return json.dumps([mounted]).encode()

                with patch.object(module, "_run", side_effect=command):
                    if rejected:
                        self._reject()
                    else:
                        verify_proof(self.root, self.proof)

    def test_malformed_duplicate_canonical_metadata_row_is_rejected(self):
        valid = (
            b"| COMM-002 | X | PW | synthetic | - | "
            + CANONICAL_PATH.encode()
            + b" | date | canonical |\n"
        )
        malformed = b"| COMM-002 | COMM-999 |\n"
        with self.assertRaises(ContractError):
            metadata_retired(valid + malformed)

    def test_runbook_uses_fresh_unpredictable_proof_directory(self):
        runbook = (ROOT / "docs/05.operations/runbooks/0029-supabase.md").read_text()
        self.assertIn("mktemp -d /tmp/smtp01.XXXXXXXX", runbook)
        self.assertNotIn("/tmp/smtp01-${task_run_id", runbook)


if __name__ == "__main__":
    unittest.main()
