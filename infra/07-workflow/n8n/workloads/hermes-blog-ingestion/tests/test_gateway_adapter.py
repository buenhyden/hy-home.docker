"""Pinned upstream schema and synthetic exporter data; no network or credentials."""

import hashlib
import json
import sys
import unittest
from pathlib import Path

WORKLOAD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKLOAD))
FIXTURES = Path(__file__).parent / "fixtures"


class GatewayAdapterTests(unittest.TestCase):
    def setUp(self):
        from publisher.gateway_adapter import GatewayAdapter

        self.adapter = GatewayAdapter(
            scheduled_at="2026-10-30T00:00:00Z",
            generated_at="2026-10-30T00:01:00Z",
            collected_at="2026-10-30T00:02:00Z",
        )
        self.raw = b"synthetic report\n"
        self.candidate = {
            "job_id": "6eabd835f969",
            "run_id": "a" * 32,
            "report_kind": "strategy-news",
            "generated_at": "2026-10-30T00:01:00Z",
            "source_ref": "cron/output/6eabd835f969/report.md",
            "source_sha256": hashlib.sha256(self.raw).hexdigest(),
            "items": [{"title": "Example", "summary": "Body", "source_url": None}],
        }
        self.snapshot = {
            "job_id": self.candidate["job_id"],
            "run_id": self.candidate["run_id"],
            "candidate": json.dumps(self.candidate).encode(),
            "source_ref": "cron/output/6eabd835f969/report.md",
            "source": self.raw,
            "source_sha256": hashlib.sha256(self.raw).hexdigest(),
            "ideas": (),
        }
        self.snapshot["candidate_sha256"] = hashlib.sha256(
            self.snapshot["candidate"]
        ).hexdigest()

    def set_candidate(self):
        self.snapshot["candidate"] = json.dumps(self.candidate).encode()
        self.snapshot["candidate_sha256"] = hashlib.sha256(
            self.snapshot["candidate"]
        ).hexdigest()

    def request(self):
        from publisher.delivery import DispatchRequest

        bound = self.adapter.prepare(self.snapshot)
        return DispatchRequest(
            (self.snapshot["job_id"], self.snapshot["run_id"]),
            self.snapshot["source_sha256"],
            hashlib.sha256(bound.body).hexdigest(),
            bound.contract_revision,
            bound.destination,
            bound.body,
        )

    def response(self, status=201, **changes):
        from publisher.http_transport import HttpResponse

        report_id = "12345678-1234-1234-1234-123456789abc"
        data = dict(
            id=report_id,
            persisted=True,
            duplicate=False,
            status="received",
            candidate_count=1,
            status_url=f"/v1/ingestions/{report_id}",
        )
        data.update(changes)
        return HttpResponse(status, json.dumps(data).encode(), "application/json")

    def test_upstream_fixture_integrity(self):
        digests = {
            "openapi-v1.json": (
                "602705cfb4fbf06953776a5e6b19344bdbcd7e1c35771d58cdd612917d46ba67"
            ),
            "ingestion-v1.schema.json": "17a56a5746a3c2a3b36c34553e9038159ec04f3a2fea02325b86f5b8ed8d00d9",
            "responses-v1.schema.json": "b1d918b3accacc85f260f34d2e9156d44e7d51fcf39c0da7886419d1498322b6",
            "synthetic-report.json": "2971ac9ae77612ca16334fe7b22de07ebfb7d367df21fa947b09d08305d50fbc",
        }
        for name, expected in digests.items():
            self.assertEqual(
                hashlib.sha256((FIXTURES / name).read_bytes()).hexdigest(), expected
            )

    def test_openapi_declares_ingestion_contract(self):
        spec = json.loads((FIXTURES / "openapi-v1.json").read_bytes())
        post = spec["paths"]["/v1/ingestions"]["post"]
        self.assertEqual(post["operationId"], "createIngestion")
        self.assertEqual(post["security"], [{"bearerAuth": []}])
        self.assertEqual(
            post["requestBody"]["content"]["application/json"]["schema"]["$ref"],
            "./ingestion-v1.schema.json",
        )
        for status in ("200", "201"):
            self.assertEqual(
                post["responses"][status]["content"]["application/json"]["schema"][
                    "$ref"
                ],
                "./responses-v1.schema.json#/definitions/receipt",
            )
        self.assertTrue(
            {"400", "401", "403", "409", "413", "415", "422", "503"}.issubset(
                post["responses"]
            )
        )

    def test_fixture_and_generated_request_conform_to_upstream_schema(self):
        import jsonschema

        schema = json.loads((FIXTURES / "ingestion-v1.schema.json").read_bytes())
        fixture = json.loads((FIXTURES / "synthetic-report.json").read_bytes())
        jsonschema.validate(fixture, schema, format_checker=jsonschema.FormatChecker())
        request = json.loads(self.request().body)
        jsonschema.validate(request, schema, format_checker=jsonschema.FormatChecker())
        self.assertEqual(request["source_text"].encode(), self.raw)
        self.assertEqual(request["source_sha256"], self.snapshot["source_sha256"])
        self.assertEqual(
            json.loads(request["items"][0]["body"])["candidate"],
            self.candidate["items"][0],
        )

    def test_authoritative_timestamps_mandatory(self):
        from publisher.gateway_adapter import GatewayAdapter

        with self.assertRaises(ValueError):
            GatewayAdapter(
                scheduled_at=None,
                generated_at="2026-10-30T00:01:00Z",
                collected_at="2026-10-30T00:02:00Z",
            )
        del self.candidate["generated_at"]
        self.set_candidate()
        with self.assertRaises(ValueError):
            self.adapter.prepare(self.snapshot)

    def test_receipt_and_replay(self):
        from publisher.delivery import OutcomeKind

        for response in (self.response(), self.response(200, duplicate=True)):
            outcome = self.adapter.interpret(response, self.request())
            self.assertEqual(outcome.kind, OutcomeKind.DURABLE)
            self.assertEqual(
                outcome.receipt.gateway_report_id,
                "12345678-1234-1234-1234-123456789abc",
            )

    def test_incomplete_or_conflicting_receipt_never_succeeds(self):
        from publisher.delivery import OutcomeKind

        for response in (
            self.response(persisted=False),
            self.response(candidate_count=2),
            self.response(201, duplicate=True),
            self.response(503),
            self.response(status_url="https://example.org/"),
        ):
            self.assertNotEqual(
                self.adapter.interpret(response, self.request()).kind,
                OutcomeKind.DURABLE,
            )
        self.assertEqual(
            self.adapter.interpret(self.response(409), self.request()).kind,
            OutcomeKind.CONFLICT,
        )

    def test_multiple_idea_contents_preserved(self):
        self.candidate.update(
            job_id="8d0925bc571d",
            report_kind="solo-dev-ideas",
            items=[
                {
                    "title": "Idea 1",
                    "source_ref": "idea1",
                    "source_sha256": hashlib.sha256(b"One").hexdigest(),
                },
                {
                    "title": "Idea 2",
                    "source_ref": "idea2",
                    "source_sha256": hashlib.sha256(b"Two").hexdigest(),
                },
            ],
        )
        self.snapshot.update(
            job_id=self.candidate["job_id"],
            candidate=json.dumps(self.candidate).encode(),
            ideas=(("idea1", b"One"), ("idea2", b"Two")),
        )
        self.set_candidate()
        items = json.loads(self.request().body)["items"]
        self.assertEqual(
            [json.loads(item["body"])["source_text"] for item in items], ["One", "Two"]
        )

    def test_changed_candidate_source_binding_rejected(self):
        self.candidate["source_sha256"] = "0" * 64
        self.set_candidate()
        with self.assertRaises(ValueError):
            self.adapter.prepare(self.snapshot)

    def test_changed_candidate_bytes_rejected(self):
        self.snapshot["candidate"] += b" "
        with self.assertRaises(ValueError):
            self.adapter.prepare(self.snapshot)

    def test_permanent_rejection_and_temporary_failure_classification(self):
        from publisher.delivery import OutcomeKind

        for status in (400, 401, 403, 404, 413, 415, 422):
            with self.subTest(status=status):
                self.assertEqual(
                    self.adapter.interpret(self.response(status), self.request()).kind,
                    OutcomeKind.REJECTED,
                )
        self.assertEqual(
            self.adapter.interpret(self.response(503), self.request()).kind,
            OutcomeKind.UNKNOWN,
        )

    def test_source_url_is_preserved_at_top_level(self):
        self.candidate["items"][0]["source_url"] = "https://example.org/news"
        self.set_candidate()
        self.assertEqual(
            json.loads(self.request().body)["items"][0]["source_url"],
            "https://example.org/news",
        )
        self.candidate["items"][0]["source_url"] = None
        self.set_candidate()
        self.assertNotIn("source_url", json.loads(self.request().body)["items"][0])
        for url in (
            "https://user:pass@example.org/",
            "https://example.org/a b",
            "ftp://example.org/",
            "https:///missing",
            "https://example.org:bad/",
        ):
            with self.subTest(url=url):
                self.candidate["items"][0]["source_url"] = url
                self.set_candidate()
                with self.assertRaises(ValueError):
                    self.request()

    def test_timestamp_must_be_rfc3339(self):
        from publisher.gateway_adapter import GatewayAdapter

        with self.assertRaises(ValueError):
            GatewayAdapter(
                scheduled_at="2026-10-30 00:00:00+00:00",
                generated_at="2026-10-30T00:01:00Z",
                collected_at="2026-10-30T00:02:00Z",
            )
        with self.assertRaises(ValueError):
            GatewayAdapter(
                scheduled_at="2026-10-30T00:00:00.1234Z",
                generated_at="2026-10-30T00:01:00Z",
                collected_at="2026-10-30T00:02:00Z",
            )


if __name__ == "__main__":
    unittest.main()
