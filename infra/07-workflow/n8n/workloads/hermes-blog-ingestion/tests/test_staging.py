"""Synthetic filesystem evidence; no host reports or credentials are read."""

import contextlib
import copy
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

WORKLOAD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKLOAD))
# The synthetic double below exercises loader wiring only; VALIDATOR is the
# main-tracked SPEC-0247 validator whose bytes the Publisher pins.
VALIDATOR = WORKLOAD.parents[4] / "scripts/validation/check-hermes-candidate.py"
VALIDATOR_SHA = "957d047c77a3448d2ae6ed4cc61d88efc2705599d6f95f20d9d7e99510695714"
PRE_MERGE_SHA = "8c988c715286edd53d2f7e5931cb349e6a5bed49be8ec2f8e7be98f2810c7297"
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

    def test_pinned_validator_compatibility(self):
        from publisher import candidates

        self.validator_patcher.stop()
        self.assertEqual(candidates.REVIEWED_SHA256, VALIDATOR_SHA)
        self.assertEqual(digest(VALIDATOR.read_bytes()), VALIDATOR_SHA)
        validator = candidates.load_validator(VALIDATOR, VALIDATOR_SHA)
        snapshot = candidates.load_candidate(
            self.root / "exports",
            JOB,
            f"{RUN}.json",
            self.root / "source",
            self.root / "items",
            validator,
        )
        self.assertEqual(snapshot.source, self.report.read_bytes())

    def test_pinned_validator_rejects_draft_changed_or_linked_bytes(self):
        from publisher import candidates
        from publisher.files import InputError

        self.validator_patcher.stop()
        changed = self.root / "changed-validator.py"
        changed.write_bytes(VALIDATOR.read_bytes() + b"\n")
        linked = self.root / "linked-validator.py"
        linked.symlink_to(VALIDATOR)
        for path, sha in (
            (VALIDATOR, PRE_MERGE_SHA),
            (changed, VALIDATOR_SHA),
            (linked, VALIDATOR_SHA),
            (self.root / "missing.py", VALIDATOR_SHA),
        ):
            with self.subTest(path=path.name, sha=sha[:8]):
                with self.assertRaises(InputError):
                    candidates.load_validator(path, sha)

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

    def test_cli_snapshots_untrusted_evidence_without_authorizing_delivery(self):
        from argparse import Namespace

        from publisher.cli import _scan
        from publisher.delivery import process_one
        from publisher.outbox import Outbox

        evidence_root = self.root / "evidence"
        evidence_root.mkdir()
        name = digest((JOB + "\0" + RUN).encode()) + ".json"
        evidence = b'{"untrusted":"private-evidence-marker"}'
        (evidence_root / name).write_bytes(evidence)
        args = Namespace(
            exports=self.root / "exports",
            source_root=self.root / "source",
            item_root=self.root / "items",
            validator=self.validator,
            validator_sha256=self.validator_sha,
            evidence_root=evidence_root,
        )
        box = Outbox(self.root / "private" / "outbox.sqlite")
        self.addCleanup(box.close)
        result = _scan(args, box)
        self.assertEqual(result["evidence_stored"], 1)
        self.assertEqual(box.get_unverified_evidence((JOB, RUN)), evidence)
        self.assertEqual(process_one(box, (JOB, RUN)), "blocked")
        (evidence_root / name).write_bytes(b"changed")
        self.assertEqual(_scan(args, box)["rejected"], 1)
        self.assertEqual(box.get_unverified_evidence((JOB, RUN)), evidence)
        self.assertEqual(box.get((JOB, RUN))["status"], "awaiting_contract")

    def test_evidence_missing_and_symlink_fail_closed(self):
        from argparse import Namespace

        from publisher.cli import _scan
        from publisher.outbox import Outbox

        evidence_root = self.root / "evidence"
        evidence_root.mkdir()
        args = Namespace(
            exports=self.root / "exports",
            source_root=self.root / "source",
            item_root=self.root / "items",
            validator=self.validator,
            validator_sha256=self.validator_sha,
            evidence_root=evidence_root,
        )
        box = Outbox(self.root / "private" / "outbox.sqlite")
        self.addCleanup(box.close)
        self.assertEqual(_scan(args, box)["rejected"], 1)
        name = digest((JOB + "\0" + RUN).encode()) + ".json"
        (evidence_root / name).symlink_to(self.export)
        self.assertEqual(_scan(args, box)["rejected"], 1)
        self.assertEqual(box.counts(), {})

    def test_cli_accepts_evidence_root_and_never_prints_evidence(self):
        from publisher.outbox import Outbox

        evidence_root = self.root / "evidence"
        evidence_root.mkdir()
        name = digest((JOB + "\0" + RUN).encode()) + ".json"
        evidence = b"private-evidence-marker"
        (evidence_root / name).write_bytes(evidence)
        db = self.root / "private" / "outbox.sqlite"
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
            str(db),
            "--evidence-root",
            str(evidence_root),
        ]
        result = subprocess.run(
            args, cwd=WORKLOAD, capture_output=True, text=True, check=False
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["evidence_stored"], 1)
        self.assertNotIn(evidence.decode(), result.stdout + result.stderr)
        box = Outbox(db)
        self.addCleanup(box.close)
        self.assertEqual(box.get_unverified_evidence((JOB, RUN)), evidence)

    def test_evidence_snapshot_rolls_back_as_one_transaction(self):
        from publisher.outbox import Outbox

        box = Outbox(self.root / "private" / "outbox.sqlite")
        self.addCleanup(box.close)
        with patch.object(
            box, "_bind_unverified_evidence", side_effect=RuntimeError("interrupt")
        ):
            with self.assertRaises(RuntimeError):
                box.stage_with_unverified_evidence(self.load(), b"evidence")
        box.close()
        box = Outbox(self.root / "private" / "outbox.sqlite")
        self.addCleanup(box.close)
        self.assertEqual(box.counts(), {})
        self.assertEqual(
            box.stage_with_unverified_evidence(self.load(), b"evidence"), "staged"
        )
        self.assertEqual(box.get_unverified_evidence((JOB, RUN)), b"evidence")

    def test_unverified_evidence_cannot_dispatch_with_adapter_and_transport(self):
        from publisher.delivery import process_one
        from publisher.gateway_adapter import DESTINATION, GatewayAdapter
        from publisher.http_transport import HttpTransport
        from publisher.outbox import Outbox

        box = Outbox(self.root / "private" / "outbox.sqlite")
        self.addCleanup(box.close)
        box.stage_with_unverified_evidence(self.load(), b"evidence")
        adapter = GatewayAdapter(
            scheduled_at="2026-10-30T00:00:00Z",
            generated_at="2026-10-30T09:00:00+09:00",
            collected_at="2026-10-30T00:02:00Z",
        )
        transport = HttpTransport(
            endpoint="http://127.0.0.1/fixture",
            destination=DESTINATION,
            auth=("Authorization", "synthetic"),
            allow_loopback_http=True,
        )
        with patch.object(HttpTransport, "send") as send:
            self.assertEqual(
                process_one(box, (JOB, RUN), adapter, transport), "blocked"
            )
            send.assert_not_called()
        self.assertIsNone(box.get((JOB, RUN))["request_body"])
        from publisher.outbox import OutboxError

        with self.assertRaisesRegex(OutboxError, "^evidence_unverified$"):
            box.bind_request((JOB, RUN), "v1", b"body")

    def test_missing_evidence_cannot_dispatch_with_gateway_adapter_and_transport(self):
        from publisher.delivery import process_one
        from publisher.gateway_adapter import DESTINATION, GatewayAdapter
        from publisher.http_transport import HttpTransport
        from publisher.outbox import Outbox

        box = Outbox(self.root / "private" / "outbox.sqlite")
        self.addCleanup(box.close)
        box.stage(self.load())
        adapter = GatewayAdapter(
            scheduled_at="2026-10-30T00:00:00Z",
            generated_at="2026-10-30T09:00:00+09:00",
            collected_at="2026-10-30T00:02:00Z",
        )
        transport = HttpTransport(
            endpoint="http://127.0.0.1/fixture",
            destination=DESTINATION,
            auth=("Authorization", "synthetic"),
            allow_loopback_http=True,
        )
        with patch.object(HttpTransport, "send") as send:
            self.assertEqual(
                process_one(box, (JOB, RUN), adapter, transport), "blocked"
            )
            send.assert_not_called()
        self.assertIsNone(box.get((JOB, RUN))["request_body"])

    def test_all_admitted_jobs_block_low_level_request_binding(self):
        from publisher.candidates import JOBS, Snapshot
        from publisher.outbox import Outbox, OutboxError

        box = Outbox(self.root / "private" / "outbox.sqlite")
        self.addCleanup(box.close)
        for job in JOBS:
            key = (job, RUN)
            box.stage(Snapshot(*key, b"candidate", "source", b"report"))
            with (
                self.subTest(job=job),
                self.assertRaisesRegex(OutboxError, "^evidence_unverified$"),
            ):
                box.bind_request(key, "v1", b"body")
            self.assertIsNone(box.get(key)["request_body"])

    def test_all_admitted_jobs_block_direct_gateway_replay(self):
        from dataclasses import replace

        from publisher.candidates import JOBS
        from publisher.delivery import DispatchRequest, TransportFailure
        from publisher.gateway_adapter import DESTINATION, REVISION
        from publisher.gateway_transport import GatewayReplayTransport
        from publisher.http_transport import HttpTransport

        class Network:
            endpoint_sha256 = "e" * 64

            def __init__(self):
                self.operations = []

            def send(self, request):
                self.operations.append(request)

        network = Network()
        transport = GatewayReplayTransport(
            object(), network, allow_idempotent_replay=True
        )
        http = HttpTransport(
            endpoint="https://example.test/ingest",
            destination=DESTINATION,
            auth=("Authorization", "synthetic"),
        )
        for job in JOBS:
            request = DispatchRequest(
                (job, RUN), "a" * 64, "b" * 64, REVISION, DESTINATION, b"body", "e" * 64
            )
            for operation in (transport.send, transport.reconcile):
                with self.subTest(job=job, operation=operation.__name__):
                    with self.assertRaises(TransportFailure):
                        operation(request)
            with patch("publisher.http_transport.subprocess.run") as child:
                with self.assertRaises(TransportFailure):
                    http.send(replace(request, endpoint_sha256=http.endpoint_sha256))
                child.assert_not_called()
        self.assertEqual(network.operations, [])

    def test_missing_evidence_root_rejected_even_when_no_candidates(self):
        from argparse import Namespace

        from publisher.cli import _scan
        from publisher.files import InputError
        from publisher.outbox import Outbox

        self.export.unlink()
        args = Namespace(
            exports=self.root / "exports",
            source_root=self.root / "source",
            item_root=self.root / "items",
            validator=self.validator,
            validator_sha256=self.validator_sha,
            evidence_root=self.root / "missing",
        )
        box = Outbox(self.root / "private" / "outbox.sqlite")
        self.addCleanup(box.close)
        with self.assertRaisesRegex(InputError, "^directory_missing$"):
            _scan(args, box)

    def test_concurrent_dispatch_cannot_enter_during_evidence_staging(self):
        from publisher.delivery import process_one
        from publisher.outbox import Outbox, OutboxError

        class SyntheticAdapter:
            pass

        class SyntheticGateway:
            def __init__(self):
                self.operations = []

        snapshot = self.load()
        path = self.root / "private" / "outbox.sqlite"
        box = Outbox(path)
        self.addCleanup(box.close)
        entered, release = threading.Event(), threading.Event()
        failures = []
        original = Outbox._bind_unverified_evidence

        def pause(local, *args):
            entered.set()
            if not release.wait(5):
                raise RuntimeError("test_timeout")
            return original(local, *args)

        def stage():
            local = Outbox(path)
            try:
                local.stage_with_unverified_evidence(snapshot, b"evidence")
            except Exception as error:
                failures.append(error)
            finally:
                local.close()

        gateway = SyntheticGateway()
        with patch.object(Outbox, "_bind_unverified_evidence", pause):
            thread = threading.Thread(target=stage)
            thread.start()
            try:
                self.assertTrue(entered.wait(5))
                with self.assertRaisesRegex(OutboxError, "^delivery_locked$"):
                    process_one(box, (JOB, RUN), SyntheticAdapter(), gateway)
            finally:
                release.set()
                thread.join(5)
        self.assertFalse(thread.is_alive())
        self.assertEqual(failures, [])
        self.assertEqual(
            process_one(box, (JOB, RUN), SyntheticAdapter(), gateway), "blocked"
        )
        self.assertEqual(gateway.operations, [])

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
