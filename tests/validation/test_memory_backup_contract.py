"""Registered mutation entrypoints use host memory-capacity admission."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESTIC = ROOT / "infra/09-platform-ops/restic"


class BackupContractTests(unittest.TestCase):
    def test_generic_local_cmd_refuses_backup_before_restic(self):
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "restic"
            executable.write_text("#!/bin/sh\necho unexpected-restic\n")
            executable.chmod(0o700)
            result = subprocess.run(
                ["sh", str(RESTIC / "backup.sh"), "cmd", "state", "backup", "/fixture"],
                capture_output=True,
                text=True,
                env={**os.environ, "PATH": directory + ":" + os.environ["PATH"]},
                check=False,
            )
            self.assertEqual(result.returncode, 64)
            self.assertNotIn("unexpected-restic", result.stdout)

    def test_daily_backup_entrypoint_is_not_admission_gated(self):
        # The 1 GiB memory cap charges 64 MiB per existing snapshot, so the
        # gate refused every daily backup (2026-11-11); the daily path stays
        # direct until SPEC-0270 redesigns snapshot accounting.
        script = (RESTIC / "backup.sh").read_text()
        body = script.split("\n    backup)\n", 1)[1].split("\n        ;;\n", 1)[0]
        self.assertNotIn("require_memory_admission", body)
        self.assertNotIn("backup-run", body)
        self.assertIn("--tag hyhome-state", body)
        offsite = (RESTIC / "offsite.sh").read_text()
        copy = offsite.split("\n    copy)\n", 1)[1].split("\n        ;;\n", 1)[0]
        self.assertNotIn("require_memory_admission", copy)
        self.assertIn("R2 repository size:", copy)

    def test_internal_backup_refuses_forged_digest(self):
        result = subprocess.run(
            ["sh", str(RESTIC / "backup.sh"), "budget-backup"],
            input="forged\n",
            capture_output=True,
            text=True,
            env={**os.environ, "HYHOME_MEMORY_ADMISSION_SHA256": "0" * 64},
            check=False,
        )
        self.assertEqual(result.returncode, 64)

    def test_daily_wrapper_runs_restic_directly(self):
        script = (RESTIC / "bin/hyhome-backup.sh").read_text()
        self.assertIn('"${compose[@]}" run --rm --no-deps restic backup', script)
        self.assertIn('"${compose[@]}" run --rm --no-deps restic-offsite copy', script)
        self.assertNotIn("backup-run --target", script)
        self.assertIn("R2 repository size:", script)


if __name__ == "__main__":
    unittest.main()
