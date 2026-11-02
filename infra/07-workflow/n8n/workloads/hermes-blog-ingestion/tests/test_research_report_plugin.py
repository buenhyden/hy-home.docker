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


class DestinationAuthorityTests(unittest.TestCase):
    """A trusted setting may select only the one reviewed ingress route."""

    def test_only_the_exact_reviewed_webhook_url_is_allowed(self):
        approved = "https://n8n.hy.home.arpa/webhook/hermes-blog-ingestion"
        self.assertEqual(tools.APPROVED_WEBHOOK_URL, approved)
        self.assertTrue(tools._allowed_url(approved))
        for url in (
            "https://n8n.hy.home.arpa/webhook/hermes-blog-ingestion/",
            "https://n8n.hy.home.arpa/webhook/hermes-blog-ingestion?next=1",
            "https://n8n.hy.home.arpa/webhook/hermes-blog-ingestion#fragment",
            "https://user@n8n.hy.home.arpa/webhook/hermes-blog-ingestion",
            "https://n8n.hy.home.arpa:443/webhook/hermes-blog-ingestion",
            "https://other.example/webhook/hermes-blog-ingestion",
            "https://n8n.hy.home.arpa/webhook/other",
            "http://n8n.hy.home.arpa/webhook/hermes-blog-ingestion",
        ):
            with self.subTest(url=url):
                self.assertFalse(tools._allowed_url(url))

    def test_disallowed_url_is_rejected_before_credential_or_network(self):
        import json
        import tempfile
        from unittest import mock

        with (
            tempfile.TemporaryDirectory() as outbox,
            mock.patch.object(tools, "_CTX", CronRun()),
            mock.patch.object(tools, "OUTBOX_DIR", Path(outbox)),
            mock.patch.object(
                tools, "_load_url", return_value="https://other.example/"
            ),
            mock.patch.object(
                tools, "_load_address_policy", return_value="10.250.1.128/32"
            ),
            mock.patch.object(tools, "_load_secret") as secret,
            mock.patch.object(tools.webhook_transport, "post") as post,
        ):
            result = json.loads(tools.handle_submit_report({"payload": make_payload()}))
        self.assertEqual(result, {"ok": False, "error": "disallowed_url"})
        secret.assert_not_called()
        post.assert_not_called()

    def test_oversize_request_is_rejected_before_policy_or_credential(self):
        import json
        from unittest import mock

        payload = make_payload()
        payload["source_text"] = "x" * (tools.webhook_transport.MAX_REQUEST_BYTES + 1)
        payload["source_sha256"] = hashlib.sha256(
            payload["source_text"].encode()
        ).hexdigest()
        with (
            mock.patch.object(tools, "_CTX", CronRun()),
            mock.patch.object(tools, "_load_address_policy") as policy,
            mock.patch.object(tools, "_load_secret") as secret,
            mock.patch.object(tools.webhook_transport, "post") as post,
        ):
            result = json.loads(tools.handle_submit_report({"payload": payload}))
        self.assertEqual(result, {"ok": False, "error": "request_too_large"})
        policy.assert_not_called()
        secret.assert_not_called()
        post.assert_not_called()


class AddressPolicyLoaderTests(unittest.TestCase):
    def test_policy_descriptor_is_closed_when_metadata_read_fails(self):
        from unittest import mock

        with (
            mock.patch.dict("os.environ", {}, clear=True),
            mock.patch.object(tools.os, "open", return_value=77),
            mock.patch.object(tools.os, "fstat", side_effect=OSError("synthetic")),
            mock.patch.object(tools.os, "close") as close,
        ):
            self.assertEqual(tools._load_address_policy(), "")
        close.assert_called_once_with(77)

    def test_policy_file_must_be_owned_regular_and_not_group_writable(self):
        import tempfile
        from unittest import mock

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy"
            policy.write_text("10.250.1.128/32", encoding="utf-8")
            with (
                mock.patch.object(tools, "ADDRESS_POLICY_FILE", policy),
                mock.patch.dict("os.environ", {}, clear=True),
            ):
                self.assertEqual(tools._load_address_policy(), "10.250.1.128/32")
                policy.chmod(0o620)
                self.assertEqual(tools._load_address_policy(), "")
                policy.chmod(0o600)
                policy.unlink()
                policy.symlink_to(root / "missing")
                self.assertEqual(tools._load_address_policy(), "")


class DeliveryBudgetTests(unittest.TestCase):
    def run_delivery(self, side_effect, *, monotonic=None):
        import json
        import tempfile
        from unittest import mock

        with (
            tempfile.TemporaryDirectory() as outbox,
            mock.patch.object(tools, "_CTX", CronRun()),
            mock.patch.object(tools, "OUTBOX_DIR", Path(outbox)),
            mock.patch.object(tools, "_load_url", return_value=approved_url()),
            mock.patch.object(
                tools, "_load_address_policy", return_value="10.250.1.128/32"
            ),
            mock.patch.object(tools, "_load_secret", return_value="synthetic"),
            mock.patch.object(
                tools.webhook_transport, "post", side_effect=side_effect
            ) as post,
            mock.patch.object(tools.time, "sleep") as sleep,
            mock.patch.object(
                tools.time,
                "monotonic",
                side_effect=monotonic,
            )
            if monotonic is not None
            else mock.patch.object(tools.time, "monotonic", return_value=0),
        ):
            result = json.loads(tools.handle_submit_report({"payload": make_payload()}))
        return result, post, sleep

    def test_retryable_transport_failure_uses_three_bounded_attempts(self):
        failure = tools.webhook_transport.TransportFailure("timeout", retryable=True)
        result, post, sleep = self.run_delivery(failure)
        self.assertEqual(result["error"], "delivery_failed")
        self.assertEqual(result["error_type"], "timeout")
        self.assertEqual(post.call_count, 3)
        self.assertEqual(
            [call.kwargs["timeout"] for call in post.call_args_list], [15, 15, 15]
        )
        self.assertEqual(sleep.call_count, 2)

    def test_non_retryable_transport_failure_is_not_replayed(self):
        failure = tools.webhook_transport.TransportFailure("tls")
        result, post, sleep = self.run_delivery(failure)
        self.assertEqual(result["error_type"], "tls")
        post.assert_called_once()
        sleep.assert_not_called()

    def test_retryable_http_status_retries_but_redirect_does_not(self):
        retry = tools.webhook_transport.Response(503, b"{}", "application/json")
        result, post, sleep = self.run_delivery(lambda *_args, **_kwargs: retry)
        self.assertEqual(result["error_type"], "http_503_not_persisted")
        self.assertEqual(post.call_count, 3)
        self.assertEqual(sleep.call_count, 2)

        redirect = tools.webhook_transport.Response(302, b"", "text/plain")
        result, post, sleep = self.run_delivery(lambda *_args, **_kwargs: redirect)
        self.assertEqual(result["error_type"], "http_302_not_persisted")
        post.assert_called_once()
        sleep.assert_not_called()

    def test_invalid_credential_never_starts_transport(self):
        import json
        import tempfile
        from unittest import mock

        with (
            tempfile.TemporaryDirectory() as outbox,
            mock.patch.object(tools, "_CTX", CronRun()),
            mock.patch.object(tools, "OUTBOX_DIR", Path(outbox)),
            mock.patch.object(tools, "_load_url", return_value=approved_url()),
            mock.patch.object(
                tools, "_load_address_policy", return_value="10.250.1.128/32"
            ),
            mock.patch.object(tools, "_load_secret", return_value=""),
            mock.patch.object(tools.webhook_transport, "post") as post,
        ):
            result = json.loads(tools.handle_submit_report({"payload": make_payload()}))
        self.assertEqual(result, {"ok": False, "error": "invalid_credential"})
        post.assert_not_called()

    def test_total_deadline_stops_before_a_second_attempt(self):
        failure = tools.webhook_transport.TransportFailure("timeout", retryable=True)
        result, post, sleep = self.run_delivery(failure, monotonic=[0, 0, 61])
        self.assertEqual(result["error_type"], "timeout")
        post.assert_called_once()
        sleep.assert_not_called()

    def test_missing_address_policy_is_rejected_before_credential_or_network(self):
        import json
        import tempfile
        from unittest import mock

        with (
            tempfile.TemporaryDirectory() as outbox,
            mock.patch.object(tools, "_CTX", CronRun()),
            mock.patch.object(tools, "OUTBOX_DIR", Path(outbox)),
            mock.patch.object(tools, "_load_url", return_value=approved_url()),
            mock.patch.object(tools, "_load_address_policy", return_value=""),
            mock.patch.object(tools, "_load_secret") as secret,
            mock.patch.object(tools.webhook_transport, "post") as post,
        ):
            result = json.loads(tools.handle_submit_report({"payload": make_payload()}))
        self.assertEqual(result, {"ok": False, "error": "missing_address_policy"})
        secret.assert_not_called()
        post.assert_not_called()


class CronRun:
    """Stands in for Hermes' plugin context during one cron execution."""

    def __init__(self, job_id="25674fbc0bf3", execution_id="0123456789abcdef"):
        from types import SimpleNamespace

        self.run = SimpleNamespace(job_id=job_id, execution_id=execution_id)

    def current_cron_execution(self):
        return self.run


def submit(payload, ctx):
    """Run the handler under ctx with a fake transport; return result and bodies."""
    import json
    import tempfile
    from unittest import mock

    sent = []

    def post(url, body, token, policy, *, timeout):
        sent.append(json.loads(body))
        return tools.webhook_transport.Response(
            201, b'{"persisted": true}', "application/json"
        )

    with (
        tempfile.TemporaryDirectory() as outbox,
        mock.patch.object(tools, "_CTX", ctx),
        mock.patch.object(tools, "OUTBOX_DIR", Path(outbox)),
        mock.patch.dict(
            "os.environ",
            {
                "RESEARCH_WEBHOOK_URL": approved_url(),
                "RESEARCH_WEBHOOK_SECRET": "synthetic",
                "RESEARCH_WEBHOOK_ALLOWED_CIDRS": "10.250.1.128/32",
            },
        ),
        mock.patch.object(tools.webhook_transport, "post", side_effect=post),
    ):
        result = json.loads(tools.handle_submit_report({"payload": payload}))
    return result, sent


def approved_url():
    return "https://n8n.hy.home.arpa/webhook/hermes-blog-ingestion"


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
