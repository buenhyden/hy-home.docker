"""Unit tests for research-report plugin source_quotes validation."""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

WORKLOAD = Path(__file__).resolve().parents[1]
PLUGIN_DIR = WORKLOAD / "hermes-plugin"
sys.path.insert(0, str(PLUGIN_DIR))
sys.path.insert(1, str(WORKLOAD))

import tools  # type: ignore  # noqa: E402
from publisher import source_collection  # noqa: E402

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
            "source_quotes": [
                "Example released version 2.1 of its build tool on 31 October."
            ],
        }
    ],
}


def make_payload(**item_overrides):
    payload = copy.deepcopy(BASE_PAYLOAD)
    if item_overrides:
        payload["items"] = [dict(payload["items"][0], **item_overrides)]
    return payload


def submission_args(payload=None):
    """The model supplies content plus one opaque collector receipt per item."""
    payload = payload or make_payload()
    return {
        "payload": {
            "schema_version": payload["schema_version"],
            "items": payload.get("items", []),
        },
        "source_receipts": [
            f"{index + 1:032x}" for index, _ in enumerate(payload.get("items", []))
        ],
    }


def resolved_sources(items):
    return [
        {
            "item_id": entry["item_id"],
            "source_url": entry.get("source_url", "https://example.com/source"),
            "body_sha256": "a" * 64,
            "fetched_at": "2026-11-01T00:00:30.000Z",
            "collection_call_id": f"collector-{index}",
            "text": "source text",
        }
        for index, entry in enumerate(items)
    ]


def resolve_submitted(_root, _job, _run, _scheduled, items, _receipts):
    return resolved_sources(items)


class SourceQuotesValidationTests(unittest.TestCase):
    def test_valid_one_to_three_quotes_passes(self):
        p = make_payload(
            source_quotes=["Sentence one.", "Sentence two.", "Sentence three."]
        )
        self.assertIsNone(tools._validate(p))

    def test_missing_source_quotes_passes(self):
        p = make_payload()
        del p["items"][0]["source_quotes"]
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
        parameters = tools.SUBMIT_RESEARCH_REPORT_SCHEMA["parameters"]
        self.assertFalse(parameters["additionalProperties"])
        self.assertEqual(set(parameters["properties"]), {"payload", "source_receipts"})
        self.assertEqual(set(parameters["required"]), {"payload", "source_receipts"})
        payload = parameters["properties"]["payload"]
        self.assertFalse(payload["additionalProperties"])
        self.assertEqual(set(payload["properties"]), {"schema_version", "items"})
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
            mock.patch.object(
                source_collection, "resolve", side_effect=resolve_submitted
            ),
        ):
            result = json.loads(tools.handle_submit_report(submission_args()))
        self.assertEqual(result, {"ok": False, "error": "disallowed_url"})
        secret.assert_not_called()
        post.assert_not_called()

    def test_oversize_request_is_rejected_before_policy_or_credential(self):
        import json
        from unittest import mock

        payload = make_payload()
        rows = resolved_sources(payload["items"])
        rows[0]["text"] = "x" * (tools.webhook_transport.MAX_REQUEST_BYTES + 1)
        with (
            mock.patch.object(tools, "_CTX", CronRun()),
            mock.patch.object(tools, "_load_address_policy") as policy,
            mock.patch.object(tools, "_load_secret") as secret,
            mock.patch.object(tools.webhook_transport, "post") as post,
            mock.patch.object(source_collection, "resolve", return_value=rows),
        ):
            result = json.loads(tools.handle_submit_report(submission_args(payload)))
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
            mock.patch.object(
                source_collection, "resolve", side_effect=resolve_submitted
            ),
        ):
            result = json.loads(tools.handle_submit_report(submission_args()))
        return result, post, sleep

    def test_preconnect_dns_failure_uses_three_bounded_attempts(self):
        failure = tools.webhook_transport.TransportFailure("dns", retryable=True)
        result, post, sleep = self.run_delivery(failure)
        self.assertEqual(result["error"], "delivery_failed")
        self.assertEqual(result["error_type"], "dns")
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

    def test_http_failure_after_request_is_uncertain_and_not_retried(self):
        retry = tools.webhook_transport.Response(503, b"{}", "application/json")
        result, post, sleep = self.run_delivery(lambda *_args, **_kwargs: retry)
        self.assertEqual(result["error"], "delivery_uncertain")
        post.assert_called_once()
        sleep.assert_not_called()

        redirect = tools.webhook_transport.Response(302, b"", "text/plain")
        result, post, sleep = self.run_delivery(lambda *_args, **_kwargs: redirect)
        self.assertEqual(result["error"], "delivery_uncertain")
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
            mock.patch.object(
                source_collection, "resolve", side_effect=resolve_submitted
            ),
        ):
            result = json.loads(tools.handle_submit_report(submission_args()))
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
            mock.patch.object(
                source_collection, "resolve", side_effect=resolve_submitted
            ),
        ):
            result = json.loads(tools.handle_submit_report(submission_args()))
        self.assertEqual(result, {"ok": False, "error": "missing_address_policy"})
        secret.assert_not_called()
        post.assert_not_called()


class CronRun:
    """Stands in for Hermes' plugin context during one cron execution."""

    def __init__(
        self,
        job_id="25674fbc0bf3",
        execution_id="0123456789abcdef",
        scheduled_instant="2026-11-01T00:00:00Z",
    ):
        from types import SimpleNamespace

        self.run = SimpleNamespace(
            job_id=job_id,
            execution_id=execution_id,
            scheduled_instant=scheduled_instant,
        )

    def current_cron_execution(self):
        return self.run


def submit(payload, ctx):
    """Run the handler under ctx with a fake transport; return result and bodies."""
    sent = []

    def post(url, body, token, policy, *, timeout):
        sent.append(json.loads(body))
        return tools.webhook_transport.Response(
            201,
            json.dumps(
                {
                    "id": "11111111-1111-1111-1111-111111111111",
                    "persisted": True,
                    "duplicate": False,
                    "status": "received",
                    "candidate_count": len(sent[-1]["items"]),
                    "status_url": (
                        "/v1/ingestions/11111111-1111-1111-1111-111111111111"
                    ),
                }
            ).encode(),
            "application/json",
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
        mock.patch.object(source_collection, "resolve", side_effect=resolve_submitted),
    ):
        result = json.loads(tools.handle_submit_report(submission_args(payload)))
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


class P11DirectDeliveryRegressionTests(unittest.TestCase):
    """Direct delivery must retain evidence and fail closed before network I/O."""

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.outbox = Path(temporary.name)
        self.context = CronRun()
        self.environment = {
            "RESEARCH_WEBHOOK_URL": approved_url(),
            "RESEARCH_WEBHOOK_SECRET": "synthetic",
            "RESEARCH_WEBHOOK_ALLOWED_CIDRS": "10.250.1.128/32",
        }

    @staticmethod
    def receipt(*, duplicate=False, status_url=None):
        report_id = "11111111-1111-1111-1111-111111111111"
        return tools.webhook_transport.Response(
            200 if duplicate else 201,
            json.dumps(
                {
                    "id": report_id,
                    "persisted": True,
                    "duplicate": duplicate,
                    "status": "received",
                    "candidate_count": 1,
                    "status_url": status_url or f"/v1/ingestions/{report_id}",
                }
            ).encode(),
            "application/json",
        )

    def run_submit(self, post, *, context=None):
        with (
            mock.patch.object(tools, "_CTX", context or self.context),
            mock.patch.object(tools, "OUTBOX_DIR", self.outbox),
            mock.patch.dict("os.environ", self.environment, clear=False),
            mock.patch.object(tools.webhook_transport, "post", side_effect=post),
            mock.patch.object(tools.time, "sleep"),
            mock.patch.object(
                source_collection, "resolve", side_effect=resolve_submitted
            ),
        ):
            return json.loads(tools.handle_submit_report(submission_args()))

    def test_scheduled_instant_is_required_before_network(self):
        post = mock.Mock(return_value=self.receipt())
        result = self.run_submit(post, context=CronRun(scheduled_instant=None))
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "scheduled_instant_required")
        post.assert_not_called()

    def test_mismatched_receipt_status_url_is_not_persisted(self):
        post = mock.Mock(
            return_value=self.receipt(
                status_url="/v1/ingestions/22222222-2222-2222-2222-222222222222"
            )
        )
        result = self.run_submit(post)
        self.assertFalse(result["ok"])
        self.assertNotEqual(result.get("status"), "persisted")

    def test_malformed_uuid_receipt_is_rejected_but_real_uuid_is_accepted(self):
        malformed_id = "-" * 36
        malformed = self.receipt(status_url=f"/v1/ingestions/{malformed_id}")
        body = json.loads(malformed.body)
        body["id"] = malformed_id
        malformed = tools.webhook_transport.Response(
            malformed.status,
            json.dumps(body).encode(),
            malformed.content_type,
        )
        rejected = self.run_submit(mock.Mock(return_value=malformed))
        with tempfile.TemporaryDirectory() as accepted_outbox:
            self.outbox = Path(accepted_outbox)
            accepted = self.run_submit(mock.Mock(return_value=self.receipt()))
        self.assertEqual(rejected["error"], "delivery_uncertain")
        self.assertTrue(accepted["ok"], accepted)
        self.assertEqual(
            accepted["response"]["id"],
            "11111111-1111-1111-1111-111111111111",
        )

    def test_corrupt_existing_state_blocks_resend(self):
        key = "25674fbc0bf3:25674fbc0bf3-0123456789abcdef"
        record = self.outbox / f"{key}.json"
        record.write_text("{", encoding="utf-8")
        record.chmod(0o600)
        post = mock.Mock(return_value=self.receipt())
        result = self.run_submit(post)
        self.assertFalse(result["ok"])
        self.assertIn(
            result["error"],
            {"state_corrupt", "outbox_corrupt", "record_unverifiable"},
        )
        post.assert_not_called()

    def test_retry_budget_is_cumulative_across_invocations(self):
        failure = tools.webhook_transport.TransportFailure("dns", retryable=True)
        post = mock.Mock(side_effect=failure)
        first = self.run_submit(post)
        second = self.run_submit(post)
        self.assertFalse(first["ok"])
        self.assertFalse(second["ok"])
        self.assertEqual(post.call_count, 3)

    def test_concurrent_same_key_uses_one_durable_submission(self):
        results = []
        failures = []
        post = mock.Mock(return_value=self.receipt())

        def invoke():
            try:
                results.append(
                    json.loads(tools.handle_submit_report(submission_args()))
                )
            except BaseException as exc:  # collected for an explicit assertion
                failures.append(exc)

        with (
            mock.patch.object(tools, "_CTX", self.context),
            mock.patch.object(tools, "OUTBOX_DIR", self.outbox),
            mock.patch.dict("os.environ", self.environment, clear=False),
            mock.patch.object(tools.webhook_transport, "post", side_effect=post),
            mock.patch.object(tools.time, "sleep"),
            mock.patch.object(
                source_collection, "resolve", side_effect=resolve_submitted
            ),
        ):
            threads = [threading.Thread(target=invoke) for _ in range(2)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(timeout=5)

        self.assertEqual(failures, [])
        self.assertEqual(len(results), 2)
        self.assertTrue(all(result["ok"] for result in results), results)
        self.assertEqual(post.call_count, 1)

    def test_ambiguous_transport_failure_is_not_replayed_on_restart(self):
        failure = tools.webhook_transport.TransportFailure("timeout", retryable=True)
        post = mock.Mock(side_effect=failure)
        first = self.run_submit(post)
        second = self.run_submit(post)
        self.assertEqual(first["error"], "delivery_uncertain")
        self.assertEqual(second["error"], "delivery_uncertain")
        post.assert_called_once()

    def test_missing_receipts_are_rejected_before_network(self):
        post = mock.Mock(return_value=self.receipt())
        with (
            mock.patch.object(tools, "_CTX", self.context),
            mock.patch.object(tools.webhook_transport, "post", post),
        ):
            result = json.loads(
                tools.handle_submit_report(
                    {
                        "payload": {
                            "schema_version": "1.0",
                            "items": make_payload()["items"],
                        }
                    }
                )
            )
        self.assertEqual(result, {"ok": False, "error": "source_receipts_required"})
        post.assert_not_called()

    def test_invalid_receipt_id_is_rejected_before_lookup_or_network(self):
        args = submission_args()
        args["source_receipts"] = ["not-a-collector-receipt"]
        post = mock.Mock(return_value=self.receipt())
        with (
            mock.patch.object(tools, "_CTX", self.context),
            mock.patch.object(source_collection, "resolve") as resolve,
            mock.patch.object(tools.webhook_transport, "post", post),
        ):
            result = json.loads(tools.handle_submit_report(args))
        self.assertEqual(result, {"ok": False, "error": "invalid_source_receipts"})
        resolve.assert_not_called()
        post.assert_not_called()

    def test_item_without_source_quote_is_rejected_before_receipt_lookup(self):
        payload = make_payload()
        del payload["items"][0]["source_quotes"]
        with (
            mock.patch.object(tools, "_CTX", self.context),
            mock.patch.object(source_collection, "resolve") as resolve,
        ):
            result = json.loads(tools.handle_submit_report(submission_args(payload)))
        self.assertEqual(result, {"ok": False, "error": "source_receipts_required"})
        resolve.assert_not_called()

    def test_duplicate_json_key_in_gateway_receipt_is_uncertain(self):
        body = (
            b'{"id":"11111111-1111-1111-1111-111111111111",'
            b'"persisted":true,"persisted":true,"duplicate":false,'
            b'"status":"received","candidate_count":1,'
            b'"status_url":"/v1/ingestions/11111111-1111-1111-1111-111111111111"}'
        )
        response = tools.webhook_transport.Response(201, body, "application/json")
        result = self.run_submit(mock.Mock(return_value=response))
        self.assertEqual(result["error"], "delivery_uncertain")

    def test_forged_persisted_payload_is_blocked_without_rewrite_or_resend(self):
        failure = tools.webhook_transport.TransportFailure("timeout", retryable=True)
        first = self.run_submit(mock.Mock(side_effect=failure))
        self.assertEqual(first["error"], "delivery_uncertain")
        record_path = next(self.outbox.glob("*.json"))
        record = json.loads(record_path.read_bytes())
        payload = json.loads(base64.b64decode(record["payload_b64"]))
        payload["items"][0]["title"] = "Forged title with unchanged input digest"
        forged = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode()
        record["payload_b64"] = base64.b64encode(forged).decode("ascii")
        record["payload_sha256"] = hashlib.sha256(forged).hexdigest()
        tampered_bytes = json.dumps(
            record,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode()
        record_path.write_bytes(tampered_bytes)
        post = mock.Mock(return_value=self.receipt())
        result = self.run_submit(post)
        self.assertEqual(result, {"ok": False, "error": "record_unverifiable"})
        post.assert_not_called()
        self.assertEqual(record_path.read_bytes(), tampered_bytes)


class P11CollectionToolTests(unittest.TestCase):
    def test_missing_schedule_is_rejected_before_fetch(self):
        collect = mock.Mock()
        with (
            mock.patch.object(tools, "_CTX", CronRun(scheduled_instant=None)),
            mock.patch.object(source_collection, "collect", collect),
        ):
            result = json.loads(
                tools.handle_collect_source(
                    {"item_id": "item-1", "source_url": "https://example.org/a"}
                )
            )
        self.assertEqual(result, {"ok": False, "error": "scheduled_instant_required"})
        collect.assert_not_called()

    def test_collector_generated_identity_is_returned_without_platform_call_id(self):
        expected = {
            "ok": True,
            "receipt_id": "receipt-1",
            "collection_call_id": "collector-generated-1",
            "normalized_text": "untrusted page text",
        }
        with (
            tempfile.TemporaryDirectory() as source_dir,
            mock.patch.object(tools, "_CTX", CronRun()),
            mock.patch.object(tools, "SOURCE_DIR", Path(source_dir)),
            mock.patch.object(
                source_collection, "collect", return_value=expected
            ) as collect,
        ):
            result = json.loads(
                tools.handle_collect_source(
                    {"item_id": "item-1", "source_url": "https://example.org/a"}
                )
            )
        self.assertEqual(result, expected)
        self.assertNotIn("call_id", result)
        self.assertEqual(
            collect.call_args.args[1:3], ("25674fbc0bf3", "0123456789abcdef")
        )

    def test_invalid_schedule_and_unknown_fields_fail_before_collection(self):
        for context, args, code in (
            (
                CronRun(scheduled_instant="not-a-time"),
                {"item_id": "item-1", "source_url": "https://example.org/a"},
                "invalid_scheduled_instant",
            ),
            (
                CronRun(),
                {
                    "item_id": "item-1",
                    "source_url": "https://example.org/a",
                    "extra": True,
                },
                "invalid_source_request",
            ),
        ):
            with (
                self.subTest(code=code),
                mock.patch.object(tools, "_CTX", context),
                mock.patch.object(source_collection, "collect") as collect,
            ):
                result = json.loads(tools.handle_collect_source(args))
            self.assertEqual(result, {"ok": False, "error": code})
            collect.assert_not_called()

    def test_expected_collection_limit_is_reported_without_detail_leak(self):
        with (
            mock.patch.object(tools, "_CTX", CronRun()),
            mock.patch.object(
                source_collection,
                "collect",
                side_effect=ValueError("source_item_limit"),
            ),
        ):
            result = json.loads(
                tools.handle_collect_source(
                    {"item_id": "item-101", "source_url": "https://example.org/a"}
                )
            )
        self.assertEqual(result, {"ok": False, "error": "source_item_limit"})

        with (
            mock.patch.object(tools, "_CTX", CronRun()),
            mock.patch.object(
                source_collection,
                "collect",
                side_effect=RuntimeError("synthetic secret detail"),
            ),
        ):
            result = json.loads(
                tools.handle_collect_source(
                    {"item_id": "item-1", "source_url": "https://example.org/a"}
                )
            )
        self.assertEqual(result, {"ok": False, "error": "source_unavailable"})
        self.assertNotIn("secret", json.dumps(result))

    def test_collect_then_submit_uses_the_persisted_receipt(self):
        sentence = "Example released version 2.1 of its build tool on 31 October."
        body = f"<html><body><p>{sentence}</p></body></html>".encode()
        fetch_result = source_collection.source_fetch.FetchResult(
            final_url="https://example.org/article",
            status=200,
            sha256=hashlib.sha256(body).hexdigest(),
            fetched_at="2026-11-01T00:00:30.000Z",
            content_type="text/html; charset=utf-8",
            body=body,
        )
        item = {
            "item_id": "item-1",
            "kind": "news",
            "title": "Example ships version 2.1",
            "body": sentence,
            "source_url": "https://example.org/article",
            "source_quotes": [sentence],
        }
        report_id = "11111111-1111-1111-1111-111111111111"
        response = tools.webhook_transport.Response(
            201,
            json.dumps(
                {
                    "id": report_id,
                    "persisted": True,
                    "duplicate": False,
                    "status": "received",
                    "candidate_count": 1,
                    "status_url": f"/v1/ingestions/{report_id}",
                }
            ).encode(),
            "application/json",
        )
        context = CronRun()
        with (
            tempfile.TemporaryDirectory() as source_dir,
            tempfile.TemporaryDirectory() as outbox,
            mock.patch.object(tools, "_CTX", context),
            mock.patch.object(tools, "SOURCE_DIR", Path(source_dir)),
            mock.patch.object(tools, "OUTBOX_DIR", Path(outbox)),
            mock.patch.dict(
                "os.environ",
                {
                    "RESEARCH_WEBHOOK_URL": approved_url(),
                    "RESEARCH_WEBHOOK_SECRET": "synthetic",
                    "RESEARCH_WEBHOOK_ALLOWED_CIDRS": "10.250.1.128/32",
                },
                clear=False,
            ),
            mock.patch.object(
                source_collection.source_fetch, "fetch", return_value=fetch_result
            ) as fetch,
            mock.patch.object(
                tools.webhook_transport, "post", return_value=response
            ) as post,
        ):
            collected = json.loads(
                tools.handle_collect_source(
                    {
                        "item_id": "item-1",
                        "source_url": "https://example.org/article",
                    }
                )
            )
            result = json.loads(
                tools.handle_submit_report(
                    {
                        "payload": {"schema_version": "1.0", "items": [item]},
                        "source_receipts": [collected["receipt_id"]],
                    }
                )
            )
        self.assertTrue(collected["ok"], collected)
        self.assertEqual(collected["normalized_text"], sentence)
        self.assertNotEqual(collected["receipt_id"], collected["collection_call_id"])
        self.assertEqual(result["status"], "persisted")
        fetch.assert_called_once_with("https://example.org/article")
        post.assert_called_once()

    def test_content_encoding_fetch_failure_is_returned_as_a_fixed_error(self):
        failure = source_collection.source_fetch.FetchFailure("content_encoding")
        with (
            tempfile.TemporaryDirectory() as source_dir,
            mock.patch.object(tools, "_CTX", CronRun()),
            mock.patch.object(tools, "SOURCE_DIR", Path(source_dir)),
            mock.patch.object(
                source_collection.source_fetch, "fetch", side_effect=failure
            ) as fetch,
        ):
            result = json.loads(
                tools.handle_collect_source(
                    {
                        "item_id": "item-1",
                        "source_url": "https://example.org/article",
                    }
                )
            )
        self.assertEqual(result, {"ok": False, "error": "content_encoding"})
        fetch.assert_called_once_with("https://example.org/article")
