"""Synthetic filesystem evidence; no host reports or credentials are read."""

import contextlib
import copy
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

WORKLOAD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKLOAD))
# Test double exercises loader wiring; it is not a schema compatibility fixture.
VALIDATOR = Path("/nonexistent/spec0247-validator.py")
VALIDATOR_SHA = "8c988c715286edd53d2f7e5931cb349e6a5bed49be8ec2f8e7be98f2810c7297"
SYNTHETIC_VALIDATOR = b"""def validate(data):
    if any('secret-private-marker' in item for item in data.get('items', [])):
        raise ValueError('synthetic malformed candidate')
    return None
"""


def synthetic_validator(root):
    path = root / "synthetic-validator.py"
    path.write_bytes(SYNTHETIC_VALIDATOR)
    return path, hashlib.sha256(SYNTHETIC_VALIDATOR).hexdigest()


JOB = "6eabd835f969"
RUN = "a" * 32


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def fixture(root, ideas=False):
    job = "8d0925bc571d" if ideas else JOB
    source = b"# synthetic report\r\nprivate-synthetic-marker\n"
    ref = f"cron/output/{job}/2026-10-30_09-00-00.md"
    item = dict(
        title="title",
        summary="summary",
        region_or_scope="global",
        category="test",
        source_url=None,
        collection_evidence=None,
        verification_status="unverified",
    )
    items = [item]
    if ideas:
        items = []
        for index in range(2):
            idea_ref = f"storage/research/solo-dev-ideas/2026-10-30/kr/idea-{index}.md"
            raw = f"# idea {index}\n".encode()
            path = root / "items" / idea_ref
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
            items.append(
                dict(
                    item,
                    customer_segment="solo",
                    problem="problem",
                    differentiation="different",
                    pricing=None,
                    revenue_model=None,
                    mvp_duration=None,
                    competitors=None,
                    alternatives=None,
                    uncertainty=["unknown"],
                    market_size_claim=None,
                    source_ref=idea_ref,
                    source_sha256=digest(raw),
                )
            )
    data = dict(
        schema_version="1.0.0",
        producer="hermes",
        job_id=job,
        run_id=RUN,
        report_kind="solo-dev-ideas" if ideas else "strategy-news",
        generated_at="2026-10-30T09:00:00+09:00",
        source_ref=ref,
        source_sha256=digest(source),
        items=items,
        state=dict(
            run_completed=True,
            source_file_ready=True,
            email_delivery="reported_sent",
            blog_data_ingested="unknown",
        ),
        export_status="ready_for_review",
        privacy_classification="unreviewed",
        warnings=[],
    )
    report = root / "source" / ref
    report.parent.mkdir(parents=True)
    report.write_bytes(source)
    export = root / "exports" / job / f"{RUN}.json"
    export.parent.mkdir(parents=True)
    export.write_bytes(json.dumps(data, ensure_ascii=False).encode())
    (root / "items").mkdir(exist_ok=True)
    return data, report, export


class StagingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="hermes-staging-", dir="/tmp")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.validator, self.validator_sha = synthetic_validator(self.root)
        self.validator_patcher = patch(
            "publisher.candidates.REVIEWED_SHA256", self.validator_sha
        )
        self.validator_patcher.start()
        self.addCleanup(self.validator_patcher.stop)
        self.data, self.report, self.export = fixture(self.root)

    def load(self, **kwargs):
        from publisher.candidates import load_candidate, load_validator

        validator = load_validator(self.validator, self.validator_sha)
        return load_candidate(
            self.root / "exports",
            JOB,
            f"{RUN}.json",
            self.root / "source",
            self.root / "items",
            validator,
            **kwargs,
        )

    def test_staging_runs_when_external_validator_is_missing(self):
        script = (
            "import sys, unittest; from pathlib import Path; "
            "sys.path.insert(0, 'tests'); import test_staging; "
            "test_staging.VALIDATOR = Path('/tmp/missing-hermes-validator.py'); "
            "suite = unittest.defaultTestLoader.loadTestsFromName("
            "'test_staging.StagingTests.test_lossless_source_candidate_and_identity'); "
            "sys.exit(not unittest.TextTestRunner().run(suite).wasSuccessful())"
        )
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=WORKLOAD,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_pinned_validator_optional_compatibility(self):
        path = os.environ.get("HERMES_SPEC0247_VALIDATOR")
        if not path:
            self.skipTest("set HERMES_SPEC0247_VALIDATOR to the exact pinned validator")
        from publisher import candidates

        self.validator_patcher.stop()
        self.assertEqual(candidates.REVIEWED_SHA256, VALIDATOR_SHA)
        validator = candidates.load_validator(Path(path), VALIDATOR_SHA)
        snapshot = candidates.load_candidate(
            self.root / "exports",
            JOB,
            f"{RUN}.json",
            self.root / "source",
            self.root / "items",
            validator,
        )
        self.assertEqual(snapshot.source, self.report.read_bytes())

    def test_lossless_source_candidate_and_identity(self):
        snapshot = self.load()
        self.assertEqual((snapshot.job_id, snapshot.run_id), (JOB, RUN))
        self.assertEqual(snapshot.source, self.report.read_bytes())
        self.assertEqual(snapshot.candidate, self.export.read_bytes())
        self.assertEqual(snapshot.ideas, ())
        self.assertTrue(self.report.exists())

    def test_multiple_ideas_preserved(self):
        from publisher.candidates import load_candidate, load_validator

        root = self.root / "ideas-fixture"
        data, report, export = fixture(root, ideas=True)
        snapshot = load_candidate(
            root / "exports",
            data["job_id"],
            export.name,
            root / "source",
            root / "items",
            load_validator(self.validator, self.validator_sha),
        )
        self.assertEqual(len(snapshot.ideas), 2)
        self.assertEqual(snapshot.ideas[1][1], b"# idea 1\n")
        self.assertEqual(snapshot.source, report.read_bytes())
        self.assertEqual(json.loads(snapshot.candidate)["items"], data["items"])

    def test_forged_source_hash_rejected_without_content_in_error(self):
        from publisher.files import InputError

        self.report.write_bytes(b"changed-private-source")
        with self.assertRaisesRegex(InputError, "^source_digest$"):
            self.load()

    def test_symlink_source_and_ancestor_rejected(self):
        from publisher.files import InputError

        original = self.report.read_bytes()
        target = self.root / "target.md"
        target.write_bytes(original)
        self.report.unlink()
        self.report.symlink_to(target)
        with self.assertRaises(InputError):
            self.load()
        self.report.unlink()
        self.report.parent.rmdir()
        self.report.parent.symlink_to(self.root)
        with self.assertRaises(InputError):
            self.load()

    def test_malformed_json_duplicate_keys_and_nonfinite_rejected(self):
        from publisher.files import InputError

        for raw in (b"{", b'{"job_id":"x","job_id":"y"}', b'{"number":NaN}'):
            with self.subTest(raw=raw):
                self.export.write_bytes(raw)
                with self.assertRaises(InputError):
                    self.load()

    def test_filename_run_and_job_must_match(self):
        from publisher.files import InputError

        for key, value in [("run_id", "b" * 32), ("job_id", "25674fbc0bf3")]:
            data = dict(self.data, **{key: value})
            self.export.write_text(json.dumps(data))
            with self.assertRaises(InputError):
                self.load()

    def test_validator_digest_missing_and_changed_fail_closed(self):
        from publisher.candidates import load_validator
        from publisher.files import InputError

        changed = self.root / "changed-validator.py"
        changed.write_bytes(SYNTHETIC_VALIDATOR + b"\n# changed\n")
        for path, sha in [
            (self.validator, "0" * 64),
            (changed, self.validator_sha),
            (self.root / "missing.py", self.validator_sha),
        ]:
            with self.assertRaises(InputError):
                load_validator(path, sha)

    def test_private_job_rejected_before_export_or_source_read(self):
        from publisher.candidates import load_candidate, load_validator
        from publisher.files import InputError

        with self.assertRaisesRegex(InputError, "^job_blocked$"):
            load_candidate(
                self.root / "missing",
                "3c3f81a925e0",
                "invalid",
                self.root / "missing",
                self.root / "missing",
                load_validator(self.validator, self.validator_sha),
            )

    def test_read_limits_and_path_escape(self):
        from publisher.files import InputError, safe_read

        with self.assertRaisesRegex(InputError, "^file_limit$"):
            safe_read(self.root, self.report.relative_to(self.root).as_posix(), limit=3)
        for ref in ("../target", "/etc/passwd", "a//b", "a/./b", "a\\b"):
            with self.subTest(ref=ref), self.assertRaises(InputError):
                safe_read(self.root, ref)
        with self.assertRaisesRegex(InputError, "^batch_limit$"):
            self.load(batch_limit=10)

    def test_cli_stages_only_approved_exports_and_sanitizes_output(self):
        private = self.root / "exports" / "3c3f81a925e0"
        private.mkdir()
        (private / f"{RUN}.json").symlink_to("/no-such-private-file")
        args = [
            sys.executable,
            "-c",
            "import runpy, sys; import publisher.candidates as c; "
            "c.REVIEWED_SHA256 = sys.argv.pop(1); "
            "runpy.run_module('publisher.cli', run_name='__main__')",
            self.validator_sha,
            "stage",
            "--exports",
            str(self.root / "exports"),
            "--source-root",
            str(self.root / "source"),
            "--item-root",
            str(self.root / "items"),
            "--validator",
            str(self.validator),
            "--validator-sha256",
            self.validator_sha,
            "--outbox",
            str(self.root / "private" / "outbox.sqlite"),
        ]
        result = subprocess.run(
            args, cwd=WORKLOAD, capture_output=True, text=True, check=False
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["staged"], 1)
        self.assertNotIn("private-synthetic-marker", result.stdout + result.stderr)
        second = subprocess.run(
            args, cwd=WORKLOAD, capture_output=True, text=True, check=False
        )
        self.assertEqual(json.loads(second.stdout)["duplicate"], 1)
        status = subprocess.run(
            [
                sys.executable,
                "-m",
                "publisher.cli",
                "status",
                "--outbox",
                str(self.root / "private" / "outbox.sqlite"),
            ],
            cwd=WORKLOAD,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(json.loads(status.stdout), {"awaiting_contract": 1})

    def test_validator_schema_error_sanitized(self):
        from publisher.files import InputError

        data = copy.deepcopy(self.data)
        data["items"][0]["secret-private-marker"] = "not a field"
        self.export.write_text(json.dumps(data))
        with contextlib.redirect_stdout(io.StringIO()) as out:
            with self.assertRaisesRegex(InputError, "^candidate_invalid$"):
                self.load()
        self.assertEqual(out.getvalue(), "")

    def test_scan_rejects_unsafe_missing_or_overflowing_export_directories(self):
        from argparse import Namespace

        from publisher.cli import _scan
        from publisher.files import InputError
        from publisher.outbox import Outbox

        args = Namespace(
            exports=self.root / "exports",
            source_root=self.root / "source",
            item_root=self.root / "items",
            validator=self.validator,
            validator_sha256=self.validator_sha,
        )
        box = Outbox(self.root / "private" / "outbox.sqlite")
        self.addCleanup(box.close)
        linked = args.exports / "25674fbc0bf3"
        linked.symlink_to(self.root)
        with self.assertRaises(InputError):
            _scan(args, box)
        linked.unlink()
        args.exports = self.root / "missing"
        with self.assertRaises(InputError):
            _scan(args, box)
        args.exports = self.root / "exports"
        for index in range(1001):
            (args.exports / JOB / f"{index:032x}.json").touch()
        with self.assertRaisesRegex(InputError, "^scan_limit$"):
            _scan(args, box)


if __name__ == "__main__":
    unittest.main()
