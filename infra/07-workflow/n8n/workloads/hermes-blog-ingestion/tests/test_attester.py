"""Queue attester: partial signing, retry window, resend, state and file modes."""

import base64
import hashlib
import json
import stat
import sys
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

WORKLOAD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKLOAD))
from publisher import attestation, attester  # noqa: E402
from publisher.delivery import FailureKind, TransportFailure  # noqa: E402
from publisher.http_transport import HttpResponse  # noqa: E402
from publisher.source_fetch import FetchFailure, FetchResult  # noqa: E402

JOB = "25674fbc0bf3"
T0 = datetime(2026, 11, 1, 12, 0, 0, tzinfo=UTC)
RID = "11111111-1111-1111-1111-111111111111"
SENTENCE = "The project shipped a new stable release for everyone today."
GOOD = "https://example.org/good"


def page(text=SENTENCE):
    body = f"<html><body><p>{text}</p></body></html>".encode()
    return FetchResult(
        final_url="https://example.org/final",
        status=200,
        sha256=hashlib.sha256(body).hexdigest(),
        fetched_at="2026-11-01T12:00:00.123Z",
        content_type="text/html; charset=utf-8",
        body=body,
    )


def item(item_id, url=GOOD, quotes=(SENTENCE,)):
    entry = {
        "item_id": item_id,
        "kind": "devops",
        "title": "A release note",
        "body": SENTENCE,
        "source_url": url,
    }
    if quotes is not None:
        entry["source_quotes"] = list(quotes)
    return entry


def request(items, job=JOB):
    return attestation._canonical(
        {
            "schema_version": "1.0",
            "producer": "hermes",
            "job_id": job,
            "run_id": "2026-11-01",
            "source_sha256": "a" * 64,
            "source_text": "x",
            "items": items,
        }
    )


class Reader:
    def __init__(self, requests):
        self.requests = requests
        self.calls = []

    def queue(self):
        return iter(list(self.requests))

    def request(self, report_id):
        self.calls.append(report_id)
        value = self.requests[report_id]
        if isinstance(value, Exception):
            raise value
        return value


class Sender:
    def __init__(self, *answers):
        self.answers = list(answers)
        self.sent = []

    def __call__(self, report_id, body):
        self.sent.append((report_id, body))
        answer = self.answers.pop(0) if self.answers else HttpResponse(201, b"{}")
        if isinstance(answer, TransportFailure):
            raise answer
        return answer


class Fetcher:
    def __init__(self, table):
        self.table = table
        self.calls = []

    def __call__(self, url):
        self.calls.append(url)
        value = self.table[url]
        if isinstance(value, Exception):
            raise value
        return value


class AttesterTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.state = Path(tmp.name) / "state"
        self.evidence = Path(tmp.name) / "evidence"
        self.key = Ed25519PrivateKey.generate()
        self.clock = T0

    def go(self, reader, sender, fetcher, **kw):
        return attester.run(
            reader,
            sender,
            key_id="k1",
            key=self.key,
            state_dir=self.state,
            evidence_dir=self.evidence,
            fetcher=fetcher,
            now=lambda: self.clock,
            **kw,
        )

    def test_partial_report_signs_only_verified_items(self):
        items = [
            item("c"),
            item("a"),
            item("b", quotes=("A sentence that is absent.",)),
        ]
        reader = Reader({RID: request(items)})
        sender = Sender()
        counts = self.go(reader, sender, Fetcher({GOOD: page()}))
        self.assertEqual(
            counts,
            {"attested": 1, "held_items": 1, "skipped": 0, "retry": 0, "rejected": 0},
        )
        body = json.loads(sender.sent[0][1])
        self.assertEqual([i["item_id"] for i in body["verified_items"]], ["a", "c"])
        self.assertEqual(
            body["verified_items"][0]["final_url"], "https://example.org/final"
        )
        raw = (self.evidence / f"{RID}.json").read_bytes()
        self.assertEqual(body["evidence_sha256"], hashlib.sha256(raw).hexdigest())
        evidence = json.loads(raw)
        self.assertEqual(evidence["verifier"], "hy-home-attester/1")
        self.assertNotIn(SENTENCE, raw.decode())
        signed = attestation.message(
            reader.requests[RID], body["verified_items"], body["evidence_sha256"]
        )
        self.key.public_key().verify(base64.b64decode(body["signature"]), signed)

    def test_unapproved_job_signs_empty_list(self):
        reader = Reader({RID: request([item("a")], job="000000000000")})
        sender, fetcher = Sender(), Fetcher({})
        counts = self.go(reader, sender, fetcher)
        self.assertEqual(json.loads(sender.sent[0][1])["verified_items"], [])
        self.assertEqual(fetcher.calls, [])
        self.assertEqual(counts["attested"], 1)

    def test_transient_failure_waits_then_signs_after_six_hours(self):
        flaky = "https://example.org/flaky"
        reader = Reader({RID: request([item("a"), item("b", url=flaky)])})
        fetcher = Fetcher(
            {GOOD: page(), flaky: FetchFailure("timeout", transient=True)}
        )
        sender = Sender()
        self.clock = T0
        self.go(reader, sender, fetcher)
        self.clock = T0 + timedelta(hours=1)
        counts = self.go(reader, sender, fetcher)
        self.assertEqual((counts["retry"], counts["attested"]), (1, 0))
        self.assertEqual(sender.sent, [])
        self.clock = T0 + timedelta(hours=6)
        counts = self.go(reader, sender, fetcher)
        self.assertEqual((counts["attested"], counts["held_items"]), (1, 1))
        body = json.loads(sender.sent[0][1])
        self.assertEqual([i["item_id"] for i in body["verified_items"]], ["a"])

    def test_lost_response_resends_identical_body(self):
        reader = Reader({RID: request([item("a")])})
        sender = Sender(TransportFailure(FailureKind.AMBIGUOUS))
        fetcher = Fetcher({GOOD: page()})
        counts = self.go(reader, sender, fetcher)
        self.assertEqual((counts["retry"], counts["attested"]), (1, 0))
        counts = self.go(reader, sender, fetcher)
        self.assertEqual(counts["attested"], 1)
        self.assertEqual(sender.sent[0], sender.sent[1])
        self.assertEqual(len(fetcher.calls), 1)
        self.assertEqual(reader.calls, [RID])

    def test_quarantined_report_recorded_and_not_refetched(self):
        reader = Reader({RID: None})
        sender = Sender()
        self.assertEqual(self.go(reader, sender, Fetcher({}))["skipped"], 1)
        self.assertEqual(self.go(reader, sender, Fetcher({}))["skipped"], 1)
        self.assertEqual(reader.calls, [RID])
        self.assertEqual(sender.sent, [])

    def test_attested_report_not_refetched_and_duplicate_200_counts_attested(self):
        reader = Reader({RID: request([item("a")])})
        sender = Sender(HttpResponse(200, b"{}"))
        fetcher = Fetcher({GOOD: page()})
        self.assertEqual(self.go(reader, sender, fetcher)["attested"], 1)
        counts = self.go(reader, sender, fetcher)
        self.assertEqual((counts["attested"], counts["skipped"]), (0, 1))
        self.assertEqual(len(sender.sent), 1)
        self.assertEqual(len(fetcher.calls), 1)

    def test_fingerprint_mismatch_rejects_without_sending(self):
        bad = request([item("a")]).replace(b'"hermes"', b'"hermes" ')
        reader = Reader({RID: bad})
        sender = Sender()
        counts = self.go(reader, sender, Fetcher({GOOD: page()}))
        self.assertEqual(counts["rejected"], 1)
        self.assertEqual(sender.sent, [])
        self.assertEqual(self.go(reader, sender, Fetcher({GOOD: page()}))["skipped"], 1)

    def test_state_and_evidence_files_are_0600_in_0700_dirs(self):
        reader = Reader({RID: request([item("a")])})
        self.go(reader, Sender(), Fetcher({GOOD: page()}))
        for directory in (self.state, self.evidence):
            self.assertEqual(stat.S_IMODE(directory.stat().st_mode), 0o700)
            for f in directory.iterdir():
                self.assertEqual(stat.S_IMODE(f.stat().st_mode), 0o600)
            self.assertEqual(len(list(directory.iterdir())), 1)

    def test_crash_in_one_report_does_not_stop_the_next(self):
        other = "22222222-2222-2222-2222-222222222222"
        reader = Reader({RID: RuntimeError("boom secret"), other: request([item("a")])})
        sender = Sender()
        counts = self.go(reader, sender, Fetcher({GOOD: page()}))
        self.assertEqual((counts["rejected"], counts["attested"]), (1, 1))
        self.assertEqual(sender.sent[0][0], other)
        self.assertNotIn("boom", json.dumps(counts))
        self.assertFalse((self.state / f"{RID}.json").exists())

    def test_rejected_stored_body_is_never_resent(self):
        reader = Reader({RID: request([item("a")])})
        sender = Sender(HttpResponse(422, b"{}"))
        fetcher = Fetcher({GOOD: page()})
        self.assertEqual(self.go(reader, sender, fetcher)["rejected"], 1)
        counts = self.go(reader, sender, fetcher)
        self.assertEqual((counts["rejected"], counts["skipped"]), (0, 1))
        self.assertEqual(len(sender.sent), 1)

    def test_auth_failure_keeps_body_and_halts_then_resends(self):
        other = "22222222-2222-2222-2222-222222222222"
        reader = Reader({RID: request([item("a")]), other: request([item("a")])})
        for failure in (HttpResponse(401, b"{}"), TransportFailure(FailureKind.TLS)):
            self.setUp()
            sender = Sender(failure)
            fetcher = Fetcher({GOOD: page()})
            counts = self.go(reader, sender, fetcher)
            self.assertEqual((counts["rejected"], counts["attested"]), (1, 0))
            self.assertEqual(len(sender.sent), 1)  # halted before the second
            state = json.loads((self.state / f"{RID}.json").read_text())
            self.assertEqual(state["status"], "signed")
            counts = self.go(reader, sender, fetcher)
            self.assertEqual(sender.sent[0], sender.sent[1])
            self.assertEqual(counts["attested"], 2)

    def test_stray_value_error_does_not_close_the_report(self):
        reader = Reader({RID: request([item("a")])})
        sender = Sender()
        counts = self.go(reader, sender, Fetcher({GOOD: ValueError("bug")}))
        self.assertEqual((counts["rejected"], sender.sent), (1, []))
        state = json.loads((self.state / f"{RID}.json").read_text())
        self.assertNotIn("status", state)
        self.assertEqual(counts["errors"], {"ValueError": 1})

    def test_more_than_100_verified_items_records_limit(self):
        items = [item(f"i{n:03d}") for n in range(101)]
        reader = Reader({RID: request(items)})
        sender = Sender()
        counts = self.go(reader, sender, Fetcher({GOOD: page()}))
        body = json.loads(sender.sent[0][1])
        self.assertEqual(len(body["verified_items"]), 100)
        self.assertEqual(counts["held_items"], 1)
        evidence = json.loads((self.evidence / f"{RID}.json").read_bytes())
        last = next(i for i in evidence["items"] if i["item_id"] == "i100")
        self.assertEqual(last["codes"], ["limit"])

    def test_identical_urls_are_fetched_once(self):
        other = "22222222-2222-2222-2222-222222222222"
        reader = Reader(
            {RID: request([item("a"), item("b")]), other: request([item("c")])}
        )
        fetcher = Fetcher({GOOD: page()})
        self.go(reader, Sender(), fetcher)
        self.assertEqual(fetcher.calls, [GOOD])

    def test_item_missing_quotes_is_not_fetched(self):
        reader = Reader({RID: request([item("a", quotes=None)])})
        fetcher = Fetcher({})
        counts = self.go(reader, Sender(), fetcher)
        self.assertEqual((fetcher.calls, counts["held_items"]), ([], 1))

    def test_invalid_report_id_is_rejected_without_io(self):
        reader = Reader({"../evil": b"{}"})
        counts = self.go(reader, Sender(), Fetcher({}))
        self.assertEqual((counts["rejected"], reader.calls), (1, []))


class ReaderTest(unittest.TestCase):
    def reader(self, answers):
        seen = []

        def opener(host, port, path, headers):
            seen.append((host, port, path, headers))
            return answers.pop(0)

        return attester.GatewayReader(
            "https://gw.example:8443", ("Authorization", "Bearer x"), opener=opener
        ), seen

    def test_queue_follows_next_after(self):
        page1 = json.dumps({"items": [{"report_id": "a"}], "next_after": 7}).encode()
        page2 = json.dumps({"items": [{"report_id": "b"}], "next_after": None}).encode()
        reader, seen = self.reader([(200, page1), (200, page2)])
        self.assertEqual(list(reader.queue()), ["a", "b"])
        self.assertIn("limit=100", seen[0][2])
        self.assertIn("after=7", seen[1][2])
        self.assertEqual(seen[0][3]["Authorization"], "Bearer x")

    def test_request_returns_none_on_quarantine_and_errors_on_redirect(self):
        reader, _ = self.reader([(409, b'{"error":{"code":"REPORT_QUARANTINED"}}')])
        self.assertIsNone(reader.request(RID))
        reader, _ = self.reader([(302, b"")])
        with self.assertRaises(attester.GatewayError):
            reader.request(RID)

    def test_http_exception_becomes_gateway_error_without_traceback(self):
        import http.client
        from unittest import mock

        from publisher import cli

        # The default opener wraps HTTPException; the CLI catches GatewayError.
        with (
            mock.patch.object(cli, "_auth", return_value=("A", "B")),
            mock.patch.object(attestation, "load_signing_key", return_value=object()),
            mock.patch.object(
                attester.http.client.HTTPSConnection,
                "request",
                side_effect=http.client.BadStatusLine("x"),
            ),
            mock.patch("builtins.print") as out,
        ):
            argv = [
                "attest-queue",
                "--gateway",
                "https://gw.example",
                "--auth-header-file",
                "/a",
                "--signing-key",
                "/k",
                "--key-id",
                "k1",
                "--state-dir",
                self.tmp,
                "--evidence-dir",
                self.tmp,
            ]
            self.assertEqual(cli.main(argv), 1)
        self.assertEqual(out.call_args.args[0], '{"error":"operation_rejected"}')

    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.tmp = t.name

    def test_non_advancing_cursor_is_an_error(self):
        loop = json.dumps({"items": [], "next_after": 0}).encode()
        reader, _ = self.reader([(200, loop)])
        with self.assertRaises(attester.GatewayError):
            list(reader.queue())


class CliTest(unittest.TestCase):
    def test_attest_queue_prints_counts_only_and_fails_on_rejected(self):
        from unittest import mock

        from publisher import cli

        for rejected, code in ((0, 0), (1, 1)):
            counts = dict(
                attested=2, held_items=0, skipped=0, retry=0, rejected=rejected
            )
            with (
                mock.patch.object(
                    cli, "_auth", return_value=("Authorization", "Bearer s")
                ),
                mock.patch.object(
                    attestation, "load_signing_key", return_value=object()
                ),
                mock.patch.object(attester, "run", return_value=counts),
                mock.patch("builtins.print") as out,
            ):
                argv = [
                    "attest-queue",
                    "--gateway",
                    "https://gw.example",
                    "--auth-header-file",
                    "/a",
                    "--signing-key",
                    "/k",
                    "--key-id",
                    "k1",
                    "--state-dir",
                    "/s",
                    "--evidence-dir",
                    "/e",
                ]
                self.assertEqual(cli.main(argv), code)
            printed = out.call_args.args[0]
            self.assertEqual(json.loads(printed), counts)
            self.assertNotIn("Bearer", printed)


if __name__ == "__main__":
    unittest.main()
