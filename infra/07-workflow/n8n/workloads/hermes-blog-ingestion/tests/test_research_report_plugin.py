"""Unit tests for research-report plugin source_quotes validation."""

from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parents[1] / "hermes-plugin"
sys.path.insert(0, str(PLUGIN_DIR))

import tools  # type: ignore  # noqa: E402

BASE_PAYLOAD = {
    "schema_version": "1.0",
    "producer": "test-producer",
    "job_id": "6eabd835f969",
    "run_id": "run-1",
    "report_kind": "news",
    "scheduled_at": "2026-11-01T00:00:00Z",
    "generated_at": "2026-11-01T00:01:00Z",
    "collected_at": "2026-11-01T00:00:30Z",
    "source_ref": "https://example.com/source",
    "source_text": "source text",
    "source_sha256": hashlib.sha256(b"source text").hexdigest(),
    "idempotency_key": "idem-1",
    "items": [{"item_id": "item-1", "kind": "news", "title": "title", "body": "body"}],
}


def make_payload(**item_overrides):
    payload = {
        k: (list(v) if isinstance(v, list) else dict(v) if isinstance(v, dict) else v)
        for k, v in BASE_PAYLOAD.items()
    }
    if item_overrides:
        payload["items"] = [dict(payload["items"][0], **item_overrides)]
    return payload


class SourceQuotesValidationTests(unittest.TestCase):
    def test_valid_one_to_three_quotes_passes(self):
        p = make_payload(
            source_quotes=["Sentence one.", "Sentence two.", "Sentence three."]
        )
        self.assertIsNone(tools._validate(p))

    def test_missing_source_quotes_passes(self):
        p = make_payload()
        self.assertIsNone(tools._validate(p))
        self.assertNotIn("source_quotes", p["items"][0])

    def test_empty_array_rejected(self):
        p = make_payload(source_quotes=[])
        self.assertEqual(tools._validate(p), "invalid_source_quotes")

    def test_four_or_more_rejected(self):
        p = make_payload(source_quotes=["a", "b", "c", "d"])
        self.assertEqual(tools._validate(p), "invalid_source_quotes")

    def test_empty_string_rejected(self):
        p = make_payload(source_quotes=[""])
        self.assertEqual(tools._validate(p), "invalid_source_quote")

    def test_whitespace_only_rejected(self):
        p = make_payload(source_quotes=["   "])
        self.assertEqual(tools._validate(p), "invalid_source_quote")

    def test_over_limit_rejected(self):
        p = make_payload(source_quotes=["x" * (tools.SOURCE_QUOTE_MAX + 1)])
        self.assertEqual(tools._validate(p), "invalid_source_quote")

    def test_non_string_elements_rejected(self):
        for bad in (42, {"a": 1}, None):
            p = make_payload(source_quotes=[bad])
            self.assertEqual(tools._validate(p), "invalid_source_quote")

    def test_top_level_non_array_rejected(self):
        for bad in ("text", 42, {"a": 1}, None):
            p = make_payload(source_quotes=bad)
            self.assertEqual(tools._validate(p), "invalid_source_quotes")

    def test_one_bad_item_rejects_whole_report(self):
        payload = {
            "schema_version": "1.0",
            "producer": "test-producer",
            "job_id": "6eabd835f969",
            "run_id": "run-1",
            "report_kind": "news",
            "scheduled_at": "2026-11-01T00:00:00Z",
            "generated_at": "2026-11-01T00:01:00Z",
            "collected_at": "2026-11-01T00:00:30Z",
            "source_ref": "https://example.com/source",
            "source_text": "source text",
            "source_sha256": hashlib.sha256(b"source text").hexdigest(),
            "idempotency_key": "idem-2",
            "items": [
                {
                    "item_id": "ok",
                    "kind": "news",
                    "title": "t",
                    "body": "b",
                    "source_quotes": ["good"],
                },
                {
                    "item_id": "bad",
                    "kind": "news",
                    "title": "t",
                    "body": "b",
                    "source_quotes": [],
                },
            ],
        }
        self.assertEqual(tools._validate(payload), "invalid_source_quotes")

    def test_companion_evidence_still_rejected(self):
        p = make_payload()
        p["companion_evidence"] = {"x": 1}
        self.assertEqual(
            tools._validate(p), "companion_evidence_not_allowed_in_gateway_request"
        )

    def test_boundary_500_passes(self):
        p = make_payload(source_quotes=["x" * tools.SOURCE_QUOTE_MAX])
        self.assertIsNone(tools._validate(p))


if __name__ == "__main__":
    unittest.main()


class HandlerResultContractTests(unittest.TestCase):
    """Hermes' tool registry accepts only a str result (or its multimodal envelope)."""

    def test_rejected_payload_returns_json_string(self):
        import json

        result = tools.handle_submit_report({"payload": {"schema_version": "0.9"}})
        self.assertIsInstance(result, str)
        self.assertEqual(
            {"ok": False, "error": "invalid_schema_version"}, json.loads(result)
        )

    def test_args_without_payload_return_json_string(self):
        import json

        result = tools.handle_submit_report(None)
        self.assertIsInstance(result, str)
        self.assertFalse(json.loads(result)["ok"])


class ProducerPinTests(unittest.TestCase):
    """The Gateway token is bound to producer "hermes"; the model must not choose it."""

    def test_sent_producer_is_pinned(self):
        import json
        import tempfile
        from unittest import mock

        sent = []

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

            def getcode(self):
                return 201

            def read(self):
                return b'{"persisted": true}'

        class Opener:
            def open(self, request, timeout):
                sent.append(json.loads(request.data))
                return Response()

        payload = make_payload()
        payload["producer"] = "hermes-cron-devops-brief"
        with (
            tempfile.TemporaryDirectory() as outbox,
            mock.patch.object(tools, "OUTBOX_DIR", Path(outbox)),
            mock.patch.dict(
                "os.environ",
                {
                    "RESEARCH_WEBHOOK_URL": "https://gateway.invalid/hook",
                    "RESEARCH_WEBHOOK_SECRET": "synthetic",
                },
            ),
            mock.patch.object(
                tools.urllib.request, "build_opener", return_value=Opener()
            ),
        ):
            result = json.loads(tools.handle_submit_report({"payload": payload}))
        self.assertTrue(result["ok"], result)
        self.assertEqual(["hermes"], [body["producer"] for body in sent])
