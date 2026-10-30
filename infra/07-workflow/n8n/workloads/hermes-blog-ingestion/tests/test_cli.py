"""In-process CLI boundary checks using synthetic files only."""

import contextlib
import io
import json
import sys
import tempfile
import unittest
from importlib import import_module
from pathlib import Path
from unittest.mock import patch

WORKLOAD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKLOAD))
sys.path.insert(0, str(Path(__file__).resolve().parent))

cli = import_module("publisher.cli")
staging = import_module("test_staging")
JOB = staging.JOB
fixture = staging.fixture


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="hermes-cli-", dir="/tmp")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.validator, self.validator_sha = staging.synthetic_validator(self.root)
        patcher = patch("publisher.candidates.REVIEWED_SHA256", self.validator_sha)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.outbox = self.root / "private" / "outbox.sqlite"
        self.data, self.report, self.export = fixture(self.root)

    def stage_args(self, *, exports=None, validator=None, sha=None):
        validator = validator or self.validator
        sha = sha or self.validator_sha
        return [
            "stage",
            "--exports",
            str(exports or self.root / "exports"),
            "--source-root",
            str(self.root / "source"),
            "--item-root",
            str(self.root / "items"),
            "--validator",
            str(validator),
            "--validator-sha256",
            sha,
            "--outbox",
            str(self.outbox),
        ]

    def invoke(self, args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = cli.main(args)
        output = stdout.getvalue() + stderr.getvalue()
        for private in ("private-synthetic-marker", str(self.root), "invalid_json"):
            self.assertNotIn(private, output)
        self.assertEqual(stderr.getvalue(), "")
        return code, json.loads(stdout.getvalue())

    def test_fresh_status_and_successful_replay(self):
        self.assertEqual(self.invoke(["status", "--outbox", str(self.outbox)]), (0, {}))
        self.assertEqual(
            self.invoke(self.stage_args()),
            (0, dict(staged=1, duplicate=0, conflict=0, rejected=0)),
        )
        self.assertEqual(
            self.invoke(self.stage_args()),
            (0, dict(staged=0, duplicate=1, conflict=0, rejected=0)),
        )
        self.assertEqual(
            self.invoke(["status", "--outbox", str(self.outbox)]),
            (0, {"awaiting_contract": 1}),
        )
        self.assertTrue(self.report.exists())

    def test_missing_or_changed_validator_fails_closed(self):
        for validator, sha in (
            (self.root / "missing.py", self.validator_sha),
            (self.validator, "0" * 64),
        ):
            with self.subTest(validator=validator, sha=sha):
                self.assertEqual(
                    self.invoke(self.stage_args(validator=validator, sha=sha)),
                    (1, {"error": "operation_rejected"}),
                )
        self.assertEqual(self.invoke(["status", "--outbox", str(self.outbox)]), (0, {}))

    def test_missing_export_root_and_symlink_job_fail_closed(self):
        with patch.object(cli, "load_validator", return_value=lambda data: []):
            self.assertEqual(
                self.invoke(self.stage_args(exports=self.root / "missing")),
                (1, {"error": "operation_rejected"}),
            )
            linked = self.root / "exports" / "25674fbc0bf3"
            linked.symlink_to(self.root / "exports" / JOB)
            self.assertEqual(
                self.invoke(self.stage_args()), (1, {"error": "operation_rejected"})
            )

    def test_invalid_candidate_is_counted_without_content(self):
        self.export.write_text('{"private-synthetic-marker":')
        with patch.object(cli, "load_validator", return_value=lambda data: []):
            self.assertEqual(
                self.invoke(self.stage_args()),
                (1, dict(staged=0, duplicate=0, conflict=0, rejected=1)),
            )
        self.assertEqual(self.invoke(["status", "--outbox", str(self.outbox)]), (0, {}))

    def test_empty_export_root_is_valid(self):
        empty = self.root / "empty"
        empty.mkdir()
        with patch.object(cli, "load_validator", return_value=lambda data: []):
            self.assertEqual(
                self.invoke(self.stage_args(exports=empty)),
                (0, dict(staged=0, duplicate=0, conflict=0, rejected=0)),
            )

    def test_cli_exposes_no_send_or_credential_arguments(self):
        for args in (
            ["send"],
            [
                "status",
                "--outbox",
                str(self.outbox),
                "--credential",
                "private-synthetic-marker",
            ],
        ):
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as exit_code:
                    cli.main(args)
                self.assertEqual(exit_code.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
