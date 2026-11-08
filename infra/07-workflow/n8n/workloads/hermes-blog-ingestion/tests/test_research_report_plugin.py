"""Unit tests for research-report plugin source_quotes validation."""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import os
import re
import stat
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


REPORT = (
    "# DevOps Daily Brief\n\n"
    "Example released version 2.1 of its build tool on 31 October.\n\n"
    "- [Release notes](https://example.com/news/2-1)\n\n"
    "## Notes\n\n"
    + "The release changes the default cache layout and documents the migration "
    "steps for existing projects in its upgrade guide.\n" * 7
)
_REPORT_ROOT = None


def setUpModule():
    """No test may reach the real Hermes report store under the home directory."""
    global _REPORT_ROOT
    _REPORT_ROOT = tempfile.TemporaryDirectory()
    root = Path(_REPORT_ROOT.name)
    # Nor the node-exporter textfile directory or the metrics state (SPEC-0265 W5).
    # Report files live in mktemp -d shaped directories under a private temp root.
    temp_root = root / "temp"
    temp_root.mkdir(mode=0o700)
    patcher = mock.patch.object(tempfile, "gettempdir", return_value=str(temp_root))
    patcher.start()
    unittest.addModuleCleanup(patcher.stop)
    for name, value in (
        ("REPORT_DIR", root / "r"),
        ("METRICS_DIR", root / "no-metrics-dir"),
        ("METRICS_STATE_DIR", root / "metrics-state"),
    ):
        patcher = mock.patch.object(tools, name, value)
        patcher.start()
        unittest.addModuleCleanup(patcher.stop)
    unittest.addModuleCleanup(_REPORT_ROOT.cleanup)


def make_payload(**item_overrides):
    payload = copy.deepcopy(BASE_PAYLOAD)
    if item_overrides:
        payload["items"] = [dict(payload["items"][0], **item_overrides)]
    return payload


def report_file(text=REPORT, *, raw=None, name="report.md"):
    """Write the report as the agent does: a new mktemp -d directory, mode 0700."""
    directory = Path(tempfile.gettempdir()) / f"tmp.{os.urandom(6).hex()}"
    directory.mkdir()
    directory.chmod(0o700)  # umask-independent
    path = directory / name
    path.write_bytes(text.encode("utf-8") if raw is None else raw)
    path.chmod(0o600)
    return str(path)


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
        "report_path": report_file(),
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
        arguments = {"payload", "source_receipts", "report_path"}
        self.assertEqual(set(parameters["properties"]), arguments)
        self.assertEqual(set(parameters["required"]), arguments)
        self.assertEqual(tools.SUBMIT_CONTRACT_VERSION, 3)
        description = tools.SUBMIT_RESEARCH_REPORT_SCHEMA["description"]
        self.assertIn("Contract v3", description)
        self.assertIn("mktemp -d", description)
        self.assertNotIn("report_markdown", description)
        self.assertEqual(parameters["properties"]["report_path"]["type"], "string")
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

        with mock.patch.object(tools, "_CTX", CronRun(execution_id="schema-09")):
            result = tools.handle_submit_report(
                {"payload": {"schema_version": "0.9"}, "report_path": report_file()}
            )
        self.assertIsInstance(result, str)
        result = json.loads(result)
        result.pop("report")  # the report is stored before the Gateway checks
        self.assertEqual({"ok": False, "error": "invalid_schema_version"}, result)

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
        result.pop("report")  # stored before delivery; the agent still sends it
        self.assertEqual(result, {"ok": False, "error": "disallowed_url"})
        secret.assert_not_called()
        post.assert_not_called()

    def test_oversize_request_is_rejected_before_policy_or_credential(self):
        # Within the code point limit, but three UTF-8 bytes each: over 1 MiB.
        for report in (
            "x" * (tools.GATEWAY_MAX_SOURCE_CHARACTERS + 1),
            "\u20ac" * tools.GATEWAY_MAX_SOURCE_CHARACTERS,
        ):
            args = submission_args()
            args["report_path"] = report_file(report)
            with (
                self.subTest(characters=len(report)),
                mock.patch.object(tools, "_CTX", CronRun(execution_id="oversize")),
                mock.patch.object(tools, "_load_address_policy") as policy,
                mock.patch.object(tools, "_load_secret") as secret,
                mock.patch.object(tools.webhook_transport, "post") as post,
                mock.patch.object(
                    source_collection, "resolve", side_effect=resolve_submitted
                ),
            ):
                result = json.loads(tools.handle_submit_report(args))
            self.assertEqual(
                result, {"ok": False, "error": "request_too_large", "state": "BLOCKED"}
            )
            policy.assert_not_called()
            secret.assert_not_called()
            post.assert_not_called()
            self.assertFalse((tools.REPORT_DIR / "25674fbc0bf3-oversize").exists())


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
            policy.chmod(0o600)  # independent of the host umask
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
        result.pop("report")
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
        result.pop("report")
        self.assertEqual(result, {"ok": False, "error": "missing_address_policy"})
        secret.assert_not_called()
        post.assert_not_called()

    def test_source_quality_lists_failed_items_and_allows_one_resubmission(self):
        import json
        import tempfile
        from unittest import mock

        failures = [
            {"item_id": "kubernetes-1-33-release", "codes": ["number_not_found"]}
        ]
        refused = source_collection.SourceQuality(failures)
        with (
            tempfile.TemporaryDirectory() as outbox,
            mock.patch.object(tools, "_CTX", CronRun(execution_id="quality-retry-1")),
            mock.patch.object(tools, "OUTBOX_DIR", Path(outbox)),
            mock.patch.object(tools.webhook_transport, "post") as post,
            mock.patch.object(source_collection, "resolve", side_effect=refused),
        ):
            args = submission_args()
            first = json.loads(tools.handle_submit_report(args))
            self.assertEqual(list(Path(outbox).iterdir()), [])
            post.assert_not_called()
            # Every failing item was dropped: the same report file goes again, empty.
            again = copy.deepcopy(args)
            again["payload"]["items"], again["source_receipts"] = [], []
            second = json.loads(tools.handle_submit_report(again))
        self.assertEqual(first["error"], "source_quality")
        self.assertEqual(first["failed_items"], failures)
        self.assertTrue(second["ok"])
        self.assertEqual(second["gateway"], "skipped_no_items")
        self.assertEqual(second["report"], first["report"])

    def test_resubmission_with_surviving_items_sends_them_once(self):
        payload = make_payload()
        kept = payload["items"][0]
        dropped = dict(kept, item_id="dropped-item-1")
        failures = [{"item_id": "dropped-item-1", "codes": ["quote_not_found"]}]
        ctx = CronRun(execution_id="quality-retry-2")
        with (
            tempfile.TemporaryDirectory() as outbox,
            mock.patch.object(tools, "_CTX", ctx),
            mock.patch.object(tools, "OUTBOX_DIR", Path(outbox)),
            mock.patch.object(
                source_collection,
                "resolve",
                side_effect=source_collection.SourceQuality(failures),
            ),
        ):
            args = submission_args({**payload, "items": [dropped, kept]})
            first = json.loads(tools.handle_submit_report(args))
        self.assertEqual(first["failed_items"], failures)
        self.assertFalse(
            Path(first["report"]["report_path"]).with_name("source-set.json").exists()
        )
        second, sent = submit(payload, ctx, report_path=args["report_path"])
        self.assertTrue(second["ok"], second)
        self.assertEqual(
            [body["items"][0]["item_id"] for body in sent], [kept["item_id"]]
        )
        self.assertEqual(second["report"], first["report"])


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


def submit(payload, ctx, report_path=None):
    """Run the handler under ctx with a fake transport; return result and bodies."""
    sent = []
    args = submission_args(payload)
    if report_path is not None:
        args["report_path"] = report_path

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
        result = json.loads(tools.handle_submit_report(args))
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
                        },
                        "report_path": report_file(),
                    }
                )
            )
        result.pop("report")
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
        result.pop("report")
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
        result.pop("report")
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
        result.pop("report")
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
            mock.patch.object(tools, "REPORT_DIR", Path(outbox) / "reports"),
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
                        "report_path": report_file(
                            REPORT + "\nhttps://example.org/article\n"
                        ),
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


class ReportSourceContractTests(unittest.TestCase):
    """SPEC-0265: source_text is the stored report; outputs derive from its bytes."""

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.context = CronRun()
        self.directory = self.root / "reports" / "25674fbc0bf3-0123456789abcdef"
        self.sent = []

    def post(self, url, body, token, policy, *, timeout):
        self.sent.append(body)
        return P11DirectDeliveryRegressionTests.receipt()

    def run_submit(self, args):
        with (
            mock.patch.object(tools, "_CTX", self.context),
            mock.patch.object(tools, "OUTBOX_DIR", self.root / "outbox"),
            mock.patch.object(tools, "REPORT_DIR", self.root / "reports"),
            mock.patch.dict(
                "os.environ",
                {
                    "RESEARCH_WEBHOOK_URL": approved_url(),
                    "RESEARCH_WEBHOOK_SECRET": "synthetic",
                    "RESEARCH_WEBHOOK_ALLOWED_CIDRS": "10.250.1.128/32",
                },
            ),
            mock.patch.object(tools.webhook_transport, "post", side_effect=self.post),
            mock.patch.object(
                source_collection, "resolve", side_effect=resolve_submitted
            ),
        ):
            return json.loads(tools.handle_submit_report(args))

    def with_report(self, report):
        args = submission_args()
        args["report_path"] = report_file(report)
        return args

    def test_request_validates_against_the_unchanged_ingestion_schema(self):
        import jsonschema

        schema = json.loads(
            (WORKLOAD / "tests/fixtures/ingestion-v1.schema.json").read_bytes()
        )
        result = self.run_submit(submission_args())
        self.assertTrue(result["ok"], result)
        (body,) = self.sent
        request = json.loads(body)
        self.assertEqual(set(request), set(schema["properties"]) - {"fire_id"})
        self.assertIn("source_quotes", request["items"][0])
        jsonschema.validate(request, schema, format_checker=jsonschema.FormatChecker())

    def test_source_text_is_the_stored_report_bytes(self):
        report = "# Brief\r\n\r\nCafé résumé — kept byte for byte.\n\n\n" + REPORT
        args = self.with_report(report)
        result = self.run_submit(args)
        self.assertTrue(result["ok"], result)
        stored = (self.directory / "report.md").read_bytes()
        request = json.loads(self.sent[0])
        self.assertEqual(stored, report.encode("utf-8"))
        # The agent's file is read, never moved, changed or removed.
        self.assertEqual(Path(args["report_path"]).read_bytes(), stored)
        self.assertEqual(request["source_text"], stored.decode("utf-8"))
        self.assertEqual(request["source_sha256"], hashlib.sha256(stored).hexdigest())
        self.assertEqual(result["report"]["report_sha256"], request["source_sha256"])
        self.assertEqual(result["report"]["contract_version"], 3)

    def test_source_ref_digest_is_the_private_receipt_set_record(self):
        result = self.run_submit(submission_args())
        self.assertTrue(result["ok"], result)
        record = self.directory / "source-set.json"
        raw = record.read_bytes()
        expected = json.dumps(
            resolved_sources(make_payload()["items"]),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.assertEqual(raw, expected)
        self.assertEqual(
            json.loads(self.sent[0])["source_ref"],
            "hermes-source-set:" + hashlib.sha256(raw).hexdigest(),
        )
        self.assertEqual(stat.S_IMODE(record.stat().st_mode), 0o600)

    def test_report_store_is_private_bound_and_written_once(self):
        first = self.run_submit(submission_args())
        self.assertTrue(first["ok"], first)
        self.assertEqual(stat.S_IMODE(self.directory.stat().st_mode), 0o700)
        names = {"report.md", "source-set.json", "email.html", "telegram.txt"}
        names.add("manifest.json")
        files = [p for p in self.directory.iterdir() if not p.name.startswith(".")]
        self.assertEqual({p.name for p in files}, names)
        for path in files:
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600, path.name)
        manifest = json.loads((self.directory / "manifest.json").read_bytes())
        self.assertEqual(
            (manifest["job_id"], manifest["execution_id"], manifest["scheduled_at"]),
            ("25674fbc0bf3", "0123456789abcdef", "2026-11-01T00:00:00.000Z"),
        )
        before = {p.name: p.read_bytes() for p in self.directory.iterdir()}

        replay = self.run_submit(submission_args())
        self.assertTrue(replay["ok"], replay)
        self.assertEqual(replay["status"], "already_persisted")
        self.assertEqual(replay["report"], first["report"])

        changed = self.run_submit(self.with_report(REPORT + "\nA later edit.\n"))
        self.assertEqual(
            changed,
            {"ok": False, "error": "report_conflict", "report": first["report"]},
        )
        self.assertEqual(
            {p.name: p.read_bytes() for p in self.directory.iterdir()}, before
        )
        self.assertEqual(len(self.sent), 1)

    def test_gateway_email_and_telegram_share_one_stored_digest(self):
        result = self.run_submit(submission_args())
        self.assertTrue(result["ok"], result)
        files = result["report"]
        stored = Path(files["report_path"]).read_bytes()
        digest = hashlib.sha256(stored).hexdigest()
        email = Path(files["email_path"]).read_text(encoding="utf-8")
        telegram = Path(files["telegram_path"]).read_text(encoding="utf-8")
        manifest = json.loads((self.directory / "manifest.json").read_bytes())
        self.assertEqual(json.loads(self.sent[0])["source_sha256"], digest)
        self.assertEqual(files["report_sha256"], digest)
        self.assertEqual(manifest["report_sha256"], digest)
        self.assertIn(f'<meta name="report-sha256" content="{digest}">', email)
        self.assertEqual(email, tools.render_email(stored.decode("utf-8"), digest))
        self.assertEqual(telegram, tools.render_telegram(stored.decode("utf-8")))
        for name, text in (("email.html", email), ("telegram.txt", telegram)):
            output = manifest["outputs"][name]
            self.assertEqual(output["derived_from_sha256"], digest)
            self.assertEqual(
                output["sha256"], hashlib.sha256(text.encode()).hexdigest()
            )

    def test_invalid_or_unfinished_reports_are_blocked_without_network(self):
        cases = (
            ("", "report_required"),
            ("  \n\t", "report_required"),
            ("TBD", "report_not_final"),
            ("placeholder", "report_not_final"),
            ("# Brief\n\nsoon", "report_not_final"),
            ("nul \x00 byte " + "x" * 40, "report_malformed"),
            ("escape \x1b[31m red " + "x" * 40, "report_malformed"),
            ("override \u202e txt.exe " + "x" * 40, "report_bidi_control"),
            ("isolate \u2066 text \u2069 " + "x" * 40, "report_bidi_control"),
            ("x" * (tools.GATEWAY_MAX_SOURCE_CHARACTERS + 1), "request_too_large"),
            ("\u20ac" * tools.GATEWAY_MAX_SOURCE_CHARACTERS, "request_too_large"),
        )
        for report, code in cases:
            args = submission_args()
            args["report_path"] = report_file(report)
            with self.subTest(code=code, report=repr(report)[:30]):
                result = self.run_submit(args)
                self.assertEqual(
                    result, {"ok": False, "error": code, "state": "BLOCKED"}
                )
        self.assertEqual(self.sent, [])
        self.assertFalse((self.root / "reports").exists())

    def test_extra_argument_is_rejected_without_network(self):
        for extra in ("source_text", "source_sha256", "email_html", "report_markdown"):
            args = submission_args()
            args[extra] = "model supplied"
            with self.subTest(extra=extra):
                result = self.run_submit(args)
                self.assertEqual(
                    result, {"ok": False, "error": "invalid_submission_fields"}
                )
        self.assertEqual(self.sent, [])

    def test_renderers_escape_and_flatten_markdown(self):
        markdown = (
            "# Title <b>\n\nLine one & two\nline <script>x</script>\n\n"
            "- [Docs](https://example.com/a?b=1&c=2)\n* plain item\n"
        )
        email = tools.render_email(markdown, "a" * 64)
        self.assertIn("<h1>Title &lt;b&gt;</h1>", email)
        self.assertIn("<p>Line one &amp; two<br>\nline &lt;script&gt;", email)
        self.assertIn("<li>Docs (https://example.com/a?b=1&amp;c=2)</li>", email)
        self.assertNotIn("<script>", email)
        self.assertNotIn("<a ", email)
        self.assertEqual(
            tools.render_telegram(markdown),
            "Title <b>\n\nLine one & two\nline <script>x</script>\n\n"
            "• Docs (https://example.com/a?b=1&c=2)\n• plain item\n",
        )

    def test_zero_width_joiner_is_allowed(self):
        report = "Family \U0001f468\u200d\U0001f469 emoji keeps its joiner. " + REPORT
        result = self.run_submit(self.with_report(report))
        self.assertTrue(result["ok"], result)

    def test_day_without_items_stores_and_renders_but_sends_nothing(self):
        args = submission_args()
        args["payload"]["items"] = []
        args["source_receipts"] = []
        result = self.run_submit(args)
        self.assertEqual(
            {k: v for k, v in result.items() if k != "report"},
            {"ok": True, "status": "stored", "gateway": "skipped_no_items"},
        )
        self.assertEqual(self.sent, [])
        self.assertEqual(Path(result["report"]["report_path"]).read_text(), REPORT)
        self.assertEqual(
            Path(result["report"]["telegram_path"]).read_text(),
            tools.render_telegram(REPORT),
        )
        manifest = json.loads((self.directory / "manifest.json").read_bytes())
        self.assertNotIn("gateway", manifest)
        self.assertFalse((self.directory / "source-set.json").exists())
        self.assertFalse((self.root / "outbox").exists())

    def test_gateway_side_failure_still_returns_the_stored_files(self):
        args = submission_args()
        args["source_receipts"] = ["not-a-collector-receipt"]
        result = self.run_submit(args)
        self.assertEqual(result["error"], "invalid_source_receipts")
        self.assertTrue(Path(result["report"]["email_path"]).is_file())
        self.assertEqual(self.sent, [])

    def test_replay_returns_stored_outputs_without_rerendering(self):
        first = self.run_submit(submission_args())
        email = Path(first["report"]["email_path"]).read_bytes()
        with (
            mock.patch.object(tools, "render_email", side_effect=AssertionError),
            mock.patch.object(tools, "render_telegram", return_value="changed\n"),
        ):
            replay = self.run_submit(submission_args())
        self.assertTrue(replay["ok"], replay)
        self.assertEqual(replay["report"], first["report"])
        self.assertEqual(Path(first["report"]["email_path"]).read_bytes(), email)

    def test_interrupted_create_leaving_a_second_link_recovers(self):
        self.directory.mkdir(parents=True, mode=0o700)
        self.directory.parent.chmod(0o700)
        self.directory.chmod(0o700)
        report = self.directory / "report.md"
        report.write_bytes(REPORT.encode())
        report.chmod(0o600)
        os.link(report, self.directory / ".tmp-0123456789abcdef")
        self.assertEqual(report.stat().st_nlink, 2)
        result = self.run_submit(submission_args())
        self.assertTrue(result["ok"], result)
        self.assertEqual(report.stat().st_nlink, 1)
        self.assertFalse((self.directory / ".tmp-0123456789abcdef").exists())
        self.assertTrue((self.directory / "email.html").is_file())

    def test_placeholder_check_is_linear_on_long_reports(self):
        import time

        n = 250_000
        for text in (
            "lorem ipsum" + "!" * n + "\n" + "!" * n + "a",
            "placeholder" + "!" * n + "a",
        ):
            with self.subTest(text=text[:11]):
                started = time.monotonic()
                tools._report_error(text)
                self.assertLess(time.monotonic() - started, 2.0)
        self.assertEqual(
            tools._report_error("Lorem ipsum dolor sit amet,\nconsectetur " * 3),
            "report_not_final",
        )

    def test_pathological_lines_render_in_linear_time(self):
        import time

        n = 200_000
        for line in (
            "[" * n,
            "[a](" + "b" * n,
            "# a" + "#" * n + "b",
            "# a" + " " * n + "b",
            "- a" + " " * n + "b",
            "[" + " " * n + "](",
        ):
            with self.subTest(line=line[:8]):
                started = time.monotonic()
                tools.render_email(line, "a" * 64)
                tools.render_telegram(line)
                self.assertLess(time.monotonic() - started, 2.0)


class ReportPathTests(unittest.TestCase):
    """Contract v3: the report comes from one private mktemp -d file, then checks."""

    setUp = ReportSourceContractTests.setUp
    post = ReportSourceContractTests.post
    run_submit = ReportSourceContractTests.run_submit

    def refused(self, report_path, code, **extra):
        args = submission_args()
        args["report_path"] = report_path
        with self.subTest(code=code, path=str(report_path)[-40:], **extra):
            self.assertEqual(self.run_submit(args), tools._blocked(code))
        self.assertEqual(self.sent, [])
        self.assertFalse((self.root / "reports").exists())

    def test_report_file_is_stored_byte_identical_and_submitted(self):
        raw = ("# Brief\r\n\r\nUnicode – kept.\n" + REPORT).encode("utf-8")
        args = submission_args()
        args["report_path"] = report_file(raw=raw)
        before = os.stat(args["report_path"])
        result = self.run_submit(args)
        self.assertEqual(result["status"], "persisted", result)
        self.assertEqual((self.directory / "report.md").read_bytes(), raw)
        self.assertEqual(json.loads(self.sent[0])["source_text"].encode(), raw)
        after = os.stat(args["report_path"])
        self.assertEqual(Path(args["report_path"]).read_bytes(), raw)
        self.assertEqual(
            (before.st_ino, before.st_mtime_ns), (after.st_ino, after.st_mtime_ns)
        )

    def test_paths_outside_a_private_mktemp_directory_are_refused(self):
        temp = Path(tempfile.gettempdir())
        nested = Path(report_file()).parent / "tmp.abcdef"
        nested.mkdir(mode=0o700)
        nested.chmod(0o700)
        (nested / "report.md").write_text(REPORT)
        named = temp / "reports.abcdef"
        named.mkdir(mode=0o700)
        named.chmod(0o700)
        (named / "report.md").write_text(REPORT)
        short = temp / "tmp.abc"
        short.mkdir(mode=0o700)
        short.chmod(0o700)
        (short / "report.md").write_text(REPORT)
        good = report_file()
        for path in (
            None,
            12,
            "",
            "report.md",
            "tmp.abcdef/report.md",
            "/etc/hostname",
            str(nested / "report.md"),
            str(named / "report.md"),
            str(short / "report.md"),
            good.replace("report.md", "report.txt"),
            good.replace("report.md", "a" * 65 + ".md"),
            good.replace("report.md", "../report.md"),
            str(Path(good).parent) + "/./report.md",
            good + "\x00",
        ):
            self.refused(path, "report_path_not_allowed")

    def test_hermes_scratch_and_tmpdir_roots_are_accepted(self):
        # Hermes sets TMPDIR of agent shells to HERMES_HOME/cache/scratch, so the
        # agent's mktemp -d lands there although this process may still use /tmp.
        base = Path(tempfile.gettempdir()) / "roots-home"
        scratch = base / "cache" / "scratch" / "tmp.scratch1"
        other = base / "elsewhere" / "tmp.tmpdir01"
        for directory in (scratch, other):
            directory.mkdir(parents=True, mode=0o700)
            directory.chmod(0o700)
            (directory / "report.md").write_text(REPORT)
            (directory / "report.md").chmod(0o600)
        with (
            mock.patch.object(tools, "HERMES_HOME", base),
            mock.patch.dict(os.environ, {"TMPDIR": str(other.parent)}),
        ):
            for directory in (scratch, other):
                self.assertEqual(
                    tools._read_report(str(directory / "report.md")),
                    REPORT.encode("utf-8"),
                )
        self.refused(str(scratch / "report.md"), "report_path_not_allowed")

    def test_secret_like_paths_are_refused(self):
        home = Path(tempfile.gettempdir()) / "tmp.hermeshome"
        (home / "secrets").mkdir(parents=True, mode=0o700)
        home.chmod(0o700)
        secret = home / "secrets" / "research-webhook.secret"
        secret.write_text("synthetic-not-a-secret\n")
        env = home / ".env"
        env.write_text("RESEARCH_WEBHOOK_SECRET=synthetic\n")
        for path in (secret, env, home / "secrets" / "research-webhook.md"):
            self.refused(str(path), "report_path_not_allowed")

    def test_unsafe_directory_or_file_is_refused(self):
        def directory_mode():
            path = report_file()
            os.chmod(Path(path).parent, 0o755)
            return path

        def file_symlink():
            path = Path(report_file())
            target = path.with_name("real.md")
            path.rename(target)
            path.symlink_to(target)
            return str(path)

        def directory_symlink():
            real = Path(report_file()).parent
            link = real.with_name("tmp.linkeddir")
            link.symlink_to(real)
            return str(link / "report.md")

        def hard_link():
            path = Path(report_file())
            os.link(path, path.with_name("second.md"))
            return str(path)

        def fifo():
            directory = Path(report_file()).parent
            os.mkfifo(directory / "pipe.md", 0o600)
            return str(directory / "pipe.md")

        def subdirectory():
            directory = Path(report_file()).parent
            (directory / "dir.md").mkdir(mode=0o700)
            return str(directory / "dir.md")

        for build in (
            directory_mode,
            file_symlink,
            directory_symlink,
            hard_link,
            fifo,
            subdirectory,
        ):
            self.refused(build(), "report_path_not_allowed", case=build.__name__)

    def test_foreign_owner_is_refused(self):
        path = report_file()
        with mock.patch.object(tools.os, "geteuid", return_value=os.geteuid() + 1):
            self.refused(path, "report_path_not_allowed")

    def test_missing_undecodable_and_oversize_files_are_refused(self):
        missing = str(Path(report_file()).with_name("missing.md"))
        self.refused(missing, "report_unreadable")
        absent_dir = str(Path(tempfile.gettempdir()) / "tmp.notthere" / "report.md")
        self.refused(absent_dir, "report_unreadable")
        self.refused(report_file(raw=b"\xff\xfe" + REPORT.encode()), "report_not_utf8")
        self.refused(
            report_file(raw=REPORT.encode() + b"\xed\xa0\x80"), "report_not_utf8"
        )
        oversize = report_file()
        os.truncate(oversize, tools.GATEWAY_MAX_SOURCE_CHARACTERS * 4 + 1)
        self.refused(oversize, "report_too_large")

    def test_growing_file_is_refused_by_the_bounded_read(self):
        path = report_file()
        real_fstat = os.fstat

        def shrunk(descriptor):
            info = real_fstat(descriptor)
            if stat.S_ISREG(info.st_mode):
                values = list(info)
                values[stat.ST_SIZE] = 10
                return os.stat_result(values)
            return info

        with mock.patch.object(tools.os, "fstat", side_effect=shrunk):
            self.refused(path, "report_too_large")

    def test_short_read_is_never_accepted_as_a_truncated_report(self):
        path = report_file()
        real_read = os.read

        def short(descriptor, size):
            return real_read(descriptor, size)[:-1]

        with mock.patch.object(tools.os, "read", side_effect=short):
            self.refused(path, "report_unreadable")

    def test_file_mode_inside_the_private_directory_does_not_matter(self):
        # umask 0002 makes 0664 files; the 0700 directory already keeps others out.
        path = report_file()
        os.chmod(path, 0o666)
        self.assertEqual(tools._read_report(path), REPORT.encode("utf-8"))

    def test_stub_and_pointer_reports_are_too_short(self):
        stub = (
            "# Daily brief\n\nSee https://example.com/news/2-1 for the release; "
            "the full report is in the attached file report.md for review.\n"
        )
        self.assertLess(len(stub.strip()), tools.MIN_REPORT_CHARACTERS)
        self.assertEqual(tools.MIN_REPORT_CHARACTERS, 800)
        self.refused(report_file(stub), "report_too_short")
        padded = "x" * 799 + "\n" * 50
        self.refused(report_file(padded), "report_too_short")

    def test_report_must_name_every_item_source_url(self):
        payload = make_payload()
        second = dict(
            payload["items"][0],
            item_id="item-2",
            source_url="https://example.com/news/other-release",
        )
        payload["items"].append(second)
        args = submission_args(payload)
        result = self.run_submit(args)
        self.assertEqual(result, tools._blocked("report_missing_item"))
        self.assertEqual(self.sent, [])
        self.assertFalse((self.root / "reports").exists())
        # Fixing the file and calling once more stores and submits it.
        Path(args["report_path"]).write_text(
            REPORT + "\n- https://example.com/news/other-release\n"
        )
        fixed = self.run_submit(args)
        # Sent once; the fake receipt counts one candidate, so delivery is uncertain.
        self.assertEqual(len(self.sent), 1, fixed)
        self.assertTrue((self.directory / "report.md").is_file())

    def test_invalid_item_structure_is_left_to_validation(self):
        for items, code in (
            (["not an item"], "invalid_item"),
            ([{"item_id": "x", "source_url": 7}], "missing_title"),
        ):
            args = submission_args()
            args["payload"]["items"] = items
            args["source_receipts"] = ["1" * 32]
            with self.subTest(code=code):
                result = self.run_submit(args)
                self.assertEqual(result["error"], code)
        for payload in ("not a payload", {"schema_version": "1.0", "items": "x"}):
            args = submission_args()
            args["payload"] = payload
            result = self.run_submit(args)
            self.assertFalse(result["ok"])
            self.assertNotEqual(result.get("state"), "BLOCKED")

    def test_no_item_day_needs_a_full_report_too(self):
        args = submission_args()
        args["payload"]["items"], args["source_receipts"] = [], []
        args["report_path"] = report_file("# No items today\n\nNothing new. " * 3)
        self.assertEqual(self.run_submit(args), tools._blocked("report_too_short"))
        args["report_path"] = report_file("# Quiet day\n\n" + "No release. " * 80)
        result = self.run_submit(args)
        self.assertEqual(result["gateway"], "skipped_no_items", result)
        self.assertEqual(result["status"], "stored")

    def test_item_kind_is_set_from_the_job(self):
        payload = make_payload()
        payload["items"].append(
            dict(payload["items"][0], item_id="item-2", kind="infrastructure")
        )
        for item in payload["items"][:1]:
            item["kind"] = "news"  # the devops job sent news, held as KIND_MISMATCH
        args = submission_args(payload)
        del args["payload"]["items"][1]["kind"]  # an omitted kind is set too
        result = self.run_submit(args)
        self.assertEqual(len(self.sent), 1, result)
        kinds = [item["kind"] for item in json.loads(self.sent[0])["items"]]
        self.assertEqual(kinds, ["devops", "devops"])
        self.assertEqual(
            {job: tools._ITEM_KIND[kind] for job, kind in tools._ALLOWED_JOBS.items()},
            {
                "6eabd835f969": "news",
                "25674fbc0bf3": "devops",
                "8d0925bc571d": "business_idea",
            },
        )

    def test_metrics_bytes_are_the_file_size(self):
        raw = ("é" * 10 + "\n" + REPORT).encode("utf-8")
        args = submission_args()
        args["report_path"] = report_file(raw=raw)
        with mock.patch.object(tools, "_update_metrics") as update:
            self.run_submit(args)
        self.assertEqual(update.call_args.args[3], len(raw))
        args["report_path"] = "/etc/hostname"
        with mock.patch.object(tools, "_update_metrics") as update:
            result = self.run_submit(args)
        self.assertEqual(result, tools._blocked("report_path_not_allowed"))
        self.assertIsNone(update.call_args.args[3])


class PrivateRecordCreateTests(unittest.TestCase):
    def test_create_is_exclusive_and_idempotent(self):
        from publisher import private_records

        with tempfile.TemporaryDirectory() as tmp:
            store = private_records.PrivateRecords(Path(tmp) / "store")
            self.addCleanup(store.close)
            with store.lock("k"):
                self.assertTrue(store.create("a", b"one"))
                self.assertFalse(store.create("a", b"one"))
                with self.assertRaises(private_records.RecordError) as raised:
                    store.create("a", b"two")
                self.assertEqual(str(raised.exception), "record_conflict")
                self.assertEqual(store.read("a"), b"one")
            path = Path(tmp) / "store" / "a"
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            self.assertEqual(path.stat().st_nlink, 1)
            self.assertEqual(
                sorted(p.name for p in path.parent.iterdir() if p.name != "a")[:1],
                [".lock-" + hashlib.sha256(b"k").hexdigest()],
            )
            self.assertFalse(
                any(p.name.startswith(".tmp-") for p in path.parent.iterdir())
            )


class ResearchMetricsTests(unittest.TestCase):
    """SPEC-0265 W5: textfile-collector gauges after every submission outcome."""

    URL_UUID_HEX = re.compile(
        r"://|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
        r"|[0-9a-f]{32}",
        re.IGNORECASE,
    )
    SAMPLE = re.compile(r"^(hermes_research_\w+)\{([^}]*)\} (\S+)$")

    def setUp(self):
        ReportSourceContractTests.setUp(self)
        self.metrics = self.root / "metrics"
        self.metrics.mkdir(mode=0o755)
        self.state_dir = self.root / "state"
        self.now = 1_800_000_000.0

    post = ReportSourceContractTests.post
    with_report = ReportSourceContractTests.with_report

    def run_submit(self, args, *, context=None):
        with (
            mock.patch.object(tools, "METRICS_DIR", self.metrics),
            mock.patch.object(tools, "METRICS_STATE_DIR", self.state_dir),
            mock.patch.object(tools.time, "time", return_value=self.now),
        ):
            self.context = context if context is not None else CronRun()
            return ReportSourceContractTests.run_submit(self, args)

    def samples(self):
        text = (self.metrics / "hermes_research.prom").read_text(encoding="utf-8")
        found = {}
        for line in text.splitlines():
            if line.startswith("#"):
                continue
            name, labels, value = self.SAMPLE.fullmatch(line).groups()
            pairs = tuple(
                tuple(pair.split("=", 1)) for pair in labels.split(",") if pair
            )
            found[(name, tuple((k, v.strip('"')) for k, v in pairs))] = float(value)
        return text, found

    def outcome(self, name):
        _, found = self.samples()
        key = (
            "hermes_research_last_outcome_timestamp_seconds",
            (("job_kind", "devops"), ("outcome", name)),
        )
        return found.get(key)

    def success(self):
        _, found = self.samples()
        return found[
            (
                "hermes_research_last_success_timestamp_seconds",
                (("job_kind", "devops"),),
            )
        ]

    def drive_every_outcome(self):
        """One submission per outcome, each at its own clock reading."""
        results = {}
        self.now += 1
        results["submitted"] = self.run_submit(submission_args())
        self.now += 1
        results["conflict"] = self.run_submit(self.with_report(REPORT + "\nlater\n"))
        self.now += 1
        results["blocked"] = self.run_submit(self.with_report(""))
        self.now += 1
        empty = submission_args(make_payload())
        empty["payload"]["items"], empty["source_receipts"] = [], []
        results["stored_no_items"] = self.run_submit(
            empty, context=CronRun(execution_id="no-items-run")
        )
        self.now += 1
        bad = submission_args()
        bad["source_receipts"] = ["not-a-receipt"]
        results["gateway_error"] = self.run_submit(
            bad, context=CronRun(execution_id="gateway-error-run")
        )
        self.now += 1
        with mock.patch.object(tools, "_store_report", side_effect=OSError):
            results["store_failed"] = self.run_submit(
                submission_args(), context=CronRun(execution_id="store-failed-run")
            )
        return results

    def test_every_outcome_writes_its_timestamp(self):
        results = self.drive_every_outcome()
        self.assertEqual(results["submitted"]["status"], "persisted")
        self.assertEqual(results["conflict"]["error"], "report_conflict")
        self.assertEqual(results["blocked"]["error"], "report_required")
        self.assertEqual(results["stored_no_items"]["status"], "stored")
        self.assertEqual(results["gateway_error"]["error"], "invalid_source_receipts")
        self.assertEqual(results["store_failed"]["error"], "report_store_unavailable")
        start = 1_800_000_000.0
        for offset, name in enumerate(
            (
                "submitted",
                "conflict",
                "blocked",
                "stored_no_items",
                "gateway_error",
                "store_failed",
            ),
            start=1,
        ):
            self.assertEqual(self.outcome(name), start + offset, name)
        # The last success is the no-items day, the later failures leave it alone.
        self.assertEqual(self.success(), start + 4)
        _, found = self.samples()
        blocked = {
            dict(labels)["blocked_reason"]: value
            for (name, labels), value in found.items()
            if name == "hermes_research_blocked_total"
        }
        self.assertEqual(
            blocked,
            {"report_required": 1, "report_store_unavailable": 1},
        )
        self.assertEqual(
            found[("hermes_research_last_report_bytes", (("job_kind", "devops"),))],
            len(REPORT.encode("utf-8")),
        )

    def test_values_survive_across_runs_and_kinds(self):
        self.run_submit(self.with_report(""))
        self.now += 10
        self.run_submit(self.with_report(""), context=CronRun(job_id="6eabd835f969"))
        _, found = self.samples()
        self.assertEqual(
            found[
                (
                    "hermes_research_blocked_total",
                    (("job_kind", "devops"), ("blocked_reason", "report_required")),
                )
            ],
            1,
        )
        self.assertEqual(
            found[
                (
                    "hermes_research_last_outcome_timestamp_seconds",
                    (("job_kind", "news"), ("outcome", "blocked")),
                )
            ],
            self.now,
        )
        state = self.root / "state"
        self.assertEqual(stat.S_IMODE(state.stat().st_mode), 0o700)
        for path in state.iterdir():
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600, path.name)

    def gauge(self, name, **labels):
        _, found = self.samples()
        return found.get((name, tuple(labels.items())))

    def test_first_seen_starts_the_success_clock_of_every_kind(self):
        self.run_submit(self.with_report(""))
        installed = self.now
        self.now += 100
        self.run_submit(self.with_report(""), context=CronRun(job_id="6eabd835f969"))
        for kind in ("business_ideas", "devops", "news"):
            self.assertEqual(
                self.gauge(
                    "hermes_research_last_success_timestamp_seconds", job_kind=kind
                ),
                installed,
                kind,
            )
        self.now += 100
        self.run_submit(submission_args())
        self.assertEqual(self.success(), self.now)

    def state_file(self):
        return self.state_dir / "state.json"

    def test_corrupt_state_resets_only_what_is_bad_and_continues(self):
        self.run_submit(self.with_report(""), context=CronRun(job_id="6eabd835f969"))
        news_seen = self.now
        cases = {
            "unreadable": b"not json",
            "not an object": b"[]",
            "nested outcomes": None,
            "count type": None,
        }
        for name, raw in cases.items():
            with self.subTest(case=name):
                if raw is None:
                    state = json.loads(self.state_file().read_bytes())
                    state["devops"] = (
                        {"first_seen": 1, "outcomes": []}
                        if name == "nested outcomes"
                        else {"first_seen": 1, "blocked": {"report_required": "x"}}
                    )
                    raw = json.dumps(state).encode()
                self.state_file().write_bytes(raw)
                self.now += 1
                self.run_submit(self.with_report(""))
                self.assertEqual(self.outcome("blocked"), self.now)
                self.assertEqual(
                    self.gauge(
                        "hermes_research_blocked_total",
                        job_kind="devops",
                        blocked_reason="report_required",
                    ),
                    1,
                )
                news = self.gauge(
                    "hermes_research_last_outcome_timestamp_seconds",
                    job_kind="news",
                    outcome="blocked",
                )
                # Only an unreadable file loses the other kinds.
                if raw in (b"not json", b"[]"):
                    self.assertIsNone(news)
                else:
                    self.assertIsNotNone(news)
                if name == "not an object":
                    self.run_submit(
                        self.with_report(""), context=CronRun(job_id="6eabd835f969")
                    )
                    news_seen = self.now
        self.assertTrue(news_seen)
        # A state file the records layer refuses (mode 0644) is replaced too.
        os.chmod(self.state_file(), 0o644)
        self.now += 1
        self.run_submit(self.with_report(""))
        self.assertEqual(self.outcome("blocked"), self.now)
        self.assertEqual(stat.S_IMODE(self.state_file().stat().st_mode), 0o600)

    def test_non_finite_state_values_are_reset(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                self.assertFalse(tools._valid_entry({"first_seen": value}))
                self.assertFalse(
                    tools._valid_entry({"first_seen": 1.0, "success": value})
                )
                self.assertFalse(
                    tools._valid_entry(
                        {"first_seen": 1.0, "outcomes": {"blocked": value}}
                    )
                )
        self.assertTrue(tools._valid_entry({"first_seen": 1.0, "success": 2}))

    def test_a_busy_metrics_lock_skips_metrics_promptly(self):
        import fcntl
        import time as clock

        self.run_submit(self.with_report(""))
        before = (self.metrics / "hermes_research.prom").read_bytes()
        lock = self.state_dir / (".lock-" + hashlib.sha256(b"metrics").hexdigest())
        holder = os.open(lock, os.O_RDWR)
        self.addCleanup(os.close, holder)
        fcntl.flock(holder, fcntl.LOCK_EX)
        self.now += 1
        started = clock.monotonic()
        result = self.run_submit(self.with_report(""))
        self.assertLess(clock.monotonic() - started, tools.METRICS_LOCK_SECONDS + 1)
        self.assertEqual(result, tools._blocked("report_required"))
        self.assertEqual((self.metrics / "hermes_research.prom").read_bytes(), before)

    def test_textfile_is_replaced_atomically_with_mode_0644(self):
        self.run_submit(self.with_report(""))
        target = self.metrics / "hermes_research.prom"
        first = target.stat().st_ino
        replaced = []
        real_replace = os.replace

        def spy(source, destination, *args, **kwargs):
            replaced.append((Path(source), Path(destination)))
            return real_replace(source, destination, *args, **kwargs)

        with mock.patch.object(tools.os, "replace", side_effect=spy):
            self.run_submit(self.with_report(""))
        (source, destination), *_ = [
            pair for pair in replaced if pair[1].name == "hermes_research.prom"
        ]
        self.assertEqual(source.parent, self.metrics)
        self.assertEqual(destination, target)
        self.assertNotEqual(target.stat().st_ino, first)
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o644)
        self.assertEqual([p.name for p in self.metrics.iterdir()], [target.name])

    def test_missing_textfile_directory_is_skipped_not_created(self):
        self.metrics.rmdir()
        result = self.run_submit(submission_args())
        self.assertTrue(result["ok"], result)
        self.assertFalse(self.metrics.exists())

    def test_a_metrics_failure_never_changes_the_tool_result(self):
        failures = (
            mock.patch.object(tools, "_write_metrics", side_effect=RuntimeError),
            mock.patch.object(tools, "_update_metrics", side_effect=RuntimeError),
            mock.patch.object(tools.tempfile, "mkstemp", side_effect=PermissionError),
            mock.patch.object(self, "state_dir", Path("/proc/forbidden")),
        )
        for index, failure in enumerate(failures):
            with self.subTest(failure=index), failure:
                self.assertEqual(
                    self.run_submit(self.with_report("")),
                    tools._blocked("report_required"),
                )
                result = self.run_submit(
                    submission_args(), context=CronRun(execution_id=f"run-{index}")
                )
                self.assertEqual(result["status"], "persisted", result)
        self.assertEqual(len(self.sent), len(failures))

    def test_labels_come_only_from_fixed_enums(self):
        self.drive_every_outcome()
        self.run_submit(self.with_report(""), context=CronRun(job_id="8d0925bc571d"))
        text, found = self.samples()
        enums = {
            "job_kind": set(tools._ALLOWED_JOBS.values()),
            "outcome": set(tools.METRIC_OUTCOMES),
            "blocked_reason": set(tools.METRIC_BLOCKED_REASONS),
        }
        self.assertEqual(
            set(tools.METRIC_OUTCOMES),
            {
                "submitted",
                "stored_no_items",
                "gateway_error",
                "blocked",
                "conflict",
                "store_failed",
            },
        )
        self.assertTrue(found)
        for (_name, labels), _value in found.items():
            for key, value in labels:
                self.assertIn(value, enums[key], key)
                self.assertIsNone(self.URL_UUID_HEX.search(value), value)
        self.assertIsNone(self.URL_UUID_HEX.search(text))
        for identifier in ("25674fbc0bf3", "0123456789abcdef", "no-items-run"):
            self.assertNotIn(identifier, text)
        names = {
            line.split()[2] for line in text.splitlines() if line.startswith("# TYPE")
        }
        self.assertEqual(names, {name for name, _ in found})

    def test_alert_rules_pass_their_promtool_cases(self):
        import subprocess

        image = (
            "sha256:5ce7540c3c00ef4ab0c9d2c995c6a5b9c421f44b4a115d97a2c7af3b1c21cbb0"
        )
        try:
            present = (
                subprocess.run(
                    ["docker", "image", "inspect", image],
                    capture_output=True,
                    check=False,
                ).returncode
                == 0
            )
        except OSError:
            present = False
        if not present:
            self.skipTest("cached promtool image is not available")
        rules = (
            WORKLOAD.parents[3]
            / "06-observability/prometheus/config/alert_rules/alert_rules.local.infra.yml"
        )
        cases = WORKLOAD / "tests/fixtures/hermes-research-alerts.test.yml"
        result = subprocess.run(
            [
                "docker", "run", "--rm", "--network", "none", "--read-only",
                "--tmpfs", "/tmp:size=32m", "--entrypoint", "/bin/promtool",
                "--mount", f"type=bind,src={rules},dst=/rules/infra.yml,readonly",
                "--mount", f"type=bind,src={cases},dst=/p/cases.yml,readonly",
                "--workdir", "/p", image, "test", "rules", "/p/cases.yml",
            ],
            capture_output=True,
            text=True,
            check=False,
        )  # fmt: skip
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

        # The plugin's own text must also lint as Prometheus exposition format.
        self.drive_every_outcome()
        lint = subprocess.run(
            [
                "docker", "run", "-i", "--rm", "--network", "none", "--read-only",
                "--entrypoint", "/bin/promtool", image, "check", "metrics",
            ],
            input=(self.metrics / "hermes_research.prom").read_text(encoding="utf-8"),
            capture_output=True,
            text=True,
            check=False,
        )  # fmt: skip
        self.assertEqual(0, lint.returncode, lint.stdout + lint.stderr)
