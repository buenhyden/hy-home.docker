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
    "items": [
        {
            "item_id": "item-1",
            "kind": "news",
            "title": "Example ships version 2.1",
            "body": "Example released version 2.1 of its build tool on 31 October.",
            "source_url": "https://example.com/news/2-1",
        }
    ],
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
                    "body": "Example released version 2.1 of its build tool.",
                    "source_url": "https://example.com/a",
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


class UnknownFieldTests(unittest.TestCase):
    """n8n screens the exact field set; name the stray field instead of a 400."""

    def test_unknown_top_level_field_is_named(self):
        p = make_payload()
        p["kind"] = "devops"
        self.assertEqual(tools._validate(p), "unknown_field:kind")

    def test_unknown_item_field_is_named(self):
        p = make_payload(url="https://example.com")
        self.assertEqual(tools._validate(p), "unknown_item_field:url")

    def test_every_screened_field_still_passes(self):
        p = make_payload(source_url="https://example.com", source_quotes=["q"])
        p["fire_id"] = "fire-1"
        self.assertIsNone(tools._validate(p))


class ItemContentTests(unittest.TestCase):
    """Each item stands for one article: no report titles or filler text."""

    def test_report_title_as_item_title_is_rejected(self):
        p = make_payload(title="DevOps Daily Brief research report")
        self.assertEqual(tools._validate(p), "placeholder_item:item-1")

    def test_filler_body_is_rejected(self):
        p = make_payload(body="Report submitted")
        self.assertEqual(tools._validate(p), "placeholder_item:item-1")

    def test_test_item_title_is_rejected(self):
        p = make_payload(title="test item")
        self.assertEqual(tools._validate(p), "placeholder_item:item-1")

    def test_one_line_body_is_too_short(self):
        p = make_payload(body="Example shipped it.")
        self.assertEqual(tools._validate(p), "body_too_short:item-1")

    def test_quotes_need_the_page_they_came_from(self):
        p = make_payload(source_quotes=["Example released version 2.1."])
        del p["items"][0]["source_url"]
        self.assertEqual(tools._validate(p), "source_url_required_with_quotes:item-1")

    def test_article_item_with_page_and_quote_passes(self):
        p = make_payload(
            source_url="https://example.com/news/2-1",
            source_quotes=["Example released version 2.1 of its build tool."],
        )
        self.assertIsNone(tools._validate(p))


class PlaceholderFalsePositiveTests(unittest.TestCase):
    """Real headlines and summaries that mention the filler words still pass."""

    def test_real_items_mentioning_filler_words_pass(self):
        for title, body in (
            (
                "Gartner forecasts IDP adoption",
                "A new Gartner research report says 40% of platform teams will adopt IDPs by 2027.",
            ),
            (
                "Kubernetes 1.33 release date still TBD",
                "The Kubernetes release team has not yet fixed a date for version 1.33.",
            ),
            (
                "Chrome 131 styles placeholders",
                "Chrome 131 styles the ::placeholder pseudo-element natively in every form field.",
            ),
        ):
            with self.subTest(title=title):
                self.assertIsNone(tools._validate(make_payload(title=title, body=body)))

    def test_non_string_title_or_body_is_named(self):
        self.assertEqual(tools._validate(make_payload(title=["x"])), "invalid_title")
        self.assertEqual(tools._validate(make_payload(body={"x": 1})), "invalid_body")

    def test_blank_source_url_does_not_carry_quotes(self):
        p = make_payload(
            source_url="  ", source_quotes=["Example released version 2.1."]
        )
        self.assertEqual(tools._validate(p), "source_url_required_with_quotes:item-1")


class ToolSchemaTests(unittest.TestCase):
    """The model sees the exact field sets the plugin and n8n accept."""

    def test_payload_schema_lists_exactly_the_accepted_fields(self):
        payload = tools.SUBMIT_RESEARCH_REPORT_SCHEMA["parameters"]["properties"][
            "payload"
        ]
        self.assertFalse(payload["additionalProperties"])
        self.assertEqual(
            set(payload["properties"]), tools._FIELDS - {"companion_evidence"}
        )
        item = payload["properties"]["items"]["items"]
        self.assertFalse(item["additionalProperties"])
        self.assertEqual(set(item["properties"]), tools._ITEM_FIELDS)


if __name__ == "__main__":
    unittest.main()


class HandlerResultContractTests(unittest.TestCase):
    """Hermes' tool registry accepts only a str result (or its multimodal envelope)."""

    def test_rejected_payload_returns_json_string(self):
        import json
        from unittest import mock

        with mock.patch.object(tools, "_CTX", CronRun()):
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


class CronRun:
    """Stands in for Hermes' plugin context during one cron execution."""

    def __init__(self, job_id="25674fbc0bf3", execution_id="0123456789abcdef"):
        from types import SimpleNamespace

        self.run = SimpleNamespace(job_id=job_id, execution_id=execution_id)

    def current_cron_execution(self):
        return self.run


def submit(payload, ctx):
    """Run the handler under ctx with a fake opener; return (result, sent bodies)."""
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

    with (
        tempfile.TemporaryDirectory() as outbox,
        mock.patch.object(tools, "_CTX", ctx),
        mock.patch.object(tools, "OUTBOX_DIR", Path(outbox)),
        mock.patch.dict(
            "os.environ",
            {
                "RESEARCH_WEBHOOK_URL": "https://gateway.invalid/hook",
                "RESEARCH_WEBHOOK_SECRET": "synthetic",
            },
        ),
        mock.patch.object(tools.urllib.request, "build_opener", return_value=Opener()),
    ):
        result = json.loads(tools.handle_submit_report({"payload": payload}))
    return result, sent


class CronIdentityTests(unittest.TestCase):
    """Identity fields come from Hermes and the Gateway token, never from the model."""

    def test_identity_fields_are_taken_from_the_cron_run(self):
        payload = make_payload()
        payload.update(
            producer="hermes-cron-devops-brief",
            job_id="devops-daily-brief",
            report_kind="news",
            run_id="2026-11-01T101627Z",
            idempotency_key="model-chosen",
        )
        result, sent = submit(payload, CronRun())
        self.assertTrue(result["ok"], result)
        self.assertEqual(1, len(sent))
        self.assertEqual("hermes", sent[0]["producer"])
        self.assertEqual("25674fbc0bf3", sent[0]["job_id"])
        self.assertEqual("devops", sent[0]["report_kind"])
        self.assertEqual("0123456789abcdef", sent[0]["run_id"])
        self.assertEqual("25674fbc0bf3-0123456789abcdef", sent[0]["idempotency_key"])

    def test_two_runs_of_one_job_do_not_collide(self):
        _, first = submit(make_payload(), CronRun(execution_id="aaaa"))
        _, second = submit(make_payload(), CronRun(execution_id="bbbb"))
        self.assertNotEqual(first[0]["idempotency_key"], second[0]["idempotency_key"])

    def test_outside_a_cron_run_nothing_is_sent(self):
        for ctx in (None, CronRun(job_id=None)):
            if ctx is not None:
                ctx.run = None
            result, sent = submit(make_payload(), ctx)
            self.assertEqual({"ok": False, "error": "not_a_cron_run"}, result)
            self.assertEqual([], sent)

    def test_a_job_outside_the_allowlist_is_refused(self):
        result, sent = submit(make_payload(), CronRun(job_id="b729b76b4def"))
        self.assertEqual({"ok": False, "error": "job_not_allowed"}, result)
        self.assertEqual([], sent)
