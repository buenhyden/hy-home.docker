"""Synthetic executable CLI acceptance; never contacts an object store."""

import hashlib
import json
import os
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "infra/11-quality/k6"))


class QualityObjectStoreTests(unittest.TestCase):
    def setUp(self):
        import object_store

        self.api = object_store
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.attempt = self.root / "attempt"
        self.attempt.mkdir()
        self.data = b"synthetic quality raw sample\n"
        self.raw = self.attempt / "raw.json"
        self.raw.write_bytes(self.data)
        self.raw.chmod(0o440)
        self.identity = {
            "project_id": "sample-a",
            "run_id": "12345678-1234-4abc-8def-1234567890ab",
            "attempt": 1,
        }
        self.entry = {
            "name": "raw.json",
            "sha256": hashlib.sha256(self.data).hexdigest(),
            "bytes": len(self.data),
        }
        self.checksums = self.attempt / "checksums.json"
        self.checksums.write_text(json.dumps({"artifacts": [self.entry]}))
        self.checksums.chmod(0o440)
        self.final = self.attempt / "final.json"
        self.final.write_text(
            json.dumps(
                dict(
                    self.identity,
                    checksums_sha256=hashlib.sha256(
                        self.checksums.read_bytes()
                    ).hexdigest(),
                    import_allowed=True,
                )
            )
        )
        self.final.chmod(0o440)
        self.contract = {
            "schema_version": "hyhome.quality-object-contract/v1",
            "project_id": "sample-a",
            "endpoint": "http://seaweedfs-s3:8333",
            "region": "us-east-1",
            "bucket": "approved-fixture",
            "prefix": "quality",
            "max_file_bytes": 1024,
            "max_total_bytes": 4096,
        }
        self.access = self.root / "access"
        self.access.write_text("synthetic-access")
        self.secret = self.root / "secret"
        self.secret.write_text("synthetic-secret")
        self.access.chmod(0o600)
        self.secret.chmod(0o600)
        self.cli = self.root / "aws"
        self.cli.write_text("""#!/usr/bin/python3
import base64, hashlib, json, os, pathlib, sys
root = pathlib.Path(__file__).parent
args = sys.argv[1:]
op = args[args.index('s3api')+1]
with (root/'calls').open('a') if op != 'get-object' else open(os.devnull,'w') as log:
 log.write(json.dumps({'args': args, 'ambient': [k for k in ('AWS_PROFILE','AWS_SESSION_TOKEN','AWS_ENDPOINT_URL') if k in os.environ]})+'\\n')
mode = (root/'mode').read_text() if (root/'mode').exists() else ''
op = args[args.index('s3api')+1]
if mode == 'denied':
 sys.stderr.write('An error occurred (AccessDenied)'); sys.exit(1)
key = args[args.index('--key')+1]
path = root / ('object-'+hashlib.sha256(key.encode()).hexdigest())
if op == 'put-object':
 if path.exists():
  sys.stderr.write('An error occurred (PreconditionFailed)'); sys.exit(1)
 path.write_bytes(pathlib.Path(args[args.index('--body')+1]).read_bytes())
if not path.exists(): sys.exit(1)
data = path.read_bytes()
if op == 'get-object': pathlib.Path(args[-1]).write_bytes(data if mode != 'corrupt' else b'bad')
checksum = base64.b64encode(hashlib.sha256(data).digest()).decode()
response = {'ContentLength': len(data), 'ChecksumSHA256': 'wrong' if mode == 'mismatch' else checksum, 'ETag': 'synthetic'}
if mode == 'missing': response.pop('ChecksumSHA256')
print(json.dumps(response))
""")
        self.cli.chmod(0o750)
        self.receipt = self.root / "upload.json"
        self.kwargs = {
            "approved_endpoints": ("http://seaweedfs-s3:8333",),
            "access_key_file": self.access,
            "secret_key_file": self.secret,
            "aws_binary": str(self.cli),
        }

    def upload(self):
        return self.api.upload(self.attempt, self.contract, self.receipt, **self.kwargs)

    def test_verified_upload_replay_and_restore(self):
        receipt = self.upload()
        self.assertEqual(receipt, self.upload())
        self.assertTrue(
            receipt["artifacts"][0]["object_ref"].startswith(
                "s3://approved-fixture/quality/sample-a/"
            )
        )
        scratch = self.root / "restore"
        scratch.mkdir()
        self.api.restore(receipt, self.contract, scratch, **self.kwargs)
        self.assertEqual(self.data, (scratch / "raw.json").read_bytes())
        with self.assertRaises(self.api.ObjectStoreError):
            self.api.restore(receipt, self.contract, scratch, **self.kwargs)

    def test_missing_or_mismatched_remote_checksum_leaves_no_receipt(self):
        for mode in ("mismatch", "missing"):
            with self.subTest(mode=mode):
                (self.root / "mode").write_text(mode)
                with self.assertRaises(self.api.ObjectStoreError):
                    self.upload()
                self.assertFalse(self.receipt.exists())

    def test_allowlist_quota_and_symlinks_fail_before_client(self):
        for change in (
            {"endpoint": "https://unapproved.invalid"},
            {"max_file_bytes": 1},
        ):
            with (
                self.subTest(change=change),
                self.assertRaises(self.api.ObjectStoreError),
            ):
                self.api.upload(
                    self.attempt,
                    dict(self.contract, **change),
                    self.receipt,
                    **self.kwargs,
                )
        self.raw.unlink()
        self.raw.symlink_to(self.access)
        with self.assertRaises(self.api.ObjectStoreError):
            self.upload()
        self.assertFalse((self.root / "calls").exists())

    def test_ambient_credentials_cannot_override_file_credentials(self):
        with mock.patch.dict(
            os.environ,
            {
                "AWS_PROFILE": "forbidden",
                "AWS_SESSION_TOKEN": "forbidden",
                "AWS_ENDPOINT_URL": "https://forbidden.invalid",
            },
        ):
            self.upload()
        calls = [
            json.loads(line) for line in (self.root / "calls").read_text().splitlines()
        ]
        self.assertTrue(all(not call["ambient"] for call in calls))
        self.assertNotIn("synthetic-secret", (self.root / "calls").read_text())

    def test_restore_corruption_is_not_committed(self):
        receipt = self.upload()
        (self.root / "mode").write_text("corrupt")
        scratch = self.root / "restore"
        scratch.mkdir()
        with self.assertRaises(self.api.ObjectStoreError):
            self.api.restore(receipt, self.contract, scratch, **self.kwargs)
        self.assertFalse((scratch / "raw.json").exists())
        self.assertFalse((scratch / "restore-receipt.json").exists())

    def test_remote_denial_and_receipt_conflict_fail_closed(self):
        (self.root / "mode").write_text("denied")
        with self.assertRaises(self.api.ObjectStoreError):
            self.upload()
        self.assertFalse(self.receipt.exists())
        (self.root / "mode").unlink()
        self.upload()
        before = (self.root / "calls").read_bytes()
        self.receipt.write_text("{}")
        with self.assertRaises(self.api.ObjectStoreError):
            self.upload()
        self.assertEqual(before, (self.root / "calls").read_bytes())

    def test_credential_symlink_and_total_quota_fail_before_client(self):
        link = self.root / "credential-link"
        link.symlink_to(self.secret)
        with self.assertRaises(self.api.ObjectStoreError):
            self.api.upload(
                self.attempt,
                self.contract,
                self.receipt,
                **dict(self.kwargs, secret_key_file=link),
            )
        with self.assertRaises(self.api.ObjectStoreError):
            self.api.upload(
                self.attempt,
                dict(self.contract, max_total_bytes=1),
                self.receipt,
                **self.kwargs,
            )
        self.assertFalse((self.root / "calls").exists())

    def test_relative_binary_or_weak_file_modes_are_denied_before_secret_read(self):
        with mock.patch.dict(os.environ, {"PATH": str(self.root)}):
            with mock.patch("object_store._environment") as credentials:
                with self.assertRaises(self.api.ObjectStoreError):
                    self.api.upload(
                        self.attempt,
                        self.contract,
                        self.receipt,
                        **dict(self.kwargs, aws_binary="aws"),
                    )
                credentials.assert_not_called()
        for mode in (0o644, 0o660):
            self.secret.chmod(mode)
            with self.assertRaises(self.api.ObjectStoreError):
                self.upload()
        self.secret.chmod(0o600)
        self.cli.chmod(0o770)
        with mock.patch("object_store._environment") as credentials:
            with self.assertRaises(self.api.ObjectStoreError):
                self.upload()
            credentials.assert_not_called()
        self.assertFalse((self.root / "calls").exists())

    def two_artifacts(self):
        second = self.attempt / "second.json"
        second.write_bytes(self.data)
        second.chmod(0o440)
        entries = [self.entry, dict(self.entry, name="second.json")]
        self.checksums.chmod(0o600)
        self.checksums.write_text(json.dumps({"artifacts": entries}))
        self.checksums.chmod(0o440)
        self.final.chmod(0o600)
        self.final.write_text(
            json.dumps(
                dict(
                    self.identity,
                    checksums_sha256=hashlib.sha256(
                        self.checksums.read_bytes()
                    ).hexdigest(),
                    import_allowed=True,
                )
            )
        )
        self.final.chmod(0o440)
        return self.upload()

    def test_restore_publication_failure_rolls_back_owned_links_only(self):
        receipt = self.two_artifacts()
        original = os.link
        for foreign in (False, True):
            scratch = self.root / ("restore-" + str(foreign))
            scratch.mkdir()
            calls = []

            def failing_link(source, target, *, calls=calls, foreign=foreign, **kwargs):
                calls.append(target)
                if len(calls) == 2:
                    if foreign:
                        pathlib.Path(target).write_bytes(b"foreign")
                    raise OSError("synthetic link failure")
                return original(source, target, **kwargs)

            with mock.patch("object_store.os.link", side_effect=failing_link):
                with self.assertRaises(self.api.ObjectStoreError):
                    self.api.restore(receipt, self.contract, scratch, **self.kwargs)
            self.assertFalse((scratch / "raw.json").exists())
            self.assertEqual(
                ["second.json"] if foreign else [],
                sorted(p.name for p in scratch.iterdir()),
            )
            if foreign:
                self.assertEqual(b"foreign", (scratch / "second.json").read_bytes())
        scratch = self.root / "restore-receipt-failure"
        scratch.mkdir()
        with mock.patch(
            "object_store._write_once", side_effect=OSError("synthetic receipt failure")
        ):
            with self.assertRaises(self.api.ObjectStoreError):
                self.api.restore(receipt, self.contract, scratch, **self.kwargs)
        self.assertEqual([], list(scratch.iterdir()))

    def test_upload_receipt_binds_before_import_and_rejects_mismatches(self):
        from tests.validation import test_k6_results as fixtures

        fixture = fixtures.K6ResultContractTests()
        fixture.setUp()
        self.addCleanup(fixture.tearDown)
        attempt = fixture.prepare()
        fixture.write_execution(attempt)
        fixtures.quality_run.finalize(attempt)
        contract = dict(self.contract, max_file_bytes=65536, max_total_bytes=262144)
        receipt = self.api.upload(attempt, contract, self.receipt, **self.kwargs)
        contract_path = self.root / "independently-approved.json"
        contract_path.write_text(json.dumps(contract))
        endpoints = ("http://seaweedfs-s3:8333",)
        with self.assertRaises(fixtures.quality_run.ContractError):
            fixtures.quality_run.prepare_import(
                attempt, self.root / "no-contract.json", self.receipt
            )
        envelope = fixtures.quality_run.prepare_import(
            attempt, self.root / "import.json", self.receipt, contract_path, endpoints
        )
        fixtures.result_import._validate(
            envelope, contract, ("http://seaweedfs-s3:8333",)
        )
        scratch = self.root / "restore-full"
        scratch.mkdir()
        self.api.restore(receipt, contract, scratch, **self.kwargs)
        fixtures.quality_run.finalize(scratch)
        self.assertEqual(
            receipt["final_sha256"],
            hashlib.sha256((scratch / "final.json").read_bytes()).hexdigest(),
        )
        self.assertEqual(
            envelope,
            fixtures.quality_run.prepare_import(
                scratch,
                self.root / "recovered-import.json",
                self.receipt,
                contract_path,
                endpoints,
            ),
        )
        self.assertTrue(all(a["object_ref"] is not None for a in envelope["artifacts"]))
        for change in ("identity", "final_sha256", "artifacts"):
            bad = json.loads(json.dumps(receipt))
            if change == "identity":
                bad["identity"]["attempt"] = 2
                for item in bad["artifacts"]:
                    item["object_ref"] = item["object_ref"].replace("/1/", "/2/")
            elif change == "final_sha256":
                bad["final_sha256"] = "0" * 64
            else:
                bad["artifacts"].pop()
            path = self.root / ("bad-" + change + ".json")
            path.write_text(json.dumps(bad))
            with (
                self.subTest(change=change),
                self.assertRaises(fixtures.quality_run.ContractError),
            ):
                fixtures.quality_run.prepare_import(
                    attempt,
                    self.root / ("import-" + change + ".json"),
                    path,
                    contract_path,
                    endpoints,
                )
        with self.assertRaises(fixtures.result_import.ImportContractError):
            fixtures.result_import._validate(envelope)
        for change, value in (
            ("bucket", "unapproved-bucket"),
            ("prefix", "evil-prefix"),
        ):
            bad = json.loads(json.dumps(envelope))
            for item in bad["artifacts"]:
                item["object_ref"] = item["object_ref"].replace(contract[change], value)
            unsigned = dict(bad)
            unsigned.pop("payload_sha256")
            bad["payload_sha256"] = hashlib.sha256(
                fixtures.canonical(unsigned)
            ).hexdigest()
            with (
                self.subTest(change=change),
                self.assertRaises(fixtures.result_import.ImportContractError),
            ):
                fixtures.result_import._validate(bad, contract, endpoints)
        for replacement in ("sample-b", "0" * 64):
            bad = json.loads(json.dumps(envelope))
            item = bad["artifacts"][0]
            original = "sample-a" if replacement == "sample-b" else item["sha256"]
            item["object_ref"] = item["object_ref"].replace(original, replacement)
            unsigned = dict(bad)
            unsigned.pop("payload_sha256")
            bad["payload_sha256"] = hashlib.sha256(
                fixtures.canonical(unsigned)
            ).hexdigest()
            with self.assertRaises(fixtures.result_import.ImportContractError):
                fixtures.result_import._validate(
                    bad, contract, ("http://seaweedfs-s3:8333",)
                )

    def test_client_missing_and_timeout_have_redacted_exit_classes(self):
        with self.assertRaises(self.api.ObjectStoreError) as missing:
            self.api.upload(
                self.attempt,
                self.contract,
                self.receipt,
                **dict(self.kwargs, aws_binary=str(self.root / "missing")),
            )
        self.assertEqual(127, missing.exception.exit_code)
        import subprocess

        with mock.patch(
            "object_store.subprocess.run",
            side_effect=subprocess.TimeoutExpired(["aws"], 30),
        ):
            with self.assertRaises(self.api.ObjectStoreError) as timeout:
                self.upload()
        self.assertEqual(124, timeout.exception.exit_code)


if __name__ == "__main__":
    unittest.main()
