"""Synthetic CLI evidence, deliberately separate from operator-host retirement."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from scripts.lib.ops import retire_materials as retirement

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "scripts/operations/retire-materials.py"


class RetirementCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "synthetic-host"
        self.target = self.root / "secrets/db/legacy-app/unused.txt"
        self.target.parent.mkdir(parents=True)
        self.target.write_text("synthetic-secret-value-do-not-print")
        relative = self.target.relative_to(self.root)
        self.row = {
            "id": "TEST-001",
            "path": relative.as_posix(),
            "scope": "root",
            "kind": "legacy-secret",
            "identity": retirement.identity(self.target),
            "parents": retirement.parent_identities(self.root, relative),
            "decision": "delete",
            "reviewed_at": datetime.now(UTC).isoformat(),
            "owner": "synthetic-operator",
            "evidence_ref": "task/cleanup",
            "checked": dict.fromkeys(retirement.CHECKS, True),
            "evidence": dict.fromkeys(retirement.CHECKS, "task/cleanup"),
            "consumers": [],
            "recovery_required": False,
        }
        private = self.base / "operator"
        private.mkdir(mode=0o700)
        self.manifest = private / "receipt.json"
        self.document = {
            "entries": [self.row],
            "maintenance": {
                "writers_stopped": True,
                "owner": "synthetic-operator",
                "reviewed_at": datetime.now(UTC).isoformat(),
                "evidence_ref": "task/cleanup",
            },
        }
        self.write_manifest()

    def write_manifest(self):
        self.manifest.write_text(json.dumps(self.document))
        self.manifest.chmod(0o600)

    def run_cli(self, *flags):
        result = subprocess.run(
            [
                sys.executable,
                str(CLI),
                "--root",
                str(self.root),
                "--manifest",
                str(self.manifest),
                *flags,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotIn(
            "synthetic-secret-value-do-not-print", result.stdout + result.stderr
        )
        for sensitive in ["ctime_ns", "mtime_ns", "synthetic-operator"]:
            self.assertNotIn(sensitive, result.stdout + result.stderr)
        return result

    def test_unicode_receipt_names_are_json_escaped(self):
        renamed = self.target.with_name("자료.txt")
        self.target.rename(renamed)
        self.target = renamed
        relative = renamed.relative_to(self.root)
        self.row["path"] = relative.as_posix()
        self.row["identity"] = retirement.identity(renamed)
        self.row["parents"] = retirement.parent_identities(self.root, relative)
        self.write_manifest()
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("자료", result.stdout)
        self.assertEqual(
            json.loads(result.stdout)["entries"][0]["path"], relative.as_posix()
        )

    def test_default_inspection_does_not_unlink(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["applied"])
        self.assertTrue(self.target.exists())

    def test_apply_and_idempotent_apply(self):
        result = self.run_cli("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["entries"][0]["result"], "deleted")
        self.assertFalse(self.target.exists())
        again = self.run_cli("--apply")
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(
            json.loads(again.stdout)["entries"][0]["result"], "already-absent"
        )

    def test_unknown_consumer_blocks_with_nonzero_exit(self):
        self.document["entries"][0]["checked"]["runtime"] = False
        self.write_manifest()
        result = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads(result.stdout)["entries"][0]["eligible"])
        result = self.run_cli("--apply")
        self.assertEqual(result.returncode, 2)
        self.assertTrue(self.target.exists())
        self.assertNotIn("Traceback", result.stderr)

    def test_manifest_permissions_and_parse_failures_are_sanitized(self):
        self.manifest.chmod(0o644)
        self.assertEqual(self.run_cli().returncode, 2)
        self.manifest.chmod(0o600)
        self.manifest.write_text("synthetic-secret-value-do-not-print")
        self.assertEqual(self.run_cli().returncode, 2)
        self.manifest.unlink()
        self.assertEqual(self.run_cli().returncode, 2)
        os.mkfifo(self.manifest, 0o600)
        self.assertEqual(self.run_cli().returncode, 2)

    def test_main_partial_receipt_is_structured_and_nonzero(self):
        rows = [
            {"path": self.row["path"], "result": "deleted-durability-unknown"},
            {"path": "secrets/db/legacy-app/second.txt", "result": "not-attempted"},
        ]
        stdout, stderr = StringIO(), StringIO()
        with patch.object(
            retirement, "apply_plan", side_effect=retirement.PartialFailure(rows)
        ):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = retirement.main(
                    [
                        "--root",
                        str(self.root),
                        "--manifest",
                        str(self.manifest),
                        "--apply",
                    ]
                )
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(stdout.getvalue())["entries"], rows)
        self.assertEqual(stderr.getvalue(), "")

    def test_review_malformed_entry_paths_exit_two_without_traceback(self):
        for row in [{}, {"path": None}, {"path": 123}, {"path": []}]:
            self.document["entries"] = [row]
            self.write_manifest()
            with self.subTest(row=row):
                result = self.run_cli()
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("Traceback", result.stderr)

    def test_main_generic_errors_do_not_expose_exception_payload(self):
        stdout, stderr = StringIO(), StringIO()
        with patch.object(
            retirement,
            "load_manifest",
            side_effect=OSError("synthetic-secret-value-do-not-print"),
        ):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = retirement.main(
                    ["--root", str(self.root), "--manifest", str(self.manifest)]
                )
        self.assertEqual(code, 2)
        self.assertNotIn("synthetic-secret-value-do-not-print", stderr.getvalue())
        self.assertEqual(stdout.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
