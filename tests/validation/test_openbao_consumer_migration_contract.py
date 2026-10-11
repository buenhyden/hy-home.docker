"""Public schema and offline CLI contracts, with synthetic stdin only."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tests.lib.ops.test_openbao_consumer_migration import receipt, wave

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "scripts/operations/openbao-consumer-migration.py"
PACKAGE = ROOT / "infra/03-security/openbao/consumer-migration"


def run_cli(arguments, raw=b""):
    return subprocess.run(
        [sys.executable, str(CLI), *arguments],
        input=raw,
        capture_output=True,
        cwd=ROOT,
        timeout=8,
        check=False,
    )


class PublicMigrationContractTests(unittest.TestCase):
    def test_closed_schemas_accept_only_pre_copy_synthetic_receipts(self):
        schemas = {}
        for kind, candidate in (("wave", wave()), ("receipt", receipt())):
            schema = json.loads((PACKAGE / f"{kind}.schema.json").read_bytes())
            Draft202012Validator.check_schema(schema)
            validator = Draft202012Validator(schema)
            self.assertTrue(validator.is_valid(candidate))
            self.assertFalse(
                validator.is_valid({**candidate, "token": "private-marker"})
            )
            self.assertFalse(
                validator.is_valid({**candidate, "evidence_kind": "native"})
            )
            schemas[kind] = schema
        self.assertEqual(
            schemas["wave"]["$defs"]["catalog"], schemas["receipt"]["$defs"]["catalog"]
        )
        candidate = receipt()
        candidate["items"][0].update(state="recoverable", kv_version=1)
        self.assertFalse(Draft202012Validator(schemas["receipt"]).is_valid(candidate))

    def test_cli_validates_synthetic_documents_without_echoing_them(self):
        for kind, candidate in (("wave", wave()), ("receipt", receipt())):
            result = run_cli(["validate-" + kind], json.dumps(candidate).encode())
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(b"PASS: public contract shape only\n", result.stdout)
            self.assertEqual(b"", result.stderr)
            self.assertNotIn(candidate["consumer"].encode(), result.stdout)

    def test_cli_errors_do_not_echo_argv_json_or_tracebacks(self):
        for arguments, raw in (
            (["--private-marker"], b""),
            (["apply", "private-marker"], b""),
            (["validate-wave", "private-marker"], b""),
            (["validate-wave"], b"private-marker"),
            (["validate-wave"], b'{"token":"private-marker"}'),
            (["validate-receipt"], b'{"a":1,"a":2}'),
            (["validate-wave"], b" " * 131073),
        ):
            result = run_cli(arguments, raw)
            self.assertEqual(2, result.returncode)
            self.assertEqual(b"", result.stdout)
            self.assertNotIn(b"private-marker", result.stderr)
            self.assertNotIn(b"Traceback", result.stderr)
            self.assertTrue(result.stderr.startswith(b"FAIL: "))

    def test_cli_help_has_no_copy_delete_rotation_or_private_inputs(self):
        result = run_cli(["--help"])
        self.assertEqual(0, result.returncode)
        self.assertIn(b"validate-wave", result.stdout)
        self.assertNotIn(b"--token", result.stdout)
        self.assertNotIn(b"--apply", result.stdout)
        self.assertIn(b"stdin", result.stdout)

    def test_cli_stdin_wait_has_a_whole_operation_deadline(self):
        process = subprocess.Popen(
            [sys.executable, str(CLI), "validate-wave"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=ROOT,
        )
        try:
            process.wait(timeout=8)
            self.assertEqual(2, process.returncode)
            self.assertEqual(b"FAIL: public_input_timeout\n", process.stderr.read())
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
            for stream in (process.stdin, process.stdout, process.stderr):
                stream.close()

    def test_new_folder_has_korean_navigation(self):
        text = (PACKAGE / "README.md").read_text()
        self.assertIn("wave.schema.json", text)
        self.assertIn("receipt.schema.json", text)
        self.assertTrue(any("\uac00" <= character <= "\ud7a3" for character in text))
